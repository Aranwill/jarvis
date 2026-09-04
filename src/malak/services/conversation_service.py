from dataclasses import replace

from malak.core.conversation import (
    ConversationRequest,
    ConversationResponse,
)
from malak.core.conversation_registry import ConversationProviderRegistry
from malak.services.conversation_context import InMemoryConversationContext


class ConversationService:
    """
    Delegates conversation requests to a registered provider.

    The service resolves the requested provider and returns its response.
    When an in-memory conversation context is provided, the service enriches
    the request with the current history and records only successful exchanges.

    It does not select runtimes, models, retries, logging, metrics,
    persistence, or governance policies.
    """

    def __init__(
        self,
        registry: ConversationProviderRegistry,
        context: InMemoryConversationContext | None = None,
    ) -> None:
        self._registry = registry
        self._context = context

    def generate(
        self,
        request: ConversationRequest,
        provider: str,
    ) -> ConversationResponse:
        conversation_provider = self._registry.get(provider)

        if self._context is None:
            return conversation_provider.generate(request)

        contextual_request = replace(
            request,
            history=self._context.snapshot(),
        )

        response = conversation_provider.generate(contextual_request)

        self._context.record_exchange(
            user_content=request.prompt,
            assistant_content=response.content,
        )

        return response

    def reset_context(self) -> None:
        if self._context is not None:
            self._context.clear()