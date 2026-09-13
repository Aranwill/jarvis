from dataclasses import FrozenInstanceError, fields, replace
from datetime import UTC, datetime, timedelta, timezone

import pytest

import malak.memory.assessment_provenance as provenance_module
from malak.memory.assessment_provenance import (
    POLICY_VERSION,
    AdmissionAssessment,
    AssessmentKind,
    AssessmentProducerRole,
    AssessmentProvenanceDecision,
    AssessmentProvenanceOutcome,
    AssessmentProvenanceReason,
    validate_assessment_provenance,
)
from malak.memory.candidate_content_identity import EpisodicCandidateContentIdentity


EVALUATED_AT = datetime(2026, 9, 9, 18, 30, tzinfo=UTC)


def _identity(
    *,
    candidate_id: str = "candidate-1",
    digest_hex: str = "a" * 64,
    digest_algorithm: str = "sha256",
    canonicalization_version: str = "episodic-memory-candidate-json/v1",
    policy_version: str = "episodic-candidate-content-identity/v1",
) -> EpisodicCandidateContentIdentity:
    return EpisodicCandidateContentIdentity(
        candidate_id=candidate_id,
        digest_algorithm=digest_algorithm,
        digest_hex=digest_hex,
        canonicalization_version=canonicalization_version,
        policy_version=policy_version,
    )


def make_assessment(**overrides: object) -> AdmissionAssessment:
    values: dict[str, object] = {
        "assessment_id": "assessment-1",
        "candidate_id": "candidate-1",
        "kind": AssessmentKind.SOURCE_AUTHORITY,
        "value": "conversation-source",
        "producer_role": AssessmentProducerRole.SOURCE_GOVERNANCE,
        "producer_reference": "source-governance/default",
        "policy_or_rule_reference": "source-authority/v1",
        "assessed_at": EVALUATED_AT - timedelta(seconds=1),
    }
    values.update(overrides)
    if "candidate_content_identity" not in overrides:
        candidate_id = values.get("candidate_id")
        identity_candidate_id = (
            candidate_id
            if isinstance(candidate_id, str) and candidate_id and candidate_id.strip() == candidate_id
            else "candidate-1"
        )
        values["candidate_content_identity"] = _identity(candidate_id=identity_candidate_id)
    return AdmissionAssessment(**values)  # type: ignore[arg-type]


def _validate(
    assessment: AdmissionAssessment,
    expected: EpisodicCandidateContentIdentity | None = None,
    evaluated_at: datetime = EVALUATED_AT,
) -> AssessmentProvenanceDecision:
    return validate_assessment_provenance(
        assessment,
        expected or assessment.candidate_content_identity,
        evaluated_at,
    )


def test_valid_structural_provenance() -> None:
    assessment = make_assessment()
    identity = assessment.candidate_content_identity
    decision = _validate(assessment)
    assert decision == AssessmentProvenanceDecision(
        assessment_id="assessment-1",
        candidate_id="candidate-1",
        candidate_content_identity=identity,
        kind=AssessmentKind.SOURCE_AUTHORITY,
        outcome=AssessmentProvenanceOutcome.VALID,
        reason_code=AssessmentProvenanceReason.VALID,
        evaluated_at=EVALUATED_AT,
        policy_version=POLICY_VERSION,
    )
    assert POLICY_VERSION == "episodic-assessment-provenance/v2"


@pytest.mark.parametrize(
    ("field_name", "reason"),
    [
        ("producer_role", AssessmentProvenanceReason.MISSING_PRODUCER_ROLE),
        ("producer_reference", AssessmentProvenanceReason.MISSING_PRODUCER_REFERENCE),
        ("policy_or_rule_reference", AssessmentProvenanceReason.MISSING_POLICY_OR_RULE_REFERENCE),
        ("assessed_at", AssessmentProvenanceReason.MISSING_ASSESSED_AT),
    ],
)
def test_missing_provenance_is_held(field_name: str, reason: AssessmentProvenanceReason) -> None:
    decision = _validate(make_assessment(**{field_name: None}))
    assert decision.outcome is AssessmentProvenanceOutcome.HOLD
    assert decision.reason_code is reason


def test_candidate_misbinding_is_invalid() -> None:
    assessment = make_assessment(candidate_id="candidate-a")
    decision = _validate(assessment, _identity(candidate_id="candidate-b"))
    assert decision.outcome is AssessmentProvenanceOutcome.INVALID
    assert decision.reason_code is AssessmentProvenanceReason.CANDIDATE_MISMATCH
    assert decision.candidate_content_identity is assessment.candidate_content_identity


def test_same_id_different_content_identity_is_invalid() -> None:
    assessment = make_assessment(candidate_content_identity=_identity(digest_hex="a" * 64))
    decision = _validate(assessment, _identity(digest_hex="b" * 64))
    assert decision.outcome is AssessmentProvenanceOutcome.INVALID
    assert decision.reason_code is AssessmentProvenanceReason.CONTENT_IDENTITY_MISMATCH
    assert decision.candidate_content_identity is assessment.candidate_content_identity


@pytest.mark.parametrize(
    "expected_identity",
    [
        _identity(digest_hex="b" * 64),
        _identity(digest_algorithm="sha256 "),
        _identity(canonicalization_version="episodic-memory-candidate-json/v2"),
        _identity(policy_version="episodic-candidate-content-identity/v2"),
    ],
)
def test_full_sidecar_equality_is_required(expected_identity: EpisodicCandidateContentIdentity) -> None:
    decision = _validate(make_assessment(), expected_identity)
    assert decision.outcome is AssessmentProvenanceOutcome.INVALID
    assert decision.reason_code is AssessmentProvenanceReason.CONTENT_IDENTITY_MISMATCH


def test_identity_mismatch_precedes_missing_metadata_hold() -> None:
    assessment = make_assessment(
        candidate_content_identity=_identity(digest_hex="a" * 64),
        producer_role=None,
        producer_reference=None,
        policy_or_rule_reference=None,
        assessed_at=None,
    )
    decision = _validate(assessment, _identity(digest_hex="b" * 64))
    assert decision.outcome is AssessmentProvenanceOutcome.INVALID
    assert decision.reason_code is AssessmentProvenanceReason.CONTENT_IDENTITY_MISMATCH


def test_future_assessment_is_held() -> None:
    decision = _validate(make_assessment(assessed_at=EVALUATED_AT + timedelta(microseconds=1)))
    assert decision.outcome is AssessmentProvenanceOutcome.HOLD
    assert decision.reason_code is AssessmentProvenanceReason.ASSESSMENT_FROM_FUTURE


def test_dimensional_producer_scope_is_enforced() -> None:
    decision = _validate(make_assessment(
        kind=AssessmentKind.SOURCE_SECURITY_STATUS,
        value="acceptable",
        producer_role=AssessmentProducerRole.DATA_CLASSIFICATION,
    ))
    assert decision.outcome is AssessmentProvenanceOutcome.INVALID
    assert decision.reason_code is AssessmentProvenanceReason.PRODUCER_ROLE_NOT_ALLOWED_FOR_KIND


@pytest.mark.parametrize(
    "producer_role",
    [AssessmentProducerRole.ADMISSION_POLICY, AssessmentProducerRole.SECURITY_TRUST_STATE],
)
def test_policy_violation_accepts_both_allowed_roles(producer_role: AssessmentProducerRole) -> None:
    decision = _validate(make_assessment(
        kind=AssessmentKind.POLICY_VIOLATION,
        value=False,
        producer_role=producer_role,
    ))
    assert decision.outcome is AssessmentProvenanceOutcome.VALID
    assert decision.reason_code is AssessmentProvenanceReason.VALID


def test_producer_reference_does_not_grant_role() -> None:
    decision = _validate(make_assessment(producer_role=None, producer_reference="security"))
    assert decision.outcome is AssessmentProvenanceOutcome.HOLD
    assert decision.reason_code is AssessmentProvenanceReason.MISSING_PRODUCER_ROLE


def test_valid_decision_does_not_claim_verified_identity() -> None:
    decision = _validate(make_assessment())
    decision_fields = {item.name for item in fields(AssessmentProvenanceDecision)}
    assert decision.outcome is AssessmentProvenanceOutcome.VALID
    assert "candidate_content_identity" in decision_fields
    assert "identity_verified" not in decision_fields
    assert "producer_authenticated" not in decision_fields


@pytest.mark.parametrize("value", ["trusted", "owner", "security", True])
def test_value_cannot_expand_producer_scope(value: str | bool) -> None:
    decision = _validate(make_assessment(
        kind=AssessmentKind.SOURCE_SECURITY_STATUS,
        value=value,
        producer_role=AssessmentProducerRole.DATA_CLASSIFICATION,
    ))
    assert decision.outcome is AssessmentProvenanceOutcome.INVALID
    assert decision.reason_code is AssessmentProvenanceReason.PRODUCER_ROLE_NOT_ALLOWED_FOR_KIND


def test_missing_provenance_precedence_is_deterministic() -> None:
    decision = _validate(make_assessment(producer_role=None, producer_reference=None))
    assert decision.reason_code is AssessmentProvenanceReason.MISSING_PRODUCER_ROLE


def test_validation_is_deterministic() -> None:
    assessment = make_assessment()
    assert _validate(assessment) == _validate(assessment)


def test_assessment_and_decision_are_immutable() -> None:
    assessment = make_assessment()
    decision = _validate(assessment)
    with pytest.raises(FrozenInstanceError):
        assessment.candidate_id = "candidate-2"  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        decision.outcome = AssessmentProvenanceOutcome.INVALID  # type: ignore[misc]


def test_validation_does_not_mutate_input_or_create_side_effects(tmp_path, monkeypatch) -> None:
    assessment = make_assessment()
    before = assessment
    monkeypatch.chdir(tmp_path)
    decision = _validate(assessment)
    assert decision.outcome is AssessmentProvenanceOutcome.VALID
    assert assessment == before
    assert list(tmp_path.iterdir()) == []


def test_candidate_has_no_g3_wiring() -> None:
    assert not hasattr(provenance_module, "EpisodicAdmissionContext")
    assert not hasattr(provenance_module, "EpisodicAdmissionSignals")
    assert not hasattr(provenance_module, "EpisodicAdmissionDecision")
    assert not hasattr(provenance_module, "evaluate_episodic_candidate")


def test_valid_does_not_mean_authority_or_persistence() -> None:
    decision_fields = {item.name for item in fields(AssessmentProvenanceDecision)}
    assert "storage" not in decision_fields
    assert "persist" not in decision_fields
    assert "permission" not in decision_fields
    assert "authority" not in decision_fields
    assert "admission_outcome" not in decision_fields


@pytest.mark.parametrize(
    ("kind", "producer_role"),
    [
        (AssessmentKind.SOURCE_AUTHORITY, AssessmentProducerRole.SOURCE_GOVERNANCE),
        (AssessmentKind.CONFIDENCE, AssessmentProducerRole.EVIDENCE_EVALUATION),
        (AssessmentKind.SENSITIVITY, AssessmentProducerRole.DATA_CLASSIFICATION),
        (AssessmentKind.SOURCE_SECURITY_STATUS, AssessmentProducerRole.SECURITY_TRUST_STATE),
        (AssessmentKind.SCOPE_APPLICABLE, AssessmentProducerRole.ADMISSION_POLICY),
        (AssessmentKind.POLICY_VIOLATION, AssessmentProducerRole.ADMISSION_POLICY),
        (AssessmentKind.POLICY_VIOLATION, AssessmentProducerRole.SECURITY_TRUST_STATE),
        (AssessmentKind.SENSITIVE_REVIEW_REQUIRED, AssessmentProducerRole.ADMISSION_POLICY),
        (AssessmentKind.SENSITIVE_REVIEW_REQUIRED, AssessmentProducerRole.DATA_CLASSIFICATION),
        (AssessmentKind.CONTRADICTION_REQUIRES_REVIEW, AssessmentProducerRole.CONFLICT_EVALUATION),
    ],
)
def test_closed_matrix_allows_declared_combinations(
    kind: AssessmentKind, producer_role: AssessmentProducerRole
) -> None:
    bool_kinds = {
        AssessmentKind.SCOPE_APPLICABLE,
        AssessmentKind.POLICY_VIOLATION,
        AssessmentKind.SENSITIVE_REVIEW_REQUIRED,
        AssessmentKind.CONTRADICTION_REQUIRES_REVIEW,
    }
    decision = _validate(make_assessment(
        kind=kind,
        value=False if kind in bool_kinds else "classified",
        producer_role=producer_role,
    ))
    assert decision.outcome is AssessmentProvenanceOutcome.VALID


@pytest.mark.parametrize("field_name", ["assessment_id", "candidate_id"])
@pytest.mark.parametrize("value", ["", "   ", " value", "value ", 1])
def test_required_ids_must_be_canonical_strings(field_name: str, value: object) -> None:
    with pytest.raises((TypeError, ValueError)):
        make_assessment(**{field_name: value})


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("kind", "source_authority"),
        ("value", 1),
        ("value", 1.0),
        ("value", None),
        ("producer_role", "source_governance"),
        ("candidate_content_identity", object()),
    ],
)
def test_contract_rejects_wrong_runtime_types(field_name: str, value: object) -> None:
    with pytest.raises(TypeError):
        make_assessment(**{field_name: value})


def test_assessment_rejects_identity_candidate_id_mismatch() -> None:
    with pytest.raises(ValueError, match="candidate_id"):
        make_assessment(
            candidate_id="candidate-1",
            candidate_content_identity=_identity(candidate_id="candidate-2"),
        )


@pytest.mark.parametrize("value", ["", "   ", " trusted", "trusted "])
def test_string_value_must_be_canonical(value: str) -> None:
    with pytest.raises(ValueError):
        make_assessment(value=value)


@pytest.mark.parametrize(
    "bad_time",
    [
        datetime(2026, 9, 9, 18, 30),
        datetime(2026, 9, 9, 15, 30, tzinfo=timezone(timedelta(hours=-3))),
    ],
)
def test_assessment_timestamp_must_be_utc_when_present(bad_time: datetime) -> None:
    with pytest.raises(ValueError):
        make_assessment(assessed_at=bad_time)


def test_expected_identity_must_have_correct_runtime_type() -> None:
    with pytest.raises(TypeError, match="expected_candidate_content_identity"):
        validate_assessment_provenance(
            make_assessment(),
            "candidate-1",  # type: ignore[arg-type]
            EVALUATED_AT,
        )


@pytest.mark.parametrize(
    "bad_time",
    [
        datetime(2026, 9, 9, 18, 30),
        datetime(2026, 9, 9, 15, 30, tzinfo=timezone(timedelta(hours=-3))),
    ],
)
def test_evaluated_at_must_be_utc(bad_time: datetime) -> None:
    with pytest.raises(ValueError):
        _validate(make_assessment(), evaluated_at=bad_time)


def test_bool_value_is_supported_without_integer_coercion() -> None:
    decision = _validate(make_assessment(
        kind=AssessmentKind.SCOPE_APPLICABLE,
        value=True,
        producer_role=AssessmentProducerRole.ADMISSION_POLICY,
    ))
    assert decision.outcome is AssessmentProvenanceOutcome.VALID


def test_dataclass_replace_cannot_desynchronize_candidate_id_and_identity() -> None:
    with pytest.raises(ValueError, match="candidate_id"):
        replace(make_assessment(), candidate_id="candidate-2")


def test_candidate_binding_mismatch_survives_valid_structural_rebind() -> None:
    original = make_assessment()
    rebound = replace(
        original,
        candidate_id="candidate-2",
        candidate_content_identity=_identity(candidate_id="candidate-2"),
    )
    decision = _validate(rebound, original.candidate_content_identity)
    assert decision.assessment_id == original.assessment_id
    assert decision.candidate_id == "candidate-2"
    assert decision.outcome is AssessmentProvenanceOutcome.INVALID
    assert decision.reason_code is AssessmentProvenanceReason.CANDIDATE_MISMATCH
