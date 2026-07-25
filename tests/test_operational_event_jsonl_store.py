"""Pruebas de la persistencia JSONL de eventos operativos."""

import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from malak.observability.operational_event import OperationalEvent
from malak.observability.operational_event_jsonl_store import (
    DEFAULT_MAX_LINE_BYTES,
    JsonlOperationalEventStore,
)


def _create_event(
    *,
    event_name: str = "conversation.failed",
    outcome: str = "failed",
    request_id: str | None = "request-001",
    reason_code: str | None = "runtime_timeout",
) -> OperationalEvent:
    return OperationalEvent(
        event_name=event_name,
        component="conversation_service",
        occurred_at=datetime(
            2026,
            7,
            24,
            23,
            0,
            tzinfo=timezone.utc,
        ),
        outcome=outcome,
        request_id=request_id,
        reason_code=reason_code,
    )


def test_jsonl_store_uses_expected_default_limit(
    tmp_path: Path,
) -> None:
    store = JsonlOperationalEventStore(
        tmp_path / "operational-events.jsonl"
    )

    assert store._max_line_bytes == DEFAULT_MAX_LINE_BYTES


def test_jsonl_store_writes_valid_allowlisted_payload(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "logs" / "operational-events.jsonl"
    store = JsonlOperationalEventStore(file_path)

    store.append(_create_event())

    lines = file_path.read_text(encoding="utf-8").splitlines()

    assert len(lines) == 1
    assert json.loads(lines[0]) == {
        "event_name": "conversation.failed",
        "component": "conversation_service",
        "occurred_at": "2026-07-24T23:00:00Z",
        "outcome": "failed",
        "request_id": "request-001",
        "reason_code": "runtime_timeout",
    }


def test_jsonl_store_appends_one_line_per_event(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "operational-events.jsonl"
    store = JsonlOperationalEventStore(file_path)

    store.append(
        _create_event(
            event_name="conversation.started",
            outcome="started",
            request_id="request-001",
            reason_code=None,
        )
    )
    store.append(
        _create_event(
            event_name="conversation.failed",
            outcome="failed",
            request_id="request-001",
            reason_code="runtime_timeout",
        )
    )

    lines = file_path.read_text(encoding="utf-8").splitlines()

    assert len(lines) == 2
    assert json.loads(lines[0])["outcome"] == "started"
    assert json.loads(lines[1])["outcome"] == "failed"


def test_jsonl_store_preserves_unicode_as_utf8(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "operational-events.jsonl"
    store = JsonlOperationalEventStore(file_path)

    event = OperationalEvent(
        event_name="conversación.iniciada",
        component="servicio_conversación",
        occurred_at=datetime(
            2026,
            7,
            24,
            23,
            0,
            tzinfo=timezone.utc,
        ),
        outcome="started",
    )

    store.append(event)

    stored_text = file_path.read_text(encoding="utf-8")

    assert "conversación.iniciada" in stored_text
    assert "\\u00f3" not in stored_text


def test_jsonl_store_accepts_line_at_exact_byte_limit(
    tmp_path: Path,
) -> None:
    event = _create_event()
    expected_payload = {
        "event_name": event.event_name,
        "component": event.component,
        "occurred_at": "2026-07-24T23:00:00Z",
        "outcome": event.outcome,
        "request_id": event.request_id,
        "reason_code": event.reason_code,
    }
    expected_line = (
        json.dumps(
            expected_payload,
            ensure_ascii=False,
            separators=(",", ":"),
        )
        + "\n"
    )
    exact_limit = len(expected_line.encode("utf-8"))
    file_path = tmp_path / "operational-events.jsonl"
    store = JsonlOperationalEventStore(
        file_path,
        max_line_bytes=exact_limit,
    )

    store.append(event)

    assert file_path.read_bytes() == expected_line.encode("utf-8")


def test_jsonl_store_rejects_line_over_byte_limit_before_writing(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "logs" / "operational-events.jsonl"
    store = JsonlOperationalEventStore(
        file_path,
        max_line_bytes=1,
    )

    with pytest.raises(
        ValueError,
        match="serialized operational event exceeds max_line_bytes",
    ):
        store.append(_create_event())

    assert not file_path.exists()
    assert not file_path.parent.exists()


@pytest.mark.parametrize("max_line_bytes", [0, -1])
def test_jsonl_store_rejects_non_positive_limits(
    tmp_path: Path,
    max_line_bytes: int,
) -> None:
    with pytest.raises(
        ValueError,
        match="max_line_bytes must be greater than zero",
    ):
        JsonlOperationalEventStore(
            tmp_path / "operational-events.jsonl",
            max_line_bytes=max_line_bytes,
        )


@pytest.mark.parametrize("max_line_bytes", [True, 1.5, "4096"])
def test_jsonl_store_rejects_non_integer_limits(
    tmp_path: Path,
    max_line_bytes: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="max_line_bytes must be an integer",
    ):
        JsonlOperationalEventStore(
            tmp_path / "operational-events.jsonl",
            max_line_bytes=max_line_bytes,  # type: ignore[arg-type]
        )


def test_jsonl_store_rejects_non_operational_event_before_writing(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "logs" / "operational-events.jsonl"
    store = JsonlOperationalEventStore(file_path)

    with pytest.raises(
        TypeError,
        match="event must be an OperationalEvent",
    ):
        store.append(object())  # type: ignore[arg-type]

    assert not file_path.exists()
    assert not file_path.parent.exists()


def test_jsonl_store_propagates_file_system_errors(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    file_path = tmp_path / "operational-events.jsonl"
    store = JsonlOperationalEventStore(file_path)

    def raise_file_system_error(
        path: Path,
        *args: object,
        **kwargs: object,
    ) -> None:
        raise OSError("disk unavailable")

    monkeypatch.setattr(Path, "open", raise_file_system_error)

    with pytest.raises(OSError, match="disk unavailable"):
        store.append(_create_event())