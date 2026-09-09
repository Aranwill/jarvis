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


EVALUATED_AT = datetime(2026, 9, 9, 18, 30, tzinfo=UTC)


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
    return AdmissionAssessment(**values)  # type: ignore[arg-type]


def test_valid_structural_provenance() -> None:
    assessment = make_assessment()

    decision = validate_assessment_provenance(
        assessment,
        "candidate-1",
        EVALUATED_AT,
    )

    assert decision == AssessmentProvenanceDecision(
        assessment_id="assessment-1",
        candidate_id="candidate-1",
        kind=AssessmentKind.SOURCE_AUTHORITY,
        outcome=AssessmentProvenanceOutcome.VALID,
        reason_code=AssessmentProvenanceReason.VALID,
        evaluated_at=EVALUATED_AT,
        policy_version=POLICY_VERSION,
    )


@pytest.mark.parametrize(
    ("field_name", "reason"),
    [
        (
            "producer_role",
            AssessmentProvenanceReason.MISSING_PRODUCER_ROLE,
        ),
        (
            "producer_reference",
            AssessmentProvenanceReason.MISSING_PRODUCER_REFERENCE,
        ),
        (
            "policy_or_rule_reference",
            AssessmentProvenanceReason.MISSING_POLICY_OR_RULE_REFERENCE,
        ),
        (
            "assessed_at",
            AssessmentProvenanceReason.MISSING_ASSESSED_AT,
        ),
    ],
)
def test_missing_provenance_is_held(
    field_name: str,
    reason: AssessmentProvenanceReason,
) -> None:
    assessment = make_assessment(**{field_name: None})

    decision = validate_assessment_provenance(
        assessment,
        "candidate-1",
        EVALUATED_AT,
    )

    assert decision.outcome is AssessmentProvenanceOutcome.HOLD
    assert decision.reason_code is reason


def test_candidate_misbinding_is_invalid() -> None:
    decision = validate_assessment_provenance(
        make_assessment(candidate_id="candidate-a"),
        "candidate-b",
        EVALUATED_AT,
    )

    assert decision.outcome is AssessmentProvenanceOutcome.INVALID
    assert decision.reason_code is AssessmentProvenanceReason.CANDIDATE_MISMATCH


def test_future_assessment_is_held() -> None:
    decision = validate_assessment_provenance(
        make_assessment(assessed_at=EVALUATED_AT + timedelta(microseconds=1)),
        "candidate-1",
        EVALUATED_AT,
    )

    assert decision.outcome is AssessmentProvenanceOutcome.HOLD
    assert decision.reason_code is AssessmentProvenanceReason.ASSESSMENT_FROM_FUTURE


def test_dimensional_producer_scope_is_enforced() -> None:
    decision = validate_assessment_provenance(
        make_assessment(
            kind=AssessmentKind.SOURCE_SECURITY_STATUS,
            value="acceptable",
            producer_role=AssessmentProducerRole.DATA_CLASSIFICATION,
        ),
        "candidate-1",
        EVALUATED_AT,
    )

    assert decision.outcome is AssessmentProvenanceOutcome.INVALID
    assert (
        decision.reason_code
        is AssessmentProvenanceReason.PRODUCER_ROLE_NOT_ALLOWED_FOR_KIND
    )


@pytest.mark.parametrize(
    "producer_role",
    [
        AssessmentProducerRole.ADMISSION_POLICY,
        AssessmentProducerRole.SECURITY_TRUST_STATE,
    ],
)
def test_policy_violation_accepts_both_allowed_roles(
    producer_role: AssessmentProducerRole,
) -> None:
    decision = validate_assessment_provenance(
        make_assessment(
            kind=AssessmentKind.POLICY_VIOLATION,
            value=False,
            producer_role=producer_role,
        ),
        "candidate-1",
        EVALUATED_AT,
    )

    assert decision.outcome is AssessmentProvenanceOutcome.VALID
    assert decision.reason_code is AssessmentProvenanceReason.VALID


def test_producer_reference_does_not_grant_role() -> None:
    decision = validate_assessment_provenance(
        make_assessment(
            producer_role=None,
            producer_reference="security",
        ),
        "candidate-1",
        EVALUATED_AT,
    )

    assert decision.outcome is AssessmentProvenanceOutcome.HOLD
    assert decision.reason_code is AssessmentProvenanceReason.MISSING_PRODUCER_ROLE


def test_valid_decision_does_not_claim_verified_identity() -> None:
    decision = validate_assessment_provenance(
        make_assessment(),
        "candidate-1",
        EVALUATED_AT,
    )
    decision_fields = {item.name for item in fields(AssessmentProvenanceDecision)}

    assert decision.outcome is AssessmentProvenanceOutcome.VALID
    assert "identity_verified" not in decision_fields
    assert "producer_authenticated" not in decision_fields


@pytest.mark.parametrize("value", ["trusted", "owner", "security", True])
def test_value_cannot_expand_producer_scope(value: str | bool) -> None:
    decision = validate_assessment_provenance(
        make_assessment(
            kind=AssessmentKind.SOURCE_SECURITY_STATUS,
            value=value,
            producer_role=AssessmentProducerRole.DATA_CLASSIFICATION,
        ),
        "candidate-1",
        EVALUATED_AT,
    )

    assert decision.outcome is AssessmentProvenanceOutcome.INVALID
    assert (
        decision.reason_code
        is AssessmentProvenanceReason.PRODUCER_ROLE_NOT_ALLOWED_FOR_KIND
    )


def test_missing_provenance_precedence_is_deterministic() -> None:
    decision = validate_assessment_provenance(
        make_assessment(
            producer_role=None,
            producer_reference=None,
        ),
        "candidate-1",
        EVALUATED_AT,
    )

    assert decision.reason_code is AssessmentProvenanceReason.MISSING_PRODUCER_ROLE


def test_validation_is_deterministic() -> None:
    assessment = make_assessment()

    first = validate_assessment_provenance(
        assessment,
        "candidate-1",
        EVALUATED_AT,
    )
    second = validate_assessment_provenance(
        assessment,
        "candidate-1",
        EVALUATED_AT,
    )

    assert first == second


def test_assessment_and_decision_are_immutable() -> None:
    assessment = make_assessment()
    decision = validate_assessment_provenance(
        assessment,
        "candidate-1",
        EVALUATED_AT,
    )

    with pytest.raises(FrozenInstanceError):
        assessment.candidate_id = "candidate-2"  # type: ignore[misc]

    with pytest.raises(FrozenInstanceError):
        decision.outcome = AssessmentProvenanceOutcome.INVALID  # type: ignore[misc]


def test_validation_does_not_mutate_input_or_create_side_effects(
    tmp_path,
    monkeypatch,
) -> None:
    assessment = make_assessment()
    before = assessment
    monkeypatch.chdir(tmp_path)

    decision = validate_assessment_provenance(
        assessment,
        "candidate-1",
        EVALUATED_AT,
    )

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
        (
            AssessmentKind.SOURCE_SECURITY_STATUS,
            AssessmentProducerRole.SECURITY_TRUST_STATE,
        ),
        (AssessmentKind.SCOPE_APPLICABLE, AssessmentProducerRole.ADMISSION_POLICY),
        (AssessmentKind.POLICY_VIOLATION, AssessmentProducerRole.ADMISSION_POLICY),
        (
            AssessmentKind.POLICY_VIOLATION,
            AssessmentProducerRole.SECURITY_TRUST_STATE,
        ),
        (
            AssessmentKind.SENSITIVE_REVIEW_REQUIRED,
            AssessmentProducerRole.ADMISSION_POLICY,
        ),
        (
            AssessmentKind.SENSITIVE_REVIEW_REQUIRED,
            AssessmentProducerRole.DATA_CLASSIFICATION,
        ),
        (
            AssessmentKind.CONTRADICTION_REQUIRES_REVIEW,
            AssessmentProducerRole.CONFLICT_EVALUATION,
        ),
    ],
)
def test_closed_matrix_allows_declared_combinations(
    kind: AssessmentKind,
    producer_role: AssessmentProducerRole,
) -> None:
    value: str | bool = (
        False
        if kind
        in {
            AssessmentKind.SCOPE_APPLICABLE,
            AssessmentKind.POLICY_VIOLATION,
            AssessmentKind.SENSITIVE_REVIEW_REQUIRED,
            AssessmentKind.CONTRADICTION_REQUIRES_REVIEW,
        }
        else "classified"
    )

    decision = validate_assessment_provenance(
        make_assessment(kind=kind, value=value, producer_role=producer_role),
        "candidate-1",
        EVALUATED_AT,
    )

    assert decision.outcome is AssessmentProvenanceOutcome.VALID


@pytest.mark.parametrize("field_name", ["assessment_id", "candidate_id"])
@pytest.mark.parametrize("value", ["", "   ", " value", "value ", 1])
def test_required_ids_must_be_canonical_strings(
    field_name: str,
    value: object,
) -> None:
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
    ],
)
def test_contract_rejects_wrong_runtime_types(
    field_name: str,
    value: object,
) -> None:
    with pytest.raises(TypeError):
        make_assessment(**{field_name: value})


@pytest.mark.parametrize("value", ["", "   ", " trusted", "trusted "])
def test_string_value_must_be_canonical(value: str) -> None:
    with pytest.raises(ValueError):
        make_assessment(value=value)


@pytest.mark.parametrize(
    "bad_time",
    [
        datetime(2026, 9, 9, 18, 30),
        datetime(
            2026,
            9,
            9,
            15,
            30,
            tzinfo=timezone(timedelta(hours=-3)),
        ),
    ],
)
def test_assessment_timestamp_must_be_utc_when_present(
    bad_time: datetime,
) -> None:
    with pytest.raises(ValueError):
        make_assessment(assessed_at=bad_time)


@pytest.mark.parametrize(
    "bad_expected_candidate_id",
    ["", "   ", " candidate-1", "candidate-1 ", 1],
)
def test_expected_candidate_id_must_be_canonical(
    bad_expected_candidate_id: object,
) -> None:
    with pytest.raises((TypeError, ValueError)):
        validate_assessment_provenance(
            make_assessment(),
            bad_expected_candidate_id,  # type: ignore[arg-type]
            EVALUATED_AT,
        )


@pytest.mark.parametrize(
    "bad_time",
    [
        datetime(2026, 9, 9, 18, 30),
        datetime(
            2026,
            9,
            9,
            15,
            30,
            tzinfo=timezone(timedelta(hours=-3)),
        ),
    ],
)
def test_evaluated_at_must_be_utc(bad_time: datetime) -> None:
    with pytest.raises(ValueError):
        validate_assessment_provenance(
            make_assessment(),
            "candidate-1",
            bad_time,
        )


def test_bool_value_is_supported_without_integer_coercion() -> None:
    assessment = make_assessment(
        kind=AssessmentKind.SCOPE_APPLICABLE,
        value=True,
        producer_role=AssessmentProducerRole.ADMISSION_POLICY,
    )

    decision = validate_assessment_provenance(
        assessment,
        "candidate-1",
        EVALUATED_AT,
    )

    assert decision.outcome is AssessmentProvenanceOutcome.VALID


def test_assessment_binding_survives_dataclass_replace() -> None:
    original = make_assessment()
    rebound = replace(original, candidate_id="candidate-2")

    decision = validate_assessment_provenance(
        rebound,
        "candidate-1",
        EVALUATED_AT,
    )

    assert decision.assessment_id == original.assessment_id
    assert decision.candidate_id == "candidate-2"
    assert decision.outcome is AssessmentProvenanceOutcome.INVALID
    assert decision.reason_code is AssessmentProvenanceReason.CANDIDATE_MISMATCH
