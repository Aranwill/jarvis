from datetime import datetime, timezone

from malak.runtime.runtime_metric_sample import RuntimeMetricSample
from malak.runtime.runtime_metrics import RuntimeMetrics


def test_runtime_metric_sample_is_created_from_runtime_metrics() -> None:
    captured_at = datetime(
        2026,
        7,
        12,
        18,
        30,
        tzinfo=timezone.utc,
    )

    metrics = RuntimeMetrics(
        model="qwen3.5:9b",
        total_duration_ns=32_604_833_900,
        load_duration_ns=12_737_770_740,
        prompt_eval_count=38,
        prompt_eval_duration_ns=12_251_242_000,
        eval_count=340,
        eval_duration_ns=7_608_376_000,
    )

    sample = RuntimeMetricSample.from_runtime_metrics(
        metrics=metrics,
        timeout_seconds=600.0,
        keep_alive=0,
        captured_at=captured_at,
    )

    assert sample.model == "qwen3.5:9b"
    assert sample.captured_at == captured_at
    assert sample.timeout_seconds == 600.0
    assert sample.keep_alive == 0

    assert sample.total_duration_seconds == 32.6048339
    assert sample.load_duration_seconds == 12.73777074
    assert sample.prompt_eval_count == 38
    assert sample.prompt_eval_duration_seconds == 12.251242
    assert sample.eval_count == 340
    assert sample.eval_duration_seconds == 7.608376
    assert sample.tokens_per_second == metrics.tokens_per_second


def test_runtime_metric_sample_rejects_naive_datetime() -> None:
    metrics = RuntimeMetrics(
        model="qwen3.5:9b",
    )

    naive_datetime = datetime(2026, 7, 12, 18, 30)

    try:
        RuntimeMetricSample.from_runtime_metrics(
            metrics=metrics,
            timeout_seconds=600.0,
            keep_alive=0,
            captured_at=naive_datetime,
        )
    except ValueError as exc:
        assert "timezone" in str(exc)
    else:
        raise AssertionError("Expected ValueError for naive datetime")


def test_runtime_metric_sample_rejects_invalid_timeout() -> None:
    metrics = RuntimeMetrics(
        model="qwen3.5:9b",
    )

    try:
        RuntimeMetricSample.from_runtime_metrics(
            metrics=metrics,
            timeout_seconds=0,
            keep_alive=0,
        )
    except ValueError as exc:
        assert "timeout_seconds" in str(exc)
    else:
        raise AssertionError("Expected ValueError for invalid timeout")