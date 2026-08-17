from malak.capabilities.conversation import ConversationCapability
from malak.kernel.kernel import Kernel
from malak.kernel.registry import CapabilityRegistry
from malak.services.conversation_service import ConversationService
from malak.services.planner import Planner


def build_conversation_kernel(
    service: ConversationService,
    provider_name: str,
    model: str | None = None,
    system_prompt: str | None = None,
) -> Kernel:
    """
    Compose a Kernel configured for the conversation capability.
    """

    capability = ConversationCapability(
        service=service,
        provider_name=provider_name,
        model=model,
        system_prompt=system_prompt,
    )

    registry = CapabilityRegistry()
    registry.register(capability)

    planner = Planner(
        capability_name=capability.name,
    )

    return Kernel(
        planner=planner,
        registry=registry,
    )
