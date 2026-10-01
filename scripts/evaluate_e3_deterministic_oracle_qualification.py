from __future__ import annotations

import hashlib
import json
from typing import Any


SCHEMA_VERSION = "MALAK-E3-DETERMINISTIC-ORACLE-QUALIFICATION-EVIDENCE/v0"
QUALIFICATION_METHOD = "INDEPENDENT_REVIEWED_DETERMINISTIC_COVERAGE"
INDEPENDENCE_EVIDENCE_KIND = "EXTERNAL_CANDIDATE_BOUND_ROLE_SEPARATION"

MAX_OBLIGATIONS = 32
MAX_OBLIGATION_STATEMENT_BYTES = 4 * 1024
MAX_VERIFICATION_REFS_PER_OBLIGATION = 16
MAX_ARTIFACT_BYTES = 512 * 1024
MAX_TEXT_BYTES = 4 * 1024

RESULTS = {"PASS", "FAIL", "INCONCLUSIVE"}

ARTIFACT_KEYS = {
    "schema_version",
    "repository",
    "evaluated_candidate_commit",
    "oracle_id",
    "oracle_version",
    "oracle_content_digest",
    "oracle_producer_subject_id",
    "relation_id",
    "evaluation_question_identity",
    "input_contract_identity",
    "output_contract_identity",
    "obligation_catalog_digest",
    "obligation_count",
    "coverage_entries",
    "qualification_method",
    "qualification_material_digest",
    "qualification_runner_version",
    "qualification_runner_digest",
    "qualification_reviewer_id",
    "qualification_validator_id",
    "qualification_result",
    "qualification_reasons",
    "authority_effect",
}

EXPECTED_BINDING_KEYS = {
    "repository",
    "evaluated_candidate_commit",
    "oracle_id",
    "oracle_version",
    "oracle_content_digest",
    "relation_id",
    "evaluation_question_identity",
    "input_contract_identity",
    "output_contract_identity",
    "obligation_catalog_digest",
    "obligation_catalog",
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

INDEPENDENCE_KEYS = {
    "evidence_kind",
    "evaluated_candidate_commit",
    "oracle_producer_subject_id",
    "qualification_reviewer_id",
    "qualification_validator_id",
    "review_evidence_digest",
    "validation_evidence_digest",
    "authority_effect",
}


def _result(result: str, *reasons: str) -> dict[str, object]:
    return {
        "qualification_result": result,
        "qualification_reasons": list(reasons),
        "authority_effect": "none",
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


def _artifact_within_bound(artifact: object) -> bool:
    try:
        encoded = _canonical_json(artifact)
    except (TypeError, ValueError, OverflowError):
        return False
    return len(encoded) <= MAX_ARTIFACT_BYTES


def _validate_global_shape(
    artifact: object,
    expected_binding: object,
) -> str | None:
    if not _is_exact_keys(artifact, ARTIFACT_KEYS):
        return "ARTIFACT_SCHEMA_INVALID"
    if not _is_exact_keys(expected_binding, EXPECTED_BINDING_KEYS):
        return "EXPECTED_BINDING_SCHEMA_INVALID"

    assert isinstance(artifact, dict)
    assert isinstance(expected_binding, dict)

    if not _artifact_within_bound(artifact):
        return "ARTIFACT_BOUND_EXCEEDED"
    if artifact["schema_version"] != SCHEMA_VERSION:
        return "SCHEMA_VERSION_INVALID"
    if artifact["authority_effect"] != "none":
        return "AUTHORITY_EFFECT_INVALID"
    if artifact["qualification_method"] != QUALIFICATION_METHOD:
        return "QUALIFICATION_METHOD_INVALID"
    if artifact["qualification_result"] not in RESULTS:
        return "DECLARED_RESULT_INVALID"
    if not isinstance(artifact["qualification_reasons"], list):
        return "DECLARED_REASONS_INVALID"

    text_fields = (
        "repository",
        "oracle_id",
        "oracle_version",
        "oracle_producer_subject_id",
        "relation_id",
        "qualification_runner_version",
        "qualification_reviewer_id",
        "qualification_validator_id",
    )
    if any(not _bounded_text(artifact[name]) for name in text_fields):
        return "IDENTITY_TEXT_INVALID"

    if not _is_sha40(artifact["evaluated_candidate_commit"]):
        return "CANDIDATE_IDENTITY_INVALID"

    sha_fields = (
        "oracle_content_digest",
        "input_contract_identity",
        "output_contract_identity",
        "obligation_catalog_digest",
        "qualification_material_digest",
        "qualification_runner_digest",
    )
    if any(not _is_sha256(artifact[name]) for name in sha_fields):
        return "DIGEST_IDENTITY_INVALID"

    if not _is_identity64(artifact["evaluation_question_identity"]):
        return "EVALUATION_QUESTION_IDENTITY_INVALID"

    if not isinstance(artifact["obligation_count"], int):
        return "OBLIGATION_COUNT_INVALID"
    if isinstance(artifact["obligation_count"], bool):
        return "OBLIGATION_COUNT_INVALID"
    if artifact["obligation_count"] < 1 or artifact["obligation_count"] > MAX_OBLIGATIONS:
        return "OBLIGATION_COUNT_OUT_OF_BOUNDS"

    if not isinstance(artifact["coverage_entries"], list):
        return "COVERAGE_ENTRIES_INVALID"
    if len(artifact["coverage_entries"]) > MAX_OBLIGATIONS:
        return "COVERAGE_ENTRIES_OUT_OF_BOUNDS"

    return None


def _validate_exact_binding(
    artifact: dict[str, Any],
    expected_binding: dict[str, Any],
) -> str | None:
    binding_fields = (
        "repository",
        "evaluated_candidate_commit",
        "oracle_id",
        "oracle_version",
        "oracle_content_digest",
        "relation_id",
        "evaluation_question_identity",
        "input_contract_identity",
        "output_contract_identity",
        "obligation_catalog_digest",
    )
    for name in binding_fields:
        if artifact[name] != expected_binding[name]:
            return "EXPECTED_BINDING_MISMATCH"

    if not _bounded_text(expected_binding["repository"]):
        return "EXPECTED_BINDING_INVALID"
    if not _is_sha40(expected_binding["evaluated_candidate_commit"]):
        return "EXPECTED_BINDING_INVALID"
    if not _is_sha256(expected_binding["oracle_content_digest"]):
        return "EXPECTED_BINDING_INVALID"
    if not _is_identity64(expected_binding["evaluation_question_identity"]):
        return "EXPECTED_BINDING_INVALID"
    for name in (
        "input_contract_identity",
        "output_contract_identity",
        "obligation_catalog_digest",
    ):
        if not _is_sha256(expected_binding[name]):
            return "EXPECTED_BINDING_INVALID"

    return None


def _validate_catalog(
    *,
    artifact: dict[str, Any],
    expected_binding: dict[str, Any],
) -> tuple[dict[str, dict[str, str]] | None, str | None]:
    catalog = expected_binding["obligation_catalog"]
    if not isinstance(catalog, list):
        return None, "OBLIGATION_CATALOG_INVALID"
    if not catalog or len(catalog) > MAX_OBLIGATIONS:
        return None, "OBLIGATION_CATALOG_OUT_OF_BOUNDS"
    if artifact["obligation_count"] != len(catalog):
        return None, "OBLIGATION_COUNT_MISMATCH"

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
        if obligation_id.lower() in {"other", "*"}:
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
                "relation_id": artifact["relation_id"],
                "evaluation_question_identity": artifact[
                    "evaluation_question_identity"
                ],
                "obligation_id": obligation_id,
                "obligation_statement": statement,
            }
        )
        if identity != expected_identity:
            return None, "OBLIGATION_IDENTITY_MISMATCH"

        by_id[obligation_id] = {
            "obligation_id": obligation_id,
            "obligation_statement": statement,
            "obligation_identity": identity,
        }
        identities.add(identity)

    return by_id, None


def _validate_independence(
    *,
    artifact: dict[str, Any],
    evidence: object,
) -> str | None:
    if not _is_exact_keys(evidence, INDEPENDENCE_KEYS):
        return "INDEPENDENCE_EVIDENCE_INVALID"

    assert isinstance(evidence, dict)

    if evidence["evidence_kind"] != INDEPENDENCE_EVIDENCE_KIND:
        return "INDEPENDENCE_EVIDENCE_KIND_INVALID"
    if evidence["authority_effect"] != "none":
        return "INDEPENDENCE_AUTHORITY_INVALID"
    if evidence["evaluated_candidate_commit"] != artifact["evaluated_candidate_commit"]:
        return "INDEPENDENCE_CANDIDATE_MISMATCH"

    identity_fields = (
        "oracle_producer_subject_id",
        "qualification_reviewer_id",
        "qualification_validator_id",
    )
    for name in identity_fields:
        if not _bounded_text(evidence[name]):
            return "INDEPENDENCE_IDENTITY_INVALID"
        if evidence[name] != artifact[name]:
            return "INDEPENDENCE_IDENTITY_MISMATCH"

    producer = artifact["oracle_producer_subject_id"]
    reviewer = artifact["qualification_reviewer_id"]
    validator = artifact["qualification_validator_id"]
    if len({producer, reviewer, validator}) != 3:
        return "ROLE_SEPARATION_NOT_DEMONSTRATED"

    if not _is_sha256(evidence["review_evidence_digest"]):
        return "REVIEW_EVIDENCE_DIGEST_INVALID"
    if not _is_sha256(evidence["validation_evidence_digest"]):
        return "VALIDATION_EVIDENCE_DIGEST_INVALID"

    return None


def _validate_coverage(
    *,
    artifact: dict[str, Any],
    catalog_by_id: dict[str, dict[str, str]],
) -> tuple[list[str] | None, str | None]:
    entries = artifact["coverage_entries"]
    if len(entries) != len(catalog_by_id):
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

        catalog_item = catalog_by_id[obligation_id]
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
                "oracle_id": artifact["oracle_id"],
                "oracle_version": artifact["oracle_version"],
                "check_id": check_id,
            }
        )
        if check_identity != expected_check_identity:
            return None, "ORACLE_CHECK_IDENTITY_MISMATCH"

        expected_check_contract_digest = _sha256(
            {
                "check_id": check_id,
                "input_contract_identity": artifact["input_contract_identity"],
                "output_contract_identity": artifact["output_contract_identity"],
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

        if entry_result not in RESULTS:
            return None, "ENTRY_RESULT_INVALID"
        if not isinstance(entry_reasons, list):
            return None, "ENTRY_REASONS_INVALID"
        if any(not _bounded_text(reason) for reason in entry_reasons):
            return None, "ENTRY_REASON_INVALID"

        seen_ids.add(obligation_id)
        outcomes.append(entry_result)

    if seen_ids != set(catalog_by_id):
        return None, "COVERAGE_SET_MISMATCH"

    return outcomes, None


def evaluate_qualification_evidence_v0(
    *,
    artifact: object,
    expected_binding: object,
    independence_evidence: object,
) -> dict[str, object]:
    """Evaluate bounded structural qualification evidence with zero authority effect."""

    try:
        global_error = _validate_global_shape(artifact, expected_binding)
        if global_error is not None:
            return _result("INCONCLUSIVE", global_error)

        assert isinstance(artifact, dict)
        assert isinstance(expected_binding, dict)

        binding_error = _validate_exact_binding(artifact, expected_binding)
        if binding_error is not None:
            return _result("INCONCLUSIVE", binding_error)

        catalog_by_id, catalog_error = _validate_catalog(
            artifact=artifact,
            expected_binding=expected_binding,
        )
        if catalog_error is not None or catalog_by_id is None:
            return _result(
                "INCONCLUSIVE",
                catalog_error or "OBLIGATION_CATALOG_INVALID",
            )

        independence_error = _validate_independence(
            artifact=artifact,
            evidence=independence_evidence,
        )
        if independence_error is not None:
            return _result("INCONCLUSIVE", independence_error)

        outcomes, coverage_error = _validate_coverage(
            artifact=artifact,
            catalog_by_id=catalog_by_id,
        )
        if coverage_error is not None or outcomes is None:
            return _result(
                "INCONCLUSIVE",
                coverage_error or "COVERAGE_INVALID",
            )

        if "FAIL" in outcomes:
            return _result("FAIL", "MATERIAL_NON_COVERAGE")
        if "INCONCLUSIVE" in outcomes:
            return _result("INCONCLUSIVE", "COVERAGE_UNRESOLVED")

        return _result("PASS", "FULL_COVERAGE_DERIVED")
    except (AssertionError, KeyError, TypeError, ValueError, OverflowError):
        return _result("INCONCLUSIVE", "QUALIFICATION_INPUT_INVALID")
