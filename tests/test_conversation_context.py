import pytest

from malak.core.conversation import ConversationMessage
from malak.services.conversation_context import InMemoryConversationContext


def test_conversation_context_starts_empty():
    context = InMemoryConversationContext()

    assert context.snapshot() == ()


def test_conversation_context_records_complete_exchange():
    context = InMemoryConversationContext()

    context.record_exchange(
        user_content="Hello Malak",
        assistant_content="Hello human",
    )

    assert context.snapshot() == (
        ConversationMessage(
            role="user",
            content="Hello Malak",
        ),
        ConversationMessage(
            role="assistant",
            content="Hello human",
        ),
    )


def test_conversation_context_preserves_exchange_order():
    context = InMemoryConversationContext()

    context.record_exchange(
        user_content="First question",
        assistant_content="First answer",
    )
    context.record_exchange(
        user_content="Second question",
        assistant_content="Second answer",
    )

    assert context.snapshot() == (
        ConversationMessage(role="user", content="First question"),
        ConversationMessage(role="assistant", content="First answer"),
        ConversationMessage(role="user", content="Second question"),
        ConversationMessage(role="assistant", content="Second answer"),
    )


def test_conversation_context_discards_oldest_complete_exchange():
    context = InMemoryConversationContext(max_exchanges=2)

    context.record_exchange(
        user_content="First question",
        assistant_content="First answer",
    )
    context.record_exchange(
        user_content="Second question",
        assistant_content="Second answer",
    )
    context.record_exchange(
        user_content="Third question",
        assistant_content="Third answer",
    )

    assert context.snapshot() == (
        ConversationMessage(role="user", content="Second question"),
        ConversationMessage(role="assistant", content="Second answer"),
        ConversationMessage(role="user", content="Third question"),
        ConversationMessage(role="assistant", content="Third answer"),
    )


def test_conversation_context_can_be_cleared():
    context = InMemoryConversationContext()

    context.record_exchange(
        user_content="Hello",
        assistant_content="Hi",
    )

    context.clear()

    assert context.snapshot() == ()


def test_conversation_context_rejects_non_positive_limit():
    with pytest.raises(ValueError):
        InMemoryConversationContext(max_exchanges=0)