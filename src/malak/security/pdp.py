from collections.abc import Iterable
from dataclasses import dataclass
from enum import StrEnum
from types import MappingProxyType
from typing import Protocol
from malak.security.context_validator import SecurityContextValidator

from malak.security.contracts import (
    AuthorizationDecision,
    AuthorizationRequest,
    HumanConfirmationEvidence,
    PermissionScope,
)


class PolicyEffect(StrEnum):
    ALLOW = "allow"
    DENY = "deny"
    REQUIRE_HUMAN_CONFIRMATION = "require_human_confirmation"


@dataclass(frozen=True, slots=True)
class PolicyRule:
    subject_id: str
    permission: PermissionScope
    effect: PolicyEffect

    def __post_init__(self) -> None:
        if not isinstance(self.subject_id, str):
            raise TypeError("subject_id must be a string")

        normalized_subject_id = self.subject_id.strip()

        if not normalized_subject_id:
            raise ValueError("subject_id must not be empty")

        if normalized_subject_id == "*":
            raise ValueError("wildcard subjects are not supported")

        object.__setattr__(self, "subject_id", normalized_subject_id)

        if not isinstance(self.permission, PermissionScope):
            raise TypeError("permission must be a PermissionScope")

        if (
            self.permission.resource == "*"
            or self.permission.action == "*"
        ):
            raise ValueError("wildcard permissions are not supported")

        if not isinstance(self.effect, PolicyEffect):
            raise TypeError("effect must be a PolicyEffect")


class HumanConfirmationVerifier(Protocol):
    def verify(
        self,
        request: AuthorizationRequest,
        evidence: HumanConfirmationEvidence,
    ) -> bool:
        ...


class PolicyDecisionPoint(Protocol):
    def decide(
        self,
        request: AuthorizationRequest,
        confirmation: HumanConfirmationEvidence | None = None,
    ) -> AuthorizationDecision:
        ...


class StaticPolicyDecisionPoint:
    def __init__(
        self,
        rules: Iterable[PolicyRule],
        *,
        context_validator: SecurityContextValidator,
        confirmation_verifier: HumanConfirmationVerifier | None = None,
    ) -> None:
        rules_by_key: dict[
            tuple[str, PermissionScope],
            PolicyRule,
        ] = {}

        for rule in rules:
            if not isinstance(rule, PolicyRule):
                raise TypeError("rules must contain only PolicyRule values")

            key = (rule.subject_id, rule.permission)

            if key in rules_by_key:
                raise ValueError(
                    "duplicate policy rule for subject and permission"
                )

            rules_by_key[key] = rule

        if (
            confirmation_verifier is not None
            and not callable(
                getattr(confirmation_verifier, "verify", None)
            )
        ):
            raise TypeError(
                "confirmation_verifier must implement verify"
            )

        self._rules = MappingProxyType(rules_by_key)
        self._confirmation_verifier = confirmation_verifier
        self._context_validator = context_validator

    def decide(
        self,
        request: AuthorizationRequest,
        confirmation: HumanConfirmationEvidence | None = None,
    ) -> AuthorizationDecision:
        if not isinstance(request, AuthorizationRequest):
            raise TypeError("request must be an AuthorizationRequest")

        if not request.context.authenticated:
            return self._deny(request, "unauthenticated_subject")

        if not self._context_validator.is_valid(request.context):
            return self._deny(request, "expired_security_context")

        rule = self._rules.get(
            (request.context.subject_id, request.permission)
        )

        if rule is None:
            return self._deny(request, "no_applicable_policy")

        if rule.effect is PolicyEffect.DENY:
            return self._deny(request, "policy_denied")

        if rule.effect is PolicyEffect.REQUIRE_HUMAN_CONFIRMATION:
            return self._decide_with_confirmation(
                request,
                confirmation,
            )

        return AuthorizationDecision(
            request_id=request.request_id,
            allowed=True,
            reason="policy_allowed",
        )

    def _decide_with_confirmation(
        self,
        request: AuthorizationRequest,
        confirmation: HumanConfirmationEvidence | None,
    ) -> AuthorizationDecision:
        if confirmation is None:
            return self._deny(
                request,
                "human_confirmation_required",
            )

        if not isinstance(
            confirmation,
            HumanConfirmationEvidence,
        ):
            return self._deny(
                request,
                "invalid_human_confirmation",
            )

        if not self._is_bound_to_request(request, confirmation):
            return self._deny(
                request,
                "invalid_human_confirmation",
            )

        if self._confirmation_verifier is None:
            return self._deny(
                request,
                "human_confirmation_verifier_unavailable",
            )

        try:
            verified = self._confirmation_verifier.verify(
                request,
                confirmation,
            )
        except Exception:
            return self._deny(
                request,
                "human_confirmation_verification_failed",
            )

        if verified is not True:
            return self._deny(
                request,
                "invalid_human_confirmation",
            )

        return AuthorizationDecision(
            request_id=request.request_id,
            allowed=True,
            reason="human_confirmation_approved",
        )

    @staticmethod
    def _is_bound_to_request(
        request: AuthorizationRequest,
        confirmation: HumanConfirmationEvidence,
    ) -> bool:
        return (
            confirmation.new_request_id == request.request_id
            and confirmation.original_request_id
            != request.request_id
            and confirmation.subject_id == request.context.subject_id
            and confirmation.permission == request.permission
        )

    @staticmethod
    def _deny(
        request: AuthorizationRequest,
        reason: str,
    ) -> AuthorizationDecision:
        return AuthorizationDecision(
            request_id=request.request_id,
            allowed=False,
            reason=reason,
        )
