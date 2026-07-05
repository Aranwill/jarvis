from malak.core.conversation import (
    ConversationProvider,
    ConversationRequest,
    ConversationResponse,
)
from malak.core.runtime import ConversationRuntime


class MockConversationProvider(ConversationProvider):
    """
    Mock provider used for development and tests.
    """

    def __init__(self, runtime: ConversationRuntime):
        self._runtime = runtime

    def generate(
        self,
        request: ConversationRequest,
    ) -> ConversationResponse:
        return self._runtime.generate(request)