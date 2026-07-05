from malak.capabilities.echo import EchoCapability
from malak.kernel.registry import CapabilityRegistry


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

    result = capability.execute("Hola Malāk")

    assert result == "Hola Malāk"