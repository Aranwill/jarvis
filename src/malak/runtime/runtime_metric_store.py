from __future__ import annotations

from malak.runtime.runtime_metric_sample import RuntimeMetricSample


class InMemoryRuntimeMetricStore:
    """
    In-memory store for runtime metric samples.

    This implementation is intentionally simple and non-persistent.
    It preserves insertion order and returns defensive copies so callers
    cannot mutate the internal collection.
    """

    def __init__(self) -> None:
        self._samples: list[RuntimeMetricSample] = []

    def append(
        self,
        sample: RuntimeMetricSample,
    ) -> None:
        self._samples.append(sample)

    def list_all(self) -> list[RuntimeMetricSample]:
        return list(self._samples)

    def list_by_model(
        self,
        model: str,
    ) -> list[RuntimeMetricSample]:
        normalized_model = model.strip()

        if not normalized_model:
            raise ValueError("model must not be empty")

        return [
            sample
            for sample in self._samples
            if sample.model == normalized_model
        ]