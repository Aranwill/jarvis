from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Final

from malak.infrastructure.repository_reader import GitRepositoryReader
from malak.knowledge.knowledge_reader import GovernedKnowledgeReader


REQUIRED_SELF_REVIEW_SOURCES: Final[tuple[str, ...]] = (
    "AGENTS.md",
    "SECURITY.md",
    "docs/governance/cognitive_constitution.md",
    "docs/governance/governance_constitution.md",
    "docs/architecture/blueprint.md",
    "docs/architecture/architecture_quality_gates.md",
    "docs/development/malak_construction_protocol.md",
    "docs/development/development_checklist.md",
    "docs/project/implementation_roadmap.md",
    "documents/projects/jarvis/ideas.md",
    "docs/project/concepts/MALAK_RESEARCH_HORIZON_MAP.md",
    "docs/project/concepts/GOVERNED_SELF_REVIEW_BOOTSTRAP_TASK.md",
    "docs/project/status/MALAK-CONSTRUCTION-FLOW-COMPLIANCE-AUDIT-V1-FINAL.md",
)
_ADR_RE = re.compile(r"^docs/architecture/adr/ADR-[0-9]{3}-.+\.md$")


@dataclass(frozen=True, slots=True)
class SelfReviewEvidenceSource:
    path: str
    blob_sha: str
    source_class: str
    authority_class: str


@dataclass(frozen=True, slots=True)
class SelfReviewEvidencePacket:
    baseline_commit: str
    status: str
    required_sources: tuple[SelfReviewEvidenceSource, ...]
    missing_required_sources: tuple[str, ...]
    unreadable_required_sources: tuple[str, ...]
    accepted_adrs: tuple[SelfReviewEvidenceSource, ...]
    concept_paths: tuple[str, ...]
    source_paths: tuple[str, ...]
    test_paths: tuple[str, ...]
    external_validation_refs: tuple[str, ...]
    authority_effect: str = "none"


def build_self_review_evidence_packet(
    *,
    repository_reader: GitRepositoryReader,
    knowledge_reader: GovernedKnowledgeReader,
    external_validation_refs: tuple[str, ...],
) -> SelfReviewEvidencePacket:
    if not isinstance(repository_reader, GitRepositoryReader):
        raise TypeError("repository_reader must be a GitRepositoryReader")
    if not isinstance(knowledge_reader, GovernedKnowledgeReader):
        raise TypeError("knowledge_reader must be a GovernedKnowledgeReader")
    if repository_reader.baseline_commit != knowledge_reader.baseline_commit:
        raise RuntimeError(
            "repository and knowledge readers must share the same baseline"
        )

    validations = _validate_external_refs(external_validation_refs)
    tracked = repository_reader.list_tracked_files()
    tracked_set = set(tracked)
    knowledge_catalog = {
        source.path: source
        for source in knowledge_reader.list_sources()
    }

    required: list[SelfReviewEvidenceSource] = []
    missing: list[str] = []
    unreadable: list[str] = []

    for path in REQUIRED_SELF_REVIEW_SOURCES:
        if path not in tracked_set:
            missing.append(path)
            continue

        source = knowledge_catalog.get(path)
        if source is None:
            unreadable.append(path)
            continue

        try:
            document = knowledge_reader.read(path)
        except (FileNotFoundError, ValueError):
            unreadable.append(path)
            continue

        if document.baseline_commit != repository_reader.baseline_commit:
            raise RuntimeError("required source baseline binding changed")
        if document.path != path:
            raise RuntimeError("required source path binding changed")

        required.append(
            SelfReviewEvidenceSource(
                path=document.path,
                blob_sha=document.blob_sha,
                source_class=document.source_class,
                authority_class=document.authority_class,
            )
        )

    accepted_adrs: list[SelfReviewEvidenceSource] = []
    catalog_inconclusive = False
    for path in sorted(item for item in tracked if _ADR_RE.fullmatch(item)):
        source = knowledge_catalog.get(path)
        if source is None:
            catalog_inconclusive = True
            continue
        try:
            document = knowledge_reader.read(path)
        except (FileNotFoundError, ValueError):
            catalog_inconclusive = True
            continue

        status = _frontmatter_status(document.content)
        if status == "accepted":
            accepted_adrs.append(
                SelfReviewEvidenceSource(
                    path=document.path,
                    blob_sha=document.blob_sha,
                    source_class=document.source_class,
                    authority_class=document.authority_class,
                )
            )

    concept_paths = tuple(
        sorted(
            path
            for path in tracked
            if path.startswith("docs/project/concepts/")
        )
    )
    source_paths = tuple(
        sorted(
            path
            for path in tracked
            if path.startswith("src/malak/")
        )
    )
    test_paths = tuple(
        sorted(
            path
            for path in tracked
            if path.startswith("tests/")
        )
    )

    status = "READY"
    if (
        missing
        or unreadable
        or not validations
        or catalog_inconclusive
    ):
        status = "INCONCLUSIVE"

    return SelfReviewEvidencePacket(
        baseline_commit=repository_reader.baseline_commit,
        status=status,
        required_sources=tuple(required),
        missing_required_sources=tuple(missing),
        unreadable_required_sources=tuple(unreadable),
        accepted_adrs=tuple(accepted_adrs),
        concept_paths=concept_paths,
        source_paths=source_paths,
        test_paths=test_paths,
        external_validation_refs=validations,
        authority_effect="none",
    )


def _validate_external_refs(value: object) -> tuple[str, ...]:
    if not isinstance(value, tuple):
        raise TypeError("external_validation_refs must be a tuple")

    seen: set[str] = set()
    for ref in value:
        if not isinstance(ref, str):
            raise TypeError("external validation refs must be strings")
        if not ref:
            raise ValueError("external validation refs must not be empty")
        if ref != ref.strip():
            raise ValueError(
                "external validation refs must not have surrounding whitespace"
            )
        if any(ord(character) < 32 or ord(character) == 127 for character in ref):
            raise ValueError(
                "external validation refs contain forbidden control characters"
            )
        if ref in seen:
            raise ValueError("external validation refs must be unique")
        seen.add(ref)

    return value


def _frontmatter_status(content: str) -> str | None:
    lines = content.splitlines()
    if not lines or lines[0] != "---":
        return None

    for line in lines[1:]:
        if line == "---":
            return None
        if line.startswith("status:"):
            return line.partition(":")[2].strip()

    return None
