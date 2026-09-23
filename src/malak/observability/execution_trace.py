from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Final, Iterable


TRACE_SCHEMA: Final[str] = "MALAK-EXECUTION-TRACE-EVENT/v0"
_SHA_RE = re.compile(r"^[0-9a-f]{40}$")

ALLOWED_EVENT_TYPES: Final[frozenset[str]] = frozenset(
    {
        "RUN_STARTED",
        "SCOPE_FROZEN",
        "EVIDENCE_PACKET_STARTED",
        "EVIDENCE_PACKET_READY",
        "COMPONENT_STARTED",
        "COMPONENT_COMPLETED",
        "COMPONENT_SKIPPED",
        "COMPONENT_FAILED",
        "GATE_EVALUATED",
        "TERMINAL_DISPOSITION",
        "ARTIFACT_FINALIZED",
        "RUN_STOPPED",
    }
)
ALLOWED_OUTCOMES: Final[frozenset[str]] = frozenset(
    {
        "STARTED",
        "SUCCEEDED",
        "FAILED",
        "INCONCLUSIVE",
        "SKIPPED",
    }
)
ALLOWED_REASON_CODES: Final[frozenset[str]] = frozenset(
    {
        "validation_failed",
        "baseline_mismatch",
        "required_evidence_missing",
        "unknown_reference",
        "component_error",
        "dependency_unavailable",
        "trace_write_failed",
        "artifact_validation_failed",
        "not_required_by_workflow",
        "precondition_not_met",
        "unresolved_contradiction",
        "policy_stop",
    }
)
_REASON_REQUIRED_OUTCOMES: Final[frozenset[str]] = frozenset(
    {"FAILED", "INCONCLUSIVE", "SKIPPED"}
)
_EVENT_OUTCOMES: Final[dict[str, frozenset[str]]] = {
    "RUN_STARTED": frozenset({"STARTED"}),
    "SCOPE_FROZEN": frozenset({"SUCCEEDED"}),
    "EVIDENCE_PACKET_STARTED": frozenset({"STARTED"}),
    "EVIDENCE_PACKET_READY": frozenset({"SUCCEEDED", "INCONCLUSIVE"}),
    "COMPONENT_STARTED": frozenset({"STARTED"}),
    "COMPONENT_COMPLETED": frozenset({"SUCCEEDED"}),
    "COMPONENT_SKIPPED": frozenset({"SKIPPED"}),
    "COMPONENT_FAILED": frozenset({"FAILED"}),
    "GATE_EVALUATED": frozenset({"SUCCEEDED", "FAILED", "INCONCLUSIVE"}),
    "TERMINAL_DISPOSITION": frozenset({"SUCCEEDED"}),
    "ARTIFACT_FINALIZED": frozenset({"SUCCEEDED"}),
    "RUN_STOPPED": frozenset({"SUCCEEDED"}),
}


@dataclass(frozen=True, slots=True)
class ExecutionTraceEvent:
    schema: str
    run_id: str
    sequence: int
    occurred_at: datetime
    baseline_commit: str
    task_id: str
    phase: str
    component: str
    event_type: str
    input_refs: tuple[str, ...]
    output_refs: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    outcome: str
    reason_code: str | None
    authority_effect: str

    def __post_init__(self) -> None:
        if self.schema != TRACE_SCHEMA:
            raise ValueError(f"schema must equal {TRACE_SCHEMA}")

        for field_name in (
            "run_id",
            "task_id",
            "phase",
            "component",
        ):
            _validate_identifier(field_name, getattr(self, field_name))

        if type(self.sequence) is not int:
            raise TypeError("sequence must be an integer")
        if self.sequence <= 0:
            raise ValueError("sequence must be greater than zero")

        if not _SHA_RE.fullmatch(self.baseline_commit):
            raise ValueError(
                "baseline_commit must be a lowercase 40-character Git SHA"
            )

        if not isinstance(self.occurred_at, datetime):
            raise TypeError("occurred_at must be a datetime")
        if self.occurred_at.tzinfo is None or self.occurred_at.utcoffset() is None:
            raise ValueError("occurred_at must be timezone-aware")
        if self.occurred_at.utcoffset() != UTC.utcoffset(self.occurred_at):
            raise ValueError("occurred_at must use UTC")

        if self.event_type not in ALLOWED_EVENT_TYPES:
            raise ValueError("event_type is not allowed")
        if self.outcome not in ALLOWED_OUTCOMES:
            raise ValueError("outcome is not allowed")
        if self.outcome not in _EVENT_OUTCOMES[self.event_type]:
            raise ValueError(
                "outcome is not valid for the selected event_type"
            )

        for field_name in ("input_refs", "output_refs", "evidence_refs"):
            _validate_refs(field_name, getattr(self, field_name))

        if self.outcome in _REASON_REQUIRED_OUTCOMES:
            if self.reason_code is None:
                raise ValueError(
                    "reason_code is required for failed, inconclusive or skipped outcomes"
                )
        elif self.reason_code is not None:
            raise ValueError(
                "reason_code must be absent for started or succeeded outcomes"
            )

        if (
            self.reason_code is not None
            and self.reason_code not in ALLOWED_REASON_CODES
        ):
            raise ValueError("reason_code is not allowed")

        if self.authority_effect != "none":
            raise ValueError("authority_effect must equal 'none'")


class ExecutionTrace:
    def __init__(
        self,
        *,
        run_id: str,
        baseline_commit: str,
        initial_refs: Iterable[str] = (),
    ) -> None:
        _validate_identifier("run_id", run_id)
        if not _SHA_RE.fullmatch(baseline_commit):
            raise ValueError(
                "baseline_commit must be a lowercase 40-character Git SHA"
            )

        initial = tuple(initial_refs)
        _validate_refs("initial_refs", initial)
        if len(set(initial)) != len(initial):
            raise ValueError("initial_refs must be unique")

        self._run_id = run_id
        self._baseline_commit = baseline_commit
        self._known_refs = set(initial)
        self._events: list[ExecutionTraceEvent] = []

    @property
    def events(self) -> tuple[ExecutionTraceEvent, ...]:
        return tuple(self._events)

    def append(self, event: ExecutionTraceEvent) -> None:
        if not isinstance(event, ExecutionTraceEvent):
            raise TypeError("event must be an ExecutionTraceEvent")
        if event.run_id != self._run_id:
            raise ValueError("event run_id does not match trace")
        if event.baseline_commit != self._baseline_commit:
            raise ValueError("event baseline_commit does not match trace")

        if self._events and event.sequence <= self._events[-1].sequence:
            raise ValueError("event sequence must be strictly monotonic")

        consumed_refs = event.input_refs + event.evidence_refs
        unknown = tuple(
            ref for ref in consumed_refs if ref not in self._known_refs
        )
        if unknown:
            raise ValueError(f"event consumes unknown refs: {unknown}")

        if set(event.output_refs) & set(consumed_refs):
            raise ValueError("event output_refs cannot self-reference")
        duplicates = tuple(
            ref for ref in event.output_refs if ref in self._known_refs
        )
        if duplicates:
            raise ValueError(f"event duplicates known output refs: {duplicates}")

        self._events.append(event)
        self._known_refs.update(event.output_refs)


def project_component_path(
    events: Iterable[ExecutionTraceEvent],
) -> tuple[str, ...]:
    return tuple(
        event.component
        for event in events
        if event.event_type == "COMPONENT_STARTED"
    )


def write_execution_trace_jsonl(
    path: str | Path,
    events: Iterable[ExecutionTraceEvent],
) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)

    lines: list[str] = []
    for event in events:
        if not isinstance(event, ExecutionTraceEvent):
            raise TypeError("events must contain ExecutionTraceEvent values")
        payload = asdict(event)
        payload["occurred_at"] = event.occurred_at.isoformat().replace(
            "+00:00",
            "Z",
        )
        payload["input_refs"] = list(event.input_refs)
        payload["output_refs"] = list(event.output_refs)
        payload["evidence_refs"] = list(event.evidence_refs)
        lines.append(
            json.dumps(
                payload,
                ensure_ascii=False,
                separators=(",", ":"),
                sort_keys=True,
            )
        )

    target.write_text(
        "".join(f"{line}\n" for line in lines),
        encoding="utf-8",
        newline="\n",
    )


def read_execution_trace_jsonl(
    path: str | Path,
) -> tuple[ExecutionTraceEvent, ...]:
    target = Path(path)
    events: list[ExecutionTraceEvent] = []

    for raw_line in target.read_text(encoding="utf-8").splitlines():
        try:
            payload = json.loads(raw_line)
        except json.JSONDecodeError as exc:
            raise ValueError("trace JSONL contains invalid JSON") from exc

        if not isinstance(payload, dict):
            raise ValueError("trace JSONL event must be an object")

        expected_keys = {
            "schema",
            "run_id",
            "sequence",
            "occurred_at",
            "baseline_commit",
            "task_id",
            "phase",
            "component",
            "event_type",
            "input_refs",
            "output_refs",
            "evidence_refs",
            "outcome",
            "reason_code",
            "authority_effect",
        }
        if set(payload) != expected_keys:
            raise ValueError("trace JSONL event keys mismatch")

        occurred_at_raw = payload["occurred_at"]
        if not isinstance(occurred_at_raw, str):
            raise ValueError("occurred_at must be a string in JSONL")
        try:
            occurred_at = datetime.fromisoformat(
                occurred_at_raw.replace("Z", "+00:00")
            )
        except ValueError as exc:
            raise ValueError("occurred_at is invalid") from exc

        events.append(
            ExecutionTraceEvent(
                schema=payload["schema"],
                run_id=payload["run_id"],
                sequence=payload["sequence"],
                occurred_at=occurred_at,
                baseline_commit=payload["baseline_commit"],
                task_id=payload["task_id"],
                phase=payload["phase"],
                component=payload["component"],
                event_type=payload["event_type"],
                input_refs=_json_refs(payload["input_refs"], "input_refs"),
                output_refs=_json_refs(payload["output_refs"], "output_refs"),
                evidence_refs=_json_refs(
                    payload["evidence_refs"],
                    "evidence_refs",
                ),
                outcome=payload["outcome"],
                reason_code=payload["reason_code"],
                authority_effect=payload["authority_effect"],
            )
        )

    if not events:
        return ()

    replay = ExecutionTrace(
        run_id=events[0].run_id,
        baseline_commit=events[0].baseline_commit,
        initial_refs=("task:input",),
    )
    for event in events:
        replay.append(event)

    return replay.events


def _json_refs(value: object, field_name: str) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise ValueError(f"{field_name} must be a JSON array")
    refs = tuple(value)
    _validate_refs(field_name, refs)
    return refs


def _validate_identifier(field_name: str, value: object) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    if not value:
        raise ValueError(f"{field_name} must not be empty")
    if value != value.strip():
        raise ValueError(
            f"{field_name} must not contain surrounding whitespace"
        )
    if any(ord(character) < 32 or ord(character) == 127 for character in value):
        raise ValueError(f"{field_name} contains forbidden control characters")


def _validate_refs(field_name: str, value: object) -> None:
    if not isinstance(value, tuple):
        raise TypeError(f"{field_name} must be a tuple")

    seen: set[str] = set()
    for ref in value:
        _validate_identifier(field_name, ref)
        if ref in seen:
            raise ValueError(f"{field_name} contains duplicate refs")
        seen.add(ref)
