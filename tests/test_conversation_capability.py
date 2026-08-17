from malak.capabilities.conversation import ConversationCapability
from malak.core.conversation import (
    ConversationProvider,
    ConversationRequest,
    ConversationResponse,
)
from malak.core.conversation_registry import ConversationProviderRegistry
from malak.services.conversation_service import ConversationService


class RecordingConversationProvider(ConversationProvider):
    def __init__(self) -> None:
        self.last_request: ConversationRequest | None = None

    def generate(
        self,
        request: ConversationRequest,
    ) -> ConversationResponse:
        self.last_request = request

        return ConversationResponse(
            content=f"reply:{request.prompt}",
            model=request.model,
            provider="recording",
        )


def test_conversation_capability_exposes_stable_name():
    registry = ConversationProviderRegistry()
    registry.register("recording", RecordingConversationProvider())

    capability = ConversationCapability(
        service=ConversationService(registry),
        provider_name="recording",
    )

    assert capability.name == "conversation"


def test_conversation_capability_delegates_to_conversation_service():
    provider = RecordingConversationProvider()

    registry = ConversationProviderRegistry()
    registry.register("recording", provider)

    capability = ConversationCapability(
        service=ConversationService(registry),
        provider_name="recording",
        model="test-model",
        system_prompt="You are Malak.",
    )

    result = capability.execute("Hola")

    assert result == "reply:Hola"

    assert provider.last_request == ConversationRequest(
        prompt="Hola",
        model="test-model",
        system_prompt="You are Malak.",
    )
