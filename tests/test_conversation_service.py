from malak.core.conversation import ConversationRequest
from malak.core.conversation_registry import ConversationProviderRegistry
from malak.providers.mock_provider import MockConversationProvider
from malak.services.conversation_service import ConversationService
from malak.runtime.mock_runtime import MockConversationRuntime

def test_conversation_service_delegates_to_registered_provider():
    registry = ConversationProviderRegistry()
    registry.register("mock", MockConversationProvider(MockConversationRuntime()))

    service = ConversationService(registry)

    response = service.generate(
        ConversationRequest(prompt="Hello"),
        provider="mock",
    )

    assert response.content == "[RUNTIME] Hello"
    assert response.provider == "runtime"


def test_conversation_service_preserves_model():
    registry = ConversationProviderRegistry()
    registry.register("mock", MockConversationProvider(MockConversationRuntime()))

    service = ConversationService(registry)

    response = service.generate(
        ConversationRequest(
            prompt="Hello",
            model="phi4",
        ),
        provider="mock",
    )

    assert response.model == "phi4"