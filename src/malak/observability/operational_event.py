"""Contrato mínimo para eventos operativos seguros de Malāk."""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Final


ALLOWED_OUTCOMES: Final[frozenset[str]] = frozenset(
    {
        "started",
        "succeeded",
        "failed",
    }
)

ALLOWED_REASON_CODES: Final[frozenset[str]] = frozenset(
    {
        "validation_failed",
        "runtime_error",
        "runtime_timeout",
        "policy_denied",
        "dependency_unavailable",
        "operation_cancelled",
    }
)


@dataclass(frozen=True, slots=True)
class OperationalEvent:
    """Representa un acontecimiento operativo mínimo y estructurado."""

    event_name: str
    component: str
    occurred_at: datetime
    outcome: str
    request_id: str | None = None
    reason_code: str | None = None

    def __post_init__(self) -> None:
        """Valida las invariantes del contrato."""

        self._validate_non_empty_identifier("event_name", self.event_name)
        self._validate_non_empty_identifier("component", self.component)

        if self.request_id is not None:
            self._validate_non_empty_identifier("request_id", self.request_id)

        if self.outcome not in ALLOWED_OUTCOMES:
            allowed = ", ".join(sorted(ALLOWED_OUTCOMES))
            raise ValueError(
                f"outcome must be one of: {allowed}"
            )

        if self.reason_code is not None:
            if self.reason_code not in ALLOWED_REASON_CODES:
                allowed = ", ".join(sorted(ALLOWED_REASON_CODES))
                raise ValueError(
                    f"reason_code must be one of: {allowed}"
                )

            if self.outcome != "failed":
                raise ValueError(
                    "reason_code can only be provided when outcome is failed"
                )

        if self.occurred_at.tzinfo is None:
            raise ValueError("occurred_at must be timezone-aware")

        if self.occurred_at.utcoffset() != timedelta(0):
            raise ValueError("occurred_at must use UTC")

    @staticmethod
    def _validate_non_empty_identifier(field_name: str, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"{field_name} must be a string")

        if not value.strip():
            raise ValueError(f"{field_name} must not be empty")

        if value != value.strip():
            raise ValueError(
                f"{field_name} must not contain surrounding whitespace"
            )