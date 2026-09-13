import dataclasses
from datetime import datetime, timedelta
from enum import StrEnum

from malak.memory.candidate_content_identity import (
    CandidateContentIdentityVerification,
    EpisodicCandidateContentIdentity,
    compute_episodic_candidate_content_identity,
    verify_episodic_candidate_content_identity,
)
from malak.memory.episodic_admission import (
    EpisodicAdmissionDecision,
    EpisodicMemoryCandidate,
    evaluate_episodic_candidate,
)
from malak.memory.governed_input_projection import (
    POLICY_VERSION as PROJECTION_POLICY_VERSION,
    GovernedAdmissionInputProjection,
    GovernedAdmissionProjectionOutcome,
)


POLICY_VERSION = "episodic-admission-governed-projection-consumption/v2"


def _require_canonical_text(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")

    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must not be empty")
    if normalized != value:
        raise ValueError(f"{field_name} must not contain surrounding whitespace")

    return value


def _require_utc_datetime(value: datetime, field_name: str) -> datetime:
    if not isinstance(value, datetime):
        raise TypeError(f"{field_name} must be a datetime")
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{field_name} must include timezone information")
    if value.utcoffset() != timedelta(0):
        raise ValueError(f"{field_name} must be UTC")
    return value


class GovernedAdmissionConsumptionOutcome(StrEnum):
    EVALUATED = "evaluated"
    BLOCKED = "blocked"


class GovernedAdmissionConsumptionReason(StrEnum):
    CANDIDATE_BINDING_MISMATCH = "candidate_binding_mismatch"
    CONTENT_IDENTITY_BINDING_MISMATCH = "content_identity_binding_mismatch"
    UNSUPPORTED_PROJECTION_POLICY = "unsupported_projection_policy"
    CONSUMPTION_TIME_PRECEDES_PROJECTION = "consumption_time_precedes_projection"
    PROJECTION_DENIED = "projection_denied"
    PROJECTION_HOLD = "projection_hold"
    CONTEXT_BINDING_MISMATCH = "context_binding_mismatch"
    EVALUATED = "evaluated"


@dataclasses.dataclass(frozen=True, slots=True)
class GovernedAdmissionConsumptionResult:
    candidate_id: str
    actual_candidate_content_identity: EpisodicCandidateContentIdentity
    presented_projection_content_identity: EpisodicCandidateContentIdentity
    outcome: GovernedAdmissionConsumptionOutcome
    reason_code: GovernedAdmissionConsumptionReason
    evaluated_at: datetime
    admission_decision: EpisodicAdmissionDecision | None = None
    policy_version: str = POLICY_VERSION

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "candidate_id",
            _require_canonical_text(self.candidate_id, "candidate_id"),
        )
        for field_name in (
            "actual_candidate_content_identity",
            "presented_projection_content_identity",
        ):
            if not isinstance(getattr(self, field_name), EpisodicCandidateContentIdentity):
                raise TypeError(f"{field_name} must be an EpisodicCandidateContentIdentity")
        if self.actual_candidate_content_identity.candidate_id != self.candidate_id:
            raise ValueError("actual_candidate_content_identity candidate_id must match result candidate_id")
        if not isinstance(self.outcome, GovernedAdmissionConsumptionOutcome):
            raise TypeError("outcome must be a GovernedAdmissionConsumptionOutcome")
        if not isinstance(self.reason_code, GovernedAdmissionConsumptionReason):
            raise TypeError("reason_code must be a GovernedAdmissionConsumptionReason")
        object.__setattr__(
            self,
            "evaluated_at",
            _require_utc_datetime(self.evaluated_at, "evaluated_at"),
        )
        if self.admission_decision is not None and not isinstance(
            self.admission_decision,
            EpisodicAdmissionDecision,
        ):
            raise TypeError(
                "admission_decision must be an EpisodicAdmissionDecision or None"
            )
        object.__setattr__(
            self,
            "policy_version",
            _require_canonical_text(self.policy_version, "policy_version"),
        )

        identities_match = (
            self.actual_candidate_content_identity
            == self.presented_projection_content_identity
        )
        if self.outcome is GovernedAdmissionConsumptionOutcome.EVALUATED:
            if self.reason_code is not GovernedAdmissionConsumptionReason.EVALUATED:
                raise ValueError("EVALUATED outcome requires EVALUATED reason_code")
            if self.admission_decision is None:
                raise ValueError("EVALUATED outcome requires admission_decision")
            if not identities_match:
                raise ValueError("EVALUATED outcome requires matching actual and presented identities")
        else:
            if self.reason_code is GovernedAdmissionConsumptionReason.EVALUATED:
                raise ValueError("BLOCKED outcome cannot use EVALUATED reason_code")
            if self.admission_decision is not None:
                raise ValueError("BLOCKED outcome must not carry admission_decision")
            binding_reasons = {
                GovernedAdmissionConsumptionReason.CANDIDATE_BINDING_MISMATCH,
                GovernedAdmissionConsumptionReason.CONTENT_IDENTITY_BINDING_MISMATCH,
            }
            if self.reason_code not in binding_reasons and not identities_match:
                raise ValueError("non-binding BLOCKED outcome requires matching actual and presented identities")

        if self.admission_decision is not None:
            if self.admission_decision.candidate_id != self.candidate_id:
                raise ValueError(
                    "admission_decision candidate_id must match result candidate_id"
                )
            if self.admission_decision.evaluated_at != self.evaluated_at:
                raise ValueError(
                    "admission_decision evaluated_at must match result evaluated_at"
                )


def consume_governed_admission_projection(
    candidate: EpisodicMemoryCandidate,
    projection: GovernedAdmissionInputProjection,
    evaluated_at: datetime,
) -> GovernedAdmissionConsumptionResult:
    if not isinstance(candidate, EpisodicMemoryCandidate):
        raise TypeError("candidate must be an EpisodicMemoryCandidate")
    if not isinstance(projection, GovernedAdmissionInputProjection):
        raise TypeError("projection must be a GovernedAdmissionInputProjection")

    evaluated_at = _require_utc_datetime(evaluated_at, "evaluated_at")
    actual_identity = compute_episodic_candidate_content_identity(candidate)
    presented_identity = projection.candidate_content_identity

    def blocked(reason: GovernedAdmissionConsumptionReason) -> GovernedAdmissionConsumptionResult:
        return GovernedAdmissionConsumptionResult(
            candidate_id=candidate.candidate_id,
            actual_candidate_content_identity=actual_identity,
            presented_projection_content_identity=presented_identity,
            outcome=GovernedAdmissionConsumptionOutcome.BLOCKED,
            reason_code=reason,
            evaluated_at=evaluated_at,
        )

    if projection.candidate_id != candidate.candidate_id:
        return blocked(GovernedAdmissionConsumptionReason.CANDIDATE_BINDING_MISMATCH)
    if (
        verify_episodic_candidate_content_identity(candidate, presented_identity)
        is not CandidateContentIdentityVerification.MATCH
    ):
        return blocked(GovernedAdmissionConsumptionReason.CONTENT_IDENTITY_BINDING_MISMATCH)
    if projection.policy_version != PROJECTION_POLICY_VERSION:
        return blocked(GovernedAdmissionConsumptionReason.UNSUPPORTED_PROJECTION_POLICY)
    if evaluated_at < projection.evaluated_at:
        return blocked(GovernedAdmissionConsumptionReason.CONSUMPTION_TIME_PRECEDES_PROJECTION)
    if projection.outcome is GovernedAdmissionProjectionOutcome.DENIED:
        return blocked(GovernedAdmissionConsumptionReason.PROJECTION_DENIED)
    if projection.outcome is GovernedAdmissionProjectionOutcome.HOLD:
        return blocked(GovernedAdmissionConsumptionReason.PROJECTION_HOLD)

    effective_context = projection.effective_context
    effective_signals = projection.effective_signals
    if (
        effective_context.subject_scope != candidate.control.subject_scope
        or effective_context.domain != candidate.control.domain
        or effective_context.purpose != candidate.control.purpose
    ):
        return blocked(GovernedAdmissionConsumptionReason.CONTEXT_BINDING_MISMATCH)

    effective_candidate = dataclasses.replace(candidate, control=effective_context)
    admission_decision = evaluate_episodic_candidate(
        effective_candidate,
        effective_signals,
        evaluated_at,
    )
    return GovernedAdmissionConsumptionResult(
        candidate_id=candidate.candidate_id,
        actual_candidate_content_identity=actual_identity,
        presented_projection_content_identity=presented_identity,
        outcome=GovernedAdmissionConsumptionOutcome.EVALUATED,
        reason_code=GovernedAdmissionConsumptionReason.EVALUATED,
        evaluated_at=evaluated_at,
        admission_decision=admission_decision,
    )
