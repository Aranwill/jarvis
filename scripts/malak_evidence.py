#!/usr/bin/env python3
"""Validador read-only para MALAK-EVIDENCE-MANIFEST/v1."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

SCHEMA = "MALAK-EVIDENCE-MANIFEST/v1"
REPOSITORY = "Aranwill/jarvis"
VALIDATOR = "MALAK-EVIDENCE-VALIDATOR/v1"
RESULTS = {"PASS", "FAIL", "INCONCLUSIVE"}
LENSES = {"risk", "readability", "reliability", "resilience"}
SHA_RE = re.compile(r"^[0-9a-f]{40}$")

TOP_KEYS = {
    "schema", "repository", "baseline_commit", "candidate_commit", "unit_id",
    "specification_reference", "gate", "risk_class", "scope_reference",
    "validations", "four_r", "finding_refs", "correction_round", "producer",
    "validator", "result", "generated_at", "evidence_references",
    "authority_effect",
}
VALIDATION_KEYS = {"id", "method", "result", "evidence_reference"}
LENS_KEYS = {"result", "finding_refs", "evidence_reference"}


class CheckError(Exception):
    def __init__(self, code: str, message: str, *, inconclusive: bool = False):
        super().__init__(message)
        self.code = code
        self.message = message
        self.inconclusive = inconclusive


def fail(code: str, message: str) -> None:
    raise CheckError(code, message)


def exact_dict(value: Any, keys: set[str], name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        fail("INVALID_FIELD", f"{name} must be an object")
    actual = set(value)
    if actual != keys:
        fail(
            "INVALID_KEYS",
            f"{name} keys mismatch; missing={sorted(keys-actual)} extra={sorted(actual-keys)}",
        )
    return value


def text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        fail("INVALID_FIELD", f"{name} must be a non-empty string")
    if value != value.strip():
        fail("NON_CANONICAL_TEXT", f"{name} has surrounding whitespace")
    return value


def sha(value: Any, name: str) -> str:
    value = text(value, name)
    if not SHA_RE.fullmatch(value):
        fail("INVALID_COMMIT_SHA", f"{name} must be a lowercase 40-char Git SHA")
    return value


def result(value: Any, name: str) -> str:
    if not isinstance(value, str) or value not in RESULTS:
        fail("INVALID_RESULT", f"{name} must be PASS, FAIL or INCONCLUSIVE")
    return value


def string_list(value: Any, name: str, *, non_empty: bool = False) -> list[str]:
    if not isinstance(value, list) or (non_empty and not value):
        fail("INVALID_FIELD", f"{name} must be {'a non-empty ' if non_empty else 'a '}list")
    for index, item in enumerate(value):
        text(item, f"{name}[{index}]")
    return value


def utc_timestamp(value: Any) -> None:
    value = text(value, "generated_at")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        fail("INVALID_TIMESTAMP", "generated_at must be valid ISO-8601")
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        fail("INVALID_TIMESTAMP", "generated_at must be timezone-aware")
    if parsed.utcoffset() != UTC.utcoffset(parsed):
        fail("INVALID_TIMESTAMP", "generated_at must use UTC")


def validate_structure(payload: Any) -> dict[str, str]:
    data = exact_dict(payload, TOP_KEYS, "manifest")

    if data["schema"] != SCHEMA:
        fail("INVALID_SCHEMA", f"schema must equal {SCHEMA}")
    if data["repository"] != REPOSITORY:
        fail("INVALID_REPOSITORY", f"repository must equal {REPOSITORY}")

    baseline = sha(data["baseline_commit"], "baseline_commit")
    candidate = sha(data["candidate_commit"], "candidate_commit")

    for name in (
        "unit_id", "specification_reference", "gate", "scope_reference",
        "producer", "validator",
    ):
        text(data[name], name)

    risk = data["risk_class"]
    if isinstance(risk, bool) or not isinstance(risk, int) or not 0 <= risk <= 4:
        fail("INVALID_RISK_CLASS", "risk_class must be an integer from 0 to 4")

    round_ = data["correction_round"]
    if isinstance(round_, bool) or not isinstance(round_, int) or round_ < 0:
        fail("INVALID_CORRECTION_ROUND", "correction_round must be >= 0")

    validations = data["validations"]
    if not isinstance(validations, list) or not validations:
        fail("INVALID_VALIDATIONS", "validations must be a non-empty list")

    seen: set[str] = set()
    observed: list[str] = []
    for index, raw in enumerate(validations):
        item = exact_dict(raw, VALIDATION_KEYS, f"validations[{index}]")
        item_id = text(item["id"], f"validations[{index}].id")
        if item_id in seen:
            fail("DUPLICATE_VALIDATION_ID", f"duplicate validation id: {item_id}")
        seen.add(item_id)
        text(item["method"], f"validations[{index}].method")
        observed.append(result(item["result"], f"validations[{index}].result"))
        text(item["evidence_reference"], f"validations[{index}].evidence_reference")

    four_r = data["four_r"]
    if not isinstance(four_r, dict):
        fail("INVALID_FOUR_R", "four_r must be an object")
    if set(four_r) - LENSES:
        fail("INVALID_FOUR_R_LENS", f"unknown lenses: {sorted(set(four_r)-LENSES)}")
    if risk in (1, 2) and not four_r:
        fail("FOUR_R_INCOMPLETE", f"risk_class {risk} requires at least one 4R lens")
    if risk in (3, 4) and set(four_r) != LENSES:
        fail("FOUR_R_INCOMPLETE", f"risk_class {risk} requires FULL 4R")

    for lens_name in sorted(four_r):
        lens = exact_dict(four_r[lens_name], LENS_KEYS, f"four_r.{lens_name}")
        observed.append(result(lens["result"], f"four_r.{lens_name}.result"))
        string_list(lens["finding_refs"], f"four_r.{lens_name}.finding_refs")
        text(lens["evidence_reference"], f"four_r.{lens_name}.evidence_reference")

    string_list(data["finding_refs"], "finding_refs")
    string_list(data["evidence_references"], "evidence_references", non_empty=True)
    utc_timestamp(data["generated_at"])

    if data["authority_effect"] != "none":
        fail("AUTHORITY_EFFECT_INVALID", "authority_effect must equal 'none'")

    top = result(data["result"], "result")
    expected = "FAIL" if "FAIL" in observed else (
        "INCONCLUSIVE" if "INCONCLUSIVE" in observed else "PASS"
    )
    if top != expected:
        fail("RESULT_AGGREGATION_MISMATCH", f"result={top}; evidence aggregates to {expected}")

    return {"baseline_commit": baseline, "candidate_commit": candidate, "result": top}


def git(repo: Path, *args: str, object_missing_is_fail: bool = False) -> str:
    try:
        done = subprocess.run(
            ["git", "-C", str(repo), *args],
            capture_output=True, text=True, timeout=15, check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CheckError("GIT_UNAVAILABLE", "Git inspection unavailable", inconclusive=True) from exc
    if done.returncode:
        message = done.stderr.strip() or done.stdout.strip() or "Git command failed"
        if object_missing_is_fail:
            raise CheckError("GIT_OBJECT_NOT_FOUND", message)
        raise CheckError("GIT_COMMAND_FAILED", message, inconclusive=True)
    return done.stdout.strip()


def require_ancestor(repo: Path, baseline: str, candidate: str) -> None:
    try:
        done = subprocess.run(
            ["git", "-C", str(repo), "merge-base", "--is-ancestor", baseline, candidate],
            capture_output=True, text=True, timeout=15, check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CheckError("GIT_UNAVAILABLE", "Git inspection unavailable", inconclusive=True) from exc
    if done.returncode == 1:
        raise CheckError(
            "BASELINE_NOT_ANCESTOR",
            f"baseline {baseline} is not an ancestor of candidate {candidate}",
        )
    if done.returncode != 0:
        message = done.stderr.strip() or done.stdout.strip() or "Git ancestry check failed"
        raise CheckError("GIT_COMMAND_FAILED", message, inconclusive=True)


def validate_git(
    repo: Path,
    manifest: dict[str, str],
    *,
    expected_candidate: str | None,
    require_current: bool,
) -> str | None:
    git(repo, "rev-parse", "--show-toplevel")
    for name in ("baseline_commit", "candidate_commit"):
        git(repo, "cat-file", "-e", f"{manifest[name]}^{{commit}}", object_missing_is_fail=True)
    require_ancestor(repo, manifest["baseline_commit"], manifest["candidate_commit"])

    expected = None
    if expected_candidate is not None:
        expected = sha(expected_candidate, "expected_candidate")
        git(repo, "cat-file", "-e", f"{expected}^{{commit}}", object_missing_is_fail=True)

    if require_current:
        expected = git(repo, "rev-parse", "HEAD")
        if git(repo, "status", "--porcelain"):
            raise CheckError("DIRTY_WORKTREE", "current worktree differs from committed HEAD")

    if expected is not None and manifest["candidate_commit"] != expected:
        raise CheckError(
            "STALE_CANDIDATE",
            f"candidate {manifest['candidate_commit']} != expected {expected}",
        )
    return expected


def load(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail("MANIFEST_NOT_FOUND", f"manifest not found: {path}")
    except json.JSONDecodeError as exc:
        fail("INVALID_JSON", f"invalid JSON: {exc.msg}")
    except (OSError, UnicodeError):
        fail("MANIFEST_READ_FAILED", f"manifest could not be read: {path}")


def report(
    status: str, code: str, message: str, *,
    manifest_result: str | None = None,
    candidate_commit: str | None = None,
    expected_candidate: str | None = None,
) -> str:
    return json.dumps(
        {
            "validator": VALIDATOR,
            "status": status,
            "code": code,
            "message": message,
            "manifest_result": manifest_result,
            "candidate_commit": candidate_commit,
            "expected_candidate": expected_candidate,
            "authority_effect": "none",
        },
        ensure_ascii=False,
        sort_keys=True,
    )


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Validate MALAK-EVIDENCE-MANIFEST/v1 read-only.")
    p.add_argument("manifest", type=Path)
    p.add_argument("--repo-root", type=Path, default=Path("."))
    binding = p.add_mutually_exclusive_group()
    binding.add_argument("--expected-candidate")
    binding.add_argument("--require-current", action="store_true")
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    manifest: dict[str, str] | None = None
    expected: str | None = None
    try:
        manifest = validate_structure(load(args.manifest))
        expected = validate_git(
            args.repo_root, manifest,
            expected_candidate=args.expected_candidate,
            require_current=args.require_current,
        )
    except CheckError as exc:
        status = "INCONCLUSIVE" if exc.inconclusive else "FAIL"
        print(report(
            status,
            exc.code,
            exc.message,
            manifest_result=manifest["result"] if manifest else None,
            candidate_commit=manifest["candidate_commit"] if manifest else None,
            expected_candidate=expected,
        ))
        return 2 if exc.inconclusive else 1

    print(report(
        "PASS", "VALID", "manifest and requested candidate binding are valid",
        manifest_result=manifest["result"],
        candidate_commit=manifest["candidate_commit"],
        expected_candidate=expected,
    ))
    return 0


if __name__ == "__main__":
    sys.exit(main())
