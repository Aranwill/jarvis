from malak.core.conversation import (
    ConversationProvider,
    ConversationRequest,
    ConversationResponse,
)


class ConversationService:
    """
    Coordinates conversation requests through the configured provider.

    This service isolates the rest of the system from provider-specific
    implementations and acts as the future extension point for logging,
    metrics, retries and provider selection.
    """

    def __init__(self, provider: ConversationProvider):
        self._provider = provider

    def generate(
        self,
        request: ConversationRequest,
    ) -> ConversationResponse:
        return self._provider.generate(request)