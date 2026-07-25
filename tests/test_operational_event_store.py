"""Pruebas del almacenamiento en memoria de eventos operativos."""

from datetime import datetime, timezone

from malak.observability.operational_event import OperationalEvent
from malak.observability.operational_event_store import (
    InMemoryOperationalEventStore,
)


def _create_event(
    event_name: str,
    outcome: str,
) -> OperationalEvent:
    return OperationalEvent(
        event_name=event_name,
        component="conversation_service",
        occurred_at=datetime(2026, 7, 24, 23, 0, tzinfo=timezone.utc),
        outcome=outcome,
    )


def test_operational_event_store_starts_empty() -> None:
    store = InMemoryOperationalEventStore()

    assert store.list_all() == []


def test_operational_event_store_appends_and_lists_events() -> None:
    store = InMemoryOperationalEventStore()

    first_event = _create_event(
        event_name="conversation.started",
        outcome="started",
    )
    second_event = _create_event(
        event_name="conversation.succeeded",
        outcome="succeeded",
    )

    store.append(first_event)
    store.append(second_event)

    assert store.list_all() == [
        first_event,
        second_event,
    ]


def test_operational_event_store_returns_defensive_copies() -> None:
    store = InMemoryOperationalEventStore()
    event = _create_event(
        event_name="conversation.started",
        outcome="started",
    )
    store.append(event)

    returned_events = store.list_all()
    returned_events.clear()

    assert store.list_all() == [event]