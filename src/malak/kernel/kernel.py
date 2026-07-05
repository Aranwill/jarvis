from malak.core.request import Request
from malak.core.response import Response
from malak.kernel.bootstrap import create_registry
from malak.services.planner import Planner


class Kernel:
    """
    Minimal governing Kernel for Malāk.
    """

    def __init__(self) -> None:
        self._planner = Planner()
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

        capability_name = self._planner.resolve(request)

        capability = self._registry.get(capability_name)

        if capability is None:
            return Response(
                content=f"Capability '{capability_name}' no encontrada.",
                source="kernel",
            )

        result = capability.execute(request.content)

        return Response(
            content=result,
            source=capability.name,
        )