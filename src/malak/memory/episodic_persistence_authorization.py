from datetime import datetime

from malak.memory.episodic_persistence_readiness import (
    EpisodicPersistenceReadinessOutcome,
    EpisodicPersistenceReadinessReason,
    EpisodicPersistenceReadinessResult,
)
from malak.security.contracts import (
    AuthorizationRequest,
    PermissionScope,
    SecurityContext,
)


def compose_episodic_persistence_authorization_request(
    readiness: EpisodicPersistenceReadinessResult,
    security_context: SecurityContext,
    created_at: datetime,
) -> AuthorizationRequest:
    if not isinstance(readiness, EpisodicPersistenceReadinessResult):
        raise TypeError(
            "readiness must be an EpisodicPersistenceReadinessResult"
        )

    if not isinstance(security_context, SecurityContext):
        raise TypeError("security_context must be a SecurityContext")

    if not isinstance(created_at, datetime):
        raise TypeError("created_at must be a datetime")

    if created_at.tzinfo is None or created_at.utcoffset() is None:
        raise ValueError("created_at must include timezone information")

    if (
        readiness.outcome is not EpisodicPersistenceReadinessOutcome.READY
        or readiness.reason_code
        is not EpisodicPersistenceReadinessReason.READY
    ):
        raise ValueError("readiness must be READY")

    operation_binding = readiness.authorization_operation_binding
    if operation_binding is None:
        raise ValueError("READY readiness must include operation binding")

    if not (
        security_context.issued_at
        <= created_at
        < security_context.expires_at
    ):
        raise ValueError(
            "created_at must be within the SecurityContext lifecycle"
        )

    return AuthorizationRequest(
        context=security_context,
        permission=PermissionScope(
            resource="memory.episodic",
            action="persist",
        ),
        created_at=created_at,
        operation_binding=operation_binding,
    )
