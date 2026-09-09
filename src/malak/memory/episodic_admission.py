from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import StrEnum


POLICY_VERSION = "episodic-admission/v1"


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


def _require_string(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    return value


def _require_utc_datetime(value: datetime, field_name: str) -> datetime:
    if not isinstance(value, datetime):
        raise TypeError(f"{field_name} must be a datetime")
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{field_name} must include timezone information")
    if value.utcoffset() != timedelta(0):
        raise ValueError(f"{field_name} must be UTC")
    return value


@dataclass(frozen=True, slots=True)
class EpisodicOrigin:
    session_id: str
    request_id: str
    request_created_at: datetime
    provider: str | None = None
    model: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "session_id",
            _require_canonical_text(self.session_id, "session_id"),
        )
        object.__setattr__(
            self,
            "request_id",
            _require_canonical_text(self.request_id, "request_id"),
        )
        object.__setattr__(
            self,
            "request_created_at",
            _require_utc_datetime(
                self.request_created_at,
                "request_created_at",
            ),
        )
        object.__setattr__(
            self,
            "provider",
            _optional_canonical_text(self.provider, "provider"),
        )
        object.__setattr__(
            self,
            "model",
            _optional_canonical_text(self.model, "model"),
        )


@dataclass(frozen=True, slots=True)
class EpisodicExperience:
    user_content: str
    assistant_content: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "user_content",
            _require_string(self.user_content, "user_content"),
        )
        object.__setattr__(
            self,
            "assistant_content",
            _require_string(self.assistant_content, "assistant_content"),
        )


@dataclass(frozen=True, slots=True)
class EpisodicAdmissionContext:
    subject_scope: str
    domain: str
    purpose: str
    source_authority_classification: str | None = None
    confidence_classification: str | None = None
    sensitivity_classification: str | None = None
    valid_from: datetime | None = None
    valid_until: datetime | None = None

    def __post_init__(self) -> None:
        for field_name in ("subject_scope", "domain", "purpose"):
            object.__setattr__(
                self,
                field_name,
                _require_canonical_text(
                    getattr(self, field_name),
                    field_name,
                ),
            )

        for field_name in (
            "source_authority_classification",
            "confidence_classification",
            "sensitivity_classification",
        ):
            object.__setattr__(
                self,
                field_name,
                _optional_canonical_text(
                    getattr(self, field_name),
                    field_name,
                ),
            )

        if self.valid_from is not None:
            object.__setattr__(
                self,
                "valid_from",
                _require_utc_datetime(self.valid_from, "valid_from"),
            )
        if self.valid_until is not None:
            object.__setattr__(
                self,
                "valid_until",
                _require_utc_datetime(self.valid_until, "valid_until"),
            )

        if (
            self.valid_from is not None
            and self.valid_until is not None
            and self.valid_until <= self.valid_from
        ):
            raise ValueError("valid_until must be after valid_from")


@dataclass(frozen=True, slots=True)
class EpisodicMemoryCandidate:
    candidate_id: str
    origin: EpisodicOrigin
    experience: EpisodicExperience
    control: EpisodicAdmissionContext
    created_at: datetime

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "candidate_id",
            _require_canonical_text(self.candidate_id, "candidate_id"),
        )
        if not isinstance(self.origin, EpisodicOrigin):
            raise TypeError("origin must be an EpisodicOrigin")
        if not isinstance(self.experience, EpisodicExperience):
            raise TypeError("experience must be an EpisodicExperience")
        if not isinstance(self.control, EpisodicAdmissionContext):
            raise TypeError("control must be an EpisodicAdmissionContext")
        object.__setattr__(
            self,
            "created_at",
            _require_utc_datetime(self.created_at, "created_at"),
        )


class SourceSecurityStatus(StrEnum):
    UNASSESSED = "unassessed"
    ACCEPTABLE = "acceptable"
    SUSPECT = "suspect"
    TAINTED = "tainted"
    REVOKED = "revoked"


@dataclass(frozen=True, slots=True)
class EpisodicAdmissionSignals:
    scope_applicable: bool
    policy_violation: bool
    source_security_status: SourceSecurityStatus
    sensitive_review_required: bool
    contradiction_requires_review: bool

    def __post_init__(self) -> None:
        for field_name in (
            "scope_applicable",
            "policy_violation",
            "sensitive_review_required",
            "contradiction_requires_review",
        ):
            if type(getattr(self, field_name)) is not bool:
                raise TypeError(f"{field_name} must be a bool")

        if not isinstance(self.source_security_status, SourceSecurityStatus):
            raise TypeError(
                "source_security_status must be a SourceSecurityStatus"
            )


class EpisodicAdmissionOutcome(StrEnum):
    REJECT = "reject"
    HOLD = "hold"
    ELIGIBLE = "eligible"


class EpisodicAdmissionReason(StrEnum):
    POLICY_VIOLATION = "policy_violation"
    OUT_OF_SCOPE = "out_of_scope"
    TEMPORAL_EXPIRED = "temporal_expired"
    TAINTED_SOURCE = "tainted_source"
    REVOKED_SOURCE = "revoked_source"
    MISSING_SOURCE_AUTHORITY_ASSESSMENT = (
        "missing_source_authority_assessment"
    )
    MISSING_CONFIDENCE_ASSESSMENT = "missing_confidence_assessment"
    MISSING_SENSITIVITY_CLASSIFICATION = (
        "missing_sensitivity_classification"
    )
    TEMPORAL_UNASSESSED = "temporal_unassessed"
    TEMPORAL_NOT_YET_VALID = "temporal_not_yet_valid"
    SOURCE_UNASSESSED = "source_unassessed"
    SUSPECT_SOURCE = "suspect_source"
    SENSITIVE_REVIEW_REQUIRED = "sensitive_review_required"
    CONTRADICTION_REQUIRES_REVIEW = "contradiction_requires_review"
    ELIGIBLE = "eligible"


@dataclass(frozen=True, slots=True)
class EpisodicAdmissionDecision:
    candidate_id: str
    outcome: EpisodicAdmissionOutcome
    reason_code: EpisodicAdmissionReason
    evaluated_at: datetime
    policy_version: str = POLICY_VERSION

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "candidate_id",
            _require_canonical_text(self.candidate_id, "candidate_id"),
        )
        if not isinstance(self.outcome, EpisodicAdmissionOutcome):
            raise TypeError("outcome must be an EpisodicAdmissionOutcome")
        if not isinstance(self.reason_code, EpisodicAdmissionReason):
            raise TypeError("reason_code must be an EpisodicAdmissionReason")
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

    @property
    def human_review_required(self) -> bool:
        return self.outcome is EpisodicAdmissionOutcome.HOLD


def _decision(
    candidate: EpisodicMemoryCandidate,
    outcome: EpisodicAdmissionOutcome,
    reason_code: EpisodicAdmissionReason,
    evaluated_at: datetime,
) -> EpisodicAdmissionDecision:
    return EpisodicAdmissionDecision(
        candidate_id=candidate.candidate_id,
        outcome=outcome,
        reason_code=reason_code,
        evaluated_at=evaluated_at,
    )


def evaluate_episodic_candidate(
    candidate: EpisodicMemoryCandidate,
    signals: EpisodicAdmissionSignals,
    evaluated_at: datetime,
) -> EpisodicAdmissionDecision:
    if not isinstance(candidate, EpisodicMemoryCandidate):
        raise TypeError("candidate must be an EpisodicMemoryCandidate")
    if not isinstance(signals, EpisodicAdmissionSignals):
        raise TypeError("signals must be EpisodicAdmissionSignals")

    evaluated_at = _require_utc_datetime(evaluated_at, "evaluated_at")
    control = candidate.control

    if signals.policy_violation:
        return _decision(
            candidate,
            EpisodicAdmissionOutcome.REJECT,
            EpisodicAdmissionReason.POLICY_VIOLATION,
            evaluated_at,
        )

    if not signals.scope_applicable:
        return _decision(
            candidate,
            EpisodicAdmissionOutcome.REJECT,
            EpisodicAdmissionReason.OUT_OF_SCOPE,
            evaluated_at,
        )

    if control.valid_until is not None and evaluated_at >= control.valid_until:
        return _decision(
            candidate,
            EpisodicAdmissionOutcome.REJECT,
            EpisodicAdmissionReason.TEMPORAL_EXPIRED,
            evaluated_at,
        )

    if signals.source_security_status is SourceSecurityStatus.TAINTED:
        return _decision(
            candidate,
            EpisodicAdmissionOutcome.REJECT,
            EpisodicAdmissionReason.TAINTED_SOURCE,
            evaluated_at,
        )

    if signals.source_security_status is SourceSecurityStatus.REVOKED:
        return _decision(
            candidate,
            EpisodicAdmissionOutcome.REJECT,
            EpisodicAdmissionReason.REVOKED_SOURCE,
            evaluated_at,
        )

    if control.source_authority_classification is None:
        return _decision(
            candidate,
            EpisodicAdmissionOutcome.HOLD,
            EpisodicAdmissionReason.MISSING_SOURCE_AUTHORITY_ASSESSMENT,
            evaluated_at,
        )

    if control.confidence_classification is None:
        return _decision(
            candidate,
            EpisodicAdmissionOutcome.HOLD,
            EpisodicAdmissionReason.MISSING_CONFIDENCE_ASSESSMENT,
            evaluated_at,
        )

    if control.sensitivity_classification is None:
        return _decision(
            candidate,
            EpisodicAdmissionOutcome.HOLD,
            EpisodicAdmissionReason.MISSING_SENSITIVITY_CLASSIFICATION,
            evaluated_at,
        )

    if control.valid_until is None:
        return _decision(
            candidate,
            EpisodicAdmissionOutcome.HOLD,
            EpisodicAdmissionReason.TEMPORAL_UNASSESSED,
            evaluated_at,
        )

    if control.valid_from is not None and evaluated_at < control.valid_from:
        return _decision(
            candidate,
            EpisodicAdmissionOutcome.HOLD,
            EpisodicAdmissionReason.TEMPORAL_NOT_YET_VALID,
            evaluated_at,
        )

    if signals.source_security_status is SourceSecurityStatus.UNASSESSED:
        return _decision(
            candidate,
            EpisodicAdmissionOutcome.HOLD,
            EpisodicAdmissionReason.SOURCE_UNASSESSED,
            evaluated_at,
        )

    if signals.source_security_status is SourceSecurityStatus.SUSPECT:
        return _decision(
            candidate,
            EpisodicAdmissionOutcome.HOLD,
            EpisodicAdmissionReason.SUSPECT_SOURCE,
            evaluated_at,
        )

    if signals.sensitive_review_required:
        return _decision(
            candidate,
            EpisodicAdmissionOutcome.HOLD,
            EpisodicAdmissionReason.SENSITIVE_REVIEW_REQUIRED,
            evaluated_at,
        )

    if signals.contradiction_requires_review:
        return _decision(
            candidate,
            EpisodicAdmissionOutcome.HOLD,
            EpisodicAdmissionReason.CONTRADICTION_REQUIRES_REVIEW,
            evaluated_at,
        )

    return _decision(
        candidate,
        EpisodicAdmissionOutcome.ELIGIBLE,
        EpisodicAdmissionReason.ELIGIBLE,
        evaluated_at,
    )
