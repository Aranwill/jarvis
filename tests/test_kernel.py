from malak.contracts.capability import Capability
from malak.core.request import Request
from malak.kernel.kernel import Kernel
from malak.kernel.registry import CapabilityRegistry
from malak.services.planner import Planner


class StaticPlanner(Planner):
    def __init__(self, capability_name: str) -> None:
        self._capability_name = capability_name

    def resolve(self, request: Request) -> str:
        return self._capability_name


class CustomCapability(Capability):
    @property
    def name(self) -> str:
        return "custom"

    def execute(self, request):
        return f"custom:{request}"


def test_kernel_returns_response():
    kernel = Kernel()

    request = Request(
        content="Hola Mundo",
        session_id="test-session",
    )

    response = kernel.receive(request)

    assert response.content == "Hola Mundo"
    assert response.source == "echo"


def test_kernel_rejects_empty_request():
    kernel = Kernel()

    request = Request(
        content="",
        session_id="test-session",
    )

    response = kernel.receive(request)

    assert response.content == "La solicitud está vacía."
    assert response.source == "kernel"


def test_kernel_dispatches_echo_capability():
    kernel = Kernel()

    request = Request(
        content="Malāk",
        session_id="dispatch-test",
    )

    response = kernel.receive(request)

    assert response.content == "Malāk"
    assert response.source == "echo"


def test_kernel_accepts_injected_planner_and_registry():
    registry = CapabilityRegistry()
    registry.register(CustomCapability())

    kernel = Kernel(
        planner=StaticPlanner("custom"),
        registry=registry,
    )

    request = Request(
        content="Hola",
        session_id="composition-test",
    )

    response = kernel.receive(request)

    assert response.content == "custom:Hola"
    assert response.source == "custom"