from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime
from typing import Final, Iterable

from malak.observability.execution_trace import ExecutionTraceEvent


_STATUS_NOT_OBSERVED: Final[str] = "NOT_OBSERVED"
_STATUS_RUNNING: Final[str] = "RUNNING"
_STATUS_COMPLETED: Final[str] = "COMPLETED"
_STATUS_SKIPPED: Final[str] = "SKIPPED"
_STATUS_FAILED: Final[str] = "FAILED"
_STATUS_INCONCLUSIVE: Final[str] = "INCONCLUSIVE"

_TERMINAL_STATUSES: Final[frozenset[str]] = frozenset(
    {
        _STATUS_COMPLETED,
        _STATUS_SKIPPED,
        _STATUS_FAILED,
        _STATUS_INCONCLUSIVE,
    }
)

_CANONICAL_NODE_SPECS: Final[tuple[tuple[str, str, str, str], ...]] = (
    ("run", "RUN", "run", "internal_interaction"),
    ("scope", "Scope", "scope", "internal_interaction"),
    ("evidence", "Evidence Packet", "evidence", "self_review_evidence"),
    (
        "engineering_inspect",
        "Inspect",
        "engineering",
        "engineering_inspect",
    ),
    (
        "engineering_analyze",
        "Analyze",
        "engineering",
        "engineering_analyze",
    ),
    (
        "engineering_propose",
        "Propose",
        "engineering",
        "engineering_propose",
    ),
    (
        "decision",
        "Terminal Disposition",
        "decision",
        "internal_interaction",
    ),
    ("artifact", "Artifact", "artifact", "internal_interaction"),
    ("stop", "STOP", "run", "internal_interaction"),
)

_ENGINEERING_COMPONENT_TO_NODE: Final[dict[str, str]] = {
    "engineering_inspect": "engineering_inspect",
    "engineering_analyze": "engineering_analyze",
    "engineering_propose": "engineering_propose",
}


@dataclass(frozen=True, slots=True)
class ExecutionTraceProjectionNode:
    node_id: str
    label: str
    phase: str
    component: str
    status: str
    started_at: datetime | None
    completed_at: datetime | None
    duration_ms: int | None
    outcome: str | None
    reason_code: str | None
    input_refs: tuple[str, ...]
    output_refs: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    last_sequence: int | None
    authority_effect: str


@dataclass(frozen=True, slots=True)
class ExecutionTraceProjection:
    run_id: str | None
    baseline_commit: str | None
    task_id: str | None
    nodes: tuple[ExecutionTraceProjectionNode, ...]
    last_sequence: int
    stopped: bool = False

    @classmethod
    def empty(cls) -> "ExecutionTraceProjection":
        nodes = tuple(
            ExecutionTraceProjectionNode(
                node_id=node_id,
                label=label,
                phase=phase,
                component=component,
                status=_STATUS_NOT_OBSERVED,
                started_at=None,
                completed_at=None,
                duration_ms=None,
                outcome=None,
                reason_code=None,
                input_refs=(),
                output_refs=(),
                evidence_refs=(),
                last_sequence=None,
                authority_effect="none",
            )
            for node_id, label, phase, component in _CANONICAL_NODE_SPECS
        )
        return cls(
            run_id=None,
            baseline_commit=None,
            task_id=None,
            nodes=nodes,
            last_sequence=0,
            stopped=False,
        )

    def node(self, node_id: str) -> ExecutionTraceProjectionNode:
        for node in self.nodes:
            if node.node_id == node_id:
                return node
        raise KeyError(node_id)

    def apply(
        self,
        event: ExecutionTraceEvent,
    ) -> "ExecutionTraceProjection":
        if not isinstance(event, ExecutionTraceEvent):
            raise TypeError("event must be an ExecutionTraceEvent")

        if self.stopped:
            raise ValueError("no event is allowed after RUN_STOPPED")

        if event.sequence <= self.last_sequence:
            raise ValueError("event sequence must be strictly increasing")

        if self.run_id is None:
            if event.event_type != "RUN_STARTED":
                raise ValueError("projection must start with RUN_STARTED")
            run_id = event.run_id
            baseline_commit = event.baseline_commit
            task_id = event.task_id
        else:
            if event.run_id != self.run_id:
                raise ValueError("event run_id does not match projection")
            if event.baseline_commit != self.baseline_commit:
                raise ValueError(
                    "event baseline_commit does not match projection"
                )
            if event.task_id != self.task_id:
                raise ValueError("event task_id does not match projection")
            run_id = self.run_id
            baseline_commit = self.baseline_commit
            task_id = self.task_id

        nodes = self.nodes
        stopped = self.stopped

        if event.event_type == "RUN_STARTED":
            if self.run_id is not None:
                raise ValueError("RUN_STARTED can occur only once")
            nodes = _replace_node(
                nodes,
                "run",
                _apply_started(self.node("run"), event),
            )
        elif event.event_type == "SCOPE_FROZEN":
            nodes = _replace_node(
                nodes,
                "scope",
                _apply_completed(self.node("scope"), event),
            )
        elif event.event_type == "EVIDENCE_PACKET_STARTED":
            nodes = _replace_node(
                nodes,
                "evidence",
                _apply_started(self.node("evidence"), event),
            )
        elif event.event_type == "EVIDENCE_PACKET_READY":
            evidence = self.node("evidence")
            if event.outcome == "INCONCLUSIVE":
                updated = _apply_terminal(
                    evidence,
                    event,
                    status=_STATUS_INCONCLUSIVE,
                )
            else:
                updated = _apply_completed(evidence, event)
            nodes = _replace_node(nodes, "evidence", updated)
        elif event.event_type in {
            "COMPONENT_STARTED",
            "COMPONENT_COMPLETED",
            "COMPONENT_SKIPPED",
            "COMPONENT_FAILED",
        }:
            node_id = _ENGINEERING_COMPONENT_TO_NODE.get(event.component)
            if node_id is None:
                raise ValueError(
                    f"unsupported projection component: {event.component}"
                )
            current = self.node(node_id)
            if event.event_type == "COMPONENT_STARTED":
                updated = _apply_started(current, event)
            elif event.event_type == "COMPONENT_COMPLETED":
                updated = _apply_completed(current, event)
            elif event.event_type == "COMPONENT_SKIPPED":
                updated = _apply_terminal(
                    current,
                    event,
                    status=_STATUS_SKIPPED,
                )
            else:
                updated = _apply_terminal(
                    current,
                    event,
                    status=_STATUS_FAILED,
                )
            nodes = _replace_node(nodes, node_id, updated)
        elif event.event_type == "TERMINAL_DISPOSITION":
            nodes = _replace_node(
                nodes,
                "decision",
                _apply_completed(self.node("decision"), event),
            )
        elif event.event_type == "ARTIFACT_FINALIZED":
            nodes = _replace_node(
                nodes,
                "artifact",
                _apply_completed(self.node("artifact"), event),
            )
        elif event.event_type == "RUN_STOPPED":
            stop_node = _apply_completed(self.node("stop"), event)
            run_node = _apply_completed(self.node("run"), event)
            nodes = _replace_node(nodes, "stop", stop_node)
            nodes = _replace_node(nodes, "run", run_node)
            stopped = True
        else:
            raise ValueError(
                f"event type is not projected in V0: {event.event_type}"
            )

        return ExecutionTraceProjection(
            run_id=run_id,
            baseline_commit=baseline_commit,
            task_id=task_id,
            nodes=nodes,
            last_sequence=event.sequence,
            stopped=stopped,
        )


class LiveTraceProjectionSink:
    def __init__(self) -> None:
        self._projection = ExecutionTraceProjection.empty()

    @property
    def projection(self) -> ExecutionTraceProjection:
        return self._projection

    def append(self, event: ExecutionTraceEvent) -> None:
        updated = self._projection.apply(event)
        self._projection = updated


def fold_execution_trace(
    events: Iterable[ExecutionTraceEvent],
) -> ExecutionTraceProjection:
    projection = ExecutionTraceProjection.empty()
    for event in events:
        projection = projection.apply(event)
    return projection


def _replace_node(
    nodes: tuple[ExecutionTraceProjectionNode, ...],
    node_id: str,
    updated: ExecutionTraceProjectionNode,
) -> tuple[ExecutionTraceProjectionNode, ...]:
    return tuple(updated if node.node_id == node_id else node for node in nodes)


def _ensure_can_start(node: ExecutionTraceProjectionNode) -> None:
    if node.status != _STATUS_NOT_OBSERVED:
        raise ValueError(
            f"node {node.node_id} cannot transition from {node.status} to RUNNING"
        )


def _ensure_can_finish(node: ExecutionTraceProjectionNode) -> None:
    if node.status in _TERMINAL_STATUSES:
        raise ValueError(
            f"node {node.node_id} cannot transition from terminal state"
        )


def _duration_ms(
    started_at: datetime | None,
    completed_at: datetime,
) -> int | None:
    if started_at is None:
        return None
    delta = completed_at - started_at
    milliseconds = int(delta.total_seconds() * 1000)
    if milliseconds < 0:
        raise ValueError("completed_at cannot precede started_at")
    return milliseconds


def _event_metadata(
    node: ExecutionTraceProjectionNode,
    event: ExecutionTraceEvent,
) -> dict[str, object]:
    return {
        "outcome": event.outcome,
        "reason_code": event.reason_code,
        "input_refs": event.input_refs,
        "output_refs": event.output_refs,
        "evidence_refs": event.evidence_refs,
        "last_sequence": event.sequence,
        "authority_effect": event.authority_effect,
    }


def _apply_started(
    node: ExecutionTraceProjectionNode,
    event: ExecutionTraceEvent,
) -> ExecutionTraceProjectionNode:
    _ensure_can_start(node)
    return replace(
        node,
        status=_STATUS_RUNNING,
        started_at=event.occurred_at,
        completed_at=None,
        duration_ms=None,
        **_event_metadata(node, event),
    )


def _apply_completed(
    node: ExecutionTraceProjectionNode,
    event: ExecutionTraceEvent,
) -> ExecutionTraceProjectionNode:
    _ensure_can_finish(node)
    return replace(
        node,
        status=_STATUS_COMPLETED,
        completed_at=event.occurred_at,
        duration_ms=_duration_ms(node.started_at, event.occurred_at),
        **_event_metadata(node, event),
    )


def _apply_terminal(
    node: ExecutionTraceProjectionNode,
    event: ExecutionTraceEvent,
    *,
    status: str,
) -> ExecutionTraceProjectionNode:
    _ensure_can_finish(node)
    duration = (
        _duration_ms(node.started_at, event.occurred_at)
        if node.started_at is not None
        else None
    )
    return replace(
        node,
        status=status,
        completed_at=event.occurred_at,
        duration_ms=duration,
        **_event_metadata(node, event),
    )
