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
    the request with history isolated by session and records only successful
    exchanges.

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
        session_id: str | None = None,
    ) -> ConversationResponse:
        conversation_provider = self._registry.get(provider)

        if self._context is None:
            return conversation_provider.generate(request)

        if session_id is None:
            raise ValueError(
                "session_id is required when conversation context is enabled"
            )

        contextual_request = replace(
            request,
            history=self._context.snapshot(session_id),
        )

        response = conversation_provider.generate(contextual_request)

        self._context.record_exchange(
            session_id=session_id,
            user_content=request.prompt,
            assistant_content=response.content,
        )

        return response

    def reset_context(
        self,
        session_id: str | None = None,
    ) -> None:
        if self._context is None:
            return

        if session_id is None:
            raise ValueError(
                "session_id is required when conversation context is enabled"
            )

        self._context.clear(session_id)
