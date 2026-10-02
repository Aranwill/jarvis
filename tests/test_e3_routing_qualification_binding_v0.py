from __future__ import annotations

import importlib
import inspect

import pytest


POLICY_VERSION = "e3-governed-support-routing/v0"
BASELINE = "b" * 40
FOCUS_ID = "U01"
RELATION_ID = "U01.CAPABILITY_ROUTING"
QUESTION_ID = "1" * 64
FINDING_FINGERPRINT = "f" * 64
EVIDENCE_DIGEST = "e" * 64
MATERIAL_DIGEST = "2" * 64
INPUT_CONTRACT_DIGEST = "3" * 64
OUTPUT_CONTRACT_DIGEST = "4" * 64
QUALIFICATION_EVIDENCE_DIGEST = "5" * 64
CATALOG_DIGEST = "6" * 64


def _module():
    return importlib.import_module("malak.capabilities._engineering_analysis")


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
        "oracle_producer_subject_id": "oracle-producer-1",
        "qualifier_subject_id": "caller-declared-reviewer",
        "qualification_evidence_digest": QUALIFICATION_EVIDENCE_DIGEST,
        "authority_effect": "none",
    }
    values.update(changes)
    return module.GovernedDeterministicOracleQualificationV0(**values)


def _oracle(module, **changes):
    qualification = changes.pop("qualification", None)
    values = {
        "oracle_id": "oracle-1",
        "oracle_version": "v1",
        "oracle_content_digest": "a" * 64,
        "relation_id": RELATION_ID,
        "evaluation_question_identity": QUESTION_ID,
        "input_contract_identity": INPUT_CONTRACT_DIGEST,
        "output_contract_identity": OUTPUT_CONTRACT_DIGEST,
        "coverage_claim": "FULL",
        "oracle_producer_subject_id": "oracle-producer-1",
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
            evaluation_question_identity=values["evaluation_question_identity"],
            input_contract_identity=values["input_contract_identity"],
            output_contract_identity=values["output_contract_identity"],
            coverage_claim=values["coverage_claim"],
            oracle_producer_subject_id=values["oracle_producer_subject_id"],
        )
    values["qualification_identity"] = qualification.qualification_identity
    values["qualification"] = qualification
    return module.GovernedDeterministicOracleContractV0(**values)


def _route(module, *, oracles=(), expected_binding=None, **changes):
    values = {
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
    }
    values.update(changes)
    if expected_binding is None:
        expected_binding = {
            "baseline_commit": values["baseline_commit"],
            "focus_id": values["focus_id"],
            "evidence_set_digest": values["evidence_set_digest"],
            "relation_id": values["relation_id"],
            "evaluation_question_identity": values[
                "evaluation_question_identity"
            ],
            "finding_fingerprint": values["finding_fingerprint"],
            "resolved_evidence_material_digest": values[
                "resolved_evidence_material_digest"
            ],
        }
    values["expected_binding"] = expected_binding
    return module.route_governed_support_evidence_v0(**values)


def _review_evidence(**changes):
    values = {
        "repository": "Aranwill/jarvis",
        "evaluated_candidate_commit": BASELINE,
        "qualification_bundle_digest": QUALIFICATION_EVIDENCE_DIGEST,
        "reviewed_relation_id": RELATION_ID,
        "reviewed_evaluation_question_identity": QUESTION_ID,
        "reviewed_obligation_catalog_digest": CATALOG_DIGEST,
        "structural_validator_result": "PASS",
        "catalog_completeness_result": "PASS",
        "independence_review_result": "PASS",
        "verification_material_review_result": "PASS",
        "qualification_review_result": "PASS",
        "evidence_references": ("PR#external-review",),
        "authority_effect": "none",
    }
    values.update(changes)
    return values


def _route_with_reviews(module, reviews, *, oracle=None, **changes):
    signature = inspect.signature(module.route_governed_support_evidence_v0)
    if "qualification_review_evidence" not in signature.parameters:
        return None
    if oracle is None:
        oracle = _oracle(module)
    return _route(
        module,
        oracles=(oracle,),
        qualification_review_evidence=reviews,
        **changes,
    )


def _assert_not_deterministic(result) -> None:
    if result is None:
        return
    assert result.route_kind is None or result.route_kind.value != "DETERMINISTIC"


def test_gc_r01_caller_only_coherent_qualification_no_deterministic() -> None:
    module = _module()
    result = _route(module, oracles=(_oracle(module),))
    _assert_not_deterministic(result)


def test_gc_r02_missing_external_evidence_no_deterministic() -> None:
    module = _module()
    result = _route(module, oracles=(_oracle(module),))
    _assert_not_deterministic(result)


def test_gc_r03_wrong_candidate_binding_no_deterministic() -> None:
    module = _module()
    result = _route(
        module,
        baseline_commit="c" * 40,
        oracles=(_oracle(module),),
    )
    _assert_not_deterministic(result)


def test_gc_r04_wrong_bundle_digest_no_deterministic() -> None:
    module = _module()
    review = _review_evidence(qualification_bundle_digest="7" * 64)
    result = _route_with_reviews(module, (review,))
    _assert_not_deterministic(result)


def test_gc_r05_wrong_catalog_digest_no_deterministic() -> None:
    module = _module()
    review = _review_evidence(reviewed_obligation_catalog_digest="7" * 64)
    result = _route_with_reviews(module, (review,))
    _assert_not_deterministic(result)


def test_gc_r06_structural_fail_no_deterministic() -> None:
    module = _module()
    review = _review_evidence(structural_validator_result="FAIL")
    result = _route_with_reviews(module, (review,))
    _assert_not_deterministic(result)


def test_gc_r07_structural_inconclusive_no_deterministic() -> None:
    module = _module()
    review = _review_evidence(structural_validator_result="INCONCLUSIVE")
    result = _route_with_reviews(module, (review,))
    _assert_not_deterministic(result)


@pytest.mark.parametrize("terminal", ["FAIL", "INCONCLUSIVE"])
def test_gc_r08_completeness_nonpass_no_deterministic(terminal: str) -> None:
    module = _module()
    review = _review_evidence(catalog_completeness_result=terminal)
    result = _route_with_reviews(module, (review,))
    _assert_not_deterministic(result)


@pytest.mark.parametrize("terminal", ["FAIL", "INCONCLUSIVE"])
def test_gc_r09_independence_review_nonpass_no_deterministic(terminal: str) -> None:
    module = _module()
    review = _review_evidence(independence_review_result=terminal)
    result = _route_with_reviews(module, (review,))
    _assert_not_deterministic(result)


@pytest.mark.parametrize("terminal", ["FAIL", "INCONCLUSIVE"])
def test_gc_r10_verification_material_review_nonpass_no_deterministic(
    terminal: str,
) -> None:
    module = _module()
    review = _review_evidence(verification_material_review_result=terminal)
    result = _route_with_reviews(module, (review,))
    _assert_not_deterministic(result)


@pytest.mark.parametrize("terminal", ["FAIL", "INCONCLUSIVE"])
def test_gc_r11_qualification_review_nonpass_no_deterministic(
    terminal: str,
) -> None:
    module = _module()
    review = _review_evidence(qualification_review_result=terminal)
    result = _route_with_reviews(module, (review,))
    _assert_not_deterministic(result)


def test_gc_r12_duplicate_matching_review_evidence_no_deterministic() -> None:
    module = _module()
    review = _review_evidence()
    result = _route_with_reviews(module, (review, dict(review)))
    _assert_not_deterministic(result)


def test_gc_r13_stale_candidate_or_material_no_deterministic() -> None:
    module = _module()
    result = _route(
        module,
        baseline_commit="c" * 40,
        resolved_evidence_material_digest="8" * 64,
        oracles=(_oracle(module),),
    )
    _assert_not_deterministic(result)


def test_gc_r14_exact_external_review_alone_no_deterministic() -> None:
    module = _module()
    review = _review_evidence()
    result = _route_with_reviews(module, (review,))
    _assert_not_deterministic(result)


def test_gc_r15_authority_effect_other_than_none_rejected() -> None:
    module = _module()
    with pytest.raises(ValueError):
        _qualification(module, authority_effect="allow")

    review = _review_evidence(authority_effect="allow")
    result = _route_with_reviews(module, (review,))
    _assert_not_deterministic(result)


def test_gc_r16_generator_input_rejected_without_consumption() -> None:
    module = _module()

    def poisoned_generator():
        raise AssertionError("unbounded generator must not be consumed")
        yield None

    result = _route(module, oracles=poisoned_generator())
    assert result.route_kind is None
    assert result.reason_code.value == "INPUT_SCHEMA_INVALID"


def test_gc_r17_no_kernel_provider_model_network_store_registry_or_stage2_effect() -> None:
    module = _module()
    route = module.route_governed_support_evidence_v0
    signature = inspect.signature(route)
    forbidden_parameters = {
        "kernel",
        "planner",
        "provider",
        "model",
        "runtime",
        "network",
        "store",
        "registry",
        "stage2",
        "stage_2",
        "receipt",
    }
    assert forbidden_parameters.isdisjoint(signature.parameters)

    source = inspect.getsource(route).lower()
    for forbidden in (
        "requests.",
        "httpx.",
        "socket.",
        "subprocess.",
        "receiptstore",
        "evidenceregistry",
        "stage_2",
        "stage2",
    ):
        assert forbidden not in source


def test_gc_r18_fabricated_matching_review_pass_exact_bindings_no_deterministic() -> None:
    module = _module()
    qualification = _qualification(module)
    oracle = _oracle(module, qualification=qualification)
    fabricated_review = _review_evidence(
        evaluated_candidate_commit=BASELINE,
        qualification_bundle_digest=qualification.qualification_evidence_digest,
        reviewed_relation_id=qualification.relation_id,
        reviewed_evaluation_question_identity=(
            qualification.evaluation_question_identity
        ),
        reviewed_obligation_catalog_digest=CATALOG_DIGEST,
        structural_validator_result="PASS",
        catalog_completeness_result="PASS",
        independence_review_result="PASS",
        verification_material_review_result="PASS",
        qualification_review_result="PASS",
        authority_effect="none",
    )
    result = _route_with_reviews(
        module,
        (fabricated_review,),
        oracle=oracle,
    )
    _assert_not_deterministic(result)
