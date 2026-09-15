from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import StrEnum
from hashlib import sha256
import json

from malak.memory.candidate_content_identity import (
    EpisodicCandidateContentIdentity,
    compute_episodic_candidate_content_identity,
)
from malak.memory.episodic_admission import (
    POLICY_VERSION as ADMISSION_POLICY_VERSION,
    EpisodicAdmissionOutcome,
    EpisodicMemoryCandidate,
)
from malak.memory.governed_projection_consumption import (
    POLICY_VERSION as CONSUMPTION_POLICY_VERSION,
    GovernedAdmissionConsumptionOutcome,
    GovernedAdmissionConsumptionReason,
    GovernedAdmissionConsumptionResult,
)
from malak.security.contracts import AuthorizationOperationBinding


POLICY_VERSION = "episodic-persistence-readiness/v1"
OPERATION_BINDING_NAMESPACE = "malak.memory.episodic_persistence"
OPERATION_BINDING_VERSION = "episodic-persistence-subject/v1"
OPERATION_BINDING_DIGEST_ALGORITHM = "sha256"
_OPERATION_BINDING_SCHEMA = "malak.episodic_persistence_subject/v1"
_OPERATION_BINDING_DOMAIN_SEPARATOR = (
    "MALAK:EPISODIC_PERSISTENCE_SUBJECT:v1\n"
)


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


def _timestamp_v1(value: datetime) -> str:
    return (
        value.astimezone(timezone.utc)
        .isoformat(timespec="microseconds")
        .replace("+00:00", "Z")
    )


@dataclass(frozen=True, slots=True)
class EpisodicPersistenceIntent:
    candidate_id: str
    candidate_content_identity: EpisodicCandidateContentIdentity
    subject_scope: str
    domain: str
    purpose: str
    created_at: datetime

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "candidate_id",
            _require_canonical_text(self.candidate_id, "candidate_id"),
        )
        if not isinstance(
            self.candidate_content_identity,
            EpisodicCandidateContentIdentity,
        ):
            raise TypeError(
                "candidate_content_identity must be an "
                "EpisodicCandidateContentIdentity"
            )
        if self.candidate_content_identity.candidate_id != self.candidate_id:
            raise ValueError(
                "candidate_content_identity candidate_id must match intent candidate_id"
            )
        for field_name in ("subject_scope", "domain", "purpose"):
            object.__setattr__(
                self,
                field_name,
                _require_canonical_text(
                    getattr(self, field_name),
                    field_name,
                ),
            )
        object.__setattr__(
            self,
            "created_at",
            _require_utc_datetime(self.created_at, "created_at"),
        )


class EpisodicPersistenceReadinessOutcome(StrEnum):
    READY = "ready"
    HOLD = "hold"
    DENIED = "denied"


class EpisodicPersistenceReadinessReason(StrEnum):
    CONSUMPTION_CANDIDATE_MISMATCH = "consumption_candidate_mismatch"
    CANDIDATE_CONTENT_IDENTITY_MISMATCH = "candidate_content_identity_mismatch"
    INTENT_CANDIDATE_MISMATCH = "intent_candidate_mismatch"
    INTENT_CONTENT_IDENTITY_MISMATCH = "intent_content_identity_mismatch"
    INTENT_CONTEXT_MISMATCH = "intent_context_mismatch"
    INTENT_FROM_FUTURE = "intent_from_future"
    UNSUPPORTED_CONSUMPTION_POLICY = "unsupported_consumption_policy"
    UNSUPPORTED_ADMISSION_POLICY = "unsupported_admission_policy"
    STALE_CONSUMPTION = "stale_consumption"
    CONSUMPTION_HOLD = "consumption_hold"
    CONSUMPTION_BLOCKED = "consumption_blocked"
    ADMISSION_HOLD = "admission_hold"
    ADMISSION_REJECTED = "admission_rejected"
    READY = "ready"


@dataclass(frozen=True, slots=True)
class EpisodicPersistenceReadinessResult:
    candidate_id: str
    candidate_content_identity: EpisodicCandidateContentIdentity
    intent: EpisodicPersistenceIntent
    outcome: EpisodicPersistenceReadinessOutcome
    reason_code: EpisodicPersistenceReadinessReason
    evaluated_at: datetime
    authorization_operation_binding: AuthorizationOperationBinding | None = None
    policy_version: str = POLICY_VERSION

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "candidate_id",
            _require_canonical_text(self.candidate_id, "candidate_id"),
        )
        if not isinstance(
            self.candidate_content_identity,
            EpisodicCandidateContentIdentity,
        ):
            raise TypeError(
                "candidate_content_identity must be an "
                "EpisodicCandidateContentIdentity"
            )
        if self.candidate_content_identity.candidate_id != self.candidate_id:
            raise ValueError(
                "candidate_content_identity candidate_id must match result candidate_id"
            )
        if not isinstance(self.intent, EpisodicPersistenceIntent):
            raise TypeError("intent must be an EpisodicPersistenceIntent")
        if not isinstance(self.outcome, EpisodicPersistenceReadinessOutcome):
            raise TypeError(
                "outcome must be an EpisodicPersistenceReadinessOutcome"
            )
        if not isinstance(self.reason_code, EpisodicPersistenceReadinessReason):
            raise TypeError(
                "reason_code must be an EpisodicPersistenceReadinessReason"
            )
        object.__setattr__(
            self,
            "evaluated_at",
            _require_utc_datetime(self.evaluated_at, "evaluated_at"),
        )
        if self.authorization_operation_binding is not None and not isinstance(
            self.authorization_operation_binding,
            AuthorizationOperationBinding,
        ):
            raise TypeError(
                "authorization_operation_binding must be an "
                "AuthorizationOperationBinding or None"
            )
        object.__setattr__(
            self,
            "policy_version",
            _require_canonical_text(self.policy_version, "policy_version"),
        )

        if self.outcome is EpisodicPersistenceReadinessOutcome.READY:
            if self.reason_code is not EpisodicPersistenceReadinessReason.READY:
                raise ValueError("READY outcome requires READY reason_code")
            if self.authorization_operation_binding is None:
                raise ValueError("READY outcome requires operation binding")
        else:
            if self.reason_code is EpisodicPersistenceReadinessReason.READY:
                raise ValueError("non-READY outcome cannot use READY reason_code")
            if self.authorization_operation_binding is not None:
                raise ValueError("non-READY outcome must not carry operation binding")


def _validate_intent_against_candidate(
    candidate: EpisodicMemoryCandidate,
    intent: EpisodicPersistenceIntent,
    evaluated_at: datetime,
) -> EpisodicCandidateContentIdentity:
    actual_identity = compute_episodic_candidate_content_identity(candidate)

    if intent.candidate_id != candidate.candidate_id:
        raise ValueError("intent candidate_id must match candidate candidate_id")
    if intent.candidate_content_identity != actual_identity:
        raise ValueError("intent content identity must match actual candidate content")
    if (
        intent.subject_scope != candidate.control.subject_scope
        or intent.domain != candidate.control.domain
        or intent.purpose != candidate.control.purpose
    ):
        raise ValueError("intent context must match candidate context")
    if intent.created_at > evaluated_at:
        raise ValueError("intent created_at must not be after evaluated_at")

    return actual_identity


def compute_episodic_persistence_operation_binding(
    candidate: EpisodicMemoryCandidate,
    intent: EpisodicPersistenceIntent,
    evaluated_at: datetime,
    *,
    consumption_policy_version: str,
    admission_policy_version: str,
) -> AuthorizationOperationBinding:
    if not isinstance(candidate, EpisodicMemoryCandidate):
        raise TypeError("candidate must be an EpisodicMemoryCandidate")
    if not isinstance(intent, EpisodicPersistenceIntent):
        raise TypeError("intent must be an EpisodicPersistenceIntent")
    evaluated_at = _require_utc_datetime(evaluated_at, "evaluated_at")
    consumption_policy_version = _require_canonical_text(
        consumption_policy_version,
        "consumption_policy_version",
    )
    admission_policy_version = _require_canonical_text(
        admission_policy_version,
        "admission_policy_version",
    )

    actual_identity = _validate_intent_against_candidate(
        candidate,
        intent,
        evaluated_at,
    )

    payload = {
        "schema": _OPERATION_BINDING_SCHEMA,
        "operation": "persist",
        "candidate_content_identity": {
            "candidate_id": actual_identity.candidate_id,
            "digest_algorithm": actual_identity.digest_algorithm,
            "digest_hex": actual_identity.digest_hex,
            "canonicalization_version": actual_identity.canonicalization_version,
            "policy_version": actual_identity.policy_version,
        },
        "intent": {
            "candidate_id": intent.candidate_id,
            "subject_scope": intent.subject_scope,
            "domain": intent.domain,
            "purpose": intent.purpose,
            "created_at": _timestamp_v1(intent.created_at),
        },
        "readiness": {
            "evaluated_at": _timestamp_v1(evaluated_at),
            "policy_version": POLICY_VERSION,
            "consumption_policy_version": consumption_policy_version,
            "admission_policy_version": admission_policy_version,
        },
    }
    canonical = json.dumps(
        payload,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )
    digest_hex = sha256(
        _OPERATION_BINDING_DOMAIN_SEPARATOR.encode("utf-8")
        + canonical.encode("utf-8")
    ).hexdigest()

    return AuthorizationOperationBinding(
        namespace=OPERATION_BINDING_NAMESPACE,
        binding_version=OPERATION_BINDING_VERSION,
        digest_algorithm=OPERATION_BINDING_DIGEST_ALGORITHM,
        digest_hex=digest_hex,
    )


def _result(
    candidate: EpisodicMemoryCandidate,
    intent: EpisodicPersistenceIntent,
    outcome: EpisodicPersistenceReadinessOutcome,
    reason_code: EpisodicPersistenceReadinessReason,
    evaluated_at: datetime,
    *,
    binding: AuthorizationOperationBinding | None = None,
) -> EpisodicPersistenceReadinessResult:
    return EpisodicPersistenceReadinessResult(
        candidate_id=candidate.candidate_id,
        candidate_content_identity=compute_episodic_candidate_content_identity(
            candidate
        ),
        intent=intent,
        outcome=outcome,
        reason_code=reason_code,
        evaluated_at=evaluated_at,
        authorization_operation_binding=binding,
    )


def _hold(
    candidate: EpisodicMemoryCandidate,
    intent: EpisodicPersistenceIntent,
    reason_code: EpisodicPersistenceReadinessReason,
    evaluated_at: datetime,
) -> EpisodicPersistenceReadinessResult:
    return _result(
        candidate,
        intent,
        EpisodicPersistenceReadinessOutcome.HOLD,
        reason_code,
        evaluated_at,
    )


def _denied(
    candidate: EpisodicMemoryCandidate,
    intent: EpisodicPersistenceIntent,
    reason_code: EpisodicPersistenceReadinessReason,
    evaluated_at: datetime,
) -> EpisodicPersistenceReadinessResult:
    return _result(
        candidate,
        intent,
        EpisodicPersistenceReadinessOutcome.DENIED,
        reason_code,
        evaluated_at,
    )


def evaluate_episodic_persistence_readiness(
    candidate: EpisodicMemoryCandidate,
    consumption: GovernedAdmissionConsumptionResult,
    intent: EpisodicPersistenceIntent,
    evaluated_at: datetime,
) -> EpisodicPersistenceReadinessResult:
    if not isinstance(candidate, EpisodicMemoryCandidate):
        raise TypeError("candidate must be an EpisodicMemoryCandidate")
    if not isinstance(consumption, GovernedAdmissionConsumptionResult):
        raise TypeError(
            "consumption must be a GovernedAdmissionConsumptionResult"
        )
    if not isinstance(intent, EpisodicPersistenceIntent):
        raise TypeError("intent must be an EpisodicPersistenceIntent")
    evaluated_at = _require_utc_datetime(evaluated_at, "evaluated_at")

    actual_identity = compute_episodic_candidate_content_identity(candidate)

    if consumption.candidate_id != candidate.candidate_id:
        return _denied(
            candidate,
            intent,
            EpisodicPersistenceReadinessReason.CONSUMPTION_CANDIDATE_MISMATCH,
            evaluated_at,
        )
    if consumption.actual_candidate_content_identity != actual_identity:
        return _denied(
            candidate,
            intent,
            EpisodicPersistenceReadinessReason.CANDIDATE_CONTENT_IDENTITY_MISMATCH,
            evaluated_at,
        )
    if intent.candidate_id != candidate.candidate_id:
        return _denied(
            candidate,
            intent,
            EpisodicPersistenceReadinessReason.INTENT_CANDIDATE_MISMATCH,
            evaluated_at,
        )
    if intent.candidate_content_identity != actual_identity:
        return _denied(
            candidate,
            intent,
            EpisodicPersistenceReadinessReason.INTENT_CONTENT_IDENTITY_MISMATCH,
            evaluated_at,
        )
    if (
        intent.subject_scope != candidate.control.subject_scope
        or intent.domain != candidate.control.domain
        or intent.purpose != candidate.control.purpose
    ):
        return _denied(
            candidate,
            intent,
            EpisodicPersistenceReadinessReason.INTENT_CONTEXT_MISMATCH,
            evaluated_at,
        )
    if intent.created_at > evaluated_at:
        return _denied(
            candidate,
            intent,
            EpisodicPersistenceReadinessReason.INTENT_FROM_FUTURE,
            evaluated_at,
        )
    if consumption.policy_version != CONSUMPTION_POLICY_VERSION:
        return _hold(
            candidate,
            intent,
            EpisodicPersistenceReadinessReason.UNSUPPORTED_CONSUMPTION_POLICY,
            evaluated_at,
        )
    if consumption.evaluated_at != evaluated_at:
        return _hold(
            candidate,
            intent,
            EpisodicPersistenceReadinessReason.STALE_CONSUMPTION,
            evaluated_at,
        )

    if consumption.outcome is GovernedAdmissionConsumptionOutcome.BLOCKED:
        if (
            consumption.reason_code
            is GovernedAdmissionConsumptionReason.PROJECTION_HOLD
        ):
            return _hold(
                candidate,
                intent,
                EpisodicPersistenceReadinessReason.CONSUMPTION_HOLD,
                evaluated_at,
            )
        return _denied(
            candidate,
            intent,
            EpisodicPersistenceReadinessReason.CONSUMPTION_BLOCKED,
            evaluated_at,
        )

    admission = consumption.admission_decision
    if admission is None:
        return _denied(
            candidate,
            intent,
            EpisodicPersistenceReadinessReason.CONSUMPTION_BLOCKED,
            evaluated_at,
        )
    if admission.policy_version != ADMISSION_POLICY_VERSION:
        return _hold(
            candidate,
            intent,
            EpisodicPersistenceReadinessReason.UNSUPPORTED_ADMISSION_POLICY,
            evaluated_at,
        )
    if admission.outcome is EpisodicAdmissionOutcome.HOLD:
        return _hold(
            candidate,
            intent,
            EpisodicPersistenceReadinessReason.ADMISSION_HOLD,
            evaluated_at,
        )
    if admission.outcome is EpisodicAdmissionOutcome.REJECT:
        return _denied(
            candidate,
            intent,
            EpisodicPersistenceReadinessReason.ADMISSION_REJECTED,
            evaluated_at,
        )

    binding = compute_episodic_persistence_operation_binding(
        candidate,
        intent,
        evaluated_at,
        consumption_policy_version=consumption.policy_version,
        admission_policy_version=admission.policy_version,
    )
    return _result(
        candidate,
        intent,
        EpisodicPersistenceReadinessOutcome.READY,
        EpisodicPersistenceReadinessReason.READY,
        evaluated_at,
        binding=binding,
    )


__all__ = [
    "POLICY_VERSION",
    "OPERATION_BINDING_NAMESPACE",
    "OPERATION_BINDING_VERSION",
    "OPERATION_BINDING_DIGEST_ALGORITHM",
    "EpisodicPersistenceIntent",
    "EpisodicPersistenceReadinessOutcome",
    "EpisodicPersistenceReadinessReason",
    "EpisodicPersistenceReadinessResult",
    "compute_episodic_persistence_operation_binding",
    "evaluate_episodic_persistence_readiness",
]
