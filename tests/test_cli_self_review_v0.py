from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

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
from malak.runtime.ollama_runtime import OllamaRuntime


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


class _HarnessResult:
    def summary(self) -> dict[str, object]:
        return {
            "run_id": "bootstrap-v0-001",
            "baseline_commit": "b" * 40,
            "runtime": "OllamaRuntime",
            "model": "qwen3:8b",
            "terminal_disposition": "NO_CHANGE_RECOMMENDED",
            "component_path": [
                "engineering_inspect",
                "engineering_analyze",
            ],
            "artifact_dir": "runtime/internal_interaction/bootstrap-v0-001",
            "live_replay_equivalence": True,
            "authority_effect": "none",
        }


class _HarnessStub:
    constructor_calls: list[dict[str, object]] = []
    run_calls: list[dict[str, object]] = []

    def __init__(self, **kwargs) -> None:
        type(self).constructor_calls.append(kwargs)

    def run(self, **kwargs):
        type(self).run_calls.append(kwargs)
        return _HarnessResult()


@pytest.fixture(autouse=True)
def _reset_harness_stub() -> None:
    _HarnessStub.constructor_calls.clear()
    _HarnessStub.run_calls.clear()


def _ollama() -> OllamaRuntime:
    return OllamaRuntime(base_url="http://127.0.0.1:11434")


def test_cli_self_review_red_c01_help_is_explicit_and_side_effect_free(
    monkeypatch,
    tmp_path: Path,
) -> None:
    outputs: list[str] = []
    conversation_runtime = _RecordingRuntime()

    monkeypatch.setattr(
        "malak.app.cli.InternalInteractionTestV0Harness",
        _HarnessStub,
        raising=False,
    )

    run_cli(
        service=build_conversation_service(runtime=conversation_runtime),
        runtime=_ollama(),
        runtime_name="OllamaRuntime",
        model="qwen3:8b",
        engineering=object(),
        repository_root=tmp_path,
        input_fn=_make_input(["/self-review help", "exit"]),
        output_fn=outputs.append,
    )

    rendered = "\n".join(outputs)
    assert "/self-review test-v0 <run_id> <validation_ref>" in rendered
    assert "read-only" in rendered.lower()
    assert "Ollama" in rendered
    assert "self-modification" in rendered.lower()
    assert "Owner" in rendered
    assert conversation_runtime.requests == []
    assert _HarnessStub.constructor_calls == []
    assert _HarnessStub.run_calls == []


def test_cli_self_review_red_c02_valid_command_routes_to_harness_without_conversation(
    monkeypatch,
    tmp_path: Path,
) -> None:
    outputs: list[str] = []
    conversation_runtime = _RecordingRuntime()
    runtime = _ollama()
    engineering = object()

    monkeypatch.setattr(
        "malak.app.cli.InternalInteractionTestV0Harness",
        _HarnessStub,
        raising=False,
    )

    run_cli(
        service=build_conversation_service(runtime=conversation_runtime),
        runtime=runtime,
        runtime_name="OllamaRuntime",
        model="qwen3:8b",
        engineering=engineering,
        repository_root=tmp_path,
        input_fn=_make_input(
            [
                (
                    "/self-review test-v0 bootstrap-v0-001 "
                    "Validation#460 Validation#458"
                ),
                "exit",
            ]
        ),
        output_fn=outputs.append,
    )

    assert conversation_runtime.requests == []
    assert len(_HarnessStub.constructor_calls) == 1
    constructor = _HarnessStub.constructor_calls[0]
    assert constructor["repository_root"] == tmp_path
    assert constructor["engineering"] is engineering
    assert constructor["runtime"] is runtime
    assert constructor["model"] == "qwen3:8b"
    assert constructor["output_fn"] == outputs.append

    assert len(_HarnessStub.run_calls) == 1
    call = _HarnessStub.run_calls[0]
    assert call["run_id"] == "bootstrap-v0-001"
    assert call["external_validation_refs"] == (
        "Validation#460",
        "Validation#458",
    )
    assert "task_id" not in call
    assert "scope" not in call

    rendered = "\n".join(outputs)
    assert "Malāk [self-review/test-v0]" in rendered
    assert "terminal_disposition: NO_CHANGE_RECOMMENDED" in rendered
    assert "live_replay_equivalence: true" in rendered
    assert "authority_effect: none" in rendered


@pytest.mark.parametrize(
    "command",
    [
        "/self-review",
        "/self-review test-v0",
        "/self-review test-v0 bootstrap-v0-001",
        "/self-review run bootstrap-v0-001 Validation#460",
        "/self-review execute bootstrap-v0-001 Validation#460",
        "/self-review unknown",
    ],
)
def test_cli_self_review_red_c03_invalid_commands_never_fall_back_to_conversation(
    monkeypatch,
    tmp_path: Path,
    command: str,
) -> None:
    outputs: list[str] = []
    conversation_runtime = _RecordingRuntime()

    monkeypatch.setattr(
        "malak.app.cli.InternalInteractionTestV0Harness",
        _HarnessStub,
        raising=False,
    )

    run_cli(
        service=build_conversation_service(runtime=conversation_runtime),
        runtime=_ollama(),
        runtime_name="OllamaRuntime",
        model="qwen3:8b",
        engineering=object(),
        repository_root=tmp_path,
        input_fn=_make_input([command, "exit"]),
        output_fn=outputs.append,
    )

    assert conversation_runtime.requests == []
    assert _HarnessStub.constructor_calls == []
    assert _HarnessStub.run_calls == []
    assert any("Comando Self-Review inválido" in item for item in outputs)


def test_cli_self_review_red_c04_controlled_harness_error_never_falls_back(
    monkeypatch,
    tmp_path: Path,
) -> None:
    outputs: list[str] = []
    conversation_runtime = _RecordingRuntime()

    class _FailingHarness:
        def __init__(self, **_) -> None:
            raise ValueError("preflight rejected")

    monkeypatch.setattr(
        "malak.app.cli.InternalInteractionTestV0Harness",
        _FailingHarness,
        raising=False,
    )

    run_cli(
        service=build_conversation_service(runtime=conversation_runtime),
        runtime=_ollama(),
        runtime_name="OllamaRuntime",
        model="qwen3:8b",
        engineering=object(),
        repository_root=tmp_path,
        input_fn=_make_input(
            [
                "/self-review test-v0 bootstrap-v0-001 Validation#460",
                "exit",
            ]
        ),
        output_fn=outputs.append,
    )

    assert conversation_runtime.requests == []
    assert any(
        "Error controlado Self-Review: preflight rejected" in item
        for item in outputs
    )


def test_cli_self_review_red_c05_missing_repository_is_controlled(
    monkeypatch,
) -> None:
    outputs: list[str] = []
    conversation_runtime = _RecordingRuntime()

    monkeypatch.setattr(
        "malak.app.cli.InternalInteractionTestV0Harness",
        _HarnessStub,
        raising=False,
    )

    run_cli(
        service=build_conversation_service(runtime=conversation_runtime),
        runtime=_ollama(),
        runtime_name="OllamaRuntime",
        model="qwen3:8b",
        engineering=None,
        repository_root=None,
        input_fn=_make_input(
            [
                "/self-review test-v0 bootstrap-v0-001 Validation#460",
                "exit",
            ]
        ),
        output_fn=outputs.append,
    )

    assert conversation_runtime.requests == []
    assert _HarnessStub.constructor_calls == []
    assert any(
        "Self-Review no disponible: configura MALAK_REPOSITORY_ROOT."
        in item
        for item in outputs
    )


def test_cli_self_review_red_c06_missing_runtime_is_controlled(
    monkeypatch,
    tmp_path: Path,
) -> None:
    outputs: list[str] = []
    conversation_runtime = _RecordingRuntime()

    monkeypatch.setattr(
        "malak.app.cli.InternalInteractionTestV0Harness",
        _HarnessStub,
        raising=False,
    )

    run_cli(
        service=build_conversation_service(runtime=conversation_runtime),
        runtime=None,
        runtime_name="MockLLMRuntime",
        model=None,
        engineering=object(),
        repository_root=tmp_path,
        input_fn=_make_input(
            [
                "/self-review test-v0 bootstrap-v0-001 Validation#460",
                "exit",
            ]
        ),
        output_fn=outputs.append,
    )

    assert conversation_runtime.requests == []
    assert _HarnessStub.constructor_calls == []
    assert any("Self-Review no disponible" in item for item in outputs)


def test_cli_self_review_red_c07_main_passes_exact_runtime_to_cli(
    monkeypatch,
) -> None:
    captured: dict[str, object] = {}
    runtime = object()

    monkeypatch.setattr(
        "malak.app.cli.build_runtime",
        lambda **_: runtime,
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
        {
            "MALAK_RUNTIME": "ollama",
            "MALAK_OLLAMA_MODEL": "qwen3:8b",
            "MALAK_REPOSITORY_ROOT": "D:/Ollama/jarvis",
        },
    )

    main()

    assert captured["runtime"] is runtime
    assert captured["runtime_name"] == "OllamaRuntime"
    assert captured["model"] == "qwen3:8b"
    assert captured["repository_root"] == "D:/Ollama/jarvis"
