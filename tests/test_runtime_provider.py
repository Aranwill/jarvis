from malak.core.conversation import ConversationRequest
from malak.providers.runtime_provider import RuntimeConversationProvider
from malak.runtime.mock_llm_runtime import MockLLMRuntime


def test_runtime_provider_returns_response():
    runtime = MockLLMRuntime()
    provider = RuntimeConversationProvider(runtime)

    response = provider.generate(
        ConversationRequest(prompt="Hello")
    )

    assert response.content == "[RUNTIME] Hello"
    assert response.provider == "runtime"
    assert response.model == "mock-runtime"


def test_runtime_provider_preserves_model():
    runtime = MockLLMRuntime()
    provider = RuntimeConversationProvider(runtime)

    response = provider.generate(
        ConversationRequest(
            prompt="Hello",
            model="test-model",
        )
    )

    assert response.model == "test-model"