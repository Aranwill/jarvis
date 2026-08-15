from dataclasses import dataclass

from malak.security.contracts import SecurityContext


@dataclass(frozen=True, slots=True)
class SecurityContextEnvelope:
    context: SecurityContext

    def __post_init__(self) -> None:
        if not isinstance(self.context, SecurityContext):
            raise TypeError("context must be a SecurityContext")