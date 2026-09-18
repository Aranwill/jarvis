from __future__ import annotations

import subprocess
from importlib import import_module
from pathlib import Path

import pytest


def git(repo: Path, *args: str) -> str:
    done = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return done.stdout.strip()


def make_repo(tmp_path: Path) -> tuple[Path, str]:
    repo = tmp_path / "repo"
    repo.mkdir()

    git(repo, "init")
    git(repo, "config", "user.email", "test@example.com")
    git(repo, "config", "user.name", "Malak Test")
    git(repo, "config", "commit.gpgsign", "false")

    (repo / "a.txt").write_text("alpha\nneedle one\n", encoding="utf-8")
    (repo / "b.txt").write_text("beta\nneedle two\n", encoding="utf-8")
    nested = repo / "docs"
    nested.mkdir()
    (nested / "c.md").write_text("gamma\nneedle three\n", encoding="utf-8")

    git(repo, "add", "a.txt", "b.txt", "docs/c.md")
    git(repo, "commit", "--no-gpg-sign", "-m", "baseline")

    return repo, git(repo, "rev-parse", "HEAD")


def reader_class():
    module = import_module("malak.infrastructure.repository_reader")
    return module.GitRepositoryReader


def test_e0_red_c01_reader_captures_exact_head(tmp_path: Path) -> None:
    repo, baseline = make_repo(tmp_path)

    reader = reader_class()(repo)

    assert reader.baseline_commit == baseline


def test_e0_red_c02_list_tracked_files_is_deterministic_and_snapshot_bound(
    tmp_path: Path,
) -> None:
    repo, _ = make_repo(tmp_path)
    (repo / "untracked.txt").write_text("hidden\n", encoding="utf-8")

    reader = reader_class()(repo)

    assert reader.list_tracked_files() == ("a.txt", "b.txt", "docs/c.md")


def test_e0_red_c03_read_text_returns_committed_content_with_provenance(
    tmp_path: Path,
) -> None:
    repo, baseline = make_repo(tmp_path)
    reader = reader_class()(repo)

    document = reader.read_text("a.txt")

    assert document.baseline_commit == baseline
    assert document.path == "a.txt"
    assert len(document.blob_sha) == 40
    assert document.content == "alpha\nneedle one\n"


def test_e0_red_c04_working_tree_modification_is_invisible(tmp_path: Path) -> None:
    repo, _ = make_repo(tmp_path)
    reader = reader_class()(repo)

    (repo / "a.txt").write_text("working tree mutation\n", encoding="utf-8")

    assert reader.read_text("a.txt").content == "alpha\nneedle one\n"


def test_e0_red_c05_staged_uncommitted_modification_is_invisible(
    tmp_path: Path,
) -> None:
    repo, _ = make_repo(tmp_path)
    reader = reader_class()(repo)

    (repo / "a.txt").write_text("staged mutation\n", encoding="utf-8")
    git(repo, "add", "a.txt")

    assert reader.read_text("a.txt").content == "alpha\nneedle one\n"


def test_e0_red_c06_reader_remains_bound_when_head_advances(tmp_path: Path) -> None:
    repo, baseline = make_repo(tmp_path)
    reader = reader_class()(repo)

    (repo / "a.txt").write_text("second commit\n", encoding="utf-8")
    git(repo, "add", "a.txt")
    git(repo, "commit", "--no-gpg-sign", "-m", "second")

    assert git(repo, "rev-parse", "HEAD") != baseline
    assert reader.baseline_commit == baseline
    assert reader.read_text("a.txt").content == "alpha\nneedle one\n"


def test_e0_red_c07_absolute_path_is_rejected(tmp_path: Path) -> None:
    repo, _ = make_repo(tmp_path)
    reader = reader_class()(repo)

    with pytest.raises(ValueError):
        reader.read_text("/etc/passwd")


def test_e0_red_c08_parent_traversal_is_rejected(tmp_path: Path) -> None:
    repo, _ = make_repo(tmp_path)
    reader = reader_class()(repo)

    with pytest.raises(ValueError):
        reader.read_text("../outside.txt")


def test_e0_red_c09_untracked_path_is_not_readable(tmp_path: Path) -> None:
    repo, _ = make_repo(tmp_path)
    (repo / "untracked.txt").write_text("untracked\n", encoding="utf-8")
    reader = reader_class()(repo)

    with pytest.raises(FileNotFoundError):
        reader.read_text("untracked.txt")


def test_e0_red_c10_oversized_text_is_rejected(tmp_path: Path) -> None:
    repo, _ = make_repo(tmp_path)
    reader = reader_class()(repo, max_text_bytes=8)

    with pytest.raises(ValueError):
        reader.read_text("a.txt")


def test_e0_red_c11_non_utf8_content_is_rejected(tmp_path: Path) -> None:
    repo, _ = make_repo(tmp_path)
    (repo / "binary.bin").write_bytes(b"\xff\xfe\xfd")
    git(repo, "add", "binary.bin")
    git(repo, "commit", "--no-gpg-sign", "-m", "binary")

    reader = reader_class()(repo)

    with pytest.raises(ValueError):
        reader.read_text("binary.bin")


def test_e0_red_c12_search_returns_literal_matches_with_provenance(
    tmp_path: Path,
) -> None:
    repo, baseline = make_repo(tmp_path)
    reader = reader_class()(repo)

    result = reader.search_text("needle")

    assert result.baseline_commit == baseline
    assert result.truncated is False
    assert [
        (match.path, match.line_number, match.line)
        for match in result.matches
    ] == [
        ("a.txt", 2, "needle one"),
        ("b.txt", 2, "needle two"),
        ("docs/c.md", 2, "needle three"),
    ]
    assert all(len(match.blob_sha) == 40 for match in result.matches)


def test_e0_red_c13_search_ignores_working_tree_mutation(tmp_path: Path) -> None:
    repo, _ = make_repo(tmp_path)
    reader = reader_class()(repo)

    (repo / "a.txt").write_text("new-only-token\n", encoding="utf-8")

    result = reader.search_text("new-only-token")

    assert result.matches == ()
    assert result.truncated is False


def test_e0_red_c14_search_result_limit_sets_truncated(tmp_path: Path) -> None:
    repo, _ = make_repo(tmp_path)
    reader = reader_class()(repo, max_search_results=2)

    result = reader.search_text("needle")

    assert len(result.matches) == 2
    assert result.truncated is True


def test_e0_red_c15_empty_search_query_is_rejected(tmp_path: Path) -> None:
    repo, _ = make_repo(tmp_path)
    reader = reader_class()(repo)

    with pytest.raises(ValueError):
        reader.search_text("")


def test_e0_red_c16_non_git_directory_fails_explicitly(tmp_path: Path) -> None:
    repo = tmp_path / "not-a-repository"
    repo.mkdir()

    with pytest.raises(RuntimeError):
        reader_class()(repo)


def test_e0_red_c17_repository_root_must_be_exact_git_toplevel(
    tmp_path: Path,
) -> None:
    repo, _ = make_repo(tmp_path)

    with pytest.raises(ValueError):
        reader_class()(repo / "docs")


def test_e0_red_c18_backslash_path_is_rejected_as_ambiguous(
    tmp_path: Path,
) -> None:
    repo, _ = make_repo(tmp_path)
    reader = reader_class()(repo)

    with pytest.raises(ValueError):
        reader.read_text("docs\\c.md")


def test_e0_red_c19_noncanonical_path_is_rejected(tmp_path: Path) -> None:
    repo, _ = make_repo(tmp_path)
    reader = reader_class()(repo)

    with pytest.raises(ValueError):
        reader.read_text("docs/./c.md")


@pytest.mark.parametrize(
    ("kwargs",),
    [
        ({"max_text_bytes": 0},),
        ({"max_text_bytes": -1},),
        ({"max_search_results": 0},),
        ({"max_search_results": -1},),
    ],
)
def test_e0_red_c20_nonpositive_limits_are_rejected(
    tmp_path: Path,
    kwargs: dict[str, int],
) -> None:
    repo, _ = make_repo(tmp_path)

    with pytest.raises(ValueError):
        reader_class()(repo, **kwargs)


def test_e0_red_c21_search_skips_non_utf8_blob(tmp_path: Path) -> None:
    repo, _ = make_repo(tmp_path)
    (repo / "binary.bin").write_bytes(b"\xff\xfe\xfdneedle")
    git(repo, "add", "binary.bin")
    git(repo, "commit", "--no-gpg-sign", "-m", "binary")

    reader = reader_class()(repo)
    result = reader.search_text("needle")

    assert [match.path for match in result.matches] == [
        "a.txt",
        "b.txt",
        "docs/c.md",
    ]


def test_e0_red_c22_search_skips_oversized_blob(tmp_path: Path) -> None:
    repo, _ = make_repo(tmp_path)
    (repo / "small.txt").write_text("needle\n", encoding="utf-8")
    (repo / "large.txt").write_text("needle too large\n", encoding="utf-8")
    git(repo, "add", "small.txt", "large.txt")
    git(repo, "commit", "--no-gpg-sign", "-m", "sizes")

    reader = reader_class()(repo, max_text_bytes=8)
    result = reader.search_text("needle")

    assert [match.path for match in result.matches] == ["small.txt"]
    assert result.truncated is False


def test_e0_red_c23_symlink_blob_is_not_interpreted_as_text_document(
    tmp_path: Path,
) -> None:
    repo, _ = make_repo(tmp_path)
    (repo / "target.txt").write_text("target secret\n", encoding="utf-8")
    (repo / "link").write_text("target.txt", encoding="utf-8")
    git(repo, "add", "target.txt", "link")
    blob_sha = git(repo, "hash-object", "link")
    git(repo, "update-index", "--add", "--cacheinfo", f"120000,{blob_sha},link")
    git(repo, "commit", "--no-gpg-sign", "-m", "symlink-mode")

    reader = reader_class()(repo)

    assert "link" in reader.list_tracked_files()
    with pytest.raises(ValueError):
        reader.read_text("link")

    result = reader.search_text("target.txt")
    assert all(match.path != "link" for match in result.matches)
