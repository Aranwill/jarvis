import pytest

from malak.core.conversation_registry import ConversationProviderRegistry
from malak.providers.mock_provider import MockConversationProvider


def test_register_provider():

    registry = ConversationProviderRegistry()

    registry.register(
        "mock",
        MockConversationProvider(),
    )

    assert registry.get("mock") is not None


def test_list_registered_providers():

    registry = ConversationProviderRegistry()

    registry.register(
        "mock",
        MockConversationProvider(),
    )

    assert registry.list() == ["mock"]


def test_unknown_provider_raises_key_error():

    registry = ConversationProviderRegistry()

    with pytest.raises(KeyError):
        registry.get("unknown")