from malak.core.conversation import (
    ConversationProvider,
    ConversationRequest,
    ConversationResponse,
)


class MockConversationProvider(ConversationProvider):
    """
    Mock provider used for development and tests.
    """

    def generate(
        self,
        request: ConversationRequest,
    ) -> ConversationResponse:

        return ConversationResponse(
            content=f"[MOCK] {request.prompt}",
            model=request.model or "mock-model",
            provider="mock",
        )