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
    context_id: str
    session_id: str
    subject_id: str
    authenticated: bool
    issued_at: datetime
    expires_at: datetime
    parent_context_id: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "context_id",
            _normalize_required_text(self.context_id, "context_id"),
        )
        object.__setattr__(
            self,
            "session_id",
            _normalize_required_text(self.session_id, "session_id"),
        )
        object.__setattr__(
            self,
            "subject_id",
            _normalize_required_text(self.subject_id, "subject_id"),
        )

        if type(self.authenticated) is not bool:
            raise TypeError("authenticated must be a bool")

        if not isinstance(self.issued_at, datetime):
            raise TypeError("issued_at must be a datetime")

        if not isinstance(self.expires_at, datetime):
            raise TypeError("expires_at must be a datetime")

        if self.issued_at.tzinfo is None or self.issued_at.utcoffset() is None:
            raise ValueError("issued_at must include timezone information")

        if self.expires_at.tzinfo is None or self.expires_at.utcoffset() is None:
            raise ValueError("expires_at must include timezone information")

        if self.expires_at <= self.issued_at:
            raise ValueError("expires_at must be after issued_at")

        if self.parent_context_id is not None:
            object.__setattr__(
                self,
                "parent_context_id",
                _normalize_required_text(
                    self.parent_context_id,
                    "parent_context_id",
                ),
            )


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
class HumanConfirmationEvidence:
    confirmation_id: str
    original_request_id: str
    new_request_id: str
    subject_id: str
    permission: PermissionScope
    confirmed_by: str
    confirmed_at: datetime

    def __post_init__(self) -> None:
        for field_name in (
            "confirmation_id",
            "original_request_id",
            "new_request_id",
            "subject_id",
            "confirmed_by",
        ):
            object.__setattr__(
                self,
                field_name,
                _normalize_required_text(
                    getattr(self, field_name),
                    field_name,
                ),
            )

        if self.original_request_id == self.new_request_id:
            raise ValueError(
                "new_request_id must differ from original_request_id"
            )

        if not isinstance(self.permission, PermissionScope):
            raise TypeError("permission must be a PermissionScope")

        if not isinstance(self.confirmed_at, datetime):
            raise TypeError("confirmed_at must be a datetime")

        if (
            self.confirmed_at.tzinfo is None
            or self.confirmed_at.utcoffset() is None
        ):
            raise ValueError("confirmed_at must include timezone information")


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