from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "malak_evidence.py"


def git(repo: Path, *args: str) -> str:
    done = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return done.stdout.strip()


def make_repo(tmp_path: Path) -> tuple[Path, str]:
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init")
    git(repo, "config", "user.email", "test@example.com")
    git(repo, "config", "user.name", "Malak Test")
    git(repo, "config", "commit.gpgsign", "false")
    (repo / "file.txt").write_text("baseline\n", encoding="utf-8")
    git(repo, "add", "file.txt")
    git(repo, "commit", "--no-gpg-sign", "-m", "baseline")
    return repo, git(repo, "rev-parse", "HEAD")


def manifest(commit: str) -> dict:
    lens = {
        "result": "PASS",
        "finding_refs": [],
        "evidence_reference": "test-evidence",
    }
    return {
        "schema": "MALAK-EVIDENCE-MANIFEST/v1",
        "repository": "Aranwill/jarvis",
        "baseline_commit": commit,
        "candidate_commit": commit,
        "unit_id": "RDD-M1",
        "specification_reference": "spec.md",
        "gate": "G5",
        "risk_class": 3,
        "scope_reference": "scope.md",
        "validations": [
            {
                "id": "pytest",
                "method": "python -m pytest",
                "result": "PASS",
                "evidence_reference": "test-evidence",
            }
        ],
        "four_r": {
            "risk": copy.deepcopy(lens),
            "readability": copy.deepcopy(lens),
            "reliability": copy.deepcopy(lens),
            "resilience": copy.deepcopy(lens),
        },
        "finding_refs": [],
        "correction_round": 0,
        "producer": "writer",
        "validator": "validator",
        "result": "PASS",
        "generated_at": "2026-09-08T18:00:00+00:00",
        "evidence_references": ["test-evidence"],
        "authority_effect": "none",
    }


def run_validator(repo: Path, payload: dict, *args: str):
    # El manifest activo queda fuera del candidate worktree. De este modo
    # --require-current puede demostrar que HEAD representa exactamente el
    # contenido evaluado sin exceptuar artefactos de evidencia.
    path = repo.parent / "manifest.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    done = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            str(path),
            "--repo-root",
            str(repo),
            *args,
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    return done.returncode, json.loads(done.stdout)


def second_commit(repo: Path) -> str:
    (repo / "file.txt").write_text("second\n", encoding="utf-8")
    git(repo, "add", "file.txt")
    git(repo, "commit", "--no-gpg-sign", "-m", "second")
    return git(repo, "rev-parse", "HEAD")


def test_valid_manifest_passes(tmp_path):
    repo, commit = make_repo(tmp_path)
    code, output = run_validator(repo, manifest(commit))

    assert code == 0
    assert output["status"] == "PASS"
    assert output["code"] == "VALID"
    assert output["candidate_commit"] == commit
    assert output["authority_effect"] == "none"


def test_authority_effect_cannot_change(tmp_path):
    repo, commit = make_repo(tmp_path)
    payload = manifest(commit)
    payload["authority_effect"] = "approved"

    code, output = run_validator(repo, payload)

    assert code == 1
    assert output["code"] == "AUTHORITY_EFFECT_INVALID"


def test_authority_or_delivery_field_cannot_be_added(tmp_path):
    repo, commit = make_repo(tmp_path)
    payload = manifest(commit)
    payload["approved"] = True

    code, output = run_validator(repo, payload)

    assert code == 1
    assert output["code"] == "INVALID_KEYS"


def test_result_cannot_hide_failed_validation(tmp_path):
    repo, commit = make_repo(tmp_path)
    payload = manifest(commit)
    payload["validations"][0]["result"] = "FAIL"

    code, output = run_validator(repo, payload)

    assert code == 1
    assert output["code"] == "RESULT_AGGREGATION_MISMATCH"


def test_inconclusive_evidence_cannot_be_promoted_to_pass(tmp_path):
    repo, commit = make_repo(tmp_path)
    payload = manifest(commit)
    payload["four_r"]["risk"]["result"] = "INCONCLUSIVE"

    code, output = run_validator(repo, payload)

    assert code == 1
    assert output["code"] == "RESULT_AGGREGATION_MISMATCH"


def test_high_risk_requires_full_4r(tmp_path):
    repo, commit = make_repo(tmp_path)
    payload = manifest(commit)
    del payload["four_r"]["resilience"]

    code, output = run_validator(repo, payload)

    assert code == 1
    assert output["code"] == "FOUR_R_INCOMPLETE"


def test_invalid_sha_is_rejected(tmp_path):
    repo, commit = make_repo(tmp_path)
    payload = manifest(commit)
    payload["candidate_commit"] = "abc"

    code, output = run_validator(repo, payload)

    assert code == 1
    assert output["code"] == "INVALID_COMMIT_SHA"


def test_non_utc_timestamp_is_rejected(tmp_path):
    repo, commit = make_repo(tmp_path)
    payload = manifest(commit)
    payload["generated_at"] = "2026-09-08T15:00:00-03:00"

    code, output = run_validator(repo, payload)

    assert code == 1
    assert output["code"] == "INVALID_TIMESTAMP"


def test_require_current_passes_for_clean_current_candidate(tmp_path):
    repo, commit = make_repo(tmp_path)

    code, output = run_validator(repo, manifest(commit), "--require-current")

    assert code == 0
    assert output["expected_candidate"] == commit


def test_require_current_detects_stale_candidate(tmp_path):
    repo, first = make_repo(tmp_path)
    payload = manifest(first)
    second_commit(repo)

    code, output = run_validator(repo, payload, "--require-current")

    assert code == 1
    assert output["code"] == "STALE_CANDIDATE"
    assert output["candidate_commit"] == first


def test_require_current_rejects_dirty_worktree(tmp_path):
    repo, commit = make_repo(tmp_path)
    payload = manifest(commit)
    (repo / "file.txt").write_text("dirty\n", encoding="utf-8")

    code, output = run_validator(repo, payload, "--require-current")

    assert code == 1
    assert output["code"] == "DIRTY_WORKTREE"


def test_expected_candidate_detects_mismatch(tmp_path):
    repo, first = make_repo(tmp_path)
    payload = manifest(first)
    second = second_commit(repo)

    code, output = run_validator(
        repo,
        payload,
        "--expected-candidate",
        second,
    )

    assert code == 1
    assert output["code"] == "STALE_CANDIDATE"


def test_unknown_commit_is_fail_closed(tmp_path):
    repo, commit = make_repo(tmp_path)
    payload = manifest(commit)
    payload["candidate_commit"] = "f" * 40

    code, output = run_validator(repo, payload)

    assert code == 1
    assert output["code"] == "GIT_OBJECT_NOT_FOUND"
