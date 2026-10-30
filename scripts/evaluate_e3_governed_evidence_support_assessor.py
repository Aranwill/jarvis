from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


RUNNER_VERSION = "e3-support-assessor-qualification/v0.2"
CASE_SET_SCHEMA = "MALAK-E3-SUPPORT-ASSESSOR-CASESET/v0.1"
RESULTS_SCHEMA = "MALAK-E3-SUPPORT-ASSESSOR-RESULTS/v0.1"
OUTPUT_SCHEMA = "MALAK-E3-SUPPORT-ASSESSOR-QUALIFICATION-OUTPUT/v0.2"
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
EXPECTED_PROPERTIES = {
    "C01": set(),
    "C02": {"FALSE_SUPPORT", "UNSUPPORTED_ESCAPE"},
    "C03": {"FALSE_SUPPORT", "UNSUPPORTED_ESCAPE"},
    "C04": {"FALSE_SUPPORT", "UNSUPPORTED_ESCAPE"},
    "C05": set(),
    "C06": {"UNRESOLVED_COUNTEREVIDENCE"},
    "C07": {"FALSE_SUPPORT", "UNSUPPORTED_ESCAPE"},
    "C08": set(),
    "C09": {"FALSE_SUPPORT", "UNSUPPORTED_ESCAPE"},
    "C10": set(),
    "C11": {"BINDING_DRIFT"},
    "C12": {"BINDING_DRIFT"},
    "C13": {"EQUIVALENT_INPUT_STABILITY"},
    "C14": set(),
    "C15": set(),
    "C16": {"FALSE_SUPPORT", "UNSUPPORTED_ESCAPE"},
    "C17": {"SELF_CERTIFICATION"},
    "C18": set(),
}

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
KNOWN_PROPERTIES = {
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
    "finding_producer_subject_id",
    "assessor_subject_id",
    "inputs",
    "comparison_rule",
}
INPUT_KEYS = {
    "input_id",
    "subject",
    "repository_evidence",
    "knowledge_evidence",
    "binding_expectation",
    "binding_prior",
    "expected_outcome",
    "expected_reason_codes",
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
BINDING_EXPECTATION_KEYS = {
    "binding_kind",
    "expected_subject_fingerprint",
    "expected_evidence_material_digest",
}
BINDING_PRIOR_KEYS = {
    "prior_subject",
    "prior_repository_evidence",
    "prior_knowledge_evidence",
}
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
ARTIFACT_CASE_KEYS = {"case_id", "observations"}
OBSERVATION_KEYS = {
    "input_id",
    "input_instance_digest",
    "semantic_input_digest",
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
    "input_count",
    "case_results",
    "metrics",
    "diagnostic_exact_match_result",
    "safety_floor_result",
    "qualification_result",
    "qualification_reasons",
    "authority_effect",
}


class QualificationInputError(ValueError):
    pass


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _canonical_json(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


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


def _read_json(
    path: Path,
    *,
    max_bytes: int,
    label: str,
) -> tuple[dict[str, Any], bytes]:
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


def _require_exact_keys(
    value: dict[str, Any],
    expected: set[str],
    label: str,
) -> None:
    if set(value) != expected:
        raise QualificationInputError(f"{label}_schema_mismatch")


def _require_string_list(
    value: object,
    *,
    label: str,
    allow_empty: bool,
    max_items: int,
    require_sorted: bool = False,
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
    result = list(value)
    if require_sorted and result != sorted(result):
        raise QualificationInputError(f"{label}_order")
    return result


def _validate_reason_coherence(
    outcome: str,
    reasons: list[str],
    *,
    label: str,
) -> None:
    if not isinstance(outcome, str) or outcome not in OUTCOMES:
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
        return

    # INCONCLUSIVE can carry model-owned uncertainty or deterministic envelope
    # errors, but never model-owned reasons reserved for INSUFFICIENT.
    allowed = {
        "COMPOUND_CLAIM_NOT_FULLY_SUPPORTED",
        "MATERIAL_COUNTEREVIDENCE_UNRESOLVED",
        "ASSESSMENT_SCOPE_EXCEEDED",
        "SUBJECT_BINDING_MISMATCH",
        "EVIDENCE_MATERIAL_INCOMPLETE",
        "ASSESSOR_UNAVAILABLE",
        "ASSESSOR_OUTPUT_INVALID",
    }
    if any(reason not in allowed for reason in reasons):
        raise QualificationInputError(f"{label}_inconclusive_reason")


def _subject_fingerprint(subject: dict[str, Any]) -> str:
    material = {
        "classification": subject["classification"],
        "limiting_or_counterevidence_refs": sorted(
            subject["limiting_or_counterevidence_refs"]
        ),
        "rationale": subject["rationale"],
        "relation_id": subject["relation_id"],
        "statement": subject["statement"],
        "supporting_knowledge_refs": sorted(subject["supporting_knowledge_refs"]),
        "supporting_repository_refs": sorted(
            subject["supporting_repository_refs"]
        ),
        "uncertainty_basis": subject["uncertainty_basis"],
    }
    return _sha256_bytes(_canonical_json(material))


def _evidence_material_digest(
    repository_evidence: list[dict[str, str]],
    knowledge_evidence: list[dict[str, str]],
) -> str:
    material = {
        "repository_evidence": sorted(
            repository_evidence,
            key=lambda item: item["ref"],
        ),
        "knowledge_evidence": sorted(
            knowledge_evidence,
            key=lambda item: item["ref"],
        ),
    }
    return _sha256_bytes(_canonical_json(material))


def _digest_material(input_record: dict[str, Any]) -> dict[str, Any]:
    return {
        "subject": copy.deepcopy(input_record["subject"]),
        "repository_evidence": copy.deepcopy(input_record["repository_evidence"]),
        "knowledge_evidence": copy.deepcopy(input_record["knowledge_evidence"]),
        "binding_expectation": copy.deepcopy(input_record["binding_expectation"]),
        "binding_prior": copy.deepcopy(input_record["binding_prior"]),
    }


def _canonicalize_subject_refs(subject: dict[str, Any]) -> None:
    for name in (
        "supporting_repository_refs",
        "supporting_knowledge_refs",
        "limiting_or_counterevidence_refs",
    ):
        subject[name] = sorted(subject[name])


def _semantic_digest_material(
    input_record: dict[str, Any],
) -> dict[str, Any]:
    material = _digest_material(input_record)
    _canonicalize_subject_refs(material["subject"])
    material["repository_evidence"] = sorted(
        material["repository_evidence"],
        key=lambda item: item["ref"],
    )
    material["knowledge_evidence"] = sorted(
        material["knowledge_evidence"],
        key=lambda item: item["ref"],
    )
    prior = material["binding_prior"]
    if isinstance(prior, dict):
        prior_subject = prior["prior_subject"]
        if isinstance(prior_subject, dict):
            _canonicalize_subject_refs(prior_subject)
        if isinstance(prior["prior_repository_evidence"], list):
            prior["prior_repository_evidence"] = sorted(
                prior["prior_repository_evidence"],
                key=lambda item: item["ref"],
            )
        if isinstance(prior["prior_knowledge_evidence"], list):
            prior["prior_knowledge_evidence"] = sorted(
                prior["prior_knowledge_evidence"],
                key=lambda item: item["ref"],
            )
    return material


def _input_instance_digest(input_record: dict[str, Any]) -> str:
    return _sha256_bytes(_canonical_json(_digest_material(input_record)))


def _semantic_input_digest(input_record: dict[str, Any]) -> str:
    return _sha256_bytes(_canonical_json(_semantic_digest_material(input_record)))


def _validate_subject(
    subject: object,
    *,
    input_id: str,
) -> dict[str, Any]:
    if not isinstance(subject, dict):
        raise QualificationInputError(f"{input_id}_subject_not_object")
    _require_exact_keys(subject, SUBJECT_KEYS, f"{input_id}_subject")

    if not _is_sha40(subject["baseline_commit"]):
        raise QualificationInputError(f"{input_id}_baseline_commit")
    if not _is_sha256(subject["evidence_set_digest"]):
        raise QualificationInputError(f"{input_id}_evidence_set_digest")

    for name in (
        "focus_id",
        "relation_id",
        "classification",
        "statement",
        "rationale",
        "uncertainty_basis",
    ):
        if not _non_empty(subject[name]):
            raise QualificationInputError(f"{input_id}_{name}")

    if len(subject["statement"].encode("utf-8")) > MAX_STATEMENT_BYTES:
        raise QualificationInputError(f"{input_id}_statement_size")
    if len(subject["rationale"].encode("utf-8")) > MAX_RATIONALE_BYTES:
        raise QualificationInputError(f"{input_id}_rationale_size")

    for name in (
        "supporting_repository_refs",
        "supporting_knowledge_refs",
        "limiting_or_counterevidence_refs",
    ):
        _require_string_list(
            subject[name],
            label=f"{input_id}_{name}",
            allow_empty=True,
            max_items=MAX_REFS_PER_ROLE,
        )
    return subject


def _validate_evidence(
    value: object,
    *,
    input_id: str,
    collection: str,
    allow_empty_material: bool = False,
) -> tuple[list[dict[str, str]], dict[str, str]]:
    if not isinstance(value, list):
        raise QualificationInputError(f"{input_id}_{collection}_not_array")
    if len(value) > MAX_REFS_PER_ROLE:
        raise QualificationInputError(f"{input_id}_{collection}_too_many")

    validated: list[dict[str, str]] = []
    by_ref: dict[str, str] = {}
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            raise QualificationInputError(
                f"{input_id}_{collection}_{index}_not_object"
            )
        _require_exact_keys(
            item,
            EVIDENCE_ITEM_KEYS,
            f"{input_id}_{collection}_{index}",
        )
        ref = item["ref"]
        material = item["material"]
        if not _non_empty(ref):
            raise QualificationInputError(
                f"{input_id}_{collection}_{index}_ref"
            )
        if not isinstance(material, str):
            raise QualificationInputError(
                f"{input_id}_{collection}_{index}_material"
            )
        if material == "":
            if not allow_empty_material:
                raise QualificationInputError(
                    f"{input_id}_{collection}_{index}_material"
                )
        elif not _non_empty(material):
            raise QualificationInputError(
                f"{input_id}_{collection}_{index}_material"
            )
        if ref in by_ref:
            raise QualificationInputError(
                f"{input_id}_{collection}_duplicate_ref"
            )
        by_ref[ref] = material
        validated.append({"ref": ref, "material": material})

    return validated, by_ref


def _validate_binding_expectation(
    value: object,
    *,
    input_id: str,
) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise QualificationInputError(
            f"{input_id}_binding_expectation_not_object"
        )
    _require_exact_keys(
        value,
        BINDING_EXPECTATION_KEYS,
        f"{input_id}_binding_expectation",
    )

    kind = value["binding_kind"]
    if (
        not isinstance(kind, str)
        or kind not in {"NONE", "SUBJECT", "EVIDENCE_MATERIAL"}
    ):
        raise QualificationInputError(f"{input_id}_binding_kind")

    expected_subject = value["expected_subject_fingerprint"]
    expected_evidence = value["expected_evidence_material_digest"]

    if kind == "NONE":
        if expected_subject is not None or expected_evidence is not None:
            raise QualificationInputError(
                f"{input_id}_binding_none_payload"
            )
    elif kind == "SUBJECT":
        if not _is_sha256(expected_subject) or expected_evidence is not None:
            raise QualificationInputError(
                f"{input_id}_subject_binding_payload"
            )
    else:
        if expected_subject is not None or not _is_sha256(expected_evidence):
            raise QualificationInputError(
                f"{input_id}_evidence_binding_payload"
            )
    return value


def _validate_binding_prior(
    value: object,
    *,
    input_id: str,
    binding_kind: str,
) -> dict[str, Any] | None:
    if binding_kind == "NONE":
        if value is not None:
            raise QualificationInputError(f"{input_id}_unexpected_binding_prior")
        return None

    if not isinstance(value, dict):
        raise QualificationInputError(f"{input_id}_binding_prior_not_object")
    _require_exact_keys(value, BINDING_PRIOR_KEYS, f"{input_id}_binding_prior")

    if binding_kind == "SUBJECT":
        if not isinstance(value["prior_subject"], dict):
            raise QualificationInputError(
                f"{input_id}_prior_subject_missing"
            )
        if value["prior_repository_evidence"] is not None:
            raise QualificationInputError(
                f"{input_id}_prior_repository_evidence_must_be_null"
            )
        if value["prior_knowledge_evidence"] is not None:
            raise QualificationInputError(
                f"{input_id}_prior_knowledge_evidence_must_be_null"
            )
        _validate_subject(value["prior_subject"], input_id=f"{input_id}_prior")
        return value

    if value["prior_subject"] is not None:
        raise QualificationInputError(
            f"{input_id}_prior_subject_must_be_null"
        )
    prior_repository, _ = _validate_evidence(
        value["prior_repository_evidence"],
        input_id=f"{input_id}_prior",
        collection="repository_evidence",
    )
    prior_knowledge, _ = _validate_evidence(
        value["prior_knowledge_evidence"],
        input_id=f"{input_id}_prior",
        collection="knowledge_evidence",
    )
    if not prior_repository and not prior_knowledge:
        raise QualificationInputError(f"{input_id}_prior_evidence_empty")
    return value


def _validate_input(
    value: object,
    *,
    case_id: str,
    expected_input_id: str,
) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise QualificationInputError(f"{expected_input_id}_not_object")
    _require_exact_keys(value, INPUT_KEYS, expected_input_id)

    if value["input_id"] != expected_input_id:
        raise QualificationInputError(f"{expected_input_id}_identity")

    subject = _validate_subject(value["subject"], input_id=expected_input_id)
    allow_empty_material = case_id == "C10"
    repository, repository_by_ref = _validate_evidence(
        value["repository_evidence"],
        input_id=expected_input_id,
        collection="repository_evidence",
        allow_empty_material=allow_empty_material,
    )
    knowledge, knowledge_by_ref = _validate_evidence(
        value["knowledge_evidence"],
        input_id=expected_input_id,
        collection="knowledge_evidence",
        allow_empty_material=allow_empty_material,
    )
    binding = _validate_binding_expectation(
        value["binding_expectation"],
        input_id=expected_input_id,
    )
    prior = _validate_binding_prior(
        value["binding_prior"],
        input_id=expected_input_id,
        binding_kind=binding["binding_kind"],
    )

    reasons = _require_string_list(
        value["expected_reason_codes"],
        label=f"{expected_input_id}_expected_reason_codes",
        allow_empty=False,
        max_items=MAX_REASON_CODES,
    )
    _validate_reason_coherence(
        value["expected_outcome"],
        reasons,
        label=f"{expected_input_id}_expected",
    )

    allow_missing_support = case_id == "C10"
    for ref in subject["supporting_repository_refs"]:
        if ref not in repository_by_ref and not allow_missing_support:
            raise QualificationInputError(
                f"{expected_input_id}_repository_ref_unresolved"
            )
    for ref in subject["supporting_knowledge_refs"]:
        if ref not in knowledge_by_ref and not allow_missing_support:
            raise QualificationInputError(
                f"{expected_input_id}_knowledge_ref_unresolved"
            )

    shared_refs = set(repository_by_ref) & set(knowledge_by_ref)
    if any(
        repository_by_ref[ref] != knowledge_by_ref[ref]
        for ref in shared_refs
    ):
        raise QualificationInputError(
            f"{expected_input_id}_cross_role_material_conflict"
        )

    known_refs = set(repository_by_ref) | set(knowledge_by_ref)
    for ref in subject["limiting_or_counterevidence_refs"]:
        if ref not in known_refs:
            raise QualificationInputError(
                f"{expected_input_id}_limiting_ref_unresolved"
            )

    if case_id == "C05":
        limiting = subject["limiting_or_counterevidence_refs"]
        if not limiting:
            raise QualificationInputError("C05_limiting_refs_empty")
        if not any(
            ref in known_refs and (
                repository_by_ref.get(ref) or knowledge_by_ref.get(ref)
            )
            for ref in limiting
        ):
            raise QualificationInputError("C05_limiting_material_missing")

    if case_id == "C11":
        if binding["binding_kind"] != "SUBJECT" or prior is None:
            raise QualificationInputError("C11_subject_binding_missing")
        expected = binding["expected_subject_fingerprint"]
        prior_fingerprint = _subject_fingerprint(prior["prior_subject"])
        current_fingerprint = _subject_fingerprint(subject)
        if prior_fingerprint != expected:
            raise QualificationInputError("C11_prior_binding_mismatch")
        if current_fingerprint == expected:
            raise QualificationInputError("C11_binding_not_stale")

    elif case_id == "C12":
        if binding["binding_kind"] != "EVIDENCE_MATERIAL" or prior is None:
            raise QualificationInputError("C12_evidence_binding_missing")
        prior_repository = prior["prior_repository_evidence"]
        prior_knowledge = prior["prior_knowledge_evidence"]
        expected = binding["expected_evidence_material_digest"]
        prior_digest = _evidence_material_digest(
            prior_repository,
            prior_knowledge,
        )
        current_digest = _evidence_material_digest(repository, knowledge)
        if prior_digest != expected:
            raise QualificationInputError("C12_prior_binding_mismatch")
        if current_digest == expected:
            raise QualificationInputError("C12_binding_not_stale")
        prior_refs = {
            item["ref"] for item in prior_repository + prior_knowledge
        }
        current_refs = {
            item["ref"] for item in repository + knowledge
        }
        if prior_refs != current_refs:
            raise QualificationInputError("C12_logical_refs_changed")

    elif binding["binding_kind"] != "NONE" or prior is not None:
        raise QualificationInputError(
            f"{expected_input_id}_unexpected_binding_kind"
        )

    return value


def _validate_case_set(
    payload: dict[str, Any],
) -> list[dict[str, Any]]:
    _require_exact_keys(payload, CASE_SET_KEYS, "case_set")
    if payload["schema_version"] != CASE_SET_SCHEMA:
        raise QualificationInputError("case_set_schema_version")
    if payload["support_policy_version"] != SUPPORT_POLICY_VERSION:
        raise QualificationInputError("support_policy_version")

    cases = payload["cases"]
    if not isinstance(cases, list) or len(cases) != len(CASE_IDS):
        raise QualificationInputError("case_catalog_count")

    validated: list[dict[str, Any]] = []
    observed_case_ids: list[str] = []
    baseline_commits: set[str] = set()

    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            raise QualificationInputError(f"case_{index}_not_object")
        _require_exact_keys(case, CASE_KEYS, f"case_{index}")

        case_id = case["case_id"]
        if not isinstance(case_id, str) or case_id not in CASE_IDS:
            raise QualificationInputError("case_catalog_id")
        observed_case_ids.append(case_id)

        expected_class = CASE_CLASSES[CASE_IDS.index(case_id)]
        if case["case_class"] != expected_class:
            raise QualificationInputError(f"{case_id}_class")

        properties = _require_string_list(
            case["critical_properties"],
            label=f"{case_id}_critical_properties",
            allow_empty=True,
            max_items=len(KNOWN_PROPERTIES),
            require_sorted=True,
        )
        if any(item not in KNOWN_PROPERTIES for item in properties):
            raise QualificationInputError(
                f"{case_id}_critical_properties_unknown"
            )
        if not EXPECTED_PROPERTIES[case_id].issubset(
            set(properties)
        ):
            raise QualificationInputError(
                f"{case_id}_critical_properties_minimum_missing"
            )

        for identity_field in (
            "finding_producer_subject_id",
            "assessor_subject_id",
        ):
            if not _non_empty(case[identity_field]):
                raise QualificationInputError(
                    f"{case_id}_{identity_field}"
                )

        if case_id == "C17":
            if (
                case["finding_producer_subject_id"]
                != case["assessor_subject_id"]
            ):
                raise QualificationInputError("C17_self_cert_scenario_missing")

        expected_input_ids = (
            ["C13.I01", "C13.I02"]
            if case_id == "C13"
            else [f"{case_id}.I01"]
        )
        inputs = case["inputs"]
        if not isinstance(inputs, list):
            raise QualificationInputError(f"{case_id}_inputs_not_array")
        if len(inputs) != len(expected_input_ids):
            raise QualificationInputError(f"{case_id}_input_count")

        validated_inputs: list[dict[str, Any]] = []
        for value, expected_input_id in zip(
            inputs,
            expected_input_ids,
            strict=True,
        ):
            validated_input = _validate_input(
                value,
                case_id=case_id,
                expected_input_id=expected_input_id,
            )
            baseline_commits.add(
                validated_input["subject"]["baseline_commit"]
            )
            validated_inputs.append(validated_input)

        if case_id == "C13":
            if case["comparison_rule"] != "STABLE_OUTCOME_AND_REASONS":
                raise QualificationInputError("C13_comparison_rule")
            left, right = validated_inputs
            if _input_instance_digest(left) == _input_instance_digest(right):
                raise QualificationInputError("C13_instances_not_distinct")
            if _semantic_input_digest(left) != _semantic_input_digest(right):
                raise QualificationInputError("C13_semantic_digest_mismatch")
            if left["expected_outcome"] != right["expected_outcome"]:
                raise QualificationInputError("C13_expected_outcome_mismatch")
            if sorted(left["expected_reason_codes"]) != sorted(
                right["expected_reason_codes"]
            ):
                raise QualificationInputError("C13_expected_reasons_mismatch")
        elif case["comparison_rule"] != "NONE":
            raise QualificationInputError(f"{case_id}_comparison_rule")

        validated.append(case)

    if observed_case_ids != list(CASE_IDS):
        if len(set(observed_case_ids)) != len(observed_case_ids):
            raise QualificationInputError("case_catalog_duplicate")
        raise QualificationInputError("case_catalog_exact_order")

    if len(baseline_commits) != 1:
        raise QualificationInputError("baseline_commit_not_uniform")

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
) -> tuple[
    dict[str, Any],
    dict[str, dict[str, dict[str, Any]]],
]:
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
    mechanism_kind = mechanism["mechanism_kind"]
    if (
        not isinstance(mechanism_kind, str)
        or mechanism_kind
        not in {"DETERMINISTIC", "MODEL_BASED", "HUMAN_REVIEWED"}
    ):
        raise QualificationInputError("assessor_mechanism_kind")
    if mechanism_kind == "MODEL_BASED":
        _validate_model_provenance(mechanism["model_provenance"])
    elif mechanism["model_provenance"] is not None:
        raise QualificationInputError(
            "assessor_mechanism_model_provenance"
        )

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

    artifact_cases = payload["case_results"]
    if not isinstance(artifact_cases, list):
        raise QualificationInputError("artifact_case_results_not_array")
    if len(artifact_cases) != len(CASE_IDS):
        raise QualificationInputError("artifact_case_count")

    expected_cases = {case["case_id"]: case for case in cases}
    observed_by_case: dict[str, dict[str, dict[str, Any]]] = {}

    for index, artifact_case in enumerate(artifact_cases):
        if not isinstance(artifact_case, dict):
            raise QualificationInputError(
                f"artifact_case_{index}_not_object"
            )
        _require_exact_keys(
            artifact_case,
            ARTIFACT_CASE_KEYS,
            f"artifact_case_{index}",
        )

        case_id = artifact_case["case_id"]
        if not isinstance(case_id, str) or case_id not in expected_cases:
            raise QualificationInputError("artifact_case_unknown")
        if case_id in observed_by_case:
            raise QualificationInputError("artifact_case_duplicate")

        expected_inputs = {
            item["input_id"]: item
            for item in expected_cases[case_id]["inputs"]
        }
        observations = artifact_case["observations"]
        if not isinstance(observations, list):
            raise QualificationInputError(
                f"{case_id}_observations_not_array"
            )
        if len(observations) != len(expected_inputs):
            raise QualificationInputError(
                f"{case_id}_observation_count"
            )

        observed_inputs: dict[str, dict[str, Any]] = {}
        for obs_index, observation in enumerate(observations):
            if not isinstance(observation, dict):
                raise QualificationInputError(
                    f"{case_id}_observation_{obs_index}_not_object"
                )
            _require_exact_keys(
                observation,
                OBSERVATION_KEYS,
                f"{case_id}_observation_{obs_index}",
            )
            input_id = observation["input_id"]
            if (
                not isinstance(input_id, str)
                or input_id not in expected_inputs
            ):
                raise QualificationInputError(
                    f"{case_id}_observation_unknown_input"
                )
            if input_id in observed_inputs:
                raise QualificationInputError(
                    f"{case_id}_observation_duplicate_input"
                )

            expected_input = expected_inputs[input_id]
            if not _is_sha256(observation["input_instance_digest"]):
                raise QualificationInputError(
                    f"{input_id}_input_instance_digest"
                )
            if (
                observation["input_instance_digest"]
                != _input_instance_digest(expected_input)
            ):
                raise QualificationInputError(
                    f"{input_id}_input_instance_digest_mismatch"
                )

            if not _is_sha256(observation["semantic_input_digest"]):
                raise QualificationInputError(
                    f"{input_id}_semantic_input_digest"
                )
            if (
                observation["semantic_input_digest"]
                != _semantic_input_digest(expected_input)
            ):
                raise QualificationInputError(
                    f"{input_id}_semantic_input_digest_mismatch"
                )

            if not _is_sha256(observation["subject_fingerprint"]):
                raise QualificationInputError(
                    f"{input_id}_subject_fingerprint"
                )
            if (
                observation["subject_fingerprint"]
                != _subject_fingerprint(expected_input["subject"])
            ):
                raise QualificationInputError(
                    f"{input_id}_subject_fingerprint_mismatch"
                )

            reasons = _require_string_list(
                observation["reason_codes"],
                label=f"{input_id}_observed_reason_codes",
                allow_empty=False,
                max_items=MAX_REASON_CODES,
            )
            _validate_reason_coherence(
                observation["outcome"],
                reasons,
                label=f"{input_id}_observed",
            )
            observed_inputs[input_id] = observation

        if set(observed_inputs) != set(expected_inputs):
            raise QualificationInputError(
                f"{case_id}_observation_catalog"
            )
        observed_by_case[case_id] = observed_inputs

    if set(observed_by_case) != set(CASE_IDS):
        raise QualificationInputError("artifact_case_catalog")

    return mechanism, observed_by_case


def _empty_metrics() -> dict[str, float | int]:
    return {
        "false_support_acceptance_rate": 0,
        "unsupported_claim_escape_rate": 0,
        "false_inconclusive_rate": 0,
        "contradiction_handling_recall": 0,
        "assessment_stability_on_equivalent_inputs": 0,
        "binding_drift_detection_rate": 0,
    }


def _rate(
    numerator: int,
    denominator: int,
    *,
    label: str,
) -> float:
    if denominator == 0:
        raise QualificationInputError(f"{label}_zero_denominator")
    return numerator / denominator


def _evaluate(
    cases: list[dict[str, Any]],
    observed_by_case: dict[str, dict[str, dict[str, Any]]],
) -> tuple[
    list[dict[str, Any]],
    dict[str, float],
    str,
    str,
    str,
    list[str],
]:
    case_results: list[dict[str, Any]] = []
    flattened: list[
        tuple[dict[str, Any], dict[str, Any], dict[str, Any]]
    ] = []

    for case in cases:
        case_id = case["case_id"]
        input_results: list[dict[str, Any]] = []
        case_mismatches: list[str] = []

        for expected_input in case["inputs"]:
            input_id = expected_input["input_id"]
            observation = observed_by_case[case_id][input_id]
            flattened.append((case, expected_input, observation))

            mismatch_reasons: list[str] = []
            if observation["outcome"] != expected_input["expected_outcome"]:
                mismatch_reasons.append("OUTCOME_MISMATCH")
            if sorted(observation["reason_codes"]) != sorted(
                expected_input["expected_reason_codes"]
            ):
                mismatch_reasons.append("REASON_CODES_MISMATCH")

            input_result = "FAIL" if mismatch_reasons else "PASS"
            if input_result == "FAIL":
                case_mismatches.append(f"{input_id}_FAIL")

            input_results.append(
                {
                    "input_id": input_id,
                    "expected_disposition": expected_input["expected_outcome"],
                    "observed_disposition": observation["outcome"],
                    "expected_reason_codes": expected_input[
                        "expected_reason_codes"
                    ],
                    "observed_reason_codes": observation["reason_codes"],
                    "input_result": input_result,
                    "mismatch_reasons": mismatch_reasons,
                }
            )

        comparison_result: dict[str, Any] | None = None
        if case["comparison_rule"] == "STABLE_OUTCOME_AND_REASONS":
            left_id = "C13.I01"
            right_id = "C13.I02"
            left = observed_by_case[case_id][left_id]
            right = observed_by_case[case_id][right_id]
            comparison_mismatches: list[str] = []
            if left["outcome"] != right["outcome"]:
                comparison_mismatches.append("OUTCOME_INSTABILITY")
            if sorted(left["reason_codes"]) != sorted(right["reason_codes"]):
                comparison_mismatches.append("REASON_CODES_INSTABILITY")
            comparison_state = (
                "FAIL" if comparison_mismatches else "PASS"
            )
            if comparison_state == "FAIL":
                case_mismatches.append("COMPARISON_FAIL")
            comparison_result = {
                "rule": "STABLE_OUTCOME_AND_REASONS",
                "input_ids": [left_id, right_id],
                "result": comparison_state,
                "mismatch_reasons": comparison_mismatches,
            }

        case_results.append(
            {
                "case_id": case_id,
                "input_results": input_results,
                "comparison_result": comparison_result,
                "case_result": "FAIL" if case_mismatches else "PASS",
                "mismatch_reasons": case_mismatches,
            }
        )

    expected_non_support = [
        item
        for item in flattened
        if item[1]["expected_outcome"] != "SUPPORTED"
    ]
    false_support = sum(
        observation["outcome"] == "SUPPORTED"
        for _, _, observation in expected_non_support
    )

    unsupported = [
        item
        for item in flattened
        if "UNSUPPORTED_ESCAPE" in item[0]["critical_properties"]
    ]
    unsupported_escape = sum(
        observation["outcome"] == "SUPPORTED"
        for _, _, observation in unsupported
    )

    expected_non_inconclusive = [
        item
        for item in flattened
        if item[1]["expected_outcome"] != "INCONCLUSIVE"
    ]
    false_inconclusive = sum(
        observation["outcome"] == "INCONCLUSIVE"
        for _, _, observation in expected_non_inconclusive
    )

    contradiction = [
        item
        for item in flattened
        if "UNRESOLVED_COUNTEREVIDENCE"
        in item[0]["critical_properties"]
    ]
    contradiction_hits = sum(
        observation["outcome"] == "INCONCLUSIVE"
        and "MATERIAL_COUNTEREVIDENCE_UNRESOLVED"
        in observation["reason_codes"]
        for _, _, observation in contradiction
    )

    binding = [
        item
        for item in flattened
        if "BINDING_DRIFT" in item[0]["critical_properties"]
    ]
    binding_hits = sum(
        observation["outcome"] == "INCONCLUSIVE"
        and "SUBJECT_BINDING_MISMATCH" in observation["reason_codes"]
        for _, _, observation in binding
    )

    equivalent_cases = [
        case
        for case in cases
        if case["comparison_rule"] == "STABLE_OUTCOME_AND_REASONS"
    ]
    stable_pairs = 0
    for case in equivalent_cases:
        observations = observed_by_case[case["case_id"]]
        left = observations["C13.I01"]
        right = observations["C13.I02"]
        if (
            left["outcome"] == right["outcome"]
            and sorted(left["reason_codes"])
            == sorted(right["reason_codes"])
        ):
            stable_pairs += 1

    self_cert_positive = any(
        "SELF_CERTIFICATION" in case["critical_properties"]
        and observation["outcome"] == "SUPPORTED"
        for case, _, observation in flattened
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
            len(contradiction),
            label="contradiction_handling_recall",
        ),
        "assessment_stability_on_equivalent_inputs": _rate(
            stable_pairs,
            len(equivalent_cases),
            label="assessment_stability_on_equivalent_inputs",
        ),
        "binding_drift_detection_rate": _rate(
            binding_hits,
            len(binding),
            label="binding_drift_detection_rate",
        ),
    }

    any_case_fail = any(
        case_result["case_result"] == "FAIL"
        for case_result in case_results
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

    diagnostic_exact_match_result = "FAIL" if any_case_fail else "PASS"
    safety_floor_result = "PASS" if safety_ok else "FAIL"
    qualification_result = (
        "PASS"
        if diagnostic_exact_match_result == "PASS"
        and safety_floor_result == "PASS"
        else "FAIL"
    )

    return (
        case_results,
        metrics,
        diagnostic_exact_match_result,
        safety_floor_result,
        qualification_result,
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
        "qualification_runner_digest": _sha256_bytes(
            Path(__file__).read_bytes()
        ),
        "assessor_mechanism_identity": mechanism_identity,
        "assessor_result_artifact_digest": artifact_digest,
        "case_count": 18,
        "input_count": 19,
        "case_results": [],
        "metrics": _empty_metrics(),
        "diagnostic_exact_match_result": "INCONCLUSIVE",
        "safety_floor_result": "INCONCLUSIVE",
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
        baseline_commit = cases[0]["inputs"][0]["subject"][
            "baseline_commit"
        ]

        if not _non_empty(args.ground_truth_reviewer_id):
            raise QualificationInputError("ground_truth_reviewer_id")
        if not _non_empty(args.runner_implementation_actor_id):
            raise QualificationInputError("runner_implementation_actor_id")
        if (
            args.ground_truth_reviewer_id
            == args.runner_implementation_actor_id
        ):
            raise QualificationInputError("reviewer_runner_collision")
        if not _is_sha256(args.reviewed_case_set_digest):
            raise QualificationInputError(
                "reviewed_case_set_digest_invalid"
            )
        if args.reviewed_case_set_digest != case_digest:
            raise QualificationInputError(
                "reviewed_case_set_digest_mismatch"
            )
        if any(
            args.ground_truth_reviewer_id
            == case["finding_producer_subject_id"]
            for case in cases
        ):
            raise QualificationInputError(
                "reviewer_finding_producer_collision"
            )

        artifact_payload, artifact_bytes = _read_json(
            artifact_path,
            max_bytes=MAX_RESULT_BYTES,
            label="assessor_results",
        )
        artifact_digest = _sha256_bytes(artifact_bytes)
        mechanism, observed_by_case = _validate_artifact(
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

        if (
            args.ground_truth_reviewer_id
            == mechanism["assessor_subject_id"]
        ):
            raise QualificationInputError("reviewer_assessor_collision")

        if (
            mechanism["producer_subject_id"]
            == mechanism["assessor_subject_id"]
        ):
            any_positive = any(
                observation["outcome"] == "SUPPORTED"
                for observations in observed_by_case.values()
                for observation in observations.values()
            )
            output = _base_output(
                case_set_digest=case_digest,
                reviewed_case_set_digest=args.reviewed_case_set_digest,
                reviewer_id=args.ground_truth_reviewer_id,
                baseline_commit=baseline_commit,
                artifact_digest=artifact_digest,
                mechanism_identity=mechanism_identity,
            )
            output["qualification_result"] = (
                "FAIL" if any_positive else "INCONCLUSIVE"
            )
            output["diagnostic_exact_match_result"] = "INCONCLUSIVE"
            output["safety_floor_result"] = (
                "FAIL" if any_positive else "INCONCLUSIVE"
            )
            output["qualification_reasons"] = ["SELF_CERTIFICATION"]
            _write_output(output)
            return 1 if any_positive else 2

        (
            case_results,
            metrics,
            diagnostic_result,
            safety_result,
            result,
            reasons,
        ) = _evaluate(
            cases,
            observed_by_case,
        )
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
        output["diagnostic_exact_match_result"] = diagnostic_result
        output["safety_floor_result"] = safety_result
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
