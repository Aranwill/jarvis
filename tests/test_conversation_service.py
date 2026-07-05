from malak.core.conversation import ConversationRequest
from malak.providers.mock_provider import MockConversationProvider
from malak.services.conversation_service import ConversationService


def test_conversation_service_delegates_to_provider():

    provider = MockConversationProvider()

    service = ConversationService(provider)

    response = service.generate(
        ConversationRequest(prompt="Hello")
    )

    assert response.content == "[MOCK] Hello"
    assert response.provider == "mock"


def test_conversation_service_preserves_model():

    provider = MockConversationProvider()

    service = ConversationService(provider)

    response = service.generate(
        ConversationRequest(
            prompt="Hello",
            model="phi4",
        )
    )

    assert response.model == "phi4"