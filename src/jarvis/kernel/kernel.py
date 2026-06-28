from jarvis.core.request import Request
from jarvis.core.response import Response


class Kernel:
    """
    Núcleo mínimo gobernante de Jarvis.
    """

    def receive(self, request: Request) -> Response:
        """
        Punto de entrada del sistema.
        """

        if not request.content.strip():
            return Response(
                content="La solicitud está vacía.",
                source="kernel",
            )

        return Response(
            content=request.content,
            source="kernel",
        )