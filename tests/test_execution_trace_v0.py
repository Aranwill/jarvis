from __future__ import annotations

from dataclasses import FrozenInstanceError
from datetime import datetime, timezone
from importlib import import_module
from pathlib import Path

import pytest


NOW = datetime(2026, 9, 23, 20, 45, tzinfo=timezone.utc)
BASELINE = "eb5a48fad12b8888192139e2b8a552bf50ce4870"


def _module():
    return import_module("malak.observability.execution_trace")


def _event(**overrides):
    values = {
        "schema": "MALAK-EXECUTION-TRACE-EVENT/v0",
        "run_id": "run-001",
        "sequence": 1,
        "occurred_at": NOW,
        "baseline_commit": BASELINE,
        "task_id": "self-review-v0",
        "phase": "scope",
        "component": "internal_interaction",
        "event_type": "RUN_STARTED",
        "input_refs": (),
        "output_refs": ("run:manifest",),
        "evidence_refs": (),
        "outcome": "STARTED",
        "reason_code": None,
        "authority_effect": "none",
    }
    values.update(overrides)
    return _module().ExecutionTraceEvent(**values)


def _trace(*, initial_refs=()):
    return _module().ExecutionTrace(
        run_id="run-001",
        baseline_commit=BASELINE,
        initial_refs=initial_refs,
    )


def test_trace_red_c01_valid_event_is_immutable_and_slotted() -> None:
    event = _event()

    assert event.run_id == "run-001"
    assert event.authority_effect == "none"
    assert not hasattr(event, "__dict__")

    with pytest.raises(FrozenInstanceError):
        event.outcome = "FAILED"  # type: ignore[misc]


@pytest.mark.parametrize(
    "event_type",
    [
        "",
        "UNKNOWN_EVENT",
        "component.started",
        "COMPONENT_SKIPPED_WITHOUT_CONTRACT",
    ],
)
def test_trace_red_c02_unknown_event_type_fails_closed(event_type: str) -> None:
    with pytest.raises(ValueError):
        _event(event_type=event_type)


@pytest.mark.parametrize("outcome", ["", "PASS", "SUCCESS", "unknown"])
def test_trace_red_c03_unknown_outcome_fails_closed(outcome: str) -> None:
    with pytest.raises(ValueError):
        _event(outcome=outcome)


@pytest.mark.parametrize(
    ("event_type", "outcome"),
    [
        ("COMPONENT_FAILED", "FAILED"),
        ("GATE_EVALUATED", "INCONCLUSIVE"),
        ("COMPONENT_SKIPPED", "SKIPPED"),
    ],
)
def test_trace_red_c04_failed_inconclusive_or_skipped_requires_reason(
    event_type: str,
    outcome: str,
) -> None:
    with pytest.raises(ValueError):
        _event(event_type=event_type, outcome=outcome, reason_code=None)


@pytest.mark.parametrize("outcome", ["STARTED", "SUCCEEDED"])
def test_trace_red_c05_started_or_succeeded_rejects_reason_code(
    outcome: str,
) -> None:
    with pytest.raises(ValueError):
        _event(outcome=outcome, reason_code="component_error")


def test_trace_red_c06_unknown_reason_code_fails_closed() -> None:
    with pytest.raises(ValueError):
        _event(
            event_type="COMPONENT_FAILED",
            outcome="FAILED",
            reason_code="raw_exception_text",
        )


@pytest.mark.parametrize("authority_effect", ["allow", "approved", "", "NONE"])
def test_trace_red_c07_authority_effect_must_be_exactly_none(
    authority_effect: str,
) -> None:
    with pytest.raises(ValueError):
        _event(authority_effect=authority_effect)


@pytest.mark.parametrize(
    ("run_id", "sequence"),
    [
        ("", 1),
        (" run-001", 1),
        ("run-001 ", 1),
        ("run-001", 0),
        ("run-001", -1),
        ("run-001", True),
    ],
)
def test_trace_red_c08_invalid_run_identity_or_sequence_is_rejected(
    run_id: str,
    sequence: object,
) -> None:
    with pytest.raises((TypeError, ValueError)):
        _event(run_id=run_id, sequence=sequence)


def test_trace_red_c09_duplicate_or_non_monotonic_sequence_is_rejected() -> None:
    trace = _trace()
    trace.append(_event(sequence=1, output_refs=("ref:one",)))

    with pytest.raises(ValueError):
        trace.append(
            _event(
                sequence=1,
                event_type="SCOPE_FROZEN",
                outcome="SUCCEEDED",
                output_refs=("ref:two",),
            )
        )

    with pytest.raises(ValueError):
        trace.append(
            _event(
                sequence=0,
                event_type="SCOPE_FROZEN",
                outcome="SUCCEEDED",
                output_refs=("ref:three",),
            )
        )

    assert len(trace.events) == 1


@pytest.mark.parametrize(
    ("run_id", "baseline_commit"),
    [
        ("run-other", BASELINE),
        ("run-001", "1" * 40),
    ],
)
def test_trace_red_c10_run_or_baseline_mismatch_is_rejected(
    run_id: str,
    baseline_commit: str,
) -> None:
    trace = _trace()

    with pytest.raises(ValueError):
        trace.append(
            _event(
                run_id=run_id,
                baseline_commit=baseline_commit,
            )
        )

    assert trace.events == ()


@pytest.mark.parametrize("field", ["input_refs", "evidence_refs"])
def test_trace_red_c11_unknown_consumed_reference_is_rejected(
    field: str,
) -> None:
    trace = _trace(initial_refs=("task:input",))
    kwargs = {
        "event_type": "SCOPE_FROZEN",
        "outcome": "SUCCEEDED",
        "output_refs": ("scope:frozen",),
        field: ("unknown:ref",),
    }

    with pytest.raises(ValueError):
        trace.append(_event(**kwargs))

    assert trace.events == ()


def test_trace_red_c12_output_reference_becomes_available_to_later_event() -> None:
    trace = _trace(initial_refs=("task:input",))
    trace.append(
        _event(
            sequence=1,
            event_type="SCOPE_FROZEN",
            outcome="SUCCEEDED",
            input_refs=("task:input",),
            output_refs=("scope:frozen",),
        )
    )
    trace.append(
        _event(
            sequence=2,
            phase="evidence",
            component="self_review_evidence",
            event_type="EVIDENCE_PACKET_READY",
            outcome="SUCCEEDED",
            input_refs=("scope:frozen",),
            output_refs=("evidence:packet",),
        )
    )

    assert len(trace.events) == 2


def test_trace_red_c13_duplicate_output_reference_is_rejected_without_mutation() -> None:
    trace = _trace()
    trace.append(_event(sequence=1, output_refs=("ref:one",)))

    with pytest.raises(ValueError):
        trace.append(
            _event(
                sequence=2,
                event_type="SCOPE_FROZEN",
                outcome="SUCCEEDED",
                output_refs=("ref:one",),
            )
        )

    assert len(trace.events) == 1


def test_trace_red_c14_component_skipped_is_explicit_and_reasoned() -> None:
    event = _event(
        event_type="COMPONENT_SKIPPED",
        phase="engineering",
        component="engineering_propose",
        outcome="SKIPPED",
        reason_code="not_required_by_workflow",
        output_refs=(),
    )

    assert event.outcome == "SKIPPED"
    assert event.reason_code == "not_required_by_workflow"


def test_trace_red_c15_component_projection_uses_real_started_events_only() -> None:
    trace = _trace()
    trace.append(_event(sequence=1, output_refs=("run:manifest",)))
    trace.append(
        _event(
            sequence=2,
            phase="engineering",
            component="engineering_inspect",
            event_type="COMPONENT_STARTED",
            outcome="STARTED",
            input_refs=("run:manifest",),
            output_refs=(),
        )
    )
    trace.append(
        _event(
            sequence=3,
            phase="engineering",
            component="engineering_inspect",
            event_type="COMPONENT_COMPLETED",
            outcome="SUCCEEDED",
            input_refs=("run:manifest",),
            output_refs=("engineering:inspect",),
        )
    )
    trace.append(
        _event(
            sequence=4,
            phase="engineering",
            component="engineering_analyze",
            event_type="COMPONENT_STARTED",
            outcome="STARTED",
            input_refs=("engineering:inspect",),
            output_refs=(),
        )
    )

    assert _module().project_component_path(trace.events) == (
        "engineering_inspect",
        "engineering_analyze",
    )


def test_trace_red_c16_jsonl_round_trip_preserves_replay_path(
    tmp_path: Path,
) -> None:
    trace = _trace()
    trace.append(_event(sequence=1, output_refs=("run:manifest",)))
    trace.append(
        _event(
            sequence=2,
            phase="engineering",
            component="engineering_inspect",
            event_type="COMPONENT_STARTED",
            outcome="STARTED",
            input_refs=("run:manifest",),
            output_refs=(),
        )
    )

    path = tmp_path / "trace.jsonl"
    _module().write_execution_trace_jsonl(path, trace.events)
    replayed = _module().read_execution_trace_jsonl(path)

    assert replayed == trace.events
    assert _module().project_component_path(replayed) == (
        "engineering_inspect",
    )
