from datetime import datetime, timezone
from malak.security.clock import Clock
from malak.security.context_validator import SecurityContextValidator

import pytest

from malak.security import (
    AuthorizationAuditOutcome,
    AuthorizationDecision,
    AuthorizationDeniedError,
    AuthorizationEnforcementError,
    AuthorizationOperationBinding,
    AuthorizationRequest,
    HumanConfirmationEvidence,
    InMemoryAuthorizationAuditStore,
    PermissionScope,
    PolicyEffect,
    PolicyRule,
    SecurityContext,
    StaticPolicyDecisionPoint,
    StrictPolicyEnforcementPoint,
)


class RecordingOperation:
    def __init__(
        self,
        result: object = "executed",
        error: Exception | None = None,
        authorization_binding: AuthorizationOperationBinding | None = None,
        required_permission: PermissionScope | None = None,
    ) -> None:
        self.result = result
        self.error = error
        self.authorization_binding = authorization_binding
        self.required_permission = required_permission
        self.calls = 0

    def execute(self) -> object:
        self.calls += 1

        if self.error is not None:
            raise self.error

        return self.result


class RecordingPolicyDecisionPoint:
    def __init__(
        self,
        decision: object,
        error: Exception | None = None,
    ) -> None:
        self.decision = decision
        self.error = error
        self.calls: list[
            tuple[
                AuthorizationRequest,
                HumanConfirmationEvidence | None,
            ]
        ] = []

    def decide(
        self,
        request: AuthorizationRequest,
        confirmation: HumanConfirmationEvidence | None = None,
    ) -> object:
        self.calls.append((request, confirmation))

        if self.error is not None:
            raise self.error

        return self.decision


class FailingAuditSink:
    def __init__(self, fail_on_write: int = 1) -> None:
        self.fail_on_write = fail_on_write
        self.calls = 0
        self.records: list[object] = []

    def write(self, record: object) -> None:
        self.calls += 1
        self.records.append(record)

        if self.calls == self.fail_on_write:
            raise RuntimeError("audit unavailable")


def make_pep(
    policy_decision_point: object,
    protected_operation: object,
    authorization_audit_sink: object | None = None,
) -> StrictPolicyEnforcementPoint[object]:
    sink = (
        authorization_audit_sink
        if authorization_audit_sink is not None
        else InMemoryAuthorizationAuditStore()
    )
    return StrictPolicyEnforcementPoint(
        policy_decision_point,
        protected_operation,
        sink,
    )


class AcceptingConfirmationVerifier:
    def verify(
        self,
        request: AuthorizationRequest,
        evidence: HumanConfirmationEvidence,
    ) -> bool:
        return True


class FixedClock:
    def __init__(self, current_time: datetime) -> None:
        self._current_time = current_time

    def now(self) -> datetime:
        return self._current_time


def make_context_validator() -> SecurityContextValidator:
    return SecurityContextValidator(
        FixedClock(
            datetime(2026, 8, 15, 18, 15, tzinfo=timezone.utc)
        )
    )


def make_binding(digest_character: str = "a") -> AuthorizationOperationBinding:
    return AuthorizationOperationBinding(
        namespace="memory.episodic.persistence",
        binding_version="v1",
        digest_algorithm="sha256",
        digest_hex=digest_character * 64,
    )


def make_request(
    *,
    request_id: str = "request-001",
    authenticated: bool = True,
    created_at: datetime | None = None,
    operation_binding: AuthorizationOperationBinding | None = None,
    permission: PermissionScope | None = None,
) -> AuthorizationRequest:
    return AuthorizationRequest(
        context=SecurityContext(
            context_id="context-001",
            session_id="session-001",
            subject_id="aranwill",
            authenticated=authenticated,
            issued_at=datetime(2026, 8, 15, 18, 0, tzinfo=timezone.utc),
            expires_at=datetime(2026, 8, 15, 18, 30, tzinfo=timezone.utc),
        ),
        permission=(
            permission
            if permission is not None
            else PermissionScope(
                resource="system",
                action="update",
            )
        ),
        request_id=request_id,
        created_at=(
            created_at
            if created_at is not None
            else datetime(2026, 8, 15, 18, 10, tzinfo=timezone.utc)
        ),
        operation_binding=operation_binding,
    )


def make_decision(
    *,
    request_id: str = "request-001",
    allowed: bool = True,
    reason: str = "policy_allowed",
    operation_binding: AuthorizationOperationBinding | None = None,
) -> AuthorizationDecision:
    return AuthorizationDecision(
        request_id=request_id,
        allowed=allowed,
        reason=reason,
        operation_binding=operation_binding,
    )


def make_confirmation(
    *,
    operation_binding: AuthorizationOperationBinding | None = None,
) -> HumanConfirmationEvidence:
    return HumanConfirmationEvidence(
        confirmation_id="confirmation-001",
        original_request_id="request-original",
        new_request_id="request-001",
        subject_id="aranwill",
        permission=PermissionScope(
            resource="system",
            action="update",
        ),
        confirmed_by="owner",
        confirmed_at=datetime(2026, 7, 26, tzinfo=timezone.utc),
        operation_binding=operation_binding,
    )


def test_allowed_decision_executes_operation_exactly_once() -> None:
    request = make_request()
    pdp = RecordingPolicyDecisionPoint(make_decision())
    operation = RecordingOperation(result={"status": "ok"})
    pep = make_pep(pdp, operation)

    result = pep.execute(request)

    assert result == {"status": "ok"}
    assert pdp.calls == [(request, None)]
    assert operation.calls == 1


def test_bound_operation_executes_only_with_exact_binding_chain() -> None:
    binding = make_binding()
    request = make_request(operation_binding=binding)
    decision = make_decision(operation_binding=binding)
    pdp = RecordingPolicyDecisionPoint(decision)
    operation = RecordingOperation(
        authorization_binding=binding,
        required_permission=request.permission,
    )
    store = InMemoryAuthorizationAuditStore()
    pep = make_pep(pdp, operation, store)

    assert pep.execute(request) == "executed"

    assert pdp.calls == [(request, None)]
    assert operation.calls == 1
    assert len(store.records) == 1
    assert store.records[0].operation_binding == binding
    assert store.records[0].protected_operation_binding == binding
    assert store.records[0].outcome is AuthorizationAuditOutcome.ALLOWED


def test_bound_request_with_unbound_operation_is_blocked_before_pdp() -> None:
    binding = make_binding()
    request = make_request(operation_binding=binding)
    pdp = RecordingPolicyDecisionPoint(make_decision(operation_binding=binding))
    operation = RecordingOperation()
    store = InMemoryAuthorizationAuditStore()
    pep = make_pep(pdp, operation, store)

    with pytest.raises(AuthorizationEnforcementError, match="binding presence differ"):
        pep.execute(request)

    assert pdp.calls == []
    assert operation.calls == 0
    assert store.records[0].reason_code == "request_operation_binding_presence_mismatch"
    assert store.records[0].operation_binding == binding
    assert store.records[0].protected_operation_binding is None


def test_unbound_request_with_bound_operation_is_blocked_before_pdp() -> None:
    binding = make_binding()
    request = make_request()
    pdp = RecordingPolicyDecisionPoint(make_decision())
    operation = RecordingOperation(
        authorization_binding=binding,
        required_permission=request.permission,
    )
    store = InMemoryAuthorizationAuditStore()
    pep = make_pep(pdp, operation, store)

    with pytest.raises(AuthorizationEnforcementError, match="binding presence differ"):
        pep.execute(request)

    assert pdp.calls == []
    assert operation.calls == 0
    assert store.records[0].reason_code == "request_operation_binding_presence_mismatch"
    assert store.records[0].operation_binding is None
    assert store.records[0].protected_operation_binding == binding


def test_mismatched_request_and_operation_binding_is_blocked_before_pdp() -> None:
    request_binding = make_binding("a")
    operation_binding = make_binding("b")
    request = make_request(operation_binding=request_binding)
    pdp = RecordingPolicyDecisionPoint(
        make_decision(operation_binding=request_binding)
    )
    operation = RecordingOperation(
        authorization_binding=operation_binding,
        required_permission=request.permission,
    )
    store = InMemoryAuthorizationAuditStore()
    pep = make_pep(pdp, operation, store)

    with pytest.raises(AuthorizationEnforcementError, match="does not match protected operation"):
        pep.execute(request)

    assert pdp.calls == []
    assert operation.calls == 0
    assert store.records[0].reason_code == "request_operation_binding_mismatch"
    assert store.records[0].operation_binding == request_binding
    assert store.records[0].protected_operation_binding == operation_binding


def test_mismatched_decision_binding_blocks_bound_operation() -> None:
    request_binding = make_binding("a")
    decision_binding = make_binding("b")
    request = make_request(operation_binding=request_binding)
    pdp = RecordingPolicyDecisionPoint(
        make_decision(operation_binding=decision_binding)
    )
    operation = RecordingOperation(
        authorization_binding=request_binding,
        required_permission=request.permission,
    )
    store = InMemoryAuthorizationAuditStore()
    pep = make_pep(pdp, operation, store)

    with pytest.raises(AuthorizationEnforcementError, match="decision operation binding"):
        pep.execute(request)

    assert pdp.calls == [(request, None)]
    assert operation.calls == 0
    assert store.records[0].outcome is AuthorizationAuditOutcome.INVALID_DECISION
    assert store.records[0].reason_code == "decision_operation_binding_mismatch"


def test_temporally_incoherent_request_is_blocked_before_pdp() -> None:
    request = make_request(
        created_at=datetime(2026, 8, 15, 18, 30, tzinfo=timezone.utc)
    )
    pdp = RecordingPolicyDecisionPoint(make_decision())
    operation = RecordingOperation()
    store = InMemoryAuthorizationAuditStore()
    pep = make_pep(pdp, operation, store)

    with pytest.raises(AuthorizationEnforcementError, match="outside security context lifecycle"):
        pep.execute(request)

    assert pdp.calls == []
    assert operation.calls == 0
    assert store.records[0].outcome is AuthorizationAuditOutcome.ENFORCEMENT_FAILED
    assert store.records[0].reason_code == "authorization_request_time_invalid"


@pytest.mark.parametrize(
    "decision_reason",
    [
        "unauthenticated_subject",
        "no_applicable_policy",
        "policy_denied",
        "human_confirmation_required",
        "invalid_human_confirmation",
    ],
)
def test_denied_decision_never_executes_operation(
    decision_reason: str,
) -> None:
    operation = RecordingOperation()
    pep = make_pep(
        RecordingPolicyDecisionPoint(
            make_decision(
                allowed=False,
                reason=decision_reason,
            )
        ),
        operation,
    )

    with pytest.raises(AuthorizationDeniedError) as error:
        pep.execute(make_request())

    assert error.value.request_id == "request-001"
    assert error.value.reason == decision_reason
    assert operation.calls == 0


def test_pep_obtains_decision_internally() -> None:
    pep = make_pep(
        RecordingPolicyDecisionPoint(make_decision()),
        RecordingOperation(),
    )

    with pytest.raises(TypeError):
        pep.execute(
            make_request(),
            decision=make_decision(),
        )


def test_confirmation_is_forwarded_to_policy_decision_point() -> None:
    request = make_request()
    confirmation = make_confirmation()
    permission = request.permission
    pdp = StaticPolicyDecisionPoint(
        [
            PolicyRule(
                subject_id=request.context.subject_id,
                permission=permission,
                effect=PolicyEffect.REQUIRE_HUMAN_CONFIRMATION,
            )
        ],
        context_validator=make_context_validator(),
        confirmation_verifier=AcceptingConfirmationVerifier(),
    )
    operation = RecordingOperation()
    pep = make_pep(pdp, operation)

    assert pep.execute(request, confirmation) == "executed"
    assert operation.calls == 1


def test_missing_confirmation_blocks_operation() -> None:
    request = make_request()
    pdp = StaticPolicyDecisionPoint(
        [
            PolicyRule(
                subject_id=request.context.subject_id,
                permission=request.permission,
                effect=PolicyEffect.REQUIRE_HUMAN_CONFIRMATION,
            )
        ],
        context_validator=make_context_validator(),
        confirmation_verifier=AcceptingConfirmationVerifier(),
    )
    operation = RecordingOperation()
    pep = make_pep(pdp, operation)

    with pytest.raises(AuthorizationDeniedError) as error:
        pep.execute(request)

    assert error.value.reason == "human_confirmation_required"
    assert operation.calls == 0


def test_mismatched_request_id_blocks_operation() -> None:
    operation = RecordingOperation()
    pep = make_pep(
        RecordingPolicyDecisionPoint(
            make_decision(request_id="another-request")
        ),
        operation,
    )

    with pytest.raises(
        AuthorizationEnforcementError,
        match="does not match request",
    ):
        pep.execute(make_request())

    assert operation.calls == 0


@pytest.mark.parametrize(
    "invalid_decision",
    [
        None,
        True,
        object(),
        {
            "request_id": "request-001",
            "allowed": True,
            "reason": "policy_allowed",
        },
    ],
)
def test_invalid_decision_type_blocks_operation(
    invalid_decision: object,
) -> None:
    operation = RecordingOperation()
    pep = make_pep(
        RecordingPolicyDecisionPoint(invalid_decision),
        operation,
    )

    with pytest.raises(
        AuthorizationEnforcementError,
        match="invalid decision",
    ):
        pep.execute(make_request())

    assert operation.calls == 0


def test_policy_decision_failure_is_fail_closed() -> None:
    operation = RecordingOperation()
    pep = make_pep(
        RecordingPolicyDecisionPoint(
            make_decision(),
            error=RuntimeError("PDP unavailable"),
        ),
        operation,
    )

    with pytest.raises(
        AuthorizationEnforcementError,
        match="policy decision failed",
    ) as error:
        pep.execute(make_request())

    assert isinstance(error.value.__cause__, RuntimeError)
    assert operation.calls == 0


def test_invalid_request_is_fail_closed() -> None:
    operation = RecordingOperation()
    pep = make_pep(
        RecordingPolicyDecisionPoint(make_decision()),
        operation,
    )

    with pytest.raises(
        AuthorizationEnforcementError,
        match="AuthorizationRequest",
    ):
        pep.execute("request")

    assert operation.calls == 0


def test_operation_failure_is_propagated_without_retry() -> None:
    operation_error = RuntimeError("operation failed")
    operation = RecordingOperation(error=operation_error)
    pep = make_pep(
        RecordingPolicyDecisionPoint(make_decision()),
        operation,
    )

    with pytest.raises(RuntimeError) as error:
        pep.execute(make_request())

    assert error.value is operation_error
    assert operation.calls == 1


def test_policy_decision_point_must_implement_decide() -> None:
    with pytest.raises(TypeError, match="must implement decide"):
        StrictPolicyEnforcementPoint(
            object(),
            RecordingOperation(),
            InMemoryAuthorizationAuditStore(),
        )


def test_protected_operation_must_implement_execute() -> None:
    with pytest.raises(TypeError, match="must implement execute"):
        StrictPolicyEnforcementPoint(
            RecordingPolicyDecisionPoint(make_decision()),
            object(),
            InMemoryAuthorizationAuditStore(),
        )


def test_audit_sink_must_implement_write() -> None:
    with pytest.raises(TypeError, match="must implement write"):
        StrictPolicyEnforcementPoint(
            RecordingPolicyDecisionPoint(make_decision()),
            RecordingOperation(),
            object(),
        )


def test_allowed_decision_is_audited_before_operation() -> None:
    request = make_request()
    store = InMemoryAuthorizationAuditStore()
    events: list[str] = []

    class OrderedOperation:
        def execute(self) -> str:
            events.append("operation")
            assert len(store.records) == 1
            return "executed"

    class OrderedSink:
        def write(self, record: object) -> None:
            events.append("audit")
            store.write(record)

    pep = make_pep(
        RecordingPolicyDecisionPoint(make_decision()),
        OrderedOperation(),
        OrderedSink(),
    )

    assert pep.execute(request) == "executed"
    assert events == ["audit", "operation"]
    assert len(store.records) == 1
    assert store.records[0].outcome is AuthorizationAuditOutcome.ALLOWED
    assert store.records[0].reason_code == "policy_allowed"
    assert store.records[0].request_id == request.request_id
    assert store.records[0].subject_id == request.context.subject_id
    assert store.records[0].resource == request.permission.resource
    assert store.records[0].action == request.permission.action


def test_allowed_operation_is_blocked_when_audit_fails() -> None:
    operation = RecordingOperation()
    pep = make_pep(
        RecordingPolicyDecisionPoint(make_decision()),
        operation,
        FailingAuditSink(),
    )

    with pytest.raises(
        AuthorizationEnforcementError,
        match="failed before protected operation",
    ) as error:
        pep.execute(make_request())

    assert isinstance(error.value.__cause__, RuntimeError)
    assert operation.calls == 0


def test_denied_decision_is_audited_before_denial_error() -> None:
    store = InMemoryAuthorizationAuditStore()
    operation = RecordingOperation()
    pep = make_pep(
        RecordingPolicyDecisionPoint(
            make_decision(
                allowed=False,
                reason="policy_denied",
            )
        ),
        operation,
        store,
    )

    with pytest.raises(AuthorizationDeniedError):
        pep.execute(make_request())

    assert operation.calls == 0
    assert len(store.records) == 1
    assert store.records[0].outcome is AuthorizationAuditOutcome.DENIED
    assert store.records[0].reason_code == "policy_denied"


def test_denied_operation_remains_blocked_when_audit_fails() -> None:
    operation = RecordingOperation()
    pep = make_pep(
        RecordingPolicyDecisionPoint(
            make_decision(
                allowed=False,
                reason="policy_denied",
            )
        ),
        operation,
        FailingAuditSink(),
    )

    with pytest.raises(
        AuthorizationEnforcementError,
        match="failed for denied decision",
    ):
        pep.execute(make_request())

    assert operation.calls == 0


def test_policy_decision_failure_is_audited() -> None:
    store = InMemoryAuthorizationAuditStore()
    operation = RecordingOperation()
    pep = make_pep(
        RecordingPolicyDecisionPoint(
            make_decision(),
            error=RuntimeError("PDP unavailable"),
        ),
        operation,
        store,
    )

    with pytest.raises(
        AuthorizationEnforcementError,
        match="policy decision failed",
    ):
        pep.execute(make_request())

    assert operation.calls == 0
    assert len(store.records) == 1
    assert (
        store.records[0].outcome
        is AuthorizationAuditOutcome.DECISION_FAILED
    )
    assert store.records[0].reason_code == "policy_decision_failed"


def test_policy_decision_and_audit_failure_remain_fail_closed() -> None:
    operation = RecordingOperation()
    pep = make_pep(
        RecordingPolicyDecisionPoint(
            make_decision(),
            error=RuntimeError("PDP unavailable"),
        ),
        operation,
        FailingAuditSink(),
    )

    with pytest.raises(
        AuthorizationEnforcementError,
        match="audit failed after policy decision failure",
    ) as error:
        pep.execute(make_request())

    assert isinstance(error.value.__cause__, RuntimeError)
    assert str(error.value.__cause__) == "audit unavailable"
    assert isinstance(error.value.__cause__.__context__, RuntimeError)
    assert str(error.value.__cause__.__context__) == "PDP unavailable"
    assert operation.calls == 0


@pytest.mark.parametrize(
    "decision, reason_code",
    [
        (None, "invalid_decision_type"),
        (
            make_decision(request_id="another-request"),
            "decision_request_mismatch",
        ),
    ],
)
def test_invalid_decision_is_audited(
    decision: object,
    reason_code: str,
) -> None:
    store = InMemoryAuthorizationAuditStore()
    operation = RecordingOperation()
    pep = make_pep(
        RecordingPolicyDecisionPoint(decision),
        operation,
        store,
    )

    with pytest.raises(AuthorizationEnforcementError):
        pep.execute(make_request())

    assert operation.calls == 0
    assert len(store.records) == 1
    assert (
        store.records[0].outcome
        is AuthorizationAuditOutcome.INVALID_DECISION
    )
    assert store.records[0].reason_code == reason_code
    assert store.records[0].request_id == "request-001"


def test_operation_failure_records_terminal_audit_without_retry() -> None:
    store = InMemoryAuthorizationAuditStore()
    operation_error = RuntimeError("operation failed")
    operation = RecordingOperation(error=operation_error)
    pep = make_pep(
        RecordingPolicyDecisionPoint(make_decision()),
        operation,
        store,
    )

    with pytest.raises(RuntimeError) as error:
        pep.execute(make_request())

    assert error.value is operation_error
    assert operation.calls == 1
    assert [
        record.outcome for record in store.records
    ] == [
        AuthorizationAuditOutcome.ALLOWED,
        AuthorizationAuditOutcome.OPERATION_FAILED,
    ]
    assert store.records[1].reason_code == "protected_operation_failed"


def test_operation_error_remains_primary_when_terminal_audit_fails() -> None:
    operation_error = RuntimeError("operation failed")
    audit_sink = FailingAuditSink(fail_on_write=2)
    operation = RecordingOperation(error=operation_error)
    pep = make_pep(
        RecordingPolicyDecisionPoint(make_decision()),
        operation,
        audit_sink,
    )

    with pytest.raises(RuntimeError) as error:
        pep.execute(make_request())

    assert error.value is operation_error
    assert isinstance(error.value.__cause__, RuntimeError)
    assert str(error.value.__cause__) == "audit unavailable"
    assert operation.calls == 1
    assert audit_sink.calls == 2


def test_invalid_request_is_not_fabricated_into_audit_record() -> None:
    store = InMemoryAuthorizationAuditStore()
    operation = RecordingOperation()
    pep = make_pep(
        RecordingPolicyDecisionPoint(make_decision()),
        operation,
        store,
    )

    with pytest.raises(AuthorizationEnforcementError):
        pep.execute("request")

    assert store.records == ()
    assert operation.calls == 0


def test_permission_mismatch_is_blocked_before_pdp_and_operation() -> None:
    requested_permission = PermissionScope(
        resource="memory.episodic",
        action="read",
    )
    required_permission = PermissionScope(
        resource="memory.episodic",
        action="persist",
    )
    request = make_request(permission=requested_permission)
    pdp = RecordingPolicyDecisionPoint(make_decision())
    operation = RecordingOperation(required_permission=required_permission)
    store = InMemoryAuthorizationAuditStore()
    pep = make_pep(pdp, operation, store)

    with pytest.raises(AuthorizationEnforcementError):
        pep.execute(request)

    assert pdp.calls == []
    assert operation.calls == 0
    assert len(store.records) == 1
    assert store.records[0].outcome is AuthorizationAuditOutcome.ENFORCEMENT_FAILED
    assert store.records[0].reason_code == "request_operation_permission_mismatch"


def test_bound_operation_without_required_permission_is_blocked_before_pdp() -> None:
    binding = make_binding()
    request = make_request(operation_binding=binding)
    pdp = RecordingPolicyDecisionPoint(
        make_decision(operation_binding=binding)
    )
    operation = RecordingOperation(authorization_binding=binding)
    store = InMemoryAuthorizationAuditStore()
    pep = make_pep(pdp, operation, store)

    with pytest.raises(AuthorizationEnforcementError):
        pep.execute(request)

    assert pdp.calls == []
    assert operation.calls == 0
    assert len(store.records) == 1
    assert store.records[0].outcome is AuthorizationAuditOutcome.ENFORCEMENT_FAILED
    assert store.records[0].reason_code == "bound_operation_permission_missing"


def test_invalid_required_permission_type_is_blocked_before_pdp() -> None:
    request = make_request()
    pdp = RecordingPolicyDecisionPoint(make_decision())
    operation = RecordingOperation()
    operation.required_permission = "memory.episodic:persist"
    store = InMemoryAuthorizationAuditStore()
    pep = make_pep(pdp, operation, store)

    with pytest.raises(AuthorizationEnforcementError):
        pep.execute(request)

    assert pdp.calls == []
    assert operation.calls == 0
    assert len(store.records) == 1
    assert store.records[0].reason_code == "invalid_protected_operation_permission"


def test_required_permission_access_failure_is_fail_closed_before_pdp() -> None:
    request = make_request()
    pdp = RecordingPolicyDecisionPoint(make_decision())
    store = InMemoryAuthorizationAuditStore()

    class PermissionAccessFailingOperation:
        calls = 0
        authorization_binding = None

        @property
        def required_permission(self) -> PermissionScope:
            raise RuntimeError("permission unavailable")

        def execute(self) -> str:
            self.calls += 1
            return "executed"

    operation = PermissionAccessFailingOperation()
    pep = make_pep(pdp, operation, store)

    with pytest.raises(AuthorizationEnforcementError):
        pep.execute(request)

    assert pdp.calls == []
    assert operation.calls == 0
    assert len(store.records) == 1
    assert store.records[0].reason_code == "protected_operation_permission_unavailable"


def test_permission_mismatch_remains_fail_closed_when_audit_fails() -> None:
    requested_permission = PermissionScope(
        resource="memory.episodic",
        action="read",
    )
    required_permission = PermissionScope(
        resource="memory.episodic",
        action="persist",
    )
    request = make_request(permission=requested_permission)
    pdp = RecordingPolicyDecisionPoint(make_decision())
    operation = RecordingOperation(required_permission=required_permission)
    pep = make_pep(pdp, operation, FailingAuditSink())

    with pytest.raises(AuthorizationEnforcementError):
        pep.execute(request)

    assert pdp.calls == []
    assert operation.calls == 0


def test_matching_required_permission_still_respects_denied_pdp_decision() -> None:
    request = make_request()
    pdp = RecordingPolicyDecisionPoint(
        make_decision(allowed=False, reason="policy_denied")
    )
    operation = RecordingOperation(required_permission=request.permission)
    pep = make_pep(pdp, operation)

    with pytest.raises(AuthorizationDeniedError):
        pep.execute(request)

    assert pdp.calls == [(request, None)]
    assert operation.calls == 0


def test_required_permission_is_read_once_per_pep_invocation() -> None:
    request = make_request()
    pdp = RecordingPolicyDecisionPoint(make_decision())

    class CountingPermissionOperation:
        def __init__(self) -> None:
            self.permission_reads = 0
            self.calls = 0
            self.authorization_binding = None

        @property
        def required_permission(self) -> PermissionScope:
            self.permission_reads += 1
            return request.permission

        def execute(self) -> str:
            self.calls += 1
            return "executed"

    operation = CountingPermissionOperation()
    pep = make_pep(pdp, operation)

    assert pep.execute(request) == "executed"
    assert operation.permission_reads == 1
    assert operation.calls == 1
