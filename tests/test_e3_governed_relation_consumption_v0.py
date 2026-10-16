from __future__ import annotations

import json
import subprocess
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


RELATION_ID = "U01.KERNEL_RESPONSIBILITY"


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
    _write(repo, "src/malak/kernel/core.py", "class Kernel: pass\n")
    _write(
        repo,
        "docs/architecture/kernel.md",
        "Kernel First. Core Kernel owns orchestration.\n",
    )
    _git(repo, "add", ".")
    _git(repo, "commit", "--no-gpg-sign", "-m", "baseline")
    return repo


def _focus(*, relation_id: str = RELATION_ID) -> GovernedEngineeringEvidenceFocus:
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
        governed_relations=(
            GovernedEngineeringRelation(
                relation_id=relation_id,
                relation_label="Kernel responsibility",
                evaluation_question="Does the Core Kernel preserve its governed responsibility?",
            ),
        ),
    )


def _response(*, relation_id: str = RELATION_ID) -> str:
    return json.dumps(
        {
            "schema_id": "malak.e3.ref-role-map.v1",
            "summary": "Governed relation evaluated.",
            "findings": [
                {
                    "relation_id": relation_id,
                    "classification": "ALIGNED",
                    "statement": "Observed implementation relates to governed knowledge.",
                    "rationale": "Repository and governed knowledge support the finding.",
                    "evidence_roles": {"R1": "SUPPORT", "K1": "SUPPORT"},
                    "uncertainty_basis": "NONE",
                }
            ],
            "uncertainties": [],
        }
    )


class _Provider(ConversationProvider):
    def __init__(self, content: str) -> None:
        self.content = content
        self.requests: list[ConversationRequest] = []

    def generate(self, request: ConversationRequest) -> ConversationResponse:
        self.requests.append(request)
        return ConversationResponse(
            content=self.content,
            model=request.model,
            provider="recording",
        )


def _capability(
    tmp_path: Path,
    *,
    response_relation_id: str = RELATION_ID,
) -> tuple[_Provider, EngineeringAnalyzeCapability]:
    repo = _repo(tmp_path)
    reader = GitRepositoryReader(repo)
    knowledge = GovernedKnowledgeReader(reader)
    provider = _Provider(_response(relation_id=response_relation_id))
    registry = ConversationProviderRegistry()
    registry.register("recording", provider)
    capability = EngineeringAnalyzeCapability(
        repository_reader=reader,
        knowledge_reader=knowledge,
        conversation_service=ConversationService(registry),
        provider_name="recording",
        model="test-model",
        evidence_focus=_focus(),
    )
    return provider, capability


def test_e3_relation_red_r01_focused_packet_exposes_exact_governed_catalog(
    tmp_path: Path,
) -> None:
    provider, capability = _capability(tmp_path)

    try:
        capability.execute(Request(content="Kernel", session_id="s"))
    except RuntimeError:
        pass

    packet = json.loads(provider.requests[-1].prompt)
    assert packet["focus"]["governed_relations"] == [
        {
            "relation_id": RELATION_ID,
            "relation_label": "Kernel responsibility",
            "evaluation_question": (
                "Does the Core Kernel preserve its governed responsibility?"
            ),
        }
    ]


def test_e3_relation_red_r02_focused_schema_requires_catalog_relation_id(
    tmp_path: Path,
) -> None:
    provider, capability = _capability(tmp_path)

    try:
        capability.execute(Request(content="Kernel", session_id="s"))
    except RuntimeError:
        pass

    schema = json.loads(provider.requests[-1].response_json_schema)
    finding = schema["properties"]["findings"]["items"]
    assert "relation_id" in finding["required"]
    assert finding["properties"]["relation_id"] == {
        "type": "string",
        "enum": [RELATION_ID],
    }


def test_e3_relation_red_r03_catalog_relation_is_accepted_and_rendered(
    tmp_path: Path,
) -> None:
    _provider, capability = _capability(tmp_path)

    result = capability.execute(Request(content="Kernel", session_id="s"))

    assert f"relation_id={RELATION_ID}" in result
    assert "authority_effect: none" in result


def test_e3_relation_red_r04_unknown_relation_fails_closed(
    tmp_path: Path,
) -> None:
    _provider, capability = _capability(
        tmp_path,
        response_relation_id="U01.UNKNOWN_RELATION",
    )

    with pytest.raises(RuntimeError):
        capability.execute(Request(content="Kernel", session_id="s"))
