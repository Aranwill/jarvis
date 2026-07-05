from malak.core.conversation import ConversationRequest
from malak.providers.mock_provider import MockConversationProvider


def test_mock_provider_returns_response():

    provider = MockConversationProvider()

    response = provider.generate(
        ConversationRequest(
            prompt="Hello"
        )
    )

    assert response.content == "[MOCK] Hello"
    assert response.provider == "mock"
    assert response.model == "mock-model"


def test_mock_provider_preserves_model():

    provider = MockConversationProvider()

    response = provider.generate(
        ConversationRequest(
            prompt="Hello",
            model="phi4",
        )
    )

    assert response.model == "phi4"