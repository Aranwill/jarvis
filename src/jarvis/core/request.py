from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass(slots=True)
class Request:
    """
    Representa una solicitud que ingresa al Kernel.
    """

    content: str
    session_id: str

    request_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=datetime.utcnow)