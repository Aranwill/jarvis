from malak.app.composition import build_conversation_kernel
from malak.core.conversation_registry import ConversationProviderRegistry
from malak.core.request import Request
from malak.kernel.kernel import Kernel
from malak.providers.runtime_provider import RuntimeConversationProvider
from malak.runtime.mock_llm_runtime import MockLLMRuntime
from malak.services.conversation_service import ConversationService


def build_service() -> ConversationService:
    registry = ConversationProviderRegistry()
    registry.register(
        "mock",
        RuntimeConversationProvider(MockLLMRuntime()),
    )

    return ConversationService(registry)


def test_build_conversation_kernel_returns_kernel():
    kernel = build_conversation_kernel(
        service=build_service(),
        provider_name="mock",
    )

    assert isinstance(kernel, Kernel)


def test_build_conversation_kernel_composes_conversation_path():
    kernel = build_conversation_kernel(
        service=build_service(),
        provider_name="mock",
        model="test-model",
        system_prompt="You are Malak.",
    )

    response = kernel.receive(
        Request(
            content="Hola",
            session_id="composition-test",
        )
    )

    assert response.content == "[RUNTIME] Hola"
    assert response.source == "conversation"
