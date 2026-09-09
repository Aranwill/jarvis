from dataclasses import FrozenInstanceError, replace
from datetime import datetime, timedelta, timezone
import builtins
import socket

import pytest

from malak.memory.assessment_provenance import (
    AdmissionAssessment,
    AssessmentKind,
    AssessmentProducerRole,
    AssessmentProvenanceDecision,
    AssessmentProvenanceOutcome,
    AssessmentProvenanceReason,
)
from malak.memory.assessment_producer_authorization import (
    AssessmentInfluenceClass,
    AssessmentProducerAuthorizationDecision,
    AssessmentProducerAuthorizationEvidence,
    AssessmentProducerAuthorizationOutcome,
    AssessmentProducerAuthorizationReason,
    required_permission_for_assessment,
    validate_assessment_producer_authorization,
)
from malak.memory.episodic_admission import (
    EpisodicAdmissionContext,
    EpisodicExperience,
    EpisodicMemoryCandidate,
    EpisodicOrigin,
    SourceSecurityStatus,
)
from malak.memory.governed_input_projection import (
    GovernedAdmissionProjectionOutcome,
    GovernedAdmissionProjectionReason,
    GovernedAssessmentProjectionInput,
    GovernedTemporalControlEvidence,
    project_governed_admission_inputs,
)
from malak.security.contracts import (
    AuthorizationDecision,
    AuthorizationRequest,
    PermissionScope,
    SecurityContext,
)


NOW = datetime(2026, 9, 9, 23, 20, tzinfo=timezone.utc)
TEMPORAL_PERMISSION = PermissionScope(
    resource="memory.episodic_admission.temporal_control",
    action="produce.validity_window",
)

KIND_VALUES: dict[AssessmentKind, str | bool] = {
    AssessmentKind.SOURCE_AUTHORITY: "governed-source-authority",
    AssessmentKind.CONFIDENCE: "governed-high-confidence",
    AssessmentKind.SENSITIVITY: "governed-internal",
    AssessmentKind.SOURCE_SECURITY_STATUS: "acceptable",
    AssessmentKind.SCOPE_APPLICABLE: True,
    AssessmentKind.POLICY_VIOLATION: False,
    AssessmentKind.SENSITIVE_REVIEW_REQUIRED: False,
    AssessmentKind.CONTRADICTION_REQUIRES_REVIEW: False,
}

ROLE_BY_KIND = {
    AssessmentKind.SOURCE_AUTHORITY: AssessmentProducerRole.SOURCE_GOVERNANCE,
    AssessmentKind.CONFIDENCE: AssessmentProducerRole.EVIDENCE_EVALUATION,
    AssessmentKind.SENSITIVITY: AssessmentProducerRole.DATA_CLASSIFICATION,
    AssessmentKind.SOURCE_SECURITY_STATUS: AssessmentProducerRole.SECURITY_TRUST_STATE,
    AssessmentKind.SCOPE_APPLICABLE: AssessmentProducerRole.ADMISSION_POLICY,
    AssessmentKind.POLICY_VIOLATION: AssessmentProducerRole.ADMISSION_POLICY,
    AssessmentKind.SENSITIVE_REVIEW_REQUIRED: AssessmentProducerRole.DATA_CLASSIFICATION,
    AssessmentKind.CONTRADICTION_REQUIRES_REVIEW: AssessmentProducerRole.CONFLICT_EVALUATION,
}


def _candidate() -> EpisodicMemoryCandidate:
    return EpisodicMemoryCandidate(
        candidate_id="candidate-1",
        origin=EpisodicOrigin(
            session_id="session-1",
            request_id="request-origin-1",
            request_created_at=NOW - timedelta(hours=1),
            provider="provider-1",
            model="model-1",
        ),
        experience=EpisodicExperience(
            user_content="user content",
            assistant_content="assistant content",
        ),
        control=EpisodicAdmissionContext(
            subject_scope="subject-scope",
            domain="domain-1",
            purpose="purpose-1",
            source_authority_classification="candidate-side-door-authority",
            confidence_classification="candidate-side-door-confidence",
            sensitivity_classification="candidate-side-door-sensitivity",
            valid_from=NOW - timedelta(days=2),
            valid_until=NOW + timedelta(days=2),
        ),
        created_at=NOW - timedelta(hours=1),
    )


def _assessment(
    kind: AssessmentKind,
    *,
    value: str | bool | None = None,
    assessment_id: str | None = None,
    candidate_id: str = "candidate-1",
) -> AdmissionAssessment:
    return AdmissionAssessment(
        assessment_id=assessment_id or f"assessment-{kind.value}",
        candidate_id=candidate_id,
        kind=kind,
        value=KIND_VALUES[kind] if value is None else value,
        producer_role=ROLE_BY_KIND[kind],
        producer_reference=f"opaque-reference-{kind.value}",
        policy_or_rule_reference=f"assessment-rule/{kind.value}/v1",
        assessed_at=NOW - timedelta(minutes=30),
    )


def _provenance(
    assessment: AdmissionAssessment,
    *,
    outcome: AssessmentProvenanceOutcome = AssessmentProvenanceOutcome.VALID,
) -> AssessmentProvenanceDecision:
    if outcome is AssessmentProvenanceOutcome.VALID:
        reason = AssessmentProvenanceReason.VALID
    elif outcome is AssessmentProvenanceOutcome.HOLD:
        reason = AssessmentProvenanceReason.MISSING_PRODUCER_REFERENCE
    else:
        reason = AssessmentProvenanceReason.CANDIDATE_MISMATCH
    return AssessmentProvenanceDecision(
        assessment_id=assessment.assessment_id,
        candidate_id=assessment.candidate_id,
        kind=assessment.kind,
        outcome=outcome,
        reason_code=reason,
        evaluated_at=NOW - timedelta(minutes=10),
    )


def _security_context(
    kind: AssessmentKind,
    *,
    subject_id: str | None = None,
    issued_at: datetime | None = None,
    expires_at: datetime | None = None,
) -> SecurityContext:
    producer = subject_id or f"producer-{kind.value}"
    return SecurityContext(
        context_id=f"context-{kind.value}",
        session_id="security-session-1",
        subject_id=producer,
        authenticated=True,
        issued_at=issued_at or NOW - timedelta(hours=1),
        expires_at=expires_at or NOW + timedelta(hours=1),
    )


def _authorization_evidence(
    assessment: AdmissionAssessment,
) -> AssessmentProducerAuthorizationEvidence:
    permission = required_permission_for_assessment(assessment)
    assert permission is not None
    influence = AssessmentInfluenceClass(permission.action.removeprefix("produce."))
    producer_subject_id = f"producer-{assessment.kind.value}"
    request = AuthorizationRequest(
        context=_security_context(
            assessment.kind,
            subject_id=producer_subject_id,
        ),
        permission=permission,
        request_id=f"authorization-request-{assessment.kind.value}",
        created_at=NOW - timedelta(minutes=20),
    )
    decision = AuthorizationDecision(
        request_id=request.request_id,
        allowed=True,
        reason="policy_allowed",
    )
    return AssessmentProducerAuthorizationEvidence(
        assessment_id=assessment.assessment_id,
        candidate_id=assessment.candidate_id,
        kind=assessment.kind,
        influence_class=influence,
        producer_subject_id=producer_subject_id,
        request=request,
        decision=decision,
    )


def _bundle(
    kind: AssessmentKind,
    *,
    value: str | bool | None = None,
    assessment_id: str | None = None,
) -> GovernedAssessmentProjectionInput:
    assessment = _assessment(
        kind,
        value=value,
        assessment_id=assessment_id,
    )
    provenance = _provenance(assessment)
    evidence = _authorization_evidence(assessment)
    authorization = validate_assessment_producer_authorization(
        assessment,
        provenance,
        evidence,
        NOW - timedelta(minutes=5),
    )
    assert authorization.outcome is AssessmentProducerAuthorizationOutcome.AUTHORIZED
    return GovernedAssessmentProjectionInput(
        assessment=assessment,
        provenance_decision=provenance,
        producer_authorization_evidence=evidence,
        producer_authorization_decision=authorization,
    )


def _all_bundles() -> tuple[GovernedAssessmentProjectionInput, ...]:
    return tuple(_bundle(kind) for kind in AssessmentKind)


def _replace_kind(
    bundles: tuple[GovernedAssessmentProjectionInput, ...],
    kind: AssessmentKind,
    replacement: GovernedAssessmentProjectionInput,
) -> tuple[GovernedAssessmentProjectionInput, ...]:
    return tuple(
        replacement if item.assessment.kind is kind else item
        for item in bundles
    )


def _without_kind(
    bundles: tuple[GovernedAssessmentProjectionInput, ...],
    kind: AssessmentKind,
) -> tuple[GovernedAssessmentProjectionInput, ...]:
    return tuple(item for item in bundles if item.assessment.kind is not kind)


def _temporal(
    *,
    candidate_id: str = "candidate-1",
    producer_subject_id: str = "temporal-producer",
    permission: PermissionScope = TEMPORAL_PERMISSION,
    request_id: str = "temporal-request-1",
    decision_request_id: str | None = None,
    allowed: bool = True,
    issued_at: datetime | None = None,
    expires_at: datetime | None = None,
    valid_from: datetime | None = None,
    valid_until: datetime | None = None,
) -> GovernedTemporalControlEvidence:
    context = SecurityContext(
        context_id="temporal-context-1",
        session_id="temporal-session-1",
        subject_id=producer_subject_id,
        authenticated=True,
        issued_at=issued_at or NOW - timedelta(hours=1),
        expires_at=expires_at or NOW + timedelta(hours=1),
    )
    request = AuthorizationRequest(
        context=context,
        permission=permission,
        request_id=request_id,
        created_at=NOW - timedelta(minutes=20),
    )
    decision = AuthorizationDecision(
        request_id=decision_request_id or request.request_id,
        allowed=allowed,
        reason="policy_allowed" if allowed else "policy_denied",
    )
    return GovernedTemporalControlEvidence(
        candidate_id=candidate_id,
        valid_from=valid_from or NOW - timedelta(minutes=10),
        valid_until=valid_until or NOW + timedelta(minutes=10),
        policy_or_rule_reference="temporal-rule/v1",
        producer_subject_id=producer_subject_id,
        request=request,
        decision=decision,
    )


def _project(
    *,
    candidate: EpisodicMemoryCandidate | None = None,
    bundles: tuple[GovernedAssessmentProjectionInput, ...] | None = None,
    temporal: GovernedTemporalControlEvidence | None = None,
    evaluated_at: datetime = NOW,
):
    return project_governed_admission_inputs(
        candidate or _candidate(),
        _all_bundles() if bundles is None else bundles,
        _temporal() if temporal is None else temporal,
        evaluated_at,
    )


def test_gp2_t01_projection_contracts_and_output_are_immutable() -> None:
    temporal = _temporal()
    bundle = _bundle(AssessmentKind.SOURCE_AUTHORITY)
    projection = _project()

    with pytest.raises(FrozenInstanceError):
        temporal.candidate_id = "changed"  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        bundle.assessment = _assessment(AssessmentKind.CONFIDENCE)  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        projection.outcome = GovernedAdmissionProjectionOutcome.HOLD  # type: ignore[misc]


def test_gp2_t02_evaluated_at_naive_fails() -> None:
    with pytest.raises(ValueError, match="timezone"):
        _project(evaluated_at=datetime(2026, 9, 9, 23, 20))


def test_gp2_t03_evaluated_at_non_utc_fails() -> None:
    non_utc = datetime(
        2026,
        9,
        9,
        20,
        20,
        tzinfo=timezone(timedelta(hours=-3)),
    )
    with pytest.raises(ValueError, match="UTC"):
        _project(evaluated_at=non_utc)


@pytest.mark.parametrize("field_name", ["valid_from", "valid_until"])
def test_gp2_t04_temporal_window_requires_utc(field_name: str) -> None:
    non_utc = datetime(
        2026,
        9,
        9,
        20,
        0,
        tzinfo=timezone(timedelta(hours=-3)),
    )
    kwargs = {
        "candidate_id": "candidate-1",
        "valid_from": NOW - timedelta(minutes=10),
        "valid_until": NOW + timedelta(minutes=10),
        "policy_or_rule_reference": "temporal-rule/v1",
        "producer_subject_id": "temporal-producer",
        "request": _temporal().request,
        "decision": _temporal().decision,
    }
    kwargs[field_name] = non_utc
    with pytest.raises(ValueError, match="UTC"):
        GovernedTemporalControlEvidence(**kwargs)


def test_gp2_t05_temporal_valid_until_must_be_after_valid_from() -> None:
    with pytest.raises(ValueError, match="after valid_from"):
        GovernedTemporalControlEvidence(
            candidate_id="candidate-1",
            valid_from=NOW,
            valid_until=NOW,
            policy_or_rule_reference="temporal-rule/v1",
            producer_subject_id="temporal-producer",
            request=_temporal().request,
            decision=_temporal().decision,
        )


def test_gp2_t06_candidate_control_cannot_replace_missing_governed_assessment() -> None:
    bundles = _without_kind(_all_bundles(), AssessmentKind.SOURCE_AUTHORITY)
    projection = _project(bundles=bundles)
    assert projection.outcome is GovernedAdmissionProjectionOutcome.HOLD
    assert projection.reason_code is GovernedAdmissionProjectionReason.MISSING_REQUIRED_ASSESSMENT


def test_gp2_t07_candidate_temporal_fields_cannot_replace_temporal_evidence() -> None:
    projection = project_governed_admission_inputs(
        _candidate(),
        _all_bundles(),
        None,
        NOW,
    )
    assert projection.outcome is GovernedAdmissionProjectionOutcome.HOLD
    assert projection.reason_code is GovernedAdmissionProjectionReason.MISSING_TEMPORAL_CONTROL


def test_gp2_t08_governed_assessments_override_candidate_side_door_values() -> None:
    projection = _project()
    assert projection.outcome is GovernedAdmissionProjectionOutcome.READY
    assert projection.effective_context is not None
    assert projection.effective_context.source_authority_classification == "governed-source-authority"
    assert projection.effective_context.confidence_classification == "governed-high-confidence"
    assert projection.effective_context.sensitivity_classification == "governed-internal"


def test_gp2_t09_candidate_is_not_mutated() -> None:
    candidate = _candidate()
    before = candidate
    _project(candidate=candidate)
    assert candidate == before
    assert candidate.control.source_authority_classification == "candidate-side-door-authority"


def test_gp2_t10_missing_source_authority_holds_with_kind() -> None:
    bundles = _without_kind(_all_bundles(), AssessmentKind.SOURCE_AUTHORITY)
    projection = _project(bundles=bundles)
    assert projection.outcome is GovernedAdmissionProjectionOutcome.HOLD
    assert projection.reason_code is GovernedAdmissionProjectionReason.MISSING_REQUIRED_ASSESSMENT
    assert projection.finding_kind is AssessmentKind.SOURCE_AUTHORITY


@pytest.mark.parametrize("missing_kind", list(AssessmentKind))
def test_gp2_t11_missing_any_required_kind_holds(missing_kind: AssessmentKind) -> None:
    projection = _project(bundles=_without_kind(_all_bundles(), missing_kind))
    assert projection.outcome is GovernedAdmissionProjectionOutcome.HOLD
    assert projection.reason_code is GovernedAdmissionProjectionReason.MISSING_REQUIRED_ASSESSMENT
    assert projection.finding_kind is missing_kind


def test_gp2_t12_duplicate_same_kind_same_value_holds() -> None:
    bundles = _all_bundles()
    duplicate = next(
        item for item in bundles
        if item.assessment.kind is AssessmentKind.SOURCE_AUTHORITY
    )
    projection = _project(bundles=bundles + (duplicate,))
    assert projection.outcome is GovernedAdmissionProjectionOutcome.HOLD
    assert projection.reason_code is GovernedAdmissionProjectionReason.DUPLICATE_REQUIRED_ASSESSMENT
    assert projection.finding_kind is AssessmentKind.SOURCE_AUTHORITY


def test_gp2_t13_duplicate_same_kind_different_values_holds() -> None:
    bundles = _all_bundles()
    duplicate = _bundle(
        AssessmentKind.SOURCE_SECURITY_STATUS,
        value="suspect",
        assessment_id="assessment-source-security-status-2",
    )
    projection = _project(bundles=bundles + (duplicate,))
    assert projection.outcome is GovernedAdmissionProjectionOutcome.HOLD
    assert projection.reason_code is GovernedAdmissionProjectionReason.DUPLICATE_REQUIRED_ASSESSMENT
    assert projection.finding_kind is AssessmentKind.SOURCE_SECURITY_STATUS


def test_gp2_t14_input_order_does_not_change_projection() -> None:
    bundles = _all_bundles()
    first = _project(bundles=bundles)
    second = _project(bundles=tuple(reversed(bundles)))
    assert first == second


def test_gp2_t15_provenance_hold_keeps_projection_on_hold() -> None:
    bundles = _all_bundles()
    target = next(item for item in bundles if item.assessment.kind is AssessmentKind.CONFIDENCE)
    target = replace(
        target,
        provenance_decision=_provenance(
            target.assessment,
            outcome=AssessmentProvenanceOutcome.HOLD,
        ),
    )
    projection = _project(bundles=_replace_kind(bundles, AssessmentKind.CONFIDENCE, target))
    assert projection.outcome is GovernedAdmissionProjectionOutcome.HOLD
    assert projection.reason_code is GovernedAdmissionProjectionReason.ASSESSMENT_PROVENANCE_HOLD


def test_gp2_t16_invalid_provenance_is_denied() -> None:
    bundles = _all_bundles()
    target = next(item for item in bundles if item.assessment.kind is AssessmentKind.CONFIDENCE)
    target = replace(
        target,
        provenance_decision=_provenance(
            target.assessment,
            outcome=AssessmentProvenanceOutcome.INVALID,
        ),
    )
    projection = _project(bundles=_replace_kind(bundles, AssessmentKind.CONFIDENCE, target))
    assert projection.outcome is GovernedAdmissionProjectionOutcome.DENIED
    assert projection.reason_code is GovernedAdmissionProjectionReason.ASSESSMENT_PROVENANCE_INVALID


def test_gp2_t17_authorization_hold_keeps_projection_on_hold() -> None:
    bundles = _all_bundles()
    target = next(item for item in bundles if item.assessment.kind is AssessmentKind.SENSITIVITY)
    decision = replace(
        target.producer_authorization_decision,
        outcome=AssessmentProducerAuthorizationOutcome.HOLD,
        reason_code=AssessmentProducerAuthorizationReason.MISSING_AUTHORIZATION_EVIDENCE,
    )
    target = replace(target, producer_authorization_decision=decision)
    projection = _project(bundles=_replace_kind(bundles, AssessmentKind.SENSITIVITY, target))
    assert projection.outcome is GovernedAdmissionProjectionOutcome.HOLD
    assert projection.reason_code is GovernedAdmissionProjectionReason.ASSESSMENT_AUTHORIZATION_HOLD


def test_gp2_t18_authorization_denied_denies_projection() -> None:
    bundles = _all_bundles()
    target = next(item for item in bundles if item.assessment.kind is AssessmentKind.SENSITIVITY)
    decision = replace(
        target.producer_authorization_decision,
        outcome=AssessmentProducerAuthorizationOutcome.DENIED,
        reason_code=AssessmentProducerAuthorizationReason.AUTHORIZATION_DENIED,
    )
    target = replace(target, producer_authorization_decision=decision)
    projection = _project(bundles=_replace_kind(bundles, AssessmentKind.SENSITIVITY, target))
    assert projection.outcome is GovernedAdmissionProjectionOutcome.DENIED
    assert projection.reason_code is GovernedAdmissionProjectionReason.ASSESSMENT_AUTHORIZATION_DENIED


def test_gp2_t19_assessment_id_binding_mismatch_is_denied() -> None:
    bundles = _all_bundles()
    target = next(item for item in bundles if item.assessment.kind is AssessmentKind.SOURCE_AUTHORITY)
    target = replace(
        target,
        provenance_decision=replace(
            target.provenance_decision,
            assessment_id="other-assessment",
        ),
    )
    projection = _project(bundles=_replace_kind(bundles, AssessmentKind.SOURCE_AUTHORITY, target))
    assert projection.outcome is GovernedAdmissionProjectionOutcome.DENIED
    assert projection.reason_code is GovernedAdmissionProjectionReason.ASSESSMENT_BINDING_MISMATCH


def test_gp2_t20_candidate_id_binding_mismatch_is_denied() -> None:
    bundles = _all_bundles()
    target = next(item for item in bundles if item.assessment.kind is AssessmentKind.CONFIDENCE)
    target = replace(
        target,
        provenance_decision=replace(
            target.provenance_decision,
            candidate_id="other-candidate",
        ),
    )
    projection = _project(bundles=_replace_kind(bundles, AssessmentKind.CONFIDENCE, target))
    assert projection.outcome is GovernedAdmissionProjectionOutcome.DENIED
    assert projection.reason_code is GovernedAdmissionProjectionReason.ASSESSMENT_BINDING_MISMATCH


def test_gp2_t21_kind_binding_mismatch_is_denied() -> None:
    bundles = _all_bundles()
    target = next(item for item in bundles if item.assessment.kind is AssessmentKind.SENSITIVITY)
    target = replace(
        target,
        provenance_decision=replace(
            target.provenance_decision,
            kind=AssessmentKind.CONFIDENCE,
        ),
    )
    projection = _project(bundles=_replace_kind(bundles, AssessmentKind.SENSITIVITY, target))
    assert projection.outcome is GovernedAdmissionProjectionOutcome.DENIED
    assert projection.reason_code is GovernedAdmissionProjectionReason.ASSESSMENT_BINDING_MISMATCH


def test_gp2_t22_incompatible_assessment_permission_is_denied() -> None:
    bundles = _all_bundles()
    target = next(item for item in bundles if item.assessment.kind is AssessmentKind.SOURCE_SECURITY_STATUS)
    wrong_request = replace(
        target.producer_authorization_evidence.request,
        permission=PermissionScope(
            resource="memory.episodic_assessment.source_security_status",
            action="produce.trust_reducing",
        ),
    )
    evidence = replace(target.producer_authorization_evidence, request=wrong_request)
    target = replace(target, producer_authorization_evidence=evidence)
    projection = _project(
        bundles=_replace_kind(bundles, AssessmentKind.SOURCE_SECURITY_STATUS, target)
    )
    assert projection.outcome is GovernedAdmissionProjectionOutcome.DENIED
    assert projection.reason_code is GovernedAdmissionProjectionReason.ASSESSMENT_AUTHORIZATION_DENIED


def test_gp2_t23_assessment_producer_subject_mismatch_is_denied() -> None:
    bundles = _all_bundles()
    target = next(item for item in bundles if item.assessment.kind is AssessmentKind.SOURCE_AUTHORITY)
    evidence = replace(
        target.producer_authorization_evidence,
        producer_subject_id="claimed-other-producer",
    )
    target = replace(target, producer_authorization_evidence=evidence)
    projection = _project(bundles=_replace_kind(bundles, AssessmentKind.SOURCE_AUTHORITY, target))
    assert projection.outcome is GovernedAdmissionProjectionOutcome.DENIED
    assert projection.reason_code is GovernedAdmissionProjectionReason.ASSESSMENT_AUTHORIZATION_DENIED


def test_gp2_t24_assessment_request_decision_mismatch_is_denied() -> None:
    bundles = _all_bundles()
    target = next(item for item in bundles if item.assessment.kind is AssessmentKind.SOURCE_AUTHORITY)
    evidence = replace(
        target.producer_authorization_evidence,
        decision=AuthorizationDecision(
            request_id="other-request",
            allowed=True,
            reason="policy_allowed",
        ),
    )
    target = replace(target, producer_authorization_evidence=evidence)
    projection = _project(bundles=_replace_kind(bundles, AssessmentKind.SOURCE_AUTHORITY, target))
    assert projection.outcome is GovernedAdmissionProjectionOutcome.DENIED
    assert projection.reason_code is GovernedAdmissionProjectionReason.ASSESSMENT_AUTHORIZATION_DENIED


def test_gp2_t25_boolean_string_is_not_coerced() -> None:
    bundles = _all_bundles()
    target = next(item for item in bundles if item.assessment.kind is AssessmentKind.POLICY_VIOLATION)
    object.__setattr__(target.assessment, "value", "false")
    projection = _project(bundles=bundles)
    assert projection.outcome is GovernedAdmissionProjectionOutcome.DENIED
    assert projection.reason_code is GovernedAdmissionProjectionReason.INVALID_EFFECTIVE_ASSESSMENT_VALUE


def test_gp2_t26_integer_one_is_not_coerced_to_true() -> None:
    bundles = _all_bundles()
    target = next(item for item in bundles if item.assessment.kind is AssessmentKind.SCOPE_APPLICABLE)
    object.__setattr__(target.assessment, "value", 1)
    projection = _project(bundles=bundles)
    assert projection.outcome is GovernedAdmissionProjectionOutcome.DENIED
    assert projection.reason_code is GovernedAdmissionProjectionReason.INVALID_EFFECTIVE_ASSESSMENT_VALUE


def test_gp2_t27_unknown_source_security_value_does_not_default_to_unassessed() -> None:
    bundles = _all_bundles()
    target = next(item for item in bundles if item.assessment.kind is AssessmentKind.SOURCE_SECURITY_STATUS)
    object.__setattr__(target.assessment, "value", "mystery")
    projection = _project(bundles=bundles)
    assert projection.outcome is GovernedAdmissionProjectionOutcome.HOLD
    assert projection.effective_signals is None


def test_gp2_t28_source_security_value_is_not_silently_trimmed() -> None:
    bundles = _all_bundles()
    target = next(item for item in bundles if item.assessment.kind is AssessmentKind.SOURCE_SECURITY_STATUS)
    object.__setattr__(target.assessment, "value", "acceptable ")
    projection = _project(bundles=bundles)
    assert projection.outcome is GovernedAdmissionProjectionOutcome.HOLD
    assert projection.effective_signals is None


def test_gp2_t29_missing_temporal_control_holds() -> None:
    projection = project_governed_admission_inputs(
        _candidate(),
        _all_bundles(),
        None,
        NOW,
    )
    assert projection.outcome is GovernedAdmissionProjectionOutcome.HOLD
    assert projection.reason_code is GovernedAdmissionProjectionReason.MISSING_TEMPORAL_CONTROL


def test_gp2_t30_temporal_candidate_mismatch_is_denied() -> None:
    projection = _project(temporal=_temporal(candidate_id="other-candidate"))
    assert projection.outcome is GovernedAdmissionProjectionOutcome.DENIED
    assert projection.reason_code is GovernedAdmissionProjectionReason.TEMPORAL_CANDIDATE_MISMATCH


def test_gp2_t31_temporal_producer_subject_mismatch_is_denied() -> None:
    temporal = _temporal()
    temporal = replace(temporal, producer_subject_id="other-producer")
    projection = _project(temporal=temporal)
    assert projection.outcome is GovernedAdmissionProjectionOutcome.DENIED
    assert projection.reason_code is GovernedAdmissionProjectionReason.TEMPORAL_PRODUCER_SUBJECT_MISMATCH


def test_gp2_t32_temporal_permission_mismatch_is_denied() -> None:
    temporal = _temporal(
        permission=PermissionScope(
            resource="memory.episodic_admission.temporal_control",
            action="produce.other",
        )
    )
    projection = _project(temporal=temporal)
    assert projection.outcome is GovernedAdmissionProjectionOutcome.DENIED
    assert projection.reason_code is GovernedAdmissionProjectionReason.TEMPORAL_PERMISSION_SCOPE_MISMATCH


def test_gp2_t33_temporal_decision_request_mismatch_is_denied() -> None:
    projection = _project(temporal=_temporal(decision_request_id="other-request"))
    assert projection.outcome is GovernedAdmissionProjectionOutcome.DENIED
    assert projection.reason_code is GovernedAdmissionProjectionReason.TEMPORAL_DECISION_REQUEST_MISMATCH


def test_gp2_t34_temporal_security_context_not_yet_valid_is_denied() -> None:
    temporal = _temporal(
        issued_at=NOW + timedelta(seconds=1),
        expires_at=NOW + timedelta(hours=2),
    )
    projection = _project(temporal=temporal)
    assert projection.outcome is GovernedAdmissionProjectionOutcome.DENIED
    assert projection.reason_code is GovernedAdmissionProjectionReason.TEMPORAL_CONTEXT_NOT_YET_VALID


def test_gp2_t35_temporal_security_context_expired_is_denied() -> None:
    temporal = _temporal(
        issued_at=NOW - timedelta(hours=1),
        expires_at=NOW,
    )
    projection = _project(temporal=temporal)
    assert projection.outcome is GovernedAdmissionProjectionOutcome.DENIED
    assert projection.reason_code is GovernedAdmissionProjectionReason.TEMPORAL_CONTEXT_EXPIRED


def test_gp2_t36_temporal_authorization_denied_is_denied() -> None:
    projection = _project(temporal=_temporal(allowed=False))
    assert projection.outcome is GovernedAdmissionProjectionOutcome.DENIED
    assert projection.reason_code is GovernedAdmissionProjectionReason.TEMPORAL_AUTHORIZATION_DENIED


def test_gp2_t37_future_governed_window_can_still_be_ready() -> None:
    temporal = _temporal(
        valid_from=NOW + timedelta(days=1),
        valid_until=NOW + timedelta(days=2),
    )
    projection = _project(temporal=temporal)
    assert projection.outcome is GovernedAdmissionProjectionOutcome.READY


def test_gp2_t38_expired_governed_window_can_still_be_ready() -> None:
    temporal = _temporal(
        valid_from=NOW - timedelta(days=2),
        valid_until=NOW - timedelta(days=1),
    )
    projection = _project(temporal=temporal)
    assert projection.outcome is GovernedAdmissionProjectionOutcome.READY


def test_gp2_t39_exactly_eight_authorized_assessments_and_temporal_evidence_are_ready() -> None:
    projection = _project()
    assert projection.outcome is GovernedAdmissionProjectionOutcome.READY
    assert projection.reason_code is GovernedAdmissionProjectionReason.READY
    assert projection.finding_kind is None


def test_gp2_t40_ready_projection_contains_exact_effective_mapping() -> None:
    temporal = _temporal()
    projection = _project(temporal=temporal)
    assert projection.effective_context == EpisodicAdmissionContext(
        subject_scope="subject-scope",
        domain="domain-1",
        purpose="purpose-1",
        source_authority_classification="governed-source-authority",
        confidence_classification="governed-high-confidence",
        sensitivity_classification="governed-internal",
        valid_from=temporal.valid_from,
        valid_until=temporal.valid_until,
    )
    assert projection.effective_signals is not None
    assert projection.effective_signals.scope_applicable is True
    assert projection.effective_signals.policy_violation is False
    assert projection.effective_signals.source_security_status is SourceSecurityStatus.ACCEPTABLE
    assert projection.effective_signals.sensitive_review_required is False
    assert projection.effective_signals.contradiction_requires_review is False


def test_gp2_t41_projection_does_not_call_episodic_admission(monkeypatch) -> None:
    import malak.memory.episodic_admission as admission_module

    def forbidden(*args, **kwargs):
        raise AssertionError("projection must not call admission")

    monkeypatch.setattr(admission_module, "evaluate_episodic_candidate", forbidden)
    projection = _project()
    assert projection.outcome is GovernedAdmissionProjectionOutcome.READY


def test_gp2_t42_same_inputs_produce_same_projection() -> None:
    candidate = _candidate()
    bundles = _all_bundles()
    temporal = _temporal()
    first = project_governed_admission_inputs(candidate, bundles, temporal, NOW)
    second = project_governed_admission_inputs(candidate, bundles, temporal, NOW)
    assert first == second


def test_gp2_t43_projection_has_no_file_or_network_side_effects(monkeypatch) -> None:
    candidate = _candidate()
    bundles = _all_bundles()
    temporal = _temporal()

    def forbidden_open(*args, **kwargs):
        raise AssertionError("file I/O is forbidden")

    class ForbiddenSocket:
        def __init__(self, *args, **kwargs):
            raise AssertionError("network I/O is forbidden")

    monkeypatch.setattr(builtins, "open", forbidden_open)
    monkeypatch.setattr(socket, "socket", ForbiddenSocket)
    projection = project_governed_admission_inputs(candidate, bundles, temporal, NOW)
    assert projection.outcome is GovernedAdmissionProjectionOutcome.READY


def test_gp2_t44_denied_finding_dominates_missing_assessment_hold() -> None:
    bundles = _without_kind(_all_bundles(), AssessmentKind.SENSITIVITY)
    target = next(item for item in bundles if item.assessment.kind is AssessmentKind.CONFIDENCE)
    target = replace(
        target,
        provenance_decision=_provenance(
            target.assessment,
            outcome=AssessmentProvenanceOutcome.INVALID,
        ),
    )
    bundles = _replace_kind(bundles, AssessmentKind.CONFIDENCE, target)
    projection = _project(bundles=bundles)
    assert projection.outcome is GovernedAdmissionProjectionOutcome.DENIED
    assert projection.reason_code is GovernedAdmissionProjectionReason.ASSESSMENT_PROVENANCE_INVALID


def test_gp2_t45_invalid_provenance_dominates_duplicate_hold() -> None:
    bundles = _all_bundles()
    target = next(item for item in bundles if item.assessment.kind is AssessmentKind.CONFIDENCE)
    target = replace(
        target,
        provenance_decision=_provenance(
            target.assessment,
            outcome=AssessmentProvenanceOutcome.INVALID,
        ),
    )
    bundles = _replace_kind(bundles, AssessmentKind.CONFIDENCE, target)
    duplicate = next(
        item for item in bundles
        if item.assessment.kind is AssessmentKind.SOURCE_AUTHORITY
    )
    projection = _project(bundles=bundles + (duplicate,))
    assert projection.outcome is GovernedAdmissionProjectionOutcome.DENIED
    assert projection.reason_code is GovernedAdmissionProjectionReason.ASSESSMENT_PROVENANCE_INVALID


def test_gp2_t46_temporal_denied_dominates_missing_assessment_hold() -> None:
    bundles = _without_kind(_all_bundles(), AssessmentKind.SENSITIVITY)
    projection = _project(
        bundles=bundles,
        temporal=_temporal(candidate_id="other-candidate"),
    )
    assert projection.outcome is GovernedAdmissionProjectionOutcome.DENIED
    assert projection.reason_code is GovernedAdmissionProjectionReason.TEMPORAL_CANDIDATE_MISMATCH


def test_gp2_t47_same_level_findings_use_canonical_kind_order() -> None:
    bundles = _all_bundles()
    source_authority = next(
        item for item in bundles
        if item.assessment.kind is AssessmentKind.SOURCE_AUTHORITY
    )
    sensitivity = next(
        item for item in bundles
        if item.assessment.kind is AssessmentKind.SENSITIVITY
    )
    source_authority = replace(
        source_authority,
        provenance_decision=_provenance(
            source_authority.assessment,
            outcome=AssessmentProvenanceOutcome.HOLD,
        ),
    )
    sensitivity = replace(
        sensitivity,
        provenance_decision=_provenance(
            sensitivity.assessment,
            outcome=AssessmentProvenanceOutcome.HOLD,
        ),
    )
    bundles = _replace_kind(bundles, AssessmentKind.SOURCE_AUTHORITY, source_authority)
    bundles = _replace_kind(bundles, AssessmentKind.SENSITIVITY, sensitivity)
    projection = _project(bundles=tuple(reversed(bundles)))
    assert projection.outcome is GovernedAdmissionProjectionOutcome.HOLD
    assert projection.reason_code is GovernedAdmissionProjectionReason.ASSESSMENT_PROVENANCE_HOLD
    assert projection.finding_kind is AssessmentKind.SOURCE_AUTHORITY
