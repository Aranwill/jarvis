import pytest

from malak.core.conversation import ConversationRequest
from malak.core.conversation_registry import (
    ConversationProviderNotFoundError,
    ConversationProviderRegistry,
)
from malak.providers.runtime_provider import RuntimeConversationProvider
from malak.runtime.mock_llm_runtime import MockLLMRuntime
from malak.services.conversation_service import ConversationService


def test_conversation_service_delegates_to_registered_provider():
    registry = ConversationProviderRegistry()
    registry.register(
        "mock",
        RuntimeConversationProvider(
            MockLLMRuntime()
        ),
    )

    service = ConversationService(registry)

    response = service.generate(
        ConversationRequest(prompt="Hello"),
        provider="mock",
    )

    assert response.content == "[RUNTIME] Hello"
    assert response.provider == "runtime"


def test_conversation_service_preserves_model():
    registry = ConversationProviderRegistry()
    registry.register(
        "mock",
        RuntimeConversationProvider(
            MockLLMRuntime()
        ),
    )

    service = ConversationService(registry)

    response = service.generate(
        ConversationRequest(
            prompt="Hello",
            model="test-model",
        ),
        provider="mock",
    )

    assert response.model == "test-model"

def test_conversation_service_propagates_provider_not_found_error() -> None:
    registry = ConversationProviderRegistry()
    service = ConversationService(registry)

    with pytest.raises(
        ConversationProviderNotFoundError,
        match="Conversation provider 'unknown' is not registered",
    ):
        service.generate(
            request=ConversationRequest(prompt="Hello"),
            provider=" UNKNOWN ",
        )
