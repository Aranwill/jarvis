from __future__ import annotations

from malak.capabilities._engineering_analysis import (
    ANALYZE_RESPONSE_JSON_SCHEMA,
    ANALYZE_SYSTEM_PROMPT,
    _Analysis,
    _Finding,
    bounded_nonempty_string as _shared_bounded_nonempty_string,
    parse_engineering_analysis,
    parse_engineering_finding,
    reject_duplicate_keys as _reject_duplicate_keys,
    reject_nonfinite_json as _reject_nonfinite_json,
    require_exact_keys as _require_exact_keys,
    run_engineering_analysis,
)
from malak.capabilities._engineering_evidence import GovernedEngineeringEvidenceFocus
from malak.contracts.capability import Capability
from malak.core.request import Request
from malak.infrastructure.repository_reader import GitRepositoryReader
from malak.knowledge.knowledge_reader import GovernedKnowledgeReader
from malak.services.conversation_service import ConversationService

_MAX_ANALYSIS_SUBJECT_BYTES = 512
_MAX_REPOSITORY_FILES = 512
_MAX_REPOSITORY_BYTES = 8 * 1024 * 1024
_MAX_REPOSITORY_MATCHES = 1000
_MAX_CONTEXT_MATCHES_PER_KIND = 12
_MAX_EVIDENCE_LINE_BYTES = 2048
_MAX_PROMPT_BYTES = 64 * 1024
_MAX_MODEL_OUTPUT_BYTES = 64 * 1024

_MAX_SUMMARY_BYTES = 8 * 1024
_MAX_FINDINGS = 16
_MAX_STATEMENT_BYTES = 4 * 1024
_MAX_RATIONALE_BYTES = 8 * 1024
_MAX_EVIDENCE_REFS_PER_FINDING = 16
_MAX_UNCERTAINTIES = 16
_MAX_UNCERTAINTY_BYTES = 4 * 1024

_RELATIONAL_CLASSES = {"ALIGNED", "PARTIAL", "GAP", "CONTRADICTION"}
_ALLOWED_CLASSES = _RELATIONAL_CLASSES | {"UNRESOLVED"}

_SYSTEM_PROMPT = ANALYZE_SYSTEM_PROMPT


class EngineeringAnalyzeCapability(Capability):
    """Grounded read-only comparison of implementation and governed knowledge."""

    def __init__(
        self,
        *,
        repository_reader: GitRepositoryReader,
        knowledge_reader: GovernedKnowledgeReader,
        conversation_service: ConversationService,
        provider_name: str,
        model: str | None = None,
        evidence_focus: GovernedEngineeringEvidenceFocus | None = None,
    ) -> None:
        if repository_reader.baseline_commit != knowledge_reader.baseline_commit:
            raise RuntimeError(
                "repository and knowledge readers must share the same baseline"
            )
        if not isinstance(provider_name, str) or not provider_name.strip():
            raise ValueError("provider_name must be a non-empty string")

        self._repository_reader = repository_reader
        self._knowledge_reader = knowledge_reader
        self._conversation_service = conversation_service
        self._provider_name = provider_name
        self._model = model
        self._evidence_focus = evidence_focus
        self._baseline_commit = repository_reader.baseline_commit

    @property
    def name(self) -> str:
        return "engineering_analyze"

    def execute(self, request: Request) -> str:
        subject = _validate_analysis_subject(request.content)
        result = run_engineering_analysis(
            repository_reader=self._repository_reader,
            knowledge_reader=self._knowledge_reader,
            conversation_service=self._conversation_service,
            provider_name=self._provider_name,
            model=self._model,
            subject=subject,
            system_prompt=_SYSTEM_PROMPT,
            max_repository_files=_MAX_REPOSITORY_FILES,
            max_repository_bytes=_MAX_REPOSITORY_BYTES,
            max_repository_matches=_MAX_REPOSITORY_MATCHES,
            max_context_matches_per_kind=_MAX_CONTEXT_MATCHES_PER_KIND,
            max_evidence_line_bytes=_MAX_EVIDENCE_LINE_BYTES,
            max_prompt_bytes=_MAX_PROMPT_BYTES,
            max_model_output_bytes=_MAX_MODEL_OUTPUT_BYTES,
            error_scope="E3",
            parse_analysis_fn=_parse_analysis,
            response_json_schema=ANALYZE_RESPONSE_JSON_SCHEMA,
            evidence_focus=self._evidence_focus,
        )

        repository_evidence = list(result.repository_evidence)
        knowledge_evidence = list(result.knowledge_evidence)

        if result.status == "UNCONFIRMED":
            return _render_unconfirmed(
                baseline_commit=self._baseline_commit,
                analysis_subject=subject,
                repository_evidence_count=len(repository_evidence),
                knowledge_evidence_count=len(knowledge_evidence),
                repository_skipped_unreadable=result.repository_skipped_unreadable,
                context_truncated=result.context_truncated,
                reason=result.reason or "analysis is unconfirmed",
                focus_id=result.focus_id,
                focus_complete=result.focus_complete,
                evidence_set_digest=result.evidence_set_digest,
                supplemental_truncated=result.supplemental_truncated,
            )

        if result.analysis is None:
            raise RuntimeError("grounded engineering analysis is missing")

        return _render_grounded(
            baseline_commit=self._baseline_commit,
            analysis_subject=subject,
            analysis=result.analysis,
            repository_evidence=repository_evidence,
            knowledge_evidence=knowledge_evidence,
            repository_skipped_unreadable=result.repository_skipped_unreadable,
            context_truncated=result.context_truncated,
            focus_id=result.focus_id,
            focus_complete=result.focus_complete,
            evidence_set_digest=result.evidence_set_digest,
            supplemental_truncated=result.supplemental_truncated,
        )


def _validate_analysis_subject(content: str) -> str:
    if not isinstance(content, str):
        raise TypeError("analysis subject must be a string")

    subject = content.strip()
    if not subject:
        raise ValueError("analysis subject cannot be empty")
    if any(ord(character) < 32 or ord(character) == 127 for character in subject):
        raise ValueError("analysis subject contains forbidden control characters")
    if len(subject.encode("utf-8")) > _MAX_ANALYSIS_SUBJECT_BYTES:
        raise ValueError("analysis subject exceeds the hard E3 UTF-8 byte limit")
    return subject


def _parse_analysis(
    raw: str,
    *,
    repository_evidence: list[dict[str, object]],
    knowledge_evidence: list[dict[str, object]],
) -> _Analysis:
    return parse_engineering_analysis(
        raw,
        repository_evidence=repository_evidence,
        knowledge_evidence=knowledge_evidence,
        max_summary_bytes=_MAX_SUMMARY_BYTES,
        max_findings=_MAX_FINDINGS,
        max_statement_bytes=_MAX_STATEMENT_BYTES,
        max_rationale_bytes=_MAX_RATIONALE_BYTES,
        max_evidence_refs_per_finding=_MAX_EVIDENCE_REFS_PER_FINDING,
        max_uncertainties=_MAX_UNCERTAINTIES,
        max_uncertainty_bytes=_MAX_UNCERTAINTY_BYTES,
    )


def _parse_finding(
    payload: object,
    *,
    allowed_refs: set[str],
) -> _Finding:
    return parse_engineering_finding(
        payload,
        allowed_refs=allowed_refs,
        max_statement_bytes=_MAX_STATEMENT_BYTES,
        max_rationale_bytes=_MAX_RATIONALE_BYTES,
        max_evidence_refs=_MAX_EVIDENCE_REFS_PER_FINDING,
    )


def _bounded_nonempty_string(
    value: object,
    *,
    field: str,
    max_bytes: int,
) -> str:
    return _shared_bounded_nonempty_string(
        value,
        field=field,
        max_bytes=max_bytes,
        reserved_pattern=r"\[[RKA][0-9]+\]",
        limit_scope="E3",
    )


def _render_unconfirmed(
    *,
    baseline_commit: str,
    analysis_subject: str,
    repository_evidence_count: int,
    knowledge_evidence_count: int,
    repository_skipped_unreadable: int,
    context_truncated: bool,
    reason: str,
    focus_id: str | None = None,
    focus_complete: bool | None = None,
    evidence_set_digest: str | None = None,
    supplemental_truncated: bool = False,
) -> str:
    lines = [
        "ENGINEERING_ANALYSIS",
        f"baseline_commit: {baseline_commit}",
        f"analysis_subject: {analysis_subject}",
        "status: UNCONFIRMED",
        f"repository_evidence_count: {repository_evidence_count}",
        f"knowledge_evidence_count: {knowledge_evidence_count}",
        f"repository_skipped_unreadable: {repository_skipped_unreadable}",
        f"context_truncated: {str(context_truncated).lower()}",
    ]
    if focus_id is not None:
        lines.extend(
            (
                f"focus_id: {focus_id}",
                f"focus_complete: {str(bool(focus_complete)).lower()}",
                f"evidence_set_digest: {evidence_set_digest}",
                f"supplemental_truncated: {str(supplemental_truncated).lower()}",
            )
        )
    lines.extend(
        (
            "authority_effect: none",
            f"reason: {reason}",
            "",
            "FINDINGS",
            "(none)",
            "",
            "EVIDENCE_REFERENCES",
            "(none)",
        )
    )
    return "\n".join(lines)


def _render_grounded(
    *,
    baseline_commit: str,
    analysis_subject: str,
    analysis: _Analysis,
    repository_evidence: list[dict[str, object]],
    knowledge_evidence: list[dict[str, object]],
    repository_skipped_unreadable: int,
    context_truncated: bool,
    focus_id: str | None = None,
    focus_complete: bool | None = None,
    evidence_set_digest: str | None = None,
    supplemental_truncated: bool = False,
) -> str:
    lines = [
        "ENGINEERING_ANALYSIS",
        f"baseline_commit: {baseline_commit}",
        f"analysis_subject: {analysis_subject}",
        "status: GROUNDED",
        f"finding_count: {len(analysis.findings)}",
        f"repository_evidence_count: {len(repository_evidence)}",
        f"knowledge_evidence_count: {len(knowledge_evidence)}",
        f"repository_skipped_unreadable: {repository_skipped_unreadable}",
        f"context_truncated: {str(context_truncated).lower()}",
    ]
    if focus_id is not None:
        lines.extend(
            (
                f"focus_id: {focus_id}",
                f"focus_complete: {str(bool(focus_complete)).lower()}",
                f"evidence_set_digest: {evidence_set_digest}",
                f"supplemental_truncated: {str(supplemental_truncated).lower()}",
            )
        )
    lines.extend(
        [
        "authority_effect: none",
        "",
        "SUMMARY",
        analysis.summary,
        "",
        "FINDINGS",
        ]
    )

    if analysis.findings:
        for index, finding in enumerate(analysis.findings, start=1):
            refs = " ".join(f"[{ref}]" for ref in finding.evidence_refs)
            lines.extend(
                (
                    f"[A{index}] classification={finding.classification}",
                    f"statement: {finding.statement}",
                    f"rationale: {finding.rationale}",
                    f"evidence_refs: {refs}",
                )
            )
    else:
        lines.append("(none)")

    lines.extend(("", "UNCERTAINTIES"))
    if analysis.uncertainties:
        lines.extend(f"- {item}" for item in analysis.uncertainties)
    else:
        lines.append("(none)")

    lines.extend(("", "EVIDENCE_REFERENCES"))
    for item in repository_evidence:
        lines.append(
            "[{ref}] path={path} blob_sha={blob_sha} line={line_number}".format(
                **item
            )
        )
    for item in knowledge_evidence:
        lines.append(
            (
                "[{ref}] path={path} blob_sha={blob_sha} "
                "source_class={source_class} authority_class={authority_class} "
                "line={line_number}"
            ).format(**item)
        )

    return "\n".join(lines)
