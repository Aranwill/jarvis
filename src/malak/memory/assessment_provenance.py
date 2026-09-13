from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import StrEnum

from malak.memory.candidate_content_identity import EpisodicCandidateContentIdentity


POLICY_VERSION = "episodic-assessment-provenance/v2"


def _require_canonical_text(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")

    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must not be empty")
    if normalized != value:
        raise ValueError(f"{field_name} must not contain surrounding whitespace")

    return value


def _optional_canonical_text(
    value: str | None,
    field_name: str,
) -> str | None:
    if value is None:
        return None
    return _require_canonical_text(value, field_name)


def _require_utc_datetime(value: datetime, field_name: str) -> datetime:
    if not isinstance(value, datetime):
        raise TypeError(f"{field_name} must be a datetime")
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{field_name} must include timezone information")
    if value.utcoffset() != timedelta(0):
        raise ValueError(f"{field_name} must be UTC")
    return value


def _require_content_identity(
    value: EpisodicCandidateContentIdentity, candidate_id: str
) -> EpisodicCandidateContentIdentity:
    if not isinstance(value, EpisodicCandidateContentIdentity):
        raise TypeError("candidate_content_identity must be an EpisodicCandidateContentIdentity")
    if value.candidate_id != candidate_id:
        raise ValueError("candidate_content_identity candidate_id must match candidate_id")
    return value


class AssessmentKind(StrEnum):
    SOURCE_AUTHORITY = "source_authority"
    CONFIDENCE = "confidence"
    SENSITIVITY = "sensitivity"
    SOURCE_SECURITY_STATUS = "source_security_status"
    SCOPE_APPLICABLE = "scope_applicable"
    POLICY_VIOLATION = "policy_violation"
    SENSITIVE_REVIEW_REQUIRED = "sensitive_review_required"
    CONTRADICTION_REQUIRES_REVIEW = "contradiction_requires_review"


class AssessmentProducerRole(StrEnum):
    SOURCE_GOVERNANCE = "source_governance"
    EVIDENCE_EVALUATION = "evidence_evaluation"
    DATA_CLASSIFICATION = "data_classification"
    SECURITY_TRUST_STATE = "security_trust_state"
    ADMISSION_POLICY = "admission_policy"
    CONFLICT_EVALUATION = "conflict_evaluation"


@dataclass(frozen=True, slots=True)
class AdmissionAssessment:
    assessment_id: str
    candidate_id: str
    candidate_content_identity: EpisodicCandidateContentIdentity
    kind: AssessmentKind
    value: str | bool
    producer_role: AssessmentProducerRole | None = None
    producer_reference: str | None = None
    policy_or_rule_reference: str | None = None
    assessed_at: datetime | None = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "assessment_id",
            _require_canonical_text(self.assessment_id, "assessment_id"),
        )
        object.__setattr__(
            self,
            "candidate_id",
            _require_canonical_text(self.candidate_id, "candidate_id"),
        )
        object.__setattr__(self, "candidate_content_identity", _require_content_identity(
            self.candidate_content_identity, self.candidate_id
        ))

        if not isinstance(self.kind, AssessmentKind):
            raise TypeError("kind must be an AssessmentKind")

        if type(self.value) is bool:
            pass
        elif isinstance(self.value, str):
            object.__setattr__(
                self,
                "value",
                _require_canonical_text(self.value, "value"),
            )
        else:
            raise TypeError("value must be a string or bool")

        if self.producer_role is not None and not isinstance(
            self.producer_role,
            AssessmentProducerRole,
        ):
            raise TypeError(
                "producer_role must be an AssessmentProducerRole or None"
            )

        object.__setattr__(
            self,
            "producer_reference",
            _optional_canonical_text(
                self.producer_reference,
                "producer_reference",
            ),
        )
        object.__setattr__(
            self,
            "policy_or_rule_reference",
            _optional_canonical_text(
                self.policy_or_rule_reference,
                "policy_or_rule_reference",
            ),
        )

        if self.assessed_at is not None:
            object.__setattr__(
                self,
                "assessed_at",
                _require_utc_datetime(self.assessed_at, "assessed_at"),
            )


class AssessmentProvenanceOutcome(StrEnum):
    HOLD = "hold"
    INVALID = "invalid"
    VALID = "valid"


class AssessmentProvenanceReason(StrEnum):
    MISSING_PRODUCER_ROLE = "missing_producer_role"
    MISSING_PRODUCER_REFERENCE = "missing_producer_reference"
    MISSING_POLICY_OR_RULE_REFERENCE = "missing_policy_or_rule_reference"
    MISSING_ASSESSED_AT = "missing_assessed_at"
    ASSESSMENT_FROM_FUTURE = "assessment_from_future"
    CANDIDATE_MISMATCH = "candidate_mismatch"
    CONTENT_IDENTITY_MISMATCH = "content_identity_mismatch"
    PRODUCER_ROLE_NOT_ALLOWED_FOR_KIND = "producer_role_not_allowed_for_kind"
    VALID = "valid"


@dataclass(frozen=True, slots=True)
class AssessmentProvenanceDecision:
    assessment_id: str
    candidate_id: str
    candidate_content_identity: EpisodicCandidateContentIdentity
    kind: AssessmentKind
    outcome: AssessmentProvenanceOutcome
    reason_code: AssessmentProvenanceReason
    evaluated_at: datetime
    policy_version: str = POLICY_VERSION

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "assessment_id",
            _require_canonical_text(self.assessment_id, "assessment_id"),
        )
        object.__setattr__(
            self,
            "candidate_id",
            _require_canonical_text(self.candidate_id, "candidate_id"),
        )
        object.__setattr__(self, "candidate_content_identity", _require_content_identity(
            self.candidate_content_identity, self.candidate_id
        ))

        if not isinstance(self.kind, AssessmentKind):
            raise TypeError("kind must be an AssessmentKind")
        if not isinstance(self.outcome, AssessmentProvenanceOutcome):
            raise TypeError("outcome must be an AssessmentProvenanceOutcome")
        if not isinstance(self.reason_code, AssessmentProvenanceReason):
            raise TypeError("reason_code must be an AssessmentProvenanceReason")

        object.__setattr__(
            self,
            "evaluated_at",
            _require_utc_datetime(self.evaluated_at, "evaluated_at"),
        )
        object.__setattr__(
            self,
            "policy_version",
            _require_canonical_text(self.policy_version, "policy_version"),
        )


_ALLOWED_PRODUCER_ROLES: dict[
    AssessmentKind,
    frozenset[AssessmentProducerRole],
] = {
    AssessmentKind.SOURCE_AUTHORITY: frozenset(
        {AssessmentProducerRole.SOURCE_GOVERNANCE}
    ),
    AssessmentKind.CONFIDENCE: frozenset(
        {AssessmentProducerRole.EVIDENCE_EVALUATION}
    ),
    AssessmentKind.SENSITIVITY: frozenset(
        {AssessmentProducerRole.DATA_CLASSIFICATION}
    ),
    AssessmentKind.SOURCE_SECURITY_STATUS: frozenset(
        {AssessmentProducerRole.SECURITY_TRUST_STATE}
    ),
    AssessmentKind.SCOPE_APPLICABLE: frozenset(
        {AssessmentProducerRole.ADMISSION_POLICY}
    ),
    AssessmentKind.POLICY_VIOLATION: frozenset(
        {
            AssessmentProducerRole.ADMISSION_POLICY,
            AssessmentProducerRole.SECURITY_TRUST_STATE,
        }
    ),
    AssessmentKind.SENSITIVE_REVIEW_REQUIRED: frozenset(
        {
            AssessmentProducerRole.ADMISSION_POLICY,
            AssessmentProducerRole.DATA_CLASSIFICATION,
        }
    ),
    AssessmentKind.CONTRADICTION_REQUIRES_REVIEW: frozenset(
        {AssessmentProducerRole.CONFLICT_EVALUATION}
    ),
}


def _decision(
    assessment: AdmissionAssessment,
    outcome: AssessmentProvenanceOutcome,
    reason_code: AssessmentProvenanceReason,
    evaluated_at: datetime,
) -> AssessmentProvenanceDecision:
    return AssessmentProvenanceDecision(
        assessment_id=assessment.assessment_id,
        candidate_id=assessment.candidate_id,
        candidate_content_identity=assessment.candidate_content_identity,
        kind=assessment.kind,
        outcome=outcome,
        reason_code=reason_code,
        evaluated_at=evaluated_at,
    )


def validate_assessment_provenance(
    assessment: AdmissionAssessment,
    expected_candidate_content_identity: EpisodicCandidateContentIdentity,
    evaluated_at: datetime,
) -> AssessmentProvenanceDecision:
    if not isinstance(assessment, AdmissionAssessment):
        raise TypeError("assessment must be an AdmissionAssessment")
    if not isinstance(expected_candidate_content_identity, EpisodicCandidateContentIdentity):
        raise TypeError(
            "expected_candidate_content_identity must be an EpisodicCandidateContentIdentity"
        )

    evaluated_at = _require_utc_datetime(evaluated_at, "evaluated_at")

    if assessment.candidate_id != expected_candidate_content_identity.candidate_id:
        return _decision(
            assessment,
            AssessmentProvenanceOutcome.INVALID,
            AssessmentProvenanceReason.CANDIDATE_MISMATCH,
            evaluated_at,
        )

    if assessment.candidate_content_identity != expected_candidate_content_identity:
        return _decision(
            assessment,
            AssessmentProvenanceOutcome.INVALID,
            AssessmentProvenanceReason.CONTENT_IDENTITY_MISMATCH,
            evaluated_at,
        )

    if assessment.producer_role is None:
        return _decision(
            assessment,
            AssessmentProvenanceOutcome.HOLD,
            AssessmentProvenanceReason.MISSING_PRODUCER_ROLE,
            evaluated_at,
        )

    if assessment.producer_reference is None:
        return _decision(
            assessment,
            AssessmentProvenanceOutcome.HOLD,
            AssessmentProvenanceReason.MISSING_PRODUCER_REFERENCE,
            evaluated_at,
        )

    if assessment.policy_or_rule_reference is None:
        return _decision(
            assessment,
            AssessmentProvenanceOutcome.HOLD,
            AssessmentProvenanceReason.MISSING_POLICY_OR_RULE_REFERENCE,
            evaluated_at,
        )

    if assessment.assessed_at is None:
        return _decision(
            assessment,
            AssessmentProvenanceOutcome.HOLD,
            AssessmentProvenanceReason.MISSING_ASSESSED_AT,
            evaluated_at,
        )

    if assessment.assessed_at > evaluated_at:
        return _decision(
            assessment,
            AssessmentProvenanceOutcome.HOLD,
            AssessmentProvenanceReason.ASSESSMENT_FROM_FUTURE,
            evaluated_at,
        )

    if assessment.producer_role not in _ALLOWED_PRODUCER_ROLES[assessment.kind]:
        return _decision(
            assessment,
            AssessmentProvenanceOutcome.INVALID,
            AssessmentProvenanceReason.PRODUCER_ROLE_NOT_ALLOWED_FOR_KIND,
            evaluated_at,
        )

    return _decision(
        assessment,
        AssessmentProvenanceOutcome.VALID,
        AssessmentProvenanceReason.VALID,
        evaluated_at,
    )
