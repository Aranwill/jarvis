from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Final


RUNTIME_MODEL_PROVENANCE_SCHEMA: Final[str] = (
    "MALAK-RUNTIME-MODEL-PROVENANCE/v0"
)
_DIGEST_RE: Final[re.Pattern[str]] = re.compile(
    r"^sha256:[0-9a-f]{64}$"
)
_SAFE_TEXT_RE: Final[re.Pattern[str]] = re.compile(
    r"^[^\x00-\x1f\x7f]+$"
)
_IDENTITY_STRENGTHS: Final[frozenset[str]] = frozenset(
    {"DIGEST_BOUND", "TAG_ONLY", "UNAVAILABLE"}
)
_PROVENANCE_STATUSES: Final[frozenset[str]] = frozenset(
    {"READY", "PARTIAL", "UNAVAILABLE"}
)


@dataclass(frozen=True, slots=True)
class RuntimeModelProvenance:
    schema: str
    captured_at: datetime
    runtime_class: str
    provider: str
    requested_model: str
    resolved_model: str | None
    model_digest: str | None
    model_identity_strength: str
    runtime_version: str | None
    declared_context_window: int | None
    context_window_source: str
    generation_options: dict[str, object]
    timeout_seconds: float
    keep_alive: int | str
    max_request_bytes: int
    max_response_bytes: int
    provenance_status: str
    authority_effect: str = "none"

    def __post_init__(self) -> None:
        if self.schema != RUNTIME_MODEL_PROVENANCE_SCHEMA:
            raise ValueError("runtime provenance schema mismatch")
        _validate_utc(self.captured_at)
        for field_name in (
            "runtime_class",
            "provider",
            "requested_model",
            "context_window_source",
        ):
            _validate_text(field_name, getattr(self, field_name))

        if self.resolved_model is not None:
            _validate_text("resolved_model", self.resolved_model)
        if self.runtime_version is not None:
            _validate_text("runtime_version", self.runtime_version)

        if self.model_identity_strength not in _IDENTITY_STRENGTHS:
            raise ValueError("unsupported model_identity_strength")
        if self.provenance_status not in _PROVENANCE_STATUSES:
            raise ValueError("unsupported provenance_status")

        if self.model_digest is not None and not _DIGEST_RE.fullmatch(
            self.model_digest
        ):
            raise ValueError("model_digest must be sha256:<64 lowercase hex>")

        if self.model_identity_strength == "DIGEST_BOUND":
            if self.resolved_model is None or self.model_digest is None:
                raise ValueError(
                    "DIGEST_BOUND requires resolved_model and model_digest"
                )
            if self.provenance_status != "READY":
                raise ValueError("DIGEST_BOUND provenance must be READY")
        elif self.model_identity_strength == "TAG_ONLY":
            if self.resolved_model is None or self.model_digest is not None:
                raise ValueError(
                    "TAG_ONLY requires resolved_model without model_digest"
                )
            if self.provenance_status != "PARTIAL":
                raise ValueError("TAG_ONLY provenance must be PARTIAL")
        else:
            if self.resolved_model is not None or self.model_digest is not None:
                raise ValueError(
                    "UNAVAILABLE identity cannot claim model or digest"
                )
            if self.provenance_status != "UNAVAILABLE":
                raise ValueError(
                    "UNAVAILABLE identity requires UNAVAILABLE status"
                )

        if self.declared_context_window is None:
            if self.context_window_source != "unavailable":
                raise ValueError(
                    "missing context window requires unavailable source"
                )
        else:
            if (
                type(self.declared_context_window) is not int
                or self.declared_context_window <= 0
            ):
                raise ValueError(
                    "declared_context_window must be a positive integer"
                )
            if self.context_window_source == "unavailable":
                raise ValueError(
                    "available context window requires an explicit source"
                )

        if not isinstance(self.generation_options, dict):
            raise TypeError("generation_options must be a dict")
        _validate_json_object(
            "generation_options",
            self.generation_options,
        )

        if (
            isinstance(self.timeout_seconds, bool)
            or not isinstance(self.timeout_seconds, (int, float))
            or self.timeout_seconds <= 0
        ):
            raise ValueError("timeout_seconds must be positive")
        if not isinstance(self.keep_alive, (int, str)) or isinstance(
            self.keep_alive,
            bool,
        ):
            raise TypeError("keep_alive must be int or string")

        for name in ("max_request_bytes", "max_response_bytes"):
            value = getattr(self, name)
            if type(value) is not int or value <= 0:
                raise ValueError(f"{name} must be a positive integer")

        if self.authority_effect != "none":
            raise ValueError(
                "runtime provenance authority_effect must remain none"
            )


def write_runtime_model_provenance(
    path: str | Path,
    provenance: RuntimeModelProvenance,
) -> None:
    if not isinstance(provenance, RuntimeModelProvenance):
        raise TypeError(
            "provenance must be a RuntimeModelProvenance"
        )

    payload = _to_payload(provenance)
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )


def read_runtime_model_provenance(
    path: str | Path,
) -> RuntimeModelProvenance:
    target = Path(path)
    try:
        payload = json.loads(target.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(
            "runtime provenance contains invalid JSON"
        ) from exc

    if not isinstance(payload, dict):
        raise ValueError(
            "runtime provenance payload must be an object"
        )

    expected_keys = {
        "schema",
        "captured_at",
        "runtime_class",
        "provider",
        "requested_model",
        "resolved_model",
        "model_digest",
        "model_identity_strength",
        "runtime_version",
        "declared_context_window",
        "context_window_source",
        "generation_options",
        "timeout_seconds",
        "keep_alive",
        "max_request_bytes",
        "max_response_bytes",
        "provenance_status",
        "authority_effect",
    }
    if set(payload) != expected_keys:
        raise ValueError("runtime provenance keys mismatch")

    captured_at = _parse_utc_datetime(payload["captured_at"])

    generation_options = payload["generation_options"]
    if not isinstance(generation_options, dict):
        raise ValueError(
            "runtime provenance generation_options must be an object"
        )

    return RuntimeModelProvenance(
        schema=payload["schema"],
        captured_at=captured_at,
        runtime_class=payload["runtime_class"],
        provider=payload["provider"],
        requested_model=payload["requested_model"],
        resolved_model=payload["resolved_model"],
        model_digest=payload["model_digest"],
        model_identity_strength=payload["model_identity_strength"],
        runtime_version=payload["runtime_version"],
        declared_context_window=payload["declared_context_window"],
        context_window_source=payload["context_window_source"],
        generation_options=generation_options,
        timeout_seconds=payload["timeout_seconds"],
        keep_alive=payload["keep_alive"],
        max_request_bytes=payload["max_request_bytes"],
        max_response_bytes=payload["max_response_bytes"],
        provenance_status=payload["provenance_status"],
        authority_effect=payload["authority_effect"],
    )


def _to_payload(
    provenance: RuntimeModelProvenance,
) -> dict[str, object]:
    return {
        "schema": provenance.schema,
        "captured_at": provenance.captured_at.isoformat().replace(
            "+00:00",
            "Z",
        ),
        "runtime_class": provenance.runtime_class,
        "provider": provenance.provider,
        "requested_model": provenance.requested_model,
        "resolved_model": provenance.resolved_model,
        "model_digest": provenance.model_digest,
        "model_identity_strength": provenance.model_identity_strength,
        "runtime_version": provenance.runtime_version,
        "declared_context_window": provenance.declared_context_window,
        "context_window_source": provenance.context_window_source,
        "generation_options": dict(provenance.generation_options),
        "timeout_seconds": float(provenance.timeout_seconds),
        "keep_alive": provenance.keep_alive,
        "max_request_bytes": provenance.max_request_bytes,
        "max_response_bytes": provenance.max_response_bytes,
        "provenance_status": provenance.provenance_status,
        "authority_effect": provenance.authority_effect,
    }


def _validate_text(field: str, value: object) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{field} must be a string")
    if not value or value != value.strip():
        raise ValueError(f"{field} must be a non-empty trimmed string")
    if not _SAFE_TEXT_RE.fullmatch(value):
        raise ValueError(f"{field} contains forbidden control characters")


def _validate_utc(value: datetime) -> None:
    if not isinstance(value, datetime):
        raise TypeError("captured_at must be a datetime")
    if value.tzinfo is None or value.utcoffset() != UTC.utcoffset(value):
        raise ValueError("captured_at must be timezone-aware UTC")


def _parse_utc_datetime(value: object) -> datetime:
    if not isinstance(value, str) or not value:
        raise ValueError("captured_at must be an ISO-8601 string")
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ValueError("captured_at is not valid ISO-8601") from exc
    _validate_utc(parsed)
    return parsed


def _validate_json_object(
    field: str,
    value: dict[str, object],
) -> None:
    for key, item in value.items():
        _validate_text(f"{field} key", key)
        if item is None or isinstance(item, (str, int, float, bool)):
            continue
        raise ValueError(
            f"{field} values must be JSON scalar values"
        )
