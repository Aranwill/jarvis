from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "MALAK-E3-DETERMINISTIC-ORACLE-QUALIFICATION-BUNDLE/v0"
REVIEW_SCHEMA_VERSION = "MALAK-E3-DETERMINISTIC-ORACLE-QUALIFICATION-REVIEW-EVIDENCE/v0"
VALIDATOR_SCHEMA_VERSION = "MALAK-E3-DETERMINISTIC-ORACLE-QUALIFICATION-STRUCTURAL-VALIDATOR/v0"
QUALIFICATION_METHOD = "INDEPENDENT_REVIEWED_DETERMINISTIC_COVERAGE"
RUNNER_VERSION = "e3-deterministic-oracle-qualification/v0"

MAX_OBLIGATIONS = 32
MAX_OBLIGATION_STATEMENT_BYTES = 4 * 1024
MAX_VERIFICATION_REFS_PER_OBLIGATION = 16
MAX_ARTIFACT_BYTES = 512 * 1024
MAX_TEXT_BYTES = 4 * 1024

RESULTS = {"PASS", "FAIL", "INCONCLUSIVE"}

BUNDLE_KEYS = {
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

ORACLE_IDENTITY_KEYS = {
    "oracle_id",
    "oracle_version",
    "oracle_content_digest",
    "oracle_producer_subject_id",
}

QUESTION_KEYS = {
    "relation_id",
    "evaluation_question_identity",
    "input_contract_identity",
    "output_contract_identity",
}

OBLIGATION_KEYS = {
    "obligation_id",
    "obligation_statement",
    "obligation_identity",
}

COVERAGE_ENTRY_KEYS = {
    "obligation_id",
    "obligation_identity",
    "oracle_check_id",
    "oracle_check_identity",
    "oracle_check_contract_digest",
    "verification_evidence_refs",
    "entry_result",
    "entry_reasons",
}

VERIFICATION_EVIDENCE_KEYS = {
    "evidence_id",
    "evidence_kind",
    "content_digest",
    "content_or_bounded_material",
    "candidate_binding",
}

QUALIFICATION_MATERIAL_KEYS = {
    "qualification_method",
    "executing_runner_version",
    "executing_runner_digest",
}

GOVERNED_BINDING_KEYS = {
    "repository",
    "evaluated_candidate_commit",
    "oracle_identity",
    "governed_question_material",
    "obligation_catalog_digest",
    "qualification_bundle_digest",
}

REVIEW_EVIDENCE_KEYS = {
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


def _canonical_json(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _sha256(value: object) -> str:
    return hashlib.sha256(_canonical_json(value)).hexdigest()


def _executing_runner_digest() -> str:
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def _is_exact_keys(value: object, keys: set[str]) -> bool:
    return isinstance(value, dict) and set(value) == keys


def _bounded_text(value: object, *, max_bytes: int = MAX_TEXT_BYTES) -> bool:
    return (
        isinstance(value, str)
        and value == value.strip()
        and bool(value)
        and len(value.encode("utf-8")) <= max_bytes
    )


def _is_sha40(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 40
        and all(char in "0123456789abcdef" for char in value)
    )


def _is_sha256(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(char in "0123456789abcdef" for char in value)
    )


def _is_identity64(value: object) -> bool:
    return (
        isinstance(value, str)
        and value == value.strip()
        and len(value) == 64
        and len(value.encode("utf-8")) == 64
    )


def _within_artifact_bound(value: object) -> bool:
    try:
        return len(_canonical_json(value)) <= MAX_ARTIFACT_BYTES
    except (TypeError, ValueError, OverflowError):
        return False


def _safe_bundle_digest(artifact: object) -> str | None:
    try:
        return _sha256(artifact)
    except (TypeError, ValueError, OverflowError):
        return None


def _result(
    *,
    validator_result: str,
    validator_reasons: list[str],
    candidate_commit: object,
    bundle_digest: str | None,
    qualification_review_result: str = "INCONCLUSIVE",
    qualification_review_reasons: list[str] | None = None,
) -> dict[str, object]:
    candidate = candidate_commit if _is_sha40(candidate_commit) else None
    return {
        "validator_schema": VALIDATOR_SCHEMA_VERSION,
        "validator_result": validator_result,
        "validator_reasons": validator_reasons,
        "candidate_commit": candidate,
        "qualification_bundle_digest": bundle_digest,
        "executing_runner_version": RUNNER_VERSION,
        "executing_runner_digest": _executing_runner_digest(),
        "requires_external_validation": True,
        "identity_independence_verified": False,
        "qualification_review_result": qualification_review_result,
        "qualification_review_reasons": (
            qualification_review_reasons
            if qualification_review_reasons is not None
            else ["EXTERNAL_REVIEW_REQUIRED"]
        ),
        "authority_effect": "none",
    }


def _validate_catalog(
    artifact: dict[str, Any],
    question: dict[str, Any],
) -> tuple[dict[str, dict[str, str]] | None, str | None]:
    catalog = artifact["obligation_catalog"]
    if not isinstance(catalog, list) or not catalog:
        return None, "OBLIGATION_CATALOG_INVALID"
    if len(catalog) > MAX_OBLIGATIONS:
        return None, "OBLIGATION_CATALOG_OUT_OF_BOUNDS"

    by_id: dict[str, dict[str, str]] = {}
    identities: set[str] = set()

    for item in catalog:
        if not _is_exact_keys(item, OBLIGATION_KEYS):
            return None, "OBLIGATION_SCHEMA_INVALID"
        assert isinstance(item, dict)

        obligation_id = item["obligation_id"]
        statement = item["obligation_statement"]
        identity = item["obligation_identity"]

        if not _bounded_text(obligation_id):
            return None, "OBLIGATION_ID_INVALID"
        if str(obligation_id).lower() in {"other", "*"}:
            return None, "OBLIGATION_CATCH_ALL_FORBIDDEN"
        if not _bounded_text(
            statement,
            max_bytes=MAX_OBLIGATION_STATEMENT_BYTES,
        ):
            return None, "OBLIGATION_STATEMENT_INVALID"
        if not _is_sha256(identity):
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

    if artifact["obligation_catalog_digest"] != _sha256(catalog):
        return None, "OBLIGATION_CATALOG_DIGEST_MISMATCH"

    return by_id, None


def _validate_verification_evidence(
    artifact: dict[str, Any],
) -> tuple[set[str] | None, str | None]:
    items = artifact["verification_evidence"]
    if not isinstance(items, list) or not items:
        return None, "VERIFICATION_EVIDENCE_INVALID"

    if artifact["verification_evidence_digest"] != _sha256(items):
        return None, "VERIFICATION_EVIDENCE_DIGEST_MISMATCH"

    candidate = artifact["evaluated_candidate_commit"]
    evidence_ids: set[str] = set()

    for item in items:
        if not _is_exact_keys(item, VERIFICATION_EVIDENCE_KEYS):
            return None, "VERIFICATION_EVIDENCE_SCHEMA_INVALID"
        assert isinstance(item, dict)

        evidence_id = item["evidence_id"]
        if not _bounded_text(evidence_id) or evidence_id in evidence_ids:
            return None, "VERIFICATION_EVIDENCE_ID_INVALID"
        if not _bounded_text(item["evidence_kind"]):
            return None, "VERIFICATION_EVIDENCE_KIND_INVALID"
        if not _is_sha256(item["content_digest"]):
            return None, "VERIFICATION_EVIDENCE_CONTENT_DIGEST_INVALID"
        if item["content_digest"] != _sha256(item["content_or_bounded_material"]):
            return None, "VERIFICATION_EVIDENCE_CONTENT_DIGEST_MISMATCH"
        if item["candidate_binding"] != candidate:
            return None, "VERIFICATION_EVIDENCE_CANDIDATE_MISMATCH"

        evidence_ids.add(str(evidence_id))

    return evidence_ids, None


def _validate_coverage(
    *,
    artifact: dict[str, Any],
    oracle: dict[str, Any],
    question: dict[str, Any],
    catalog_by_id: dict[str, dict[str, str]],
    evidence_ids: set[str],
) -> tuple[str | None, str | None]:
    entries = artifact["coverage_entries"]
    if not isinstance(entries, list):
        return None, "COVERAGE_ENTRIES_INVALID"
    if len(entries) != len(catalog_by_id) or len(entries) > MAX_OBLIGATIONS:
        return None, "COVERAGE_CARDINALITY_MISMATCH"

    seen_ids: set[str] = set()
    outcomes: list[str] = []

    for entry in entries:
        if not _is_exact_keys(entry, COVERAGE_ENTRY_KEYS):
            return None, "COVERAGE_ENTRY_SCHEMA_INVALID"
        assert isinstance(entry, dict)

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

        catalog_item = catalog_by_id[str(obligation_id)]
        if obligation_identity != catalog_item["obligation_identity"]:
            return None, "COVERAGE_OBLIGATION_IDENTITY_MISMATCH"

        if not _bounded_text(check_id):
            return None, "ORACLE_CHECK_ID_INVALID"
        if not _is_sha256(check_identity):
            return None, "ORACLE_CHECK_IDENTITY_INVALID"
        if not _is_sha256(check_contract_digest):
            return None, "ORACLE_CHECK_CONTRACT_DIGEST_INVALID"

        expected_check_identity = _sha256(
            {
                "oracle_id": oracle["oracle_id"],
                "oracle_version": oracle["oracle_version"],
                "check_id": check_id,
            }
        )
        if check_identity != expected_check_identity:
            return None, "ORACLE_CHECK_IDENTITY_MISMATCH"

        expected_check_contract_digest = _sha256(
            {
                "check_id": check_id,
                "input_contract_identity": question["input_contract_identity"],
                "output_contract_identity": question["output_contract_identity"],
            }
        )
        if check_contract_digest != expected_check_contract_digest:
            return None, "ORACLE_CHECK_CONTRACT_MISMATCH"

        if not isinstance(refs, list):
            return None, "VERIFICATION_EVIDENCE_REFS_INVALID"
        if not refs or len(refs) > MAX_VERIFICATION_REFS_PER_OBLIGATION:
            return None, "VERIFICATION_EVIDENCE_REFS_OUT_OF_BOUNDS"
        if any(not _bounded_text(ref) for ref in refs):
            return None, "VERIFICATION_EVIDENCE_REF_INVALID"
        if len(set(refs)) != len(refs):
            return None, "VERIFICATION_EVIDENCE_REF_DUPLICATE"
        if any(ref not in evidence_ids for ref in refs):
            return None, "VERIFICATION_EVIDENCE_REF_UNRESOLVED"

        if entry_result not in RESULTS:
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


def _validate_bundle(
    artifact: object,
) -> tuple[str, list[str], str | None, str | None]:
    bundle_digest = _safe_bundle_digest(artifact)
    if not _is_exact_keys(artifact, BUNDLE_KEYS):
        return "INCONCLUSIVE", ["BUNDLE_SCHEMA_INVALID"], None, bundle_digest
    assert isinstance(artifact, dict)

    if not _within_artifact_bound(artifact):
        return "INCONCLUSIVE", ["BUNDLE_BOUND_EXCEEDED"], None, bundle_digest
    if artifact["schema_version"] != SCHEMA_VERSION:
        return "INCONCLUSIVE", ["BUNDLE_SCHEMA_VERSION_INVALID"], None, bundle_digest
    if not _bounded_text(artifact["repository"]):
        return "INCONCLUSIVE", ["REPOSITORY_INVALID"], None, bundle_digest
    if not _is_sha40(artifact["evaluated_candidate_commit"]):
        return "INCONCLUSIVE", ["CANDIDATE_IDENTITY_INVALID"], None, bundle_digest

    oracle = artifact["oracle_identity"]
    if not _is_exact_keys(oracle, ORACLE_IDENTITY_KEYS):
        return "INCONCLUSIVE", ["ORACLE_IDENTITY_SCHEMA_INVALID"], None, bundle_digest
    assert isinstance(oracle, dict)
    if any(
        not _bounded_text(oracle[name])
        for name in ("oracle_id", "oracle_version", "oracle_producer_subject_id")
    ):
        return "INCONCLUSIVE", ["ORACLE_IDENTITY_INVALID"], None, bundle_digest
    if not _is_sha256(oracle["oracle_content_digest"]):
        return "INCONCLUSIVE", ["ORACLE_CONTENT_DIGEST_INVALID"], None, bundle_digest

    question = artifact["governed_question_material"]
    if not _is_exact_keys(question, QUESTION_KEYS):
        return "INCONCLUSIVE", ["QUESTION_MATERIAL_SCHEMA_INVALID"], None, bundle_digest
    assert isinstance(question, dict)
    if not _bounded_text(question["relation_id"]):
        return "INCONCLUSIVE", ["RELATION_ID_INVALID"], None, bundle_digest
    if not _is_identity64(question["evaluation_question_identity"]):
        return "INCONCLUSIVE", ["EVALUATION_QUESTION_IDENTITY_INVALID"], None, bundle_digest
    if not _is_sha256(question["input_contract_identity"]):
        return "INCONCLUSIVE", ["INPUT_CONTRACT_IDENTITY_INVALID"], None, bundle_digest
    if not _is_sha256(question["output_contract_identity"]):
        return "INCONCLUSIVE", ["OUTPUT_CONTRACT_IDENTITY_INVALID"], None, bundle_digest

    if not _is_sha256(artifact["obligation_catalog_digest"]):
        return "INCONCLUSIVE", ["OBLIGATION_CATALOG_DIGEST_INVALID"], None, bundle_digest
    catalog_by_id, error = _validate_catalog(artifact, question)
    if error is not None or catalog_by_id is None:
        return "INCONCLUSIVE", [error or "OBLIGATION_CATALOG_INVALID"], None, bundle_digest

    if not _is_sha256(artifact["verification_evidence_digest"]):
        return "INCONCLUSIVE", ["VERIFICATION_EVIDENCE_DIGEST_INVALID"], None, bundle_digest
    evidence_ids, error = _validate_verification_evidence(artifact)
    if error is not None or evidence_ids is None:
        return "INCONCLUSIVE", [error or "VERIFICATION_EVIDENCE_INVALID"], None, bundle_digest

    coverage_result, error = _validate_coverage(
        artifact=artifact,
        oracle=oracle,
        question=question,
        catalog_by_id=catalog_by_id,
        evidence_ids=evidence_ids,
    )
    if error is not None or coverage_result is None:
        return "INCONCLUSIVE", [error or "COVERAGE_INVALID"], None, bundle_digest

    material = artifact["qualification_material"]
    if not _is_exact_keys(material, QUALIFICATION_MATERIAL_KEYS):
        return "INCONCLUSIVE", ["QUALIFICATION_MATERIAL_SCHEMA_INVALID"], None, bundle_digest
    assert isinstance(material, dict)
    if material["qualification_method"] != QUALIFICATION_METHOD:
        return "INCONCLUSIVE", ["QUALIFICATION_METHOD_INVALID"], None, bundle_digest
    if material["executing_runner_version"] != RUNNER_VERSION:
        return "INCONCLUSIVE", ["RUNNER_VERSION_INVALID"], None, bundle_digest
    if not _is_sha256(material["executing_runner_digest"]):
        return "INCONCLUSIVE", ["RUNNER_DIGEST_INVALID"], None, bundle_digest
    if material["executing_runner_digest"] != _executing_runner_digest():
        return "INCONCLUSIVE", ["RUNNER_DIGEST_MISMATCH"], None, bundle_digest

    if not _is_sha256(artifact["qualification_material_digest"]):
        return "INCONCLUSIVE", ["QUALIFICATION_MATERIAL_DIGEST_INVALID"], None, bundle_digest
    if artifact["qualification_material_digest"] != _sha256(material):
        return "INCONCLUSIVE", ["QUALIFICATION_MATERIAL_DIGEST_MISMATCH"], None, bundle_digest

    return "PASS", [], coverage_result, bundle_digest


def _validate_governed_binding(
    *,
    artifact: dict[str, Any],
    expected_binding: object,
    bundle_digest: str,
) -> str | None:
    if not _is_exact_keys(expected_binding, GOVERNED_BINDING_KEYS):
        return "GOVERNED_BINDING_SCHEMA_INVALID"
    assert isinstance(expected_binding, dict)

    if expected_binding["repository"] != artifact["repository"]:
        return "GOVERNED_BINDING_REPOSITORY_MISMATCH"
    if (
        expected_binding["evaluated_candidate_commit"]
        != artifact["evaluated_candidate_commit"]
    ):
        return "GOVERNED_BINDING_CANDIDATE_MISMATCH"
    if expected_binding["oracle_identity"] != artifact["oracle_identity"]:
        return "GOVERNED_BINDING_ORACLE_MISMATCH"
    if (
        expected_binding["governed_question_material"]
        != artifact["governed_question_material"]
    ):
        return "GOVERNED_BINDING_QUESTION_MISMATCH"
    if (
        expected_binding["obligation_catalog_digest"]
        != artifact["obligation_catalog_digest"]
    ):
        return "GOVERNED_BINDING_CATALOG_MISMATCH"
    if expected_binding["qualification_bundle_digest"] != bundle_digest:
        return "GOVERNED_BINDING_BUNDLE_MISMATCH"

    return None


def _validate_review_evidence(
    *,
    artifact: dict[str, Any],
    review_evidence: object,
    bundle_digest: str,
    validator_result: str,
    coverage_result: str,
) -> tuple[str, list[str]]:
    if review_evidence is None:
        return "INCONCLUSIVE", ["EXTERNAL_REVIEW_REQUIRED"]
    if not _is_exact_keys(review_evidence, REVIEW_EVIDENCE_KEYS):
        return "INCONCLUSIVE", ["REVIEW_EVIDENCE_SCHEMA_INVALID"]
    assert isinstance(review_evidence, dict)

    if review_evidence["schema_version"] != REVIEW_SCHEMA_VERSION:
        return "INCONCLUSIVE", ["REVIEW_SCHEMA_VERSION_INVALID"]
    if review_evidence["authority_effect"] != "none":
        return "INCONCLUSIVE", ["REVIEW_AUTHORITY_EFFECT_INVALID"]
    if review_evidence["repository"] != artifact["repository"]:
        return "INCONCLUSIVE", ["REVIEW_REPOSITORY_MISMATCH"]
    if (
        review_evidence["evaluated_candidate_commit"]
        != artifact["evaluated_candidate_commit"]
    ):
        return "INCONCLUSIVE", ["REVIEW_CANDIDATE_MISMATCH"]
    if review_evidence["qualification_bundle_digest"] != bundle_digest:
        return "INCONCLUSIVE", ["REVIEW_BUNDLE_DIGEST_MISMATCH"]

    question = artifact["governed_question_material"]
    assert isinstance(question, dict)
    if review_evidence["reviewed_relation_id"] != question["relation_id"]:
        return "INCONCLUSIVE", ["REVIEW_RELATION_MISMATCH"]
    if (
        review_evidence["reviewed_evaluation_question_identity"]
        != question["evaluation_question_identity"]
    ):
        return "INCONCLUSIVE", ["REVIEW_QUESTION_MISMATCH"]
    if (
        review_evidence["reviewed_obligation_catalog_digest"]
        != artifact["obligation_catalog_digest"]
    ):
        return "INCONCLUSIVE", ["REVIEW_CATALOG_DIGEST_MISMATCH"]

    role_fields = (
        "implementation_actor_id",
        "qualification_reviewer_id",
        "qualification_validator_id",
    )
    if any(not _bounded_text(review_evidence[name]) for name in role_fields):
        return "INCONCLUSIVE", ["REVIEW_ROLE_ID_INVALID"]

    oracle = artifact["oracle_identity"]
    assert isinstance(oracle, dict)
    declared_roles = {
        str(oracle["oracle_producer_subject_id"]),
        *(str(review_evidence[name]) for name in role_fields),
    }
    if len(declared_roles) != 4:
        return "INCONCLUSIVE", ["DECLARED_ROLE_SEPARATION_NOT_DEMONSTRATED"]

    if not _bounded_text(review_evidence["structural_validator_evidence_reference"]):
        return "INCONCLUSIVE", ["STRUCTURAL_VALIDATOR_EVIDENCE_REF_INVALID"]

    if review_evidence["structural_validator_result"] not in RESULTS:
        return "INCONCLUSIVE", ["REVIEW_STRUCTURAL_RESULT_INVALID"]
    if review_evidence["structural_validator_result"] != validator_result:
        return "INCONCLUSIVE", ["REVIEW_STRUCTURAL_RESULT_MISMATCH"]

    dimension_fields = (
        "catalog_completeness_result",
        "independence_review_result",
        "verification_material_review_result",
    )
    if any(review_evidence[name] not in RESULTS for name in dimension_fields):
        return "INCONCLUSIVE", ["REVIEW_DIMENSION_RESULT_INVALID"]
    if review_evidence["qualification_review_result"] not in RESULTS:
        return "INCONCLUSIVE", ["REVIEW_TERMINAL_RESULT_INVALID"]

    finding_refs = review_evidence["finding_refs"]
    evidence_refs = review_evidence["evidence_references"]
    if not isinstance(finding_refs, list) or any(
        not _bounded_text(ref) for ref in finding_refs
    ):
        return "INCONCLUSIVE", ["REVIEW_FINDING_REFS_INVALID"]
    if (
        not isinstance(evidence_refs, list)
        or not evidence_refs
        or any(not _bounded_text(ref) for ref in evidence_refs)
    ):
        return "INCONCLUSIVE", ["REVIEW_EVIDENCE_REFS_INVALID"]

    if validator_result != "PASS":
        derived = validator_result
    elif coverage_result == "FAIL":
        derived = "FAIL"
    elif coverage_result == "INCONCLUSIVE":
        derived = "INCONCLUSIVE"
    else:
        dimensions = [str(review_evidence[name]) for name in dimension_fields]
        if "FAIL" in dimensions:
            derived = "FAIL"
        elif "INCONCLUSIVE" in dimensions:
            derived = "INCONCLUSIVE"
        else:
            derived = "PASS"

    if review_evidence["qualification_review_result"] != derived:
        return "INCONCLUSIVE", ["REVIEW_TERMINAL_RESULT_MISMATCH"]

    return derived, []


def evaluate_qualification_evidence_v0(
    *,
    artifact: object,
    expected_binding: object,
    independence_evidence: object,
) -> dict[str, object]:
    """Validate a bounded qualification bundle without acquiring authority."""

    try:
        validator_result, reasons, coverage_result, bundle_digest = _validate_bundle(
            artifact
        )

        candidate_commit = (
            artifact.get("evaluated_candidate_commit")
            if isinstance(artifact, dict)
            else None
        )

        if validator_result != "PASS" or coverage_result is None or bundle_digest is None:
            return _result(
                validator_result=validator_result,
                validator_reasons=reasons,
                candidate_commit=candidate_commit,
                bundle_digest=bundle_digest,
            )

        assert isinstance(artifact, dict)

        binding_error = _validate_governed_binding(
            artifact=artifact,
            expected_binding=expected_binding,
            bundle_digest=bundle_digest,
        )
        if binding_error is not None:
            return _result(
                validator_result="INCONCLUSIVE",
                validator_reasons=[binding_error],
                candidate_commit=candidate_commit,
                bundle_digest=bundle_digest,
            )

        review_result, review_reasons = _validate_review_evidence(
            artifact=artifact,
            review_evidence=independence_evidence,
            bundle_digest=bundle_digest,
            validator_result=validator_result,
            coverage_result=coverage_result,
        )

        return _result(
            validator_result=validator_result,
            validator_reasons=[],
            candidate_commit=candidate_commit,
            bundle_digest=bundle_digest,
            qualification_review_result=review_result,
            qualification_review_reasons=review_reasons,
        )
    except (AssertionError, KeyError, TypeError, ValueError, OverflowError, OSError):
        candidate_commit = (
            artifact.get("evaluated_candidate_commit")
            if isinstance(artifact, dict)
            else None
        )
        return _result(
            validator_result="INCONCLUSIVE",
            validator_reasons=["QUALIFICATION_INPUT_INVALID"],
            candidate_commit=candidate_commit,
            bundle_digest=_safe_bundle_digest(artifact),
        )
