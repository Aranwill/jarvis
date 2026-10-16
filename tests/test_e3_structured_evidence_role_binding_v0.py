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
    _write(
        repo,
        "src/malak/kernel/core.py",
        "class Kernel:\n    pass\n",
    )
    _write(
        repo,
        "docs/architecture/kernel.md",
        "Kernel First. Core Kernel owns orchestration.\n",
    )
    _git(repo, "add", ".")
    _git(repo, "commit", "--no-gpg-sign", "-m", "baseline")
    return repo


def _focus() -> GovernedEngineeringEvidenceFocus:
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
                relation_id=RELATION_ID,
                relation_label="Kernel responsibility",
                evaluation_question=(
                    "Does the Core Kernel preserve its governed responsibility?"
                ),
            ),
        ),
    )


def _role_finding(
    *,
    classification: str = "ALIGNED",
    supporting_repository_refs: list[str] | None = None,
    supporting_knowledge_refs: list[str] | None = None,
    limiting_or_counterevidence_refs: list[str] | None = None,
    uncertainty_basis: str = "NONE",
) -> dict[str, object]:
    return {
        "relation_id": RELATION_ID,
        "classification": classification,
        "statement": "Observed implementation relates to governed knowledge.",
        "rationale": "The explicitly bound evidence roles support this finding.",
        "supporting_repository_refs": (
            ["R1"]
            if supporting_repository_refs is None
            else supporting_repository_refs
        ),
        "supporting_knowledge_refs": (
            ["K1"]
            if supporting_knowledge_refs is None
            else supporting_knowledge_refs
        ),
        "limiting_or_counterevidence_refs": (
            []
            if limiting_or_counterevidence_refs is None
            else limiting_or_counterevidence_refs
        ),
        "uncertainty_basis": uncertainty_basis,
    }


def _role_response(**finding_overrides: object) -> str:
    finding = _role_finding(**finding_overrides)
    # Sólo fixture de integración válida. Los negativos canónicos se ejercitan
    # directamente contra el parser final en _parse_role_finding.
    roles = {}
    for field, role in (("supporting_repository_refs", "SUPPORT"),
                        ("supporting_knowledge_refs", "SUPPORT"),
                        ("limiting_or_counterevidence_refs", "LIMIT")):
        for ref in finding.pop(field):
            if ref in roles:
                raise ValueError("fixture cannot overwrite an evidence role")
            roles[ref] = role
    finding["evidence_roles"] = roles
    return json.dumps({
        "schema_id": "malak.e3.ref-role-map.v1",
        "summary": "Governed relation evaluated with explicit evidence roles.",
        "findings": [finding], "uncertainties": [],
    })


def _legacy_response(*, relation_id: str | None = None) -> str:
    finding: dict[str, object] = {
        "classification": "ALIGNED",
        "statement": "Observed implementation relates to governed knowledge.",
        "rationale": "Repository and governed knowledge support this finding.",
        "evidence_refs": ["R1", "K1"],
    }
    if relation_id is not None:
        finding["relation_id"] = relation_id
    return json.dumps(
        {
            "summary": "Legacy grounded engineering analysis.",
            "findings": [finding],
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
    response: str,
    focused: bool = True,
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
        evidence_focus=_focus() if focused else None,
    )
    return provider, capability


def _execute(capability: EngineeringAnalyzeCapability) -> str:
    return capability.execute(Request(content="Kernel", session_id="s"))


def _repository_evidence() -> list[dict[str, object]]:
    return [
        {
            "ref": "R1",
            "path": "src/malak/kernel/core.py",
            "blob_sha": "r" * 40,
            "line_number": 1,
            "text": "class Kernel:",
        }
    ]


def _knowledge_evidence(
    *,
    authority_class: str = "normative_subordinate",
    source_class: str = "APPROVED_SPECIFICATION",
) -> list[dict[str, object]]:
    return [
        {
            "ref": "K1",
            "path": "docs/architecture/kernel.md",
            "blob_sha": "k" * 40,
            "line_number": 1,
            "text": "Kernel First. Core Kernel owns orchestration.",
            "source_class": source_class,
            "authority_class": authority_class,
        }
    ]


def _parse_role_finding(
    finding: dict[str, object],
    *,
    knowledge_evidence: list[dict[str, object]] | None = None,
):
    analyze = import_module("malak.capabilities.engineering_analyze")
    return analyze._parse_canonical_analysis(
        json.dumps(
            {
                "summary": "Role-bound analysis.",
                "findings": [finding],
                "uncertainties": [],
            }
        ),
        repository_evidence=_repository_evidence(),
        knowledge_evidence=(
            _knowledge_evidence()
            if knowledge_evidence is None
            else knowledge_evidence
        ),
        allowed_relation_ids=(RELATION_ID,),
    )


def test_e3_role_binding_red_r01_relation_schema_requires_exact_role_fields(
    tmp_path: Path,
) -> None:
    provider, capability = _capability(
        tmp_path,
        response=_role_response(),
    )

    try:
        _execute(capability)
    except RuntimeError:
        pass

    schema = json.loads(provider.requests[-1].response_json_schema)
    finding = schema["properties"]["findings"]["items"]
    properties = finding["properties"]

    assert set(finding["required"]) == {
        "relation_id",
        "classification",
        "statement",
        "rationale",
        "evidence_roles",
        "uncertainty_basis",
    }
    assert "evidence_refs" not in properties
    assert "supporting_repository_refs" not in properties
    assert set(properties["evidence_roles"]["properties"]) == {"R1", "K1"}
    assert properties["evidence_roles"]["additionalProperties"] is False


def test_e3_role_binding_red_r02_knowledge_ref_in_repository_support_fails_closed() -> None:
    with pytest.raises(RuntimeError) as exc:
        _parse_role_finding(
            _role_finding(supporting_repository_refs=["K1"]),
        )

    assert "supporting_repository_refs" in str(exc.value)
    assert "repository" in str(exc.value).lower()


def test_e3_role_binding_red_r03_repository_ref_in_knowledge_support_fails_closed() -> None:
    with pytest.raises(RuntimeError) as exc:
        _parse_role_finding(
            _role_finding(supporting_knowledge_refs=["R1"]),
        )

    assert "supporting_knowledge_refs" in str(exc.value)
    assert "knowledge" in str(exc.value).lower()


def test_e3_role_binding_red_r04_unknown_duplicate_or_overlap_fails_closed() -> None:
    cases = (
        (
            _role_finding(supporting_repository_refs=["R9"]),
            "unknown",
        ),
        (
            _role_finding(supporting_repository_refs=["R1", "R1"]),
            "duplicate",
        ),
        (
            _role_finding(limiting_or_counterevidence_refs=["R1"]),
            "overlap",
        ),
    )

    for finding, marker in cases:
        with pytest.raises(RuntimeError) as exc:
            _parse_role_finding(finding)
        assert marker in str(exc.value).lower()


def test_e3_role_binding_red_r05_relational_class_requires_both_support_roles() -> None:
    cases = (
        _role_finding(supporting_repository_refs=[]),
        _role_finding(supporting_knowledge_refs=[]),
    )

    for finding in cases:
        with pytest.raises(RuntimeError) as exc:
            _parse_role_finding(finding)
        message = str(exc.value).lower()
        assert "repository" in message
        assert "knowledge" in message
        assert "support" in message


def test_e3_role_binding_red_r06_unresolved_requires_valid_non_none_basis() -> None:
    cases = (
        _role_finding(
            classification="UNRESOLVED",
            uncertainty_basis="NONE",
        ),
        _role_finding(
            classification="UNRESOLVED",
            uncertainty_basis="NOT_A_GOVERNED_BASIS",
        ),
    )

    for finding in cases:
        with pytest.raises(RuntimeError) as exc:
            _parse_role_finding(finding)
        assert "uncertainty_basis" in str(exc.value)


def test_e3_role_binding_red_r07_resolved_class_requires_none_basis() -> None:
    with pytest.raises(RuntimeError) as exc:
        _parse_role_finding(
            _role_finding(
                classification="ALIGNED",
                uncertainty_basis="CURRENT_MATERIAL_AMBIGUITY",
            )
        )

    assert "uncertainty_basis" in str(exc.value)


def test_e3_role_binding_red_r08_current_precedence_requires_normative_knowledge() -> None:
    non_normative = _knowledge_evidence(
        authority_class="non_normative",
        source_class="CURATED_REFERENCE",
    )

    with pytest.raises(RuntimeError) as exc:
        _parse_role_finding(
            _role_finding(
                classification="UNRESOLVED",
                uncertainty_basis="UNRESOLVED_CURRENT_PRECEDENCE",
            ),
            knowledge_evidence=non_normative,
        )

    message = str(exc.value).lower()
    assert "precedence" in message
    assert "normative" in message


def test_e3_role_binding_red_r09_valid_binding_renders_explicit_unverified_assurance(
    tmp_path: Path,
) -> None:
    _provider, capability = _capability(
        tmp_path,
        response=_role_response(),
    )

    result = _execute(capability)

    assert "status: GROUNDED" in result
    assert "semantic_assurance: NOT_VERIFIED" in result
    assert f"relation_id={RELATION_ID}" in result
    assert "supporting_repository_refs: [R1]" in result
    assert "supporting_knowledge_refs: [K1]" in result
    assert "limiting_or_counterevidence_refs: (none)" in result
    assert "uncertainty_basis: NONE" in result
    assert "authority_effect: none" in result


def test_e3_role_binding_red_r10_empty_catalog_preserves_exact_generic_contract(
    tmp_path: Path,
) -> None:
    provider, capability = _capability(
        tmp_path,
        response=_legacy_response(),
        focused=False,
    )

    result = _execute(capability)
    analyze = import_module("malak.capabilities.engineering_analyze")

    assert provider.requests[-1].response_json_schema == analyze.ANALYZE_RESPONSE_JSON_SCHEMA
    assert "relation_id=" not in result
    assert "evidence_refs: [R1] [K1]" in result
    assert "semantic_assurance:" not in result
    assert "status: GROUNDED" in result
    assert "authority_effect: none" in result


def test_e3_role_binding_red_r11_e4_legacy_analysis_remains_relationless() -> None:
    propose = import_module("malak.capabilities.engineering_propose")

    analysis = propose._parse_analysis(
        _legacy_response(),
        repository_evidence=[{"ref": "R1"}],
        knowledge_evidence=[{"ref": "K1"}],
    )

    assert len(analysis.findings) == 1
    assert analysis.findings[0].relation_id is None
    assert analysis.findings[0].classification == "ALIGNED"
    assert analysis.findings[0].evidence_refs == ("R1", "K1")
