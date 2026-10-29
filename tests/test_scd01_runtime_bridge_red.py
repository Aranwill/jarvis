"""SCD-01 first A/B dispatch RED: genuine OllamaRuntime, intercepted transport.

The E3 source constants and real frozen-case projection are verified first.
Expected behavioral RED: HTTP dispatch count is 0 but the contract requires 2.
No live Ollama, model, network or evaluator/scorer may be invoked.
"""
from __future__ import annotations

from dataclasses import replace
from urllib.error import URLError
import hashlib
import importlib.util
import json
from pathlib import Path
from unittest.mock import patch

import pytest

from malak.core.conversation import ConversationMessage, ConversationRequest
from malak.runtime.ollama_runtime import OllamaRuntime
from malak.runtime.runtime_generation_contract import RuntimeGenerationContract


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "scripts" / "run_e3_governed_blind_assessor_ollama_experiment.py"
BRIDGE = ROOT / "scripts" / "run_scd01_runtime_bridge.py"
PREFIX = "BLIND_EVIDENCE_PACKET_JSON:\n"
MODEL = "qwen3.5:9b"
CASE_ID = "P-06ABAC84A1"  # For test diagnostics, never included in model-visible prompt.
PACKET = {
    "statement": "Sensor checks every device in the declared pool.",
    "evidence": [
        {"ref": "R1", "material": "The entire declared device pool is {A, B, C}."},
        {"ref": "R2", "material": "Sensor check log records A:PASS and B:PASS."},
        {"ref": "R3", "material": "The displayed check-log excerpt was collected at 14:00."},
    ],
}
PACKET_SHA256 = "06abac84a103acbc3f91a0cc57912cc1afdbd7e2808b0161ac7ded0a8de2b54f"
A_SHA256 = "22b29f8841473fdcea30fa531d6b9d7535eb1abbdecb57fca44c52df477a67ab"
B_SHA256 = "82e775aba848baa49c65d9f2926e6f631c9bd5b3dcf6dd5fe4ec4390bd774076"
B_ADDITION = """Before choosing the existing contractual outcome and reason code, identify the material assertions explicitly made by the statement without adding assertions from the evidence.

Do not treat an activity, example, prerequisite, stage, observation, or limitation mentioned only by supporting evidence as an additional asserted part of the statement.

Use the statement and its explicit scope as written. Do not split or expand the statement merely because the evidence enumerates stages, examples, or subactivities, and do not infer a decomposition rule from surface syntax alone.

When more than one material assertion is explicitly present, evaluate the supplied evidence against those assertions only as an aid to applying the existing E3 semantics.

This method does not define logical independence, implication, or a new contractual meaning of "compound". Apply only the current E3 reason semantics and established precedence.

Distinguish relevant-but-insufficient support, direct unresolved material contradiction, and an explicitly named external evidence dependency.

Do not invent evidence, labels, keys, fields, expected answers, or new precedence.

Return only the existing required JSON; no chain-of-thought or additional trace fields.
"""


def _load(path: Path, name: str):
    assert path.is_file(), f"required original module missing: {path.name}"
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _canonical(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def _frozen_pair() -> tuple[ConversationRequest, ConversationRequest]:
    e3 = _load(SOURCE, "scd01_e3_original")
    a = e3.EXACT_SYSTEM_PROMPT.encode("utf-8")
    b = a + b"\n" + B_ADDITION.encode("utf-8")
    assert len(a) == 2512 and _sha(a) == A_SHA256, "source A identity mismatch"
    assert len(B_ADDITION.encode("utf-8")) == 1247, "frozen addition size mismatch"
    assert len(b) == 3760 and _sha(b) == B_SHA256, "frozen B identity mismatch"
    assert e3.EXACT_USER_PREFIX == PREFIX, "E3 user prefix mismatch"
    projected = _canonical(PACKET)
    assert _sha(projected) == PACKET_SHA256, "frozen packet SHA mismatch"
    contract = RuntimeGenerationContract(
        context_window_tokens=8192,
        max_output_tokens=256,
        thinking_enabled=False,
    )
    requests = tuple(
        ConversationRequest(
            prompt=PREFIX + projected.decode("utf-8"),
            model=MODEL,
            system_prompt=system.decode("utf-8"),
            history=(),
            response_json_schema=e3.EXACT_RESPONSE_JSON_SCHEMA,
            generation_contract=contract,
        )
        for system in (a, b)
    )
    assert len(requests) == 2
    assert requests[0].prompt == requests[1].prompt
    assert requests[0].response_json_schema == requests[1].response_json_schema
    assert requests[0].history == requests[1].history == ()
    return requests


def test_scd01_frozen_pair_preconditions_pass_without_model():
    """If this fails, STOP: it is a setup/fixture failure, not a valid RED."""
    pair = _frozen_pair()
    assert (pair[0].model, pair[1].model) == (MODEL, MODEL)
    assert [p.generation_contract.thinking_enabled for p in pair] == [
        False, False,
    ]
    assert [p.generation_contract.max_output_tokens for p in pair] == [
        256, 256,
    ]
    assert CASE_ID not in pair[0].prompt
    assert CASE_ID not in pair[1].prompt


def test_scd01_pair_dispatches_through_real_ollama_runtime_transport():
    """Original RED was disconnected; after GREEN exactly two calls are required.

    This tests the real OllamaRuntime.generate() transport path, not a fake
    runtime. Only its urlopen transport is intercepted; no actual HTTP is sent.
    """
    bridge = _load(BRIDGE, "scd01_bridge_red")
    pair = _frozen_pair()
    captured = []

    class LocalHTTPResponse:
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
                "model": MODEL,
                "message": {
                    "role": "assistant",
                    "content": '{"outcome":"INSUFFICIENT","reason_codes":["SUPPORTING_REFS_INSUFFICIENT"]}',
                },
                "done": True,
                "done_reason": "stop",
                "prompt_eval_count": 15,
                "eval_count": 25,
            }).encode("utf-8")

    def transport(request, timeout):
        captured.append((request, timeout, json.loads(request.data)))
        return LocalHTTPResponse(request)

    runtime = OllamaRuntime(
        base_url="http://127.0.0.1:11434",
        timeout_seconds=300,
        keep_alive=0,
        max_request_bytes=1048576,
        max_response_bytes=65536,
    )
    with patch("malak.runtime.ollama_runtime.urlopen", side_effect=transport):
        responses = bridge.dispatch_scd01_pair_v1(runtime=runtime, pair=pair)

    # RED-to-GREEN invariant: exactly two genuine intercepted HTTP calls.
    assert len(captured) == 2, (
        "SCD01_CONSUMER_NOT_CONNECTED: expected 2 real-runtime dispatches, "
        f"observed {len(captured)}"
    )
    assert all(
        request.full_url == "http://127.0.0.1:11434/api/chat"
        for request, _, _ in captured
    )
    for (request, _, payload), expected in zip(captured, pair, strict=True):
        assert request.get_method() == "POST"
        assert payload["model"] == MODEL
        assert payload["messages"] == [
            {"role": "system", "content": expected.system_prompt},
            {"role": "user", "content": expected.prompt},
        ]
        assert payload["think"] is False
        assert payload["truncate"] is False
        assert payload["shift"] is False
        assert payload["options"] == {"num_ctx": 8192, "num_predict": 256}
        assert payload["format"] == json.loads(expected.response_json_schema)
    assert len(responses) == 2
    assert all(x.model == MODEL and x.provider == "ollama" for x in responses)


def _test_runtime() -> OllamaRuntime:
    return OllamaRuntime(
        base_url="http://127.0.0.1:11434",
        timeout_seconds=300,
        keep_alive=0,
        max_request_bytes=1048576,
        max_response_bytes=65536,
    )


class _TransportSuccess:
    """Synthetic Ollama HTTP success for the real runtime's transport seam."""

    def __init__(self, request, *, response_model: str = MODEL):
        self.url = request.full_url
        self.response_model = response_model

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def geturl(self):
        return self.url

    def read(self, _limit):
        return json.dumps({
            "model": self.response_model,
            "message": {
                "role": "assistant",
                "content": '{"outcome":"INSUFFICIENT","reason_codes":["SUPPORTING_REFS_INSUFFICIENT"]}',
            },
            "done": True,
            "done_reason": "stop",
            "prompt_eval_count": 15,
            "eval_count": 25,
        }).encode("utf-8")


@pytest.mark.parametrize(
    "change",
    (
        "model",
        "prompt",
        "system_prompt",
        "response_json_schema",
        "generation_contract",
        "history",
        "missing_system_prompt",
    ),
)
def test_scd01_rejects_non_comparable_pair_before_transport(change: str):
    """No side effects before complete A/B comparability admission."""
    bridge = _load(BRIDGE, "scd01_bridge_negative_compare")
    a, b = _frozen_pair()

    replacement = {
        "model": {"model": "other:model"},
        "prompt": {"prompt": PREFIX + "{}"},
        "system_prompt": {"system_prompt": a.system_prompt},
        "response_json_schema": {
            "response_json_schema": '{"type":"object"}',
        },
        "generation_contract": {
            "generation_contract": RuntimeGenerationContract(
                context_window_tokens=8192,
                max_output_tokens=128,
                thinking_enabled=False,
            ),
        },
        "history": {
            "history": (ConversationMessage(role="user", content="forbidden"),),
        },
        "missing_system_prompt": {"system_prompt": None},
    }[change]
    modified_pair = (a, replace(b, **replacement))
    with patch(
        "malak.runtime.ollama_runtime.urlopen",
        side_effect=AssertionError("unexpected HTTP dispatch"),
    ) as transport:
        with pytest.raises(ValueError, match="SCD-01 requires comparable"):
            bridge.dispatch_scd01_pair_v1(
                runtime=_test_runtime(),
                pair=modified_pair,
            )
    transport.assert_not_called()


def test_scd01_rejects_non_runtime_or_non_pair_before_transport():
    bridge = _load(BRIDGE, "scd01_bridge_negative_shape")
    pair = _frozen_pair()
    with patch(
        "malak.runtime.ollama_runtime.urlopen",
        side_effect=AssertionError("unexpected HTTP dispatch"),
    ) as transport:
        with pytest.raises(TypeError, match="existing OllamaRuntime"):
            bridge.dispatch_scd01_pair_v1(runtime=object(), pair=pair)
        with pytest.raises(TypeError, match="exactly two"):
            bridge.dispatch_scd01_pair_v1(runtime=_test_runtime(), pair=(pair[0],))
        with pytest.raises(TypeError, match="exactly two"):
            bridge.dispatch_scd01_pair_v1(runtime=_test_runtime(), pair=[*pair])
    transport.assert_not_called()


def test_scd01_first_transport_failure_propagates_without_retry():
    """First failure must abort: no second arm, no automatic retry."""
    bridge = _load(BRIDGE, "scd01_bridge_negative_first_http")
    pair = _frozen_pair()
    with patch(
        "malak.runtime.ollama_runtime.urlopen",
        side_effect=URLError("synthetic transport failure"),
    ) as transport:
        with pytest.raises(RuntimeError, match="Unable to connect to Ollama"):
            bridge.dispatch_scd01_pair_v1(runtime=_test_runtime(), pair=pair)
    assert transport.call_count == 1


def test_scd01_second_transport_failure_propagates_without_retry():
    """A succeeds, B fails, no successful pair is returned and no retry."""
    bridge = _load(BRIDGE, "scd01_bridge_negative_second_http")
    pair = _frozen_pair()
    calls = []

    def transport(request, timeout):
        calls.append((request.full_url, timeout))
        if len(calls) == 1:
            return _TransportSuccess(request)
        raise URLError("synthetic second-arm transport failure")

    with patch("malak.runtime.ollama_runtime.urlopen", side_effect=transport):
        with pytest.raises(RuntimeError, match="Unable to connect to Ollama"):
            bridge.dispatch_scd01_pair_v1(runtime=_test_runtime(), pair=pair)
    assert [url for url, _ in calls] == [
        "http://127.0.0.1:11434/api/chat",
        "http://127.0.0.1:11434/api/chat",
    ]


def test_scd01_first_response_model_mismatch_stops_pair_without_retry():
    """Existing runtime's strict model identity check must gate arm B."""
    bridge = _load(BRIDGE, "scd01_bridge_negative_model")
    pair = _frozen_pair()
    with patch(
        "malak.runtime.ollama_runtime.urlopen",
        side_effect=lambda request, timeout: _TransportSuccess(
            request,
            response_model="unexpected:model",
        ),
    ) as transport:
        with pytest.raises(RuntimeError, match="does not match requested model"):
            bridge.dispatch_scd01_pair_v1(runtime=_test_runtime(), pair=pair)
    assert transport.call_count == 1
