from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from malak.capabilities.conversation import ConversationCapability
from malak.capabilities.engineering_analyze import EngineeringAnalyzeCapability
from malak.capabilities.engineering_inspect import EngineeringInspectCapability
from malak.capabilities.engineering_propose import EngineeringProposeCapability
from malak.infrastructure.repository_reader import GitRepositoryReader
from malak.kernel.kernel import Kernel
from malak.kernel.registry import CapabilityRegistry
from malak.knowledge.knowledge_reader import GovernedKnowledgeReader
from malak.services.conversation_service import ConversationService
from malak.services.planner import Planner


@dataclass(frozen=True, slots=True)
class EngineeringKernelSet:
    baseline_commit: str
    kernels: dict[str, Kernel]
    repository_reader: GitRepositoryReader
    knowledge_reader: GovernedKnowledgeReader


def _build_fixed_kernel(capability) -> Kernel:
    registry = CapabilityRegistry()
    registry.register(capability)

    planner = Planner(
        capability_name=capability.name,
    )

    return Kernel(
        planner=planner,
        registry=registry,
    )


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

    return _build_fixed_kernel(capability)


def build_engineering_kernel_set(
    *,
    repository_root: str | Path,
    service: ConversationService,
    provider_name: str,
    model: str | None = None,
) -> EngineeringKernelSet:
    """
    Compose E2/E3/E4 over one exact repository snapshot.

    The repository reader is created once and shared by every Engineering
    capability. This keeps inspect, analyze and propose bound to the same
    captured Git baseline for the lifetime of the composed set.
    """

    repository_reader = GitRepositoryReader(repository_root)
    knowledge_reader = GovernedKnowledgeReader(repository_reader)

    capabilities = {
        "inspect": EngineeringInspectCapability(
            repository_reader=repository_reader,
            knowledge_reader=knowledge_reader,
            conversation_service=service,
            provider_name=provider_name,
            model=model,
        ),
        "analyze": EngineeringAnalyzeCapability(
            repository_reader=repository_reader,
            knowledge_reader=knowledge_reader,
            conversation_service=service,
            provider_name=provider_name,
            model=model,
        ),
        "propose": EngineeringProposeCapability(
            repository_reader=repository_reader,
            knowledge_reader=knowledge_reader,
            conversation_service=service,
            provider_name=provider_name,
            model=model,
        ),
    }

    return EngineeringKernelSet(
        baseline_commit=repository_reader.baseline_commit,
        kernels={
            action: _build_fixed_kernel(capability)
            for action, capability in capabilities.items()
        },
        repository_reader=repository_reader,
        knowledge_reader=knowledge_reader,
    )
