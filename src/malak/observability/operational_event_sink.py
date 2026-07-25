"""Contrato de recepción de eventos operativos de Malāk."""

from typing import Protocol

from malak.observability.operational_event import OperationalEvent


class OperationalEventSink(Protocol):
    """Define un destino capaz de recibir eventos operativos."""

    def append(self, event: OperationalEvent) -> None:
        """Recibe un evento operativo."""
        ...