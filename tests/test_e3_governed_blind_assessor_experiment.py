from __future__ import annotations

import copy
import hashlib
import importlib.util
import inspect
import json
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
CASE_SET = ROOT / "evaluations" / "e3_governed_evidence_support_assessor_v0" / "cases.json"
PROFILE = ROOT / "evaluations" / "e3_governed_evidence_support_assessor_v0" / "experiment_profile.json"
RUNNER = ROOT / "scripts" / "run_e3_governed_blind_assessor_experiment.py"
GITATTRIBUTES = ROOT / ".gitattributes"
QUALIFICATION_RUNNER = ROOT / "scripts" / "evaluate_e3_governed_evidence_support_assessor.py"
EXPECTED_CASE_SET_DIGEST = "ef4253478ae27d86121318356c2031ae64f8855e687153b3cff673e3ae8ccb10"
EXACT_GITATTRIBUTES_RULE = (
    "/evaluations/e3_governed_evidence_support_assessor_v0/cases.json text eol=lf"
)

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
    **{f"R{i:02d}": "cross-platform raw-byte identity amendment" for i in range(41, 46)},
}

REQUIREMENT_COVERAGE.update(
    {
        "R16": "test_correction_omitted_eligible_invocation_fails_closed",
        "R18": "test_correction_runner_rejects_consumer_invalid_reason_codes",
        "R19": "test_correction_runner_rejects_consumer_invalid_reason_codes",
        "R25": "test_correction_runner_rejects_consumer_invalid_reason_codes",
        "R26": "test_correction_binding_rejects_valid_but_different_mechanism",
        "R28": "test_correction_binding_rejects_other_valid_harness_digest",
        "R29": "test_correction_binding_rejects_other_valid_harness_digest",
        "R30": "test_correction_binding_rejects_other_valid_harness_digest",
        "R35": "test_correction_binding_rejects_stale_artifact_after_valid_profile_change",
    }
)


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


def _candidate_material_from_input(input_record: dict) -> dict:
    subject = input_record["subject"]
    repository_by_ref = {
        item["ref"]: item for item in input_record["repository_evidence"]
    }
    knowledge_by_ref = {
        item["ref"]: item for item in input_record["knowledge_evidence"]
    }
    return {
        "relation_id": subject["relation_id"],
        "classification": subject["classification"],
        "statement": subject["statement"],
        "rationale": subject["rationale"],
        "supporting_repository_evidence": tuple(
            repository_by_ref[ref]
            for ref in subject["supporting_repository_refs"]
        ),
        "supporting_knowledge_evidence": tuple(
            knowledge_by_ref[ref]
            for ref in subject["supporting_knowledge_refs"]
        ),
        "limiting_or_counterevidence": tuple(
            repository_by_ref.get(ref, knowledge_by_ref.get(ref))
            for ref in subject["limiting_or_counterevidence_refs"]
        ),
        "uncertainty_basis": subject["uncertainty_basis"],
    }


def _material_key(material: dict) -> bytes:
    return _canonical_json(material)


def _qualification_oracle():
    structural_or_fault = {
        "C10.I01",
        "C11.I01",
        "C12.I01",
        "C14.I01",
        "C15.I01",
        "C17.I01",
    }
    expected: dict[bytes, dict] = {}
    for case in _case_set()["cases"]:
        for input_record in case["inputs"]:
            if input_record["input_id"] in structural_or_fault:
                continue
            key = _material_key(_candidate_material_from_input(input_record))
            assert key not in expected
            expected[key] = {
                "outcome": input_record["expected_outcome"],
                "reason_codes": list(input_record["expected_reason_codes"]),
            }
    assert len(expected) == 13

    calls: list[dict] = []

    def assessor(material: dict) -> dict:
        calls.append(copy.deepcopy(material))
        key = _material_key(material)
        assert key in expected
        return copy.deepcopy(expected[key])

    return assessor, calls


def _qualification_pack(artifact: dict, tmp_path: Path) -> subprocess.CompletedProcess[str]:
    artifact_path = tmp_path / "assessor-results.json"
    artifact_path.write_text(
        json.dumps(
            artifact,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ) + "\n",
        encoding="utf-8",
    )
    return subprocess.run(
        [
            sys.executable,
            str(QUALIFICATION_RUNNER),
            "--case-set",
            str(CASE_SET),
            "--assessor-results",
            str(artifact_path),
            "--ground-truth-reviewer-id",
            "independent-ground-truth-reviewer",
            "--runner-implementation-actor-id",
            "green-e2e-runner",
            "--reviewed-case-set-digest",
            EXPECTED_CASE_SET_DIGEST,
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def test_red_requirement_matrix_has_no_silent_omissions() -> None:
    assert set(REQUIREMENT_COVERAGE) == {f"R{i:02d}" for i in range(1, 46)}


def test_correction_requirement_matrix_points_to_causal_assertions() -> None:
    for requirement in ("R16", "R18", "R19", "R25", "R26", "R28", "R29", "R30", "R35"):
        assert REQUIREMENT_COVERAGE[requirement].startswith("test_correction_")


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


@pytest.mark.parametrize(
    "field",
    [
        "harness_policy_digest",
        "budget_manifest_digest",
        "attempt_policy_digest",
    ],
)
def test_correction_binding_rejects_other_valid_harness_digest(field: str) -> None:
    module = _runner_module()
    profile = _profile()
    artifact = {
        "assessor_mechanism": copy.deepcopy(profile["expected_mechanism"]),
        "harness": _expected_harness_from_profile(profile),
    }
    artifact["harness"][field] = "0" * 64
    assert artifact["harness"][field] != _expected_harness_from_profile(profile)[field]
    with pytest.raises(module.ExperimentBindingError, match="harness_binding_mismatch"):
        module.verify_expected_experiment_binding_v0(profile=profile, artifact=artifact)


@pytest.mark.parametrize(
    ("field", "replacement"),
    [
        ("mechanism_id", "e3-blind-assessor-deterministic-test-other"),
        ("config_digest", "1" * 64),
    ],
)
def test_correction_binding_rejects_valid_but_different_mechanism(
    field: str,
    replacement: str,
) -> None:
    module = _runner_module()
    profile = _profile()
    artifact = {
        "assessor_mechanism": copy.deepcopy(profile["expected_mechanism"]),
        "harness": _expected_harness_from_profile(profile),
    }
    artifact["assessor_mechanism"][field] = replacement
    with pytest.raises(module.ExperimentBindingError, match="assessor_mechanism_mismatch"):
        module.verify_expected_experiment_binding_v0(profile=profile, artifact=artifact)


def test_correction_binding_rejects_stale_artifact_after_valid_profile_change() -> None:
    module = _runner_module()
    profile = _profile()
    artifact = {
        "assessor_mechanism": copy.deepcopy(profile["expected_mechanism"]),
        "harness": _expected_harness_from_profile(profile),
    }
    changed_profile = copy.deepcopy(profile)
    changed_profile["expected_case_set_digest"] = "1" * 64
    assert module.load_experiment_profile_v0(PROFILE) == profile
    with pytest.raises(module.ExperimentBindingError, match="harness_binding_mismatch"):
        module.verify_expected_experiment_binding_v0(
            profile=changed_profile,
            artifact=artifact,
        )


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


@pytest.mark.parametrize(
    "reason_codes",
    [
        ["ASSESSMENT_SCOPE_EXCEEDED", "ASSESSMENT_SCOPE_EXCEEDED"],
        ["ASSESSMENT_SCOPE_EXCEEDED"] * 11,
    ],
)
def test_correction_runner_rejects_consumer_invalid_reason_codes(
    reason_codes: list[str],
) -> None:
    calls: list[dict] = []

    def assessor(material: dict) -> dict:
        calls.append(copy.deepcopy(material))
        return {
            "outcome": "INCONCLUSIVE",
            "reason_codes": list(reason_codes),
        }

    module = _runner_module()
    with pytest.raises(
        module.ExperimentBindingError,
        match="observation_reason_(duplicate|count_invalid)",
    ):
        module.run_governed_blind_assessor_experiment_v0(
            case_set_path=CASE_SET,
            profile_path=PROFILE,
            assessor=assessor,
        )
    assert len(calls) == 1


def test_correction_omitted_eligible_invocation_fails_closed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _runner_module()
    original_assessment = module._assessment
    omitted = False

    def omit_once(**kwargs):
        nonlocal omitted
        if (
            not omitted
            and kwargs["assessor"] is not None
            and kwargs["force_binding_mismatch"] is False
        ):
            omitted = True
            altered = dict(kwargs)
            altered["assessor"] = None
            return original_assessment(**altered)
        return original_assessment(**kwargs)

    monkeypatch.setattr(module, "_assessment", omit_once)
    spy = SpyAssessor()
    with pytest.raises(
        module.ExperimentBindingError,
        match="candidate_invocation_count_mismatch",
    ):
        module.run_governed_blind_assessor_experiment_v0(
            case_set_path=CASE_SET,
            profile_path=PROFILE,
            assessor=spy,
        )
    assert omitted is True
    assert len(spy.calls) == 12


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


def test_red_r41_gitattributes_rule_is_exact_and_path_scoped() -> None:
    assert GITATTRIBUTES.is_file()
    assert GITATTRIBUTES.read_text(encoding="utf-8") == EXACT_GITATTRIBUTES_RULE + "\n"


def test_red_r42_r43_case_set_raw_bytes_are_lf_and_match_frozen_digest() -> None:
    raw = _case_set_bytes()
    assert b"\r" not in raw
    assert _sha256(raw) == EXPECTED_CASE_SET_DIGEST
    assert _profile()["expected_case_set_digest"] == EXPECTED_CASE_SET_DIGEST


def test_red_r44_crlf_variant_is_not_normalized_by_harness(tmp_path: Path) -> None:
    raw = _case_set_bytes()
    assert b"\r" not in raw
    crlf_path = tmp_path / "cases-crlf.json"
    crlf_path.write_bytes(raw.replace(b"\n", b"\r\n"))
    spy = SpyAssessor()
    module = _runner_module()
    with pytest.raises(ValueError):
        module.run_governed_blind_assessor_experiment_v0(
            case_set_path=crlf_path,
            profile_path=PROFILE,
            assessor=spy,
        )
    assert spy.calls == []


def test_red_r45_qualification_pack_retains_raw_byte_digest_contract() -> None:
    source = QUALIFICATION_RUNNER.read_text(encoding="utf-8")
    assert "raw = path.read_bytes()" in source
    assert "return payload, raw" in source
    assert "case_digest = _sha256_bytes(case_bytes)" in source
    assert 'payload["case_set_digest"] != case_set_digest' in source


def test_green_e2e_generated_artifact_passes_existing_qualification_pack(
    tmp_path: Path,
) -> None:
    assessor, calls = _qualification_oracle()
    module = _runner_module()
    artifact = module.run_governed_blind_assessor_experiment_v0(
        case_set_path=CASE_SET,
        profile_path=PROFILE,
        assessor=assessor,
    )
    assert len(calls) == 13
    assert module.verify_expected_experiment_binding_v0(
        profile=_profile(),
        artifact=artifact,
    ) is None

    completed = _qualification_pack(artifact, tmp_path)
    assert completed.returncode == 0, completed.stderr or completed.stdout
    output = json.loads(completed.stdout)
    assert output["qualification_result"] == "PASS"
    assert output["qualification_reasons"] == []
    assert output["case_count"] == 18
    assert output["input_count"] == 19
    assert output["case_set_digest"] == EXPECTED_CASE_SET_DIGEST
    assert output["authority_effect"] == "none"


def test_green_e2e_consumer_contract_mutation_is_rejected_by_qualification_pack(
    tmp_path: Path,
) -> None:
    assessor, _calls = _qualification_oracle()
    artifact = _runner_module().run_governed_blind_assessor_experiment_v0(
        case_set_path=CASE_SET,
        profile_path=PROFILE,
        assessor=assessor,
    )
    artifact["case_set_digest"] = "0" * 64

    completed = _qualification_pack(artifact, tmp_path)
    assert completed.returncode == 2
    output = json.loads(completed.stdout)
    assert output["qualification_result"] == "INCONCLUSIVE"
    assert output["qualification_reasons"] == [
        "assessor_results_case_set_digest"
    ]
    assert output["authority_effect"] == "none"


def test_red_hard_zero_and_authority_guards_remain_explicit() -> None:
    module = _runner_module()
    assert module.NETWORK_AUTHORIZED is False
    assert module.REPO_WRITES_AUTHORIZED is False
    assert module.SUPPORT_SUFFICIENT_WIRING_AUTHORIZED is False
    assert module.MODEL_PROVIDER_EXECUTION_AUTHORIZED is False
    assert module.RDD_STAGE_2_AUTHORIZED is False
    assert module.AUTHORITY_EFFECT == "none"


LEGACY_GROUND_TRUTH_DIGEST_PR262 = (
    "23e045b5e5aede8341323c486e77893d7161899f0c20870703efff28789f3f83"
)


def _repair_case(case_id: str) -> dict:
    cases = {case["case_id"]: case for case in _case_set()["cases"]}
    return cases[case_id]


def _repair_input(case_id: str, input_id: str | None = None) -> dict:
    case = _repair_case(case_id)
    if input_id is None:
        assert len(case["inputs"]) == 1
        return case["inputs"][0]
    return next(item for item in case["inputs"] if item["input_id"] == input_id)


def _repair_materials(input_record: dict) -> list[str]:
    return [
        item["material"]
        for item in (
            list(input_record["repository_evidence"])
            + list(input_record["knowledge_evidence"])
        )
    ]


def test_ground_truth_repair_red_gtr_r01_legacy_oracle_bytes_are_rejected() -> None:
    assert _sha256(_case_set_bytes()) != LEGACY_GROUND_TRUTH_DIGEST_PR262


def test_ground_truth_repair_red_gtr_r26_c01_material_support_is_explicit() -> None:
    item = _repair_input("C01")
    assert item["subject"]["statement"] == (
        "Kernel coordinates orchestration between Planner and registered Capabilities."
    )
    material = " ".join(_repair_materials(item))
    assert "Kernel coordinates orchestration between Planner and registered Capabilities" in material
    assert "does not establish durable persistence authority" in material


def test_ground_truth_repair_red_gtr_r03_r04_irrelevant_and_insufficient_are_materialized() -> None:
    c02 = _repair_input("C02")
    c02_material = " ".join(_repair_materials(c02))
    assert "Formatting note:" in c02_material
    assert "Naming guideline:" in c02_material
    assert "orchestration" not in c02_material.lower()

    c03 = _repair_input("C03")
    assert "complete execution lifecycle" in c03["subject"]["statement"]
    c03_material = " ".join(_repair_materials(c03))
    assert "dispatches planned Capabilities" in c03_material
    assert "does not establish ownership of the complete execution lifecycle" in c03_material


def test_ground_truth_repair_red_gtr_r05_r06_r08_r09_limits_conflict_authority_and_context_are_visible() -> None:
    c05 = _repair_input("C05")
    assert any(
        "does not grant durable persistence authority" in material
        for material in _repair_materials(c05)
    )

    c06 = _repair_input("C06")
    assert any(
        "Kernel does not coordinate Capability execution" in material
        for material in _repair_materials(c06)
    )

    c07 = _repair_input("C07")
    c07_material = " ".join(_repair_materials(c07))
    assert "Authoritative naming rule:" in c07_material
    assert "Governance formatting rule:" in c07_material
    assert "orchestration" not in c07_material.lower()

    c08 = _repair_input("C08")
    c08_material = " ".join(_repair_materials(c08))
    assert "Contextual developer note (non-normative):" in c08_material
    assert "Kernel -> Planner -> CapabilityRegistry -> Capability" in c08_material


def test_ground_truth_repair_red_gtr_r10_r18_r20_overclaim_confidence_and_scope_are_concrete() -> None:
    c09 = _repair_input("C09")
    assert "durable persistence authority" in c09["subject"]["statement"]
    assert "therefore Kernel owns durable persistence authority" in c09["subject"]["rationale"]\n    assert "overclaim" not in c09["subject"]["rationale"].lower()
    assert any(
        "does not establish durable persistence authority" in material
        for material in _repair_materials(c09)
    )

    c16 = _repair_input("C16")
    assert "Evaluator confidence 0.99" in c16["subject"]["rationale"]
    assert "durable persistence authorization" in c16["subject"]["statement"]
    assert all(
        "durable persistence authorization" not in material
        for material in _repair_materials(c16)
    )

    c18 = _repair_input("C18")
    c18_material = " ".join(_repair_materials(c18))
    assert "production deployment logs are outside this packet" in c18_material
    assert "cannot be verified from this bounded packet" in c18_material


def test_ground_truth_repair_red_gtr_r12_r13_binding_priors_are_material_and_recomputable() -> None:
    module = _runner_module()

    c11 = _repair_input("C11")
    prior_subject = c11["binding_prior"]["prior_subject"]
    assert prior_subject["statement"] != c11["subject"]["statement"]
    assert "Planner owns orchestration" in c11["subject"]["statement"]
    assert "Kernel coordinates orchestration" in prior_subject["statement"]
    assert (
        module._subject_fingerprint(prior_subject)
        == c11["binding_expectation"]["expected_subject_fingerprint"]
    )

    c12 = _repair_input("C12")
    prior_repository = c12["binding_prior"]["prior_repository_evidence"]
    prior_knowledge = c12["binding_prior"]["prior_knowledge_evidence"]
    assert any("Kernel coordinates orchestration" in item["material"] for item in prior_repository)
    assert any("Planner coordinates orchestration directly" in item["material"] for item in c12["repository_evidence"])
    assert (
        module._evidence_material_digest(prior_repository, prior_knowledge)
        == c12["binding_expectation"]["expected_evidence_material_digest"]
    )
    assert module._evidence_material_digest(
        c12["repository_evidence"],
        c12["knowledge_evidence"],
    ) != c12["binding_expectation"]["expected_evidence_material_digest"]


def test_ground_truth_repair_red_gtr_r14_r15_c13_equivalence_also_has_material_support() -> None:
    first = _repair_input("C13", "C13.I01")
    second = _repair_input("C13", "C13.I02")
    for item in (first, second):
        material = " ".join(_repair_materials(item))
        assert item["subject"]["statement"] == (
            "Kernel coordinates orchestration between Planner and registered Capabilities."
        )
        assert "Kernel coordinates orchestration between Planner and registered Capabilities" in material
        assert "Repository execution path:" in material
        assert "Architecture summary:" in material

    module = _runner_module()
    assert module._input_instance_digest(first) != module._input_instance_digest(second)
    assert module._semantic_input_digest(first) == module._semantic_input_digest(second)


def test_ground_truth_repair_red_gtr_r19_c17_self_certification_identity_is_explicit() -> None:
    case = _repair_case("C17")
    item = _repair_input("C17")
    assert case["finding_producer_subject_id"] == "same-subject"
    assert case["assessor_subject_id"] == "same-subject"
    assert "same subject" in item["subject"]["rationale"].lower()
