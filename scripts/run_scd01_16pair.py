"""SCD01-16PAIR/v1 — offline, provenance-bound scheduled observation runner.

Experiment only. This is NOT a live model execution entrypoint, an oracle,
scorer, authority transition, or final-response component. Every HTTP call
must be intercepted through the required offline_transport argument.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Callable
from unittest.mock import patch

from malak.core.conversation import ConversationRequest
from malak.runtime.ollama_runtime import OllamaRuntime
from malak.runtime.runtime_provenance import RuntimeModelProvenance
from scripts.run_scd01_governed_pair import _load_existing_script
from scripts.run_scd01_runtime_bridge import validate_scd01_pair_v1


ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / "tests" / "fixtures" / "scd01_16pair"
FROZEN_SHA256 = {
    "03-AB-SCHEDULE-DESIGN.json":
        "6ceae88c04a99e74ae80a3934f12fb27335f4db9038982599d84967d139d02f3",
    "REFERENCE-BR01-CHALLENGE-CORPUS.json":
        "d1a5b859e6c45e09bf1cefc1d7053ffb24b5dff74e160bb31d63acaf976f1ae8",
}
PROMPT_SHA256 = {
    "A": "22b29f8841473fdcea30fa531d6b9d7535eb1abbdecb57fca44c52df477a67ab",
    "B": "82e775aba848baa49c65d9f2926e6f631c9bd5b3dcf6dd5fe4ec4390bd774076",
}


@dataclass(frozen=True, slots=True)
class SCD01ScheduledRequest:
    ordinal: int
    case_id: str
    arm: str
    request: ConversationRequest


class SCD0116PairAborted(RuntimeError):
    """Fail-closed stop; rows are non-authoritative and contain no model output."""

    def __init__(self, *, rows: tuple[dict[str, object], ...]) -> None:
        self.rows = rows
        self.status = "INCONCLUSIVE"
        self.authority_effect = "none"
        super().__init__("SCD01_16PAIR_ABORTED: no experiment result admitted")


def _reject_duplicate_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("SCD01 frozen JSON contains duplicate keys")
        result[key] = value
    return result


def _reject_nonfinite(value: str) -> None:
    raise ValueError(f"SCD01 frozen JSON has nonfinite value: {value}")


def _read_frozen(name: str) -> dict[str, object]:
    source = FROZEN / name
    if not source.is_file():
        raise RuntimeError(f"SCD01_FROZEN_MISSING: {name}")
    raw = source.read_bytes()
    if hashlib.sha256(raw).hexdigest() != FROZEN_SHA256[name]:
        raise RuntimeError(f"SCD01_FROZEN_SHA_MISMATCH: {name}")
    value = json.loads(
        raw,
        object_pairs_hook=_reject_duplicate_pairs,
        parse_constant=_reject_nonfinite,
    )
    if type(value) is not dict:
        raise ValueError("SCD01 frozen document root must be an object")
    return value


def _canonical(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True,
        separators=(",", ":"), allow_nan=False,
    ).encode("utf-8")


def _validate_frozen_plan(
    *, runtime: OllamaRuntime,
    scheduled: tuple[SCD01ScheduledRequest, ...],
) -> None:
    """Validate all 32 positions and exact frozen bytes before any inference."""
    if not isinstance(runtime, OllamaRuntime):
        raise TypeError("runtime must be the existing OllamaRuntime")
    if type(scheduled) is not tuple or len(scheduled) != 32:
        raise ValueError("SCD01-16PAIR requires exactly 32 scheduled requests")

    ordinal_values: list[int] = []
    cases: dict[str, dict[str, ConversationRequest]] = {}
    for item in scheduled:
        if type(item) is not SCD01ScheduledRequest:
            raise TypeError("scheduled entries must be SCD01ScheduledRequest")
        if type(item.ordinal) is not int or item.ordinal < 0:
            raise ValueError("scheduled ordinal must be a nonnegative integer")
        if type(item.case_id) is not str or not item.case_id.strip():
            raise ValueError("scheduled case_id must be nonempty")
        if item.arm not in ("A", "B"):
            raise ValueError("scheduled arm must be A or B")
        if not isinstance(item.request, ConversationRequest):
            raise TypeError("scheduled request must be a real ConversationRequest")
        ordinal_values.append(item.ordinal)
        arms = cases.setdefault(item.case_id, {})
        if item.arm in arms:
            raise ValueError("SCD01-16PAIR duplicate case/arm")
        arms[item.arm] = item.request

    if len(set(ordinal_values)) != 32:
        raise ValueError("SCD01-16PAIR duplicate ordinals")
    if ordinal_values != sorted(ordinal_values):
        raise ValueError("SCD01-16PAIR schedule is not in ordinal order")
    if len(cases) != 16:
        raise ValueError("SCD01-16PAIR requires exactly 16 distinct pairs")
    for arms in cases.values():
        if set(arms) != {"A", "B"}:
            raise ValueError("SCD01-16PAIR requires complete A/B pairs")
        validate_scd01_pair_v1(runtime=runtime, pair=(arms["A"], arms["B"]))

    # A caller cannot supply a different, yet syntactically comparable, plan.
    schedule = _read_frozen("03-AB-SCHEDULE-DESIGN.json")
    corpus = _read_frozen("REFERENCE-BR01-CHALLENGE-CORPUS.json")
    if schedule.get("authority_effect") != "none" or corpus.get("authority_effect") != "none":
        raise ValueError("SCD01 frozen material must be authority-free")
    rows = schedule.get("requests")
    case_rows = corpus.get("cases")
    if type(rows) is not list or len(rows) != 32:
        raise ValueError("SCD01 frozen schedule is not 32 requests")
    if type(case_rows) is not list or len(case_rows) != 16:
        raise ValueError("SCD01 frozen corpus is not 16 cases")
    case_map: dict[str, dict[str, object]] = {}
    for case in case_rows:
        if type(case) is not dict or set(case) != {"id", "statement", "evidence"}:
            raise ValueError("SCD01 frozen case shape changed")
        cid = case["id"]
        if type(cid) is not str or not cid or cid in case_map:
            raise ValueError("SCD01 frozen case identity invalid")
        case_map[cid] = case

    e3 = _load_existing_script("run_e3_governed_blind_assessor_ollama_experiment")
    if not isinstance(e3.EXACT_SYSTEM_PROMPT, str):
        raise ValueError("SCD01 original E3 prompt missing")
    if hashlib.sha256(e3.EXACT_SYSTEM_PROMPT.encode("utf-8")).hexdigest() != PROMPT_SHA256["A"]:
        raise ValueError("SCD01 original E3 prompt identity mismatch")

    for expected, actual in zip(rows, scheduled, strict=True):
        if type(expected) is not dict or not {"ordinal", "case_id", "arm", "model_visible_packet_sha256"}.issubset(expected):
            raise ValueError("SCD01 frozen schedule row shape invalid")
        if (expected["ordinal"], expected["case_id"], expected["arm"]) != (
            actual.ordinal, actual.case_id, actual.arm
        ):
            raise ValueError("SCD01 schedule ordinal/arm binding mismatch")
        case = case_map.get(actual.case_id)
        if case is None:
            raise ValueError("SCD01 schedule references absent case")
        packet = _canonical({"statement": case["statement"], "evidence": case["evidence"]})
        if hashlib.sha256(packet).hexdigest() != expected["model_visible_packet_sha256"]:
            raise ValueError("SCD01 model-visible packet digest mismatch")
        request = actual.request
        if request.prompt != e3.EXACT_USER_PREFIX + packet.decode("utf-8"):
            raise ValueError("SCD01 model-visible prompt mismatch")
        if actual.case_id in request.prompt:
            raise ValueError("SCD01 blind case identity leakage")
        if request.model != "qwen3.5:9b":
            raise ValueError("SCD01 model identity mismatch")
        if request.response_json_schema != e3.EXACT_RESPONSE_JSON_SCHEMA:
            raise ValueError("SCD01 E3 response schema mismatch")
        if request.generation_contract != e3._generation_contract():
            raise ValueError("SCD01 E3 generation contract mismatch")
        if request.system_prompt is None or hashlib.sha256(
            request.system_prompt.encode("utf-8")
        ).hexdigest() != PROMPT_SHA256[actual.arm]:
            raise ValueError("SCD01 frozen A/B prompt identity mismatch")
        if actual.arm == "A" and request.system_prompt != e3.EXACT_SYSTEM_PROMPT:
            raise ValueError("SCD01 source E3 prompt mismatch")
        if request.history != ():
            raise ValueError("SCD01 history is not empty")


def _abort_rows(
    scheduled: tuple[SCD01ScheduledRequest, ...],
    observed: dict[tuple[str, str], dict[str, object]],
    failed: tuple[str, str],
) -> tuple[dict[str, object], ...]:
    result: list[dict[str, object]] = []
    for item in scheduled:
        key = (item.case_id, item.arm)
        if key == failed:
            status = "INCONCLUSIVE"
        elif key in observed:
            status = "OBSERVATION_WITHHELD"
        else:
            status = "NOT_EXECUTED"
        result.append({
            "ordinal": item.ordinal,
            "case_id": item.case_id,
            "arm": item.arm,
            "status": status,
            "authority_effect": "none",
        })
    return tuple(result)


def run_scd01_16pair_v1(
    *,
    runtime: OllamaRuntime,
    scheduled: tuple[SCD01ScheduledRequest, ...],
    offline_transport: Callable[..., object] | None = None,
) -> tuple[dict[str, object], ...]:
    """Execute the exact frozen schedule offline, in ordinal order.

    The offline transport is mandatory. No scores, oracle, persistence, retry,
    or live-model path. On failure, raises SCD0116PairAborted with exactly 32
    sanitized positions; no partial observations are returned to the caller.
    """
    _validate_frozen_plan(runtime=runtime, scheduled=scheduled)
    if not callable(offline_transport):
        raise PermissionError("SCD01_LIVE_INFERENCE_NOT_AUTHORIZED")

    e3 = _load_existing_script("run_e3_governed_blind_assessor_ollama_experiment")
    model = scheduled[0].request.model
    contract = scheduled[0].request.generation_contract
    assert model is not None and contract is not None

    first_seen: set[str] = set()
    observed: dict[tuple[str, str], dict[str, object]] = {}
    stable_tuple: tuple[object, ...] | None = None
    drift_state = {"invalid": False}

    # Each case: baseline, before/after its first arm, before/after its second
    # arm, final = six snapshots. Interleaved A/B order is preserved exactly.
    def capture_initial() -> RuntimeModelProvenance:
        nonlocal stable_tuple
        snapshot = runtime.capture_provenance(model, generation_contract=contract)
        if not isinstance(snapshot, RuntimeModelProvenance):
            raise TypeError("SCD01 provenance type mismatch")
        e3._validate_baseline_provenance(snapshot, model=model)
        identity = e3._provenance_tuple(snapshot)
        if stable_tuple is None:
            stable_tuple = identity
        elif identity != stable_tuple:
            raise RuntimeError("SCD01 cross-pair provenance drift detected")
        return snapshot

    def capture_stable() -> None:
        assert stable_tuple is not None
        snapshot = e3._capture_stable(
            runtime, model=model, contract=contract,
            baseline_tuple=stable_tuple, drift_state=drift_state,
        )
        if not isinstance(snapshot, RuntimeModelProvenance):
            raise TypeError("SCD01 provenance type mismatch")
        e3._validate_baseline_provenance(snapshot, model=model)

    # Defense-in-depth: even accidental direct calls cannot access a live
    # network through OllamaRuntime.urlopen without the injected test seam.
    with patch("malak.runtime.ollama_runtime.urlopen", side_effect=offline_transport):
        for item in scheduled:
            key = (item.case_id, item.arm)
            try:
                if item.case_id not in first_seen:
                    capture_initial()
                    first_seen.add(item.case_id)
                capture_stable()  # before this scheduled request
                response = None
                generation_error: Exception | None = None
                try:
                    response = runtime.generate(item.request)
                except Exception as exc:
                    generation_error = exc
                # Preserve E3 temporal checks even after transport failure.
                # If provenance drifted, that takes precedence over the HTTP error.
                capture_stable()  # after this scheduled request, success or error
                if generation_error is not None:
                    raise generation_error
                if response is None:
                    raise RuntimeError("SCD01 runtime returned no response")
                if response.model != model or response.provider != "ollama":
                    raise ValueError("SCD01 Ollama response identity mismatch")
                parsed = e3.parse_model_assessor_output_v0(response.content)
                if not e3._model_output_pair_is_valid_v0(parsed):
                    raise ValueError("SCD01 E3 outcome/reason pairing invalid")
                observed[key] = {
                    "ordinal": item.ordinal,
                    "case_id": item.case_id,
                    "arm": item.arm,
                    "status": "MODEL_OBSERVATION_ONLY",
                    "parsed": parsed,
                    "authority_effect": "none",
                }
                if sum(x[0] == item.case_id for x in observed) == 2:
                    capture_stable()  # final, after both arms
            except Exception as exc:
                raise SCD0116PairAborted(
                    rows=_abort_rows(scheduled, observed, key)
                ) from exc

    if len(observed) != 32 or len(first_seen) != 16 or drift_state["invalid"]:
        # This check does not reinterpret incomplete evidence as success.
        raise SCD0116PairAborted(
            rows=_abort_rows(scheduled, observed, ("", ""))
        )
    return tuple(observed[(item.case_id, item.arm)] for item in scheduled)
