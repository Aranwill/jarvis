from collections.abc import Callable, Iterator
from datetime import timedelta, timezone
from malak.core.response import Response
from uuid import UUID

from malak.services.conversation_service import ConversationService

from malak.app.cli import (
    CLIConfiguration,
    HELP_MESSAGE,
    build_cli_configuration,
    build_conversation_service,
    build_runtime,
    main,
    run_cli,
)

from malak.core.conversation import (
    ConversationRequest,
    ConversationResponse,
)

from malak.core.llm_runtime import LLMRuntime
from malak.observability.operational_event import OperationalEvent
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


class RecordingOperationalEventSink:
    def __init__(self) -> None:
        self.events: list[OperationalEvent] = []

    def append(self, event: OperationalEvent) -> None:
        self.events.append(event)


class RecordingKernel:
    def __init__(self) -> None:
        self.requests = []

    def receive(self, request):
        self.requests.append(request)

        return Response(
            content="Respuesta desde Kernel",
            source="conversation",
        )


class FailingOperationalEventSink(RecordingOperationalEventSink):
    def __init__(
        self,
        event_name: str,
        failures: int | None = None,
    ) -> None:
        super().__init__()
        self.event_name = event_name
        self.failures = failures
        self.attempted_event_names: list[str] = []

    def append(self, event: OperationalEvent) -> None:
        self.attempted_event_names.append(event.event_name)

        if event.event_name == self.event_name:
            if self.failures is None or self.failures > 0:
                if self.failures is not None:
                    self.failures -= 1
                raise RuntimeError("sink no disponible")

        super().append(event)


class FailingConversationService:
    def __init__(self) -> None:
        self.call_count = 0

    def generate(
        self,
        request: ConversationRequest,
        provider: str,
        session_id: str | None = None,
    ) -> ConversationResponse:
        self.call_count += 1
        raise RuntimeError("fallo conversacional")


def test_build_conversation_service_uses_mock_provider() -> None:
    service = build_conversation_service()

    response = service.generate(
        request=ConversationRequest(prompt="Hola"),
        provider="mock",
        session_id="build-mock-test",
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
        session_id="build-runtime-test",
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


def test_run_cli_emits_correlated_started_and_succeeded_events(
    monkeypatch,
) -> None:
    fixed_uuid = UUID("12345678-1234-5678-1234-567812345678")
    monkeypatch.setattr(
        "malak.app.cli.uuid.uuid4",
        lambda: fixed_uuid,
    )
    outputs: list[str] = []
    sink = RecordingOperationalEventSink()

    run_cli(
        input_fn=make_input(["Hola Malāk", "exit"]),
        output_fn=outputs.append,
        operational_event_sink=sink,
    )

    assert len(sink.events) == 2
    started, succeeded = sink.events
    assert started == OperationalEvent(
        event_name="conversation.started",
        component="cli",
        occurred_at=started.occurred_at,
        outcome="started",
        request_id=str(fixed_uuid),
        reason_code=None,
    )
    assert succeeded == OperationalEvent(
        event_name="conversation.succeeded",
        component="cli",
        occurred_at=succeeded.occurred_at,
        outcome="succeeded",
        request_id=str(fixed_uuid),
        reason_code=None,
    )
    assert started.occurred_at.utcoffset() == timedelta(0)
    assert succeeded.occurred_at.utcoffset() == timedelta(0)
    assert started.occurred_at.tzinfo is timezone.utc
    assert succeeded.occurred_at.tzinfo is timezone.utc


def test_run_cli_emits_correlated_started_and_failed_events(
    monkeypatch,
) -> None:
    fixed_uuid = UUID("87654321-4321-8765-4321-876543218765")
    monkeypatch.setattr(
        "malak.app.cli.uuid.uuid4",
        lambda: fixed_uuid,
    )
    outputs: list[str] = []
    sink = RecordingOperationalEventSink()
    service = FailingConversationService()

    run_cli(
        service=service,  # type: ignore[arg-type]
        input_fn=make_input(["Hola Malāk", "exit"]),
        output_fn=outputs.append,
        operational_event_sink=sink,
    )

    assert len(sink.events) == 2
    started, failed = sink.events
    assert started.event_name == "conversation.started"
    assert started.request_id == str(fixed_uuid)
    assert failed == OperationalEvent(
        event_name="conversation.failed",
        component="cli",
        occurred_at=failed.occurred_at,
        outcome="failed",
        request_id=str(fixed_uuid),
        reason_code="runtime_error",
    )
    assert "Error controlado: fallo conversacional" in outputs


def test_run_cli_without_sink_preserves_existing_behavior() -> None:
    outputs: list[str] = []

    run_cli(
        input_fn=make_input(["Hola Malāk", "exit"]),
        output_fn=outputs.append,
    )

    assert "Malāk> [RUNTIME] Hola Malāk" in outputs
    assert not any(
        "observabilidad" in output
        for output in outputs
    )


def test_run_cli_does_not_emit_events_for_commands_or_empty_input() -> None:
    outputs: list[str] = []
    sink = RecordingOperationalEventSink()

    run_cli(
        input_fn=make_input(["   ", "help", "status", "exit"]),
        output_fn=outputs.append,
        operational_event_sink=sink,
    )

    assert sink.events == []


def test_run_cli_skips_service_when_started_event_fails_and_continues() -> None:
    outputs: list[str] = []
    runtime = RecordingRuntime()
    service = build_conversation_service(runtime=runtime)
    sink = FailingOperationalEventSink(
        event_name="conversation.started",
        failures=1,
    )

    run_cli(
        service=service,
        input_fn=make_input(["Primero", "Segundo", "exit"]),
        output_fn=outputs.append,
        operational_event_sink=sink,
    )

    assert runtime.last_request is not None
    assert runtime.last_request.prompt == "Segundo"
    assert sink.attempted_event_names == [
        "conversation.started",
        "conversation.started",
        "conversation.succeeded",
    ]
    assert "Error controlado de observabilidad: sink no disponible" in outputs
    assert "Malāk> Respuesta controlada" in outputs


def test_run_cli_preserves_response_when_succeeded_event_fails() -> None:
    outputs: list[str] = []
    sink = FailingOperationalEventSink(
        event_name="conversation.succeeded",
    )

    run_cli(
        input_fn=make_input(["Hola Malāk", "exit"]),
        output_fn=outputs.append,
        operational_event_sink=sink,
    )

    assert sink.attempted_event_names == [
        "conversation.started",
        "conversation.succeeded",
    ]
    assert "Malāk> [RUNTIME] Hola Malāk" in outputs
    assert "Error controlado de observabilidad: sink no disponible" in outputs
    assert "conversation.failed" not in sink.attempted_event_names


def test_run_cli_reports_conversation_and_final_event_failures() -> None:
    outputs: list[str] = []
    sink = FailingOperationalEventSink(
        event_name="conversation.failed",
    )
    service = FailingConversationService()

    run_cli(
        service=service,  # type: ignore[arg-type]
        input_fn=make_input(["Hola Malāk", "exit"]),
        output_fn=outputs.append,
        operational_event_sink=sink,
    )

    assert service.call_count == 1
    assert sink.attempted_event_names == [
        "conversation.started",
        "conversation.failed",
    ]
    assert "Error controlado: fallo conversacional" in outputs
    assert "Error controlado de observabilidad: sink no disponible" in outputs


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
    assert "new     Inicia una nueva conversación." in HELP_MESSAGE

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

def test_main_composes_mock_runtime_by_default(monkeypatch) -> None:
    captured: dict[str, object] = {}

    def fake_run_cli(**kwargs: object) -> None:
        captured.update(kwargs)

    monkeypatch.setattr("malak.app.cli.run_cli", fake_run_cli)
    monkeypatch.setattr("malak.app.cli.environ", {})

    main()

    assert captured["provider_name"] == "mock"
    assert captured["runtime_name"] == "MockLLMRuntime"
    assert captured["model"] is None
    assert isinstance(captured["service"], ConversationService)

def test_run_cli_routes_prompt_through_kernel(monkeypatch) -> None:
    outputs: list[str] = []
    kernel = RecordingKernel()

    def fake_build_conversation_kernel(**kwargs):
        return kernel

    monkeypatch.setattr(
        "malak.app.cli.build_conversation_kernel",
        fake_build_conversation_kernel,
    )

    run_cli(
        service=build_conversation_service(),
        input_fn=make_input(["Hola", "exit"]),
        output_fn=outputs.append,
    )

    assert len(kernel.requests) == 1
    assert kernel.requests[0].content == "Hola"
    assert (
        str(UUID(kernel.requests[0].session_id))
        == kernel.requests[0].session_id
    )
    assert "Malāk> Respuesta desde Kernel" in outputs

def test_run_cli_preserves_history_between_prompts() -> None:
    outputs: list[str] = []
    runtime = RecordingRuntime()
    service = build_conversation_service(runtime=runtime)

    run_cli(
        service=service,
        input_fn=make_input(["Primero", "Segundo", "exit"]),
        output_fn=outputs.append,
    )

    assert runtime.last_request is not None
    assert runtime.last_request.prompt == "Segundo"
    assert [
        (message.role, message.content)
        for message in runtime.last_request.history
    ] == [
        ("user", "Primero"),
        ("assistant", "Respuesta controlada"),
    ]


def test_run_cli_new_resets_history_without_generating() -> None:
    outputs: list[str] = []
    runtime = RecordingRuntime()
    service = build_conversation_service(runtime=runtime)

    run_cli(
        service=service,
        input_fn=make_input(
            ["Primero", "new", "Segundo", "exit"]
        ),
        output_fn=outputs.append,
    )

    assert runtime.last_request is not None
    assert runtime.last_request.prompt == "Segundo"
    assert runtime.last_request.history == ()
    assert outputs.count("Malāk> Respuesta controlada") == 2
    assert "Nueva conversación iniciada." in outputs

def test_run_cli_new_rotates_session_id(monkeypatch) -> None:
    outputs: list[str] = []
    kernel = RecordingKernel()

    generated_uuids = iter(
        [
            UUID("11111111-1111-1111-1111-111111111111"),
            UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
            UUID("22222222-2222-2222-2222-222222222222"),
            UUID("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"),
        ]
    )

    monkeypatch.setattr(
        "malak.app.cli.uuid.uuid4",
        lambda: next(generated_uuids),
    )

    def fake_build_conversation_kernel(**kwargs):
        return kernel

    monkeypatch.setattr(
        "malak.app.cli.build_conversation_kernel",
        fake_build_conversation_kernel,
    )

    run_cli(
        service=build_conversation_service(),
        input_fn=make_input(
            ["Primero", "new", "Segundo", "exit"]
        ),
        output_fn=outputs.append,
    )

    assert len(kernel.requests) == 2
    assert (
        kernel.requests[0].session_id
        == "11111111-1111-1111-1111-111111111111"
    )
    assert (
        kernel.requests[1].session_id
        == "22222222-2222-2222-2222-222222222222"
    )
    assert (
        kernel.requests[0].session_id
        != kernel.requests[1].session_id
    )
