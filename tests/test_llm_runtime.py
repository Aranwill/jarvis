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


def test_analyze_structured_output_red_s07_mock_runtime_fails_closed_on_schema():
    runtime = MockLLMRuntime()
    request = ConversationRequest(
        prompt="Return structured output.",
        model="mock-model",
    )
    object.__setattr__(
        request,
        "response_json_schema",
        '{"type":"object"}',
    )

    with pytest.raises(
        RuntimeError,
        match="structured output",
    ):
        runtime.generate(request)
