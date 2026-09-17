from importlib import import_module
from pathlib import Path
from datetime import datetime, timedelta, timezone
import builtins

import pytest

from malak.memory.candidate_content_identity import (
    EpisodicCandidateContentIdentity,
)
from malak.memory.episodic_persistence_readiness import (
    OPERATION_BINDING_DIGEST_ALGORITHM,
    OPERATION_BINDING_NAMESPACE,
    OPERATION_BINDING_VERSION,
    EpisodicPersistenceIntent,
    EpisodicPersistenceReadinessOutcome,
    EpisodicPersistenceReadinessReason,
    EpisodicPersistenceReadinessResult,
)
from malak.security.contracts import (
    AuthorizationOperationBinding,
    AuthorizationRequest,
    PermissionScope,
    SecurityContext,
)


NOW = datetime(2026, 9, 17, 20, 0, tzinfo=timezone.utc)


def _composer():
    module = import_module(
        "malak.memory.episodic_persistence_authorization"
    )
    return module.compose_episodic_persistence_authorization_request


def _identity() -> EpisodicCandidateContentIdentity:
    return EpisodicCandidateContentIdentity(
        candidate_id="candidate-1",
        digest_algorithm="sha256",
        digest_hex="cd" * 32,
        canonicalization_version="episodic-memory-candidate-json/v1",
        policy_version="episodic-candidate-content-identity/v1",
    )


def _intent(
    identity: EpisodicCandidateContentIdentity | None = None,
) -> EpisodicPersistenceIntent:
    actual_identity = identity or _identity()
    return EpisodicPersistenceIntent(
        candidate_id=actual_identity.candidate_id,
        candidate_content_identity=actual_identity,
        subject_scope="owner",
        domain="personal",
        purpose="continuity",
        created_at=NOW - timedelta(minutes=2),
    )


def _binding() -> AuthorizationOperationBinding:
    return AuthorizationOperationBinding(
        namespace=OPERATION_BINDING_NAMESPACE,
        binding_version=OPERATION_BINDING_VERSION,
        digest_algorithm=OPERATION_BINDING_DIGEST_ALGORITHM,
        digest_hex="ab" * 32,
    )


def _readiness(
    outcome: EpisodicPersistenceReadinessOutcome = (
        EpisodicPersistenceReadinessOutcome.READY
    ),
) -> EpisodicPersistenceReadinessResult:
    identity = _identity()
    intent = _intent(identity)

    if outcome is EpisodicPersistenceReadinessOutcome.READY:
        reason = EpisodicPersistenceReadinessReason.READY
        binding = _binding()
    elif outcome is EpisodicPersistenceReadinessOutcome.HOLD:
        reason = EpisodicPersistenceReadinessReason.STALE_CONSUMPTION
        binding = None
    else:
        reason = EpisodicPersistenceReadinessReason.CONSUMPTION_BLOCKED
        binding = None

    return EpisodicPersistenceReadinessResult(
        candidate_id=identity.candidate_id,
        candidate_content_identity=identity,
        intent=intent,
        outcome=outcome,
        reason_code=reason,
        evaluated_at=NOW - timedelta(minutes=1),
        authorization_operation_binding=binding,
    )


def _security_context() -> SecurityContext:
    return SecurityContext(
        context_id="context-1",
        session_id="session-1",
        subject_id="owner-1",
        authenticated=True,
        issued_at=NOW - timedelta(minutes=10),
        expires_at=NOW + timedelta(minutes=10),
    )


def test_g2pb_red_c01_ready_composes_authorization_request() -> None:
    created_at = NOW
    request = _composer()(_readiness(), _security_context(), created_at)

    assert isinstance(request, AuthorizationRequest)
    assert request.created_at == created_at


def test_g2pb_red_c02_permission_is_exact_persistence_scope() -> None:
    request = _composer()(_readiness(), _security_context(), NOW)

    assert request.permission == PermissionScope(
        resource="memory.episodic",
        action="persist",
    )


def test_g2pb_red_c03_caller_cannot_select_alternative_permission() -> None:
    compose = _composer()

    with pytest.raises(TypeError):
        compose(
            _readiness(),
            _security_context(),
            NOW,
            permission=PermissionScope("memory.episodic", "delete"),
        )


def test_g2pb_red_c04_operation_binding_is_preserved_exactly() -> None:
    readiness = _readiness()

    request = _composer()(readiness, _security_context(), NOW)

    assert request.operation_binding is readiness.authorization_operation_binding


def test_g2pb_red_c05_security_context_is_preserved_exactly() -> None:
    context = _security_context()

    request = _composer()(_readiness(), context, NOW)

    assert request.context is context


def test_g2pb_red_c06_hold_readiness_fails_closed() -> None:
    compose = _composer()

    with pytest.raises(ValueError):
        compose(
            _readiness(EpisodicPersistenceReadinessOutcome.HOLD),
            _security_context(),
            NOW,
        )


def test_g2pb_red_c07_denied_readiness_fails_closed() -> None:
    compose = _composer()

    with pytest.raises(ValueError):
        compose(
            _readiness(EpisodicPersistenceReadinessOutcome.DENIED),
            _security_context(),
            NOW,
        )


def test_g2pb_red_c08_invalid_readiness_type_fails_closed() -> None:
    compose = _composer()

    with pytest.raises(TypeError):
        compose(object(), _security_context(), NOW)


def test_g2pb_red_c09_invalid_security_context_type_fails_closed() -> None:
    compose = _composer()

    with pytest.raises(TypeError):
        compose(_readiness(), object(), NOW)


def test_g2pb_red_c10_naive_created_at_fails_closed() -> None:
    compose = _composer()

    with pytest.raises(ValueError):
        compose(
            _readiness(),
            _security_context(),
            datetime(2026, 9, 17, 20, 0),
        )


def test_g2pb_red_c11_created_at_before_context_issuance_fails_closed() -> None:
    context = _security_context()
    compose = _composer()

    with pytest.raises(ValueError):
        compose(
            _readiness(),
            context,
            context.issued_at - timedelta(microseconds=1),
        )


def test_g2pb_red_c12_created_at_at_or_after_expiry_fails_closed() -> None:
    context = _security_context()
    compose = _composer()

    with pytest.raises(ValueError):
        compose(_readiness(), context, context.expires_at)


def test_g2pb_red_c13_binding_is_not_recomputed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def _forbidden_recomputation(*args: object, **kwargs: object) -> None:
        raise AssertionError("G2P-B must preserve the readiness binding")

    monkeypatch.setattr(
        "malak.memory.episodic_persistence_readiness."
        "compute_episodic_persistence_operation_binding",
        _forbidden_recomputation,
    )
    readiness = _readiness()

    request = _composer()(readiness, _security_context(), NOW)

    assert request.operation_binding is readiness.authorization_operation_binding


def test_g2pb_red_c14_composition_does_not_consult_pdp(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def _forbidden_pdp_call(*args: object, **kwargs: object) -> None:
        raise AssertionError("G2P-B composition must not consult the PDP")

    monkeypatch.setattr(
        "malak.security.pdp.StaticPolicyDecisionPoint.decide",
        _forbidden_pdp_call,
    )

    request = _composer()(_readiness(), _security_context(), NOW)

    assert isinstance(request, AuthorizationRequest)


def test_g2pb_red_c15_composition_does_not_execute_pep(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def _forbidden_pep_call(*args: object, **kwargs: object) -> None:
        raise AssertionError("G2P-B composition must not execute the PEP")

    monkeypatch.setattr(
        "malak.security.pep.StrictPolicyEnforcementPoint.execute",
        _forbidden_pep_call,
    )

    request = _composer()(_readiness(), _security_context(), NOW)

    assert isinstance(request, AuthorizationRequest)


def test_g2pb_red_c16_composition_has_no_filesystem_side_effects(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    compose = _composer()

    def _forbidden_side_effect(*args: object, **kwargs: object) -> None:
        raise AssertionError("G2P-B composition must not write to storage")

    monkeypatch.setattr(builtins, "open", _forbidden_side_effect)
    monkeypatch.setattr(Path, "write_text", _forbidden_side_effect)
    monkeypatch.setattr(Path, "write_bytes", _forbidden_side_effect)
    monkeypatch.setattr(Path, "mkdir", _forbidden_side_effect)
    monkeypatch.setattr(Path, "touch", _forbidden_side_effect)

    request = compose(_readiness(), _security_context(), NOW)

    assert isinstance(request, AuthorizationRequest)
