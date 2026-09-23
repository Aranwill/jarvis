from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from importlib import import_module
from pathlib import Path
from types import SimpleNamespace

import pytest

from malak.core.response import Response
from malak.infrastructure.repository_reader import GitRepositoryReader
from malak.knowledge.knowledge_reader import GovernedKnowledgeReader


NOW = datetime(2026, 9, 23, 21, 0, tzinfo=timezone.utc)

REQUIRED_TEXT_FILES = {
    "AGENTS.md": "agent rules\n",
    "SECURITY.md": "security policy\n",
    "docs/governance/cognitive_constitution.md": "cognitive constitution\n",
    "docs/governance/governance_constitution.md": "governance constitution\n",
    "docs/architecture/blueprint.md": "blueprint\n",
    "docs/architecture/architecture_quality_gates.md": "quality gates\n",
    "docs/development/malak_construction_protocol.md": "construction protocol\n",
    "docs/development/development_checklist.md": "development checklist\n",
    "docs/project/implementation_roadmap.md": "implementation roadmap\n",
    "documents/projects/jarvis/ideas.md": "ideas\n",
    "docs/project/concepts/MALAK_RESEARCH_HORIZON_MAP.md": "research horizon\n",
    "docs/project/concepts/GOVERNED_SELF_REVIEW_BOOTSTRAP_TASK.md": "self review bootstrap\n",
    "docs/project/status/MALAK-CONSTRUCTION-FLOW-COMPLIANCE-AUDIT-V1-FINAL.md": "audit v1\n",
}

ARTIFACT_FILES = {
    "manifest.json",
    "trace.jsonl",
    "evidence.json",
    "assessment.json",
    "outcome.json",
    "attestation.json",
}


def _module():
    return import_module("malak.app.internal_interaction")


def _trace_module():
    return import_module("malak.observability.execution_trace")


def _git(repo: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def _write(repo: Path, relative: str, content: str) -> None:
    path = repo / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _make_repo(
    tmp_path: Path,
    *,
    omit: str | None = None,
) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()

    _git(repo, "init")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Malak Test")
    _git(repo, "config", "commit.gpgsign", "false")

    for relative, text in REQUIRED_TEXT_FILES.items():
        if relative != omit:
            _write(repo, relative, text)

    _write(
        repo,
        "docs/architecture/adr/ADR-003-test.md",
        "---\nid: ADR-003\nstatus: accepted\n---\naccepted\n",
    )
    _write(
        repo,
        "docs/project/concepts/README.md",
        "concept catalog\n",
    )
    _write(
        repo,
        "src/malak/example.py",
        "VALUE = 1\n",
    )
    _write(
        repo,
        "tests/test_example.py",
        "def test_example():\n    assert True\n",
    )
    _write(repo, ".gitignore", "/runtime/\n")

    _git(repo, "add", ".")
    _git(repo, "commit", "--no-gpg-sign", "-m", "baseline")
    return repo


class _Kernel:
    def __init__(
        self,
        content: str,
        *,
        name: str,
        calls: list[str],
        failure: Exception | None = None,
    ) -> None:
        self._content = content
        self._name = name
        self._calls = calls
        self._failure = failure

    def receive(self, request) -> Response:
        self._calls.append(self._name)
        if self._failure is not None:
            raise self._failure
        return Response(content=self._content, source=self._name)


def _engineering(
    repo: Path,
    *,
    analyze_classification: str = "ALIGNED",
    analyze_status: str = "GROUNDED",
    analyze_failure: Exception | None = None,
):
    reader = GitRepositoryReader(repo)
    knowledge = GovernedKnowledgeReader(reader)
    baseline = reader.baseline_commit
    calls: list[str] = []

    inspect = "\n".join(
        (
            "ENGINEERING_INSPECTION",
            f"baseline_commit: {baseline}",
            "status: GROUNDED",
            "authority_effect: none",
            "ANALYSIS",
            "bounded inspection",
        )
    )
    analyze = "\n".join(
        (
            "ENGINEERING_ANALYSIS",
            f"baseline_commit: {baseline}",
            f"status: {analyze_status}",
            "authority_effect: none",
            "FINDINGS",
            (
                f"[A1] classification={analyze_classification}"
                if analyze_status == "GROUNDED"
                else "(none)"
            ),
            "UNCERTAINTIES",
            "(none)",
        )
    )
    propose = "\n".join(
        (
            "ENGINEERING_PROPOSAL",
            f"baseline_commit: {baseline}",
            "status: GROUNDED",
            "proposal_count: 1",
            "authority_effect: none",
            "owner_authorization_required: true",
            "PROPOSALS",
            "[P1] kind=HARDEN",
        )
    )

    kernels = {
        "inspect": _Kernel(inspect, name="inspect", calls=calls),
        "analyze": _Kernel(
            analyze,
            name="analyze",
            calls=calls,
            failure=analyze_failure,
        ),
        "propose": _Kernel(propose, name="propose", calls=calls),
    }
    engineering = SimpleNamespace(
        baseline_commit=baseline,
        kernels=kernels,
        repository_reader=reader,
        knowledge_reader=knowledge,
    )
    return engineering, calls


def _runner(repo: Path, engineering, *, artifact_root: Path | None = None):
    root = (
        artifact_root
        if artifact_root is not None
        else repo / "runtime" / "internal_interaction"
    )
    return _module().InternalInteractionRunner(
        engineering=engineering,
        artifact_root=root,
    )


def _run(runner):
    return runner.run(
        task_id="self-review-v0",
        scope="kernel-and-observability",
        external_validation_refs=("Validation#428",),
        run_id="run-001",
        created_at=NOW,
    )


def test_interaction_red_c01_terminal_disposition_is_closed() -> None:
    disposition = _module().TerminalDisposition

    assert {item.value for item in disposition} == {
        "NO_CHANGE_RECOMMENDED",
        "HARDENING_PROPOSAL",
        "RESEARCH_REQUIRED",
        "DEFER",
        "INCONCLUSIVE",
    }

    with pytest.raises(ValueError):
        disposition("APPROVED")


def test_interaction_red_c02_aligned_analysis_stops_without_proposal(
    tmp_path: Path,
) -> None:
    repo = _make_repo(tmp_path)
    engineering, calls = _engineering(repo, analyze_classification="ALIGNED")

    result = _run(_runner(repo, engineering))

    assert result.disposition.value == "NO_CHANGE_RECOMMENDED"
    assert calls == ["inspect", "analyze"]
    assert "engineering_inspect" in result.component_path
    assert "engineering_analyze" in result.component_path
    assert "engineering_propose" not in result.component_path
    assert result.authority_effect == "none"


@pytest.mark.parametrize("classification", ["GAP", "PARTIAL"])
def test_interaction_red_c03_actionable_analysis_runs_proposal(
    tmp_path: Path,
    classification: str,
) -> None:
    repo = _make_repo(tmp_path)
    engineering, calls = _engineering(
        repo,
        analyze_classification=classification,
    )

    result = _run(_runner(repo, engineering))

    assert result.disposition.value == "HARDENING_PROPOSAL"
    assert calls == ["inspect", "analyze", "propose"]
    assert result.component_path[-1] == "engineering_propose"
    assert result.authority_effect == "none"


@pytest.mark.parametrize("classification", ["CONTRADICTION", "UNRESOLVED"])
def test_interaction_red_c04_unresolved_analysis_is_inconclusive(
    tmp_path: Path,
    classification: str,
) -> None:
    repo = _make_repo(tmp_path)
    engineering, calls = _engineering(
        repo,
        analyze_classification=classification,
    )

    result = _run(_runner(repo, engineering))

    assert result.disposition.value == "INCONCLUSIVE"
    assert calls == ["inspect", "analyze"]
    assert result.authority_effect == "none"


def test_interaction_red_c05_missing_required_packet_input_stops_before_models(
    tmp_path: Path,
) -> None:
    repo = _make_repo(tmp_path, omit="SECURITY.md")
    engineering, calls = _engineering(repo)

    result = _run(_runner(repo, engineering))

    assert result.disposition.value == "INCONCLUSIVE"
    assert calls == []
    assert result.authority_effect == "none"


def test_interaction_red_c06_component_failure_is_visible_and_inconclusive(
    tmp_path: Path,
) -> None:
    repo = _make_repo(tmp_path)
    engineering, calls = _engineering(
        repo,
        analyze_failure=RuntimeError("synthetic failure"),
    )

    result = _run(_runner(repo, engineering))

    assert result.disposition.value == "INCONCLUSIVE"
    assert calls == ["inspect", "analyze"]
    failed = [
        event
        for event in result.trace_events
        if event.event_type == "COMPONENT_FAILED"
    ]
    assert len(failed) == 1
    assert failed[0].component == "engineering_analyze"
    assert failed[0].reason_code == "component_error"
    assert "synthetic failure" not in json.dumps(
        [event.reason_code for event in result.trace_events]
    )


def test_interaction_red_c07_successful_run_writes_exact_artifact_set(
    tmp_path: Path,
) -> None:
    repo = _make_repo(tmp_path)
    engineering, _ = _engineering(repo)

    result = _run(_runner(repo, engineering))

    assert result.artifact_dir.name == "run-001"
    assert {item.name for item in result.artifact_dir.iterdir()} == ARTIFACT_FILES

    for name in (
        "manifest.json",
        "evidence.json",
        "assessment.json",
        "outcome.json",
        "attestation.json",
    ):
        payload = json.loads(
            (result.artifact_dir / name).read_text(encoding="utf-8")
        )
        assert payload["authority_effect"] == "none"


def test_interaction_red_c08_attestation_detects_exact_byte_tampering(
    tmp_path: Path,
) -> None:
    repo = _make_repo(tmp_path)
    engineering, _ = _engineering(repo)

    result = _run(_runner(repo, engineering))
    _module().validate_internal_interaction_artifacts(result.artifact_dir)

    outcome_path = result.artifact_dir / "outcome.json"
    outcome_path.write_bytes(outcome_path.read_bytes() + b" ")

    with pytest.raises(ValueError):
        _module().validate_internal_interaction_artifacts(result.artifact_dir)


def test_interaction_red_c09_trace_persistence_failure_blocks_success(
    tmp_path: Path,
) -> None:
    repo = _make_repo(tmp_path)
    engineering, _ = _engineering(repo)
    blocked = tmp_path / "blocked"
    blocked.write_text("not a directory", encoding="utf-8")

    runner = _runner(
        repo,
        engineering,
        artifact_root=blocked / "internal_interaction",
    )

    with pytest.raises((OSError, RuntimeError)):
        _run(runner)


def test_interaction_red_c10_run_keeps_git_state_clean(
    tmp_path: Path,
) -> None:
    repo = _make_repo(tmp_path)
    engineering, _ = _engineering(repo)
    before = _git(repo, "status", "--porcelain")

    result = _run(_runner(repo, engineering))
    after = _git(repo, "status", "--porcelain")

    assert before == ""
    assert after == ""
    assert result.artifact_dir.is_relative_to(
        repo / "runtime" / "internal_interaction"
    )


def test_interaction_red_c11_replay_matches_live_component_path(
    tmp_path: Path,
) -> None:
    repo = _make_repo(tmp_path)
    engineering, _ = _engineering(
        repo,
        analyze_classification="GAP",
    )

    result = _run(_runner(repo, engineering))
    replayed = _trace_module().read_execution_trace_jsonl(
        result.artifact_dir / "trace.jsonl"
    )
    replay_path = _trace_module().project_component_path(replayed)

    assert replay_path == result.component_path


def test_interaction_red_c12_all_trace_events_remain_authority_free(
    tmp_path: Path,
) -> None:
    repo = _make_repo(tmp_path)
    engineering, _ = _engineering(repo)

    result = _run(_runner(repo, engineering))

    assert result.trace_events
    assert {
        event.authority_effect
        for event in result.trace_events
    } == {"none"}


def test_interaction_red_c13_non_actionable_propose_is_explicitly_skipped(
    tmp_path: Path,
) -> None:
    repo = _make_repo(tmp_path)
    engineering, _ = _engineering(repo, analyze_classification="ALIGNED")

    result = _run(_runner(repo, engineering))

    skipped = [
        event
        for event in result.trace_events
        if event.event_type == "COMPONENT_SKIPPED"
        and event.component == "engineering_propose"
    ]
    assert len(skipped) == 1
    assert skipped[0].outcome == "SKIPPED"
    assert skipped[0].reason_code == "not_required_by_workflow"
