from datetime import datetime, timezone
from pathlib import Path

import pytest

from malak.runtime.runtime_metric_jsonl_store import (
    JsonlRuntimeMetricStore,
)
from malak.runtime.runtime_metric_sample import RuntimeMetricSample


def _create_sample(
    model: str,
    captured_at: datetime,
    total_duration_seconds: float,
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


def test_jsonl_store_creates_parent_directory_and_file(
    tmp_path: Path,
) -> None:
    file_path = (
        tmp_path
        / "runtime_metrics"
        / "runtime_metrics.jsonl"
    )

    store = JsonlRuntimeMetricStore(file_path)

    sample = _create_sample(
        model="qwen3.5:9b",
        captured_at=datetime(
            2026,
            7,
            12,
            18,
            0,
            tzinfo=timezone.utc,
        ),
        total_duration_seconds=30.0,
    )

    store.append(sample)

    assert file_path.exists()
    assert file_path.parent.exists()


def test_jsonl_store_persists_and_reloads_samples(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "runtime_metrics.jsonl"

    first_store = JsonlRuntimeMetricStore(file_path)

    first_sample = _create_sample(
        model="qwen3.5:9b",
        captured_at=datetime(
            2026,
            7,
            12,
            18,
            0,
            tzinfo=timezone.utc,
        ),
        total_duration_seconds=30.0,
    )

    second_sample = _create_sample(
        model="deepseek-coder-v2:16b",
        captured_at=datetime(
            2026,
            7,
            12,
            19,
            0,
            tzinfo=timezone.utc,
        ),
        total_duration_seconds=120.0,
    )

    first_store.append(first_sample)
    first_store.append(second_sample)

    reloaded_store = JsonlRuntimeMetricStore(file_path)

    assert reloaded_store.list_all() == [
        first_sample,
        second_sample,
    ]


def test_jsonl_store_filters_samples_by_model(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "runtime_metrics.jsonl"
    store = JsonlRuntimeMetricStore(file_path)

    qwen_sample = _create_sample(
        model="qwen3.5:9b",
        captured_at=datetime(
            2026,
            7,
            12,
            18,
            0,
            tzinfo=timezone.utc,
        ),
        total_duration_seconds=30.0,
    )

    deepseek_sample = _create_sample(
        model="deepseek-coder-v2:16b",
        captured_at=datetime(
            2026,
            7,
            12,
            19,
            0,
            tzinfo=timezone.utc,
        ),
        total_duration_seconds=120.0,
    )

    store.append(qwen_sample)
    store.append(deepseek_sample)

    assert store.list_by_model("qwen3.5:9b") == [
        qwen_sample,
    ]


def test_jsonl_store_returns_empty_list_when_file_does_not_exist(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "missing.jsonl"
    store = JsonlRuntimeMetricStore(file_path)

    assert store.list_all() == []


def test_jsonl_store_rejects_empty_model_filter(
    tmp_path: Path,
) -> None:
    store = JsonlRuntimeMetricStore(
        tmp_path / "runtime_metrics.jsonl"
    )

    with pytest.raises(
        ValueError,
        match="model",
    ):
        store.list_by_model("   ")


def test_jsonl_store_reports_corrupted_line(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "runtime_metrics.jsonl"

    file_path.write_text(
        (
            '{"model":"qwen3.5:9b",'
            '"captured_at":"2026-07-12T18:00:00+00:00",'
            '"timeout_seconds":600.0,'
            '"keep_alive":0,'
            '"total_duration_seconds":30.0,'
            '"load_duration_seconds":10.0,'
            '"prompt_eval_count":40,'
            '"prompt_eval_duration_seconds":5.0,'
            '"eval_count":100,'
            '"eval_duration_seconds":4.0,'
            '"tokens_per_second":25.0}'
            "\n"
            "this is not valid json\n"
        ),
        encoding="utf-8",
    )

    store = JsonlRuntimeMetricStore(file_path)

    with pytest.raises(
        RuntimeError,
        match="line 2",
    ):
        store.list_all()