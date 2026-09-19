from __future__ import annotations

import re
from dataclasses import dataclass

from malak.infrastructure.repository_reader import GitRepositoryReader

_MAX_KNOWLEDGE_SOURCES = 256
_MAX_QUERY_BYTES = 4096
_MAX_SEARCHABLE_BYTES = 8 * 1024 * 1024
_MAX_SEARCH_RESULTS = 100
_MAX_SEARCH_OUTPUT_BYTES = 256 * 1024

_GOVERNING_SOURCES = {
    "docs/governance/cognitive_constitution.md",
    "docs/governance/governance_constitution.md",
    "docs/architecture/blueprint.md",
}
_DERIVED_STATE_SOURCES = {
    "docs/project/implementation_roadmap.md",
    "docs/project/project_context.md",
    "docs/project/roadmap.md",
}
_ADR_RE = re.compile(r"^docs/architecture/adr/ADR-[0-9]{3}-.+\.md$")


@dataclass(frozen=True)
class KnowledgeSource:
    baseline_commit: str
    path: str
    source_class: str
    authority_class: str


@dataclass(frozen=True)
class KnowledgeDocument:
    baseline_commit: str
    path: str
    blob_sha: str
    source_class: str
    authority_class: str
    content: str


@dataclass(frozen=True)
class KnowledgeTextMatch:
    baseline_commit: str
    path: str
    blob_sha: str
    source_class: str
    authority_class: str
    line_number: int
    line: str


@dataclass(frozen=True)
class KnowledgeSearchResult:
    baseline_commit: str
    matches: tuple[KnowledgeTextMatch, ...]
    truncated: bool


class GovernedKnowledgeReader:
    """
    Read-only classified view over knowledge sources in one captured repository snapshot.

    Classification is documentary metadata only. It does not interpret source
    content, grant authority, infer ADR status or authorize any operation.
    """

    def __init__(self, repository_reader: GitRepositoryReader) -> None:
        self._repository_reader = repository_reader
        self._baseline_commit = repository_reader.baseline_commit

        sources: dict[str, KnowledgeSource] = {}
        for path in repository_reader.list_tracked_files():
            classification = _classify_source(path)
            if classification is None:
                continue

            if len(sources) >= _MAX_KNOWLEDGE_SOURCES:
                raise RuntimeError(
                    "captured snapshot exceeds the hard E1 knowledge-source limit"
                )

            source_class, authority_class = classification
            sources[path] = KnowledgeSource(
                baseline_commit=self._baseline_commit,
                path=path,
                source_class=source_class,
                authority_class=authority_class,
            )

        self._sources = sources

    @property
    def baseline_commit(self) -> str:
        return self._baseline_commit

    def list_sources(self) -> tuple[KnowledgeSource, ...]:
        return tuple(self._sources[path] for path in sorted(self._sources))

    def read(self, path: str) -> KnowledgeDocument:
        if not isinstance(path, str):
            raise TypeError("knowledge path must be a string")

        source = self._sources.get(path)
        if source is None:
            raise ValueError(f"path is not a recognized E1 knowledge source: {path}")

        document = self._repository_reader.read_text(path)
        if document.baseline_commit != self._baseline_commit:
            raise RuntimeError("repository reader baseline changed unexpectedly")

        return KnowledgeDocument(
            baseline_commit=document.baseline_commit,
            path=document.path,
            blob_sha=document.blob_sha,
            source_class=source.source_class,
            authority_class=source.authority_class,
            content=document.content,
        )

    def search_text(self, query: str) -> KnowledgeSearchResult:
        _validate_query(query)

        documents: list[tuple[KnowledgeSource, KnowledgeDocument]] = []
        searchable_bytes = 0

        for source in self.list_sources():
            document = self.read(source.path)
            searchable_bytes += len(document.content.encode("utf-8"))
            if searchable_bytes > _MAX_SEARCHABLE_BYTES:
                raise RuntimeError(
                    "captured snapshot exceeds the hard E1 searchable-byte limit"
                )
            documents.append((source, document))

        matches: list[KnowledgeTextMatch] = []
        output_bytes = 0

        for source, document in documents:
            for line_number, line in enumerate(document.content.splitlines(), start=1):
                if query not in line:
                    continue

                if len(matches) >= _MAX_SEARCH_RESULTS:
                    return KnowledgeSearchResult(
                        baseline_commit=self._baseline_commit,
                        matches=tuple(matches),
                        truncated=True,
                    )

                line_bytes = len(line.encode("utf-8"))
                if output_bytes + line_bytes > _MAX_SEARCH_OUTPUT_BYTES:
                    return KnowledgeSearchResult(
                        baseline_commit=self._baseline_commit,
                        matches=tuple(matches),
                        truncated=True,
                    )

                matches.append(
                    KnowledgeTextMatch(
                        baseline_commit=document.baseline_commit,
                        path=document.path,
                        blob_sha=document.blob_sha,
                        source_class=source.source_class,
                        authority_class=source.authority_class,
                        line_number=line_number,
                        line=line,
                    )
                )
                output_bytes += line_bytes

        return KnowledgeSearchResult(
            baseline_commit=self._baseline_commit,
            matches=tuple(matches),
            truncated=False,
        )


def _classify_source(path: str) -> tuple[str, str] | None:
    if path in _GOVERNING_SOURCES:
        return "GOVERNING", "normative"

    if path == "SECURITY.md":
        return "SECURITY_POLICY", "protected_subordinate"

    if _ADR_RE.fullmatch(path):
        return "DECISION_RECORD", "status_dependent"

    if (
        path.startswith("docs/architecture/")
        and "/" not in path.removeprefix("docs/architecture/")
        and path.endswith(".md")
    ):
        return "ARCHITECTURE_REFERENCE", "reference"

    if path.startswith("docs/architecture/decisions/"):
        return "ARCHITECTURE_REFERENCE", "reference"

    if path.startswith("docs/architecture/schemas/"):
        return "ARCHITECTURE_REFERENCE", "reference"

    if path == "AGENTS.md" or path.startswith("docs/development/"):
        return "ENGINEERING_METHOD", "process_reference"

    if path.startswith("docs/knowledge/templates/"):
        return None

    if path.startswith("docs/knowledge/"):
        return "CURATED_KNOWLEDGE", "curated_reference"

    if path in _DERIVED_STATE_SOURCES or path.startswith("docs/project/status/"):
        return "DERIVED_STATE", "derived"

    if path == "documents/projects/jarvis/ideas.md":
        return "NON_NORMATIVE_IDEA", "non_normative"

    if path.startswith("docs/project/concepts/"):
        return "NON_NORMATIVE_CONCEPT", "non_normative"

    return None


def _validate_query(query: str) -> None:
    if not isinstance(query, str):
        raise TypeError("search query must be a string")
    if not query:
        raise ValueError("search query cannot be empty")
    if any(ord(character) < 32 or ord(character) == 127 for character in query):
        raise ValueError("search query contains forbidden control characters")
    if len(query.encode("utf-8")) > _MAX_QUERY_BYTES:
        raise ValueError(
            f"search query cannot exceed {_MAX_QUERY_BYTES} UTF-8 bytes"
        )
