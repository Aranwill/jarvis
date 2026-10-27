"""SCD-01 provenance-bound pair coordinator: intentional behavioral RED.

Runtime/contract are genuine Malak types. The RED candidate is disconnected:
zero introspection, zero HTTP, zero model calls. GREEN requires Owner approval.
This is NOT an entrypoint for the 32-request pilot.
"""
from __future__ import annotations

from malak.core.conversation import ConversationRequest
from malak.runtime.ollama_runtime import OllamaRuntime


def run_scd01_governed_pair_v1(
    *,
    runtime: OllamaRuntime,
    pair: tuple[ConversationRequest, ConversationRequest],
) -> tuple[dict[str, object], ...]:
    """Return bounded candidate observations from a provenance-checked pair."""
    if not isinstance(runtime, OllamaRuntime):
        raise TypeError("SCD-01 requires the authentic OllamaRuntime")
    if (
        type(pair) is not tuple
        or len(pair) != 2
        or any(not isinstance(req, ConversationRequest) for req in pair)
    ):
        raise TypeError("SCD-01 requires exactly two ConversationRequest items")

    # RED: provenance snapshots and runtime dispatch are deliberately absent.
    # A real setup/fixture failure must not count as a successful behavioral RED.
    return ()
