from collections.abc import Callable, Iterator

from malak.app.cli import (
    HELP_MESSAGE,
    build_conversation_service,
    build_runtime,
    run_cli,
)
from malak.core.conversation import ConversationRequest
from malak.runtime.mock_llm_runtime import MockLLMRuntime
from malak.runtime.ollama_runtime import OllamaRuntime


def make_input(values: list[str]) -> Callable[[str], str]:
    iterator: Iterator[str] = iter(values)

    def input_fn(_: str) -> str:
        return next(iterator)

    return input_fn


def test_build_conversation_service_uses_mock_provider() -> None:
    service = build_conversation_service()

    response = service.generate(
        request=ConversationRequest(prompt="Hola"),
        provider="mock",
    )

    assert response.content == "[RUNTIME] Hola"
    assert response.provider == "runtime"


def test_build_conversation_service_accepts_injected_runtime() -> None:
    runtime = MockLLMRuntime()

    service = build_conversation_service(
        runtime=runtime,
        provider_name="ollama",
    )

    response = service.generate(
        request=ConversationRequest(prompt="Hola"),
        provider="ollama",
    )

    assert response.content == "[RUNTIME] Hola"
    assert response.provider == "runtime"


def test_build_runtime_defaults_to_mock() -> None:
    runtime = build_runtime()

    assert isinstance(runtime, MockLLMRuntime)


def test_build_runtime_selects_mock_explicitly() -> None:
    runtime = build_runtime(runtime_name="mock")

    assert isinstance(runtime, MockLLMRuntime)


def test_build_runtime_selects_ollama() -> None:
    runtime = build_runtime(runtime_name="ollama")

    assert isinstance(runtime, OllamaRuntime)


def test_build_runtime_rejects_unknown_runtime() -> None:
    try:
        build_runtime(runtime_name="unknown")
    except ValueError as exc:
        assert str(exc) == "Unsupported runtime: unknown"
    else:
        raise AssertionError("Expected ValueError")


def test_run_cli_processes_prompt_and_exits() -> None:
    outputs: list[str] = []

    run_cli(
        input_fn=make_input(["Hola Malāk", "exit"]),
        output_fn=outputs.append,
    )

    assert "Malāk CLI" in outputs
    assert "Malāk> [RUNTIME] Hola Malāk" in outputs
    assert "Sesión finalizada." in outputs


def test_run_cli_rejects_empty_input() -> None:
    outputs: list[str] = []

    run_cli(
        input_fn=make_input(["   ", "exit"]),
        output_fn=outputs.append,
    )

    assert "La entrada no puede estar vacía." in outputs


def test_run_cli_displays_help() -> None:
    outputs: list[str] = []

    run_cli(
        input_fn=make_input(["help", "exit"]),
        output_fn=outputs.append,
    )

    assert HELP_MESSAGE in outputs


def test_run_cli_displays_status() -> None:
    outputs: list[str] = []

    run_cli(
        input_fn=make_input(["status", "exit"]),
        output_fn=outputs.append,
    )

    assert (
        "Estado: operativo | Provider: mock | "
        "Runtime: MockLLMRuntime"
    ) in outputs


def test_run_cli_handles_keyboard_interrupt() -> None:
    outputs: list[str] = []

    def interrupted_input(_: str) -> str:
        raise KeyboardInterrupt

    run_cli(
        input_fn=interrupted_input,
        output_fn=outputs.append,
    )

    assert "Sesión finalizada." in outputs