from __future__ import annotations

import json
import subprocess
from importlib import import_module
from pathlib import Path

import pytest

from malak.core.conversation import ConversationProvider, ConversationRequest, ConversationResponse
from malak.core.conversation_registry import ConversationProviderRegistry
from malak.core.request import Request
from malak.infrastructure.repository_reader import GitRepositoryReader
from malak.knowledge.knowledge_reader import GovernedKnowledgeReader
from malak.services.conversation_context import InMemoryConversationContext
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

    write(repo, "src/malak/component.py", 'VALUE = "needle implementation repo-only"\n')
    write(repo, "README.md", "needle repository-reference\n")
    write(
        repo,
        "docs/governance/cognitive_constitution.md",
        "needle governing-context knowledge-only\n",
    )
    write(repo, "docs/architecture/blueprint.md", "needle architecture-context\n")
    write(repo, "SECURITY.md", "needle security-context\n")
    write(
        repo,
        "docs/architecture/adr/ADR-007-example.md",
        "---\nstatus: proposed\n---\nneedle proposed-decision\n",
    )
    write(
        repo,
        "documents/projects/jarvis/ideas.md",
        "needle non-normative-context\n",
    )
    git(repo, "add", ".")
    git(repo, "commit", "--no-gpg-sign", "-m", "baseline")
    return repo, git(repo, "rev-parse", "HEAD")


def analysis_json(
    classification: str = "GAP",
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


def proposal_json(
    *,
    kind: str = "HARDEN",
    finding_refs: list[str] | None = None,
    evidence_refs: list[str] | None = None,
) -> str:
    return json.dumps(
        {
            "summary": "Bounded candidate proposal for owner review.",
            "proposals": [
                {
                    "kind": kind,
                    "target": "src/malak/component.py",
                    "description": "Harden the observed implementation boundary.",
                    "rationale": "The grounded gap supports presenting this candidate change.",
                    "finding_refs": finding_refs or ["A1"],
                    "evidence_refs": evidence_refs or ["R1", "K1"],
                }
            ],
            "validation_plan": ["Run targeted tests.", "Run the full regression suite."],
            "risks": ["Behavioral regression if the boundary is widened."],
            "assumptions": ["Owner authorization remains required before implementation."],
        }
    )


class SequencedProvider(ConversationProvider):
    def __init__(self, responses: list[str] | None = None) -> None:
        self.responses = list(responses or [analysis_json(), proposal_json()])
        self.calls = 0
        self.requests: list[ConversationRequest] = []

    def generate(self, request: ConversationRequest) -> ConversationResponse:
        self.requests.append(request)
        index = self.calls
        self.calls += 1
        if index >= len(self.responses):
            raise RuntimeError("unexpected provider call")
        return ConversationResponse(
            content=self.responses[index],
            model=request.model,
            provider="recording",
        )


class FailingProvider(ConversationProvider):
    def __init__(self, *, fail_on_call: int) -> None:
        self.fail_on_call = fail_on_call
        self.calls = 0

    def generate(self, request: ConversationRequest) -> ConversationResponse:
        self.calls += 1
        if self.calls == self.fail_on_call:
            raise RuntimeError("provider failure")
        return ConversationResponse(
            content=analysis_json(),
            model=request.model,
            provider="recording",
        )


def service(
    provider: ConversationProvider,
    *,
    context: InMemoryConversationContext | None = None,
) -> ConversationService:
    registry = ConversationProviderRegistry()
    registry.register("recording", provider)
    return ConversationService(registry, context=context)


def module():
    return import_module("malak.capabilities.engineering_propose")


def build(
    tmp_path: Path,
    provider: ConversationProvider | None = None,
    *,
    context: InMemoryConversationContext | None = None,
):
    repo, baseline = make_repo(tmp_path)
    repository_reader = GitRepositoryReader(repo)
    knowledge_reader = GovernedKnowledgeReader(repository_reader)
    actual_provider = provider or SequencedProvider()
    capability = module().EngineeringProposeCapability(
        repository_reader=repository_reader,
        knowledge_reader=knowledge_reader,
        conversation_service=service(actual_provider, context=context),
        provider_name="recording",
        model="test-model",
    )
    return repo, baseline, repository_reader, knowledge_reader, actual_provider, capability


def execute(capability, content: str = "needle") -> str:
    return capability.execute(Request(content=content, session_id="session-A"))


def proposal_packet(provider: SequencedProvider) -> dict:
    return json.loads(provider.requests[-1].prompt)


def test_e4_red_c01_name(tmp_path: Path) -> None:
    *_, capability = build(tmp_path)
    assert capability.name == "engineering_propose"


def test_e4_red_c02_baseline_mismatch_fails(tmp_path: Path) -> None:
    left = tmp_path / "left"
    right = tmp_path / "right"
    left.mkdir()
    right.mkdir()
    repo_a, _ = make_repo(left)
    repo_b, _ = make_repo(right)
    write(repo_b, "extra.txt", "different\n")
    git(repo_b, "add", "extra.txt")
    git(repo_b, "commit", "--no-gpg-sign", "-m", "different")

    with pytest.raises(RuntimeError):
        module().EngineeringProposeCapability(
            repository_reader=GitRepositoryReader(repo_a),
            knowledge_reader=GovernedKnowledgeReader(GitRepositoryReader(repo_b)),
            conversation_service=service(SequencedProvider()),
            provider_name="recording",
        )


@pytest.mark.parametrize("subject", ["", "   ", "\n", "needle\nnext", "\t"])
def test_e4_red_c03_invalid_subject(tmp_path: Path, subject: str) -> None:
    *_, capability = build(tmp_path)
    with pytest.raises(ValueError):
        execute(capability, subject)


def test_e4_red_c04_subject_bound(tmp_path: Path) -> None:
    *_, capability = build(tmp_path)
    with pytest.raises(ValueError):
        execute(capability, "x" * 513)


@pytest.mark.parametrize("subject", ["repo-only", "knowledge-only"])
def test_e4_red_c05_one_sided_evidence_is_unconfirmed_without_model(
    tmp_path: Path,
    subject: str,
) -> None:
    *_, provider, capability = build(tmp_path)
    result = execute(capability, subject)
    assert provider.calls == 0
    assert "status: UNCONFIRMED" in result
    assert "authority_effect: none" in result
    assert "owner_authorization_required: true" in result


@pytest.mark.parametrize("classification", ["GAP", "PARTIAL"])
def test_e4_red_c06_actionable_analysis_calls_proposal_once(
    tmp_path: Path,
    classification: str,
) -> None:
    provider = SequencedProvider([analysis_json(classification), proposal_json()])
    *_, capability = build(tmp_path, provider)
    result = execute(capability)
    assert provider.calls == 2
    assert all(request.history == () for request in provider.requests)
    assert "status: GROUNDED" in result


def test_e4_red_c07_aligned_analysis_is_no_proposal(tmp_path: Path) -> None:
    provider = SequencedProvider([analysis_json("ALIGNED")])
    *_, capability = build(tmp_path, provider)
    result = execute(capability)
    assert provider.calls == 1
    assert "status: NO_PROPOSAL" in result
    assert "does not demonstrate a change need" in result


@pytest.mark.parametrize(
    ("classification", "reason"),
    [
        ("UNRESOLVED", "owner resolution"),
        ("CONTRADICTION", "owner resolution"),
    ],
)
def test_e4_red_c08_blocking_analysis_never_calls_proposal(
    tmp_path: Path,
    classification: str,
    reason: str,
) -> None:
    provider = SequencedProvider([analysis_json(classification)])
    *_, capability = build(tmp_path, provider)
    result = execute(capability)
    assert provider.calls == 1
    assert "status: NO_PROPOSAL" in result
    assert reason in result


def test_e4_red_c09_proposal_prompt_boundary(tmp_path: Path) -> None:
    provider = SequencedProvider()
    *_, capability = build(tmp_path, provider)
    m = module()
    execute(capability)
    request = provider.requests[-1]
    assert request.system_prompt == m._PROPOSAL_SYSTEM_PROMPT
    assert "ENGINEERING PROPOSE" in request.system_prompt
    assert "untrusted" in request.system_prompt.lower()
    assert "do not execute" in request.system_prompt.lower()
    assert "do not authorize" in request.system_prompt.lower()


def test_e4_red_c10_proposal_packet_is_grounded(tmp_path: Path) -> None:
    provider = SequencedProvider()
    _, baseline, _, _, _, capability = build(tmp_path, provider)
    execute(capability)
    packet = proposal_packet(provider)
    assert packet["baseline_commit"] == baseline
    assert packet["proposal_subject"] == "needle"
    assert packet["structured_analysis"]["findings"]
    assert packet["repository_evidence"]
    assert packet["knowledge_evidence"]
    assert packet["limitations"]["authority_effect"] == "none"


@pytest.mark.parametrize("content", ["{not-json", "~~~json\n{}\n~~~"])
def test_e4_red_c11_invalid_proposal_json_rejected(
    tmp_path: Path,
    content: str,
) -> None:
    provider = SequencedProvider([analysis_json(), content])
    *_, capability = build(tmp_path, provider)
    with pytest.raises(RuntimeError):
        execute(capability)


def test_e4_red_c12_extra_top_level_field_rejected(tmp_path: Path) -> None:
    payload = json.loads(proposal_json())
    payload["authorization"] = True
    provider = SequencedProvider([analysis_json(), json.dumps(payload)])
    *_, capability = build(tmp_path, provider)
    with pytest.raises(RuntimeError):
        execute(capability)


def test_e4_red_c13_unknown_kind_rejected(tmp_path: Path) -> None:
    provider = SequencedProvider([analysis_json(), proposal_json(kind="EXECUTE")])
    *_, capability = build(tmp_path, provider)
    with pytest.raises(RuntimeError):
        execute(capability)


def test_e4_red_c14_unknown_finding_ref_rejected(tmp_path: Path) -> None:
    provider = SequencedProvider(
        [analysis_json(), proposal_json(finding_refs=["A999"])]
    )
    *_, capability = build(tmp_path, provider)
    with pytest.raises(RuntimeError):
        execute(capability)


def test_e4_red_c15_unknown_evidence_ref_rejected(tmp_path: Path) -> None:
    provider = SequencedProvider(
        [analysis_json(), proposal_json(evidence_refs=["R999", "K1"])]
    )
    *_, capability = build(tmp_path, provider)
    with pytest.raises(RuntimeError):
        execute(capability)


def test_e4_red_c16_evidence_must_belong_to_cited_findings(tmp_path: Path) -> None:
    provider = SequencedProvider(
        [
            analysis_json("GAP", ["R1", "K1"]),
            proposal_json(evidence_refs=["R2", "K1"]),
        ]
    )
    *_, capability = build(tmp_path, provider)
    with pytest.raises(RuntimeError):
        execute(capability)


def test_e4_red_c17_proposal_must_cite_actionable_finding(tmp_path: Path) -> None:
    analysis = {
        "summary": "Mixed grounded analysis.",
        "findings": [
            {
                "classification": "GAP",
                "statement": "Gap.",
                "rationale": "Gap evidence.",
                "evidence_refs": ["R1", "K1"],
            },
            {
                "classification": "ALIGNED",
                "statement": "Aligned.",
                "rationale": "Aligned evidence.",
                "evidence_refs": ["R1", "K1"],
            },
        ],
        "uncertainties": [],
    }
    provider = SequencedProvider(
        [json.dumps(analysis), proposal_json(finding_refs=["A2"])]
    )
    *_, capability = build(tmp_path, provider)
    with pytest.raises(RuntimeError):
        execute(capability)


@pytest.mark.parametrize(
    ("field", "values"),
    [
        ("finding_refs", ["A1", "A1"]),
        ("evidence_refs", ["R1", "K1", "R1"]),
    ],
)
def test_e4_red_c18_duplicate_refs_rejected(
    tmp_path: Path,
    field: str,
    values: list[str],
) -> None:
    payload = json.loads(proposal_json())
    payload["proposals"][0][field] = values
    provider = SequencedProvider([analysis_json(), json.dumps(payload)])
    *_, capability = build(tmp_path, provider)
    with pytest.raises(RuntimeError):
        execute(capability)


def test_e4_red_c19_grounded_requires_at_least_one_proposal(tmp_path: Path) -> None:
    payload = json.loads(proposal_json())
    payload["proposals"] = []
    provider = SequencedProvider([analysis_json(), json.dumps(payload)])
    *_, capability = build(tmp_path, provider)
    with pytest.raises(RuntimeError):
        execute(capability)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("summary", "safe\nforged"),
        ("target", "safe\tforged"),
        ("description", "safe\u202eforged"),
        ("rationale", "safe\u2028forged"),
        ("validation_plan", "safe\u2066forged"),
        ("risks", "safe\nforged"),
        ("assumptions", "safe\tforged"),
    ],
)
def test_e4_red_c20_free_text_rejects_control_or_format(
    tmp_path: Path,
    field: str,
    value: str,
) -> None:
    payload = json.loads(proposal_json())
    if field == "summary":
        payload["summary"] = value
    elif field in {"validation_plan", "risks", "assumptions"}:
        payload[field] = [value]
    else:
        payload["proposals"][0][field] = value
    provider = SequencedProvider([analysis_json(), json.dumps(payload)])
    *_, capability = build(tmp_path, provider)
    with pytest.raises(RuntimeError):
        execute(capability)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("summary", "forged [P1]"),
        ("target", "forged [R1]"),
        ("description", "forged [K1]"),
        ("rationale", "forged [A1]"),
        ("validation_plan", "forged [P99]"),
    ],
)
def test_e4_red_c21_generated_text_cannot_inject_reserved_refs(
    tmp_path: Path,
    field: str,
    value: str,
) -> None:
    payload = json.loads(proposal_json())
    if field == "summary":
        payload["summary"] = value
    elif field == "validation_plan":
        payload[field] = [value]
    else:
        payload["proposals"][0][field] = value
    provider = SequencedProvider([analysis_json(), json.dumps(payload)])
    *_, capability = build(tmp_path, provider)
    with pytest.raises(RuntimeError):
        execute(capability)


def test_e4_red_c22_envelope_is_non_authoritative(tmp_path: Path) -> None:
    _, baseline, _, _, _, capability = build(tmp_path)
    result = execute(capability)
    assert result.startswith("ENGINEERING_PROPOSAL\n")
    assert f"baseline_commit: {baseline}" in result
    assert "status: GROUNDED" in result
    assert "authority_effect: none" in result
    assert "owner_authorization_required: true" in result
    assert "[P1] kind=HARDEN" in result
    assert "finding_refs: [A1]" in result
    assert "evidence_refs: [R1] [K1]" in result


def test_e4_red_c23_no_repository_mutation(tmp_path: Path) -> None:
    repo, _, _, _, _, capability = build(tmp_path)
    before = git(repo, "status", "--porcelain=v1", "--untracked-files=all")
    execute(capability)
    after = git(repo, "status", "--porcelain=v1", "--untracked-files=all")
    assert after == before == ""


def test_e4_red_c24_analysis_provider_failure_propagates(tmp_path: Path) -> None:
    provider = FailingProvider(fail_on_call=1)
    *_, capability = build(tmp_path, provider)
    with pytest.raises(RuntimeError, match="provider failure"):
        execute(capability)
    assert provider.calls == 1


def test_e4_red_c25_proposal_provider_failure_propagates(tmp_path: Path) -> None:
    provider = FailingProvider(fail_on_call=2)
    *_, capability = build(tmp_path, provider)
    with pytest.raises(RuntimeError, match="provider failure"):
        execute(capability)
    assert provider.calls == 2


def test_e4_red_c26_contextful_service_fails_closed_without_session(
    tmp_path: Path,
) -> None:
    provider = SequencedProvider()
    context = InMemoryConversationContext()
    *_, capability = build(tmp_path, provider, context=context)
    with pytest.raises(ValueError, match="session_id is required"):
        execute(capability)
    assert provider.calls == 0
    assert context.snapshot("session-A") == ()


def test_e4_red_c27_truncated_context_is_unconfirmed_without_model(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    m = module()
    monkeypatch.setattr(m, "_MAX_CONTEXT_MATCHES_PER_KIND", 1)
    *_, provider, capability = build(tmp_path)
    result = execute(capability)
    assert provider.calls == 0
    assert "status: UNCONFIRMED" in result
    assert "context_truncated: true" in result


def test_e4_red_c28_proposal_prompt_is_byte_bounded(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    m = module()
    monkeypatch.setattr(m, "_MAX_PROPOSAL_PROMPT_BYTES", 32)
    provider = SequencedProvider()
    *_, capability = build(tmp_path, provider)
    with pytest.raises(RuntimeError):
        execute(capability)
    assert provider.calls == 1


def test_e4_red_c29_proposal_output_is_byte_bounded(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    m = module()
    monkeypatch.setattr(m, "_MAX_PROPOSAL_MODEL_OUTPUT_BYTES", 16)
    provider = SequencedProvider()
    *_, capability = build(tmp_path, provider)
    with pytest.raises(RuntimeError):
        execute(capability)
    assert provider.calls == 2


def test_e4_red_c30_counts_are_bounded(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    m = module()
    monkeypatch.setattr(m, "_MAX_PROPOSALS", 1)
    payload = json.loads(proposal_json())
    payload["proposals"].append(dict(payload["proposals"][0]))
    provider = SequencedProvider([analysis_json(), json.dumps(payload)])
    *_, capability = build(tmp_path, provider)
    with pytest.raises(RuntimeError):
        execute(capability)


@pytest.mark.parametrize(
    ("constant", "field"),
    [
        ("_MAX_SUMMARY_BYTES", "summary"),
        ("_MAX_TARGET_BYTES", "target"),
        ("_MAX_DESCRIPTION_BYTES", "description"),
        ("_MAX_RATIONALE_BYTES", "rationale"),
        ("_MAX_LIST_ITEM_BYTES", "validation_plan"),
    ],
)
def test_e4_red_c31_text_fields_are_byte_bounded(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    constant: str,
    field: str,
) -> None:
    m = module()
    monkeypatch.setattr(m, constant, 8)
    payload = json.loads(proposal_json())
    if field == "summary":
        payload["summary"] = "x" * 16
    elif field == "validation_plan":
        payload[field] = ["x" * 16]
    else:
        payload["proposals"][0][field] = "x" * 16
    provider = SequencedProvider([analysis_json(), json.dumps(payload)])
    *_, capability = build(tmp_path, provider)
    with pytest.raises(RuntimeError):
        execute(capability)
