from __future__ import annotations

import uuid
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from datetime import datetime, timezone
from os import environ

from malak.app.composition import (
    EngineeringKernelSet,
    build_conversation_kernel,
    build_engineering_kernel_set,
)
from malak.core.conversation import (
    ConversationRequest,
    ConversationResponse,
)
from malak.core.conversation_registry import ConversationProviderRegistry
from malak.core.llm_runtime import LLMRuntime
from malak.core.request import Request
from malak.observability.operational_event import OperationalEvent
from malak.observability.operational_event_sink import OperationalEventSink
from malak.providers.runtime_provider import RuntimeConversationProvider
from malak.runtime.mock_llm_runtime import MockLLMRuntime
from malak.runtime.ollama_runtime import OllamaRuntime
from malak.services.conversation_context import InMemoryConversationContext
from malak.services.conversation_service import ConversationService


DEFAULT_PROVIDER = "mock"

HELP_MESSAGE = """
Comandos disponibles:
  help    Muestra esta ayuda.
  status  Muestra el estado básico de la CLI.
  new     Inicia una nueva conversación.
  /engineering help
          Muestra los comandos Engineering disponibles.
  exit    Finaliza la sesión.
""".strip()

ENGINEERING_HELP_MESSAGE = """
Comandos Engineering:
  /engineering inspect <subject>
  /engineering analyze <subject>
  /engineering propose <subject>
""".strip()

_ENGINEERING_ACTIONS = frozenset({"inspect", "analyze", "propose"})


@dataclass(frozen=True, slots=True)
class CLIConfiguration:
    runtime_name: str
    provider_name: str
    runtime_display_name: str
    model: str | None
    ollama_base_url: str
    repository_root: str | None = None


def build_cli_configuration(
    environment: Mapping[str, str],
) -> CLIConfiguration:
    """
    Build validated CLI configuration from an external environment mapping.
    """
    runtime_name = environment.get("MALAK_RUNTIME", "mock").strip().lower()
    ollama_base_url = environment.get(
        "MALAK_OLLAMA_BASE_URL",
        "http://localhost:11434",
    ).strip()

    raw_repository_root = environment.get("MALAK_REPOSITORY_ROOT")
    repository_root = (
        raw_repository_root.strip()
        if raw_repository_root is not None and raw_repository_root.strip()
        else None
    )

    if runtime_name == "mock":
        return CLIConfiguration(
            runtime_name="mock",
            provider_name="mock",
            runtime_display_name="MockLLMRuntime",
            model=None,
            ollama_base_url=ollama_base_url,
            repository_root=repository_root,
        )

    if runtime_name == "ollama":
        model = environment.get("MALAK_OLLAMA_MODEL", "").strip()

        if not model:
            raise ValueError(
                "MALAK_OLLAMA_MODEL is required "
                "when MALAK_RUNTIME=ollama"
            )

        return CLIConfiguration(
            runtime_name="ollama",
            provider_name="ollama",
            runtime_display_name="OllamaRuntime",
            model=model,
            ollama_base_url=ollama_base_url,
            repository_root=repository_root,
        )

    raise ValueError(f"Unsupported runtime: {runtime_name}")


def build_runtime(
    runtime_name: str = DEFAULT_PROVIDER,
    ollama_base_url: str = "http://localhost:11434",
) -> LLMRuntime:
    """
    Build a supported runtime for the CLI application boundary.
    """
    normalized_runtime_name = runtime_name.strip().lower()

    if normalized_runtime_name == "mock":
        return MockLLMRuntime()

    if normalized_runtime_name == "ollama":
        return OllamaRuntime(base_url=ollama_base_url)

    raise ValueError(f"Unsupported runtime: {runtime_name}")


def build_conversation_service(
    runtime: LLMRuntime | None = None,
    provider_name: str = DEFAULT_PROVIDER,
) -> ConversationService:
    """
    Build the minimal conversation service used by the development CLI.
    """
    selected_runtime = runtime if runtime is not None else MockLLMRuntime()
    provider = RuntimeConversationProvider(selected_runtime)

    registry = ConversationProviderRegistry()
    registry.register(provider_name, provider)

    context = InMemoryConversationContext()

    return ConversationService(
        registry,
        context=context,
    )


def _emit_event(
    sink: OperationalEventSink,
    *,
    event_name: str,
    outcome: str,
    request_id: str,
    reason_code: str | None = None,
) -> None:
    sink.append(
        OperationalEvent(
            event_name=event_name,
            component="cli",
            occurred_at=datetime.now(timezone.utc),
            outcome=outcome,
            request_id=request_id,
            reason_code=reason_code,
        )
    )


def _engineering_command(
    prompt: str,
) -> tuple[str, str | None] | None:
    parts = prompt.split(maxsplit=2)

    if not parts or parts[0].lower() != "/engineering":
        return None

    if len(parts) == 1:
        return "", None

    action = parts[1].lower()
    subject = parts[2].strip() if len(parts) == 3 else None
    return action, subject


def _run_engineering(
    *,
    action: str,
    subject: str,
    session_id: str,
    engineering: EngineeringKernelSet,
    output_fn: Callable[[str], None],
    operational_event_sink: OperationalEventSink | None,
) -> None:
    kernel = engineering.kernels[action]
    request_id = str(uuid.uuid4())
    request = Request(
        content=subject,
        session_id=session_id,
        request_id=request_id,
    )
    event_prefix = f"engineering.{action}"

    if operational_event_sink is not None:
        try:
            _emit_event(
                operational_event_sink,
                event_name=f"{event_prefix}.started",
                outcome="started",
                request_id=request_id,
            )
        except Exception as exc:
            output_fn(
                f"Error controlado de observabilidad: {exc}"
            )
            return

    try:
        response = kernel.receive(request)
    except Exception as exc:
        output_fn(f"Error controlado: {exc}")

        if operational_event_sink is not None:
            try:
                _emit_event(
                    operational_event_sink,
                    event_name=f"{event_prefix}.failed",
                    outcome="failed",
                    request_id=request_id,
                    reason_code="runtime_error",
                )
            except Exception as observability_exc:
                output_fn(
                    "Error controlado de observabilidad: "
                    f"{observability_exc}"
                )
        return

    if operational_event_sink is not None:
        try:
            _emit_event(
                operational_event_sink,
                event_name=f"{event_prefix}.succeeded",
                outcome="succeeded",
                request_id=request_id,
            )
        except Exception as exc:
            output_fn(
                f"Error controlado de observabilidad: {exc}"
            )

    output_fn(
        f"Malāk [engineering/{action}]> {response.content}"
    )


def run_cli(
    service: ConversationService | None = None,
    provider_name: str = DEFAULT_PROVIDER,
    runtime_name: str = "MockLLMRuntime",
    model: str | None = None,
    engineering: EngineeringKernelSet | None = None,
    input_fn: Callable[[str], str] = input,
    output_fn: Callable[[str], None] = print,
    operational_event_sink: OperationalEventSink | None = None,
) -> None:
    """
    Run the interactive Malāk command-line interface.
    """
    conversation_service = (
        service
        if service is not None
        else build_conversation_service(provider_name=provider_name)
    )

    kernel = build_conversation_kernel(
        service=conversation_service,
        provider_name=provider_name,
        model=model,
    )

    session_id = str(uuid.uuid4())

    output_fn("Malāk CLI")
    output_fn(f"Runtime activo: {runtime_name}")
    output_fn("Escribe 'help' para ver los comandos disponibles.")

    while True:
        try:
            raw_input = input_fn("Tú> ")
        except (EOFError, KeyboardInterrupt):
            output_fn("")
            output_fn("Sesión finalizada.")
            break

        prompt = raw_input.strip()

        if not prompt:
            output_fn("La entrada no puede estar vacía.")
            continue

        command = prompt.lower()

        if command in {"exit", "quit", "salir"}:
            output_fn("Sesión finalizada.")
            break

        if command in {"help", "ayuda"}:
            output_fn(HELP_MESSAGE)
            continue

        if command == "status":
            output_fn(
                f"Estado: operativo | Provider: {provider_name} | "
                f"Runtime: {runtime_name}"
            )
            if engineering is None:
                output_fn("Engineering: unavailable")
            else:
                output_fn("Engineering: available")
                output_fn(
                    f"Engineering baseline: {engineering.baseline_commit}"
                )
            continue

        if command == "new":
            conversation_service.reset_context(session_id)
            session_id = str(uuid.uuid4())
            output_fn("Nueva conversación iniciada.")
            continue

        engineering_command = _engineering_command(prompt)
        if engineering_command is not None:
            action, subject = engineering_command

            if action == "help" and subject is None:
                output_fn(ENGINEERING_HELP_MESSAGE)
                continue

            if action not in _ENGINEERING_ACTIONS or not subject:
                output_fn(
                    "Comando Engineering inválido. "
                    "Usa /engineering help."
                )
                continue

            if engineering is None:
                output_fn(
                    "Engineering no disponible: configura "
                    "MALAK_REPOSITORY_ROOT."
                )
                continue

            _run_engineering(
                action=action,
                subject=subject,
                session_id=session_id,
                engineering=engineering,
                output_fn=output_fn,
                operational_event_sink=operational_event_sink,
            )
            continue

        request_id = str(uuid.uuid4())
        request = Request(
            content=prompt,
            session_id=session_id,
            request_id=request_id,
        )

        if operational_event_sink is not None:
            try:
                _emit_event(
                    operational_event_sink,
                    event_name="conversation.started",
                    outcome="started",
                    request_id=request_id,
                )
            except Exception as exc:
                output_fn(
                    f"Error controlado de observabilidad: {exc}"
                )
                continue

        try:
            response = kernel.receive(request)
        except Exception as exc:
            output_fn(f"Error controlado: {exc}")

            if operational_event_sink is not None:
                try:
                    _emit_event(
                        operational_event_sink,
                        event_name="conversation.failed",
                        outcome="failed",
                        request_id=request_id,
                        reason_code="runtime_error",
                    )
                except Exception as observability_exc:
                    output_fn(
                        "Error controlado de observabilidad: "
                        f"{observability_exc}"
                    )

            continue

        if operational_event_sink is not None:
            try:
                _emit_event(
                    operational_event_sink,
                    event_name="conversation.succeeded",
                    outcome="succeeded",
                    request_id=request_id,
                )
            except Exception as exc:
                output_fn(
                    f"Error controlado de observabilidad: {exc}"
                )

        output_fn(f"Malāk> {response.content}")


def main() -> None:
    configuration = build_cli_configuration(environ)

    runtime = build_runtime(
        runtime_name=configuration.runtime_name,
        ollama_base_url=configuration.ollama_base_url,
    )

    service = build_conversation_service(
        runtime=runtime,
        provider_name=configuration.provider_name,
    )

    engineering = None
    if configuration.repository_root is not None:
        engineering = build_engineering_kernel_set(
            repository_root=configuration.repository_root,
            service=service,
            provider_name=configuration.provider_name,
            model=configuration.model,
        )

    run_cli(
        service=service,
        provider_name=configuration.provider_name,
        runtime_name=configuration.runtime_display_name,
        model=configuration.model,
        engineering=engineering,
    )


if __name__ == "__main__":
    main()
