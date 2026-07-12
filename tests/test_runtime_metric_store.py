from datetime import datetime, timezone

from malak.runtime.runtime_metric_sample import RuntimeMetricSample
from malak.runtime.runtime_metric_store import InMemoryRuntimeMetricStore


def _create_sample(
    model: str,
    total_duration_seconds: float,
    captured_at: datetime,
) -> RuntimeMetricSample:
    return RuntimeMetricSample(
        model=model,
        captured_at=captured_at,
        timeout_seconds=600.0,
        keep_alive=0,
        total_duration_seconds=total_duration_seconds,
        load_duration_seconds=10.0,
        prompt_eval_count=40,
        prompt_eval_duration_seconds=5.0,
        eval_count=100,
        eval_duration_seconds=4.0,
        tokens_per_second=25.0,
    )


def test_runtime_metric_store_appends_and_lists_samples() -> None:
    store = InMemoryRuntimeMetricStore()

    first_sample = _create_sample(
        model="qwen3.5:9b",
        total_duration_seconds=30.0,
        captured_at=datetime(
            2026,
            7,
            12,
            18,
            0,
            tzinfo=timezone.utc,
        ),
    )

    second_sample = _create_sample(
        model="qwen3.5:9b",
        total_duration_seconds=40.0,
        captured_at=datetime(
            2026,
            7,
            12,
            19,
            0,
            tzinfo=timezone.utc,
        ),
    )

    store.append(first_sample)
    store.append(second_sample)

    assert store.list_all() == [
        first_sample,
        second_sample,
    ]


def test_runtime_metric_store_filters_samples_by_model() -> None:
    store = InMemoryRuntimeMetricStore()

    qwen_sample = _create_sample(
        model="qwen3.5:9b",
        total_duration_seconds=30.0,
        captured_at=datetime(
            2026,
            7,
            12,
            18,
            0,
            tzinfo=timezone.utc,
        ),
    )

    deepseek_sample = _create_sample(
        model="deepseek-coder-v2:16b",
        total_duration_seconds=120.0,
        captured_at=datetime(
            2026,
            7,
            12,
            19,
            0,
            tzinfo=timezone.utc,
        ),
    )

    store.append(qwen_sample)
    store.append(deepseek_sample)

    assert store.list_by_model("qwen3.5:9b") == [
        qwen_sample,
    ]

    assert store.list_by_model("deepseek-coder-v2:16b") == [
        deepseek_sample,
    ]


def test_runtime_metric_store_returns_defensive_copies() -> None:
    store = InMemoryRuntimeMetricStore()

    sample = _create_sample(
        model="qwen3.5:9b",
        total_duration_seconds=30.0,
        captured_at=datetime(
            2026,
            7,
            12,
            18,
            0,
            tzinfo=timezone.utc,
        ),
    )

    store.append(sample)

    returned_samples = store.list_all()
    returned_samples.clear()

    assert store.list_all() == [sample]


def test_runtime_metric_store_rejects_empty_model_filter() -> None:
    store = InMemoryRuntimeMetricStore()

    try:
        store.list_by_model("   ")
    except ValueError as exc:
        assert "model" in str(exc)
    else:
        raise AssertionError("Expected ValueError for empty model")