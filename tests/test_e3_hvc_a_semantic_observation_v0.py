from __future__ import annotations

import copy
import importlib
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
VISIBLE = ROOT / "evaluations/e3_hvc_a_semantic_observation_v0/visible_cases.json"
GROUND_TRUTH = ROOT / "evaluations/e3_hvc_a_semantic_observation_v0/ground_truth.json"


def _module():
    return importlib.import_module("malak.capabilities._engineering_analysis")


def _api():
    module = _module()
    required = (
        "SemanticMaterialBearingV0",
        "SemanticStanceV0",
        "SemanticScopeDependencyV0",
        "SemanticCoverageV0",
        "SemanticObservationV0",
        "project_hvc_a_visible_semantic_observation_case_v0",
        "validate_hvc_a_semantic_observation_v0",
    )
    for name in required:
        assert hasattr(module, name), f"missing HVC-A contract symbol: {name}"
    return module


def _data():
    return json.loads(VISIBLE.read_text(encoding="utf-8")), json.loads(
        GROUND_TRUTH.read_text(encoding="utf-8")
    )


def _case(case_id: str):
    visible, hidden = _data()
    v = next(item for item in visible["cases"] if item["case_id"] == case_id)
    h = next(item for item in hidden["cases"] if item["case_id"] == case_id)
    return v, h


def _observation(module, visible: dict, hidden: dict, **changes):
    value = dict(
        policy_version=visible["policy_version"],
        baseline_commit=visible["baseline_commit"],
        focus_id=visible["focus_id"],
        evidence_set_digest=visible["evidence_set_digest"],
        relation_id=visible["relation_id"],
        finding_fingerprint=visible["finding_fingerprint"],
        evidence_ref=visible["evidence_ref"],
        claim_part_id=visible.get("claim_part_id"),
        material_bearing=module.SemanticMaterialBearingV0(
            hidden["expected_material_bearing"]
        ),
        semantic_stance=module.SemanticStanceV0(
            hidden["expected_semantic_stance"]
        ),
        scope_dependency=module.SemanticScopeDependencyV0(
            hidden["expected_scope_dependency"]
        ),
        coverage=module.SemanticCoverageV0(hidden["expected_coverage"]),
        rationale="bounded audit rationale",
    )
    value.update(changes)
    return module.SemanticObservationV0(**value)


def test_red_hvc_a_01_public_contract_symbols_exist() -> None:
    _api()


def test_red_hvc_a_02_enum_domains_are_exact() -> None:
    module = _api()
    assert {x.value for x in module.SemanticMaterialBearingV0} == {
        "MATERIAL", "NON_MATERIAL", "UNKNOWN"
    }
    assert {x.value for x in module.SemanticStanceV0} == {
        "SUPPORTS", "LIMITS", "CONTRADICTS", "UNKNOWN"
    }
    assert {x.value for x in module.SemanticScopeDependencyV0} == {
        "NONE", "EXTERNAL_REQUIRED", "UNKNOWN"
    }
    assert {x.value for x in module.SemanticCoverageV0} == {
        "FULL", "PARTIAL", "UNKNOWN"
    }


def test_red_hvc_a_03_hidden_labels_are_absent_from_visible_cases() -> None:
    visible, _ = _data()
    forbidden = {
        "expected_material_bearing", "expected_semantic_stance",
        "expected_scope_dependency", "expected_coverage", "expected_outcome",
        "expected_reason_codes", "case_class", "reviewer_annotations",
        "qualification_thresholds", "ground_truth", "oracle_label",
    }
    raw = json.dumps(visible, ensure_ascii=False)
    assert all(key not in raw for key in forbidden)


@pytest.mark.parametrize("case_id", [f"HVC-A-C{i:02d}" for i in range(1, 11)])
def test_red_hvc_a_04_ground_truth_observations_validate(case_id: str) -> None:
    module = _api()
    visible, hidden = _case(case_id)
    projected = module.project_hvc_a_visible_semantic_observation_case_v0(visible)
    observation = _observation(module, visible, hidden)
    assert module.validate_hvc_a_semantic_observation_v0(observation, projected) is observation
    assert observation.authority_effect == "none"
    assert not hasattr(observation, "support_sufficient")


def test_red_hvc_a_05_non_material_cannot_claim_semantic_support() -> None:
    module = _api()
    visible, hidden = _case("HVC-A-C03")
    with pytest.raises(ValueError):
        _observation(
            module, visible, hidden,
            semantic_stance=module.SemanticStanceV0.SUPPORTS,
        )


def test_red_hvc_a_06_partial_requires_material_supports() -> None:
    module = _api()
    visible, hidden = _case("HVC-A-C05")
    with pytest.raises(ValueError):
        _observation(
            module, visible, hidden,
            semantic_stance=module.SemanticStanceV0.LIMITS,
            coverage=module.SemanticCoverageV0.PARTIAL,
        )


@pytest.mark.parametrize("case_id", ["HVC-A-C06", "HVC-A-C07"])
def test_red_hvc_a_07_limits_and_contradiction_have_unknown_coverage(case_id: str) -> None:
    module = _api()
    visible, hidden = _case(case_id)
    observation = _observation(module, visible, hidden)
    assert observation.coverage is module.SemanticCoverageV0.UNKNOWN


def test_red_hvc_a_08_scope_none_does_not_create_support() -> None:
    module = _api()
    visible, hidden = _case("HVC-A-C03")
    observation = _observation(module, visible, hidden)
    assert observation.scope_dependency is module.SemanticScopeDependencyV0.NONE
    assert observation.semantic_stance is module.SemanticStanceV0.UNKNOWN


def test_red_hvc_a_09_unknown_scope_cannot_be_coerced_to_none() -> None:
    module = _api()
    visible, hidden = _case("HVC-A-C09")
    observation = _observation(module, visible, hidden)
    assert observation.scope_dependency is module.SemanticScopeDependencyV0.UNKNOWN


def test_red_hvc_a_10_evidence_ref_must_resolve_inside_visible_case() -> None:
    module = _api()
    visible, hidden = _case("HVC-A-C01")
    observation = _observation(module, visible, hidden, evidence_ref="R404")
    with pytest.raises(ValueError):
        module.validate_hvc_a_semantic_observation_v0(observation, visible)


def test_red_hvc_a_11_binding_drift_is_rejected() -> None:
    module = _api()
    visible, hidden = _case("HVC-A-C01")
    observation = _observation(module, visible, hidden, finding_fingerprint="f" * 64)
    with pytest.raises(ValueError):
        module.validate_hvc_a_semantic_observation_v0(observation, visible)


def test_red_hvc_a_12_projection_fails_closed_on_hidden_key_leakage() -> None:
    module = _api()
    visible, _ = _case("HVC-A-C01")
    leaked = copy.deepcopy(visible)
    leaked["expected_coverage"] = "FULL"
    with pytest.raises(ValueError):
        module.project_hvc_a_visible_semantic_observation_case_v0(leaked)


def test_red_hvc_a_13_root_claim_and_upstream_claim_part_remain_distinct() -> None:
    module = _api()
    root, root_gt = _case("HVC-A-C01")
    part, part_gt = _case("HVC-A-C10")
    assert _observation(module, root, root_gt).claim_part_id is None
    assert _observation(module, part, part_gt).claim_part_id == "clause-orchestration"


def test_red_hvc_a_14_hvc_a_does_not_accept_observation_sets() -> None:
    module = _api()
    visible, hidden = _case("HVC-A-C01")
    observation = _observation(module, visible, hidden)
    with pytest.raises((TypeError, ValueError)):
        module.validate_hvc_a_semantic_observation_v0([observation], visible)


@pytest.mark.parametrize(
    "left,right",
    [
        ("HVC-A-C01", "HVC-A-C02"),
        ("HVC-A-C03", "HVC-A-C04"),
        ("HVC-A-C04", "HVC-A-C05"),
        ("HVC-A-C06", "HVC-A-C07"),
        ("HVC-A-C08", "HVC-A-C09"),
    ],
)
def test_red_hvc_a_15_ground_truth_boundaries_are_discriminable(left: str, right: str) -> None:
    _, lhs = _case(left)
    _, rhs = _case(right)
    dimensions = (
        "expected_material_bearing",
        "expected_semantic_stance",
        "expected_scope_dependency",
        "expected_coverage",
    )
    assert tuple(lhs[k] for k in dimensions) != tuple(rhs[k] for k in dimensions)

def test_red_hvc_a_16_structural_adversarials_are_frozen_in_ground_truth() -> None:
    _, hidden = _data()
    vectors = {item["adversarial_id"]: item for item in hidden["contract_adversarials"]}
    assert set(vectors) == {"HVC-A-A01", "HVC-A-A02", "HVC-A-A03", "HVC-A-A04"}
    assert all(item["expected_validation"] == "INVALID" for item in vectors.values())
    assert all(item["authority_effect"] == "none" for item in vectors.values())


def test_red_hvc_a_17_missing_material_vector_fails_before_semantic_unknown() -> None:
    module = _api()
    visible, _ = _case("HVC-A-C09")
    invalid = copy.deepcopy(visible)
    invalid["evidence_material_by_ref"].pop("R1")
    with pytest.raises(ValueError):
        module.project_hvc_a_visible_semantic_observation_case_v0(invalid)


def test_red_hvc_a_18_binding_drift_vector_fails_closed() -> None:
    module = _api()
    visible, hidden = _case("HVC-A-C01")
    observation = _observation(module, visible, hidden, finding_fingerprint="f" * 64)
    with pytest.raises(ValueError):
        module.validate_hvc_a_semantic_observation_v0(observation, visible)


def test_red_hvc_a_19_duplicate_observation_vector_is_outside_hvc_a() -> None:
    module = _api()
    visible, hidden = _case("HVC-A-C01")
    observation = _observation(module, visible, hidden)
    with pytest.raises((TypeError, ValueError)):
        module.validate_hvc_a_semantic_observation_v0([observation, observation], visible)


def test_red_hvc_a_20_unknown_enum_vector_is_contract_invalid() -> None:
    module = _api()
    with pytest.raises(ValueError):
        module.SemanticStanceV0("MAYBE")

def test_red_hvc_a_21_root_claim_allows_claim_part_id_to_be_absent() -> None:
    module = _api()
    visible, hidden = _case("HVC-A-C01")
    assert "claim_part_id" not in visible
    projected = module.project_hvc_a_visible_semantic_observation_case_v0(visible)
    assert projected["claim_part_id"] is None
    observation = _observation(module, visible, hidden)
    assert observation.claim_part_id is None
    assert module.validate_hvc_a_semantic_observation_v0(observation, visible) is observation


def test_red_hvc_a_22_upstream_claim_part_remains_explicit_when_present() -> None:
    module = _api()
    visible, hidden = _case("HVC-A-C10")
    assert visible["claim_part_id"] == "clause-orchestration"
    projected = module.project_hvc_a_visible_semantic_observation_case_v0(visible)
    assert projected["claim_part_id"] == "clause-orchestration"
    assert _observation(module, visible, hidden).claim_part_id == "clause-orchestration"
