from malak.core.conversation import (
    ConversationProvider,
    ConversationRequest,
    ConversationResponse,
)
from malak.core.llm_runtime import LLMRuntime


class MockConversationProvider(ConversationProvider):
    """
    Mock provider used for development and tests.
    """

    def __init__(self, runtime: LLMRuntime):
        self._runtime = runtime

    def generate(
        self,
        request: ConversationRequest,
    ) -> ConversationResponse:
        return self._runtime.generate(request)