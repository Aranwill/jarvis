#!/usr/bin/env python3
"""Emisor y validador de MALAK-RDD-VALIDATION-RECEIPT/v1."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any

import malak_evidence as stage1

SCHEMA = "MALAK-RDD-VALIDATION-RECEIPT/v1"
VALIDATOR = "MALAK-RDD-RECEIPT-VALIDATOR/v1"
REPOSITORY = "Aranwill/jarvis"
RESULTS = {"PASS", "FAIL", "INCONCLUSIVE"}
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
DIGEST_RE = re.compile(r"^[0-9a-f]{64}$")
UTC_Z_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")

RECEIPT_KEYS = {
    "schema",
    "repository",
    "baseline_commit",
    "candidate_commit",
    "candidate_tree",
    "unit_id",
    "risk_class",
    "specification_reference",
    "scope_reference",
    "stage1_manifest_schema",
    "stage1_manifest_digest",
    "stage1_manifest_result",
    "candidate_conformance_result",
    "candidate_conformance_reference",
    "correction_round",
    "finding_refs",
    "validator",
    "independence_reference",
    "evidence_references",
    "issued_at",
    "receipt_digest",
    "authority_effect",
}

MANIFEST_BOUND_FIELDS = {
    "repository": "repository",
    "baseline_commit": "baseline_commit",
    "candidate_commit": "candidate_commit",
    "unit_id": "unit_id",
    "risk_class": "risk_class",
    "specification_reference": "specification_reference",
    "scope_reference": "scope_reference",
    "correction_round": "correction_round",
    "finding_refs": "finding_refs",
    "stage1_manifest_schema": "schema",
    "stage1_manifest_result": "result",
}


class CheckError(Exception):
    def __init__(self, code: str, message: str, *, inconclusive: bool = False):
        super().__init__(message)
        self.code = code
        self.message = message
        self.inconclusive = inconclusive


def fail(code: str, message: str) -> None:
    raise CheckError(code, message)


def non_standard_constant(value: str) -> None:
    raise CheckError("NON_STANDARD_JSON_NUMBER", f"non-standard JSON number: {value}")


def no_duplicate_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise CheckError("DUPLICATE_KEY", f"duplicate JSON object key: {key}")
        result[key] = value
    return result


def strict_load(path: Path) -> Any:
    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        fail("INPUT_NOT_FOUND", f"input not found: {path}")
    except (OSError, UnicodeError):
        fail("INPUT_READ_FAILED", f"input could not be read: {path}")

    try:
        return json.loads(
            raw,
            object_pairs_hook=no_duplicate_object,
            parse_constant=non_standard_constant,
        )
    except CheckError:
        raise
    except json.JSONDecodeError as exc:
        fail("INVALID_JSON", f"invalid JSON: {exc.msg}")
    except ValueError as exc:
        fail("INVALID_JSON", f"invalid JSON value: {exc}")


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
    if not isinstance(value, str) or not value.strip() or value != value.strip():
        fail("INVALID_FIELD", f"{name} must be a non-empty canonical string")
    return value


def sha(value: Any, name: str) -> str:
    value = text(value, name)
    if not SHA_RE.fullmatch(value):
        fail("INVALID_COMMIT_SHA", f"{name} must be a lowercase 40-char Git SHA")
    return value


def digest(value: Any, name: str) -> str:
    value = text(value, name)
    if not DIGEST_RE.fullmatch(value):
        fail("INVALID_DIGEST", f"{name} must be a lowercase 64-char SHA-256")
    return value


def result(value: Any, name: str) -> str:
    if not isinstance(value, str) or value not in RESULTS:
        fail("INVALID_RESULT", f"{name} must be PASS, FAIL or INCONCLUSIVE")
    return value


def integer(value: Any, name: str, *, minimum: int, maximum: int | None = None) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        fail("INVALID_FIELD", f"{name} must be an integer")
    if value < minimum or (maximum is not None and value > maximum):
        fail("INVALID_FIELD", f"{name} is outside the permitted range")
    return value


def string_list(
    value: Any,
    name: str,
    *,
    non_empty: bool = False,
    unique: bool = False,
) -> list[str]:
    if not isinstance(value, list) or (non_empty and not value):
        fail("INVALID_FIELD", f"{name} must be {'a non-empty ' if non_empty else 'a '}list")
    checked = [text(item, f"{name}[{index}]") for index, item in enumerate(value)]
    if unique and len(checked) != len(set(checked)):
        fail("INVALID_FIELD", f"{name} must not contain duplicates")
    return checked


def receipt_timestamp(value: Any) -> str:
    value = text(value, "issued_at")
    if not UTC_Z_RE.fullmatch(value):
        fail("INVALID_TIMESTAMP", "issued_at must use canonical UTC YYYY-MM-DDTHH:MM:SSZ")
    try:
        datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        fail("INVALID_TIMESTAMP", "issued_at must be a valid UTC timestamp")
    return value


def canonical_bytes(payload: Any) -> bytes:
    try:
        value = json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
        return value.encode("utf-8")
    except (TypeError, ValueError, UnicodeError) as exc:
        raise CheckError("INVALID_FIELD", "payload is not canonically serializable as UTF-8") from exc


def sha256_payload(payload: Any) -> str:
    return hashlib.sha256(canonical_bytes(payload)).hexdigest()


def validate_receipt_structure(payload: Any) -> dict[str, Any]:
    data = exact_dict(payload, RECEIPT_KEYS, "receipt")

    if data["schema"] != SCHEMA:
        fail("INVALID_SCHEMA", f"schema must equal {SCHEMA}")
    if data["repository"] != REPOSITORY:
        fail("INVALID_REPOSITORY", f"repository must equal {REPOSITORY}")

    sha(data["baseline_commit"], "baseline_commit")
    sha(data["candidate_commit"], "candidate_commit")
    sha(data["candidate_tree"], "candidate_tree")

    for name in (
        "unit_id",
        "specification_reference",
        "scope_reference",
        "candidate_conformance_reference",
        "validator",
        "independence_reference",
    ):
        text(data[name], name)

    integer(data["risk_class"], "risk_class", minimum=0, maximum=4)
    integer(data["correction_round"], "correction_round", minimum=0)

    if data["stage1_manifest_schema"] != stage1.SCHEMA:
        fail("INVALID_SCHEMA", f"stage1_manifest_schema must equal {stage1.SCHEMA}")
    digest(data["stage1_manifest_digest"], "stage1_manifest_digest")
    result(data["stage1_manifest_result"], "stage1_manifest_result")
    result(data["candidate_conformance_result"], "candidate_conformance_result")

    string_list(data["finding_refs"], "finding_refs")
    string_list(
        data["evidence_references"],
        "evidence_references",
        non_empty=True,
        unique=True,
    )
    receipt_timestamp(data["issued_at"])
    digest(data["receipt_digest"], "receipt_digest")

    if data["authority_effect"] != "none":
        fail("AUTHORITY_EFFECT_INVALID", "authority_effect must equal 'none'")

    return data


def translate_stage1_error(exc: stage1.CheckError) -> CheckError:
    return CheckError(exc.code, exc.message, inconclusive=exc.inconclusive)


def validate_manifest(payload: Any) -> tuple[dict[str, Any], dict[str, str]]:
    try:
        checked = stage1.validate_structure(payload)
    except stage1.CheckError as exc:
        raise translate_stage1_error(exc) from exc
    return payload, checked


def validate_manifest_git(
    repo: Path,
    checked: dict[str, str],
    *,
    expected_candidate: str | None,
    require_current: bool,
) -> tuple[str | None, Path]:
    try:
        expected = stage1.validate_git(
            repo,
            checked,
            expected_candidate=expected_candidate,
            require_current=require_current,
        )
        root_text = stage1.git(repo, "rev-parse", "--show-toplevel")
    except stage1.CheckError as exc:
        raise translate_stage1_error(exc) from exc

    try:
        effective_root = Path(root_text).resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise CheckError(
            "GIT_ROOT_UNRESOLVED",
            "effective Git repository root could not be resolved safely",
            inconclusive=True,
        ) from exc
    return expected, effective_root


def candidate_tree(repo: Path, candidate: str) -> str:
    try:
        return stage1.git(
            repo,
            "rev-parse",
            f"{candidate}^{{tree}}",
            object_missing_is_fail=True,
        )
    except stage1.CheckError as exc:
        raise translate_stage1_error(exc) from exc


def validate_cross_binding(receipt: dict[str, Any], manifest: dict[str, Any]) -> None:
    for receipt_field, manifest_field in MANIFEST_BOUND_FIELDS.items():
        if receipt[receipt_field] != manifest[manifest_field]:
            fail(
                "MANIFEST_RECEIPT_MISMATCH",
                f"{receipt_field} does not match manifest.{manifest_field}",
            )


def validate_manifest_digest(receipt: dict[str, Any], manifest: dict[str, Any]) -> None:
    expected = sha256_payload(manifest)
    if receipt["stage1_manifest_digest"] != expected:
        fail("DIGEST_MISMATCH", "stage1_manifest_digest does not match manifest")


def validate_receipt_digest(receipt: dict[str, Any]) -> None:
    content = dict(receipt)
    supplied = content.pop("receipt_digest")
    expected = sha256_payload(content)
    if supplied != expected:
        fail("DIGEST_MISMATCH", "receipt_digest does not match receipt content")


def validate_tree(repo: Path, receipt: dict[str, Any]) -> None:
    expected = candidate_tree(repo, receipt["candidate_commit"])
    if receipt["candidate_tree"] != expected:
        fail("CANDIDATE_TREE_MISMATCH", "candidate_tree does not match candidate commit")


def output_target(output: Path, repo_root: Path, inputs: list[Path]) -> Path:
    try:
        root = repo_root.resolve(strict=True)
        target = output.resolve(strict=False)
        resolved_inputs = {path.resolve(strict=False) for path in inputs}
    except (OSError, RuntimeError):
        fail("OUTPUT_PATH_UNRESOLVED", "output path could not be resolved safely")

    if target == root or root in target.parents:
        fail("OUTPUT_INSIDE_REPOSITORY", "output must be outside repository root")
    if target in resolved_inputs:
        fail("OUTPUT_OVERWRITES_INPUT", "output must not overwrite an input")
    if target.exists():
        fail("OUTPUT_EXISTS", "output already exists")
    if not target.parent.exists() or not target.parent.is_dir():
        fail("OUTPUT_PARENT_MISSING", "output parent directory must already exist")
    return target


def write_atomic_json(target: Path, payload: dict[str, Any]) -> None:
    temp_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=target.parent,
            prefix=f".{target.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temp_name = handle.name
            json.dump(payload, handle, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, target)
        temp_name = None
    except OSError as exc:
        raise CheckError("OUTPUT_WRITE_FAILED", "receipt output could not be published") from exc
    finally:
        if temp_name is not None:
            try:
                Path(temp_name).unlink(missing_ok=True)
            except OSError:
                pass


def build_receipt(
    manifest: dict[str, Any],
    repo: Path,
    *,
    candidate_conformance_result: str,
    candidate_conformance_reference: str,
    validator: str,
    independence_reference: str,
    evidence_references: list[str],
    issued_at: str,
) -> dict[str, Any]:
    conformance = result(candidate_conformance_result, "candidate_conformance_result")
    conformance_ref = text(candidate_conformance_reference, "candidate_conformance_reference")
    validator_value = text(validator, "validator")
    independence = text(independence_reference, "independence_reference")
    refs = string_list(
        evidence_references,
        "evidence_references",
        non_empty=True,
        unique=True,
    )
    timestamp = receipt_timestamp(issued_at)

    receipt: dict[str, Any] = {
        "schema": SCHEMA,
        "repository": manifest["repository"],
        "baseline_commit": manifest["baseline_commit"],
        "candidate_commit": manifest["candidate_commit"],
        "candidate_tree": candidate_tree(repo, manifest["candidate_commit"]),
        "unit_id": manifest["unit_id"],
        "risk_class": manifest["risk_class"],
        "specification_reference": manifest["specification_reference"],
        "scope_reference": manifest["scope_reference"],
        "stage1_manifest_schema": manifest["schema"],
        "stage1_manifest_digest": sha256_payload(manifest),
        "stage1_manifest_result": manifest["result"],
        "candidate_conformance_result": conformance,
        "candidate_conformance_reference": conformance_ref,
        "correction_round": manifest["correction_round"],
        "finding_refs": list(manifest["finding_refs"]),
        "validator": validator_value,
        "independence_reference": independence,
        "evidence_references": refs,
        "issued_at": timestamp,
        "authority_effect": "none",
    }
    receipt["receipt_digest"] = sha256_payload(receipt)
    validate_receipt_structure(receipt)
    return receipt


def report(
    validator_result: str,
    code: str,
    message: str,
    *,
    candidate_commit: str | None = None,
    candidate_conformance_result: str | None = None,
) -> str:
    return json.dumps(
        {
            "validator": VALIDATOR,
            "validator_result": validator_result,
            "code": code,
            "message": message,
            "candidate_commit": candidate_commit,
            "candidate_conformance_result": candidate_conformance_result,
            "authority_effect": "none",
        },
        ensure_ascii=False,
        sort_keys=True,
    )


def binding_args(parser: argparse.ArgumentParser) -> None:
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--expected-candidate")
    group.add_argument("--require-current", action="store_true")


def parser() -> argparse.ArgumentParser:
    top = argparse.ArgumentParser(
        description="Issue or validate MALAK-RDD-VALIDATION-RECEIPT/v1."
    )
    commands = top.add_subparsers(dest="command", required=True)

    issue = commands.add_parser("issue", help="Issue a candidate-bound validation Receipt.")
    issue.add_argument("--manifest", type=Path, required=True)
    issue.add_argument("--repo-root", type=Path, default=Path("."))
    issue.add_argument("--candidate-conformance-result", required=True)
    issue.add_argument("--candidate-conformance-reference", required=True)
    issue.add_argument("--validator", required=True)
    issue.add_argument("--independence-reference", required=True)
    issue.add_argument("--evidence-reference", action="append", required=True)
    issue.add_argument("--issued-at", required=True)
    issue.add_argument("--output", type=Path)
    binding_args(issue)

    validate = commands.add_parser("validate", help="Validate an existing Receipt.")
    validate.add_argument("--receipt", type=Path, required=True)
    validate.add_argument("--manifest", type=Path, required=True)
    validate.add_argument("--repo-root", type=Path, default=Path("."))
    binding_args(validate)

    return top


def run_issue(args: argparse.Namespace) -> int:
    manifest_payload = strict_load(args.manifest)
    manifest, checked = validate_manifest(manifest_payload)
    _, effective_root = validate_manifest_git(
        args.repo_root,
        checked,
        expected_candidate=args.expected_candidate,
        require_current=args.require_current,
    )
    receipt = build_receipt(
        manifest,
        effective_root,
        candidate_conformance_result=args.candidate_conformance_result,
        candidate_conformance_reference=args.candidate_conformance_reference,
        validator=args.validator,
        independence_reference=args.independence_reference,
        evidence_references=args.evidence_reference,
        issued_at=args.issued_at,
    )

    if args.output is None:
        print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))
        return 0

    target = output_target(args.output, effective_root, [args.manifest])
    write_atomic_json(target, receipt)
    print(report(
        "PASS",
        "ISSUED",
        "receipt issued outside repository root",
        candidate_commit=receipt["candidate_commit"],
        candidate_conformance_result=receipt["candidate_conformance_result"],
    ))
    return 0


def run_validate(args: argparse.Namespace) -> int:
    receipt = validate_receipt_structure(strict_load(args.receipt))
    manifest_payload = strict_load(args.manifest)
    manifest, checked = validate_manifest(manifest_payload)

    validate_cross_binding(receipt, manifest)
    _, effective_root = validate_manifest_git(
        args.repo_root,
        checked,
        expected_candidate=args.expected_candidate,
        require_current=args.require_current,
    )
    validate_tree(effective_root, receipt)
    validate_manifest_digest(receipt, manifest)
    validate_receipt_digest(receipt)

    print(report(
        "PASS",
        "VALID",
        "receipt structure, manifest binding and candidate applicability are valid",
        candidate_commit=receipt["candidate_commit"],
        candidate_conformance_result=receipt["candidate_conformance_result"],
    ))
    return 0


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "issue":
            return run_issue(args)
        return run_validate(args)
    except CheckError as exc:
        validator_result = "INCONCLUSIVE" if exc.inconclusive else "FAIL"
        print(report(validator_result, exc.code, exc.message))
        return 2 if exc.inconclusive else 1


if __name__ == "__main__":
    sys.exit(main())
