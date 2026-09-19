from __future__ import annotations

import json
import subprocess
from importlib import import_module
from pathlib import Path

import pytest

from malak.capabilities.engineering_inspect import EngineeringInspectCapability
from malak.core.conversation import ConversationProvider, ConversationRequest, ConversationResponse
from malak.core.conversation_registry import ConversationProviderRegistry
from malak.core.request import Request
from malak.infrastructure.repository_reader import GitRepositoryReader
from malak.knowledge.knowledge_reader import GovernedKnowledgeReader
from malak.services.conversation_service import ConversationService


def git(repo: Path, *args: str) -> str:
    done = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return done.stdout.strip()


def write(repo: Path, relative: str, content: str) -> None:
    path = repo / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def make_repo(tmp_path: Path) -> tuple[Path, str]:
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init")
    git(repo, "config", "user.email", "test@example.com")
    git(repo, "config", "user.name", "Malak Test")
    git(repo, "config", "commit.gpgsign", "false")

    write(repo, "src/malak/component.py", 'VALUE = "needle implementation repo-only"\\n')
    write(repo, "README.md", "needle repository-reference\\n")
    write(
        repo,
        "docs/governance/cognitive_constitution.md",
        "needle governing-context knowledge-only\\n",
    )
    write(repo, "docs/architecture/blueprint.md", "needle architecture-context\\n")
    write(repo, "SECURITY.md", "needle security-context\\n")
    write(
        repo,
        "docs/architecture/adr/ADR-007-example.md",
        "---\\nstatus: proposed\\n---\\nneedle proposed-decision\\n",
    )
    write(
        repo,
        "documents/projects/jarvis/ideas.md",
        "needle non-normative-context\\n",
    )
    git(repo, "add", ".")
    git(repo, "commit", "--no-gpg-sign", "-m", "baseline")
    return repo, git(repo, "rev-parse", "HEAD")


def valid_json(
    classification: str = "ALIGNED",
    refs: list[str] | None = None,
) -> str:
    return json.dumps(
        {
            "summary": "Grounded engineering analysis.",
            "findings": [
                {
                    "classification": classification,
                    "statement": "Observed implementation relates to governed knowledge.",
                    "rationale": "The supplied evidence supports this finding.",
                    "evidence_refs": refs or ["R1", "K1"],
                }
            ],
            "uncertainties": [],
        }
    )


class RecordingProvider(ConversationProvider):
    def __init__(self, content: str | None = None) -> None:
        self.content = content or valid_json()
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


def service(provider: ConversationProvider) -> ConversationService:
    registry = ConversationProviderRegistry()
    registry.register("recording", provider)
    return ConversationService(registry)


def module():
    return import_module("malak.capabilities.engineering_analyze")


def build(tmp_path: Path, provider: RecordingProvider | None = None):
    repo, baseline = make_repo(tmp_path)
    repository_reader = GitRepositoryReader(repo)
    knowledge_reader = GovernedKnowledgeReader(repository_reader)
    actual_provider = provider or RecordingProvider()
    capability = module().EngineeringAnalyzeCapability(
        repository_reader=repository_reader,
        knowledge_reader=knowledge_reader,
        conversation_service=service(actual_provider),
        provider_name="recording",
        model="test-model",
    )
    return repo, baseline, repository_reader, knowledge_reader, actual_provider, capability


def execute(capability, content: str = "needle") -> str:
    return capability.execute(Request(content=content, session_id="session-A"))


def packet(provider: RecordingProvider) -> dict:
    return json.loads(provider.requests[-1].prompt)


def test_e3_red_c01_name(tmp_path: Path) -> None:
    *_, capability = build(tmp_path)
    assert capability.name == "engineering_analyze"


def test_e3_red_c02_baseline_mismatch_fails(tmp_path: Path) -> None:
    left = tmp_path / "left"
    right = tmp_path / "right"
    left.mkdir()
    right.mkdir()
    repo_a, _ = make_repo(left)
    repo_b, _ = make_repo(right)
    write(repo_b, "extra.txt", "different\\n")
    git(repo_b, "add", "extra.txt")
    git(repo_b, "commit", "--no-gpg-sign", "-m", "different")

    with pytest.raises(RuntimeError):
        module().EngineeringAnalyzeCapability(
            repository_reader=GitRepositoryReader(repo_a),
            knowledge_reader=GovernedKnowledgeReader(GitRepositoryReader(repo_b)),
            conversation_service=service(RecordingProvider()),
            provider_name="recording",
        )


@pytest.mark.parametrize("subject", ["", "   ", "\\n", "needle\\nnext", "\\t"])
def test_e3_red_c03_invalid_subject(tmp_path: Path, subject: str) -> None:
    *_, capability = build(tmp_path)
    with pytest.raises(ValueError):
        execute(capability, subject)


def test_e3_red_c04_subject_bound(tmp_path: Path) -> None:
    *_, capability = build(tmp_path)
    with pytest.raises(ValueError):
        execute(capability, "x" * 513)


@pytest.mark.parametrize("subject", ["repo-only", "knowledge-only"])
def test_e3_red_c05_one_sided_evidence_is_unconfirmed_without_model(
    tmp_path: Path,
    subject: str,
) -> None:
    *_, provider, capability = build(tmp_path)
    result = execute(capability, subject)
    assert provider.calls == 0
    assert "status: UNCONFIRMED" in result
    assert "analysis requires both implementation and governed knowledge evidence" in result


def test_e3_red_c06_both_surfaces_call_model_once(tmp_path: Path) -> None:
    *_, provider, capability = build(tmp_path)
    execute(capability)
    assert provider.calls == 1
    assert provider.requests[-1].history == ()


def test_e3_red_c07_prompt_boundary(tmp_path: Path) -> None:
    *_, provider, capability = build(tmp_path)
    m = module()
    execute(capability)
    request = provider.requests[-1]
    assert request.system_prompt == m._SYSTEM_PROMPT
    assert "ENGINEERING ANALYZE" in request.system_prompt
    assert "untrusted" in request.system_prompt.lower()
    assert "do not propose" in request.system_prompt.lower()
    assert '"analysis_subject":"needle"' in request.prompt


def test_e3_red_c08_e2_e3_evidence_is_identical(tmp_path: Path) -> None:
    repo, _ = make_repo(tmp_path)
    repository_reader = GitRepositoryReader(repo)
    knowledge_reader = GovernedKnowledgeReader(repository_reader)

    inspect_provider = RecordingProvider("inspection [R1] [K1]")
    inspect = EngineeringInspectCapability(
        repository_reader=repository_reader,
        knowledge_reader=knowledge_reader,
        conversation_service=service(inspect_provider),
        provider_name="recording",
    )

    analyze_provider = RecordingProvider()
    analyze = module().EngineeringAnalyzeCapability(
        repository_reader=repository_reader,
        knowledge_reader=knowledge_reader,
        conversation_service=service(analyze_provider),
        provider_name="recording",
    )

    request = Request(content="needle", session_id="s")
    inspect.execute(request)
    analyze.execute(request)

    inspect_packet = json.loads(inspect_provider.requests[-1].prompt)
    analyze_packet = json.loads(analyze_provider.requests[-1].prompt)
    assert analyze_packet["repository_evidence"] == inspect_packet["repository_evidence"]
    assert analyze_packet["knowledge_evidence"] == inspect_packet["knowledge_evidence"]
    assert analyze_packet["limitations"] == inspect_packet["limitations"]


def test_e3_red_c09_roles_preserved(tmp_path: Path) -> None:
    *_, provider, capability = build(tmp_path)
    execute(capability)
    roles = {
        (item["source_class"], item["authority_class"])
        for item in packet(provider)["knowledge_evidence"]
    }
    assert ("GOVERNING", "normative") in roles
    assert ("SECURITY_POLICY", "protected_subordinate") in roles
    assert ("DECISION_RECORD", "status_dependent") in roles
    assert ("NON_NORMATIVE_IDEA", "non_normative") in roles


@pytest.mark.parametrize("content", ["{not-json", "~~~json\\n{}\\n~~~"])
def test_e3_red_c10_invalid_json_shape_rejected(tmp_path: Path, content: str) -> None:
    provider = RecordingProvider(content)
    *_, capability = build(tmp_path, provider)
    with pytest.raises(RuntimeError):
        execute(capability)


def test_e3_red_c11_extra_fields_rejected(tmp_path: Path) -> None:
    payload = json.loads(valid_json())
    payload["authorization"] = True
    provider = RecordingProvider(json.dumps(payload))
    *_, capability = build(tmp_path, provider)
    with pytest.raises(RuntimeError):
        execute(capability)


def test_e3_red_c12_unknown_classification_rejected(tmp_path: Path) -> None:
    provider = RecordingProvider(valid_json("PERFECT"))
    *_, capability = build(tmp_path, provider)
    with pytest.raises(RuntimeError):
        execute(capability)


def test_e3_red_c13_unknown_ref_rejected(tmp_path: Path) -> None:
    provider = RecordingProvider(valid_json(refs=["R999", "K1"]))
    *_, capability = build(tmp_path, provider)
    with pytest.raises(RuntimeError):
        execute(capability)


def test_e3_red_c14_duplicate_ref_rejected(tmp_path: Path) -> None:
    provider = RecordingProvider(valid_json(refs=["R1", "K1", "R1"]))
    *_, capability = build(tmp_path, provider)
    with pytest.raises(RuntimeError):
        execute(capability)


@pytest.mark.parametrize("classification", ["ALIGNED", "PARTIAL", "GAP", "CONTRADICTION"])
@pytest.mark.parametrize("refs", [["R1"], ["K1"]])
def test_e3_red_c15_relational_findings_require_both_surfaces(
    tmp_path: Path,
    classification: str,
    refs: list[str],
) -> None:
    provider = RecordingProvider(valid_json(classification, refs))
    *_, capability = build(tmp_path, provider)
    with pytest.raises(RuntimeError):
        execute(capability)


@pytest.mark.parametrize("refs", [["R1"], ["K1"], ["R1", "K1"]])
def test_e3_red_c16_unresolved_allows_real_grounded_refs(
    tmp_path: Path,
    refs: list[str],
) -> None:
    provider = RecordingProvider(valid_json("UNRESOLVED", refs))
    *_, capability = build(tmp_path, provider)
    result = execute(capability)
    assert "classification=UNRESOLVED" in result


def test_e3_red_c17_envelope_is_non_authoritative(tmp_path: Path) -> None:
    _, baseline, _, _, _, capability = build(tmp_path)
    result = execute(capability)
    assert result.startswith("ENGINEERING_ANALYSIS\\n")
    assert f"baseline_commit: {baseline}" in result
    assert "status: GROUNDED" in result
    assert "authority_effect: none" in result
    assert "[A1] classification=ALIGNED" in result
    assert "evidence_refs: [R1] [K1]" in result


def test_e3_red_c18_no_repository_mutation(tmp_path: Path) -> None:
    repo, _, _, _, _, capability = build(tmp_path)
    before = git(repo, "status", "--porcelain=v1", "--untracked-files=all")
    execute(capability)
    after = git(repo, "status", "--porcelain=v1", "--untracked-files=all")
    assert after == before == ""
