from __future__ import annotations

import copy
import json
import os
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "malak_rdd_receipt.py"


def git(repo: Path, *args: str) -> str:
    done = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return done.stdout.strip()


def make_repo(tmp_path: Path) -> tuple[Path, str, str]:
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init")
    git(repo, "config", "user.email", "test@example.com")
    git(repo, "config", "user.name", "Malak Test")
    git(repo, "config", "commit.gpgsign", "false")

    (repo / "file.txt").write_text("baseline\n", encoding="utf-8")
    git(repo, "add", "file.txt")
    git(repo, "commit", "--no-gpg-sign", "-m", "baseline")
    baseline = git(repo, "rev-parse", "HEAD")

    (repo / "file.txt").write_text("candidate\n", encoding="utf-8")
    git(repo, "add", "file.txt")
    git(repo, "commit", "--no-gpg-sign", "-m", "candidate")
    candidate = git(repo, "rev-parse", "HEAD")
    return repo, baseline, candidate


def manifest(baseline: str, candidate: str) -> dict:
    lens = {
        "result": "PASS",
        "finding_refs": [],
        "evidence_reference": "4r-evidence",
    }
    return {
        "schema": "MALAK-EVIDENCE-MANIFEST/v1",
        "repository": "Aranwill/jarvis",
        "baseline_commit": baseline,
        "candidate_commit": candidate,
        "unit_id": "RDD2-V1-TEST",
        "specification_reference": "design.md",
        "gate": "G5",
        "risk_class": 3,
        "scope_reference": "scope.md",
        "validations": [
            {
                "id": "pytest",
                "method": "python -m pytest",
                "result": "PASS",
                "evidence_reference": "ci-evidence",
            }
        ],
        "four_r": {
            "risk": copy.deepcopy(lens),
            "readability": copy.deepcopy(lens),
            "reliability": copy.deepcopy(lens),
            "resilience": copy.deepcopy(lens),
        },
        "finding_refs": ["F-RESOLVED-01", "F-RESOLVED-02"],
        "correction_round": 1,
        "producer": "writer",
        "validator": "stage1-validator",
        "result": "PASS",
        "generated_at": "2026-10-10T15:00:00+00:00",
        "evidence_references": ["ci-evidence", "4r-evidence"],
        "authority_effect": "none",
    }


def write_json(path: Path, payload: dict) -> Path:
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    return path


def run_cli(*args: str):
    done = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        check=False,
    )
    output = json.loads(done.stdout)
    return done.returncode, output


def issue(
    tmp_path: Path,
    repo: Path,
    payload: dict,
    *,
    result: str = "PASS",
    issued_at: str = "2026-10-10T15:00:00Z",
    extra: list[str] | None = None,
):
    path = write_json(tmp_path / "manifest.json", payload)
    args = [
        "issue",
        "--manifest", str(path),
        "--repo-root", str(repo),
        "--candidate-conformance-result", result,
        "--candidate-conformance-reference", "PR#266-comment",
        "--validator", "receipt-validator",
        "--independence-reference", "independent-review",
        "--evidence-reference", "ci-evidence",
        "--issued-at", issued_at,
    ]
    if extra:
        args.extend(extra)
    return run_cli(*args)


def issue_receipt(tmp_path: Path, repo: Path, payload: dict, *, result: str = "PASS") -> dict:
    code, output = issue(tmp_path, repo, payload, result=result)
    assert code == 0, output
    assert output["schema"] == "MALAK-RDD-VALIDATION-RECEIPT/v1"
    return output


def validate(
    tmp_path: Path,
    repo: Path,
    receipt: dict,
    payload: dict,
    *,
    extra: list[str] | None = None,
):
    receipt_path = write_json(tmp_path / "receipt.json", receipt)
    manifest_path = write_json(tmp_path / "manifest-validate.json", payload)
    args = [
        "validate",
        "--receipt", str(receipt_path),
        "--manifest", str(manifest_path),
        "--repo-root", str(repo),
    ]
    if extra:
        args.extend(extra)
    return run_cli(*args)


def test_issue_and_validate_candidate_bound_receipt(tmp_path):
    repo, baseline, candidate = make_repo(tmp_path)
    payload = manifest(baseline, candidate)

    receipt = issue_receipt(tmp_path, repo, payload)
    code, report = validate(tmp_path, repo, receipt, payload)

    assert code == 0
    assert report["validator_result"] == "PASS"
    assert report["code"] == "VALID"
    assert report["candidate_conformance_result"] == "PASS"
    assert receipt["repository"] == payload["repository"]
    assert receipt["baseline_commit"] == baseline
    assert receipt["candidate_commit"] == candidate
    assert receipt["candidate_tree"] == git(repo, "rev-parse", f"{candidate}^{{tree}}")
    assert receipt["unit_id"] == payload["unit_id"]
    assert receipt["risk_class"] == payload["risk_class"]
    assert receipt["specification_reference"] == payload["specification_reference"]
    assert receipt["scope_reference"] == payload["scope_reference"]
    assert receipt["correction_round"] == payload["correction_round"]
    assert receipt["finding_refs"] == payload["finding_refs"]
    assert receipt["stage1_manifest_result"] == payload["result"]
    assert receipt["authority_effect"] == "none"


def test_manifest_shape_and_identity_fail_closed(tmp_path):
    repo, baseline, candidate = make_repo(tmp_path)
    base = manifest(baseline, candidate)
    cases = [
        ("missing", lambda p: p.pop("scope_reference"), "INVALID_KEYS"),
        ("extra", lambda p: p.__setitem__("approved", True), "INVALID_KEYS"),
        ("schema", lambda p: p.__setitem__("schema", "OTHER"), "INVALID_SCHEMA"),
        ("repo", lambda p: p.__setitem__("repository", "Other/repo"), "INVALID_REPOSITORY"),
        ("sha", lambda p: p.__setitem__("candidate_commit", "ABC"), "INVALID_COMMIT_SHA"),
        ("authority", lambda p: p.__setitem__("authority_effect", "approved"), "AUTHORITY_EFFECT_INVALID"),
    ]
    for name, mutate, expected in cases:
        payload = copy.deepcopy(base)
        mutate(payload)
        code, output = issue(tmp_path, repo, payload)
        assert code == 1, name
        assert output["code"] == expected, (name, output)


def test_manifest_duplicate_keys_rejected_before_digest(tmp_path):
    repo, baseline, candidate = make_repo(tmp_path)
    payload = manifest(baseline, candidate)
    raw = json.dumps(payload)
    raw = raw.replace(
        '"repository": "Aranwill/jarvis",',
        '"repository": "Aranwill/jarvis", "repository": "Aranwill/jarvis",',
        1,
    )
    path = tmp_path / "dup-manifest.json"
    path.write_text(raw, encoding="utf-8")
    code, output = run_cli(
        "issue",
        "--manifest", str(path),
        "--repo-root", str(repo),
        "--candidate-conformance-result", "PASS",
        "--candidate-conformance-reference", "ref",
        "--validator", "validator",
        "--independence-reference", "independent",
        "--evidence-reference", "evidence",
        "--issued-at", "2026-10-10T15:00:00Z",
    )
    assert code == 1
    assert output["code"] == "DUPLICATE_KEY"

    nested = json.dumps(payload).replace(
        '"method": "python -m pytest",',
        '"method": "python -m pytest", "method": "python -m pytest",',
        1,
    )
    path.write_text(nested, encoding="utf-8")
    code, output = run_cli(
        "issue",
        "--manifest", str(path),
        "--repo-root", str(repo),
        "--candidate-conformance-result", "PASS",
        "--candidate-conformance-reference", "ref",
        "--validator", "validator",
        "--independence-reference", "independent",
        "--evidence-reference", "evidence",
        "--issued-at", "2026-10-10T15:00:00Z",
    )
    assert code == 1
    assert output["code"] == "DUPLICATE_KEY"


def test_non_standard_json_numbers_rejected(tmp_path):
    repo, baseline, candidate = make_repo(tmp_path)
    payload = manifest(baseline, candidate)
    raw = json.dumps(payload).replace('"risk_class": 3', '"risk_class": NaN', 1)
    path = tmp_path / "nan-manifest.json"
    path.write_text(raw, encoding="utf-8")
    code, output = run_cli(
        "issue",
        "--manifest", str(path),
        "--repo-root", str(repo),
        "--candidate-conformance-result", "PASS",
        "--candidate-conformance-reference", "ref",
        "--validator", "validator",
        "--independence-reference", "independent",
        "--evidence-reference", "evidence",
        "--issued-at", "2026-10-10T15:00:00Z",
    )
    assert code == 1
    assert output["code"] == "NON_STANDARD_JSON_NUMBER"


def test_manifest_bool_as_integer_and_full4r_are_rejected(tmp_path):
    repo, baseline, candidate = make_repo(tmp_path)
    for field in ("risk_class", "correction_round"):
        payload = manifest(baseline, candidate)
        payload[field] = True
        code, output = issue(tmp_path, repo, payload)
        assert code == 1
        assert output["validator_result"] == "FAIL"

    payload = manifest(baseline, candidate)
    del payload["four_r"]["resilience"]
    code, output = issue(tmp_path, repo, payload)
    assert code == 1
    assert output["code"] == "FOUR_R_INCOMPLETE"


def test_receipt_preserves_pass_fail_inconclusive_without_rewriting(tmp_path):
    repo, baseline, candidate = make_repo(tmp_path)
    payload = manifest(baseline, candidate)

    for result in ("PASS", "FAIL", "INCONCLUSIVE"):
        receipt = issue_receipt(tmp_path, repo, payload, result=result)
        code, report = validate(tmp_path, repo, receipt, payload)
        assert code == 0
        assert report["validator_result"] == "PASS"
        assert report["candidate_conformance_result"] == result
        assert receipt["candidate_conformance_result"] == result


def test_receipt_substitution_matrix_fails_closed(tmp_path):
    repo, baseline, candidate = make_repo(tmp_path)
    payload = manifest(baseline, candidate)
    receipt = issue_receipt(tmp_path, repo, payload)

    other_baseline = candidate
    cases = [
        ("repository", "Other/repo"),
        ("baseline_commit", other_baseline),
        ("unit_id", "OTHER-UNIT"),
        ("risk_class", 2),
        ("specification_reference", "other-spec.md"),
        ("scope_reference", "other-scope.md"),
        ("correction_round", 0),
        ("finding_refs", ["F-RESOLVED-02", "F-RESOLVED-01"]),
        ("stage1_manifest_schema", "OTHER"),
        ("stage1_manifest_result", "FAIL"),
    ]
    for field, value in cases:
        mutated = copy.deepcopy(receipt)
        mutated[field] = value
        # Deliberately leave receipt_digest stale: validation must still fail closed.
        code, output = validate(tmp_path, repo, mutated, payload)
        assert code == 1, field
        assert output["validator_result"] == "FAIL"


def test_manifest_semantic_substitution_is_detected_even_same_candidate(tmp_path):
    repo, baseline, candidate = make_repo(tmp_path)
    payload = manifest(baseline, candidate)
    receipt = issue_receipt(tmp_path, repo, payload)

    changed = copy.deepcopy(payload)
    changed["scope_reference"] = "changed-scope.md"
    code, output = validate(tmp_path, repo, receipt, changed)

    assert code == 1
    assert output["code"] in {"MANIFEST_RECEIPT_MISMATCH", "DIGEST_MISMATCH"}


def test_wrong_candidate_tree_is_rejected(tmp_path):
    repo, baseline, candidate = make_repo(tmp_path)
    payload = manifest(baseline, candidate)
    receipt = issue_receipt(tmp_path, repo, payload)
    receipt["candidate_tree"] = "0" * 40

    code, output = validate(tmp_path, repo, receipt, payload)

    assert code == 1
    assert output["code"] in {"CANDIDATE_TREE_MISMATCH", "DIGEST_MISMATCH"}


def test_receipt_digest_mismatch_is_rejected(tmp_path):
    repo, baseline, candidate = make_repo(tmp_path)
    payload = manifest(baseline, candidate)
    receipt = issue_receipt(tmp_path, repo, payload)
    receipt["receipt_digest"] = "0" * 64

    code, output = validate(tmp_path, repo, receipt, payload)

    assert code == 1
    assert output["code"] == "DIGEST_MISMATCH"


def test_expected_candidate_detects_stale_receipt(tmp_path):
    repo, baseline, candidate = make_repo(tmp_path)
    payload = manifest(baseline, candidate)
    receipt = issue_receipt(tmp_path, repo, payload)

    (repo / "file.txt").write_text("next\n", encoding="utf-8")
    git(repo, "add", "file.txt")
    git(repo, "commit", "--no-gpg-sign", "-m", "next")
    next_candidate = git(repo, "rev-parse", "HEAD")

    code, output = validate(
        tmp_path, repo, receipt, payload,
        extra=["--expected-candidate", next_candidate],
    )
    assert code == 1
    assert output["code"] == "STALE_CANDIDATE"


def test_require_current_detects_dirty_worktree(tmp_path):
    repo, baseline, candidate = make_repo(tmp_path)
    payload = manifest(baseline, candidate)
    receipt = issue_receipt(tmp_path, repo, payload)
    (repo / "file.txt").write_text("dirty\n", encoding="utf-8")

    code, output = validate(
        tmp_path, repo, receipt, payload,
        extra=["--require-current"],
    )
    assert code == 1
    assert output["code"] == "DIRTY_WORKTREE"


def test_unknown_git_object_and_non_ancestor_fail_closed(tmp_path):
    repo, baseline, candidate = make_repo(tmp_path)

    payload = manifest(baseline, candidate)
    payload["candidate_commit"] = "f" * 40
    code, output = issue(tmp_path, repo, payload)
    assert code == 1
    assert output["code"] == "GIT_OBJECT_NOT_FOUND"

    payload = manifest(candidate, baseline)
    code, output = issue(tmp_path, repo, payload)
    assert code == 1
    assert output["code"] == "BASELINE_NOT_ANCESTOR"


def test_receipt_strict_types_enums_timestamp_and_digest_shape(tmp_path):
    repo, baseline, candidate = make_repo(tmp_path)
    payload = manifest(baseline, candidate)
    receipt = issue_receipt(tmp_path, repo, payload)

    cases = [
        ("risk_class", True, "INVALID_FIELD"),
        ("correction_round", True, "INVALID_FIELD"),
        ("candidate_conformance_result", "MAYBE", "INVALID_RESULT"),
        ("issued_at", "2026-10-10T12:00:00-03:00", "INVALID_TIMESTAMP"),
        ("candidate_commit", candidate.upper(), "INVALID_COMMIT_SHA"),
        ("stage1_manifest_digest", "A" * 64, "INVALID_DIGEST"),
        ("authority_effect", "approved", "AUTHORITY_EFFECT_INVALID"),
        ("validator", " ", "INVALID_FIELD"),
        ("evidence_references", ["same", "same"], "INVALID_FIELD"),
    ]
    for field, value, expected in cases:
        mutated = copy.deepcopy(receipt)
        mutated[field] = value
        code, output = validate(tmp_path, repo, mutated, payload)
        assert code == 1, field
        assert output["code"] == expected, (field, output)


def test_receipt_duplicate_keys_rejected_before_digest(tmp_path):
    repo, baseline, candidate = make_repo(tmp_path)
    payload = manifest(baseline, candidate)
    receipt = issue_receipt(tmp_path, repo, payload)
    manifest_path = write_json(tmp_path / "manifest-dup-receipt.json", payload)

    raw = json.dumps(receipt).replace(
        '"candidate_commit":',
        '"candidate_commit": "' + candidate + '", "candidate_commit":',
        1,
    )
    receipt_path = tmp_path / "dup-receipt.json"
    receipt_path.write_text(raw, encoding="utf-8")

    code, output = run_cli(
        "validate",
        "--receipt", str(receipt_path),
        "--manifest", str(manifest_path),
        "--repo-root", str(repo),
    )
    assert code == 1
    assert output["code"] == "DUPLICATE_KEY"

    nested = json.dumps(receipt)
    nested = nested[:-1] + ', "unexpected": {"x": 1, "x": 2}}'
    receipt_path.write_text(nested, encoding="utf-8")
    code, output = run_cli(
        "validate",
        "--receipt", str(receipt_path),
        "--manifest", str(manifest_path),
        "--repo-root", str(repo),
    )
    assert code == 1
    assert output["code"] == "DUPLICATE_KEY"


def test_manifest_digest_is_semantic_and_whitespace_independent(tmp_path):
    repo, baseline, candidate = make_repo(tmp_path)
    payload = manifest(baseline, candidate)
    receipt_a = issue_receipt(tmp_path, repo, payload)

    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(payload, indent=4, ensure_ascii=False), encoding="utf-8")
    code, receipt_b = run_cli(
        "issue",
        "--manifest", str(path),
        "--repo-root", str(repo),
        "--candidate-conformance-result", "PASS",
        "--candidate-conformance-reference", "PR#266-comment",
        "--validator", "receipt-validator",
        "--independence-reference", "independent-review",
        "--evidence-reference", "ci-evidence",
        "--issued-at", "2026-10-10T15:00:00Z",
    )
    assert code == 0
    assert receipt_b["stage1_manifest_digest"] == receipt_a["stage1_manifest_digest"]

    changed = copy.deepcopy(payload)
    changed["scope_reference"] = "semantic-change.md"
    receipt_c = issue_receipt(tmp_path, repo, changed)
    assert receipt_c["stage1_manifest_digest"] != receipt_a["stage1_manifest_digest"]


def test_output_inside_repo_is_rejected(tmp_path):
    repo, baseline, candidate = make_repo(tmp_path)
    payload = manifest(baseline, candidate)
    output = repo / "receipt.json"

    code, report = issue(
        tmp_path, repo, payload,
        extra=["--output", str(output)],
    )

    assert code == 1
    assert report["code"] == "OUTPUT_INSIDE_REPOSITORY"
    assert not output.exists()


def test_output_symlink_into_repo_is_rejected_when_supported(tmp_path):
    repo, baseline, candidate = make_repo(tmp_path)
    payload = manifest(baseline, candidate)
    link = tmp_path / "repo-link"
    try:
        link.symlink_to(repo, target_is_directory=True)
    except OSError:
        return

    output = link / "receipt.json"
    code, report = issue(
        tmp_path, repo, payload,
        extra=["--output", str(output)],
    )

    assert code == 1
    assert report["code"] == "OUTPUT_INSIDE_REPOSITORY"
    assert not (repo / "receipt.json").exists()


def test_output_is_non_destructive_and_no_partial_file_on_failure(tmp_path):
    repo, baseline, candidate = make_repo(tmp_path)
    payload = manifest(baseline, candidate)
    manifest_path = write_json(tmp_path / "manifest-existing.json", payload)

    code, report = run_cli(
        "issue",
        "--manifest", str(manifest_path),
        "--repo-root", str(repo),
        "--candidate-conformance-result", "PASS",
        "--candidate-conformance-reference", "ref",
        "--validator", "validator",
        "--independence-reference", "independent",
        "--evidence-reference", "evidence",
        "--issued-at", "not-a-time",
        "--output", str(tmp_path / "bad-receipt.json"),
    )
    assert code == 1
    assert report["code"] == "INVALID_TIMESTAMP"
    assert not (tmp_path / "bad-receipt.json").exists()

    existing = tmp_path / "existing.json"
    existing.write_text("do-not-overwrite", encoding="utf-8")
    code, report = issue(
        tmp_path, repo, payload,
        extra=["--output", str(existing)],
    )
    assert code == 1
    assert report["code"] == "OUTPUT_EXISTS"
    assert existing.read_text(encoding="utf-8") == "do-not-overwrite"


def test_output_file_is_receipt_and_stdout_is_report(tmp_path):
    repo, baseline, candidate = make_repo(tmp_path)
    payload = manifest(baseline, candidate)
    output = tmp_path / "receipt-out.json"

    code, report = issue(
        tmp_path, repo, payload,
        extra=["--output", str(output)],
    )

    assert code == 0
    assert report["validator_result"] == "PASS"
    assert report["code"] == "ISSUED"
    receipt = json.loads(output.read_text(encoding="utf-8"))
    assert receipt["schema"] == "MALAK-RDD-VALIDATION-RECEIPT/v1"
    assert receipt["authority_effect"] == "none"


def test_output_cannot_overwrite_manifest_input(tmp_path):
    repo, baseline, candidate = make_repo(tmp_path)
    payload = manifest(baseline, candidate)
    manifest_path = write_json(tmp_path / "same.json", payload)

    code, report = run_cli(
        "issue",
        "--manifest", str(manifest_path),
        "--repo-root", str(repo),
        "--candidate-conformance-result", "PASS",
        "--candidate-conformance-reference", "ref",
        "--validator", "validator",
        "--independence-reference", "independent",
        "--evidence-reference", "evidence",
        "--issued-at", "2026-10-10T15:00:00Z",
        "--output", str(manifest_path),
    )

    assert code == 1
    assert report["code"] in {"OUTPUT_OVERWRITES_INPUT", "OUTPUT_EXISTS"}


def test_stdout_issue_does_not_claim_destination_confinement(tmp_path):
    repo, baseline, candidate = make_repo(tmp_path)
    payload = manifest(baseline, candidate)

    code, receipt = issue(tmp_path, repo, payload)

    assert code == 0
    assert receipt["schema"] == "MALAK-RDD-VALIDATION-RECEIPT/v1"
    assert "output_path" not in receipt
    assert receipt["authority_effect"] == "none"
