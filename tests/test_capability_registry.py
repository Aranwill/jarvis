from malak.capabilities.echo import EchoCapability
from malak.kernel.registry import CapabilityRegistry
from malak.core.request import Request


def test_register_and_get_capability():

    registry = CapabilityRegistry()

    registry.register(EchoCapability())

    capability = registry.get("echo")

    assert capability is not None
    assert capability.name == "echo"


def test_list_capabilities():

    registry = CapabilityRegistry()

    registry.register(EchoCapability())

    assert registry.list() == ["echo"]


def test_execute_echo_capability():

    capability = EchoCapability()

    request = Request(
        content="Hola Malāk",
        session_id="capability-test",
    )

    result = capability.execute(request)

    assert result == "Hola Malāk"