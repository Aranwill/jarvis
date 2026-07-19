from __future__ import annotations

from pathlib import Path

from malak.runtime.ollama_runtime import OllamaRuntime
from malak.runtime.runtime_metric_jsonl_store import (
    JsonlRuntimeMetricStore,
)
from malak.runtime.runtime_metric_sink import RuntimeMetricSink
from malak.runtime.runtime_metric_store import (
    InMemoryRuntimeMetricStore,
)


def test_in_memory_store_satisfies_runtime_metric_sink() -> None:
    sink: RuntimeMetricSink = InMemoryRuntimeMetricStore()

    runtime = OllamaRuntime(metric_store=sink)

    assert runtime is not None


def test_jsonl_store_satisfies_runtime_metric_sink(
    tmp_path: Path,
) -> None:
    sink: RuntimeMetricSink = JsonlRuntimeMetricStore(
        tmp_path / "runtime_metrics.jsonl"
    )

    runtime = OllamaRuntime(metric_store=sink)

    assert runtime is not None