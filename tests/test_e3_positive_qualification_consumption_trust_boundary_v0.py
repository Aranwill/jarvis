from __future__ import annotations

import copy
import dataclasses
from datetime import datetime, timedelta, timezone
import hashlib
import importlib
import inspect
import json
from pathlib import Path

import pytest

from malak.security.audit import (
    AuthorizationAuditOutcome,
    InMemoryAuthorizationAuditStore,
)
from malak.security.clock import Clock
from malak.security.context_validator import SecurityContextValidator
from malak.security.contracts import (
    AuthorizationDecision,
    AuthorizationOperationBinding,
    AuthorizationRequest,
    PermissionScope,
    SecurityContext,
)
from malak.security.pdp import (
    PolicyEffect,
    PolicyRule,
    StaticPolicyDecisionPoint,
)
from malak.security.pep import (
    AuthorizationEnforcementError,
    StrictPolicyEnforcementPoint,
)


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts" / "evaluate_e3_deterministic_oracle_qualification.py"

REPOSITORY = "Aranwill/jarvis"
CANDIDATE = "c" * 40
OTHER_CANDIDATE = "d" * 40
POLICY_VERSION = "e3-governed-support-routing/v0"
FOCUS_ID = "U01"
RELATION_ID = "U01.CAPABILITY_ROUTING"
QUESTION_ID = "1" * 64
FINDING_FINGERPRINT = "f" * 64
EVIDENCE_DIGEST = "e" * 64
MATERIAL_DIGEST = "2" * 64
INPUT_CONTRACT_DIGEST = "3" * 64
OUTPUT_CONTRACT_DIGEST = "4" * 64
ORACLE_CONTENT_DIGEST = "a" * 64
ORACLE_PRODUCER_SUBJECT_ID = "oracle-producer-1"
REVIEWER_SUBJECT_ID = "qualification-reviewer-1"
IMPLEMENTATION_ACTOR_ID = "implementation-actor-1"
VALIDATOR_SUBJECT_ID = "qualification-validator-1"
ADMITTER_SUBJECT_ID = "qualification-admitter-1"

BUNDLE_SCHEMA = "MALAK-E3-DETERMINISTIC-ORACLE-QUALIFICATION-BUNDLE/v0"
REVIEW_SCHEMA = "MALAK-E3-DETERMINISTIC-ORACLE-QUALIFICATION-REVIEW-EVIDENCE/v0"

ADMISSION_PERMISSION = PermissionScope(
    resource="engineering.qualification_review_consumption",
    action="admit",
)

NOW = datetime(2026, 10, 3, 20, 0, tzinfo=timezone.utc)


class MutableClock(Clock):
    def __init__(self, current: datetime = NOW) -> None:
        self.current = current
        self.mode = "normal"
        self.calls = 0

    def now(self):
        self.calls += 1
        if self.mode == "raise":
            raise RuntimeError("clock unavailable")
        if self.mode == "naive":
            return self.current.replace(tzinfo=None)
        if self.mode == "non_datetime":
            return "not-a-datetime"
        return self.current


class SequenceClock(Clock):
    def __init__(self, values: list[datetime]) -> None:
        self._values = list(values)
        self._last = values[-1]
        self.calls = 0

    def now(self) -> datetime:
        self.calls += 1
        if self._values:
            self._last = self._values.pop(0)
        return self._last


class EventClock(MutableClock):
    def __init__(self, events: list[str], current: datetime = NOW) -> None:
        super().__init__(current)
        self.events = events

    def now(self):
        self.events.append("clock_now")
        return super().now()


class EventOracleList(list):
    def __init__(self, values, events: list[str], *, on_iter=None) -> None:
        super().__init__(values)
        self.events = events
        self.on_iter = on_iter

    def __iter__(self):
        self.events.append("oracles_iter")
        if self.on_iter is not None:
            self.on_iter()
        return super().__iter__()


class RecordingPDP:
    def __init__(self, delegate: StaticPolicyDecisionPoint) -> None:
        self.delegate = delegate
        self.calls: list[tuple[AuthorizationRequest, object]] = []

    def decide(self, request, confirmation=None):
        self.calls.append((request, confirmation))
        return self.delegate.decide(request, confirmation)


class DecisionBindingTamperingPDP(RecordingPDP):
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


class ProbeOperation:
    def __init__(
        self,
        *,
        permission: PermissionScope = ADMISSION_PERMISSION,
        binding: AuthorizationOperationBinding,
    ) -> None:
        self.required_permission = permission
        self.authorization_binding = binding
        self.execute_count = 0

    def execute(self):
        self.execute_count += 1
        return "executed"


def _canonical_json(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _sha256(value: object) -> str:
    return hashlib.sha256(_canonical_json(value)).hexdigest()


def _runner_digest() -> str:
    return hashlib.sha256(RUNNER.read_bytes()).hexdigest()


def _obligation(obligation_id: str, statement: str) -> dict[str, str]:
    return {
        "obligation_id": obligation_id,
        "obligation_statement": statement,
        "obligation_identity": _sha256(
            {
                "relation_id": RELATION_ID,
                "evaluation_question_identity": QUESTION_ID,
                "obligation_id": obligation_id,
                "obligation_statement": statement,
            }
        ),
    }


def _catalog() -> list[dict[str, str]]:
    return [
        _obligation(
            "O01",
            "The selected qualification must remain exactly bound to admitted evidence.",
        ),
        _obligation(
            "O02",
            "Positive deterministic routing must remain fail-closed under ambiguity.",
        ),
    ]


def _coverage_entry(
    obligation: dict[str, str],
    *,
    index: int,
) -> dict[str, object]:
    evidence_ref = f"evidence:CHECK-{index:02d}"
    return {
        "obligation_id": obligation["obligation_id"],
        "obligation_identity": obligation["obligation_identity"],
        "oracle_check_id": f"CHECK-{index:02d}",
        "oracle_check_identity": _sha256(
            {
                "oracle_id": "oracle-1",
                "oracle_version": "v1",
                "check_id": f"CHECK-{index:02d}",
            }
        ),
        "oracle_check_contract_digest": _sha256(
            {
                "check_id": f"CHECK-{index:02d}",
                "input_contract_identity": INPUT_CONTRACT_DIGEST,
                "output_contract_identity": OUTPUT_CONTRACT_DIGEST,
            }
        ),
        "verification_evidence_refs": [evidence_ref],
        "entry_result": "PASS",
        "entry_reasons": [],
    }


def _verification_evidence(
    evidence_id: str,
    *,
    candidate: str = CANDIDATE,
) -> dict[str, object]:
    material = {"evidence_id": evidence_id, "observed": True}
    return {
        "evidence_id": evidence_id,
        "evidence_kind": "BOUNDED_DETERMINISTIC_CHECK_OUTPUT",
        "content_digest": _sha256(material),
        "content_or_bounded_material": material,
        "candidate_binding": candidate,
    }


def _qualification_bundle(
    *,
    repository: str = REPOSITORY,
    candidate: str = CANDIDATE,
    oracle_id: str = "oracle-1",
    oracle_version: str = "v1",
    oracle_content_digest: str = ORACLE_CONTENT_DIGEST,
    oracle_producer_subject_id: str = ORACLE_PRODUCER_SUBJECT_ID,
    relation_id: str = RELATION_ID,
    question_id: str = QUESTION_ID,
    input_contract_identity: str = INPUT_CONTRACT_DIGEST,
    output_contract_identity: str = OUTPUT_CONTRACT_DIGEST,
) -> dict[str, object]:
    obligations = _catalog()
    coverage = [
        _coverage_entry(obligation, index=index)
        for index, obligation in enumerate(obligations, start=1)
    ]
    evidence = [
        _verification_evidence(
            str(entry["verification_evidence_refs"][0]),
            candidate=candidate,
        )
        for entry in coverage
    ]
    qualification_material = {
        "qualification_method": "INDEPENDENT_REVIEWED_DETERMINISTIC_COVERAGE",
        "executing_runner_version": "e3-deterministic-oracle-qualification/v0",
        "executing_runner_digest": _runner_digest(),
    }
    return {
        "schema_version": BUNDLE_SCHEMA,
        "repository": repository,
        "evaluated_candidate_commit": candidate,
        "oracle_identity": {
            "oracle_id": oracle_id,
            "oracle_version": oracle_version,
            "oracle_content_digest": oracle_content_digest,
            "oracle_producer_subject_id": oracle_producer_subject_id,
        },
        "governed_question_material": {
            "relation_id": relation_id,
            "evaluation_question_identity": question_id,
            "input_contract_identity": input_contract_identity,
            "output_contract_identity": output_contract_identity,
        },
        "obligation_catalog": obligations,
        "obligation_catalog_digest": _sha256(obligations),
        "coverage_entries": coverage,
        "verification_evidence": evidence,
        "verification_evidence_digest": _sha256(evidence),
        "qualification_material": qualification_material,
        "qualification_material_digest": _sha256(qualification_material),
    }


def _bundle_digest(bundle: dict[str, object]) -> str:
    return _sha256(bundle)


def _review_evidence(
    bundle: dict[str, object],
    *,
    implementation_actor_id: str = IMPLEMENTATION_ACTOR_ID,
    reviewer_id: str = REVIEWER_SUBJECT_ID,
    validator_id: str = VALIDATOR_SUBJECT_ID,
    structural: str = "PASS",
    catalog: str = "PASS",
    independence: str = "PASS",
    verification: str = "PASS",
    qualification: str = "PASS",
    evidence_references: list[str] | None = None,
    authority_effect: str = "none",
) -> dict[str, object]:
    question = bundle["governed_question_material"]
    assert isinstance(question, dict)
    return {
        "schema_version": REVIEW_SCHEMA,
        "repository": bundle["repository"],
        "evaluated_candidate_commit": bundle["evaluated_candidate_commit"],
        "qualification_bundle_digest": _bundle_digest(bundle),
        "reviewed_relation_id": question["relation_id"],
        "reviewed_evaluation_question_identity": question[
            "evaluation_question_identity"
        ],
        "reviewed_obligation_catalog_digest": bundle["obligation_catalog_digest"],
        "implementation_actor_id": implementation_actor_id,
        "qualification_reviewer_id": reviewer_id,
        "qualification_validator_id": validator_id,
        "structural_validator_result": structural,
        "structural_validator_evidence_reference": "external:structural-validation",
        "catalog_completeness_result": catalog,
        "independence_review_result": independence,
        "verification_material_review_result": verification,
        "qualification_review_result": qualification,
        "finding_refs": [],
        "evidence_references": (
            evidence_references
            if evidence_references is not None
            else ["external:review-evidence"]
        ),
        "authority_effect": authority_effect,
    }


def _routing_module():
    return importlib.import_module("malak.capabilities._engineering_analysis")


def _trust_api(red_id: str):
    module = None
    for module_name in (
        "malak.capabilities._engineering_qualification_consumption",
        "malak.capabilities._engineering_analysis",
    ):
        try:
            candidate = importlib.import_module(module_name)
        except ModuleNotFoundError as error:
            if error.name != module_name:
                raise
            continue
        if hasattr(candidate, "GovernedQualificationConsumptionBoundaryV0"):
            module = candidate
            break
    if module is None:
        pytest.fail(
            f"RED {red_id}: positive qualification consumption boundary is not implemented"
        )
    required = (
        "GovernedQualificationReviewAdmissionOperationV0",
        "GovernedQualificationReviewAdmissionV0",
        "GovernedQualificationReviewAdmissionOutcome",
        "GovernedQualificationConsumptionBoundaryV0",
        "RuntimeQualificationBindingV0",
        "RuntimeQualificationBindingKeyV0",
        "AdmissionInstanceKeyV0",
    )
    for name in required:
        assert hasattr(module, name), f"RED {red_id}: missing contract {name}"
    return module


def _composition_factory(red_id: str):
    composition = importlib.import_module("malak.app.composition")
    factory = getattr(
        composition,
        "compose_governed_qualification_consumption_boundary_v0",
        None,
    )
    if factory is None:
        trust = _trust_api(red_id)
        factory = getattr(
            trust,
            "compose_governed_qualification_consumption_boundary_v0",
            None,
        )
    assert callable(factory), (
        f"RED {red_id}: composition-owned qualification consumption factory "
        "is not implemented"
    )
    return factory


def _qualification(
    bundle: dict[str, object],
    *,
    reviewer_id: str = REVIEWER_SUBJECT_ID,
    **changes,
):
    module = _routing_module()
    oracle = bundle["oracle_identity"]
    question = bundle["governed_question_material"]
    assert isinstance(oracle, dict)
    assert isinstance(question, dict)
    values = {
        "oracle_id": oracle["oracle_id"],
        "oracle_version": oracle["oracle_version"],
        "oracle_content_digest": oracle["oracle_content_digest"],
        "relation_id": question["relation_id"],
        "evaluation_question_identity": question["evaluation_question_identity"],
        "input_contract_identity": question["input_contract_identity"],
        "output_contract_identity": question["output_contract_identity"],
        "coverage_claim": "FULL",
        "oracle_producer_subject_id": oracle["oracle_producer_subject_id"],
        "qualifier_subject_id": reviewer_id,
        "qualification_evidence_digest": _bundle_digest(bundle),
        "authority_effect": "none",
    }
    values.update(changes)
    return module.GovernedDeterministicOracleQualificationV0(**values)


def _oracle(
    bundle: dict[str, object],
    *,
    qualification=None,
    qualification_identity: str | None = None,
    **changes,
):
    module = _routing_module()
    q = qualification or _qualification(bundle)
    oracle = bundle["oracle_identity"]
    question = bundle["governed_question_material"]
    assert isinstance(oracle, dict)
    assert isinstance(question, dict)
    values = {
        "oracle_id": oracle["oracle_id"],
        "oracle_version": oracle["oracle_version"],
        "oracle_content_digest": oracle["oracle_content_digest"],
        "relation_id": question["relation_id"],
        "evaluation_question_identity": question["evaluation_question_identity"],
        "input_contract_identity": question["input_contract_identity"],
        "output_contract_identity": question["output_contract_identity"],
        "coverage_claim": "FULL",
        "oracle_producer_subject_id": oracle["oracle_producer_subject_id"],
        "qualification_identity": (
            qualification_identity or q.qualification_identity
        ),
        "qualification": q,
        "authority_effect": "none",
        "side_effect_class": "NONE",
    }
    values.update(changes)
    return module.GovernedDeterministicOracleContractV0(**values)


def _routing_values(oracles=(), *, baseline_commit: str = CANDIDATE):
    return {
        "policy_version": POLICY_VERSION,
        "baseline_commit": baseline_commit,
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
            "baseline_commit": baseline_commit,
            "focus_id": FOCUS_ID,
            "evidence_set_digest": EVIDENCE_DIGEST,
            "relation_id": RELATION_ID,
            "evaluation_question_identity": QUESTION_ID,
            "finding_fingerprint": FINDING_FINGERPRINT,
            "resolved_evidence_material_digest": MATERIAL_DIGEST,
        },
    }


def _free_route(*, oracles=(), **changes):
    values = _routing_values(oracles)
    values.update(changes)
    return _routing_module().route_governed_support_evidence_v0(**values)


def _context(
    *,
    issued_at: datetime = NOW - timedelta(minutes=5),
    expires_at: datetime = NOW + timedelta(minutes=30),
    authenticated: bool = True,
) -> SecurityContext:
    return SecurityContext(
        context_id="qualification-admission-context-1",
        session_id="qualification-admission-session-1",
        subject_id=ADMITTER_SUBJECT_ID,
        authenticated=authenticated,
        issued_at=issued_at,
        expires_at=expires_at,
    )


def _recording_pdp(
    clock: Clock,
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


def _compose(
    red_id: str,
    *,
    bundle: dict[str, object] | None = None,
    review: dict[str, object] | None = None,
    clock: Clock | None = None,
    context: SecurityContext | None = None,
    pdp=None,
    audit=None,
):
    bundle = bundle or _qualification_bundle()
    review = review or _review_evidence(bundle)
    clock = clock or MutableClock()
    context = context or _context()
    pdp = pdp or _recording_pdp(clock)
    audit = audit or InMemoryAuthorizationAuditStore()
    factory = _composition_factory(red_id)
    signature = inspect.signature(factory)
    required = {
        "qualification_bundle",
        "qualification_review_evidence",
        "expected_repository",
        "expected_candidate_commit",
        "security_context",
        "policy_decision_point",
        "authorization_audit_sink",
        "clock",
    }
    assert required.issubset(signature.parameters), (
        f"RED {red_id}: composition factory must own the governed trust inputs"
    )
    boundary = factory(
        qualification_bundle=copy.deepcopy(bundle),
        qualification_review_evidence=copy.deepcopy(review),
        expected_repository=REPOSITORY,
        expected_candidate_commit=CANDIDATE,
        security_context=context,
        policy_decision_point=pdp,
        authorization_audit_sink=audit,
        clock=clock,
    )
    api = _trust_api(red_id)
    assert isinstance(boundary, api.GovernedQualificationConsumptionBoundaryV0)
    return boundary, api, clock, context, pdp, audit


def _admissions(boundary, api):
    admission_type = api.GovernedQualificationReviewAdmissionV0
    values = []
    if dataclasses.is_dataclass(boundary):
        values.extend(getattr(boundary, field.name) for field in dataclasses.fields(boundary))
    else:
        values.extend(
            getattr(boundary, name)
            for name in dir(boundary)
            if not name.startswith("__")
        )

    found = []
    for value in values:
        if isinstance(value, admission_type):
            found.append(value)
        elif isinstance(value, dict):
            found.extend(
                item for item in value.values() if isinstance(item, admission_type)
            )
        elif isinstance(value, (tuple, list, frozenset)):
            found.extend(
                item for item in value if isinstance(item, admission_type)
            )
    return tuple(found)


def _single_admission(boundary, api):
    items = _admissions(boundary, api)
    assert len(items) == 1, "RED: expected exactly one installed admission"
    return items[0]


def _with_admissions(boundary, api, admissions):
    assert dataclasses.is_dataclass(boundary), (
        "RED: ambiguity validation requires immutable dataclass boundary state"
    )
    admission_type = api.GovernedQualificationReviewAdmissionV0
    for field in dataclasses.fields(boundary):
        value = getattr(boundary, field.name)
        if isinstance(value, (tuple, list, frozenset)) and any(
            isinstance(item, admission_type) for item in value
        ):
            return dataclasses.replace(
                boundary,
                **{field.name: tuple(admissions)},
            )
        if isinstance(value, dict) and any(
            isinstance(item, admission_type) for item in value.values()
        ):
            return dataclasses.replace(
                boundary,
                **{
                    field.name: {
                        str(index): admission
                        for index, admission in enumerate(admissions)
                    }
                },
            )
    pytest.fail("RED: cannot locate immutable admitted set")


def _outcome(admission):
    return _value(getattr(admission, "outcome"))


def _reason(result):
    return _value(getattr(result, "reason_code", None))


def _value(value):
    return getattr(value, "value", value)


def _assert_not_deterministic(result) -> None:
    assert _value(result.route_kind) != "DETERMINISTIC"


def _boundary_route(boundary, oracles, **changes):
    values = _routing_values(oracles)
    values.update(changes)
    return boundary.route(**values)


def _retained_context(admission) -> SecurityContext:
    if dataclasses.is_dataclass(admission):
        for field in dataclasses.fields(admission):
            value = getattr(admission, field.name)
            if isinstance(value, SecurityContext):
                return value
    pytest.fail("RED: READY admission must retain the exact SecurityContext")


def _admission_evaluated_at(admission) -> datetime:
    value = getattr(admission, "admission_evaluated_at", None)
    assert isinstance(value, datetime)
    return value


def _pep_binding(seed: str) -> AuthorizationOperationBinding:
    return AuthorizationOperationBinding(
        namespace="engineering.qualification_review_consumption",
        binding_version="v0",
        digest_algorithm="sha256",
        digest_hex=seed * 64,
    )


def test_pqctb_r01_caller_only_full_through_free_route_is_inferential() -> None:
    bundle = _qualification_bundle()
    result = _free_route(oracles=(_oracle(bundle),))
    assert _value(result.route_kind) == "INFERENTIAL"


def test_pqctb_r02_boundary_route_exposes_no_trust_inputs() -> None:
    api = _trust_api("PQCTB-R02")
    signature = inspect.signature(api.GovernedQualificationConsumptionBoundaryV0.route)
    forbidden = {
        "review", "review_evidence", "qualification_review_evidence",
        "admission", "authorization_request", "authorization_decision",
        "security_context", "clock", "policy_decision_point", "pep",
    }
    assert forbidden.isdisjoint(signature.parameters)


def test_pqctb_r03_request_cannot_replace_precomposed_admitted_set() -> None:
    api = _trust_api("PQCTB-R03")
    signature = inspect.signature(api.GovernedQualificationConsumptionBoundaryV0.route)
    forbidden = {
        "admissions", "boundary", "configuration", "factory", "review",
        "security_context", "clock", "policy_decision_point",
    }
    assert forbidden.isdisjoint(signature.parameters)


def test_pqctb_r04_missing_admission_remains_inferential() -> None:
    bundle = _qualification_bundle()
    result = _free_route(oracles=(_oracle(bundle),))
    assert _value(result.route_kind) == "INFERENTIAL"


def test_pqctb_r05_repository_mismatch_blocks_ready_and_deterministic() -> None:
    bundle = _qualification_bundle(repository="Other/repository")
    boundary, api, _, _, _, _ = _compose(
        "PQCTB-R05",
        bundle=bundle,
        review=_review_evidence(bundle),
    )
    assert _outcome(_single_admission(boundary, api)) != "READY"


def test_pqctb_r06_evaluated_candidate_mismatch_blocks_ready() -> None:
    bundle = _qualification_bundle(candidate=OTHER_CANDIDATE)
    boundary, api, _, _, _, _ = _compose(
        "PQCTB-R06",
        bundle=bundle,
        review=_review_evidence(bundle),
    )
    assert _outcome(_single_admission(boundary, api)) != "READY"


def test_pqctb_r07_review_bundle_digest_mismatch_blocks_ready() -> None:
    bundle = _qualification_bundle()
    review = _review_evidence(bundle)
    review["qualification_bundle_digest"] = "7" * 64
    boundary, api, _, _, _, _ = _compose(
        "PQCTB-R07", bundle=bundle, review=review
    )
    assert _outcome(_single_admission(boundary, api)) != "READY"


def test_pqctb_r08_oracle_identity_drift_cannot_use_prior_admission() -> None:
    bundle = _qualification_bundle()
    boundary, _, _, _, _, _ = _compose("PQCTB-R08", bundle=bundle)
    drifted = _qualification_bundle(oracle_content_digest="8" * 64)
    _assert_not_deterministic(
        _boundary_route(boundary, (_oracle(drifted),))
    )


def test_pqctb_r09_question_or_contract_drift_cannot_use_prior_admission() -> None:
    bundle = _qualification_bundle()
    boundary, _, _, _, _, _ = _compose("PQCTB-R09", bundle=bundle)
    drifted = _qualification_bundle(input_contract_identity="9" * 64)
    _assert_not_deterministic(
        _boundary_route(boundary, (_oracle(drifted),))
    )


def test_pqctb_r10_catalog_digest_mismatch_blocks_ready() -> None:
    bundle = _qualification_bundle()
    review = _review_evidence(bundle)
    review["reviewed_obligation_catalog_digest"] = "9" * 64
    boundary, api, _, _, _, _ = _compose(
        "PQCTB-R10", bundle=bundle, review=review
    )
    assert _outcome(_single_admission(boundary, api)) != "READY"


def test_pqctb_r11_catalog_completeness_fail_is_denied() -> None:
    bundle = _qualification_bundle()
    boundary, api, _, _, _, _ = _compose(
        "PQCTB-R11",
        bundle=bundle,
        review=_review_evidence(bundle, catalog="FAIL"),
    )
    assert _outcome(_single_admission(boundary, api)) == "DENIED"


def test_pqctb_r12_catalog_completeness_inconclusive_is_hold() -> None:
    bundle = _qualification_bundle()
    boundary, api, _, _, _, _ = _compose(
        "PQCTB-R12",
        bundle=bundle,
        review=_review_evidence(bundle, catalog="INCONCLUSIVE"),
    )
    assert _outcome(_single_admission(boundary, api)) == "HOLD"


def test_pqctb_r13_structural_fail_is_denied() -> None:
    bundle = _qualification_bundle()
    boundary, api, _, _, _, _ = _compose(
        "PQCTB-R13",
        bundle=bundle,
        review=_review_evidence(bundle, structural="FAIL"),
    )
    assert _outcome(_single_admission(boundary, api)) == "DENIED"


def test_pqctb_r14_structural_inconclusive_is_hold() -> None:
    bundle = _qualification_bundle()
    boundary, api, _, _, _, _ = _compose(
        "PQCTB-R14",
        bundle=bundle,
        review=_review_evidence(bundle, structural="INCONCLUSIVE"),
    )
    assert _outcome(_single_admission(boundary, api)) == "HOLD"


def test_pqctb_r15_independence_non_pass_blocks_ready() -> None:
    for terminal in ("FAIL", "INCONCLUSIVE"):
        bundle = _qualification_bundle()
        boundary, api, _, _, _, _ = _compose(
            "PQCTB-R15",
            bundle=bundle,
            review=_review_evidence(bundle, independence=terminal),
        )
        assert _outcome(_single_admission(boundary, api)) != "READY"


def test_pqctb_r16_verification_non_pass_blocks_ready() -> None:
    for terminal in ("FAIL", "INCONCLUSIVE"):
        bundle = _qualification_bundle()
        boundary, api, _, _, _, _ = _compose(
            "PQCTB-R16",
            bundle=bundle,
            review=_review_evidence(bundle, verification=terminal),
        )
        assert _outcome(_single_admission(boundary, api)) != "READY"


def test_pqctb_r17_qualification_review_non_pass_blocks_ready() -> None:
    for terminal in ("FAIL", "INCONCLUSIVE"):
        bundle = _qualification_bundle()
        boundary, api, _, _, _, _ = _compose(
            "PQCTB-R17",
            bundle=bundle,
            review=_review_evidence(bundle, qualification=terminal),
        )
        assert _outcome(_single_admission(boundary, api)) != "READY"


def test_pqctb_r18_caller_supplied_authorization_decision_is_not_an_input() -> None:
    factory = _composition_factory("PQCTB-R18")
    assert "authorization_decision" not in inspect.signature(factory).parameters
    api = _trust_api("PQCTB-R18")
    assert "authorization_decision" not in inspect.signature(
        api.GovernedQualificationConsumptionBoundaryV0.route
    ).parameters


def test_pqctb_r19_configured_pdp_is_invoked_once_on_positive_admission() -> None:
    clock = MutableClock()
    pdp = _recording_pdp(clock)
    audit = InMemoryAuthorizationAuditStore()
    boundary, api, _, _, _, _ = _compose(
        "PQCTB-R19", clock=clock, pdp=pdp, audit=audit
    )
    assert _outcome(_single_admission(boundary, api)) == "READY"
    assert len(pdp.calls) == 1
    assert any(
        record.outcome is AuthorizationAuditOutcome.ALLOWED
        for record in audit.records
    )


def test_pqctb_r20_permission_scope_mismatch_blocks_before_operation() -> None:
    clock = MutableClock()
    pdp = _recording_pdp(clock)
    operation = ProbeOperation(binding=_pep_binding("1"))
    request = AuthorizationRequest(
        context=_context(),
        permission=PermissionScope(
            resource=ADMISSION_PERMISSION.resource,
            action="read",
        ),
        created_at=NOW,
        operation_binding=operation.authorization_binding,
    )
    pep = StrictPolicyEnforcementPoint(
        pdp, operation, InMemoryAuthorizationAuditStore()
    )
    with pytest.raises(AuthorizationEnforcementError):
        pep.execute(request)
    assert operation.execute_count == 0
    assert len(pdp.calls) == 0


def test_pqctb_r21_request_operation_binding_mismatch_blocks() -> None:
    clock = MutableClock()
    pdp = _recording_pdp(clock)
    operation = ProbeOperation(binding=_pep_binding("1"))
    request = AuthorizationRequest(
        context=_context(),
        permission=ADMISSION_PERMISSION,
        created_at=NOW,
        operation_binding=_pep_binding("2"),
    )
    pep = StrictPolicyEnforcementPoint(
        pdp, operation, InMemoryAuthorizationAuditStore()
    )
    with pytest.raises(AuthorizationEnforcementError):
        pep.execute(request)
    assert operation.execute_count == 0
    assert len(pdp.calls) == 0


def test_pqctb_r22_decision_request_binding_mismatch_blocks() -> None:
    clock = MutableClock()
    delegate = _recording_pdp(clock).delegate
    pdp = DecisionBindingTamperingPDP(delegate)
    operation = ProbeOperation(binding=_pep_binding("1"))
    request = AuthorizationRequest(
        context=_context(),
        permission=ADMISSION_PERMISSION,
        created_at=NOW,
        operation_binding=operation.authorization_binding,
    )
    pep = StrictPolicyEnforcementPoint(
        pdp, operation, InMemoryAuthorizationAuditStore()
    )
    with pytest.raises(AuthorizationEnforcementError):
        pep.execute(request)
    assert operation.execute_count == 0
    assert len(pdp.calls) == 1


def test_pqctb_r23_authority_effect_other_than_none_blocks() -> None:
    bundle = _qualification_bundle()
    boundary, api, _, _, _, _ = _compose(
        "PQCTB-R23",
        bundle=bundle,
        review=_review_evidence(bundle, authority_effect="allow"),
    )
    assert _outcome(_single_admission(boundary, api)) != "READY"


def test_pqctb_r24_invalid_context_blocks_admission() -> None:
    clock = MutableClock()
    expired = _context(
        issued_at=NOW - timedelta(hours=2),
        expires_at=NOW - timedelta(hours=1),
    )
    boundary, api, _, _, _, _ = _compose(
        "PQCTB-R24", clock=clock, context=expired
    )
    assert _outcome(_single_admission(boundary, api)) != "READY"


def test_pqctb_r25_expiry_between_pep_and_ready_freeze_blocks_ready() -> None:
    context = _context(expires_at=NOW + timedelta(minutes=5))
    clock = SequenceClock(
        [NOW, NOW, NOW + timedelta(minutes=6), NOW + timedelta(minutes=6)]
    )
    boundary, api, _, _, _, _ = _compose(
        "PQCTB-R25",
        clock=clock,
        context=context,
        pdp=_recording_pdp(clock),
    )
    assert _outcome(_single_admission(boundary, api)) != "READY"


def test_pqctb_r26_consume_at_equal_admission_evaluated_at_may_proceed() -> None:
    clock = MutableClock()
    bundle = _qualification_bundle()
    boundary, api, _, _, _, _ = _compose(
        "PQCTB-R26", bundle=bundle, clock=clock
    )
    admission = _single_admission(boundary, api)
    assert _outcome(admission) == "READY"
    clock.current = _admission_evaluated_at(admission)
    assert _value(
        _boundary_route(boundary, (_oracle(bundle),)).route_kind
    ) == "DETERMINISTIC"


def test_pqctb_r27_consume_at_equal_expiry_is_stale() -> None:
    clock = MutableClock()
    context = _context(expires_at=NOW + timedelta(minutes=5))
    bundle = _qualification_bundle()
    boundary, _, _, _, _, _ = _compose(
        "PQCTB-R27", bundle=bundle, clock=clock, context=context
    )
    clock.current = context.expires_at
    result = _boundary_route(boundary, (_oracle(bundle),))
    _assert_not_deterministic(result)
    assert _reason(result) == "ADMISSION_STALE"


def test_pqctb_r28_consume_after_expiry_is_stale() -> None:
    clock = MutableClock()
    context = _context(expires_at=NOW + timedelta(minutes=5))
    bundle = _qualification_bundle()
    boundary, _, _, _, _, _ = _compose(
        "PQCTB-R28", bundle=bundle, clock=clock, context=context
    )
    clock.current = context.expires_at + timedelta(seconds=1)
    result = _boundary_route(boundary, (_oracle(bundle),))
    _assert_not_deterministic(result)
    assert _reason(result) == "ADMISSION_STALE"


def test_pqctb_r29_clock_reversal_blocks_positive_consumption() -> None:
    clock = MutableClock()
    bundle = _qualification_bundle()
    boundary, api, _, _, _, _ = _compose(
        "PQCTB-R29", bundle=bundle, clock=clock
    )
    admission = _single_admission(boundary, api)
    clock.current = _admission_evaluated_at(admission) - timedelta(seconds=1)
    result = _boundary_route(boundary, (_oracle(bundle),))
    _assert_not_deterministic(result)
    assert _reason(result) == "CLOCK_REVERSED"


def test_pqctb_r30_malformed_naive_or_throwing_clock_fails_closed() -> None:
    for mode in ("naive", "non_datetime", "raise"):
        clock = MutableClock()
        bundle = _qualification_bundle()
        boundary, _, _, _, _, _ = _compose(
            "PQCTB-R30", bundle=bundle, clock=clock
        )
        clock.mode = mode
        _assert_not_deterministic(
            _boundary_route(boundary, (_oracle(bundle),))
        )


def test_pqctb_r31_duplicate_ready_same_runtime_key_is_ambiguous() -> None:
    bundle = _qualification_bundle()
    first, api, clock, _, _, _ = _compose("PQCTB-R31", bundle=bundle)
    second, _, _, _, _, _ = _compose(
        "PQCTB-R31", bundle=bundle, clock=clock
    )
    combined = _with_admissions(
        first,
        api,
        (
            _single_admission(first, api),
            _single_admission(second, api),
        ),
    )
    result = _boundary_route(combined, (_oracle(bundle),))
    _assert_not_deterministic(result)
    assert _reason(result) == "ADMISSION_AMBIGUOUS"


def test_pqctb_r32_ready_mixed_with_hold_same_runtime_key_is_ambiguous() -> None:
    bundle = _qualification_bundle()
    ready, api, clock, _, _, _ = _compose("PQCTB-R32", bundle=bundle)
    hold, _, _, _, _, _ = _compose(
        "PQCTB-R32",
        bundle=bundle,
        review=_review_evidence(bundle, catalog="INCONCLUSIVE"),
        clock=clock,
    )
    combined = _with_admissions(
        ready,
        api,
        (
            _single_admission(ready, api),
            _single_admission(hold, api),
        ),
    )
    result = _boundary_route(combined, (_oracle(bundle),))
    _assert_not_deterministic(result)
    assert _reason(result) == "ADMISSION_AMBIGUOUS"


def test_pqctb_r33_ambiguous_full_oracles_preserve_oracle_ambiguous() -> None:
    first_bundle = _qualification_bundle()
    second_bundle = _qualification_bundle(
        oracle_id="oracle-2",
        oracle_content_digest="d" * 64,
    )
    result = _free_route(
        oracles=(_oracle(first_bundle), _oracle(second_bundle))
    )
    assert _reason(result) == "ORACLE_AMBIGUOUS"
    _assert_not_deterministic(result)


def test_pqctb_r34_exact_governed_positive_path_can_route_deterministic() -> None:
    bundle = _qualification_bundle()
    boundary, api, _, _, _, _ = _compose("PQCTB-R34", bundle=bundle)
    assert _outcome(_single_admission(boundary, api)) == "READY"
    assert _value(
        _boundary_route(boundary, (_oracle(bundle),)).route_kind
    ) == "DETERMINISTIC"


def test_pqctb_r35_positive_result_reports_selected_oracle_id() -> None:
    bundle = _qualification_bundle()
    boundary, _, _, _, _, _ = _compose("PQCTB-R35", bundle=bundle)
    oracle = _oracle(bundle)
    result = _boundary_route(boundary, (oracle,))
    assert _value(result.route_kind) == "DETERMINISTIC"
    assert result.selected_oracle_id == oracle.oracle_id


def test_pqctb_r36_p01_p09_regression_equivalent_between_free_and_boundary() -> None:
    bundle = _qualification_bundle()
    boundary, _, _, _, _, _ = _compose("PQCTB-R36", bundle=bundle)
    oracle = _oracle(bundle)
    cases = [
        {"policy_version": "unknown-policy"},
        {
            "expected_binding": {
                **_routing_values((oracle,))["expected_binding"],
                "focus_id": "OTHER",
            }
        },
        {"declared_evidence_complete": False},
    ]
    for changes in cases:
        free_values = _routing_values((oracle,))
        free_values.update(changes)
        free_result = _routing_module().route_governed_support_evidence_v0(
            **free_values
        )
        boundary_result = _boundary_route(boundary, (oracle,), **changes)
        assert _reason(boundary_result) == _reason(free_result)


def test_pqctb_r37_stale_runner_digest_or_material_blocks_ready() -> None:
    bundle = _qualification_bundle()
    material = copy.deepcopy(bundle["qualification_material"])
    assert isinstance(material, dict)
    material["executing_runner_digest"] = "0" * 64
    bundle["qualification_material"] = material
    bundle["qualification_material_digest"] = _sha256(material)
    boundary, api, _, _, _, _ = _compose(
        "PQCTB-R37",
        bundle=bundle,
        review=_review_evidence(bundle),
    )
    assert _outcome(_single_admission(boundary, api)) != "READY"


def test_pqctb_r38_unresolved_verification_reference_blocks_ready() -> None:
    bundle = _qualification_bundle()
    coverage = copy.deepcopy(bundle["coverage_entries"])
    assert isinstance(coverage, list)
    coverage[0]["verification_evidence_refs"] = ["evidence:missing"]
    bundle["coverage_entries"] = coverage
    boundary, api, _, _, _, _ = _compose(
        "PQCTB-R38",
        bundle=bundle,
        review=_review_evidence(bundle),
    )
    assert _outcome(_single_admission(boundary, api)) != "READY"


def test_pqctb_r39_runtime_material_change_invalidates_prior_admission() -> None:
    bundle = _qualification_bundle()
    boundary, _, _, _, _, _ = _compose("PQCTB-R39", bundle=bundle)
    changed = _qualification_bundle()
    catalog = copy.deepcopy(changed["obligation_catalog"])
    assert isinstance(catalog, list)
    catalog[0]["obligation_statement"] = "Changed material obligation."
    changed["obligation_catalog"] = catalog
    changed["obligation_catalog_digest"] = _sha256(catalog)
    _assert_not_deterministic(
        _boundary_route(boundary, (_oracle(changed),))
    )


def test_pqctb_r40_candidate_change_invalidates_prior_admission() -> None:
    bundle = _qualification_bundle()
    boundary, _, _, _, _, _ = _compose("PQCTB-R40", bundle=bundle)
    oracle = _oracle(bundle)
    result = _boundary_route(
        boundary,
        (oracle,),
        baseline_commit=OTHER_CANDIDATE,
        expected_binding={
            **_routing_values((oracle,))["expected_binding"],
            "baseline_commit": OTHER_CANDIDATE,
        },
    )
    _assert_not_deterministic(result)


def test_pqctb_r41_rdd_or_review_references_are_not_runtime_credentials() -> None:
    api = _trust_api("PQCTB-R41")
    signatures = (
        inspect.signature(_routing_module().route_governed_support_evidence_v0),
        inspect.signature(api.GovernedQualificationConsumptionBoundaryV0.route),
    )
    forbidden = {
        "rdd_manifest", "rdd_receipt", "review_reference",
        "validator_reference", "evidence_reference", "approval",
    }
    for signature in signatures:
        assert forbidden.isdisjoint(signature.parameters)


def test_pqctb_r42_hard_zero_architectural_effects_remain_absent() -> None:
    api = _trust_api("PQCTB-R42")
    objects = (
        api.GovernedQualificationReviewAdmissionOperationV0,
        api.GovernedQualificationConsumptionBoundaryV0,
        api.RuntimeQualificationBindingV0,
    )
    source = "\n".join(inspect.getsource(obj).lower() for obj in objects)
    forbidden = (
        "malak.kernel", "malak.services.planner", "malak.runtime",
        "conversationcapability", "support_sufficient", "protectedfinal",
        "internalinteraction", "requests.", "httpx.", "socket.",
        "receiptstore", "evidenceregistry", "rdd_stage_2", "stage2",
    )
    for token in forbidden:
        assert token not in source


def test_pqctb_r43_runtime_evidence_digest_mismatch_blocks_prior_admission() -> None:
    bundle = _qualification_bundle()
    boundary, _, _, _, _, _ = _compose("PQCTB-R43", bundle=bundle)
    q = _qualification(bundle, qualification_evidence_digest="9" * 64)
    _assert_not_deterministic(
        _boundary_route(boundary, (_oracle(bundle, qualification=q),))
    )


def test_pqctb_r44_runtime_qualifier_mismatch_blocks_prior_admission() -> None:
    bundle = _qualification_bundle()
    boundary, _, _, _, _, _ = _compose("PQCTB-R44", bundle=bundle)
    q = _qualification(bundle, reviewer_id="different-reviewer")
    _assert_not_deterministic(
        _boundary_route(boundary, (_oracle(bundle, qualification=q),))
    )


def test_pqctb_r45_forged_coherent_qualification_identity_is_recomputed() -> None:
    bundle = _qualification_bundle()
    boundary, _, _, _, _, _ = _compose("PQCTB-R45", bundle=bundle)
    q = _qualification(bundle)
    forged_identity = "9" * 64
    object.__setattr__(q, "qualification_identity", forged_identity)
    oracle = _oracle(
        bundle,
        qualification=q,
        qualification_identity=forged_identity,
    )
    _assert_not_deterministic(_boundary_route(boundary, (oracle,)))


def test_pqctb_r46_route_baseline_must_equal_admitted_candidate() -> None:
    bundle = _qualification_bundle()
    boundary, _, _, _, _, _ = _compose("PQCTB-R46", bundle=bundle)
    oracle = _oracle(bundle)
    result = _boundary_route(
        boundary,
        (oracle,),
        baseline_commit=OTHER_CANDIDATE,
        expected_binding={
            **_routing_values((oracle,))["expected_binding"],
            "baseline_commit": OTHER_CANDIDATE,
        },
    )
    _assert_not_deterministic(result)


def test_pqctb_r47_multiple_reviews_same_runtime_key_are_ambiguous() -> None:
    bundle = _qualification_bundle()
    first, api, clock, _, _, _ = _compose(
        "PQCTB-R47",
        bundle=bundle,
        review=_review_evidence(
            bundle,
            evidence_references=["external:review-a"],
        ),
    )
    second, _, _, _, _, _ = _compose(
        "PQCTB-R47",
        bundle=bundle,
        review=_review_evidence(
            bundle,
            evidence_references=["external:review-b"],
        ),
        clock=clock,
    )
    combined = _with_admissions(
        first,
        api,
        (
            _single_admission(first, api),
            _single_admission(second, api),
        ),
    )
    result = _boundary_route(combined, (_oracle(bundle),))
    _assert_not_deterministic(result)
    assert _reason(result) == "ADMISSION_AMBIGUOUS"


def test_pqctb_r48_admission_start_equal_context_issued_at_may_proceed() -> None:
    clock = MutableClock(NOW)
    context = _context(
        issued_at=NOW,
        expires_at=NOW + timedelta(minutes=30),
    )
    boundary, api, _, _, _, _ = _compose(
        "PQCTB-R48", clock=clock, context=context
    )
    assert _outcome(_single_admission(boundary, api)) == "READY"


def test_pqctb_r49_admission_evaluated_equal_started_may_proceed() -> None:
    clock = MutableClock(NOW)
    boundary, api, _, _, _, _ = _compose("PQCTB-R49", clock=clock)
    admission = _single_admission(boundary, api)
    assert _outcome(admission) == "READY"
    request_created = getattr(admission, "authorization_request_created_at")
    assert _admission_evaluated_at(admission) == request_created


def test_pqctb_r50_expiry_during_structural_work_is_observed_after_lookup() -> None:
    clock = MutableClock(NOW)
    context = _context(expires_at=NOW + timedelta(minutes=5))
    bundle = _qualification_bundle()
    boundary, _, _, _, _, _ = _compose(
        "PQCTB-R50", bundle=bundle, clock=clock, context=context
    )
    events: list[str] = []
    oracles = EventOracleList(
        [_oracle(bundle)],
        events,
        on_iter=lambda: setattr(clock, "current", context.expires_at),
    )
    result = _boundary_route(boundary, oracles)
    _assert_not_deterministic(result)
    assert _reason(result) == "ADMISSION_STALE"


def test_pqctb_r51_consumption_clock_sample_occurs_after_structural_and_lookup() -> None:
    events: list[str] = []
    clock = EventClock(events, NOW)
    bundle = _qualification_bundle()
    boundary, _, _, _, _, _ = _compose(
        "PQCTB-R51", bundle=bundle, clock=clock
    )
    events.clear()
    clock.calls = 0
    oracles = EventOracleList([_oracle(bundle)], events)
    result = _boundary_route(boundary, oracles)
    assert _value(result.route_kind) == "DETERMINISTIC"
    assert events.count("clock_now") == 1
    assert "oracles_iter" in events
    assert events.index("oracles_iter") < events.index("clock_now")


def test_pqctb_r52_consumption_uses_exact_frozen_security_context() -> None:
    context = _context()
    bundle = _qualification_bundle()
    boundary, api, _, _, _, _ = _compose(
        "PQCTB-R52", bundle=bundle, context=context
    )
    admission = _single_admission(boundary, api)
    assert _retained_context(admission) is context
    assert "security_context" not in inspect.signature(
        boundary.route
    ).parameters
    assert _value(
        _boundary_route(boundary, (_oracle(bundle),)).route_kind
    ) == "DETERMINISTIC"

def test_f250_4r_01_malformed_coverage_result_returns_hold() -> None:
    bundle = _qualification_bundle()
    review = _review_evidence(bundle)
    coverage = copy.deepcopy(bundle["coverage_entries"])
    assert isinstance(coverage, list)
    coverage[0]["entry_result"] = []
    bundle["coverage_entries"] = coverage

    boundary, api, _, _, _, _ = _compose(
        "F250-4R-01-COVERAGE",
        bundle=bundle,
        review=review,
    )
    admission = _single_admission(boundary, api)
    assert _outcome(admission) == "HOLD"
    assert admission.reason_code == "ENTRY_RESULT_INVALID"


def test_f250_4r_01_malformed_review_result_returns_hold() -> None:
    bundle = _qualification_bundle()
    review = _review_evidence(bundle)
    review["catalog_completeness_result"] = []

    boundary, api, _, _, _, _ = _compose(
        "F250-4R-01-REVIEW",
        bundle=bundle,
        review=review,
    )
    admission = _single_admission(boundary, api)
    assert _outcome(admission) == "HOLD"
    assert admission.reason_code == "REVIEW_RESULT_INVALID"


def test_f250_4r_01_nonserializable_bundle_material_returns_hold() -> None:
    bundle = _qualification_bundle()
    review = _review_evidence(bundle)
    coverage = copy.deepcopy(bundle["coverage_entries"])
    assert isinstance(coverage, list)
    coverage[0]["entry_reasons"] = {"not-json-serializable"}
    bundle["coverage_entries"] = coverage

    boundary, api, _, _, _, _ = _compose(
        "F250-4R-01-NONSERIALIZABLE",
        bundle=bundle,
        review=review,
    )
    admission = _single_admission(boundary, api)
    assert _outcome(admission) == "HOLD"
    assert admission.reason_code == "BUNDLE_MATERIAL_INVALID"


def test_f250_4r_01_invalid_unicode_bundle_material_returns_hold() -> None:
    bundle = _qualification_bundle()
    review = _review_evidence(bundle)
    bundle["repository"] = "\ud800"

    boundary, api, _, _, _, _ = _compose(
        "F250-4R-01-UNICODE",
        bundle=bundle,
        review=review,
    )
    admission = _single_admission(boundary, api)
    assert _outcome(admission) == "HOLD"
    assert admission.reason_code == "BUNDLE_MATERIAL_INVALID"


def test_f250_4r_02_review_aggregate_bound_returns_hold() -> None:
    bundle = _qualification_bundle()

    refs = []
    for index in range(130):
        prefix = f"external:review-{index:03d}:"
        refs.append(prefix + ("x" * (4096 - len(prefix))))
    review = _review_evidence(bundle, evidence_references=refs)

    boundary, api, _, _, _, _ = _compose(
        "F250-4R-02-SIZE",
        bundle=bundle,
        review=review,
    )
    admission = _single_admission(boundary, api)
    assert _outcome(admission) == "HOLD"
    assert admission.reason_code == "REVIEW_BOUND_EXCEEDED"


def test_f250_4r_02_review_reference_cardinality_is_bounded() -> None:
    bundle = _qualification_bundle()

    at_limit = _review_evidence(
        bundle,
        evidence_references=[
            f"external:review-{index:03d}"
            for index in range(512)
        ],
    )
    boundary, api, _, _, _, _ = _compose(
        "F250-4R-02-CARDINALITY-LIMIT",
        bundle=bundle,
        review=at_limit,
    )
    assert _outcome(_single_admission(boundary, api)) == "READY"

    over_limit = _review_evidence(
        bundle,
        evidence_references=[
            f"external:review-{index:03d}"
            for index in range(513)
        ],
    )
    boundary, api, _, _, _, _ = _compose(
        "F250-4R-02-CARDINALITY-OVER",
        bundle=bundle,
        review=over_limit,
    )
    admission = _single_admission(boundary, api)
    assert _outcome(admission) == "HOLD"
    assert admission.reason_code == "REVIEW_REFERENCES_OUT_OF_BOUNDS"


def test_f250_4r_02_duplicate_review_references_return_hold() -> None:
    bundle = _qualification_bundle()
    review = _review_evidence(
        bundle,
        evidence_references=[
            "external:review-duplicate",
            "external:review-duplicate",
        ],
    )

    boundary, api, _, _, _, _ = _compose(
        "F250-4R-02-DUPLICATE",
        bundle=bundle,
        review=review,
    )
    admission = _single_admission(boundary, api)
    assert _outcome(admission) == "HOLD"
    assert admission.reason_code == "REVIEW_REFERENCE_DUPLICATE"

def test_f250_fv_01_deep_nested_verification_material_returns_hold() -> None:
    bundle = _qualification_bundle()
    review = _review_evidence(bundle)

    nested: object = 0
    for _ in range(10000):
        nested = [nested]

    evidence = copy.deepcopy(bundle["verification_evidence"])
    assert isinstance(evidence, list)
    evidence[0]["content_or_bounded_material"] = nested
    bundle["verification_evidence"] = evidence

    red_id = "F250-FV-01-BUNDLE-DEEP"
    clock = MutableClock()
    context = _context()
    pdp = _recording_pdp(clock)
    audit = InMemoryAuthorizationAuditStore()
    factory = _composition_factory(red_id)
    boundary = factory(
        qualification_bundle=bundle,
        qualification_review_evidence=review,
        expected_repository=REPOSITORY,
        expected_candidate_commit=CANDIDATE,
        security_context=context,
        policy_decision_point=pdp,
        authorization_audit_sink=audit,
        clock=clock,
    )
    api = _trust_api(red_id)
    admission = _single_admission(boundary, api)
    assert _outcome(admission) == "HOLD"
    assert admission.reason_code == "BUNDLE_MATERIAL_INVALID"


def test_f250_fv_01_deep_nested_review_material_returns_hold() -> None:
    bundle = _qualification_bundle()
    review = _review_evidence(bundle)

    nested: object = 0
    for _ in range(10000):
        nested = [nested]

    review["finding_refs"] = nested

    red_id = "F250-FV-01-REVIEW-DEEP"
    clock = MutableClock()
    context = _context()
    pdp = _recording_pdp(clock)
    audit = InMemoryAuthorizationAuditStore()
    factory = _composition_factory(red_id)
    boundary = factory(
        qualification_bundle=bundle,
        qualification_review_evidence=review,
        expected_repository=REPOSITORY,
        expected_candidate_commit=CANDIDATE,
        security_context=context,
        policy_decision_point=pdp,
        authorization_audit_sink=audit,
        clock=clock,
    )
    api = _trust_api(red_id)
    admission = _single_admission(boundary, api)
    assert _outcome(admission) == "HOLD"
    assert admission.reason_code == "REVIEW_MATERIAL_INVALID"
