from malak.core.request import Request


class Planner:
    """
    Minimal deterministic planner.

    The Planner decides which capability
    should handle an incoming request.
    """

    def resolve(self, request: Request) -> str:
        """
        Resolve the capability name.

        MVP:
        Always returns the Echo capability.
        """

        return "echo"
        