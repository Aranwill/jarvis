from collections.abc import Callable, Iterator

from malak.app.cli import (
    HELP_MESSAGE,
    build_conversation_service,
    build_runtime,
    run_cli,
    CLIConfiguration,
    build_cli_configuration,
)

from malak.core.conversation import (
    ConversationRequest,
    ConversationResponse,
)

from malak.core.llm_runtime import LLMRuntime
from malak.runtime.mock_llm_runtime import MockLLMRuntime
from malak.runtime.ollama_runtime import OllamaRuntime


def make_input(values: list[str]) -> Callable[[str], str]:
    iterator: Iterator[str] = iter(values)

    def input_fn(_: str) -> str:
        return next(iterator)

    return input_fn


class RecordingRuntime(LLMRuntime):
    def __init__(self) -> None:
        self.last_request: ConversationRequest | None = None

    def generate(
        self,
        request: ConversationRequest,
    ) -> ConversationResponse:
        self.last_request = request

        return ConversationResponse(
            content="Respuesta controlada",
            model=request.model,
            provider="recording-runtime",
        )


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

def test_build_cli_configuration_defaults_to_mock() -> None:
    configuration = build_cli_configuration({})

    assert configuration == CLIConfiguration(
        runtime_name="mock",
        provider_name="mock",
        runtime_display_name="MockLLMRuntime",
        model=None,
        ollama_base_url="http://localhost:11434",
    )


def test_build_cli_configuration_selects_ollama() -> None:
    configuration = build_cli_configuration(
        {
            "MALAK_RUNTIME": "ollama",
            "MALAK_OLLAMA_MODEL": "qwen3.5:9b",
            "MALAK_OLLAMA_BASE_URL": "http://localhost:11434",
        }
    )

    assert configuration == CLIConfiguration(
        runtime_name="ollama",
        provider_name="ollama",
        runtime_display_name="OllamaRuntime",
        model="qwen3.5:9b",
        ollama_base_url="http://localhost:11434",
    )


def test_build_cli_configuration_requires_model_for_ollama() -> None:
    try:
        build_cli_configuration(
            {
                "MALAK_RUNTIME": "ollama",
            }
        )
    except ValueError as exc:
        assert str(exc) == (
            "MALAK_OLLAMA_MODEL is required "
            "when MALAK_RUNTIME=ollama"
        )
    else:
        raise AssertionError("Expected ValueError")


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


def test_run_cli_uses_configured_provider_runtime_and_model() -> None:
    outputs: list[str] = []
    runtime = RecordingRuntime()

    service = build_conversation_service(
        runtime=runtime,
        provider_name="ollama",
    )

    run_cli(
        service=service,
        provider_name="ollama",
        runtime_name="OllamaRuntime",
        model="modelo-local",
        input_fn=make_input(["Hola", "exit"]),
        output_fn=outputs.append,
    )

    assert runtime.last_request is not None
    assert runtime.last_request.prompt == "Hola"
    assert runtime.last_request.model == "modelo-local"
    assert "Runtime activo: OllamaRuntime" in outputs
    assert (
        "Estado: operativo | Provider: ollama | "
        "Runtime: OllamaRuntime"
    ) not in outputs
    assert "Malāk> Respuesta controlada" in outputs


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