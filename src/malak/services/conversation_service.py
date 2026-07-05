from malak.core.conversation import (
    ConversationRequest,
    ConversationResponse,
)
from malak.core.conversation_registry import ConversationProviderRegistry


class ConversationService:
    """
    Coordinates conversation requests through the provider registry.

    This service isolates the rest of the system from provider-specific
    implementations and acts as the future extension point for logging,
    metrics, retries and provider selection.
    """

    def __init__(self, registry: ConversationProviderRegistry):
        self._registry = registry

    def generate(
        self,
        request: ConversationRequest,
        provider: str,
    ) -> ConversationResponse:
        conversation_provider = self._registry.get(provider)
        return conversation_provider.generate(request)