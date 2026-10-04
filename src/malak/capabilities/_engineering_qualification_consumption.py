from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import hashlib
import json
from pathlib import Path
import unicodedata
from typing import Any

from malak.capabilities._engineering_analysis import (
    GovernedDeterministicOracleContractV0,
    GovernedSupportEvidenceRouteKind,
    GovernedSupportEvidenceRouteReason,
    GovernedSupportEvidenceRoutingV0,
    _evaluate_governed_support_evidence_structural_v0,
    _routing_result,
)
from malak.security.audit import AuthorizationAuditSink
from malak.security.clock import Clock
from malak.security.contracts import (
    AuthorizationOperationBinding,
    AuthorizationRequest,
    HumanConfirmationEvidence,
    PermissionScope,
    SecurityContext,
)
from malak.security.pdp import PolicyDecisionPoint
from malak.security.pep import (
    AuthorizationDeniedError,
    AuthorizationEnforcementError,
    StrictPolicyEnforcementPoint,
)


_BUNDLE_SCHEMA = "MALAK-E3-DETERMINISTIC-ORACLE-QUALIFICATION-BUNDLE/v0"
_REVIEW_SCHEMA = "MALAK-E3-DETERMINISTIC-ORACLE-QUALIFICATION-REVIEW-EVIDENCE/v0"
_QUALIFICATION_METHOD = "INDEPENDENT_REVIEWED_DETERMINISTIC_COVERAGE"
_RUNNER_VERSION = "e3-deterministic-oracle-qualification/v0"
_EXPECTED_RUNNER_DIGEST = "0592d70456ea3e44378500c5ad6bb3af2e4eeae89638f2e45c0d9dfa809994ef"
_ADMISSION_SCHEMA = "QUALIFICATION_REVIEW_ADMISSION_BINDING/v0"
_RESULTS = {"PASS", "FAIL", "INCONCLUSIVE"}
_MAX_OBLIGATIONS = 32
_MAX_OBLIGATION_STATEMENT_BYTES = 4 * 1024
_MAX_VERIFICATION_REFS_PER_OBLIGATION = 16
_MAX_REVIEW_REFERENCES = _MAX_OBLIGATIONS * _MAX_VERIFICATION_REFS_PER_OBLIGATION
_MAX_ARTIFACT_BYTES = 512 * 1024
_MAX_TEXT_BYTES = 4 * 1024

_BUNDLE_KEYS = {
    "schema_version",
    "repository",
    "evaluated_candidate_commit",
    "oracle_identity",
    "governed_question_material",
    "obligation_catalog",
    "obligation_catalog_digest",
    "coverage_entries",
    "verification_evidence",
    "verification_evidence_digest",
    "qualification_material",
    "qualification_material_digest",
}
_ORACLE_KEYS = {
    "oracle_id",
    "oracle_version",
    "oracle_content_digest",
    "oracle_producer_subject_id",
}
_QUESTION_KEYS = {
    "relation_id",
    "evaluation_question_identity",
    "input_contract_identity",
    "output_contract_identity",
}
_OBLIGATION_KEYS = {
    "obligation_id",
    "obligation_statement",
    "obligation_identity",
}
_COVERAGE_ENTRY_KEYS = {
    "obligation_id",
    "obligation_identity",
    "oracle_check_id",
    "oracle_check_identity",
    "oracle_check_contract_digest",
    "verification_evidence_refs",
    "entry_result",
    "entry_reasons",
}
_VERIFICATION_EVIDENCE_KEYS = {
    "evidence_id",
    "evidence_kind",
    "content_digest",
    "content_or_bounded_material",
    "candidate_binding",
}
_QUALIFICATION_MATERIAL_KEYS = {
    "qualification_method",
    "executing_runner_version",
    "executing_runner_digest",
}
_REVIEW_KEYS = {
    "schema_version",
    "repository",
    "evaluated_candidate_commit",
    "qualification_bundle_digest",
    "reviewed_relation_id",
    "reviewed_evaluation_question_identity",
    "reviewed_obligation_catalog_digest",
    "implementation_actor_id",
    "qualification_reviewer_id",
    "qualification_validator_id",
    "structural_validator_result",
    "structural_validator_evidence_reference",
    "catalog_completeness_result",
    "independence_review_result",
    "verification_material_review_result",
    "qualification_review_result",
    "finding_refs",
    "evidence_references",
    "authority_effect",
}

_ADMISSION_PERMISSION = PermissionScope(
    resource="engineering.qualification_review_consumption",
    action="admit",
)


class GovernedQualificationReviewAdmissionOutcome(str, Enum):
    READY = "READY"
    HOLD = "HOLD"
    DENIED = "DENIED"


@dataclass(frozen=True, slots=True)
class RuntimeQualificationBindingV0:
    repository: str
    evaluated_candidate_commit: str
    oracle_id: str
    oracle_version: str
    oracle_content_digest: str
    relation_id: str
    evaluation_question_identity: str
    input_contract_identity: str
    output_contract_identity: str
    coverage_claim: str
    oracle_producer_subject_id: str
    qualifier_subject_id: str
    qualification_evidence_digest: str
    qualification_identity: str
    authority_effect: str = "none"


@dataclass(frozen=True, slots=True)
class RuntimeQualificationBindingKeyV0:
    binding: RuntimeQualificationBindingV0


@dataclass(frozen=True, slots=True)
class AdmissionInstanceKeyV0:
    runtime_binding_key: RuntimeQualificationBindingKeyV0
    qualification_bundle_digest: str
    review_evidence_digest: str
    authorization_context_id: str
    authorization_request_id: str
    authorization_operation_binding_digest: str


@dataclass(frozen=True, slots=True)
class GovernedQualificationReviewAdmissionV0:
    outcome: GovernedQualificationReviewAdmissionOutcome
    reason_code: str
    runtime_binding: RuntimeQualificationBindingV0 | None
    runtime_binding_key: RuntimeQualificationBindingKeyV0 | None
    qualification_bundle_digest: str | None
    review_evidence_digest: str | None
    authorization_context: SecurityContext
    authorization_request_id: str | None = None
    authorization_request_created_at: datetime | None = None
    authorization_operation_binding: AuthorizationOperationBinding | None = None
    admission_evaluated_at: datetime | None = None
    instance_key: AdmissionInstanceKeyV0 | None = None
    authority_effect: str = "none"


@dataclass(frozen=True, slots=True)
class GovernedQualificationReviewAdmissionOperationV0:
    runtime_binding: RuntimeQualificationBindingV0
    authorization_binding: AuthorizationOperationBinding
    required_permission: PermissionScope = _ADMISSION_PERMISSION

    def execute(self) -> RuntimeQualificationBindingV0:
        return self.runtime_binding


@dataclass(frozen=True, slots=True)
class GovernedQualificationConsumptionBoundaryV0:
    expected_repository: str
    expected_candidate_commit: str
    clock: Clock
    admissions: tuple[GovernedQualificationReviewAdmissionV0, ...]

    def route(
        self,
        *,
        policy_version: str,
        baseline_commit: str,
        focus_id: str,
        evidence_set_digest: str,
        relation_id: str,
        evaluation_question_identity: str,
        finding_fingerprint: str,
        resolved_evidence_material_digest: str,
        declared_evidence_complete: bool,
        scope_expansion_required: bool,
        oracles,
        expected_binding=None,
    ) -> GovernedSupportEvidenceRoutingV0:
        structural = _evaluate_governed_support_evidence_structural_v0(
            policy_version=policy_version,
            baseline_commit=baseline_commit,
            focus_id=focus_id,
            evidence_set_digest=evidence_set_digest,
            relation_id=relation_id,
            evaluation_question_identity=evaluation_question_identity,
            finding_fingerprint=finding_fingerprint,
            resolved_evidence_material_digest=resolved_evidence_material_digest,
            declared_evidence_complete=declared_evidence_complete,
            scope_expansion_required=scope_expansion_required,
            oracles=oracles,
            expected_binding=expected_binding,
        )
        result = structural.result
        oracle = structural.selected_oracle
        if (
            oracle is None
            or result.reason_code
            is not GovernedSupportEvidenceRouteReason.INFERENTIAL_RESIDUAL
        ):
            return result
        if baseline_commit != self.expected_candidate_commit:
            return result

        runtime_binding = _runtime_binding_from_oracle(
            oracle,
            repository=self.expected_repository,
            candidate_commit=self.expected_candidate_commit,
        )
        if runtime_binding is None:
            return result
        runtime_key = RuntimeQualificationBindingKeyV0(runtime_binding)
        matches = tuple(
            admission
            for admission in self.admissions
            if admission.runtime_binding_key == runtime_key
        )
        if len(matches) > 1:
            return _routing_result(
                _routing_subject(
                    policy_version=policy_version,
                    baseline_commit=baseline_commit,
                    focus_id=focus_id,
                    evidence_set_digest=evidence_set_digest,
                    relation_id=relation_id,
                    evaluation_question_identity=evaluation_question_identity,
                    finding_fingerprint=finding_fingerprint,
                    resolved_evidence_material_digest=resolved_evidence_material_digest,
                ),
                GovernedSupportEvidenceRouteKind.INFERENTIAL,
                GovernedSupportEvidenceRouteReason.ADMISSION_AMBIGUOUS,
            )
        if len(matches) != 1:
            return result

        admission = matches[0]
        if admission.outcome is not GovernedQualificationReviewAdmissionOutcome.READY:
            return result
        if (
            admission.admission_evaluated_at is None
            or admission.authorization_operation_binding is None
        ):
            return result

        consume_at = _safe_clock_now(self.clock)
        subject = _routing_subject(
            policy_version=policy_version,
            baseline_commit=baseline_commit,
            focus_id=focus_id,
            evidence_set_digest=evidence_set_digest,
            relation_id=relation_id,
            evaluation_question_identity=evaluation_question_identity,
            finding_fingerprint=finding_fingerprint,
            resolved_evidence_material_digest=resolved_evidence_material_digest,
        )
        if consume_at is None:
            return _routing_result(
                subject,
                GovernedSupportEvidenceRouteKind.INFERENTIAL,
                GovernedSupportEvidenceRouteReason.CLOCK_INVALID,
            )
        if consume_at < admission.admission_evaluated_at:
            return _routing_result(
                subject,
                GovernedSupportEvidenceRouteKind.INFERENTIAL,
                GovernedSupportEvidenceRouteReason.CLOCK_REVERSED,
            )
        context = admission.authorization_context
        if consume_at < context.issued_at:
            return _routing_result(
                subject,
                GovernedSupportEvidenceRouteKind.INFERENTIAL,
                GovernedSupportEvidenceRouteReason.CLOCK_REVERSED,
            )
        if consume_at >= context.expires_at:
            return _routing_result(
                subject,
                GovernedSupportEvidenceRouteKind.INFERENTIAL,
                GovernedSupportEvidenceRouteReason.ADMISSION_STALE,
            )
        return _routing_result(
            subject,
            GovernedSupportEvidenceRouteKind.DETERMINISTIC,
            GovernedSupportEvidenceRouteReason.DETERMINISTIC_ORACLE_ELIGIBLE,
            selected_oracle_id=oracle.oracle_id,
        )


@dataclass(frozen=True, slots=True)
class _AdmissionValidation:
    outcome: GovernedQualificationReviewAdmissionOutcome
    reason_code: str
    runtime_binding: RuntimeQualificationBindingV0 | None
    qualification_bundle_digest: str | None
    review_evidence_digest: str | None
    operation_payload: dict[str, Any] | None


def _canonical_json(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _sha256(value: object) -> str:
    return hashlib.sha256(_canonical_json(value)).hexdigest()


def _safe_canonical_bytes(value: object) -> bytes | None:
    try:
        return _canonical_json(value)
    except (TypeError, ValueError, RecursionError):
        return None


def _safe_sha256(value: object) -> str | None:
    material = _safe_canonical_bytes(value)
    if material is None:
        return None
    return hashlib.sha256(material).hexdigest()


def _is_sha(value: object, length: int) -> bool:
    return (
        isinstance(value, str)
        and len(value) == length
        and all(character in "0123456789abcdef" for character in value)
    )


def _bounded_text(value: object, *, max_bytes: int = _MAX_TEXT_BYTES) -> bool:
    return (
        isinstance(value, str)
        and bool(value.strip())
        and len(value) <= max_bytes
        and len(value.encode("utf-8")) <= max_bytes
        and not any(
            unicodedata.category(character) in {"Cc", "Cf", "Zl", "Zp"}
            for character in value
        )
    )


def _within_artifact_bound(value: object) -> bool:
    material = _safe_canonical_bytes(value)
    return material is not None and len(material) <= _MAX_ARTIFACT_BYTES


def _safe_clock_now(clock: Clock) -> datetime | None:
    try:
        value = clock.now()
    except Exception:
        return None
    if not isinstance(value, datetime):
        return None
    if value.tzinfo is None or value.utcoffset() is None:
        return None
    return value


def _runner_bytes() -> bytes | None:
    runner = (
        Path(__file__).resolve().parents[3]
        / "scripts"
        / "evaluate_e3_deterministic_oracle_qualification.py"
    )
    try:
        return runner.read_bytes()
    except OSError:
        return None


def _runner_contract_digests() -> frozenset[str]:
    raw = _runner_bytes()
    if raw is None:
        return frozenset()

    # Git stores the canonical source with LF. Windows worktrees may expose
    # the exact same source as CRLF. Normalize first to verify the V0 contract,
    # then admit only the two byte encodings that the current runner itself
    # can report through its read_bytes()-based executing_runner_digest.
    normalized = raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    canonical_digest = hashlib.sha256(normalized).hexdigest()
    if canonical_digest != _EXPECTED_RUNNER_DIGEST:
        return frozenset()

    crlf = normalized.replace(b"\n", b"\r\n")
    return frozenset(
        {
            canonical_digest,
            hashlib.sha256(crlf).hexdigest(),
        }
    )


def _qualification_identity_material(
    *,
    oracle_id: str,
    oracle_version: str,
    oracle_content_digest: str,
    relation_id: str,
    evaluation_question_identity: str,
    input_contract_identity: str,
    output_contract_identity: str,
    coverage_claim: str,
    oracle_producer_subject_id: str,
    qualifier_subject_id: str,
    qualification_evidence_digest: str,
) -> str:
    material = {
        "coverage_claim": coverage_claim,
        "evaluation_question_identity": evaluation_question_identity,
        "input_contract_identity": input_contract_identity,
        "oracle_content_digest": oracle_content_digest,
        "oracle_id": oracle_id,
        "oracle_producer_subject_id": oracle_producer_subject_id,
        "oracle_version": oracle_version,
        "output_contract_identity": output_contract_identity,
        "qualification_evidence_digest": qualification_evidence_digest,
        "qualifier_subject_id": qualifier_subject_id,
        "relation_id": relation_id,
    }
    return _sha256(material)


def _runtime_binding_from_material(
    bundle: dict[str, Any],
    review: dict[str, Any],
    bundle_digest: str,
) -> RuntimeQualificationBindingV0 | None:
    oracle = bundle.get("oracle_identity")
    question = bundle.get("governed_question_material")
    if not isinstance(oracle, dict) or not isinstance(question, dict):
        return None
    reviewer = review.get("qualification_reviewer_id")
    if not _bounded_text(reviewer):
        return None
    try:
        identity = _qualification_identity_material(
            oracle_id=oracle["oracle_id"],
            oracle_version=oracle["oracle_version"],
            oracle_content_digest=oracle["oracle_content_digest"],
            relation_id=question["relation_id"],
            evaluation_question_identity=question["evaluation_question_identity"],
            input_contract_identity=question["input_contract_identity"],
            output_contract_identity=question["output_contract_identity"],
            coverage_claim="FULL",
            oracle_producer_subject_id=oracle["oracle_producer_subject_id"],
            qualifier_subject_id=reviewer,
            qualification_evidence_digest=bundle_digest,
        )
        return RuntimeQualificationBindingV0(
            repository=bundle["repository"],
            evaluated_candidate_commit=bundle["evaluated_candidate_commit"],
            oracle_id=oracle["oracle_id"],
            oracle_version=oracle["oracle_version"],
            oracle_content_digest=oracle["oracle_content_digest"],
            relation_id=question["relation_id"],
            evaluation_question_identity=question["evaluation_question_identity"],
            input_contract_identity=question["input_contract_identity"],
            output_contract_identity=question["output_contract_identity"],
            coverage_claim="FULL",
            oracle_producer_subject_id=oracle["oracle_producer_subject_id"],
            qualifier_subject_id=reviewer,
            qualification_evidence_digest=bundle_digest,
            qualification_identity=identity,
        )
    except (KeyError, TypeError, ValueError):
        return None


def _runtime_binding_from_oracle(
    oracle: GovernedDeterministicOracleContractV0,
    *,
    repository: str,
    candidate_commit: str,
) -> RuntimeQualificationBindingV0 | None:
    qualification = oracle.qualification
    expected_identity = _qualification_identity_material(
        oracle_id=qualification.oracle_id,
        oracle_version=qualification.oracle_version,
        oracle_content_digest=qualification.oracle_content_digest,
        relation_id=qualification.relation_id,
        evaluation_question_identity=qualification.evaluation_question_identity,
        input_contract_identity=qualification.input_contract_identity,
        output_contract_identity=qualification.output_contract_identity,
        coverage_claim=qualification.coverage_claim,
        oracle_producer_subject_id=qualification.oracle_producer_subject_id,
        qualifier_subject_id=qualification.qualifier_subject_id,
        qualification_evidence_digest=qualification.qualification_evidence_digest,
    )
    if (
        qualification.coverage_claim != "FULL"
        or qualification.authority_effect != "none"
        or oracle.authority_effect != "none"
        or expected_identity != qualification.qualification_identity
        or expected_identity != oracle.qualification_identity
    ):
        return None
    return RuntimeQualificationBindingV0(
        repository=repository,
        evaluated_candidate_commit=candidate_commit,
        oracle_id=qualification.oracle_id,
        oracle_version=qualification.oracle_version,
        oracle_content_digest=qualification.oracle_content_digest,
        relation_id=qualification.relation_id,
        evaluation_question_identity=qualification.evaluation_question_identity,
        input_contract_identity=qualification.input_contract_identity,
        output_contract_identity=qualification.output_contract_identity,
        coverage_claim=qualification.coverage_claim,
        oracle_producer_subject_id=qualification.oracle_producer_subject_id,
        qualifier_subject_id=qualification.qualifier_subject_id,
        qualification_evidence_digest=qualification.qualification_evidence_digest,
        qualification_identity=expected_identity,
    )


# This block intentionally mirrors the bounded deterministic qualification
# runner's catalog/evidence/coverage invariants for admission-time consumption.
# The runner remains the canonical producer/evaluator; this boundary rechecks
# caller-supplied material fail-closed before positive reliance. Any runner
# schema/semantic change requires a new runner digest and affected revalidation.
#
def _validate_catalog(
    bundle: dict[str, Any],
    question: dict[str, Any],
) -> tuple[dict[str, dict[str, str]] | None, str | None]:
    catalog = bundle["obligation_catalog"]
    if not isinstance(catalog, list) or not catalog:
        return None, "OBLIGATION_CATALOG_INVALID"
    if len(catalog) > _MAX_OBLIGATIONS:
        return None, "OBLIGATION_CATALOG_OUT_OF_BOUNDS"

    by_id: dict[str, dict[str, str]] = {}
    identities: set[str] = set()
    for item in catalog:
        if not isinstance(item, dict) or set(item) != _OBLIGATION_KEYS:
            return None, "OBLIGATION_SCHEMA_INVALID"
        obligation_id = item["obligation_id"]
        statement = item["obligation_statement"]
        identity = item["obligation_identity"]
        if not _bounded_text(obligation_id):
            return None, "OBLIGATION_ID_INVALID"
        if str(obligation_id).lower() in {"other", "*"}:
            return None, "OBLIGATION_CATCH_ALL_FORBIDDEN"
        if not _bounded_text(
            statement,
            max_bytes=_MAX_OBLIGATION_STATEMENT_BYTES,
        ):
            return None, "OBLIGATION_STATEMENT_INVALID"
        if not _is_sha(identity, 64):
            return None, "OBLIGATION_IDENTITY_INVALID"
        if obligation_id in by_id or identity in identities:
            return None, "OBLIGATION_DUPLICATE"
        expected_identity = _sha256(
            {
                "relation_id": question["relation_id"],
                "evaluation_question_identity": question[
                    "evaluation_question_identity"
                ],
                "obligation_id": obligation_id,
                "obligation_statement": statement,
            }
        )
        if identity != expected_identity:
            return None, "OBLIGATION_IDENTITY_MISMATCH"
        by_id[str(obligation_id)] = {
            "obligation_id": str(obligation_id),
            "obligation_statement": str(statement),
            "obligation_identity": str(identity),
        }
        identities.add(str(identity))

    if bundle["obligation_catalog_digest"] != _sha256(catalog):
        return None, "OBLIGATION_CATALOG_DIGEST_MISMATCH"
    return by_id, None


def _validate_verification_evidence(
    bundle: dict[str, Any],
) -> tuple[set[str] | None, str | None]:
    items = bundle["verification_evidence"]
    if not isinstance(items, list) or not items:
        return None, "VERIFICATION_EVIDENCE_INVALID"
    evidence_digest = _safe_sha256(items)
    if evidence_digest is None:
        return None, "VERIFICATION_EVIDENCE_MATERIAL_INVALID"
    if bundle["verification_evidence_digest"] != evidence_digest:
        return None, "VERIFICATION_EVIDENCE_DIGEST_MISMATCH"

    candidate = bundle["evaluated_candidate_commit"]
    evidence_ids: set[str] = set()
    for item in items:
        if not isinstance(item, dict) or set(item) != _VERIFICATION_EVIDENCE_KEYS:
            return None, "VERIFICATION_EVIDENCE_SCHEMA_INVALID"
        evidence_id = item["evidence_id"]
        if not _bounded_text(evidence_id) or evidence_id in evidence_ids:
            return None, "VERIFICATION_EVIDENCE_ID_INVALID"
        if not _bounded_text(item["evidence_kind"]):
            return None, "VERIFICATION_EVIDENCE_KIND_INVALID"
        if not _is_sha(item["content_digest"], 64):
            return None, "VERIFICATION_EVIDENCE_CONTENT_DIGEST_INVALID"
        content_digest = _safe_sha256(item["content_or_bounded_material"])
        if content_digest is None:
            return None, "VERIFICATION_EVIDENCE_CONTENT_INVALID"
        if item["content_digest"] != content_digest:
            return None, "VERIFICATION_EVIDENCE_CONTENT_DIGEST_MISMATCH"
        if item["candidate_binding"] != candidate:
            return None, "VERIFICATION_EVIDENCE_CANDIDATE_MISMATCH"
        evidence_ids.add(str(evidence_id))
    return evidence_ids, None


def _validate_coverage(
    *,
    bundle: dict[str, Any],
    oracle: dict[str, Any],
    question: dict[str, Any],
    catalog_by_id: dict[str, dict[str, str]],
    evidence_ids: set[str],
) -> tuple[str | None, str | None]:
    entries = bundle["coverage_entries"]
    if not isinstance(entries, list):
        return None, "COVERAGE_ENTRIES_INVALID"
    if len(entries) != len(catalog_by_id) or len(entries) > _MAX_OBLIGATIONS:
        return None, "COVERAGE_CARDINALITY_MISMATCH"

    seen_ids: set[str] = set()
    outcomes: list[str] = []
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != _COVERAGE_ENTRY_KEYS:
            return None, "COVERAGE_ENTRY_SCHEMA_INVALID"
        obligation_id = entry["obligation_id"]
        obligation_identity = entry["obligation_identity"]
        check_id = entry["oracle_check_id"]
        check_identity = entry["oracle_check_identity"]
        check_contract_digest = entry["oracle_check_contract_digest"]
        refs = entry["verification_evidence_refs"]
        entry_result = entry["entry_result"]
        entry_reasons = entry["entry_reasons"]

        if not _bounded_text(obligation_id) or obligation_id in seen_ids:
            return None, "COVERAGE_OBLIGATION_DUPLICATE_OR_INVALID"
        if obligation_id not in catalog_by_id:
            return None, "COVERAGE_OBLIGATION_UNKNOWN"
        if (
            obligation_identity
            != catalog_by_id[str(obligation_id)]["obligation_identity"]
        ):
            return None, "COVERAGE_OBLIGATION_IDENTITY_MISMATCH"
        if not _bounded_text(check_id):
            return None, "ORACLE_CHECK_ID_INVALID"
        if not _is_sha(check_identity, 64):
            return None, "ORACLE_CHECK_IDENTITY_INVALID"
        if not _is_sha(check_contract_digest, 64):
            return None, "ORACLE_CHECK_CONTRACT_DIGEST_INVALID"
        if check_identity != _sha256(
            {
                "oracle_id": oracle["oracle_id"],
                "oracle_version": oracle["oracle_version"],
                "check_id": check_id,
            }
        ):
            return None, "ORACLE_CHECK_IDENTITY_MISMATCH"
        if check_contract_digest != _sha256(
            {
                "check_id": check_id,
                "input_contract_identity": question["input_contract_identity"],
                "output_contract_identity": question["output_contract_identity"],
            }
        ):
            return None, "ORACLE_CHECK_CONTRACT_MISMATCH"
        if not isinstance(refs, list):
            return None, "VERIFICATION_EVIDENCE_REFS_INVALID"
        if not refs or len(refs) > _MAX_VERIFICATION_REFS_PER_OBLIGATION:
            return None, "VERIFICATION_EVIDENCE_REFS_OUT_OF_BOUNDS"
        if any(not _bounded_text(ref) for ref in refs):
            return None, "VERIFICATION_EVIDENCE_REF_INVALID"
        if len(set(refs)) != len(refs):
            return None, "VERIFICATION_EVIDENCE_REF_DUPLICATE"
        if any(ref not in evidence_ids for ref in refs):
            return None, "VERIFICATION_EVIDENCE_REF_UNRESOLVED"
        if not isinstance(entry_result, str) or entry_result not in _RESULTS:
            return None, "ENTRY_RESULT_INVALID"
        if not isinstance(entry_reasons, list):
            return None, "ENTRY_REASONS_INVALID"
        if any(not _bounded_text(reason) for reason in entry_reasons):
            return None, "ENTRY_REASON_INVALID"
        seen_ids.add(str(obligation_id))
        outcomes.append(str(entry_result))

    if seen_ids != set(catalog_by_id):
        return None, "COVERAGE_SET_MISMATCH"
    if "FAIL" in outcomes:
        return "FAIL", None
    if "INCONCLUSIVE" in outcomes:
        return "INCONCLUSIVE", None
    return "PASS", None


def _validate_bundle_and_review(
    *,
    bundle: object,
    review: object,
    expected_repository: str,
    expected_candidate_commit: str,
) -> _AdmissionValidation:
    if not isinstance(bundle, dict) or set(bundle) != _BUNDLE_KEYS:
        return _invalid("BUNDLE_SCHEMA_INVALID", hold=True)

    bundle_material = _safe_canonical_bytes(bundle)
    if bundle_material is None:
        return _invalid("BUNDLE_MATERIAL_INVALID", hold=True)
    if len(bundle_material) > _MAX_ARTIFACT_BYTES:
        return _invalid("BUNDLE_BOUND_EXCEEDED", hold=True)
    bundle_digest = hashlib.sha256(bundle_material).hexdigest()
    if bundle.get("schema_version") != _BUNDLE_SCHEMA:
        return _invalid(
            "BUNDLE_SCHEMA_VERSION_INVALID",
            hold=True,
            bundle_digest=bundle_digest,
        )
    if not _bounded_text(bundle.get("repository")):
        return _invalid(
            "REPOSITORY_INVALID",
            hold=True,
            bundle_digest=bundle_digest,
        )
    if not _is_sha(bundle.get("evaluated_candidate_commit"), 40):
        return _invalid(
            "CANDIDATE_IDENTITY_INVALID",
            hold=True,
            bundle_digest=bundle_digest,
        )
    if (
        bundle.get("repository") != expected_repository
        or bundle.get("evaluated_candidate_commit") != expected_candidate_commit
    ):
        return _invalid(
            "EXPECTED_BINDING_MISMATCH",
            bundle_digest=bundle_digest,
        )
    if not _is_sha(expected_candidate_commit, 40):
        return _invalid(
            "EXPECTED_CANDIDATE_INVALID",
            hold=True,
            bundle_digest=bundle_digest,
        )

    oracle = bundle.get("oracle_identity")
    question = bundle.get("governed_question_material")
    material = bundle.get("qualification_material")
    if (
        not isinstance(oracle, dict)
        or set(oracle) != _ORACLE_KEYS
        or not isinstance(question, dict)
        or set(question) != _QUESTION_KEYS
        or not isinstance(material, dict)
        or set(material) != _QUALIFICATION_MATERIAL_KEYS
    ):
        return _invalid(
            "BUNDLE_MATERIAL_SCHEMA_INVALID",
            hold=True,
            bundle_digest=bundle_digest,
        )
    if (
        not all(
            _bounded_text(oracle.get(name))
            for name in ("oracle_id", "oracle_version", "oracle_producer_subject_id")
        )
        or not _is_sha(oracle.get("oracle_content_digest"), 64)
        or not _bounded_text(question.get("relation_id"))
        or not _is_sha(question.get("evaluation_question_identity"), 64)
        or not _is_sha(question.get("input_contract_identity"), 64)
        or not _is_sha(question.get("output_contract_identity"), 64)
    ):
        return _invalid(
            "BUNDLE_IDENTITY_INVALID",
            hold=True,
            bundle_digest=bundle_digest,
        )

    catalog_by_id, catalog_error = _validate_catalog(bundle, question)
    if catalog_error is not None or catalog_by_id is None:
        return _invalid(
            catalog_error or "OBLIGATION_CATALOG_INVALID",
            hold=True,
            bundle_digest=bundle_digest,
        )
    evidence_ids, evidence_error = _validate_verification_evidence(bundle)
    if evidence_error is not None or evidence_ids is None:
        return _invalid(
            evidence_error or "VERIFICATION_EVIDENCE_INVALID",
            hold=True,
            bundle_digest=bundle_digest,
        )
    coverage_result, coverage_error = _validate_coverage(
        bundle=bundle,
        oracle=oracle,
        question=question,
        catalog_by_id=catalog_by_id,
        evidence_ids=evidence_ids,
    )
    if coverage_error is not None or coverage_result is None:
        return _invalid(
            coverage_error or "COVERAGE_INVALID",
            hold=True,
            bundle_digest=bundle_digest,
        )

    if (
        material.get("qualification_method") != _QUALIFICATION_METHOD
        or material.get("executing_runner_version") != _RUNNER_VERSION
        or not _is_sha(material.get("executing_runner_digest"), 64)
        or material.get("executing_runner_digest")
        not in _runner_contract_digests()
    ):
        return _invalid(
            "RUNNER_IDENTITY_MISMATCH",
            bundle_digest=bundle_digest,
        )
    if bundle.get("qualification_material_digest") != _sha256(material):
        return _invalid(
            "QUALIFICATION_MATERIAL_DIGEST_MISMATCH",
            bundle_digest=bundle_digest,
        )

    if not isinstance(review, dict) or set(review) != _REVIEW_KEYS:
        return _invalid(
            "REVIEW_EVIDENCE_SCHEMA_INVALID",
            hold=True,
            bundle_digest=bundle_digest,
        )

    review_material = _safe_canonical_bytes(review)
    if review_material is None:
        return _invalid(
            "REVIEW_MATERIAL_INVALID",
            hold=True,
            bundle_digest=bundle_digest,
        )
    if len(review_material) > _MAX_ARTIFACT_BYTES:
        return _invalid(
            "REVIEW_BOUND_EXCEEDED",
            hold=True,
            bundle_digest=bundle_digest,
        )
    review_digest = hashlib.sha256(review_material).hexdigest()
    runtime_binding = _runtime_binding_from_material(bundle, review, bundle_digest)
    if review.get("schema_version") != _REVIEW_SCHEMA:
        return _invalid(
            "REVIEW_SCHEMA_VERSION_INVALID",
            hold=True,
            runtime_binding=runtime_binding,
            bundle_digest=bundle_digest,
            review_digest=review_digest,
        )
    if review.get("authority_effect") != "none":
        return _invalid(
            "REVIEW_AUTHORITY_EFFECT_INVALID",
            runtime_binding=runtime_binding,
            bundle_digest=bundle_digest,
            review_digest=review_digest,
        )
    if (
        review.get("repository") != expected_repository
        or review.get("evaluated_candidate_commit") != expected_candidate_commit
        or review.get("qualification_bundle_digest") != bundle_digest
        or review.get("reviewed_relation_id") != question.get("relation_id")
        or review.get("reviewed_evaluation_question_identity")
        != question.get("evaluation_question_identity")
        or review.get("reviewed_obligation_catalog_digest")
        != bundle.get("obligation_catalog_digest")
    ):
        return _invalid(
            "REVIEW_BINDING_MISMATCH",
            runtime_binding=runtime_binding,
            bundle_digest=bundle_digest,
            review_digest=review_digest,
        )

    role_fields = (
        "implementation_actor_id",
        "qualification_reviewer_id",
        "qualification_validator_id",
    )
    roles = [
        oracle.get("oracle_producer_subject_id"),
        *(review.get(name) for name in role_fields),
    ]
    if any(not _bounded_text(role) for role in roles) or len(set(roles)) != 4:
        return _invalid(
            "DECLARED_ROLE_SEPARATION_INVALID",
            hold=True,
            runtime_binding=runtime_binding,
            bundle_digest=bundle_digest,
            review_digest=review_digest,
        )
    if not _bounded_text(review.get("structural_validator_evidence_reference")):
        return _invalid(
            "STRUCTURAL_VALIDATOR_EVIDENCE_REF_INVALID",
            hold=True,
            runtime_binding=runtime_binding,
            bundle_digest=bundle_digest,
            review_digest=review_digest,
        )
    finding_refs = review.get("finding_refs")
    evidence_refs = review.get("evidence_references")
    if (
        not isinstance(finding_refs, list)
        or any(not _bounded_text(ref) for ref in finding_refs)
        or not isinstance(evidence_refs, list)
        or not evidence_refs
        or any(not _bounded_text(ref) for ref in evidence_refs)
    ):
        return _invalid(
            "REVIEW_REFERENCE_INVALID",
            hold=True,
            runtime_binding=runtime_binding,
            bundle_digest=bundle_digest,
            review_digest=review_digest,
        )
    if len(finding_refs) + len(evidence_refs) > _MAX_REVIEW_REFERENCES:
        return _invalid(
            "REVIEW_REFERENCES_OUT_OF_BOUNDS",
            hold=True,
            runtime_binding=runtime_binding,
            bundle_digest=bundle_digest,
            review_digest=review_digest,
        )
    if (
        len(set(finding_refs)) != len(finding_refs)
        or len(set(evidence_refs)) != len(evidence_refs)
    ):
        return _invalid(
            "REVIEW_REFERENCE_DUPLICATE",
            hold=True,
            runtime_binding=runtime_binding,
            bundle_digest=bundle_digest,
            review_digest=review_digest,
        )

    structural = review.get("structural_validator_result")
    catalog = review.get("catalog_completeness_result")
    independence = review.get("independence_review_result")
    verification = review.get("verification_material_review_result")
    terminal = review.get("qualification_review_result")
    dimensions = (structural, catalog, independence, verification, terminal)
    if any(
        not isinstance(value, str) or value not in _RESULTS
        for value in dimensions
    ):
        return _invalid(
            "REVIEW_RESULT_INVALID",
            hold=True,
            runtime_binding=runtime_binding,
            bundle_digest=bundle_digest,
            review_digest=review_digest,
        )

    # Explicit negative review outcomes fail closed according to the admitted
    # trust contract.  Coverage is independently recomputed above.
    if "FAIL" in dimensions or coverage_result == "FAIL":
        return _invalid(
            "REVIEW_RESULT_FAIL",
            runtime_binding=runtime_binding,
            bundle_digest=bundle_digest,
            review_digest=review_digest,
        )
    if "INCONCLUSIVE" in dimensions or coverage_result == "INCONCLUSIVE":
        return _invalid(
            "REVIEW_RESULT_INCONCLUSIVE",
            hold=True,
            runtime_binding=runtime_binding,
            bundle_digest=bundle_digest,
            review_digest=review_digest,
        )

    if runtime_binding is None:
        return _invalid(
            "RUNTIME_BINDING_UNAVAILABLE",
            hold=True,
            bundle_digest=bundle_digest,
            review_digest=review_digest,
        )

    operation_payload = {
        "schema": _ADMISSION_SCHEMA,
        "repository": bundle["repository"],
        "evaluated_candidate_commit": bundle["evaluated_candidate_commit"],
        "qualification_bundle_schema_version": bundle["schema_version"],
        "qualification_bundle_digest": bundle_digest,
        "oracle_identity": bundle["oracle_identity"],
        "governed_question_material": bundle["governed_question_material"],
        "obligation_catalog_digest": bundle["obligation_catalog_digest"],
        "verification_evidence_digest": bundle["verification_evidence_digest"],
        "qualification_material_digest": bundle["qualification_material_digest"],
        "qualification_method": material["qualification_method"],
        "executing_runner_version": material["executing_runner_version"],
        "executing_runner_digest": material["executing_runner_digest"],
        "review_evidence_schema_version": review["schema_version"],
        "review_evidence_digest": review_digest,
        "reviewed_relation_id": review["reviewed_relation_id"],
        "reviewed_evaluation_question_identity": review[
            "reviewed_evaluation_question_identity"
        ],
        "reviewed_obligation_catalog_digest": review[
            "reviewed_obligation_catalog_digest"
        ],
        "structural_validator_result": structural,
        "catalog_completeness_result": catalog,
        "independence_review_result": independence,
        "verification_material_review_result": verification,
        "qualification_review_result": terminal,
        "implementation_actor_id": review["implementation_actor_id"],
        "qualification_reviewer_id": review["qualification_reviewer_id"],
        "qualification_validator_id": review["qualification_validator_id"],
        "authority_effect": review["authority_effect"],
    }
    return _AdmissionValidation(
        outcome=GovernedQualificationReviewAdmissionOutcome.READY,
        reason_code="MATERIAL_VALIDATION_PASS",
        runtime_binding=runtime_binding,
        qualification_bundle_digest=bundle_digest,
        review_evidence_digest=review_digest,
        operation_payload=operation_payload,
    )


def _invalid(
    reason_code: str,
    *,
    hold: bool = False,
    runtime_binding: RuntimeQualificationBindingV0 | None = None,
    bundle_digest: str | None = None,
    review_digest: str | None = None,
) -> _AdmissionValidation:
    return _AdmissionValidation(
        outcome=(
            GovernedQualificationReviewAdmissionOutcome.HOLD
            if hold
            else GovernedQualificationReviewAdmissionOutcome.DENIED
        ),
        reason_code=reason_code,
        runtime_binding=runtime_binding,
        qualification_bundle_digest=bundle_digest,
        review_evidence_digest=review_digest,
        operation_payload=None,
    )


def _routing_subject(
    *,
    policy_version: str,
    baseline_commit: str,
    focus_id: str,
    evidence_set_digest: str,
    relation_id: str,
    evaluation_question_identity: str,
    finding_fingerprint: str,
    resolved_evidence_material_digest: str,
) -> dict[str, str]:
    return {
        "policy_version": policy_version,
        "baseline_commit": baseline_commit,
        "focus_id": focus_id,
        "evidence_set_digest": evidence_set_digest,
        "relation_id": relation_id,
        "evaluation_question_identity": evaluation_question_identity,
        "finding_fingerprint": finding_fingerprint,
        "resolved_evidence_material_digest": resolved_evidence_material_digest,
    }


def _admission_from_validation(
    validation: _AdmissionValidation,
    *,
    security_context: SecurityContext,
) -> GovernedQualificationReviewAdmissionV0:
    runtime_key = (
        RuntimeQualificationBindingKeyV0(validation.runtime_binding)
        if validation.runtime_binding is not None
        else None
    )
    return GovernedQualificationReviewAdmissionV0(
        outcome=validation.outcome,
        reason_code=validation.reason_code,
        runtime_binding=validation.runtime_binding,
        runtime_binding_key=runtime_key,
        qualification_bundle_digest=validation.qualification_bundle_digest,
        review_evidence_digest=validation.review_evidence_digest,
        authorization_context=security_context,
    )


def compose_governed_qualification_consumption_boundary_v0(
    *,
    qualification_bundle,
    qualification_review_evidence,
    expected_repository: str,
    expected_candidate_commit: str,
    security_context: SecurityContext,
    policy_decision_point: PolicyDecisionPoint,
    authorization_audit_sink: AuthorizationAuditSink,
    clock: Clock,
    human_confirmation_evidence: HumanConfirmationEvidence | None = None,
) -> GovernedQualificationConsumptionBoundaryV0:
    validation = _validate_bundle_and_review(
        bundle=qualification_bundle,
        review=qualification_review_evidence,
        expected_repository=expected_repository,
        expected_candidate_commit=expected_candidate_commit,
    )
    if validation.outcome is not GovernedQualificationReviewAdmissionOutcome.READY:
        return GovernedQualificationConsumptionBoundaryV0(
            expected_repository=expected_repository,
            expected_candidate_commit=expected_candidate_commit,
            clock=clock,
            admissions=(
                _admission_from_validation(
                    validation,
                    security_context=security_context,
                ),
            ),
        )

    admission_started_at = _safe_clock_now(clock)
    if (
        admission_started_at is None
        or admission_started_at < security_context.issued_at
        or admission_started_at >= security_context.expires_at
    ):
        held = _invalid(
            "ADMISSION_CLOCK_INVALID",
            hold=True,
            runtime_binding=validation.runtime_binding,
            bundle_digest=validation.qualification_bundle_digest,
            review_digest=validation.review_evidence_digest,
        )
        return GovernedQualificationConsumptionBoundaryV0(
            expected_repository=expected_repository,
            expected_candidate_commit=expected_candidate_commit,
            clock=clock,
            admissions=(
                _admission_from_validation(
                    held,
                    security_context=security_context,
                ),
            ),
        )

    assert validation.runtime_binding is not None
    assert validation.operation_payload is not None
    assert validation.qualification_bundle_digest is not None
    assert validation.review_evidence_digest is not None

    operation_binding = AuthorizationOperationBinding(
        namespace="engineering.qualification_review_consumption",
        binding_version="v0",
        digest_algorithm="sha256",
        digest_hex=_sha256(validation.operation_payload),
    )
    request = AuthorizationRequest(
        context=security_context,
        permission=_ADMISSION_PERMISSION,
        created_at=admission_started_at,
        operation_binding=operation_binding,
    )
    operation = GovernedQualificationReviewAdmissionOperationV0(
        runtime_binding=validation.runtime_binding,
        authorization_binding=operation_binding,
    )
    pep = StrictPolicyEnforcementPoint(
        policy_decision_point,
        operation,
        authorization_audit_sink,
    )
    try:
        executed_binding = pep.execute(
            request,
            human_confirmation_evidence,
        )
    except AuthorizationDeniedError:
        denied = _invalid(
            "POLICY_DENIED",
            runtime_binding=validation.runtime_binding,
            bundle_digest=validation.qualification_bundle_digest,
            review_digest=validation.review_evidence_digest,
        )
        return GovernedQualificationConsumptionBoundaryV0(
            expected_repository=expected_repository,
            expected_candidate_commit=expected_candidate_commit,
            clock=clock,
            admissions=(
                _admission_from_validation(
                    denied,
                    security_context=security_context,
                ),
            ),
        )
    except AuthorizationEnforcementError:
        held = _invalid(
            "PEP_ENFORCEMENT_FAILED",
            hold=True,
            runtime_binding=validation.runtime_binding,
            bundle_digest=validation.qualification_bundle_digest,
            review_digest=validation.review_evidence_digest,
        )
        return GovernedQualificationConsumptionBoundaryV0(
            expected_repository=expected_repository,
            expected_candidate_commit=expected_candidate_commit,
            clock=clock,
            admissions=(
                _admission_from_validation(
                    held,
                    security_context=security_context,
                ),
            ),
        )

    admission_evaluated_at = _safe_clock_now(clock)
    if (
        executed_binding != validation.runtime_binding
        or admission_evaluated_at is None
        or admission_evaluated_at < admission_started_at
        or admission_evaluated_at >= security_context.expires_at
    ):
        held = _invalid(
            "FINAL_ADMISSION_CHECK_FAILED",
            hold=True,
            runtime_binding=validation.runtime_binding,
            bundle_digest=validation.qualification_bundle_digest,
            review_digest=validation.review_evidence_digest,
        )
        return GovernedQualificationConsumptionBoundaryV0(
            expected_repository=expected_repository,
            expected_candidate_commit=expected_candidate_commit,
            clock=clock,
            admissions=(
                _admission_from_validation(
                    held,
                    security_context=security_context,
                ),
            ),
        )

    runtime_key = RuntimeQualificationBindingKeyV0(validation.runtime_binding)
    instance_key = AdmissionInstanceKeyV0(
        runtime_binding_key=runtime_key,
        qualification_bundle_digest=validation.qualification_bundle_digest,
        review_evidence_digest=validation.review_evidence_digest,
        authorization_context_id=security_context.context_id,
        authorization_request_id=request.request_id,
        authorization_operation_binding_digest=operation_binding.digest_hex,
    )
    admission = GovernedQualificationReviewAdmissionV0(
        outcome=GovernedQualificationReviewAdmissionOutcome.READY,
        reason_code="READY",
        runtime_binding=validation.runtime_binding,
        runtime_binding_key=runtime_key,
        qualification_bundle_digest=validation.qualification_bundle_digest,
        review_evidence_digest=validation.review_evidence_digest,
        authorization_context=security_context,
        authorization_request_id=request.request_id,
        authorization_request_created_at=request.created_at,
        authorization_operation_binding=operation_binding,
        admission_evaluated_at=admission_evaluated_at,
        instance_key=instance_key,
    )
    return GovernedQualificationConsumptionBoundaryV0(
        expected_repository=expected_repository,
        expected_candidate_commit=expected_candidate_commit,
        clock=clock,
        admissions=(admission,),
    )
