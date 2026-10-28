"""Behavioral RED for authentic frozen 16-pair/32-request SCD-01 coordination.

Only the real existing OllamaRuntime class is used. Every I/O interaction is
intercepted. Frozen corpus/schedule files MUST pass hash and binding checks
before the single expected behavioral RED may be admitted.
"""
from __future__ import annotations

from dataclasses import replace
import hashlib
import importlib.util
import json
from pathlib import Path
from unittest.mock import patch

import pytest

from scripts.run_scd01_16pair import (
    SCD01ScheduledRequest,
    run_scd01_16pair_v1,
)

ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / "tests" / "fixtures" / "scd01_16pair"
BRIDGE_TEST = ROOT / "tests" / "test_scd01_runtime_bridge_red.py"
PAIR_TEST = ROOT / "tests" / "test_scd01_governed_pair_red.py"
SHA = {
    "03-AB-SCHEDULE-DESIGN.json":
        "6ceae88c04a99e74ae80a3934f12fb27335f4db9038982599d84967d139d02f3",
    "REFERENCE-BR01-CHALLENGE-CORPUS.json":
        "d1a5b859e6c45e09bf1cefc1d7053ffb24b5dff74e160bb31d63acaf976f1ae8",
}


def _load_module(path: Path, name: str):
    if not path.is_file():
        raise RuntimeError(f"PRECONDITION_STOP: missing original source {path.name}")
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("PRECONDITION_STOP: cannot load existing test source")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _strict_pairs(pairs):
    value = {}
    for key, member in pairs:
        if key in value:
            raise ValueError("duplicate JSON member")
        value[key] = member
    return value


def _strict_constant(value: str):
    raise ValueError(f"non-finite JSON constant: {value}")


def _read_frozen(name: str) -> dict:
    path = FROZEN / name
    if not path.is_file():
        raise RuntimeError(f"PRECONDITION_STOP: missing frozen fixture {name}")
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SHA[name]:
        raise RuntimeError(f"PRECONDITION_STOP: SHA mismatch {name}")
    result = json.loads(
        raw,
        object_pairs_hook=_strict_pairs,
        parse_constant=_strict_constant,
    )
    if type(result) is not dict:
        raise RuntimeError(f"PRECONDITION_STOP: non-object JSON {name}")
    return result


def _canonical(value: object) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def _frozen_schedule() -> tuple[SCD01ScheduledRequest, ...]:
    corpus = _read_frozen("REFERENCE-BR01-CHALLENGE-CORPUS.json")
    schedule = _read_frozen("03-AB-SCHEDULE-DESIGN.json")
    if corpus.get("authority_effect") != "none":
        raise RuntimeError("PRECONDITION_STOP: corpus authority invalid")
    if schedule.get("authority_effect") != "none":
        raise RuntimeError("PRECONDITION_STOP: schedule authority invalid")
    cases = corpus.get("cases")
    requests = schedule.get("requests")
    if type(cases) is not list or len(cases) != 16:
        raise RuntimeError("PRECONDITION_STOP: corpus is not exactly 16 cases")
    if type(requests) is not list or len(requests) != 32:
        raise RuntimeError("PRECONDITION_STOP: schedule is not 32 requests")
    case_map = {}
    for case in cases:
        if type(case) is not dict or set(case) != {"id", "statement", "evidence"}:
            raise RuntimeError("PRECONDITION_STOP: case schema mismatch")
        cid = case["id"]
        if type(cid) is not str or cid in case_map:
            raise RuntimeError("PRECONDITION_STOP: duplicate/invalid case ID")
        case_map[cid] = case

    existing = _load_module(BRIDGE_TEST, "scd01_existing_frozen_pair_fixture")
    a, b = existing._frozen_pair()
    if a.model != "qwen3.5:9b" or b.model != a.model:
        raise RuntimeError("PRECONDITION_STOP: model mismatch")
    if a.system_prompt == b.system_prompt:
        raise RuntimeError("PRECONDITION_STOP: prompt arms identical")

    result: list[SCD01ScheduledRequest] = []
    seen: set[tuple[str, str]] = set()
    for record in requests:
        if type(record) is not dict:
            raise RuntimeError("PRECONDITION_STOP: malformed schedule record")
        case_id = record.get("case_id")
        arm = record.get("arm")
        ordinal = record.get("ordinal")
        if type(case_id) is not str or case_id not in case_map:
            raise RuntimeError("PRECONDITION_STOP: schedule references unknown case")
        if arm not in ("A", "B") or (case_id, arm) in seen:
            raise RuntimeError("PRECONDITION_STOP: duplicate/invalid schedule arm")
        if type(ordinal) is not int:
            raise RuntimeError("PRECONDITION_STOP: invalid schedule ordinal")
        seen.add((case_id, arm))

        case = case_map[case_id]
        visible = {"statement": case["statement"], "evidence": case["evidence"]}
        projected = _canonical(visible)
        digest = hashlib.sha256(projected).hexdigest()
        if record.get("model_visible_packet_sha256") != digest:
            raise RuntimeError(
                f"PRECONDITION_STOP: model-visible packet SHA mismatch {case_id}"
            )
        template = a if arm == "A" else b
        request = replace(
            template,
            prompt="BLIND_EVIDENCE_PACKET_JSON:\n" + projected.decode("utf-8"),
        )
        if case_id in request.prompt:
            raise RuntimeError("PRECONDITION_STOP: case identity leaked to prompt")
        result.append(SCD01ScheduledRequest(ordinal, case_id, arm, request))

    if len(seen) != 32:
        raise RuntimeError("PRECONDITION_STOP: schedule missing A/B arm")
    result.sort(key=lambda item: item.ordinal)
    return tuple(result)


def test_red_preconditions_original_frozen_16pair_material():
    scheduled = _frozen_schedule()
    existing = _load_module(PAIR_TEST, "scd01_existing_pair_runtime_fixture")
    runtime = existing._runtime()
    # The RED boundary itself validates 32 positions and 16 complete pairs.
    with patch.object(
        runtime, "capture_provenance", side_effect=AssertionError("unexpected provenance")
    ), patch(
        "malak.runtime.ollama_runtime.urlopen",
        side_effect=AssertionError("unexpected HTTP")
    ):
        result = run_scd01_16pair_v1(runtime=runtime, scheduled=scheduled)
    assert len(result) == 32
    assert all(row["status"] == "NOT_EXECUTED" for row in result)
    assert all(row["authority_effect"] == "none" for row in result)


def test_red_invalid_ordinal_rejected_without_side_effects():
    scheduled = _frozen_schedule()
    existing = _load_module(PAIR_TEST, "scd01_existing_pair_invalid_fixture")
    runtime = existing._runtime()
    duplicate = replace(scheduled[1], ordinal=scheduled[0].ordinal)
    with patch.object(
        runtime, "capture_provenance", side_effect=AssertionError("unexpected provenance")
    ), patch(
        "malak.runtime.ollama_runtime.urlopen",
        side_effect=AssertionError("unexpected HTTP")
    ):
        with pytest.raises(ValueError, match="duplicate ordinals"):
            run_scd01_16pair_v1(runtime=runtime, scheduled=(scheduled[0], duplicate, *scheduled[2:]))


def test_scd01_16pair_behavioral_red_authentic_runtime_requires_32_dispatches():
    """Expected RED: prepared inputs pass; real runtime sees zero of 32 calls."""
    scheduled = _frozen_schedule()
    existing = _load_module(PAIR_TEST, "scd01_existing_pair_behavior_fixture")
    runtime = existing._runtime()
    provenance = existing._provenance(existing._genuine_pair())
    captured: list[str] = []

    def transport(request, timeout):
        captured.append(request.full_url)
        return existing._SyntheticHTTP(request)

    with patch.object(
        runtime, "capture_provenance", return_value=provenance
    ) as snapshots, patch(
        "malak.runtime.ollama_runtime.urlopen", side_effect=transport
    ):
        result = run_scd01_16pair_v1(runtime=runtime, scheduled=scheduled)

    assert len(captured) == 32, (
        "SCD01_16PAIR_NOT_CONNECTED: expected 32 authentic runtime dispatches, "
        f"observed {len(captured)}"
    )
    assert snapshots.call_count == 96, (
        "SCD01_16PAIR_PROVENANCE_NOT_CONNECTED: expected 96 snapshots, "
        f"observed {snapshots.call_count}"
    )
    assert len(result) == 32
    assert all(row["status"] == "MODEL_OBSERVATION_ONLY" for row in result)
    assert all(row["authority_effect"] == "none" for row in result)
