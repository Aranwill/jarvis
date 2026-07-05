from __future__ import annotations

from abc import ABC, abstractmethod

from malak.core.conversation import (
    ConversationRequest,
    ConversationResponse,
)


class LLMRuntime(ABC):
    """
    Abstract runtime capable of executing LLM operations.
    """

    @abstractmethod
    def generate(
        self,
        request: ConversationRequest,
    ) -> ConversationResponse:
        raise NotImplementedError