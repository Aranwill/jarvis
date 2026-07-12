from malak.core.conversation import ConversationRequest
from malak.core.conversation_registry import ConversationProviderRegistry
from malak.providers.mock_provider import MockConversationProvider
from malak.runtime.mock_llm_runtime import MockLLMRuntime
from malak.services.conversation_service import ConversationService


def test_conversation_flow_through_provider_and_runtime() -> None:
    runtime = MockLLMRuntime()
    provider = MockConversationProvider(runtime)

    registry = ConversationProviderRegistry()
    registry.register("mock", provider)

    service = ConversationService(registry)

    request = ConversationRequest(
        prompt="Hola Malak",
        model="deepseek-coder-v2",
        system_prompt="Responde como runtime de prueba.",
    )

    response = service.generate(
        request=request,
        provider="mock",
    )

    assert response.content == "[RUNTIME] Hola Malak"
    assert response.model == "deepseek-coder-v2"
    assert response.provider == "runtime"
    assert registry.list() == ["mock"]