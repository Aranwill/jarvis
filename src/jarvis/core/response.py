from dataclasses import dataclass


@dataclass(slots=True)
class Response:
    """
    Representa la respuesta generada por Jarvis.
    """

    content: str
    source: str = "kernel"