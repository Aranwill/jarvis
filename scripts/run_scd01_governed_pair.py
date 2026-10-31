"""SCD-01 experimental provenance-bound pair: offline GREEN candidate.

Reuse the existing E3 provenance rules, E3 parser and OllamaRuntime. This
function is NOT the 16-pair/32-request governed experiment runner and does not
issue authority, persist evidence, or run an oracle. Tests intercept all I/O.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

from malak.core.conversation import ConversationRequest
from malak.runtime.ollama_runtime import OllamaRuntime
from malak.runtime.runtime_provenance import RuntimeModelProvenance


def _load_existing_script(name: str) -> ModuleType:
    """Load an exact developer-owned sibling script, never user-supplied input."""
    if name not in {
        "run_e3_governed_blind_assessor_ollama_experiment",
        "run_scd01_runtime_bridge",
    }:
        raise ValueError("unsupported Malāk source module")
    source = Path(__file__).resolve().parent / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"scd01_reuse_{name}", source)
    if spec is None or spec.loader is None:
        raise RuntimeError("SCD-01 governed source is unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_scd01_governed_pair_v1(
    *,
    runtime: OllamaRuntime,
    pair: tuple[ConversationRequest, ConversationRequest],
) -> tuple[dict[str, object], ...]:
    """Verify six provenance snapshots and return two candidate observations.

    Baseline, before A, after A, before B, after B, final. No retries,
    no partial successful pair, no scoring, and no model-derived authority.
    """
    bridge = _load_existing_script("run_scd01_runtime_bridge")
    bridge.validate_scd01_pair_v1(runtime=runtime, pair=pair)
    a, b = pair

    # Reuse E3's exact contract and model-output semantics, without editing E3.
    e3 = _load_existing_script(
        "run_e3_governed_blind_assessor_ollama_experiment"
    )
    contract = a.generation_contract
    if (
        contract != e3._generation_contract()
        or a.system_prompt != e3.EXACT_SYSTEM_PROMPT
        or a.response_json_schema != e3.EXACT_RESPONSE_JSON_SCHEMA
        or not a.prompt.startswith(e3.EXACT_USER_PREFIX)
    ):
        raise ValueError("SCD-01 pair does not match the existing E3 contract")
    assert contract is not None
    assert a.model is not None

    # No generation can occur until the full READY/TAG_DIGEST_BOUND baseline
    # has been admitted using E3's existing deterministic validator.
    baseline = runtime.capture_provenance(
        a.model, generation_contract=contract
    )
    if not isinstance(baseline, RuntimeModelProvenance):
        raise TypeError("SCD-01 baseline provenance is invalid")
    e3._validate_baseline_provenance(baseline, model=a.model)
    baseline_tuple = e3._provenance_tuple(baseline)
    drift_state = {"invalid": False}
    candidates: list[dict[str, object]] = []

    def checked_capture() -> None:
        # E3's stable tuple deliberately omits runtime_class. Re-admit each
        # snapshot using E3's complete validator to reject class drift too.
        snapshot = e3._capture_stable(
            runtime,
            model=a.model,
            contract=contract,
            baseline_tuple=baseline_tuple,
            drift_state=drift_state,
        )
        e3._validate_baseline_provenance(snapshot, model=a.model)

    for arm, request in (("A", a), ("B", b)):
        checked_capture()
        generation_error: Exception | None = None
        response = None
        try:
            response = runtime.generate(request)
        except Exception as exc:
            generation_error = exc

        # Check temporal identity even when the generation itself failed.
        # A drift error takes precedence over returning partial results.
        checked_capture()
        if generation_error is not None:
            raise generation_error
        assert response is not None
        if response.model != a.model or response.provider != "ollama":
            raise e3.LocalOllamaExperimentError(
                "SCD-01 response identity mismatch"
            )
        parsed = e3.parse_model_assessor_output_v0(response.content)
        if not e3._model_output_pair_is_valid_v0(parsed):
            raise e3.LocalOllamaExperimentError(
                "SCD-01 model outcome/reason pairing invalid"
            )
        candidates.append(
            {
                "arm": arm,
                "status": "MODEL_OBSERVATION_ONLY",
                "parsed": parsed,
                "authority_effect": "none",
            }
        )

    # A successful pair cannot be exposed before the final stability check.
    checked_capture()
    return tuple(candidates)
