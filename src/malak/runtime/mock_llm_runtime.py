from malak.core.conversation import (
    ConversationRequest,
    ConversationResponse,
)
from malak.core.llm_runtime import LLMRuntime


class MockLLMRuntime(LLMRuntime):
    """
    Runtime used for development and tests.
    """

    def generate(
        self,
        request: ConversationRequest,
    ) -> ConversationResponse:
        return ConversationResponse(
            content=f"[RUNTIME] {request.prompt}",
            model=request.model or "mock-runtime",
            provider="runtime",
        )