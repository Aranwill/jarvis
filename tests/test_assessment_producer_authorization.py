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
from malak.security.contracts import (
    AuthorizationDecision,
    AuthorizationRequest,
    PermissionScope,
    SecurityContext,
)


NOW = datetime(2026, 9, 9, 22, 20, tzinfo=timezone.utc)


def _assessment(
    *,
    assessment_id: str = "assessment-1",
    candidate_id: str = "candidate-1",
    kind: AssessmentKind = AssessmentKind.SOURCE_SECURITY_STATUS,
    value: str | bool = "suspect",
    producer_reference: str = "opaque-producer-reference",
) -> AdmissionAssessment:
    role_by_kind = {
        AssessmentKind.SOURCE_AUTHORITY: AssessmentProducerRole.SOURCE_GOVERNANCE,
        AssessmentKind.CONFIDENCE: AssessmentProducerRole.EVIDENCE_EVALUATION,
        AssessmentKind.SENSITIVITY: AssessmentProducerRole.DATA_CLASSIFICATION,
        AssessmentKind.SOURCE_SECURITY_STATUS: AssessmentProducerRole.SECURITY_TRUST_STATE,
        AssessmentKind.SCOPE_APPLICABLE: AssessmentProducerRole.ADMISSION_POLICY,
        AssessmentKind.POLICY_VIOLATION: AssessmentProducerRole.ADMISSION_POLICY,
        AssessmentKind.SENSITIVE_REVIEW_REQUIRED: AssessmentProducerRole.DATA_CLASSIFICATION,
        AssessmentKind.CONTRADICTION_REQUIRES_REVIEW: AssessmentProducerRole.CONFLICT_EVALUATION,
    }
    return AdmissionAssessment(
        assessment_id=assessment_id,
        candidate_id=candidate_id,
        kind=kind,
        value=value,
        producer_role=role_by_kind[kind],
        producer_reference=producer_reference,
        policy_or_rule_reference="assessment-rule/v1",
        assessed_at=NOW - timedelta(minutes=5),
    )


def _provenance(
    assessment: AdmissionAssessment,
    *,
    outcome: AssessmentProvenanceOutcome = AssessmentProvenanceOutcome.VALID,
    assessment_id: str | None = None,
    candidate_id: str | None = None,
    kind: AssessmentKind | None = None,
) -> AssessmentProvenanceDecision:
    reason = AssessmentProvenanceReason.VALID
    if outcome is AssessmentProvenanceOutcome.HOLD:
        reason = AssessmentProvenanceReason.MISSING_PRODUCER_REFERENCE
    elif outcome is AssessmentProvenanceOutcome.INVALID:
        reason = AssessmentProvenanceReason.CANDIDATE_MISMATCH

    return AssessmentProvenanceDecision(
        assessment_id=assessment_id or assessment.assessment_id,
        candidate_id=candidate_id or assessment.candidate_id,
        kind=kind or assessment.kind,
        outcome=outcome,
        reason_code=reason,
        evaluated_at=NOW - timedelta(minutes=1),
    )


def _context(
    *,
    subject_id: str = "security-producer",
    issued_at: datetime | None = None,
    expires_at: datetime | None = None,
) -> SecurityContext:
    return SecurityContext(
        context_id="context-1",
        session_id="session-1",
        subject_id=subject_id,
        authenticated=True,
        issued_at=issued_at or NOW - timedelta(hours=1),
        expires_at=expires_at or NOW + timedelta(hours=1),
    )


def _evidence(
    assessment: AdmissionAssessment,
    *,
    influence_class: AssessmentInfluenceClass = AssessmentInfluenceClass.TRUST_REDUCING,
    producer_subject_id: str = "security-producer",
    permission: PermissionScope | None = None,
    request_id: str = "request-1",
    decision_request_id: str | None = None,
    allowed: bool = True,
    context: SecurityContext | None = None,
    assessment_id: str | None = None,
    candidate_id: str | None = None,
    kind: AssessmentKind | None = None,
) -> AssessmentProducerAuthorizationEvidence:
    request = AuthorizationRequest(
        context=context or _context(subject_id=producer_subject_id),
        permission=permission
        or PermissionScope(
            resource="memory.episodic_assessment.source_security_status",
            action="produce.trust_reducing",
        ),
        request_id=request_id,
        created_at=NOW - timedelta(minutes=2),
    )
    decision = AuthorizationDecision(
        request_id=decision_request_id or request.request_id,
        allowed=allowed,
        reason="policy_allowed" if allowed else "policy_denied",
    )
    return AssessmentProducerAuthorizationEvidence(
        assessment_id=assessment_id or assessment.assessment_id,
        candidate_id=candidate_id or assessment.candidate_id,
        kind=kind or assessment.kind,
        influence_class=influence_class,
        producer_subject_id=producer_subject_id,
        request=request,
        decision=decision,
    )


def _validate(
    assessment: AdmissionAssessment,
    *,
    provenance: AssessmentProvenanceDecision | None = None,
    evidence: AssessmentProducerAuthorizationEvidence | None = None,
    evaluated_at: datetime = NOW,
) -> AssessmentProducerAuthorizationDecision:
    return validate_assessment_producer_authorization(
        assessment,
        provenance if provenance is not None else _provenance(assessment),
        evidence,
        evaluated_at,
    )


def test_missing_provenance_holds() -> None:
    assessment = _assessment()
    decision = validate_assessment_producer_authorization(
        assessment,
        None,
        None,
        NOW,
    )
    assert decision.outcome is AssessmentProducerAuthorizationOutcome.HOLD
    assert decision.reason_code is AssessmentProducerAuthorizationReason.MISSING_PROVENANCE_DECISION


def test_provenance_hold_keeps_authorization_on_hold() -> None:
    assessment = _assessment()
    decision = validate_assessment_producer_authorization(
        assessment,
        _provenance(assessment, outcome=AssessmentProvenanceOutcome.HOLD),
        None,
        NOW,
    )
    assert decision.outcome is AssessmentProducerAuthorizationOutcome.HOLD
    assert decision.reason_code is AssessmentProducerAuthorizationReason.PROVENANCE_HOLD


def test_invalid_provenance_is_denied() -> None:
    assessment = _assessment()
    decision = validate_assessment_producer_authorization(
        assessment,
        _provenance(assessment, outcome=AssessmentProvenanceOutcome.INVALID),
        None,
        NOW,
    )
    assert decision.outcome is AssessmentProducerAuthorizationOutcome.DENIED
    assert decision.reason_code is AssessmentProducerAuthorizationReason.PROVENANCE_INVALID


@pytest.mark.parametrize(
    ("provenance", "reason"),
    [
        (lambda a: _provenance(a, assessment_id="other-assessment"), AssessmentProducerAuthorizationReason.ASSESSMENT_ID_MISMATCH),
        (lambda a: _provenance(a, candidate_id="other-candidate"), AssessmentProducerAuthorizationReason.CANDIDATE_ID_MISMATCH),
        (lambda a: _provenance(a, kind=AssessmentKind.CONFIDENCE), AssessmentProducerAuthorizationReason.KIND_MISMATCH),
    ],
)
def test_provenance_must_bind_to_exact_assessment(
    provenance,
    reason: AssessmentProducerAuthorizationReason,
) -> None:
    assessment = _assessment()
    decision = validate_assessment_producer_authorization(
        assessment,
        provenance(assessment),
        None,
        NOW,
    )
    assert decision.outcome is AssessmentProducerAuthorizationOutcome.DENIED
    assert decision.reason_code is reason


def test_unknown_closed_value_holds_without_inference() -> None:
    assessment = _assessment(value="mystery")
    assert required_permission_for_assessment(assessment) is None
    decision = _validate(assessment)
    assert decision.outcome is AssessmentProducerAuthorizationOutcome.HOLD
    assert decision.reason_code is AssessmentProducerAuthorizationReason.UNSUPPORTED_ASSESSMENT_VALUE


@pytest.mark.parametrize(
    "kind",
    [AssessmentKind.SOURCE_AUTHORITY, AssessmentKind.CONFIDENCE, AssessmentKind.SENSITIVITY],
)
def test_open_string_dimensions_are_unclassified_deterministically(kind: AssessmentKind) -> None:
    assessment = _assessment(kind=kind, value="high")
    permission = required_permission_for_assessment(assessment)
    assert permission == PermissionScope(
        resource=f"memory.episodic_assessment.{kind.value}",
        action="produce.unclassified",
    )


def test_missing_authorization_evidence_holds() -> None:
    assessment = _assessment()
    decision = _validate(assessment)
    assert decision.outcome is AssessmentProducerAuthorizationOutcome.HOLD
    assert decision.reason_code is AssessmentProducerAuthorizationReason.MISSING_AUTHORIZATION_EVIDENCE


@pytest.mark.parametrize(
    ("evidence", "reason"),
    [
        (lambda a: _evidence(a, assessment_id="other-assessment"), AssessmentProducerAuthorizationReason.ASSESSMENT_ID_MISMATCH),
        (lambda a: _evidence(a, candidate_id="other-candidate"), AssessmentProducerAuthorizationReason.CANDIDATE_ID_MISMATCH),
        (lambda a: _evidence(a, kind=AssessmentKind.CONFIDENCE), AssessmentProducerAuthorizationReason.KIND_MISMATCH),
    ],
)
def test_authorization_evidence_must_bind_to_exact_assessment(
    evidence,
    reason: AssessmentProducerAuthorizationReason,
) -> None:
    assessment = _assessment()
    decision = _validate(assessment, evidence=evidence(assessment))
    assert decision.outcome is AssessmentProducerAuthorizationOutcome.DENIED
    assert decision.reason_code is reason


def test_caller_supplied_influence_cannot_override_derived_influence() -> None:
    assessment = _assessment(value="suspect")
    evidence = _evidence(
        assessment,
        influence_class=AssessmentInfluenceClass.TRUST_INCREASING,
    )
    decision = _validate(assessment, evidence=evidence)
    assert decision.outcome is AssessmentProducerAuthorizationOutcome.DENIED
    assert decision.reason_code is AssessmentProducerAuthorizationReason.INFLUENCE_CLASS_MISMATCH


def test_producer_subject_must_match_request_context_subject() -> None:
    assessment = _assessment()
    evidence = _evidence(
        assessment,
        producer_subject_id="claimed-producer",
        context=_context(subject_id="actual-producer"),
    )
    decision = _validate(assessment, evidence=evidence)
    assert decision.outcome is AssessmentProducerAuthorizationOutcome.DENIED
    assert decision.reason_code is AssessmentProducerAuthorizationReason.PRODUCER_SUBJECT_MISMATCH


@pytest.mark.parametrize(
    "permission",
    [
        PermissionScope(resource="memory.other", action="produce.trust_reducing"),
        PermissionScope(resource="memory.episodic_assessment.source_security_status", action="produce.trust_increasing"),
    ],
)
def test_permission_scope_must_match_exact_resource_and_action(permission: PermissionScope) -> None:
    assessment = _assessment()
    evidence = _evidence(assessment, permission=permission)
    decision = _validate(assessment, evidence=evidence)
    assert decision.outcome is AssessmentProducerAuthorizationOutcome.DENIED
    assert decision.reason_code is AssessmentProducerAuthorizationReason.PERMISSION_SCOPE_MISMATCH


def test_authorization_decision_must_bind_to_request_id() -> None:
    assessment = _assessment()
    evidence = _evidence(assessment, decision_request_id="other-request")
    decision = _validate(assessment, evidence=evidence)
    assert decision.outcome is AssessmentProducerAuthorizationOutcome.DENIED
    assert decision.reason_code is AssessmentProducerAuthorizationReason.DECISION_REQUEST_MISMATCH


def test_context_not_yet_valid_is_denied() -> None:
    assessment = _assessment()
    context = _context(issued_at=NOW + timedelta(seconds=1), expires_at=NOW + timedelta(hours=1))
    evidence = _evidence(assessment, context=context)
    decision = _validate(assessment, evidence=evidence)
    assert decision.outcome is AssessmentProducerAuthorizationOutcome.DENIED
    assert decision.reason_code is AssessmentProducerAuthorizationReason.CONTEXT_NOT_YET_VALID


def test_context_expired_exactly_at_evaluation_is_denied() -> None:
    assessment = _assessment()
    context = _context(issued_at=NOW - timedelta(hours=1), expires_at=NOW)
    evidence = _evidence(assessment, context=context)
    decision = _validate(assessment, evidence=evidence)
    assert decision.outcome is AssessmentProducerAuthorizationOutcome.DENIED
    assert decision.reason_code is AssessmentProducerAuthorizationReason.CONTEXT_EXPIRED


def test_explicit_security_denial_remains_denied_regardless_of_reason_text() -> None:
    assessment = _assessment()
    evidence = _evidence(assessment, allowed=False)
    evidence = replace(
        evidence,
        decision=AuthorizationDecision(
            request_id=evidence.request.request_id,
            allowed=False,
            reason="looks_positive_but_allowed_is_false",
        ),
    )
    decision = _validate(assessment, evidence=evidence)
    assert decision.outcome is AssessmentProducerAuthorizationOutcome.DENIED
    assert decision.reason_code is AssessmentProducerAuthorizationReason.AUTHORIZATION_DENIED


def test_exact_allowed_scope_and_bindings_authorize_only_this_boundary() -> None:
    assessment = _assessment()
    evidence = _evidence(assessment)
    decision = _validate(assessment, evidence=evidence)
    assert decision.outcome is AssessmentProducerAuthorizationOutcome.AUTHORIZED
    assert decision.reason_code is AssessmentProducerAuthorizationReason.AUTHORIZED
    assert decision.influence_class is AssessmentInfluenceClass.TRUST_REDUCING
    assert decision.producer_subject_id == "security-producer"
    assert decision.authorization_request_id == "request-1"


def test_trust_reducing_permission_cannot_authorize_trust_increasing_value() -> None:
    assessment = _assessment(value="acceptable")
    evidence = _evidence(
        assessment,
        influence_class=AssessmentInfluenceClass.TRUST_INCREASING,
        permission=PermissionScope(
            resource="memory.episodic_assessment.source_security_status",
            action="produce.trust_reducing",
        ),
    )
    decision = _validate(assessment, evidence=evidence)
    assert decision.outcome is AssessmentProducerAuthorizationOutcome.DENIED
    assert decision.reason_code is AssessmentProducerAuthorizationReason.PERMISSION_SCOPE_MISMATCH


def test_hard_reject_permission_cannot_authorize_clearing_value() -> None:
    assessment = _assessment(kind=AssessmentKind.POLICY_VIOLATION, value=False)
    evidence = _evidence(
        assessment,
        influence_class=AssessmentInfluenceClass.TRUST_INCREASING,
        permission=PermissionScope(
            resource="memory.episodic_assessment.policy_violation",
            action="produce.hard_reject",
        ),
    )
    decision = _validate(assessment, evidence=evidence)
    assert decision.outcome is AssessmentProducerAuthorizationOutcome.DENIED
    assert decision.reason_code is AssessmentProducerAuthorizationReason.PERMISSION_SCOPE_MISMATCH


def test_unauthorized_revoked_assessment_does_not_become_admission_reject() -> None:
    assessment = _assessment(value="revoked")
    decision = _validate(assessment, evidence=None)
    assert decision.outcome is AssessmentProducerAuthorizationOutcome.HOLD
    assert decision.reason_code is AssessmentProducerAuthorizationReason.MISSING_AUTHORIZATION_EVIDENCE
    assert not hasattr(decision, "admission_outcome")


def test_producer_reference_is_opaque_and_not_subject_identity() -> None:
    assessment = _assessment(producer_reference="reference-that-is-not-the-subject")
    evidence = _evidence(assessment, producer_subject_id="security-producer")
    decision = _validate(assessment, evidence=evidence)
    assert decision.outcome is AssessmentProducerAuthorizationOutcome.AUTHORIZED
    assert assessment.producer_reference != decision.producer_subject_id


def test_same_inputs_produce_same_decision() -> None:
    assessment = _assessment()
    provenance = _provenance(assessment)
    evidence = _evidence(assessment)
    first = validate_assessment_producer_authorization(assessment, provenance, evidence, NOW)
    second = validate_assessment_producer_authorization(assessment, provenance, evidence, NOW)
    assert first == second


def test_inputs_and_outputs_are_immutable() -> None:
    assessment = _assessment()
    provenance = _provenance(assessment)
    evidence = _evidence(assessment)
    decision = validate_assessment_producer_authorization(assessment, provenance, evidence, NOW)

    with pytest.raises(FrozenInstanceError):
        evidence.assessment_id = "changed"  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        decision.outcome = AssessmentProducerAuthorizationOutcome.DENIED  # type: ignore[misc]

    assert assessment.assessment_id == "assessment-1"
    assert provenance.assessment_id == "assessment-1"
    assert evidence.assessment_id == "assessment-1"


def test_validator_has_no_filesystem_or_network_side_effects(monkeypatch: pytest.MonkeyPatch) -> None:
    assessment = _assessment()
    evidence = _evidence(assessment)

    def forbidden(*args, **kwargs):
        raise AssertionError("side effect attempted")

    monkeypatch.setattr(builtins, "open", forbidden)
    monkeypatch.setattr(socket, "create_connection", forbidden)

    decision = _validate(assessment, evidence=evidence)
    assert decision.outcome is AssessmentProducerAuthorizationOutcome.AUTHORIZED


def test_validator_does_not_call_pdp_or_pep(monkeypatch: pytest.MonkeyPatch) -> None:
    from malak.security.pdp import StaticPolicyDecisionPoint

    def forbidden(*args, **kwargs):
        raise AssertionError("Security execution must stay outside Memory validator")

    monkeypatch.setattr(StaticPolicyDecisionPoint, "decide", forbidden)

    assessment = _assessment()
    evidence = _evidence(assessment)
    decision = _validate(assessment, evidence=evidence)
    assert decision.outcome is AssessmentProducerAuthorizationOutcome.AUTHORIZED


def test_validator_has_no_llm_or_runtime_dependency() -> None:
    names = set(validate_assessment_producer_authorization.__code__.co_names)
    forbidden = {"llm", "runtime", "provider", "generate", "chat", "completion"}
    assert names.isdisjoint(forbidden)


def test_authorized_decision_cannot_self_promote_to_admission_or_storage() -> None:
    assessment = _assessment()
    decision = _validate(assessment, evidence=_evidence(assessment))
    assert decision.outcome is AssessmentProducerAuthorizationOutcome.AUTHORIZED
    assert not hasattr(decision, "eligible")
    assert not hasattr(decision, "stored")
    assert not hasattr(decision, "persistence_authorized")
    assert not hasattr(decision, "knowledge")


@pytest.mark.parametrize(
    ("kind", "value", "expected_action"),
    [
        (AssessmentKind.SOURCE_SECURITY_STATUS, "acceptable", "produce.trust_increasing"),
        (AssessmentKind.SOURCE_SECURITY_STATUS, "unassessed", "produce.review_forcing"),
        (AssessmentKind.SOURCE_SECURITY_STATUS, "suspect", "produce.trust_reducing"),
        (AssessmentKind.SOURCE_SECURITY_STATUS, "tainted", "produce.hard_reject"),
        (AssessmentKind.SOURCE_SECURITY_STATUS, "revoked", "produce.hard_reject"),
        (AssessmentKind.SCOPE_APPLICABLE, True, "produce.trust_increasing"),
        (AssessmentKind.SCOPE_APPLICABLE, False, "produce.hard_reject"),
        (AssessmentKind.POLICY_VIOLATION, False, "produce.trust_increasing"),
        (AssessmentKind.POLICY_VIOLATION, True, "produce.hard_reject"),
        (AssessmentKind.SENSITIVE_REVIEW_REQUIRED, False, "produce.trust_increasing"),
        (AssessmentKind.SENSITIVE_REVIEW_REQUIRED, True, "produce.review_forcing"),
        (AssessmentKind.CONTRADICTION_REQUIRES_REVIEW, False, "produce.trust_increasing"),
        (AssessmentKind.CONTRADICTION_REQUIRES_REVIEW, True, "produce.review_forcing"),
    ],
)
def test_closed_influence_matrix_is_exact(
    kind: AssessmentKind,
    value: str | bool,
    expected_action: str,
) -> None:
    assessment = _assessment(kind=kind, value=value)
    permission = required_permission_for_assessment(assessment)
    assert permission == PermissionScope(
        resource=f"memory.episodic_assessment.{kind.value}",
        action=expected_action,
    )


def test_contract_rejects_non_utc_evaluation_time() -> None:
    assessment = _assessment()
    with pytest.raises(ValueError, match="evaluated_at must be UTC"):
        validate_assessment_producer_authorization(
            assessment,
            _provenance(assessment),
            _evidence(assessment),
            datetime(
                2026,
                9,
                9,
                19,
                20,
                tzinfo=timezone(timedelta(hours=-3)),
            ),
        )


def test_evidence_requires_canonical_ids() -> None:
    assessment = _assessment()
    base = _evidence(assessment)
    with pytest.raises(ValueError, match="assessment_id must not contain surrounding whitespace"):
        AssessmentProducerAuthorizationEvidence(
            assessment_id=" assessment-1 ",
            candidate_id=base.candidate_id,
            kind=base.kind,
            influence_class=base.influence_class,
            producer_subject_id=base.producer_subject_id,
            request=base.request,
            decision=base.decision,
        )
