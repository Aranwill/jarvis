from __future__ import annotations

import ast
import hashlib
import json
from dataclasses import asdict, dataclass

from malak.infrastructure.repository_reader import GitRepositoryReader


_HARD_MAX_PYTHON_FILES = 256
_HARD_MAX_PYTHON_BYTES = 4 * 1024 * 1024
_HARD_MAX_SYMBOLS = 8192
_HARD_MAX_IMPORTS = 8192


@dataclass(frozen=True)
class ModuleFact:
    baseline_commit: str
    path: str
    blob_sha: str
    module_name: str


@dataclass(frozen=True)
class SymbolFact:
    baseline_commit: str
    path: str
    blob_sha: str
    module_name: str
    qualified_name: str
    kind: str
    line_number: int


@dataclass(frozen=True)
class ImportFact:
    baseline_commit: str
    path: str
    blob_sha: str
    source_module: str
    target_module: str
    imported_name: str | None
    line_number: int
    relative_level: int


@dataclass(frozen=True)
class RepositoryStructuralProjection:
    baseline_commit: str
    modules: tuple[ModuleFact, ...]
    symbols: tuple[SymbolFact, ...]
    imports: tuple[ImportFact, ...]
    projection_digest: str


class RepositoryStructuralProjector:
    """Derive bounded, syntax-only facts from one E0 repository snapshot."""

    def __init__(
        self,
        repository_reader: GitRepositoryReader,
        *,
        max_python_files: int = _HARD_MAX_PYTHON_FILES,
        max_python_bytes: int = _HARD_MAX_PYTHON_BYTES,
        max_symbols: int = _HARD_MAX_SYMBOLS,
        max_imports: int = _HARD_MAX_IMPORTS,
    ) -> None:
        self._repository_reader = repository_reader
        self._max_python_files = _validated_limit(
            max_python_files,
            name="max_python_files",
            hard_max=_HARD_MAX_PYTHON_FILES,
        )
        self._max_python_bytes = _validated_limit(
            max_python_bytes,
            name="max_python_bytes",
            hard_max=_HARD_MAX_PYTHON_BYTES,
        )
        self._max_symbols = _validated_limit(
            max_symbols,
            name="max_symbols",
            hard_max=_HARD_MAX_SYMBOLS,
        )
        self._max_imports = _validated_limit(
            max_imports,
            name="max_imports",
            hard_max=_HARD_MAX_IMPORTS,
        )

    @property
    def baseline_commit(self) -> str:
        return self._repository_reader.baseline_commit

    def project(self) -> RepositoryStructuralProjection:
        python_paths = tuple(
            path
            for path in self._repository_reader.list_tracked_files()
            if path.endswith(".py")
        )
        if len(python_paths) > self._max_python_files:
            raise RuntimeError(
                "captured snapshot exceeds repository-structure Python-file limit"
            )

        modules: list[ModuleFact] = []
        symbols: list[SymbolFact] = []
        imports: list[ImportFact] = []
        processed_bytes = 0

        for path in python_paths:
            document = self._repository_reader.read_text(path)
            if document.baseline_commit != self.baseline_commit:
                raise RuntimeError("repository structure baseline binding changed unexpectedly")
            if document.path != path:
                raise RuntimeError("repository structure path binding changed unexpectedly")

            processed_bytes += len(document.content.encode("utf-8"))
            if processed_bytes > self._max_python_bytes:
                raise RuntimeError(
                    "captured snapshot exceeds repository-structure Python-byte limit"
                )

            module_name = _module_name(path)
            try:
                tree = ast.parse(document.content, filename=path)
            except SyntaxError as exc:
                raise ValueError(f"Python syntax error in captured path: {path}") from exc

            modules.append(
                ModuleFact(
                    baseline_commit=document.baseline_commit,
                    path=document.path,
                    blob_sha=document.blob_sha,
                    module_name=module_name,
                )
            )

            extractor = _FactExtractor(
                baseline_commit=document.baseline_commit,
                path=document.path,
                blob_sha=document.blob_sha,
                module_name=module_name,
            )
            extractor.visit(tree)
            symbols.extend(extractor.symbols)
            imports.extend(extractor.imports)

            if len(symbols) > self._max_symbols:
                raise RuntimeError(
                    "captured snapshot exceeds repository-structure symbol limit"
                )
            if len(imports) > self._max_imports:
                raise RuntimeError(
                    "captured snapshot exceeds repository-structure import limit"
                )

        ordered_modules = tuple(sorted(modules, key=lambda fact: fact.path))
        ordered_symbols = tuple(
            sorted(
                symbols,
                key=lambda fact: (fact.path, fact.line_number, fact.qualified_name),
            )
        )
        ordered_imports = tuple(
            sorted(
                imports,
                key=lambda fact: (
                    fact.path,
                    fact.line_number,
                    fact.target_module,
                    fact.imported_name or "",
                ),
            )
        )

        digest = _projection_digest(
            baseline_commit=self.baseline_commit,
            modules=ordered_modules,
            symbols=ordered_symbols,
            imports=ordered_imports,
        )
        return RepositoryStructuralProjection(
            baseline_commit=self.baseline_commit,
            modules=ordered_modules,
            symbols=ordered_symbols,
            imports=ordered_imports,
            projection_digest=digest,
        )


class _FactExtractor(ast.NodeVisitor):
    def __init__(
        self,
        *,
        baseline_commit: str,
        path: str,
        blob_sha: str,
        module_name: str,
    ) -> None:
        self._baseline_commit = baseline_commit
        self._path = path
        self._blob_sha = blob_sha
        self._module_name = module_name
        self._scope: list[tuple[str, str]] = []
        self.symbols: list[SymbolFact] = []
        self.imports: list[ImportFact] = []

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self._record_symbol(node=node, kind="CLASS")
        self._scope.append(("class", node.name))
        self.generic_visit(node)
        self._scope.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        kind = "METHOD" if self._immediate_parent_is_class() else "FUNCTION"
        self._record_symbol(node=node, kind=kind)
        self._scope.append(("function", node.name))
        self.generic_visit(node)
        self._scope.pop()

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        kind = "ASYNC_METHOD" if self._immediate_parent_is_class() else "ASYNC_FUNCTION"
        self._record_symbol(node=node, kind=kind)
        self._scope.append(("function", node.name))
        self.generic_visit(node)
        self._scope.pop()

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            self.imports.append(
                ImportFact(
                    baseline_commit=self._baseline_commit,
                    path=self._path,
                    blob_sha=self._blob_sha,
                    source_module=self._module_name,
                    target_module=alias.name,
                    imported_name=None,
                    line_number=node.lineno,
                    relative_level=0,
                )
            )

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        target_module = node.module or ""
        for alias in node.names:
            self.imports.append(
                ImportFact(
                    baseline_commit=self._baseline_commit,
                    path=self._path,
                    blob_sha=self._blob_sha,
                    source_module=self._module_name,
                    target_module=target_module,
                    imported_name=alias.name,
                    line_number=node.lineno,
                    relative_level=node.level,
                )
            )

    def _record_symbol(
        self,
        *,
        node: ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef,
        kind: str,
    ) -> None:
        parts = [self._module_name, *(name for _, name in self._scope), node.name]
        self.symbols.append(
            SymbolFact(
                baseline_commit=self._baseline_commit,
                path=self._path,
                blob_sha=self._blob_sha,
                module_name=self._module_name,
                qualified_name=".".join(part for part in parts if part),
                kind=kind,
                line_number=node.lineno,
            )
        )

    def _immediate_parent_is_class(self) -> bool:
        return bool(self._scope and self._scope[-1][0] == "class")


def _module_name(path: str) -> str:
    logical = path[:-3]
    if logical.startswith("src/"):
        logical = logical[4:]
    parts = logical.split("/")
    if parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts)


def _validated_limit(value: int, *, name: str, hard_max: int) -> int:
    if type(value) is not int or value <= 0:
        raise ValueError(f"{name} must be a positive integer")
    if value > hard_max:
        raise ValueError(f"{name} cannot exceed hard limit {hard_max}")
    return value


def _projection_digest(
    *,
    baseline_commit: str,
    modules: tuple[ModuleFact, ...],
    symbols: tuple[SymbolFact, ...],
    imports: tuple[ImportFact, ...],
) -> str:
    payload = {
        "baseline_commit": baseline_commit,
        "modules": [asdict(fact) for fact in modules],
        "symbols": [asdict(fact) for fact in symbols],
        "imports": [asdict(fact) for fact in imports],
    }
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()
