from dataclasses import FrozenInstanceError, replace
from datetime import datetime, timedelta, timezone

import pytest

from malak.memory.candidate_content_identity import (
    compute_episodic_candidate_content_identity,
)
from malak.memory.episodic_admission import (
    POLICY_VERSION as ADMISSION_POLICY_VERSION,
    EpisodicAdmissionContext,
    EpisodicAdmissionDecision,
    EpisodicAdmissionOutcome,
    EpisodicAdmissionReason,
    EpisodicExperience,
    EpisodicMemoryCandidate,
    EpisodicOrigin,
)
from malak.memory.episodic_persistence_readiness import (
    OPERATION_BINDING_NAMESPACE,
    OPERATION_BINDING_VERSION,
    POLICY_VERSION,
    EpisodicPersistenceIntent,
    EpisodicPersistenceReadinessOutcome,
    EpisodicPersistenceReadinessReason,
    EpisodicPersistenceReadinessResult,
    compute_episodic_persistence_operation_binding,
    evaluate_episodic_persistence_readiness,
)
from malak.memory.governed_projection_consumption import (
    POLICY_VERSION as CONSUMPTION_POLICY_VERSION,
    GovernedAdmissionConsumptionOutcome,
    GovernedAdmissionConsumptionReason,
    GovernedAdmissionConsumptionResult,
)
from malak.security.contracts import AuthorizationOperationBinding


NOW = datetime(2026, 9, 15, 20, 0, tzinfo=timezone.utc)


def _context(
    *,
    subject_scope: str = "owner",
    domain: str = "personal",
    purpose: str = "continuity",
) -> EpisodicAdmissionContext:
    return EpisodicAdmissionContext(
        subject_scope=subject_scope,
        domain=domain,
        purpose=purpose,
        source_authority_classification="governed",
        confidence_classification="high",
        sensitivity_classification="private",
        valid_from=NOW - timedelta(hours=1),
        valid_until=NOW + timedelta(hours=1),
    )


def _candidate(
    *,
    candidate_id: str = "candidate-1",
    user_content: str = "remember this",
    control: EpisodicAdmissionContext | None = None,
) -> EpisodicMemoryCandidate:
    return EpisodicMemoryCandidate(
        candidate_id=candidate_id,
        origin=EpisodicOrigin(
            session_id="session-1",
            request_id="request-1",
            request_created_at=NOW - timedelta(minutes=10),
            provider="provider-1",
            model="model-1",
        ),
        experience=EpisodicExperience(
            user_content=user_content,
            assistant_content="acknowledged",
        ),
        control=control or _context(),
        created_at=NOW - timedelta(minutes=9),
    )


def _intent(
    candidate: EpisodicMemoryCandidate | None = None,
    *,
    candidate_id: str | None = None,
    subject_scope: str | None = None,
    domain: str | None = None,
    purpose: str | None = None,
    created_at: datetime = NOW - timedelta(minutes=1),
) -> EpisodicPersistenceIntent:
    actual = candidate or _candidate()
    return EpisodicPersistenceIntent(
        candidate_id=candidate_id or actual.candidate_id,
        candidate_content_identity=compute_episodic_candidate_content_identity(actual),
        subject_scope=subject_scope or actual.control.subject_scope,
        domain=domain or actual.control.domain,
        purpose=purpose or actual.control.purpose,
        created_at=created_at,
    )


def _admission_decision(
    *,
    candidate_id: str = "candidate-1",
    outcome: EpisodicAdmissionOutcome = EpisodicAdmissionOutcome.ELIGIBLE,
    reason: EpisodicAdmissionReason = EpisodicAdmissionReason.ELIGIBLE,
    evaluated_at: datetime = NOW,
    policy_version: str = ADMISSION_POLICY_VERSION,
) -> EpisodicAdmissionDecision:
    return EpisodicAdmissionDecision(
        candidate_id=candidate_id,
        outcome=outcome,
        reason_code=reason,
        evaluated_at=evaluated_at,
        policy_version=policy_version,
    )


def _consumption(
    candidate: EpisodicMemoryCandidate | None = None,
    *,
    outcome: GovernedAdmissionConsumptionOutcome = GovernedAdmissionConsumptionOutcome.EVALUATED,
    reason: GovernedAdmissionConsumptionReason = GovernedAdmissionConsumptionReason.EVALUATED,
    evaluated_at: datetime = NOW,
    admission_outcome: EpisodicAdmissionOutcome = EpisodicAdmissionOutcome.ELIGIBLE,
    admission_reason: EpisodicAdmissionReason = EpisodicAdmissionReason.ELIGIBLE,
    policy_version: str = CONSUMPTION_POLICY_VERSION,
    admission_policy_version: str = ADMISSION_POLICY_VERSION,
) -> GovernedAdmissionConsumptionResult:
    actual = candidate or _candidate()
    identity = compute_episodic_candidate_content_identity(actual)
    decision = None
    if outcome is GovernedAdmissionConsumptionOutcome.EVALUATED:
        decision = _admission_decision(
            candidate_id=actual.candidate_id,
            outcome=admission_outcome,
            reason=admission_reason,
            evaluated_at=evaluated_at,
            policy_version=admission_policy_version,
        )
    return GovernedAdmissionConsumptionResult(
        candidate_id=actual.candidate_id,
        actual_candidate_content_identity=identity,
        presented_projection_content_identity=identity,
        outcome=outcome,
        reason_code=reason,
        evaluated_at=evaluated_at,
        admission_decision=decision,
        policy_version=policy_version,
    )


def test_g2b_t01_intent_is_immutable() -> None:
    intent = _intent()
    with pytest.raises(FrozenInstanceError):
        intent.purpose = "other"  # type: ignore[misc]


def test_g2b_t02_ready_requires_exact_current_evaluated_consumption() -> None:
    candidate = _candidate()
    result = evaluate_episodic_persistence_readiness(
        candidate,
        _consumption(candidate),
        _intent(candidate),
        NOW,
    )

    assert result.outcome is EpisodicPersistenceReadinessOutcome.READY
    assert result.reason_code is EpisodicPersistenceReadinessReason.READY
    assert isinstance(result.authorization_operation_binding, AuthorizationOperationBinding)
    assert result.authorization_operation_binding.namespace == OPERATION_BINDING_NAMESPACE
    assert result.authorization_operation_binding.binding_version == OPERATION_BINDING_VERSION
    assert result.policy_version == POLICY_VERSION
    assert not hasattr(result, "authorization_decision")


def test_g2b_t03_ready_binding_is_deterministic() -> None:
    candidate = _candidate()
    consumption = _consumption(candidate)
    intent = _intent(candidate)

    first = evaluate_episodic_persistence_readiness(candidate, consumption, intent, NOW)
    second = evaluate_episodic_persistence_readiness(candidate, consumption, intent, NOW)

    assert first.authorization_operation_binding == second.authorization_operation_binding


def test_g2b_t04_same_id_different_content_is_denied() -> None:
    original = _candidate()
    changed = _candidate(user_content="substituted")

    result = evaluate_episodic_persistence_readiness(
        changed,
        _consumption(original),
        _intent(original),
        NOW,
    )

    assert result.outcome is EpisodicPersistenceReadinessOutcome.DENIED
    assert (
        result.reason_code
        is EpisodicPersistenceReadinessReason.CANDIDATE_CONTENT_IDENTITY_MISMATCH
    )
    assert result.authorization_operation_binding is None


def test_g2b_t05_intent_candidate_mismatch_is_denied() -> None:
    candidate = _candidate()
    intent = replace(_intent(candidate), candidate_id="candidate-2")

    result = evaluate_episodic_persistence_readiness(
        candidate,
        _consumption(candidate),
        intent,
        NOW,
    )

    assert result.outcome is EpisodicPersistenceReadinessOutcome.DENIED
    assert result.reason_code is EpisodicPersistenceReadinessReason.INTENT_CANDIDATE_MISMATCH


def test_g2b_t06_intent_content_identity_mismatch_is_denied() -> None:
    candidate = _candidate()
    other = _candidate(user_content="other")
    intent = replace(
        _intent(candidate),
        candidate_content_identity=compute_episodic_candidate_content_identity(other),
    )

    result = evaluate_episodic_persistence_readiness(
        candidate,
        _consumption(candidate),
        intent,
        NOW,
    )

    assert result.outcome is EpisodicPersistenceReadinessOutcome.DENIED
    assert (
        result.reason_code
        is EpisodicPersistenceReadinessReason.INTENT_CONTENT_IDENTITY_MISMATCH
    )


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("subject_scope", "other-owner"),
        ("domain", "other-domain"),
        ("purpose", "other-purpose"),
    ],
)
def test_g2b_t07_intent_context_widening_is_denied(
    field_name: str,
    value: str,
) -> None:
    candidate = _candidate()
    intent = replace(_intent(candidate), **{field_name: value})

    result = evaluate_episodic_persistence_readiness(
        candidate,
        _consumption(candidate),
        intent,
        NOW,
    )

    assert result.outcome is EpisodicPersistenceReadinessOutcome.DENIED
    assert result.reason_code is EpisodicPersistenceReadinessReason.INTENT_CONTEXT_MISMATCH


def test_g2b_t08_future_intent_is_denied() -> None:
    candidate = _candidate()
    result = evaluate_episodic_persistence_readiness(
        candidate,
        _consumption(candidate),
        _intent(candidate, created_at=NOW + timedelta(seconds=1)),
        NOW,
    )

    assert result.outcome is EpisodicPersistenceReadinessOutcome.DENIED
    assert result.reason_code is EpisodicPersistenceReadinessReason.INTENT_FROM_FUTURE


def test_g2b_t09_stale_consumption_is_hold() -> None:
    candidate = _candidate()
    stale_time = NOW - timedelta(seconds=1)
    result = evaluate_episodic_persistence_readiness(
        candidate,
        _consumption(candidate, evaluated_at=stale_time),
        _intent(candidate),
        NOW,
    )

    assert result.outcome is EpisodicPersistenceReadinessOutcome.HOLD
    assert result.reason_code is EpisodicPersistenceReadinessReason.STALE_CONSUMPTION
    assert result.authorization_operation_binding is None


def test_g2b_t10_unsupported_consumption_policy_is_hold() -> None:
    candidate = _candidate()
    result = evaluate_episodic_persistence_readiness(
        candidate,
        _consumption(candidate, policy_version="old-consumption-policy"),
        _intent(candidate),
        NOW,
    )

    assert result.outcome is EpisodicPersistenceReadinessOutcome.HOLD
    assert (
        result.reason_code
        is EpisodicPersistenceReadinessReason.UNSUPPORTED_CONSUMPTION_POLICY
    )


def test_g2b_t11_unsupported_admission_policy_is_hold() -> None:
    candidate = _candidate()
    result = evaluate_episodic_persistence_readiness(
        candidate,
        _consumption(candidate, admission_policy_version="old-admission-policy"),
        _intent(candidate),
        NOW,
    )

    assert result.outcome is EpisodicPersistenceReadinessOutcome.HOLD
    assert result.reason_code is EpisodicPersistenceReadinessReason.UNSUPPORTED_ADMISSION_POLICY


def test_g2b_t12_projection_hold_propagates_as_hold() -> None:
    candidate = _candidate()
    consumption = _consumption(
        candidate,
        outcome=GovernedAdmissionConsumptionOutcome.BLOCKED,
        reason=GovernedAdmissionConsumptionReason.PROJECTION_HOLD,
    )

    result = evaluate_episodic_persistence_readiness(
        candidate,
        consumption,
        _intent(candidate),
        NOW,
    )

    assert result.outcome is EpisodicPersistenceReadinessOutcome.HOLD
    assert result.reason_code is EpisodicPersistenceReadinessReason.CONSUMPTION_HOLD


def test_g2b_t13_binding_block_propagates_as_denied() -> None:
    candidate = _candidate()
    consumption = _consumption(
        candidate,
        outcome=GovernedAdmissionConsumptionOutcome.BLOCKED,
        reason=GovernedAdmissionConsumptionReason.CONTENT_IDENTITY_BINDING_MISMATCH,
    )

    result = evaluate_episodic_persistence_readiness(
        candidate,
        consumption,
        _intent(candidate),
        NOW,
    )

    assert result.outcome is EpisodicPersistenceReadinessOutcome.DENIED
    assert result.reason_code is EpisodicPersistenceReadinessReason.CONSUMPTION_BLOCKED


def test_g2b_t14_admission_hold_propagates_as_hold() -> None:
    candidate = _candidate()
    consumption = _consumption(
        candidate,
        admission_outcome=EpisodicAdmissionOutcome.HOLD,
        admission_reason=EpisodicAdmissionReason.SENSITIVE_REVIEW_REQUIRED,
    )

    result = evaluate_episodic_persistence_readiness(
        candidate,
        consumption,
        _intent(candidate),
        NOW,
    )

    assert result.outcome is EpisodicPersistenceReadinessOutcome.HOLD
    assert result.reason_code is EpisodicPersistenceReadinessReason.ADMISSION_HOLD


def test_g2b_t15_admission_reject_propagates_as_denied() -> None:
    candidate = _candidate()
    consumption = _consumption(
        candidate,
        admission_outcome=EpisodicAdmissionOutcome.REJECT,
        admission_reason=EpisodicAdmissionReason.REVOKED_SOURCE,
    )

    result = evaluate_episodic_persistence_readiness(
        candidate,
        consumption,
        _intent(candidate),
        NOW,
    )

    assert result.outcome is EpisodicPersistenceReadinessOutcome.DENIED
    assert result.reason_code is EpisodicPersistenceReadinessReason.ADMISSION_REJECTED


def test_g2b_t16_binding_changes_when_material_changes() -> None:
    first_candidate = _candidate(user_content="first")
    second_candidate = _candidate(user_content="second")

    first = compute_episodic_persistence_operation_binding(
        first_candidate,
        _intent(first_candidate),
        NOW,
        consumption_policy_version=CONSUMPTION_POLICY_VERSION,
        admission_policy_version=ADMISSION_POLICY_VERSION,
    )
    second = compute_episodic_persistence_operation_binding(
        second_candidate,
        _intent(second_candidate),
        NOW,
        consumption_policy_version=CONSUMPTION_POLICY_VERSION,
        admission_policy_version=ADMISSION_POLICY_VERSION,
    )

    assert first != second


def test_g2b_t17_binding_changes_when_readiness_time_changes() -> None:
    candidate = _candidate()
    intent = _intent(candidate)

    first = compute_episodic_persistence_operation_binding(
        candidate,
        intent,
        NOW,
        consumption_policy_version=CONSUMPTION_POLICY_VERSION,
        admission_policy_version=ADMISSION_POLICY_VERSION,
    )
    second = compute_episodic_persistence_operation_binding(
        candidate,
        intent,
        NOW + timedelta(seconds=1),
        consumption_policy_version=CONSUMPTION_POLICY_VERSION,
        admission_policy_version=ADMISSION_POLICY_VERSION,
    )

    assert first != second


def test_g2b_t18_non_ready_result_cannot_carry_binding() -> None:
    binding = AuthorizationOperationBinding(
        namespace=OPERATION_BINDING_NAMESPACE,
        binding_version=OPERATION_BINDING_VERSION,
        digest_algorithm="sha256",
        digest_hex="ab" * 32,
    )
    candidate = _candidate()
    intent = _intent(candidate)

    with pytest.raises(ValueError, match="binding"):
        EpisodicPersistenceReadinessResult(
            candidate_id=candidate.candidate_id,
            candidate_content_identity=compute_episodic_candidate_content_identity(candidate),
            intent=intent,
            outcome=EpisodicPersistenceReadinessOutcome.HOLD,
            reason_code=EpisodicPersistenceReadinessReason.STALE_CONSUMPTION,
            evaluated_at=NOW,
            authorization_operation_binding=binding,
        )


def test_g2b_t19_ready_result_requires_binding() -> None:
    candidate = _candidate()
    intent = _intent(candidate)

    with pytest.raises(ValueError, match="binding"):
        EpisodicPersistenceReadinessResult(
            candidate_id=candidate.candidate_id,
            candidate_content_identity=compute_episodic_candidate_content_identity(candidate),
            intent=intent,
            outcome=EpisodicPersistenceReadinessOutcome.READY,
            reason_code=EpisodicPersistenceReadinessReason.READY,
            evaluated_at=NOW,
            authorization_operation_binding=None,
        )


def test_g2b_t20_wrong_input_types_fail_closed() -> None:
    candidate = _candidate()
    consumption = _consumption(candidate)
    intent = _intent(candidate)

    with pytest.raises(TypeError, match="candidate"):
        evaluate_episodic_persistence_readiness(object(), consumption, intent, NOW)  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="consumption"):
        evaluate_episodic_persistence_readiness(candidate, object(), intent, NOW)  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="intent"):
        evaluate_episodic_persistence_readiness(candidate, consumption, object(), NOW)  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="evaluated_at"):
        evaluate_episodic_persistence_readiness(candidate, consumption, intent, "now")  # type: ignore[arg-type]


def test_g2b_t21_non_utc_readiness_time_is_rejected() -> None:
    candidate = _candidate()
    non_utc = datetime(2026, 9, 15, 17, 0, tzinfo=timezone(timedelta(hours=-3)))

    with pytest.raises(ValueError, match="UTC"):
        evaluate_episodic_persistence_readiness(
            candidate,
            _consumption(candidate),
            _intent(candidate),
            non_utc,
        )
