from dataclasses import FrozenInstanceError, replace
from datetime import datetime, timedelta, timezone
import builtins
import socket

import pytest

import malak.memory.governed_input_projection as projection_module
from malak.memory.episodic_admission import (
    EpisodicAdmissionContext,
    EpisodicAdmissionDecision,
    EpisodicAdmissionOutcome,
    EpisodicAdmissionReason,
    EpisodicAdmissionSignals,
    EpisodicExperience,
    EpisodicMemoryCandidate,
    EpisodicOrigin,
    SourceSecurityStatus,
)
from malak.memory.governed_input_projection import (
    POLICY_VERSION as PROJECTION_POLICY_VERSION,
    GovernedAdmissionInputProjection,
    GovernedAdmissionProjectionOutcome,
    GovernedAdmissionProjectionReason,
)
import malak.memory.governed_projection_consumption as consumption
from malak.memory.governed_projection_consumption import (
    POLICY_VERSION,
    GovernedAdmissionConsumptionOutcome,
    GovernedAdmissionConsumptionReason,
    GovernedAdmissionConsumptionResult,
    consume_governed_admission_projection,
)


NOW = datetime(2026, 9, 10, 12, 45, tzinfo=timezone.utc)


def _context(
    *,
    subject_scope: str = "subject-scope",
    domain: str = "domain-1",
    purpose: str = "purpose-1",
    source_authority: str | None = "governed-authority",
    confidence: str | None = "governed-confidence",
    sensitivity: str | None = "governed-sensitivity",
    valid_from: datetime | None = None,
    valid_until: datetime | None = None,
) -> EpisodicAdmissionContext:
    return EpisodicAdmissionContext(
        subject_scope=subject_scope,
        domain=domain,
        purpose=purpose,
        source_authority_classification=source_authority,
        confidence_classification=confidence,
        sensitivity_classification=sensitivity,
        valid_from=valid_from if valid_from is not None else NOW - timedelta(hours=1),
        valid_until=valid_until if valid_until is not None else NOW + timedelta(hours=1),
    )


def _candidate(
    *,
    candidate_id: str = "candidate-1",
    control: EpisodicAdmissionContext | None = None,
) -> EpisodicMemoryCandidate:
    return EpisodicMemoryCandidate(
        candidate_id=candidate_id,
        origin=EpisodicOrigin(
            session_id="session-1",
            request_id="request-1",
            request_created_at=NOW - timedelta(hours=2),
            provider="provider-1",
            model="model-1",
        ),
        experience=EpisodicExperience(
            user_content="user content",
            assistant_content="assistant content",
        ),
        control=control or _context(
            source_authority="original-authority",
            confidence="original-confidence",
            sensitivity="original-sensitivity",
        ),
        created_at=NOW - timedelta(hours=2),
    )


def _signals(
    *,
    scope_applicable: bool = True,
    policy_violation: bool = False,
    source_security_status: SourceSecurityStatus = SourceSecurityStatus.ACCEPTABLE,
    sensitive_review_required: bool = False,
    contradiction_requires_review: bool = False,
) -> EpisodicAdmissionSignals:
    return EpisodicAdmissionSignals(
        scope_applicable=scope_applicable,
        policy_violation=policy_violation,
        source_security_status=source_security_status,
        sensitive_review_required=sensitive_review_required,
        contradiction_requires_review=contradiction_requires_review,
    )


def _projection(
    *,
    candidate_id: str = "candidate-1",
    outcome: GovernedAdmissionProjectionOutcome = GovernedAdmissionProjectionOutcome.READY,
    evaluated_at: datetime = NOW,
    effective_context: EpisodicAdmissionContext | None = None,
    effective_signals: EpisodicAdmissionSignals | None = None,
    policy_version: str = PROJECTION_POLICY_VERSION,
) -> GovernedAdmissionInputProjection:
    if outcome is GovernedAdmissionProjectionOutcome.READY:
        return GovernedAdmissionInputProjection(
            candidate_id=candidate_id,
            outcome=outcome,
            reason_code=GovernedAdmissionProjectionReason.READY,
            evaluated_at=evaluated_at,
            effective_context=effective_context or _context(),
            effective_signals=effective_signals or _signals(),
            policy_version=policy_version,
        )
    if outcome is GovernedAdmissionProjectionOutcome.HOLD:
        reason = GovernedAdmissionProjectionReason.MISSING_REQUIRED_ASSESSMENT
    else:
        reason = GovernedAdmissionProjectionReason.ASSESSMENT_AUTHORIZATION_DENIED
    return GovernedAdmissionInputProjection(
        candidate_id=candidate_id,
        outcome=outcome,
        reason_code=reason,
        evaluated_at=evaluated_at,
        policy_version=policy_version,
    )


def _decision(
    *,
    candidate_id: str = "candidate-1",
    evaluated_at: datetime = NOW,
    outcome: EpisodicAdmissionOutcome = EpisodicAdmissionOutcome.ELIGIBLE,
    reason: EpisodicAdmissionReason = EpisodicAdmissionReason.ELIGIBLE,
) -> EpisodicAdmissionDecision:
    return EpisodicAdmissionDecision(
        candidate_id=candidate_id,
        outcome=outcome,
        reason_code=reason,
        evaluated_at=evaluated_at,
    )


def _consume(
    *,
    candidate: EpisodicMemoryCandidate | None = None,
    projection: GovernedAdmissionInputProjection | None = None,
    evaluated_at: datetime = NOW,
) -> GovernedAdmissionConsumptionResult:
    return consume_governed_admission_projection(
        candidate or _candidate(),
        projection or _projection(),
        evaluated_at,
    )


def _assert_evaluated(
    result: GovernedAdmissionConsumptionResult,
    outcome: EpisodicAdmissionOutcome,
    reason: EpisodicAdmissionReason,
) -> None:
    assert result.outcome is GovernedAdmissionConsumptionOutcome.EVALUATED
    assert result.reason_code is GovernedAdmissionConsumptionReason.EVALUATED
    assert result.admission_decision is not None
    assert result.admission_decision.outcome is outcome
    assert result.admission_decision.reason_code is reason


def test_gc2_t01_result_is_immutable() -> None:
    result = _consume()
    with pytest.raises(FrozenInstanceError):
        result.outcome = GovernedAdmissionConsumptionOutcome.BLOCKED  # type: ignore[misc]


def test_gc2_t02_wrong_candidate_type_raises_type_error() -> None:
    with pytest.raises(TypeError, match="candidate"):
        consume_governed_admission_projection(object(), _projection(), NOW)  # type: ignore[arg-type]


def test_gc2_t03_wrong_projection_type_raises_type_error() -> None:
    with pytest.raises(TypeError, match="projection"):
        consume_governed_admission_projection(_candidate(), object(), NOW)  # type: ignore[arg-type]


def test_gc2_t04_wrong_evaluated_at_type_raises_type_error() -> None:
    with pytest.raises(TypeError, match="evaluated_at"):
        consume_governed_admission_projection(_candidate(), _projection(), "now")  # type: ignore[arg-type]


def test_gc2_t05_naive_evaluated_at_raises_value_error() -> None:
    with pytest.raises(ValueError, match="timezone"):
        _consume(evaluated_at=datetime(2026, 9, 10, 12, 45))


def test_gc2_t06_non_utc_evaluated_at_raises_value_error() -> None:
    non_utc = datetime(2026, 9, 10, 9, 45, tzinfo=timezone(timedelta(hours=-3)))
    with pytest.raises(ValueError, match="UTC"):
        _consume(evaluated_at=non_utc)


def test_gc2_t07_evaluated_result_requires_decision() -> None:
    with pytest.raises(ValueError):
        GovernedAdmissionConsumptionResult(
            candidate_id="candidate-1",
            outcome=GovernedAdmissionConsumptionOutcome.EVALUATED,
            reason_code=GovernedAdmissionConsumptionReason.EVALUATED,
            evaluated_at=NOW,
        )


def test_gc2_t08_blocked_result_forbids_decision() -> None:
    with pytest.raises(ValueError):
        GovernedAdmissionConsumptionResult(
            candidate_id="candidate-1",
            outcome=GovernedAdmissionConsumptionOutcome.BLOCKED,
            reason_code=GovernedAdmissionConsumptionReason.PROJECTION_HOLD,
            evaluated_at=NOW,
            admission_decision=_decision(),
        )


def test_gc2_t09_outcome_reason_mismatch_fails_construction() -> None:
    with pytest.raises(ValueError):
        GovernedAdmissionConsumptionResult(
            candidate_id="candidate-1",
            outcome=GovernedAdmissionConsumptionOutcome.BLOCKED,
            reason_code=GovernedAdmissionConsumptionReason.EVALUATED,
            evaluated_at=NOW,
        )


def test_gc2_t10_decision_candidate_id_must_match_result() -> None:
    with pytest.raises(ValueError):
        GovernedAdmissionConsumptionResult(
            candidate_id="candidate-1",
            outcome=GovernedAdmissionConsumptionOutcome.EVALUATED,
            reason_code=GovernedAdmissionConsumptionReason.EVALUATED,
            evaluated_at=NOW,
            admission_decision=_decision(candidate_id="candidate-2"),
        )


def test_gc2_t11_decision_evaluated_at_must_match_result() -> None:
    with pytest.raises(ValueError):
        GovernedAdmissionConsumptionResult(
            candidate_id="candidate-1",
            outcome=GovernedAdmissionConsumptionOutcome.EVALUATED,
            reason_code=GovernedAdmissionConsumptionReason.EVALUATED,
            evaluated_at=NOW,
            admission_decision=_decision(evaluated_at=NOW + timedelta(seconds=1)),
        )


def test_gc2_t12_candidate_id_mismatch_blocks() -> None:
    result = _consume(projection=_projection(candidate_id="candidate-2"))
    assert result.outcome is GovernedAdmissionConsumptionOutcome.BLOCKED
    assert result.reason_code is GovernedAdmissionConsumptionReason.CANDIDATE_BINDING_MISMATCH
    assert result.admission_decision is None


def test_gc2_t13_unknown_projection_policy_blocks() -> None:
    result = _consume(projection=_projection(policy_version="projection/unknown"))
    assert result.reason_code is GovernedAdmissionConsumptionReason.UNSUPPORTED_PROJECTION_POLICY
    assert result.admission_decision is None


def test_gc2_t14_time_reversal_blocks() -> None:
    projection = _projection(evaluated_at=NOW + timedelta(seconds=1))
    result = _consume(projection=projection, evaluated_at=NOW)
    assert result.reason_code is GovernedAdmissionConsumptionReason.CONSUMPTION_TIME_PRECEDES_PROJECTION
    assert result.admission_decision is None


def test_gc2_t15_denied_projection_blocks_without_admission_decision() -> None:
    result = _consume(projection=_projection(outcome=GovernedAdmissionProjectionOutcome.DENIED))
    assert result.reason_code is GovernedAdmissionConsumptionReason.PROJECTION_DENIED
    assert result.admission_decision is None


def test_gc2_t16_hold_projection_blocks_without_admission_decision() -> None:
    result = _consume(projection=_projection(outcome=GovernedAdmissionProjectionOutcome.HOLD))
    assert result.reason_code is GovernedAdmissionConsumptionReason.PROJECTION_HOLD
    assert result.admission_decision is None


def test_gc2_t17_subject_scope_mismatch_blocks() -> None:
    result = _consume(projection=_projection(effective_context=_context(subject_scope="other-scope")))
    assert result.reason_code is GovernedAdmissionConsumptionReason.CONTEXT_BINDING_MISMATCH


def test_gc2_t18_domain_mismatch_blocks() -> None:
    result = _consume(projection=_projection(effective_context=_context(domain="other-domain")))
    assert result.reason_code is GovernedAdmissionConsumptionReason.CONTEXT_BINDING_MISMATCH


def test_gc2_t19_purpose_mismatch_blocks() -> None:
    result = _consume(projection=_projection(effective_context=_context(purpose="other-purpose")))
    assert result.reason_code is GovernedAdmissionConsumptionReason.CONTEXT_BINDING_MISMATCH


def test_gc2_t20_multiple_blockers_follow_exact_precedence() -> None:
    candidate = _candidate(candidate_id="candidate-1")
    result = _consume(
        candidate=candidate,
        projection=_projection(
            candidate_id="candidate-2",
            outcome=GovernedAdmissionProjectionOutcome.DENIED,
            evaluated_at=NOW + timedelta(minutes=1),
            policy_version="projection/unknown",
        ),
        evaluated_at=NOW,
    )
    assert result.reason_code is GovernedAdmissionConsumptionReason.CANDIDATE_BINDING_MISMATCH

    result = _consume(
        projection=_projection(
            outcome=GovernedAdmissionProjectionOutcome.DENIED,
            evaluated_at=NOW + timedelta(minutes=1),
            policy_version="projection/unknown",
        ),
        evaluated_at=NOW,
    )
    assert result.reason_code is GovernedAdmissionConsumptionReason.UNSUPPORTED_PROJECTION_POLICY

    result = _consume(
        projection=_projection(
            outcome=GovernedAdmissionProjectionOutcome.DENIED,
            evaluated_at=NOW + timedelta(minutes=1),
        ),
        evaluated_at=NOW,
    )
    assert result.reason_code is GovernedAdmissionConsumptionReason.CONSUMPTION_TIME_PRECEDES_PROJECTION


def test_gc2_t21_equal_projection_and_consumption_time_can_evaluate() -> None:
    _assert_evaluated(_consume(), EpisodicAdmissionOutcome.ELIGIBLE, EpisodicAdmissionReason.ELIGIBLE)


def test_gc2_t22_later_consumption_time_can_evaluate() -> None:
    result = _consume(evaluated_at=NOW + timedelta(minutes=10))
    _assert_evaluated(result, EpisodicAdmissionOutcome.ELIGIBLE, EpisodicAdmissionReason.ELIGIBLE)


def test_gc2_t23_projection_age_alone_does_not_block() -> None:
    old_time = NOW - timedelta(days=365)
    context = _context(valid_from=old_time - timedelta(days=1), valid_until=NOW + timedelta(days=1))
    projection = _projection(evaluated_at=old_time, effective_context=context)
    _assert_evaluated(_consume(projection=projection), EpisodicAdmissionOutcome.ELIGIBLE, EpisodicAdmissionReason.ELIGIBLE)


def test_gc2_t24_effective_expiry_uses_fresh_consumption_time() -> None:
    context = _context(valid_from=NOW - timedelta(hours=2), valid_until=NOW + timedelta(minutes=1))
    projection = _projection(effective_context=context)
    result = _consume(projection=projection, evaluated_at=NOW + timedelta(minutes=2))
    _assert_evaluated(result, EpisodicAdmissionOutcome.REJECT, EpisodicAdmissionReason.TEMPORAL_EXPIRED)


def test_gc2_t25_effective_future_window_remains_admission_owned() -> None:
    context = _context(valid_from=NOW + timedelta(minutes=5), valid_until=NOW + timedelta(hours=1))
    result = _consume(projection=_projection(effective_context=context))
    _assert_evaluated(result, EpisodicAdmissionOutcome.HOLD, EpisodicAdmissionReason.TEMPORAL_NOT_YET_VALID)


def test_gc2_t26_original_source_authority_cannot_leak() -> None:
    original = _context(source_authority=None)
    result = _consume(candidate=_candidate(control=original))
    _assert_evaluated(result, EpisodicAdmissionOutcome.ELIGIBLE, EpisodicAdmissionReason.ELIGIBLE)


def test_gc2_t27_original_confidence_cannot_leak() -> None:
    original = _context(confidence=None)
    result = _consume(candidate=_candidate(control=original))
    _assert_evaluated(result, EpisodicAdmissionOutcome.ELIGIBLE, EpisodicAdmissionReason.ELIGIBLE)


def test_gc2_t28_original_sensitivity_cannot_leak() -> None:
    original = _context(sensitivity=None)
    result = _consume(candidate=_candidate(control=original))
    _assert_evaluated(result, EpisodicAdmissionOutcome.ELIGIBLE, EpisodicAdmissionReason.ELIGIBLE)


def test_gc2_t29_original_valid_until_cannot_leak() -> None:
    original = _context(valid_from=NOW - timedelta(days=2), valid_until=NOW - timedelta(days=1))
    result = _consume(candidate=_candidate(control=original))
    _assert_evaluated(result, EpisodicAdmissionOutcome.ELIGIBLE, EpisodicAdmissionReason.ELIGIBLE)


def test_gc2_t30_original_valid_from_cannot_leak() -> None:
    original = _context(valid_from=NOW + timedelta(days=1), valid_until=NOW + timedelta(days=2))
    result = _consume(candidate=_candidate(control=original))
    _assert_evaluated(result, EpisodicAdmissionOutcome.ELIGIBLE, EpisodicAdmissionReason.ELIGIBLE)


def test_gc2_t31_original_candidate_remains_unmodified() -> None:
    candidate = _candidate()
    before = candidate
    original_control = candidate.control
    _consume(candidate=candidate)
    assert candidate == before
    assert candidate.control is original_control


def test_gc2_t32_effective_candidate_view_does_not_escape(monkeypatch: pytest.MonkeyPatch) -> None:
    candidate = _candidate()
    projection = _projection()
    captured: list[EpisodicMemoryCandidate] = []

    def fake_evaluator(
        effective_candidate: EpisodicMemoryCandidate,
        signals: EpisodicAdmissionSignals,
        evaluated_at: datetime,
    ) -> EpisodicAdmissionDecision:
        captured.append(effective_candidate)
        assert signals is projection.effective_signals
        return _decision(candidate_id=effective_candidate.candidate_id, evaluated_at=evaluated_at)

    monkeypatch.setattr(consumption, "evaluate_episodic_candidate", fake_evaluator)
    result = _consume(candidate=candidate, projection=projection)
    assert len(captured) == 1
    assert captured[0] is not candidate
    assert captured[0].candidate_id == candidate.candidate_id
    assert captured[0].origin is candidate.origin
    assert captured[0].experience is candidate.experience
    assert captured[0].created_at == candidate.created_at
    assert captured[0].control is projection.effective_context
    assert not hasattr(result, "effective_candidate")


def test_gc2_t33_policy_violation_is_admission_owned() -> None:
    projection = _projection(effective_signals=_signals(policy_violation=True))
    _assert_evaluated(_consume(projection=projection), EpisodicAdmissionOutcome.REJECT, EpisodicAdmissionReason.POLICY_VIOLATION)


def test_gc2_t34_out_of_scope_is_admission_owned() -> None:
    projection = _projection(effective_signals=_signals(scope_applicable=False))
    _assert_evaluated(_consume(projection=projection), EpisodicAdmissionOutcome.REJECT, EpisodicAdmissionReason.OUT_OF_SCOPE)


def test_gc2_t35_tainted_source_is_admission_owned() -> None:
    projection = _projection(effective_signals=_signals(source_security_status=SourceSecurityStatus.TAINTED))
    _assert_evaluated(_consume(projection=projection), EpisodicAdmissionOutcome.REJECT, EpisodicAdmissionReason.TAINTED_SOURCE)


def test_gc2_t36_revoked_source_is_admission_owned() -> None:
    projection = _projection(effective_signals=_signals(source_security_status=SourceSecurityStatus.REVOKED))
    _assert_evaluated(_consume(projection=projection), EpisodicAdmissionOutcome.REJECT, EpisodicAdmissionReason.REVOKED_SOURCE)


def test_gc2_t37_unassessed_source_is_admission_owned() -> None:
    projection = _projection(effective_signals=_signals(source_security_status=SourceSecurityStatus.UNASSESSED))
    _assert_evaluated(_consume(projection=projection), EpisodicAdmissionOutcome.HOLD, EpisodicAdmissionReason.SOURCE_UNASSESSED)


def test_gc2_t38_suspect_source_is_admission_owned() -> None:
    projection = _projection(effective_signals=_signals(source_security_status=SourceSecurityStatus.SUSPECT))
    _assert_evaluated(_consume(projection=projection), EpisodicAdmissionOutcome.HOLD, EpisodicAdmissionReason.SUSPECT_SOURCE)


def test_gc2_t39_sensitive_review_is_admission_owned() -> None:
    projection = _projection(effective_signals=_signals(sensitive_review_required=True))
    _assert_evaluated(_consume(projection=projection), EpisodicAdmissionOutcome.HOLD, EpisodicAdmissionReason.SENSITIVE_REVIEW_REQUIRED)


def test_gc2_t40_contradiction_review_is_admission_owned() -> None:
    projection = _projection(effective_signals=_signals(contradiction_requires_review=True))
    _assert_evaluated(_consume(projection=projection), EpisodicAdmissionOutcome.HOLD, EpisodicAdmissionReason.CONTRADICTION_REQUIRES_REVIEW)


def test_gc2_t41_admissible_inputs_produce_eligible_without_storage() -> None:
    result = _consume()
    _assert_evaluated(result, EpisodicAdmissionOutcome.ELIGIBLE, EpisodicAdmissionReason.ELIGIBLE)
    assert not hasattr(result, "persistence_authorization")


def test_gc2_t42_evaluated_calls_admission_exactly_once(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = 0

    def fake_evaluator(
        candidate: EpisodicMemoryCandidate,
        signals: EpisodicAdmissionSignals,
        evaluated_at: datetime,
    ) -> EpisodicAdmissionDecision:
        nonlocal calls
        calls += 1
        return _decision(candidate_id=candidate.candidate_id, evaluated_at=evaluated_at)

    monkeypatch.setattr(consumption, "evaluate_episodic_candidate", fake_evaluator)
    _consume()
    assert calls == 1


def test_gc2_t43_all_blocked_paths_call_admission_zero_times(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = 0

    def fake_evaluator(*args: object, **kwargs: object) -> EpisodicAdmissionDecision:
        nonlocal calls
        calls += 1
        return _decision()

    monkeypatch.setattr(consumption, "evaluate_episodic_candidate", fake_evaluator)
    cases = (
        (_candidate(), _projection(candidate_id="candidate-2"), NOW),
        (_candidate(), _projection(policy_version="projection/unknown"), NOW),
        (_candidate(), _projection(evaluated_at=NOW + timedelta(seconds=1)), NOW),
        (_candidate(), _projection(outcome=GovernedAdmissionProjectionOutcome.DENIED), NOW),
        (_candidate(), _projection(outcome=GovernedAdmissionProjectionOutcome.HOLD), NOW),
        (_candidate(), _projection(effective_context=_context(domain="other-domain")), NOW),
    )
    for candidate, projection, evaluated_at in cases:
        result = consume_governed_admission_projection(candidate, projection, evaluated_at)
        assert result.outcome is GovernedAdmissionConsumptionOutcome.BLOCKED
    assert calls == 0


def test_gc2_t44_admission_decision_is_preserved_exactly(monkeypatch: pytest.MonkeyPatch) -> None:
    sentinel = _decision()

    def fake_evaluator(
        candidate: EpisodicMemoryCandidate,
        signals: EpisodicAdmissionSignals,
        evaluated_at: datetime,
    ) -> EpisodicAdmissionDecision:
        return sentinel

    monkeypatch.setattr(consumption, "evaluate_episodic_candidate", fake_evaluator)
    result = _consume()
    assert result.admission_decision is sentinel


def test_gc2_t45_same_inputs_and_time_are_deterministic() -> None:
    candidate = _candidate()
    projection = _projection()
    first = consume_governed_admission_projection(candidate, projection, NOW)
    second = consume_governed_admission_projection(candidate, projection, NOW)
    assert first == second


def test_gc2_t46_consumer_does_not_recompute_projection(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*args: object, **kwargs: object) -> object:
        raise AssertionError("projection recomputation is forbidden")

    monkeypatch.setattr(projection_module, "project_governed_admission_inputs", forbidden)
    _assert_evaluated(_consume(), EpisodicAdmissionOutcome.ELIGIBLE, EpisodicAdmissionReason.ELIGIBLE)


def test_gc2_t47_consumer_has_no_security_reauthorization_surface() -> None:
    forbidden_names = {
        "AuthorizationRequest",
        "AuthorizationDecision",
        "SecurityContext",
        "validate_assessment_producer_authorization",
        "project_governed_admission_inputs",
    }
    assert forbidden_names.isdisjoint(vars(consumption))


def test_gc2_t48_consumer_has_no_filesystem_network_or_persistence_side_effects(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbidden(*args: object, **kwargs: object) -> object:
        raise AssertionError("I/O is forbidden")

    monkeypatch.setattr(builtins, "open", forbidden)
    monkeypatch.setattr(socket, "socket", forbidden)
    _assert_evaluated(_consume(), EpisodicAdmissionOutcome.ELIGIBLE, EpisodicAdmissionReason.ELIGIBLE)


def test_gc2_t49_eligible_stops_without_persistence_authorization() -> None:
    result = _consume()
    assert result.policy_version == POLICY_VERSION
    assert result.admission_decision is not None
    assert result.admission_decision.outcome is EpisodicAdmissionOutcome.ELIGIBLE
    assert set(result.__dataclass_fields__) == {
        "candidate_id",
        "outcome",
        "reason_code",
        "evaluated_at",
        "admission_decision",
        "policy_version",
    }
