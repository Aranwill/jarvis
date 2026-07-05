from __future__ import annotations

from abc import ABC, abstractmethod

from malak.core.conversation import (
    ConversationRequest,
    ConversationResponse,
)


class ConversationRuntime(ABC):
    """
    Abstract runtime capable of executing conversation requests.

    Concrete implementations encapsulate the communication with
    inference backends such as Ollama, OpenAI, LM Studio, vLLM,
    llama.cpp or any future runtime.
    """

    @abstractmethod
    def generate(
        self,
        request: ConversationRequest,
    ) -> ConversationResponse:
        raise NotImplementedError