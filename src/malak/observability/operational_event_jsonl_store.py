"""Persistencia JSONL para eventos operativos de Malāk."""

import json
from pathlib import Path
from typing import Final

from malak.observability.operational_event import OperationalEvent


DEFAULT_MAX_LINE_BYTES: Final[int] = 4096


class JsonlOperationalEventStore:
    """Persiste eventos operativos como líneas JSON independientes."""

    def __init__(
        self,
        file_path: str | Path,
        max_line_bytes: int = DEFAULT_MAX_LINE_BYTES,
    ) -> None:
        if isinstance(max_line_bytes, bool) or not isinstance(max_line_bytes, int):
            raise TypeError("max_line_bytes must be an integer")

        if max_line_bytes <= 0:
            raise ValueError("max_line_bytes must be greater than zero")

        self._file_path = Path(file_path)
        self._max_line_bytes = max_line_bytes

    def append(self, event: OperationalEvent) -> None:
        """Serializa y agrega un evento al archivo JSONL."""

        if not isinstance(event, OperationalEvent):
            raise TypeError("event must be an OperationalEvent")

        payload = {
            "event_name": event.event_name,
            "component": event.component,
            "occurred_at": event.occurred_at.isoformat().replace(
                "+00:00",
                "Z",
            ),
            "outcome": event.outcome,
            "request_id": event.request_id,
            "reason_code": event.reason_code,
        }

        serialized_line = (
            json.dumps(
                payload,
                ensure_ascii=False,
                separators=(",", ":"),
            )
            + "\n"
        )

        line_size = len(serialized_line.encode("utf-8"))

        if line_size > self._max_line_bytes:
            raise ValueError(
                "serialized operational event exceeds max_line_bytes"
            )

        self._file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with self._file_path.open(
            "a",
            encoding="utf-8",
            newline="\n",
        ) as jsonl_file:
            jsonl_file.write(serialized_line)