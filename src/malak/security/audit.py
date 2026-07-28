from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Protocol
from uuid import uuid4


def _normalize_required_text(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")

    normalized = value.strip()

    if not normalized:
        raise ValueError(f"{field_name} must not be empty")

    return normalized


class AuthorizationAuditOutcome(str, Enum):
    ALLOWED = "allowed"
    DENIED = "denied"
    DECISION_FAILED = "decision_failed"
    INVALID_DECISION = "invalid_decision"
    ENFORCEMENT_FAILED = "enforcement_failed"
    OPERATION_FAILED = "operation_failed"


@dataclass(frozen=True, slots=True)
class AuthorizationAuditRecord:
    request_id: str
    subject_id: str
    resource: str
    action: str
    outcome: AuthorizationAuditOutcome
    reason_code: str
    audit_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def __post_init__(self) -> None:
        for field_name in (
            "request_id",
            "subject_id",
            "resource",
            "action",
            "reason_code",
            "audit_id",
        ):
            object.__setattr__(
                self,
                field_name,
                _normalize_required_text(
                    getattr(self, field_name),
                    field_name,
                ),
            )

        if not isinstance(self.outcome, AuthorizationAuditOutcome):
            raise TypeError(
                "outcome must be an AuthorizationAuditOutcome"
            )

        if not isinstance(self.created_at, datetime):
            raise TypeError("created_at must be a datetime")

        if (
            self.created_at.tzinfo is None
            or self.created_at.utcoffset() is None
        ):
            raise ValueError(
                "created_at must include timezone information"
            )


class AuthorizationAuditSink(Protocol):
    def write(self, record: AuthorizationAuditRecord) -> None:
        ...


class InMemoryAuthorizationAuditStore:
    def __init__(self) -> None:
        self._records: list[AuthorizationAuditRecord] = []

    def write(self, record: AuthorizationAuditRecord) -> None:
        if not isinstance(record, AuthorizationAuditRecord):
            raise TypeError(
                "record must be an AuthorizationAuditRecord"
            )

        self._records.append(record)

    @property
    def records(self) -> tuple[AuthorizationAuditRecord, ...]:
        return tuple(self._records)