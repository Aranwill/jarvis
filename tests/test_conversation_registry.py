import pytest

from malak.core.conversation_registry import (
    ConversationProviderNotFoundError,
    ConversationProviderRegistry,
)
from malak.providers.runtime_provider import RuntimeConversationProvider
from malak.runtime.mock_llm_runtime import MockLLMRuntime


def build_provider() -> RuntimeConversationProvider:
    return RuntimeConversationProvider(MockLLMRuntime())


def test_register_provider() -> None:
    registry = ConversationProviderRegistry()

    provider = build_provider()
    registry.register("mock", provider)

    assert registry.get("mock") is provider


def test_registry_normalizes_provider_names() -> None:
    registry = ConversationProviderRegistry()

    provider = build_provider()
    registry.register("  Mock  ", provider)

    assert registry.get("MOCK") is provider
    assert registry.list() == ["mock"]


def test_registry_rejects_empty_provider_name() -> None:
    registry = ConversationProviderRegistry()

    with pytest.raises(
        ValueError,
        match="Conversation provider name must not be empty",
    ):
        registry.register("   ", build_provider())


def test_registry_rejects_duplicate_provider() -> None:
    registry = ConversationProviderRegistry()

    registry.register("mock", build_provider())

    with pytest.raises(
        ValueError,
        match="Conversation provider 'mock' is already registered",
    ):
        registry.register(" MOCK ", build_provider())


def test_list_registered_providers_is_sorted() -> None:
    registry = ConversationProviderRegistry()

    registry.register("ollama", build_provider())
    registry.register("mock", build_provider())

    assert registry.list() == ["mock", "ollama"]


def test_unknown_provider_raises_explicit_error() -> None:
    registry = ConversationProviderRegistry()

    with pytest.raises(
        ConversationProviderNotFoundError,
        match="Conversation provider 'unknown' is not registered",
    ):
        registry.get(" UNKNOWN ")


def test_get_rejects_empty_provider_name() -> None:
    registry = ConversationProviderRegistry()

    with pytest.raises(
        ValueError,
        match="Conversation provider name must not be empty",
    ):
        registry.get("   ")
        