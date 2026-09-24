from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

from malak.infrastructure.repository_reader import GitRepositoryReader
from malak.knowledge.knowledge_reader import (
    GovernedKnowledgeReader,
    KnowledgeSearchResult,
)


_ALLOWED_SELECTOR_KINDS = frozenset({"EXACT_PATH", "PATH_PREFIX"})
_SELECTOR_STATUSES = frozenset({"RESOLVED", "MISSING", "UNREADABLE", "TRUNCATED"})
_COMPLETENESS_CRITERIA = "ALL_REQUIRED_SELECTORS_RESOLVED"


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


@dataclass(frozen=True, slots=True)
class EvidenceSelector:
    kind: str
    value: str
    terms: tuple[str, ...]
    max_matches: int

    def __post_init__(self) -> None:
        if self.kind not in _ALLOWED_SELECTOR_KINDS:
            raise ValueError("unsupported evidence selector kind")
        _validate_repo_path(self.value, prefix=self.kind == "PATH_PREFIX")
        if not isinstance(self.terms, tuple) or not self.terms:
            raise ValueError("selector terms must be a non-empty tuple")
        for term in self.terms:
            _validate_text("selector term", term)
        if not isinstance(self.max_matches, int) or isinstance(self.max_matches, bool):
            raise TypeError("selector max_matches must be an integer")
        if self.max_matches <= 0:
            raise ValueError("selector max_matches must be greater than zero")


@dataclass(frozen=True, slots=True)
class GovernedEngineeringEvidenceFocus:
    focus_id: str
    focus_label: str
    subject: str
    repository_required_selectors: tuple[EvidenceSelector, ...]
    knowledge_required_selectors: tuple[EvidenceSelector, ...]
    supplemental_terms: tuple[str, ...]
    supplemental_max_matches_per_kind: int
    max_evidence_line_bytes: int
    completeness_criteria: str = _COMPLETENESS_CRITERIA
    authority_effect: str = "none"

    def __post_init__(self) -> None:
        _validate_text("focus_id", self.focus_id)
        _validate_text("focus_label", self.focus_label)
        _validate_text("subject", self.subject)
        if self.completeness_criteria != _COMPLETENESS_CRITERIA:
            raise ValueError("unsupported focus completeness criteria")
        if self.authority_effect != "none":
            raise ValueError("focus authority_effect must remain none")
        _validate_selector_tuple(
            "repository_required_selectors",
            self.repository_required_selectors,
        )
        _validate_selector_tuple(
            "knowledge_required_selectors",
            self.knowledge_required_selectors,
        )
        if not isinstance(self.supplemental_terms, tuple):
            raise TypeError("supplemental_terms must be a tuple")
        for term in self.supplemental_terms:
            _validate_text("supplemental term", term)
        if len(set(self.supplemental_terms)) != len(self.supplemental_terms):
            raise ValueError("duplicate supplemental term")
        if (
            not isinstance(self.supplemental_max_matches_per_kind, int)
            or isinstance(self.supplemental_max_matches_per_kind, bool)
        ):
            raise TypeError(
                "supplemental_max_matches_per_kind must be an integer"
            )
        if self.supplemental_max_matches_per_kind <= 0:
            raise ValueError(
                "supplemental_max_matches_per_kind must be greater than zero"
            )
        if (
            not isinstance(self.max_evidence_line_bytes, int)
            or isinstance(self.max_evidence_line_bytes, bool)
        ):
            raise TypeError("max_evidence_line_bytes must be an integer")
        if self.max_evidence_line_bytes <= 0:
            raise ValueError("max_evidence_line_bytes must be greater than zero")


@dataclass(frozen=True, slots=True)
class EvidenceSelectorResult:
    source_kind: str
    selector_kind: str
    selector_value: str
    status: str
    matched_paths: tuple[str, ...]
    match_count: int
    selected_count: int

    def __post_init__(self) -> None:
        if self.source_kind not in {"repository", "knowledge"}:
            raise ValueError("invalid selector result source_kind")
        if self.selector_kind not in _ALLOWED_SELECTOR_KINDS:
            raise ValueError("invalid selector result selector_kind")
        if self.status not in _SELECTOR_STATUSES:
            raise ValueError("invalid selector result status")


@dataclass(frozen=True, slots=True)
class FocusedEngineeringEvidenceBundle:
    baseline_commit: str
    focus_id: str
    subject: str
    repository_evidence: tuple[dict[str, object], ...]
    knowledge_evidence: tuple[dict[str, object], ...]
    selector_results: tuple[EvidenceSelectorResult, ...]
    repository_match_count: int
    knowledge_match_count: int
    repository_skipped_unreadable: int
    context_truncated: bool
    supplemental_truncated: bool
    complete: bool
    evidence_set_digest: str
    authority_effect: str = "none"


@dataclass(frozen=True, slots=True)
class BootstrapFocusCompletion:
    states: dict[str, str]
    complete: bool
    authority_effect: str = "none"


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


def collect_focused_engineering_evidence(
    *,
    repository_reader: GitRepositoryReader,
    knowledge_reader: GovernedKnowledgeReader,
    focus: GovernedEngineeringEvidenceFocus,
) -> FocusedEngineeringEvidenceBundle:
    if not isinstance(focus, GovernedEngineeringEvidenceFocus):
        raise TypeError("focus must be a GovernedEngineeringEvidenceFocus")

    baseline_commit = repository_reader.baseline_commit
    if knowledge_reader.baseline_commit != baseline_commit:
        raise RuntimeError(
            "repository and knowledge readers must share the same baseline"
        )

    tracked_paths = repository_reader.list_tracked_files()
    knowledge_catalog = {
        source.path: source
        for source in knowledge_reader.list_sources()
    }
    knowledge_paths = set(knowledge_catalog)
    repository_paths = tuple(
        path for path in tracked_paths if path not in knowledge_paths
    )

    repository_raw: list[dict[str, object]] = []
    knowledge_raw: list[dict[str, object]] = []
    selector_results: list[EvidenceSelectorResult] = []
    repository_skipped_unreadable = 0

    for selector in focus.repository_required_selectors:
        result, evidence, skipped = _collect_required_selector(
            source_kind="repository",
            selector=selector,
            available_paths=repository_paths,
            repository_reader=repository_reader,
            knowledge_reader=knowledge_reader,
            max_line_bytes=focus.max_evidence_line_bytes,
        )
        selector_results.append(result)
        repository_raw.extend(evidence)
        repository_skipped_unreadable += skipped

    for selector in focus.knowledge_required_selectors:
        result, evidence, _ = _collect_required_selector(
            source_kind="knowledge",
            selector=selector,
            available_paths=tuple(sorted(knowledge_paths)),
            repository_reader=repository_reader,
            knowledge_reader=knowledge_reader,
            max_line_bytes=focus.max_evidence_line_bytes,
        )
        selector_results.append(result)
        knowledge_raw.extend(evidence)

    supplemental_truncated = False
    for term in focus.supplemental_terms:
        supplemental = collect_engineering_evidence(
            repository_reader=repository_reader,
            knowledge_reader=knowledge_reader,
            subject=term,
            max_repository_files=512,
            max_repository_bytes=8 * 1024 * 1024,
            max_repository_matches=1000,
            max_context_matches_per_kind=focus.supplemental_max_matches_per_kind,
            max_evidence_line_bytes=focus.max_evidence_line_bytes,
            error_scope="FOCUS",
        )
        supplemental_truncated = (
            supplemental_truncated or supplemental.context_truncated
        )
        repository_skipped_unreadable += supplemental.repository_skipped_unreadable
        repository_raw.extend(
            _strip_ref(item, required=False)
            for item in supplemental.repository_evidence
        )
        knowledge_raw.extend(
            _strip_ref(item, required=False)
            for item in supplemental.knowledge_evidence
        )

    repository_evidence = _canonicalize_evidence(repository_raw, prefix="R")
    knowledge_evidence = _canonicalize_evidence(knowledge_raw, prefix="K")

    complete = all(
        result.status == "RESOLVED"
        for result in selector_results
    )
    required_truncated = any(
        result.status == "TRUNCATED"
        for result in selector_results
    )

    digest_payload = {
        "baseline_commit": baseline_commit,
        "focus_id": focus.focus_id,
        "subject": focus.subject,
        "selector_results": [
            {
                "source_kind": result.source_kind,
                "selector_kind": result.selector_kind,
                "selector_value": result.selector_value,
                "status": result.status,
                "matched_paths": list(result.matched_paths),
                "match_count": result.match_count,
                "selected_count": result.selected_count,
            }
            for result in selector_results
        ],
        "repository_evidence": [
            _digest_evidence_item(item)
            for item in repository_evidence
        ],
        "knowledge_evidence": [
            _digest_evidence_item(item)
            for item in knowledge_evidence
        ],
        "supplemental_truncated": supplemental_truncated,
        "authority_effect": "none",
    }
    canonical = json.dumps(
        digest_payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    evidence_set_digest = hashlib.sha256(canonical).hexdigest()

    return FocusedEngineeringEvidenceBundle(
        baseline_commit=baseline_commit,
        focus_id=focus.focus_id,
        subject=focus.subject,
        repository_evidence=repository_evidence,
        knowledge_evidence=knowledge_evidence,
        selector_results=tuple(selector_results),
        repository_match_count=len(repository_evidence),
        knowledge_match_count=len(knowledge_evidence),
        repository_skipped_unreadable=repository_skipped_unreadable,
        context_truncated=required_truncated or supplemental_truncated,
        supplemental_truncated=supplemental_truncated,
        complete=complete,
        evidence_set_digest=evidence_set_digest,
        authority_effect="none",
    )


def bootstrap_engineering_evidence_focuses(
) -> tuple[GovernedEngineeringEvidenceFocus, ...]:
    return (
        GovernedEngineeringEvidenceFocus(
            focus_id="U01",
            focus_label="U01 Core Kernel",
            subject="Kernel",
            repository_required_selectors=(
                EvidenceSelector(
                    "PATH_PREFIX",
                    "src/malak/kernel/",
                    ("Kernel", "Capability", "Planner"),
                    64,
                ),
                EvidenceSelector(
                    "EXACT_PATH",
                    "src/malak/services/planner.py",
                    ("Planner", "capability"),
                    32,
                ),
                EvidenceSelector(
                    "EXACT_PATH",
                    "src/malak/contracts/capability.py",
                    ("Capability",),
                    32,
                ),
                EvidenceSelector(
                    "EXACT_PATH",
                    "src/malak/app/composition.py",
                    ("Kernel", "Capability", "engineering"),
                    64,
                ),
                EvidenceSelector(
                    "EXACT_PATH",
                    "tests/test_kernel.py",
                    ("Kernel", "kernel"),
                    64,
                ),
            ),
            knowledge_required_selectors=(
                EvidenceSelector(
                    "EXACT_PATH",
                    "docs/architecture/blueprint.md",
                    ("Kernel", "Capability"),
                    64,
                ),
                EvidenceSelector(
                    "EXACT_PATH",
                    "docs/architecture/architecture_quality_gates.md",
                    ("Kernel", "complex"),
                    64,
                ),
                EvidenceSelector(
                    "EXACT_PATH",
                    "docs/governance/cognitive_constitution.md",
                    ("Kernel", "evidence"),
                    64,
                ),
                EvidenceSelector(
                    "EXACT_PATH",
                    "docs/governance/governance_constitution.md",
                    ("authority", "evidence"),
                    64,
                ),
                EvidenceSelector(
                    "EXACT_PATH",
                    "docs/project/concepts/GOVERNED_SELF_REVIEW_BOOTSTRAP_TASK.md",
                    ("U01", "Kernel"),
                    64,
                ),
                EvidenceSelector(
                    "EXACT_PATH",
                    "docs/project/status/MALAK-CONSTRUCTION-FLOW-COMPLIANCE-AUDIT-V1-BATCH-D.md",
                    ("U01", "Kernel"),
                    64,
                ),
            ),
            supplemental_terms=("Kernel", "Capability First", "Kernel First"),
            supplemental_max_matches_per_kind=12,
            max_evidence_line_bytes=2048,
        ),
        GovernedEngineeringEvidenceFocus(
            focus_id="U04",
            focus_label="U04 Observability",
            subject="Observability",
            repository_required_selectors=(
                EvidenceSelector(
                    "PATH_PREFIX",
                    "src/malak/observability/",
                    ("Event", "Trace", "observ"),
                    96,
                ),
                EvidenceSelector(
                    "EXACT_PATH",
                    "src/malak/runtime/runtime_metrics.py",
                    ("metric", "Metric"),
                    48,
                ),
                EvidenceSelector(
                    "EXACT_PATH",
                    "src/malak/runtime/runtime_performance_profile.py",
                    ("performance", "Performance"),
                    48,
                ),
                EvidenceSelector(
                    "EXACT_PATH",
                    "src/malak/runtime/runtime_performance_profiler.py",
                    ("performance", "Performance"),
                    48,
                ),
                EvidenceSelector(
                    "EXACT_PATH",
                    "tests/test_operational_event.py",
                    ("event", "Event"),
                    64,
                ),
                EvidenceSelector(
                    "EXACT_PATH",
                    "tests/test_operational_event_store.py",
                    ("event", "Event"),
                    64,
                ),
                EvidenceSelector(
                    "EXACT_PATH",
                    "tests/test_runtime_performance_profiler.py",
                    ("performance", "metric"),
                    64,
                ),
            ),
            knowledge_required_selectors=(
                EvidenceSelector(
                    "EXACT_PATH",
                    "docs/project/concepts/GOVERNED_SELF_REVIEW_BOOTSTRAP_TASK.md",
                    ("U04", "metrics", "telemetry", "observation"),
                    64,
                ),
                EvidenceSelector(
                    "EXACT_PATH",
                    "docs/project/status/MALAK-CONSTRUCTION-FLOW-COMPLIANCE-AUDIT-V1-BATCH-D.md",
                    ("U04", "Observability"),
                    64,
                ),
                EvidenceSelector(
                    "EXACT_PATH",
                    "docs/project/status/MALAK-CONSTRUCTION-FLOW-COMPLIANCE-AUDIT-V1-FINAL.md",
                    ("observability", "metrics"),
                    64,
                ),
                EvidenceSelector(
                    "EXACT_PATH",
                    "docs/project/sprints/proposals/MALAK-E2-STRUCTURAL-EVIDENCE-OBSERVABILITY-V0-G0-G1-DESIGN.md",
                    ("Observability", "authority", "evaluation"),
                    96,
                ),
            ),
            supplemental_terms=("Observability", "metrics", "telemetry"),
            supplemental_max_matches_per_kind=12,
            max_evidence_line_bytes=2048,
        ),
        GovernedEngineeringEvidenceFocus(
            focus_id="RR-03",
            focus_label="RR-03 Strong SecurityContext Provenance",
            subject="SecurityContext Provenance",
            repository_required_selectors=(
                EvidenceSelector(
                    "EXACT_PATH",
                    "src/malak/security/contracts.py",
                    ("SecurityContext",),
                    64,
                ),
                EvidenceSelector(
                    "EXACT_PATH",
                    "src/malak/security/context_issuer.py",
                    ("SecurityContext",),
                    64,
                ),
                EvidenceSelector(
                    "EXACT_PATH",
                    "src/malak/security/context_validator.py",
                    ("SecurityContext",),
                    64,
                ),
                EvidenceSelector(
                    "EXACT_PATH",
                    "src/malak/security/context_renewer.py",
                    ("SecurityContext",),
                    64,
                ),
                EvidenceSelector(
                    "EXACT_PATH",
                    "src/malak/security/context_propagation.py",
                    ("SecurityContext",),
                    64,
                ),
                EvidenceSelector(
                    "EXACT_PATH",
                    "src/malak/security/pdp.py",
                    ("SecurityContext", "context"),
                    64,
                ),
                EvidenceSelector(
                    "EXACT_PATH",
                    "tests/test_authorization_contracts.py",
                    ("SecurityContext",),
                    64,
                ),
            ),
            knowledge_required_selectors=(
                EvidenceSelector(
                    "EXACT_PATH",
                    "SECURITY.md",
                    ("SecurityContext", "provenance"),
                    64,
                ),
                EvidenceSelector(
                    "EXACT_PATH",
                    "docs/architecture/adr/ADR-002-policy-enforcement-boundary.md",
                    ("provenance", "authenticity"),
                    64,
                ),
                EvidenceSelector(
                    "EXACT_PATH",
                    "docs/project/concepts/GOVERNED_SELF_REVIEW_BOOTSTRAP_TASK.md",
                    ("RR-03", "SecurityContext"),
                    64,
                ),
                EvidenceSelector(
                    "EXACT_PATH",
                    "docs/project/status/MALAK-CONSTRUCTION-FLOW-COMPLIANCE-AUDIT-V1-FINAL.md",
                    ("RR-03", "SecurityContext"),
                    64,
                ),
                EvidenceSelector(
                    "EXACT_PATH",
                    "docs/project/sprints/SPRINT-7.7.md",
                    ("SecurityContext", "provenance"),
                    64,
                ),
                EvidenceSelector(
                    "EXACT_PATH",
                    "docs/project/sprints/SPRINT-7.9.md",
                    ("SecurityContext", "provenance"),
                    64,
                ),
            ),
            supplemental_terms=("SecurityContext", "provenance"),
            supplemental_max_matches_per_kind=12,
            max_evidence_line_bytes=2048,
        ),
    )


def evaluate_bootstrap_focus_completion(
    states: dict[str, str],
) -> BootstrapFocusCompletion:
    if not isinstance(states, dict):
        raise TypeError("states must be a dict")
    expected = ("U01", "U04", "RR-03")
    if set(states) != set(expected):
        raise ValueError("bootstrap focus states must cover U01, U04 and RR-03")
    allowed = {"COMPLETE", "INCONCLUSIVE", "DEFERRED", "NOT_EXECUTED"}
    normalized: dict[str, str] = {}
    for focus_id in expected:
        state = states[focus_id]
        if state not in allowed:
            raise ValueError("invalid bootstrap focus state")
        normalized[focus_id] = state
    return BootstrapFocusCompletion(
        states=normalized,
        complete=all(state == "COMPLETE" for state in normalized.values()),
        authority_effect="none",
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


def _collect_required_selector(
    *,
    source_kind: str,
    selector: EvidenceSelector,
    available_paths: tuple[str, ...],
    repository_reader: GitRepositoryReader,
    knowledge_reader: GovernedKnowledgeReader,
    max_line_bytes: int,
) -> tuple[EvidenceSelectorResult, list[dict[str, object]], int]:
    matched_paths = _resolve_selector_paths(selector, available_paths)
    if not matched_paths:
        return (
            EvidenceSelectorResult(
                source_kind=source_kind,
                selector_kind=selector.kind,
                selector_value=selector.value,
                status="MISSING",
                matched_paths=(),
                match_count=0,
                selected_count=0,
            ),
            [],
            0,
        )

    matches: list[dict[str, object]] = []
    unreadable = 0
    line_truncated = False

    for path in matched_paths:
        try:
            if source_kind == "knowledge":
                document = knowledge_reader.read(path)
                source_class = document.source_class
                authority_class = document.authority_class
            else:
                document = repository_reader.read_text(path)
                source_class = None
                authority_class = None
        except (FileNotFoundError, ValueError):
            unreadable += 1
            continue

        if document.baseline_commit != repository_reader.baseline_commit:
            raise RuntimeError("focused evidence baseline binding changed")
        if document.path != path:
            raise RuntimeError("focused evidence path binding changed")

        for line_number, line in enumerate(document.content.splitlines(), start=1):
            if not any(term in line for term in selector.terms):
                continue
            bounded, was_truncated = truncate_utf8(line, max_line_bytes)
            line_truncated = line_truncated or was_truncated
            item: dict[str, object] = {
                "path": document.path,
                "blob_sha": document.blob_sha,
                "line_number": line_number,
                "line": bounded,
                "line_truncated": was_truncated,
                "required": True,
            }
            if source_class is not None:
                item["source_class"] = source_class
                item["authority_class"] = authority_class
            matches.append(item)

    if unreadable:
        status = "UNREADABLE"
    elif not matches:
        status = "MISSING"
    elif len(matches) > selector.max_matches or line_truncated:
        status = "TRUNCATED"
    else:
        status = "RESOLVED"

    selected = matches[: selector.max_matches]
    return (
        EvidenceSelectorResult(
            source_kind=source_kind,
            selector_kind=selector.kind,
            selector_value=selector.value,
            status=status,
            matched_paths=matched_paths,
            match_count=len(matches),
            selected_count=len(selected),
        ),
        selected,
        unreadable if source_kind == "repository" else 0,
    )


def _resolve_selector_paths(
    selector: EvidenceSelector,
    available_paths: tuple[str, ...],
) -> tuple[str, ...]:
    if selector.kind == "EXACT_PATH":
        return (selector.value,) if selector.value in available_paths else ()
    return tuple(
        path
        for path in available_paths
        if path.startswith(selector.value)
    )


def _strip_ref(
    item: dict[str, object],
    *,
    required: bool,
) -> dict[str, object]:
    stripped = {key: value for key, value in item.items() if key != "ref"}
    stripped["required"] = required
    return stripped


def _canonicalize_evidence(
    items: list[dict[str, object]],
    *,
    prefix: str,
) -> tuple[dict[str, object], ...]:
    ordered = sorted(
        items,
        key=lambda item: (
            str(item["path"]),
            int(item["line_number"]),
            str(item["line"]),
            not bool(item.get("required", False)),
        ),
    )
    seen: set[tuple[str, int, str]] = set()
    result: list[dict[str, object]] = []
    for item in ordered:
        identity = (
            str(item["path"]),
            int(item["line_number"]),
            str(item["line"]),
        )
        if identity in seen:
            continue
        seen.add(identity)
        normalized = dict(item)
        normalized["ref"] = f"{prefix}{len(result) + 1}"
        result.append(normalized)
    return tuple(result)


def _digest_evidence_item(item: dict[str, object]) -> dict[str, object]:
    return {
        key: value
        for key, value in item.items()
        if key != "ref"
    }


def _validate_selector_tuple(
    field: str,
    selectors: object,
) -> None:
    if not isinstance(selectors, tuple):
        raise TypeError(f"{field} must be a tuple")
    seen: set[EvidenceSelector] = set()
    for selector in selectors:
        if not isinstance(selector, EvidenceSelector):
            raise TypeError(f"{field} must contain EvidenceSelector values")
        if selector in seen:
            raise ValueError(f"duplicate selector in {field}")
        seen.add(selector)


def _validate_repo_path(value: object, *, prefix: bool) -> None:
    _validate_text("selector value", value)
    assert isinstance(value, str)
    if value.startswith("/") or "\\" in value:
        raise ValueError("selector value must be a repository-relative POSIX path")
    if any(part in {"", ".", ".."} for part in value.split("/") if not (prefix and part == "")):
        raise ValueError("selector value contains an invalid path segment")
    if prefix and not value.endswith("/"):
        raise ValueError("PATH_PREFIX selector must end with '/'")
    if not prefix and value.endswith("/"):
        raise ValueError("EXACT_PATH selector must not end with '/'")


def _validate_text(field: str, value: object) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{field} must be a string")
    if not value or value != value.strip():
        raise ValueError(f"{field} must be a non-empty trimmed string")
    if any(ord(character) < 32 or ord(character) == 127 for character in value):
        raise ValueError(f"{field} contains forbidden control characters")


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
