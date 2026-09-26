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


def test_build_conversation_service_supports_stateless_engineering_use() -> None:
    runtime = RecordingRuntime()

    service = build_conversation_service(
        runtime=runtime,
        provider_name="mock",
        with_context=False,
    )

    response = service.generate(
        request=ConversationRequest(prompt="Inspect Memory"),
        provider="mock",
    )

    assert response.content == "Respuesta controlada"
    assert runtime.last_request is not None
    assert runtime.last_request.prompt == "Inspect Memory"
    assert runtime.last_request.history == ()


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


def test_build_cli_configuration_builds_generation_contract() -> None:
    configuration = build_cli_configuration(
        {
            "MALAK_RUNTIME": "ollama",
            "MALAK_OLLAMA_MODEL": "qwen3.5:9b",
            "MALAK_OLLAMA_CONTEXT_WINDOW_TOKENS": "8192",
            "MALAK_OLLAMA_MAX_OUTPUT_TOKENS": "2048",
            "MALAK_OLLAMA_THINKING": "disabled",
        }
    )

    contract = configuration.generation_contract
    assert contract is not None
    assert contract.context_window_tokens == 8192
    assert contract.max_output_tokens == 2048
    assert contract.thinking_enabled is False


def test_build_cli_configuration_rejects_partial_generation_contract() -> None:
    try:
        build_cli_configuration(
            {
                "MALAK_RUNTIME": "ollama",
                "MALAK_OLLAMA_MODEL": "qwen3.5:9b",
                "MALAK_OLLAMA_CONTEXT_WINDOW_TOKENS": "8192",
            }
        )
    except ValueError as exc:
        assert "required together" in str(exc)
    else:
        raise AssertionError("Expected ValueError")


def test_build_cli_configuration_rejects_ambiguous_thinking_mode() -> None:
    try:
        build_cli_configuration(
            {
                "MALAK_RUNTIME": "ollama",
                "MALAK_OLLAMA_MODEL": "qwen3.5:9b",
                "MALAK_OLLAMA_CONTEXT_WINDOW_TOKENS": "8192",
                "MALAK_OLLAMA_MAX_OUTPUT_TOKENS": "2048",
                "MALAK_OLLAMA_THINKING": "auto",
            }
        )
    except ValueError as exc:
        assert "enabled" in str(exc)
        assert "disabled" in str(exc)
    else:
        raise AssertionError("Expected ValueError")


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


class RecordingEngineeringKernel:
    def __init__(self, action: str) -> None:
        self.action = action
        self.requests = []

    def receive(self, request):
        self.requests.append(request)

        return Response(
            content=f"{self.action}-payload",
            source=f"engineering_{self.action}",
        )


class FailingEngineeringKernel(RecordingEngineeringKernel):
    def receive(self, request):
        self.requests.append(request)
        raise RuntimeError("fallo engineering")


class EngineeringKernelSetStub:
    def __init__(self) -> None:
        self.baseline_commit = (
            "0123456789abcdef0123456789abcdef01234567"
        )
        self.kernels = {
            action: RecordingEngineeringKernel(action)
            for action in ("inspect", "analyze", "propose")
        }


def test_build_cli_configuration_preserves_explicit_repository_root() -> None:
    configuration = build_cli_configuration(
        {
            "MALAK_REPOSITORY_ROOT": "D:/Ollama/jarvis",
        }
    )

    assert configuration.repository_root == "D:/Ollama/jarvis"


def test_build_cli_configuration_does_not_infer_repository_root() -> None:
    configuration = build_cli_configuration({})

    assert configuration.repository_root is None


def test_main_composes_engineering_only_from_explicit_repository_root(
    monkeypatch,
) -> None:
    captured: dict[str, object] = {}
    builder_calls: list[dict[str, object]] = []
    engineering = EngineeringKernelSetStub()

    def fake_run_cli(**kwargs: object) -> None:
        captured.update(kwargs)

    def fake_build_engineering_kernel_set(**kwargs: object):
        builder_calls.append(kwargs)
        return engineering

    monkeypatch.setattr("malak.app.cli.run_cli", fake_run_cli)
    monkeypatch.setattr(
        "malak.app.cli.build_engineering_kernel_set",
        fake_build_engineering_kernel_set,
        raising=False,
    )
    monkeypatch.setattr(
        "malak.app.cli.environ",
        {"MALAK_REPOSITORY_ROOT": "D:/Ollama/jarvis"},
    )

    main()

    assert len(builder_calls) == 1
    assert builder_calls[0]["repository_root"] == "D:/Ollama/jarvis"
    assert captured["engineering"] is engineering


def test_main_uses_separate_stateless_service_for_engineering(
    monkeypatch,
) -> None:
    service_builds: list[tuple[bool, object]] = []
    captured_cli: dict[str, object] = {}
    captured_engineering: dict[str, object] = {}

    def fake_build_conversation_service(
        runtime=None,
        provider_name="mock",
        *,
        with_context=True,
    ):
        service = object()
        service_builds.append((with_context, service))
        return service

    def fake_build_engineering_kernel_set(**kwargs: object):
        captured_engineering.update(kwargs)
        return EngineeringKernelSetStub()

    def fake_run_cli(**kwargs: object) -> None:
        captured_cli.update(kwargs)

    monkeypatch.setattr(
        "malak.app.cli.build_conversation_service",
        fake_build_conversation_service,
    )
    monkeypatch.setattr(
        "malak.app.cli.build_engineering_kernel_set",
        fake_build_engineering_kernel_set,
    )
    monkeypatch.setattr("malak.app.cli.run_cli", fake_run_cli)
    monkeypatch.setattr(
        "malak.app.cli.environ",
        {"MALAK_REPOSITORY_ROOT": "D:/Ollama/jarvis"},
    )

    main()

    assert [with_context for with_context, _ in service_builds] == [
        True,
        False,
    ]
    conversation_service = service_builds[0][1]
    engineering_service = service_builds[1][1]
    assert conversation_service is not engineering_service
    assert captured_cli["service"] is conversation_service
    assert captured_engineering["service"] is engineering_service


def test_main_does_not_use_current_working_directory_as_repository_root(
    monkeypatch,
    tmp_path,
) -> None:
    captured: dict[str, object] = {}
    builder_calls: list[dict[str, object]] = []

    def fake_run_cli(**kwargs: object) -> None:
        captured.update(kwargs)

    def fake_build_engineering_kernel_set(**kwargs: object):
        builder_calls.append(kwargs)
        return EngineeringKernelSetStub()

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("malak.app.cli.run_cli", fake_run_cli)
    monkeypatch.setattr(
        "malak.app.cli.build_engineering_kernel_set",
        fake_build_engineering_kernel_set,
        raising=False,
    )
    monkeypatch.setattr("malak.app.cli.environ", {})

    main()

    assert builder_calls == []
    assert captured["engineering"] is None


def test_run_cli_engineering_help_is_deterministic_and_side_effect_free(
    monkeypatch,
) -> None:
    outputs: list[str] = []
    conversation_kernel = RecordingKernel()
    engineering = EngineeringKernelSetStub()

    monkeypatch.setattr(
        "malak.app.cli.build_conversation_kernel",
        lambda **_: conversation_kernel,
    )

    run_cli(
        service=build_conversation_service(),
        engineering=engineering,
        input_fn=make_input(["/engineering help", "exit"]),
        output_fn=outputs.append,
    )

    rendered = "\n".join(outputs).lower()
    assert "inspect" in rendered
    assert "analyze" in rendered
    assert "propose" in rendered
    assert conversation_kernel.requests == []
    assert all(
        kernel.requests == []
        for kernel in engineering.kernels.values()
    )


def test_run_cli_routes_engineering_commands_to_exact_kernel_and_preserves_subject(
    monkeypatch,
) -> None:
    outputs: list[str] = []
    conversation_kernel = RecordingKernel()
    engineering = EngineeringKernelSetStub()

    monkeypatch.setattr(
        "malak.app.cli.build_conversation_kernel",
        lambda **_: conversation_kernel,
    )

    run_cli(
        service=build_conversation_service(),
        engineering=engineering,
        input_fn=make_input(
            [
                "/EnGiNeErInG InSpEcT   Memory  Layer",
                "/engineering analyze Blueprint",
                "/engineering propose Security",
                "exit",
            ]
        ),
        output_fn=outputs.append,
    )

    assert conversation_kernel.requests == []

    inspect = engineering.kernels["inspect"]
    analyze = engineering.kernels["analyze"]
    propose = engineering.kernels["propose"]

    assert [request.content for request in inspect.requests] == [
        "Memory  Layer"
    ]
    assert [request.content for request in analyze.requests] == [
        "Blueprint"
    ]
    assert [request.content for request in propose.requests] == [
        "Security"
    ]

    rendered = "\n".join(outputs)
    for action in ("inspect", "analyze", "propose"):
        assert f"[engineering/{action}]" in rendered
        assert f"{action}-payload" in rendered


def test_run_cli_invalid_engineering_command_never_falls_back_to_conversation(
    monkeypatch,
) -> None:
    outputs: list[str] = []
    conversation_kernel = RecordingKernel()
    engineering = EngineeringKernelSetStub()

    monkeypatch.setattr(
        "malak.app.cli.build_conversation_kernel",
        lambda **_: conversation_kernel,
    )

    run_cli(
        service=build_conversation_service(),
        engineering=engineering,
        input_fn=make_input(
            [
                "/engineering unknown Memory",
                "/engineering inspect",
                "exit",
            ]
        ),
        output_fn=outputs.append,
    )

    assert conversation_kernel.requests == []
    assert all(
        kernel.requests == []
        for kernel in engineering.kernels.values()
    )
    assert "/engineering help" in "\n".join(outputs)


def test_run_cli_non_command_engineering_text_remains_conversation(
    monkeypatch,
) -> None:
    outputs: list[str] = []
    conversation_kernel = RecordingKernel()
    engineering = EngineeringKernelSetStub()

    monkeypatch.setattr(
        "malak.app.cli.build_conversation_kernel",
        lambda **_: conversation_kernel,
    )

    run_cli(
        service=build_conversation_service(),
        engineering=engineering,
        input_fn=make_input(["engineering inspect Memory", "exit"]),
        output_fn=outputs.append,
    )

    assert [
        request.content for request in conversation_kernel.requests
    ] == ["engineering inspect Memory"]
    assert all(
        kernel.requests == []
        for kernel in engineering.kernels.values()
    )


def test_run_cli_status_reports_engineering_availability_and_baseline() -> None:
    outputs: list[str] = []
    engineering = EngineeringKernelSetStub()

    run_cli(
        engineering=engineering,
        input_fn=make_input(["status", "exit"]),
        output_fn=outputs.append,
    )

    rendered = "\n".join(outputs)
    assert "Engineering: available" in rendered
    assert engineering.baseline_commit in rendered


def test_run_cli_status_reports_engineering_unavailable_without_repository() -> None:
    outputs: list[str] = []

    run_cli(
        input_fn=make_input(["status", "exit"]),
        output_fn=outputs.append,
    )

    assert "Engineering: unavailable" in "\n".join(outputs)


def test_run_cli_engineering_emits_correlated_operational_events() -> None:
    outputs: list[str] = []
    sink = RecordingOperationalEventSink()
    engineering = EngineeringKernelSetStub()

    run_cli(
        engineering=engineering,
        input_fn=make_input(["/engineering inspect Memory", "exit"]),
        output_fn=outputs.append,
        operational_event_sink=sink,
    )

    assert [event.event_name for event in sink.events] == [
        "engineering.inspect.started",
        "engineering.inspect.succeeded",
    ]
    assert sink.events[0].request_id == sink.events[1].request_id
    assert sink.events[0].request_id is not None


def test_run_cli_engineering_started_event_failure_blocks_kernel() -> None:
    outputs: list[str] = []
    sink = FailingOperationalEventSink(
        event_name="engineering.inspect.started",
    )
    engineering = EngineeringKernelSetStub()

    run_cli(
        engineering=engineering,
        input_fn=make_input(["/engineering inspect Memory", "exit"]),
        output_fn=outputs.append,
        operational_event_sink=sink,
    )

    assert engineering.kernels["inspect"].requests == []
    assert sink.attempted_event_names == [
        "engineering.inspect.started",
    ]
    assert (
        "Error controlado de observabilidad: sink no disponible"
        in outputs
    )


def test_run_cli_engineering_final_event_failure_preserves_response() -> None:
    outputs: list[str] = []
    sink = FailingOperationalEventSink(
        event_name="engineering.inspect.succeeded",
    )
    engineering = EngineeringKernelSetStub()

    run_cli(
        engineering=engineering,
        input_fn=make_input(["/engineering inspect Memory", "exit"]),
        output_fn=outputs.append,
        operational_event_sink=sink,
    )

    rendered = "\n".join(outputs)
    assert "inspect-payload" in rendered
    assert sink.attempted_event_names == [
        "engineering.inspect.started",
        "engineering.inspect.succeeded",
    ]
    assert "engineering.inspect.failed" not in sink.attempted_event_names


def test_run_cli_engineering_kernel_failure_emits_failed_event() -> None:
    outputs: list[str] = []
    sink = RecordingOperationalEventSink()
    engineering = EngineeringKernelSetStub()
    engineering.kernels["inspect"] = FailingEngineeringKernel("inspect")

    run_cli(
        engineering=engineering,
        input_fn=make_input(["/engineering inspect Memory", "exit"]),
        output_fn=outputs.append,
        operational_event_sink=sink,
    )

    assert [event.event_name for event in sink.events] == [
        "engineering.inspect.started",
        "engineering.inspect.failed",
    ]
    assert sink.events[0].request_id == sink.events[1].request_id
    assert "Error controlado: fallo engineering" in outputs


class ExplorerValue:
    def __init__(self, **values: object) -> None:
        self.__dict__.update(values)


class ExplorerRepositoryReaderStub:
    def __init__(self, baseline: str) -> None:
        self.baseline_commit = baseline
        self.read_paths: list[str] = []
        self.search_queries: list[str] = []

    def list_tracked_files(self):
        return (
            "README.md",
            "docs/governance/cognitive_constitution.md",
            "src/malak/app/cli.py",
        )

    def read_text(self, path: str):
        self.read_paths.append(path)
        return ExplorerValue(
            baseline_commit=self.baseline_commit,
            path=path,
            blob_sha="a" * 40,
            content="repository document body",
        )

    def search_text(self, query: str):
        self.search_queries.append(query)
        return ExplorerValue(
            baseline_commit=self.baseline_commit,
            matches=(
                ExplorerValue(
                    baseline_commit=self.baseline_commit,
                    path="src/malak/app/cli.py",
                    blob_sha="b" * 40,
                    line_number=42,
                    line="needle in repository",
                ),
            ),
            truncated=True,
        )


class ExplorerKnowledgeReaderStub:
    def __init__(self, baseline: str) -> None:
        self.baseline_commit = baseline
        self.read_paths: list[str] = []
        self.search_queries: list[str] = []

    def list_sources(self):
        return (
            ExplorerValue(
                baseline_commit=self.baseline_commit,
                path="docs/governance/cognitive_constitution.md",
                source_class="GOVERNING",
                authority_class="normative",
            ),
            ExplorerValue(
                baseline_commit=self.baseline_commit,
                path="docs/project/project_context.md",
                source_class="DERIVED_STATE",
                authority_class="derived",
            ),
        )

    def read(self, path: str):
        self.read_paths.append(path)
        return ExplorerValue(
            baseline_commit=self.baseline_commit,
            path=path,
            blob_sha="c" * 40,
            source_class="GOVERNING",
            authority_class="normative",
            content="knowledge document body",
        )

    def search_text(self, query: str):
        self.search_queries.append(query)
        return ExplorerValue(
            baseline_commit=self.baseline_commit,
            matches=(
                ExplorerValue(
                    baseline_commit=self.baseline_commit,
                    path="docs/governance/cognitive_constitution.md",
                    blob_sha="d" * 40,
                    source_class="GOVERNING",
                    authority_class="normative",
                    line_number=7,
                    line="evidence before authority",
                ),
            ),
            truncated=False,
        )


class ExplorerEngineeringKernelSetStub(EngineeringKernelSetStub):
    def __init__(self) -> None:
        super().__init__()
        self.repository_reader = ExplorerRepositoryReaderStub(
            self.baseline_commit
        )
        self.knowledge_reader = ExplorerKnowledgeReaderStub(
            self.baseline_commit
        )


def _run_explorer_command(
    monkeypatch,
    command: str,
) -> tuple[list[str], RecordingKernel, ExplorerEngineeringKernelSetStub]:
    outputs: list[str] = []
    conversation_kernel = RecordingKernel()
    engineering = ExplorerEngineeringKernelSetStub()

    monkeypatch.setattr(
        "malak.app.cli.build_conversation_kernel",
        lambda **_: conversation_kernel,
    )

    run_cli(
        service=build_conversation_service(),
        engineering=engineering,
        input_fn=make_input([command, "exit"]),
        output_fn=outputs.append,
    )

    return outputs, conversation_kernel, engineering


def test_run_cli_explore_help_is_deterministic_and_side_effect_free(
    monkeypatch,
) -> None:
    outputs, conversation_kernel, engineering = _run_explorer_command(
        monkeypatch,
        "/explore help",
    )

    rendered = "\n".join(outputs).lower()
    for command in (
        "/explore repo list",
        "/explore repo read",
        "/explore repo search",
        "/explore knowledge list",
        "/explore knowledge read",
        "/explore knowledge search",
    ):
        assert command in rendered

    assert conversation_kernel.requests == []
    assert all(
        kernel.requests == []
        for kernel in engineering.kernels.values()
    )


def test_run_cli_explore_repo_list_supports_prefix_filter(
    monkeypatch,
) -> None:
    outputs, conversation_kernel, _ = _run_explorer_command(
        monkeypatch,
        "/explore repo list docs/",
    )

    rendered = "\n".join(outputs)
    assert "docs/governance/cognitive_constitution.md" in rendered
    assert "src/malak/app/cli.py" not in rendered
    assert "README.md" not in rendered
    assert conversation_kernel.requests == []


def test_run_cli_explore_repo_read_uses_existing_reader(
    monkeypatch,
) -> None:
    path = "docs/governance/cognitive_constitution.md"
    outputs, conversation_kernel, engineering = _run_explorer_command(
        monkeypatch,
        f"/explore repo read {path}",
    )

    assert engineering.repository_reader.read_paths == [path]
    rendered = "\n".join(outputs)
    assert path in rendered
    assert "repository document body" in rendered
    assert engineering.baseline_commit in rendered
    assert conversation_kernel.requests == []


def test_run_cli_explore_repo_search_preserves_query_and_truncation(
    monkeypatch,
) -> None:
    outputs, conversation_kernel, engineering = _run_explorer_command(
        monkeypatch,
        "/explore repo search Evidence Bound",
    )

    assert engineering.repository_reader.search_queries == [
        "Evidence Bound"
    ]
    rendered = "\n".join(outputs)
    assert "src/malak/app/cli.py" in rendered
    assert "needle in repository" in rendered
    assert "truncated: true" in rendered.lower()
    assert conversation_kernel.requests == []


def test_run_cli_explore_knowledge_list_preserves_authority_metadata(
    monkeypatch,
) -> None:
    outputs, conversation_kernel, _ = _run_explorer_command(
        monkeypatch,
        "/explore knowledge list",
    )

    rendered = "\n".join(outputs)
    assert "GOVERNING" in rendered
    assert "normative" in rendered
    assert "DERIVED_STATE" in rendered
    assert "derived" in rendered
    assert conversation_kernel.requests == []


def test_run_cli_explore_knowledge_read_uses_existing_reader(
    monkeypatch,
) -> None:
    path = "docs/governance/cognitive_constitution.md"
    outputs, conversation_kernel, engineering = _run_explorer_command(
        monkeypatch,
        f"/explore knowledge read {path}",
    )

    assert engineering.knowledge_reader.read_paths == [path]
    rendered = "\n".join(outputs)
    assert path in rendered
    assert "GOVERNING" in rendered
    assert "normative" in rendered
    assert "knowledge document body" in rendered
    assert engineering.baseline_commit in rendered
    assert conversation_kernel.requests == []


def test_run_cli_explore_knowledge_search_preserves_grounded_match(
    monkeypatch,
) -> None:
    outputs, conversation_kernel, engineering = _run_explorer_command(
        monkeypatch,
        "/explore knowledge search evidence before authority",
    )

    assert engineering.knowledge_reader.search_queries == [
        "evidence before authority"
    ]
    rendered = "\n".join(outputs)
    assert "GOVERNING" in rendered
    assert "normative" in rendered
    assert "evidence before authority" in rendered
    assert conversation_kernel.requests == []


def test_run_cli_invalid_explore_command_never_falls_back_to_conversation(
    monkeypatch,
) -> None:
    outputs: list[str] = []
    conversation_kernel = RecordingKernel()
    engineering = ExplorerEngineeringKernelSetStub()

    monkeypatch.setattr(
        "malak.app.cli.build_conversation_kernel",
        lambda **_: conversation_kernel,
    )

    run_cli(
        service=build_conversation_service(),
        engineering=engineering,
        input_fn=make_input(
            [
                "/explore repo unknown",
                "/explore knowledge",
                "exit",
            ]
        ),
        output_fn=outputs.append,
    )

    assert conversation_kernel.requests == []
    assert all(
        kernel.requests == []
        for kernel in engineering.kernels.values()
    )
    assert "/explore help" in "\n".join(outputs)


def test_run_cli_explore_is_unavailable_without_repository_root(
    monkeypatch,
) -> None:
    outputs: list[str] = []
    conversation_kernel = RecordingKernel()

    monkeypatch.setattr(
        "malak.app.cli.build_conversation_kernel",
        lambda **_: conversation_kernel,
    )

    run_cli(
        service=build_conversation_service(),
        engineering=None,
        input_fn=make_input(["/explore repo list", "exit"]),
        output_fn=outputs.append,
    )

    assert "Explorer no disponible" in "\n".join(outputs)
    assert conversation_kernel.requests == []
