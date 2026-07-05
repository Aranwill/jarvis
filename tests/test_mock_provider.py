from malak.core.conversation import ConversationRequest
from malak.providers.mock_provider import MockConversationProvider
from malak.runtime.mock_llm_runtime import MockLLMRuntime


def test_mock_provider_returns_response():
    runtime = MockLLMRuntime()
    provider = MockConversationProvider(runtime)

    response = provider.generate(
        ConversationRequest(prompt="Hello")
    )

    assert response.content == "[RUNTIME] Hello"
    assert response.provider == "runtime"
    assert response.model == "mock-runtime"


def test_mock_provider_preserves_model():
    runtime = MockLLMRuntime()
    provider = MockConversationProvider(runtime)

    response = provider.generate(
        ConversationRequest(
            prompt="Hello",
            model="phi4",
        )
    )

    assert response.model == "phi4"