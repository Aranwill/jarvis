from __future__ import annotations

import json
import subprocess
from importlib import import_module
from pathlib import Path

import pytest

from malak.capabilities._engineering_evidence import (
    EvidenceSelector,
    GovernedEngineeringEvidenceFocus,
    GovernedEngineeringRelation,
)
from malak.capabilities.engineering_analyze import EngineeringAnalyzeCapability
from malak.core.conversation import (
    ConversationProvider,
    ConversationRequest,
    ConversationResponse,
)
from malak.core.conversation_registry import ConversationProviderRegistry
from malak.core.request import Request
from malak.infrastructure.repository_reader import GitRepositoryReader
from malak.knowledge.knowledge_reader import GovernedKnowledgeReader
from malak.services.conversation_service import ConversationService


RELATION_A = "U01.KERNEL_RESPONSIBILITY"
RELATION_B = "U01.KERNEL_INSTANCE_CARDINALITY"


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _write(repo: Path, relative: str, content: str) -> None:
    path = repo / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Malak Test")
    _git(repo, "config", "commit.gpgsign", "false")
    _write(
        repo,
        "src/malak/kernel/core.py",
        "class Kernel:\n    pass\n",
    )
    _write(
        repo,
        "docs/architecture/kernel.md",
        (
            "Kernel First. Core Kernel owns orchestration.\n"
            "Multiple concrete Kernel instances may preserve one Core Kernel.\n"
        ),
    )
    _git(repo, "add", ".")
    _git(repo, "commit", "--no-gpg-sign", "-m", "baseline")
    return repo


def _relation(index: int) -> GovernedEngineeringRelation:
    if index == 0:
        return GovernedEngineeringRelation(
            relation_id=RELATION_A,
            relation_label="Kernel responsibility",
            evaluation_question=(
                "Does the Core Kernel preserve its governed responsibility?"
            ),
        )
    if index == 1:
        return GovernedEngineeringRelation(
            relation_id=RELATION_B,
            relation_label="Kernel instance cardinality",
            evaluation_question=(
                "Do concrete Kernel instances preserve one architectural Core Kernel?"
            ),
        )
    return GovernedEngineeringRelation(
        relation_id=f"U01.REL_{index + 1:02d}",
        relation_label=f"Governed relation {index + 1}",
        evaluation_question=f"Is governed relation {index + 1} satisfied?",
    )


def _focus(
    *,
    relation_count: int,
) -> GovernedEngineeringEvidenceFocus:
    relations = tuple(_relation(index) for index in range(relation_count))
    return GovernedEngineeringEvidenceFocus(
        focus_id="U01",
        focus_label="U01 Core Kernel",
        subject="Kernel",
        repository_required_selectors=(
            EvidenceSelector(
                "EXACT_PATH",
                "src/malak/kernel/core.py",
                ("Kernel",),
                8,
            ),
        ),
        knowledge_required_selectors=(
            EvidenceSelector(
                "EXACT_PATH",
                "docs/architecture/kernel.md",
                ("Kernel",),
                8,
            ),
        ),
        supplemental_terms=(),
        supplemental_max_matches_per_kind=4,
        max_evidence_line_bytes=1024,
        governed_relations=relations,
    )


def _finding(relation_id: str | None) -> dict[str, object]:
    finding: dict[str, object] = {
        "classification": "ALIGNED",
        "statement": "Observed implementation relates to governed knowledge.",
        "rationale": "Repository and governed knowledge support this finding.",
        "evidence_refs": ["R1", "K1"],
    }
    if relation_id is not None:
        finding["relation_id"] = relation_id
    return finding


def _response(*relation_ids: str | None) -> str:
    return json.dumps(
        {
            "summary": "Governed relations evaluated.",
            "findings": [_finding(relation_id) for relation_id in relation_ids],
            "uncertainties": [],
        }
    )


class _Provider(ConversationProvider):
    def __init__(self, content: str) -> None:
        self.content = content
        self.calls = 0
        self.requests: list[ConversationRequest] = []

    def generate(self, request: ConversationRequest) -> ConversationResponse:
        self.calls += 1
        self.requests.append(request)
        return ConversationResponse(
            content=self.content,
            model=request.model,
            provider="recording",
        )


def _capability(
    tmp_path: Path,
    *,
    relation_count: int,
    response: str,
) -> tuple[_Provider, EngineeringAnalyzeCapability]:
    repo = _repo(tmp_path)
    reader = GitRepositoryReader(repo)
    knowledge = GovernedKnowledgeReader(reader)
    provider = _Provider(response)
    registry = ConversationProviderRegistry()
    registry.register("recording", provider)
    capability = EngineeringAnalyzeCapability(
        repository_reader=reader,
        knowledge_reader=knowledge,
        conversation_service=ConversationService(registry),
        provider_name="recording",
        model="test-model",
        evidence_focus=_focus(relation_count=relation_count),
    )
    return provider, capability


def _execute(capability: EngineeringAnalyzeCapability) -> str:
    return capability.execute(Request(content="Kernel", session_id="s"))


def _rendered_relation_ids(result: str) -> list[str]:
    return [
        line.removeprefix("relation_id=")
        for line in result.splitlines()
        if line.startswith("relation_id=")
    ]


def test_e3_relation_coverage_red_r01_missing_governed_relation_fails_closed(
    tmp_path: Path,
) -> None:
    _provider, capability = _capability(
        tmp_path,
        relation_count=2,
        response=_response(RELATION_A),
    )

    with pytest.raises(RuntimeError):
        _execute(capability)


def test_e3_relation_coverage_red_r02_duplicate_governed_relation_fails_closed(
    tmp_path: Path,
) -> None:
    _provider, capability = _capability(
        tmp_path,
        relation_count=2,
        response=_response(RELATION_A, RELATION_A),
    )

    with pytest.raises(RuntimeError):
        _execute(capability)


def test_e3_relation_coverage_red_r03_complete_coverage_is_accepted(
    tmp_path: Path,
) -> None:
    _provider, capability = _capability(
        tmp_path,
        relation_count=2,
        response=_response(RELATION_A, RELATION_B),
    )

    result = _execute(capability)

    assert _rendered_relation_ids(result) == [RELATION_A, RELATION_B]
    assert "status: GROUNDED" in result
    assert "authority_effect: none" in result


def test_e3_relation_coverage_red_r04_out_of_order_coverage_is_canonicalized(
    tmp_path: Path,
) -> None:
    _provider, capability = _capability(
        tmp_path,
        relation_count=2,
        response=_response(RELATION_B, RELATION_A),
    )

    result = _execute(capability)

    assert _rendered_relation_ids(result) == [RELATION_A, RELATION_B]


def test_e3_relation_coverage_red_r05_catalog_over_capacity_fails_before_model(
    tmp_path: Path,
) -> None:
    provider, capability = _capability(
        tmp_path,
        relation_count=17,
        response=_response(RELATION_A),
    )

    with pytest.raises(RuntimeError):
        _execute(capability)

    assert provider.calls == 0


def test_e3_relation_coverage_red_r06_empty_catalog_preserves_generic_contract(
    tmp_path: Path,
) -> None:
    provider, capability = _capability(
        tmp_path,
        relation_count=0,
        response=_response(None),
    )

    result = _execute(capability)

    assert provider.calls == 1
    assert "relation_id=" not in result
    assert "status: GROUNDED" in result
    assert "authority_effect: none" in result


def test_e3_relation_coverage_red_r07_e4_legacy_analysis_remains_relationless() -> None:
    propose = import_module("malak.capabilities.engineering_propose")

    analysis = propose._parse_analysis(
        _response(None),
        repository_evidence=[{"ref": "R1"}],
        knowledge_evidence=[{"ref": "K1"}],
    )

    assert len(analysis.findings) == 1
    assert analysis.findings[0].relation_id is None
    assert analysis.findings[0].classification == "ALIGNED"
