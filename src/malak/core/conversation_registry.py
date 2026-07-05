from __future__ import annotations

from malak.core.conversation import ConversationProvider


class ConversationProviderRegistry:
    """
    Registry of available conversation providers.
    """

    def __init__(self) -> None:
        self._providers: dict[str, ConversationProvider] = {}

    def register(
        self,
        name: str,
        provider: ConversationProvider,
    ) -> None:
        self._providers[name] = provider

    def get(
        self,
        name: str,
    ) -> ConversationProvider:
        return self._providers[name]

    def list(self) -> list[str]:
        return sorted(self._providers.keys())
        