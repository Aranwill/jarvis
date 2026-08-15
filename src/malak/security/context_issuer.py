from datetime import timedelta
from uuid import uuid4

from malak.security.clock import Clock
from malak.security.contracts import SecurityContext


class SecurityContextIssuer:
    def __init__(self, clock: Clock) -> None:
        self._clock = clock

    def issue(
        self,
        *,
        session_id: str,
        subject_id: str,
        authenticated: bool,
        lifetime: timedelta,
        parent_context_id: str | None = None,
    ) -> SecurityContext:
        if not isinstance(lifetime, timedelta):
            raise TypeError("lifetime must be a timedelta")

        if lifetime <= timedelta(0):
            raise ValueError("lifetime must be positive")

        issued_at = self._clock.now()

        return SecurityContext(
            context_id=str(uuid4()),
            session_id=session_id,
            subject_id=subject_id,
            authenticated=authenticated,
            issued_at=issued_at,
            expires_at=issued_at + lifetime,
            parent_context_id=parent_context_id,
        )