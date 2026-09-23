from __future__ import annotations

import re
from collections.abc import Callable
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
) -> str:
    if not isinstance(projection, ExecutionTraceProjection):
        raise TypeError("projection must be an ExecutionTraceProjection")

    run_id = projection.run_id or "NOT_OBSERVED"
    baseline = projection.baseline_commit or "NOT_OBSERVED"

    run = _render_node(projection.node("run"))
    scope = _render_node(projection.node("scope"))
    evidence = _render_node(projection.node("evidence"))
    inspect = _render_node(projection.node("engineering_inspect"))
    analyze = _render_node(projection.node("engineering_analyze"))
    propose = _render_node(projection.node("engineering_propose"))
    decision = _render_node(projection.node("decision"))
    artifact = _render_node(projection.node("artifact"))
    stop = _render_node(projection.node("stop"))

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
    ) -> None:
        if not callable(output_fn):
            raise TypeError("output_fn must be callable")
        self._output_fn = output_fn
        self._sink = LiveTraceProjectionSink()

    @property
    def projection(self) -> ExecutionTraceProjection:
        return self._sink.projection

    def append(self, event: ExecutionTraceEvent) -> None:
        self._sink.append(event)
        self._output_fn(render_trace_projection(self._sink.projection))


def _validate_run_id(run_id: object) -> None:
    if not isinstance(run_id, str):
        raise TypeError("run_id must be a string")
    if not _RUN_ID_RE.fullmatch(run_id):
        raise ValueError("run_id is not safe for runtime replay")


def _render_node(node) -> str:
    token = _STATUS_TOKEN[node.status]
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
