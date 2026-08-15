from malak.security.clock import Clock
from malak.security.contracts import SecurityContext


class SecurityContextValidator:
    def __init__(self, clock: Clock) -> None:
        self._clock = clock

    def is_valid(self, context: SecurityContext) -> bool:
        current_time = self._clock.now()
        return context.issued_at <= current_time < context.expires_at