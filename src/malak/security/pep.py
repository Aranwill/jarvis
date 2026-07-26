from typing import Generic, Protocol, TypeVar

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

        self._policy_decision_point = policy_decision_point
        self._protected_operation = protected_operation

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
            raise AuthorizationEnforcementError(
                "policy decision failed"
            ) from error

        self._validate_decision(request, decision)

        if not decision.allowed:
            raise AuthorizationDeniedError(
                decision.request_id,
                decision.reason,
            )

        return self._protected_operation.execute()

    @staticmethod
    def _validate_decision(
        request: AuthorizationRequest,
        decision: object,
    ) -> None:
        if not isinstance(decision, AuthorizationDecision):
            raise AuthorizationEnforcementError(
                "policy decision point returned an invalid decision"
            )

        if decision.request_id != request.request_id:
            raise AuthorizationEnforcementError(
                "authorization decision does not match request"
            )
