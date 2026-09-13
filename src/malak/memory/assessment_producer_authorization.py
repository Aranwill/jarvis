from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import StrEnum

from malak.memory.assessment_provenance import (
    AdmissionAssessment,
    AssessmentKind,
    AssessmentProvenanceDecision,
    AssessmentProvenanceOutcome,
)
from malak.memory.candidate_content_identity import (
    EpisodicCandidateContentIdentity,
)
from malak.security.contracts import (
    AuthorizationDecision,
    AuthorizationRequest,
    PermissionScope,
)


POLICY_VERSION = "episodic-assessment-producer-authorization/v2"


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
    value: EpisodicCandidateContentIdentity,
    candidate_id: str,
) -> EpisodicCandidateContentIdentity:
    if not isinstance(value, EpisodicCandidateContentIdentity):
        raise TypeError(
            "candidate_content_identity must be an "
            "EpisodicCandidateContentIdentity"
        )
    if value.candidate_id != candidate_id:
        raise ValueError(
            "candidate_content_identity candidate_id must match candidate_id"
        )
    return value


class AssessmentInfluenceClass(StrEnum):
    TRUST_INCREASING = "trust_increasing"
    TRUST_REDUCING = "trust_reducing"
    REVIEW_FORCING = "review_forcing"
    HARD_REJECT = "hard_reject"
    UNCLASSIFIED = "unclassified"


@dataclass(frozen=True, slots=True)
class AssessmentProducerAuthorizationEvidence:
    assessment_id: str
    candidate_id: str
    candidate_content_identity: EpisodicCandidateContentIdentity
    kind: AssessmentKind
    influence_class: AssessmentInfluenceClass
    producer_subject_id: str
    request: AuthorizationRequest
    decision: AuthorizationDecision

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
        object.__setattr__(
            self,
            "candidate_content_identity",
            _require_content_identity(
                self.candidate_content_identity,
                self.candidate_id,
            ),
        )
        object.__setattr__(
            self,
            "producer_subject_id",
            _require_canonical_text(
                self.producer_subject_id,
                "producer_subject_id",
            ),
        )

        if not isinstance(self.kind, AssessmentKind):
            raise TypeError("kind must be an AssessmentKind")
        if not isinstance(self.influence_class, AssessmentInfluenceClass):
            raise TypeError(
                "influence_class must be an AssessmentInfluenceClass"
            )
        if not isinstance(self.request, AuthorizationRequest):
            raise TypeError("request must be an AuthorizationRequest")
        if not isinstance(self.decision, AuthorizationDecision):
            raise TypeError("decision must be an AuthorizationDecision")


class AssessmentProducerAuthorizationOutcome(StrEnum):
    AUTHORIZED = "authorized"
    HOLD = "hold"
    DENIED = "denied"


class AssessmentProducerAuthorizationReason(StrEnum):
    MISSING_PROVENANCE_DECISION = "missing_provenance_decision"
    PROVENANCE_HOLD = "provenance_hold"
    PROVENANCE_INVALID = "provenance_invalid"
    MISSING_AUTHORIZATION_EVIDENCE = "missing_authorization_evidence"
    ASSESSMENT_ID_MISMATCH = "assessment_id_mismatch"
    CANDIDATE_ID_MISMATCH = "candidate_id_mismatch"
    CONTENT_IDENTITY_MISMATCH = "content_identity_mismatch"
    KIND_MISMATCH = "kind_mismatch"
    UNSUPPORTED_ASSESSMENT_VALUE = "unsupported_assessment_value"
    INFLUENCE_CLASS_MISMATCH = "influence_class_mismatch"
    PRODUCER_SUBJECT_MISMATCH = "producer_subject_mismatch"
    PERMISSION_SCOPE_MISMATCH = "permission_scope_mismatch"
    DECISION_REQUEST_MISMATCH = "decision_request_mismatch"
    CONTEXT_NOT_YET_VALID = "context_not_yet_valid"
    CONTEXT_EXPIRED = "context_expired"
    AUTHORIZATION_DENIED = "authorization_denied"
    AUTHORIZED = "authorized"


@dataclass(frozen=True, slots=True)
class AssessmentProducerAuthorizationDecision:
    assessment_id: str
    candidate_id: str
    candidate_content_identity: EpisodicCandidateContentIdentity
    kind: AssessmentKind
    outcome: AssessmentProducerAuthorizationOutcome
    reason_code: AssessmentProducerAuthorizationReason
    evaluated_at: datetime
    influence_class: AssessmentInfluenceClass | None = None
    producer_subject_id: str | None = None
    authorization_request_id: str | None = None
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
        object.__setattr__(
            self,
            "candidate_content_identity",
            _require_content_identity(
                self.candidate_content_identity,
                self.candidate_id,
            ),
        )

        if not isinstance(self.kind, AssessmentKind):
            raise TypeError("kind must be an AssessmentKind")
        if not isinstance(
            self.outcome,
            AssessmentProducerAuthorizationOutcome,
        ):
            raise TypeError(
                "outcome must be an AssessmentProducerAuthorizationOutcome"
            )
        if not isinstance(
            self.reason_code,
            AssessmentProducerAuthorizationReason,
        ):
            raise TypeError(
                "reason_code must be an AssessmentProducerAuthorizationReason"
            )

        object.__setattr__(
            self,
            "evaluated_at",
            _require_utc_datetime(self.evaluated_at, "evaluated_at"),
        )

        if self.influence_class is not None and not isinstance(
            self.influence_class,
            AssessmentInfluenceClass,
        ):
            raise TypeError(
                "influence_class must be an AssessmentInfluenceClass or None"
            )

        object.__setattr__(
            self,
            "producer_subject_id",
            _optional_canonical_text(
                self.producer_subject_id,
                "producer_subject_id",
            ),
        )
        object.__setattr__(
            self,
            "authorization_request_id",
            _optional_canonical_text(
                self.authorization_request_id,
                "authorization_request_id",
            ),
        )
        object.__setattr__(
            self,
            "policy_version",
            _require_canonical_text(self.policy_version, "policy_version"),
        )


_CLOSED_INFLUENCE_BY_KIND_AND_VALUE: dict[
    AssessmentKind,
    dict[str | bool, AssessmentInfluenceClass],
] = {
    AssessmentKind.SOURCE_SECURITY_STATUS: {
        "acceptable": AssessmentInfluenceClass.TRUST_INCREASING,
        "unassessed": AssessmentInfluenceClass.REVIEW_FORCING,
        "suspect": AssessmentInfluenceClass.TRUST_REDUCING,
        "tainted": AssessmentInfluenceClass.HARD_REJECT,
        "revoked": AssessmentInfluenceClass.HARD_REJECT,
    },
    AssessmentKind.SCOPE_APPLICABLE: {
        True: AssessmentInfluenceClass.TRUST_INCREASING,
        False: AssessmentInfluenceClass.HARD_REJECT,
    },
    AssessmentKind.POLICY_VIOLATION: {
        False: AssessmentInfluenceClass.TRUST_INCREASING,
        True: AssessmentInfluenceClass.HARD_REJECT,
    },
    AssessmentKind.SENSITIVE_REVIEW_REQUIRED: {
        False: AssessmentInfluenceClass.TRUST_INCREASING,
        True: AssessmentInfluenceClass.REVIEW_FORCING,
    },
    AssessmentKind.CONTRADICTION_REQUIRES_REVIEW: {
        False: AssessmentInfluenceClass.TRUST_INCREASING,
        True: AssessmentInfluenceClass.REVIEW_FORCING,
    },
}

_OPEN_STRING_KINDS = frozenset(
    {
        AssessmentKind.SOURCE_AUTHORITY,
        AssessmentKind.CONFIDENCE,
        AssessmentKind.SENSITIVITY,
    }
)


def _influence_for_assessment(
    assessment: AdmissionAssessment,
) -> AssessmentInfluenceClass | None:
    if assessment.kind in _OPEN_STRING_KINDS:
        if isinstance(assessment.value, str):
            return AssessmentInfluenceClass.UNCLASSIFIED
        return None

    allowed_values = _CLOSED_INFLUENCE_BY_KIND_AND_VALUE.get(assessment.kind)
    if allowed_values is None:
        return None

    if assessment.kind is AssessmentKind.SOURCE_SECURITY_STATUS:
        if not isinstance(assessment.value, str):
            return None
    elif type(assessment.value) is not bool:
        return None

    return allowed_values.get(assessment.value)


def required_permission_for_assessment(
    assessment: AdmissionAssessment,
) -> PermissionScope | None:
    if not isinstance(assessment, AdmissionAssessment):
        raise TypeError("assessment must be an AdmissionAssessment")

    influence_class = _influence_for_assessment(assessment)
    if influence_class is None:
        return None

    return PermissionScope(
        resource=f"memory.episodic_assessment.{assessment.kind.value}",
        action=f"produce.{influence_class.value}",
    )


def _decision(
    assessment: AdmissionAssessment,
    outcome: AssessmentProducerAuthorizationOutcome,
    reason_code: AssessmentProducerAuthorizationReason,
    evaluated_at: datetime,
    *,
    influence_class: AssessmentInfluenceClass | None = None,
    evidence: AssessmentProducerAuthorizationEvidence | None = None,
) -> AssessmentProducerAuthorizationDecision:
    return AssessmentProducerAuthorizationDecision(
        assessment_id=assessment.assessment_id,
        candidate_id=assessment.candidate_id,
        candidate_content_identity=assessment.candidate_content_identity,
        kind=assessment.kind,
        outcome=outcome,
        reason_code=reason_code,
        evaluated_at=evaluated_at,
        influence_class=influence_class,
        producer_subject_id=(
            evidence.producer_subject_id if evidence is not None else None
        ),
        authorization_request_id=(
            evidence.request.request_id if evidence is not None else None
        ),
    )


def _denied(
    assessment: AdmissionAssessment,
    reason_code: AssessmentProducerAuthorizationReason,
    evaluated_at: datetime,
    *,
    influence_class: AssessmentInfluenceClass | None = None,
    evidence: AssessmentProducerAuthorizationEvidence | None = None,
) -> AssessmentProducerAuthorizationDecision:
    return _decision(
        assessment,
        AssessmentProducerAuthorizationOutcome.DENIED,
        reason_code,
        evaluated_at,
        influence_class=influence_class,
        evidence=evidence,
    )


def _hold(
    assessment: AdmissionAssessment,
    reason_code: AssessmentProducerAuthorizationReason,
    evaluated_at: datetime,
    *,
    influence_class: AssessmentInfluenceClass | None = None,
    evidence: AssessmentProducerAuthorizationEvidence | None = None,
) -> AssessmentProducerAuthorizationDecision:
    return _decision(
        assessment,
        AssessmentProducerAuthorizationOutcome.HOLD,
        reason_code,
        evaluated_at,
        influence_class=influence_class,
        evidence=evidence,
    )


def validate_assessment_producer_authorization(
    assessment: AdmissionAssessment,
    provenance_decision: AssessmentProvenanceDecision | None,
    evidence: AssessmentProducerAuthorizationEvidence | None,
    evaluated_at: datetime,
) -> AssessmentProducerAuthorizationDecision:
    if not isinstance(assessment, AdmissionAssessment):
        raise TypeError("assessment must be an AdmissionAssessment")
    if provenance_decision is not None and not isinstance(
        provenance_decision,
        AssessmentProvenanceDecision,
    ):
        raise TypeError(
            "provenance_decision must be an AssessmentProvenanceDecision or None"
        )
    if evidence is not None and not isinstance(
        evidence,
        AssessmentProducerAuthorizationEvidence,
    ):
        raise TypeError(
            "evidence must be an AssessmentProducerAuthorizationEvidence or None"
        )

    evaluated_at = _require_utc_datetime(evaluated_at, "evaluated_at")

    if provenance_decision is None:
        return _hold(
            assessment,
            AssessmentProducerAuthorizationReason.MISSING_PROVENANCE_DECISION,
            evaluated_at,
        )

    if provenance_decision.assessment_id != assessment.assessment_id:
        return _denied(
            assessment,
            AssessmentProducerAuthorizationReason.ASSESSMENT_ID_MISMATCH,
            evaluated_at,
        )

    if provenance_decision.candidate_id != assessment.candidate_id:
        return _denied(
            assessment,
            AssessmentProducerAuthorizationReason.CANDIDATE_ID_MISMATCH,
            evaluated_at,
        )

    if (
        provenance_decision.candidate_content_identity
        != assessment.candidate_content_identity
    ):
        return _denied(
            assessment,
            AssessmentProducerAuthorizationReason.CONTENT_IDENTITY_MISMATCH,
            evaluated_at,
        )

    if provenance_decision.kind is not assessment.kind:
        return _denied(
            assessment,
            AssessmentProducerAuthorizationReason.KIND_MISMATCH,
            evaluated_at,
        )

    if provenance_decision.outcome is AssessmentProvenanceOutcome.HOLD:
        return _hold(
            assessment,
            AssessmentProducerAuthorizationReason.PROVENANCE_HOLD,
            evaluated_at,
        )

    if provenance_decision.outcome is AssessmentProvenanceOutcome.INVALID:
        return _denied(
            assessment,
            AssessmentProducerAuthorizationReason.PROVENANCE_INVALID,
            evaluated_at,
        )

    influence_class = _influence_for_assessment(assessment)
    expected_permission = required_permission_for_assessment(assessment)
    if influence_class is None or expected_permission is None:
        return _hold(
            assessment,
            AssessmentProducerAuthorizationReason.UNSUPPORTED_ASSESSMENT_VALUE,
            evaluated_at,
        )

    if evidence is None:
        return _hold(
            assessment,
            AssessmentProducerAuthorizationReason.MISSING_AUTHORIZATION_EVIDENCE,
            evaluated_at,
            influence_class=influence_class,
        )

    if evidence.assessment_id != assessment.assessment_id:
        return _denied(
            assessment,
            AssessmentProducerAuthorizationReason.ASSESSMENT_ID_MISMATCH,
            evaluated_at,
            influence_class=influence_class,
            evidence=evidence,
        )

    if evidence.candidate_id != assessment.candidate_id:
        return _denied(
            assessment,
            AssessmentProducerAuthorizationReason.CANDIDATE_ID_MISMATCH,
            evaluated_at,
            influence_class=influence_class,
            evidence=evidence,
        )

    if evidence.candidate_content_identity != assessment.candidate_content_identity:
        return _denied(
            assessment,
            AssessmentProducerAuthorizationReason.CONTENT_IDENTITY_MISMATCH,
            evaluated_at,
            influence_class=influence_class,
            evidence=evidence,
        )

    if evidence.kind is not assessment.kind:
        return _denied(
            assessment,
            AssessmentProducerAuthorizationReason.KIND_MISMATCH,
            evaluated_at,
            influence_class=influence_class,
            evidence=evidence,
        )

    if evidence.influence_class is not influence_class:
        return _denied(
            assessment,
            AssessmentProducerAuthorizationReason.INFLUENCE_CLASS_MISMATCH,
            evaluated_at,
            influence_class=influence_class,
            evidence=evidence,
        )

    if evidence.producer_subject_id != evidence.request.context.subject_id:
        return _denied(
            assessment,
            AssessmentProducerAuthorizationReason.PRODUCER_SUBJECT_MISMATCH,
            evaluated_at,
            influence_class=influence_class,
            evidence=evidence,
        )

    if evidence.request.permission != expected_permission:
        return _denied(
            assessment,
            AssessmentProducerAuthorizationReason.PERMISSION_SCOPE_MISMATCH,
            evaluated_at,
            influence_class=influence_class,
            evidence=evidence,
        )

    if evidence.decision.request_id != evidence.request.request_id:
        return _denied(
            assessment,
            AssessmentProducerAuthorizationReason.DECISION_REQUEST_MISMATCH,
            evaluated_at,
            influence_class=influence_class,
            evidence=evidence,
        )

    context = evidence.request.context
    if evaluated_at < context.issued_at:
        return _denied(
            assessment,
            AssessmentProducerAuthorizationReason.CONTEXT_NOT_YET_VALID,
            evaluated_at,
            influence_class=influence_class,
            evidence=evidence,
        )

    if evaluated_at >= context.expires_at:
        return _denied(
            assessment,
            AssessmentProducerAuthorizationReason.CONTEXT_EXPIRED,
            evaluated_at,
            influence_class=influence_class,
            evidence=evidence,
        )

    if evidence.decision.allowed is False:
        return _denied(
            assessment,
            AssessmentProducerAuthorizationReason.AUTHORIZATION_DENIED,
            evaluated_at,
            influence_class=influence_class,
            evidence=evidence,
        )

    return _decision(
        assessment,
        AssessmentProducerAuthorizationOutcome.AUTHORIZED,
        AssessmentProducerAuthorizationReason.AUTHORIZED,
        evaluated_at,
        influence_class=influence_class,
        evidence=evidence,
    )
