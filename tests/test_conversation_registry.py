import pytest

from malak.core.conversation_registry import ConversationProviderRegistry
from malak.providers.mock_provider import MockConversationProvider
from malak.runtime.mock_runtime import MockConversationRuntime


def test_register_provider():

    registry = ConversationProviderRegistry()

    registry.register(
        "mock",
        MockConversationProvider(
        MockConversationRuntime()
    )
    )

    assert registry.get("mock") is not None


def test_list_registered_providers():

    registry = ConversationProviderRegistry()

    registry.register(
        "mock",
        MockConversationProvider(
        MockConversationRuntime()
    )
    )

    assert registry.list() == ["mock"]


def test_unknown_provider_raises_key_error():

    registry = ConversationProviderRegistry()

    with pytest.raises(KeyError):
        registry.get("unknown")