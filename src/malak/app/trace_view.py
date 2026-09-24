from __future__ import annotations

import re
import threading
import time
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Final

from malak.observability.execution_trace import (
    ExecutionTraceEvent,
    read_execution_trace_jsonl,
)
from malak.observability.execution_trace_projection import (
    ExecutionTraceProjection,
    LiveTraceProjectionSink,
    fold_execution_trace,
)


_RUN_ID_RE: Final[re.Pattern[str]] = re.compile(
    r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$"
)
_DEFAULT_REFRESH_INTERVAL_SECONDS: Final[float] = 1.0

_STATUS_TOKEN: Final[dict[str, str]] = {
    "NOT_OBSERVED": "[..]",
    "RUNNING": "[>>]",
    "COMPLETED": "[OK]",
    "SKIPPED": "[--]",
    "FAILED": "[!!]",
    "INCONCLUSIVE": "[??]",
}


def load_trace_projection(
    *,
    repository_root: str | Path,
    run_id: str,
) -> ExecutionTraceProjection:
    root = Path(repository_root).expanduser()
    if not root.is_dir():
        raise ValueError("repository_root must be an existing directory")

    _validate_run_id(run_id)

    boundary = (root / "runtime" / "internal_interaction").resolve()
    trace_path = (boundary / run_id / "trace.jsonl").resolve()

    try:
        trace_path.relative_to(boundary)
    except ValueError as exc:
        raise ValueError("trace path escapes runtime boundary") from exc

    if not trace_path.is_file():
        raise FileNotFoundError(
            f"trace not found for run_id: {run_id}"
        )

    events = read_execution_trace_jsonl(trace_path)
    return fold_execution_trace(events)


def render_trace_projection(
    projection: ExecutionTraceProjection,
    *,
    elapsed_ms_by_node: Mapping[str, int] | None = None,
) -> str:
    if not isinstance(projection, ExecutionTraceProjection):
        raise TypeError("projection must be an ExecutionTraceProjection")

    elapsed = elapsed_ms_by_node or {}

    run_id = projection.run_id or "NOT_OBSERVED"
    baseline = projection.baseline_commit or "NOT_OBSERVED"

    run = _render_node(
        projection.node("run"),
        elapsed_ms=elapsed.get("run"),
    )
    scope = _render_node(
        projection.node("scope"),
        elapsed_ms=elapsed.get("scope"),
    )
    evidence = _render_node(
        projection.node("evidence"),
        elapsed_ms=elapsed.get("evidence"),
    )
    inspect = _render_node(
        projection.node("engineering_inspect"),
        elapsed_ms=elapsed.get("engineering_inspect"),
    )
    analyze = _render_node(
        projection.node("engineering_analyze"),
        elapsed_ms=elapsed.get("engineering_analyze"),
    )
    propose = _render_node(
        projection.node("engineering_propose"),
        elapsed_ms=elapsed.get("engineering_propose"),
    )
    decision = _render_node(
        projection.node("decision"),
        elapsed_ms=elapsed.get("decision"),
    )
    artifact = _render_node(
        projection.node("artifact"),
        elapsed_ms=elapsed.get("artifact"),
    )
    stop = _render_node(
        projection.node("stop"),
        elapsed_ms=elapsed.get("stop"),
    )

    lines = [
        f"MALAK INTERNAL INTERACTION - {run_id}",
        f"baseline {baseline}",
        "",
        run,
        f" |-- {scope}",
        f" |-- {evidence}",
        " |-- Engineering",
        f" |    |-- {inspect}",
        f" |    |-- {analyze}",
        f" |    `-- {propose}",
        f" |-- {decision}",
        f" |-- {artifact}",
        f" `-- {stop}",
    ]
    rendered = "\n".join(lines)

    if not rendered.isascii():
        raise ValueError("trace renderer must produce ASCII output")
    return rendered


def render_trace_node(
    projection: ExecutionTraceProjection,
    node_id: str,
) -> str:
    if not isinstance(projection, ExecutionTraceProjection):
        raise TypeError("projection must be an ExecutionTraceProjection")
    if not isinstance(node_id, str) or not node_id:
        raise ValueError("node_id must be a non-empty string")

    node = projection.node(node_id)

    lines = [
        f"node_id: {node.node_id}",
        f"label: {node.label}",
        f"status: {node.status}",
        f"phase: {node.phase}",
        f"component: {node.component}",
        f"started_at: {_format_datetime(node.started_at)}",
        f"completed_at: {_format_datetime(node.completed_at)}",
        f"duration_ms: {_format_optional(node.duration_ms)}",
        f"outcome: {_format_optional(node.outcome)}",
        f"reason_code: {_format_optional(node.reason_code)}",
        f"last_sequence: {_format_optional(node.last_sequence)}",
        f"authority_effect: {node.authority_effect}",
        f"input_refs: {_format_refs(node.input_refs)}",
        f"output_refs: {_format_refs(node.output_refs)}",
        f"evidence_refs: {_format_refs(node.evidence_refs)}",
    ]
    rendered = "\n".join(lines)

    if not rendered.isascii():
        raise ValueError("node renderer must produce ASCII output")
    return rendered


class LiveTraceTextView:
    def __init__(
        self,
        *,
        output_fn: Callable[[str], None] = print,
        monotonic_fn: Callable[[], float] = time.monotonic,
        refresh_interval_seconds: float = _DEFAULT_REFRESH_INTERVAL_SECONDS,
    ) -> None:
        if not callable(output_fn):
            raise TypeError("output_fn must be callable")
        if not callable(monotonic_fn):
            raise TypeError("monotonic_fn must be callable")
        if (
            isinstance(refresh_interval_seconds, bool)
            or not isinstance(refresh_interval_seconds, (int, float))
        ):
            raise TypeError("refresh_interval_seconds must be numeric")
        if refresh_interval_seconds <= 0:
            raise ValueError(
                "refresh_interval_seconds must be greater than zero"
            )

        self._output_fn = output_fn
        self._monotonic_fn = monotonic_fn
        self._refresh_interval_seconds = float(refresh_interval_seconds)
        self._sink = LiveTraceProjectionSink()
        self._running_started_monotonic: dict[str, float] = {}
        self._lock = threading.RLock()
        self._stop_event = threading.Event()
        self._liveness_thread: threading.Thread | None = None
        self._liveness_error: Exception | None = None

    @property
    def projection(self) -> ExecutionTraceProjection:
        with self._lock:
            return self._sink.projection

    @property
    def liveness_active(self) -> bool:
        with self._lock:
            thread = self._liveness_thread
            return thread is not None and thread.is_alive()

    def append(self, event: ExecutionTraceEvent) -> None:
        with self._lock:
            self._sink.append(event)
            self._sync_running_nodes_locked()
            self._output_fn(self._render_live_locked())

    def refresh_elapsed(self) -> None:
        with self._lock:
            if not self._running_started_monotonic:
                return
            self._output_fn(self._render_live_locked())

    def start_liveness(self) -> None:
        with self._lock:
            thread = self._liveness_thread
            if thread is not None and thread.is_alive():
                raise RuntimeError("live liveness ticker is already running")

            self._liveness_error = None
            self._stop_event.clear()
            thread = threading.Thread(
                target=self._run_liveness,
                name="malak-live-elapsed",
                daemon=True,
            )
            self._liveness_thread = thread
            thread.start()

    def stop_liveness(self) -> None:
        with self._lock:
            thread = self._liveness_thread
            if thread is None:
                return
            self._stop_event.set()

        thread.join(
            timeout=max(
                1.0,
                self._refresh_interval_seconds * 2.0,
            )
        )

        with self._lock:
            if thread.is_alive():
                raise RuntimeError(
                    "live liveness ticker did not stop cleanly"
                )
            error = self._liveness_error
            self._liveness_thread = None
            self._stop_event.clear()
            self._liveness_error = None

        if error is not None:
            raise RuntimeError(
                "live liveness ticker failed"
            ) from error

    def _run_liveness(self) -> None:
        try:
            while not self._stop_event.wait(
                self._refresh_interval_seconds
            ):
                self.refresh_elapsed()
        except Exception as exc:
            with self._lock:
                self._liveness_error = exc
                self._stop_event.set()

    def _sync_running_nodes_locked(self) -> None:
        now = self._monotonic_fn()
        running_ids = {
            node.node_id
            for node in self._sink.projection.nodes
            if node.status == "RUNNING"
        }

        for node_id in running_ids:
            self._running_started_monotonic.setdefault(node_id, now)

        for node_id in tuple(self._running_started_monotonic):
            if node_id not in running_ids:
                self._running_started_monotonic.pop(node_id, None)

    def _render_live_locked(self) -> str:
        now = self._monotonic_fn()
        elapsed: dict[str, int] = {}
        for node_id, started in self._running_started_monotonic.items():
            delta = now - started
            if delta < 0:
                raise RuntimeError(
                    "monotonic clock moved backwards"
                )
            elapsed[node_id] = int(delta * 1000)

        return render_trace_projection(
            self._sink.projection,
            elapsed_ms_by_node=elapsed,
        )


def _validate_run_id(run_id: object) -> None:
    if not isinstance(run_id, str):
        raise TypeError("run_id must be a string")
    if not _RUN_ID_RE.fullmatch(run_id):
        raise ValueError("run_id is not safe for runtime replay")


def _render_node(
    node,
    *,
    elapsed_ms: int | None = None,
) -> str:
    token = _STATUS_TOKEN[node.status]
    if node.status == "RUNNING" and elapsed_ms is not None:
        duration = f" elapsed={elapsed_ms} ms"
    else:
        duration = (
            f" {node.duration_ms} ms"
            if node.duration_ms is not None
            else ""
        )
    reason = (
        f" ({node.reason_code})"
        if node.reason_code is not None
        else ""
    )
    return f"{token} {node.label}{duration}{reason}"


def _format_datetime(value) -> str:
    if value is None:
        return "none"
    return value.isoformat().replace("+00:00", "Z")


def _format_optional(value: object | None) -> str:
    return "none" if value is None else str(value)


def _format_refs(values: tuple[str, ...]) -> str:
    return ",".join(values) if values else "none"
