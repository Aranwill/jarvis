from __future__ import annotations

from dataclasses import FrozenInstanceError
from datetime import UTC, datetime, timedelta
from importlib import import_module

import pytest

from malak.observability.execution_trace import (
    TRACE_SCHEMA,
    ExecutionTraceEvent,
)


BASELINE = "675121c3c3180c8436a6e436997247307b19207b"
T0 = datetime(2026, 9, 23, 22, 0, tzinfo=UTC)

CANONICAL_NODE_IDS = (
    "run",
    "scope",
    "evidence",
    "engineering_inspect",
    "engineering_analyze",
    "engineering_propose",
    "decision",
    "artifact",
    "stop",
)


def _module():
    return import_module("malak.observability.execution_trace_projection")


def _event(
    sequence: int,
    event_type: str,
    *,
    component: str = "internal_interaction",
    phase: str = "run",
    outcome: str | None = None,
    reason_code: str | None = None,
    seconds: int = 0,
    input_refs: tuple[str, ...] = (),
    output_refs: tuple[str, ...] = (),
    evidence_refs: tuple[str, ...] = (),
    run_id: str = "run-001",
    baseline_commit: str = BASELINE,
    task_id: str = "self-review-v0",
) -> ExecutionTraceEvent:
    default_outcomes = {
        "RUN_STARTED": "STARTED",
        "SCOPE_FROZEN": "SUCCEEDED",
        "EVIDENCE_PACKET_STARTED": "STARTED",
        "EVIDENCE_PACKET_READY": "SUCCEEDED",
        "COMPONENT_STARTED": "STARTED",
        "COMPONENT_COMPLETED": "SUCCEEDED",
        "COMPONENT_SKIPPED": "SKIPPED",
        "COMPONENT_FAILED": "FAILED",
        "TERMINAL_DISPOSITION": "SUCCEEDED",
        "ARTIFACT_FINALIZED": "SUCCEEDED",
        "RUN_STOPPED": "SUCCEEDED",
    }
    selected_outcome = outcome or default_outcomes[event_type]
    selected_reason = reason_code
    if selected_reason is None:
        if selected_outcome == "SKIPPED":
            selected_reason = "not_required_by_workflow"
        elif selected_outcome == "FAILED":
            selected_reason = "component_error"
        elif selected_outcome == "INCONCLUSIVE":
            selected_reason = "required_evidence_missing"

    return ExecutionTraceEvent(
        schema=TRACE_SCHEMA,
        run_id=run_id,
        sequence=sequence,
        occurred_at=T0 + timedelta(seconds=seconds),
        baseline_commit=baseline_commit,
        task_id=task_id,
        phase=phase,
        component=component,
        event_type=event_type,
        input_refs=input_refs,
        output_refs=output_refs,
        evidence_refs=evidence_refs,
        outcome=selected_outcome,
        reason_code=selected_reason,
        authority_effect="none",
    )


def test_projection_red_c01_empty_projection_has_only_canonical_not_observed_nodes() -> None:
    projection = _module().ExecutionTraceProjection.empty()

    assert projection.run_id is None
    assert projection.baseline_commit is None
    assert projection.task_id is None
    assert tuple(node.node_id for node in projection.nodes) == CANONICAL_NODE_IDS
    assert {node.status for node in projection.nodes} == {"NOT_OBSERVED"}


def test_projection_red_c02_projection_and_nodes_are_immutable() -> None:
    projection = _module().ExecutionTraceProjection.empty()
    node = projection.node("run")

    with pytest.raises(FrozenInstanceError):
        node.status = "RUNNING"  # type: ignore[misc]

    with pytest.raises(FrozenInstanceError):
        projection.last_sequence = 99  # type: ignore[misc]


def test_projection_red_c03_run_started_advances_only_run_node() -> None:
    projection = _module().ExecutionTraceProjection.empty().apply(
        _event(1, "RUN_STARTED")
    )

    assert projection.run_id == "run-001"
    assert projection.baseline_commit == BASELINE
    assert projection.task_id == "self-review-v0"
    assert projection.last_sequence == 1
    assert projection.node("run").status == "RUNNING"

    untouched = tuple(
        node.status
        for node in projection.nodes
        if node.node_id != "run"
    )
    assert set(untouched) == {"NOT_OBSERVED"}


@pytest.mark.parametrize(
    ("event", "node_id", "status"),
    [
        (
            _event(2, "SCOPE_FROZEN", phase="scope"),
            "scope",
            "COMPLETED",
        ),
        (
            _event(
                2,
                "EVIDENCE_PACKET_STARTED",
                component="self_review_evidence",
                phase="evidence",
            ),
            "evidence",
            "RUNNING",
        ),
        (
            _event(
                2,
                "COMPONENT_STARTED",
                component="engineering_inspect",
                phase="engineering",
            ),
            "engineering_inspect",
            "RUNNING",
        ),
        (
            _event(
                2,
                "COMPONENT_SKIPPED",
                component="engineering_propose",
                phase="engineering",
                reason_code="not_required_by_workflow",
            ),
            "engineering_propose",
            "SKIPPED",
        ),
        (
            _event(
                2,
                "TERMINAL_DISPOSITION",
                phase="decision",
            ),
            "decision",
            "COMPLETED",
        ),
        (
            _event(
                2,
                "ARTIFACT_FINALIZED",
                phase="artifact",
            ),
            "artifact",
            "COMPLETED",
        ),
    ],
)
def test_projection_red_c04_event_mapping_advances_exact_node_only(
    event: ExecutionTraceEvent,
    node_id: str,
    status: str,
) -> None:
    projection = _module().ExecutionTraceProjection.empty()
    projection = projection.apply(_event(1, "RUN_STARTED"))
    projection = projection.apply(event)

    assert projection.node(node_id).status == status


def test_projection_red_c05_evidence_inconclusive_is_visible() -> None:
    projection = _module().fold_execution_trace(
        (
            _event(1, "RUN_STARTED"),
            _event(
                2,
                "EVIDENCE_PACKET_STARTED",
                component="self_review_evidence",
                phase="evidence",
                seconds=1,
            ),
            _event(
                3,
                "EVIDENCE_PACKET_READY",
                component="self_review_evidence",
                phase="evidence",
                outcome="INCONCLUSIVE",
                reason_code="required_evidence_missing",
                seconds=2,
            ),
        )
    )

    evidence = projection.node("evidence")
    assert evidence.status == "INCONCLUSIVE"
    assert evidence.reason_code == "required_evidence_missing"


def test_projection_red_c06_completed_component_derives_duration_from_real_events() -> None:
    projection = _module().fold_execution_trace(
        (
            _event(1, "RUN_STARTED"),
            _event(
                2,
                "COMPONENT_STARTED",
                component="engineering_inspect",
                phase="engineering",
                seconds=1,
            ),
            _event(
                3,
                "COMPONENT_COMPLETED",
                component="engineering_inspect",
                phase="engineering",
                seconds=4,
            ),
        )
    )

    node = projection.node("engineering_inspect")
    assert node.status == "COMPLETED"
    assert node.started_at == T0 + timedelta(seconds=1)
    assert node.completed_at == T0 + timedelta(seconds=4)
    assert node.duration_ms == 3000


def test_projection_red_c07_completed_without_start_has_no_invented_duration() -> None:
    projection = _module().fold_execution_trace(
        (
            _event(1, "RUN_STARTED"),
            _event(
                2,
                "SCOPE_FROZEN",
                phase="scope",
                seconds=2,
            ),
        )
    )

    scope = projection.node("scope")
    assert scope.status == "COMPLETED"
    assert scope.started_at is None
    assert scope.duration_ms is None


def test_projection_red_c08_skipped_component_has_reason_and_no_duration() -> None:
    projection = _module().fold_execution_trace(
        (
            _event(1, "RUN_STARTED"),
            _event(
                2,
                "COMPONENT_SKIPPED",
                component="engineering_propose",
                phase="engineering",
                reason_code="not_required_by_workflow",
                seconds=2,
            ),
        )
    )

    node = projection.node("engineering_propose")
    assert node.status == "SKIPPED"
    assert node.reason_code == "not_required_by_workflow"
    assert node.duration_ms is None


def test_projection_red_c09_failed_component_preserves_reason() -> None:
    projection = _module().fold_execution_trace(
        (
            _event(1, "RUN_STARTED"),
            _event(
                2,
                "COMPONENT_STARTED",
                component="engineering_analyze",
                phase="engineering",
                seconds=1,
            ),
            _event(
                3,
                "COMPONENT_FAILED",
                component="engineering_analyze",
                phase="engineering",
                reason_code="component_error",
                seconds=3,
            ),
        )
    )

    node = projection.node("engineering_analyze")
    assert node.status == "FAILED"
    assert node.reason_code == "component_error"
    assert node.duration_ms == 2000


@pytest.mark.parametrize(
    "value",
    [
        object(),
        "not-an-event",
        {"event_type": "RUN_STARTED"},
    ],
)
def test_projection_red_c10_non_contract_input_is_rejected(value: object) -> None:
    projection = _module().ExecutionTraceProjection.empty()

    with pytest.raises(TypeError):
        projection.apply(value)


def test_projection_red_c11_run_identity_cannot_change_mid_projection() -> None:
    projection = _module().ExecutionTraceProjection.empty().apply(
        _event(1, "RUN_STARTED")
    )

    with pytest.raises(ValueError):
        projection.apply(
            _event(
                2,
                "SCOPE_FROZEN",
                phase="scope",
                run_id="run-other",
            )
        )


def test_projection_red_c12_baseline_cannot_change_mid_projection() -> None:
    projection = _module().ExecutionTraceProjection.empty().apply(
        _event(1, "RUN_STARTED")
    )

    with pytest.raises(ValueError):
        projection.apply(
            _event(
                2,
                "SCOPE_FROZEN",
                phase="scope",
                baseline_commit="1" * 40,
            )
        )


def test_projection_red_c13_task_identity_cannot_change_mid_projection() -> None:
    projection = _module().ExecutionTraceProjection.empty().apply(
        _event(1, "RUN_STARTED")
    )

    with pytest.raises(ValueError):
        projection.apply(
            _event(
                2,
                "SCOPE_FROZEN",
                phase="scope",
                task_id="other-task",
            )
        )


@pytest.mark.parametrize("sequence", [1, 0])
def test_projection_red_c14_sequence_must_advance_strictly(sequence: int) -> None:
    projection = _module().ExecutionTraceProjection.empty().apply(
        _event(1, "RUN_STARTED")
    )

    with pytest.raises(ValueError):
        projection.apply(
            _event(
                sequence,
                "SCOPE_FROZEN",
                phase="scope",
            )
        )


def test_projection_red_c15_completed_node_cannot_return_to_running() -> None:
    projection = _module().fold_execution_trace(
        (
            _event(1, "RUN_STARTED"),
            _event(
                2,
                "COMPONENT_STARTED",
                component="engineering_inspect",
                phase="engineering",
            ),
            _event(
                3,
                "COMPONENT_COMPLETED",
                component="engineering_inspect",
                phase="engineering",
                seconds=1,
            ),
        )
    )

    with pytest.raises(ValueError):
        projection.apply(
            _event(
                4,
                "COMPONENT_STARTED",
                component="engineering_inspect",
                phase="engineering",
                seconds=2,
            )
        )


@pytest.mark.parametrize(
    "component",
    [
        "unknown_component",
        "agent_future",
        "engineering_unknown",
    ],
)
def test_projection_red_c16_unknown_component_is_rejected(component: str) -> None:
    projection = _module().ExecutionTraceProjection.empty().apply(
        _event(1, "RUN_STARTED")
    )

    with pytest.raises(ValueError):
        projection.apply(
            _event(
                2,
                "COMPONENT_STARTED",
                component=component,
                phase="engineering",
            )
        )


def test_projection_red_c17_run_stopped_completes_run_and_stop_nodes() -> None:
    projection = _module().fold_execution_trace(
        (
            _event(1, "RUN_STARTED"),
            _event(
                2,
                "RUN_STOPPED",
                seconds=5,
            ),
        )
    )

    assert projection.node("run").status == "COMPLETED"
    assert projection.node("run").duration_ms == 5000
    assert projection.node("stop").status == "COMPLETED"


def test_projection_red_c18_no_event_is_accepted_after_run_stopped() -> None:
    projection = _module().fold_execution_trace(
        (
            _event(1, "RUN_STARTED"),
            _event(2, "RUN_STOPPED", seconds=1),
        )
    )

    with pytest.raises(ValueError):
        projection.apply(
            _event(
                3,
                "SCOPE_FROZEN",
                phase="scope",
                seconds=2,
            )
        )


def test_projection_red_c19_unknown_node_does_not_fabricate_not_observed() -> None:
    projection = _module().ExecutionTraceProjection.empty()

    with pytest.raises(KeyError):
        projection.node("future-agent")


def test_projection_red_c20_node_exposes_projection_metadata_only() -> None:
    projection = _module().fold_execution_trace(
        (
            _event(1, "RUN_STARTED", output_refs=("run:manifest",)),
            _event(
                2,
                "COMPONENT_STARTED",
                component="engineering_inspect",
                phase="engineering",
                input_refs=("run:manifest",),
                evidence_refs=("evidence:packet",),
            ),
        )
    )

    node = projection.node("engineering_inspect")
    fields = set(node.__dataclass_fields__)

    assert fields == {
        "node_id",
        "label",
        "phase",
        "component",
        "status",
        "started_at",
        "completed_at",
        "duration_ms",
        "outcome",
        "reason_code",
        "input_refs",
        "output_refs",
        "evidence_refs",
        "last_sequence",
        "authority_effect",
    }
    assert not hasattr(node, "content")
    assert not hasattr(node, "prompt")
    assert not hasattr(node, "chain_of_thought")


def test_projection_red_c21_live_sink_and_replay_fold_are_materially_equal() -> None:
    events = (
        _event(1, "RUN_STARTED"),
        _event(2, "SCOPE_FROZEN", phase="scope", seconds=1),
        _event(
            3,
            "COMPONENT_STARTED",
            component="engineering_inspect",
            phase="engineering",
            seconds=2,
        ),
        _event(
            4,
            "COMPONENT_COMPLETED",
            component="engineering_inspect",
            phase="engineering",
            seconds=4,
        ),
    )

    sink = _module().LiveTraceProjectionSink()
    for event in events:
        sink.append(event)

    replay_projection = _module().fold_execution_trace(events)

    assert sink.projection == replay_projection
