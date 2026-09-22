from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


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
        "RED: E2 Structural Evidence Evaluation Pack V0 case-set is not implemented"
    )
    return CASE_SET


def _require_runner() -> Path:
    assert RUNNER.is_file(), (
        "RED: E2 Structural Evidence Evaluation Pack V0 runner is not implemented"
    )
    return RUNNER


def _run_pack() -> dict[str, object]:
    runner = _require_runner()
    completed = subprocess.run(
        [sys.executable, str(runner)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=60,
    )
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


def test_red_case_set_artifact_is_missing_before_green() -> None:
    _require_case_set()


def test_red_runner_artifact_is_missing_before_green() -> None:
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


def test_case_set_exists_without_becoming_executable_input() -> None:
    case_set = _require_case_set()
    raw = case_set.read_text(encoding="utf-8")

    forbidden_markers = (
        "http://",
        "https://",
        "subprocess",
        "os.system",
        "shell=True",
    )
    assert not any(marker in raw for marker in forbidden_markers)
