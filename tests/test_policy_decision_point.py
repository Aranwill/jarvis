from dataclasses import FrozenInstanceError
from datetime import datetime, timezone

import pytest

from malak.security import (
    AuthorizationRequest,
    HumanConfirmationEvidence,
    PermissionScope,
    PolicyEffect,
    PolicyRule,
    SecurityContext,
    StaticPolicyDecisionPoint,
)


class RecordingVerifier:
    def __init__(
        self,
        result: object = True,
        error: Exception | None = None,
    ) -> None:
        self.result = result
        self.error = error
        self.calls: list[
            tuple[AuthorizationRequest, HumanConfirmationEvidence]
        ] = []

    def verify(
        self,
        request: AuthorizationRequest,
        evidence: HumanConfirmationEvidence,
    ) -> bool:
        self.calls.append((request, evidence))

        if self.error is not None:
            raise self.error

        return self.result


def make_request(
    *,
    request_id: str = "request-new",
    subject_id: str = "aranwill",
    authenticated: bool = True,
    resource: str = "system",
    action: str = "update",
) -> AuthorizationRequest:
    return AuthorizationRequest(
        context=SecurityContext(
            context_id="context-001",
            session_id="session-001",
            subject_id=subject_id,
            authenticated=authenticated,
            issued_at=datetime(2026, 8, 15, 18, 0, tzinfo=timezone.utc),
            expires_at=datetime(2026, 8, 15, 18, 30, tzinfo=timezone.utc),
        ),
        permission=PermissionScope(
            resource=resource,
            action=action,
        ),
        request_id=request_id,
    )


def make_rule(
    effect: PolicyEffect,
    *,
    subject_id: str = "aranwill",
    resource: str = "system",
    action: str = "update",
) -> PolicyRule:
    return PolicyRule(
        subject_id=subject_id,
        permission=PermissionScope(
            resource=resource,
            action=action,
        ),
        effect=effect,
    )


def make_confirmation(
    *,
    original_request_id: str = "request-original",
    new_request_id: str = "request-new",
    subject_id: str = "aranwill",
    resource: str = "system",
    action: str = "update",
) -> HumanConfirmationEvidence:
    return HumanConfirmationEvidence(
        confirmation_id="confirmation-001",
        original_request_id=original_request_id,
        new_request_id=new_request_id,
        subject_id=subject_id,
        permission=PermissionScope(
            resource=resource,
            action=action,
        ),
        confirmed_by="owner",
        confirmed_at=datetime(2026, 7, 26, tzinfo=timezone.utc),
    )


def test_exact_allow_rule_authorizes_request() -> None:
    request = make_request()
    pdp = StaticPolicyDecisionPoint(
        [make_rule(PolicyEffect.ALLOW)]
    )

    decision = pdp.decide(request)

    assert decision.request_id == request.request_id
    assert decision.allowed is True
    assert decision.reason == "policy_allowed"


@pytest.mark.parametrize(
    "authorization_request",
    [
        make_request(subject_id="other"),
        make_request(resource="conversation"),
        make_request(action="read"),
    ],
)
def test_policy_matching_is_exact(
    authorization_request: AuthorizationRequest,
) -> None:
    pdp = StaticPolicyDecisionPoint(
        [make_rule(PolicyEffect.ALLOW)]
    )

    decision = pdp.decide(authorization_request)

    assert decision.allowed is False
    assert decision.reason == "no_applicable_policy"


def test_unauthenticated_subject_is_denied_before_policy() -> None:
    request = make_request(authenticated=False)
    pdp = StaticPolicyDecisionPoint(
        [make_rule(PolicyEffect.ALLOW)]
    )

    decision = pdp.decide(request)

    assert decision.allowed is False
    assert decision.reason == "unauthenticated_subject"


def test_explicit_deny_rule_denies_request() -> None:
    request = make_request()
    pdp = StaticPolicyDecisionPoint(
        [make_rule(PolicyEffect.DENY)]
    )

    decision = pdp.decide(request)

    assert decision.allowed is False
    assert decision.reason == "policy_denied"


def test_confirmation_rule_denies_original_request() -> None:
    request = make_request(request_id="request-original")
    verifier = RecordingVerifier()
    pdp = StaticPolicyDecisionPoint(
        [make_rule(PolicyEffect.REQUIRE_HUMAN_CONFIRMATION)],
        confirmation_verifier=verifier,
    )

    decision = pdp.decide(request)

    assert decision.allowed is False
    assert decision.reason == "human_confirmation_required"
    assert verifier.calls == []


def test_verified_confirmation_authorizes_only_new_request() -> None:
    request = make_request()
    confirmation = make_confirmation()
    verifier = RecordingVerifier()
    pdp = StaticPolicyDecisionPoint(
        [make_rule(PolicyEffect.REQUIRE_HUMAN_CONFIRMATION)],
        confirmation_verifier=verifier,
    )

    decision = pdp.decide(request, confirmation)

    assert decision.allowed is True
    assert decision.reason == "human_confirmation_approved"
    assert verifier.calls == [(request, confirmation)]


@pytest.mark.parametrize(
    "confirmation",
    [
        make_confirmation(new_request_id="another-request"),
        make_confirmation(subject_id="other"),
        make_confirmation(resource="conversation"),
        make_confirmation(action="read"),
    ],
)
def test_incongruent_confirmation_is_denied_before_verification(
    confirmation: HumanConfirmationEvidence,
) -> None:
    request = make_request()
    verifier = RecordingVerifier()
    pdp = StaticPolicyDecisionPoint(
        [make_rule(PolicyEffect.REQUIRE_HUMAN_CONFIRMATION)],
        confirmation_verifier=verifier,
    )

    decision = pdp.decide(request, confirmation)

    assert decision.allowed is False
    assert decision.reason == "invalid_human_confirmation"
    assert verifier.calls == []


def test_confirmation_without_verifier_is_denied() -> None:
    pdp = StaticPolicyDecisionPoint(
        [make_rule(PolicyEffect.REQUIRE_HUMAN_CONFIRMATION)]
    )

    decision = pdp.decide(make_request(), make_confirmation())

    assert decision.allowed is False
    assert (
        decision.reason
        == "human_confirmation_verifier_unavailable"
    )


@pytest.mark.parametrize("verifier_result", [False, None, 1])
def test_unverified_confirmation_is_denied(
    verifier_result: object,
) -> None:
    pdp = StaticPolicyDecisionPoint(
        [make_rule(PolicyEffect.REQUIRE_HUMAN_CONFIRMATION)],
        confirmation_verifier=RecordingVerifier(verifier_result),
    )

    decision = pdp.decide(make_request(), make_confirmation())

    assert decision.allowed is False
    assert decision.reason == "invalid_human_confirmation"


def test_verifier_failure_is_denied_safely() -> None:
    pdp = StaticPolicyDecisionPoint(
        [make_rule(PolicyEffect.REQUIRE_HUMAN_CONFIRMATION)],
        confirmation_verifier=RecordingVerifier(
            error=RuntimeError("verification unavailable")
        ),
    )

    decision = pdp.decide(make_request(), make_confirmation())

    assert decision.allowed is False
    assert (
        decision.reason
        == "human_confirmation_verification_failed"
    )


def test_invalid_confirmation_type_is_denied() -> None:
    pdp = StaticPolicyDecisionPoint(
        [make_rule(PolicyEffect.REQUIRE_HUMAN_CONFIRMATION)],
        confirmation_verifier=RecordingVerifier(),
    )

    decision = pdp.decide(make_request(), "confirmed")

    assert decision.allowed is False
    assert decision.reason == "invalid_human_confirmation"


def test_invalid_request_type_raises_type_error() -> None:
    pdp = StaticPolicyDecisionPoint([])

    with pytest.raises(TypeError):
        pdp.decide("request")


def test_duplicate_policy_rule_is_rejected() -> None:
    with pytest.raises(ValueError):
        StaticPolicyDecisionPoint(
            [
                make_rule(PolicyEffect.ALLOW),
                make_rule(PolicyEffect.DENY),
            ]
        )


def test_wildcard_subject_rule_is_rejected() -> None:
    with pytest.raises(ValueError):
        PolicyRule(
            subject_id="*",
            permission=PermissionScope(
                resource="system",
                action="update",
            ),
            effect=PolicyEffect.ALLOW,
        )


@pytest.mark.parametrize(
    "resource, action",
    [
        ("*", "update"),
        ("system", "*"),
    ],
)
def test_wildcard_permission_rule_is_rejected(
    resource: str,
    action: str,
) -> None:
    with pytest.raises(ValueError):
        make_rule(
            PolicyEffect.ALLOW,
            resource=resource,
            action=action,
        )


def test_rule_requires_policy_effect() -> None:
    with pytest.raises(TypeError):
        PolicyRule(
            subject_id="aranwill",
            permission=PermissionScope(
                resource="system",
                action="update",
            ),
            effect="allow",
        )


def test_rules_must_contain_only_policy_rules() -> None:
    with pytest.raises(TypeError):
        StaticPolicyDecisionPoint(["allow"])


def test_verifier_must_implement_verify() -> None:
    with pytest.raises(TypeError):
        StaticPolicyDecisionPoint(
            [],
            confirmation_verifier=object(),
        )


def test_same_request_cannot_be_used_as_confirmation_origin() -> None:
    with pytest.raises(ValueError):
        make_confirmation(
            original_request_id="request-new",
            new_request_id="request-new",
        )


def test_confirmation_requires_timezone_aware_timestamp() -> None:
    with pytest.raises(ValueError):
        HumanConfirmationEvidence(
            confirmation_id="confirmation-001",
            original_request_id="request-original",
            new_request_id="request-new",
            subject_id="aranwill",
            permission=PermissionScope(
                resource="system",
                action="update",
            ),
            confirmed_by="owner",
            confirmed_at=datetime(2026, 7, 26),
        )


def test_policy_decisions_are_deterministic() -> None:
    request = make_request()
    pdp = StaticPolicyDecisionPoint(
        [make_rule(PolicyEffect.ALLOW)]
    )

    first = pdp.decide(request)
    second = pdp.decide(request)

    assert first == second


@pytest.mark.parametrize(
    "instance, field_name, replacement",
    [
        (
            make_rule(PolicyEffect.ALLOW),
            "effect",
            PolicyEffect.DENY,
        ),
        (
            make_confirmation(),
            "confirmed_by",
            "other",
        ),
    ],
)
def test_pdp_value_objects_are_immutable(
    instance: object,
    field_name: str,
    replacement: object,
) -> None:
    with pytest.raises(FrozenInstanceError):
        setattr(instance, field_name, replacement)