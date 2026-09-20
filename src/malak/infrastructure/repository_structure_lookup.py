from __future__ import annotations

from malak.infrastructure.repository_structure import (
    ImportFact,
    RepositoryStructuralProjection,
    SymbolFact,
)


class RepositoryStructuralLookup:
    """Exact, read-only lookup over one structural projection."""

    def __init__(self, projection: RepositoryStructuralProjection) -> None:
        if not isinstance(projection, RepositoryStructuralProjection):
            raise TypeError("projection must be a RepositoryStructuralProjection")
        self._projection = projection

    def lookup_symbol(self, qualified_name: str) -> SymbolFact | None:
        query = _validate_query(qualified_name, name="qualified_name")
        matches = tuple(
            fact
            for fact in self._projection.symbols
            if fact.qualified_name == query
        )

        if len(matches) > 1:
            raise RuntimeError(
                "structural lookup found multiple exact symbol matches"
            )
        if not matches:
            return None
        return matches[0]

    def symbols_in_module(self, module_name: str) -> tuple[SymbolFact, ...]:
        query = _validate_query(module_name, name="module_name")
        return tuple(
            fact
            for fact in self._projection.symbols
            if fact.module_name == query
        )

    def imports_from(self, module_name: str) -> tuple[ImportFact, ...]:
        query = _validate_query(module_name, name="module_name")
        return tuple(
            fact
            for fact in self._projection.imports
            if fact.source_module == query
        )


def _validate_query(value: str, *, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    if not value.strip():
        raise ValueError(f"{name} must not be blank")
    return value
