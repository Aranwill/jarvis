from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import StrEnum


POLICY_VERSION = "protected-finalization/v1"


def _require_canonical_text(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")

    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must not be empty")
    if normalized != value:
        raise ValueError(f"{field_name} must not contain surrounding whitespace")

    return value


def _require_non_blank_string(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    if not value.strip():
        raise ValueError(f"{field_name} must not be blank")
    return value


def _optional_canonical_text(
    value: str | None,
    field_name: str,
) -> str | None:
    if value is None:
        return None
    return _require_canonical_text(value, field_name)


def _require_bool(value: bool, field_name: str) -> bool:
    if type(value) is not bool:
        raise TypeError(f"{field_name} must be a bool")
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
class ProtectedResponseCandidate:
    request_id: str
    session_id: str
    content: str
    provider: str | None = None
    model: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "request_id",
            _require_canonical_text(self.request_id, "request_id"),
        )
        object.__setattr__(
            self,
            "session_id",
            _require_canonical_text(self.session_id, "session_id"),
        )
        object.__setattr__(
            self,
            "content",
            _require_non_blank_string(self.content, "content"),
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


class AssuranceApplicability(StrEnum):
    NOT_APPLICABLE = "not_applicable"
    REQUIRED = "required"
    UNRESOLVED = "unresolved"


@dataclass(frozen=True, slots=True)
class ProtectedFinalizationInput:
    applicability: AssuranceApplicability
    evidence_required: bool
    support_sufficient: bool
    contradiction_unresolved: bool
    policy_violation: bool

    def __post_init__(self) -> None:
        if not isinstance(self.applicability, AssuranceApplicability):
            raise TypeError(
                "applicability must be an AssuranceApplicability"
            )

        for field_name in (
            "evidence_required",
            "support_sufficient",
            "contradiction_unresolved",
            "policy_violation",
        ):
            object.__setattr__(
                self,
                field_name,
                _require_bool(getattr(self, field_name), field_name),
            )


class ProtectedFinalizationOutcome(StrEnum):
    ACCEPT = "accept"
    ABSTAIN = "abstain"
    BLOCK = "block"


class ProtectedFinalizationReason(StrEnum):
    POLICY_VIOLATION = "policy_violation"
    APPLICABILITY_UNRESOLVED = "applicability_unresolved"
    INCONSISTENT_ASSURANCE_INPUT = "inconsistent_assurance_input"
    ASSURANCE_NOT_APPLICABLE = "assurance_not_applicable"
    CONTRADICTION_UNRESOLVED = "contradiction_unresolved"
    INSUFFICIENT_SUPPORT = "insufficient_support"
    ASSURANCE_SATISFIED = "assurance_satisfied"


@dataclass(frozen=True, slots=True)
class ProtectedFinalizationDecision:
    request_id: str
    outcome: ProtectedFinalizationOutcome
    reason_code: ProtectedFinalizationReason
    evaluated_at: datetime
    policy_version: str = POLICY_VERSION

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "request_id",
            _require_canonical_text(self.request_id, "request_id"),
        )
        if not isinstance(self.outcome, ProtectedFinalizationOutcome):
            raise TypeError(
                "outcome must be a ProtectedFinalizationOutcome"
            )
        if not isinstance(self.reason_code, ProtectedFinalizationReason):
            raise TypeError(
                "reason_code must be a ProtectedFinalizationReason"
            )
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


def _decision(
    candidate: ProtectedResponseCandidate,
    outcome: ProtectedFinalizationOutcome,
    reason_code: ProtectedFinalizationReason,
    evaluated_at: datetime,
) -> ProtectedFinalizationDecision:
    return ProtectedFinalizationDecision(
        request_id=candidate.request_id,
        outcome=outcome,
        reason_code=reason_code,
        evaluated_at=evaluated_at,
    )


def evaluate_protected_finalization(
    candidate: ProtectedResponseCandidate,
    assurance_input: ProtectedFinalizationInput,
    evaluated_at: datetime,
) -> ProtectedFinalizationDecision:
    if not isinstance(candidate, ProtectedResponseCandidate):
        raise TypeError("candidate must be a ProtectedResponseCandidate")
    if not isinstance(assurance_input, ProtectedFinalizationInput):
        raise TypeError(
            "assurance_input must be a ProtectedFinalizationInput"
        )

    evaluated_at = _require_utc_datetime(evaluated_at, "evaluated_at")

    if assurance_input.policy_violation:
        return _decision(
            candidate,
            ProtectedFinalizationOutcome.BLOCK,
            ProtectedFinalizationReason.POLICY_VIOLATION,
            evaluated_at,
        )

    if assurance_input.applicability is AssuranceApplicability.UNRESOLVED:
        return _decision(
            candidate,
            ProtectedFinalizationOutcome.ABSTAIN,
            ProtectedFinalizationReason.APPLICABILITY_UNRESOLVED,
            evaluated_at,
        )

    if (
        assurance_input.applicability is AssuranceApplicability.NOT_APPLICABLE
        and assurance_input.evidence_required
    ):
        return _decision(
            candidate,
            ProtectedFinalizationOutcome.ABSTAIN,
            ProtectedFinalizationReason.INCONSISTENT_ASSURANCE_INPUT,
            evaluated_at,
        )

    if assurance_input.applicability is AssuranceApplicability.NOT_APPLICABLE:
        return _decision(
            candidate,
            ProtectedFinalizationOutcome.ACCEPT,
            ProtectedFinalizationReason.ASSURANCE_NOT_APPLICABLE,
            evaluated_at,
        )

    if assurance_input.contradiction_unresolved:
        return _decision(
            candidate,
            ProtectedFinalizationOutcome.ABSTAIN,
            ProtectedFinalizationReason.CONTRADICTION_UNRESOLVED,
            evaluated_at,
        )

    if (
        assurance_input.evidence_required
        and not assurance_input.support_sufficient
    ):
        return _decision(
            candidate,
            ProtectedFinalizationOutcome.ABSTAIN,
            ProtectedFinalizationReason.INSUFFICIENT_SUPPORT,
            evaluated_at,
        )

    return _decision(
        candidate,
        ProtectedFinalizationOutcome.ACCEPT,
        ProtectedFinalizationReason.ASSURANCE_SATISFIED,
        evaluated_at,
    )
