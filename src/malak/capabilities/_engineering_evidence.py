from __future__ import annotations

from dataclasses import dataclass

from malak.infrastructure.repository_reader import GitRepositoryReader
from malak.knowledge.knowledge_reader import (
    GovernedKnowledgeReader,
    KnowledgeSearchResult,
)


@dataclass(frozen=True)
class EngineeringEvidenceBundle:
    baseline_commit: str
    subject: str
    repository_evidence: tuple[dict[str, object], ...]
    knowledge_evidence: tuple[dict[str, object], ...]
    repository_match_count: int
    knowledge_match_count: int
    repository_skipped_unreadable: int
    context_truncated: bool


def collect_engineering_evidence(
    *,
    repository_reader: GitRepositoryReader,
    knowledge_reader: GovernedKnowledgeReader,
    subject: str,
    max_repository_files: int,
    max_repository_bytes: int,
    max_repository_matches: int,
    max_context_matches_per_kind: int,
    max_evidence_line_bytes: int,
    error_scope: str,
) -> EngineeringEvidenceBundle:
    baseline_commit = repository_reader.baseline_commit
    if knowledge_reader.baseline_commit != baseline_commit:
        raise RuntimeError(
            "repository and knowledge readers must share the same baseline"
        )

    knowledge_paths = {source.path for source in knowledge_reader.list_sources()}
    candidate_paths = tuple(
        path
        for path in repository_reader.list_tracked_files()
        if path not in knowledge_paths
    )

    if len(candidate_paths) > max_repository_files:
        raise RuntimeError(
            f"captured snapshot exceeds the hard {error_scope} repository-file limit"
        )

    repository_evidence: list[dict[str, object]] = []
    processed_bytes = 0
    repository_match_count = 0
    repository_skipped_unreadable = 0
    repository_context_truncated = False

    for path in candidate_paths:
        try:
            document = repository_reader.read_text(path)
        except ValueError:
            repository_skipped_unreadable += 1
            continue

        if document.baseline_commit != baseline_commit:
            raise RuntimeError(
                "repository evidence baseline binding changed unexpectedly"
            )
        if document.path != path:
            raise RuntimeError(
                "repository evidence path binding changed unexpectedly"
            )

        processed_bytes += len(document.content.encode("utf-8"))
        if processed_bytes > max_repository_bytes:
            raise RuntimeError(
                f"captured snapshot exceeds the hard {error_scope} repository-byte limit"
            )

        for line_number, line in enumerate(document.content.splitlines(), start=1):
            if subject not in line:
                continue

            repository_match_count += 1
            if repository_match_count > max_repository_matches:
                raise RuntimeError(
                    f"captured snapshot exceeds the hard {error_scope} repository-match limit"
                )

            if len(repository_evidence) >= max_context_matches_per_kind:
                repository_context_truncated = True
                continue

            bounded_line, line_truncated = truncate_utf8(
                line,
                max_evidence_line_bytes,
            )
            if line_truncated:
                repository_context_truncated = True

            repository_evidence.append(
                {
                    "ref": f"R{len(repository_evidence) + 1}",
                    "path": document.path,
                    "blob_sha": document.blob_sha,
                    "line_number": line_number,
                    "line": bounded_line,
                    "line_truncated": line_truncated,
                }
            )

    if repository_match_count > len(repository_evidence):
        repository_context_truncated = True

    knowledge_result = knowledge_reader.search_text(subject)
    _validate_knowledge_evidence(
        result=knowledge_result,
        knowledge_reader=knowledge_reader,
        baseline_commit=baseline_commit,
    )
    knowledge_evidence, knowledge_context_truncated = _knowledge_context(
        knowledge_result,
        max_context_matches=max_context_matches_per_kind,
        max_line_bytes=max_evidence_line_bytes,
    )

    return EngineeringEvidenceBundle(
        baseline_commit=baseline_commit,
        subject=subject,
        repository_evidence=tuple(repository_evidence),
        knowledge_evidence=tuple(knowledge_evidence),
        repository_match_count=repository_match_count,
        knowledge_match_count=len(knowledge_result.matches),
        repository_skipped_unreadable=repository_skipped_unreadable,
        context_truncated=(
            repository_context_truncated or knowledge_context_truncated
        ),
    )


def truncate_utf8(value: str, max_bytes: int) -> tuple[str, bool]:
    raw = value.encode("utf-8")
    if len(raw) <= max_bytes:
        return value, False

    bounded = raw[:max_bytes]
    while bounded:
        try:
            return bounded.decode("utf-8"), True
        except UnicodeDecodeError:
            bounded = bounded[:-1]

    return "", True


def _validate_knowledge_evidence(
    *,
    result: KnowledgeSearchResult,
    knowledge_reader: GovernedKnowledgeReader,
    baseline_commit: str,
) -> None:
    if result.baseline_commit != baseline_commit:
        raise RuntimeError(
            "knowledge search baseline binding changed unexpectedly"
        )

    source_catalog = {
        source.path: source
        for source in knowledge_reader.list_sources()
    }
    for source in source_catalog.values():
        if source.baseline_commit != baseline_commit:
            raise RuntimeError(
                "knowledge source baseline binding changed unexpectedly"
            )

    for match in result.matches:
        if match.baseline_commit != baseline_commit:
            raise RuntimeError(
                "knowledge match baseline binding changed unexpectedly"
            )

        source = source_catalog.get(match.path)
        if source is None:
            raise RuntimeError(
                "knowledge match path is not present in the governed source catalog"
            )
        if (
            match.source_class != source.source_class
            or match.authority_class != source.authority_class
        ):
            raise RuntimeError(
                "knowledge match documentary-role binding changed unexpectedly"
            )


def _knowledge_context(
    result: KnowledgeSearchResult,
    *,
    max_context_matches: int,
    max_line_bytes: int,
) -> tuple[list[dict[str, object]], bool]:
    evidence: list[dict[str, object]] = []
    context_truncated = result.truncated

    for match in result.matches:
        if len(evidence) >= max_context_matches:
            context_truncated = True
            continue

        bounded_line, line_truncated = truncate_utf8(
            match.line,
            max_line_bytes,
        )
        if line_truncated:
            context_truncated = True

        evidence.append(
            {
                "ref": f"K{len(evidence) + 1}",
                "path": match.path,
                "blob_sha": match.blob_sha,
                "source_class": match.source_class,
                "authority_class": match.authority_class,
                "line_number": match.line_number,
                "line": bounded_line,
                "line_truncated": line_truncated,
            }
        )

    if len(result.matches) > len(evidence):
        context_truncated = True

    return evidence, context_truncated
