from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from enum import Enum
from collections.abc import Callable
from pathlib import Path
from typing import Final

from malak.core.request import Request
from malak.infrastructure.repository_reader import GitRepositoryReader
from malak.observability.execution_trace import (
    TRACE_SCHEMA,
    ExecutionTrace,
    ExecutionTraceEvent,
    project_component_path,
    read_execution_trace_jsonl,
    write_execution_trace_jsonl,
)
from malak.observability.safe_diagnostic import (
    SafeDiagnosticEnvelope,
    build_safe_diagnostic,
    read_safe_diagnostics_jsonl,
    write_safe_diagnostics_jsonl,
)
from malak.services.self_review_evidence import (
    SelfReviewEvidencePacket,
    build_self_review_evidence_packet,
)


_RUN_SCHEMA: Final[str] = "MALAK-INTERNAL-INTERACTION-RUN/v0"
_ARTIFACT_SCHEMA: Final[str] = "MALAK-INTERNAL-INTERACTION-ATTESTATION/v0"
_WORKFLOW_VERSION: Final[str] = "internal-interaction-v0"
_MAX_COMPONENT_OUTPUT_BYTES: Final[int] = 256 * 1024
_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
_FOCUS_DIGEST_RE = re.compile(r"^[0-9a-f]{64}$")
_RUN_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
_FINDING_RE = re.compile(
    r"^\[A[1-9][0-9]*\] classification="
    r"(ALIGNED|PARTIAL|GAP|CONTRADICTION|UNRESOLVED)$",
    re.MULTILINE,
)
_ARTIFACT_PAYLOAD_FILES: Final[tuple[str, ...]] = (
    "assessment.json",
    "diagnostics.jsonl",
    "evidence.json",
    "manifest.json",
    "outcome.json",
    "trace.jsonl",
)
_EXPECTED_ARTIFACT_FILES: Final[frozenset[str]] = frozenset(
    (*_ARTIFACT_PAYLOAD_FILES, "attestation.json")
)


class TerminalDisposition(str, Enum):
    NO_CHANGE_RECOMMENDED = "NO_CHANGE_RECOMMENDED"
    HARDENING_PROPOSAL = "HARDENING_PROPOSAL"
    RESEARCH_REQUIRED = "RESEARCH_REQUIRED"
    DEFER = "DEFER"
    INCONCLUSIVE = "INCONCLUSIVE"


class _ComponentEnvelopeError(ValueError):
    def __init__(self, reason_code: str) -> None:
        super().__init__(reason_code)
        self.reason_code = reason_code


@dataclass(frozen=True, slots=True)
class _ComponentFocusEnvelope:
    focus_id: str
    complete: bool
    evidence_set_digest: str


@dataclass(frozen=True, slots=True)
class InternalInteractionResult:
    run_id: str
    baseline_commit: str
    disposition: TerminalDisposition
    component_path: tuple[str, ...]
    artifact_dir: Path
    trace_events: tuple[ExecutionTraceEvent, ...]
    authority_effect: str = "none"


class InternalInteractionRunner:
    def __init__(
        self,
        *,
        engineering,
        artifact_root: str | Path,
        runtime_name: str = "engineering_kernel_set",
        model: str | None = None,
        event_sink: Callable[[ExecutionTraceEvent], None] | None = None,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        required = (
            "baseline_commit",
            "kernels",
            "repository_reader",
            "knowledge_reader",
        )
        for attribute in required:
            if not hasattr(engineering, attribute):
                raise TypeError(
                    f"engineering must expose {attribute}"
                )

        if engineering.repository_reader.baseline_commit != engineering.baseline_commit:
            raise RuntimeError("engineering repository baseline mismatch")
        if engineering.knowledge_reader.baseline_commit != engineering.baseline_commit:
            raise RuntimeError("engineering knowledge baseline mismatch")

        if not isinstance(runtime_name, str) or not runtime_name.strip():
            raise ValueError("runtime_name must be a non-empty string")
        if runtime_name != runtime_name.strip():
            raise ValueError("runtime_name must not have surrounding whitespace")
        if model is not None:
            _validate_text("model", model)
        if event_sink is not None and not callable(event_sink):
            raise TypeError("event_sink must be callable")
        if clock is not None and not callable(clock):
            raise TypeError("clock must be callable")

        artifact_root_path = Path(artifact_root).expanduser()
        if (
            artifact_root_path.name != "internal_interaction"
            or artifact_root_path.parent.name != "runtime"
        ):
            raise ValueError(
                "artifact_root must end in runtime/internal_interaction"
            )

        repository_root = artifact_root_path.parent.parent
        boundary_reader = GitRepositoryReader(repository_root)
        if boundary_reader.baseline_commit != engineering.baseline_commit:
            raise RuntimeError(
                "artifact_root repository baseline does not match engineering"
            )
        if artifact_root_path.parent.is_symlink() or artifact_root_path.is_symlink():
            raise RuntimeError("artifact_root boundary must not use symlinks")

        self._engineering = engineering
        self._artifact_root = artifact_root_path
        self._repository_root = repository_root.resolve()
        self._runtime_name = runtime_name
        self._model = model
        self._event_sink = event_sink
        self._clock = clock if clock is not None else _utc_now

    def run(
        self,
        *,
        task_id: str,
        scope: str,
        external_validation_refs: tuple[str, ...],
        run_id: str,
        created_at: datetime,
    ) -> InternalInteractionResult:
        _validate_text("task_id", task_id)
        _validate_text("scope", scope)
        _validate_run_id(run_id)
        _validate_utc(created_at)

        baseline = self._engineering.baseline_commit
        if not _SHA_RE.fullmatch(baseline):
            raise ValueError("engineering baseline is not a supported Git SHA")

        trace = ExecutionTrace(
            run_id=run_id,
            baseline_commit=baseline,
            initial_refs=("task:input",),
        )
        sequence = 0
        diagnostics: list[SafeDiagnosticEnvelope] = []

        def record_diagnostic(
            *,
            exc: Exception,
            phase: str,
            component: str,
            reason_code: str = "component_error",
        ) -> str:
            if len(diagnostics) >= 9999:
                raise RuntimeError("diagnostic capacity exceeded")
            diagnostic_id = f"D{len(diagnostics) + 1:04d}"
            diagnostic = build_safe_diagnostic(
                exc=exc,
                repository_root=self._repository_root,
                diagnostic_id=diagnostic_id,
                run_id=run_id,
                baseline_commit=baseline,
                task_id=task_id,
                phase=phase,
                component=component,
                reason_code=reason_code,
            )
            diagnostics.append(diagnostic)
            return f"diagnostic:{diagnostic_id}"

        def emit(
            *,
            phase: str,
            component: str,
            event_type: str,
            input_refs: tuple[str, ...] = (),
            output_refs: tuple[str, ...] = (),
            evidence_refs: tuple[str, ...] = (),
            outcome: str,
            reason_code: str | None = None,
        ) -> ExecutionTraceEvent:
            nonlocal sequence
            sequence += 1
            occurred_at = self._clock()
            _validate_utc(occurred_at)
            event = ExecutionTraceEvent(
                schema=TRACE_SCHEMA,
                run_id=run_id,
                sequence=sequence,
                occurred_at=occurred_at,
                baseline_commit=baseline,
                task_id=task_id,
                phase=phase,
                component=component,
                event_type=event_type,
                input_refs=input_refs,
                output_refs=output_refs,
                evidence_refs=evidence_refs,
                outcome=outcome,
                reason_code=reason_code,
                authority_effect="none",
            )
            trace.append(event)
            if self._event_sink is not None:
                self._event_sink(event)
            return event

        emit(
            phase="run",
            component="internal_interaction",
            event_type="RUN_STARTED",
            output_refs=("run:manifest",),
            outcome="STARTED",
        )
        emit(
            phase="scope",
            component="internal_interaction",
            event_type="SCOPE_FROZEN",
            input_refs=("task:input",),
            output_refs=("scope:frozen",),
            outcome="SUCCEEDED",
        )
        emit(
            phase="evidence",
            component="self_review_evidence",
            event_type="EVIDENCE_PACKET_STARTED",
            input_refs=("scope:frozen",),
            outcome="STARTED",
        )

        packet = build_self_review_evidence_packet(
            repository_reader=self._engineering.repository_reader,
            knowledge_reader=self._engineering.knowledge_reader,
            external_validation_refs=external_validation_refs,
        )

        packet_ready = packet.status == "READY"
        emit(
            phase="evidence",
            component="self_review_evidence",
            event_type="EVIDENCE_PACKET_READY",
            input_refs=("scope:frozen",),
            output_refs=("evidence:packet",),
            outcome="SUCCEEDED" if packet_ready else "INCONCLUSIVE",
            reason_code=None if packet_ready else "required_evidence_missing",
        )

        assessment: dict[str, object] = {
            "inspection_status": "NOT_RUN",
            "analysis_status": "NOT_RUN",
            "finding_classifications": [],
            "proposal_status": "NOT_RUN",
            "operational_rationale": [],
            "component_outputs": {
                "engineering_inspect": None,
                "engineering_analyze": None,
                "engineering_propose": None,
            },
            "authority_effect": "none",
        }
        terminal_refs: tuple[str, ...] = ("evidence:packet",)

        if not packet_ready:
            for component in (
                "engineering_inspect",
                "engineering_analyze",
                "engineering_propose",
            ):
                emit(
                    phase="engineering",
                    component=component,
                    event_type="COMPONENT_SKIPPED",
                    input_refs=("evidence:packet",),
                    outcome="SKIPPED",
                    reason_code="precondition_not_met",
                )
            disposition = TerminalDisposition.INCONCLUSIVE
            assessment["operational_rationale"] = [
                "mandatory self-review evidence packet is incomplete"
            ]
        else:
            disposition, terminal_refs = self._run_engineering(
                scope=scope,
                run_id=run_id,
                trace_emit=emit,
                assessment=assessment,
                record_diagnostic=record_diagnostic,
            )

        emit(
            phase="decision",
            component="internal_interaction",
            event_type="TERMINAL_DISPOSITION",
            input_refs=terminal_refs,
            output_refs=("outcome:terminal",),
            outcome="SUCCEEDED",
        )

        artifact_dir = self._artifact_root / run_id
        artifact_dir.mkdir(parents=True, exist_ok=False)

        manifest = {
            "schema": _RUN_SCHEMA,
            "run_id": run_id,
            "task_id": task_id,
            "created_at": created_at.isoformat().replace("+00:00", "Z"),
            "baseline_commit": baseline,
            "workflow_version": _WORKFLOW_VERSION,
            "runtime_name": self._runtime_name,
            "model": self._model,
            "scope": scope,
            "authority_effect": "none",
        }
        evidence_payload = _packet_payload(packet)
        outcome_payload = {
            "schema": "MALAK-INTERNAL-INTERACTION-OUTCOME/v0",
            "run_id": run_id,
            "baseline_commit": baseline,
            "disposition": disposition.value,
            "authority_effect": "none",
        }

        _write_json(artifact_dir / "manifest.json", manifest)
        _write_json(artifact_dir / "evidence.json", evidence_payload)
        _write_json(artifact_dir / "assessment.json", assessment)
        _write_json(artifact_dir / "outcome.json", outcome_payload)
        write_safe_diagnostics_jsonl(
            artifact_dir / "diagnostics.jsonl",
            diagnostics,
        )

        emit(
            phase="artifact",
            component="internal_interaction",
            event_type="ARTIFACT_FINALIZED",
            input_refs=("outcome:terminal",),
            output_refs=("artifact:set",),
            outcome="SUCCEEDED",
        )
        emit(
            phase="run",
            component="internal_interaction",
            event_type="RUN_STOPPED",
            input_refs=("artifact:set",),
            outcome="SUCCEEDED",
        )

        write_execution_trace_jsonl(
            artifact_dir / "trace.jsonl",
            trace.events,
        )
        _write_attestation(
            artifact_dir=artifact_dir,
            run_id=run_id,
            baseline_commit=baseline,
        )
        validate_internal_interaction_artifacts(artifact_dir)

        return InternalInteractionResult(
            run_id=run_id,
            baseline_commit=baseline,
            disposition=disposition,
            component_path=project_component_path(trace.events),
            artifact_dir=artifact_dir,
            trace_events=trace.events,
            authority_effect="none",
        )

    def _run_engineering(
        self,
        *,
        scope: str,
        run_id: str,
        trace_emit,
        assessment: dict[str, object],
        record_diagnostic,
    ) -> tuple[TerminalDisposition, tuple[str, ...]]:
        request = Request(content=scope, session_id=run_id)

        trace_emit(
            phase="engineering",
            component="engineering_inspect",
            event_type="COMPONENT_STARTED",
            input_refs=("evidence:packet",),
            outcome="STARTED",
        )
        try:
            inspect_response = self._engineering.kernels["inspect"].receive(
                request
            )
        except Exception as exc:
            diagnostic_ref = record_diagnostic(
                exc=exc,
                phase="engineering",
                component="engineering_inspect",
            )
            trace_emit(
                phase="engineering",
                component="engineering_inspect",
                event_type="COMPONENT_FAILED",
                input_refs=("evidence:packet",),
                output_refs=(diagnostic_ref,),
                outcome="FAILED",
                reason_code="component_error",
            )
            self._skip_following_components(
                trace_emit,
                ("engineering_analyze", "engineering_propose"),
            )
            assessment["operational_rationale"] = [
                "engineering inspect failed"
            ]
            return (
                TerminalDisposition.INCONCLUSIVE,
                ("evidence:packet",),
            )

        try:
            inspection_status = _component_envelope_status(
                inspect_response.content,
                expected_baseline=self._engineering.baseline_commit,
            )
            inspection_focus = _component_focus_envelope(
                inspect_response.content,
            )
        except _ComponentEnvelopeError as exc:
            trace_emit(
                phase="engineering",
                component="engineering_inspect",
                event_type="COMPONENT_FAILED",
                input_refs=("evidence:packet",),
                outcome="FAILED",
                reason_code=exc.reason_code,
            )
            self._skip_following_components(
                trace_emit,
                ("engineering_analyze", "engineering_propose"),
            )
            assessment["operational_rationale"] = [
                "engineering inspect envelope validation failed"
            ]
            return (
                TerminalDisposition.INCONCLUSIVE,
                ("evidence:packet",),
            )

        assessment["inspection_status"] = inspection_status
        assessment["component_outputs"]["engineering_inspect"] = (
            inspect_response.content
        )
        trace_emit(
            phase="engineering",
            component="engineering_inspect",
            event_type="COMPONENT_COMPLETED",
            input_refs=("evidence:packet",),
            output_refs=("engineering:inspect",),
            outcome="SUCCEEDED",
        )

        if inspection_focus is not None:
            assessment["focus_id"] = inspection_focus.focus_id
            assessment["focus_complete"] = inspection_focus.complete
            assessment["evidence_set_digest"] = (
                inspection_focus.evidence_set_digest
            )
            if not inspection_focus.complete:
                self._skip_following_components(
                    trace_emit,
                    ("engineering_analyze", "engineering_propose"),
                )
                assessment["operational_rationale"] = [
                    "governed engineering focus evidence is incomplete"
                ]
                return (
                    TerminalDisposition.INCONCLUSIVE,
                    ("engineering:inspect",),
                )

        if inspection_status != "GROUNDED":
            self._skip_following_components(
                trace_emit,
                ("engineering_analyze", "engineering_propose"),
            )
            assessment["operational_rationale"] = [
                "engineering inspection is not grounded"
            ]
            return (
                TerminalDisposition.INCONCLUSIVE,
                ("engineering:inspect",),
            )

        trace_emit(
            phase="engineering",
            component="engineering_analyze",
            event_type="COMPONENT_STARTED",
            input_refs=("evidence:packet",),
            outcome="STARTED",
        )
        try:
            analyze_response = self._engineering.kernels["analyze"].receive(
                request
            )
        except Exception as exc:
            diagnostic_ref = record_diagnostic(
                exc=exc,
                phase="engineering",
                component="engineering_analyze",
            )
            trace_emit(
                phase="engineering",
                component="engineering_analyze",
                event_type="COMPONENT_FAILED",
                input_refs=("evidence:packet",),
                output_refs=(diagnostic_ref,),
                outcome="FAILED",
                reason_code="component_error",
            )
            self._skip_following_components(
                trace_emit,
                ("engineering_propose",),
            )
            assessment["operational_rationale"] = [
                "engineering analysis failed"
            ]
            return (
                TerminalDisposition.INCONCLUSIVE,
                ("evidence:packet",),
            )

        try:
            analysis_status = _component_envelope_status(
                analyze_response.content,
                expected_baseline=self._engineering.baseline_commit,
            )
            analysis_focus = _component_focus_envelope(
                analyze_response.content,
            )
            _validate_focus_continuity(
                inspection_focus,
                analysis_focus,
            )
        except _ComponentEnvelopeError as exc:
            trace_emit(
                phase="engineering",
                component="engineering_analyze",
                event_type="COMPONENT_FAILED",
                input_refs=("evidence:packet",),
                outcome="FAILED",
                reason_code=exc.reason_code,
            )
            self._skip_following_components(
                trace_emit,
                ("engineering_propose",),
            )
            assessment["operational_rationale"] = [
                "engineering analysis envelope validation failed"
            ]
            return (
                TerminalDisposition.INCONCLUSIVE,
                ("evidence:packet",),
            )

        classifications = tuple(
            _FINDING_RE.findall(analyze_response.content)
        )
        assessment["analysis_status"] = analysis_status
        assessment["finding_classifications"] = list(classifications)
        assessment["component_outputs"]["engineering_analyze"] = (
            analyze_response.content
        )

        trace_emit(
            phase="engineering",
            component="engineering_analyze",
            event_type="COMPONENT_COMPLETED",
            input_refs=("evidence:packet",),
            output_refs=("engineering:analyze",),
            outcome="SUCCEEDED",
        )

        if analysis_status != "GROUNDED":
            self._skip_following_components(
                trace_emit,
                ("engineering_propose",),
            )
            assessment["operational_rationale"] = [
                "engineering analysis is not grounded"
            ]
            return (
                TerminalDisposition.INCONCLUSIVE,
                ("engineering:analyze",),
            )

        if any(
            classification in {"CONTRADICTION", "UNRESOLVED"}
            for classification in classifications
        ):
            self._skip_following_components(
                trace_emit,
                ("engineering_propose",),
            )
            assessment["operational_rationale"] = [
                "analysis contains unresolved or contradictory findings"
            ]
            return (
                TerminalDisposition.INCONCLUSIVE,
                ("engineering:analyze",),
            )

        actionable = any(
            classification in {"GAP", "PARTIAL"}
            for classification in classifications
        )
        if not actionable:
            trace_emit(
                phase="engineering",
                component="engineering_propose",
                event_type="COMPONENT_SKIPPED",
                input_refs=("evidence:packet",),
                outcome="SKIPPED",
                reason_code="not_required_by_workflow",
            )
            assessment["operational_rationale"] = [
                "analysis found no material actionable gap"
            ]
            return (
                TerminalDisposition.NO_CHANGE_RECOMMENDED,
                ("engineering:analyze",),
            )

        trace_emit(
            phase="engineering",
            component="engineering_propose",
            event_type="COMPONENT_STARTED",
            input_refs=("evidence:packet",),
            outcome="STARTED",
        )
        try:
            propose_response = self._engineering.kernels["propose"].receive(
                request
            )
        except Exception as exc:
            diagnostic_ref = record_diagnostic(
                exc=exc,
                phase="engineering",
                component="engineering_propose",
            )
            trace_emit(
                phase="engineering",
                component="engineering_propose",
                event_type="COMPONENT_FAILED",
                input_refs=("evidence:packet",),
                output_refs=(diagnostic_ref,),
                outcome="FAILED",
                reason_code="component_error",
            )
            assessment["operational_rationale"] = [
                "engineering proposal failed"
            ]
            return (
                TerminalDisposition.INCONCLUSIVE,
                ("engineering:analyze",),
            )

        try:
            proposal_status = _component_envelope_status(
                propose_response.content,
                expected_baseline=self._engineering.baseline_commit,
            )
            proposal_focus = _component_focus_envelope(
                propose_response.content,
            )
            _validate_focus_continuity(
                inspection_focus,
                proposal_focus,
            )
        except _ComponentEnvelopeError as exc:
            trace_emit(
                phase="engineering",
                component="engineering_propose",
                event_type="COMPONENT_FAILED",
                input_refs=("evidence:packet",),
                outcome="FAILED",
                reason_code=exc.reason_code,
            )
            assessment["operational_rationale"] = [
                "engineering proposal envelope validation failed"
            ]
            return (
                TerminalDisposition.INCONCLUSIVE,
                ("engineering:analyze",),
            )

        assessment["proposal_status"] = proposal_status
        assessment["component_outputs"]["engineering_propose"] = (
            propose_response.content
        )
        trace_emit(
            phase="engineering",
            component="engineering_propose",
            event_type="COMPONENT_COMPLETED",
            input_refs=("evidence:packet",),
            output_refs=("engineering:propose",),
            outcome="SUCCEEDED",
        )

        if proposal_status != "GROUNDED":
            assessment["operational_rationale"] = [
                "proposal is not grounded"
            ]
            return (
                TerminalDisposition.INCONCLUSIVE,
                ("engineering:propose",),
            )

        assessment["operational_rationale"] = [
            "grounded actionable finding produced a bounded proposal"
        ]
        return (
            TerminalDisposition.HARDENING_PROPOSAL,
            ("engineering:analyze", "engineering:propose"),
        )

    @staticmethod
    def _skip_following_components(
        trace_emit,
        components: tuple[str, ...],
    ) -> None:
        for component in components:
            trace_emit(
                phase="engineering",
                component=component,
                event_type="COMPONENT_SKIPPED",
                input_refs=("evidence:packet",),
                outcome="SKIPPED",
                reason_code="precondition_not_met",
            )


def validate_internal_interaction_artifacts(
    artifact_dir: str | Path,
) -> None:
    root = Path(artifact_dir)
    if not root.is_dir():
        raise ValueError("artifact_dir must be an existing directory")

    actual_files = {
        item.name
        for item in root.iterdir()
        if item.is_file()
    }
    if actual_files != _EXPECTED_ARTIFACT_FILES:
        raise ValueError("internal interaction artifact set mismatch")

    try:
        attestation = json.loads(
            (root / "attestation.json").read_text(encoding="utf-8")
        )
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError("attestation.json is invalid") from exc

    expected_keys = {
        "schema",
        "run_id",
        "baseline_commit",
        "digest_algorithm",
        "files",
        "authority_effect",
    }
    if not isinstance(attestation, dict) or set(attestation) != expected_keys:
        raise ValueError("attestation keys mismatch")
    if attestation["schema"] != _ARTIFACT_SCHEMA:
        raise ValueError("attestation schema mismatch")
    if attestation["digest_algorithm"] != "sha256":
        raise ValueError("attestation digest algorithm mismatch")
    if attestation["authority_effect"] != "none":
        raise ValueError("attestation authority_effect must be none")

    manifest = _load_json_object(root / "manifest.json", "manifest")
    evidence = _load_json_object(root / "evidence.json", "evidence")
    assessment = _load_json_object(root / "assessment.json", "assessment")
    outcome = _load_json_object(root / "outcome.json", "outcome")

    run_id = manifest.get("run_id")
    baseline_commit = manifest.get("baseline_commit")
    if not isinstance(run_id, str) or not _RUN_ID_RE.fullmatch(run_id):
        raise ValueError("manifest run_id is invalid")
    if not isinstance(baseline_commit, str) or not _SHA_RE.fullmatch(
        baseline_commit
    ):
        raise ValueError("manifest baseline_commit is invalid")

    if attestation["run_id"] != run_id:
        raise ValueError("attestation run_id does not match manifest")
    if attestation["baseline_commit"] != baseline_commit:
        raise ValueError(
            "attestation baseline_commit does not match manifest"
        )

    if evidence.get("baseline_commit") != baseline_commit:
        raise ValueError("evidence baseline_commit does not match manifest")
    if outcome.get("run_id") != run_id:
        raise ValueError("outcome run_id does not match manifest")
    if outcome.get("baseline_commit") != baseline_commit:
        raise ValueError("outcome baseline_commit does not match manifest")
    if outcome.get("disposition") not in {
        item.value for item in TerminalDisposition
    }:
        raise ValueError("outcome disposition is invalid")

    for payload_name, payload in (
        ("manifest", manifest),
        ("evidence", evidence),
        ("assessment", assessment),
        ("outcome", outcome),
    ):
        if payload.get("authority_effect") != "none":
            raise ValueError(
                f"{payload_name} authority_effect must remain none"
            )

    files = attestation["files"]
    if not isinstance(files, dict):
        raise ValueError("attestation files must be an object")
    if tuple(files) != _ARTIFACT_PAYLOAD_FILES:
        raise ValueError("attestation file order/set mismatch")

    for name in _ARTIFACT_PAYLOAD_FILES:
        digest = files[name]
        if not isinstance(digest, str) or not re.fullmatch(
            r"[0-9a-f]{64}",
            digest,
        ):
            raise ValueError("attestation contains invalid digest")
        actual = hashlib.sha256((root / name).read_bytes()).hexdigest()
        if actual != digest:
            raise ValueError(f"artifact digest mismatch: {name}")

    events = read_execution_trace_jsonl(root / "trace.jsonl")
    if not events:
        raise ValueError("trace must not be empty")
    if any(event.authority_effect != "none" for event in events):
        raise ValueError("trace authority_effect must remain none")
    if any(event.run_id != run_id for event in events):
        raise ValueError("trace run_id does not match manifest")
    if any(
        event.baseline_commit != baseline_commit
        for event in events
    ):
        raise ValueError("trace baseline_commit does not match manifest")


def _load_json_object(path: Path, label: str) -> dict[str, object]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{label} JSON is invalid") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"{label} must be a JSON object")
    return payload


def _write_attestation(
    *,
    artifact_dir: Path,
    run_id: str,
    baseline_commit: str,
) -> None:
    files = {
        name: hashlib.sha256(
            (artifact_dir / name).read_bytes()
        ).hexdigest()
        for name in _ARTIFACT_PAYLOAD_FILES
    }
    payload = {
        "schema": _ARTIFACT_SCHEMA,
        "run_id": run_id,
        "baseline_commit": baseline_commit,
        "digest_algorithm": "sha256",
        "files": files,
        "authority_effect": "none",
    }
    _write_json(artifact_dir / "attestation.json", payload)


def _packet_payload(
    packet: SelfReviewEvidencePacket,
) -> dict[str, object]:
    return {
        "schema": "MALAK-SELF-REVIEW-EVIDENCE-PACKET/v0",
        "baseline_commit": packet.baseline_commit,
        "status": packet.status,
        "required_sources": [
            asdict(source)
            for source in packet.required_sources
        ],
        "missing_required_sources": list(
            packet.missing_required_sources
        ),
        "unreadable_required_sources": list(
            packet.unreadable_required_sources
        ),
        "accepted_adrs": [
            asdict(source)
            for source in packet.accepted_adrs
        ],
        "concept_paths": list(packet.concept_paths),
        "source_paths": list(packet.source_paths),
        "test_paths": list(packet.test_paths),
        "external_validation_refs": list(
            packet.external_validation_refs
        ),
        "authority_effect": "none",
    }


def _write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(
        json.dumps(
            payload,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _rendered_field(content: str, field: str) -> str | None:
    prefix = f"{field}:"
    for line in content.splitlines():
        if line.startswith(prefix):
            return line.partition(":")[2].strip()
    return None


def _component_focus_envelope(
    content: object,
) -> _ComponentFocusEnvelope | None:
    if not isinstance(content, str):
        raise _ComponentEnvelopeError("validation_failed")

    focus_id = _rendered_field(content, "focus_id")
    complete = _rendered_field(content, "focus_complete")
    digest = _rendered_field(content, "evidence_set_digest")
    values = (focus_id, complete, digest)
    if all(value is None for value in values):
        return None
    if any(value is None for value in values):
        raise _ComponentEnvelopeError("validation_failed")

    assert focus_id is not None
    assert complete is not None
    assert digest is not None

    if (
        not focus_id
        or focus_id != focus_id.strip()
        or any(ord(character) < 32 or ord(character) == 127 for character in focus_id)
    ):
        raise _ComponentEnvelopeError("validation_failed")
    if complete not in {"true", "false"}:
        raise _ComponentEnvelopeError("validation_failed")
    if not _FOCUS_DIGEST_RE.fullmatch(digest):
        raise _ComponentEnvelopeError("validation_failed")

    return _ComponentFocusEnvelope(
        focus_id=focus_id,
        complete=complete == "true",
        evidence_set_digest=digest,
    )


def _validate_focus_continuity(
    expected: _ComponentFocusEnvelope | None,
    observed: _ComponentFocusEnvelope | None,
) -> None:
    if expected is None and observed is None:
        return
    if expected is None or observed is None:
        raise _ComponentEnvelopeError("validation_failed")
    if (
        expected.focus_id != observed.focus_id
        or expected.evidence_set_digest != observed.evidence_set_digest
        or not observed.complete
    ):
        raise _ComponentEnvelopeError("validation_failed")


def _component_envelope_status(
    content: object,
    *,
    expected_baseline: str,
) -> str:
    if not isinstance(content, str):
        raise _ComponentEnvelopeError("validation_failed")
    if len(content.encode("utf-8")) > _MAX_COMPONENT_OUTPUT_BYTES:
        raise _ComponentEnvelopeError("validation_failed")

    baseline = _rendered_field(content, "baseline_commit")
    if baseline != expected_baseline:
        raise _ComponentEnvelopeError("baseline_mismatch")

    authority_effect = _rendered_field(content, "authority_effect")
    if authority_effect != "none":
        raise _ComponentEnvelopeError("validation_failed")

    status = _rendered_field(content, "status")
    if status not in {"GROUNDED", "UNCONFIRMED"}:
        raise _ComponentEnvelopeError("validation_failed")

    return status


def _validate_run_id(value: object) -> None:
    if not isinstance(value, str):
        raise TypeError("run_id must be a string")
    if not _RUN_ID_RE.fullmatch(value):
        raise ValueError(
            "run_id must be a path-safe identifier of 1-128 characters"
        )


def _validate_text(field_name: str, value: object) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    if not value:
        raise ValueError(f"{field_name} must not be empty")
    if value != value.strip():
        raise ValueError(
            f"{field_name} must not contain surrounding whitespace"
        )
    if any(ord(character) < 32 or ord(character) == 127 for character in value):
        raise ValueError(
            f"{field_name} contains forbidden control characters"
        )


def _utc_now() -> datetime:
    return datetime.now(UTC)


def _validate_utc(value: object) -> None:
    if not isinstance(value, datetime):
        raise TypeError("created_at must be a datetime")
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("created_at must be timezone-aware")
    if value.utcoffset() != UTC.utcoffset(value):
        raise ValueError("created_at must use UTC")
