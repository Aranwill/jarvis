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


@pytest.mark.parametrize("query", ["\n", "needle\nsecond", "needle\rsecond"])
def test_e0_red_c24_multiline_search_query_is_rejected(
    tmp_path: Path,
    query: str,
) -> None:
    repo, _ = make_repo(tmp_path)
    reader = reader_class()(repo)

    with pytest.raises(ValueError):
        reader.search_text(query)


def test_e0_red_c25_unicode_and_space_paths_are_preserved(tmp_path: Path) -> None:
    repo, _ = make_repo(tmp_path)
    path = repo / "docs" / "dátá file.md"
    path.write_text("unicode needle\n", encoding="utf-8")
    git(repo, "add", "docs/dátá file.md")
    git(repo, "commit", "--no-gpg-sign", "-m", "unicode path")

    reader = reader_class()(repo)

    assert "docs/dátá file.md" in reader.list_tracked_files()
    assert reader.read_text("docs/dátá file.md").content == "unicode needle\n"


def test_e0_red_c26_utf8_with_nul_is_rejected_as_binary(tmp_path: Path) -> None:
    repo, _ = make_repo(tmp_path)
    (repo / "contains-nul.bin").write_bytes(b"valid\x00text")
    git(repo, "add", "contains-nul.bin")
    git(repo, "commit", "--no-gpg-sign", "-m", "nul")

    reader = reader_class()(repo)

    with pytest.raises(ValueError):
        reader.read_text("contains-nul.bin")

    result = reader.search_text("valid")
    assert all(match.path != "contains-nul.bin" for match in result.matches)


@pytest.mark.parametrize(
    ("kwargs",),
    [
        ({"max_text_bytes": (256 * 1024) + 1},),
        ({"max_search_results": 101},),
    ],
)
def test_e0_red_c27_hard_bounds_cannot_be_raised(
    tmp_path: Path,
    kwargs: dict[str, int],
) -> None:
    repo, _ = make_repo(tmp_path)

    with pytest.raises(ValueError):
        reader_class()(repo, **kwargs)


def test_e0_red_c28_git_environment_cannot_redirect_repository(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo, baseline = make_repo(tmp_path)

    other = tmp_path / "other"
    other.mkdir()
    git(other, "init")
    git(other, "config", "user.email", "test@example.com")
    git(other, "config", "user.name", "Malak Test")
    git(other, "config", "commit.gpgsign", "false")
    (other / "other.txt").write_text("other\n", encoding="utf-8")
    git(other, "add", "other.txt")
    git(other, "commit", "--no-gpg-sign", "-m", "other")

    monkeypatch.setenv("GIT_DIR", str(other / ".git"))
    monkeypatch.setenv("GIT_WORK_TREE", str(other))
    monkeypatch.setenv("GIT_INDEX_FILE", str(other / ".git" / "index"))

    reader = reader_class()(repo)

    assert reader.baseline_commit == baseline
    assert reader.list_tracked_files() == ("a.txt", "b.txt", "docs/c.md")


def test_e0_red_c29_replace_refs_cannot_change_blob_evidence(
    tmp_path: Path,
) -> None:
    repo, _ = make_repo(tmp_path)
    original_blob = git(repo, "rev-parse", "HEAD:a.txt")

    replacement = repo / "replacement.txt"
    replacement.write_text("omega\nneedle two\n", encoding="utf-8")
    replacement_blob = git(repo, "hash-object", "-w", "replacement.txt")
    git(repo, "replace", original_blob, replacement_blob)

    reader = reader_class()(repo)
    document = reader.read_text("a.txt")

    assert document.blob_sha == original_blob
    assert document.content == "alpha\nneedle one\n"


def test_e0_red_c30_tracked_blob_count_has_a_hard_snapshot_bound(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo, _ = make_repo(tmp_path)
    module = import_module("malak.infrastructure.repository_reader")
    monkeypatch.setattr(module, "_MAX_TRACKED_BLOBS", 2)

    with pytest.raises(RuntimeError):
        module.GitRepositoryReader(repo)


def test_e0_red_c31_searchable_snapshot_bytes_have_a_hard_bound(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo, _ = make_repo(tmp_path)
    module = import_module("malak.infrastructure.repository_reader")
    monkeypatch.setattr(module, "_MAX_SEARCHABLE_BYTES", 8)

    reader = module.GitRepositoryReader(repo)

    with pytest.raises(RuntimeError):
        reader.search_text("needle")


def test_e0_red_c32_blob_content_must_match_reported_blob_sha(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo, _ = make_repo(tmp_path)
    reader = reader_class()(repo)
    original_git_bytes = reader._git_bytes

    def tampered_git_bytes(*args: str) -> bytes:
        if args[:2] == ("cat-file", "blob"):
            return b"omega\nneedle two\n"
        return original_git_bytes(*args)

    monkeypatch.setattr(reader, "_git_bytes", tampered_git_bytes)

    with pytest.raises(RuntimeError):
        reader.read_text("a.txt")



@pytest.mark.parametrize("query", ["x" * 4097, "á" * 2049])
def test_e0_red_c33_search_query_has_a_hard_utf8_byte_bound(
    tmp_path: Path,
    query: str,
) -> None:
    repo, _ = make_repo(tmp_path)
    reader = reader_class()(repo)

    with pytest.raises(ValueError):
        reader.search_text(query)


def test_e0_red_c34_search_blob_reads_have_a_hard_bound(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo, _ = make_repo(tmp_path)
    module = import_module("malak.infrastructure.repository_reader")
    monkeypatch.setattr(module, "_MAX_SEARCH_BLOBS", 2)

    reader = module.GitRepositoryReader(repo)

    with pytest.raises(RuntimeError):
        reader.search_text("needle")


def test_e0_red_c35_search_output_bytes_are_bounded_and_signal_truncation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo, _ = make_repo(tmp_path)
    module = import_module("malak.infrastructure.repository_reader")
    monkeypatch.setattr(module, "_MAX_SEARCH_OUTPUT_BYTES", 10)

    reader = module.GitRepositoryReader(repo)
    result = reader.search_text("needle")

    assert [(match.path, match.line) for match in result.matches] == [
        ("a.txt", "needle one"),
    ]
    assert result.truncated is True


def test_e0_red_c36_git_environment_drops_untrusted_ambient_git_state(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = import_module("malak.infrastructure.repository_reader")
    monkeypatch.setenv("GIT_PREFIX", "redirect")
    monkeypatch.setenv("GIT_LITERAL_PATHSPECS", "1")
    monkeypatch.setenv("GIT_SSH_COMMAND", "unexpected-command")

    env = module._git_environment()

    assert "GIT_PREFIX" not in env
    assert "GIT_LITERAL_PATHSPECS" not in env
    assert "GIT_SSH_COMMAND" not in env
    assert env["GIT_CONFIG_NOSYSTEM"] == "1"
    assert env["GIT_NO_REPLACE_OBJECTS"] == "1"


@pytest.mark.parametrize("query", ["needle\x01", "\t"])
def test_e0_red_c37_search_query_rejects_control_characters(
    tmp_path: Path,
    query: str,
) -> None:
    repo, _ = make_repo(tmp_path)
    reader = reader_class()(repo)

    with pytest.raises(ValueError):
        reader.search_text(query)
