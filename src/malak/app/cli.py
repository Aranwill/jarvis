from __future__ import annotations

from collections.abc import Callable

from malak.core.conversation import ConversationRequest
from malak.core.conversation_registry import ConversationProviderRegistry
from malak.providers.mock_provider import MockConversationProvider
from malak.runtime.mock_llm_runtime import MockLLMRuntime
from malak.services.conversation_service import ConversationService


DEFAULT_PROVIDER = "mock"

HELP_MESSAGE = """
Comandos disponibles:
  help    Muestra esta ayuda.
  status  Muestra el estado básico de la CLI.
  exit    Finaliza la sesión.
""".strip()


def build_conversation_service() -> ConversationService:
    """
    Build the minimal conversation service used by the development CLI.
    """
    runtime = MockLLMRuntime()
    provider = MockConversationProvider(runtime)

    registry = ConversationProviderRegistry()
    registry.register(DEFAULT_PROVIDER, provider)

    return ConversationService(registry)


def run_cli(
    service: ConversationService | None = None,
    input_fn: Callable[[str], str] = input,
    output_fn: Callable[[str], None] = print,
) -> None:
    """
    Run the minimal interactive Malāk command-line interface.
    """
    conversation_service = service or build_conversation_service()

    output_fn("Malāk CLI")
    output_fn("Runtime activo: MockLLMRuntime")
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
                "Estado: operativo | Provider: mock | "
                "Runtime: MockLLMRuntime"
            )
            continue

        try:
            request = ConversationRequest(prompt=prompt)

            response = conversation_service.generate(
                request=request,
                provider=DEFAULT_PROVIDER,
            )
        except Exception as exc:
            output_fn(f"Error controlado: {exc}")
            continue

        output_fn(f"Malāk> {response.content}")


def main() -> None:
    run_cli()


if __name__ == "__main__":
    main()