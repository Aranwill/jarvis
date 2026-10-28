"""SCD01-16PAIR/v1: RED-only fail-closed orchestration boundary.

This is deliberately NOT a production coordinator. The validated frozen plan
currently yields NOT_EXECUTED rows. No generation, network, scoring, state
promotion or authority is permitted in this RED candidate.
"""
from __future__ import annotations

from dataclasses import dataclass

from malak.core.conversation import ConversationRequest
from malak.runtime.ollama_runtime import OllamaRuntime

from scripts.run_scd01_runtime_bridge import validate_scd01_pair_v1


@dataclass(frozen=True, slots=True)
class SCD01ScheduledRequest:
    ordinal: int
    case_id: str
    arm: str
    request: ConversationRequest


def _validate_frozen_plan(
    *,
    runtime: OllamaRuntime,
    scheduled: tuple[SCD01ScheduledRequest, ...],
) -> None:
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
        if not isinstance(item.case_id, str) or not item.case_id.strip():
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


def run_scd01_16pair_v1(
    *,
    runtime: OllamaRuntime,
    scheduled: tuple[SCD01ScheduledRequest, ...],
) -> tuple[dict[str, object], ...]:
    """RED boundary: preserve all 32 positions WITHOUT dispatching.

    GREEN must later replace this NOT_EXECUTED-only behavior after separate
    Owner authorization and governed RED admission. The behavioral test must
    currently fail because this coordinator never calls the existing pair
    implementation. No retry, no inferred classification, no model authority.
    """
    _validate_frozen_plan(runtime=runtime, scheduled=scheduled)
    return tuple(
        {
            "ordinal": item.ordinal,
            "case_id": item.case_id,
            "arm": item.arm,
            "status": "NOT_EXECUTED",
            "authority_effect": "none",
        }
        for item in scheduled
    )
