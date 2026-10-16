from __future__ import annotations

import json
from functools import partial

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
from malak.runtime.runtime_generation_contract import RuntimeGenerationContract

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
_FOCUSED_SYSTEM_PROMPT = ANALYZE_SYSTEM_PROMPT.replace(
    "summary, findings, uncertainties.", "schema_id, summary, findings, uncertainties.",
) + """
Use schema_id malak.e3.ref-role-map.v1. For each governed relation, select only
needed refs in evidence_roles, with exactly one SUPPORT or LIMIT role per ref.
Omitted refs are not cited and never imply support. Use only the supplied catalog;
never duplicate a JSON key. Do not emit the canonical supporting/limiting lists.
Do not place reserved evidence ref tokens in summary, statement, rationale or
uncertainties. The deterministic adapter projects validated roles to those lists;
all canonical evidence and uncertainty requirements remain enforced.
"""


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
        generation_contract: RuntimeGenerationContract | None = None,
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
        self._generation_contract = generation_contract
        self._evidence_focus = evidence_focus
        self._baseline_commit = repository_reader.baseline_commit

    @property
    def name(self) -> str:
        return "engineering_analyze"

    def execute(self, request: Request) -> str:
        subject = _validate_analysis_subject(request.content)
        governed_relation_ids = (
            tuple(
                relation.relation_id
                for relation in self._evidence_focus.governed_relations
            )
            if self._evidence_focus is not None
            else ()
        )
        analysis_parser = _parse_analysis
        response_json_schema = ANALYZE_RESPONSE_JSON_SCHEMA
        response_json_schema_builder = None
        if governed_relation_ids:
            if len(governed_relation_ids) > _MAX_FINDINGS:
                raise RuntimeError(
                    "governed relation catalog exceeds hard E3 finding limit"
                )
            analysis_parser = partial(
                _parse_analysis,
                allowed_relation_ids=governed_relation_ids,
            )
            response_json_schema = None
            response_json_schema_builder = partial(
                _build_relation_response_json_schema,
                governed_relation_ids,
            )

        result = run_engineering_analysis(
            repository_reader=self._repository_reader,
            knowledge_reader=self._knowledge_reader,
            conversation_service=self._conversation_service,
            provider_name=self._provider_name,
            model=self._model,
            subject=subject,
            system_prompt=(
                _FOCUSED_SYSTEM_PROMPT if governed_relation_ids else _SYSTEM_PROMPT
            ),
            max_repository_files=_MAX_REPOSITORY_FILES,
            max_repository_bytes=_MAX_REPOSITORY_BYTES,
            max_repository_matches=_MAX_REPOSITORY_MATCHES,
            max_context_matches_per_kind=_MAX_CONTEXT_MATCHES_PER_KIND,
            max_evidence_line_bytes=_MAX_EVIDENCE_LINE_BYTES,
            max_prompt_bytes=_MAX_PROMPT_BYTES,
            max_model_output_bytes=_MAX_MODEL_OUTPUT_BYTES,
            error_scope="E3",
            parse_analysis_fn=analysis_parser,
            response_json_schema=response_json_schema,
            response_json_schema_builder=response_json_schema_builder,
            generation_contract=self._generation_contract,
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


def _build_relation_response_json_schema(
    allowed_relation_ids: tuple[str, ...],
    repository_evidence: tuple[dict[str, object], ...],
    knowledge_evidence: tuple[dict[str, object], ...],
) -> str:
    if not allowed_relation_ids:
        return ANALYZE_RESPONSE_JSON_SCHEMA
    if len(set(allowed_relation_ids)) != len(allowed_relation_ids):
        raise ValueError("governed relation ids must be unique")

    repository_refs = [str(item["ref"]) for item in repository_evidence]
    knowledge_refs = [str(item["ref"]) for item in knowledge_evidence]
    all_refs = repository_refs + knowledge_refs
    if len(all_refs) != len(set(all_refs)):
        raise ValueError("focused evidence refs must be unique")

    schema = json.loads(ANALYZE_RESPONSE_JSON_SCHEMA)
    finding = schema["properties"]["findings"]["items"]
    schema["required"] = ["schema_id", "summary", "findings", "uncertainties"]
    schema["properties"]["schema_id"] = {
        "type": "string", "const": "malak.e3.ref-role-map.v1",
    }
    finding["required"] = [
        "relation_id", "classification", "statement", "rationale",
        "evidence_roles", "uncertainty_basis",
    ]
    finding["properties"].pop("evidence_refs")
    finding["properties"]["relation_id"] = {
        "type": "string", "enum": list(allowed_relation_ids),
    }
    finding["properties"]["evidence_roles"] = {
        "type": "object", "additionalProperties": False, "maxProperties": 16,
        "properties": {
            ref: {"type": "string", "enum": ["SUPPORT", "LIMIT"]}
            for ref in all_refs
        },
    }
    finding["properties"]["uncertainty_basis"] = {
        "type": "string",
        "enum": [
            "NONE",
            "CURRENT_MATERIAL_AMBIGUITY",
            "INSUFFICIENT_SUPPLIED_EVIDENCE",
            "UNRESOLVED_CURRENT_PRECEDENCE",
        ],
    }
    schema["properties"]["findings"]["minItems"] = len(allowed_relation_ids)
    schema["properties"]["findings"]["maxItems"] = len(allowed_relation_ids)
    return json.dumps(
        schema,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _parse_analysis(
    raw: str,
    *,
    repository_evidence: list[dict[str, object]],
    knowledge_evidence: list[dict[str, object]],
    allowed_relation_ids: tuple[str, ...] = (),
) -> _Analysis:
    if allowed_relation_ids:
        raw = _project_role_map(raw, repository_evidence, knowledge_evidence)
    return _parse_canonical_analysis(
        raw, repository_evidence=repository_evidence,
        knowledge_evidence=knowledge_evidence, allowed_relation_ids=allowed_relation_ids,
    )


def _project_role_map(
    raw: str,
    repository_evidence: list[dict[str, object]],
    knowledge_evidence: list[dict[str, object]],
) -> str:
    # No autodetección ni reparación del formato anterior.
    if not isinstance(raw, str) or len(raw.encode("utf-8")) > _MAX_MODEL_OUTPUT_BYTES:
        raise RuntimeError("engineering analysis model response exceeds hard UTF-8 byte limit")
    try:
        payload = json.loads(
            raw,
            object_pairs_hook=_reject_duplicate_keys,
            parse_constant=_reject_nonfinite_json,
        )
    except (ValueError, TypeError, RecursionError) as exc:
        raise RuntimeError("engineering analysis model response is not strict JSON") from exc
    if not isinstance(payload, dict):
        raise RuntimeError("engineering analysis JSON must be an object")
    _require_exact_keys(payload, {"schema_id", "summary", "findings", "uncertainties"}, "analysis V1")
    if payload["schema_id"] != "malak.e3.ref-role-map.v1":
        raise RuntimeError("engineering analysis schema_id is not supported")
    repository_refs = [str(item["ref"]) for item in repository_evidence]
    knowledge_refs = [str(item["ref"]) for item in knowledge_evidence]
    all_refs = repository_refs + knowledge_refs
    if len(all_refs) != len(set(all_refs)):
        raise RuntimeError("focused evidence refs must be unique")
    findings = payload["findings"]
    if not isinstance(findings, list) or not 1 <= len(findings) <= _MAX_FINDINGS:
        raise RuntimeError("finding count exceeds hard E3 limit or is empty")

    def wire_text(value: object, field: str, limit: int) -> None:
        _shared_bounded_nonempty_string(
            value, field=field, max_bytes=limit,
            reserved_pattern=r"(?<![A-Za-z0-9_])[RKSA][0-9]+(?![A-Za-z0-9_])",
            limit_scope="E3",
        )

    wire_text(payload["summary"], "summary", _MAX_SUMMARY_BYTES)
    uncertainties = payload["uncertainties"]
    if not isinstance(uncertainties, list) or len(uncertainties) > _MAX_UNCERTAINTIES:
        raise RuntimeError("uncertainties must be a list of at most 16 items")
    for uncertainty in uncertainties:
        wire_text(uncertainty, "uncertainty", _MAX_UNCERTAINTY_BYTES)

    projected = []
    for finding in findings:
        if not isinstance(finding, dict):
            raise RuntimeError("each finding must be an object")
        _require_exact_keys(finding, {
            "relation_id", "classification", "statement", "rationale",
            "evidence_roles", "uncertainty_basis",
        }, "finding V1")
        wire_text(finding["statement"], "finding statement", _MAX_STATEMENT_BYTES)
        wire_text(finding["rationale"], "finding rationale", _MAX_RATIONALE_BYTES)
        roles = finding["evidence_roles"]
        if not isinstance(roles, dict) or len(roles) > _MAX_EVIDENCE_REFS_PER_FINDING:
            raise RuntimeError("evidence_roles must be an object of at most 16 refs")
        unknown = sorted(set(roles) - set(all_refs))
        if unknown:
            raise RuntimeError("evidence_roles contains unknown evidence refs: " + ", ".join(unknown))
        if any(not isinstance(role, str) or role not in {"SUPPORT", "LIMIT"} for role in roles.values()):
            raise RuntimeError("evidence role must be SUPPORT or LIMIT")
        canonical = {key: value for key, value in finding.items() if key != "evidence_roles"}
        canonical["supporting_repository_refs"] = [
            ref for ref in repository_refs if roles.get(ref) == "SUPPORT"
        ]
        canonical["supporting_knowledge_refs"] = [
            ref for ref in knowledge_refs if roles.get(ref) == "SUPPORT"
        ]
        canonical["limiting_or_counterevidence_refs"] = [
            ref for ref in all_refs if roles.get(ref) == "LIMIT"
        ]
        projected.append(canonical)
    return json.dumps({"summary": payload["summary"], "findings": projected,
                       "uncertainties": payload["uncertainties"]},
                      ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _parse_canonical_analysis(
    raw: str,
    *,
    repository_evidence: list[dict[str, object]],
    knowledge_evidence: list[dict[str, object]],
    allowed_relation_ids: tuple[str, ...] = (),
) -> _Analysis:
    analysis = parse_engineering_analysis(
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
        allowed_relation_ids=allowed_relation_ids,
        structured_evidence_roles=bool(allowed_relation_ids),
    )
    if not allowed_relation_ids:
        return analysis

    observed_relation_ids = tuple(
        finding.relation_id for finding in analysis.findings
    )
    if len(observed_relation_ids) != len(allowed_relation_ids):
        raise RuntimeError(
            "focused engineering analysis must cover every governed relation exactly once"
        )
    if len(set(observed_relation_ids)) != len(observed_relation_ids):
        raise RuntimeError(
            "focused engineering analysis contains duplicate governed relations"
        )
    if set(observed_relation_ids) != set(allowed_relation_ids):
        raise RuntimeError(
            "focused engineering analysis relation coverage does not match governed catalog"
        )

    finding_by_relation = {
        finding.relation_id: finding
        for finding in analysis.findings
    }
    return _Analysis(
        summary=analysis.summary,
        findings=tuple(
            finding_by_relation[relation_id]
            for relation_id in allowed_relation_ids
        ),
        uncertainties=analysis.uncertainties,
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
    if any(finding.uncertainty_basis is not None for finding in analysis.findings):
        lines.append("semantic_assurance: NOT_VERIFIED")
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
            finding_lines = [
                f"[A{index}] classification={finding.classification}",
            ]
            if finding.relation_id is not None:
                finding_lines.append(f"relation_id={finding.relation_id}")
            finding_lines.extend(
                (
                    f"statement: {finding.statement}",
                    f"rationale: {finding.rationale}",
                )
            )
            if finding.uncertainty_basis is not None:
                repository_refs = " ".join(
                    f"[{ref}]" for ref in finding.supporting_repository_refs
                ) or "(none)"
                knowledge_refs = " ".join(
                    f"[{ref}]" for ref in finding.supporting_knowledge_refs
                ) or "(none)"
                limiting_refs = " ".join(
                    f"[{ref}]"
                    for ref in finding.limiting_or_counterevidence_refs
                ) or "(none)"
                finding_lines.extend(
                    (
                        f"supporting_repository_refs: {repository_refs}",
                        f"supporting_knowledge_refs: {knowledge_refs}",
                        (
                            "limiting_or_counterevidence_refs: "
                            f"{limiting_refs}"
                        ),
                        f"uncertainty_basis: {finding.uncertainty_basis}",
                    )
                )
            else:
                refs = " ".join(f"[{ref}]" for ref in finding.evidence_refs)
                finding_lines.append(f"evidence_refs: {refs}")
            lines.extend(finding_lines)
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
