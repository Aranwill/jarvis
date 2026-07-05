import pytest

from malak.core.conversation import ConversationRequest
from malak.core.llm_runtime import LLMRuntime
from malak.runtime.mock_llm_runtime import MockLLMRuntime


def test_runtime_contract_can_be_implemented():
    runtime = MockLLMRuntime()

    response = runtime.generate(
        ConversationRequest(prompt="Hello")
    )

    assert response.content == "[RUNTIME] Hello"
    assert response.provider == "runtime"


def test_runtime_preserves_model():
    runtime = MockLLMRuntime()

    response = runtime.generate(
        ConversationRequest(
            prompt="Hello",
            model="phi4",
        )
    )

    assert response.model == "phi4"


def test_runtime_cannot_be_instantiated():
    with pytest.raises(TypeError):
        LLMRuntime()