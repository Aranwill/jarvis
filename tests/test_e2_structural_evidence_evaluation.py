from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
from functools import lru_cache
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
CASE_SET = ROOT / "evaluations" / "e2_structural_evidence_v0" / "cases.json"
RUNNER = ROOT / "scripts" / "evaluate_e2_structural_evidence.py"

EXPECTED_CASE_IDS = {
    "C1-exact-symbol",
    "C2-exact-module",
    "C3-substring",
    "C4-textual-knowledge",
    "C5-absent",
    "C6-truncation",
}

REQUIRED_OUTPUT_KEYS = {
    "baseline_commit",
    "case_count",
    "case_results",
    "structural_coverage_gain_count",
    "unexpected_structural_activation_count",
    "structural_fact_mismatch_count",
    "non_structural_regression_count",
    "invalid_paired_baseline_count",
    "conformance_result",
    "utility_observation",
}

REQUIRED_CASE_RESULT_KEYS = {
    "case_id",
    "case_result",
    "expected",
    "observed_a",
    "observed_b",
    "mismatches",
}


def _require_case_set() -> Path:
    assert CASE_SET.is_file(), (
        "E2 Structural Evidence Evaluation Pack V0 case-set is not implemented"
    )
    return CASE_SET


def _require_runner() -> Path:
    assert RUNNER.is_file(), (
        "E2 Structural Evidence Evaluation Pack V0 runner is not implemented"
    )
    return RUNNER


def _case_set_digest() -> str:
    return hashlib.sha256(_require_case_set().read_bytes()).hexdigest()


def _valid_review_args() -> list[str]:
    return [
        "--reviewer-id",
        "test-owner-reviewer",
        "--implementation-actor-id",
        "test-runner-writer",
        "--reviewed-case-set-digest",
        _case_set_digest(),
        "--review-evidence-reference",
        "TEST-ONLY-REVIEW-ATTESTATION",
    ]


def _run_raw(extra_args: list[str] | None = None) -> subprocess.CompletedProcess[str]:
    runner = _require_runner()
    return subprocess.run(
        [sys.executable, str(runner), *(extra_args or [])],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=60,
    )


@lru_cache(maxsize=1)
def _run_pack() -> dict[str, object]:
    completed = _run_raw(_valid_review_args())
    assert completed.returncode == 0, (
        "evaluation runner must complete successfully on its fixed deterministic "
        f"V0 pack; stderr={completed.stderr!r}"
    )
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise AssertionError(
            "evaluation runner must emit one JSON document to stdout"
        ) from exc
    assert isinstance(payload, dict), "evaluation output must be a JSON object"
    return payload


@lru_cache(maxsize=1)
def _runner_module():
    spec = importlib.util.spec_from_file_location(
        "malak_e2_structural_eval_runner_test",
        RUNNER,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _case_set_payload() -> dict:
    return json.loads(_require_case_set().read_text(encoding="utf-8"))


def _write_case_set(tmp_path: Path, payload: dict) -> Path:
    path = tmp_path / "cases.json"
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return path


def _assert_case_set_rejected(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    payload: dict,
    message: str,
) -> None:
    module = _runner_module()
    path = _write_case_set(tmp_path, payload)
    monkeypatch.setattr(module, "CASE_SET", path)
    with pytest.raises(ValueError, match=message):
        module._load_case_set()


def test_case_set_and_runner_artifacts_exist() -> None:
    _require_case_set()
    _require_runner()


def test_evaluation_output_has_closed_required_surface() -> None:
    payload = _run_pack()
    assert set(payload) == REQUIRED_OUTPUT_KEYS


def test_evaluation_pack_executes_exactly_the_six_declared_v0_cases() -> None:
    payload = _run_pack()
    case_results = payload["case_results"]
    assert isinstance(case_results, list)
    assert payload["case_count"] == 6
    assert len(case_results) == 6

    observed_ids = {
        result["case_id"]
        for result in case_results
        if isinstance(result, dict) and "case_id" in result
    }
    assert observed_ids == EXPECTED_CASE_IDS


def test_each_case_preserves_expected_observed_and_mismatch_evidence() -> None:
    payload = _run_pack()
    case_results = payload["case_results"]
    assert isinstance(case_results, list)

    for result in case_results:
        assert isinstance(result, dict)
        assert set(result) == REQUIRED_CASE_RESULT_KEYS
        assert result["case_result"] in {"PASS", "FAIL", "INVALID"}
        assert isinstance(result["mismatches"], list)


def test_pack_preserves_non_aggregate_failure_visibility() -> None:
    payload = _run_pack()
    case_results = payload["case_results"]
    assert isinstance(case_results, list)

    invalid_or_failed = [
        result
        for result in case_results
        if isinstance(result, dict)
        and result.get("case_result") in {"FAIL", "INVALID"}
    ]
    if invalid_or_failed:
        assert payload["conformance_result"] != "PASS"


def test_pack_preserves_evaluation_separations() -> None:
    payload = _run_pack()

    assert isinstance(payload["structural_coverage_gain_count"], int)
    assert isinstance(payload["unexpected_structural_activation_count"], int)
    assert isinstance(payload["structural_fact_mismatch_count"], int)
    assert isinstance(payload["non_structural_regression_count"], int)
    assert isinstance(payload["invalid_paired_baseline_count"], int)

    assert payload["unexpected_structural_activation_count"] == 0
    assert payload["structural_fact_mismatch_count"] == 0
    assert payload["non_structural_regression_count"] == 0
    assert payload["invalid_paired_baseline_count"] == 0

    assert payload["conformance_result"] in {"PASS", "FAIL", "INCONCLUSIVE"}
    assert payload["utility_observation"] is not None
    assert payload["utility_observation"]["authority_effect"] == "none"


def test_case_set_cannot_self_attest_ground_truth_review() -> None:
    raw = _require_case_set().read_text(encoding="utf-8")
    assert "ground_truth_review_status" not in raw
    assert "OWNER_APPROVED_DESIGN" not in raw


def test_valid_review_attestation_is_declared_not_self_verified() -> None:
    payload = _run_pack()
    review = payload["utility_observation"]["ground_truth_review"]

    assert review["status"] == "EXTERNAL_ATTESTATION_DECLARED"
    assert review["evaluation_executable"] is True
    assert review["identity_independence_claimed"] is True
    assert review["identity_independence_verified"] is False
    assert review["requires_external_validation"] is True
    assert review["reviewed_case_set_digest"] == _case_set_digest()
    assert review["review_evidence_reference"] == "TEST-ONLY-REVIEW-ATTESTATION"
    assert "must still be validated outside this runner" in review["reason"]


def test_missing_external_review_is_inconclusive_and_not_executable() -> None:
    completed = _run_raw()
    payload = json.loads(completed.stdout)

    assert completed.returncode == 2
    assert payload["conformance_result"] == "INCONCLUSIVE"
    assert payload["case_results"] == []
    review = payload["utility_observation"]["ground_truth_review"]
    assert review["status"] == "MISSING_EXTERNAL_ATTESTATION"
    assert review["evaluation_executable"] is False
    assert review["requires_external_validation"] is True


def test_review_digest_mismatch_is_inconclusive_and_not_executable() -> None:
    args = _valid_review_args()
    digest_index = args.index("--reviewed-case-set-digest") + 1
    args[digest_index] = "0" * 64

    completed = _run_raw(args)
    payload = json.loads(completed.stdout)

    assert completed.returncode == 2
    assert payload["conformance_result"] == "INCONCLUSIVE"
    review = payload["utility_observation"]["ground_truth_review"]
    assert review["status"] == "REVIEW_DIGEST_MISMATCH"
    assert review["evaluation_executable"] is False


def test_reviewer_implementer_collision_is_inconclusive() -> None:
    args = _valid_review_args()
    reviewer = args[args.index("--reviewer-id") + 1]
    actor_index = args.index("--implementation-actor-id") + 1
    args[actor_index] = reviewer

    completed = _run_raw(args)
    payload = json.loads(completed.stdout)

    assert completed.returncode == 2
    assert payload["conformance_result"] == "INCONCLUSIVE"
    review = payload["utility_observation"]["ground_truth_review"]
    assert review["status"] == "REVIEWER_IMPLEMENTER_COLLISION"
    assert review["evaluation_executable"] is False


def test_partial_review_attestation_is_inconclusive() -> None:
    args = _valid_review_args()
    ref_index = args.index("--review-evidence-reference")
    del args[ref_index : ref_index + 2]

    completed = _run_raw(args)
    payload = json.loads(completed.stdout)

    assert completed.returncode == 2
    assert payload["conformance_result"] == "INCONCLUSIVE"
    review = payload["utility_observation"]["ground_truth_review"]
    assert review["status"] == "PARTIAL_EXTERNAL_ATTESTATION"
    assert review["evaluation_executable"] is False


def test_malformed_review_digest_is_inconclusive() -> None:
    args = _valid_review_args()
    digest_index = args.index("--reviewed-case-set-digest") + 1
    args[digest_index] = "NOT-A-SHA256"

    completed = _run_raw(args)
    payload = json.loads(completed.stdout)

    assert completed.returncode == 2
    assert payload["conformance_result"] == "INCONCLUSIVE"
    review = payload["utility_observation"]["ground_truth_review"]
    assert review["status"] == "INVALID_REVIEW_DIGEST"
    assert review["evaluation_executable"] is False


def test_malformed_review_provenance_is_inconclusive() -> None:
    args = _valid_review_args()
    reviewer_index = args.index("--reviewer-id") + 1
    args[reviewer_index] = " test-owner-reviewer"

    completed = _run_raw(args)
    payload = json.loads(completed.stdout)

    assert completed.returncode == 2
    assert payload["conformance_result"] == "INCONCLUSIVE"
    review = payload["utility_observation"]["ground_truth_review"]
    assert review["status"] == "INVALID_REVIEW_PROVENANCE"
    assert review["evaluation_executable"] is False


def test_case_set_exists_without_becoming_executable_input() -> None:
    raw = _require_case_set().read_text(encoding="utf-8")

    forbidden_markers = (
        "http://",
        "https://",
        "subprocess",
        "os.system",
        "shell=True",
    )
    assert not any(marker in raw for marker in forbidden_markers)


def test_schema_rejects_unknown_top_level_field(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    payload = _case_set_payload()
    payload["unexpected"] = True
    _assert_case_set_rejected(
        monkeypatch,
        tmp_path,
        payload,
        "case-set top-level schema mismatch",
    )


def test_schema_rejects_missing_case_field(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    payload = _case_set_payload()
    del payload["cases"][0]["subject"]
    _assert_case_set_rejected(
        monkeypatch,
        tmp_path,
        payload,
        "case schema mismatch",
    )


def test_schema_rejects_unknown_case_field_including_review_self_attestation(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    payload = _case_set_payload()
    payload["cases"][0]["ground_truth_review_status"] = "OWNER_APPROVED_DESIGN"
    _assert_case_set_rejected(
        monkeypatch,
        tmp_path,
        payload,
        "case schema mismatch",
    )


def test_schema_rejects_wrong_type(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    payload = _case_set_payload()
    payload["cases"][0]["expected_total_structural_count"] = "1"
    _assert_case_set_rejected(
        monkeypatch,
        tmp_path,
        payload,
        "expected_total_structural_count must be int",
    )


def test_schema_rejects_unknown_enum(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    payload = _case_set_payload()
    payload["cases"][0]["comparison_class"] = "MAGIC"
    _assert_case_set_rejected(
        monkeypatch,
        tmp_path,
        payload,
        "unsupported comparison class",
    )


def test_schema_rejects_duplicate_case_id(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    payload = _case_set_payload()
    payload["cases"][1]["case_id"] = payload["cases"][0]["case_id"]
    _assert_case_set_rejected(
        monkeypatch,
        tmp_path,
        payload,
        "duplicate case_id",
    )


def test_schema_rejects_blank_subject(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    payload = _case_set_payload()
    payload["cases"][0]["subject"] = "   "
    _assert_case_set_rejected(
        monkeypatch,
        tmp_path,
        payload,
        "subject must be non-empty",
    )


def test_schema_rejects_unsupported_fixture(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    payload = _case_set_payload()
    payload["cases"][0]["fixture_profile"] = "arbitrary"
    _assert_case_set_rejected(
        monkeypatch,
        tmp_path,
        payload,
        "unsupported fixture profile",
    )


def test_schema_rejects_unknown_structural_fact_type(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    payload = _case_set_payload()
    payload["cases"][0]["expected_structural_facts"][0]["fact_type"] = "semantic"
    _assert_case_set_rejected(
        monkeypatch,
        tmp_path,
        payload,
        "unsupported structural fact type",
    )
