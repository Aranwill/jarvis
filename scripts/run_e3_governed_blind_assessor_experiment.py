from __future__ import annotations

"""Governed E3 blind-assessor experiment harness V0.

This evaluation-side harness composes existing Malāk primitives. It does not
select a model/provider, perform network access, write repository state, wire
support_sufficient, or elevate authority.
"""

import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Callable

from malak.capabilities._engineering_analysis import (
    assess_governed_evidence_support_v0,
    governed_evidence_support_finding_fingerprint,
    project_blind_support_assessor_input_v0,
)


PROFILE_SCHEMA = "MALAK-E3-BLIND-ASSESSOR-EXPERIMENT-PROFILE/v0"
HARNESS_POLICY_VERSION = "e3-governed-blind-assessor-experiment-harness/v0"
RESULTS_SCHEMA = "MALAK-E3-SUPPORT-ASSESSOR-RESULTS/v0.1"
CASE_SET_SCHEMA = "MALAK-E3-SUPPORT-ASSESSOR-CASESET/v0.1"
SUPPORT_POLICY_VERSION = "e3-governed-evidence-support/v0"
MAX_REASON_CODES = 10
RESULT_OUTCOMES = {"SUPPORTED", "INSUFFICIENT", "INCONCLUSIVE"}
RESULT_REASONS = {
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

CASE_IDS = tuple(f"C{i:02d}" for i in range(1, 19))
EXPECTED_INPUT_IDS = (
    "C01.I01", "C02.I01", "C03.I01", "C04.I01", "C05.I01",
    "C06.I01", "C07.I01", "C08.I01", "C09.I01", "C10.I01",
    "C11.I01", "C12.I01", "C13.I01", "C13.I02", "C14.I01",
    "C15.I01", "C16.I01", "C17.I01", "C18.I01",
)
PROFILE_KEYS = {
    "schema_version",
    "harness_policy_version",
    "expected_case_set_schema_version",
    "expected_case_set_digest",
    "execution_order",
    "max_attempts_per_input",
    "expected_input_count",
    "expected_observation_count",
    "expected_candidate_invocations",
    "artifact_max_bytes",
    "candidate_argument_policy",
    "expected_mechanism",
    "fault_modes",
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
FAULT_KEYS = {"input_id", "mode"}
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

NETWORK_AUTHORIZED = False
REPO_WRITES_AUTHORIZED = False
SUPPORT_SUFFICIENT_WIRING_AUTHORIZED = False
MODEL_PROVIDER_EXECUTION_AUTHORIZED = False
RDD_STAGE_2_AUTHORIZED = False
AUTHORITY_EFFECT = "none"


class ExperimentProfileError(ValueError):
    """Fail-closed profile validation error."""


class ExperimentBindingError(ValueError):
    """Fail-closed experiment/case-set/artifact binding error."""


def _canonical_json(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _is_sha256(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(char in "0123456789abcdef" for char in value)
    )


def _non_empty(value: object) -> bool:
    return isinstance(value, str) and value == value.strip() and bool(value)


def _reject_duplicate_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_nonfinite(value: str) -> None:
    raise ValueError(f"non-finite JSON constant: {value}")


def _decode_json_object(raw: bytes, *, label: str) -> dict[str, Any]:
    try:
        payload = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=_reject_duplicate_pairs,
            parse_constant=_reject_nonfinite,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise ValueError(f"{label}_malformed") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"{label}_not_object")
    return payload


def _require_exact_keys(
    value: dict[str, Any],
    expected: set[str],
    *,
    label: str,
    error_type: type[ValueError],
) -> None:
    if set(value) != expected:
        raise error_type(f"{label}_schema_mismatch")


def _validate_mechanism(value: object) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ExperimentProfileError("expected_mechanism_not_object")
    _require_exact_keys(
        value,
        MECHANISM_KEYS,
        label="expected_mechanism",
        error_type=ExperimentProfileError,
    )
    for field in (
        "mechanism_id",
        "mechanism_version",
        "producer_subject_id",
        "assessor_subject_id",
    ):
        if not _non_empty(value[field]):
            raise ExperimentProfileError(f"expected_mechanism_{field}")
    if value["mechanism_kind"] not in {
        "DETERMINISTIC",
        "HUMAN_REVIEWED",
        "MODEL_BASED",
    }:
        raise ExperimentProfileError("expected_mechanism_kind")
    if not _is_sha256(value["config_digest"]):
        raise ExperimentProfileError("expected_mechanism_config_digest")

    provenance = value["model_provenance"]
    if value["mechanism_kind"] in {"DETERMINISTIC", "HUMAN_REVIEWED"}:
        if provenance is not None:
            raise ExperimentProfileError("unexpected_model_provenance")
    else:
        if not isinstance(provenance, dict):
            raise ExperimentProfileError("model_provenance_missing")
        _require_exact_keys(
            provenance,
            MODEL_PROVENANCE_KEYS,
            label="model_provenance",
            error_type=ExperimentProfileError,
        )
        for field, item in provenance.items():
            if field.endswith("_digest"):
                if not _is_sha256(item):
                    raise ExperimentProfileError(f"model_provenance_{field}")
            elif not _non_empty(item):
                raise ExperimentProfileError(f"model_provenance_{field}")
    return copy.deepcopy(value)


def _validate_profile_object(value: object) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ExperimentProfileError("profile_not_object")
    _require_exact_keys(
        value,
        PROFILE_KEYS,
        label="profile",
        error_type=ExperimentProfileError,
    )

    exact_strings = {
        "schema_version": PROFILE_SCHEMA,
        "harness_policy_version": HARNESS_POLICY_VERSION,
        "expected_case_set_schema_version": CASE_SET_SCHEMA,
        "execution_order": "CASESET_INPUT_ORDER_SEQUENTIAL",
        "candidate_argument_policy": "EXISTING_SUPPORT_ASSESSMENT_MATERIAL_ONLY",
    }
    for field, expected in exact_strings.items():
        if value[field] != expected:
            raise ExperimentProfileError(f"profile_{field}")

    if not _is_sha256(value["expected_case_set_digest"]):
        raise ExperimentProfileError("profile_expected_case_set_digest")

    exact_integers = {
        "max_attempts_per_input": 1,
        "expected_input_count": 19,
        "expected_observation_count": 19,
        "expected_candidate_invocations": 13,
        "artifact_max_bytes": 524288,
    }
    for field, expected in exact_integers.items():
        item = value[field]
        if type(item) is not int or item != expected:
            raise ExperimentProfileError(f"profile_{field}")

    _validate_mechanism(value["expected_mechanism"])

    faults = value["fault_modes"]
    if not isinstance(faults, list) or len(faults) != len(EXPECTED_INPUT_IDS):
        raise ExperimentProfileError("fault_modes_count")

    observed_ids: list[str] = []
    for index, fault in enumerate(faults):
        if not isinstance(fault, dict):
            raise ExperimentProfileError(f"fault_mode_{index}_not_object")
        _require_exact_keys(
            fault,
            FAULT_KEYS,
            label=f"fault_mode_{index}",
            error_type=ExperimentProfileError,
        )
        input_id = fault["input_id"]
        mode = fault["mode"]
        if input_id != EXPECTED_INPUT_IDS[index]:
            raise ExperimentProfileError("fault_modes_order")
        if mode not in {
            "NORMAL",
            "FORCE_UNAVAILABLE",
            "FORCE_MALFORMED_OUTPUT",
        }:
            raise ExperimentProfileError("fault_mode_unknown")
        expected_mode = (
            "FORCE_UNAVAILABLE"
            if input_id == "C14.I01"
            else (
                "FORCE_MALFORMED_OUTPUT"
                if input_id == "C15.I01"
                else "NORMAL"
            )
        )
        if mode != expected_mode:
            raise ExperimentProfileError("fault_mode_mapping")
        observed_ids.append(input_id)

    if len(set(observed_ids)) != len(observed_ids):
        raise ExperimentProfileError("fault_modes_duplicate")

    return copy.deepcopy(value)


def load_experiment_profile_v0(path: Path) -> dict[str, Any]:
    """Load and strictly validate the frozen V0 experiment profile."""
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise ExperimentProfileError("profile_unreadable") from exc
    try:
        payload = _decode_json_object(raw, label="profile")
    except ValueError as exc:
        raise ExperimentProfileError(str(exc)) from exc
    return _validate_profile_object(payload)


def build_expected_harness_v0(profile: dict[str, Any]) -> dict[str, str]:
    """Derive the exact four-field expected harness object."""
    validated = _validate_profile_object(profile)
    budget = {
        "artifact_max_bytes": validated["artifact_max_bytes"],
        "expected_candidate_invocations": validated["expected_candidate_invocations"],
        "expected_input_count": validated["expected_input_count"],
        "expected_observation_count": validated["expected_observation_count"],
    }
    attempt = {
        "execution_order": validated["execution_order"],
        "max_attempts_per_input": validated["max_attempts_per_input"],
    }
    return {
        "harness_policy_version": validated["harness_policy_version"],
        "harness_policy_digest": _sha256_bytes(_canonical_json(validated)),
        "budget_manifest_digest": _sha256_bytes(_canonical_json(budget)),
        "attempt_policy_digest": _sha256_bytes(_canonical_json(attempt)),
    }


def verify_expected_experiment_binding_v0(
    *,
    profile: dict[str, Any],
    artifact: dict[str, Any],
) -> None:
    """Fail closed unless mechanism and full expected harness match exactly."""
    validated = _validate_profile_object(profile)
    if not isinstance(artifact, dict):
        raise ExperimentBindingError("artifact_not_object")
    if artifact.get("assessor_mechanism") != validated["expected_mechanism"]:
        raise ExperimentBindingError("assessor_mechanism_mismatch")
    if artifact.get("harness") != build_expected_harness_v0(validated):
        raise ExperimentBindingError("harness_binding_mismatch")


def _subject_fingerprint(subject: dict[str, Any]) -> str:
    return governed_evidence_support_finding_fingerprint(**subject)


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


def _semantic_digest_material(input_record: dict[str, Any]) -> dict[str, Any]:
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


def _load_case_set(
    path: Path,
    *,
    profile: dict[str, Any],
) -> tuple[dict[str, Any], bytes]:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise ExperimentBindingError("case_set_unreadable") from exc
    if len(raw) > 1024 * 1024:
        raise ExperimentBindingError("case_set_size_exceeded")
    if _sha256_bytes(raw) != profile["expected_case_set_digest"]:
        raise ExperimentBindingError("case_set_digest_mismatch")
    try:
        payload = _decode_json_object(raw, label="case_set")
    except ValueError as exc:
        raise ExperimentBindingError(str(exc)) from exc

    _require_exact_keys(
        payload,
        CASE_SET_KEYS,
        label="case_set",
        error_type=ExperimentBindingError,
    )
    if payload["schema_version"] != profile["expected_case_set_schema_version"]:
        raise ExperimentBindingError("case_set_schema_version")
    if payload["support_policy_version"] != SUPPORT_POLICY_VERSION:
        raise ExperimentBindingError("support_policy_version")

    cases = payload["cases"]
    if not isinstance(cases, list) or len(cases) != len(CASE_IDS):
        raise ExperimentBindingError("case_count")

    observed_case_ids: list[str] = []
    observed_input_ids: list[str] = []
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            raise ExperimentBindingError(f"case_{index}_not_object")
        _require_exact_keys(
            case,
            CASE_KEYS,
            label=f"case_{index}",
            error_type=ExperimentBindingError,
        )
        if case["case_id"] != CASE_IDS[index]:
            raise ExperimentBindingError("case_order")
        observed_case_ids.append(case["case_id"])

        inputs = case["inputs"]
        if not isinstance(inputs, list):
            raise ExperimentBindingError(f"{case['case_id']}_inputs")
        expected_count = 2 if case["case_id"] == "C13" else 1
        if len(inputs) != expected_count:
            raise ExperimentBindingError(f"{case['case_id']}_input_count")
        for item in inputs:
            if not isinstance(item, dict):
                raise ExperimentBindingError("input_not_object")
            _require_exact_keys(
                item,
                INPUT_KEYS,
                label="case_input",
                error_type=ExperimentBindingError,
            )
            observed_input_ids.append(item["input_id"])

    if tuple(observed_case_ids) != CASE_IDS:
        raise ExperimentBindingError("case_catalog")
    if tuple(observed_input_ids) != EXPECTED_INPUT_IDS:
        raise ExperimentBindingError("input_catalog")
    if len(observed_input_ids) != profile["expected_input_count"]:
        raise ExperimentBindingError("profile_input_count_mismatch")
    return payload, raw


def _binding_drift(visible: dict[str, Any]) -> bool:
    binding = visible["binding_expectation"]
    kind = binding.get("binding_kind")
    if kind == "NONE":
        return False
    if kind == "SUBJECT":
        expected = binding.get("expected_subject_fingerprint")
        return (
            not _is_sha256(expected)
            or _subject_fingerprint(visible["subject"]) != expected
        )
    if kind == "EVIDENCE_MATERIAL":
        expected = binding.get("expected_evidence_material_digest")
        return (
            not _is_sha256(expected)
            or _evidence_material_digest(
                visible["repository_evidence"],
                visible["knowledge_evidence"],
            )
            != expected
        )
    raise ExperimentBindingError("binding_kind_unknown")


def _assessment(
    *,
    visible: dict[str, Any],
    case: dict[str, Any],
    assessor: Callable[[dict[str, Any]], dict[str, Any]] | None,
    force_binding_mismatch: bool = False,
):
    subject = visible["subject"]
    expected_binding = (
        {"baseline_commit": "__binding_mismatch__"}
        if force_binding_mismatch
        else None
    )
    return assess_governed_evidence_support_v0(
        policy_version=SUPPORT_POLICY_VERSION,
        baseline_commit=subject["baseline_commit"],
        focus_id=subject["focus_id"],
        evidence_set_digest=subject["evidence_set_digest"],
        relation_id=subject["relation_id"],
        classification=subject["classification"],
        statement=subject["statement"],
        rationale=subject["rationale"],
        supporting_repository_refs=subject["supporting_repository_refs"],
        supporting_knowledge_refs=subject["supporting_knowledge_refs"],
        limiting_or_counterevidence_refs=subject["limiting_or_counterevidence_refs"],
        uncertainty_basis=subject["uncertainty_basis"],
        repository_evidence=visible["repository_evidence"],
        knowledge_evidence=visible["knowledge_evidence"],
        assessor_subject_id=case["assessor_subject_id"],
        finding_producer_subject_id=case["finding_producer_subject_id"],
        assessor=assessor,
        expected_binding=expected_binding,
    )


def _malformed_fault_stub(_material: dict[str, Any]) -> dict[str, Any]:
    return {"malformed": True}


def _validate_observation_output_contract(
    *,
    outcome: str,
    reason_codes: list[str],
) -> None:
    """Enforce the existing RESULTS/v0.1 consumer contract before return."""
    if outcome not in RESULT_OUTCOMES:
        raise ExperimentBindingError("observation_outcome_invalid")
    if not reason_codes or len(reason_codes) > MAX_REASON_CODES:
        raise ExperimentBindingError("observation_reason_count_invalid")
    if any(reason not in RESULT_REASONS for reason in reason_codes):
        raise ExperimentBindingError("observation_reason_unknown")
    if len(set(reason_codes)) != len(reason_codes):
        raise ExperimentBindingError("observation_reason_duplicate")

    if outcome == "SUPPORTED":
        if reason_codes != ["MATERIAL_SUPPORT_CONFIRMED"]:
            raise ExperimentBindingError("observation_supported_reason_invalid")
        return

    if "MATERIAL_SUPPORT_CONFIRMED" in reason_codes:
        raise ExperimentBindingError("observation_positive_reason_mismatch")

    if outcome == "INSUFFICIENT":
        allowed = {
            "SUPPORTING_REFS_IRRELEVANT",
            "SUPPORTING_REFS_INSUFFICIENT",
        }
        if any(reason not in allowed for reason in reason_codes):
            raise ExperimentBindingError("observation_insufficient_reason_invalid")


def run_governed_blind_assessor_experiment_v0(
    *,
    case_set_path: Path,
    profile_path: Path,
    assessor: Callable[[dict[str, Any]], dict[str, Any]],
) -> dict[str, Any]:
    """Produce the bounded RESULTS/v0.1 artifact for the exact V0 case-set."""
    if not callable(assessor):
        raise TypeError("assessor must be callable")

    profile = load_experiment_profile_v0(profile_path)
    case_set, case_bytes = _load_case_set(case_set_path, profile=profile)
    mode_by_id = {
        item["input_id"]: item["mode"] for item in profile["fault_modes"]
    }

    real_candidate_invocations = 0

    def tracked_assessor(material: dict[str, Any]) -> dict[str, Any]:
        nonlocal real_candidate_invocations
        real_candidate_invocations += 1
        return assessor(material)

    case_results: list[dict[str, Any]] = []
    observations_produced = 0

    for case in case_set["cases"]:
        observations: list[dict[str, Any]] = []
        for input_record in case["inputs"]:
            input_id = input_record["input_id"]
            mode = mode_by_id[input_id]

            visible = project_blind_support_assessor_input_v0(input_record)
            drift = _binding_drift(visible)

            if mode == "FORCE_UNAVAILABLE":
                selected_assessor = None
                force_binding_mismatch = False
            elif mode == "FORCE_MALFORMED_OUTPUT":
                selected_assessor = _malformed_fault_stub
                force_binding_mismatch = False
            elif drift:
                selected_assessor = tracked_assessor
                force_binding_mismatch = True
            else:
                selected_assessor = tracked_assessor
                force_binding_mismatch = False

            result = _assessment(
                visible=visible,
                case=case,
                assessor=selected_assessor,
                force_binding_mismatch=force_binding_mismatch,
            )
            outcome_value = result.outcome.value
            reason_values = [reason.value for reason in result.reason_codes]
            _validate_observation_output_contract(
                outcome=outcome_value,
                reason_codes=reason_values,
            )
            observations.append(
                {
                    "input_id": input_id,
                    "input_instance_digest": _input_instance_digest(input_record),
                    "semantic_input_digest": _semantic_input_digest(input_record),
                    "subject_fingerprint": _subject_fingerprint(visible["subject"]),
                    "outcome": outcome_value,
                    "reason_codes": reason_values,
                }
            )
            observations_produced += 1

        case_results.append(
            {
                "case_id": case["case_id"],
                "observations": observations,
            }
        )

    if observations_produced != profile["expected_observation_count"]:
        raise ExperimentBindingError("observation_count_mismatch")
    if real_candidate_invocations != profile["expected_candidate_invocations"]:
        raise ExperimentBindingError("candidate_invocation_count_mismatch")

    artifact = {
        "schema_version": RESULTS_SCHEMA,
        "case_set_digest": _sha256_bytes(case_bytes),
        "assessor_mechanism": copy.deepcopy(profile["expected_mechanism"]),
        "harness": build_expected_harness_v0(profile),
        "case_results": case_results,
    }
    if len(_canonical_json(artifact)) > profile["artifact_max_bytes"]:
        raise ExperimentBindingError("artifact_size_exceeded")

    verify_expected_experiment_binding_v0(profile=profile, artifact=artifact)
    return artifact
