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
    "case_results",
    "metrics",
    "qualification_result",
    "qualification_reasons",
    "authority_effect",
}
EXPECTED_CASE_RESULT_KEYS = {
    "case_id",
    "expected_disposition",
    "observed_disposition",
    "expected_reason_class",
    "observed_reason_codes",
    "case_result",
    "mismatch_reasons",
}


def _require_case_set() -> Path:
    assert CASE_SET.is_file(), "R01: fixed C01-C18 case-set is absent"
    return CASE_SET


def _require_runner() -> Path:
    assert RUNNER.is_file(), "R01: qualification runner is absent"
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


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _fingerprint(subject: dict) -> str:
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
    encoded = json.dumps(
        material,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _valid_artifact(case_set: dict, case_set_digest: str) -> dict:
    return {
        "schema_version": "MALAK-E3-SUPPORT-ASSESSOR-RESULTS/v0",
        "case_set_digest": case_set_digest,
        "assessor_mechanism": {
            "mechanism_id": "test-assessor",
            "mechanism_version": "v0",
            "mechanism_kind": "DETERMINISTIC",
            "config_digest": "c" * 64,
            "producer_subject_id": "experiment-producer",
            "assessor_subject_id": "candidate-assessor",
            "model_provenance": None,
        },
        "harness": {
            "harness_policy_version": "test-harness/v0",
            "harness_policy_digest": "h" * 64,
            "budget_manifest_digest": "b" * 64,
            "attempt_policy_digest": "a" * 64,
        },
        "case_results": [
            {
                "case_id": case["case_id"],
                "subject_fingerprint": _fingerprint(case["subject"]),
                "outcome": case["expected_outcome"],
                "reason_codes": case["expected_reason_codes"],
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


def _case(payload: dict, case_id: str) -> dict:
    return next(item for item in payload["case_results"] if item["case_id"] == case_id)


def test_red_r01_required_artifacts_absent() -> None:
    _require_case_set()
    _require_runner()


def test_red_r02_unknown_top_level_case_set_field_is_rejected(tmp_path: Path) -> None:
    case_set = _case_set_payload()
    case_set["unexpected"] = True
    completed, payload = _run_payload(tmp_path, case_set=case_set)
    assert completed.returncode != 0
    assert payload["qualification_result"] == "INCONCLUSIVE"


@pytest.mark.parametrize("mutation", ["missing", "wrong_type", "unknown"])
def test_red_r03_case_schema_invalid_is_rejected(tmp_path: Path, mutation: str) -> None:
    case_set = _case_set_payload()
    case = case_set["cases"][0]
    if mutation == "missing":
        del case["case_class"]
    elif mutation == "wrong_type":
        case["critical_properties"] = "FALSE_SUPPORT"
    else:
        case["unexpected"] = True
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
        case_set["cases"].append(extra)
    completed, payload = _run_payload(tmp_path, case_set=case_set)
    assert completed.returncode != 0
    assert payload["qualification_result"] == "INCONCLUSIVE"


def test_red_r05_unsupported_schema_version_is_rejected(tmp_path: Path) -> None:
    case_set = _case_set_payload()
    case_set["schema_version"] = "future/v9"
    completed, payload = _run_payload(tmp_path, case_set=case_set)
    assert completed.returncode != 0
    assert payload["qualification_result"] == "INCONCLUSIVE"


def test_red_r06_ground_truth_digest_mismatch_blocks_pass(tmp_path: Path) -> None:
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


def test_red_r07_reviewer_runner_actor_collision_blocks_pass(tmp_path: Path) -> None:
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


def test_red_r08_reviewer_assessor_collision_blocks_pass(tmp_path: Path) -> None:
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
def test_red_r09_artifact_schema_invalid_is_rejected(
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


def test_red_r10_artifact_case_set_digest_mismatch_blocks_pass(tmp_path: Path) -> None:
    def mutate(artifact: dict) -> None:
        artifact["case_set_digest"] = "0" * 64

    completed, payload = _run_payload(tmp_path, artifact_mutator=mutate)
    assert completed.returncode != 0
    assert payload["qualification_result"] == "INCONCLUSIVE"


def test_red_r11_subject_fingerprint_drift_blocks_pass(tmp_path: Path) -> None:
    def mutate(artifact: dict) -> None:
        artifact["case_results"][0]["subject_fingerprint"] = "0" * 64

    completed, payload = _run_payload(tmp_path, artifact_mutator=mutate)
    assert completed.returncode != 0
    assert payload["qualification_result"] == "INCONCLUSIVE"


def test_red_r12_model_based_artifact_requires_complete_provenance(
    tmp_path: Path,
) -> None:
    def mutate(artifact: dict) -> None:
        artifact["assessor_mechanism"]["mechanism_kind"] = "MODEL_BASED"
        artifact["assessor_mechanism"]["model_provenance"] = None

    completed, payload = _run_payload(tmp_path, artifact_mutator=mutate)
    assert completed.returncode != 0
    assert payload["qualification_result"] == "INCONCLUSIVE"


def test_red_r13_mechanism_cannot_self_certify(tmp_path: Path) -> None:
    def mutate(artifact: dict) -> None:
        artifact["assessor_mechanism"]["producer_subject_id"] = (
            artifact["assessor_mechanism"]["assessor_subject_id"]
        )

    completed, payload = _run_payload(tmp_path, artifact_mutator=mutate)
    assert completed.returncode != 0
    assert payload["qualification_result"] != "PASS"


def test_red_r14_exact_support_case_can_pass(tmp_path: Path) -> None:
    completed, payload = _run_payload(tmp_path)
    assert completed.returncode == 0
    assert _case(payload, "C01")["case_result"] == "PASS"


@pytest.mark.parametrize("case_id", ["C02", "C03", "C07", "C09", "C16"])
def test_red_r15_unsupported_cases_cannot_be_promoted_to_supported(
    tmp_path: Path, case_id: str
) -> None:
    def mutate(artifact: dict) -> None:
        result = next(x for x in artifact["case_results"] if x["case_id"] == case_id)
        result["outcome"] = "SUPPORTED"
        result["reason_codes"] = ["MATERIAL_SUPPORT_CONFIRMED"]

    completed, payload = _run_payload(tmp_path, artifact_mutator=mutate)
    assert completed.returncode != 0
    assert payload["qualification_result"] == "FAIL"
    assert _case(payload, case_id)["case_result"] == "FAIL"


def test_red_r16_compound_partial_support_remains_inconclusive(
    tmp_path: Path,
) -> None:
    def mutate(artifact: dict) -> None:
        result = next(x for x in artifact["case_results"] if x["case_id"] == "C04")
        result["outcome"] = "SUPPORTED"
        result["reason_codes"] = ["MATERIAL_SUPPORT_CONFIRMED"]

    completed, payload = _run_payload(tmp_path, artifact_mutator=mutate)
    assert completed.returncode != 0
    assert payload["qualification_result"] == "FAIL"


def test_red_r17_unresolved_counterevidence_cannot_be_supported(
    tmp_path: Path,
) -> None:
    def mutate(artifact: dict) -> None:
        result = next(x for x in artifact["case_results"] if x["case_id"] == "C06")
        result["outcome"] = "SUPPORTED"
        result["reason_codes"] = ["MATERIAL_SUPPORT_CONFIRMED"]

    completed, payload = _run_payload(tmp_path, artifact_mutator=mutate)
    assert completed.returncode != 0
    assert payload["qualification_result"] == "FAIL"


@pytest.mark.parametrize("case_id", ["C11", "C12"])
def test_red_r18_binding_drift_is_detected_fail_closed(
    tmp_path: Path, case_id: str
) -> None:
    completed, payload = _run_payload(tmp_path)
    assert completed.returncode == 0
    assert _case(payload, case_id)["case_result"] == "PASS"
    assert payload["metrics"]["binding_drift_detection_rate"] == 1


def test_red_r19_equivalent_ref_permutation_is_stable(tmp_path: Path) -> None:
    baseline = _case_set_payload()
    permuted = copy.deepcopy(baseline)
    case = next(x for x in permuted["cases"] if x["case_id"] == "C13")
    case["subject"]["supporting_repository_refs"].reverse()
    case["repository_evidence"].reverse()

    original_case = next(x for x in baseline["cases"] if x["case_id"] == "C13")
    assert _fingerprint(original_case["subject"]) == _fingerprint(case["subject"])

    completed, payload = _run_payload(tmp_path, case_set=permuted)
    assert completed.returncode == 0
    assert payload["metrics"]["assessment_stability_on_equivalent_inputs"] == 1


@pytest.mark.parametrize("case_id", ["C14", "C15"])
def test_red_r20_unavailable_or_malformed_assessor_remains_non_positive(
    tmp_path: Path, case_id: str
) -> None:
    def mutate(artifact: dict) -> None:
        result = next(x for x in artifact["case_results"] if x["case_id"] == case_id)
        result["outcome"] = "SUPPORTED"
        result["reason_codes"] = ["MATERIAL_SUPPORT_CONFIRMED"]

    completed, payload = _run_payload(tmp_path, artifact_mutator=mutate)
    assert completed.returncode != 0
    assert payload["qualification_result"] == "FAIL"


def test_red_r21_metric_formulas_match_frozen_expectations(tmp_path: Path) -> None:
    completed, payload = _run_payload(tmp_path)
    assert completed.returncode == 0
    metrics = payload["metrics"]
    assert metrics["false_support_acceptance_rate"] == 0
    assert metrics["unsupported_claim_escape_rate"] == 0
    assert metrics["false_inconclusive_rate"] == 0
    assert metrics["contradiction_handling_recall"] == 1
    assert metrics["assessment_stability_on_equivalent_inputs"] == 1
    assert metrics["binding_drift_detection_rate"] == 1


def test_red_r22_any_safety_floor_violation_prevents_pass(tmp_path: Path) -> None:
    def mutate(artifact: dict) -> None:
        result = next(x for x in artifact["case_results"] if x["case_id"] == "C03")
        result["outcome"] = "SUPPORTED"
        result["reason_codes"] = ["MATERIAL_SUPPORT_CONFIRMED"]

    completed, payload = _run_payload(tmp_path, artifact_mutator=mutate)
    assert completed.returncode != 0
    assert payload["qualification_result"] == "FAIL"


def test_red_r23_authority_effect_is_fixed_to_none(tmp_path: Path) -> None:
    completed, payload = _run_payload(tmp_path)
    assert completed.returncode == 0
    assert set(payload) == EXPECTED_OUTPUT_KEYS
    assert payload["authority_effect"] == "none"
    for result in payload["case_results"]:
        assert set(result) == EXPECTED_CASE_RESULT_KEYS


def test_red_r24_runner_has_no_model_network_or_repo_write_side_effects(
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


def test_red_r25_no_case_selection_or_skip_interface_exists() -> None:
    source = _require_runner().read_text(encoding="utf-8")
    forbidden = (
        "--case-id",
        "--filter",
        "--select",
        "--skip",
        "xfail",
        "pytest.skip",
    )
    assert not any(marker in source for marker in forbidden)


def test_red_r26_pass_requires_all_18_cases_valid_and_evaluable(
    tmp_path: Path,
) -> None:
    completed, payload = _run_payload(tmp_path)
    assert completed.returncode == 0
    assert payload["qualification_result"] == "PASS"
    assert payload["case_count"] == 18
    assert {x["case_id"] for x in payload["case_results"]} == EXPECTED_CASE_IDS
    assert all(x["case_result"] == "PASS" for x in payload["case_results"])
