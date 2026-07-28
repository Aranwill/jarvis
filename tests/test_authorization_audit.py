from dataclasses import FrozenInstanceError
from datetime import datetime, timedelta, timezone
from uuid import UUID

import pytest

from malak.security import (
    AuthorizationAuditOutcome,
    AuthorizationAuditRecord,
    AuthorizationAuditSink,
    InMemoryAuthorizationAuditStore,
)


def make_record(
    *,
    outcome: AuthorizationAuditOutcome = (
        AuthorizationAuditOutcome.DENIED
    ),
) -> AuthorizationAuditRecord:
    return AuthorizationAuditRecord(
        request_id="request-001",
        subject_id="aranwill",
        resource="conversation",
        action="write",
        outcome=outcome,
        reason_code="no_applicable_policy",
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


def test_authorization_audit_record_is_immutable() -> None:
    record = make_record()

    with pytest.raises(FrozenInstanceError):
        record.reason_code = "replacement"


def test_authorization_audit_record_excludes_sensitive_payloads() -> None:
    record = make_record()

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


def test_in_memory_store_appends_records_in_order() -> None:
    store = InMemoryAuthorizationAuditStore()
    first = make_record(outcome=AuthorizationAuditOutcome.DENIED)
    second = make_record(outcome=AuthorizationAuditOutcome.ALLOWED)

    store.write(first)
    store.write(second)

    assert store.records == (first, second)


def test_in_memory_store_returns_immutable_projection() -> None:
    store = InMemoryAuthorizationAuditStore()
    store.write(make_record())

    records = store.records

    assert isinstance(records, tuple)


def test_in_memory_store_rejects_invalid_records() -> None:
    store = InMemoryAuthorizationAuditStore()

    with pytest.raises(TypeError):
        store.write("invalid")


def test_in_memory_store_satisfies_sink_protocol() -> None:
    sink: AuthorizationAuditSink = InMemoryAuthorizationAuditStore()

    sink.write(make_record())