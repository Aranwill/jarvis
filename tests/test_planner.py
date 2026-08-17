from malak.core.request import Request
from malak.services.planner import Planner


def test_planner_returns_echo_by_default():
    planner = Planner()

    request = Request(
        content="Hola",
        session_id="planner-test",
    )

    capability = planner.resolve(request)

    assert capability == "echo"


def test_planner_can_be_configured_for_conversation():
    planner = Planner(capability_name="conversation")

    request = Request(
        content="Hola",
        session_id="conversation-routing-test",
    )

    capability = planner.resolve(request)

    assert capability == "conversation"
