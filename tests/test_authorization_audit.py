from dataclasses import FrozenInstanceError
from datetime import datetime, timedelta, timezone
from uuid import UUID

import pytest

from malak.security import (
    AuthorizationAuditOutcome,
    AuthorizationAuditRecord,
    AuthorizationAuditSink,
    AuthorizationOperationBinding,
    InMemoryAuthorizationAuditStore,
)


def make_binding(digest_character: str = "a") -> AuthorizationOperationBinding:
    return AuthorizationOperationBinding(
        namespace="memory.episodic.persistence",
        binding_version="v1",
        digest_algorithm="sha256",
        digest_hex=digest_character * 64,
    )


def make_record(
    *,
    outcome: AuthorizationAuditOutcome = (
        AuthorizationAuditOutcome.DENIED
    ),
    operation_binding: AuthorizationOperationBinding | None = None,
    protected_operation_binding: AuthorizationOperationBinding | None = None,
) -> AuthorizationAuditRecord:
    return AuthorizationAuditRecord(
        request_id="request-001",
        subject_id="aranwill",
        resource="conversation",
        action="write",
        outcome=outcome,
        reason_code="no_applicable_policy",
        operation_binding=operation_binding,
        protected_operation_binding=protected_operation_binding,
    )


def test_authorization_audit_outcomes_are_closed_and_stable() -> None:
    assert {
        outcome.value for outcome in AuthorizationAuditOutcome
    } == {
        "allowed",
        "denied",
        "decision_failed",
        "invalid_decision",
        "enforcement_failed",
        "operation_failed",
    }


def test_authorization_audit_record_generates_traceable_defaults() -> None:
    record = make_record()

    assert str(UUID(record.audit_id)) == record.audit_id
    assert record.created_at.tzinfo is not None
    assert record.created_at.utcoffset() == timedelta(0)


@pytest.mark.parametrize(
    "field_name",
    [
        "request_id",
        "subject_id",
        "resource",
        "action",
        "reason_code",
        "audit_id",
    ],
)
def test_authorization_audit_record_normalizes_required_text(
    field_name: str,
) -> None:
    values = {
        "request_id": " request-001 ",
        "subject_id": " aranwill ",
        "resource": " conversation ",
        "action": " write ",
        "outcome": AuthorizationAuditOutcome.DENIED,
        "reason_code": " no_applicable_policy ",
        "audit_id": " audit-001 ",
    }

    record = AuthorizationAuditRecord(**values)

    assert getattr(record, field_name) == values[field_name].strip()


@pytest.mark.parametrize(
    "field_name",
    [
        "request_id",
        "subject_id",
        "resource",
        "action",
        "reason_code",
        "audit_id",
    ],
)
@pytest.mark.parametrize("value", ["", "   "])
def test_authorization_audit_record_rejects_empty_text(
    field_name: str,
    value: str,
) -> None:
    values = {
        "request_id": "request-001",
        "subject_id": "aranwill",
        "resource": "conversation",
        "action": "write",
        "outcome": AuthorizationAuditOutcome.DENIED,
        "reason_code": "no_applicable_policy",
        "audit_id": "audit-001",
    }
    values[field_name] = value

    with pytest.raises(ValueError):
        AuthorizationAuditRecord(**values)


@pytest.mark.parametrize(
    "field_name",
    [
        "request_id",
        "subject_id",
        "resource",
        "action",
        "reason_code",
        "audit_id",
    ],
)
@pytest.mark.parametrize("value", [None, 1, True])
def test_authorization_audit_record_rejects_non_string_text(
    field_name: str,
    value: object,
) -> None:
    values = {
        "request_id": "request-001",
        "subject_id": "aranwill",
        "resource": "conversation",
        "action": "write",
        "outcome": AuthorizationAuditOutcome.DENIED,
        "reason_code": "no_applicable_policy",
        "audit_id": "audit-001",
    }
    values[field_name] = value

    with pytest.raises(TypeError):
        AuthorizationAuditRecord(**values)


def test_authorization_audit_record_requires_closed_outcome() -> None:
    with pytest.raises(TypeError):
        AuthorizationAuditRecord(
            request_id="request-001",
            subject_id="aranwill",
            resource="conversation",
            action="write",
            outcome="denied",
            reason_code="no_applicable_policy",
        )


def test_authorization_audit_record_requires_datetime() -> None:
    with pytest.raises(TypeError):
        AuthorizationAuditRecord(
            request_id="request-001",
            subject_id="aranwill",
            resource="conversation",
            action="write",
            outcome=AuthorizationAuditOutcome.DENIED,
            reason_code="no_applicable_policy",
            created_at="2026-07-28T00:00:00Z",
        )


def test_authorization_audit_record_rejects_naive_datetime() -> None:
    with pytest.raises(ValueError):
        AuthorizationAuditRecord(
            request_id="request-001",
            subject_id="aranwill",
            resource="conversation",
            action="write",
            outcome=AuthorizationAuditOutcome.DENIED,
            reason_code="no_applicable_policy",
            created_at=datetime(2026, 7, 28),
        )


def test_authorization_audit_record_accepts_aware_datetime() -> None:
    created_at = datetime(2026, 7, 28, tzinfo=timezone.utc)

    record = AuthorizationAuditRecord(
        request_id="request-001",
        subject_id="aranwill",
        resource="conversation",
        action="write",
        outcome=AuthorizationAuditOutcome.DENIED,
        reason_code="no_applicable_policy",
        created_at=created_at,
    )

    assert record.created_at == created_at


def test_authorization_audit_record_preserves_legacy_positional_optionals() -> None:
    created_at = datetime(2026, 7, 28, tzinfo=timezone.utc)

    record = AuthorizationAuditRecord(
        "request-001",
        "aranwill",
        "conversation",
        "write",
        AuthorizationAuditOutcome.DENIED,
        "no_applicable_policy",
        "audit-001",
        created_at,
    )

    assert record.audit_id == "audit-001"
    assert record.created_at == created_at
    assert record.operation_binding is None
    assert record.protected_operation_binding is None


def test_authorization_audit_record_is_immutable() -> None:
    record = make_record()

    with pytest.raises(FrozenInstanceError):
        record.reason_code = "replacement"


def test_authorization_audit_record_excludes_sensitive_payloads() -> None:
    record = make_record(
        operation_binding=make_binding("a"),
        protected_operation_binding=make_binding("b"),
    )

    for field_name in (
        "prompt",
        "response",
        "payload",
        "secret",
        "token",
        "credentials",
        "confirmation",
        "exception",
        "stack_trace",
    ):
        assert not hasattr(record, field_name)


def test_authorization_audit_record_preserves_requested_and_actual_bindings() -> None:
    requested = make_binding("a")
    actual = make_binding("b")

    record = make_record(
        operation_binding=requested,
        protected_operation_binding=actual,
    )

    assert record.operation_binding == requested
    assert record.protected_operation_binding == actual


@pytest.mark.parametrize(
    "field_name",
    ["operation_binding", "protected_operation_binding"],
)
def test_authorization_audit_record_rejects_invalid_bindings(
    field_name: str,
) -> None:
    values = {
        "request_id": "request-001",
        "subject_id": "aranwill",
        "resource": "conversation",
        "action": "write",
        "outcome": AuthorizationAuditOutcome.DENIED,
        "reason_code": "no_applicable_policy",
        "operation_binding": None,
        "protected_operation_binding": None,
    }
    values[field_name] = "not-a-binding"

    with pytest.raises(TypeError, match=field_name):
        AuthorizationAuditRecord(**values)
