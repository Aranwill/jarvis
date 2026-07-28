from typing import Generic, Protocol, TypeVar

from malak.security.audit import (
    AuthorizationAuditOutcome,
    AuthorizationAuditRecord,
    AuthorizationAuditSink,
)
from malak.security.contracts import (
    AuthorizationDecision,
    AuthorizationRequest,
    HumanConfirmationEvidence,
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

        try:
            decision = self._policy_decision_point.decide(
                request,
                confirmation,
            )
        except Exception as error:
            self._write_audit(
                request=request,
                outcome=AuthorizationAuditOutcome.DECISION_FAILED,
                reason_code="policy_decision_failed",
                failure_message=(
                    "authorization audit failed after "
                    "policy decision failure"
                ),
            )
            raise AuthorizationEnforcementError(
                "policy decision failed"
            ) from error

        if not isinstance(decision, AuthorizationDecision):
            self._write_audit(
                request=request,
                outcome=AuthorizationAuditOutcome.INVALID_DECISION,
                reason_code="invalid_decision_type",
                failure_message=(
                    "authorization audit failed after "
                    "invalid policy decision"
                ),
            )
            raise AuthorizationEnforcementError(
                "policy decision point returned an invalid decision"
            )

        if decision.request_id != request.request_id:
            self._write_audit(
                request=request,
                outcome=AuthorizationAuditOutcome.INVALID_DECISION,
                reason_code="decision_request_mismatch",
                failure_message=(
                    "authorization audit failed after "
                    "decision request mismatch"
                ),
            )
            raise AuthorizationEnforcementError(
                "authorization decision does not match request"
            )

        if not decision.allowed:
            self._write_audit(
                request=request,
                outcome=AuthorizationAuditOutcome.DENIED,
                reason_code=decision.reason,
                failure_message=(
                    "authorization audit failed for denied decision"
                ),
            )
            raise AuthorizationDeniedError(
                decision.request_id,
                decision.reason,
            )

        self._write_audit(
            request=request,
            outcome=AuthorizationAuditOutcome.ALLOWED,
            reason_code=decision.reason,
            failure_message=(
                "authorization audit failed before protected operation"
            ),
        )

        try:
            return self._protected_operation.execute()
        except Exception as operation_error:
            try:
                self._write_audit(
                    request=request,
                    outcome=AuthorizationAuditOutcome.OPERATION_FAILED,
                    reason_code="protected_operation_failed",
                    failure_message=(
                        "authorization audit failed after "
                        "protected operation failure"
                    ),
                )
            except AuthorizationEnforcementError as audit_error:
                secondary_error = audit_error.__cause__ or audit_error
                raise operation_error from secondary_error

            raise

    def _write_audit(
        self,
        *,
        request: AuthorizationRequest,
        outcome: AuthorizationAuditOutcome,
        reason_code: str,
        failure_message: str,
    ) -> None:
        record = AuthorizationAuditRecord(
            request_id=request.request_id,
            subject_id=request.context.subject_id,
            resource=request.permission.resource,
            action=request.permission.action,
            outcome=outcome,
            reason_code=reason_code,
        )

        try:
            self._authorization_audit_sink.write(record)
        except Exception as error:
            raise AuthorizationEnforcementError(
                failure_message
            ) from error
