from __future__ import annotations

import copy
import hashlib
import importlib
import json
from dataclasses import replace
from pathlib import Path

import pytest

from malak.capabilities._engineering_evidence import (
    EvidenceSelector,
    EvidenceSelectorResult,
    FocusedEngineeringEvidenceBundle,
    GovernedEngineeringEvidenceFocus,
    GovernedEngineeringRelation,
)


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
        "bind_hvc_a_semantic_observation_case_v0",
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


def _focus(visible: dict) -> GovernedEngineeringEvidenceFocus:
    return GovernedEngineeringEvidenceFocus(
        focus_id=visible["focus_id"],
        focus_label="HVC-A bound-input fixture",
        subject="Kernel",
        repository_required_selectors=(),
        knowledge_required_selectors=(),
        supplemental_terms=(),
        supplemental_max_matches_per_kind=1,
        max_evidence_line_bytes=2048,
        governed_relations=(
            GovernedEngineeringRelation(
                relation_id=visible["relation_id"],
                relation_label="HVC-A fixture relation",
                evaluation_question="Does the evidence materially bear on the claim?",
            ),
        ),
    )


def _focused_digest(
    *,
    visible: dict,
    focus: GovernedEngineeringEvidenceFocus,
    repository_evidence: tuple[dict[str, object], ...],
    knowledge_evidence: tuple[dict[str, object], ...] = (),
    selector_results: tuple[EvidenceSelectorResult, ...] = (),
    supplemental_truncated: bool = False,
) -> str:
    payload = {
        "baseline_commit": visible["baseline_commit"],
        "focus_id": focus.focus_id,
        "subject": focus.subject,
        "selector_results": [
            {
                "source_kind": result.source_kind,
                "selector_kind": result.selector_kind,
                "selector_value": result.selector_value,
                "status": result.status,
                "matched_paths": list(result.matched_paths),
                "match_count": result.match_count,
                "selected_count": result.selected_count,
            }
            for result in selector_results
        ],
        "repository_evidence": [
            {key: value for key, value in item.items() if key != "ref"}
            for item in repository_evidence
        ],
        "knowledge_evidence": [
            {key: value for key, value in item.items() if key != "ref"}
            for item in knowledge_evidence
        ],
        "supplemental_truncated": supplemental_truncated,
        "authority_effect": "none",
        "governed_relations": [
            {
                "relation_id": relation.relation_id,
                "relation_label": relation.relation_label,
                "evaluation_question": relation.evaluation_question,
            }
            for relation in focus.governed_relations
        ],
    }
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def _bound_fixture(
    module,
    visible: dict,
    *,
    claim: str | None = None,
    material: str | None = None,
    claim_part_id: str | None = None,
    reuse_digest: str | None = None,
    include_evidence: bool = True,
    evidence_ref: str = "R1",
):
    focus = _focus(visible)
    repository_evidence: tuple[dict[str, object], ...]
    if include_evidence:
        repository_evidence = (
            {
                "ref": "R1",
                "path": "tests/hvc_a_fixture.md",
                "blob_sha": "b" * 40,
                "line_number": 1,
                "line": (
                    material
                    if material is not None
                    else visible["evidence_material_by_ref"]["R1"]
                ),
                "line_truncated": False,
            },
        )
    else:
        repository_evidence = ()

    digest = reuse_digest or _focused_digest(
        visible=visible,
        focus=focus,
        repository_evidence=repository_evidence,
    )
    bundle = FocusedEngineeringEvidenceBundle(
        baseline_commit=visible["baseline_commit"],
        focus_id=focus.focus_id,
        subject=focus.subject,
        repository_evidence=repository_evidence,
        knowledge_evidence=(),
        selector_results=(),
        repository_match_count=len(repository_evidence),
        knowledge_match_count=0,
        repository_skipped_unreadable=0,
        context_truncated=False,
        supplemental_truncated=False,
        complete=True,
        evidence_set_digest=digest,
        authority_effect="none",
    )
    finding = module._Finding(
        classification="UNRESOLVED",
        statement=claim if claim is not None else visible["claim"],
        rationale="bounded upstream finding",
        evidence_refs=("R1",),
        relation_id=visible["relation_id"],
        supporting_repository_refs=("R1",),
        supporting_knowledge_refs=(),
        limiting_or_counterevidence_refs=(),
        uncertainty_basis="INSUFFICIENT_SUPPLIED_EVIDENCE",
        claim_part_id=claim_part_id,
    )
    return module.bind_hvc_a_semantic_observation_case_v0(
        case_id=visible["case_id"],
        evidence_focus=focus,
        evidence_bundle=bundle,
        finding=finding,
        evidence_ref=evidence_ref,
    )


def _observation(module, binding: dict, hidden: dict, **changes):
    value = dict(
        policy_version=binding["policy_version"],
        baseline_commit=binding["baseline_commit"],
        focus_id=binding["focus_id"],
        evidence_set_digest=binding["evidence_set_digest"],
        relation_id=binding["relation_id"],
        finding_fingerprint=binding["finding_fingerprint"],
        evidence_ref=binding["evidence_ref"],
        claim_part_id=binding.get("claim_part_id"),
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


@pytest.mark.parametrize("case_id", [f"HVC-A-C{i:02d}" for i in range(1, 10)])
def test_red_hvc_a_04_bound_ground_truth_observations_validate(case_id: str) -> None:
    module = _api()
    visible, hidden = _case(case_id)
    bound = _bound_fixture(module, visible)
    projected = module.project_hvc_a_visible_semantic_observation_case_v0(bound)
    observation = _observation(module, projected, hidden)
    assert module.validate_hvc_a_semantic_observation_v0(observation, bound) is observation
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


def test_red_hvc_a_10_evidence_ref_must_resolve_inside_bound_packet() -> None:
    module = _api()
    visible, _ = _case("HVC-A-C01")
    with pytest.raises(ValueError):
        _bound_fixture(module, visible, evidence_ref="R404")


def test_red_hvc_a_11_observation_binding_drift_is_rejected() -> None:
    module = _api()
    visible, hidden = _case("HVC-A-C01")
    bound = _bound_fixture(module, visible)
    projected = module.project_hvc_a_visible_semantic_observation_case_v0(bound)
    observation = _observation(
        module,
        projected,
        hidden,
        finding_fingerprint="f" * 64,
    )
    with pytest.raises(ValueError):
        module.validate_hvc_a_semantic_observation_v0(observation, bound)


def test_red_hvc_a_12_free_visible_dict_is_not_a_provenance_boundary() -> None:
    module = _api()
    visible, hidden = _case("HVC-A-C01")
    with pytest.raises(TypeError):
        module.project_hvc_a_visible_semantic_observation_case_v0(visible)
    observation = _observation(module, visible, hidden)
    with pytest.raises(TypeError):
        module.validate_hvc_a_semantic_observation_v0(observation, visible)


def test_red_hvc_a_13_root_claim_and_contract_claim_part_remain_distinct() -> None:
    module = _api()
    root, root_gt = _case("HVC-A-C01")
    part, part_gt = _case("HVC-A-C10")
    assert _observation(module, root, root_gt).claim_part_id is None
    assert _observation(module, part, part_gt).claim_part_id == "clause-orchestration"


def test_red_hvc_a_14_hvc_a_does_not_accept_observation_sets() -> None:
    module = _api()
    visible, hidden = _case("HVC-A-C01")
    bound = _bound_fixture(module, visible)
    projected = module.project_hvc_a_visible_semantic_observation_case_v0(bound)
    observation = _observation(module, projected, hidden)
    with pytest.raises((TypeError, ValueError)):
        module.validate_hvc_a_semantic_observation_v0(
            [observation, observation],
            bound,
        )


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
    with pytest.raises(ValueError):
        _bound_fixture(module, visible, include_evidence=False)


def test_red_hvc_a_18_binding_drift_vector_fails_closed() -> None:
    module = _api()
    visible, hidden = _case("HVC-A-C01")
    bound = _bound_fixture(module, visible)
    projected = module.project_hvc_a_visible_semantic_observation_case_v0(bound)
    observation = _observation(
        module,
        projected,
        hidden,
        finding_fingerprint="f" * 64,
    )
    with pytest.raises(ValueError):
        module.validate_hvc_a_semantic_observation_v0(observation, bound)


def test_red_hvc_a_19_duplicate_observation_vector_is_outside_hvc_a() -> None:
    module = _api()
    visible, hidden = _case("HVC-A-C01")
    bound = _bound_fixture(module, visible)
    projected = module.project_hvc_a_visible_semantic_observation_case_v0(bound)
    observation = _observation(module, projected, hidden)
    with pytest.raises((TypeError, ValueError)):
        module.validate_hvc_a_semantic_observation_v0(
            [observation, observation],
            bound,
        )


def test_red_hvc_a_20_unknown_enum_vector_is_contract_invalid() -> None:
    module = _api()
    with pytest.raises(ValueError):
        module.SemanticStanceV0("MAYBE")


def test_red_hvc_a_21_root_claim_projection_omits_claim_part_id() -> None:
    module = _api()
    visible, hidden = _case("HVC-A-C01")
    bound = _bound_fixture(module, visible)
    projected = module.project_hvc_a_visible_semantic_observation_case_v0(bound)
    assert "claim_part_id" not in projected
    observation = _observation(module, projected, hidden)
    assert observation.claim_part_id is None
    assert module.validate_hvc_a_semantic_observation_v0(observation, bound) is observation


def test_red_hvc_a_22_contract_can_represent_upstream_claim_part() -> None:
    module = _api()
    visible, hidden = _case("HVC-A-C10")
    observation = _observation(module, visible, hidden)
    assert observation.claim_part_id == "clause-orchestration"


def test_hvc_a_f03_01_changed_claim_cannot_preserve_finding_identity() -> None:
    module = _api()
    visible, _ = _case("HVC-A-C01")
    original = _bound_fixture(module, visible)
    changed = _bound_fixture(
        module,
        visible,
        claim="Kernel grants unrestricted persistence and deployment authority.",
    )
    original_projection = module.project_hvc_a_visible_semantic_observation_case_v0(
        original
    )
    changed_projection = module.project_hvc_a_visible_semantic_observation_case_v0(
        changed
    )
    assert original_projection["finding_fingerprint"] != changed_projection[
        "finding_fingerprint"
    ]


def test_hvc_a_f03_02_changed_material_with_old_digest_is_rejected() -> None:
    module = _api()
    visible, _ = _case("HVC-A-C01")
    original = _bound_fixture(module, visible)
    original_projection = module.project_hvc_a_visible_semantic_observation_case_v0(
        original
    )
    with pytest.raises(ValueError):
        _bound_fixture(
            module,
            visible,
            material="Arbitrary substituted content unrelated to the original evidence.",
            reuse_digest=original_projection["evidence_set_digest"],
        )


def test_hvc_a_f03_03_changed_material_requires_new_evidence_identity() -> None:
    module = _api()
    visible, _ = _case("HVC-A-C01")
    original = _bound_fixture(module, visible)
    changed = _bound_fixture(
        module,
        visible,
        material="Arbitrary substituted content unrelated to the original evidence.",
    )
    original_projection = module.project_hvc_a_visible_semantic_observation_case_v0(
        original
    )
    changed_projection = module.project_hvc_a_visible_semantic_observation_case_v0(
        changed
    )
    assert original_projection["evidence_set_digest"] != changed_projection[
        "evidence_set_digest"
    ]


def test_hvc_a_f03_04_caller_invented_claim_part_is_rejected_by_bound_input() -> None:
    module = _api()
    visible, _ = _case("HVC-A-C01")
    with pytest.raises(ValueError, match="no authorized upstream claim-part provider"):
        _bound_fixture(
            module,
            visible,
            claim_part_id="caller-invented-part",
        )


def test_hvc_a_f03_05_bound_projection_uses_exact_upstream_material() -> None:
    module = _api()
    visible, _ = _case("HVC-A-C01")
    bound = _bound_fixture(module, visible)
    projected = module.project_hvc_a_visible_semantic_observation_case_v0(bound)
    assert projected["claim"] == visible["claim"]
    assert projected["evidence_material_by_ref"] == visible["evidence_material_by_ref"]


def test_hvc_a_f03_06_bound_evidence_digest_is_recomputed() -> None:
    module = _api()
    visible, _ = _case("HVC-A-C01")
    bound = _bound_fixture(module, visible)
    projected = module.project_hvc_a_visible_semantic_observation_case_v0(bound)
    assert projected["evidence_set_digest"] != visible["evidence_set_digest"]


def test_hvc_a_f03_07_finding_role_ref_must_match_selected_ref() -> None:
    module = _api()
    visible, _ = _case("HVC-A-C01")
    with pytest.raises(ValueError):
        _bound_fixture(module, visible, evidence_ref="K404")


def test_hvc_a_f03_r4_01_bound_object_exposes_no_replaceable_derived_fields() -> None:
    module = _api()
    visible, _ = _case("HVC-A-C01")
    bound = _bound_fixture(module, visible)

    for field_name, value in (
        ("claim", "substituted claim"),
        ("evidence_material", "substituted material"),
        ("claim_part_id", "caller-invented-part"),
        ("finding_fingerprint", "f" * 64),
        ("evidence_set_digest", "e" * 64),
    ):
        with pytest.raises(TypeError):
            replace(bound, **{field_name: value})


def test_hvc_a_f03_r4_02_replaced_finding_recomputes_identity() -> None:
    module = _api()
    visible, _ = _case("HVC-A-C01")
    bound = _bound_fixture(module, visible)
    original = module.project_hvc_a_visible_semantic_observation_case_v0(bound)

    changed_finding = replace(
        bound.finding,
        statement="Kernel grants unrestricted persistence and deployment authority.",
    )
    changed_bound = replace(bound, finding=changed_finding)
    changed = module.project_hvc_a_visible_semantic_observation_case_v0(
        changed_bound
    )

    assert changed["claim"] != original["claim"]
    assert changed["finding_fingerprint"] != original["finding_fingerprint"]
    assert changed["evidence_set_digest"] == original["evidence_set_digest"]


def test_hvc_a_f03_r4_03_replaced_bundle_material_cannot_preserve_digest() -> None:
    module = _api()
    visible, _ = _case("HVC-A-C01")
    bound = _bound_fixture(module, visible)
    original = module.project_hvc_a_visible_semantic_observation_case_v0(bound)

    changed_item = dict(bound.evidence_bundle.repository_evidence[0])
    changed_item["line"] = "Arbitrary substituted content unrelated to the original evidence."
    changed_bundle = replace(
        bound.evidence_bundle,
        repository_evidence=(changed_item,),
    )
    changed_bound = replace(bound, evidence_bundle=changed_bundle)

    with pytest.raises(ValueError, match="evidence_set_digest"):
        module.project_hvc_a_visible_semantic_observation_case_v0(changed_bound)

    assert original["authority_effect"] == "none"


def test_hvc_a_f03_r4_04_invented_claim_part_in_replaced_finding_is_rejected() -> None:
    module = _api()
    visible, _ = _case("HVC-A-C01")
    bound = _bound_fixture(module, visible)
    changed_bound = replace(
        bound,
        finding=replace(bound.finding, claim_part_id="caller-invented-part"),
    )
    with pytest.raises(ValueError, match="no authorized upstream claim-part provider"):
        module.project_hvc_a_visible_semantic_observation_case_v0(changed_bound)


def test_hvc_a_f03_r4_05_permuted_ref_to_material_assignment_is_rejected() -> None:
    module = _api()
    visible, _ = _case("HVC-A-C01")
    focus = _focus(visible)
    canonical_evidence = (
        {
            "ref": "R1",
            "path": "tests/a_hvc_a_fixture.md",
            "blob_sha": "a" * 40,
            "line_number": 1,
            "line": "first canonical material",
            "line_truncated": False,
        },
        {
            "ref": "R2",
            "path": "tests/b_hvc_a_fixture.md",
            "blob_sha": "b" * 40,
            "line_number": 1,
            "line": "second canonical material",
            "line_truncated": False,
        },
    )
    digest = _focused_digest(
        visible=visible,
        focus=focus,
        repository_evidence=canonical_evidence,
    )
    permuted_refs = (
        {**canonical_evidence[0], "ref": "R2"},
        {**canonical_evidence[1], "ref": "R1"},
    )
    bundle = FocusedEngineeringEvidenceBundle(
        baseline_commit=visible["baseline_commit"],
        focus_id=focus.focus_id,
        subject=focus.subject,
        repository_evidence=permuted_refs,
        knowledge_evidence=(),
        selector_results=(),
        repository_match_count=2,
        knowledge_match_count=0,
        repository_skipped_unreadable=0,
        context_truncated=False,
        supplemental_truncated=False,
        complete=True,
        evidence_set_digest=digest,
        authority_effect="none",
    )
    finding = module._Finding(
        classification="UNRESOLVED",
        statement=visible["claim"],
        rationale="bounded upstream finding",
        evidence_refs=("R1", "R2"),
        relation_id=visible["relation_id"],
        supporting_repository_refs=("R1", "R2"),
        supporting_knowledge_refs=(),
        limiting_or_counterevidence_refs=(),
        uncertainty_basis="INSUFFICIENT_SUPPLIED_EVIDENCE",
    )
    with pytest.raises(ValueError, match="ref assignment is not canonical"):
        module.bind_hvc_a_semantic_observation_case_v0(
            case_id=visible["case_id"],
            evidence_focus=focus,
            evidence_bundle=bundle,
            finding=finding,
            evidence_ref="R1",
        )


def test_hvc_a_f03_r4_06_noncanonical_evidence_order_is_rejected() -> None:
    module = _api()
    visible, _ = _case("HVC-A-C01")
    focus = _focus(visible)
    evidence = (
        {
            "ref": "R1",
            "path": "tests/b_hvc_a_fixture.md",
            "blob_sha": "b" * 40,
            "line_number": 1,
            "line": "second material",
            "line_truncated": False,
        },
        {
            "ref": "R2",
            "path": "tests/a_hvc_a_fixture.md",
            "blob_sha": "a" * 40,
            "line_number": 1,
            "line": "first material",
            "line_truncated": False,
        },
    )
    digest = _focused_digest(
        visible=visible,
        focus=focus,
        repository_evidence=evidence,
    )
    bundle = FocusedEngineeringEvidenceBundle(
        baseline_commit=visible["baseline_commit"],
        focus_id=focus.focus_id,
        subject=focus.subject,
        repository_evidence=evidence,
        knowledge_evidence=(),
        selector_results=(),
        repository_match_count=2,
        knowledge_match_count=0,
        repository_skipped_unreadable=0,
        context_truncated=False,
        supplemental_truncated=False,
        complete=True,
        evidence_set_digest=digest,
        authority_effect="none",
    )
    finding = module._Finding(
        classification="UNRESOLVED",
        statement=visible["claim"],
        rationale="bounded upstream finding",
        evidence_refs=("R1", "R2"),
        relation_id=visible["relation_id"],
        supporting_repository_refs=("R1", "R2"),
        supporting_knowledge_refs=(),
        limiting_or_counterevidence_refs=(),
        uncertainty_basis="INSUFFICIENT_SUPPLIED_EVIDENCE",
    )
    with pytest.raises(ValueError, match="canonical order"):
        module.bind_hvc_a_semantic_observation_case_v0(
            case_id=visible["case_id"],
            evidence_focus=focus,
            evidence_bundle=bundle,
            finding=finding,
            evidence_ref="R1",
        )


def test_hvc_a_f03_r4_07_replaced_evidence_refs_cannot_escape_fingerprinted_roles() -> None:
    module = _api()
    visible, _ = _case("HVC-A-C01")
    focus = _focus(visible)
    evidence = (
        {
            "ref": "R1",
            "path": "tests/a_hvc_a_fixture.md",
            "blob_sha": "a" * 40,
            "line_number": 1,
            "line": "fingerprinted material",
            "line_truncated": False,
        },
        {
            "ref": "R2",
            "path": "tests/b_hvc_a_fixture.md",
            "blob_sha": "b" * 40,
            "line_number": 1,
            "line": "unfingerprinted alternate material",
            "line_truncated": False,
        },
    )
    digest = _focused_digest(
        visible=visible,
        focus=focus,
        repository_evidence=evidence,
    )
    bundle = FocusedEngineeringEvidenceBundle(
        baseline_commit=visible["baseline_commit"],
        focus_id=focus.focus_id,
        subject=focus.subject,
        repository_evidence=evidence,
        knowledge_evidence=(),
        selector_results=(),
        repository_match_count=2,
        knowledge_match_count=0,
        repository_skipped_unreadable=0,
        context_truncated=False,
        supplemental_truncated=False,
        complete=True,
        evidence_set_digest=digest,
        authority_effect="none",
    )
    finding = module._Finding(
        classification="UNRESOLVED",
        statement=visible["claim"],
        rationale="bounded upstream finding",
        evidence_refs=("R1",),
        relation_id=visible["relation_id"],
        supporting_repository_refs=("R1",),
        supporting_knowledge_refs=(),
        limiting_or_counterevidence_refs=(),
        uncertainty_basis="INSUFFICIENT_SUPPLIED_EVIDENCE",
    )
    bound = module.bind_hvc_a_semantic_observation_case_v0(
        case_id=visible["case_id"],
        evidence_focus=focus,
        evidence_bundle=bundle,
        finding=finding,
        evidence_ref="R1",
    )
    tampered = replace(
        bound,
        finding=replace(bound.finding, evidence_refs=("R1", "R2")),
        evidence_ref="R2",
    )
    with pytest.raises(
        ValueError,
        match="evidence_refs must equal structured role-bound refs",
    ):
        module.project_hvc_a_visible_semantic_observation_case_v0(tampered)


def test_hvc_a_f03_r4_08_role_overlap_is_rejected_after_replace() -> None:
    module = _api()
    visible, _ = _case("HVC-A-C01")
    bound = _bound_fixture(module, visible)
    tampered_finding = replace(
        bound.finding,
        evidence_refs=("R1", "R1"),
        limiting_or_counterevidence_refs=("R1",),
    )
    tampered = replace(bound, finding=tampered_finding)
    with pytest.raises(ValueError):
        module.project_hvc_a_visible_semantic_observation_case_v0(tampered)


def _r5_selector_result(status: str) -> EvidenceSelectorResult:
    return EvidenceSelectorResult(
        source_kind="repository",
        selector_kind="EXACT_PATH",
        selector_value="tests/hvc_a_fixture.md",
        status=status,
        matched_paths=("tests/hvc_a_fixture.md",),
        match_count=2 if status == "TRUNCATED" else 1,
        selected_count=1,
    )


def _r5_bundle_with_selector_status(
    visible: dict,
    *,
    status: str,
    complete: bool,
    context_truncated: bool,
) -> tuple[
    GovernedEngineeringEvidenceFocus,
    FocusedEngineeringEvidenceBundle,
]:
    focus = replace(
        _focus(visible),
        repository_required_selectors=(
            EvidenceSelector(
                kind="EXACT_PATH",
                value="tests/hvc_a_fixture.md",
                terms=("support",),
                max_matches=8,
            ),
        ),
    )
    repository_evidence = (
        {
            "ref": "R1",
            "path": "tests/hvc_a_fixture.md",
            "blob_sha": "b" * 40,
            "line_number": 1,
            "line": visible["evidence_material_by_ref"]["R1"],
            "line_truncated": False,
            "required": True,
        },
    )
    selector_result = _r5_selector_result(status)
    digest = _focused_digest(
        visible=visible,
        focus=focus,
        repository_evidence=repository_evidence,
        selector_results=(selector_result,),
    )
    bundle = FocusedEngineeringEvidenceBundle(
        baseline_commit=visible["baseline_commit"],
        focus_id=focus.focus_id,
        subject=focus.subject,
        repository_evidence=repository_evidence,
        knowledge_evidence=(),
        selector_results=(selector_result,),
        repository_match_count=1,
        knowledge_match_count=0,
        repository_skipped_unreadable=0,
        context_truncated=context_truncated,
        supplemental_truncated=False,
        complete=complete,
        evidence_set_digest=digest,
        authority_effect="none",
    )
    return focus, bundle


def _r5_finding(module, visible: dict):
    return module._Finding(
        classification="UNRESOLVED",
        statement=visible["claim"],
        rationale="bounded upstream finding",
        evidence_refs=("R1",),
        relation_id=visible["relation_id"],
        supporting_repository_refs=("R1",),
        supporting_knowledge_refs=(),
        limiting_or_counterevidence_refs=(),
        uncertainty_basis="INSUFFICIENT_SUPPLIED_EVIDENCE",
    )


def test_hvc_a_f03_r5_01_truncated_required_selector_cannot_fake_completeness() -> None:
    module = _api()
    visible, _ = _case("HVC-A-C01")
    focus, original_bundle = _r5_bundle_with_selector_status(
        visible,
        status="TRUNCATED",
        complete=False,
        context_truncated=True,
    )

    with pytest.raises(ValueError, match="requires complete focused evidence"):
        module.bind_hvc_a_semantic_observation_case_v0(
            case_id=visible["case_id"],
            evidence_focus=focus,
            evidence_bundle=original_bundle,
            finding=_r5_finding(module, visible),
            evidence_ref="R1",
        )

    tampered = replace(
        original_bundle,
        complete=True,
        context_truncated=False,
    )
    assert tampered.evidence_set_digest == original_bundle.evidence_set_digest

    with pytest.raises(ValueError, match="complete flag does not match selector_results"):
        module.bind_hvc_a_semantic_observation_case_v0(
            case_id=visible["case_id"],
            evidence_focus=focus,
            evidence_bundle=tampered,
            finding=_r5_finding(module, visible),
            evidence_ref="R1",
        )


def test_hvc_a_f03_r5_02_context_truncated_must_match_selector_results() -> None:
    module = _api()
    visible, _ = _case("HVC-A-C01")
    focus, bundle = _r5_bundle_with_selector_status(
        visible,
        status="TRUNCATED",
        complete=False,
        context_truncated=False,
    )
    with pytest.raises(
        ValueError,
        match="context_truncated flag does not match selector_results",
    ):
        module.bind_hvc_a_semantic_observation_case_v0(
            case_id=visible["case_id"],
            evidence_focus=focus,
            evidence_bundle=bundle,
            finding=_r5_finding(module, visible),
            evidence_ref="R1",
        )


def test_hvc_a_f03_r5_03_complete_must_match_selector_results() -> None:
    module = _api()
    visible, _ = _case("HVC-A-C01")
    focus, bundle = _r5_bundle_with_selector_status(
        visible,
        status="RESOLVED",
        complete=False,
        context_truncated=False,
    )
    with pytest.raises(
        ValueError,
        match="complete flag does not match selector_results",
    ):
        module.bind_hvc_a_semantic_observation_case_v0(
            case_id=visible["case_id"],
            evidence_focus=focus,
            evidence_bundle=bundle,
            finding=_r5_finding(module, visible),
            evidence_ref="R1",
        )


def test_hvc_a_f03_r5_04_resolved_selector_control_remains_valid() -> None:
    module = _api()
    visible, hidden = _case("HVC-A-C01")
    focus, bundle = _r5_bundle_with_selector_status(
        visible,
        status="RESOLVED",
        complete=True,
        context_truncated=False,
    )
    bound = module.bind_hvc_a_semantic_observation_case_v0(
        case_id=visible["case_id"],
        evidence_focus=focus,
        evidence_bundle=bundle,
        finding=_r5_finding(module, visible),
        evidence_ref="R1",
    )
    projected = module.project_hvc_a_visible_semantic_observation_case_v0(bound)
    observation = _observation(module, projected, hidden)
    assert module.validate_hvc_a_semantic_observation_v0(
        observation,
        bound,
    ) is observation


def _r6_focus_with_two_required_selectors(
    visible: dict,
) -> GovernedEngineeringEvidenceFocus:
    base = _focus(visible)
    return replace(
        base,
        repository_required_selectors=(
            EvidenceSelector(
                kind="EXACT_PATH",
                value="tests/hvc_a_fixture.md",
                terms=("support",),
                max_matches=8,
            ),
            EvidenceSelector(
                kind="EXACT_PATH",
                value="tests/missing.md",
                terms=("missing",),
                max_matches=8,
            ),
        ),
    )


def _r6_repository_evidence(visible: dict) -> tuple[dict[str, object], ...]:
    return (
        {
            "ref": "R1",
            "path": "tests/hvc_a_fixture.md",
            "blob_sha": "b" * 40,
            "line_number": 1,
            "line": visible["evidence_material_by_ref"]["R1"],
            "line_truncated": False,
            "required": True,
        },
    )


def _r6_result(
    *,
    value: str,
    status: str,
    matched_paths: object,
    match_count: object,
    selected_count: object,
    source_kind: str = "repository",
    selector_kind: str = "EXACT_PATH",
) -> EvidenceSelectorResult:
    return EvidenceSelectorResult(
        source_kind=source_kind,
        selector_kind=selector_kind,
        selector_value=value,
        status=status,
        matched_paths=matched_paths,
        match_count=match_count,
        selected_count=selected_count,
    )


def _r6_bundle(
    *,
    visible: dict,
    focus: GovernedEngineeringEvidenceFocus,
    selector_results: tuple[EvidenceSelectorResult, ...],
    complete: bool,
    context_truncated: bool = False,
) -> FocusedEngineeringEvidenceBundle:
    repository_evidence = _r6_repository_evidence(visible)
    digest = _focused_digest(
        visible=visible,
        focus=focus,
        repository_evidence=repository_evidence,
        selector_results=selector_results,
    )
    return FocusedEngineeringEvidenceBundle(
        baseline_commit=visible["baseline_commit"],
        focus_id=focus.focus_id,
        subject=focus.subject,
        repository_evidence=repository_evidence,
        knowledge_evidence=(),
        selector_results=selector_results,
        repository_match_count=1,
        knowledge_match_count=0,
        repository_skipped_unreadable=0,
        context_truncated=context_truncated,
        supplemental_truncated=False,
        complete=complete,
        evidence_set_digest=digest,
        authority_effect="none",
    )


def test_hvc_a_f03_r6_01_omitted_required_selector_is_rejected() -> None:
    module = _api()
    visible, _ = _case("HVC-A-C01")
    focus = _r6_focus_with_two_required_selectors(visible)
    only_resolved = (
        _r6_result(
            value="tests/hvc_a_fixture.md",
            status="RESOLVED",
            matched_paths=("tests/hvc_a_fixture.md",),
            match_count=1,
            selected_count=1,
        ),
    )
    bundle = _r6_bundle(
        visible=visible,
        focus=focus,
        selector_results=only_resolved,
        complete=True,
    )
    with pytest.raises(ValueError, match="exactly correspond"):
        module.bind_hvc_a_semantic_observation_case_v0(
            case_id=visible["case_id"],
            evidence_focus=focus,
            evidence_bundle=bundle,
            finding=_r5_finding(module, visible),
            evidence_ref="R1",
        )


def test_hvc_a_f03_r6_02_empty_results_cannot_self_certify_required_focus() -> None:
    module = _api()
    visible, _ = _case("HVC-A-C01")
    focus = _r6_focus_with_two_required_selectors(visible)
    bundle = _r6_bundle(
        visible=visible,
        focus=focus,
        selector_results=(),
        complete=True,
    )
    with pytest.raises(ValueError, match="exactly correspond"):
        module.bind_hvc_a_semantic_observation_case_v0(
            case_id=visible["case_id"],
            evidence_focus=focus,
            evidence_bundle=bundle,
            finding=_r5_finding(module, visible),
            evidence_ref="R1",
        )


@pytest.mark.parametrize(
    "selector_results",
    [
        (
            _r6_result(
                value="tests/missing.md",
                status="MISSING",
                matched_paths=(),
                match_count=0,
                selected_count=0,
            ),
            _r6_result(
                value="tests/hvc_a_fixture.md",
                status="RESOLVED",
                matched_paths=("tests/hvc_a_fixture.md",),
                match_count=1,
                selected_count=1,
            ),
        ),
        (
            _r6_result(
                value="tests/hvc_a_fixture.md",
                status="RESOLVED",
                matched_paths=("tests/hvc_a_fixture.md",),
                match_count=1,
                selected_count=1,
                source_kind="knowledge",
            ),
            _r6_result(
                value="tests/missing.md",
                status="MISSING",
                matched_paths=(),
                match_count=0,
                selected_count=0,
            ),
        ),
    ],
)
def test_hvc_a_f03_r6_03_required_selector_order_and_source_must_match_focus(
    selector_results: tuple[EvidenceSelectorResult, ...],
) -> None:
    module = _api()
    visible, _ = _case("HVC-A-C01")
    focus = _r6_focus_with_two_required_selectors(visible)
    bundle = _r6_bundle(
        visible=visible,
        focus=focus,
        selector_results=selector_results,
        complete=False,
    )
    with pytest.raises(ValueError, match="exactly correspond"):
        module.bind_hvc_a_semantic_observation_case_v0(
            case_id=visible["case_id"],
            evidence_focus=focus,
            evidence_bundle=bundle,
            finding=_r5_finding(module, visible),
            evidence_ref="R1",
        )


@pytest.mark.parametrize(
    "result",
    [
        _r6_result(
            value="tests/hvc_a_fixture.md",
            status="RESOLVED",
            matched_paths=["tests/hvc_a_fixture.md"],
            match_count=1,
            selected_count=1,
        ),
        _r6_result(
            value="tests/hvc_a_fixture.md",
            status="RESOLVED",
            matched_paths=("tests/hvc_a_fixture.md",),
            match_count=-1,
            selected_count=0,
        ),
        _r6_result(
            value="tests/hvc_a_fixture.md",
            status="RESOLVED",
            matched_paths=("tests/hvc_a_fixture.md",),
            match_count=1,
            selected_count=True,
        ),
    ],
)
def test_hvc_a_f03_r6_04_noncanonical_selector_result_representation_is_rejected(
    result: EvidenceSelectorResult,
) -> None:
    module = _api()
    visible, _ = _case("HVC-A-C01")
    focus = replace(
        _focus(visible),
        repository_required_selectors=(
            EvidenceSelector(
                kind="EXACT_PATH",
                value="tests/hvc_a_fixture.md",
                terms=("support",),
                max_matches=8,
            ),
        ),
    )
    bundle = _r6_bundle(
        visible=visible,
        focus=focus,
        selector_results=(result,),
        complete=True,
    )
    with pytest.raises((TypeError, ValueError)):
        module.bind_hvc_a_semantic_observation_case_v0(
            case_id=visible["case_id"],
            evidence_focus=focus,
            evidence_bundle=bundle,
            finding=_r5_finding(module, visible),
            evidence_ref="R1",
        )


def test_hvc_a_f03_r6_05_valid_required_selector_sequence_preserves_control() -> None:
    module = _api()
    visible, hidden = _case("HVC-A-C01")
    focus = replace(
        _focus(visible),
        repository_required_selectors=(
            EvidenceSelector(
                kind="EXACT_PATH",
                value="tests/hvc_a_fixture.md",
                terms=("support",),
                max_matches=8,
            ),
        ),
    )
    result = _r6_result(
        value="tests/hvc_a_fixture.md",
        status="RESOLVED",
        matched_paths=("tests/hvc_a_fixture.md",),
        match_count=1,
        selected_count=1,
    )
    bundle = _r6_bundle(
        visible=visible,
        focus=focus,
        selector_results=(result,),
        complete=True,
    )
    bound = module.bind_hvc_a_semantic_observation_case_v0(
        case_id=visible["case_id"],
        evidence_focus=focus,
        evidence_bundle=bundle,
        finding=_r5_finding(module, visible),
        evidence_ref="R1",
    )
    projected = module.project_hvc_a_visible_semantic_observation_case_v0(bound)
    observation = _observation(module, projected, hidden)
    assert module.validate_hvc_a_semantic_observation_v0(observation, bound) is observation
