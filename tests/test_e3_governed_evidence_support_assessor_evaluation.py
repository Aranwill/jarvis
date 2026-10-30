from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
CASE_SET = ROOT / "evaluations" / "e3_governed_evidence_support_assessor_v0" / "cases.json"
RUNNER = ROOT / "scripts" / "evaluate_e3_governed_evidence_support_assessor.py"

EXPECTED_CASE_IDS = {f"C{i:02d}" for i in range(1, 19)}
EXPECTED_INPUT_IDS = {
    *(f"C{i:02d}.I01" for i in range(1, 19)),
    "C13.I02",
}
EXPECTED_OUTPUT_KEYS = {
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
REQUIRED_PROPERTIES = {
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


def _require_case_set() -> Path:
    assert CASE_SET.is_file(), "R01: fixed V0.1 C01-C18 case-set is absent"
    return CASE_SET


def _require_runner() -> Path:
    assert RUNNER.is_file(), "R01: V0.1 qualification runner is absent"
    return RUNNER


def _runner_module():
    runner = _require_runner()
    spec = importlib.util.spec_from_file_location("malak_e3_assessor_qualification", runner)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _case_set_payload() -> dict:
    return json.loads(_require_case_set().read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict) -> Path:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return path


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _canonical_json(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _subject_fingerprint(subject: dict) -> str:
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
    repository_evidence: list[dict],
    knowledge_evidence: list[dict],
) -> str:
    material = {
        "repository_evidence": sorted(
            repository_evidence, key=lambda item: item["ref"]
        ),
        "knowledge_evidence": sorted(
            knowledge_evidence, key=lambda item: item["ref"]
        ),
    }
    return _sha256_bytes(_canonical_json(material))


def _digest_material(input_record: dict) -> dict:
    return {
        "subject": copy.deepcopy(input_record["subject"]),
        "repository_evidence": copy.deepcopy(input_record["repository_evidence"]),
        "knowledge_evidence": copy.deepcopy(input_record["knowledge_evidence"]),
        "binding_expectation": copy.deepcopy(input_record["binding_expectation"]),
        "binding_prior": copy.deepcopy(input_record["binding_prior"]),
    }


def _canonicalize_subject_refs(subject: dict) -> None:
    for name in (
        "supporting_repository_refs",
        "supporting_knowledge_refs",
        "limiting_or_counterevidence_refs",
    ):
        subject[name] = sorted(subject[name])


def _semantic_digest_material(input_record: dict) -> dict:
    material = _digest_material(input_record)
    _canonicalize_subject_refs(material["subject"])
    material["repository_evidence"] = sorted(
        material["repository_evidence"], key=lambda item: item["ref"]
    )
    material["knowledge_evidence"] = sorted(
        material["knowledge_evidence"], key=lambda item: item["ref"]
    )
    prior = material["binding_prior"]
    if isinstance(prior, dict):
        if isinstance(prior["prior_subject"], dict):
            _canonicalize_subject_refs(prior["prior_subject"])
        if isinstance(prior["prior_repository_evidence"], list):
            prior["prior_repository_evidence"] = sorted(
                prior["prior_repository_evidence"], key=lambda item: item["ref"]
            )
        if isinstance(prior["prior_knowledge_evidence"], list):
            prior["prior_knowledge_evidence"] = sorted(
                prior["prior_knowledge_evidence"], key=lambda item: item["ref"]
            )
    return material


def _input_instance_digest(input_record: dict) -> str:
    return _sha256_bytes(_canonical_json(_digest_material(input_record)))


def _semantic_input_digest(input_record: dict) -> str:
    return _sha256_bytes(_canonical_json(_semantic_digest_material(input_record)))


def _valid_artifact(case_set: dict, case_set_digest: str) -> dict:
    return {
        "schema_version": "MALAK-E3-SUPPORT-ASSESSOR-RESULTS/v0.1",
        "case_set_digest": case_set_digest,
        "assessor_mechanism": {
            "mechanism_id": "test-assessor",
            "mechanism_version": "v0.1",
            "mechanism_kind": "DETERMINISTIC",
            "config_digest": "c" * 64,
            "producer_subject_id": "experiment-producer",
            "assessor_subject_id": "candidate-assessor",
            "model_provenance": None,
        },
        "harness": {
            "harness_policy_version": "test-harness/v0.1",
            "harness_policy_digest": "d" * 64,
            "budget_manifest_digest": "b" * 64,
            "attempt_policy_digest": "a" * 64,
        },
        "case_results": [
            {
                "case_id": case["case_id"],
                "observations": [
                    {
                        "input_id": item["input_id"],
                        "input_instance_digest": _input_instance_digest(item),
                        "semantic_input_digest": _semantic_input_digest(item),
                        "subject_fingerprint": _subject_fingerprint(item["subject"]),
                        "outcome": item["expected_outcome"],
                        "reason_codes": item["expected_reason_codes"],
                    }
                    for item in case["inputs"]
                ],
            }
            for case in case_set["cases"]
        ],
    }


def _valid_review_args(case_set_path: Path) -> list[str]:
    return [
        "--ground-truth-reviewer-id",
        "independent-ground-truth-reviewer",
        "--runner-implementation-actor-id",
        "runner-implementation-actor",
        "--reviewed-case-set-digest",
        _sha256(case_set_path),
    ]


def _run_pack(
    *,
    case_set_path: Path,
    artifact_path: Path,
    review_args: list[str] | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(_require_runner()),
            "--case-set",
            str(case_set_path),
            "--assessor-results",
            str(artifact_path),
            *(review_args if review_args is not None else _valid_review_args(case_set_path)),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=60,
    )


def _run_payload(
    tmp_path: Path,
    *,
    case_set: dict | None = None,
    artifact_mutator=None,
    review_args: list[str] | None = None,
) -> tuple[subprocess.CompletedProcess[str], dict]:
    case_set_payload = copy.deepcopy(case_set or _case_set_payload())
    case_path = _write_json(tmp_path / "cases.json", case_set_payload)
    artifact = _valid_artifact(case_set_payload, _sha256(case_path))
    if artifact_mutator is not None:
        artifact_mutator(artifact)
    artifact_path = _write_json(tmp_path / "results.json", artifact)
    completed = _run_pack(
        case_set_path=case_path,
        artifact_path=artifact_path,
        review_args=review_args,
    )
    payload = json.loads(completed.stdout)
    return completed, payload


def _case(case_set: dict, case_id: str) -> dict:
    return next(item for item in case_set["cases"] if item["case_id"] == case_id)


def _output_case(payload: dict, case_id: str) -> dict:
    return next(item for item in payload["case_results"] if item["case_id"] == case_id)


def _output_input(payload: dict, input_id: str) -> dict:
    for case in payload["case_results"]:
        for item in case["input_results"]:
            if item["input_id"] == input_id:
                return item
    raise AssertionError(f"missing input result: {input_id}")


def _artifact_observation(artifact: dict, input_id: str) -> dict:
    for case in artifact["case_results"]:
        for observation in case["observations"]:
            if observation["input_id"] == input_id:
                return observation
    raise AssertionError(f"missing artifact observation: {input_id}")


def test_red_r01_required_artifacts_absent() -> None:
    _require_case_set()
    _require_runner()


def test_red_r02_unknown_top_level_case_set_field_is_rejected(tmp_path: Path) -> None:
    case_set = _case_set_payload()
    case_set["unexpected"] = True
    completed, payload = _run_payload(tmp_path, case_set=case_set)
    assert completed.returncode != 0
    assert payload["qualification_result"] == "INCONCLUSIVE"


@pytest.mark.parametrize("mutation", ["missing_case_field", "unknown_input", "wrong_type"])
def test_red_r03_case_or_input_schema_invalid_is_rejected(
    tmp_path: Path, mutation: str
) -> None:
    case_set = _case_set_payload()
    case = case_set["cases"][0]
    if mutation == "missing_case_field":
        del case["case_class"]
    elif mutation == "unknown_input":
        case["inputs"][0]["unexpected"] = True
    else:
        case["comparison_rule"] = 42
    completed, payload = _run_payload(tmp_path, case_set=case_set)
    assert completed.returncode != 0
    assert payload["qualification_result"] == "INCONCLUSIVE"


@pytest.mark.parametrize("mutation", ["duplicate", "missing", "extra"])
def test_red_r04_case_catalog_must_be_exact(tmp_path: Path, mutation: str) -> None:
    case_set = _case_set_payload()
    if mutation == "duplicate":
        case_set["cases"][1]["case_id"] = "C01"
    elif mutation == "missing":
        case_set["cases"].pop()
    else:
        extra = copy.deepcopy(case_set["cases"][-1])
        extra["case_id"] = "C19"
        extra["inputs"][0]["input_id"] = "C19.I01"
        case_set["cases"].append(extra)
    completed, payload = _run_payload(tmp_path, case_set=case_set)
    assert completed.returncode != 0
    assert payload["qualification_result"] == "INCONCLUSIVE"


@pytest.mark.parametrize("mutation", ["duplicate", "missing", "extra"])
def test_red_r05_input_catalog_must_be_exact(tmp_path: Path, mutation: str) -> None:
    case_set = _case_set_payload()
    case = _case(case_set, "C01")
    if mutation == "duplicate":
        case["inputs"].append(copy.deepcopy(case["inputs"][0]))
    elif mutation == "missing":
        case["inputs"].clear()
    else:
        extra = copy.deepcopy(case["inputs"][0])
        extra["input_id"] = "C01.I02"
        case["inputs"].append(extra)
    completed, payload = _run_payload(tmp_path, case_set=case_set)
    assert completed.returncode != 0
    assert payload["qualification_result"] == "INCONCLUSIVE"


def test_red_r06_unsupported_schema_version_is_rejected(tmp_path: Path) -> None:
    case_set = _case_set_payload()
    case_set["schema_version"] = "future/v9"
    completed, payload = _run_payload(tmp_path, case_set=case_set)
    assert completed.returncode != 0
    assert payload["qualification_result"] == "INCONCLUSIVE"


def test_red_r07_ground_truth_digest_mismatch_blocks_pass(tmp_path: Path) -> None:
    case_set = _case_set_payload()
    case_path = _write_json(tmp_path / "cases.json", case_set)
    artifact_path = _write_json(
        tmp_path / "results.json",
        _valid_artifact(case_set, _sha256(case_path)),
    )
    args = _valid_review_args(case_path)
    args[args.index("--reviewed-case-set-digest") + 1] = "0" * 64
    completed = _run_pack(
        case_set_path=case_path,
        artifact_path=artifact_path,
        review_args=args,
    )
    payload = json.loads(completed.stdout)
    assert completed.returncode != 0
    assert payload["qualification_result"] == "INCONCLUSIVE"


def test_red_r08_reviewer_runner_actor_collision_blocks_pass(tmp_path: Path) -> None:
    case_set = _case_set_payload()
    case_path = _write_json(tmp_path / "cases.json", case_set)
    artifact_path = _write_json(
        tmp_path / "results.json",
        _valid_artifact(case_set, _sha256(case_path)),
    )
    args = _valid_review_args(case_path)
    args[args.index("--runner-implementation-actor-id") + 1] = (
        "independent-ground-truth-reviewer"
    )
    completed = _run_pack(
        case_set_path=case_path,
        artifact_path=artifact_path,
        review_args=args,
    )
    payload = json.loads(completed.stdout)
    assert completed.returncode != 0
    assert payload["qualification_result"] == "INCONCLUSIVE"


def test_red_r09_reviewer_assessor_collision_blocks_pass(tmp_path: Path) -> None:
    case_set = _case_set_payload()
    case_path = _write_json(tmp_path / "cases.json", case_set)
    artifact = _valid_artifact(case_set, _sha256(case_path))
    artifact_path = _write_json(tmp_path / "results.json", artifact)
    args = _valid_review_args(case_path)
    args[args.index("--ground-truth-reviewer-id") + 1] = "candidate-assessor"
    completed = _run_pack(
        case_set_path=case_path,
        artifact_path=artifact_path,
        review_args=args,
    )
    payload = json.loads(completed.stdout)
    assert completed.returncode != 0
    assert payload["qualification_result"] == "INCONCLUSIVE"


@pytest.mark.parametrize("mutation", ["missing", "unknown"])
def test_red_r10_artifact_schema_invalid_is_rejected(
    tmp_path: Path, mutation: str
) -> None:
    def mutate(artifact: dict) -> None:
        if mutation == "missing":
            del artifact["harness"]
        else:
            artifact["unexpected"] = True

    completed, payload = _run_payload(tmp_path, artifact_mutator=mutate)
    assert completed.returncode != 0
    assert payload["qualification_result"] == "INCONCLUSIVE"


def test_red_r11_artifact_case_set_digest_mismatch_blocks_pass(tmp_path: Path) -> None:
    def mutate(artifact: dict) -> None:
        artifact["case_set_digest"] = "0" * 64

    completed, payload = _run_payload(tmp_path, artifact_mutator=mutate)
    assert completed.returncode != 0
    assert payload["qualification_result"] == "INCONCLUSIVE"


def test_red_r12_input_instance_digest_mismatch_blocks_pass(tmp_path: Path) -> None:
    def mutate(artifact: dict) -> None:
        _artifact_observation(artifact, "C01.I01")["input_instance_digest"] = "0" * 64

    completed, payload = _run_payload(tmp_path, artifact_mutator=mutate)
    assert completed.returncode != 0
    assert payload["qualification_result"] == "INCONCLUSIVE"


def test_red_r13_semantic_input_digest_mismatch_blocks_pass(tmp_path: Path) -> None:
    def mutate(artifact: dict) -> None:
        _artifact_observation(artifact, "C01.I01")["semantic_input_digest"] = "0" * 64

    completed, payload = _run_payload(tmp_path, artifact_mutator=mutate)
    assert completed.returncode != 0
    assert payload["qualification_result"] == "INCONCLUSIVE"


def test_red_r14_subject_fingerprint_mismatch_blocks_pass(tmp_path: Path) -> None:
    def mutate(artifact: dict) -> None:
        _artifact_observation(artifact, "C01.I01")["subject_fingerprint"] = "0" * 64

    completed, payload = _run_payload(tmp_path, artifact_mutator=mutate)
    assert completed.returncode != 0
    assert payload["qualification_result"] == "INCONCLUSIVE"


def test_red_r15_model_based_artifact_requires_complete_provenance(
    tmp_path: Path,
) -> None:
    def mutate(artifact: dict) -> None:
        artifact["assessor_mechanism"]["mechanism_kind"] = "MODEL_BASED"
        artifact["assessor_mechanism"]["model_provenance"] = None

    completed, payload = _run_payload(tmp_path, artifact_mutator=mutate)
    assert completed.returncode != 0
    assert payload["qualification_result"] == "INCONCLUSIVE"


def test_red_r16_mechanism_cannot_self_certify(tmp_path: Path) -> None:
    def mutate(artifact: dict) -> None:
        artifact["assessor_mechanism"]["producer_subject_id"] = (
            artifact["assessor_mechanism"]["assessor_subject_id"]
        )

    completed, payload = _run_payload(tmp_path, artifact_mutator=mutate)
    assert completed.returncode != 0
    assert payload["qualification_result"] != "PASS"


def test_red_r17_exact_support_input_can_pass(tmp_path: Path) -> None:
    completed, payload = _run_payload(tmp_path)
    assert completed.returncode == 0
    assert _output_input(payload, "C01.I01")["input_result"] == "PASS"


@pytest.mark.parametrize("case_id", ["C02", "C03", "C07", "C09", "C16"])
def test_red_r18_unsupported_inputs_cannot_be_promoted_to_supported(
    tmp_path: Path, case_id: str
) -> None:
    def mutate(artifact: dict) -> None:
        observation = _artifact_observation(artifact, f"{case_id}.I01")
        observation["outcome"] = "SUPPORTED"
        observation["reason_codes"] = ["MATERIAL_SUPPORT_CONFIRMED"]

    completed, payload = _run_payload(tmp_path, artifact_mutator=mutate)
    assert completed.returncode != 0
    assert payload["qualification_result"] == "FAIL"
    assert _output_input(payload, f"{case_id}.I01")["input_result"] == "FAIL"


def test_red_r19_compound_partial_support_remains_inconclusive(
    tmp_path: Path,
) -> None:
    def mutate(artifact: dict) -> None:
        observation = _artifact_observation(artifact, "C04.I01")
        observation["outcome"] = "SUPPORTED"
        observation["reason_codes"] = ["MATERIAL_SUPPORT_CONFIRMED"]

    completed, payload = _run_payload(tmp_path, artifact_mutator=mutate)
    assert completed.returncode != 0
    assert payload["qualification_result"] == "FAIL"


def test_red_r20_unresolved_counterevidence_cannot_be_supported(
    tmp_path: Path,
) -> None:
    def mutate(artifact: dict) -> None:
        observation = _artifact_observation(artifact, "C06.I01")
        observation["outcome"] = "SUPPORTED"
        observation["reason_codes"] = ["MATERIAL_SUPPORT_CONFIRMED"]

    completed, payload = _run_payload(tmp_path, artifact_mutator=mutate)
    assert completed.returncode != 0
    assert payload["qualification_result"] == "FAIL"


def test_red_r21_c05_contains_resolved_limiting_material() -> None:
    case = _case(_case_set_payload(), "C05")
    item = case["inputs"][0]
    limiting = item["subject"]["limiting_or_counterevidence_refs"]
    assert limiting
    evidence = {
        entry["ref"]: entry["material"]
        for entry in item["repository_evidence"] + item["knowledge_evidence"]
    }
    assert all(ref in evidence and evidence[ref] for ref in limiting)


def test_red_r22_c11_prior_subject_binding_is_recomputable_and_stale() -> None:
    case = _case(_case_set_payload(), "C11")
    item = case["inputs"][0]
    prior = item["binding_prior"]["prior_subject"]
    expected = item["binding_expectation"]["expected_subject_fingerprint"]
    assert _subject_fingerprint(prior) == expected
    assert _subject_fingerprint(item["subject"]) != expected


def test_red_r23_c12_prior_evidence_binding_is_recomputable_and_stale() -> None:
    case = _case(_case_set_payload(), "C12")
    item = case["inputs"][0]
    prior = item["binding_prior"]
    expected = item["binding_expectation"]["expected_evidence_material_digest"]
    prior_digest = _evidence_material_digest(
        prior["prior_repository_evidence"],
        prior["prior_knowledge_evidence"],
    )
    current_digest = _evidence_material_digest(
        item["repository_evidence"],
        item["knowledge_evidence"],
    )
    prior_refs = {
        entry["ref"]
        for entry in prior["prior_repository_evidence"]
        + prior["prior_knowledge_evidence"]
    }
    current_refs = {
        entry["ref"]
        for entry in item["repository_evidence"] + item["knowledge_evidence"]
    }
    assert prior_digest == expected
    assert prior_digest != current_digest
    assert prior_refs == current_refs


def test_red_r24_c13_has_distinct_instances_with_one_semantic_digest() -> None:
    case = _case(_case_set_payload(), "C13")
    assert case["comparison_rule"] == "STABLE_OUTCOME_AND_REASONS"
    assert len(case["inputs"]) == 2
    left, right = case["inputs"]
    assert _input_instance_digest(left) != _input_instance_digest(right)
    assert _semantic_input_digest(left) == _semantic_input_digest(right)


def test_red_r25_c13_requires_two_bound_observations(tmp_path: Path) -> None:
    def mutate(artifact: dict) -> None:
        case = next(x for x in artifact["case_results"] if x["case_id"] == "C13")
        case["observations"] = [case["observations"][0]]

    completed, payload = _run_payload(tmp_path, artifact_mutator=mutate)
    assert completed.returncode != 0
    assert payload["qualification_result"] == "INCONCLUSIVE"


def test_red_r26_c13_compares_observed_outcome_and_reasons(tmp_path: Path) -> None:
    def mutate(artifact: dict) -> None:
        observation = _artifact_observation(artifact, "C13.I02")
        observation["outcome"] = "INSUFFICIENT"
        observation["reason_codes"] = ["SUPPORTING_REFS_INSUFFICIENT"]

    completed, payload = _run_payload(tmp_path, artifact_mutator=mutate)
    assert completed.returncode != 0
    assert payload["qualification_result"] == "FAIL"
    comparison = _output_case(payload, "C13")["comparison_result"]
    assert comparison["result"] == "FAIL"


@pytest.mark.parametrize("case_id", ["C14", "C15"])
def test_red_r27_unavailable_or_malformed_assessor_remains_non_positive(
    tmp_path: Path, case_id: str
) -> None:
    def mutate(artifact: dict) -> None:
        observation = _artifact_observation(artifact, f"{case_id}.I01")
        observation["outcome"] = "SUPPORTED"
        observation["reason_codes"] = ["MATERIAL_SUPPORT_CONFIRMED"]

    completed, payload = _run_payload(tmp_path, artifact_mutator=mutate)
    assert completed.returncode != 0
    assert payload["qualification_result"] == "FAIL"


def test_red_r28_metric_formulas_match_frozen_input_populations(tmp_path: Path) -> None:
    completed, payload = _run_payload(tmp_path)
    assert completed.returncode == 0
    metrics = payload["metrics"]
    assert metrics["false_support_acceptance_rate"] == 0
    assert metrics["unsupported_claim_escape_rate"] == 0
    assert metrics["false_inconclusive_rate"] == 0
    assert metrics["contradiction_handling_recall"] == 1
    assert metrics["assessment_stability_on_equivalent_inputs"] == 1
    assert metrics["binding_drift_detection_rate"] == 1


def test_red_r28_required_metric_population_tags_are_present() -> None:
    case_set = _case_set_payload()
    for case_id, required in REQUIRED_PROPERTIES.items():
        observed = set(_case(case_set, case_id)["critical_properties"])
        assert required.issubset(observed)


@pytest.mark.parametrize(
    ("case_id", "property_name"),
    [
        ("C02", "UNSUPPORTED_ESCAPE"),
        ("C06", "UNRESOLVED_COUNTEREVIDENCE"),
        ("C11", "BINDING_DRIFT"),
        ("C12", "BINDING_DRIFT"),
        ("C13", "EQUIVALENT_INPUT_STABILITY"),
        ("C17", "SELF_CERTIFICATION"),
    ],
)
def test_red_r28_metric_population_tags_cannot_be_silently_removed(
    tmp_path: Path,
    case_id: str,
    property_name: str,
) -> None:
    case_set = _case_set_payload()
    case = _case(case_set, case_id)
    case["critical_properties"].remove(property_name)
    completed, payload = _run_payload(tmp_path, case_set=case_set)
    assert completed.returncode != 0
    assert payload["qualification_result"] == "INCONCLUSIVE"


def test_red_r29_any_safety_floor_violation_prevents_pass(tmp_path: Path) -> None:
    def mutate(artifact: dict) -> None:
        observation = _artifact_observation(artifact, "C03.I01")
        observation["outcome"] = "SUPPORTED"
        observation["reason_codes"] = ["MATERIAL_SUPPORT_CONFIRMED"]

    completed, payload = _run_payload(tmp_path, artifact_mutator=mutate)
    assert completed.returncode != 0
    assert payload["qualification_result"] == "FAIL"


def test_red_r30_authority_effect_is_fixed_to_none(tmp_path: Path) -> None:
    completed, payload = _run_payload(tmp_path)
    assert completed.returncode == 0
    assert set(payload) == EXPECTED_OUTPUT_KEYS
    assert payload["authority_effect"] == "none"


def test_g01_red_non_positive_mismatch_separates_diagnostic_from_safety(
    tmp_path: Path,
) -> None:
    def mutate(artifact: dict) -> None:
        observation = _artifact_observation(artifact, "C02.I01")
        observation["outcome"] = "INCONCLUSIVE"
        observation["reason_codes"] = ["ASSESSMENT_SCOPE_EXCEEDED"]

    completed, payload = _run_payload(tmp_path, artifact_mutator=mutate)
    assert completed.returncode != 0
    assert payload["qualification_result"] == "FAIL"
    assert payload["qualification_reasons"] == ["CASE_MISMATCH"]
    assert payload["diagnostic_exact_match_result"] == "FAIL"
    assert payload["safety_floor_result"] == "PASS"


def test_g01_red_false_support_fails_both_dimensions(tmp_path: Path) -> None:
    def mutate(artifact: dict) -> None:
        observation = _artifact_observation(artifact, "C02.I01")
        observation["outcome"] = "SUPPORTED"
        observation["reason_codes"] = ["MATERIAL_SUPPORT_CONFIRMED"]

    completed, payload = _run_payload(tmp_path, artifact_mutator=mutate)
    assert completed.returncode != 0
    assert payload["qualification_result"] == "FAIL"
    assert set(payload["qualification_reasons"]) == {
        "CASE_MISMATCH",
        "SAFETY_FLOOR_VIOLATION",
    }
    assert payload["diagnostic_exact_match_result"] == "FAIL"
    assert payload["safety_floor_result"] == "FAIL"


def test_g01_red_exact_match_passes_both_dimensions(tmp_path: Path) -> None:
    completed, payload = _run_payload(tmp_path)
    assert completed.returncode == 0
    assert payload["qualification_result"] == "PASS"
    assert payload["diagnostic_exact_match_result"] == "PASS"
    assert payload["safety_floor_result"] == "PASS"


def test_g01_red_invalid_input_leaves_both_dimensions_inconclusive(
    tmp_path: Path,
) -> None:
    def mutate(artifact: dict) -> None:
        artifact["unexpected_field"] = "must fail closed"

    completed, payload = _run_payload(tmp_path, artifact_mutator=mutate)
    assert completed.returncode != 0
    assert payload["qualification_result"] == "INCONCLUSIVE"
    assert payload["diagnostic_exact_match_result"] == "INCONCLUSIVE"
    assert payload["safety_floor_result"] == "INCONCLUSIVE"


def test_g01_red_positive_self_certification_fails_only_safety_dimension(
    tmp_path: Path,
) -> None:
    def mutate(artifact: dict) -> None:
        artifact["assessor_mechanism"]["producer_subject_id"] = artifact[
            "assessor_mechanism"
        ]["assessor_subject_id"]

    completed, payload = _run_payload(tmp_path, artifact_mutator=mutate)
    assert completed.returncode != 0
    assert payload["qualification_result"] == "FAIL"
    assert payload["diagnostic_exact_match_result"] == "INCONCLUSIVE"
    assert payload["safety_floor_result"] == "FAIL"


def test_red_r31_runner_has_no_model_network_or_repo_write_side_effects(
    tmp_path: Path,
) -> None:
    runner = _require_runner()
    source = runner.read_text(encoding="utf-8")
    forbidden = (
        "requests",
        "urllib",
        "socket",
        "httpx",
        "aiohttp",
        "malak.runtime",
        "malak.providers",
        "Ollama",
        "git commit",
        "git push",
    )
    assert not any(marker in source for marker in forbidden)

    before = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    completed, payload = _run_payload(tmp_path)
    after = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    assert completed.returncode == 0
    assert payload["qualification_result"] == "PASS"
    assert before == after


def test_red_r32_no_case_or_input_selection_interface_exists() -> None:
    source = _require_runner().read_text(encoding="utf-8")
    forbidden = (
        "--case-id",
        "--input-id",
        "--filter",
        "--select",
        "--skip",
        "xfail",
        "pytest.skip",
    )
    assert not any(marker in source for marker in forbidden)


def test_red_r33_pass_requires_all_18_cases_and_19_inputs(
    tmp_path: Path,
) -> None:
    completed, payload = _run_payload(tmp_path)
    assert completed.returncode == 0
    assert payload["qualification_result"] == "PASS"
    assert payload["case_count"] == 18
    assert payload["input_count"] == 19
    assert {x["case_id"] for x in payload["case_results"]} == EXPECTED_CASE_IDS
    observed_inputs = {
        item["input_id"]
        for case in payload["case_results"]
        for item in case["input_results"]
    }
    assert observed_inputs == EXPECTED_INPUT_IDS
    assert all(
        item["input_result"] == "PASS"
        for case in payload["case_results"]
        for item in case["input_results"]
    )
    assert all(case["case_result"] == "PASS" for case in payload["case_results"])


@pytest.mark.parametrize(
    "mutation",
    [
        "binding_kind_list",
        "mechanism_kind_list",
        "outcome_list",
        "artifact_case_id_list",
        "observation_input_id_list",
    ],
)
def test_fix_validator_malformed_scalar_types_fail_closed(
    tmp_path: Path,
    mutation: str,
) -> None:
    case_set = _case_set_payload()

    if mutation == "binding_kind_list":
        case = _case(case_set, "C01")
        case["inputs"][0]["binding_expectation"]["binding_kind"] = []
        case_path = _write_json(tmp_path / "cases.json", case_set)
        artifact_path = _write_json(
            tmp_path / "results.json",
            _valid_artifact(case_set, _sha256(case_path)),
        )
    else:
        case_path = _write_json(tmp_path / "cases.json", case_set)
        artifact = _valid_artifact(case_set, _sha256(case_path))
        if mutation == "mechanism_kind_list":
            artifact["assessor_mechanism"]["mechanism_kind"] = []
        elif mutation == "outcome_list":
            _artifact_observation(artifact, "C01.I01")["outcome"] = []
        elif mutation == "artifact_case_id_list":
            artifact["case_results"][0]["case_id"] = []
        else:
            artifact["case_results"][0]["observations"][0]["input_id"] = []
        artifact_path = _write_json(tmp_path / "results.json", artifact)

    completed = _run_pack(
        case_set_path=case_path,
        artifact_path=artifact_path,
    )
    assert completed.returncode != 0
    payload = json.loads(completed.stdout)
    assert payload["qualification_result"] == "INCONCLUSIVE"


def test_fix_validator_cross_role_ref_conflict_fail_closed(
    tmp_path: Path,
) -> None:
    case_set = _case_set_payload()
    item = _case(case_set, "C01")["inputs"][0]
    item["subject"]["supporting_knowledge_refs"] = ["R1"]
    item["knowledge_evidence"] = [
        {"ref": "R1", "material": "Conflicting knowledge material."}
    ]

    completed, payload = _run_payload(tmp_path, case_set=case_set)
    assert completed.returncode != 0
    assert payload["qualification_result"] == "INCONCLUSIVE"


def test_fix_validator_c10_may_model_explicitly_absent_material(
    tmp_path: Path,
) -> None:
    case_set = _case_set_payload()
    item = _case(case_set, "C10")["inputs"][0]
    item["repository_evidence"] = [{"ref": "R1", "material": ""}]

    completed, payload = _run_payload(tmp_path, case_set=case_set)
    assert completed.returncode == 0
    assert payload["qualification_result"] == "PASS"


def test_fix_validator_additional_known_property_is_not_silently_forbidden(
    tmp_path: Path,
) -> None:
    case_set = _case_set_payload()
    case = _case(case_set, "C06")
    case["critical_properties"] = sorted(
        [*case["critical_properties"], "FALSE_SUPPORT"]
    )

    completed, payload = _run_payload(tmp_path, case_set=case_set)
    assert completed.returncode == 0
    assert payload["qualification_result"] == "PASS"


@pytest.mark.parametrize(
    "reason",
    [
        "SUPPORTING_REFS_IRRELEVANT",
        "SUPPORTING_REFS_INSUFFICIENT",
    ],
)
def test_e3_red_qualification_rejects_incoherent_reason_pair(
    tmp_path: Path,
    reason: str,
) -> None:
    """Invalid assessor envelopes are INPUT_INVALID, not a semantic model FAIL."""
    def mutate(artifact: dict) -> None:
        observation = _artifact_observation(artifact, "C01.I01")
        observation["outcome"] = "INCONCLUSIVE"
        observation["reason_codes"] = [reason]

    completed, payload = _run_payload(tmp_path, artifact_mutator=mutate)
    assert completed.returncode == 2
    assert payload["qualification_result"] == "INCONCLUSIVE"
    assert any("reason" in item for item in payload["qualification_reasons"])
