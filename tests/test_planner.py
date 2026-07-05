from malak.core.request import Request
from malak.services.planner import Planner


def test_planner_returns_echo():

    planner = Planner()

    request = Request(
        content="Hola",
        session_id="planner-test",
    )

    capability = planner.resolve(request)

    assert capability == "echo"