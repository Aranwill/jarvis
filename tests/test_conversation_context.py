import pytest

from malak.core.conversation import ConversationMessage
from malak.services.conversation_context import InMemoryConversationContext


def test_conversation_context_starts_empty():
    context = InMemoryConversationContext()

    assert context.snapshot("session-A") == ()


def test_conversation_context_records_complete_exchange():
    context = InMemoryConversationContext()

    context.record_exchange(
        session_id="session-A",
        user_content="Hello Malak",
        assistant_content="Hello human",
    )

    assert context.snapshot("session-A") == (
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
        session_id="session-A",
        user_content="First question",
        assistant_content="First answer",
    )
    context.record_exchange(
        session_id="session-A",
        user_content="Second question",
        assistant_content="Second answer",
    )

    assert context.snapshot("session-A") == (
        ConversationMessage(role="user", content="First question"),
        ConversationMessage(role="assistant", content="First answer"),
        ConversationMessage(role="user", content="Second question"),
        ConversationMessage(role="assistant", content="Second answer"),
    )


def test_conversation_context_discards_oldest_complete_exchange():
    context = InMemoryConversationContext(max_exchanges=2)

    context.record_exchange(
        session_id="session-A",
        user_content="First question",
        assistant_content="First answer",
    )
    context.record_exchange(
        session_id="session-A",
        user_content="Second question",
        assistant_content="Second answer",
    )
    context.record_exchange(
        session_id="session-A",
        user_content="Third question",
        assistant_content="Third answer",
    )

    assert context.snapshot("session-A") == (
        ConversationMessage(role="user", content="Second question"),
        ConversationMessage(role="assistant", content="Second answer"),
        ConversationMessage(role="user", content="Third question"),
        ConversationMessage(role="assistant", content="Third answer"),
    )


def test_conversation_context_can_be_cleared():
    context = InMemoryConversationContext()

    context.record_exchange(
        session_id="session-A",
        user_content="Hello",
        assistant_content="Hi",
    )

    context.clear("session-A")

    assert context.snapshot("session-A") == ()


def test_conversation_context_rejects_non_positive_limit():
    with pytest.raises(ValueError):
        InMemoryConversationContext(max_exchanges=0)


def test_conversation_context_isolates_sessions():
    context = InMemoryConversationContext()

    context.record_exchange(
        session_id="session-A",
        user_content="Question A",
        assistant_content="Answer A",
    )
    context.record_exchange(
        session_id="session-B",
        user_content="Question B",
        assistant_content="Answer B",
    )

    assert context.snapshot("session-A") == (
        ConversationMessage(role="user", content="Question A"),
        ConversationMessage(role="assistant", content="Answer A"),
    )
    assert context.snapshot("session-B") == (
        ConversationMessage(role="user", content="Question B"),
        ConversationMessage(role="assistant", content="Answer B"),
    )


def test_conversation_context_clear_is_session_scoped():
    context = InMemoryConversationContext()

    context.record_exchange(
        session_id="session-A",
        user_content="Question A",
        assistant_content="Answer A",
    )
    context.record_exchange(
        session_id="session-B",
        user_content="Question B",
        assistant_content="Answer B",
    )

    context.clear("session-A")

    assert context.snapshot("session-A") == ()
    assert context.snapshot("session-B") == (
        ConversationMessage(role="user", content="Question B"),
        ConversationMessage(role="assistant", content="Answer B"),
    )


def test_conversation_context_eviction_is_session_scoped():
    context = InMemoryConversationContext(max_exchanges=1)

    context.record_exchange(
        session_id="session-B",
        user_content="Question B",
        assistant_content="Answer B",
    )

    context.record_exchange(
        session_id="session-A",
        user_content="Question A1",
        assistant_content="Answer A1",
    )
    context.record_exchange(
        session_id="session-A",
        user_content="Question A2",
        assistant_content="Answer A2",
    )

    assert context.snapshot("session-A") == (
        ConversationMessage(role="user", content="Question A2"),
        ConversationMessage(role="assistant", content="Answer A2"),
    )
    assert context.snapshot("session-B") == (
        ConversationMessage(role="user", content="Question B"),
        ConversationMessage(role="assistant", content="Answer B"),
    )
