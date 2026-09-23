from __future__ import annotations

import json
import subprocess
from datetime import UTC, datetime
from importlib import import_module
from pathlib import Path
from types import SimpleNamespace

import pytest

from malak.core.response import Response
from malak.infrastructure.repository_reader import GitRepositoryReader
from malak.knowledge.knowledge_reader import GovernedKnowledgeReader
from malak.runtime.mock_llm_runtime import MockLLMRuntime
from malak.runtime.ollama_runtime import OllamaRuntime


NOW = datetime(2026, 9, 23, 23, 30, tzinfo=UTC)

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
    "docs/project/concepts/GOVERNED_SELF_REVIEW_BOOTSTRAP_TASK.md": "bootstrap task\n",
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
    return import_module("malak.app.internal_interaction_test_v0")


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
    branch: str = "main",
    dirty_tracked: bool = False,
) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()

    _git(repo, "init")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Malak Test")
    _git(repo, "config", "commit.gpgsign", "false")

    for relative, text in REQUIRED_TEXT_FILES.items():
        _write(repo, relative, text)

    _write(
        repo,
        "docs/architecture/adr/ADR-003-test.md",
        "---\nid: ADR-003\nstatus: accepted\n---\naccepted\n",
    )
    _write(repo, "docs/project/concepts/README.md", "concept catalog\n")
    _write(repo, "src/malak/example.py", "VALUE = 1\n")
    _write(
        repo,
        "tests/test_example.py",
        "def test_example():\n    assert True\n",
    )
    _write(repo, "README.md", "baseline\n")
    _write(repo, ".gitignore", "/runtime/\n")

    _git(repo, "add", ".")
    _git(repo, "commit", "--no-gpg-sign", "-m", "baseline")
    _git(repo, "branch", "-M", branch)

    if dirty_tracked:
        _write(repo, "README.md", "dirty tracked change\n")

    return repo


class _Kernel:
    def __init__(
        self,
        content: str,
        *,
        calls: list[tuple[str, object]],
        name: str,
        mutate_repo: Path | None = None,
    ) -> None:
        self._content = content
        self._calls = calls
        self._name = name
        self._mutate_repo = mutate_repo

    def receive(self, request) -> Response:
        self._calls.append((self._name, request))
        if self._mutate_repo is not None:
            _write(
                self._mutate_repo,
                "README.md",
                "tracked mutation during run\n",
            )
        return Response(content=self._content, source=self._name)


def _engineering(
    repo: Path,
    *,
    mutate_during_inspect: bool = False,
):
    reader = GitRepositoryReader(repo)
    knowledge = GovernedKnowledgeReader(reader)
    baseline = reader.baseline_commit
    calls: list[tuple[str, object]] = []

    inspect = "\n".join(
        (
            "ENGINEERING_INSPECTION",
            f"baseline_commit: {baseline}",
            "status: GROUNDED",
            "authority_effect: none",
            "ANALYSIS",
            "bounded bootstrap inspection",
        )
    )
    analyze = "\n".join(
        (
            "ENGINEERING_ANALYSIS",
            f"baseline_commit: {baseline}",
            "status: GROUNDED",
            "authority_effect: none",
            "SUMMARY",
            "bounded bootstrap analysis",
            "FINDINGS",
            "[A1] classification=ALIGNED",
            "statement: current baseline is aligned",
            "rationale: bounded evidence",
            "evidence_refs: [R1]",
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

    engineering = SimpleNamespace(
        baseline_commit=baseline,
        repository_reader=reader,
        knowledge_reader=knowledge,
        kernels={
            "inspect": _Kernel(
                inspect,
                calls=calls,
                name="inspect",
                mutate_repo=repo if mutate_during_inspect else None,
            ),
            "analyze": _Kernel(analyze, calls=calls, name="analyze"),
            "propose": _Kernel(propose, calls=calls, name="propose"),
        },
    )
    return engineering, calls


def _ollama() -> OllamaRuntime:
    return OllamaRuntime(base_url="http://127.0.0.1:11434")


def _harness(
    repo: Path,
    engineering,
    *,
    runtime=None,
    model: str | None = "qwen3:8b",
    outputs: list[str] | None = None,
):
    return _module().InternalInteractionTestV0Harness(
        repository_root=repo,
        engineering=engineering,
        runtime=_ollama() if runtime is None else runtime,
        model=model,
        output_fn=(outputs.append if outputs is not None else lambda _: None),
    )


def _run(
    harness,
    *,
    run_id: str = "bootstrap-v0-001",
    refs: tuple[str, ...] = ("Validation#460",),
):
    return harness.run(
        run_id=run_id,
        external_validation_refs=refs,
        created_at=NOW,
    )


def test_harness_red_c01_task_and_scope_are_fixed_constants() -> None:
    module = _module()

    assert module.TASK_ID == "governed-self-review-bootstrap-v0"
    assert "U01 Core Kernel" in module.SCOPE
    assert "U04 Observability" in module.SCOPE
    assert "RR-03 Strong SecurityContext Provenance" in module.SCOPE
    assert "no-change is a valid outcome" in module.SCOPE
    assert "authority_effect=none" in module.SCOPE


def test_harness_red_c02_mock_runtime_is_rejected_before_run(
    tmp_path: Path,
) -> None:
    repo = _make_repo(tmp_path)
    engineering, calls = _engineering(repo)

    with pytest.raises(ValueError):
        _harness(
            repo,
            engineering,
            runtime=MockLLMRuntime(),
        )

    assert calls == []


def test_harness_red_c03_missing_model_is_rejected_before_run(
    tmp_path: Path,
) -> None:
    repo = _make_repo(tmp_path)
    engineering, calls = _engineering(repo)

    with pytest.raises(ValueError):
        _harness(repo, engineering, model=None)

    assert calls == []


def test_harness_red_c04_missing_repository_root_is_rejected() -> None:
    module = _module()

    with pytest.raises((TypeError, ValueError, RuntimeError)):
        module.InternalInteractionTestV0Harness(
            repository_root=None,
            engineering=object(),
            runtime=_ollama(),
            model="qwen3:8b",
        )


def test_harness_red_c05_missing_engineering_is_rejected(
    tmp_path: Path,
) -> None:
    repo = _make_repo(tmp_path)

    with pytest.raises((TypeError, ValueError)):
        _module().InternalInteractionTestV0Harness(
            repository_root=repo,
            engineering=None,
            runtime=_ollama(),
            model="qwen3:8b",
        )


@pytest.mark.parametrize("refs", [(), ("",), (" Validation#460",), ("Validation#460 ",)])
def test_harness_red_c06_invalid_validation_refs_stop_before_engineering(
    tmp_path: Path,
    refs: tuple[str, ...],
) -> None:
    repo = _make_repo(tmp_path)
    engineering, calls = _engineering(repo)
    harness = _harness(repo, engineering)

    with pytest.raises(ValueError):
        _run(harness, refs=refs)

    assert calls == []


@pytest.mark.parametrize(
    "run_id",
    [
        "../escape",
        "nested/run",
        "nested\\run",
        ".",
        "..",
        "",
        " run-001",
        "run-001 ",
    ],
)
def test_harness_red_c07_unsafe_run_id_stops_before_engineering(
    tmp_path: Path,
    run_id: str,
) -> None:
    repo = _make_repo(tmp_path)
    engineering, calls = _engineering(repo)
    harness = _harness(repo, engineering)

    with pytest.raises(ValueError):
        _run(harness, run_id=run_id)

    assert calls == []


def test_harness_red_c08_non_main_branch_stops_before_engineering(
    tmp_path: Path,
) -> None:
    repo = _make_repo(tmp_path, branch="feature/test")
    engineering, calls = _engineering(repo)

    with pytest.raises(RuntimeError):
        _run(_harness(repo, engineering))

    assert calls == []
    assert not (repo / "runtime" / "internal_interaction").exists()


def test_harness_red_c09_dirty_tracked_tree_stops_before_engineering(
    tmp_path: Path,
) -> None:
    repo = _make_repo(tmp_path, dirty_tracked=True)
    engineering, calls = _engineering(repo)

    with pytest.raises(RuntimeError):
        _run(_harness(repo, engineering))

    assert calls == []
    assert not (repo / "runtime" / "internal_interaction").exists()


def test_harness_red_c10_existing_run_stops_before_engineering(
    tmp_path: Path,
) -> None:
    repo = _make_repo(tmp_path)
    target = repo / "runtime" / "internal_interaction" / "bootstrap-v0-001"
    target.mkdir(parents=True)
    engineering, calls = _engineering(repo)

    with pytest.raises(FileExistsError):
        _run(_harness(repo, engineering))

    assert calls == []


def test_harness_red_c11_success_reuses_existing_engineering_and_fixed_scope(
    tmp_path: Path,
) -> None:
    repo = _make_repo(tmp_path)
    engineering, calls = _engineering(repo)

    result = _run(_harness(repo, engineering))

    assert [name for name, _ in calls] == ["inspect", "analyze"]
    assert {
        request.content
        for _, request in calls
    } == {_module().SCOPE}
    assert {
        request.session_id
        for _, request in calls
    } == {"bootstrap-v0-001"}

    assert result.internal_result.baseline_commit == engineering.baseline_commit
    assert result.internal_result.disposition.value == "NO_CHANGE_RECOMMENDED"
    assert result.authority_effect == "none"


def test_harness_red_c12_success_writes_and_validates_exact_artifact_set(
    tmp_path: Path,
) -> None:
    repo = _make_repo(tmp_path)
    engineering, _ = _engineering(repo)

    result = _run(_harness(repo, engineering))

    assert {item.name for item in result.internal_result.artifact_dir.iterdir()} == ARTIFACT_FILES

    _module().validate_internal_interaction_artifacts(
        result.internal_result.artifact_dir
    )

    evidence = json.loads(
        (result.internal_result.artifact_dir / "evidence.json").read_text(
            encoding="utf-8"
        )
    )
    assert evidence["external_validation_refs"] == ["Validation#460"]


def test_harness_red_c13_live_sink_receives_real_events_and_renders(
    tmp_path: Path,
) -> None:
    repo = _make_repo(tmp_path)
    engineering, _ = _engineering(repo)
    outputs: list[str] = []

    result = _run(_harness(repo, engineering, outputs=outputs))

    assert outputs
    assert any("MALAK INTERNAL INTERACTION - bootstrap-v0-001" in item for item in outputs)
    assert "[OK] STOP" in outputs[-1]
    assert result.live_projection.node("run").status == "COMPLETED"


def test_harness_red_c14_live_and_replay_are_materially_equal(
    tmp_path: Path,
) -> None:
    repo = _make_repo(tmp_path)
    engineering, _ = _engineering(repo)

    result = _run(_harness(repo, engineering))

    assert result.live_replay_equivalence is True
    assert result.live_projection == result.replay_projection
    assert result.acceptance == "PASS"


def test_harness_red_c15_replay_mismatch_is_inconclusive_not_reinterpreted(
    tmp_path: Path,
    monkeypatch,
) -> None:
    repo = _make_repo(tmp_path)
    engineering, _ = _engineering(repo)
    module = _module()

    monkeypatch.setattr(
        module,
        "load_trace_projection",
        lambda **_: import_module(
            "malak.observability.execution_trace_projection"
        ).ExecutionTraceProjection.empty(),
    )

    result = _run(_harness(repo, engineering))

    assert result.live_replay_equivalence is False
    assert result.acceptance == "INCONCLUSIVE"
    assert result.internal_result.disposition.value == "NO_CHANGE_RECOMMENDED"
    assert result.internal_result.artifact_dir.is_dir()
    assert result.authority_effect == "none"


def test_harness_red_c16_tracked_drift_after_run_is_inconclusive(
    tmp_path: Path,
) -> None:
    repo = _make_repo(tmp_path)
    engineering, _ = _engineering(
        repo,
        mutate_during_inspect=True,
    )

    result = _run(_harness(repo, engineering))

    assert result.tracked_tree_clean is False
    assert result.acceptance == "INCONCLUSIVE"
    assert result.internal_result.artifact_dir.is_dir()
    assert result.authority_effect == "none"


def test_harness_red_c17_clean_run_preserves_tracked_tree(
    tmp_path: Path,
) -> None:
    repo = _make_repo(tmp_path)
    engineering, _ = _engineering(repo)
    before = _git(repo, "status", "--porcelain", "--untracked-files=no")

    result = _run(_harness(repo, engineering))
    after = _git(repo, "status", "--porcelain", "--untracked-files=no")

    assert before == ""
    assert after == ""
    assert result.tracked_tree_clean is True
    assert result.acceptance == "PASS"


def test_harness_red_c18_summary_exposes_only_governed_run_metadata(
    tmp_path: Path,
) -> None:
    repo = _make_repo(tmp_path)
    engineering, _ = _engineering(repo)

    result = _run(_harness(repo, engineering))
    summary = result.summary()

    assert summary["run_id"] == "bootstrap-v0-001"
    assert summary["baseline_commit"] == engineering.baseline_commit
    assert summary["runtime"] == "OllamaRuntime"
    assert summary["model"] == "qwen3:8b"
    assert summary["terminal_disposition"] == "NO_CHANGE_RECOMMENDED"
    assert summary["live_replay_equivalence"] is True
    assert summary["authority_effect"] == "none"

    forbidden = {
        "prompt",
        "raw_model_request",
        "chain_of_thought",
        "component_outputs",
        "secrets",
    }
    assert forbidden.isdisjoint(summary)


def test_harness_red_c19_harness_exposes_no_arbitrary_task_or_scope_parameters(
    tmp_path: Path,
) -> None:
    repo = _make_repo(tmp_path)
    engineering, _ = _engineering(repo)
    harness = _harness(repo, engineering)

    with pytest.raises(TypeError):
        harness.run(
            run_id="bootstrap-v0-001",
            external_validation_refs=("Validation#460",),
            created_at=NOW,
            task_id="arbitrary",
        )

    with pytest.raises(TypeError):
        harness.run(
            run_id="bootstrap-v0-001",
            external_validation_refs=("Validation#460",),
            created_at=NOW,
            scope="arbitrary",
        )
