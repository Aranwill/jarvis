"""SCD-01 experimental A/B bridge — minimal GREEN for governed transport.

This adapter delegates to the existing OllamaRuntime without introducing a
second runtime, parser, scorer, or source of authority. Callers must provide
a frozen, comparable pair and separately authorize any live inference.
"""
from __future__ import annotations

from malak.core.conversation import ConversationRequest, ConversationResponse
from malak.runtime.ollama_runtime import OllamaRuntime


def validate_scd01_pair_v1(
    *,
    runtime: OllamaRuntime,
    pair: tuple[ConversationRequest, ConversationRequest],
) -> None:
    """Pure pre-dispatch validation, shared with the governed coordinator."""
    if not isinstance(runtime, OllamaRuntime):
        raise TypeError("runtime must be the existing OllamaRuntime")
    if (
        type(pair) is not tuple
        or len(pair) != 2
        or any(not isinstance(item, ConversationRequest) for item in pair)
    ):
        raise TypeError(
            "pair must contain exactly two genuine ConversationRequest instances"
        )

    a, b = pair
    if (
        not a.model
        or a.model != b.model
        or not a.prompt
        or a.prompt != b.prompt
        or a.response_json_schema is None
        or a.response_json_schema != b.response_json_schema
        or a.generation_contract is None
        or a.generation_contract != b.generation_contract
        or a.history != ()
        or b.history != ()
        or not a.system_prompt
        or not b.system_prompt
        or a.system_prompt == b.system_prompt
    ):
        raise ValueError(
            "SCD-01 requires comparable A/B requests with a single "
            "system-prompt difference and empty history"
        )


def dispatch_scd01_pair_v1(
    *,
    runtime: OllamaRuntime,
    pair: tuple[ConversationRequest, ConversationRequest],
) -> tuple[ConversationResponse, ...]:
    """Dispatch A then B through the authentic runtime with no retries."""
    validate_scd01_pair_v1(runtime=runtime, pair=pair)

    # No try/retry: any runtime error aborts the pair and propagates.
    # The caller remains responsible for provenance, parsing, evidence,
    # safe run accounting and independent scoring.
    a, b = pair
    return (runtime.generate(a), runtime.generate(b))
