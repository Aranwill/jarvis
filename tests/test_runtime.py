import pytest

from malak.core.conversation import ConversationRequest
from malak.core.runtime import ConversationRuntime
from malak.runtime.mock_runtime import MockConversationRuntime


def test_runtime_contract_can_be_implemented():

    runtime = MockConversationRuntime()

    response = runtime.generate(
        ConversationRequest(prompt="Hello")
    )

    assert response.content == "[RUNTIME] Hello"
    assert response.provider == "runtime"


def test_runtime_preserves_model():

    runtime = MockConversationRuntime()

    response = runtime.generate(
        ConversationRequest(
            prompt="Hello",
            model="phi4",
        )
    )

    assert response.model == "phi4"


def test_runtime_cannot_be_instantiated():

    with pytest.raises(TypeError):
        ConversationRuntime()