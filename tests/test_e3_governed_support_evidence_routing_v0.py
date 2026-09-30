from __future__ import annotations

import copy
import importlib
import inspect
import socket
import subprocess

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
ORACLE_PRODUCER_SUBJECT_ID = "oracle-producer-1"
QUALIFIER_SUBJECT_ID = "oracle-qualifier-1"


def _module():
    return importlib.import_module("malak.capabilities._engineering_analysis")


def _routing_api():
    module = _module()
    for name in (
        "GovernedSupportEvidenceRouteKind",
        "GovernedSupportEvidenceRouteReason",
        "GovernedDeterministicOracleQualificationV0",
        "GovernedDeterministicOracleContractV0",
        "route_governed_support_evidence_v0",
    ):
        assert hasattr(module, name), f"RED: missing routing API {name}"
    return module


def _projection_api():
    module = _module()
    assert hasattr(
        module,
        "project_blind_support_assessor_input_v0",
    ), "RED: missing blind projection API project_blind_support_assessor_input_v0"
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


def _route(module, **changes):
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
        "oracles": (),
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
    values.update(changes)
    return module.route_governed_support_evidence_v0(**values)


def test_red_r01_route_kind_enum_is_closed() -> None:
    module = _routing_api()
    assert {item.value for item in module.GovernedSupportEvidenceRouteKind} == {
        "DETERMINISTIC",
        "INFERENTIAL",
        "INSUFFICIENT",
    }


def test_red_r02_exact_unique_full_oracle_routes_deterministic() -> None:
    module = _routing_api()
    result = _route(module, oracles=(_oracle(module),))
    assert result.route_kind.value == "DETERMINISTIC"
    assert result.reason_code.value == "DETERMINISTIC_ORACLE_ELIGIBLE"
    assert result.authority_effect == "none"


def test_red_r03_partial_oracle_never_routes_deterministic() -> None:
    module = _routing_api()
    partial_qualification = _qualification(module, coverage_claim="PARTIAL")
    partial = _oracle(
        module,
        coverage_claim="PARTIAL",
        qualification=partial_qualification,
    )

    result = _route(module, oracles=(partial,))

    assert result.route_kind.value == "INFERENTIAL"
    assert result.reason_code.value == "INFERENTIAL_RESIDUAL"


def test_red_r04_no_full_oracle_with_complete_material_routes_inferential() -> None:
    module = _routing_api()
    result = _route(module)
    assert result.route_kind.value == "INFERENTIAL"


def test_red_r05_incomplete_declared_material_routes_insufficient() -> None:
    module = _routing_api()
    result = _route(module, declared_evidence_complete=False)
    assert result.route_kind.value == "INSUFFICIENT"


def test_red_r06_unknown_policy_version_produces_no_positive_route() -> None:
    module = _routing_api()
    result = _route(module, policy_version="future/v9")
    assert result.route_kind is None
    assert result.reason_code.value == "POLICY_VERSION_MISMATCH"
    assert result.authority_effect == "none"


def test_red_r07_stale_oracle_qualification_cannot_route_deterministic() -> None:
    module = _routing_api()
    stale = _qualification(module, oracle_content_digest="6" * 64)
    oracle = _oracle(module, qualification=stale)

    result = _route(module, oracles=(oracle,))

    assert result.route_kind is None
    assert result.reason_code.value == "ORACLE_QUALIFICATION_STALE"


def test_red_r08_multiple_eligible_full_oracles_fail_closed() -> None:
    module = _routing_api()
    first = _oracle(module)
    second_qualification = _qualification(
        module,
        oracle_id="oracle-2",
        oracle_content_digest="c" * 64,
        qualification_evidence_digest="7" * 64,
    )
    second = _oracle(
        module,
        oracle_id="oracle-2",
        oracle_content_digest="c" * 64,
        qualification=second_qualification,
    )

    result = _route(module, oracles=(first, second))

    assert result.route_kind is None
    assert result.reason_code.value == "ORACLE_AMBIGUOUS"


def test_red_r09_relation_mismatch_cannot_route_deterministic() -> None:
    module = _routing_api()
    mismatch_relation = "U01.KERNEL_RESPONSIBILITY"
    mismatch_q = _qualification(module, relation_id=mismatch_relation)
    mismatch = _oracle(
        module,
        relation_id=mismatch_relation,
        qualification=mismatch_q,
    )

    result = _route(module, oracles=(mismatch,))

    assert result.route_kind is None
    assert result.reason_code.value == "ORACLE_CONTRACT_INVALID"


def test_red_r10_evaluation_question_drift_invalidates_prior_routing() -> None:
    module = _routing_api()
    result = _route(
        module,
        evaluation_question_identity="6" * 64,
    )
    assert result.route_kind is None
    assert result.reason_code.value == "SUBJECT_BINDING_MISMATCH"


@pytest.mark.parametrize(
    "field,value",
    [
        ("finding_fingerprint", "7" * 64),
        ("resolved_evidence_material_digest", "8" * 64),
        ("evidence_set_digest", "9" * 64),
    ],
)
def test_red_r11_evidence_or_finding_drift_invalidates_prior_routing(
    field: str,
    value: object,
) -> None:
    module = _routing_api()
    result = _route(module, **{field: value})
    assert result.route_kind is None
    assert result.reason_code.value == "SUBJECT_BINDING_MISMATCH"


def test_red_r12_routing_performs_no_network_or_process_calls(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _routing_api()

    def forbidden(*_args, **_kwargs):
        raise AssertionError("routing attempted an external/runtime side effect")

    monkeypatch.setattr(socket, "socket", forbidden)
    monkeypatch.setattr(subprocess, "run", forbidden)

    result = _route(module, oracles=(_oracle(module),))
    assert result.route_kind.value == "DETERMINISTIC"


@pytest.mark.parametrize("route_kind", ["INFERENTIAL", "INSUFFICIENT"])
def test_red_r13_r14_non_deterministic_routes_have_no_assessor_or_model_callback(
    route_kind: str,
) -> None:
    module = _routing_api()
    signature = inspect.signature(module.route_governed_support_evidence_v0)
    forbidden = {"assessor", "model", "provider", "llm", "runtime"}
    assert forbidden.isdisjoint(signature.parameters)

    result = (
        _route(module)
        if route_kind == "INFERENTIAL"
        else _route(module, declared_evidence_complete=False)
    )
    assert result.route_kind.value == route_kind


def test_red_r15_deterministic_selection_exposes_no_implicit_fallback_route() -> None:
    module = _routing_api()
    result = _route(module, oracles=(_oracle(module),))
    assert result.route_kind.value == "DETERMINISTIC"
    assert not hasattr(result, "fallback_route_kind")


def test_red_r16_authority_effect_other_than_none_fails_closed() -> None:
    module = _routing_api()
    with pytest.raises((TypeError, ValueError)):
        _oracle(module, authority_effect="allow")


def test_fix_b01_oracle_identity_must_be_nonempty_and_bounded() -> None:
    module = _routing_api()
    with pytest.raises(ValueError):
        _qualification(module, oracle_id="")
    with pytest.raises(ValueError):
        _qualification(module, oracle_id="x" * 257)


def test_fix_b01_oracle_digests_must_be_sha256() -> None:
    module = _routing_api()
    with pytest.raises(ValueError):
        _qualification(module, oracle_content_digest="not-a-digest")
    with pytest.raises(ValueError):
        _qualification(module, evaluation_question_identity="A" * 64)


def test_fix_b01_qualification_requires_independent_subjects() -> None:
    module = _routing_api()
    with pytest.raises(ValueError):
        _qualification(
            module,
            qualifier_subject_id=ORACLE_PRODUCER_SUBJECT_ID,
        )


def test_fix_b01_qualification_identity_is_derived_and_bound() -> None:
    module = _routing_api()
    qualification = _qualification(module)
    assert len(qualification.qualification_identity) == 64

    oracle = _oracle(
        module,
        qualification=qualification,
        qualification_identity="0" * 64,
    )
    result = _route(module, oracles=(oracle,))

    assert result.route_kind is None
    assert result.reason_code.value == "ORACLE_QUALIFICATION_STALE"


def test_fix_b02_oracles_none_fails_closed_without_exception() -> None:
    module = _routing_api()
    result = _route(module, oracles=None)
    assert result.route_kind is None
    assert result.reason_code.value == "INPUT_SCHEMA_INVALID"


def test_fix_b02_generator_is_rejected_without_consumption() -> None:
    module = _routing_api()

    def poisoned_generator():
        raise AssertionError("unbounded generator must not be consumed")
        yield None

    result = _route(module, oracles=poisoned_generator())

    assert result.route_kind is None
    assert result.reason_code.value == "INPUT_SCHEMA_INVALID"


def test_fix_b02_oracle_cardinality_is_hard_bounded() -> None:
    module = _routing_api()
    oracle = _oracle(module)
    result = _route(module, oracles=[oracle] * 17)
    assert result.route_kind is None
    assert result.reason_code.value == "INPUT_BOUNDS_EXCEEDED"


def test_fix_b02_missing_expected_binding_fails_closed() -> None:
    module = _routing_api()
    result = _route(module, expected_binding=None)
    assert result.route_kind is None
    assert result.reason_code.value == "INPUT_SCHEMA_INVALID"


def test_fix_b02_malformed_subject_identity_fails_closed() -> None:
    module = _routing_api()
    result = _route(module, baseline_commit="")
    assert result.route_kind is None
    assert result.reason_code.value == "INPUT_SCHEMA_INVALID"


def _blind_case() -> dict[str, object]:
    return {
        "input_id": "C01.I01",
        "subject": {
            "baseline_commit": BASELINE,
            "focus_id": FOCUS_ID,
            "evidence_set_digest": EVIDENCE_DIGEST,
            "relation_id": RELATION_ID,
            "classification": "ALIGNED",
            "statement": "Capability routing follows the governed path.",
            "rationale": "Bounded repository and knowledge evidence agree.",
            "supporting_repository_refs": ["R1"],
            "supporting_knowledge_refs": ["K1"],
            "limiting_or_counterevidence_refs": [],
            "uncertainty_basis": "NONE",
        },
        "repository_evidence": [
            {"ref": "R1", "material": "bounded repository material"}
        ],
        "knowledge_evidence": [
            {"ref": "K1", "material": "bounded knowledge material"}
        ],
        "binding_expectation": {
            "binding_kind": "NONE",
            "expected_subject_fingerprint": None,
            "expected_evidence_material_digest": None,
        },
        "binding_prior": None,
        "expected_outcome": "SUPPORTED",
        "expected_reason_codes": ["MATERIAL_SUPPORT_CONFIRMED"],
        "critical_properties": ["FALSE_SUPPORT"],
        "case_class": "EXACT_SUPPORT",
    }


def test_red_r17_blind_projection_excludes_ground_truth_fields() -> None:
    module = _projection_api()
    case_input = _blind_case()

    projected = module.project_blind_support_assessor_input_v0(case_input)

    assert set(projected) == {
        "input_id",
        "subject",
        "repository_evidence",
        "knowledge_evidence",
        "binding_expectation",
    }
    assert "expected_outcome" not in projected
    assert "expected_reason_codes" not in projected
    assert "critical_properties" not in projected
    assert "case_class" not in projected


def test_fix_b03_blind_projection_rejects_ground_truth_nested_in_subject() -> None:
    module = _projection_api()
    case_input = _blind_case()
    case_input["subject"]["expected_outcome"] = "SUPPORTED"

    with pytest.raises(ValueError, match="ground-truth"):
        module.project_blind_support_assessor_input_v0(case_input)


def test_fix_b03_blind_projection_rejects_ground_truth_nested_in_evidence() -> None:
    module = _projection_api()
    case_input = _blind_case()
    case_input["repository_evidence"][0]["critical_properties"] = ["FALSE_SUPPORT"]

    with pytest.raises(ValueError, match="ground-truth"):
        module.project_blind_support_assessor_input_v0(case_input)


def test_fix_b03_blind_projection_rejects_ground_truth_nested_in_binding() -> None:
    module = _projection_api()
    case_input = _blind_case()
    case_input["binding_expectation"]["expected_reason_codes"] = [
        "MATERIAL_SUPPORT_CONFIRMED"
    ]

    with pytest.raises(ValueError, match="ground-truth"):
        module.project_blind_support_assessor_input_v0(case_input)


def test_fix_b03_blind_projection_enforces_material_bounds() -> None:
    module = _projection_api()
    case_input = _blind_case()
    case_input["repository_evidence"][0]["material"] = "x" * (64 * 1024 + 1)

    with pytest.raises(ValueError):
        module.project_blind_support_assessor_input_v0(case_input)


def test_fix_b03_blind_projection_returns_detached_copy() -> None:
    module = _projection_api()
    case_input = _blind_case()
    projected = module.project_blind_support_assessor_input_v0(case_input)

    assert projected["subject"] is not case_input["subject"]
    assert (
        projected["repository_evidence"][0]
        is not case_input["repository_evidence"][0]
    )
    projected["subject"]["statement"] = "changed"
    projected["repository_evidence"][0]["material"] = "changed"

    assert case_input["subject"]["statement"] != "changed"
    assert case_input["repository_evidence"][0]["material"] != "changed"


def test_red_r18_candidate_artifact_precedes_hidden_ground_truth_comparison() -> None:
    module = _projection_api()
    case_input = _blind_case()
    projected = module.project_blind_support_assessor_input_v0(case_input)
    events: list[str] = []

    def candidate_mechanism(material: dict[str, object]) -> dict[str, object]:
        assert "expected_outcome" not in material
        assert "expected_reason_codes" not in material
        assert "critical_properties" not in material
        assert "case_class" not in material
        events.append("candidate_artifact_produced")
        return {
            "input_id": material["input_id"],
            "outcome": "SUPPORTED",
            "reason_codes": ["MATERIAL_SUPPORT_CONFIRMED"],
        }

    candidate_artifact = candidate_mechanism(projected)
    assert events == ["candidate_artifact_produced"]

    events.append("qualification_compared")
    assert candidate_artifact["outcome"] == case_input["expected_outcome"]
    assert candidate_artifact["reason_codes"] == case_input["expected_reason_codes"]
    assert events == ["candidate_artifact_produced", "qualification_compared"]


def test_guard_r19_generic_e3_support_assessment_contract_remains_unchanged() -> None:
    module = _module()
    signature = inspect.signature(module.assess_governed_evidence_support_v0)
    assert tuple(signature.parameters) == (
        "policy_version",
        "baseline_commit",
        "focus_id",
        "evidence_set_digest",
        "relation_id",
        "classification",
        "statement",
        "rationale",
        "supporting_repository_refs",
        "supporting_knowledge_refs",
        "limiting_or_counterevidence_refs",
        "uncertainty_basis",
        "repository_evidence",
        "knowledge_evidence",
        "assessor_subject_id",
        "finding_producer_subject_id",
        "assessor",
        "expected_binding",
    )


def test_guard_r20_e4_remains_unwired_to_support_routing() -> None:
    module = importlib.import_module("malak.capabilities.engineering_propose")
    source = inspect.getsource(module)
    assert "route_governed_support_evidence_v0" not in source
    assert "project_blind_support_assessor_input_v0" not in source


def test_guard_r21_kernel_planner_registry_remain_unwired() -> None:
    for module_name in (
        "malak.kernel.kernel",
        "malak.kernel.registry",
        "malak.services.planner",
    ):
        source = inspect.getsource(importlib.import_module(module_name))
        assert "_engineering_analysis" not in source
        assert "route_governed_support_evidence_v0" not in source
        assert "project_blind_support_assessor_input_v0" not in source


def test_guard_r22_support_sufficient_remains_unwired() -> None:
    signal_source = inspect.getsource(
        importlib.import_module("malak.core.assurance_signal_projection")
    )
    assert "route_governed_support_evidence_v0" not in signal_source
    assert "project_blind_support_assessor_input_v0" not in signal_source

    module = _module()
    if hasattr(module, "route_governed_support_evidence_v0"):
        route_source = inspect.getsource(module.route_governed_support_evidence_v0)
        assert "support_sufficient" not in route_source
