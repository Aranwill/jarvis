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


def test_is_provider_registered_normalizes_name_without_generation() -> None:
    registry = ConversationProviderRegistry()
    provider = RecordingConversationProvider()
    registry.register("mock", provider)
    service = ConversationService(registry)

    assert service.is_provider_registered(" MoCk ") is True
    assert provider.last_request is None


def test_is_provider_registered_returns_false_for_unknown_or_empty() -> None:
    registry = ConversationProviderRegistry()
    provider = RecordingConversationProvider()
    registry.register("mock", provider)
    service = ConversationService(registry)

    assert service.is_provider_registered("unknown") is False
    assert service.is_provider_registered("   ") is False
    assert provider.last_request is None


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


def test_conversation_service_passes_session_history_and_records_exchange():
    registry = ConversationProviderRegistry()
    provider = RecordingConversationProvider()
    registry.register("recording", provider)

    context = InMemoryConversationContext()
    context.record_exchange(
        session_id="session-A",
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
        session_id="session-A",
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

    assert context.snapshot("session-A") == (
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


def test_conversation_service_isolates_session_history():
    registry = ConversationProviderRegistry()
    provider = RecordingConversationProvider()
    registry.register("recording", provider)

    context = InMemoryConversationContext()
    context.record_exchange(
        session_id="session-A",
        user_content="Question A",
        assistant_content="Answer A",
    )

    service = ConversationService(
        registry,
        context=context,
    )

    service.generate(
        ConversationRequest(prompt="Question B"),
        provider="recording",
        session_id="session-B",
    )

    assert provider.last_request == ConversationRequest(
        prompt="Question B",
        history=(),
    )

    assert context.snapshot("session-A") == (
        ConversationMessage(role="user", content="Question A"),
        ConversationMessage(role="assistant", content="Answer A"),
    )


def test_conversation_service_requires_session_id_with_context():
    registry = ConversationProviderRegistry()
    registry.register(
        "recording",
        RecordingConversationProvider(),
    )

    service = ConversationService(
        registry,
        context=InMemoryConversationContext(),
    )

    with pytest.raises(
        ValueError,
        match="session_id is required",
    ):
        service.generate(
            ConversationRequest(prompt="Question"),
            provider="recording",
        )


def test_conversation_service_does_not_mutate_context_when_provider_fails():
    registry = ConversationProviderRegistry()
    registry.register(
        "failing",
        FailingConversationProvider(),
    )

    context = InMemoryConversationContext()
    context.record_exchange(
        session_id="session-A",
        user_content="Existing question",
        assistant_content="Existing answer",
    )

    service = ConversationService(
        registry,
        context=context,
    )

    before = context.snapshot("session-A")

    with pytest.raises(
        RuntimeError,
        match="provider failure",
    ):
        service.generate(
            ConversationRequest(
                prompt="Failed question",
            ),
            provider="failing",
            session_id="session-A",
        )

    assert context.snapshot("session-A") == before


def test_conversation_service_reset_is_session_scoped():
    registry = ConversationProviderRegistry()
    context = InMemoryConversationContext()

    context.record_exchange(
        session_id="session-A",
        user_content="Question A",
        assistant_content="Answer A",
    )
    context.record_exchange(
        session_id="session-B",
        user_content="Question B",
        assistant_content="Answer B",
    )

    service = ConversationService(
        registry,
        context=context,
    )

    service.reset_context("session-A")

    assert context.snapshot("session-A") == ()
    assert context.snapshot("session-B") == (
        ConversationMessage(role="user", content="Question B"),
        ConversationMessage(role="assistant", content="Answer B"),
    )


def test_conversation_service_reset_requires_session_id_with_context():
    registry = ConversationProviderRegistry()
    service = ConversationService(
        registry,
        context=InMemoryConversationContext(),
    )

    with pytest.raises(
        ValueError,
        match="session_id is required",
    ):
        service.reset_context()


def test_conversation_service_reset_without_context_is_safe():
    registry = ConversationProviderRegistry()
    service = ConversationService(registry)

    service.reset_context()




def test_retained_exchange_count_is_bounded_isolated_and_read_only() -> None:
    context = InMemoryConversationContext(max_exchanges=2)
    service = ConversationService(ConversationProviderRegistry(), context)

    for index in range(3):
        context.record_exchange("session-A", f"Pregunta {index}", "Respuesta")
    context.record_exchange("session-B", "Pregunta secreta", "Respuesta")

    before_a = context.snapshot("session-A")
    before_b = context.snapshot("session-B")
    assert service.retained_exchange_count("session-A") == 2
    assert service.retained_exchange_count("session-B") == 1
    assert service.retained_exchange_count("no-existe") == 0
    assert context.snapshot("session-A") == before_a
    assert context.snapshot("session-B") == before_b

    service.reset_context("session-A")
    assert service.retained_exchange_count("session-A") == 0
    assert service.retained_exchange_count("session-B") == 1


def test_retained_exchange_count_requires_session_with_context() -> None:
    service = ConversationService(
        ConversationProviderRegistry(),
        context=InMemoryConversationContext(),
    )

    with pytest.raises(ValueError, match="session_id is required"):
        service.retained_exchange_count()


def test_retained_exchange_count_without_context_is_zero() -> None:
    service = ConversationService(ConversationProviderRegistry())

    assert service.retained_exchange_count() == 0


def test_analyze_structured_output_green_g04_context_replace_preserves_schema():
    registry = ConversationProviderRegistry()
    provider = RecordingConversationProvider()
    registry.register("recording", provider)

    context = InMemoryConversationContext()
    context.record_exchange(
        session_id="session-A",
        user_content="First question",
        assistant_content="First answer",
    )

    service = ConversationService(
        registry,
        context=context,
    )
    schema = '{"type":"object"}'

    request = ConversationRequest(
        prompt="Second question",
        model="test-model",
        response_json_schema=schema,
    )

    service.generate(
        request,
        provider="recording",
        session_id="session-A",
    )

    assert provider.last_request is not None
    assert provider.last_request.response_json_schema == schema
    assert provider.last_request.history == (
        ConversationMessage(
            role="user",
            content="First question",
        ),
        ConversationMessage(
            role="assistant",
            content="First answer",
        ),
    )
