from dataclasses import FrozenInstanceError
from datetime import datetime, timedelta, timezone
from uuid import UUID

import pytest

from malak.security import (
    AuthorizationDecision,
    AuthorizationRequest,
    HumanConfirmationEvidence,
    PermissionScope,
    SecurityContext,
)


def test_permission_scope_normalizes_required_text() -> None:
    permission = PermissionScope(
        resource="  conversation  ",
        action="  read  ",
    )

    assert permission.resource == "conversation"
    assert permission.action == "read"


@pytest.mark.parametrize("field_name", ["resource", "action"])
@pytest.mark.parametrize("value", ["", "   "])
def test_permission_scope_rejects_empty_text(
    field_name: str,
    value: str,
) -> None:
    values = {
        "resource": "conversation",
        "action": "read",
    }
    values[field_name] = value

    with pytest.raises(ValueError):
        PermissionScope(**values)


@pytest.mark.parametrize("field_name", ["resource", "action"])
@pytest.mark.parametrize("value", [None, 1, True])
def test_permission_scope_rejects_non_string_values(
    field_name: str,
    value: object,
) -> None:
    values = {
        "resource": "conversation",
        "action": "read",
    }
    values[field_name] = value

    with pytest.raises(TypeError):
        PermissionScope(**values)


def test_permission_scope_has_structural_equality() -> None:
    first = PermissionScope(
        resource="conversation",
        action="read",
    )
    second = PermissionScope(
        resource="conversation",
        action="read",
    )

    assert first == second


def test_security_context_normalizes_subject_id() -> None:
    context = SecurityContext(
        subject_id="  aranwill  ",
        authenticated=True,
    )

    assert context.subject_id == "aranwill"
    assert context.authenticated is True


@pytest.mark.parametrize("subject_id", ["", "   "])
def test_security_context_rejects_empty_subject_id(
    subject_id: str,
) -> None:
    with pytest.raises(ValueError):
        SecurityContext(
            subject_id=subject_id,
            authenticated=True,
        )


@pytest.mark.parametrize("subject_id", [None, 1, True])
def test_security_context_rejects_non_string_subject_id(
    subject_id: object,
) -> None:
    with pytest.raises(TypeError):
        SecurityContext(
            subject_id=subject_id,
            authenticated=True,
        )


@pytest.mark.parametrize("authenticated", [None, 0, 1, "true"])
def test_security_context_requires_strict_boolean_authentication(
    authenticated: object,
) -> None:
    with pytest.raises(TypeError):
        SecurityContext(
            subject_id="aranwill",
            authenticated=authenticated,
        )


def test_authorization_request_generates_traceable_defaults() -> None:
    request = AuthorizationRequest(
        context=SecurityContext(
            subject_id="aranwill",
            authenticated=True,
        ),
        permission=PermissionScope(
            resource="conversation",
            action="read",
        ),
    )

    assert str(UUID(request.request_id)) == request.request_id
    assert request.created_at.tzinfo is not None
    assert request.created_at.utcoffset() == timedelta(0)


def test_authorization_request_normalizes_explicit_request_id() -> None:
    request = AuthorizationRequest(
        context=SecurityContext(
            subject_id="aranwill",
            authenticated=True,
        ),
        permission=PermissionScope(
            resource="conversation",
            action="read",
        ),
        request_id="  request-001  ",
    )

    assert request.request_id == "request-001"


@pytest.mark.parametrize("request_id", ["", "   "])
def test_authorization_request_rejects_empty_request_id(
    request_id: str,
) -> None:
    with pytest.raises(ValueError):
        AuthorizationRequest(
            context=SecurityContext(
                subject_id="aranwill",
                authenticated=True,
            ),
            permission=PermissionScope(
                resource="conversation",
                action="read",
            ),
            request_id=request_id,
        )


def test_authorization_request_requires_security_context() -> None:
    with pytest.raises(TypeError):
        AuthorizationRequest(
            context="aranwill",
            permission=PermissionScope(
                resource="conversation",
                action="read",
            ),
        )


def test_authorization_request_requires_permission_scope() -> None:
    with pytest.raises(TypeError):
        AuthorizationRequest(
            context=SecurityContext(
                subject_id="aranwill",
                authenticated=True,
            ),
            permission="conversation:read",
        )


def test_authorization_request_requires_datetime_created_at() -> None:
    with pytest.raises(TypeError):
        AuthorizationRequest(
            context=SecurityContext(
                subject_id="aranwill",
                authenticated=True,
            ),
            permission=PermissionScope(
                resource="conversation",
                action="read",
            ),
            created_at="2026-07-24T00:00:00Z",
        )


def test_authorization_request_rejects_naive_datetime() -> None:
    with pytest.raises(ValueError):
        AuthorizationRequest(
            context=SecurityContext(
                subject_id="aranwill",
                authenticated=True,
            ),
            permission=PermissionScope(
                resource="conversation",
                action="read",
            ),
            created_at=datetime(2026, 7, 24),
        )


def test_authorization_request_accepts_timezone_aware_datetime() -> None:
    created_at = datetime(
        2026,
        7,
        24,
        18,
        0,
        tzinfo=timezone.utc,
    )

    request = AuthorizationRequest(
        context=SecurityContext(
            subject_id="aranwill",
            authenticated=True,
        ),
        permission=PermissionScope(
            resource="conversation",
            action="read",
        ),
        created_at=created_at,
    )

    assert request.created_at == created_at


def test_authorization_request_does_not_contain_a_decision() -> None:
    request = AuthorizationRequest(
        context=SecurityContext(
            subject_id="aranwill",
            authenticated=True,
        ),
        permission=PermissionScope(
            resource="conversation",
            action="read",
        ),
    )

    assert not hasattr(request, "allowed")
    assert not hasattr(request, "reason")
    assert not hasattr(request.context, "permissions")


def test_human_confirmation_evidence_normalizes_required_text() -> None:
    evidence = HumanConfirmationEvidence(
        confirmation_id="  confirmation-001  ",
        original_request_id="  request-original  ",
        new_request_id="  request-new  ",
        subject_id="  aranwill  ",
        permission=PermissionScope(
            resource="system",
            action="update",
        ),
        confirmed_by="  owner  ",
        confirmed_at=datetime(2026, 7, 26, tzinfo=timezone.utc),
    )

    assert evidence.confirmation_id == "confirmation-001"
    assert evidence.original_request_id == "request-original"
    assert evidence.new_request_id == "request-new"
    assert evidence.subject_id == "aranwill"
    assert evidence.confirmed_by == "owner"


@pytest.mark.parametrize(
    "field_name",
    [
        "confirmation_id",
        "original_request_id",
        "new_request_id",
        "subject_id",
        "confirmed_by",
    ],
)
@pytest.mark.parametrize("value", ["", "   "])
def test_human_confirmation_evidence_rejects_empty_text(
    field_name: str,
    value: str,
) -> None:
    values = {
        "confirmation_id": "confirmation-001",
        "original_request_id": "request-original",
        "new_request_id": "request-new",
        "subject_id": "aranwill",
        "permission": PermissionScope(
            resource="system",
            action="update",
        ),
        "confirmed_by": "owner",
        "confirmed_at": datetime(
            2026,
            7,
            26,
            tzinfo=timezone.utc,
        ),
    }
    values[field_name] = value

    with pytest.raises(ValueError):
        HumanConfirmationEvidence(**values)


@pytest.mark.parametrize(
    "field_name",
    [
        "confirmation_id",
        "original_request_id",
        "new_request_id",
        "subject_id",
        "confirmed_by",
    ],
)
@pytest.mark.parametrize("value", [None, 1, True])
def test_human_confirmation_evidence_rejects_non_string_text(
    field_name: str,
    value: object,
) -> None:
    values = {
        "confirmation_id": "confirmation-001",
        "original_request_id": "request-original",
        "new_request_id": "request-new",
        "subject_id": "aranwill",
        "permission": PermissionScope(
            resource="system",
            action="update",
        ),
        "confirmed_by": "owner",
        "confirmed_at": datetime(
            2026,
            7,
            26,
            tzinfo=timezone.utc,
        ),
    }
    values[field_name] = value

    with pytest.raises(TypeError):
        HumanConfirmationEvidence(**values)


def test_human_confirmation_evidence_requires_permission_scope() -> None:
    with pytest.raises(TypeError):
        HumanConfirmationEvidence(
            confirmation_id="confirmation-001",
            original_request_id="request-original",
            new_request_id="request-new",
            subject_id="aranwill",
            permission="system:update",
            confirmed_by="owner",
            confirmed_at=datetime(
                2026,
                7,
                26,
                tzinfo=timezone.utc,
            ),
        )


def test_human_confirmation_evidence_requires_datetime() -> None:
    with pytest.raises(TypeError):
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
            confirmed_at="2026-07-26T00:00:00Z",
        )


def test_authorization_decision_normalizes_required_text() -> None:
    decision = AuthorizationDecision(
        request_id="  request-001  ",
        allowed=False,
        reason="  no_applicable_policy  ",
    )

    assert decision.request_id == "request-001"
    assert decision.allowed is False
    assert decision.reason == "no_applicable_policy"


@pytest.mark.parametrize("request_id", ["", "   "])
def test_authorization_decision_rejects_empty_request_id(
    request_id: str,
) -> None:
    with pytest.raises(ValueError):
        AuthorizationDecision(
            request_id=request_id,
            allowed=False,
            reason="no_applicable_policy",
        )


@pytest.mark.parametrize("allowed", [None, 0, 1, "false"])
def test_authorization_decision_requires_strict_boolean_result(
    allowed: object,
) -> None:
    with pytest.raises(TypeError):
        AuthorizationDecision(
            request_id="request-001",
            allowed=allowed,
            reason="no_applicable_policy",
        )


@pytest.mark.parametrize("reason", ["", "   "])
def test_authorization_decision_rejects_empty_reason(
    reason: str,
) -> None:
    with pytest.raises(ValueError):
        AuthorizationDecision(
            request_id="request-001",
            allowed=False,
            reason=reason,
        )


@pytest.mark.parametrize(
    "instance, field_name, replacement",
    [
        (
            PermissionScope(
                resource="conversation",
                action="read",
            ),
            "action",
            "write",
        ),
        (
            SecurityContext(
                subject_id="aranwill",
                authenticated=True,
            ),
            "authenticated",
            False,
        ),
        (
            AuthorizationRequest(
                context=SecurityContext(
                    subject_id="aranwill",
                    authenticated=True,
                ),
                permission=PermissionScope(
                    resource="conversation",
                    action="read",
                ),
            ),
            "request_id",
            "replacement",
        ),
        (
            AuthorizationDecision(
                request_id="request-001",
                allowed=False,
                reason="no_applicable_policy",
            ),
            "allowed",
            True,
        ),
    ],
)
def test_authorization_contracts_are_immutable(
    instance: object,
    field_name: str,
    replacement: object,
) -> None:
    with pytest.raises(FrozenInstanceError):
        setattr(instance, field_name, replacement)
