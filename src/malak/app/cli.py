from __future__ import annotations
from collections.abc import Callable
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from os import environ

from malak.core.conversation import ConversationRequest
from malak.core.conversation_registry import ConversationProviderRegistry
from malak.core.llm_runtime import LLMRuntime
from malak.providers.mock_provider import MockConversationProvider
from malak.runtime.mock_llm_runtime import MockLLMRuntime
from malak.runtime.ollama_runtime import OllamaRuntime
from malak.services.conversation_service import ConversationService


DEFAULT_PROVIDER = "mock"

HELP_MESSAGE = """
Comandos disponibles:
  help    Muestra esta ayuda.
  status  Muestra el estado básico de la CLI.
  exit    Finaliza la sesión.
""".strip()

@dataclass(frozen=True, slots=True)
class CLIConfiguration:
    runtime_name: str
    provider_name: str
    runtime_display_name: str
    model: str | None
    ollama_base_url: str

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

    if runtime_name == "mock":
        return CLIConfiguration(
            runtime_name="mock",
            provider_name="mock",
            runtime_display_name="MockLLMRuntime",
            model=None,
            ollama_base_url=ollama_base_url,
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
    provider = MockConversationProvider(selected_runtime)

    registry = ConversationProviderRegistry()
    registry.register(provider_name, provider)

    return ConversationService(registry)


def run_cli(
    service: ConversationService | None = None,
    provider_name: str = DEFAULT_PROVIDER,
    runtime_name: str = "MockLLMRuntime",
    model: str | None = None,
    input_fn: Callable[[str], str] = input,
    output_fn: Callable[[str], None] = print,
) -> None:
    """
    Run the minimal interactive Malāk command-line interface.
    """
    conversation_service = (
        service
        if service is not None
        else build_conversation_service(provider_name=provider_name)
    )

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
            continue

        try:
            request = ConversationRequest(
                prompt=prompt,
                model=model,
            )

            response = conversation_service.generate(
                request=request,
                provider=provider_name,
            )
        except Exception as exc:
            output_fn(f"Error controlado: {exc}")
            continue

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

    run_cli(
        service=service,
        provider_name=configuration.provider_name,
        runtime_name=configuration.runtime_display_name,
        model=configuration.model,
    )

if __name__ == "__main__":
    main()