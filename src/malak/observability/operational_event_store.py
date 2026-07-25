"""Almacenamiento en memoria para eventos operativos de Malāk."""

from malak.observability.operational_event import OperationalEvent


class InMemoryOperationalEventStore:
    """Conserva eventos operativos en memoria y en orden de inserción."""

    def __init__(self) -> None:
        self._events: list[OperationalEvent] = []

    def append(self, event: OperationalEvent) -> None:
        """Agrega un evento al almacenamiento."""
        self._events.append(event)

    def list_all(self) -> list[OperationalEvent]:
        """Devuelve una copia de todos los eventos almacenados."""
        return list(self._events)