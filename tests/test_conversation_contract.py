import pytest

from malak.core.conversation import (
    ConversationMessage,
    ConversationProvider,
    ConversationRequest,
    ConversationResponse,
)


class FakeConversationProvider(ConversationProvider):
    def generate(self, request: ConversationRequest) -> ConversationResponse:
        return ConversationResponse(
            content=f"echo: {request.prompt}",
            model=request.model,
            provider="fake",
        )


def test_conversation_request_can_be_created():
    request = ConversationRequest(
        prompt="Hello Malak",
        model="test-model",
        system_prompt="You are Malak.",
    )

    assert request.prompt == "Hello Malak"
    assert request.model == "test-model"
    assert request.system_prompt == "You are Malak."

def test_conversation_message_can_be_created():
    message = ConversationMessage(
        role="user",
        content="Hello Malak",
    )

    assert message.role == "user"
    assert message.content == "Hello Malak"

def test_conversation_message_rejects_system_role():
    with pytest.raises(
        ValueError,
        match="role",
    ):
        ConversationMessage(
            role="system",
            content="You are Malak.",
        )

def test_conversation_request_defaults_to_empty_history():
    request = ConversationRequest(
        prompt="Hello Malak",
    )

    assert request.history == ()


def test_conversation_request_can_receive_history():
    history = (
        ConversationMessage(
            role="user",
            content="My name is Aranwill.",
        ),
        ConversationMessage(
            role="assistant",
            content="Understood.",
        ),
    )

    request = ConversationRequest(
        prompt="What is my name?",
        history=history,
    )

    assert request.history == history

def test_conversation_response_can_be_created():
    response = ConversationResponse(
        content="Hello human",
        model="test-model",
        provider="fake",
    )

    assert response.content == "Hello human"
    assert response.model == "test-model"
    assert response.provider == "fake"


def test_conversation_provider_contract_can_be_implemented():
    provider = FakeConversationProvider()

    response = provider.generate(
        ConversationRequest(prompt="ping", model="fake-model")
    )

    assert response.content == "echo: ping"
    assert response.model == "fake-model"
    assert response.provider == "fake"


def test_conversation_provider_cannot_be_instantiated_directly():
    with pytest.raises(TypeError):
        ConversationProvider()


def test_analyze_structured_output_red_s01_conversation_request_accepts_schema_contract():
    schema = '{"additionalProperties":false,"type":"object"}'

    request = ConversationRequest(
        prompt="Return structured output.",
        response_json_schema=schema,
    )

    assert request.response_json_schema == schema



def test_analyze_structured_output_green_g01_schema_is_canonicalized():
    request = ConversationRequest(
        prompt="Return structured output.",
        response_json_schema='{ "type": "object", "additionalProperties": false }',
    )

    assert request.response_json_schema == (
        '{"additionalProperties":false,"type":"object"}'
    )


@pytest.mark.parametrize(
    "schema",
    [
        "",
        "   ",
        "{not-json",
        "[]",
        '{"x":NaN}',
        '{"x":1,"x":2}',
    ],
)
def test_analyze_structured_output_green_g02_invalid_schema_fails_closed(
    schema: str,
) -> None:
    with pytest.raises(ValueError):
        ConversationRequest(
            prompt="Return structured output.",
            response_json_schema=schema,
        )


def test_analyze_structured_output_green_g03_schema_is_byte_bounded():
    schema = '{"value":"' + ("x" * (70 * 1024)) + '"}'

    with pytest.raises(
        ValueError,
        match="byte limit",
    ):
        ConversationRequest(
            prompt="Return structured output.",
            response_json_schema=schema,
        )
