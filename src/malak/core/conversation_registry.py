from __future__ import annotations

from malak.core.conversation import ConversationProvider


class ConversationProviderNotFoundError(LookupError):
    """
    Raised when a requested conversation provider is not registered.
    """


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
        normalized_name = self._normalize_name(name)

        if normalized_name in self._providers:
            raise ValueError(
                f"Conversation provider '{normalized_name}' "
                "is already registered."
            )

        self._providers[normalized_name] = provider

    def get(
        self,
        name: str,
    ) -> ConversationProvider:
        normalized_name = self._normalize_name(name)

        try:
            return self._providers[normalized_name]
        except KeyError as exc:
            raise ConversationProviderNotFoundError(
                f"Conversation provider '{normalized_name}' "
                "is not registered."
            ) from exc

    def list(self) -> list[str]:
        return sorted(self._providers.keys())

    @staticmethod
    def _normalize_name(name: str) -> str:
        normalized_name = name.strip().lower()

        if not normalized_name:
            raise ValueError(
                "Conversation provider name must not be empty."
            )

        return normalized_name
