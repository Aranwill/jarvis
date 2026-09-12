from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import StrEnum

from malak.core.protected_finalization import (
    AssuranceApplicability,
    ProtectedFinalizationInput,
    ProtectedResponseCandidate,
)
from malak.security.contracts import (
    AuthorizationDecision,
    AuthorizationRequest,
    PermissionScope,
)


POLICY_VERSION = "assurance-signal-projection/v1"
SIGNAL_POLICY_VERSION = "assurance-signal-authority/v1"
_MAX_SIGNALS = 5


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


class AssuranceSignalKind(StrEnum):
    APPLICABILITY = "applicability"
    EVIDENCE_REQUIRED = "evidence_required"
    SUPPORT_SUFFICIENT = "support_sufficient"
    CONTRADICTION_UNRESOLVED = "contradiction_unresolved"
    POLICY_VIOLATION = "policy_violation"


@dataclass(frozen=True, slots=True)
class AssuranceSignalObservation:
    signal_kind: AssuranceSignalKind
    value: object
    request_id: str
    session_id: str
    producer_subject_id: str
    signal_policy_version: str

    def __post_init__(self) -> None:
        if not isinstance(self.signal_kind, AssuranceSignalKind):
            raise TypeError("signal_kind must be an AssuranceSignalKind")
        for field_name in (
            "request_id",
            "session_id",
            "producer_subject_id",
            "signal_policy_version",
        ):
            object.__setattr__(
                self,
                field_name,
                _require_canonical_text(getattr(self, field_name), field_name),
            )


@dataclass(frozen=True, slots=True)
class AssuranceSignalProducerAuthorizationEvidence:
    signal_kind: AssuranceSignalKind
    canonical_value: str
    request_id: str
    session_id: str
    producer_subject_id: str
    authorization_request: AuthorizationRequest
    authorization_decision: AuthorizationDecision

    def __post_init__(self) -> None:
        if not isinstance(self.signal_kind, AssuranceSignalKind):
            raise TypeError("signal_kind must be an AssuranceSignalKind")
        for field_name in (
            "canonical_value",
            "request_id",
            "session_id",
            "producer_subject_id",
        ):
            object.__setattr__(
                self,
                field_name,
                _require_canonical_text(getattr(self, field_name), field_name),
            )
        if not isinstance(self.authorization_request, AuthorizationRequest):
            raise TypeError("authorization_request must be an AuthorizationRequest")
        if not isinstance(self.authorization_decision, AuthorizationDecision):
            raise TypeError("authorization_decision must be an AuthorizationDecision")


class AssuranceSignalProjectionOutcome(StrEnum):
    READY = "ready"
    HOLD = "hold"
    DENIED = "denied"


class AssuranceSignalProjectionReason(StrEnum):
    MISSING_SIGNAL = "missing_signal"
    MISSING_AUTHORIZATION_EVIDENCE = "missing_authorization_evidence"
    DUPLICATE_SIGNAL = "duplicate_signal"
    DUPLICATE_AUTHORIZATION_EVIDENCE = "duplicate_authorization_evidence"
    DUPLICATE_AUTHORIZATION_REQUEST_ID = "duplicate_authorization_request_id"
    INPUT_CARDINALITY_EXCEEDED = "input_cardinality_exceeded"
    REQUEST_ID_MISMATCH = "request_id_mismatch"
    SESSION_ID_MISMATCH = "session_id_mismatch"
    SIGNAL_KIND_MISMATCH = "signal_kind_mismatch"
    SIGNAL_VALUE_MISMATCH = "signal_value_mismatch"
    SIGNAL_VALUE_INVALID = "signal_value_invalid"
    SIGNAL_SET_INCOHERENT = "signal_set_incoherent"
    PRODUCER_SUBJECT_MISMATCH = "producer_subject_mismatch"
    PRODUCER_NOT_AUTHENTICATED = "producer_not_authenticated"
    PERMISSION_SCOPE_MISMATCH = "permission_scope_mismatch"
    DECISION_REQUEST_MISMATCH = "decision_request_mismatch"
    AUTHORIZATION_REQUEST_TIME_INVALID = "authorization_request_time_invalid"
    CONTEXT_NOT_YET_VALID = "context_not_yet_valid"
    CONTEXT_EXPIRED = "context_expired"
    AUTHORIZATION_DENIED = "authorization_denied"
    SIGNAL_POLICY_VERSION_MISMATCH = "signal_policy_version_mismatch"
    READY = "ready"


@dataclass(frozen=True, slots=True)
class AssuranceSignalProjectionDecision:
    request_id: str
    outcome: AssuranceSignalProjectionOutcome
    reason_code: AssuranceSignalProjectionReason
    evaluated_at: datetime
    projected_input: ProtectedFinalizationInput | None = None
    policy_version: str = POLICY_VERSION

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "request_id",
            _require_canonical_text(self.request_id, "request_id"),
        )
        if not isinstance(self.outcome, AssuranceSignalProjectionOutcome):
            raise TypeError("outcome must be an AssuranceSignalProjectionOutcome")
        if not isinstance(self.reason_code, AssuranceSignalProjectionReason):
            raise TypeError("reason_code must be an AssuranceSignalProjectionReason")
        object.__setattr__(
            self,
            "evaluated_at",
            _require_utc_datetime(self.evaluated_at, "evaluated_at"),
        )
        if self.projected_input is not None and not isinstance(
            self.projected_input,
            ProtectedFinalizationInput,
        ):
            raise TypeError(
                "projected_input must be a ProtectedFinalizationInput or None"
            )
        if self.outcome is AssuranceSignalProjectionOutcome.READY:
            if self.projected_input is None:
                raise ValueError("READY requires projected_input")
        elif self.projected_input is not None:
            raise ValueError("non-READY outcome must not contain projected_input")
        object.__setattr__(
            self,
            "policy_version",
            _require_canonical_text(self.policy_version, "policy_version"),
        )


def _canonical_signal_value(
    kind: AssuranceSignalKind,
    value: object,
) -> str | None:
    if kind is AssuranceSignalKind.APPLICABILITY:
        if not isinstance(value, AssuranceApplicability):
            return None
        return value.value
    if type(value) is not bool:
        return None
    return "true" if value else "false"


def required_permission_for_signal(
    kind: AssuranceSignalKind,
    value: object,
) -> PermissionScope | None:
    if not isinstance(kind, AssuranceSignalKind):
        raise TypeError("kind must be an AssuranceSignalKind")
    canonical_value = _canonical_signal_value(kind, value)
    if canonical_value is None:
        return None
    return PermissionScope(
        resource=f"cognition.assurance_signal.{kind.value}",
        action=f"produce.{canonical_value}",
    )


def _result(
    candidate: ProtectedResponseCandidate,
    outcome: AssuranceSignalProjectionOutcome,
    reason: AssuranceSignalProjectionReason,
    evaluated_at: datetime,
    *,
    projected_input: ProtectedFinalizationInput | None = None,
) -> AssuranceSignalProjectionDecision:
    return AssuranceSignalProjectionDecision(
        request_id=candidate.request_id,
        outcome=outcome,
        reason_code=reason,
        evaluated_at=evaluated_at,
        projected_input=projected_input,
    )


def _denied(
    candidate: ProtectedResponseCandidate,
    reason: AssuranceSignalProjectionReason,
    evaluated_at: datetime,
) -> AssuranceSignalProjectionDecision:
    return _result(
        candidate,
        AssuranceSignalProjectionOutcome.DENIED,
        reason,
        evaluated_at,
    )


def _hold(
    candidate: ProtectedResponseCandidate,
    reason: AssuranceSignalProjectionReason,
    evaluated_at: datetime,
) -> AssuranceSignalProjectionDecision:
    return _result(
        candidate,
        AssuranceSignalProjectionOutcome.HOLD,
        reason,
        evaluated_at,
    )


def project_assurance_signals(
    candidate: ProtectedResponseCandidate,
    observations: tuple[AssuranceSignalObservation, ...],
    authorization_evidence: tuple[
        AssuranceSignalProducerAuthorizationEvidence,
        ...,
    ],
    evaluated_at: datetime,
) -> AssuranceSignalProjectionDecision:
    if not isinstance(candidate, ProtectedResponseCandidate):
        raise TypeError("candidate must be a ProtectedResponseCandidate")
    if type(observations) is not tuple:
        raise TypeError("observations must be a materialized tuple")
    if type(authorization_evidence) is not tuple:
        raise TypeError("authorization_evidence must be a materialized tuple")
    if not all(isinstance(item, AssuranceSignalObservation) for item in observations):
        raise TypeError("observations must contain AssuranceSignalObservation values")
    if not all(
        isinstance(item, AssuranceSignalProducerAuthorizationEvidence)
        for item in authorization_evidence
    ):
        raise TypeError(
            "authorization_evidence must contain "
            "AssuranceSignalProducerAuthorizationEvidence values"
        )

    evaluated_at = _require_utc_datetime(evaluated_at, "evaluated_at")
    for item in authorization_evidence:
        context = item.authorization_request.context
        _require_utc_datetime(context.issued_at, "context.issued_at")
        _require_utc_datetime(context.expires_at, "context.expires_at")
        _require_utc_datetime(
            item.authorization_request.created_at,
            "authorization_request.created_at",
        )

    if (
        len(observations) > _MAX_SIGNALS
        or len(authorization_evidence) > _MAX_SIGNALS
    ):
        return _denied(
            candidate,
            AssuranceSignalProjectionReason.INPUT_CARDINALITY_EXCEEDED,
            evaluated_at,
        )

    observation_counts = Counter(item.signal_kind for item in observations)
    evidence_counts = Counter(item.signal_kind for item in authorization_evidence)
    if any(count > 1 for count in observation_counts.values()):
        return _denied(
            candidate,
            AssuranceSignalProjectionReason.DUPLICATE_SIGNAL,
            evaluated_at,
        )
    if any(count > 1 for count in evidence_counts.values()):
        return _denied(
            candidate,
            AssuranceSignalProjectionReason.DUPLICATE_AUTHORIZATION_EVIDENCE,
            evaluated_at,
        )
    request_id_counts = Counter(
        item.authorization_request.request_id
        for item in authorization_evidence
    )
    if any(count > 1 for count in request_id_counts.values()):
        return _denied(
            candidate,
            AssuranceSignalProjectionReason.DUPLICATE_AUTHORIZATION_REQUEST_ID,
            evaluated_at,
        )

    required_kinds = frozenset(AssuranceSignalKind)
    if frozenset(observation_counts) != required_kinds:
        return _hold(
            candidate,
            AssuranceSignalProjectionReason.MISSING_SIGNAL,
            evaluated_at,
        )
    if frozenset(evidence_counts) != required_kinds:
        return _hold(
            candidate,
            AssuranceSignalProjectionReason.MISSING_AUTHORIZATION_EVIDENCE,
            evaluated_at,
        )

    observation_by_kind = {item.signal_kind: item for item in observations}
    evidence_by_kind = {
        item.signal_kind: item for item in authorization_evidence
    }

    if any(
        item.request_id != candidate.request_id
        for item in observations
    ) or any(
        item.request_id != candidate.request_id
        for item in authorization_evidence
    ):
        return _denied(
            candidate,
            AssuranceSignalProjectionReason.REQUEST_ID_MISMATCH,
            evaluated_at,
        )

    if any(
        item.session_id != candidate.session_id
        for item in observations
    ) or any(
        item.session_id != candidate.session_id
        or item.authorization_request.context.session_id != candidate.session_id
        for item in authorization_evidence
    ):
        return _denied(
            candidate,
            AssuranceSignalProjectionReason.SESSION_ID_MISMATCH,
            evaluated_at,
        )

    canonical_values: dict[AssuranceSignalKind, str] = {}
    for kind in AssuranceSignalKind:
        observation = observation_by_kind[kind]
        canonical = _canonical_signal_value(kind, observation.value)
        if canonical is None:
            return _denied(
                candidate,
                AssuranceSignalProjectionReason.SIGNAL_VALUE_INVALID,
                evaluated_at,
            )
        canonical_values[kind] = canonical
    if any(
        evidence_by_kind[kind].canonical_value != canonical_values[kind]
        for kind in AssuranceSignalKind
    ):
        return _denied(
            candidate,
            AssuranceSignalProjectionReason.SIGNAL_VALUE_MISMATCH,
            evaluated_at,
        )

    if any(
        evidence_by_kind[kind].producer_subject_id
        != observation_by_kind[kind].producer_subject_id
        or evidence_by_kind[kind].producer_subject_id
        != evidence_by_kind[kind].authorization_request.context.subject_id
        for kind in AssuranceSignalKind
    ):
        return _denied(
            candidate,
            AssuranceSignalProjectionReason.PRODUCER_SUBJECT_MISMATCH,
            evaluated_at,
        )
    if any(
        evidence_by_kind[kind].authorization_request.context.authenticated
        is not True
        for kind in AssuranceSignalKind
    ):
        return _denied(
            candidate,
            AssuranceSignalProjectionReason.PRODUCER_NOT_AUTHENTICATED,
            evaluated_at,
        )

    for kind in AssuranceSignalKind:
        expected_permission = required_permission_for_signal(
            kind,
            observation_by_kind[kind].value,
        )
        if evidence_by_kind[kind].authorization_request.permission != expected_permission:
            return _denied(
                candidate,
                AssuranceSignalProjectionReason.PERMISSION_SCOPE_MISMATCH,
                evaluated_at,
            )

    contexts = [
        evidence_by_kind[kind].authorization_request.context
        for kind in AssuranceSignalKind
    ]
    requests = [
        evidence_by_kind[kind].authorization_request
        for kind in AssuranceSignalKind
    ]
    if any(evaluated_at < context.issued_at for context in contexts):
        return _denied(
            candidate,
            AssuranceSignalProjectionReason.CONTEXT_NOT_YET_VALID,
            evaluated_at,
        )
    if any(evaluated_at >= context.expires_at for context in contexts):
        return _denied(
            candidate,
            AssuranceSignalProjectionReason.CONTEXT_EXPIRED,
            evaluated_at,
        )
    if any(
        request.created_at < request.context.issued_at
        or request.created_at > evaluated_at
        for request in requests
    ):
        return _denied(
            candidate,
            AssuranceSignalProjectionReason.AUTHORIZATION_REQUEST_TIME_INVALID,
            evaluated_at,
        )

    if any(
        evidence_by_kind[kind].authorization_decision.request_id
        != evidence_by_kind[kind].authorization_request.request_id
        for kind in AssuranceSignalKind
    ):
        return _denied(
            candidate,
            AssuranceSignalProjectionReason.DECISION_REQUEST_MISMATCH,
            evaluated_at,
        )
    if any(
        evidence_by_kind[kind].authorization_decision.allowed is False
        for kind in AssuranceSignalKind
    ):
        return _denied(
            candidate,
            AssuranceSignalProjectionReason.AUTHORIZATION_DENIED,
            evaluated_at,
        )

    if any(
        observation_by_kind[kind].signal_policy_version
        != SIGNAL_POLICY_VERSION
        for kind in AssuranceSignalKind
    ):
        return _denied(
            candidate,
            AssuranceSignalProjectionReason.SIGNAL_POLICY_VERSION_MISMATCH,
            evaluated_at,
        )

    applicability = observation_by_kind[AssuranceSignalKind.APPLICABILITY].value
    evidence_required = observation_by_kind[
        AssuranceSignalKind.EVIDENCE_REQUIRED
    ].value
    support_sufficient = observation_by_kind[
        AssuranceSignalKind.SUPPORT_SUFFICIENT
    ].value
    contradiction_unresolved = observation_by_kind[
        AssuranceSignalKind.CONTRADICTION_UNRESOLVED
    ].value
    policy_violation = observation_by_kind[
        AssuranceSignalKind.POLICY_VIOLATION
    ].value

    if applicability is AssuranceApplicability.NOT_APPLICABLE and (
        evidence_required is not False
        or support_sufficient is not False
        or contradiction_unresolved is not False
    ):
        return _denied(
            candidate,
            AssuranceSignalProjectionReason.SIGNAL_SET_INCOHERENT,
            evaluated_at,
        )

    projected_input = ProtectedFinalizationInput(
        applicability=applicability,
        evidence_required=evidence_required,
        support_sufficient=support_sufficient,
        contradiction_unresolved=contradiction_unresolved,
        policy_violation=policy_violation,
    )
    return _result(
        candidate,
        AssuranceSignalProjectionOutcome.READY,
        AssuranceSignalProjectionReason.READY,
        evaluated_at,
        projected_input=projected_input,
    )
