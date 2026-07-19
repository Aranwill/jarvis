from __future__ import annotations

from typing import Protocol

from malak.runtime.runtime_metric_sample import RuntimeMetricSample


class RuntimeMetricSink(Protocol):
    """
    Receives completed runtime metric samples.

    The sink contract is intentionally write-only. It does not expose
    persistence, querying, profiling, or runtime configuration behavior.
    """

    def append(
        self,
        sample: RuntimeMetricSample,
    ) -> None:
        """
        Store or forward one completed runtime metric sample.
        """
        ...