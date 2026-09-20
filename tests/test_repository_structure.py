from __future__ import annotations

import subprocess
from importlib import import_module
from pathlib import Path

import pytest


HARD_MAX_PYTHON_FILES = 256
HARD_MAX_PYTHON_BYTES = 4 * 1024 * 1024
HARD_MAX_SYMBOLS = 8192
HARD_MAX_IMPORTS = 8192


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
    (repo / "src" / "malak" / "pkg").mkdir(parents=True)
    (repo / "tests").mkdir()

    git(repo, "init")
    git(repo, "config", "user.email", "test@example.com")
    git(repo, "config", "user.name", "Malak Test")
    git(repo, "config", "commit.gpgsign", "false")

    (repo / "src" / "malak" / "__init__.py").write_text("", encoding="utf-8")
    (repo / "src" / "malak" / "pkg" / "__init__.py").write_text("", encoding="utf-8")
    (repo / "src" / "malak" / "pkg" / "helper.py").write_text(
        "VALUE = 1\n\ndef thing():\n    return VALUE\n",
        encoding="utf-8",
    )
    (repo / "src" / "malak" / "pkg" / "sample.py").write_text(
        "import os as operating_system\n"
        "from malak.services import planner as planner_module\n"
        "from .helper import thing\n\n"
        "class Example:\n"
        "    def method(self):\n"
        "        return thing()\n\n"
        "    async def async_method(self):\n"
        "        return 1\n\n"
        "def top_level():\n"
        "    return operating_system.name\n\n"
        "async def async_top_level():\n"
        "    return 1\n",
        encoding="utf-8",
    )
    (repo / "tests" / "test_sample.py").write_text(
        "from malak.pkg.sample import Example\n",
        encoding="utf-8",
    )
    (repo / "README.md").write_text("not python\n", encoding="utf-8")

    git(repo, "add", ".")
    git(repo, "commit", "--no-gpg-sign", "-m", "baseline")
    return repo, git(repo, "rev-parse", "HEAD")


def reader_class():
    return import_module("malak.infrastructure.repository_reader").GitRepositoryReader


def structure_module():
    return import_module("malak.infrastructure.repository_structure")


def projector_class():
    return structure_module().RepositoryStructuralProjector


def test_rspv0_red_c01_expected_module_and_projector_do_not_exist_yet() -> None:
    # RED must fail here until GREEN introduces the admitted primitive.
    module = structure_module()
    assert hasattr(module, "RepositoryStructuralProjector")


def test_rspv0_red_c02_projection_is_baseline_bound_and_deterministic(
    tmp_path: Path,
) -> None:
    repo, baseline = make_repo(tmp_path)
    reader = reader_class()(repo)

    first = projector_class()(reader).project()
    second = projector_class()(reader).project()

    assert first.baseline_commit == baseline
    assert first == second
    assert first.projection_digest == second.projection_digest
    assert len(first.projection_digest) == 64


def test_rspv0_red_c03_projection_ignores_worktree_staged_and_untracked(
    tmp_path: Path,
) -> None:
    repo, _ = make_repo(tmp_path)
    reader = reader_class()(repo)
    baseline = projector_class()(reader).project()

    sample = repo / "src" / "malak" / "pkg" / "sample.py"
    sample.write_text("class WorkingTreeOnly:\n    pass\n", encoding="utf-8")
    git(repo, "add", "src/malak/pkg/sample.py")
    (repo / "src" / "malak" / "pkg" / "untracked.py").write_text(
        "class Untracked:\n    pass\n",
        encoding="utf-8",
    )

    assert projector_class()(reader).project() == baseline


def test_rspv0_red_c04_captured_reader_does_not_move_when_head_advances(
    tmp_path: Path,
) -> None:
    repo, baseline = make_repo(tmp_path)
    reader = reader_class()(repo)
    before = projector_class()(reader).project()

    sample = repo / "src" / "malak" / "pkg" / "sample.py"
    sample.write_text("class NewHeadOnly:\n    pass\n", encoding="utf-8")
    git(repo, "add", "src/malak/pkg/sample.py")
    git(repo, "commit", "--no-gpg-sign", "-m", "advance")

    assert git(repo, "rev-parse", "HEAD") != baseline
    assert projector_class()(reader).project() == before


def test_rspv0_red_c05_symbol_facts_are_exact_and_qualified(tmp_path: Path) -> None:
    repo, baseline = make_repo(tmp_path)
    projection = projector_class()(reader_class()(repo)).project()

    observed = {
        (fact.module_name, fact.qualified_name, fact.kind, fact.line_number)
        for fact in projection.symbols
        if fact.path == "src/malak/pkg/sample.py"
    }

    assert ("malak.pkg.sample", "malak.pkg.sample.Example", "CLASS", 5) in observed
    assert ("malak.pkg.sample", "malak.pkg.sample.Example.method", "METHOD", 6) in observed
    assert (
        "malak.pkg.sample",
        "malak.pkg.sample.Example.async_method",
        "ASYNC_METHOD",
        9,
    ) in observed
    assert ("malak.pkg.sample", "malak.pkg.sample.top_level", "FUNCTION", 12) in observed
    assert (
        "malak.pkg.sample",
        "malak.pkg.sample.async_top_level",
        "ASYNC_FUNCTION",
        15,
    ) in observed

    assert all(fact.baseline_commit == baseline for fact in projection.symbols)
    assert all(len(fact.blob_sha) == 40 for fact in projection.symbols)


def test_rspv0_red_c06_import_facts_preserve_syntax_without_semantic_inference(
    tmp_path: Path,
) -> None:
    repo, _ = make_repo(tmp_path)
    projection = projector_class()(reader_class()(repo)).project()

    imports = [
        fact for fact in projection.imports
        if fact.path == "src/malak/pkg/sample.py"
    ]
    observed = {
        (
            fact.source_module,
            fact.target_module,
            fact.imported_name,
            fact.relative_level,
        )
        for fact in imports
    }

    assert ("malak.pkg.sample", "os", None, 0) in observed
    assert ("malak.pkg.sample", "malak.services", "planner", 0) in observed
    assert ("malak.pkg.sample", "helper", "thing", 1) in observed
    assert all(fact.target_module != "malak.services.planner" for fact in imports)


def test_rspv0_red_c07_non_python_files_do_not_generate_modules(tmp_path: Path) -> None:
    repo, _ = make_repo(tmp_path)
    projection = projector_class()(reader_class()(repo)).project()

    assert all(fact.path != "README.md" for fact in projection.modules)


def test_rspv0_red_c08_python_syntax_error_fails_without_partial_projection(
    tmp_path: Path,
) -> None:
    repo, _ = make_repo(tmp_path)
    broken = repo / "src" / "malak" / "broken.py"
    broken.write_text("def broken(:\n", encoding="utf-8")
    git(repo, "add", "src/malak/broken.py")
    git(repo, "commit", "--no-gpg-sign", "-m", "broken")

    with pytest.raises(ValueError):
        projector_class()(reader_class()(repo)).project()


def test_rspv0_red_c09_projection_order_is_stable(tmp_path: Path) -> None:
    repo, _ = make_repo(tmp_path)
    projection = projector_class()(reader_class()(repo)).project()

    assert tuple(projection.modules) == tuple(sorted(projection.modules, key=lambda x: x.path))
    assert tuple(projection.symbols) == tuple(
        sorted(projection.symbols, key=lambda x: (x.path, x.line_number, x.qualified_name))
    )
    assert tuple(projection.imports) == tuple(
        sorted(
            projection.imports,
            key=lambda x: (
                x.path,
                x.line_number,
                x.target_module,
                x.imported_name or "",
            ),
        )
    )


def test_rspv0_red_c10_digest_changes_when_committed_structure_changes(
    tmp_path: Path,
) -> None:
    repo, _ = make_repo(tmp_path)
    first = projector_class()(reader_class()(repo)).project()

    sample = repo / "src" / "malak" / "pkg" / "sample.py"
    sample.write_text(
        sample.read_text(encoding="utf-8") + "\nclass Added:\n    pass\n",
        encoding="utf-8",
    )
    git(repo, "add", "src/malak/pkg/sample.py")
    git(repo, "commit", "--no-gpg-sign", "-m", "structure change")

    second = projector_class()(reader_class()(repo)).project()

    assert second.projection_digest != first.projection_digest


@pytest.mark.parametrize(
    ("kwargs",),
    [
        ({"max_python_files": 0},),
        ({"max_python_bytes": 0},),
        ({"max_symbols": 0},),
        ({"max_imports": 0},),
    ],
)
def test_rspv0_red_c11_nonpositive_resource_limits_are_rejected(
    tmp_path: Path,
    kwargs: dict[str, int],
) -> None:
    repo, _ = make_repo(tmp_path)

    with pytest.raises(ValueError):
        projector_class()(reader_class()(repo), **kwargs)


@pytest.mark.parametrize(
    ("kwargs",),
    [
        ({"max_python_files": HARD_MAX_PYTHON_FILES + 1},),
        ({"max_python_bytes": HARD_MAX_PYTHON_BYTES + 1},),
        ({"max_symbols": HARD_MAX_SYMBOLS + 1},),
        ({"max_imports": HARD_MAX_IMPORTS + 1},),
    ],
)
def test_rspv0_red_c12_hard_resource_limits_cannot_be_raised(
    tmp_path: Path,
    kwargs: dict[str, int],
) -> None:
    repo, _ = make_repo(tmp_path)

    with pytest.raises(ValueError):
        projector_class()(reader_class()(repo), **kwargs)


def test_rspv0_red_c13_file_budget_fails_before_partial_projection(
    tmp_path: Path,
) -> None:
    repo, _ = make_repo(tmp_path)

    with pytest.raises(RuntimeError):
        projector_class()(reader_class()(repo), max_python_files=1).project()


def test_rspv0_red_c14_byte_budget_fails_before_partial_projection(
    tmp_path: Path,
) -> None:
    repo, _ = make_repo(tmp_path)

    with pytest.raises(RuntimeError):
        projector_class()(reader_class()(repo), max_python_bytes=8).project()


def test_rspv0_red_c15_fact_budget_fails_explicitly(tmp_path: Path) -> None:
    repo, _ = make_repo(tmp_path)
    reader = reader_class()(repo)

    with pytest.raises(RuntimeError):
        projector_class()(reader, max_symbols=1).project()

    with pytest.raises(RuntimeError):
        projector_class()(reader, max_imports=1).project()


def test_rspv0_red_c16_contract_has_no_authority_or_execution_fields(
    tmp_path: Path,
) -> None:
    repo, _ = make_repo(tmp_path)
    projection = projector_class()(reader_class()(repo)).project()

    forbidden = {"authority", "permission", "execute", "decision", "severity", "score"}
    for fact in (*projection.modules, *projection.symbols, *projection.imports):
        assert forbidden.isdisjoint(vars(fact))
