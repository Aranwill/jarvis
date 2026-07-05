from dataclasses import dataclass


@dataclass(slots=True)
class Response:
    """
    Representa la respuesta generada por Malāk.
    """

    content: str
    source: str = "kernel"