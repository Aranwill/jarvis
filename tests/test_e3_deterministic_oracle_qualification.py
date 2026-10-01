from __future__ import annotations

import ast
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts" / "evaluate_e3_deterministic_oracle_qualification.py"

SCHEMA = "MALAK-E3-DETERMINISTIC-ORACLE-QUALIFICATION-EVIDENCE/v0"
REPOSITORY = "Aranwill/jarvis"
LOCAL_TEST_CANDIDATE = "f" * 40
CANDIDATE = os.environ.get("CANDIDATE_SHA", LOCAL_TEST_CANDIDATE)
RELATION = "U01.RUNTIME_INDEPENDENCE"
QUESTION = "q" * 64
ORACLE_DIGEST = "a" * 64
INPUT_CONTRACT = "b" * 64
OUTPUT_CONTRACT = "c" * 64
CATALOG_DIGEST = "d" * 64
MATERIAL_DIGEST = "e" * 64
RUNNER_DIGEST = "f" * 64

EXPECTED_RESULT_KEYS = {
    "qualification_result",
    "qualification_reasons",
    "authority_effect",
}


def _canonical_json(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _sha256(value: object) -> str:
    return hashlib.sha256(_canonical_json(value)).hexdigest()


def _obligation(
    obligation_id: str,
    statement: str,
) -> dict[str, str]:
    identity = _sha256(
        {
            "relation_id": RELATION,
            "evaluation_question_identity": QUESTION,
            "obligation_id": obligation_id,
            "obligation_statement": statement,
        }
    )
    return {
        "obligation_id": obligation_id,
        "obligation_statement": statement,
        "obligation_identity": identity,
    }


def _catalog() -> list[dict[str, str]]:
    return [
        _obligation(
            "O01",
            "The oracle must prove that Kernel remains free of direct runtime/provider dependency.",
        ),
        _obligation(
            "O02",
            "The oracle must prove that runtime/provider implementations stay outside Kernel responsibility.",
        ),
    ]


def _coverage_entry(
    obligation: dict[str, str],
    *,
    check_id: str,
    result: str = "PASS",
) -> dict[str, object]:
    return {
        "obligation_id": obligation["obligation_id"],
        "obligation_identity": obligation["obligation_identity"],
        "oracle_check_id": check_id,
        "oracle_check_identity": _sha256(
            {
                "oracle_id": "oracle-runtime-independence",
                "oracle_version": "v0",
                "check_id": check_id,
            }
        ),
        "oracle_check_contract_digest": _sha256(
            {
                "check_id": check_id,
                "input_contract_identity": INPUT_CONTRACT,
                "output_contract_identity": OUTPUT_CONTRACT,
            }
        ),
        "verification_evidence_refs": [f"evidence:{check_id}"],
        "entry_result": result,
        "entry_reasons": [],
    }


def _base_artifact() -> dict[str, object]:
    catalog = _catalog()
    return {
        "schema_version": SCHEMA,
        "repository": REPOSITORY,
        "evaluated_candidate_commit": CANDIDATE,
        "oracle_id": "oracle-runtime-independence",
        "oracle_version": "v0",
        "oracle_content_digest": ORACLE_DIGEST,
        "oracle_producer_subject_id": "oracle-producer",
        "relation_id": RELATION,
        "evaluation_question_identity": QUESTION,
        "input_contract_identity": INPUT_CONTRACT,
        "output_contract_identity": OUTPUT_CONTRACT,
        "obligation_catalog_digest": CATALOG_DIGEST,
        "obligation_count": len(catalog),
        "coverage_entries": [
            _coverage_entry(catalog[0], check_id="CHECK-01"),
            _coverage_entry(catalog[1], check_id="CHECK-02"),
        ],
        "qualification_method": "INDEPENDENT_REVIEWED_DETERMINISTIC_COVERAGE",
        "qualification_material_digest": MATERIAL_DIGEST,
        "qualification_runner_version": "e3-deterministic-oracle-qualification/v0",
        "qualification_runner_digest": RUNNER_DIGEST,
        "qualification_reviewer_id": "independent-reviewer",
        "qualification_validator_id": "independent-validator",
        "qualification_result": "PASS",
        "qualification_reasons": [],
        "authority_effect": "none",
    }


def _expected_binding(
    *,
    catalog: list[dict[str, str]] | None = None,
    candidate: str = CANDIDATE,
    oracle_digest: str = ORACLE_DIGEST,
) -> dict[str, object]:
    return {
        "repository": REPOSITORY,
        "evaluated_candidate_commit": candidate,
        "oracle_id": "oracle-runtime-independence",
        "oracle_version": "v0",
        "oracle_content_digest": oracle_digest,
        "relation_id": RELATION,
        "evaluation_question_identity": QUESTION,
        "input_contract_identity": INPUT_CONTRACT,
        "output_contract_identity": OUTPUT_CONTRACT,
        "obligation_catalog_digest": CATALOG_DIGEST,
        "obligation_catalog": copy.deepcopy(catalog if catalog is not None else _catalog()),
    }


def _independence_evidence(
    *,
    reviewer_id: str = "independent-reviewer",
    validator_id: str = "independent-validator",
) -> dict[str, object]:
    return {
        "evidence_kind": "EXTERNAL_CANDIDATE_BOUND_ROLE_SEPARATION",
        "evaluated_candidate_commit": CANDIDATE,
        "oracle_producer_subject_id": "oracle-producer",
        "qualification_reviewer_id": reviewer_id,
        "qualification_validator_id": validator_id,
        "review_evidence_digest": "1" * 64,
        "validation_evidence_digest": "2" * 64,
        "authority_effect": "none",
    }


def _runner_module():
    assert RUNNER.is_file(), (
        "RED: deterministic oracle qualification runner is not implemented"
    )
    spec = importlib.util.spec_from_file_location(
        "malak_e3_deterministic_oracle_qualification",
        RUNNER,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    evaluator = getattr(module, "evaluate_qualification_evidence_v0", None)
    assert callable(evaluator), (
        "RED: evaluate_qualification_evidence_v0 is not implemented"
    )
    return module


BUNDLE_SCHEMA = "MALAK-E3-DETERMINISTIC-ORACLE-QUALIFICATION-BUNDLE/v0"
REVIEW_SCHEMA = "MALAK-E3-DETERMINISTIC-ORACLE-QUALIFICATION-REVIEW-EVIDENCE/v0"


def _runner_digest() -> str:
    return hashlib.sha256(RUNNER.read_bytes()).hexdigest()


def _verification_evidence(
    evidence_id: str,
    material: object,
    *,
    candidate: str = CANDIDATE,
) -> dict[str, object]:
    return {
        "evidence_id": evidence_id,
        "evidence_kind": "BOUNDED_DETERMINISTIC_CHECK_OUTPUT",
        "content_digest": _sha256(material),
        "content_or_bounded_material": material,
        "candidate_binding": candidate,
    }


def _qualification_bundle(
    *,
    catalog: list[dict[str, str]] | None = None,
    coverage_results: tuple[str, ...] | None = None,
    candidate: str = CANDIDATE,
) -> dict[str, object]:
    obligations = copy.deepcopy(catalog if catalog is not None else _catalog())
    results = coverage_results or tuple("PASS" for _ in obligations)

    coverage_entries = [
        _coverage_entry(
            obligation,
            check_id=f"CHECK-{index:02d}",
            result=results[index - 1],
        )
        for index, obligation in enumerate(obligations, start=1)
    ]

    evidence_items = [
        _verification_evidence(
            str(entry["verification_evidence_refs"][0]),
            {
                "obligation_id": entry["obligation_id"],
                "observed": True,
            },
            candidate=candidate,
        )
        for entry in coverage_entries
    ]

    qualification_material = {
        "qualification_method": "INDEPENDENT_REVIEWED_DETERMINISTIC_COVERAGE",
        "executing_runner_version": "e3-deterministic-oracle-qualification/v0",
        "executing_runner_digest": _runner_digest(),
    }

    return {
        "schema_version": BUNDLE_SCHEMA,
        "repository": REPOSITORY,
        "evaluated_candidate_commit": candidate,
        "oracle_identity": {
            "oracle_id": "oracle-runtime-independence",
            "oracle_version": "v0",
            "oracle_content_digest": ORACLE_DIGEST,
            "oracle_producer_subject_id": "oracle-producer",
        },
        "governed_question_material": {
            "relation_id": RELATION,
            "evaluation_question_identity": QUESTION,
            "input_contract_identity": INPUT_CONTRACT,
            "output_contract_identity": OUTPUT_CONTRACT,
        },
        "obligation_catalog": obligations,
        "obligation_catalog_digest": _sha256(obligations),
        "coverage_entries": coverage_entries,
        "verification_evidence": evidence_items,
        "verification_evidence_digest": _sha256(evidence_items),
        "qualification_material": qualification_material,
        "qualification_material_digest": _sha256(qualification_material),
    }


def _bundle_digest(bundle: dict[str, object]) -> str:
    return _sha256(bundle)


def _governed_binding(bundle: dict[str, object]) -> dict[str, object]:
    return {
        "repository": bundle["repository"],
        "evaluated_candidate_commit": bundle["evaluated_candidate_commit"],
        "oracle_identity": copy.deepcopy(bundle["oracle_identity"]),
        "governed_question_material": copy.deepcopy(
            bundle["governed_question_material"]
        ),
        "obligation_catalog_digest": bundle["obligation_catalog_digest"],
        "qualification_bundle_digest": _bundle_digest(bundle),
    }


def _review_evidence(
    bundle: dict[str, object],
    *,
    catalog_result: str = "PASS",
    independence_result: str = "PASS",
    verification_result: str = "PASS",
    qualification_result: str = "PASS",
) -> dict[str, object]:
    question = bundle["governed_question_material"]
    assert isinstance(question, dict)

    return {
        "schema_version": REVIEW_SCHEMA,
        "repository": REPOSITORY,
        "evaluated_candidate_commit": bundle["evaluated_candidate_commit"],
        "qualification_bundle_digest": _bundle_digest(bundle),
        "reviewed_relation_id": question["relation_id"],
        "reviewed_evaluation_question_identity": question[
            "evaluation_question_identity"
        ],
        "reviewed_obligation_catalog_digest": bundle[
            "obligation_catalog_digest"
        ],
        "implementation_actor_id": "implementation-actor",
        "qualification_reviewer_id": "independent-reviewer",
        "qualification_validator_id": "independent-validator",
        "structural_validator_result": "PASS",
        "structural_validator_evidence_reference": (
            "external:structural-validation"
        ),
        "catalog_completeness_result": catalog_result,
        "independence_review_result": independence_result,
        "verification_material_review_result": verification_result,
        "qualification_review_result": qualification_result,
        "finding_refs": [],
        "evidence_references": ["external:review-evidence"],
        "authority_effect": "none",
    }


def _evaluate(
    *,
    artifact: object,
    expected_binding: object,
    review_evidence: object,
    expected_candidate_commit: str = CANDIDATE,
) -> dict[str, object]:
    module = _runner_module()
    result = module.evaluate_qualification_evidence_v0(
        artifact=copy.deepcopy(artifact),
        expected_binding=copy.deepcopy(expected_binding),
        independence_evidence=copy.deepcopy(review_evidence),
        expected_candidate_commit=expected_candidate_commit,
    )
    assert isinstance(result, dict)
    return result


def _terminal_result(result: dict[str, object]) -> object:
    return result.get(
        "qualification_review_result",
        result.get("qualification_result"),
    )


def _structural_result(result: dict[str, object]) -> object:
    return result.get("validator_result", result.get("qualification_result"))


def test_tb_r01_structural_pass_cannot_claim_independence_verified() -> None:
    bundle = _qualification_bundle()
    result = _evaluate(
        artifact=bundle,
        expected_binding=_governed_binding(bundle),
        review_evidence=_review_evidence(bundle),
    )

    assert result.get("requires_external_validation") is True
    assert result.get("identity_independence_verified") is False
    assert result.get("validator_result") in {"PASS", "FAIL", "INCONCLUSIVE"}


def test_tb_r02_missing_external_review_evidence_cannot_qualify_pass() -> None:
    bundle = _qualification_bundle()
    result = _evaluate(
        artifact=bundle,
        expected_binding=_governed_binding(bundle),
        review_evidence=None,
    )

    assert _terminal_result(result) != "PASS"
    assert result.get("requires_external_validation") is True


def test_tb_r03_fabricated_role_claims_cannot_prove_independence() -> None:
    bundle = _qualification_bundle()
    review = _review_evidence(bundle)
    review["qualification_reviewer_id"] = review["implementation_actor_id"]

    result = _evaluate(
        artifact=bundle,
        expected_binding=_governed_binding(bundle),
        review_evidence=review,
    )

    assert _terminal_result(result) == "INCONCLUSIVE"
    assert result.get("identity_independence_verified") is False
    assert result.get("requires_external_validation") is True

def test_tb_r04_catalog_digest_is_recomputed_from_catalog_material() -> None:
    bundle = _qualification_bundle()
    bundle["obligation_catalog_digest"] = "0" * 64

    result = _evaluate(
        artifact=bundle,
        expected_binding=_governed_binding(bundle),
        review_evidence=_review_evidence(bundle),
    )

    assert _structural_result(result) == "INCONCLUSIVE"
    assert "OBLIGATION_CATALOG_DIGEST_MISMATCH" in result["validator_reasons"]

def test_tb_r05_qualification_material_digest_requires_bound_material() -> None:
    bundle = _qualification_bundle()
    bundle["qualification_material_digest"] = "0" * 64

    result = _evaluate(
        artifact=bundle,
        expected_binding=_governed_binding(bundle),
        review_evidence=_review_evidence(bundle),
    )

    assert _structural_result(result) == "INCONCLUSIVE"
    assert "QUALIFICATION_MATERIAL_DIGEST_MISMATCH" in result["validator_reasons"]

def test_tb_r06_verification_refs_require_resolved_evidence_material() -> None:
    bundle = _qualification_bundle()
    evidence = bundle["verification_evidence"]
    assert isinstance(evidence, list)
    evidence[0]["evidence_id"] = "evidence:renamed"
    bundle["verification_evidence_digest"] = _sha256(evidence)

    result = _evaluate(
        artifact=bundle,
        expected_binding=_governed_binding(bundle),
        review_evidence=_review_evidence(bundle),
    )

    assert _structural_result(result) == "INCONCLUSIVE"
    assert "VERIFICATION_EVIDENCE_REF_UNRESOLVED" in result["validator_reasons"]

def test_tb_r07_fake_or_unresolved_verification_ref_is_inconclusive() -> None:
    bundle = _qualification_bundle()
    coverage = bundle["coverage_entries"]
    assert isinstance(coverage, list)
    coverage[0]["verification_evidence_refs"] = ["evidence:fake"]

    result = _evaluate(
        artifact=bundle,
        expected_binding=_governed_binding(bundle),
        review_evidence=_review_evidence(bundle),
    )

    assert _structural_result(result) == "INCONCLUSIVE"
    assert "VERIFICATION_EVIDENCE_REF_UNRESOLVED" in result["validator_reasons"]

def test_tb_r08_runner_identity_is_derived_not_caller_declared() -> None:
    bundle = _qualification_bundle()
    material = bundle["qualification_material"]
    assert isinstance(material, dict)
    material["executing_runner_digest"] = "0" * 64
    bundle["qualification_material_digest"] = _sha256(material)

    result = _evaluate(
        artifact=bundle,
        expected_binding=_governed_binding(bundle),
        review_evidence=_review_evidence(bundle),
    )

    assert _structural_result(result) == "INCONCLUSIVE"
    assert "RUNNER_DIGEST_MISMATCH" in result["validator_reasons"]

def test_tb_r09_stale_runner_identity_is_inconclusive() -> None:
    bundle = _qualification_bundle()
    material = copy.deepcopy(bundle["qualification_material"])
    assert isinstance(material, dict)
    material["executing_runner_digest"] = "0" * 64
    bundle["qualification_material"] = material
    bundle["qualification_material_digest"] = _sha256(material)

    result = _evaluate(
        artifact=bundle,
        expected_binding=_governed_binding(bundle),
        review_evidence=_review_evidence(bundle),
    )

    assert _structural_result(result) == "INCONCLUSIVE"


def test_tb_r10_exact_single_obligation_catalog_needs_external_completeness() -> None:
    bundle = _qualification_bundle(catalog=[_catalog()[0]])
    review = _review_evidence(
        bundle,
        catalog_result="INCONCLUSIVE",
        qualification_result="INCONCLUSIVE",
    )

    result = _evaluate(
        artifact=bundle,
        expected_binding=_governed_binding(bundle),
        review_evidence=review,
    )

    assert _structural_result(result) == "PASS"
    assert _terminal_result(result) == "INCONCLUSIVE"

def test_tb_r11_review_bound_to_wrong_catalog_digest_is_inconclusive() -> None:
    bundle = _qualification_bundle()
    review = _review_evidence(bundle)
    review["reviewed_obligation_catalog_digest"] = "0" * 64

    result = _evaluate(
        artifact=bundle,
        expected_binding=_governed_binding(bundle),
        review_evidence=review,
    )

    assert _terminal_result(result) == "INCONCLUSIVE"


def test_tb_r12_review_bound_to_wrong_bundle_digest_is_inconclusive() -> None:
    bundle = _qualification_bundle()
    review = _review_evidence(bundle)
    review["qualification_bundle_digest"] = "0" * 64

    result = _evaluate(
        artifact=bundle,
        expected_binding=_governed_binding(bundle),
        review_evidence=review,
    )

    assert _terminal_result(result) == "INCONCLUSIVE"


def test_tb_r13_review_bound_to_wrong_candidate_is_inconclusive() -> None:
    bundle = _qualification_bundle()
    review = _review_evidence(bundle)
    review["evaluated_candidate_commit"] = "0" * 40

    result = _evaluate(
        artifact=bundle,
        expected_binding=_governed_binding(bundle),
        review_evidence=review,
    )

    assert _terminal_result(result) == "INCONCLUSIVE"


def test_tb_r14_structural_fail_prevents_qualification_pass() -> None:
    bundle = _qualification_bundle(coverage_results=("PASS", "FAIL"))
    review = _review_evidence(bundle, qualification_result="FAIL")
    review["structural_validator_result"] = "FAIL"

    result = _evaluate(
        artifact=bundle,
        expected_binding=_governed_binding(bundle),
        review_evidence=review,
    )

    assert _terminal_result(result) != "PASS"


def test_tb_r15_structural_inconclusive_prevents_qualification_pass() -> None:
    bundle = _qualification_bundle()
    question = copy.deepcopy(bundle["governed_question_material"])
    assert isinstance(question, dict)
    question["evaluation_question_identity"] = "not-an-identity"
    bundle["governed_question_material"] = question

    result = _evaluate(
        artifact=bundle,
        expected_binding=_governed_binding(bundle),
        review_evidence=_review_evidence(bundle),
    )

    assert _terminal_result(result) != "PASS"


def test_tb_r16_external_review_fail_propagates_fail() -> None:
    bundle = _qualification_bundle()
    review = _review_evidence(
        bundle,
        catalog_result="FAIL",
        qualification_result="FAIL",
    )

    result = _evaluate(
        artifact=bundle,
        expected_binding=_governed_binding(bundle),
        review_evidence=review,
    )

    assert _terminal_result(result) == "FAIL"


def test_tb_r17_external_review_inconclusive_propagates_inconclusive() -> None:
    bundle = _qualification_bundle()
    review = _review_evidence(
        bundle,
        independence_result="INCONCLUSIVE",
        qualification_result="INCONCLUSIVE",
    )

    result = _evaluate(
        artifact=bundle,
        expected_binding=_governed_binding(bundle),
        review_evidence=review,
    )

    assert _terminal_result(result) == "INCONCLUSIVE"


def test_tb_r18_all_exact_dimensions_pass_can_support_review_pass() -> None:
    bundle = _qualification_bundle()
    result = _evaluate(
        artifact=bundle,
        expected_binding=_governed_binding(bundle),
        review_evidence=_review_evidence(bundle),
    )

    assert _structural_result(result) == "PASS"
    assert _terminal_result(result) == "PASS"
    assert result.get("identity_independence_verified") is False
    assert result.get("requires_external_validation") is True


def test_tb_r19_authority_effect_remains_none() -> None:
    bundle = _qualification_bundle()
    result = _evaluate(
        artifact=bundle,
        expected_binding=_governed_binding(bundle),
        review_evidence=_review_evidence(bundle),
    )

    assert result.get("authority_effect") == "none"


def test_tb_r20_no_stage2_runtime_routing_or_external_dependency() -> None:
    source = RUNNER.read_text(encoding="utf-8")
    tree = ast.parse(source)

    forbidden_import_roots = {
        "anthropic",
        "httpx",
        "ollama",
        "openai",
        "requests",
        "socket",
        "subprocess",
        "urllib",
    }

    imported_roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_roots.add(node.module.split(".")[0])

    assert not (imported_roots & forbidden_import_roots)

    downstream_paths = [
        ROOT / "src" / "malak" / "core" / "assurance_signal_projection.py",
        ROOT / "src" / "malak" / "core" / "protected_finalization.py",
        ROOT / "src" / "malak" / "capabilities" / "_engineering_analysis.py",
    ]
    forbidden_tokens = {
        BUNDLE_SCHEMA,
        REVIEW_SCHEMA,
        "qualification_bundle_digest",
        "catalog_completeness_result",
    }
    for downstream_path in downstream_paths:
        downstream = downstream_path.read_text(encoding="utf-8")
        for token in forbidden_tokens:
            assert token not in downstream


def test_tb_r21_declared_result_or_reasons_are_rejected_by_bundle_schema() -> None:
    result = _evaluate(
        artifact=_base_artifact(),
        expected_binding=_expected_binding(),
        review_evidence=_independence_evidence(),
    )

    assert _structural_result(result) == "INCONCLUSIVE"
    assert _terminal_result(result) != "PASS"

def test_tb_r22_expected_candidate_exact_match_is_required() -> None:
    bundle = _qualification_bundle()

    exact = _evaluate(
        artifact=bundle,
        expected_binding=_governed_binding(bundle),
        review_evidence=_review_evidence(bundle),
        expected_candidate_commit=CANDIDATE,
    )
    assert _structural_result(exact) == "PASS"

    wrong_expected = "0" * 40 if CANDIDATE != "0" * 40 else "1" * 40
    mismatched = _evaluate(
        artifact=bundle,
        expected_binding=_governed_binding(bundle),
        review_evidence=_review_evidence(bundle),
        expected_candidate_commit=wrong_expected,
    )
    assert _structural_result(mismatched) == "INCONCLUSIVE"
    assert "EXPECTED_CANDIDATE_MISMATCH" in mismatched["validator_reasons"]


def test_tb_r23_stale_coherent_candidate_material_cannot_pass() -> None:
    stale = "0" * 40 if CANDIDATE != "0" * 40 else "1" * 40
    bundle = _qualification_bundle(candidate=stale)

    result = _evaluate(
        artifact=bundle,
        expected_binding=_governed_binding(bundle),
        review_evidence=_review_evidence(bundle),
        expected_candidate_commit=CANDIDATE,
    )

    assert _structural_result(result) == "INCONCLUSIVE"
    assert _terminal_result(result) != "PASS"
    assert "EXPECTED_CANDIDATE_MISMATCH" in result["validator_reasons"]


def test_tb_r24_candidate_fixture_uses_validation_context_when_available() -> None:
    validation_candidate = os.environ.get("CANDIDATE_SHA")

    if validation_candidate is not None:
        assert CANDIDATE == validation_candidate
        assert CANDIDATE != "c86a9bc3e716046bd8c803e5893fc36289c1d485"
    else:
        assert CANDIDATE == LOCAL_TEST_CANDIDATE
