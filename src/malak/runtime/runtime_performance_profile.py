from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RuntimePerformanceProfile:
    """
    Immutable statistical profile built from runtime metric samples.

    The profile is descriptive only. It does not modify runtime configuration
    or apply timeout policies automatically.
    """

    model: str
    sample_count: int

    total_duration_sample_count: int
    average_total_duration_seconds: float | None
    maximum_total_duration_seconds: float | None

    load_duration_sample_count: int
    average_load_duration_seconds: float | None
    maximum_load_duration_seconds: float | None

    prompt_eval_duration_sample_count: int
    average_prompt_eval_duration_seconds: float | None

    generation_duration_sample_count: int
    average_generation_duration_seconds: float | None

    tokens_per_second_sample_count: int
    average_tokens_per_second: float | None

    average_observed_timeout_seconds: float
    minimum_observed_timeout_seconds: float
    maximum_observed_timeout_seconds: float

    recommended_timeout_seconds: float | None
    confidence_level: str