from __future__ import annotations

from datetime import UTC, datetime, timedelta
from importlib import import_module
from pathlib import Path
import time

import pytest

from malak.observability.execution_trace import (
    TRACE_SCHEMA,
    ExecutionTraceEvent,
    write_execution_trace_jsonl,
)


BASELINE = "675121c3c3180c8436a6e436997247307b19207b"
T0 = datetime(2026, 9, 23, 22, 30, tzinfo=UTC)


def _projection_module():
    return import_module("malak.observability.execution_trace_projection")


def _view_module():
    return import_module("malak.app.trace_view")


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
) -> ExecutionTraceEvent:
    outcomes = {
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
    selected = outcome or outcomes[event_type]
    selected_reason = reason_code
    if selected_reason is None:
        if selected == "SKIPPED":
            selected_reason = "not_required_by_workflow"
        elif selected == "FAILED":
            selected_reason = "component_error"
        elif selected == "INCONCLUSIVE":
            selected_reason = "required_evidence_missing"

    return ExecutionTraceEvent(
        schema=TRACE_SCHEMA,
        run_id="run-001",
        sequence=sequence,
        occurred_at=T0 + timedelta(seconds=seconds),
        baseline_commit=BASELINE,
        task_id="self-review-v0",
        phase=phase,
        component=component,
        event_type=event_type,
        input_refs=input_refs,
        output_refs=output_refs,
        evidence_refs=evidence_refs,
        outcome=selected,
        reason_code=selected_reason,
        authority_effect="none",
    )


def _events() -> tuple[ExecutionTraceEvent, ...]:
    return (
        _event(
            1,
            "RUN_STARTED",
            output_refs=("run:manifest",),
        ),
        _event(
            2,
            "SCOPE_FROZEN",
            phase="scope",
            seconds=1,
            input_refs=("task:input",),
            output_refs=("scope:frozen",),
        ),
        _event(
            3,
            "EVIDENCE_PACKET_STARTED",
            component="self_review_evidence",
            phase="evidence",
            seconds=2,
            input_refs=("scope:frozen",),
        ),
        _event(
            4,
            "EVIDENCE_PACKET_READY",
            component="self_review_evidence",
            phase="evidence",
            seconds=3,
            input_refs=("scope:frozen",),
            output_refs=("evidence:packet",),
        ),
        _event(
            5,
            "COMPONENT_STARTED",
            component="engineering_inspect",
            phase="engineering",
            seconds=4,
            input_refs=("evidence:packet",),
        ),
        _event(
            6,
            "COMPONENT_COMPLETED",
            component="engineering_inspect",
            phase="engineering",
            seconds=6,
            input_refs=("evidence:packet",),
            output_refs=("engineering:inspect",),
        ),
        _event(
            7,
            "COMPONENT_SKIPPED",
            component="engineering_analyze",
            phase="engineering",
            seconds=7,
            input_refs=("engineering:inspect",),
            reason_code="not_required_by_workflow",
        ),
        _event(
            8,
            "COMPONENT_SKIPPED",
            component="engineering_propose",
            phase="engineering",
            seconds=8,
            input_refs=("engineering:inspect",),
            reason_code="not_required_by_workflow",
        ),
        _event(
            9,
            "TERMINAL_DISPOSITION",
            phase="decision",
            seconds=9,
            input_refs=("engineering:inspect",),
            output_refs=("outcome:terminal",),
        ),
        _event(
            10,
            "ARTIFACT_FINALIZED",
            phase="artifact",
            seconds=10,
            input_refs=("outcome:terminal",),
            output_refs=("artifact:set",),
        ),
        _event(
            11,
            "RUN_STOPPED",
            seconds=11,
            input_refs=("artifact:set",),
        ),
    )


def _write_run(root: Path, run_id: str = "run-001") -> Path:
    trace_path = (
        root
        / "runtime"
        / "internal_interaction"
        / run_id
        / "trace.jsonl"
    )
    write_execution_trace_jsonl(trace_path, _events())
    return trace_path


def test_trace_view_red_c01_renderer_is_deterministic_and_ascii() -> None:
    projection = _projection_module().fold_execution_trace(_events())

    first = _view_module().render_trace_projection(projection)
    second = _view_module().render_trace_projection(projection)

    assert first == second
    assert first.isascii()
    assert "MALAK INTERNAL INTERACTION - run-001" in first
    assert f"baseline {BASELINE}" in first
    assert "[OK] RUN" in first
    assert "Engineering" in first
    assert "[OK] Inspect" in first
    assert "[--] Analyze" in first
    assert "[--] Propose" in first
    assert "[OK] STOP" in first


def test_trace_view_red_c02_renderer_shows_not_observed_without_claiming_waiting() -> None:
    projection = _projection_module().fold_execution_trace(
        (_event(1, "RUN_STARTED"),)
    )

    rendered = _view_module().render_trace_projection(projection)

    assert "[..] Scope" in rendered
    assert "[..] Evidence Packet" in rendered
    assert "[..] Inspect" in rendered
    assert "WAITING" not in rendered


def test_trace_view_red_c03_renderer_shows_running_failed_and_inconclusive_states() -> None:
    running = _projection_module().fold_execution_trace(
        (
            _event(1, "RUN_STARTED"),
            _event(
                2,
                "COMPONENT_STARTED",
                component="engineering_analyze",
                phase="engineering",
                seconds=1,
            ),
        )
    )
    failed = running.apply(
        _event(
            3,
            "COMPONENT_FAILED",
            component="engineering_analyze",
            phase="engineering",
            reason_code="component_error",
            seconds=2,
        )
    )
    inconclusive = _projection_module().fold_execution_trace(
        (
            _event(1, "RUN_STARTED"),
            _event(
                2,
                "EVIDENCE_PACKET_STARTED",
                component="self_review_evidence",
                phase="evidence",
            ),
            _event(
                3,
                "EVIDENCE_PACKET_READY",
                component="self_review_evidence",
                phase="evidence",
                outcome="INCONCLUSIVE",
                reason_code="required_evidence_missing",
                seconds=1,
            ),
        )
    )

    assert "[>>] Analyze" in _view_module().render_trace_projection(running)
    assert "[!!] Analyze" in _view_module().render_trace_projection(failed)
    assert "[??] Evidence Packet" in _view_module().render_trace_projection(
        inconclusive
    )


def test_trace_view_red_c04_completed_component_renders_observed_duration() -> None:
    projection = _projection_module().fold_execution_trace(_events())

    rendered = _view_module().render_trace_projection(projection)

    assert "Inspect" in rendered
    assert "2000 ms" in rendered


def test_trace_view_red_c05_node_inspection_contains_only_projection_metadata() -> None:
    projection = _projection_module().fold_execution_trace(_events())

    rendered = _view_module().render_trace_node(
        projection,
        "engineering_inspect",
    )

    for expected in (
        "node_id: engineering_inspect",
        "status: COMPLETED",
        "phase: engineering",
        "component: engineering_inspect",
        "duration_ms: 2000",
        "outcome: SUCCEEDED",
        "last_sequence: 6",
        "authority_effect: none",
        "input_refs:",
        "output_refs:",
        "evidence_refs:",
    ):
        assert expected in rendered

    lowered = rendered.lower()
    assert "prompt" not in lowered
    assert "chain_of_thought" not in lowered
    assert "component_outputs" not in lowered


def test_trace_view_red_c06_unknown_node_inspection_fails_closed() -> None:
    projection = _projection_module().fold_execution_trace(_events())

    with pytest.raises(KeyError):
        _view_module().render_trace_node(projection, "future-agent")


def test_trace_view_red_c07_replay_reads_only_fixed_runtime_location(
    tmp_path: Path,
) -> None:
    _write_run(tmp_path)

    projection = _view_module().load_trace_projection(
        repository_root=tmp_path,
        run_id="run-001",
    )

    assert projection.run_id == "run-001"
    assert projection.node("run").status == "COMPLETED"
    assert projection.node("engineering_inspect").status == "COMPLETED"


@pytest.mark.parametrize(
    "run_id",
    [
        "../escape",
        "a/b",
        "a\\b",
        "/absolute",
        ".",
        "..",
        " run-001",
        "run-001 ",
        "",
    ],
)
def test_trace_view_red_c08_replay_rejects_unsafe_run_id(
    tmp_path: Path,
    run_id: str,
) -> None:
    with pytest.raises(ValueError):
        _view_module().load_trace_projection(
            repository_root=tmp_path,
            run_id=run_id,
        )


def test_trace_view_red_c09_replay_does_not_accept_arbitrary_trace_path(
    tmp_path: Path,
) -> None:
    outside = tmp_path / "outside.jsonl"
    write_execution_trace_jsonl(outside, _events())

    with pytest.raises((TypeError, ValueError)):
        _view_module().load_trace_projection(
            repository_root=outside,
            run_id="run-001",
        )


def test_trace_view_red_c10_missing_trace_is_controlled_not_found(
    tmp_path: Path,
) -> None:
    with pytest.raises(FileNotFoundError):
        _view_module().load_trace_projection(
            repository_root=tmp_path,
            run_id="run-missing",
        )


def test_trace_view_red_c11_corrupt_trace_fails_closed(tmp_path: Path) -> None:
    trace = (
        tmp_path
        / "runtime"
        / "internal_interaction"
        / "run-001"
        / "trace.jsonl"
    )
    trace.parent.mkdir(parents=True)
    trace.write_text("{not-json}\n", encoding="utf-8")

    with pytest.raises(ValueError):
        _view_module().load_trace_projection(
            repository_root=tmp_path,
            run_id="run-001",
        )


def test_trace_view_red_c12_replay_projection_matches_direct_fold(
    tmp_path: Path,
) -> None:
    _write_run(tmp_path)

    replay = _view_module().load_trace_projection(
        repository_root=tmp_path,
        run_id="run-001",
    )
    direct = _projection_module().fold_execution_trace(_events())

    assert replay == direct
    assert _view_module().render_trace_projection(replay) == (
        _view_module().render_trace_projection(direct)
    )


def test_trace_view_red_c13_live_text_view_renders_from_real_events_only() -> None:
    outputs: list[str] = []
    live = _view_module().LiveTraceTextView(output_fn=outputs.append)

    for event in _events():
        live.append(event)

    assert live.projection == _projection_module().fold_execution_trace(
        _events()
    )
    assert outputs
    assert outputs[-1] == _view_module().render_trace_projection(
        live.projection
    )
    assert "[OK] STOP" in outputs[-1]


def test_live_elapsed_red_a01_running_node_refreshes_without_new_trace_event() -> None:
    outputs: list[str] = []
    monotonic = [100.0]
    live = _view_module().LiveTraceTextView(
        output_fn=outputs.append,
        monotonic_fn=lambda: monotonic[0],
        refresh_interval_seconds=10.0,
    )
    events = (
        _event(1, "RUN_STARTED"),
        _event(
            2,
            "COMPONENT_STARTED",
            component="engineering_analyze",
            phase="engineering",
            seconds=1,
        ),
    )

    for event in events:
        live.append(event)

    projection_before = live.projection
    sequence_before = live.projection.last_sequence
    monotonic[0] = 101.25

    live.refresh_elapsed()

    assert live.projection == projection_before
    assert live.projection.last_sequence == sequence_before
    assert "[>>] Analyze elapsed=1250 ms" in outputs[-1]


def test_live_elapsed_red_a02_never_renders_fake_progress_or_eta() -> None:
    outputs: list[str] = []
    monotonic = [20.0]
    live = _view_module().LiveTraceTextView(
        output_fn=outputs.append,
        monotonic_fn=lambda: monotonic[0],
        refresh_interval_seconds=10.0,
    )
    live.append(_event(1, "RUN_STARTED"))
    live.append(
        _event(
            2,
            "COMPONENT_STARTED",
            component="engineering_inspect",
            phase="engineering",
            seconds=1,
        )
    )
    monotonic[0] = 25.0

    live.refresh_elapsed()

    rendered = outputs[-1].lower()
    assert "elapsed=5000 ms" in rendered
    assert "%" not in rendered
    assert "eta" not in rendered
    assert "progress=" not in rendered
    assert "almost done" not in rendered


def test_live_elapsed_red_a03_uses_monotonic_clock_not_event_wall_clock() -> None:
    outputs: list[str] = []
    monotonic = [500.0]
    live = _view_module().LiveTraceTextView(
        output_fn=outputs.append,
        monotonic_fn=lambda: monotonic[0],
        refresh_interval_seconds=10.0,
    )
    live.append(_event(1, "RUN_STARTED", seconds=0))
    live.append(
        _event(
            2,
            "COMPONENT_STARTED",
            component="engineering_inspect",
            phase="engineering",
            seconds=100,
        )
    )
    monotonic[0] = 501.5

    live.refresh_elapsed()

    assert "elapsed=1500 ms" in outputs[-1]


def test_live_elapsed_red_a04_terminal_node_stops_elapsed_and_uses_trace_duration() -> None:
    outputs: list[str] = []
    monotonic = [30.0]
    live = _view_module().LiveTraceTextView(
        output_fn=outputs.append,
        monotonic_fn=lambda: monotonic[0],
        refresh_interval_seconds=10.0,
    )
    live.append(_event(1, "RUN_STARTED"))
    live.append(
        _event(
            2,
            "COMPONENT_STARTED",
            component="engineering_inspect",
            phase="engineering",
            seconds=4,
        )
    )
    monotonic[0] = 37.5
    live.refresh_elapsed()
    assert "elapsed=7500 ms" in outputs[-1]

    live.append(
        _event(
            3,
            "COMPONENT_COMPLETED",
            component="engineering_inspect",
            phase="engineering",
            seconds=6,
        )
    )
    monotonic[0] = 99.0
    live.refresh_elapsed()

    rendered = outputs[-1]
    assert "[OK] Inspect 2000 ms" in rendered
    assert "Inspect elapsed=" not in rendered


def test_live_elapsed_red_a05_ticker_stops_and_cannot_outlive_teardown() -> None:
    outputs: list[str] = []
    live = _view_module().LiveTraceTextView(
        output_fn=outputs.append,
        refresh_interval_seconds=0.01,
    )
    live.append(_event(1, "RUN_STARTED"))
    live.append(
        _event(
            2,
            "COMPONENT_STARTED",
            component="engineering_analyze",
            phase="engineering",
            seconds=1,
        )
    )

    live.start_liveness()
    deadline = time.monotonic() + 0.5
    while (
        not any("elapsed=" in item for item in outputs)
        and time.monotonic() < deadline
    ):
        time.sleep(0.01)

    assert live.liveness_active is True
    assert any("elapsed=" in item for item in outputs)

    live.stop_liveness()
    count_after_stop = len(outputs)
    time.sleep(0.05)

    assert live.liveness_active is False
    assert len(outputs) == count_after_stop


def test_live_elapsed_red_a06_final_material_projection_still_matches_replay_fold() -> None:
    outputs: list[str] = []
    live = _view_module().LiveTraceTextView(
        output_fn=outputs.append,
        refresh_interval_seconds=10.0,
    )

    events = _events()
    for event in events:
        live.append(event)

    live.refresh_elapsed()

    assert live.projection == _projection_module().fold_execution_trace(events)
    assert live.projection.stopped is True
    assert "elapsed=" not in outputs[-1]
