from malak.app.composition import build_conversation_kernel
from malak.core.conversation_registry import ConversationProviderRegistry
from malak.core.request import Request
from malak.providers.runtime_provider import RuntimeConversationProvider
from malak.runtime.mock_llm_runtime import MockLLMRuntime
from malak.services.conversation_service import ConversationService


def build_kernel():
    provider_registry = ConversationProviderRegistry()
    provider_registry.register(
        "mock",
        RuntimeConversationProvider(MockLLMRuntime()),
    )

    service = ConversationService(provider_registry)

    return build_conversation_kernel(
        service=service,
        provider_name="mock",
        model="test-model",
        system_prompt="You are Malak.",
    )


def test_conversation_execution_path_end_to_end():
    kernel = build_kernel()

    response = kernel.receive(
        Request(
            content="Hola Malak",
            session_id="e2e-test",
        )
    )

    assert response.content == "[RUNTIME] Hola Malak"
    assert response.source == "conversation"


def test_conversation_execution_path_preserves_empty_request_guard():
    kernel = build_kernel()

    response = kernel.receive(
        Request(
            content="   ",
            session_id="e2e-empty-test",
        )
    )

    assert response.content == "La solicitud está vacía."
    assert response.source == "kernel"