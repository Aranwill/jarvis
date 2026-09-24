from __future__ import annotations

import dataclasses
import json
import re
from importlib import import_module
from pathlib import Path

import pytest


BASELINE = "74f46a62e05eadd2700a1058d7ab88cf08a83f1d"


def _module():
    return import_module("malak.observability.safe_diagnostic")


def _raise_runtime_error(message: str = "synthetic failure") -> Exception:
    try:
        raise RuntimeError(message)
    except RuntimeError as exc:
        return exc


def _raise_timeout_with_cause() -> Exception:
    try:
        try:
            raise TimeoutError("secret-token=abc123")
        except TimeoutError as cause:
            raise RuntimeError("outer secret payload") from cause
    except RuntimeError as exc:
        return exc


def _raise_from_repo(repo: Path) -> Exception:
    target = repo / "src" / "malak" / "synthetic_component.py"
    target.parent.mkdir(parents=True, exist_ok=True)
    source = (
        "def synthetic_component():\n"
        "    raise TimeoutError('do-not-persist-this-message')\n"
    )
    target.write_text(source, encoding="utf-8")
    namespace: dict[str, object] = {}
    exec(compile(source, str(target), "exec"), namespace)
    try:
        namespace["synthetic_component"]()
    except TimeoutError as exc:
        return exc
    raise AssertionError("synthetic component did not fail")


def _build(
    exc: Exception,
    *,
    repository_root: Path,
    diagnostic_id: str = "D0001",
):
    return _module().build_safe_diagnostic(
        exc=exc,
        repository_root=repository_root,
        diagnostic_id=diagnostic_id,
        run_id="run-001",
        baseline_commit=BASELINE,
        task_id="self-review-v0",
        phase="engineering",
        component="engineering_analyze",
        reason_code="component_error",
    )


def test_safe_diagnostic_red_b01_contract_is_frozen_and_authority_free(
    tmp_path: Path,
) -> None:
    diagnostic = _build(
        _raise_runtime_error(),
        repository_root=tmp_path,
    )

    assert dataclasses.is_dataclass(diagnostic)
    assert diagnostic.schema == "MALAK-SAFE-DIAGNOSTIC/v0"
    assert diagnostic.diagnostic_id == "D0001"
    assert diagnostic.run_id == "run-001"
    assert diagnostic.baseline_commit == BASELINE
    assert diagnostic.component == "engineering_analyze"
    assert diagnostic.reason_code == "component_error"
    assert diagnostic.authority_effect == "none"

    with pytest.raises(dataclasses.FrozenInstanceError):
        diagnostic.reason_code = "validation_failed"


def test_safe_diagnostic_red_b02_reason_code_remains_component_error(
    tmp_path: Path,
) -> None:
    diagnostic = _build(
        _raise_runtime_error("raw failure message"),
        repository_root=tmp_path,
    )

    assert diagnostic.reason_code == "component_error"
    assert diagnostic.exception_type == "RuntimeError"


def test_safe_diagnostic_red_b03_raw_exception_message_is_not_persisted(
    tmp_path: Path,
) -> None:
    secret = "secret-token=abc123"
    diagnostic = _build(
        _raise_runtime_error(secret),
        repository_root=tmp_path,
    )
    serialized = json.dumps(dataclasses.asdict(diagnostic), sort_keys=True)

    assert secret not in serialized
    assert "abc123" not in serialized
    assert diagnostic.safe_summary == "component raised an unexpected exception"


def test_safe_diagnostic_red_b04_raw_traceback_is_not_in_schema(
    tmp_path: Path,
) -> None:
    diagnostic = _build(
        _raise_runtime_error(),
        repository_root=tmp_path,
    )
    payload = dataclasses.asdict(diagnostic)

    forbidden = {
        "traceback",
        "stack",
        "locals",
        "exception_message",
        "exception_args",
        "prompt",
        "response",
        "headers",
        "environment",
    }
    assert not (forbidden & set(payload))


def test_safe_diagnostic_red_b05_absolute_local_paths_are_not_persisted(
    tmp_path: Path,
) -> None:
    diagnostic = _build(
        _raise_from_repo(tmp_path),
        repository_root=tmp_path,
    )
    serialized = json.dumps(dataclasses.asdict(diagnostic), sort_keys=True)

    assert str(tmp_path) not in serialized
    assert "\\" not in diagnostic.repo_relative_file
    assert not diagnostic.repo_relative_file.startswith("/")


def test_safe_diagnostic_red_b06_repo_relative_origin_is_preserved(
    tmp_path: Path,
) -> None:
    diagnostic = _build(
        _raise_from_repo(tmp_path),
        repository_root=tmp_path,
    )

    assert diagnostic.origin_scope == "repository"
    assert diagnostic.repo_relative_file == "src/malak/synthetic_component.py"
    assert diagnostic.function == "synthetic_component"
    assert isinstance(diagnostic.line, int)
    assert diagnostic.line > 0


def test_safe_diagnostic_red_b07_external_origin_does_not_leak_path(
    tmp_path: Path,
) -> None:
    diagnostic = _build(
        _raise_runtime_error(),
        repository_root=tmp_path,
    )

    assert diagnostic.origin_scope == "external"
    assert diagnostic.repo_relative_file is None
    assert diagnostic.line is None


def test_safe_diagnostic_red_b08_cause_chain_preserves_types_only(
    tmp_path: Path,
) -> None:
    diagnostic = _build(
        _raise_timeout_with_cause(),
        repository_root=tmp_path,
    )
    serialized = json.dumps(dataclasses.asdict(diagnostic), sort_keys=True)

    assert diagnostic.cause_chain_types == ("RuntimeError", "TimeoutError")
    assert "secret-token=abc123" not in serialized
    assert "outer secret payload" not in serialized


def test_safe_diagnostic_red_b09_diagnostic_id_is_path_safe_and_closed(
    tmp_path: Path,
) -> None:
    module = _module()

    for invalid in ("../D1", "D/1", "D\\1", "", " D0001", "D0001 "):
        with pytest.raises(ValueError):
            module.build_safe_diagnostic(
                exc=_raise_runtime_error(),
                repository_root=tmp_path,
                diagnostic_id=invalid,
                run_id="run-001",
                baseline_commit=BASELINE,
                task_id="self-review-v0",
                phase="engineering",
                component="engineering_analyze",
                reason_code="component_error",
            )

    diagnostic = _build(
        _raise_runtime_error(),
        repository_root=tmp_path,
        diagnostic_id="D0007",
    )
    assert re.fullmatch(r"D[0-9]{4}", diagnostic.diagnostic_id)


def test_safe_diagnostic_red_b10_fingerprint_is_deterministic_for_safe_inputs(
    tmp_path: Path,
) -> None:
    first = _build(
        _raise_from_repo(tmp_path),
        repository_root=tmp_path,
        diagnostic_id="D0001",
    )
    second = _build(
        _raise_from_repo(tmp_path),
        repository_root=tmp_path,
        diagnostic_id="D0002",
    )

    assert first.diagnostic_fingerprint == second.diagnostic_fingerprint
    assert re.fullmatch(r"[0-9a-f]{64}", first.diagnostic_fingerprint)


def test_safe_diagnostic_red_b11_jsonl_round_trip_is_exact_and_bound(
    tmp_path: Path,
) -> None:
    module = _module()
    diagnostic = _build(
        _raise_from_repo(tmp_path),
        repository_root=tmp_path,
    )
    path = tmp_path / "diagnostics.jsonl"

    module.write_safe_diagnostics_jsonl(path, (diagnostic,))
    loaded = module.read_safe_diagnostics_jsonl(path)

    assert loaded == (diagnostic,)
    assert loaded[0].run_id == "run-001"
    assert loaded[0].baseline_commit == BASELINE
    assert loaded[0].authority_effect == "none"


def test_safe_diagnostic_red_b12_jsonl_rejects_unknown_or_malformed_fields(
    tmp_path: Path,
) -> None:
    module = _module()
    path = tmp_path / "diagnostics.jsonl"
    path.write_text(
        json.dumps(
            {
                "schema": "MALAK-SAFE-DIAGNOSTIC/v0",
                "diagnostic_id": "D0001",
                "unexpected": "field",
            }
        )
        + "\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        module.read_safe_diagnostics_jsonl(path)


def test_safe_diagnostic_red_b13_safe_summary_is_closed_by_exception_type(
    tmp_path: Path,
) -> None:
    timeout = _build(
        TimeoutError("secret timeout URL https://example.invalid/token"),
        repository_root=tmp_path,
    )
    value = _build(
        ValueError("password=hunter2"),
        repository_root=tmp_path,
        diagnostic_id="D0002",
    )

    assert timeout.safe_summary == "operation timed out"
    assert value.safe_summary == "component rejected invalid value"


def test_safe_diagnostic_red_b14_schema_contains_no_prompt_response_or_secret_fields(
    tmp_path: Path,
) -> None:
    diagnostic = _build(
        _raise_timeout_with_cause(),
        repository_root=tmp_path,
    )
    fields = {field.name for field in dataclasses.fields(diagnostic)}

    forbidden = {
        "prompt",
        "response",
        "request_body",
        "headers",
        "token",
        "secret",
        "environment",
        "locals",
        "traceback",
    }
    assert not (fields & forbidden)
