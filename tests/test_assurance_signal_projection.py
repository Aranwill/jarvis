from dataclasses import replace
from datetime import datetime, timedelta, timezone
from itertools import permutations

import pytest

from malak.core.assurance_signal_projection import (
    SIGNAL_POLICY_VERSION,
    AssuranceSignalKind,
    AssuranceSignalObservation,
    AssuranceSignalProducerAuthorizationEvidence,
    AssuranceSignalProjectionOutcome,
    AssuranceSignalProjectionReason,
    project_assurance_signals,
    required_permission_for_signal,
)
from malak.core.protected_finalization import (
    AssuranceApplicability,
    ProtectedFinalizationOutcome,
    ProtectedResponseCandidate,
    evaluate_protected_finalization,
)
from malak.security.contracts import (
    AuthorizationDecision,
    AuthorizationRequest,
    SecurityContext,
)


EVALUATED_AT = datetime(2026, 9, 12, 3, 0, tzinfo=timezone.utc)
REQUEST_ID = "request-g2"
SESSION_ID = "session-g2"


def _candidate() -> ProtectedResponseCandidate:
    return ProtectedResponseCandidate(
        request_id=REQUEST_ID,
        session_id=SESSION_ID,
        content="candidate response",
        provider="test-provider",
        model="test-model",
    )


def _default_values() -> dict[AssuranceSignalKind, object]:
    return {
        AssuranceSignalKind.APPLICABILITY: AssuranceApplicability.REQUIRED,
        AssuranceSignalKind.EVIDENCE_REQUIRED: True,
        AssuranceSignalKind.SUPPORT_SUFFICIENT: True,
        AssuranceSignalKind.CONTRADICTION_UNRESOLVED: False,
        AssuranceSignalKind.POLICY_VIOLATION: False,
    }


def _canonical_value(kind: AssuranceSignalKind, value: object) -> str:
    if kind is AssuranceSignalKind.APPLICABILITY:
        assert isinstance(value, AssuranceApplicability)
        return value.value
    assert type(value) is bool
    return "true" if value else "false"


def _material(
    *,
    values: dict[AssuranceSignalKind, object] | None = None,
    authenticated: bool = True,
    allowed: bool = True,
    signal_policy_version: str = SIGNAL_POLICY_VERSION,
    request_id: str = REQUEST_ID,
    session_id: str = SESSION_ID,
    created_at: datetime | None = None,
    issued_at: datetime | None = None,
    expires_at: datetime | None = None,
) -> tuple[
    tuple[AssuranceSignalObservation, ...],
    tuple[AssuranceSignalProducerAuthorizationEvidence, ...],
]:
    signal_values = _default_values() if values is None else values
    issued = issued_at or EVALUATED_AT - timedelta(minutes=10)
    expires = expires_at or EVALUATED_AT + timedelta(minutes=10)
    created = created_at or EVALUATED_AT - timedelta(minutes=5)

    observations: list[AssuranceSignalObservation] = []
    evidence: list[AssuranceSignalProducerAuthorizationEvidence] = []

    for index, kind in enumerate(AssuranceSignalKind):
        value = signal_values[kind]
        subject_id = f"producer-{kind.value}"
        observation = AssuranceSignalObservation(
            signal_kind=kind,
            value=value,
            request_id=request_id,
            session_id=session_id,
            producer_subject_id=subject_id,
            signal_policy_version=signal_policy_version,
        )
        observations.append(observation)

        permission = required_permission_for_signal(kind, value)
        assert permission is not None
        authorization_request = AuthorizationRequest(
            context=SecurityContext(
                context_id=f"context-{index}",
                session_id=session_id,
                subject_id=subject_id,
                authenticated=authenticated,
                issued_at=issued,
                expires_at=expires,
            ),
            permission=permission,
            request_id=f"auth-request-{index}",
            created_at=created,
        )
        authorization_decision = AuthorizationDecision(
            request_id=authorization_request.request_id,
            allowed=allowed,
            reason="test decision",
        )
        evidence.append(
            AssuranceSignalProducerAuthorizationEvidence(
                signal_kind=kind,
                canonical_value=_canonical_value(kind, value),
                request_id=request_id,
                session_id=session_id,
                producer_subject_id=subject_id,
                authorization_request=authorization_request,
                authorization_decision=authorization_decision,
            )
        )

    return tuple(observations), tuple(evidence)


def _replace_observation(
    observations: tuple[AssuranceSignalObservation, ...],
    kind: AssuranceSignalKind,
    **changes: object,
) -> tuple[AssuranceSignalObservation, ...]:
    return tuple(
        replace(item, **changes) if item.signal_kind is kind else item
        for item in observations
    )


def _replace_evidence(
    evidence: tuple[AssuranceSignalProducerAuthorizationEvidence, ...],
    kind: AssuranceSignalKind,
    **changes: object,
) -> tuple[AssuranceSignalProducerAuthorizationEvidence, ...]:
    return tuple(
        replace(item, **changes) if item.signal_kind is kind else item
        for item in evidence
    )


def test_not_applicable_projects_and_g2a_accepts() -> None:
    values = _default_values()
    values.update(
        {
            AssuranceSignalKind.APPLICABILITY: AssuranceApplicability.NOT_APPLICABLE,
            AssuranceSignalKind.EVIDENCE_REQUIRED: False,
            AssuranceSignalKind.SUPPORT_SUFFICIENT: False,
            AssuranceSignalKind.CONTRADICTION_UNRESOLVED: False,
        }
    )
    observations, evidence = _material(values=values)

    result = project_assurance_signals(
        _candidate(), observations, evidence, EVALUATED_AT
    )

    assert result.outcome is AssuranceSignalProjectionOutcome.READY
    assert result.reason_code is AssuranceSignalProjectionReason.READY
    assert result.projected_input is not None
    assert result.projected_input.applicability is AssuranceApplicability.NOT_APPLICABLE
    assert result.projected_input.evidence_required is False
    assert result.projected_input.support_sufficient is False
    assert result.projected_input.contradiction_unresolved is False
    assert result.projected_input.policy_violation is False

    final = evaluate_protected_finalization(
        _candidate(), result.projected_input, EVALUATED_AT
    )
    assert final.outcome is ProtectedFinalizationOutcome.ACCEPT


def test_required_insufficient_support_projects_and_g2a_abstains() -> None:
    values = _default_values()
    values[AssuranceSignalKind.SUPPORT_SUFFICIENT] = False
    observations, evidence = _material(values=values)

    result = project_assurance_signals(
        _candidate(), observations, evidence, EVALUATED_AT
    )

    assert result.outcome is AssuranceSignalProjectionOutcome.READY
    assert result.projected_input is not None
    final = evaluate_protected_finalization(
        _candidate(), result.projected_input, EVALUATED_AT
    )
    assert final.outcome is ProtectedFinalizationOutcome.ABSTAIN


def test_policy_violation_projects_and_g2a_blocks() -> None:
    values = _default_values()
    values[AssuranceSignalKind.POLICY_VIOLATION] = True
    observations, evidence = _material(values=values)

    result = project_assurance_signals(
        _candidate(), observations, evidence, EVALUATED_AT
    )

    assert result.outcome is AssuranceSignalProjectionOutcome.READY
    assert result.projected_input is not None
    final = evaluate_protected_finalization(
        _candidate(), result.projected_input, EVALUATED_AT
    )
    assert final.outcome is ProtectedFinalizationOutcome.BLOCK


def test_missing_signal_holds_without_partial_projection() -> None:
    observations, evidence = _material()

    result = project_assurance_signals(
        _candidate(), observations[:-1], evidence, EVALUATED_AT
    )

    assert result.outcome is AssuranceSignalProjectionOutcome.HOLD
    assert result.reason_code is AssuranceSignalProjectionReason.MISSING_SIGNAL
    assert result.projected_input is None


def test_missing_authorization_evidence_holds() -> None:
    observations, evidence = _material()

    result = project_assurance_signals(
        _candidate(), observations, evidence[:-1], EVALUATED_AT
    )

    assert result.outcome is AssuranceSignalProjectionOutcome.HOLD
    assert (
        result.reason_code
        is AssuranceSignalProjectionReason.MISSING_AUTHORIZATION_EVIDENCE
    )
    assert result.projected_input is None


def test_wrong_permission_denies_trust_clearing_value() -> None:
    observations, evidence = _material()
    target = next(
        item
        for item in evidence
        if item.signal_kind is AssuranceSignalKind.SUPPORT_SUFFICIENT
    )
    wrong_request = replace(
        target.authorization_request,
        permission=required_permission_for_signal(
            AssuranceSignalKind.SUPPORT_SUFFICIENT,
            False,
        ),
    )
    evidence = _replace_evidence(
        evidence,
        AssuranceSignalKind.SUPPORT_SUFFICIENT,
        authorization_request=wrong_request,
    )

    result = project_assurance_signals(
        _candidate(), observations, evidence, EVALUATED_AT
    )

    assert result.outcome is AssuranceSignalProjectionOutcome.DENIED
    assert (
        result.reason_code
        is AssuranceSignalProjectionReason.PERMISSION_SCOPE_MISMATCH
    )


def test_unauthenticated_context_denies_even_with_allowed_decision() -> None:
    observations, evidence = _material(authenticated=False, allowed=True)

    result = project_assurance_signals(
        _candidate(), observations, evidence, EVALUATED_AT
    )

    assert result.outcome is AssuranceSignalProjectionOutcome.DENIED
    assert result.reason_code is AssuranceSignalProjectionReason.PRODUCER_NOT_AUTHENTICATED


def test_authorization_evidence_from_other_request_denies() -> None:
    observations, evidence = _material()
    evidence = _replace_evidence(
        evidence,
        AssuranceSignalKind.POLICY_VIOLATION,
        request_id="other-request",
    )

    result = project_assurance_signals(
        _candidate(), observations, evidence, EVALUATED_AT
    )

    assert result.outcome is AssuranceSignalProjectionOutcome.DENIED
    assert result.reason_code is AssuranceSignalProjectionReason.REQUEST_ID_MISMATCH


def test_authorization_request_created_after_evaluation_denies() -> None:
    observations, evidence = _material(
        created_at=EVALUATED_AT + timedelta(seconds=1)
    )

    result = project_assurance_signals(
        _candidate(), observations, evidence, EVALUATED_AT
    )

    assert result.outcome is AssuranceSignalProjectionOutcome.DENIED
    assert (
        result.reason_code
        is AssuranceSignalProjectionReason.AUTHORIZATION_REQUEST_TIME_INVALID
    )


def test_not_applicable_with_unresolved_contradiction_denies() -> None:
    values = _default_values()
    values.update(
        {
            AssuranceSignalKind.APPLICABILITY: AssuranceApplicability.NOT_APPLICABLE,
            AssuranceSignalKind.EVIDENCE_REQUIRED: False,
            AssuranceSignalKind.SUPPORT_SUFFICIENT: False,
            AssuranceSignalKind.CONTRADICTION_UNRESOLVED: True,
        }
    )
    observations, evidence = _material(values=values)

    result = project_assurance_signals(
        _candidate(), observations, evidence, EVALUATED_AT
    )

    assert result.outcome is AssuranceSignalProjectionOutcome.DENIED
    assert result.reason_code is AssuranceSignalProjectionReason.SIGNAL_SET_INCOHERENT


def test_duplicate_authorization_request_id_denies() -> None:
    observations, evidence = _material()
    source = evidence[0].authorization_request.request_id
    target = evidence[1]
    duplicate_request = replace(target.authorization_request, request_id=source)
    duplicate_decision = replace(target.authorization_decision, request_id=source)
    evidence = _replace_evidence(
        evidence,
        target.signal_kind,
        authorization_request=duplicate_request,
        authorization_decision=duplicate_decision,
    )

    result = project_assurance_signals(
        _candidate(), observations, evidence, EVALUATED_AT
    )

    assert result.outcome is AssuranceSignalProjectionOutcome.DENIED
    assert (
        result.reason_code
        is AssuranceSignalProjectionReason.DUPLICATE_AUTHORIZATION_REQUEST_ID
    )


def test_all_input_permutations_preserve_ready_semantics() -> None:
    observations, evidence = _material()
    baseline = project_assurance_signals(
        _candidate(), observations, evidence, EVALUATED_AT
    )
    assert baseline.outcome is AssuranceSignalProjectionOutcome.READY

    for observation_order in permutations(observations):
        for evidence_order in permutations(evidence):
            result = project_assurance_signals(
                _candidate(), observation_order, evidence_order, EVALUATED_AT
            )
            assert result.outcome is baseline.outcome
            assert result.reason_code is baseline.reason_code
            assert result.projected_input == baseline.projected_input


@pytest.mark.parametrize(
    "bad_candidate,bad_observations,bad_evidence",
    [
        (object(), (), ()),
        (_candidate(), [], ()),
        (_candidate(), (), []),
        (_candidate(), (item for item in ()), ()),
        (_candidate(), (), (item for item in ())),
    ],
)
def test_invalid_top_level_contract_fails_safe(
    bad_candidate: object,
    bad_observations: object,
    bad_evidence: object,
) -> None:
    with pytest.raises(TypeError):
        project_assurance_signals(
            bad_candidate,  # type: ignore[arg-type]
            bad_observations,  # type: ignore[arg-type]
            bad_evidence,  # type: ignore[arg-type]
            EVALUATED_AT,
        )


def test_non_utc_evaluated_at_fails_safe() -> None:
    observations, evidence = _material()
    local_time = EVALUATED_AT.astimezone(timezone(timedelta(hours=-3)))

    with pytest.raises(ValueError, match="evaluated_at must be UTC"):
        project_assurance_signals(_candidate(), observations, evidence, local_time)


def test_non_utc_authorization_request_time_fails_safe() -> None:
    observations, evidence = _material()
    target = evidence[0]
    local_time = target.authorization_request.created_at.astimezone(
        timezone(timedelta(hours=-3))
    )
    evidence = _replace_evidence(
        evidence,
        target.signal_kind,
        authorization_request=replace(
            target.authorization_request,
            created_at=local_time,
        ),
    )

    with pytest.raises(ValueError, match="authorization_request.created_at must be UTC"):
        project_assurance_signals(
            _candidate(), observations, evidence, EVALUATED_AT
        )


def test_cardinality_above_maximum_denies() -> None:
    observations, evidence = _material()

    result = project_assurance_signals(
        _candidate(), observations + (observations[0],), evidence, EVALUATED_AT
    )

    assert result.outcome is AssuranceSignalProjectionOutcome.DENIED
    assert result.reason_code is AssuranceSignalProjectionReason.INPUT_CARDINALITY_EXCEEDED


def test_duplicate_signal_denies_before_missing_checks() -> None:
    observations, evidence = _material()
    duplicated = observations[:-1] + (observations[0],)

    result = project_assurance_signals(
        _candidate(), duplicated, evidence, EVALUATED_AT
    )

    assert result.reason_code is AssuranceSignalProjectionReason.DUPLICATE_SIGNAL


def test_duplicate_authorization_evidence_denies() -> None:
    observations, evidence = _material()
    duplicated = evidence[:-1] + (evidence[0],)

    result = project_assurance_signals(
        _candidate(), observations, duplicated, EVALUATED_AT
    )

    assert (
        result.reason_code
        is AssuranceSignalProjectionReason.DUPLICATE_AUTHORIZATION_EVIDENCE
    )


def test_observation_request_and_session_mismatch_are_denied_canonically() -> None:
    observations, evidence = _material()
    observations = _replace_observation(
        observations,
        AssuranceSignalKind.APPLICABILITY,
        request_id="other-request",
        session_id="other-session",
    )

    result = project_assurance_signals(
        _candidate(), observations, evidence, EVALUATED_AT
    )

    assert result.reason_code is AssuranceSignalProjectionReason.REQUEST_ID_MISMATCH


def test_session_mismatch_denies() -> None:
    observations, evidence = _material()
    evidence = _replace_evidence(
        evidence,
        AssuranceSignalKind.APPLICABILITY,
        session_id="other-session",
    )

    result = project_assurance_signals(
        _candidate(), observations, evidence, EVALUATED_AT
    )

    assert result.reason_code is AssuranceSignalProjectionReason.SESSION_ID_MISMATCH


def test_signal_kind_mismatch_denies() -> None:
    observations, evidence = _material()
    target = evidence[0]
    evidence = _replace_evidence(
        evidence,
        target.signal_kind,
        signal_kind=AssuranceSignalKind.EVIDENCE_REQUIRED,
    )

    result = project_assurance_signals(
        _candidate(), observations, evidence, EVALUATED_AT
    )

    assert result.reason_code is AssuranceSignalProjectionReason.DUPLICATE_AUTHORIZATION_EVIDENCE


def test_signal_value_mismatch_denies() -> None:
    observations, evidence = _material()
    evidence = _replace_evidence(
        evidence,
        AssuranceSignalKind.SUPPORT_SUFFICIENT,
        canonical_value="false",
    )

    result = project_assurance_signals(
        _candidate(), observations, evidence, EVALUATED_AT
    )

    assert result.reason_code is AssuranceSignalProjectionReason.SIGNAL_VALUE_MISMATCH


def test_invalid_bool_value_denies_without_coercion() -> None:
    observations, evidence = _material()
    observations = _replace_observation(
        observations,
        AssuranceSignalKind.SUPPORT_SUFFICIENT,
        value=1,
    )

    result = project_assurance_signals(
        _candidate(), observations, evidence, EVALUATED_AT
    )

    assert result.reason_code is AssuranceSignalProjectionReason.SIGNAL_VALUE_INVALID


def test_producer_subject_mismatch_denies() -> None:
    observations, evidence = _material()
    evidence = _replace_evidence(
        evidence,
        AssuranceSignalKind.SUPPORT_SUFFICIENT,
        producer_subject_id="other-subject",
    )

    result = project_assurance_signals(
        _candidate(), observations, evidence, EVALUATED_AT
    )

    assert result.reason_code is AssuranceSignalProjectionReason.PRODUCER_SUBJECT_MISMATCH


def test_decision_request_mismatch_denies() -> None:
    observations, evidence = _material()
    target = evidence[0]
    evidence = _replace_evidence(
        evidence,
        target.signal_kind,
        authorization_decision=replace(
            target.authorization_decision,
            request_id="other-auth-request",
        ),
    )

    result = project_assurance_signals(
        _candidate(), observations, evidence, EVALUATED_AT
    )

    assert result.reason_code is AssuranceSignalProjectionReason.DECISION_REQUEST_MISMATCH


def test_authorization_request_created_before_context_denies() -> None:
    issued = EVALUATED_AT - timedelta(minutes=10)
    observations, evidence = _material(
        issued_at=issued,
        created_at=issued - timedelta(seconds=1),
    )

    result = project_assurance_signals(
        _candidate(), observations, evidence, EVALUATED_AT
    )

    assert (
        result.reason_code
        is AssuranceSignalProjectionReason.AUTHORIZATION_REQUEST_TIME_INVALID
    )


def test_context_not_yet_valid_denies() -> None:
    issued = EVALUATED_AT + timedelta(minutes=1)
    observations, evidence = _material(
        issued_at=issued,
        expires_at=issued + timedelta(minutes=10),
        created_at=issued,
    )

    result = project_assurance_signals(
        _candidate(), observations, evidence, EVALUATED_AT
    )

    assert result.reason_code is AssuranceSignalProjectionReason.CONTEXT_NOT_YET_VALID


def test_context_expired_denies() -> None:
    observations, evidence = _material(
        issued_at=EVALUATED_AT - timedelta(minutes=20),
        expires_at=EVALUATED_AT,
        created_at=EVALUATED_AT - timedelta(minutes=10),
    )

    result = project_assurance_signals(
        _candidate(), observations, evidence, EVALUATED_AT
    )

    assert result.reason_code is AssuranceSignalProjectionReason.CONTEXT_EXPIRED


def test_authorization_denied_is_not_mapped_to_policy_violation() -> None:
    observations, evidence = _material(allowed=False)

    result = project_assurance_signals(
        _candidate(), observations, evidence, EVALUATED_AT
    )

    assert result.outcome is AssuranceSignalProjectionOutcome.DENIED
    assert result.reason_code is AssuranceSignalProjectionReason.AUTHORIZATION_DENIED
    assert result.projected_input is None


def test_unknown_signal_policy_version_denies() -> None:
    observations, evidence = _material(signal_policy_version="future/v2")

    result = project_assurance_signals(
        _candidate(), observations, evidence, EVALUATED_AT
    )

    assert (
        result.reason_code
        is AssuranceSignalProjectionReason.SIGNAL_POLICY_VERSION_MISMATCH
    )


@pytest.mark.parametrize(
    "changes",
    [
        {AssuranceSignalKind.EVIDENCE_REQUIRED: True},
        {AssuranceSignalKind.SUPPORT_SUFFICIENT: True},
        {AssuranceSignalKind.CONTRADICTION_UNRESOLVED: True},
    ],
)
def test_not_applicable_noncanonical_shapes_deny(
    changes: dict[AssuranceSignalKind, object],
) -> None:
    values = _default_values()
    values.update(
        {
            AssuranceSignalKind.APPLICABILITY: AssuranceApplicability.NOT_APPLICABLE,
            AssuranceSignalKind.EVIDENCE_REQUIRED: False,
            AssuranceSignalKind.SUPPORT_SUFFICIENT: False,
            AssuranceSignalKind.CONTRADICTION_UNRESOLVED: False,
        }
    )
    values.update(changes)
    observations, evidence = _material(values=values)

    result = project_assurance_signals(
        _candidate(), observations, evidence, EVALUATED_AT
    )

    assert result.reason_code is AssuranceSignalProjectionReason.SIGNAL_SET_INCOHERENT
