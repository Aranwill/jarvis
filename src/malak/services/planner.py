from malak.core.request import Request


class Planner:
    """
    Minimal deterministic planner.

    The Planner decides which capability
    should handle an incoming request.
    """

    def __init__(
        self,
        capability_name: str = "echo",
    ) -> None:
        self._capability_name = capability_name

    def resolve(self, request: Request) -> str:
        """
        Resolve the capability name.
        """

        return self._capability_name