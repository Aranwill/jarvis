from __future__ import annotations

import copy
import hashlib
import importlib.util
import inspect
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
CASE_SET = ROOT / "evaluations" / "e3_governed_evidence_support_assessor_v0" / "cases.json"
PROFILE = ROOT / "evaluations" / "e3_governed_evidence_support_assessor_v0" / "experiment_profile.json"
RUNNER = ROOT / "scripts" / "run_e3_governed_blind_assessor_experiment.py"

PROFILE_SCHEMA = "MALAK-E3-BLIND-ASSESSOR-EXPERIMENT-PROFILE/v0"
HARNESS_POLICY_VERSION = "e3-governed-blind-assessor-experiment-harness/v0"
CASE_SET_SCHEMA = "MALAK-E3-SUPPORT-ASSESSOR-CASESET/v0.1"
RESULTS_SCHEMA = "MALAK-E3-SUPPORT-ASSESSOR-RESULTS/v0.1"

EXPECTED_INPUT_IDS = [
    "C01.I01", "C02.I01", "C03.I01", "C04.I01", "C05.I01",
    "C06.I01", "C07.I01", "C08.I01", "C09.I01", "C10.I01",
    "C11.I01", "C12.I01", "C13.I01", "C13.I02", "C14.I01",
    "C15.I01", "C16.I01", "C17.I01", "C18.I01",
]
STRUCTURAL_ZERO_CALL = {"C10.I01", "C11.I01", "C12.I01", "C17.I01"}
FAULT_ZERO_CALL = {"C14.I01", "C15.I01"}
FORBIDDEN_CANDIDATE_KEYS = {
    "input_id",
    "case_id",
    "case_class",
    "critical_properties",
    "expected_outcome",
    "expected_reason_codes",
    "binding_prior",
    "fault_mode",
    "profile",
    "qualification_result",
}
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
HARNESS_KEYS = {
    "harness_policy_version",
    "harness_policy_digest",
    "budget_manifest_digest",
    "attempt_policy_digest",
}

REQUIREMENT_COVERAGE = {
    **{f"R{i:02d}": "profile/corpus admission" for i in range(1, 4)},
    **{f"R{i:02d}": "blind candidate boundary" for i in range(4, 11)},
    **{f"R{i:02d}": "structural/fault/call discipline" for i in range(11, 19)},
    **{f"R{i:02d}": "artifact/mechanism/digest contract" for i in range(19, 28)},
    **{f"R{i:02d}": "harness identity/budget/attempt/E2E" for i in range(28, 36)},
    **{f"R{i:02d}": "side-effect/hard-zero/authority guards" for i in range(36, 41)},
}


def _runner_module():
    assert RUNNER.is_file(), "RED scope requires the harness runner seam"
    spec = importlib.util.spec_from_file_location("malak_e3_blind_assessor_harness", RUNNER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _case_set_bytes() -> bytes:
    assert CASE_SET.is_file()
    return CASE_SET.read_bytes()


def _case_set() -> dict:
    return json.loads(_case_set_bytes())


def _profile() -> dict:
    assert PROFILE.is_file()
    return json.loads(PROFILE.read_text(encoding="utf-8"))


def _write_profile(tmp_path: Path, payload: dict) -> Path:
    path = tmp_path / "experiment_profile.json"
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return path


def _canonical_json(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _expected_harness_from_profile(profile: dict) -> dict:
    budget = {
        "artifact_max_bytes": 524288,
        "expected_candidate_invocations": 13,
        "expected_input_count": 19,
        "expected_observation_count": 19,
    }
    attempt = {
        "execution_order": "CASESET_INPUT_ORDER_SEQUENTIAL",
        "max_attempts_per_input": 1,
    }
    return {
        "harness_policy_version": profile["harness_policy_version"],
        "harness_policy_digest": _sha256(_canonical_json(profile)),
        "budget_manifest_digest": _sha256(_canonical_json(budget)),
        "attempt_policy_digest": _sha256(_canonical_json(attempt)),
    }


class SpyAssessor:
    def __init__(self, *, raises: bool = False, mutate: bool = False) -> None:
        self.calls: list[dict] = []
        self.raises = raises
        self.mutate = mutate

    def __call__(self, material: dict) -> dict:
        self.calls.append(copy.deepcopy(material))
        if self.mutate:
            material.clear()
            material["candidate_mutation"] = True
        if self.raises:
            raise RuntimeError("controlled assessor failure")
        return {
            "outcome": "INCONCLUSIVE",
            "reason_codes": ["ASSESSMENT_SCOPE_EXCEEDED"],
        }


def _run(assessor: SpyAssessor | None = None) -> tuple[dict, SpyAssessor]:
    spy = assessor or SpyAssessor()
    artifact = _runner_module().run_governed_blind_assessor_experiment_v0(
        case_set_path=CASE_SET,
        profile_path=PROFILE,
        assessor=spy,
    )
    return artifact, spy


def _observations(artifact: dict) -> dict[str, dict]:
    return {
        observation["input_id"]: observation
        for case in artifact["case_results"]
        for observation in case["observations"]
    }


def test_red_requirement_matrix_has_no_silent_omissions() -> None:
    assert set(REQUIREMENT_COVERAGE) == {f"R{i:02d}" for i in range(1, 41)}


def test_red_profile_instance_is_exact_and_contains_no_ground_truth() -> None:
    profile = _profile()
    case_set = _case_set()
    assert set(profile) == PROFILE_KEYS
    assert profile["schema_version"] == PROFILE_SCHEMA
    assert profile["harness_policy_version"] == HARNESS_POLICY_VERSION
    assert profile["expected_case_set_schema_version"] == CASE_SET_SCHEMA
    assert profile["expected_case_set_digest"] == _sha256(_case_set_bytes())
    assert profile["execution_order"] == "CASESET_INPUT_ORDER_SEQUENTIAL"
    assert profile["max_attempts_per_input"] == 1
    assert profile["expected_input_count"] == 19
    assert profile["expected_observation_count"] == 19
    assert profile["expected_candidate_invocations"] == 13
    assert profile["artifact_max_bytes"] == 524288
    assert profile["candidate_argument_policy"] == "EXISTING_SUPPORT_ASSESSMENT_MATERIAL_ONLY"
    assert set(profile["expected_mechanism"]) == MECHANISM_KEYS
    assert profile["expected_mechanism"]["mechanism_kind"] == "DETERMINISTIC"
    assert profile["expected_mechanism"]["model_provenance"] is None

    input_ids = [item["input_id"] for case in case_set["cases"] for item in case["inputs"]]
    assert input_ids == EXPECTED_INPUT_IDS
    assert [item["input_id"] for item in profile["fault_modes"]] == EXPECTED_INPUT_IDS
    assert len(profile["fault_modes"]) == 19
    mode_by_id = {item["input_id"]: item["mode"] for item in profile["fault_modes"]}
    assert mode_by_id["C14.I01"] == "FORCE_UNAVAILABLE"
    assert mode_by_id["C15.I01"] == "FORCE_MALFORMED_OUTPUT"
    assert all(
        mode == "NORMAL"
        for input_id, mode in mode_by_id.items()
        if input_id not in {"C14.I01", "C15.I01"}
    )

    encoded = json.dumps(profile, ensure_ascii=False)
    for forbidden in (
        "expected_outcome",
        "expected_reason_codes",
        "critical_properties",
        "qualification_thresholds",
    ):
        assert forbidden not in encoded


def test_red_runner_public_seams_are_frozen_without_green_behavior() -> None:
    module = _runner_module()
    assert tuple(inspect.signature(module.load_experiment_profile_v0).parameters) == ("path",)
    assert tuple(inspect.signature(module.build_expected_harness_v0).parameters) == ("profile",)
    assert tuple(inspect.signature(module.verify_expected_experiment_binding_v0).parameters) == (
        "profile",
        "artifact",
    )
    assert tuple(inspect.signature(module.run_governed_blind_assessor_experiment_v0).parameters) == (
        "case_set_path",
        "profile_path",
        "assessor",
    )


def test_red_exact_profile_must_load_strictly() -> None:
    loaded = _runner_module().load_experiment_profile_v0(PROFILE)
    assert loaded == _profile()


@pytest.mark.parametrize(
    "mutation",
    [
        "unknown_schema",
        "missing_key",
        "extra_key",
        "bool_as_integer",
        "wrong_count",
        "fault_missing",
        "fault_duplicate",
        "fault_reordered",
        "fault_shifted",
    ],
)
def test_red_profile_drift_fails_closed(tmp_path: Path, mutation: str) -> None:
    profile = copy.deepcopy(_profile())
    if mutation == "unknown_schema":
        profile["schema_version"] = "future/v9"
    elif mutation == "missing_key":
        del profile["artifact_max_bytes"]
    elif mutation == "extra_key":
        profile["unexpected"] = True
    elif mutation == "bool_as_integer":
        profile["max_attempts_per_input"] = True
    elif mutation == "wrong_count":
        profile["expected_candidate_invocations"] = 12
    elif mutation == "fault_missing":
        profile["fault_modes"].pop()
    elif mutation == "fault_duplicate":
        profile["fault_modes"][1]["input_id"] = profile["fault_modes"][0]["input_id"]
    elif mutation == "fault_reordered":
        profile["fault_modes"][0], profile["fault_modes"][1] = (
            profile["fault_modes"][1],
            profile["fault_modes"][0],
        )
    else:
        profile["fault_modes"][0]["mode"] = "FORCE_UNAVAILABLE"

    module = _runner_module()
    with pytest.raises(module.ExperimentProfileError):
        module.load_experiment_profile_v0(_write_profile(tmp_path, profile))


def test_red_expected_harness_is_exact_four_field_object() -> None:
    module = _runner_module()
    profile = module.load_experiment_profile_v0(PROFILE)
    expected = module.build_expected_harness_v0(profile)
    assert expected == _expected_harness_from_profile(profile)
    assert set(expected) == HARNESS_KEYS


def test_red_binding_rejects_wrong_harness_version_even_with_correct_hashes() -> None:
    module = _runner_module()
    profile = _profile()
    artifact = {
        "assessor_mechanism": copy.deepcopy(profile["expected_mechanism"]),
        "harness": _expected_harness_from_profile(profile),
    }
    artifact["harness"]["harness_policy_version"] = (
        "e3-governed-blind-assessor-experiment-harness/v-other"
    )
    with pytest.raises(module.ExperimentBindingError):
        module.verify_expected_experiment_binding_v0(profile=profile, artifact=artifact)


def test_red_binding_accepts_only_exact_expected_harness_and_mechanism() -> None:
    module = _runner_module()
    profile = _profile()
    artifact = {
        "assessor_mechanism": copy.deepcopy(profile["expected_mechanism"]),
        "harness": _expected_harness_from_profile(profile),
    }
    assert module.verify_expected_experiment_binding_v0(profile=profile, artifact=artifact) is None


def test_red_full_corpus_produces_exact_counts_and_result_schema() -> None:
    artifact, spy = _run()
    assert artifact["schema_version"] == RESULTS_SCHEMA
    assert artifact["case_set_digest"] == _sha256(_case_set_bytes())
    assert artifact["assessor_mechanism"] == _profile()["expected_mechanism"]
    assert artifact["harness"] == _expected_harness_from_profile(_profile())
    assert len(artifact["case_results"]) == 18
    observations = _observations(artifact)
    assert list(observations) == EXPECTED_INPUT_IDS
    assert len(observations) == 19
    assert len(spy.calls) == 13


def test_red_candidate_api_exposes_no_hidden_or_lookup_fields() -> None:
    _, spy = _run()
    assert len(spy.calls) == 13
    for material in spy.calls:
        assert FORBIDDEN_CANDIDATE_KEYS.isdisjoint(material)


def test_red_structural_and_fault_inputs_make_zero_real_candidate_calls() -> None:
    artifact, spy = _run()
    observations = _observations(artifact)
    assert len(spy.calls) == 13
    assert STRUCTURAL_ZERO_CALL | FAULT_ZERO_CALL <= observations.keys()
    assert observations["C14.I01"]["outcome"] == "INCONCLUSIVE"
    assert observations["C14.I01"]["reason_codes"] == ["ASSESSOR_UNAVAILABLE"]
    assert observations["C15.I01"]["outcome"] == "INCONCLUSIVE"
    assert observations["C15.I01"]["reason_codes"] == ["ASSESSOR_OUTPUT_INVALID"]


def test_red_candidate_exception_is_one_call_no_retry_and_nonpositive() -> None:
    artifact, spy = _run(SpyAssessor(raises=True))
    assert len(spy.calls) == 13
    observations = _observations(artifact)
    eligible = set(EXPECTED_INPUT_IDS) - STRUCTURAL_ZERO_CALL - FAULT_ZERO_CALL
    for input_id in eligible:
        assert observations[input_id]["outcome"] != "SUPPORTED"


def test_red_candidate_mutation_cannot_modify_trusted_corpus() -> None:
    before = _case_set_bytes()
    _run(SpyAssessor(mutate=True))
    assert _case_set_bytes() == before


def test_red_c13_preserves_instance_identity_but_semantic_equivalence() -> None:
    artifact, _ = _run()
    observations = _observations(artifact)
    first = observations["C13.I01"]
    second = observations["C13.I02"]
    assert first["input_instance_digest"] != second["input_instance_digest"]
    assert first["semantic_input_digest"] == second["semantic_input_digest"]


def test_red_artifact_size_is_bounded_and_no_subset_is_certified() -> None:
    artifact, _ = _run()
    encoded = json.dumps(
        artifact,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    assert len(encoded) <= _profile()["artifact_max_bytes"]
    assert len(_observations(artifact)) == 19


def test_red_hard_zero_and_authority_guards_remain_explicit() -> None:
    module = _runner_module()
    assert module.NETWORK_AUTHORIZED is False
    assert module.REPO_WRITES_AUTHORIZED is False
    assert module.SUPPORT_SUFFICIENT_WIRING_AUTHORIZED is False
    assert module.MODEL_PROVIDER_EXECUTION_AUTHORIZED is False
    assert module.RDD_STAGE_2_AUTHORIZED is False
    assert module.AUTHORITY_EFFECT == "none"
