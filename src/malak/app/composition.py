from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from malak.capabilities.conversation import ConversationCapability
from malak.capabilities._engineering_evidence import GovernedEngineeringEvidenceFocus
from malak.capabilities.engineering_analyze import EngineeringAnalyzeCapability
from malak.capabilities.engineering_inspect import EngineeringInspectCapability
from malak.capabilities.engineering_propose import EngineeringProposeCapability
from malak.infrastructure.repository_reader import GitRepositoryReader
from malak.infrastructure.repository_structure import RepositoryStructuralProjector
from malak.kernel.kernel import Kernel
from malak.kernel.registry import CapabilityRegistry
from malak.knowledge.knowledge_reader import GovernedKnowledgeReader
from malak.runtime.runtime_generation_contract import RuntimeGenerationContract
from malak.services.conversation_service import ConversationService
from malak.services.planner import Planner


@dataclass(frozen=True, slots=True)
class EngineeringKernelSet:
    baseline_commit: str
    kernels: dict[str, Kernel]
    repository_reader: GitRepositoryReader
    knowledge_reader: GovernedKnowledgeReader
    generation_contract: RuntimeGenerationContract | None
    _service: ConversationService
    _provider_name: str
    _model: str | None

    def with_evidence_focus(
        self,
        focus: GovernedEngineeringEvidenceFocus,
    ) -> "EngineeringKernelSet":
        if not isinstance(focus, GovernedEngineeringEvidenceFocus):
            raise TypeError("focus must be a GovernedEngineeringEvidenceFocus")

        capabilities = {
            "inspect": EngineeringInspectCapability(
                repository_reader=self.repository_reader,
                knowledge_reader=self.knowledge_reader,
                structural_projection=None,
                conversation_service=self._service,
                provider_name=self._provider_name,
                model=self._model,
                generation_contract=self.generation_contract,
                evidence_focus=focus,
            ),
            "analyze": EngineeringAnalyzeCapability(
                repository_reader=self.repository_reader,
                knowledge_reader=self.knowledge_reader,
                conversation_service=self._service,
                provider_name=self._provider_name,
                model=self._model,
                generation_contract=self.generation_contract,
                evidence_focus=focus,
            ),
            "propose": EngineeringProposeCapability(
                repository_reader=self.repository_reader,
                knowledge_reader=self.knowledge_reader,
                conversation_service=self._service,
                provider_name=self._provider_name,
                model=self._model,
                generation_contract=self.generation_contract,
                evidence_focus=focus,
            ),
        }
        return EngineeringKernelSet(
            baseline_commit=self.baseline_commit,
            kernels={
                action: _build_fixed_kernel(capability)
                for action, capability in capabilities.items()
            },
            repository_reader=self.repository_reader,
            knowledge_reader=self.knowledge_reader,
            generation_contract=self.generation_contract,
            _service=self._service,
            _provider_name=self._provider_name,
            _model=self._model,
        )


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
    generation_contract: RuntimeGenerationContract | None = None,
) -> EngineeringKernelSet:
    """
    Compose E2/E3/E4 over one exact repository snapshot.

    The repository reader is created once and shared by every Engineering
    capability. This keeps inspect, analyze and propose bound to the same
    captured Git baseline for the lifetime of the composed set.
    """

    repository_reader = GitRepositoryReader(repository_root)
    knowledge_reader = GovernedKnowledgeReader(repository_reader)
    structural_projection = RepositoryStructuralProjector(repository_reader).project()

    capabilities = {
        "inspect": EngineeringInspectCapability(
            repository_reader=repository_reader,
            knowledge_reader=knowledge_reader,
            structural_projection=structural_projection,
            conversation_service=service,
            provider_name=provider_name,
            model=model,
            generation_contract=generation_contract,
        ),
        "analyze": EngineeringAnalyzeCapability(
            repository_reader=repository_reader,
            knowledge_reader=knowledge_reader,
            conversation_service=service,
            provider_name=provider_name,
            model=model,
            generation_contract=generation_contract,
        ),
        "propose": EngineeringProposeCapability(
            repository_reader=repository_reader,
            knowledge_reader=knowledge_reader,
            conversation_service=service,
            provider_name=provider_name,
            model=model,
            generation_contract=generation_contract,
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
        generation_contract=generation_contract,
        _service=service,
        _provider_name=provider_name,
        _model=model,
    )
