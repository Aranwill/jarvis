from __future__ import annotations

import subprocess
from importlib import import_module
from pathlib import Path

import pytest

from malak.infrastructure.repository_structure import (
    ImportFact,
    ModuleFact,
    RepositoryStructuralProjection,
    SymbolFact,
)


BASELINE = "a" * 40
BLOB_A = "1" * 40
BLOB_B = "2" * 40


def lookup_class():
    return import_module(
        "malak.infrastructure.repository_structure_lookup"
    ).RepositoryStructuralLookup


def projection(*, duplicate_symbol: bool = False) -> RepositoryStructuralProjection:
    alpha = SymbolFact(
        baseline_commit=BASELINE,
        path="src/malak/pkg/alpha.py",
        blob_sha=BLOB_A,
        module_name="malak.pkg.alpha",
        qualified_name="malak.pkg.alpha.Alpha",
        kind="CLASS",
        line_number=3,
    )
    beta = SymbolFact(
        baseline_commit=BASELINE,
        path="src/malak/pkg/alpha.py",
        blob_sha=BLOB_A,
        module_name="malak.pkg.alpha",
        qualified_name="malak.pkg.alpha.beta",
        kind="FUNCTION",
        line_number=9,
    )
    other = SymbolFact(
        baseline_commit=BASELINE,
        path="src/malak/pkg/other.py",
        blob_sha=BLOB_B,
        module_name="malak.pkg.other",
        qualified_name="malak.pkg.other.Other",
        kind="CLASS",
        line_number=2,
    )
    symbols = [alpha, beta, other]
    if duplicate_symbol:
        symbols.append(
            SymbolFact(
                baseline_commit=BASELINE,
                path="src/malak/pkg/duplicate.py",
                blob_sha="3" * 40,
                module_name="malak.pkg.duplicate",
                qualified_name="malak.pkg.alpha.Alpha",
                kind="CLASS",
                line_number=1,
            )
        )

    return RepositoryStructuralProjection(
        baseline_commit=BASELINE,
        modules=(
            ModuleFact(BASELINE, "src/malak/pkg/alpha.py", BLOB_A, "malak.pkg.alpha"),
            ModuleFact(BASELINE, "src/malak/pkg/other.py", BLOB_B, "malak.pkg.other"),
        ),
        symbols=tuple(symbols),
        imports=(
            ImportFact(
                BASELINE,
                "src/malak/pkg/alpha.py",
                BLOB_A,
                "malak.pkg.alpha",
                "os",
                None,
                1,
                0,
            ),
            ImportFact(
                BASELINE,
                "src/malak/pkg/alpha.py",
                BLOB_A,
                "malak.pkg.alpha",
                "malak.pkg",
                "other",
                2,
                0,
            ),
            ImportFact(
                BASELINE,
                "src/malak/pkg/other.py",
                BLOB_B,
                "malak.pkg.other",
                "typing",
                None,
                1,
                0,
            ),
        ),
        projection_digest="d" * 64,
    )


def test_rslv0_red_c01_lookup_module_does_not_exist_yet() -> None:
    module = import_module("malak.infrastructure.repository_structure_lookup")
    assert hasattr(module, "RepositoryStructuralLookup")


def test_rslv0_red_c02_exact_symbol_lookup_and_missing_are_deterministic() -> None:
    source = projection()
    lookup = lookup_class()(source)

    found = lookup.lookup_symbol("malak.pkg.alpha.Alpha")

    assert found == source.symbols[0]
    assert found.baseline_commit == BASELINE
    assert found.path == "src/malak/pkg/alpha.py"
    assert found.blob_sha == BLOB_A
    assert lookup.lookup_symbol("malak.pkg.alpha.Alph") is None
    assert lookup.lookup_symbol("Alpha") is None
    assert lookup.lookup_symbol("malak.pkg.missing.Missing") is None


def test_rslv0_red_c03_duplicate_exact_symbol_fails_closed() -> None:
    lookup = lookup_class()(projection(duplicate_symbol=True))

    with pytest.raises(RuntimeError):
        lookup.lookup_symbol("malak.pkg.alpha.Alpha")


def test_rslv0_red_c04_symbols_and_imports_filter_exact_module_and_keep_order() -> None:
    source = projection()
    lookup = lookup_class()(source)

    symbols = lookup.symbols_in_module("malak.pkg.alpha")
    imports = lookup.imports_from("malak.pkg.alpha")

    assert symbols == source.symbols[:2]
    assert tuple(fact.qualified_name for fact in symbols) == (
        "malak.pkg.alpha.Alpha",
        "malak.pkg.alpha.beta",
    )
    assert imports == source.imports[:2]
    assert all(fact.module_name == "malak.pkg.alpha" for fact in symbols)
    assert all(fact.source_module == "malak.pkg.alpha" for fact in imports)

    assert lookup.symbols_in_module("malak.pkg.alph") == ()
    assert lookup.imports_from("malak.pkg.alph") == ()


@pytest.mark.parametrize("method_name", ["lookup_symbol", "symbols_in_module", "imports_from"])
@pytest.mark.parametrize("query", ["", "   "])
def test_rslv0_red_c05_blank_queries_are_rejected(
    method_name: str,
    query: str,
) -> None:
    method = getattr(lookup_class()(projection()), method_name)

    with pytest.raises(ValueError):
        method(query)


@pytest.mark.parametrize("method_name", ["lookup_symbol", "symbols_in_module", "imports_from"])
def test_rslv0_red_c06_non_string_queries_are_rejected(method_name: str) -> None:
    method = getattr(lookup_class()(projection()), method_name)

    with pytest.raises(TypeError):
        method(None)


def test_rslv0_red_c07_lookup_does_not_mutate_projection_or_perform_io(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = projection()
    lookup = lookup_class()(source)
    before = source

    def forbidden(*args, **kwargs):
        raise AssertionError("Structural Lookup V0 must not perform repository/filesystem I/O")

    monkeypatch.setattr(subprocess, "run", forbidden)
    monkeypatch.setattr(Path, "open", forbidden)
    monkeypatch.setattr(Path, "read_text", forbidden)
    monkeypatch.setattr(Path, "write_text", forbidden)

    assert lookup.lookup_symbol("malak.pkg.alpha.Alpha") == source.symbols[0]
    assert lookup.symbols_in_module("malak.pkg.alpha") == source.symbols[:2]
    assert lookup.imports_from("malak.pkg.alpha") == source.imports[:2]
    assert source == before


def test_rslv0_red_c08_lookup_contract_has_no_authority_or_scoring_surface() -> None:
    lookup = lookup_class()(projection())

    forbidden = {
        "authority",
        "permission",
        "decision",
        "severity",
        "score",
        "rank",
        "execute",
    }
    assert forbidden.isdisjoint(vars(lookup))
