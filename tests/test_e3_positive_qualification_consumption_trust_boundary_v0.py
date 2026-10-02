from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timedelta, timezone
import importlib
import inspect

import pytest

from malak.security.clock import Clock
from malak.security.context_validator import SecurityContextValidator
from malak.security.contracts import (
    AuthorizationDecision,
    AuthorizationOperationBinding,
    PermissionScope,
    SecurityContext,
)
from malak.security.pdp import (
    PolicyEffect,
    PolicyRule,
    StaticPolicyDecisionPoint,
)


POLICY_VERSION = "e3-governed-support-routing/v0"
BASELINE = "b" * 40
EVALUATED_CANDIDATE = "c" * 40
FOCUS_ID = "U01"
RELATION_ID = "U01.CAPABILITY_ROUTING"
QUESTION_ID = "1" * 64
FINDING_FINGERPRINT = "f" * 64
EVIDENCE_DIGEST = "e" * 64
MATERIAL_DIGEST = "2" * 64
INPUT_CONTRACT_DIGEST = "3" * 64
OUTPUT_CONTRACT_DIGEST = "4" * 64
QUALIFICATION_EVIDENCE_DIGEST = "5" * 64
OBLIGATION_CATALOG_DIGEST = "6" * 64
ORACLE_PRODUCER_SUBJECT_ID = "oracle-producer-1"
QUALIFIER_SUBJECT_ID = "oracle-qualifier-1"
REVIEWER_SUBJECT_ID = "qualification-reviewer-1"
ADMITTER_SUBJECT_ID = "qualification-review-admitter-1"
ADMISSION_PERMISSION = PermissionScope(
    resource="engineering.qualification_review_consumption",
    action="admit",
)
NOW = datetime(2026, 10, 2, 20, 0, tzinfo=timezone.utc)


class MutableClock(Clock):
    def __init__(self, current: datetime = NOW) -> None:
        self.current = current

    def now(self) -> datetime:
        return self.current

    def advance(self, delta: timedelta) -> None:
        self.current = self.current + delta


class RecordingPDP:
    def __init__(self, delegate: StaticPolicyDecisionPoint) -> None:
        self.delegate = delegate
        self.calls = []

    def decide(self, request, confirmation=None):
        self.calls.append((request, confirmation))
        return self.delegate.decide(request, confirmation)


class TamperingPDP(RecordingPDP):
    def decide(self, request, confirmation=None):
        decision = super().decide(request, confirmation)
        return AuthorizationDecision(
            request_id=decision.request_id,
            allowed=True,
            reason="policy_allowed",
            operation_binding=AuthorizationOperationBinding(
                namespace="engineering.qualification_review_consumption",
                binding_version="v0",
                digest_algorithm="sha256",
                digest_hex="0" * 64,
            ),
        )


def _routing_module():
    return importlib.import_module("malak.capabilities._engineering_analysis")


def _trust_module_optional():
    try:
        return importlib.import_module(
            "malak.capabilities._engineering_qualification_consumption"
        )
    except ModuleNotFoundError:
        return None


def _trust_api(red_id: str):
    try:
        module = importlib.import_module(
            "malak.capabilities._engineering_qualification_consumption"
        )
    except ModuleNotFoundError:
        pytest.fail(
            f"RED {red_id}: positive qualification consumption boundary is not implemented"
        )
    for name in (
        "GovernedQualificationReviewEvidenceV0",
        "GovernedQualificationReviewAdmissionV0",
        "GovernedQualificationReviewAdmissionOutcome",
        "GovernedQualificationConsumptionBoundaryV0",
        "admit_governed_qualification_review_v0",
    ):
        assert hasattr(module, name), f"RED {red_id}: missing trust-boundary API {name}"
    return module


def _qualification(module, **changes):
    values = {
        "oracle_id": "oracle-1",
        "oracle_version": "v1",
        "oracle_content_digest": "a" * 64,
        "relation_id": RELATION_ID,
        "evaluation_question_identity": QUESTION_ID,
        "input_contract_identity": INPUT_CONTRACT_DIGEST,
        "output_contract_identity": OUTPUT_CONTRACT_DIGEST,
        "coverage_claim": "FULL",
        "oracle_producer_subject_id": ORACLE_PRODUCER_SUBJECT_ID,
        "qualifier_subject_id": QUALIFIER_SUBJECT_ID,
        "qualification_evidence_digest": QUALIFICATION_EVIDENCE_DIGEST,
        "authority_effect": "none",
    }
    values.update(changes)
    return module.GovernedDeterministicOracleQualificationV0(**values)


def _oracle(module, **changes):
    qualification = changes.pop("qualification", None)
    qualification_identity = changes.pop("qualification_identity", None)
    values = {
        "oracle_id": "oracle-1",
        "oracle_version": "v1",
        "oracle_content_digest": "a" * 64,
        "relation_id": RELATION_ID,
        "evaluation_question_identity": QUESTION_ID,
        "input_contract_identity": INPUT_CONTRACT_DIGEST,
        "output_contract_identity": OUTPUT_CONTRACT_DIGEST,
        "coverage_claim": "FULL",
        "oracle_producer_subject_id": ORACLE_PRODUCER_SUBJECT_ID,
        "authority_effect": "none",
        "side_effect_class": "NONE",
    }
    values.update(changes)
    if qualification is None:
        qualification = _qualification(
            module,
            oracle_id=values["oracle_id"],
            oracle_version=values["oracle_version"],
            oracle_content_digest=values["oracle_content_digest"],
            relation_id=values["relation_id"],
            evaluation_question_identity=values[
                "evaluation_question_identity"
            ],
            input_contract_identity=values["input_contract_identity"],
            output_contract_identity=values["output_contract_identity"],
            coverage_claim=values["coverage_claim"],
            oracle_producer_subject_id=values[
                "oracle_producer_subject_id"
            ],
        )
    values["qualification"] = qualification
    values["qualification_identity"] = (
        qualification_identity or qualification.qualification_identity
    )
    return module.GovernedDeterministicOracleContractV0(**values)


def _routing_values(oracles=()):
    return {
        "policy_version": POLICY_VERSION,
        "baseline_commit": BASELINE,
        "focus_id": FOCUS_ID,
        "evidence_set_digest": EVIDENCE_DIGEST,
        "relation_id": RELATION_ID,
        "evaluation_question_identity": QUESTION_ID,
        "finding_fingerprint": FINDING_FINGERPRINT,
        "resolved_evidence_material_digest": MATERIAL_DIGEST,
        "declared_evidence_complete": True,
        "scope_expansion_required": False,
        "oracles": oracles,
        "expected_binding": {
            "baseline_commit": BASELINE,
            "focus_id": FOCUS_ID,
            "evidence_set_digest": EVIDENCE_DIGEST,
            "relation_id": RELATION_ID,
            "evaluation_question_identity": QUESTION_ID,
            "finding_fingerprint": FINDING_FINGERPRINT,
            "resolved_evidence_material_digest": MATERIAL_DIGEST,
        },
    }


def _free_route(module, **changes):
    values = _routing_values()
    values.update(changes)
    return module.route_governed_support_evidence_v0(**values)


def _review(api, oracle, **changes):
    q = oracle.qualification
    values = {
        "repository": "Aranwill/jarvis",
        "evaluated_candidate_commit": EVALUATED_CANDIDATE,
        "qualification_identity": q.qualification_identity,
        "qualification_bundle_digest": q.qualification_evidence_digest,
        "reviewed_oracle_id": oracle.oracle_id,
        "reviewed_oracle_version": oracle.oracle_version,
        "reviewed_oracle_content_digest": oracle.oracle_content_digest,
        "reviewed_relation_id": oracle.relation_id,
        "reviewed_evaluation_question_identity": oracle.evaluation_question_identity,
        "reviewed_input_contract_identity": oracle.input_contract_identity,
        "reviewed_output_contract_identity": oracle.output_contract_identity,
        "reviewed_coverage_claim": oracle.coverage_claim,
        "reviewed_oracle_producer_subject_id": oracle.oracle_producer_subject_id,
        "reviewed_obligation_catalog_digest": OBLIGATION_CATALOG_DIGEST,
        "structural_validator_result": "PASS",
        "catalog_completeness_result": "PASS",
        "independence_review_result": "PASS",
        "verification_material_review_result": "PASS",
        "qualification_review_result": "PASS",
        "reviewer_subject_id": REVIEWER_SUBJECT_ID,
        "evidence_references": (
            "pr-review://242/exact-candidate",
            "validator-artifact://qualification-v0",
        ),
        "authority_effect": "none",
    }
    values.update(changes)
    return api.GovernedQualificationReviewEvidenceV0(**values)


def _context(
    *,
    authenticated: bool = True,
    issued_at: datetime | None = None,
    expires_at: datetime | None = None,
):
    return SecurityContext(
        context_id="qualification-admission-context-1",
        session_id="qualification-admission-session-1",
        subject_id=ADMITTER_SUBJECT_ID,
        authenticated=authenticated,
        issued_at=issued_at or NOW - timedelta(minutes=5),
        expires_at=expires_at or NOW + timedelta(minutes=30),
    )


def _recording_pdp(
    clock: MutableClock,
    *,
    effect: PolicyEffect = PolicyEffect.ALLOW,
    permission: PermissionScope = ADMISSION_PERMISSION,
):
    delegate = StaticPolicyDecisionPoint(
        [
            PolicyRule(
                subject_id=ADMITTER_SUBJECT_ID,
                permission=permission,
                effect=effect,
            )
        ],
        context_validator=SecurityContextValidator(clock),
    )
    return RecordingPDP(delegate)


def _admit(
    api,
    *,
    oracle,
    review=None,
    clock=None,
    context=None,
    pdp=None,
):
    clock = clock or MutableClock()
    context = context or _context()
    pdp = pdp or _recording_pdp(clock)
    review = review or _review(api, oracle)
    admission = api.admit_governed_qualification_review_v0(
        review=review,
        oracle=oracle,
        routing_baseline_commit=BASELINE,
        authorization_context=context,
        policy_decision_point=pdp,
        clock=clock,
    )
    return admission, clock, pdp


def _boundary(api, admissions, clock):
    return api.GovernedQualificationConsumptionBoundaryV0(
        admissions=tuple(admissions),
        clock=clock,
    )


def _boundary_route(boundary, oracles):
    return boundary.route(**_routing_values(oracles=oracles))


def _value(value):
    return getattr(value, "value", value)


def _assert_not_deterministic(result):
    assert _value(result.route_kind) != "DETERMINISTIC"


def test_pqctb_r01_caller_only_full_qualification_is_not_deterministic() -> None:
    module = _routing_module()
    result = _free_route(module, oracles=(_oracle(module),))
    assert _value(result.route_kind) == "INFERENTIAL"


def test_pqctb_r02_free_route_exposes_no_review_evidence_input() -> None:
    module = _routing_module()
    signature = inspect.signature(module.route_governed_support_evidence_v0)
    forbidden = {
        "review",
        "review_evidence",
        "qualification_review_evidence",
        "admission",
    }
    assert forbidden.isdisjoint(signature.parameters)


def test_pqctb_r03_request_cannot_supply_or_replace_trust_configuration() -> None:
    module = _routing_module()
    signature = inspect.signature(module.route_governed_support_evidence_v0)
    forbidden = {
        "admission_factory",
        "security_context",
        "authorization_request",
        "authorization_decision",
        "human_confirmation",
        "clock",
        "boundary",
        "configuration",
        "policy_decision_point",
    }
    assert forbidden.isdisjoint(signature.parameters)


def test_pqctb_r04_missing_composition_admission_remains_inferential() -> None:
    module = _routing_module()
    result = _free_route(module, oracles=(_oracle(module),))
    assert _value(result.route_kind) == "INFERENTIAL"
    assert _value(result.reason_code) == "INFERENTIAL_RESIDUAL"


@pytest.mark.parametrize(
    ("red_id", "review_changes"),
    [
        ("PQCTB-R05", {"repository": "Other/repository"}),
        ("PQCTB-R06", {"evaluated_candidate_commit": "d" * 40}),
        ("PQCTB-R07", {"qualification_identity": "7" * 64}),
        ("PQCTB-R08", {"reviewed_oracle_content_digest": "8" * 64}),
        ("PQCTB-R09", {"reviewed_relation_id": "OTHER.RELATION"}),
        ("PQCTB-R10", {"reviewed_obligation_catalog_digest": "9" * 64}),
    ],
)
def test_pqctb_r05_r10_binding_mismatches_cannot_route_deterministic(
    red_id: str,
    review_changes: dict,
) -> None:
    api = _trust_api(red_id)
    module = _routing_module()
    oracle = _oracle(module)
    review = _review(api, oracle, **review_changes)
    admission, clock, _ = _admit(api, oracle=oracle, review=review)
    boundary = _boundary(api, (admission,), clock)
    result = _boundary_route(boundary, (oracle,))
    _assert_not_deterministic(result)


@pytest.mark.parametrize("completeness", ["FAIL", "INCONCLUSIVE"])
def test_pqctb_r11_catalog_completeness_alone_blocks_ready_and_deterministic(
    completeness: str,
) -> None:
    api = _trust_api("PQCTB-R11")
    module = _routing_module()
    oracle = _oracle(module)
    review = _review(
        api,
        oracle,
        catalog_completeness_result=completeness,
    )
    admission, clock, _ = _admit(api, oracle=oracle, review=review)
    assert _value(admission.outcome) != "READY"
    boundary = _boundary(api, (admission,), clock)
    _assert_not_deterministic(_boundary_route(boundary, (oracle,)))


@pytest.mark.parametrize(
    ("red_id", "field"),
    [
        ("PQCTB-R12", "structural_validator_result"),
        ("PQCTB-R13", "independence_review_result"),
        ("PQCTB-R14", "verification_material_review_result"),
        ("PQCTB-R15", "qualification_review_result"),
    ],
)
@pytest.mark.parametrize("terminal", ["FAIL", "INCONCLUSIVE"])
def test_pqctb_r12_r15_required_review_dimension_blocks_positive_route(
    red_id: str,
    field: str,
    terminal: str,
) -> None:
    api = _trust_api(red_id)
    module = _routing_module()
    oracle = _oracle(module)
    review = _review(api, oracle, **{field: terminal})
    admission, clock, _ = _admit(api, oracle=oracle, review=review)
    assert _value(admission.outcome) != "READY"
    boundary = _boundary(api, (admission,), clock)
    _assert_not_deterministic(_boundary_route(boundary, (oracle,)))


def test_pqctb_r16_missing_configured_authorization_cannot_admit() -> None:
    api = _trust_api("PQCTB-R16")
    module = _routing_module()
    oracle = _oracle(module)
    review = _review(api, oracle)
    with pytest.raises((TypeError, ValueError)):
        api.admit_governed_qualification_review_v0(
            review=review,
            oracle=oracle,
            routing_baseline_commit=BASELINE,
            authorization_context=_context(),
            policy_decision_point=None,
            clock=MutableClock(),
        )


def test_pqctb_r17_denied_authorization_cannot_admit_ready() -> None:
    api = _trust_api("PQCTB-R17")
    module = _routing_module()
    oracle = _oracle(module)
    clock = MutableClock()
    pdp = _recording_pdp(clock, effect=PolicyEffect.DENY)
    admission, _, recording = _admit(
        api,
        oracle=oracle,
        clock=clock,
        pdp=pdp,
    )
    assert len(recording.calls) == 1
    assert _value(admission.outcome) != "READY"


def test_pqctb_r18_permission_mismatch_cannot_admit_ready() -> None:
    api = _trust_api("PQCTB-R18")
    module = _routing_module()
    oracle = _oracle(module)
    clock = MutableClock()
    wrong_permission = PermissionScope(
        resource="engineering.qualification_review_consumption",
        action="read",
    )
    pdp = _recording_pdp(clock, permission=wrong_permission)
    admission, _, recording = _admit(
        api,
        oracle=oracle,
        clock=clock,
        pdp=pdp,
    )
    assert len(recording.calls) == 1
    assert _value(admission.outcome) != "READY"


def test_pqctb_r19_operation_binding_tamper_cannot_admit_ready() -> None:
    api = _trust_api("PQCTB-R19")
    module = _routing_module()
    oracle = _oracle(module)
    clock = MutableClock()
    delegate = _recording_pdp(clock).delegate
    pdp = TamperingPDP(delegate)
    admission, _, recording = _admit(
        api,
        oracle=oracle,
        clock=clock,
        pdp=pdp,
    )
    assert len(recording.calls) == 1
    assert _value(admission.outcome) != "READY"


def test_pqctb_r20_context_invalid_at_admission_cannot_be_ready() -> None:
    api = _trust_api("PQCTB-R20")
    module = _routing_module()
    oracle = _oracle(module)
    clock = MutableClock()
    expired = _context(
        issued_at=NOW - timedelta(hours=2),
        expires_at=NOW - timedelta(hours=1),
    )
    pdp = _recording_pdp(clock)
    admission, _, _ = _admit(
        api,
        oracle=oracle,
        clock=clock,
        context=expired,
        pdp=pdp,
    )
    assert _value(admission.outcome) != "READY"


def test_pqctb_r21_ready_admission_expires_before_consumption() -> None:
    api = _trust_api("PQCTB-R21")
    module = _routing_module()
    oracle = _oracle(module)
    clock = MutableClock()
    context = _context(expires_at=NOW + timedelta(minutes=5))
    admission, _, _ = _admit(
        api,
        oracle=oracle,
        clock=clock,
        context=context,
    )
    assert _value(admission.outcome) == "READY"
    boundary = _boundary(api, (admission,), clock)
    clock.advance(timedelta(minutes=6))
    result = _boundary_route(boundary, (oracle,))
    _assert_not_deterministic(result)
    assert _value(result.reason_code) == "ADMISSION_STALE"


def test_pqctb_r22_duplicate_ready_admissions_fail_closed() -> None:
    api = _trust_api("PQCTB-R22")
    module = _routing_module()
    oracle = _oracle(module)
    first, clock, _ = _admit(api, oracle=oracle)
    second, _, _ = _admit(api, oracle=oracle, clock=clock)
    assert _value(first.outcome) == "READY"
    assert _value(second.outcome) == "READY"
    boundary = _boundary(api, (first, second), clock)
    result = _boundary_route(boundary, (oracle,))
    _assert_not_deterministic(result)


def test_pqctb_r23_ambiguous_full_oracles_preserve_existing_fail_closed_reason() -> None:
    module = _routing_module()
    oracle_1 = _oracle(module)
    oracle_2 = _oracle(
        module,
        oracle_id="oracle-2",
        oracle_content_digest="d" * 64,
    )
    result = _free_route(module, oracles=(oracle_1, oracle_2))
    assert _value(result.reason_code) == "ORACLE_AMBIGUOUS"
    assert _value(result.route_kind) != "DETERMINISTIC"


def test_pqctb_r24_governed_configuration_exact_ready_and_full_can_route_deterministic() -> None:
    api = _trust_api("PQCTB-R24")
    module = _routing_module()
    oracle = _oracle(module)
    admission, clock, pdp = _admit(api, oracle=oracle)
    assert len(pdp.calls) == 1
    assert _value(admission.outcome) == "READY"
    boundary = _boundary(api, (admission,), clock)
    result = _boundary_route(boundary, (oracle,))
    assert _value(result.route_kind) == "DETERMINISTIC"


def test_pqctb_r25_positive_route_reports_selected_exact_oracle_id() -> None:
    api = _trust_api("PQCTB-R25")
    module = _routing_module()
    oracle = _oracle(module)
    admission, clock, _ = _admit(api, oracle=oracle)
    boundary = _boundary(api, (admission,), clock)
    result = _boundary_route(boundary, (oracle,))
    assert _value(result.route_kind) == "DETERMINISTIC"
    assert result.selected_oracle_id == oracle.oracle_id


def test_pqctb_r26_authority_effect_other_than_none_is_rejected() -> None:
    module = _routing_module()
    with pytest.raises((TypeError, ValueError)):
        _oracle(module, authority_effect="allow")


def test_pqctb_r27_scope_guards_remain_zero_and_no_runtime_callbacks_enter_route() -> None:
    module = _routing_module()
    signature = inspect.signature(module.route_governed_support_evidence_v0)
    forbidden = {
        "kernel",
        "planner",
        "model",
        "provider",
        "runtime",
        "network",
        "store",
        "registry",
        "rdd_stage_2",
        "support_sufficient",
    }
    assert forbidden.isdisjoint(signature.parameters)


def test_pqctb_r28_existing_p01_p09_structural_routing_semantics_remain_regression_equivalent() -> None:
    module = _routing_module()
    policy_mismatch = _free_route(module, policy_version="unknown-policy")
    assert _value(policy_mismatch.reason_code) == "POLICY_VERSION_MISMATCH"

    wrong_binding = _routing_values()
    wrong_binding["expected_binding"] = dict(wrong_binding["expected_binding"])
    wrong_binding["expected_binding"]["focus_id"] = "OTHER"
    subject_mismatch = module.route_governed_support_evidence_v0(**wrong_binding)
    assert _value(subject_mismatch.reason_code) == "SUBJECT_BINDING_MISMATCH"


def test_pqctb_r29_request_facing_signatures_expose_no_trust_inputs() -> None:
    module = _routing_module()
    signatures = [inspect.signature(module.route_governed_support_evidence_v0)]
    trust_module = _trust_module_optional()
    if trust_module is not None and hasattr(
        trust_module,
        "GovernedQualificationConsumptionBoundaryV0",
    ):
        signatures.append(
            inspect.signature(
                trust_module.GovernedQualificationConsumptionBoundaryV0.route
            )
        )
    forbidden = {
        "review",
        "review_evidence",
        "authorization_request",
        "authorization_decision",
        "security_context",
        "human_confirmation",
        "admission",
        "clock",
        "consume_at",
        "policy_decision_point",
        "factory",
        "configuration",
    }
    for signature in signatures:
        assert forbidden.isdisjoint(signature.parameters)


def test_pqctb_r30_rdd_or_review_references_are_not_runtime_credentials() -> None:
    module = _routing_module()
    signature = inspect.signature(module.route_governed_support_evidence_v0)
    forbidden = {
        "rdd_manifest",
        "rdd_receipt",
        "review_reference",
        "validator_reference",
        "evidence_reference",
        "approval",
    }
    assert forbidden.isdisjoint(signature.parameters)


def test_pqctb_r31_material_or_candidate_drift_invalidates_prior_admission() -> None:
    api = _trust_api("PQCTB-R31")
    module = _routing_module()
    original = _oracle(module)
    admission, clock, _ = _admit(api, oracle=original)
    assert _value(admission.outcome) == "READY"

    drifted_qualification = _qualification(
        module,
        oracle_content_digest="d" * 64,
    )
    drifted = _oracle(
        module,
        oracle_content_digest="d" * 64,
        qualification=drifted_qualification,
    )
    boundary = _boundary(api, (admission,), clock)
    result = _boundary_route(boundary, (drifted,))
    _assert_not_deterministic(result)
