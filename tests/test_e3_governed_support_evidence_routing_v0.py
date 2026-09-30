from __future__ import annotations

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


def _module():
    return importlib.import_module("malak.capabilities._engineering_analysis")


def _routing_api():
    module = _module()
    for name in (
        "GovernedSupportEvidenceRouteKind",
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
        "qualification_id": "qual-1",
        "oracle_id": "oracle-1",
        "oracle_version": "v1",
        "oracle_content_digest": "a" * 64,
        "relation_id": RELATION_ID,
        "evaluation_question_identity": QUESTION_ID,
        "input_contract_identity": INPUT_CONTRACT_DIGEST,
        "output_contract_identity": OUTPUT_CONTRACT_DIGEST,
        "coverage_claim": "FULL",
        "authority_effect": "none",
    }
    values.update(changes)
    return module.GovernedDeterministicOracleQualificationV0(**values)


def _oracle(module, **changes):
    values = {
        "oracle_id": "oracle-1",
        "oracle_version": "v1",
        "oracle_content_digest": "a" * 64,
        "relation_id": RELATION_ID,
        "evaluation_question_identity": QUESTION_ID,
        "input_contract_identity": INPUT_CONTRACT_DIGEST,
        "output_contract_identity": OUTPUT_CONTRACT_DIGEST,
        "coverage_claim": "FULL",
        "qualification": _qualification(module),
        "authority_effect": "none",
        "side_effect_class": "NONE",
    }
    values.update(changes)
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
    assert result.authority_effect == "none"


def test_red_r03_partial_oracle_never_routes_deterministic() -> None:
    module = _routing_api()
    try:
        partial_qualification = _qualification(module, coverage_claim="PARTIAL")
        partial = _oracle(
            module,
            coverage_claim="PARTIAL",
            qualification=partial_qualification,
        )
    except (TypeError, ValueError):
        return

    result = _route(module, oracles=(partial,))
    assert result.route_kind is None or result.route_kind.value != "DETERMINISTIC"


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
    assert result.authority_effect == "none"


def test_red_r07_stale_oracle_qualification_cannot_route_deterministic() -> None:
    module = _routing_api()
    stale = _qualification(module, oracle_content_digest="5" * 64)
    try:
        oracle = _oracle(module, qualification=stale)
    except (TypeError, ValueError):
        return

    result = _route(module, oracles=(oracle,))
    assert result.route_kind is None or result.route_kind.value != "DETERMINISTIC"


def test_red_r08_multiple_eligible_full_oracles_fail_closed() -> None:
    module = _routing_api()
    first = _oracle(module)
    second_qualification = _qualification(
        module,
        qualification_id="qual-2",
        oracle_id="oracle-2",
        oracle_content_digest="c" * 64,
    )
    second = _oracle(
        module,
        oracle_id="oracle-2",
        oracle_content_digest="c" * 64,
        qualification=second_qualification,
    )
    result = _route(module, oracles=(first, second))
    assert result.route_kind is None


def test_red_r09_relation_mismatch_cannot_route_deterministic() -> None:
    module = _routing_api()
    mismatch_q = _qualification(module, relation_id="U01.KERNEL_RESPONSIBILITY")
    try:
        mismatch = _oracle(
            module,
            relation_id="U01.KERNEL_RESPONSIBILITY",
            qualification=mismatch_q,
        )
    except (TypeError, ValueError):
        return

    result = _route(module, oracles=(mismatch,))
    assert result.route_kind is None or result.route_kind.value != "DETERMINISTIC"


def test_red_r10_evaluation_question_drift_invalidates_prior_routing() -> None:
    module = _routing_api()
    result = _route(
        module,
        evaluation_question_identity="6" * 64,
    )
    assert result.route_kind is None


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


def _blind_case() -> dict[str, object]:
    return {
        "input_id": "C01.I01",
        "subject": {
            "relation_id": RELATION_ID,
            "statement": "Capability routing follows the governed Kernel path.",
        },
        "repository_evidence": [
            {"ref": "R1", "text": "bounded repository material"}
        ],
        "knowledge_evidence": [
            {"ref": "K1", "text": "bounded knowledge material"}
        ],
        "binding_expectation": {"binding_kind": "NONE"},
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
    assert projected["input_id"] == case_input["input_id"]
    assert projected["subject"] == case_input["subject"]
    assert projected["repository_evidence"] == case_input["repository_evidence"]
    assert projected["knowledge_evidence"] == case_input["knowledge_evidence"]
    assert projected["binding_expectation"] == case_input["binding_expectation"]


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
