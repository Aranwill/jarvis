"""Pruebas del contrato OperationalEventSink."""

from malak.observability.operational_event_sink import OperationalEventSink
from malak.observability.operational_event_store import (
    InMemoryOperationalEventStore,
)


def _accepts_operational_event_sink(
    sink: OperationalEventSink,
) -> OperationalEventSink:
    return sink


def test_in_memory_store_satisfies_operational_event_sink() -> None:
    sink: OperationalEventSink = InMemoryOperationalEventStore()

    assert _accepts_operational_event_sink(sink) is not None