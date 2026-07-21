from malak.core.conversation import (
    ConversationRequest,
    ConversationResponse,
)
from malak.core.conversation_registry import ConversationProviderRegistry


class ConversationService:
    """
    Delegates conversation requests to a registered provider.

    The service resolves the requested provider and returns its response.
    It does not select runtimes, models, retries, logging, metrics,
    persistence, or governance policies.
    """

    def __init__(
        self,
        registry: ConversationProviderRegistry,
    ) -> None:
        self._registry = registry

    def generate(
        self,
        request: ConversationRequest,
        provider: str,
    ) -> ConversationResponse:
        conversation_provider = self._registry.get(provider)
        return conversation_provider.generate(request)