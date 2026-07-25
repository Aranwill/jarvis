"""Pruebas del contrato OperationalEvent."""

from dataclasses import FrozenInstanceError
from datetime import datetime, timedelta, timezone

import pytest

from malak.observability import OperationalEvent


def test_operational_event_accepts_valid_minimal_event() -> None:
    occurred_at = datetime(2026, 7, 24, 23, 0, tzinfo=timezone.utc)

    event = OperationalEvent(
        event_name="conversation.started",
        component="conversation_service",
        occurred_at=occurred_at,
        outcome="started",
    )

    assert event.event_name == "conversation.started"
    assert event.component == "conversation_service"
    assert event.occurred_at == occurred_at
    assert event.outcome == "started"
    assert event.request_id is None
    assert event.reason_code is None


def test_operational_event_accepts_failed_event_with_reason_code() -> None:
    event = OperationalEvent(
        event_name="conversation.failed",
        component="conversation_service",
        occurred_at=datetime.now(timezone.utc),
        outcome="failed",
        request_id="request-001",
        reason_code="runtime_timeout",
    )

    assert event.request_id == "request-001"
    assert event.reason_code == "runtime_timeout"


def test_operational_event_is_immutable() -> None:
    event = OperationalEvent(
        event_name="conversation.succeeded",
        component="conversation_service",
        occurred_at=datetime.now(timezone.utc),
        outcome="succeeded",
    )

    with pytest.raises(FrozenInstanceError):
        event.outcome = "failed"  # type: ignore[misc]


def test_operational_event_uses_slots() -> None:
    event = OperationalEvent(
        event_name="conversation.started",
        component="conversation_service",
        occurred_at=datetime.now(timezone.utc),
        outcome="started",
    )

    assert not hasattr(event, "__dict__")


@pytest.mark.parametrize(
    ("field_name", "field_value"),
    [
        ("event_name", ""),
        ("event_name", "   "),
        ("event_name", " conversation.started"),
        ("component", ""),
        ("component", "   "),
        ("component", "conversation_service "),
    ],
)
def test_operational_event_rejects_invalid_required_identifiers(
    field_name: str,
    field_value: str,
) -> None:
    arguments = {
        "event_name": "conversation.started",
        "component": "conversation_service",
        "occurred_at": datetime.now(timezone.utc),
        "outcome": "started",
    }
    arguments[field_name] = field_value

    with pytest.raises(ValueError):
        OperationalEvent(**arguments)  # type: ignore[arg-type]


@pytest.mark.parametrize("request_id", ["", "   ", " request-001", "request-001 "])
def test_operational_event_rejects_invalid_request_id(
    request_id: str,
) -> None:
    with pytest.raises(ValueError):
        OperationalEvent(
            event_name="conversation.started",
            component="conversation_service",
            occurred_at=datetime.now(timezone.utc),
            outcome="started",
            request_id=request_id,
        )


def test_operational_event_rejects_naive_datetime() -> None:
    with pytest.raises(
        ValueError,
        match="occurred_at must be timezone-aware",
    ):
        OperationalEvent(
            event_name="conversation.started",
            component="conversation_service",
            occurred_at=datetime(2026, 7, 24, 23, 0),
            outcome="started",
        )


def test_operational_event_rejects_non_utc_datetime() -> None:
    non_utc_timezone = timezone(timedelta(hours=-3))

    with pytest.raises(
        ValueError,
        match="occurred_at must use UTC",
    ):
        OperationalEvent(
            event_name="conversation.started",
            component="conversation_service",
            occurred_at=datetime.now(non_utc_timezone),
            outcome="started",
        )


@pytest.mark.parametrize("outcome", ["", "completed", "success", "FAILED"])
def test_operational_event_rejects_unknown_outcome(outcome: str) -> None:
    with pytest.raises(
        ValueError,
        match="outcome must be one of",
    ):
        OperationalEvent(
            event_name="conversation.finished",
            component="conversation_service",
            occurred_at=datetime.now(timezone.utc),
            outcome=outcome,
        )


def test_operational_event_rejects_unknown_reason_code() -> None:
    with pytest.raises(
        ValueError,
        match="reason_code must be one of",
    ):
        OperationalEvent(
            event_name="conversation.failed",
            component="conversation_service",
            occurred_at=datetime.now(timezone.utc),
            outcome="failed",
            reason_code="raw_exception_message",
        )


@pytest.mark.parametrize("outcome", ["started", "succeeded"])
def test_operational_event_rejects_reason_code_for_non_failed_outcome(
    outcome: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="reason_code can only be provided when outcome is failed",
    ):
        OperationalEvent(
            event_name="conversation.event",
            component="conversation_service",
            occurred_at=datetime.now(timezone.utc),
            outcome=outcome,
            reason_code="runtime_timeout",
        )