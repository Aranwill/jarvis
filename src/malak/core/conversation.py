from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class ConversationRequest:
    prompt: str
    model: str | None = None
    system_prompt: str | None = None


@dataclass(frozen=True)
class ConversationResponse:
    content: str
    model: str | None = None
    provider: str | None = None


class ConversationProvider(ABC):
    @abstractmethod
    def generate(self, request: ConversationRequest) -> ConversationResponse:
        raise NotImplementedError