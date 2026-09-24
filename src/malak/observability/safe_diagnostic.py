from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from types import TracebackType
from typing import Final, Iterable


SAFE_DIAGNOSTIC_SCHEMA: Final[str] = "MALAK-SAFE-DIAGNOSTIC/v0"
_DIAGNOSTIC_ID_RE: Final[re.Pattern[str]] = re.compile(r"^D[0-9]{4}$")
_SHA_RE: Final[re.Pattern[str]] = re.compile(r"^[0-9a-f]{40}$")
_IDENTIFIER_RE: Final[re.Pattern[str]] = re.compile(
    r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$"
)
_TYPE_RE: Final[re.Pattern[str]] = re.compile(
    r"^[A-Za-z_][A-Za-z0-9_.]{0,127}$"
)
_FINGERPRINT_RE: Final[re.Pattern[str]] = re.compile(r"^[0-9a-f]{64}$")
_SAFE_SUMMARIES: Final[dict[type[BaseException], str]] = {
    TimeoutError: "operation timed out",
    ValueError: "component rejected invalid value",
    ConnectionError: "runtime dependency request failed",
    OSError: "runtime dependency operation failed",
}


@dataclass(frozen=True, slots=True)
class SafeDiagnosticEnvelope:
    schema: str
    diagnostic_id: str
    diagnostic_fingerprint: str
    run_id: str
    baseline_commit: str
    task_id: str
    phase: str
    component: str
    reason_code: str
    exception_type: str
    cause_chain_types: tuple[str, ...]
    safe_summary: str
    origin_scope: str
    repo_relative_file: str | None
    function: str | None
    line: int | None
    authority_effect: str = "none"

    def __post_init__(self) -> None:
        if self.schema != SAFE_DIAGNOSTIC_SCHEMA:
            raise ValueError("diagnostic schema mismatch")
        if not _DIAGNOSTIC_ID_RE.fullmatch(self.diagnostic_id):
            raise ValueError("diagnostic_id must match D0001-style format")
        if not _FINGERPRINT_RE.fullmatch(self.diagnostic_fingerprint):
            raise ValueError("diagnostic_fingerprint must be sha256 hex")
        for name in ("run_id", "task_id", "phase", "component"):
            _validate_identifier(name, getattr(self, name))
        if not _SHA_RE.fullmatch(self.baseline_commit):
            raise ValueError(
                "baseline_commit must be a lowercase 40-character Git SHA"
            )
        if self.reason_code != "component_error":
            raise ValueError(
                "safe diagnostic reason_code must remain component_error"
            )
        if not _TYPE_RE.fullmatch(self.exception_type):
            raise ValueError("exception_type is invalid")
        if not self.cause_chain_types:
            raise ValueError("cause_chain_types must not be empty")
        for item in self.cause_chain_types:
            if not _TYPE_RE.fullmatch(item):
                raise ValueError("cause_chain_types contains invalid type")
        _validate_safe_text("safe_summary", self.safe_summary)
        if self.origin_scope not in {"repository", "external"}:
            raise ValueError("origin_scope must be repository or external")
        if self.origin_scope == "repository":
            if self.repo_relative_file is None:
                raise ValueError(
                    "repository diagnostic requires repo_relative_file"
                )
            _validate_repo_relative_path(self.repo_relative_file)
            if self.function is None:
                raise ValueError("repository diagnostic requires function")
            _validate_safe_text("function", self.function)
            if type(self.line) is not int or self.line <= 0:
                raise ValueError(
                    "repository diagnostic requires positive line"
                )
        else:
            if self.repo_relative_file is not None or self.line is not None:
                raise ValueError(
                    "external diagnostic must not expose local file or line"
                )
            if self.function is not None:
                _validate_safe_text("function", self.function)
        if self.authority_effect != "none":
            raise ValueError("diagnostic authority_effect must remain none")


def build_safe_diagnostic(
    *,
    exc: Exception,
    repository_root: str | Path,
    diagnostic_id: str,
    run_id: str,
    baseline_commit: str,
    task_id: str,
    phase: str,
    component: str,
    reason_code: str,
) -> SafeDiagnosticEnvelope:
    if not isinstance(exc, Exception):
        raise TypeError("exc must be an Exception")

    root = Path(repository_root).expanduser().resolve()
    if not root.is_dir():
        raise ValueError("repository_root must be an existing directory")

    exception_type = type(exc).__name__
    cause_chain_types = _cause_chain_types(exc)
    safe_summary = _safe_summary(exc)
    origin_scope, repo_relative_file, function, line = _safe_origin(
        exc.__traceback__,
        root,
    )

    fingerprint_payload = {
        "component": component,
        "reason_code": reason_code,
        "exception_type": exception_type,
        "cause_chain_types": list(cause_chain_types),
        "origin_scope": origin_scope,
        "repo_relative_file": repo_relative_file,
        "function": function,
    }
    canonical = json.dumps(
        fingerprint_payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    fingerprint = hashlib.sha256(canonical).hexdigest()

    return SafeDiagnosticEnvelope(
        schema=SAFE_DIAGNOSTIC_SCHEMA,
        diagnostic_id=diagnostic_id,
        diagnostic_fingerprint=fingerprint,
        run_id=run_id,
        baseline_commit=baseline_commit,
        task_id=task_id,
        phase=phase,
        component=component,
        reason_code=reason_code,
        exception_type=exception_type,
        cause_chain_types=cause_chain_types,
        safe_summary=safe_summary,
        origin_scope=origin_scope,
        repo_relative_file=repo_relative_file,
        function=function,
        line=line,
        authority_effect="none",
    )


def write_safe_diagnostics_jsonl(
    path: str | Path,
    diagnostics: Iterable[SafeDiagnosticEnvelope],
) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)

    lines: list[str] = []
    seen_ids: set[str] = set()
    for diagnostic in diagnostics:
        if not isinstance(diagnostic, SafeDiagnosticEnvelope):
            raise TypeError(
                "diagnostics must contain SafeDiagnosticEnvelope values"
            )
        if diagnostic.diagnostic_id in seen_ids:
            raise ValueError("duplicate diagnostic_id")
        seen_ids.add(diagnostic.diagnostic_id)

        payload = asdict(diagnostic)
        payload["cause_chain_types"] = list(
            diagnostic.cause_chain_types
        )
        lines.append(
            json.dumps(
                payload,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            )
        )

    target.write_text(
        "".join(f"{line}\n" for line in lines),
        encoding="utf-8",
        newline="\n",
    )


def read_safe_diagnostics_jsonl(
    path: str | Path,
) -> tuple[SafeDiagnosticEnvelope, ...]:
    target = Path(path)
    diagnostics: list[SafeDiagnosticEnvelope] = []
    seen_ids: set[str] = set()

    expected_keys = {
        "schema",
        "diagnostic_id",
        "diagnostic_fingerprint",
        "run_id",
        "baseline_commit",
        "task_id",
        "phase",
        "component",
        "reason_code",
        "exception_type",
        "cause_chain_types",
        "safe_summary",
        "origin_scope",
        "repo_relative_file",
        "function",
        "line",
        "authority_effect",
    }

    for raw_line in target.read_text(encoding="utf-8").splitlines():
        try:
            payload = json.loads(raw_line)
        except json.JSONDecodeError as exc:
            raise ValueError(
                "diagnostics JSONL contains invalid JSON"
            ) from exc

        if not isinstance(payload, dict):
            raise ValueError("diagnostic JSONL entry must be an object")
        if set(payload) != expected_keys:
            raise ValueError("diagnostic JSONL keys mismatch")

        cause_chain = payload["cause_chain_types"]
        if (
            not isinstance(cause_chain, list)
            or not all(isinstance(item, str) for item in cause_chain)
        ):
            raise ValueError(
                "diagnostic cause_chain_types must be a string list"
            )

        diagnostic = SafeDiagnosticEnvelope(
            schema=payload["schema"],
            diagnostic_id=payload["diagnostic_id"],
            diagnostic_fingerprint=payload["diagnostic_fingerprint"],
            run_id=payload["run_id"],
            baseline_commit=payload["baseline_commit"],
            task_id=payload["task_id"],
            phase=payload["phase"],
            component=payload["component"],
            reason_code=payload["reason_code"],
            exception_type=payload["exception_type"],
            cause_chain_types=tuple(cause_chain),
            safe_summary=payload["safe_summary"],
            origin_scope=payload["origin_scope"],
            repo_relative_file=payload["repo_relative_file"],
            function=payload["function"],
            line=payload["line"],
            authority_effect=payload["authority_effect"],
        )
        if diagnostic.diagnostic_id in seen_ids:
            raise ValueError("duplicate diagnostic_id")
        seen_ids.add(diagnostic.diagnostic_id)
        diagnostics.append(diagnostic)

    return tuple(diagnostics)


def _safe_summary(exc: Exception) -> str:
    for exc_type, summary in _SAFE_SUMMARIES.items():
        if isinstance(exc, exc_type):
            return summary
    return "component raised an unexpected exception"


def _cause_chain_types(exc: Exception) -> tuple[str, ...]:
    result: list[str] = []
    seen: set[int] = set()
    current: BaseException | None = exc

    while current is not None and len(result) < 8:
        identity = id(current)
        if identity in seen:
            break
        seen.add(identity)
        result.append(type(current).__name__)

        if current.__cause__ is not None:
            current = current.__cause__
        elif (
            current.__context__ is not None
            and not current.__suppress_context__
        ):
            current = current.__context__
        else:
            current = None

    return tuple(result)


def _safe_origin(
    traceback: TracebackType | None,
    repository_root: Path,
) -> tuple[str, str | None, str | None, int | None]:
    candidate: tuple[str, str, int] | None = None
    current = traceback

    while current is not None:
        filename = current.tb_frame.f_code.co_filename
        try:
            resolved = Path(filename).expanduser().resolve()
            relative = resolved.relative_to(repository_root)
        except (OSError, RuntimeError, ValueError):
            current = current.tb_next
            continue

        relative_text = relative.as_posix()
        _validate_repo_relative_path(relative_text)
        function = current.tb_frame.f_code.co_name
        _validate_safe_text("function", function)
        candidate = (
            relative_text,
            function,
            current.tb_lineno,
        )
        current = current.tb_next

    if candidate is None:
        return "external", None, None, None

    return "repository", candidate[0], candidate[1], candidate[2]


def _validate_identifier(field: str, value: object) -> None:
    if not isinstance(value, str) or not _IDENTIFIER_RE.fullmatch(value):
        raise ValueError(f"{field} is not a safe identifier")


def _validate_safe_text(field: str, value: object) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{field} must be a string")
    if not value or value != value.strip():
        raise ValueError(f"{field} must be a non-empty trimmed string")
    if any(ord(character) < 32 or ord(character) == 127 for character in value):
        raise ValueError(f"{field} contains forbidden control characters")


def _validate_repo_relative_path(value: str) -> None:
    _validate_safe_text("repo_relative_file", value)
    if value.startswith("/") or "\\" in value:
        raise ValueError(
            "repo_relative_file must be repository-relative POSIX path"
        )
    if any(part in {"", ".", ".."} for part in value.split("/")):
        raise ValueError("repo_relative_file contains invalid segment")
