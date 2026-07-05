from malak.core.request import Request
from malak.core.response import Response
from malak.kernel.bootstrap import create_registry


class Kernel:
    """
    Minimal governing Kernel for Malāk.
    """

    def __init__(self) -> None:
        self._registry = create_registry()

    def receive(self, request: Request) -> Response:
        """
        System entry point.
        """

        if not request.content.strip():
            return Response(
                content="La solicitud está vacía.",
                source="kernel",
            )

        capability = self._registry.get("echo")

        if capability is None:
            return Response(
                content="Capability 'echo' no encontrada.",
                source="kernel",
            )

        result = capability.execute(request.content)

        return Response(
            content=result,
            source=capability.name,
        )