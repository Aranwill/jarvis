import pytest

from malak.core.conversation import (
    ConversationMessage,
    ConversationProvider,
    ConversationRequest,
    ConversationResponse,
)
from malak.core.conversation_registry import (
    ConversationProviderNotFoundError,
    ConversationProviderRegistry,
)

from malak.providers.runtime_provider import RuntimeConversationProvider
from malak.runtime.mock_llm_runtime import MockLLMRuntime
from malak.services.conversation_service import ConversationService
from malak.services.conversation_context import InMemoryConversationContext

class RecordingConversationProvider(ConversationProvider):
    def __init__(self) -> None:
        self.last_request: ConversationRequest | None = None

    def generate(
        self,
        request: ConversationRequest,
    ) -> ConversationResponse:
        self.last_request = request
        return ConversationResponse(
            content="Second answer",
            provider="recording",
        )


class FailingConversationProvider(ConversationProvider):
    def generate(
        self,
        request: ConversationRequest,
    ) -> ConversationResponse:
        raise RuntimeError("provider failure")


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

def test_conversation_service_without_context_preserves_existing_behavior():
    registry = ConversationProviderRegistry()
    provider = RecordingConversationProvider()
    registry.register("recording", provider)

    service = ConversationService(registry)

    request = ConversationRequest(
        prompt="Current question",
    )

    response = service.generate(
        request,
        provider="recording",
    )

    assert response.content == "Second answer"
    assert provider.last_request is request


def test_conversation_service_passes_history_and_records_successful_exchange():
    registry = ConversationProviderRegistry()
    provider = RecordingConversationProvider()
    registry.register("recording", provider)

    context = InMemoryConversationContext()
    context.record_exchange(
        user_content="First question",
        assistant_content="First answer",
    )

    service = ConversationService(
        registry,
        context=context,
    )

    response = service.generate(
        ConversationRequest(
            prompt="Second question",
            model="test-model",
            system_prompt="You are Malak.",
        ),
        provider="recording",
    )

    assert provider.last_request == ConversationRequest(
        prompt="Second question",
        model="test-model",
        system_prompt="You are Malak.",
        history=(
            ConversationMessage(
                role="user",
                content="First question",
            ),
            ConversationMessage(
                role="assistant",
                content="First answer",
            ),
        ),
    )

    assert response.content == "Second answer"

    assert context.snapshot() == (
        ConversationMessage(
            role="user",
            content="First question",
        ),
        ConversationMessage(
            role="assistant",
            content="First answer",
        ),
        ConversationMessage(
            role="user",
            content="Second question",
        ),
        ConversationMessage(
            role="assistant",
            content="Second answer",
        ),
    )


def test_conversation_service_does_not_mutate_context_when_provider_fails():
    registry = ConversationProviderRegistry()
    registry.register(
        "failing",
        FailingConversationProvider(),
    )

    context = InMemoryConversationContext()
    context.record_exchange(
        user_content="Existing question",
        assistant_content="Existing answer",
    )

    service = ConversationService(
        registry,
        context=context,
    )

    before = context.snapshot()

    with pytest.raises(
        RuntimeError,
        match="provider failure",
    ):
        service.generate(
            ConversationRequest(
                prompt="Failed question",
            ),
            provider="failing",
        )

    assert context.snapshot() == before

def test_conversation_service_can_reset_context():
    registry = ConversationProviderRegistry()
    context = InMemoryConversationContext()

    context.record_exchange(
        user_content="Existing question",
        assistant_content="Existing answer",
    )

    service = ConversationService(
        registry,
        context=context,
    )

    service.reset_context()

    assert context.snapshot() == ()


def test_conversation_service_reset_without_context_is_safe():
    registry = ConversationProviderRegistry()
    service = ConversationService(registry)

    service.reset_context()
