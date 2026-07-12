from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from malak.runtime.runtime_metrics import RuntimeMetrics


@dataclass(frozen=True, slots=True)
class RuntimeMetricSample:
    """
    Immutable snapshot of one completed runtime execution.

    The sample stores normalized values suitable for future persistence,
    aggregation and per-model performance profiling.
    """

    model: str
    captured_at: datetime
    timeout_seconds: float
    keep_alive: int | str

    total_duration_seconds: float | None
    load_duration_seconds: float | None

    prompt_eval_count: int | None
    prompt_eval_duration_seconds: float | None

    eval_count: int | None
    eval_duration_seconds: float | None

    tokens_per_second: float | None

    @classmethod
    def from_runtime_metrics(
        cls,
        metrics: RuntimeMetrics,
        timeout_seconds: float,
        keep_alive: int | str,
        captured_at: datetime | None = None,
    ) -> "RuntimeMetricSample":
        if timeout_seconds <= 0:
            raise ValueError(
                "timeout_seconds must be greater than zero"
            )

        resolved_captured_at = captured_at or datetime.now(timezone.utc)

        if (
            resolved_captured_at.tzinfo is None
            or resolved_captured_at.utcoffset() is None
        ):
            raise ValueError(
                "captured_at must include timezone information"
            )

        if not metrics.model.strip():
            raise ValueError("metrics model must not be empty")

        return cls(
            model=metrics.model,
            captured_at=resolved_captured_at,
            timeout_seconds=float(timeout_seconds),
            keep_alive=keep_alive,
            total_duration_seconds=metrics.total_duration_seconds,
            load_duration_seconds=metrics.load_duration_seconds,
            prompt_eval_count=metrics.prompt_eval_count,
            prompt_eval_duration_seconds=(
                metrics.prompt_eval_duration_seconds
            ),
            eval_count=metrics.eval_count,
            eval_duration_seconds=metrics.eval_duration_seconds,
            tokens_per_second=metrics.tokens_per_second,
        )