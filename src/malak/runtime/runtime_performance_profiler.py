from __future__ import annotations

from math import ceil
from statistics import fmean
from typing import Iterable

from malak.runtime.runtime_metric_sample import RuntimeMetricSample
from malak.runtime.runtime_performance_profile import (
    RuntimePerformanceProfile,
)


class RuntimePerformanceProfiler:
    """
    Builds a descriptive performance profile from runtime metric samples.

    This component performs pure statistical aggregation. It does not read
    persistent stores, invoke runtimes, or apply configuration changes.
    """

    _TIMEOUT_SAFETY_FACTOR = 1.50
    _TIMEOUT_ROUNDING_STEP_SECONDS = 30.0
    _MINIMUM_RECOMMENDED_TIMEOUT_SECONDS = 30.0

    def build(
        self,
        samples: Iterable[RuntimeMetricSample],
    ) -> RuntimePerformanceProfile:
        resolved_samples = list(samples)

        if not resolved_samples:
            raise ValueError("samples must not be empty")

        model = resolved_samples[0].model

        if any(sample.model != model for sample in resolved_samples):
            raise ValueError("all samples must belong to the same model")

        total_durations = self._present_values(
            sample.total_duration_seconds
            for sample in resolved_samples
        )
        load_durations = self._present_values(
            sample.load_duration_seconds
            for sample in resolved_samples
        )
        prompt_eval_durations = self._present_values(
            sample.prompt_eval_duration_seconds
            for sample in resolved_samples
        )
        generation_durations = self._present_values(
            sample.eval_duration_seconds
            for sample in resolved_samples
        )
        tokens_per_second_values = self._present_values(
            sample.tokens_per_second
            for sample in resolved_samples
        )

        timeout_values = [
            sample.timeout_seconds
            for sample in resolved_samples
        ]

        maximum_total_duration = self._maximum_or_none(
            total_durations
        )

        return RuntimePerformanceProfile(
            model=model,
            sample_count=len(resolved_samples),
            total_duration_sample_count=len(total_durations),
            average_total_duration_seconds=self._average_or_none(
                total_durations
            ),
            maximum_total_duration_seconds=maximum_total_duration,
            load_duration_sample_count=len(load_durations),
            average_load_duration_seconds=self._average_or_none(
                load_durations
            ),
            maximum_load_duration_seconds=self._maximum_or_none(
                load_durations
            ),
            prompt_eval_duration_sample_count=len(
                prompt_eval_durations
            ),
            average_prompt_eval_duration_seconds=self._average_or_none(
                prompt_eval_durations
            ),
            generation_duration_sample_count=len(
                generation_durations
            ),
            average_generation_duration_seconds=self._average_or_none(
                generation_durations
            ),
            tokens_per_second_sample_count=len(
                tokens_per_second_values
            ),
            average_tokens_per_second=self._average_or_none(
                tokens_per_second_values
            ),
            average_observed_timeout_seconds=fmean(timeout_values),
            minimum_observed_timeout_seconds=min(timeout_values),
            maximum_observed_timeout_seconds=max(timeout_values),
            recommended_timeout_seconds=self._recommend_timeout(
                maximum_total_duration
            ),
            confidence_level=self._confidence_level(
                len(total_durations)
            ),
        )

    @staticmethod
    def _present_values(
        values: Iterable[float | None],
    ) -> list[float]:
        return [
            value
            for value in values
            if value is not None
        ]

    @staticmethod
    def _average_or_none(
        values: list[float],
    ) -> float | None:
        if not values:
            return None

        return fmean(values)

    @staticmethod
    def _maximum_or_none(
        values: list[float],
    ) -> float | None:
        if not values:
            return None

        return max(values)

    def _recommend_timeout(
        self,
        maximum_total_duration_seconds: float | None,
    ) -> float | None:
        if maximum_total_duration_seconds is None:
            return None

        buffered_timeout = (
            maximum_total_duration_seconds
            * self._TIMEOUT_SAFETY_FACTOR
        )

        rounded_timeout = (
            ceil(
                buffered_timeout
                / self._TIMEOUT_ROUNDING_STEP_SECONDS
            )
            * self._TIMEOUT_ROUNDING_STEP_SECONDS
        )

        return max(
            rounded_timeout,
            self._MINIMUM_RECOMMENDED_TIMEOUT_SECONDS,
        )

    @staticmethod
    def _confidence_level(
        valid_total_duration_count: int,
    ) -> str:
        if valid_total_duration_count == 0:
            return "insufficient"

        if valid_total_duration_count < 5:
            return "low"

        if valid_total_duration_count < 20:
            return "medium"

        return "high"