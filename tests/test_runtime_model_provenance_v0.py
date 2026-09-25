from __future__ import annotations

import dataclasses
import json
import re
from datetime import UTC, datetime
from importlib import import_module

import pytest

from malak.runtime.ollama_runtime import OllamaRuntime


RAW_DIGEST = "a" * 64
DIGEST = "sha256:" + RAW_DIGEST


class _FakeHTTPResponse:
    def __init__(self, payload: dict[str, object]) -> None:
        self._raw = json.dumps(payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *args: object) -> None:
        return None

    def read(self, size: int = -1) -> bytes:
        return self._raw if size < 0 else self._raw[:size]


def _module():
    return import_module("malak.runtime.runtime_provenance")


def _capture(
    monkeypatch: pytest.MonkeyPatch,
    *,
    digest: str | None = RAW_DIGEST,
    resolved_model: str = "qwen3:8b",
    context_window: int | None = 32768,
):
    calls: list[tuple[str, str]] = []

    def fake_urlopen(request, timeout: float):
        calls.append((request.full_url, request.get_method()))
        if request.full_url.endswith("/api/version"):
            return _FakeHTTPResponse({"version": "0.12.0"})
        if request.full_url.endswith("/api/tags"):
            models: list[dict[str, object]] = []
            if resolved_model:
                item: dict[str, object] = {
                    "name": resolved_model,
                    "model": resolved_model,
                }
                if digest is not None:
                    item["digest"] = digest
                models.append(item)
            return _FakeHTTPResponse({"models": models})
        if request.full_url.endswith("/api/show"):
            model_info: dict[str, object] = {}
            if context_window is not None:
                model_info["qwen3.context_length"] = context_window
            return _FakeHTTPResponse(
                {
                    "model_info": model_info,
                    "details": {},
                }
            )
        raise AssertionError(f"unexpected introspection URL: {request.full_url}")

    monkeypatch.setattr(
        "malak.runtime.ollama_runtime.urlopen",
        fake_urlopen,
    )
    runtime = OllamaRuntime(
        base_url="http://127.0.0.1:11434",
        timeout_seconds=30.0,
        keep_alive=0,
        max_request_bytes=1024,
        max_response_bytes=2048,
    )
    provenance = runtime.capture_provenance("qwen3:8b")
    return provenance, calls


def test_model_provenance_red_c01_contract_is_frozen_and_authority_free(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    provenance, _ = _capture(monkeypatch)

    assert dataclasses.is_dataclass(provenance)
    assert provenance.schema == "MALAK-RUNTIME-MODEL-PROVENANCE/v0"
    assert provenance.runtime_class == "OllamaRuntime"
    assert provenance.provider == "ollama"
    assert provenance.authority_effect == "none"
    assert provenance.captured_at.tzinfo is not None

    with pytest.raises(dataclasses.FrozenInstanceError):
        provenance.requested_model = "other"


def test_model_provenance_red_c02_records_requested_and_resolved_model(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    provenance, _ = _capture(monkeypatch)

    assert provenance.requested_model == "qwen3:8b"
    assert provenance.resolved_model == "qwen3:8b"


def test_model_provenance_red_c03_digest_binds_exact_model_identity(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    provenance, _ = _capture(monkeypatch)

    assert provenance.model_digest == DIGEST
    assert re.fullmatch(r"sha256:[0-9a-f]{64}", provenance.model_digest)
    assert provenance.model_identity_strength == "DIGEST_BOUND"
    assert provenance.provenance_status == "READY"


def test_model_provenance_red_c04_missing_digest_never_fabricates_identity(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    provenance, _ = _capture(monkeypatch, digest=None)

    assert provenance.model_digest is None
    assert provenance.model_identity_strength == "TAG_ONLY"
    assert provenance.provenance_status == "PARTIAL"


def test_model_provenance_red_c05_unavailable_model_is_explicit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    provenance, _ = _capture(
        monkeypatch,
        digest=None,
        resolved_model="",
        context_window=None,
    )

    assert provenance.resolved_model is None
    assert provenance.model_digest is None
    assert provenance.model_identity_strength == "UNAVAILABLE"
    assert provenance.provenance_status == "UNAVAILABLE"


def test_model_provenance_red_c06_runtime_version_and_declared_context_are_explicit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    provenance, _ = _capture(monkeypatch)

    assert provenance.runtime_version == "0.12.0"
    assert provenance.declared_context_window == 32768
    assert provenance.context_window_source == "ollama:model_info"
    assert provenance.context_window_source != "actual_usage"


def test_model_provenance_red_c07_missing_context_is_not_estimated(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    provenance, _ = _capture(monkeypatch, context_window=None)

    assert provenance.declared_context_window is None
    assert provenance.context_window_source == "unavailable"


def test_model_provenance_red_c08_records_only_explicit_runtime_configuration(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    provenance, _ = _capture(monkeypatch)

    assert provenance.generation_options == {}
    assert provenance.timeout_seconds == 30.0
    assert provenance.keep_alive == 0
    assert provenance.max_request_bytes == 1024
    assert provenance.max_response_bytes == 2048


def test_model_provenance_red_c09_introspection_is_read_only(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, calls = _capture(monkeypatch)

    urls = [url for url, _ in calls]
    assert any(url.endswith("/api/version") for url in urls)
    assert any(url.endswith("/api/tags") for url in urls)
    assert any(url.endswith("/api/show") for url in urls)

    forbidden = (
        "/api/pull",
        "/api/delete",
        "/api/create",
        "/api/copy",
        "/api/generate",
        "/api/chat",
    )
    assert all(
        not any(item in url for item in forbidden)
        for url in urls
    )


def test_model_provenance_red_c10_serialization_is_closed_and_round_trippable(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    module = _module()
    provenance, _ = _capture(monkeypatch)
    path = tmp_path / "runtime_provenance.json"

    module.write_runtime_model_provenance(path, provenance)
    loaded = module.read_runtime_model_provenance(path)

    assert loaded == provenance


def test_model_provenance_red_c11_unknown_fields_fail_closed(
    tmp_path,
) -> None:
    module = _module()
    path = tmp_path / "runtime_provenance.json"
    path.write_text(
        json.dumps(
            {
                "schema": "MALAK-RUNTIME-MODEL-PROVENANCE/v0",
                "unexpected": True,
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        module.read_runtime_model_provenance(path)


def test_model_provenance_red_c12_metrics_are_not_evaluation_or_authority(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    provenance, _ = _capture(monkeypatch)
    fields = {field.name for field in dataclasses.fields(provenance)}

    forbidden = {
        "quality_score",
        "capability_score",
        "benchmark_verdict",
        "recommended_model",
        "authorization",
        "approval",
    }
    assert forbidden.isdisjoint(fields)
    assert provenance.authority_effect == "none"
