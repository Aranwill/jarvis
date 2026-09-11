from datetime import UTC, datetime, timedelta, timezone

import pytest

from malak.core.protected_finalization import (
    POLICY_VERSION,
    AssuranceApplicability,
    ProtectedFinalizationInput,
    ProtectedFinalizationOutcome,
    ProtectedFinalizationReason,
    ProtectedResponseCandidate,
    evaluate_protected_finalization,
)


EVALUATED_AT = datetime(2026, 9, 11, 21, 15, tzinfo=UTC)


def _candidate() -> ProtectedResponseCandidate:
    return ProtectedResponseCandidate(
        request_id="request-1",
        session_id="session-1",
        content="Candidate response",
        provider="provider-a",
        model="model-a",
    )


def _input(
    *,
    applicability: AssuranceApplicability = AssuranceApplicability.REQUIRED,
    evidence_required: bool = True,
    support_sufficient: bool = True,
    contradiction_unresolved: bool = False,
    policy_violation: bool = False,
) -> ProtectedFinalizationInput:
    return ProtectedFinalizationInput(
        applicability=applicability,
        evidence_required=evidence_required,
        support_sufficient=support_sufficient,
        contradiction_unresolved=contradiction_unresolved,
        policy_violation=policy_violation,
    )


def test_candidate_preserves_generated_content_exactly() -> None:
    candidate = ProtectedResponseCandidate(
        request_id="request-1",
        session_id="session-1",
        content="  formatted candidate\n",
    )

    assert candidate.content == "  formatted candidate\n"


@pytest.mark.parametrize(
    ("field_name", "field_value"),
    [
        ("request_id", " request-1"),
        ("request_id", ""),
        ("session_id", "session-1 "),
        ("session_id", "   "),
        ("provider", " provider-a"),
        ("model", "model-a "),
    ],
)
def test_candidate_rejects_non_canonical_metadata(
    field_name: str,
    field_value: str,
) -> None:
    values = {
        "request_id": "request-1",
        "session_id": "session-1",
        "content": "Candidate response",
        "provider": "provider-a",
        "model": "model-a",
    }
    values[field_name] = field_value

    with pytest.raises(ValueError):
        ProtectedResponseCandidate(**values)


def test_candidate_rejects_blank_content() -> None:
    with pytest.raises(ValueError, match="content must not be blank"):
        ProtectedResponseCandidate(
            request_id="request-1",
            session_id="session-1",
            content=" \n\t ",
        )


def test_assurance_input_requires_closed_applicability_enum() -> None:
    with pytest.raises(
        TypeError,
        match="applicability must be an AssuranceApplicability",
    ):
        ProtectedFinalizationInput(
            applicability="required",  # type: ignore[arg-type]
            evidence_required=True,
            support_sufficient=True,
            contradiction_unresolved=False,
            policy_violation=False,
        )


def test_assurance_input_requires_actual_booleans() -> None:
    with pytest.raises(TypeError, match="evidence_required must be a bool"):
        ProtectedFinalizationInput(
            applicability=AssuranceApplicability.REQUIRED,
            evidence_required=1,  # type: ignore[arg-type]
            support_sufficient=True,
            contradiction_unresolved=False,
            policy_violation=False,
        )


def test_evaluator_rejects_wrong_candidate_type() -> None:
    with pytest.raises(
        TypeError,
        match="candidate must be a ProtectedResponseCandidate",
    ):
        evaluate_protected_finalization(
            candidate=object(),  # type: ignore[arg-type]
            assurance_input=_input(),
            evaluated_at=EVALUATED_AT,
        )


def test_evaluator_rejects_wrong_assurance_input_type() -> None:
    with pytest.raises(
        TypeError,
        match="assurance_input must be a ProtectedFinalizationInput",
    ):
        evaluate_protected_finalization(
            candidate=_candidate(),
            assurance_input=object(),  # type: ignore[arg-type]
            evaluated_at=EVALUATED_AT,
        )


@pytest.mark.parametrize(
    "evaluated_at",
    [
        datetime(2026, 9, 11, 21, 15),
        datetime(
            2026,
            9,
            11,
            18,
            15,
            tzinfo=timezone(-timedelta(hours=3)),
        ),
    ],
)
def test_evaluator_requires_explicit_utc_time(
    evaluated_at: datetime,
) -> None:
    with pytest.raises(ValueError):
        evaluate_protected_finalization(
            candidate=_candidate(),
            assurance_input=_input(),
            evaluated_at=evaluated_at,
        )


def test_policy_violation_blocks_with_highest_policy_precedence() -> None:
    decision = evaluate_protected_finalization(
        candidate=_candidate(),
        assurance_input=_input(
            applicability=AssuranceApplicability.UNRESOLVED,
            support_sufficient=False,
            contradiction_unresolved=True,
            policy_violation=True,
        ),
        evaluated_at=EVALUATED_AT,
    )

    assert decision.outcome is ProtectedFinalizationOutcome.BLOCK
    assert decision.reason_code is ProtectedFinalizationReason.POLICY_VIOLATION


def test_unresolved_applicability_cannot_be_accepted() -> None:
    decision = evaluate_protected_finalization(
        candidate=_candidate(),
        assurance_input=_input(
            applicability=AssuranceApplicability.UNRESOLVED,
        ),
        evaluated_at=EVALUATED_AT,
    )

    assert decision.outcome is ProtectedFinalizationOutcome.ABSTAIN
    assert (
        decision.reason_code
        is ProtectedFinalizationReason.APPLICABILITY_UNRESOLVED
    )


def test_not_applicable_with_required_evidence_fails_safe() -> None:
    decision = evaluate_protected_finalization(
        candidate=_candidate(),
        assurance_input=_input(
            applicability=AssuranceApplicability.NOT_APPLICABLE,
            evidence_required=True,
        ),
        evaluated_at=EVALUATED_AT,
    )

    assert decision.outcome is ProtectedFinalizationOutcome.ABSTAIN
    assert (
        decision.reason_code
        is ProtectedFinalizationReason.INCONSISTENT_ASSURANCE_INPUT
    )


def test_valid_not_applicable_case_is_accepted() -> None:
    decision = evaluate_protected_finalization(
        candidate=_candidate(),
        assurance_input=_input(
            applicability=AssuranceApplicability.NOT_APPLICABLE,
            evidence_required=False,
            support_sufficient=False,
        ),
        evaluated_at=EVALUATED_AT,
    )

    assert decision.outcome is ProtectedFinalizationOutcome.ACCEPT
    assert (
        decision.reason_code
        is ProtectedFinalizationReason.ASSURANCE_NOT_APPLICABLE
    )


def test_required_assurance_with_unresolved_contradiction_abstains() -> None:
    decision = evaluate_protected_finalization(
        candidate=_candidate(),
        assurance_input=_input(contradiction_unresolved=True),
        evaluated_at=EVALUATED_AT,
    )

    assert decision.outcome is ProtectedFinalizationOutcome.ABSTAIN
    assert (
        decision.reason_code
        is ProtectedFinalizationReason.CONTRADICTION_UNRESOLVED
    )


def test_required_evidence_with_insufficient_support_abstains() -> None:
    decision = evaluate_protected_finalization(
        candidate=_candidate(),
        assurance_input=_input(support_sufficient=False),
        evaluated_at=EVALUATED_AT,
    )

    assert decision.outcome is ProtectedFinalizationOutcome.ABSTAIN
    assert decision.reason_code is ProtectedFinalizationReason.INSUFFICIENT_SUPPORT


def test_required_evidence_with_sufficient_support_is_accepted() -> None:
    decision = evaluate_protected_finalization(
        candidate=_candidate(),
        assurance_input=_input(),
        evaluated_at=EVALUATED_AT,
    )

    assert decision.outcome is ProtectedFinalizationOutcome.ACCEPT
    assert decision.reason_code is ProtectedFinalizationReason.ASSURANCE_SATISFIED


def test_required_assurance_without_evidence_requirement_can_be_accepted() -> None:
    decision = evaluate_protected_finalization(
        candidate=_candidate(),
        assurance_input=_input(
            evidence_required=False,
            support_sufficient=False,
        ),
        evaluated_at=EVALUATED_AT,
    )

    assert decision.outcome is ProtectedFinalizationOutcome.ACCEPT
    assert decision.reason_code is ProtectedFinalizationReason.ASSURANCE_SATISFIED


def test_same_inputs_produce_same_decision_semantics() -> None:
    candidate = _candidate()
    assurance_input = _input()

    first = evaluate_protected_finalization(
        candidate=candidate,
        assurance_input=assurance_input,
        evaluated_at=EVALUATED_AT,
    )
    second = evaluate_protected_finalization(
        candidate=candidate,
        assurance_input=assurance_input,
        evaluated_at=EVALUATED_AT,
    )

    assert first == second
    assert first.request_id == candidate.request_id
    assert first.policy_version == POLICY_VERSION
