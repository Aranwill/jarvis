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


def _canonical_text(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    if not value.strip():
        raise ValueError(f"{field_name} must not be empty")
    if value.strip() != value:
        raise ValueError(f"{field_name} must not contain surrounding whitespace")
    return value


def _utc(value: datetime, field_name: str) -> datetime:
    if not isinstance(value, datetime):
        raise TypeError(f"{field_name} must be a datetime")
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{field_name} must include timezone information")
    if value.utcoffset() != timedelta(0):
        raise ValueError(f"{field_name} must be UTC")
    return value


def _normalize_text_fields(instance: object, names: tuple[str, ...]) -> None:
    for name in names:
        object.__setattr__(
            instance,
            name,
            _canonical_text(getattr(instance, name), name),
        )


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
        _normalize_text_fields(
            self,
            (
                "request_id",
                "session_id",
                "producer_subject_id",
                "signal_policy_version",
            ),
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
        _normalize_text_fields(
            self,
            (
                "canonical_value",
                "request_id",
                "session_id",
                "producer_subject_id",
            ),
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
            _canonical_text(self.request_id, "request_id"),
        )
        if not isinstance(self.outcome, AssuranceSignalProjectionOutcome):
            raise TypeError("outcome must be an AssuranceSignalProjectionOutcome")
        if not isinstance(self.reason_code, AssuranceSignalProjectionReason):
            raise TypeError("reason_code must be an AssuranceSignalProjectionReason")
        object.__setattr__(self, "evaluated_at", _utc(self.evaluated_at, "evaluated_at"))
        if self.projected_input is not None and not isinstance(
            self.projected_input, ProtectedFinalizationInput
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
            _canonical_text(self.policy_version, "policy_version"),
        )


def _signal_value(kind: AssuranceSignalKind, value: object) -> str | None:
    if kind is AssuranceSignalKind.APPLICABILITY:
        return value.value if isinstance(value, AssuranceApplicability) else None
    if type(value) is not bool:
        return None
    return "true" if value else "false"


def required_permission_for_signal(
    kind: AssuranceSignalKind,
    value: object,
) -> PermissionScope | None:
    if not isinstance(kind, AssuranceSignalKind):
        raise TypeError("kind must be an AssuranceSignalKind")
    canonical = _signal_value(kind, value)
    if canonical is None:
        return None
    return PermissionScope(
        resource=f"cognition.assurance_signal.{kind.value}",
        action=f"produce.{canonical}",
    )


def _decision(
    candidate: ProtectedResponseCandidate,
    outcome: AssuranceSignalProjectionOutcome,
    reason: AssuranceSignalProjectionReason,
    evaluated_at: datetime,
    projected_input: ProtectedFinalizationInput | None = None,
) -> AssuranceSignalProjectionDecision:
    return AssuranceSignalProjectionDecision(
        request_id=candidate.request_id,
        outcome=outcome,
        reason_code=reason,
        evaluated_at=evaluated_at,
        projected_input=projected_input,
    )


def project_assurance_signals(
    candidate: ProtectedResponseCandidate,
    observations: tuple[AssuranceSignalObservation, ...],
    authorization_evidence: tuple[
        AssuranceSignalProducerAuthorizationEvidence, ...
    ],
    evaluated_at: datetime,
) -> AssuranceSignalProjectionDecision:
    if not isinstance(candidate, ProtectedResponseCandidate):
        raise TypeError("candidate must be a ProtectedResponseCandidate")
    if type(observations) is not tuple:
        raise TypeError("observations must be a materialized tuple")
    if type(authorization_evidence) is not tuple:
        raise TypeError("authorization_evidence must be a materialized tuple")
    if not all(isinstance(x, AssuranceSignalObservation) for x in observations):
        raise TypeError("observations must contain AssuranceSignalObservation values")
    if not all(
        isinstance(x, AssuranceSignalProducerAuthorizationEvidence)
        for x in authorization_evidence
    ):
        raise TypeError(
            "authorization_evidence must contain "
            "AssuranceSignalProducerAuthorizationEvidence values"
        )

    evaluated_at = _utc(evaluated_at, "evaluated_at")
    for item in authorization_evidence:
        request = item.authorization_request
        _utc(request.context.issued_at, "context.issued_at")
        _utc(request.context.expires_at, "context.expires_at")
        _utc(request.created_at, "authorization_request.created_at")

    deny = lambda reason: _decision(  # noqa: E731
        candidate,
        AssuranceSignalProjectionOutcome.DENIED,
        reason,
        evaluated_at,
    )
    hold = lambda reason: _decision(  # noqa: E731
        candidate,
        AssuranceSignalProjectionOutcome.HOLD,
        reason,
        evaluated_at,
    )

    if max(len(observations), len(authorization_evidence)) > _MAX_SIGNALS:
        return deny(AssuranceSignalProjectionReason.INPUT_CARDINALITY_EXCEEDED)

    observation_counts = Counter(x.signal_kind for x in observations)
    evidence_counts = Counter(x.signal_kind for x in authorization_evidence)
    if any(count > 1 for count in observation_counts.values()):
        return deny(AssuranceSignalProjectionReason.DUPLICATE_SIGNAL)
    if any(count > 1 for count in evidence_counts.values()):
        return deny(AssuranceSignalProjectionReason.DUPLICATE_AUTHORIZATION_EVIDENCE)
    auth_request_counts = Counter(
        x.authorization_request.request_id for x in authorization_evidence
    )
    if any(count > 1 for count in auth_request_counts.values()):
        return deny(AssuranceSignalProjectionReason.DUPLICATE_AUTHORIZATION_REQUEST_ID)

    required_kinds = frozenset(AssuranceSignalKind)
    if frozenset(observation_counts) != required_kinds:
        return hold(AssuranceSignalProjectionReason.MISSING_SIGNAL)
    if frozenset(evidence_counts) != required_kinds:
        return hold(AssuranceSignalProjectionReason.MISSING_AUTHORIZATION_EVIDENCE)

    obs = {x.signal_kind: x for x in observations}
    auth = {x.signal_kind: x for x in authorization_evidence}

    if any(x.request_id != candidate.request_id for x in observations) or any(
        x.request_id != candidate.request_id for x in authorization_evidence
    ):
        return deny(AssuranceSignalProjectionReason.REQUEST_ID_MISMATCH)
    if any(x.session_id != candidate.session_id for x in observations) or any(
        x.session_id != candidate.session_id
        or x.authorization_request.context.session_id != candidate.session_id
        for x in authorization_evidence
    ):
        return deny(AssuranceSignalProjectionReason.SESSION_ID_MISMATCH)

    canonical: dict[AssuranceSignalKind, str] = {}
    for kind in AssuranceSignalKind:
        value = _signal_value(kind, obs[kind].value)
        if value is None:
            return deny(AssuranceSignalProjectionReason.SIGNAL_VALUE_INVALID)
        canonical[kind] = value
    if any(auth[k].canonical_value != canonical[k] for k in AssuranceSignalKind):
        return deny(AssuranceSignalProjectionReason.SIGNAL_VALUE_MISMATCH)

    if any(
        auth[k].producer_subject_id != obs[k].producer_subject_id
        or auth[k].producer_subject_id
        != auth[k].authorization_request.context.subject_id
        for k in AssuranceSignalKind
    ):
        return deny(AssuranceSignalProjectionReason.PRODUCER_SUBJECT_MISMATCH)
    if any(
        auth[k].authorization_request.context.authenticated is not True
        for k in AssuranceSignalKind
    ):
        return deny(AssuranceSignalProjectionReason.PRODUCER_NOT_AUTHENTICATED)

    if any(
        auth[k].authorization_request.permission
        != required_permission_for_signal(k, obs[k].value)
        for k in AssuranceSignalKind
    ):
        return deny(AssuranceSignalProjectionReason.PERMISSION_SCOPE_MISMATCH)

    requests = [auth[k].authorization_request for k in AssuranceSignalKind]
    if any(evaluated_at < request.context.issued_at for request in requests):
        return deny(AssuranceSignalProjectionReason.CONTEXT_NOT_YET_VALID)
    if any(evaluated_at >= request.context.expires_at for request in requests):
        return deny(AssuranceSignalProjectionReason.CONTEXT_EXPIRED)
    if any(
        request.created_at < request.context.issued_at
        or request.created_at > evaluated_at
        for request in requests
    ):
        return deny(AssuranceSignalProjectionReason.AUTHORIZATION_REQUEST_TIME_INVALID)

    if any(
        auth[k].authorization_decision.request_id
        != auth[k].authorization_request.request_id
        for k in AssuranceSignalKind
    ):
        return deny(AssuranceSignalProjectionReason.DECISION_REQUEST_MISMATCH)
    if any(
        auth[k].authorization_decision.allowed is False
        for k in AssuranceSignalKind
    ):
        return deny(AssuranceSignalProjectionReason.AUTHORIZATION_DENIED)

    if any(
        obs[k].signal_policy_version != SIGNAL_POLICY_VERSION
        for k in AssuranceSignalKind
    ):
        return deny(AssuranceSignalProjectionReason.SIGNAL_POLICY_VERSION_MISMATCH)

    applicability = obs[AssuranceSignalKind.APPLICABILITY].value
    evidence_required = obs[AssuranceSignalKind.EVIDENCE_REQUIRED].value
    support_sufficient = obs[AssuranceSignalKind.SUPPORT_SUFFICIENT].value
    contradiction_unresolved = obs[
        AssuranceSignalKind.CONTRADICTION_UNRESOLVED
    ].value
    policy_violation = obs[AssuranceSignalKind.POLICY_VIOLATION].value

    if applicability is AssuranceApplicability.NOT_APPLICABLE and (
        evidence_required is not False
        or support_sufficient is not False
        or contradiction_unresolved is not False
    ):
        return deny(AssuranceSignalProjectionReason.SIGNAL_SET_INCOHERENT)

    projected = ProtectedFinalizationInput(
        applicability=applicability,
        evidence_required=evidence_required,
        support_sufficient=support_sufficient,
        contradiction_unresolved=contradiction_unresolved,
        policy_violation=policy_violation,
    )
    return _decision(
        candidate,
        AssuranceSignalProjectionOutcome.READY,
        AssuranceSignalProjectionReason.READY,
        evaluated_at,
        projected,
    )
