from __future__ import annotations

from dataclasses import dataclass
from typing import Any


NANOSECONDS_PER_SECOND = 1_000_000_000


@dataclass(frozen=True, slots=True)
class RuntimeMetrics:
    """
    Performance metrics captured from a completed runtime execution.

    Duration values are stored in nanoseconds, matching the Ollama API.
    """

    model: str
    total_duration_ns: int | None = None
    load_duration_ns: int | None = None
    prompt_eval_count: int | None = None
    prompt_eval_duration_ns: int | None = None
    eval_count: int | None = None
    eval_duration_ns: int | None = None

    @classmethod
    def from_ollama_payload(
        cls,
        model: str,
        payload: dict[str, Any],
    ) -> "RuntimeMetrics":
        return cls(
            model=model,
            total_duration_ns=_optional_non_negative_int(
                payload.get("total_duration")
            ),
            load_duration_ns=_optional_non_negative_int(
                payload.get("load_duration")
            ),
            prompt_eval_count=_optional_non_negative_int(
                payload.get("prompt_eval_count")
            ),
            prompt_eval_duration_ns=_optional_non_negative_int(
                payload.get("prompt_eval_duration")
            ),
            eval_count=_optional_non_negative_int(
                payload.get("eval_count")
            ),
            eval_duration_ns=_optional_non_negative_int(
                payload.get("eval_duration")
            ),
        )

    @property
    def total_duration_seconds(self) -> float | None:
        return _nanoseconds_to_seconds(self.total_duration_ns)

    @property
    def load_duration_seconds(self) -> float | None:
        return _nanoseconds_to_seconds(self.load_duration_ns)

    @property
    def prompt_eval_duration_seconds(self) -> float | None:
        return _nanoseconds_to_seconds(self.prompt_eval_duration_ns)

    @property
    def eval_duration_seconds(self) -> float | None:
        return _nanoseconds_to_seconds(self.eval_duration_ns)

    @property
    def tokens_per_second(self) -> float | None:
        duration_seconds = self.eval_duration_seconds

        if (
            self.eval_count is None
            or duration_seconds is None
            or duration_seconds <= 0
        ):
            return None

        return self.eval_count / duration_seconds


def _optional_non_negative_int(value: object) -> int | None:
    if isinstance(value, bool):
        return None

    if isinstance(value, int) and value >= 0:
        return value

    return None


def _nanoseconds_to_seconds(value: int | None) -> float | None:
    if value is None:
        return None

    return value / NANOSECONDS_PER_SECOND