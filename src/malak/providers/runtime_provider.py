from malak.core.conversation import (
    ConversationProvider,
    ConversationRequest,
    ConversationResponse,
)
from malak.core.llm_runtime import LLMRuntime


class RuntimeConversationProvider(ConversationProvider):
    """
    Adapts conversation requests to an injected LLM runtime.

    The provider preserves the conversation boundary while remaining
    independent from any concrete runtime implementation.
    """

    def __init__(self, runtime: LLMRuntime) -> None:
        self._runtime = runtime

    def generate(
        self,
        request: ConversationRequest,
    ) -> ConversationResponse:
        return self._runtime.generate(request)