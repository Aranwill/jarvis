from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4


def _normalize_required_text(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")

    normalized = value.strip()

    if not normalized:
        raise ValueError(f"{field_name} must not be empty")

    return normalized


@dataclass(frozen=True, slots=True)
class PermissionScope:
    resource: str
    action: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "resource",
            _normalize_required_text(self.resource, "resource"),
        )
        object.__setattr__(
            self,
            "action",
            _normalize_required_text(self.action, "action"),
        )


@dataclass(frozen=True, slots=True)
class SecurityContext:
    subject_id: str
    authenticated: bool

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "subject_id",
            _normalize_required_text(self.subject_id, "subject_id"),
        )

        if type(self.authenticated) is not bool:
            raise TypeError("authenticated must be a bool")


@dataclass(frozen=True, slots=True)
class AuthorizationRequest:
    context: SecurityContext
    permission: PermissionScope
    request_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def __post_init__(self) -> None:
        if not isinstance(self.context, SecurityContext):
            raise TypeError("context must be a SecurityContext")

        if not isinstance(self.permission, PermissionScope):
            raise TypeError("permission must be a PermissionScope")

        object.__setattr__(
            self,
            "request_id",
            _normalize_required_text(self.request_id, "request_id"),
        )

        if not isinstance(self.created_at, datetime):
            raise TypeError("created_at must be a datetime")

        if (
            self.created_at.tzinfo is None
            or self.created_at.utcoffset() is None
        ):
            raise ValueError("created_at must include timezone information")


@dataclass(frozen=True, slots=True)
class AuthorizationDecision:
    request_id: str
    allowed: bool
    reason: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "request_id",
            _normalize_required_text(self.request_id, "request_id"),
        )

        if type(self.allowed) is not bool:
            raise TypeError("allowed must be a bool")

        object.__setattr__(
            self,
            "reason",
            _normalize_required_text(self.reason, "reason"),
        )