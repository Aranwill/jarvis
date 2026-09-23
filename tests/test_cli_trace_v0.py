from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from malak.app.cli import (
    build_conversation_service,
    main,
    run_cli,
)
from malak.core.conversation import (
    ConversationRequest,
    ConversationResponse,
)
from malak.core.llm_runtime import LLMRuntime
from malak.observability.execution_trace import (
    TRACE_SCHEMA,
    ExecutionTraceEvent,
    write_execution_trace_jsonl,
)


BASELINE = "675121c3c3180c8436a6e436997247307b19207b"
T0 = datetime(2026, 9, 23, 23, 0, tzinfo=UTC)


def _make_input(values: list[str]):
    iterator = iter(values)

    def input_fn(_: str) -> str:
        return next(iterator)

    return input_fn


class _RecordingRuntime(LLMRuntime):
    def __init__(self) -> None:
        self.requests: list[ConversationRequest] = []

    def generate(
        self,
        request: ConversationRequest,
    ) -> ConversationResponse:
        self.requests.append(request)
        return ConversationResponse(
            content="NO_DEBE_INVOCARSE",
            model=request.model,
            provider="recording",
        )


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
) -> ExecutionTraceEvent:
    outcomes = {
        "RUN_STARTED": "STARTED",
        "SCOPE_FROZEN": "SUCCEEDED",
        "COMPONENT_STARTED": "STARTED",
        "COMPONENT_COMPLETED": "SUCCEEDED",
        "COMPONENT_SKIPPED": "SKIPPED",
        "TERMINAL_DISPOSITION": "SUCCEEDED",
        "ARTIFACT_FINALIZED": "SUCCEEDED",
        "RUN_STOPPED": "SUCCEEDED",
    }
    selected = outcome or outcomes[event_type]
    selected_reason = reason_code
    if selected == "SKIPPED" and selected_reason is None:
        selected_reason = "not_required_by_workflow"

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
        evidence_refs=(),
        outcome=selected,
        reason_code=selected_reason,
        authority_effect="none",
    )


def _write_run(root: Path) -> None:
    events = (
        _event(1, "RUN_STARTED", output_refs=("run:manifest",)),
        _event(
            2,
            "SCOPE_FROZEN",
            phase="scope",
            input_refs=("task:input",),
            output_refs=("scope:frozen",),
            seconds=1,
        ),
        _event(
            3,
            "COMPONENT_STARTED",
            component="engineering_inspect",
            phase="engineering",
            input_refs=("scope:frozen",),
            seconds=2,
        ),
        _event(
            4,
            "COMPONENT_COMPLETED",
            component="engineering_inspect",
            phase="engineering",
            input_refs=("scope:frozen",),
            output_refs=("engineering:inspect",),
            seconds=4,
        ),
        _event(
            5,
            "COMPONENT_SKIPPED",
            component="engineering_analyze",
            phase="engineering",
            input_refs=("engineering:inspect",),
            seconds=5,
        ),
        _event(
            6,
            "COMPONENT_SKIPPED",
            component="engineering_propose",
            phase="engineering",
            input_refs=("engineering:inspect",),
            seconds=6,
        ),
        _event(
            7,
            "TERMINAL_DISPOSITION",
            phase="decision",
            input_refs=("engineering:inspect",),
            output_refs=("outcome:terminal",),
            seconds=7,
        ),
        _event(
            8,
            "ARTIFACT_FINALIZED",
            phase="artifact",
            input_refs=("outcome:terminal",),
            output_refs=("artifact:set",),
            seconds=8,
        ),
        _event(
            9,
            "RUN_STOPPED",
            input_refs=("artifact:set",),
            seconds=9,
        ),
    )
    path = (
        root
        / "runtime"
        / "internal_interaction"
        / "run-001"
        / "trace.jsonl"
    )
    write_execution_trace_jsonl(path, events)


def test_cli_trace_red_c01_help_is_deterministic_and_does_not_call_model(
    tmp_path: Path,
) -> None:
    outputs: list[str] = []
    runtime = _RecordingRuntime()

    run_cli(
        service=build_conversation_service(runtime=runtime),
        repository_root=tmp_path,
        input_fn=_make_input(["/trace help", "exit"]),
        output_fn=outputs.append,
    )

    rendered = "\n".join(outputs)
    assert "/trace replay <run_id>" in rendered
    assert "/trace inspect <run_id> <node_id>" in rendered
    assert "/trace run" not in rendered
    assert runtime.requests == []


def test_cli_trace_red_c02_replay_renders_existing_trace_without_model_call(
    tmp_path: Path,
) -> None:
    _write_run(tmp_path)
    outputs: list[str] = []
    runtime = _RecordingRuntime()

    run_cli(
        service=build_conversation_service(runtime=runtime),
        repository_root=tmp_path,
        input_fn=_make_input(["/trace replay run-001", "exit"]),
        output_fn=outputs.append,
    )

    rendered = "\n".join(outputs)
    assert "MALAK INTERNAL INTERACTION - run-001" in rendered
    assert "[OK] RUN" in rendered
    assert "[OK] Inspect" in rendered
    assert "[--] Analyze" in rendered
    assert "[--] Propose" in rendered
    assert "[OK] STOP" in rendered
    assert runtime.requests == []


def test_cli_trace_red_c03_inspect_renders_projection_metadata_without_model_call(
    tmp_path: Path,
) -> None:
    _write_run(tmp_path)
    outputs: list[str] = []
    runtime = _RecordingRuntime()

    run_cli(
        service=build_conversation_service(runtime=runtime),
        repository_root=tmp_path,
        input_fn=_make_input(
            [
                "/trace inspect run-001 engineering_inspect",
                "exit",
            ]
        ),
        output_fn=outputs.append,
    )

    rendered = "\n".join(outputs)
    assert "node_id: engineering_inspect" in rendered
    assert "status: COMPLETED" in rendered
    assert "duration_ms: 2000" in rendered
    assert "authority_effect: none" in rendered
    assert "prompt" not in rendered.lower()
    assert runtime.requests == []


@pytest.mark.parametrize(
    "command",
    [
        "/trace run run-001",
        "/trace execute run-001",
        "/trace replay",
        "/trace inspect run-001",
        "/trace unknown run-001",
    ],
)
def test_cli_trace_red_c04_invalid_or_execution_commands_do_not_fall_back_to_model(
    tmp_path: Path,
    command: str,
) -> None:
    outputs: list[str] = []
    runtime = _RecordingRuntime()

    run_cli(
        service=build_conversation_service(runtime=runtime),
        repository_root=tmp_path,
        input_fn=_make_input([command, "exit"]),
        output_fn=outputs.append,
    )

    assert any("Comando Trace inválido" in output for output in outputs)
    assert runtime.requests == []


def test_cli_trace_red_c05_trace_requires_explicit_repository_root() -> None:
    outputs: list[str] = []
    runtime = _RecordingRuntime()

    run_cli(
        service=build_conversation_service(runtime=runtime),
        input_fn=_make_input(["/trace replay run-001", "exit"]),
        output_fn=outputs.append,
    )

    assert (
        "Trace no disponible: configura MALAK_REPOSITORY_ROOT."
        in outputs
    )
    assert runtime.requests == []


@pytest.mark.parametrize(
    "run_id",
    [
        "../escape",
        "a/b",
        "a\\b",
        "..",
    ],
)
def test_cli_trace_red_c06_unsafe_run_id_is_controlled_and_does_not_call_model(
    tmp_path: Path,
    run_id: str,
) -> None:
    outputs: list[str] = []
    runtime = _RecordingRuntime()

    run_cli(
        service=build_conversation_service(runtime=runtime),
        repository_root=tmp_path,
        input_fn=_make_input(
            [
                f"/trace replay {run_id}",
                "exit",
            ]
        ),
        output_fn=outputs.append,
    )

    assert any("Error controlado Trace:" in output for output in outputs)
    assert runtime.requests == []


def test_cli_trace_red_c07_missing_run_is_controlled_and_does_not_call_model(
    tmp_path: Path,
) -> None:
    outputs: list[str] = []
    runtime = _RecordingRuntime()

    run_cli(
        service=build_conversation_service(runtime=runtime),
        repository_root=tmp_path,
        input_fn=_make_input(
            [
                "/trace replay run-missing",
                "exit",
            ]
        ),
        output_fn=outputs.append,
    )

    assert any("Error controlado Trace:" in output for output in outputs)
    assert runtime.requests == []


def test_cli_trace_red_c08_corrupt_replay_is_controlled_and_does_not_call_model(
    tmp_path: Path,
) -> None:
    trace = (
        tmp_path
        / "runtime"
        / "internal_interaction"
        / "run-001"
        / "trace.jsonl"
    )
    trace.parent.mkdir(parents=True)
    trace.write_text("{broken}\n", encoding="utf-8")

    outputs: list[str] = []
    runtime = _RecordingRuntime()

    run_cli(
        service=build_conversation_service(runtime=runtime),
        repository_root=tmp_path,
        input_fn=_make_input(
            [
                "/trace replay run-001",
                "exit",
            ]
        ),
        output_fn=outputs.append,
    )

    assert any("Error controlado Trace:" in output for output in outputs)
    assert runtime.requests == []


def test_cli_trace_red_c09_main_propagates_explicit_repository_root_to_cli(
    monkeypatch,
) -> None:
    captured: dict[str, object] = {}

    monkeypatch.setattr(
        "malak.app.cli.build_runtime",
        lambda **_: object(),
    )
    monkeypatch.setattr(
        "malak.app.cli.build_conversation_service",
        lambda **_: object(),
    )
    monkeypatch.setattr(
        "malak.app.cli.build_engineering_kernel_set",
        lambda **_: object(),
    )
    monkeypatch.setattr(
        "malak.app.cli.run_cli",
        lambda **kwargs: captured.update(kwargs),
    )
    monkeypatch.setattr(
        "malak.app.cli.environ",
        {"MALAK_REPOSITORY_ROOT": "D:/Ollama/jarvis"},
    )

    main()

    assert captured["repository_root"] == "D:/Ollama/jarvis"
