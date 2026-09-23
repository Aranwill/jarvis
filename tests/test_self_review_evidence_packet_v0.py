from __future__ import annotations

import subprocess
from importlib import import_module
from pathlib import Path

import pytest

from malak.infrastructure.repository_reader import GitRepositoryReader
from malak.knowledge.knowledge_reader import GovernedKnowledgeReader


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


def _module():
    return import_module("malak.services.self_review_evidence")


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


def _write_bytes(repo: Path, relative: str, content: bytes) -> None:
    path = repo / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)


def _make_repo(
    tmp_path: Path,
    *,
    omit: str | None = None,
    unreadable: str | None = None,
) -> tuple[Path, GitRepositoryReader, GovernedKnowledgeReader]:
    repo = tmp_path / "repo"
    repo.mkdir()

    _git(repo, "init")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Malak Test")
    _git(repo, "config", "commit.gpgsign", "false")

    for relative, text in REQUIRED_TEXT_FILES.items():
        if relative == omit:
            continue
        if relative == unreadable:
            _write_bytes(repo, relative, b"binary\x00content")
        else:
            _write(repo, relative, text)

    _write(
        repo,
        "docs/architecture/adr/ADR-001-accepted.md",
        "---\nid: ADR-001\nstatus: accepted\n---\naccepted one\n",
    )
    _write(
        repo,
        "docs/architecture/adr/ADR-002-accepted.md",
        "---\nid: ADR-002\nstatus: accepted\n---\naccepted two\n",
    )
    _write(
        repo,
        "docs/architecture/adr/ADR-099-proposed.md",
        "---\nid: ADR-099\nstatus: proposed\n---\nproposed\n",
    )
    _write(
        repo,
        "docs/project/concepts/README.md",
        "concept catalog\n",
    )
    _write(
        repo,
        "docs/project/concepts/EXTRA_CONCEPT.md",
        "extra concept\n",
    )
    _write(
        repo,
        "src/malak/example.py",
        "VALUE = 1\n",
    )
    _write(
        repo,
        "src/malak/nested/component.py",
        "VALUE = 2\n",
    )
    _write(
        repo,
        "tests/test_example.py",
        "def test_example():\n    assert True\n",
    )
    _write(
        repo,
        ".gitignore",
        "/runtime/\n",
    )

    _git(repo, "add", ".")
    _git(repo, "commit", "--no-gpg-sign", "-m", "baseline")

    repository_reader = GitRepositoryReader(repo)
    knowledge_reader = GovernedKnowledgeReader(repository_reader)
    return repo, repository_reader, knowledge_reader


def _build(
    repository_reader: GitRepositoryReader,
    knowledge_reader: GovernedKnowledgeReader,
    *,
    external_validation_refs: tuple[str, ...] = ("Validation#428",),
):
    return _module().build_self_review_evidence_packet(
        repository_reader=repository_reader,
        knowledge_reader=knowledge_reader,
        external_validation_refs=external_validation_refs,
    )


def _paths(values) -> set[str]:
    return {item.path for item in values}


def test_packet_red_c01_complete_packet_is_ready_and_authority_free(
    tmp_path: Path,
) -> None:
    _, repository_reader, knowledge_reader = _make_repo(tmp_path)

    packet = _build(repository_reader, knowledge_reader)

    assert packet.status == "READY"
    assert packet.authority_effect == "none"
    assert packet.missing_required_sources == ()
    assert packet.unreadable_required_sources == ()


def test_packet_red_c02_packet_is_bound_to_exact_repository_baseline(
    tmp_path: Path,
) -> None:
    _, repository_reader, knowledge_reader = _make_repo(tmp_path)

    packet = _build(repository_reader, knowledge_reader)

    assert packet.baseline_commit == repository_reader.baseline_commit
    assert packet.baseline_commit == knowledge_reader.baseline_commit


def test_packet_red_c03_missing_required_source_is_inconclusive_and_visible(
    tmp_path: Path,
) -> None:
    missing = "SECURITY.md"
    _, repository_reader, knowledge_reader = _make_repo(
        tmp_path,
        omit=missing,
    )

    packet = _build(repository_reader, knowledge_reader)

    assert packet.status == "INCONCLUSIVE"
    assert packet.missing_required_sources == (missing,)
    assert packet.authority_effect == "none"


def test_packet_red_c04_unreadable_required_source_is_inconclusive_and_visible(
    tmp_path: Path,
) -> None:
    unreadable = "AGENTS.md"
    _, repository_reader, knowledge_reader = _make_repo(
        tmp_path,
        unreadable=unreadable,
    )

    packet = _build(repository_reader, knowledge_reader)

    assert packet.status == "INCONCLUSIVE"
    assert packet.unreadable_required_sources == (unreadable,)
    assert packet.authority_effect == "none"


def test_packet_red_c05_missing_external_validation_reference_is_inconclusive(
    tmp_path: Path,
) -> None:
    _, repository_reader, knowledge_reader = _make_repo(tmp_path)

    packet = _build(
        repository_reader,
        knowledge_reader,
        external_validation_refs=(),
    )

    assert packet.status == "INCONCLUSIVE"
    assert packet.external_validation_refs == ()


def test_packet_red_c06_all_accepted_adrs_are_cataloged_without_proposed_adrs(
    tmp_path: Path,
) -> None:
    _, repository_reader, knowledge_reader = _make_repo(tmp_path)

    packet = _build(repository_reader, knowledge_reader)

    assert _paths(packet.accepted_adrs) == {
        "docs/architecture/adr/ADR-001-accepted.md",
        "docs/architecture/adr/ADR-002-accepted.md",
    }


def test_packet_red_c07_concepts_source_and_test_catalogs_are_explicit(
    tmp_path: Path,
) -> None:
    _, repository_reader, knowledge_reader = _make_repo(tmp_path)

    packet = _build(repository_reader, knowledge_reader)

    assert "docs/project/concepts/README.md" in packet.concept_paths
    assert "docs/project/concepts/EXTRA_CONCEPT.md" in packet.concept_paths
    assert "src/malak/example.py" in packet.source_paths
    assert "src/malak/nested/component.py" in packet.source_paths
    assert "tests/test_example.py" in packet.test_paths


def test_packet_red_c08_required_source_preserves_blob_and_document_role(
    tmp_path: Path,
) -> None:
    _, repository_reader, knowledge_reader = _make_repo(tmp_path)

    packet = _build(repository_reader, knowledge_reader)
    sources = {item.path: item for item in packet.required_sources}

    cognitive = sources["docs/governance/cognitive_constitution.md"]
    security = sources["SECURITY.md"]

    assert len(cognitive.blob_sha) == 40
    assert cognitive.source_class == "GOVERNING"
    assert cognitive.authority_class == "normative"

    assert len(security.blob_sha) == 40
    assert security.source_class == "SECURITY_POLICY"
    assert security.authority_class == "protected_subordinate"


@pytest.mark.parametrize(
    "external_validation_refs",
    [
        ("",),
        (" Validation#428",),
        ("Validation#428 ",),
    ],
)
def test_packet_red_c09_invalid_validation_reference_is_rejected(
    tmp_path: Path,
    external_validation_refs: tuple[str, ...],
) -> None:
    _, repository_reader, knowledge_reader = _make_repo(tmp_path)

    with pytest.raises(ValueError):
        _build(
            repository_reader,
            knowledge_reader,
            external_validation_refs=external_validation_refs,
        )
