from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import StrEnum

from malak.memory.assessment_provenance import (
    AdmissionAssessment,
    AssessmentKind,
    AssessmentProvenanceDecision,
    AssessmentProvenanceOutcome,
)
from malak.memory.assessment_producer_authorization import (
    AssessmentProducerAuthorizationDecision,
    AssessmentProducerAuthorizationEvidence,
    AssessmentProducerAuthorizationOutcome,
    AssessmentProducerAuthorizationReason,
    validate_assessment_producer_authorization,
)
from malak.memory.candidate_content_identity import (
    EpisodicCandidateContentIdentity,
    compute_episodic_candidate_content_identity,
)
from malak.memory.episodic_admission import (
    EpisodicAdmissionContext,
    EpisodicAdmissionSignals,
    EpisodicMemoryCandidate,
    SourceSecurityStatus,
)
from malak.security.contracts import (
    AuthorizationDecision,
    AuthorizationRequest,
    PermissionScope,
)


POLICY_VERSION = "episodic-admission-governed-input-projection/v2"

_TEMPORAL_PERMISSION = PermissionScope(
    resource="memory.episodic_admission.temporal_control",
    action="produce.validity_window",
)

_CANONICAL_KIND_ORDER = tuple(AssessmentKind)
_KIND_INDEX = {
    kind: index
    for index, kind in enumerate(_CANONICAL_KIND_ORDER)
}
_OPEN_STRING_KINDS = frozenset(
    {
        AssessmentKind.SOURCE_AUTHORITY,
        AssessmentKind.CONFIDENCE,
        AssessmentKind.SENSITIVITY,
    }
)
_BOOL_KINDS = frozenset(
    {
        AssessmentKind.SCOPE_APPLICABLE,
        AssessmentKind.POLICY_VIOLATION,
        AssessmentKind.SENSITIVE_REVIEW_REQUIRED,
        AssessmentKind.CONTRADICTION_REQUIRES_REVIEW,
    }
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


@dataclass(frozen=True, slots=True)
class GovernedTemporalControlEvidence:
    candidate_id: str
    candidate_content_identity: EpisodicCandidateContentIdentity
    valid_from: datetime
    valid_until: datetime
    policy_or_rule_reference: str
    producer_subject_id: str
    request: AuthorizationRequest
    decision: AuthorizationDecision

    def __post_init__(self) -> None:
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
            "valid_from",
            _require_utc_datetime(self.valid_from, "valid_from"),
        )
        object.__setattr__(
            self,
            "valid_until",
            _require_utc_datetime(self.valid_until, "valid_until"),
        )
        if self.valid_until <= self.valid_from:
            raise ValueError("valid_until must be after valid_from")

        object.__setattr__(
            self,
            "policy_or_rule_reference",
            _require_canonical_text(
                self.policy_or_rule_reference,
                "policy_or_rule_reference",
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

        if not isinstance(self.request, AuthorizationRequest):
            raise TypeError("request must be an AuthorizationRequest")
        if not isinstance(self.decision, AuthorizationDecision):
            raise TypeError("decision must be an AuthorizationDecision")


@dataclass(frozen=True, slots=True)
class GovernedAssessmentProjectionInput:
    assessment: AdmissionAssessment
    provenance_decision: AssessmentProvenanceDecision
    producer_authorization_evidence: AssessmentProducerAuthorizationEvidence
    producer_authorization_decision: AssessmentProducerAuthorizationDecision

    def __post_init__(self) -> None:
        if not isinstance(self.assessment, AdmissionAssessment):
            raise TypeError("assessment must be an AdmissionAssessment")
        if not isinstance(
            self.provenance_decision,
            AssessmentProvenanceDecision,
        ):
            raise TypeError(
                "provenance_decision must be an AssessmentProvenanceDecision"
            )
        if not isinstance(
            self.producer_authorization_evidence,
            AssessmentProducerAuthorizationEvidence,
        ):
            raise TypeError(
                "producer_authorization_evidence must be an "
                "AssessmentProducerAuthorizationEvidence"
            )
        if not isinstance(
            self.producer_authorization_decision,
            AssessmentProducerAuthorizationDecision,
        ):
            raise TypeError(
                "producer_authorization_decision must be an "
                "AssessmentProducerAuthorizationDecision"
            )


class GovernedAdmissionProjectionOutcome(StrEnum):
    READY = "ready"
    HOLD = "hold"
    DENIED = "denied"


class GovernedAdmissionProjectionReason(StrEnum):
    ASSESSMENT_CONTENT_IDENTITY_MISMATCH = (
        "assessment_content_identity_mismatch"
    )
    ASSESSMENT_BINDING_MISMATCH = "assessment_binding_mismatch"
    ASSESSMENT_PROVENANCE_HOLD = "assessment_provenance_hold"
    ASSESSMENT_PROVENANCE_INVALID = "assessment_provenance_invalid"
    ASSESSMENT_AUTHORIZATION_HOLD = "assessment_authorization_hold"
    ASSESSMENT_AUTHORIZATION_DENIED = "assessment_authorization_denied"
    MISSING_REQUIRED_ASSESSMENT = "missing_required_assessment"
    DUPLICATE_REQUIRED_ASSESSMENT = "duplicate_required_assessment"
    INVALID_EFFECTIVE_ASSESSMENT_VALUE = "invalid_effective_assessment_value"
    MISSING_TEMPORAL_CONTROL = "missing_temporal_control"
    TEMPORAL_CANDIDATE_MISMATCH = "temporal_candidate_mismatch"
    TEMPORAL_CONTENT_IDENTITY_MISMATCH = "temporal_content_identity_mismatch"
    TEMPORAL_PRODUCER_SUBJECT_MISMATCH = "temporal_producer_subject_mismatch"
    TEMPORAL_PERMISSION_SCOPE_MISMATCH = "temporal_permission_scope_mismatch"
    TEMPORAL_DECISION_REQUEST_MISMATCH = "temporal_decision_request_mismatch"
    TEMPORAL_CONTEXT_NOT_YET_VALID = "temporal_context_not_yet_valid"
    TEMPORAL_CONTEXT_EXPIRED = "temporal_context_expired"
    TEMPORAL_AUTHORIZATION_DENIED = "temporal_authorization_denied"
    READY = "ready"


@dataclass(frozen=True, slots=True)
class GovernedAdmissionInputProjection:
    candidate_id: str
    candidate_content_identity: EpisodicCandidateContentIdentity
    outcome: GovernedAdmissionProjectionOutcome
    reason_code: GovernedAdmissionProjectionReason
    evaluated_at: datetime
    effective_context: EpisodicAdmissionContext | None = None
    effective_signals: EpisodicAdmissionSignals | None = None
    finding_kind: AssessmentKind | None = None
    policy_version: str = POLICY_VERSION

    def __post_init__(self) -> None:
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
        if not isinstance(self.outcome, GovernedAdmissionProjectionOutcome):
            raise TypeError("outcome must be a GovernedAdmissionProjectionOutcome")
        if not isinstance(self.reason_code, GovernedAdmissionProjectionReason):
            raise TypeError("reason_code must be a GovernedAdmissionProjectionReason")
        object.__setattr__(
            self,
            "evaluated_at",
            _require_utc_datetime(self.evaluated_at, "evaluated_at"),
        )

        if self.effective_context is not None and not isinstance(
            self.effective_context,
            EpisodicAdmissionContext,
        ):
            raise TypeError(
                "effective_context must be an EpisodicAdmissionContext or None"
            )
        if self.effective_signals is not None and not isinstance(
            self.effective_signals,
            EpisodicAdmissionSignals,
        ):
            raise TypeError(
                "effective_signals must be an EpisodicAdmissionSignals or None"
            )
        if self.finding_kind is not None and not isinstance(
            self.finding_kind,
            AssessmentKind,
        ):
            raise TypeError("finding_kind must be an AssessmentKind or None")

        object.__setattr__(
            self,
            "policy_version",
            _require_canonical_text(self.policy_version, "policy_version"),
        )

        if self.outcome is GovernedAdmissionProjectionOutcome.READY:
            if self.reason_code is not GovernedAdmissionProjectionReason.READY:
                raise ValueError("READY outcome requires READY reason_code")
            if self.effective_context is None or self.effective_signals is None:
                raise ValueError(
                    "READY outcome requires effective_context and effective_signals"
                )
            if self.finding_kind is not None:
                raise ValueError("READY outcome must not carry finding_kind")
        else:
            if self.reason_code is GovernedAdmissionProjectionReason.READY:
                raise ValueError("non-READY outcome cannot use READY reason_code")
            if self.effective_context is not None or self.effective_signals is not None:
                raise ValueError(
                    "HOLD and DENIED outcomes must not carry effective inputs"
                )


@dataclass(frozen=True, slots=True)
class _Finding:
    outcome: GovernedAdmissionProjectionOutcome
    reason_code: GovernedAdmissionProjectionReason
    rank: int
    kind: AssessmentKind | None = None


_DENIED_RANK = {
    GovernedAdmissionProjectionReason.ASSESSMENT_CONTENT_IDENTITY_MISMATCH: 1,
    GovernedAdmissionProjectionReason.ASSESSMENT_BINDING_MISMATCH: 2,
    GovernedAdmissionProjectionReason.ASSESSMENT_PROVENANCE_INVALID: 3,
    GovernedAdmissionProjectionReason.ASSESSMENT_AUTHORIZATION_DENIED: 4,
    GovernedAdmissionProjectionReason.INVALID_EFFECTIVE_ASSESSMENT_VALUE: 5,
    GovernedAdmissionProjectionReason.TEMPORAL_CANDIDATE_MISMATCH: 6,
    GovernedAdmissionProjectionReason.TEMPORAL_CONTENT_IDENTITY_MISMATCH: 7,
    GovernedAdmissionProjectionReason.TEMPORAL_PRODUCER_SUBJECT_MISMATCH: 8,
    GovernedAdmissionProjectionReason.TEMPORAL_PERMISSION_SCOPE_MISMATCH: 9,
    GovernedAdmissionProjectionReason.TEMPORAL_DECISION_REQUEST_MISMATCH: 10,
    GovernedAdmissionProjectionReason.TEMPORAL_CONTEXT_NOT_YET_VALID: 11,
    GovernedAdmissionProjectionReason.TEMPORAL_CONTEXT_EXPIRED: 11,
    GovernedAdmissionProjectionReason.TEMPORAL_AUTHORIZATION_DENIED: 12,
}

_HOLD_RANK = {
    GovernedAdmissionProjectionReason.ASSESSMENT_PROVENANCE_HOLD: 1,
    GovernedAdmissionProjectionReason.ASSESSMENT_AUTHORIZATION_HOLD: 2,
    GovernedAdmissionProjectionReason.DUPLICATE_REQUIRED_ASSESSMENT: 3,
    GovernedAdmissionProjectionReason.MISSING_REQUIRED_ASSESSMENT: 4,
    GovernedAdmissionProjectionReason.INVALID_EFFECTIVE_ASSESSMENT_VALUE: 5,
    GovernedAdmissionProjectionReason.MISSING_TEMPORAL_CONTROL: 6,
}


def _denied(
    reason_code: GovernedAdmissionProjectionReason,
    *,
    kind: AssessmentKind | None = None,
) -> _Finding:
    return _Finding(
        outcome=GovernedAdmissionProjectionOutcome.DENIED,
        reason_code=reason_code,
        rank=_DENIED_RANK[reason_code],
        kind=kind,
    )


def _hold(
    reason_code: GovernedAdmissionProjectionReason,
    *,
    kind: AssessmentKind | None = None,
) -> _Finding:
    return _Finding(
        outcome=GovernedAdmissionProjectionOutcome.HOLD,
        reason_code=reason_code,
        rank=_HOLD_RANK[reason_code],
        kind=kind,
    )


def _kind_sort_index(kind: AssessmentKind | None) -> int:
    if kind is None:
        return len(_CANONICAL_KIND_ORDER)
    return _KIND_INDEX[kind]


def _select_finding(findings: list[_Finding]) -> _Finding | None:
    denied_findings = [
        finding
        for finding in findings
        if finding.outcome is GovernedAdmissionProjectionOutcome.DENIED
    ]
    if denied_findings:
        return min(
            denied_findings,
            key=lambda finding: (
                finding.rank,
                _kind_sort_index(finding.kind),
            ),
        )

    hold_findings = [
        finding
        for finding in findings
        if finding.outcome is GovernedAdmissionProjectionOutcome.HOLD
    ]
    if hold_findings:
        return min(
            hold_findings,
            key=lambda finding: (
                finding.rank,
                _kind_sort_index(finding.kind),
            ),
        )

    return None


def _has_assessment_binding_mismatch(
    bundle: GovernedAssessmentProjectionInput,
    expected_candidate_id: str,
) -> bool:
    assessment = bundle.assessment
    provenance = bundle.provenance_decision
    evidence = bundle.producer_authorization_evidence
    authorization = bundle.producer_authorization_decision

    if not isinstance(assessment.kind, AssessmentKind):
        return True

    return not (
        assessment.assessment_id
        == provenance.assessment_id
        == evidence.assessment_id
        == authorization.assessment_id
        and assessment.candidate_id
        == provenance.candidate_id
        == evidence.candidate_id
        == authorization.candidate_id
        == expected_candidate_id
        and assessment.kind
        is provenance.kind
        is evidence.kind
        is authorization.kind
    )


def _has_assessment_content_identity_mismatch(
    bundle: GovernedAssessmentProjectionInput,
    actual_identity: EpisodicCandidateContentIdentity,
) -> bool:
    return not (
        bundle.assessment.candidate_content_identity
        == bundle.provenance_decision.candidate_content_identity
        == bundle.producer_authorization_evidence.candidate_content_identity
        == bundle.producer_authorization_decision.candidate_content_identity
        == actual_identity
    )


def _effective_assessment_value(
    assessment: AdmissionAssessment,
) -> tuple[str | bool | SourceSecurityStatus | None, _Finding | None]:
    kind = assessment.kind
    value = assessment.value

    if kind in _OPEN_STRING_KINDS:
        if not isinstance(value, str):
            return None, _denied(
                GovernedAdmissionProjectionReason.INVALID_EFFECTIVE_ASSESSMENT_VALUE,
                kind=kind,
            )
        if not value or value.strip() != value:
            return None, _denied(
                GovernedAdmissionProjectionReason.INVALID_EFFECTIVE_ASSESSMENT_VALUE,
                kind=kind,
            )
        return value, None

    if kind in _BOOL_KINDS:
        if type(value) is not bool:
            return None, _denied(
                GovernedAdmissionProjectionReason.INVALID_EFFECTIVE_ASSESSMENT_VALUE,
                kind=kind,
            )
        return value, None

    if kind is AssessmentKind.SOURCE_SECURITY_STATUS:
        if not isinstance(value, str):
            return None, _denied(
                GovernedAdmissionProjectionReason.INVALID_EFFECTIVE_ASSESSMENT_VALUE,
                kind=kind,
            )
        if not value or value.strip() != value:
            return None, _hold(
                GovernedAdmissionProjectionReason.INVALID_EFFECTIVE_ASSESSMENT_VALUE,
                kind=kind,
            )
        try:
            return SourceSecurityStatus(value), None
        except ValueError:
            return None, _hold(
                GovernedAdmissionProjectionReason.INVALID_EFFECTIVE_ASSESSMENT_VALUE,
                kind=kind,
            )

    return None, _denied(
        GovernedAdmissionProjectionReason.INVALID_EFFECTIVE_ASSESSMENT_VALUE,
        kind=kind if isinstance(kind, AssessmentKind) else None,
    )


def _bundle_findings(
    bundle: GovernedAssessmentProjectionInput,
    candidate: EpisodicMemoryCandidate,
    actual_identity: EpisodicCandidateContentIdentity,
    evaluated_at: datetime,
) -> tuple[list[_Finding], str | bool | SourceSecurityStatus | None]:
    assessment = bundle.assessment
    kind = assessment.kind if isinstance(assessment.kind, AssessmentKind) else None
    findings: list[_Finding] = []

    if _has_assessment_content_identity_mismatch(bundle, actual_identity):
        findings.append(
            _denied(
                GovernedAdmissionProjectionReason.ASSESSMENT_CONTENT_IDENTITY_MISMATCH,
                kind=kind,
            )
        )
        return findings, None

    if _has_assessment_binding_mismatch(bundle, candidate.candidate_id):
        findings.append(
            _denied(
                GovernedAdmissionProjectionReason.ASSESSMENT_BINDING_MISMATCH,
                kind=kind,
            )
        )
        return findings, None

    provenance = bundle.provenance_decision
    if provenance.outcome is AssessmentProvenanceOutcome.HOLD:
        findings.append(
            _hold(
                GovernedAdmissionProjectionReason.ASSESSMENT_PROVENANCE_HOLD,
                kind=assessment.kind,
            )
        )
    elif provenance.outcome is AssessmentProvenanceOutcome.INVALID:
        findings.append(
            _denied(
                GovernedAdmissionProjectionReason.ASSESSMENT_PROVENANCE_INVALID,
                kind=assessment.kind,
            )
        )

    effective_value, value_finding = _effective_assessment_value(assessment)
    if value_finding is not None:
        findings.append(value_finding)

    supplied_authorization = bundle.producer_authorization_decision
    if (
        supplied_authorization.outcome
        is AssessmentProducerAuthorizationOutcome.HOLD
    ):
        findings.append(
            _hold(
                GovernedAdmissionProjectionReason.ASSESSMENT_AUTHORIZATION_HOLD,
                kind=assessment.kind,
            )
        )
    elif (
        supplied_authorization.outcome
        is AssessmentProducerAuthorizationOutcome.DENIED
    ):
        findings.append(
            _denied(
                GovernedAdmissionProjectionReason.ASSESSMENT_AUTHORIZATION_DENIED,
                kind=assessment.kind,
            )
        )
    else:
        expected_authorization = validate_assessment_producer_authorization(
            assessment,
            provenance,
            bundle.producer_authorization_evidence,
            evaluated_at,
        )
        if (
            expected_authorization.outcome
            is AssessmentProducerAuthorizationOutcome.HOLD
        ):
            findings.append(
                _hold(
                    GovernedAdmissionProjectionReason.ASSESSMENT_AUTHORIZATION_HOLD,
                    kind=assessment.kind,
                )
            )
        elif (
            expected_authorization.outcome
            is AssessmentProducerAuthorizationOutcome.DENIED
        ):
            findings.append(
                _denied(
                    GovernedAdmissionProjectionReason.ASSESSMENT_AUTHORIZATION_DENIED,
                    kind=assessment.kind,
                )
            )
        elif not (
            supplied_authorization.reason_code
            is AssessmentProducerAuthorizationReason.AUTHORIZED
            and supplied_authorization.influence_class
            is expected_authorization.influence_class
            and supplied_authorization.producer_subject_id
            == expected_authorization.producer_subject_id
            and supplied_authorization.authorization_request_id
            == expected_authorization.authorization_request_id
        ):
            findings.append(
                _denied(
                    GovernedAdmissionProjectionReason.ASSESSMENT_BINDING_MISMATCH,
                    kind=assessment.kind,
                )
            )

    return findings, effective_value


def _temporal_findings(
    temporal_control: GovernedTemporalControlEvidence | None,
    candidate: EpisodicMemoryCandidate,
    actual_identity: EpisodicCandidateContentIdentity,
    evaluated_at: datetime,
) -> list[_Finding]:
    if temporal_control is None:
        return [
            _hold(
                GovernedAdmissionProjectionReason.MISSING_TEMPORAL_CONTROL,
            )
        ]

    findings: list[_Finding] = []
    if temporal_control.candidate_id != candidate.candidate_id:
        findings.append(
            _denied(
                GovernedAdmissionProjectionReason.TEMPORAL_CANDIDATE_MISMATCH,
            )
        )

    if temporal_control.candidate_content_identity != actual_identity:
        findings.append(
            _denied(
                GovernedAdmissionProjectionReason.TEMPORAL_CONTENT_IDENTITY_MISMATCH,
            )
        )

    if (
        temporal_control.producer_subject_id
        != temporal_control.request.context.subject_id
    ):
        findings.append(
            _denied(
                GovernedAdmissionProjectionReason.TEMPORAL_PRODUCER_SUBJECT_MISMATCH,
            )
        )

    if temporal_control.request.permission != _TEMPORAL_PERMISSION:
        findings.append(
            _denied(
                GovernedAdmissionProjectionReason.TEMPORAL_PERMISSION_SCOPE_MISMATCH,
            )
        )

    if temporal_control.decision.request_id != temporal_control.request.request_id:
        findings.append(
            _denied(
                GovernedAdmissionProjectionReason.TEMPORAL_DECISION_REQUEST_MISMATCH,
            )
        )

    context = temporal_control.request.context
    if evaluated_at < context.issued_at:
        findings.append(
            _denied(
                GovernedAdmissionProjectionReason.TEMPORAL_CONTEXT_NOT_YET_VALID,
            )
        )
    elif evaluated_at >= context.expires_at:
        findings.append(
            _denied(
                GovernedAdmissionProjectionReason.TEMPORAL_CONTEXT_EXPIRED,
            )
        )

    if temporal_control.decision.allowed is False:
        findings.append(
            _denied(
                GovernedAdmissionProjectionReason.TEMPORAL_AUTHORIZATION_DENIED,
            )
        )

    return findings


def _projection_from_finding(
    candidate: EpisodicMemoryCandidate,
    actual_identity: EpisodicCandidateContentIdentity,
    finding: _Finding,
    evaluated_at: datetime,
) -> GovernedAdmissionInputProjection:
    return GovernedAdmissionInputProjection(
        candidate_id=candidate.candidate_id,
        candidate_content_identity=actual_identity,
        outcome=finding.outcome,
        reason_code=finding.reason_code,
        evaluated_at=evaluated_at,
        finding_kind=finding.kind,
    )


def project_governed_admission_inputs(
    candidate: EpisodicMemoryCandidate,
    assessment_inputs: tuple[GovernedAssessmentProjectionInput, ...],
    temporal_control: GovernedTemporalControlEvidence | None,
    evaluated_at: datetime,
) -> GovernedAdmissionInputProjection:
    if not isinstance(candidate, EpisodicMemoryCandidate):
        raise TypeError("candidate must be an EpisodicMemoryCandidate")
    if type(assessment_inputs) is not tuple:
        raise TypeError("assessment_inputs must be a tuple")
    for item in assessment_inputs:
        if not isinstance(item, GovernedAssessmentProjectionInput):
            raise TypeError(
                "assessment_inputs must contain GovernedAssessmentProjectionInput"
            )
    if temporal_control is not None and not isinstance(
        temporal_control,
        GovernedTemporalControlEvidence,
    ):
        raise TypeError(
            "temporal_control must be a GovernedTemporalControlEvidence or None"
        )

    evaluated_at = _require_utc_datetime(evaluated_at, "evaluated_at")
    actual_identity = compute_episodic_candidate_content_identity(candidate)

    findings: list[_Finding] = []
    groups: dict[AssessmentKind, list[GovernedAssessmentProjectionInput]] = {
        kind: []
        for kind in _CANONICAL_KIND_ORDER
    }
    effective_values: dict[
        AssessmentKind,
        str | bool | SourceSecurityStatus,
    ] = {}

    for bundle in assessment_inputs:
        kind = bundle.assessment.kind
        if isinstance(kind, AssessmentKind):
            groups[kind].append(bundle)
        bundle_findings, effective_value = _bundle_findings(
            bundle,
            candidate,
            actual_identity,
            evaluated_at,
        )
        findings.extend(bundle_findings)
        if (
            isinstance(kind, AssessmentKind)
            and effective_value is not None
            and len(groups[kind]) == 1
        ):
            effective_values[kind] = effective_value

    for kind in _CANONICAL_KIND_ORDER:
        count = len(groups[kind])
        if count == 0:
            findings.append(
                _hold(
                    GovernedAdmissionProjectionReason.MISSING_REQUIRED_ASSESSMENT,
                    kind=kind,
                )
            )
        elif count > 1:
            findings.append(
                _hold(
                    GovernedAdmissionProjectionReason.DUPLICATE_REQUIRED_ASSESSMENT,
                    kind=kind,
                )
            )
            effective_values.pop(kind, None)

    findings.extend(
        _temporal_findings(
            temporal_control,
            candidate,
            actual_identity,
            evaluated_at,
        )
    )

    selected_finding = _select_finding(findings)
    if selected_finding is not None:
        return _projection_from_finding(
            candidate,
            actual_identity,
            selected_finding,
            evaluated_at,
        )

    if temporal_control is None:
        raise AssertionError("temporal control must exist when projection is READY")

    context = EpisodicAdmissionContext(
        subject_scope=candidate.control.subject_scope,
        domain=candidate.control.domain,
        purpose=candidate.control.purpose,
        source_authority_classification=effective_values[
            AssessmentKind.SOURCE_AUTHORITY
        ],
        confidence_classification=effective_values[
            AssessmentKind.CONFIDENCE
        ],
        sensitivity_classification=effective_values[
            AssessmentKind.SENSITIVITY
        ],
        valid_from=temporal_control.valid_from,
        valid_until=temporal_control.valid_until,
    )
    signals = EpisodicAdmissionSignals(
        scope_applicable=effective_values[AssessmentKind.SCOPE_APPLICABLE],
        policy_violation=effective_values[AssessmentKind.POLICY_VIOLATION],
        source_security_status=effective_values[
            AssessmentKind.SOURCE_SECURITY_STATUS
        ],
        sensitive_review_required=effective_values[
            AssessmentKind.SENSITIVE_REVIEW_REQUIRED
        ],
        contradiction_requires_review=effective_values[
            AssessmentKind.CONTRADICTION_REQUIRES_REVIEW
        ],
    )

    return GovernedAdmissionInputProjection(
        candidate_id=candidate.candidate_id,
        candidate_content_identity=actual_identity,
        outcome=GovernedAdmissionProjectionOutcome.READY,
        reason_code=GovernedAdmissionProjectionReason.READY,
        evaluated_at=evaluated_at,
        effective_context=context,
        effective_signals=signals,
    )


__all__ = [
    "POLICY_VERSION",
    "GovernedTemporalControlEvidence",
    "GovernedAssessmentProjectionInput",
    "GovernedAdmissionProjectionOutcome",
    "GovernedAdmissionProjectionReason",
    "GovernedAdmissionInputProjection",
    "project_governed_admission_inputs",
]
