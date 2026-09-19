from __future__ import annotations

import subprocess
from importlib import import_module
from pathlib import Path

import pytest

from malak.infrastructure.repository_reader import GitRepositoryReader


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

    write(repo, "AGENTS.md", "engineering method\nshared-token\n")
    write(repo, "SECURITY.md", "security policy\nshared-token\n")
    write(
        repo,
        "docs/governance/cognitive_constitution.md",
        "cognitive constitution\nshared-token\nbudget a\n",
    )
    write(
        repo,
        "docs/governance/governance_constitution.md",
        "governance constitution\nshared-token\nbudget b\n",
    )
    write(repo, "docs/governance/new_policy.md", "future policy\nshared-token\n")
    write(repo, "docs/architecture/blueprint.md", "blueprint\nshared-token\n")
    write(repo, "docs/architecture/kernel.md", "kernel reference\nshared-token\n")
    write(
        repo,
        "docs/architecture/schemas/knowledge_schema.yaml",
        "schema: knowledge\nshared-token: true\n",
    )
    write(
        repo,
        "docs/architecture/adr/ADR-007-example.md",
        "---\nstatus: proposed\n---\n# ADR-007\nshared-token\n",
    )
    write(
        repo,
        "docs/architecture/adr/ADR-TEMPLATE.md",
        "---\nstatus: proposed\n---\n# ADR-000 Template\nshared-token\n",
    )
    write(
        repo,
        "docs/development/engineering_method.md",
        "engineering method detail\nshared-token\n",
    )
    write(
        repo,
        "docs/knowledge/standards/STD-001.md",
        "curated standard\nshared-token\n",
    )
    write(
        repo,
        "docs/knowledge/templates/ARTIFACT_TEMPLATE.md",
        "template only\nshared-token\n",
    )
    write(
        repo,
        "docs/project/implementation_roadmap.md",
        "derived roadmap\nshared-token\n",
    )
    write(repo, "docs/project/project_context.md", "derived context\nshared-token\n")
    write(repo, "docs/project/status/CURRENT.md", "derived status\nshared-token\n")
    write(
        repo,
        "documents/projects/jarvis/ideas.md",
        "non normative idea\nshared-token\n",
    )
    write(
        repo,
        "docs/project/concepts/README.md",
        "non normative concept\nshared-token\n",
    )
    write(
        repo,
        "src/malak/example.py",
        'VALUE = "shared-token code-only-token"\n',
    )

    git(repo, "add", ".")
    git(repo, "commit", "--no-gpg-sign", "-m", "baseline")

    return repo, git(repo, "rev-parse", "HEAD")


def knowledge_module():
    return import_module("malak.knowledge.knowledge_reader")


def make_reader(tmp_path: Path):
    repo, baseline = make_repo(tmp_path)
    repository_reader = GitRepositoryReader(repo)
    reader = knowledge_module().GovernedKnowledgeReader(repository_reader)
    return repo, baseline, repository_reader, reader


def source_rows(reader) -> list[tuple[str, str, str]]:
    return [
        (source.path, source.source_class, source.authority_class)
        for source in reader.list_sources()
    ]


def test_e1_red_c01_baseline_is_inherited_from_e0(tmp_path: Path) -> None:
    _, baseline, repository_reader, reader = make_reader(tmp_path)

    assert reader.baseline_commit == baseline
    assert reader.baseline_commit == repository_reader.baseline_commit


def test_e1_red_c02_source_catalog_is_exact_and_deterministic(tmp_path: Path) -> None:
    _, _, _, reader = make_reader(tmp_path)

    assert source_rows(reader) == [
        ("AGENTS.md", "ENGINEERING_METHOD", "process_reference"),
        ("SECURITY.md", "SECURITY_POLICY", "protected_subordinate"),
        (
            "docs/architecture/adr/ADR-007-example.md",
            "DECISION_RECORD",
            "status_dependent",
        ),
        ("docs/architecture/blueprint.md", "GOVERNING", "normative"),
        (
            "docs/architecture/kernel.md",
            "ARCHITECTURE_REFERENCE",
            "reference",
        ),
        (
            "docs/architecture/schemas/knowledge_schema.yaml",
            "ARCHITECTURE_REFERENCE",
            "reference",
        ),
        (
            "docs/development/engineering_method.md",
            "ENGINEERING_METHOD",
            "process_reference",
        ),
        (
            "docs/governance/cognitive_constitution.md",
            "GOVERNING",
            "normative",
        ),
        (
            "docs/governance/governance_constitution.md",
            "GOVERNING",
            "normative",
        ),
        (
            "docs/knowledge/standards/STD-001.md",
            "CURATED_KNOWLEDGE",
            "curated_reference",
        ),
        (
            "docs/project/concepts/README.md",
            "NON_NORMATIVE_CONCEPT",
            "non_normative",
        ),
        (
            "docs/project/implementation_roadmap.md",
            "DERIVED_STATE",
            "derived",
        ),
        ("docs/project/project_context.md", "DERIVED_STATE", "derived"),
        ("docs/project/status/CURRENT.md", "DERIVED_STATE", "derived"),
        (
            "documents/projects/jarvis/ideas.md",
            "NON_NORMATIVE_IDEA",
            "non_normative",
        ),
    ]


def test_e1_red_c03_templates_and_unknown_governance_are_not_sources(
    tmp_path: Path,
) -> None:
    _, _, _, reader = make_reader(tmp_path)
    paths = {source.path for source in reader.list_sources()}

    assert "docs/architecture/adr/ADR-TEMPLATE.md" not in paths
    assert "docs/knowledge/templates/ARTIFACT_TEMPLATE.md" not in paths
    assert "docs/governance/new_policy.md" not in paths


def test_e1_red_c04_source_code_is_not_knowledge(tmp_path: Path) -> None:
    _, _, _, reader = make_reader(tmp_path)

    assert "src/malak/example.py" not in {
        source.path for source in reader.list_sources()
    }


def test_e1_red_c05_list_sources_does_not_read_content(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, _, repository_reader, reader = make_reader(tmp_path)

    def forbidden_read(_: str):
        raise AssertionError("list_sources must not read content")

    monkeypatch.setattr(repository_reader, "read_text", forbidden_read)

    assert reader.list_sources()


def test_e1_red_c06_read_preserves_repository_provenance_and_classification(
    tmp_path: Path,
) -> None:
    _, baseline, _, reader = make_reader(tmp_path)

    document = reader.read("docs/governance/cognitive_constitution.md")

    assert document.baseline_commit == baseline
    assert document.path == "docs/governance/cognitive_constitution.md"
    assert len(document.blob_sha) == 40
    assert document.source_class == "GOVERNING"
    assert document.authority_class == "normative"
    assert document.content.startswith("cognitive constitution")


def test_e1_red_c07_unknown_source_read_fails_closed(tmp_path: Path) -> None:
    _, _, _, reader = make_reader(tmp_path)

    with pytest.raises(ValueError):
        reader.read("src/malak/example.py")


@pytest.mark.parametrize(
    "path",
    [
        "docs/architecture/adr/ADR-TEMPLATE.md",
        "docs/knowledge/templates/ARTIFACT_TEMPLATE.md",
        "docs/governance/new_policy.md",
    ],
)
def test_e1_red_c08_explicitly_excluded_or_unknown_source_read_is_rejected(
    tmp_path: Path,
    path: str,
) -> None:
    _, _, _, reader = make_reader(tmp_path)

    with pytest.raises(ValueError):
        reader.read(path)


def test_e1_red_c09_working_tree_mutation_remains_invisible(tmp_path: Path) -> None:
    repo, _, _, reader = make_reader(tmp_path)
    path = repo / "SECURITY.md"
    path.write_text("working tree mutation\n", encoding="utf-8")

    assert reader.read("SECURITY.md").content == "security policy\nshared-token\n"


def test_e1_red_c10_search_only_reads_classified_sources(tmp_path: Path) -> None:
    _, _, _, reader = make_reader(tmp_path)

    result = reader.search_text("code-only-token")

    assert result.matches == ()
    assert result.truncated is False


def test_e1_red_c11_search_returns_source_and_authority_provenance(
    tmp_path: Path,
) -> None:
    _, baseline, _, reader = make_reader(tmp_path)

    result = reader.search_text("shared-token")

    assert result.baseline_commit == baseline
    assert result.matches
    assert all(match.baseline_commit == baseline for match in result.matches)
    assert all(len(match.blob_sha) == 40 for match in result.matches)
    assert all(match.source_class for match in result.matches)
    assert all(match.authority_class for match in result.matches)
    assert all(not match.path.startswith("src/") for match in result.matches)


def test_e1_red_c12_search_order_is_deterministic(tmp_path: Path) -> None:
    _, _, _, reader = make_reader(tmp_path)

    result = reader.search_text("budget")

    assert [(m.path, m.line_number, m.line) for m in result.matches] == [
        ("docs/governance/cognitive_constitution.md", 3, "budget a"),
        ("docs/governance/governance_constitution.md", 3, "budget b"),
    ]


@pytest.mark.parametrize("query", ["", "\n", "shared\nsecond", "\t", "x\x01"])
def test_e1_red_c13_invalid_query_is_rejected(
    tmp_path: Path,
    query: str,
) -> None:
    _, _, _, reader = make_reader(tmp_path)

    with pytest.raises(ValueError):
        reader.search_text(query)


@pytest.mark.parametrize("query", ["x" * 4097, "á" * 2049])
def test_e1_red_c14_query_has_a_hard_utf8_byte_bound(
    tmp_path: Path,
    query: str,
) -> None:
    _, _, _, reader = make_reader(tmp_path)

    with pytest.raises(ValueError):
        reader.search_text(query)


def test_e1_red_c15_source_count_has_a_hard_bound(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo, _ = make_repo(tmp_path)
    module = knowledge_module()
    monkeypatch.setattr(module, "_MAX_KNOWLEDGE_SOURCES", 2)

    with pytest.raises(RuntimeError):
        module.GovernedKnowledgeReader(GitRepositoryReader(repo))


def test_e1_red_c16_searchable_bytes_have_a_hard_bound(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, _, _, reader = make_reader(tmp_path)
    module = knowledge_module()
    monkeypatch.setattr(module, "_MAX_SEARCHABLE_BYTES", 8)

    with pytest.raises(RuntimeError):
        reader.search_text("shared-token")


def test_e1_red_c17_search_result_count_is_bounded_and_signals_truncation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, _, _, reader = make_reader(tmp_path)
    module = knowledge_module()
    monkeypatch.setattr(module, "_MAX_SEARCH_RESULTS", 2)

    result = reader.search_text("shared-token")

    assert len(result.matches) == 2
    assert result.truncated is True


def test_e1_red_c18_search_output_bytes_are_bounded_and_signal_truncation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, _, _, reader = make_reader(tmp_path)
    module = knowledge_module()
    monkeypatch.setattr(module, "_MAX_SEARCH_OUTPUT_BYTES", 8)

    result = reader.search_text("budget")

    assert [(m.path, m.line) for m in result.matches] == [
        ("docs/governance/cognitive_constitution.md", "budget a"),
    ]
    assert result.truncated is True


def test_e1_red_c19_binary_recognized_source_fails_search_explicitly(
    tmp_path: Path,
) -> None:
    repo, _ = make_repo(tmp_path)
    path = repo / "docs" / "project" / "concepts" / "BINARY.md"
    path.write_bytes(b"\xff\xfe\xfd")
    git(repo, "add", "docs/project/concepts/BINARY.md")
    git(repo, "commit", "--no-gpg-sign", "-m", "binary knowledge")

    reader = knowledge_module().GovernedKnowledgeReader(GitRepositoryReader(repo))

    with pytest.raises(ValueError):
        reader.search_text("shared-token")


def test_e1_red_c20_new_unknown_path_does_not_gain_implicit_classification(
    tmp_path: Path,
) -> None:
    repo, _ = make_repo(tmp_path)
    write(repo, "docs/project/new-governed-source.md", "shared-token\n")
    git(repo, "add", "docs/project/new-governed-source.md")
    git(repo, "commit", "--no-gpg-sign", "-m", "unknown source")

    reader = knowledge_module().GovernedKnowledgeReader(GitRepositoryReader(repo))

    assert "docs/project/new-governed-source.md" not in {
        source.path for source in reader.list_sources()
    }
    with pytest.raises(ValueError):
        reader.read("docs/project/new-governed-source.md")


def test_e1_red_c21_adr_status_is_not_inferred_as_accepted(tmp_path: Path) -> None:
    _, _, _, reader = make_reader(tmp_path)

    document = reader.read("docs/architecture/adr/ADR-007-example.md")

    assert document.source_class == "DECISION_RECORD"
    assert document.authority_class == "status_dependent"
    assert "status: proposed" in document.content


def test_e1_red_c22_search_fails_if_recognized_source_exceeds_e0_text_bound(
    tmp_path: Path,
) -> None:
    repo, _ = make_repo(tmp_path)
    path = repo / "docs" / "project" / "concepts" / "HUGE.md"
    path.write_text("x" * ((256 * 1024) + 1), encoding="utf-8")
    git(repo, "add", "docs/project/concepts/HUGE.md")
    git(repo, "commit", "--no-gpg-sign", "-m", "oversized knowledge")

    reader = knowledge_module().GovernedKnowledgeReader(GitRepositoryReader(repo))

    with pytest.raises(ValueError):
        reader.search_text("shared-token")


def test_e1_red_c23_read_of_valid_source_propagates_e0_text_failure(
    tmp_path: Path,
) -> None:
    repo, _ = make_repo(tmp_path)
    path = repo / "docs" / "project" / "concepts" / "BINARY.md"
    path.write_bytes(b"\xff\xfe\xfd")
    git(repo, "add", "docs/project/concepts/BINARY.md")
    git(repo, "commit", "--no-gpg-sign", "-m", "binary knowledge")

    reader = knowledge_module().GovernedKnowledgeReader(GitRepositoryReader(repo))

    with pytest.raises(ValueError):
        reader.read("docs/project/concepts/BINARY.md")



def test_e1_red_c24_truncation_cannot_hide_later_unreadable_source(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo, _ = make_repo(tmp_path)
    path = repo / "docs" / "project" / "concepts" / "ZZZ-BINARY.md"
    path.write_bytes(b"\xff\xfe\xfd")
    git(repo, "add", "docs/project/concepts/ZZZ-BINARY.md")
    git(repo, "commit", "--no-gpg-sign", "-m", "late binary knowledge")

    module = knowledge_module()
    monkeypatch.setattr(module, "_MAX_SEARCH_RESULTS", 1)
    reader = module.GovernedKnowledgeReader(GitRepositoryReader(repo))

    with pytest.raises(ValueError):
        reader.search_text("shared-token")


def test_e1_red_c25_read_rejects_non_string_path_explicitly(tmp_path: Path) -> None:
    _, _, _, reader = make_reader(tmp_path)

    with pytest.raises(TypeError):
        reader.read(123)  # type: ignore[arg-type]
