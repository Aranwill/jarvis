from malak.security.clock import Clock
from malak.security.contracts import SecurityContext


class SecurityContextValidator:
    def __init__(self, clock: Clock) -> None:
        self._clock = clock

    def is_valid(self, context: SecurityContext) -> bool:
        return self._clock.now() < context.expires_at