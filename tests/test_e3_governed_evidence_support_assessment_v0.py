from __future__ import annotations

import importlib

import pytest


POLICY_VERSION = "e3-governed-evidence-support/v0"
RELATION_ID = "U01.KERNEL_RESPONSIBILITY"


def _module():
    return importlib.import_module("malak.capabilities._engineering_analysis")


def _api():
    module = _module()
    assert hasattr(module, "GovernedEvidenceSupportAssessmentV0")
    assert hasattr(module, "GovernedEvidenceSupportOutcome")
    assert hasattr(module, "GovernedEvidenceSupportReason")
    assert hasattr(module, "assess_governed_evidence_support_v0")
    assert hasattr(module, "governed_evidence_support_finding_fingerprint")
    return module


def _subject(**changes: object) -> dict[str, object]:
    value: dict[str, object] = {
        "policy_version": POLICY_VERSION,
        "baseline_commit": "b" * 40,
        "focus_id": "U01",
        "evidence_set_digest": "e" * 64,
        "relation_id": RELATION_ID,
        "classification": "ALIGNED",
        "statement": "Core Kernel owns orchestration.",
        "rationale": "Repository implementation and governed knowledge directly agree.",
        "supporting_repository_refs": ("R1",),
        "supporting_knowledge_refs": ("K1",),
        "limiting_or_counterevidence_refs": (),
        "uncertainty_basis": "NONE",
        "repository_evidence": (
            {
                "ref": "R1",
                "path": "src/malak/kernel/core.py",
                "blob_sha": "r" * 40,
                "line_number": 1,
                "text": "class Kernel: # owns orchestration",
            },
        ),
        "knowledge_evidence": (
            {
                "ref": "K1",
                "path": "docs/architecture/kernel.md",
                "blob_sha": "k" * 40,
                "line_number": 1,
                "text": "Core Kernel owns orchestration.",
                "source_class": "APPROVED_SPECIFICATION",
                "authority_class": "normative_subordinate",
            },
        ),
    }
    value.update(changes)
    return value


def _assessment(module, subject: dict[str, object], *, disposition: str = "SUPPORTED"):
    return module.assess_governed_evidence_support_v0(
        **subject,
        assessor_subject_id="independent-test-assessor",
        finding_producer_subject_id="e3-test-producer",
        assessor=lambda _material: {
            "outcome": disposition,
            "reason_codes": (
                ["MATERIAL_SUPPORT_CONFIRMED"]
                if disposition == "SUPPORTED"
                else ["SUPPORTING_REFS_INSUFFICIENT"]
            ),
        },
    )


def test_red_r01_fingerprint_is_stable_for_identical_material() -> None:
    module = _api()
    subject = _subject()
    left = module.governed_evidence_support_finding_fingerprint(**subject)
    right = module.governed_evidence_support_finding_fingerprint(**subject)
    assert left == right
    assert len(left) == 64


@pytest.mark.parametrize(
    "field,value",
    [
        ("statement", "Different statement."),
        ("rationale", "Different rationale."),
        ("relation_id", "U01.CAPABILITY_ROUTING"),
        ("supporting_repository_refs", ("R2",)),
        ("supporting_knowledge_refs", ("K2",)),
    ],
)
def test_red_r02_finding_material_drift_changes_fingerprint(
    field: str, value: object
) -> None:
    module = _api()
    baseline = module.governed_evidence_support_finding_fingerprint(**_subject())
    changed = module.governed_evidence_support_finding_fingerprint(
        **_subject(**{field: value})
    )
    assert changed != baseline


@pytest.mark.parametrize(
    "field,value",
    [
        ("baseline_commit", "c" * 40),
        ("focus_id", "OTHER"),
        ("evidence_set_digest", "d" * 64),
    ],
)
def test_red_r03_subject_binding_mismatch_cannot_yield_supported(
    field: str, value: object
) -> None:
    module = _api()
    subject = _subject()
    expected = {
        "baseline_commit": subject["baseline_commit"],
        "focus_id": subject["focus_id"],
        "evidence_set_digest": subject["evidence_set_digest"],
    }
    subject[field] = value
    result = module.assess_governed_evidence_support_v0(
        **subject,
        expected_binding=expected,
        assessor_subject_id="independent-test-assessor",
        finding_producer_subject_id="e3-test-producer",
        assessor=lambda _material: {
            "outcome": "SUPPORTED",
            "reason_codes": ["MATERIAL_SUPPORT_CONFIRMED"],
        },
    )
    assert result.outcome.value != "SUPPORTED"


def test_red_r04_missing_resolved_ref_material_cannot_yield_supported() -> None:
    module = _api()
    result = _assessment(
        module,
        _subject(repository_evidence=()),
    )
    assert result.outcome.value != "SUPPORTED"


def test_red_r05_exact_material_support_can_yield_supported() -> None:
    module = _api()
    result = _assessment(module, _subject())
    assert result.outcome.value == "SUPPORTED"
    assert [item.value for item in result.reason_codes] == [
        "MATERIAL_SUPPORT_CONFIRMED"
    ]


@pytest.mark.parametrize("disposition", ["INSUFFICIENT"])
def test_red_r06_r07_irrelevant_or_insufficient_support_is_insufficient(
    disposition: str,
) -> None:
    module = _api()
    result = _assessment(module, _subject(), disposition=disposition)
    assert result.outcome.value == "INSUFFICIENT"


def test_red_r08_compound_partial_support_is_inconclusive() -> None:
    module = _api()
    result = module.assess_governed_evidence_support_v0(
        **_subject(statement="Core Kernel owns orchestration and persistence."),
        assessor_subject_id="independent-test-assessor",
        finding_producer_subject_id="e3-test-producer",
        assessor=lambda _material: {
            "outcome": "INCONCLUSIVE",
            "reason_codes": ["COMPOUND_CLAIM_NOT_FULLY_SUPPORTED"],
        },
    )
    assert result.outcome.value == "INCONCLUSIVE"


def test_red_r09_unresolved_counterevidence_is_inconclusive() -> None:
    module = _api()
    subject = _subject(
        limiting_or_counterevidence_refs=("K2",),
        knowledge_evidence=_subject()["knowledge_evidence"]
        + (
            {
                "ref": "K2",
                "path": "docs/architecture/other.md",
                "blob_sha": "x" * 40,
                "line_number": 1,
                "text": "Orchestration belongs elsewhere.",
                "source_class": "APPROVED_SPECIFICATION",
                "authority_class": "normative_subordinate",
            },
        ),
    )
    result = module.assess_governed_evidence_support_v0(
        **subject,
        assessor_subject_id="independent-test-assessor",
        finding_producer_subject_id="e3-test-producer",
        assessor=lambda _material: {
            "outcome": "INCONCLUSIVE",
            "reason_codes": ["MATERIAL_COUNTEREVIDENCE_UNRESOLVED"],
        },
    )
    assert result.outcome.value == "INCONCLUSIVE"


def test_red_r10_compatible_limitation_does_not_force_inconclusive() -> None:
    module = _api()
    subject = _subject(
        limiting_or_counterevidence_refs=("K2",),
        knowledge_evidence=_subject()["knowledge_evidence"]
        + (
            {
                "ref": "K2",
                "path": "docs/architecture/scope.md",
                "blob_sha": "x" * 40,
                "line_number": 1,
                "text": "Kernel orchestration remains intentionally minimal.",
                "source_class": "APPROVED_SPECIFICATION",
                "authority_class": "normative_subordinate",
            },
        ),
    )
    assert _assessment(module, subject).outcome.value == "SUPPORTED"


def test_red_r11_reason_outcome_incoherence_fails_closed() -> None:
    module = _api()
    result = module.assess_governed_evidence_support_v0(
        **_subject(),
        assessor_subject_id="independent-test-assessor",
        finding_producer_subject_id="e3-test-producer",
        assessor=lambda _material: {
            "outcome": "SUPPORTED",
            "reason_codes": ["SUPPORTING_REFS_INSUFFICIENT"],
        },
    )
    assert result.outcome.value != "SUPPORTED"


def test_red_r12_unknown_policy_version_fails_closed() -> None:
    module = _api()
    result = _assessment(module, _subject(policy_version="future/v2"))
    assert result.outcome.value != "SUPPORTED"


def test_red_r13_assessor_unavailable_is_inconclusive() -> None:
    module = _api()
    result = module.assess_governed_evidence_support_v0(
        **_subject(),
        assessor_subject_id="independent-test-assessor",
        finding_producer_subject_id="e3-test-producer",
        assessor=None,
    )
    assert result.outcome.value == "INCONCLUSIVE"
    assert "ASSESSOR_UNAVAILABLE" in [item.value for item in result.reason_codes]


def test_red_r14_malformed_assessor_output_cannot_yield_supported() -> None:
    module = _api()
    result = module.assess_governed_evidence_support_v0(
        **_subject(),
        assessor_subject_id="independent-test-assessor",
        finding_producer_subject_id="e3-test-producer",
        assessor=lambda _material: {"outcome": "SUPPORTED"},
    )
    assert result.outcome.value != "SUPPORTED"


def test_red_r15_self_certifying_producer_cannot_yield_supported() -> None:
    module = _api()
    result = module.assess_governed_evidence_support_v0(
        **_subject(),
        assessor_subject_id="same-subject",
        finding_producer_subject_id="same-subject",
        assessor=lambda _material: {
            "outcome": "SUPPORTED",
            "reason_codes": ["MATERIAL_SUPPORT_CONFIRMED"],
        },
    )
    assert result.outcome.value != "SUPPORTED"


def test_red_r16_equivalent_ref_permutations_preserve_disposition() -> None:
    module = _api()
    repository = _subject()["repository_evidence"] + (
        {
            "ref": "R2",
            "path": "src/malak/kernel/other.py",
            "blob_sha": "z" * 40,
            "line_number": 1,
            "text": "orchestration helper",
        },
    )
    first = _subject(
        supporting_repository_refs=("R1", "R2"),
        repository_evidence=repository,
    )
    second = _subject(
        supporting_repository_refs=("R2", "R1"),
        repository_evidence=tuple(reversed(repository)),
    )
    assert _assessment(module, first).outcome == _assessment(module, second).outcome


def test_red_r17_authority_effect_is_always_none() -> None:
    module = _api()
    result = _assessment(module, _subject())
    assert result.authority_effect == "none"


def test_red_r18_assessment_contract_does_not_expose_support_sufficient() -> None:
    module = _api()
    result = _assessment(module, _subject())
    assert not hasattr(result, "support_sufficient")


def test_red_r19_generic_e3_contract_remains_legacy() -> None:
    analyze = importlib.import_module("malak.capabilities.engineering_analyze")
    assert "evidence_refs" in analyze.ANALYZE_RESPONSE_JSON_SCHEMA
    assert "finding_fingerprint" not in analyze.ANALYZE_RESPONSE_JSON_SCHEMA


def test_red_r20_e4_remains_relationless() -> None:
    propose = importlib.import_module("malak.capabilities.engineering_propose")
    analysis = propose._parse_analysis(
        '{"summary":"s","findings":[{"classification":"ALIGNED",'
        '"statement":"s","rationale":"r","evidence_refs":["R1","K1"]}],'
        '"uncertainties":[]}',
        repository_evidence=[{"ref": "R1"}],
        knowledge_evidence=[{"ref": "K1"}],
    )
    assert analysis.findings[0].relation_id is None


def test_red_r21_no_kernel_planner_registry_contract_is_required() -> None:
    module = _api()
    assert module.__name__ == "malak.capabilities._engineering_analysis"


@pytest.mark.parametrize(
    "reason",
    [
        "SUPPORTING_REFS_IRRELEVANT",
        "SUPPORTING_REFS_INSUFFICIENT",
    ],
)
def test_e3_red_inconclusive_cannot_use_insufficient_reason(
    reason: str,
) -> None:
    """A model-owned reason for INSUFFICIENT must fail closed under INCONCLUSIVE."""
    module = _api()
    result = module.assess_governed_evidence_support_v0(
        **_subject(),
        assessor_subject_id="independent-test-assessor",
        finding_producer_subject_id="e3-test-producer",
        assessor=lambda _material: {
            "outcome": "INCONCLUSIVE",
            "reason_codes": [reason],
        },
    )

    assert result.outcome.value == "INCONCLUSIVE"
    assert [item.value for item in result.reason_codes] == [
        "ASSESSOR_OUTPUT_INVALID"
    ]
