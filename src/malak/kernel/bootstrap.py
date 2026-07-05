from malak.capabilities.echo import EchoCapability
from malak.kernel.registry import CapabilityRegistry


def create_registry() -> CapabilityRegistry:
    """
    Creates the default Capability Registry.
    """

    registry = CapabilityRegistry()

    registry.register(EchoCapability())

    return registry