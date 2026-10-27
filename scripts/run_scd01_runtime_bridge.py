"""SCD-01 runtime bridge: intentional RED-stage consumer boundary.

No model, network, oracle or scorer execution is possible at this stage.
The implementation is intentionally incomplete until separately authorized GREEN.
"""
from __future__ import annotations

from malak.core.conversation import ConversationRequest, ConversationResponse
from malak.runtime.ollama_runtime import OllamaRuntime


def dispatch_scd01_pair_v1(
    *,
    runtime: OllamaRuntime,
    pair: tuple[ConversationRequest, ConversationRequest],
) -> tuple[ConversationResponse, ...]:
    """Dispatch one authentic frozen A/B pair, NOT CONNECTED during RED."""
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
    # Deliberately no runtime.generate() until GREEN authorization.
    return ()
