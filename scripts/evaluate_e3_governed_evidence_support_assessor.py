from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


RUNNER_VERSION = "e3-support-assessor-qualification/v0"
CASE_SET_SCHEMA = "MALAK-E3-SUPPORT-ASSESSOR-CASESET/v0"
RESULTS_SCHEMA = "MALAK-E3-SUPPORT-ASSESSOR-RESULTS/v0"
OUTPUT_SCHEMA = "MALAK-E3-SUPPORT-ASSESSOR-QUALIFICATION-OUTPUT/v0"
SUPPORT_POLICY_VERSION = "e3-governed-evidence-support/v0"

MAX_CASE_SET_BYTES = 1024 * 1024
MAX_RESULT_BYTES = 512 * 1024
MAX_STATEMENT_BYTES = 4 * 1024
MAX_RATIONALE_BYTES = 8 * 1024
MAX_REASON_CODES = 10
MAX_REFS_PER_ROLE = 16

CASE_IDS = tuple(f"C{i:02d}" for i in range(1, 19))
CASE_CLASSES = (
    "EXACT_SUPPORT",
    "IRRELEVANT_SUPPORT",
    "INSUFFICIENT_SUPPORT",
    "COMPOUND_PARTIAL_SUPPORT",
    "COMPATIBLE_LIMITING_EVIDENCE",
    "UNRESOLVED_COUNTEREVIDENCE",
    "AUTHORITY_SEMANTIC_MISMATCH",
    "LOW_AUTHORITY_RELEVANT_SUPPORT",
    "RATIONALE_OVERCLAIM",
    "MISSING_EVIDENCE_MATERIAL",
    "STATEMENT_BINDING_DRIFT",
    "EVIDENCE_MATERIAL_BINDING_DRIFT",
    "EQUIVALENT_INPUT_PERMUTATION",
    "ASSESSOR_UNAVAILABLE",
    "MALFORMED_ASSESSOR_OUTPUT",
    "HIGH_CONFIDENCE_UNSUPPORTED",
    "SELF_CERTIFICATION",
    "SCOPE_EXPANSION_REQUIRED",
)
OUTCOMES = {"SUPPORTED", "INSUFFICIENT", "INCONCLUSIVE"}
REASONS = {
    "MATERIAL_SUPPORT_CONFIRMED",
    "SUPPORTING_REFS_IRRELEVANT",
    "SUPPORTING_REFS_INSUFFICIENT",
    "COMPOUND_CLAIM_NOT_FULLY_SUPPORTED",
    "MATERIAL_COUNTEREVIDENCE_UNRESOLVED",
    "SUBJECT_BINDING_MISMATCH",
    "EVIDENCE_MATERIAL_INCOMPLETE",
    "ASSESSOR_UNAVAILABLE",
    "ASSESSOR_OUTPUT_INVALID",
    "ASSESSMENT_SCOPE_EXCEEDED",
}
CRITICAL_PROPERTIES = {
    "FALSE_SUPPORT",
    "BINDING_DRIFT",
    "UNRESOLVED_COUNTEREVIDENCE",
    "SELF_CERTIFICATION",
    "EQUIVALENT_INPUT_STABILITY",
    "UNSUPPORTED_ESCAPE",
}
CASE_SET_KEYS = {"schema_version", "support_policy_version", "cases"}
CASE_KEYS = {
    "case_id",
    "case_class",
    "critical_properties",
    "subject",
    "repository_evidence",
    "knowledge_evidence",
    "finding_producer_subject_id",
    "assessor_subject_id",
    "expected_outcome",
    "expected_reason_codes",
    "equivalence_group",
}
SUBJECT_KEYS = {
    "baseline_commit",
    "focus_id",
    "evidence_set_digest",
    "relation_id",
    "classification",
    "statement",
    "rationale",
    "supporting_repository_refs",
    "supporting_knowledge_refs",
    "limiting_or_counterevidence_refs",
    "uncertainty_basis",
}
EVIDENCE_ITEM_KEYS = {"ref", "material"}
RESULT_TOP_KEYS = {
    "schema_version",
    "case_set_digest",
    "assessor_mechanism",
    "harness",
    "case_results",
}
MECHANISM_KEYS = {
    "mechanism_id",
    "mechanism_version",
    "mechanism_kind",
    "config_digest",
    "producer_subject_id",
    "assessor_subject_id",
    "model_provenance",
}
MODEL_PROVENANCE_KEYS = {
    "provider_id",
    "model_id",
    "model_version",
    "model_artifact_digest",
    "prompt_template_digest",
    "runtime_settings_digest",
    "execution_profile_digest",
}
HARNESS_KEYS = {
    "harness_policy_version",
    "harness_policy_digest",
    "budget_manifest_digest",
    "attempt_policy_digest",
}
ARTIFACT_CASE_KEYS = {
    "case_id",
    "subject_fingerprint",
    "outcome",
    "reason_codes",
}
OUTPUT_KEYS = {
    "schema_version",
    "malak_baseline_commit",
    "case_set_schema_version",
    "case_set_digest",
    "reviewed_case_set_digest",
    "ground_truth_reviewer_id",
    "qualification_runner_version",
    "qualification_runner_digest",
    "assessor_mechanism_identity",
    "assessor_result_artifact_digest",
    "case_count",
    "case_results",
    "metrics",
    "qualification_result",
    "qualification_reasons",
    "authority_effect",
}


class QualificationInputError(ValueError):
    pass


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _is_sha256(value: object) -> bool:
    if not isinstance(value, str) or len(value) != 64:
        return False
    return all(char in "0123456789abcdef" for char in value)


def _is_sha40(value: object) -> bool:
    if not isinstance(value, str) or len(value) != 40:
        return False
    return all(char in "0123456789abcdef" for char in value)


def _non_empty(value: object) -> bool:
    return isinstance(value, str) and value == value.strip() and bool(value)


def _read_json(path: Path, *, max_bytes: int, label: str) -> tuple[dict[str, Any], bytes]:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise QualificationInputError(f"{label}_unreadable") from exc
    if len(raw) > max_bytes:
        raise QualificationInputError(f"{label}_size_exceeded")
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise QualificationInputError(f"{label}_malformed") from exc
    if not isinstance(payload, dict):
        raise QualificationInputError(f"{label}_not_object")
    return payload, raw


def _require_exact_keys(value: dict[str, Any], expected: set[str], label: str) -> None:
    if set(value) != expected:
        raise QualificationInputError(f"{label}_schema_mismatch")


def _require_string_list(
    value: object,
    *,
    label: str,
    allow_empty: bool,
    max_items: int,
) -> list[str]:
    if not isinstance(value, list):
        raise QualificationInputError(f"{label}_not_array")
    if not allow_empty and not value:
        raise QualificationInputError(f"{label}_empty")
    if len(value) > max_items:
        raise QualificationInputError(f"{label}_too_many")
    if any(not _non_empty(item) for item in value):
        raise QualificationInputError(f"{label}_invalid_item")
    if len(set(value)) != len(value):
        raise QualificationInputError(f"{label}_duplicate")
    return list(value)


def _validate_reason_coherence(outcome: str, reasons: list[str], *, label: str) -> None:
    if outcome not in OUTCOMES:
        raise QualificationInputError(f"{label}_outcome")
    if not reasons or len(reasons) > MAX_REASON_CODES:
        raise QualificationInputError(f"{label}_reason_count")
    if any(reason not in REASONS for reason in reasons):
        raise QualificationInputError(f"{label}_reason_unknown")
    if len(set(reasons)) != len(reasons):
        raise QualificationInputError(f"{label}_reason_duplicate")

    if outcome == "SUPPORTED":
        if reasons != ["MATERIAL_SUPPORT_CONFIRMED"]:
            raise QualificationInputError(f"{label}_supported_reason")
        return

    if "MATERIAL_SUPPORT_CONFIRMED" in reasons:
        raise QualificationInputError(f"{label}_positive_reason_mismatch")

    if outcome == "INSUFFICIENT":
        allowed = {
            "SUPPORTING_REFS_IRRELEVANT",
            "SUPPORTING_REFS_INSUFFICIENT",
        }
        if any(reason not in allowed for reason in reasons):
            raise QualificationInputError(f"{label}_insufficient_reason")


def _finding_fingerprint(subject: dict[str, Any]) -> str:
    material = {
        "classification": subject["classification"],
        "limiting_or_counterevidence_refs": sorted(
            subject["limiting_or_counterevidence_refs"]
        ),
        "rationale": subject["rationale"],
        "relation_id": subject["relation_id"],
        "statement": subject["statement"],
        "supporting_knowledge_refs": sorted(subject["supporting_knowledge_refs"]),
        "supporting_repository_refs": sorted(subject["supporting_repository_refs"]),
        "uncertainty_basis": subject["uncertainty_basis"],
    }
    encoded = json.dumps(
        material,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return _sha256_bytes(encoded)


def _validate_subject(subject: object, *, case_id: str) -> dict[str, Any]:
    if not isinstance(subject, dict):
        raise QualificationInputError(f"{case_id}_subject_not_object")
    _require_exact_keys(subject, SUBJECT_KEYS, f"{case_id}_subject")

    if not _is_sha40(subject["baseline_commit"]):
        raise QualificationInputError(f"{case_id}_baseline_commit")
    if not _is_sha256(subject["evidence_set_digest"]):
        raise QualificationInputError(f"{case_id}_evidence_set_digest")

    for name in (
        "focus_id",
        "relation_id",
        "classification",
        "statement",
        "rationale",
        "uncertainty_basis",
    ):
        if not _non_empty(subject[name]):
            raise QualificationInputError(f"{case_id}_{name}")

    if len(subject["statement"].encode("utf-8")) > MAX_STATEMENT_BYTES:
        raise QualificationInputError(f"{case_id}_statement_size")
    if len(subject["rationale"].encode("utf-8")) > MAX_RATIONALE_BYTES:
        raise QualificationInputError(f"{case_id}_rationale_size")

    for name in (
        "supporting_repository_refs",
        "supporting_knowledge_refs",
        "limiting_or_counterevidence_refs",
    ):
        _require_string_list(
            subject[name],
            label=f"{case_id}_{name}",
            allow_empty=True,
            max_items=MAX_REFS_PER_ROLE,
        )
    return subject


def _validate_evidence(
    value: object,
    *,
    case_id: str,
    collection: str,
    allow_empty_material: bool,
) -> dict[str, str]:
    if not isinstance(value, list):
        raise QualificationInputError(f"{case_id}_{collection}_not_array")
    if len(value) > MAX_REFS_PER_ROLE:
        raise QualificationInputError(f"{case_id}_{collection}_too_many")

    by_ref: dict[str, str] = {}
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            raise QualificationInputError(f"{case_id}_{collection}_{index}_not_object")
        _require_exact_keys(
            item,
            EVIDENCE_ITEM_KEYS,
            f"{case_id}_{collection}_{index}",
        )
        ref = item["ref"]
        material = item["material"]
        if not _non_empty(ref):
            raise QualificationInputError(f"{case_id}_{collection}_{index}_ref")
        if not isinstance(material, str):
            raise QualificationInputError(f"{case_id}_{collection}_{index}_material")
        if not material and not allow_empty_material:
            raise QualificationInputError(
                f"{case_id}_{collection}_{index}_material_empty"
            )
        if ref in by_ref:
            raise QualificationInputError(f"{case_id}_{collection}_duplicate_ref")
        by_ref[ref] = material
    return by_ref


def _validate_case_set(payload: dict[str, Any]) -> list[dict[str, Any]]:
    _require_exact_keys(payload, CASE_SET_KEYS, "case_set")
    if payload["schema_version"] != CASE_SET_SCHEMA:
        raise QualificationInputError("case_set_schema_version")
    if payload["support_policy_version"] != SUPPORT_POLICY_VERSION:
        raise QualificationInputError("support_policy_version")

    cases = payload["cases"]
    if not isinstance(cases, list) or len(cases) != len(CASE_IDS):
        raise QualificationInputError("case_catalog_count")

    observed_ids: list[str] = []
    validated: list[dict[str, Any]] = []

    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            raise QualificationInputError(f"case_{index}_not_object")
        _require_exact_keys(case, CASE_KEYS, f"case_{index}")

        case_id = case["case_id"]
        if not isinstance(case_id, str):
            raise QualificationInputError(f"case_{index}_id_type")
        observed_ids.append(case_id)
        if case_id not in CASE_IDS:
            raise QualificationInputError("case_catalog_id")

        expected_class = CASE_CLASSES[CASE_IDS.index(case_id)]
        if case["case_class"] != expected_class:
            raise QualificationInputError(f"{case_id}_class")

        properties = _require_string_list(
            case["critical_properties"],
            label=f"{case_id}_critical_properties",
            allow_empty=True,
            max_items=len(CRITICAL_PROPERTIES),
        )
        if properties != sorted(properties):
            raise QualificationInputError(f"{case_id}_critical_properties_order")
        if any(item not in CRITICAL_PROPERTIES for item in properties):
            raise QualificationInputError(f"{case_id}_critical_properties_unknown")

        subject = _validate_subject(case["subject"], case_id=case_id)
        allow_missing = case_id == "C10"
        repository = _validate_evidence(
            case["repository_evidence"],
            case_id=case_id,
            collection="repository_evidence",
            allow_empty_material=allow_missing,
        )
        knowledge = _validate_evidence(
            case["knowledge_evidence"],
            case_id=case_id,
            collection="knowledge_evidence",
            allow_empty_material=allow_missing,
        )

        if not _non_empty(case["finding_producer_subject_id"]):
            raise QualificationInputError(f"{case_id}_finding_producer_subject_id")
        if not _non_empty(case["assessor_subject_id"]):
            raise QualificationInputError(f"{case_id}_assessor_subject_id")

        expected_outcome = case["expected_outcome"]
        expected_reasons = _require_string_list(
            case["expected_reason_codes"],
            label=f"{case_id}_expected_reason_codes",
            allow_empty=False,
            max_items=MAX_REASON_CODES,
        )
        _validate_reason_coherence(
            expected_outcome,
            expected_reasons,
            label=f"{case_id}_expected",
        )

        group = case["equivalence_group"]
        if case_id == "C13":
            if not _non_empty(group) or group == "NONE":
                raise QualificationInputError("C13_equivalence_group")
        elif group != "NONE":
            raise QualificationInputError(f"{case_id}_equivalence_group")

        for ref in subject["supporting_repository_refs"]:
            if ref not in repository and case_id != "C10":
                raise QualificationInputError(f"{case_id}_repository_ref_unresolved")
        for ref in subject["supporting_knowledge_refs"]:
            if ref not in knowledge and case_id != "C10":
                raise QualificationInputError(f"{case_id}_knowledge_ref_unresolved")

        known_refs = set(repository) | set(knowledge)
        for ref in subject["limiting_or_counterevidence_refs"]:
            if ref not in known_refs:
                raise QualificationInputError(f"{case_id}_limiting_ref_unresolved")

        validated.append(case)

    if observed_ids != list(CASE_IDS):
        if len(set(observed_ids)) != len(observed_ids):
            raise QualificationInputError("case_catalog_duplicate")
        raise QualificationInputError("case_catalog_exact_order")

    minimum_properties = {
        "C02": {"FALSE_SUPPORT", "UNSUPPORTED_ESCAPE"},
        "C03": {"FALSE_SUPPORT", "UNSUPPORTED_ESCAPE"},
        "C04": {"FALSE_SUPPORT", "UNSUPPORTED_ESCAPE"},
        "C06": {"UNRESOLVED_COUNTEREVIDENCE"},
        "C07": {"FALSE_SUPPORT", "UNSUPPORTED_ESCAPE"},
        "C09": {"FALSE_SUPPORT", "UNSUPPORTED_ESCAPE"},
        "C11": {"BINDING_DRIFT"},
        "C12": {"BINDING_DRIFT"},
        "C13": {"EQUIVALENT_INPUT_STABILITY"},
        "C16": {"FALSE_SUPPORT", "UNSUPPORTED_ESCAPE"},
        "C17": {"SELF_CERTIFICATION"},
    }
    for case in validated:
        required = minimum_properties.get(case["case_id"], set())
        if not required.issubset(set(case["critical_properties"])):
            raise QualificationInputError(
                f"{case['case_id']}_critical_properties_missing"
            )

    return validated


def _validate_model_provenance(value: object) -> None:
    if not isinstance(value, dict):
        raise QualificationInputError("model_provenance_missing")
    _require_exact_keys(value, MODEL_PROVENANCE_KEYS, "model_provenance")
    for name, item in value.items():
        if name.endswith("_digest"):
            if not _is_sha256(item):
                raise QualificationInputError(f"model_provenance_{name}")
        elif not _non_empty(item):
            raise QualificationInputError(f"model_provenance_{name}")


def _validate_artifact(
    payload: dict[str, Any],
    *,
    case_set_digest: str,
    cases: list[dict[str, Any]],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    _require_exact_keys(payload, RESULT_TOP_KEYS, "assessor_results")
    if payload["schema_version"] != RESULTS_SCHEMA:
        raise QualificationInputError("assessor_results_schema")
    if payload["case_set_digest"] != case_set_digest:
        raise QualificationInputError("assessor_results_case_set_digest")

    mechanism = payload["assessor_mechanism"]
    if not isinstance(mechanism, dict):
        raise QualificationInputError("assessor_mechanism_not_object")
    _require_exact_keys(mechanism, MECHANISM_KEYS, "assessor_mechanism")
    for name in (
        "mechanism_id",
        "mechanism_version",
        "producer_subject_id",
        "assessor_subject_id",
    ):
        if not _non_empty(mechanism[name]):
            raise QualificationInputError(f"assessor_mechanism_{name}")
    if not _is_sha256(mechanism["config_digest"]):
        raise QualificationInputError("assessor_mechanism_config_digest")
    if mechanism["mechanism_kind"] not in {
        "DETERMINISTIC",
        "MODEL_BASED",
        "HUMAN_REVIEWED",
    }:
        raise QualificationInputError("assessor_mechanism_kind")

    if mechanism["mechanism_kind"] == "MODEL_BASED":
        _validate_model_provenance(mechanism["model_provenance"])
    elif mechanism["model_provenance"] is not None:
        raise QualificationInputError("assessor_mechanism_model_provenance")

    harness = payload["harness"]
    if not isinstance(harness, dict):
        raise QualificationInputError("harness_not_object")
    _require_exact_keys(harness, HARNESS_KEYS, "harness")
    if not _non_empty(harness["harness_policy_version"]):
        raise QualificationInputError("harness_policy_version")
    for name in (
        "harness_policy_digest",
        "budget_manifest_digest",
        "attempt_policy_digest",
    ):
        if not _is_sha256(harness[name]):
            raise QualificationInputError(name)

    results = payload["case_results"]
    if not isinstance(results, list) or len(results) != len(CASE_IDS):
        raise QualificationInputError("artifact_case_count")

    by_id: dict[str, dict[str, Any]] = {}
    expected_by_id = {case["case_id"]: case for case in cases}
    for index, result in enumerate(results):
        if not isinstance(result, dict):
            raise QualificationInputError(f"artifact_case_{index}_not_object")
        _require_exact_keys(result, ARTIFACT_CASE_KEYS, f"artifact_case_{index}")

        case_id = result["case_id"]
        if case_id not in expected_by_id:
            raise QualificationInputError("artifact_case_unknown")
        if case_id in by_id:
            raise QualificationInputError("artifact_case_duplicate")
        if not _is_sha256(result["subject_fingerprint"]):
            raise QualificationInputError(f"{case_id}_subject_fingerprint")
        expected_fingerprint = _finding_fingerprint(expected_by_id[case_id]["subject"])
        if result["subject_fingerprint"] != expected_fingerprint:
            raise QualificationInputError(f"{case_id}_subject_fingerprint_mismatch")

        reasons = _require_string_list(
            result["reason_codes"],
            label=f"{case_id}_observed_reason_codes",
            allow_empty=False,
            max_items=MAX_REASON_CODES,
        )
        _validate_reason_coherence(
            result["outcome"],
            reasons,
            label=f"{case_id}_observed",
        )
        by_id[case_id] = result

    if set(by_id) != set(CASE_IDS):
        raise QualificationInputError("artifact_case_catalog")

    return mechanism, [by_id[case_id] for case_id in CASE_IDS]


def _empty_metrics() -> dict[str, float | int]:
    return {
        "false_support_acceptance_rate": 0,
        "unsupported_claim_escape_rate": 0,
        "false_inconclusive_rate": 0,
        "contradiction_handling_recall": 0,
        "assessment_stability_on_equivalent_inputs": 0,
        "binding_drift_detection_rate": 0,
    }


def _rate(numerator: int, denominator: int, *, label: str) -> float:
    if denominator == 0:
        raise QualificationInputError(f"{label}_zero_denominator")
    return numerator / denominator


def _stability_for_case(case: dict[str, Any]) -> bool:
    subject = case["subject"]
    left = _finding_fingerprint(subject)

    permuted = dict(subject)
    permuted["supporting_repository_refs"] = list(
        reversed(subject["supporting_repository_refs"])
    )
    permuted["supporting_knowledge_refs"] = list(
        reversed(subject["supporting_knowledge_refs"])
    )
    permuted["limiting_or_counterevidence_refs"] = list(
        reversed(subject["limiting_or_counterevidence_refs"])
    )
    right = _finding_fingerprint(permuted)
    return left == right


def _evaluate(
    cases: list[dict[str, Any]],
    artifact_results: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, float], str, list[str]]:
    results_by_id = {result["case_id"]: result for result in artifact_results}
    case_results: list[dict[str, Any]] = []

    for case in cases:
        observed = results_by_id[case["case_id"]]
        expected_reasons = sorted(case["expected_reason_codes"])
        observed_reasons = sorted(observed["reason_codes"])
        mismatches: list[str] = []

        if observed["outcome"] != case["expected_outcome"]:
            mismatches.append("OUTCOME_MISMATCH")
        if observed_reasons != expected_reasons:
            mismatches.append("REASON_CODES_MISMATCH")

        case_results.append(
            {
                "case_id": case["case_id"],
                "expected_disposition": case["expected_outcome"],
                "observed_disposition": observed["outcome"],
                "expected_reason_class": case["expected_reason_codes"][0],
                "observed_reason_codes": observed["reason_codes"],
                "case_result": "FAIL" if mismatches else "PASS",
                "mismatch_reasons": mismatches,
            }
        )

    expected_non_support = [
        case for case in cases if case["expected_outcome"] != "SUPPORTED"
    ]
    false_support = sum(
        results_by_id[case["case_id"]]["outcome"] == "SUPPORTED"
        for case in expected_non_support
    )

    unsupported = [
        case for case in cases if "UNSUPPORTED_ESCAPE" in case["critical_properties"]
    ]
    unsupported_escape = sum(
        results_by_id[case["case_id"]]["outcome"] == "SUPPORTED"
        for case in unsupported
    )

    expected_non_inconclusive = [
        case for case in cases if case["expected_outcome"] != "INCONCLUSIVE"
    ]
    false_inconclusive = sum(
        results_by_id[case["case_id"]]["outcome"] == "INCONCLUSIVE"
        for case in expected_non_inconclusive
    )

    contradiction_cases = [
        case
        for case in cases
        if "UNRESOLVED_COUNTEREVIDENCE" in case["critical_properties"]
    ]
    contradiction_hits = sum(
        results_by_id[case["case_id"]]["outcome"] == "INCONCLUSIVE"
        and "MATERIAL_COUNTEREVIDENCE_UNRESOLVED"
        in results_by_id[case["case_id"]]["reason_codes"]
        for case in contradiction_cases
    )

    binding_cases = [
        case for case in cases if "BINDING_DRIFT" in case["critical_properties"]
    ]
    binding_hits = sum(
        results_by_id[case["case_id"]]["outcome"] == "INCONCLUSIVE"
        and "SUBJECT_BINDING_MISMATCH"
        in results_by_id[case["case_id"]]["reason_codes"]
        for case in binding_cases
    )

    equivalent = [
        case
        for case in cases
        if "EQUIVALENT_INPUT_STABILITY" in case["critical_properties"]
    ]
    stable = sum(
        _stability_for_case(case)
        and results_by_id[case["case_id"]]["outcome"] == case["expected_outcome"]
        and sorted(results_by_id[case["case_id"]]["reason_codes"])
        == sorted(case["expected_reason_codes"])
        for case in equivalent
    )

    metrics = {
        "false_support_acceptance_rate": _rate(
            false_support,
            len(expected_non_support),
            label="false_support_acceptance_rate",
        ),
        "unsupported_claim_escape_rate": _rate(
            unsupported_escape,
            len(unsupported),
            label="unsupported_claim_escape_rate",
        ),
        "false_inconclusive_rate": _rate(
            false_inconclusive,
            len(expected_non_inconclusive),
            label="false_inconclusive_rate",
        ),
        "contradiction_handling_recall": _rate(
            contradiction_hits,
            len(contradiction_cases),
            label="contradiction_handling_recall",
        ),
        "assessment_stability_on_equivalent_inputs": _rate(
            stable,
            len(equivalent),
            label="assessment_stability_on_equivalent_inputs",
        ),
        "binding_drift_detection_rate": _rate(
            binding_hits,
            len(binding_cases),
            label="binding_drift_detection_rate",
        ),
    }

    any_case_fail = any(item["case_result"] == "FAIL" for item in case_results)
    self_cert_positive = any(
        "SELF_CERTIFICATION" in case["critical_properties"]
        and results_by_id[case["case_id"]]["outcome"] == "SUPPORTED"
        for case in cases
    )
    safety_ok = (
        metrics["false_support_acceptance_rate"] == 0
        and metrics["unsupported_claim_escape_rate"] == 0
        and metrics["binding_drift_detection_rate"] == 1
        and metrics["contradiction_handling_recall"] == 1
        and metrics["assessment_stability_on_equivalent_inputs"] == 1
        and not self_cert_positive
    )

    reasons: list[str] = []
    if any_case_fail:
        reasons.append("CASE_MISMATCH")
    if not safety_ok:
        reasons.append("SAFETY_FLOOR_VIOLATION")

    return (
        case_results,
        metrics,
        "FAIL" if reasons else "PASS",
        reasons,
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case-set", required=True)
    parser.add_argument("--assessor-results", required=True)
    parser.add_argument("--ground-truth-reviewer-id", required=True)
    parser.add_argument("--runner-implementation-actor-id", required=True)
    parser.add_argument("--reviewed-case-set-digest", required=True)
    return parser


def _base_output(
    *,
    case_set_digest: str,
    reviewed_case_set_digest: str,
    reviewer_id: str,
    baseline_commit: str,
    artifact_digest: str,
    mechanism_identity: dict[str, Any] | None,
) -> dict[str, Any]:
    return {
        "schema_version": OUTPUT_SCHEMA,
        "malak_baseline_commit": baseline_commit,
        "case_set_schema_version": CASE_SET_SCHEMA,
        "case_set_digest": case_set_digest,
        "reviewed_case_set_digest": reviewed_case_set_digest,
        "ground_truth_reviewer_id": reviewer_id,
        "qualification_runner_version": RUNNER_VERSION,
        "qualification_runner_digest": _sha256_bytes(Path(__file__).read_bytes()),
        "assessor_mechanism_identity": mechanism_identity,
        "assessor_result_artifact_digest": artifact_digest,
        "case_count": 18,
        "case_results": [],
        "metrics": _empty_metrics(),
        "qualification_result": "INCONCLUSIVE",
        "qualification_reasons": ["INPUT_NOT_VALIDATED"],
        "authority_effect": "none",
    }


def _write_output(payload: dict[str, Any]) -> None:
    if set(payload) != OUTPUT_KEYS:
        raise RuntimeError("internal_output_schema_mismatch")
    sys.stdout.write(
        json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    )


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    case_path = Path(args.case_set)
    artifact_path = Path(args.assessor_results)

    case_digest = ""
    artifact_digest = ""
    baseline_commit = "0" * 40
    mechanism_identity: dict[str, Any] | None = None

    try:
        case_payload, case_bytes = _read_json(
            case_path,
            max_bytes=MAX_CASE_SET_BYTES,
            label="case_set",
        )
        case_digest = _sha256_bytes(case_bytes)
        cases = _validate_case_set(case_payload)
        baseline_commit = cases[0]["subject"]["baseline_commit"]

        if not _non_empty(args.ground_truth_reviewer_id):
            raise QualificationInputError("ground_truth_reviewer_id")
        if not _non_empty(args.runner_implementation_actor_id):
            raise QualificationInputError("runner_implementation_actor_id")
        if args.ground_truth_reviewer_id == args.runner_implementation_actor_id:
            raise QualificationInputError("reviewer_runner_collision")
        if not _is_sha256(args.reviewed_case_set_digest):
            raise QualificationInputError("reviewed_case_set_digest_invalid")
        if args.reviewed_case_set_digest != case_digest:
            raise QualificationInputError("reviewed_case_set_digest_mismatch")
        if any(
            args.ground_truth_reviewer_id == case["finding_producer_subject_id"]
            for case in cases
        ):
            raise QualificationInputError("reviewer_finding_producer_collision")

        artifact_payload, artifact_bytes = _read_json(
            artifact_path,
            max_bytes=MAX_RESULT_BYTES,
            label="assessor_results",
        )
        artifact_digest = _sha256_bytes(artifact_bytes)
        mechanism, artifact_results = _validate_artifact(
            artifact_payload,
            case_set_digest=case_digest,
            cases=cases,
        )
        mechanism_identity = {
            "mechanism_id": mechanism["mechanism_id"],
            "mechanism_version": mechanism["mechanism_version"],
            "mechanism_kind": mechanism["mechanism_kind"],
            "config_digest": mechanism["config_digest"],
            "producer_subject_id": mechanism["producer_subject_id"],
            "assessor_subject_id": mechanism["assessor_subject_id"],
            "model_provenance": mechanism["model_provenance"],
        }

        if args.ground_truth_reviewer_id == mechanism["assessor_subject_id"]:
            raise QualificationInputError("reviewer_assessor_collision")

        if mechanism["producer_subject_id"] == mechanism["assessor_subject_id"]:
            positive = any(
                result["outcome"] == "SUPPORTED"
                for result in artifact_results
            )
            output = _base_output(
                case_set_digest=case_digest,
                reviewed_case_set_digest=args.reviewed_case_set_digest,
                reviewer_id=args.ground_truth_reviewer_id,
                baseline_commit=baseline_commit,
                artifact_digest=artifact_digest,
                mechanism_identity=mechanism_identity,
            )
            output["qualification_result"] = "FAIL" if positive else "INCONCLUSIVE"
            output["qualification_reasons"] = ["SELF_CERTIFICATION"]
            _write_output(output)
            return 1 if positive else 2

        case_results, metrics, result, reasons = _evaluate(cases, artifact_results)
        output = _base_output(
            case_set_digest=case_digest,
            reviewed_case_set_digest=args.reviewed_case_set_digest,
            reviewer_id=args.ground_truth_reviewer_id,
            baseline_commit=baseline_commit,
            artifact_digest=artifact_digest,
            mechanism_identity=mechanism_identity,
        )
        output["case_results"] = case_results
        output["metrics"] = metrics
        output["qualification_result"] = result
        output["qualification_reasons"] = reasons
        _write_output(output)
        return 0 if result == "PASS" else 1

    except QualificationInputError as exc:
        output = _base_output(
            case_set_digest=case_digest,
            reviewed_case_set_digest=args.reviewed_case_set_digest,
            reviewer_id=args.ground_truth_reviewer_id,
            baseline_commit=baseline_commit,
            artifact_digest=artifact_digest,
            mechanism_identity=mechanism_identity,
        )
        output["qualification_result"] = "INCONCLUSIVE"
        output["qualification_reasons"] = [str(exc)]
        _write_output(output)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
