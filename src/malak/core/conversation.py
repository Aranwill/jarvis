from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class ConversationMessage:
    role: str
    content: str


    def __post_init__(self) -> None:
        if self.role not in {"user", "assistant"}:
            raise ValueError("role must be 'user' or 'assistant'")


@dataclass(frozen=True)
class ConversationRequest:
    prompt: str
    model: str | None = None
    system_prompt: str | None = None
    history: tuple[ConversationMessage, ...] = ()


@dataclass(frozen=True)
class ConversationResponse:
    content: str
    model: str | None = None
    provider: str | None = None


class ConversationProvider(ABC):
    @abstractmethod
    def generate(self, request: ConversationRequest) -> ConversationResponse:
        raise NotImplementedError