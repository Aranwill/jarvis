from datetime import datetime, timezone

from malak.runtime.runtime_metric_sample import RuntimeMetricSample
from malak.runtime.runtime_performance_profiler import (
    RuntimePerformanceProfiler,
)


def _create_sample(
    *,
    model: str = "qwen3.5:9b",
    timeout_seconds: float = 600.0,
    total_duration_seconds: float | None = 30.0,
    load_duration_seconds: float | None = 10.0,
    prompt_eval_duration_seconds: float | None = 5.0,
    eval_duration_seconds: float | None = 4.0,
    tokens_per_second: float | None = 25.0,
) -> RuntimeMetricSample:
    return RuntimeMetricSample(
        model=model,
        captured_at=datetime(
            2026,
            7,
            12,
            18,
            0,
            tzinfo=timezone.utc,
        ),
        timeout_seconds=timeout_seconds,
        keep_alive=0,
        total_duration_seconds=total_duration_seconds,
        load_duration_seconds=load_duration_seconds,
        prompt_eval_count=40,
        prompt_eval_duration_seconds=prompt_eval_duration_seconds,
        eval_count=100,
        eval_duration_seconds=eval_duration_seconds,
        tokens_per_second=tokens_per_second,
    )


def test_runtime_performance_profiler_builds_profile() -> None:
    samples = [
        _create_sample(
            timeout_seconds=600.0,
            total_duration_seconds=30.0,
            load_duration_seconds=10.0,
            prompt_eval_duration_seconds=5.0,
            eval_duration_seconds=4.0,
            tokens_per_second=25.0,
        ),
        _create_sample(
            timeout_seconds=900.0,
            total_duration_seconds=60.0,
            load_duration_seconds=20.0,
            prompt_eval_duration_seconds=10.0,
            eval_duration_seconds=8.0,
            tokens_per_second=50.0,
        ),
        _create_sample(
            timeout_seconds=1200.0,
            total_duration_seconds=90.0,
            load_duration_seconds=30.0,
            prompt_eval_duration_seconds=15.0,
            eval_duration_seconds=12.0,
            tokens_per_second=75.0,
        ),
    ]

    profile = RuntimePerformanceProfiler().build(samples)

    assert profile.model == "qwen3.5:9b"
    assert profile.sample_count == 3

    assert profile.total_duration_sample_count == 3
    assert profile.average_total_duration_seconds == 60.0
    assert profile.maximum_total_duration_seconds == 90.0

    assert profile.load_duration_sample_count == 3
    assert profile.average_load_duration_seconds == 20.0
    assert profile.maximum_load_duration_seconds == 30.0

    assert profile.prompt_eval_duration_sample_count == 3
    assert profile.average_prompt_eval_duration_seconds == 10.0

    assert profile.generation_duration_sample_count == 3
    assert profile.average_generation_duration_seconds == 8.0

    assert profile.tokens_per_second_sample_count == 3
    assert profile.average_tokens_per_second == 50.0

    assert profile.average_observed_timeout_seconds == 900.0
    assert profile.minimum_observed_timeout_seconds == 600.0
    assert profile.maximum_observed_timeout_seconds == 1200.0

    assert profile.recommended_timeout_seconds == 150.0
    assert profile.confidence_level == "low"


def test_runtime_performance_profiler_ignores_missing_metric_values() -> None:
    samples = [
        _create_sample(
            total_duration_seconds=40.0,
            load_duration_seconds=None,
            prompt_eval_duration_seconds=5.0,
            eval_duration_seconds=None,
            tokens_per_second=20.0,
        ),
        _create_sample(
            total_duration_seconds=None,
            load_duration_seconds=10.0,
            prompt_eval_duration_seconds=None,
            eval_duration_seconds=8.0,
            tokens_per_second=None,
        ),
    ]

    profile = RuntimePerformanceProfiler().build(samples)

    assert profile.sample_count == 2

    assert profile.total_duration_sample_count == 1
    assert profile.average_total_duration_seconds == 40.0
    assert profile.maximum_total_duration_seconds == 40.0

    assert profile.load_duration_sample_count == 1
    assert profile.average_load_duration_seconds == 10.0
    assert profile.maximum_load_duration_seconds == 10.0

    assert profile.prompt_eval_duration_sample_count == 1
    assert profile.average_prompt_eval_duration_seconds == 5.0

    assert profile.generation_duration_sample_count == 1
    assert profile.average_generation_duration_seconds == 8.0

    assert profile.tokens_per_second_sample_count == 1
    assert profile.average_tokens_per_second == 20.0

    assert profile.recommended_timeout_seconds == 60.0
    assert profile.confidence_level == "low"


def test_runtime_performance_profiler_reports_insufficient_confidence_without_total_duration() -> None:
    samples = [
        _create_sample(
            total_duration_seconds=None,
        ),
        _create_sample(
            total_duration_seconds=None,
        ),
    ]

    profile = RuntimePerformanceProfiler().build(samples)

    assert profile.sample_count == 2
    assert profile.total_duration_sample_count == 0
    assert profile.average_total_duration_seconds is None
    assert profile.maximum_total_duration_seconds is None
    assert profile.recommended_timeout_seconds is None
    assert profile.confidence_level == "insufficient"


def test_runtime_performance_profiler_rejects_empty_collection() -> None:
    try:
        RuntimePerformanceProfiler().build([])
    except ValueError as exc:
        assert "samples" in str(exc)
    else:
        raise AssertionError("Expected ValueError for empty samples")


def test_runtime_performance_profiler_rejects_mixed_models() -> None:
    samples = [
        _create_sample(model="qwen3.5:9b"),
        _create_sample(model="deepseek-coder-v2:16b"),
    ]

    try:
        RuntimePerformanceProfiler().build(samples)
    except ValueError as exc:
        assert "model" in str(exc)
    else:
        raise AssertionError("Expected ValueError for mixed models")

def test_runtime_performance_profiler_uses_medium_confidence_from_five_samples() -> None:
    samples = [
        _create_sample(total_duration_seconds=30.0)
        for _ in range(5)
    ]

    profile = RuntimePerformanceProfiler().build(samples)

    assert profile.confidence_level == "medium"


def test_runtime_performance_profiler_uses_high_confidence_from_twenty_samples() -> None:
    samples = [
        _create_sample(total_duration_seconds=30.0)
        for _ in range(20)
    ]

    profile = RuntimePerformanceProfiler().build(samples)

    assert profile.confidence_level == "high"


def test_runtime_performance_profiler_rounds_timeout_up_to_next_step() -> None:
    samples = [
        _create_sample(total_duration_seconds=40.1),
    ]

    profile = RuntimePerformanceProfiler().build(samples)

    assert profile.recommended_timeout_seconds == 90.0


def test_runtime_performance_profiler_enforces_minimum_timeout() -> None:
    samples = [
        _create_sample(total_duration_seconds=1.0),
    ]

    profile = RuntimePerformanceProfiler().build(samples)

    assert profile.recommended_timeout_seconds == 30.0


def test_runtime_performance_profiler_accepts_iterables() -> None:
    samples = (
        _create_sample(total_duration_seconds=value)
        for value in [30.0, 60.0]
    )

    profile = RuntimePerformanceProfiler().build(samples)

    assert profile.sample_count == 2
    assert profile.average_total_duration_seconds == 45.0