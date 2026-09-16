from typing import Generic, Protocol, TypeVar

from malak.security.audit import (
    AuthorizationAuditOutcome,
    AuthorizationAuditRecord,
    AuthorizationAuditSink,
)
from malak.security.contracts import (
    AuthorizationDecision,
    AuthorizationOperationBinding,
    AuthorizationRequest,
    HumanConfirmationEvidence,
    PermissionScope,
)
from malak.security.pdp import PolicyDecisionPoint


ResultT = TypeVar("ResultT", covariant=True)


class ProtectedOperation(Protocol[ResultT]):
    def execute(self) -> ResultT:
        ...


class PolicyEnforcementPoint(Protocol[ResultT]):
    def execute(
        self,
        request: AuthorizationRequest,
        confirmation: HumanConfirmationEvidence | None = None,
    ) -> ResultT:
        ...


class AuthorizationDeniedError(PermissionError):
    def __init__(self, request_id: str, reason: str) -> None:
        self.request_id = request_id
        self.reason = reason
        super().__init__(
            f"authorization denied for request {request_id}: {reason}"
        )


class AuthorizationEnforcementError(RuntimeError):
    pass


class StrictPolicyEnforcementPoint(Generic[ResultT]):
    def __init__(
        self,
        policy_decision_point: PolicyDecisionPoint,
        protected_operation: ProtectedOperation[ResultT],
        authorization_audit_sink: AuthorizationAuditSink,
    ) -> None:
        if not callable(
            getattr(policy_decision_point, "decide", None)
        ):
            raise TypeError(
                "policy_decision_point must implement decide"
            )

        if not callable(
            getattr(protected_operation, "execute", None)
        ):
            raise TypeError(
                "protected_operation must implement execute"
            )

        if not callable(
            getattr(authorization_audit_sink, "write", None)
        ):
            raise TypeError(
                "authorization_audit_sink must implement write"
            )

        self._policy_decision_point = policy_decision_point
        self._protected_operation = protected_operation
        self._authorization_audit_sink = authorization_audit_sink

    def execute(
        self,
        request: AuthorizationRequest,
        confirmation: HumanConfirmationEvidence | None = None,
    ) -> ResultT:
        if not isinstance(request, AuthorizationRequest):
            raise AuthorizationEnforcementError(
                "request must be an AuthorizationRequest"
            )

        operation_binding = self._read_operation_binding(request)

        if not self._is_temporally_coherent(request):
            self._write_audit(
                request=request,
                protected_operation_binding=operation_binding,
                outcome=AuthorizationAuditOutcome.ENFORCEMENT_FAILED,
                reason_code="authorization_request_time_invalid",
                failure_message=(
                    "authorization audit failed after request time rejection"
                ),
            )
            raise AuthorizationEnforcementError(
                "authorization request is outside security context lifecycle"
            )

        required_permission = self._read_required_permission(
            request,
            operation_binding,
        )

        self._validate_request_operation_binding(
            request,
            operation_binding,
            required_permission,
        )

        try:
            decision = self._policy_decision_point.decide(
                request,
                confirmation,
            )
        except Exception as error:
            self._write_audit(
                request=request,
                protected_operation_binding=operation_binding,
                outcome=AuthorizationAuditOutcome.DECISION_FAILED,
                reason_code="policy_decision_failed",
                failure_message=(
                    "authorization audit failed after "
                    "policy decision failure"
                ),
                protected_operation_permission=required_permission,
            )
            raise AuthorizationEnforcementError(
                "policy decision failed"
            ) from error

        if not isinstance(decision, AuthorizationDecision):
            self._write_audit(
                request=request,
                protected_operation_binding=operation_binding,
                outcome=AuthorizationAuditOutcome.INVALID_DECISION,
                reason_code="invalid_decision_type",
                failure_message=(
                    "authorization audit failed after "
                    "invalid policy decision"
                ),
                protected_operation_permission=required_permission,
            )
            raise AuthorizationEnforcementError(
                "policy decision point returned an invalid decision"
            )

        if decision.request_id != request.request_id:
            self._write_audit(
                request=request,
                protected_operation_binding=operation_binding,
                outcome=AuthorizationAuditOutcome.INVALID_DECISION,
                reason_code="decision_request_mismatch",
                failure_message=(
                    "authorization audit failed after "
                    "decision request mismatch"
                ),
                protected_operation_permission=required_permission,
            )
            raise AuthorizationEnforcementError(
                "authorization decision does not match request"
            )

        if decision.operation_binding != request.operation_binding:
            self._write_audit(
                request=request,
                protected_operation_binding=operation_binding,
                outcome=AuthorizationAuditOutcome.INVALID_DECISION,
                reason_code="decision_operation_binding_mismatch",
                failure_message=(
                    "authorization audit failed after "
                    "decision operation binding mismatch"
                ),
                protected_operation_permission=required_permission,
            )
            raise AuthorizationEnforcementError(
                "authorization decision operation binding does not match request"
            )

        if not decision.allowed:
            self._write_audit(
                request=request,
                protected_operation_binding=operation_binding,
                outcome=AuthorizationAuditOutcome.DENIED,
                reason_code=decision.reason,
                failure_message=(
                    "authorization audit failed for denied decision"
                ),
                protected_operation_permission=required_permission,
            )
            raise AuthorizationDeniedError(
                decision.request_id,
                decision.reason,
            )

        self._write_audit(
            request=request,
            protected_operation_binding=operation_binding,
            outcome=AuthorizationAuditOutcome.ALLOWED,
            reason_code=decision.reason,
            failure_message=(
                "authorization audit failed before protected operation"
            ),
            protected_operation_permission=required_permission,
        )

        try:
            return self._protected_operation.execute()
        except Exception as operation_error:
            try:
                self._write_audit(
                    request=request,
                    protected_operation_binding=operation_binding,
                    outcome=AuthorizationAuditOutcome.OPERATION_FAILED,
                    reason_code="protected_operation_failed",
                    failure_message=(
                        "authorization audit failed after "
                        "protected operation failure"
                    ),
                    protected_operation_permission=required_permission,
                )
            except AuthorizationEnforcementError as audit_error:
                secondary_error = audit_error.__cause__ or audit_error
                raise operation_error from secondary_error

            raise

    def _read_operation_binding(
        self,
        request: AuthorizationRequest,
    ) -> AuthorizationOperationBinding | None:
        try:
            operation_binding = getattr(
                self._protected_operation,
                "authorization_binding",
                None,
            )
        except Exception as error:
            self._write_audit(
                request=request,
                protected_operation_binding=None,
                outcome=AuthorizationAuditOutcome.ENFORCEMENT_FAILED,
                reason_code="protected_operation_binding_unavailable",
                failure_message=(
                    "authorization audit failed after protected operation "
                    "binding access failure"
                ),
            )
            raise AuthorizationEnforcementError(
                "protected operation binding could not be read"
            ) from error

        if operation_binding is not None and not isinstance(
            operation_binding,
            AuthorizationOperationBinding,
        ):
            self._write_audit(
                request=request,
                protected_operation_binding=None,
                outcome=AuthorizationAuditOutcome.ENFORCEMENT_FAILED,
                reason_code="invalid_protected_operation_binding",
                failure_message=(
                    "authorization audit failed after invalid protected "
                    "operation binding"
                ),
            )
            raise AuthorizationEnforcementError(
                "protected operation returned an invalid authorization binding"
            )

        return operation_binding

    def _read_required_permission(
        self,
        request: AuthorizationRequest,
        operation_binding: AuthorizationOperationBinding | None,
    ) -> PermissionScope | None:
        try:
            required_permission = getattr(
                self._protected_operation,
                "required_permission",
                None,
            )
        except Exception as error:
            self._write_audit(
                request=request,
                protected_operation_binding=operation_binding,
                outcome=AuthorizationAuditOutcome.ENFORCEMENT_FAILED,
                reason_code="protected_operation_permission_unavailable",
                failure_message=(
                    "authorization audit failed after protected operation "
                    "permission access failure"
                ),
            )
            raise AuthorizationEnforcementError(
                "protected operation permission could not be read"
            ) from error

        if required_permission is not None and not isinstance(
            required_permission,
            PermissionScope,
        ):
            self._write_audit(
                request=request,
                protected_operation_binding=operation_binding,
                outcome=AuthorizationAuditOutcome.ENFORCEMENT_FAILED,
                reason_code="invalid_protected_operation_permission",
                failure_message=(
                    "authorization audit failed after invalid protected "
                    "operation permission"
                ),
            )
            raise AuthorizationEnforcementError(
                "protected operation returned an invalid required permission"
            )

        if operation_binding is not None and required_permission is None:
            self._write_audit(
                request=request,
                protected_operation_binding=operation_binding,
                outcome=AuthorizationAuditOutcome.ENFORCEMENT_FAILED,
                reason_code="bound_operation_permission_missing",
                failure_message=(
                    "authorization audit failed after bound operation "
                    "permission rejection"
                ),
            )
            raise AuthorizationEnforcementError(
                "bound protected operation must declare a required permission"
            )

        if (
            required_permission is not None
            and request.permission != required_permission
        ):
            self._write_audit(
                request=request,
                protected_operation_binding=operation_binding,
                outcome=AuthorizationAuditOutcome.ENFORCEMENT_FAILED,
                reason_code="request_operation_permission_mismatch",
                failure_message=(
                    "authorization audit failed after request/operation "
                    "permission mismatch"
                ),
                protected_operation_permission=required_permission,
            )
            raise AuthorizationEnforcementError(
                "authorization request permission does not match protected operation"
            )

        return required_permission

    def _validate_request_operation_binding(
        self,
        request: AuthorizationRequest,
        operation_binding: AuthorizationOperationBinding | None,
        required_permission: PermissionScope | None,
    ) -> None:
        request_binding = request.operation_binding

        if (request_binding is None) != (operation_binding is None):
            self._write_audit(
                request=request,
                protected_operation_binding=operation_binding,
                outcome=AuthorizationAuditOutcome.ENFORCEMENT_FAILED,
                reason_code="request_operation_binding_presence_mismatch",
                failure_message=(
                    "authorization audit failed after request/operation "
                    "binding presence mismatch"
                ),
                protected_operation_permission=required_permission,
            )
            raise AuthorizationEnforcementError(
                "authorization request and protected operation binding presence differ"
            )

        if (
            request_binding is not None
            and operation_binding is not None
            and request_binding != operation_binding
        ):
            self._write_audit(
                request=request,
                protected_operation_binding=operation_binding,
                outcome=AuthorizationAuditOutcome.ENFORCEMENT_FAILED,
                reason_code="request_operation_binding_mismatch",
                failure_message=(
                    "authorization audit failed after request/operation "
                    "binding mismatch"
                ),
                protected_operation_permission=required_permission,
            )
            raise AuthorizationEnforcementError(
                "authorization request does not match protected operation"
            )

    @staticmethod
    def _is_temporally_coherent(request: AuthorizationRequest) -> bool:
        return (
            request.context.issued_at
            <= request.created_at
            < request.context.expires_at
        )

    def _write_audit(
        self,
        *,
        request: AuthorizationRequest,
        protected_operation_binding: AuthorizationOperationBinding | None,
        outcome: AuthorizationAuditOutcome,
        reason_code: str,
        failure_message: str,
        protected_operation_permission: PermissionScope | None = None,
    ) -> None:
        record = AuthorizationAuditRecord(
            request_id=request.request_id,
            subject_id=request.context.subject_id,
            resource=request.permission.resource,
            action=request.permission.action,
            outcome=outcome,
            reason_code=reason_code,
            operation_binding=request.operation_binding,
            protected_operation_binding=protected_operation_binding,
            protected_operation_permission=protected_operation_permission,
        )

        try:
            self._authorization_audit_sink.write(record)
        except Exception as error:
            raise AuthorizationEnforcementError(
                failure_message
            ) from error
