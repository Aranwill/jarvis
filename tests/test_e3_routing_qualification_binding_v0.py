from __future__ import annotations

import importlib


RELATION_ID = "U01.CAPABILITY_ROUTING"
QUESTION_ID = "1" * 64
INPUT_CONTRACT_DIGEST = "3" * 64
OUTPUT_CONTRACT_DIGEST = "4" * 64


def test_red_r01_caller_declared_qualification_cannot_route_deterministic() -> None:
    """F235-B01: self-declared qualification must not authorize deterministic routing."""

    module = importlib.import_module("malak.capabilities._engineering_analysis")

    qualification = module.GovernedDeterministicOracleQualificationV0(
        oracle_id="oracle-1",
        oracle_version="v1",
        oracle_content_digest="a" * 64,
        relation_id=RELATION_ID,
        evaluation_question_identity=QUESTION_ID,
        input_contract_identity=INPUT_CONTRACT_DIGEST,
        output_contract_identity=OUTPUT_CONTRACT_DIGEST,
        coverage_claim="FULL",
        oracle_producer_subject_id="oracle-producer-1",
        qualifier_subject_id="caller-declared-independent-reviewer",
        qualification_evidence_digest="5" * 64,
        authority_effect="none",
    )
    oracle = module.GovernedDeterministicOracleContractV0(
        oracle_id="oracle-1",
        oracle_version="v1",
        oracle_content_digest="a" * 64,
        relation_id=RELATION_ID,
        evaluation_question_identity=QUESTION_ID,
        input_contract_identity=INPUT_CONTRACT_DIGEST,
        output_contract_identity=OUTPUT_CONTRACT_DIGEST,
        coverage_claim="FULL",
        oracle_producer_subject_id="oracle-producer-1",
        qualification_identity=qualification.qualification_identity,
        qualification=qualification,
        authority_effect="none",
        side_effect_class="NONE",
    )

    result = module.route_governed_support_evidence_v0(
        policy_version="e3-governed-support-routing/v0",
        baseline_commit="b" * 40,
        focus_id="U01",
        evidence_set_digest="e" * 64,
        relation_id=RELATION_ID,
        evaluation_question_identity=QUESTION_ID,
        finding_fingerprint="f" * 64,
        resolved_evidence_material_digest="2" * 64,
        declared_evidence_complete=True,
        scope_expansion_required=False,
        oracles=(oracle,),
        expected_binding={
            "baseline_commit": "b" * 40,
            "focus_id": "U01",
            "evidence_set_digest": "e" * 64,
            "relation_id": RELATION_ID,
            "evaluation_question_identity": QUESTION_ID,
            "finding_fingerprint": "f" * 64,
            "resolved_evidence_material_digest": "2" * 64,
        },
    )

    assert result.route_kind is None or result.route_kind.value != "DETERMINISTIC"
