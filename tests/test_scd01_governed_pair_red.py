"""SCD-01 provenance pair behavioral RED on real OllamaRuntime.

No live model calls: capture_provenance and urlopen are intercepted on the
genuine runtime instance. The original RED found zero snapshots and dispatches; after GREEN it must pass.
"""
from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime
import importlib.util
import json
from pathlib import Path
from urllib.error import URLError
from unittest.mock import patch

import pytest

from malak.runtime.ollama_runtime import OllamaRuntime
from malak.runtime.runtime_provenance import (
    RUNTIME_MODEL_PROVENANCE_SCHEMA,
    RuntimeModelProvenance,
)

ROOT = Path(__file__).resolve().parents[1]
EXISTING_TEST = ROOT / "tests" / "test_scd01_runtime_bridge_red.py"
COORDINATOR = ROOT / "scripts" / "run_scd01_governed_pair.py"


def _load(path: Path, name: str):
    assert path.is_file(), f"missing source: {path.name}"
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _genuine_pair():
    previous = _load(EXISTING_TEST, "scd01_genuine_frozen_pair_fixture")
    return previous._frozen_pair()


def _runtime():
    return OllamaRuntime(
        base_url="http://127.0.0.1:11434",
        timeout_seconds=300,
        keep_alive=0,
        max_request_bytes=1048576,
        max_response_bytes=65536,
    )


def _provenance(pair):
    contract = pair[0].generation_contract
    assert contract is not None
    return RuntimeModelProvenance(
        schema=RUNTIME_MODEL_PROVENANCE_SCHEMA,
        captured_at=datetime(2026, 10, 27, 20, 0, tzinfo=UTC),
        runtime_class="OllamaRuntime",
        provider="ollama",
        requested_model="qwen3.5:9b",
        resolved_model="qwen3.5:9b",
        model_digest="sha256:" + "a" * 64,
        model_identity_strength="TAG_DIGEST_BOUND",
        runtime_version="0.40.11",
        declared_context_window=32768,
        context_window_source="ollama:model_info",
        generation_options=contract.to_generation_options(),
        timeout_seconds=300,
        keep_alive=0,
        max_request_bytes=1048576,
        max_response_bytes=65536,
        provenance_status="READY",
        authority_effect="none",
    )


class _SyntheticHTTP:
    def __init__(self, request):
        self.url = request.full_url

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def geturl(self):
        return self.url

    def read(self, _limit):
        return json.dumps({
            "model": "qwen3.5:9b",
            "message": {
                "role": "assistant",
                "content": json.dumps({
                    "outcome": "INSUFFICIENT",
                    "reason_codes": ["SUPPORTING_REFS_INSUFFICIENT"],
                }),
            },
            "done": True,
            "done_reason": "stop",
            "prompt_eval_count": 12,
            "eval_count": 18,
        }).encode("utf-8")


def test_scd01_provenance_red_setup_authentic_frozen_inputs():
    """Must pass before counting a disconnected path as a valid RED."""
    pair = _genuine_pair()
    coordinator = _load(COORDINATOR, "scd01_governed_pair_red_setup")
    runtime = _runtime()
    provenance = _provenance(pair)
    assert provenance.provenance_status == "READY"
    assert provenance.model_identity_strength == "TAG_DIGEST_BOUND"
    assert provenance.generation_options["thinking_enabled"] is False
    assert provenance.generation_options["context_window_tokens"] == 8192
    assert provenance.generation_options["max_output_tokens"] == 256
    assert pair[0].prompt == pair[1].prompt
    assert pair[0].system_prompt != pair[1].system_prompt
    assert hasattr(coordinator, "run_scd01_governed_pair_v1")
    assert isinstance(runtime, OllamaRuntime)


def test_scd01_provenance_bound_pair_uses_real_runtime_without_live_http():
    """GREEN requires six provenance captures and two intercepted HTTP calls."""
    pair = _genuine_pair()
    provenance = _provenance(pair)
    runtime = _runtime()
    coordinator = _load(COORDINATOR, "scd01_governed_pair_red_behavior")

    captured_requests = []

    def local_transport(request, timeout):
        captured_requests.append((request.full_url, timeout))
        return _SyntheticHTTP(request)

    with patch.object(
        runtime, "capture_provenance", return_value=provenance
    ) as snapshots, patch(
        "malak.runtime.ollama_runtime.urlopen",
        side_effect=local_transport,
    ):
        result = coordinator.run_scd01_governed_pair_v1(
            runtime=runtime,
            pair=pair,
        )

    assert snapshots.call_count == 6, (
        "SCD01_PROVENANCE_PAIR_NOT_CONNECTED: expected 6 snapshots, "
        f"observed {snapshots.call_count}"
    )
    assert len(captured_requests) == 2, (
        "SCD01_PROVENANCE_PAIR_NOT_CONNECTED: expected 2 genuine "
        f"runtime dispatches, observed {len(captured_requests)}"
    )
    assert all(
        url == "http://127.0.0.1:11434/api/chat"
        for url, _ in captured_requests
    )
    assert len(result) == 2
    assert all(item["authority_effect"] == "none" for item in result)
    assert all(item["status"] == "MODEL_OBSERVATION_ONLY" for item in result)
    assert all(item["parsed"]["outcome"] == "INSUFFICIENT" for item in result)



def _coordinator():
    return _load(COORDINATOR, "scd01_governed_pair_negative")


def test_scd01_provenance_unready_baseline_blocks_all_dispatch():
    pair = _genuine_pair()
    runtime = _runtime()
    unready = replace(
        _provenance(pair),
        model_identity_strength="TAG_ONLY",
        provenance_status="PARTIAL",
        model_digest=None,
    )
    with patch.object(
        runtime, "capture_provenance", return_value=unready
    ) as captures, patch(
        "malak.runtime.ollama_runtime.urlopen",
        side_effect=AssertionError("no HTTP may occur"),
    ) as transport:
        with pytest.raises(RuntimeError, match="READY/TAG_DIGEST_BOUND"):
            _coordinator().run_scd01_governed_pair_v1(runtime=runtime, pair=pair)
    assert captures.call_count == 1
    transport.assert_not_called()


def test_scd01_invalid_pair_blocks_provenance_and_transport():
    pair = _genuine_pair()
    runtime = _runtime()
    bad_pair = (pair[0], replace(pair[1], model="different:model"))
    with patch.object(
        runtime, "capture_provenance",
        side_effect=AssertionError("no introspection may occur"),
    ) as captures, patch(
        "malak.runtime.ollama_runtime.urlopen",
        side_effect=AssertionError("no HTTP may occur"),
    ) as transport:
        with pytest.raises(ValueError, match="requires comparable"):
            _coordinator().run_scd01_governed_pair_v1(
                runtime=runtime, pair=bad_pair
            )
    captures.assert_not_called()
    transport.assert_not_called()


@pytest.mark.parametrize(
    "drift_capture,expected_http",
    ((2, 0), (3, 1), (4, 1), (5, 2), (6, 2)),
)
def test_scd01_provenance_drift_stops_without_exposing_pair(
    drift_capture: int, expected_http: int,
):
    """Before/after each arm and final drift must fail closed, no retry."""
    pair = _genuine_pair()
    runtime = _runtime()
    good = _provenance(pair)
    drift = replace(good, model_digest="sha256:" + "b" * 64)
    snapshots_seen = []
    sends = []

    def capture(model, *, generation_contract):
        snapshots_seen.append((model, generation_contract))
        return drift if len(snapshots_seen) == drift_capture else good

    def transport(request, timeout):
        sends.append(request)
        return _SyntheticHTTP(request)

    with patch.object(
        runtime, "capture_provenance", side_effect=capture
    ), patch(
        "malak.runtime.ollama_runtime.urlopen", side_effect=transport
    ):
        with pytest.raises(RuntimeError, match="provenance drift detected"):
            _coordinator().run_scd01_governed_pair_v1(runtime=runtime, pair=pair)
    assert len(snapshots_seen) == drift_capture
    assert len(sends) == expected_http


@pytest.mark.parametrize(
    "failed_arm,expected_snapshots",
    ((1, 3), (2, 5)),
)
def test_scd01_transport_error_stops_pair_without_retry(
    failed_arm: int, expected_snapshots: int,
):
    """Even on generation failure, temporal provenance is checked once more."""
    pair = _genuine_pair()
    runtime = _runtime()
    provenance = _provenance(pair)
    sends = []

    def transport(request, timeout):
        sends.append(request)
        if len(sends) == failed_arm:
            raise URLError("synthetic transport error")
        return _SyntheticHTTP(request)

    with patch.object(
        runtime, "capture_provenance", return_value=provenance
    ) as captures, patch(
        "malak.runtime.ollama_runtime.urlopen", side_effect=transport
    ):
        with pytest.raises(RuntimeError, match="Unable to connect to Ollama"):
            _coordinator().run_scd01_governed_pair_v1(runtime=runtime, pair=pair)
    assert captures.call_count == expected_snapshots
    assert len(sends) == failed_arm


@pytest.mark.parametrize(
    "failed_arm,invalid_content",
    (
        (1, '{"outcome":"INSUFFICIENT"'),
        (2, '{"outcome":"INSUFFICIENT"'),
        (1, '{"outcome":"SUPPORTED","reason_codes":["SUPPORTING_REFS_INSUFFICIENT"]}'),
        (2, '{"outcome":"SUPPORTED","reason_codes":["SUPPORTING_REFS_INSUFFICIENT"]}'),
    ),
)
def test_scd01_e3_output_contract_invalid_blocks_successful_pair(
    failed_arm: int, invalid_content: str,
):
    """Use E3's actual strict parser and outcome/reason pairing, never a fake."""
    pair = _genuine_pair()
    runtime = _runtime()
    provenance = _provenance(pair)
    sends = []

    class InvalidOutput(_SyntheticHTTP):
        def read(self, _limit):
            return json.dumps({
                "model": "qwen3.5:9b",
                "message": {
                    "role": "assistant",
                    "content": invalid_content,
                },
                "done": True,
                "done_reason": "stop",
                "prompt_eval_count": 12,
                "eval_count": 18,
            }).encode("utf-8")

    def transport(request, timeout):
        sends.append(request)
        if len(sends) == failed_arm:
            return InvalidOutput(request)
        return _SyntheticHTTP(request)

    with patch.object(
        runtime, "capture_provenance", return_value=provenance
    ), patch(
        "malak.runtime.ollama_runtime.urlopen", side_effect=transport
    ):
        with pytest.raises(
            RuntimeError,
            match="invalid JSON|outcome/reason pairing invalid",
        ):
            _coordinator().run_scd01_governed_pair_v1(runtime=runtime, pair=pair)
    assert len(sends) == failed_arm



def test_scd01_runtime_class_drift_rejected_even_when_tuple_equal():
    """Full E3 baseline admission is rerun after every temporal snapshot.

    E3's legacy stability tuple omits runtime_class; a changed class must
    still fail closed before the first model dispatch.
    """
    pair = _genuine_pair()
    runtime = _runtime()
    baseline = _provenance(pair)
    altered_class = replace(baseline, runtime_class="DifferentRuntime")
    captures = []

    def capture(model, *, generation_contract):
        captures.append(model)
        return baseline if len(captures) == 1 else altered_class

    with patch.object(
        runtime, "capture_provenance", side_effect=capture
    ), patch(
        "malak.runtime.ollama_runtime.urlopen",
        side_effect=AssertionError("unexpected HTTP"),
    ) as transport:
        with pytest.raises(
            RuntimeError, match="baseline provenance runtime class is invalid"
        ):
            _coordinator().run_scd01_governed_pair_v1(
                runtime=runtime, pair=pair
            )
    assert len(captures) == 2
    transport.assert_not_called()
