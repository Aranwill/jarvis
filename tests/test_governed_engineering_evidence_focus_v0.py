from __future__ import annotations

import dataclasses
import re
import subprocess
from importlib import import_module
from pathlib import Path

import pytest

from malak.infrastructure.repository_reader import GitRepositoryReader
from malak.knowledge.knowledge_reader import GovernedKnowledgeReader


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


def _make_repo(tmp_path: Path) -> tuple[Path, GitRepositoryReader, GovernedKnowledgeReader]:
    repo = tmp_path / "repo"
    repo.mkdir()

    _git(repo, "init")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Malak Test")
    _git(repo, "config", "commit.gpgsign", "false")

    _write(repo, "src/malak/kernel/kernel.py", "class Kernel:\n    pass\n")
    _write(repo, "src/malak/kernel/registry.py", "class CapabilityRegistry:\n    pass\n")
    _write(repo, "src/malak/services/planner.py", "class Planner:\n    pass\n")
    _write(repo, "tests/test_kernel.py", "def test_kernel():\n    assert 'Kernel'\n")
    _write(
        repo,
        "docs/architecture/blueprint.md",
        "Kernel First\nCapability First\n",
    )
    _write(
        repo,
        "docs/governance/cognitive_constitution.md",
        "Kernel evidence must remain bounded.\n",
    )
    _write(
        repo,
        "docs/governance/governance_constitution.md",
        "Evidence != Authority\n",
    )
    _write(
        repo,
        "docs/project/concepts/GOVERNED_SELF_REVIEW_BOOTSTRAP_TASK.md",
        "U01 Core Kernel\nU04 Observability\nRR-03 Strong SecurityContext Provenance\n",
    )
    _write(repo, ".gitignore", "/runtime/\n")

    _git(repo, "add", ".")
    _git(repo, "commit", "--no-gpg-sign", "-m", "baseline")

    reader = GitRepositoryReader(repo)
    return repo, reader, GovernedKnowledgeReader(reader)


def _module():
    return import_module("malak.capabilities._engineering_evidence")


def _selector(
    *,
    kind: str = "EXACT_PATH",
    value: str = "src/malak/kernel/kernel.py",
    terms: tuple[str, ...] = ("Kernel",),
    max_matches: int = 4,
):
    return _module().EvidenceSelector(
        kind=kind,
        value=value,
        terms=terms,
        max_matches=max_matches,
    )


def _focus(
    *,
    repository_selectors=None,
    knowledge_selectors=None,
    supplemental_terms: tuple[str, ...] = ("Capability",),
    supplemental_max_matches_per_kind: int = 2,
):
    return _module().GovernedEngineeringEvidenceFocus(
        focus_id="U01",
        focus_label="U01 Core Kernel",
        subject="Kernel",
        repository_required_selectors=(
            repository_selectors
            if repository_selectors is not None
            else (_selector(),)
        ),
        knowledge_required_selectors=(
            knowledge_selectors
            if knowledge_selectors is not None
            else (
                _selector(
                    value="docs/architecture/blueprint.md",
                    terms=("Kernel First",),
                ),
            )
        ),
        supplemental_terms=supplemental_terms,
        supplemental_max_matches_per_kind=supplemental_max_matches_per_kind,
        max_evidence_line_bytes=512,
        completeness_criteria="ALL_REQUIRED_SELECTORS_RESOLVED",
        authority_effect="none",
    )


def _collect(reader, knowledge, focus):
    return _module().collect_focused_engineering_evidence(
        repository_reader=reader,
        knowledge_reader=knowledge,
        focus=focus,
    )


def test_focus_red_f01_focus_contract_is_exact_and_immutable() -> None:
    focus = _focus()

    assert focus.focus_id == "U01"
    assert focus.subject == "Kernel"
    assert focus.completeness_criteria == "ALL_REQUIRED_SELECTORS_RESOLVED"
    assert focus.authority_effect == "none"

    with pytest.raises(dataclasses.FrozenInstanceError):
        focus.focus_id = "U04"


@pytest.mark.parametrize("kind", ["REGEX", "SEMANTIC", "GLOB", "MODEL_SELECTED"])
def test_focus_red_f02_unknown_selector_kind_is_rejected(kind: str) -> None:
    with pytest.raises(ValueError):
        _selector(kind=kind)


def test_focus_red_f03_duplicate_required_selector_is_rejected() -> None:
    selector = _selector()

    with pytest.raises(ValueError):
        _focus(repository_selectors=(selector, selector))


def test_focus_red_f04_authority_effect_cannot_be_elevated() -> None:
    module = _module()

    with pytest.raises(ValueError):
        module.GovernedEngineeringEvidenceFocus(
            focus_id="U01",
            focus_label="U01 Core Kernel",
            subject="Kernel",
            repository_required_selectors=(_selector(),),
            knowledge_required_selectors=(),
            supplemental_terms=(),
            supplemental_max_matches_per_kind=1,
            max_evidence_line_bytes=512,
            completeness_criteria="ALL_REQUIRED_SELECTORS_RESOLVED",
            authority_effect="write",
        )


def test_focus_red_f05_baseline_mismatch_fails_closed(tmp_path: Path) -> None:
    root_a = tmp_path / "a"
    root_b = tmp_path / "b"
    root_a.mkdir()
    root_b.mkdir()
    _, reader_a, _ = _make_repo(root_a)
    repo_b, _, _ = _make_repo(root_b)
    _write(repo_b, "extra.txt", "different baseline\n")
    _git(repo_b, "add", "extra.txt")
    _git(repo_b, "commit", "--no-gpg-sign", "-m", "different")
    reader_b = GitRepositoryReader(repo_b)
    knowledge_b = GovernedKnowledgeReader(reader_b)

    with pytest.raises(RuntimeError):
        _collect(reader_a, knowledge_b, _focus())


def test_focus_red_f06_missing_required_selector_is_incomplete(tmp_path: Path) -> None:
    _, reader, knowledge = _make_repo(tmp_path)
    focus = _focus(
        repository_selectors=(
            _selector(value="src/malak/kernel/missing.py"),
        )
    )

    bundle = _collect(reader, knowledge, focus)

    assert bundle.complete is False
    assert any(result.status == "MISSING" for result in bundle.selector_results)


def test_focus_red_f07_unreadable_required_selector_is_incomplete(tmp_path: Path) -> None:
    repo, _, _ = _make_repo(tmp_path)
    binary = repo / "src" / "malak" / "kernel" / "binary.bin"
    binary.write_bytes(b"\xff\xfe\xfd")
    _git(repo, "add", "src/malak/kernel/binary.bin")
    _git(repo, "commit", "--no-gpg-sign", "-m", "binary")
    reader = GitRepositoryReader(repo)
    knowledge = GovernedKnowledgeReader(reader)
    focus = _focus(
        repository_selectors=(
            _selector(
                value="src/malak/kernel/binary.bin",
                terms=("Kernel",),
            ),
        )
    )

    bundle = _collect(reader, knowledge, focus)

    assert bundle.complete is False
    assert any(result.status == "UNREADABLE" for result in bundle.selector_results)


def test_focus_red_f08_required_budget_overflow_is_incomplete(tmp_path: Path) -> None:
    repo, _, _ = _make_repo(tmp_path)
    _write(repo, "src/malak/kernel/a.py", "Kernel one\n")
    _write(repo, "src/malak/kernel/b.py", "Kernel two\n")
    _git(repo, "add", "src/malak/kernel/a.py", "src/malak/kernel/b.py")
    _git(repo, "commit", "--no-gpg-sign", "-m", "more kernel evidence")
    reader = GitRepositoryReader(repo)
    knowledge = GovernedKnowledgeReader(reader)
    focus = _focus(
        repository_selectors=(
            _selector(
                kind="PATH_PREFIX",
                value="src/malak/kernel/",
                terms=("Kernel",),
                max_matches=1,
            ),
        )
    )

    bundle = _collect(reader, knowledge, focus)

    assert bundle.complete is False
    assert any(result.status == "TRUNCATED" for result in bundle.selector_results)


def test_focus_red_f09_supplemental_truncation_is_visible_but_not_required(
    tmp_path: Path,
) -> None:
    repo, _, _ = _make_repo(tmp_path)
    _write(repo, "src/malak/extra_a.py", "SupplementalToken\n")
    _write(repo, "src/malak/extra_b.py", "SupplementalToken\n")
    _git(repo, "add", "src/malak/extra_a.py", "src/malak/extra_b.py")
    _git(repo, "commit", "--no-gpg-sign", "-m", "supplemental")
    reader = GitRepositoryReader(repo)
    knowledge = GovernedKnowledgeReader(reader)

    bundle = _collect(
        reader,
        knowledge,
        _focus(
            supplemental_terms=("SupplementalToken",),
            supplemental_max_matches_per_kind=1,
        ),
    )

    assert bundle.complete is True
    assert bundle.supplemental_truncated is True


def test_focus_red_f10_supplemental_evidence_cannot_heal_missing_required(
    tmp_path: Path,
) -> None:
    repo, reader, knowledge = _make_repo(tmp_path)
    _write(repo, "src/malak/supplemental.py", "MissingTarget\n")
    _git(repo, "add", "src/malak/supplemental.py")
    _git(repo, "commit", "--no-gpg-sign", "-m", "supplemental target")
    reader = GitRepositoryReader(repo)
    knowledge = GovernedKnowledgeReader(reader)

    bundle = _collect(
        reader,
        knowledge,
        _focus(
            repository_selectors=(
                _selector(value="src/malak/kernel/not-there.py"),
            ),
            supplemental_terms=("MissingTarget",),
        ),
    )

    assert bundle.complete is False
    assert bundle.repository_evidence


def test_focus_red_f11_evidence_set_digest_is_deterministic(tmp_path: Path) -> None:
    _, reader, knowledge = _make_repo(tmp_path)
    focus = _focus()

    first = _collect(reader, knowledge, focus)
    second = _collect(reader, knowledge, focus)

    assert first.evidence_set_digest == second.evidence_set_digest
    assert re.fullmatch(r"[0-9a-f]{64}", first.evidence_set_digest)


def test_focus_red_f12_bootstrap_catalog_has_three_independent_slices() -> None:
    focuses = _module().bootstrap_engineering_evidence_focuses()

    assert tuple(focus.focus_id for focus in focuses) == ("U01", "U04", "RR-03")
    assert len({focus.subject for focus in focuses}) == 3
    assert all(focus.authority_effect == "none" for focus in focuses)


def test_focus_green_catalog_preserves_required_context_sources() -> None:
    focuses = {
        focus.focus_id: focus
        for focus in _module().bootstrap_engineering_evidence_focuses()
    }

    u04_repository = {
        selector.value
        for selector in focuses["U04"].repository_required_selectors
    }
    rr03_repository = {
        selector.value
        for selector in focuses["RR-03"].repository_required_selectors
    }
    u04_knowledge = {
        selector.value
        for selector in focuses["U04"].knowledge_required_selectors
    }
    rr03_knowledge = {
        selector.value
        for selector in focuses["RR-03"].knowledge_required_selectors
    }

    observability_design = (
        "docs/project/sprints/proposals/"
        "MALAK-E2-STRUCTURAL-EVIDENCE-OBSERVABILITY-V0-G0-G1-DESIGN.md"
    )
    assert observability_design in u04_repository
    assert observability_design not in u04_knowledge

    assert "docs/project/sprints/SPRINT-7.7.md" in rr03_repository
    assert "docs/project/sprints/SPRINT-7.9.md" in rr03_repository
    assert "docs/project/sprints/SPRINT-7.7.md" not in rr03_knowledge
    assert "docs/project/sprints/SPRINT-7.9.md" not in rr03_knowledge


def test_focus_red_f13_inconclusive_slice_prevents_bootstrap_complete() -> None:
    summary = _module().evaluate_bootstrap_focus_completion(
        {
            "U01": "COMPLETE",
            "U04": "INCONCLUSIVE",
            "RR-03": "COMPLETE",
        }
    )

    assert summary.complete is False
    assert summary.states["U04"] == "INCONCLUSIVE"


@pytest.mark.parametrize("state", ["DEFERRED", "NOT_EXECUTED"])
def test_focus_red_f14_deferred_or_not_executed_prevents_bootstrap_complete(
    state: str,
) -> None:
    summary = _module().evaluate_bootstrap_focus_completion(
        {
            "U01": "COMPLETE",
            "U04": state,
            "RR-03": "COMPLETE",
        }
    )

    assert summary.complete is False


def test_focus_red_f15_existing_global_context_limit_is_not_increased() -> None:
    inspect = import_module("malak.capabilities.engineering_inspect")
    analyze = import_module("malak.capabilities.engineering_analyze")
    propose = import_module("malak.capabilities.engineering_propose")

    assert inspect._MAX_CONTEXT_MATCHES_PER_KIND == 12
    assert analyze._MAX_CONTEXT_MATCHES_PER_KIND == 12
    assert propose._MAX_CONTEXT_MATCHES_PER_KIND == 12


def test_focus_red_f16_generic_collector_contract_remains_available() -> None:
    module = _module()

    assert callable(module.collect_engineering_evidence)


def test_focus_red_f17_focus_contract_does_not_live_in_kernel_or_planner() -> None:
    kernel_module = import_module("malak.kernel.kernel")
    planner_module = import_module("malak.services.planner")

    assert not hasattr(kernel_module, "GovernedEngineeringEvidenceFocus")
    assert not hasattr(planner_module, "GovernedEngineeringEvidenceFocus")


def test_focus_red_f18_bundle_remains_authority_free(tmp_path: Path) -> None:
    _, reader, knowledge = _make_repo(tmp_path)

    bundle = _collect(reader, knowledge, _focus())

    assert bundle.authority_effect == "none"
