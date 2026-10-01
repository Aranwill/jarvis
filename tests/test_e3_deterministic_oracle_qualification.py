from __future__ import annotations

import ast
import copy
import hashlib
import importlib.util
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts" / "evaluate_e3_deterministic_oracle_qualification.py"

SCHEMA = "MALAK-E3-DETERMINISTIC-ORACLE-QUALIFICATION-EVIDENCE/v0"
REPOSITORY = "Aranwill/jarvis"
CANDIDATE = "c86a9bc3e716046bd8c803e5893fc36289c1d485"
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


def _evaluate(
    *,
    artifact: dict[str, object] | None = None,
    expected_binding: dict[str, object] | None = None,
    independence_evidence: dict[str, object] | None = None,
) -> dict[str, object]:
    module = _runner_module()
    result = module.evaluate_qualification_evidence_v0(
        artifact=copy.deepcopy(artifact if artifact is not None else _base_artifact()),
        expected_binding=copy.deepcopy(
            expected_binding if expected_binding is not None else _expected_binding()
        ),
        independence_evidence=copy.deepcopy(
            independence_evidence
            if independence_evidence is not None
            else _independence_evidence()
        ),
    )
    assert isinstance(result, dict)
    assert set(result) == EXPECTED_RESULT_KEYS
    assert result["authority_effect"] == "none"
    assert result["qualification_result"] in {"PASS", "FAIL", "INCONCLUSIVE"}
    assert isinstance(result["qualification_reasons"], list)
    return result


def test_red_r01_self_declared_full_never_qualifies() -> None:
    artifact = _base_artifact()
    artifact["coverage_claim"] = "FULL"

    result = _evaluate(artifact=artifact)

    assert result["qualification_result"] == "INCONCLUSIVE"


def test_red_r02_malformed_oracle_question_or_contract_identity_is_inconclusive() -> None:
    artifact = _base_artifact()
    artifact["evaluation_question_identity"] = "not-a-sha256"

    result = _evaluate(artifact=artifact)

    assert result["qualification_result"] == "INCONCLUSIVE"


def test_red_r03_stale_candidate_or_oracle_digest_is_inconclusive() -> None:
    artifact = _base_artifact()
    artifact["evaluated_candidate_commit"] = "0" * 40

    stale_candidate = _evaluate(artifact=artifact)
    assert stale_candidate["qualification_result"] == "INCONCLUSIVE"

    artifact = _base_artifact()
    artifact["oracle_content_digest"] = "9" * 64
    stale_oracle = _evaluate(artifact=artifact)
    assert stale_oracle["qualification_result"] == "INCONCLUSIVE"


def test_red_r04_missing_obligation_is_inconclusive() -> None:
    artifact = _base_artifact()
    artifact["coverage_entries"] = artifact["coverage_entries"][:-1]
    artifact["obligation_count"] = 1

    result = _evaluate(artifact=artifact)

    assert result["qualification_result"] == "INCONCLUSIVE"


def test_red_r05_duplicate_obligation_is_inconclusive() -> None:
    artifact = _base_artifact()
    artifact["coverage_entries"][1] = copy.deepcopy(artifact["coverage_entries"][0])

    result = _evaluate(artifact=artifact)

    assert result["qualification_result"] == "INCONCLUSIVE"


def test_red_r06_unknown_obligation_is_inconclusive() -> None:
    artifact = _base_artifact()
    unknown = _obligation("O99", "Unknown obligation not present in reviewed catalog.")
    artifact["coverage_entries"][1] = _coverage_entry(
        unknown,
        check_id="CHECK-99",
    )

    result = _evaluate(artifact=artifact)

    assert result["qualification_result"] == "INCONCLUSIVE"


def test_red_r07_partial_coverage_is_fail() -> None:
    artifact = _base_artifact()
    artifact["coverage_entries"][1]["entry_result"] = "FAIL"
    artifact["qualification_result"] = "PASS"

    result = _evaluate(artifact=artifact)

    assert result["qualification_result"] == "FAIL"


def test_red_r08_unresolved_coverage_mapping_is_inconclusive() -> None:
    artifact = _base_artifact()
    artifact["coverage_entries"][1]["entry_result"] = "INCONCLUSIVE"
    artifact["qualification_result"] = "PASS"

    result = _evaluate(artifact=artifact)

    assert result["qualification_result"] == "INCONCLUSIVE"


def test_red_r09_exact_complete_mapping_can_qualify_pass() -> None:
    result = _evaluate()

    assert result["qualification_result"] == "PASS"


def test_red_r10_oracle_producer_equal_to_reviewer_cannot_pass() -> None:
    artifact = _base_artifact()
    artifact["qualification_reviewer_id"] = "oracle-producer"
    evidence = _independence_evidence(reviewer_id="oracle-producer")

    result = _evaluate(
        artifact=artifact,
        independence_evidence=evidence,
    )

    assert result["qualification_result"] == "INCONCLUSIVE"


def test_red_r11_missing_external_independence_evidence_cannot_pass() -> None:
    module = _runner_module()
    result = module.evaluate_qualification_evidence_v0(
        artifact=_base_artifact(),
        expected_binding=_expected_binding(),
        independence_evidence=None,
    )

    assert isinstance(result, dict)
    assert result["qualification_result"] == "INCONCLUSIVE"
    assert result["authority_effect"] == "none"


def test_red_r12_aggregation_is_deterministic_and_fail_closed() -> None:
    artifact = _base_artifact()
    artifact["coverage_entries"][0]["entry_result"] = "FAIL"
    artifact["coverage_entries"][1]["entry_result"] = "INCONCLUSIVE"
    fail_result = _evaluate(artifact=artifact)
    assert fail_result["qualification_result"] == "FAIL"

    artifact = _base_artifact()
    artifact["coverage_entries"][1]["entry_result"] = "INCONCLUSIVE"
    inconclusive_result = _evaluate(artifact=artifact)
    assert inconclusive_result["qualification_result"] == "INCONCLUSIVE"

    pass_result = _evaluate()
    assert pass_result["qualification_result"] == "PASS"


def test_red_r13_authority_effect_other_than_none_is_rejected() -> None:
    artifact = _base_artifact()
    artifact["authority_effect"] = "authorize"

    result = _evaluate(artifact=artifact)

    assert result["qualification_result"] == "INCONCLUSIVE"
    assert result["authority_effect"] == "none"


def test_red_r14_resource_bounds_are_enforced() -> None:
    large_catalog = [
        _obligation(f"O{i:02d}", f"Bounded obligation {i}")
        for i in range(1, 34)
    ]
    artifact = _base_artifact()
    artifact["obligation_count"] = len(large_catalog)
    artifact["coverage_entries"] = [
        _coverage_entry(item, check_id=f"CHECK-{i:02d}")
        for i, item in enumerate(large_catalog, start=1)
    ]
    too_many = _evaluate(
        artifact=artifact,
        expected_binding=_expected_binding(catalog=large_catalog),
    )
    assert too_many["qualification_result"] == "INCONCLUSIVE"

    oversized_catalog = _catalog()
    oversized_catalog[0] = _obligation("O01", "x" * (4 * 1024 + 1))
    artifact = _base_artifact()
    artifact["coverage_entries"][0] = _coverage_entry(
        oversized_catalog[0],
        check_id="CHECK-01",
    )
    oversized = _evaluate(
        artifact=artifact,
        expected_binding=_expected_binding(catalog=oversized_catalog),
    )
    assert oversized["qualification_result"] == "INCONCLUSIVE"


def test_red_r15_runner_has_no_model_provider_network_tool_or_process_dependency() -> None:
    _runner_module()
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


def test_red_r16_stage2_or_authority_fields_are_absent_from_output() -> None:
    result = _evaluate()

    forbidden = {
        "receipt_id",
        "receipt",
        "stage_2",
        "stage2",
        "approved",
        "authorized",
        "merged",
        "promoted",
        "released",
        "authority",
    }
    assert not (set(result) & forbidden)
    assert result["authority_effect"] == "none"


def test_red_r17_downstream_finalization_remains_unwired() -> None:
    paths = [
        ROOT / "src" / "malak" / "core" / "assurance_signal_projection.py",
        ROOT / "src" / "malak" / "core" / "protected_finalization.py",
    ]
    forbidden_tokens = {
        "MALAK-E3-DETERMINISTIC-ORACLE-QUALIFICATION-EVIDENCE/v0",
        "qualification_material_digest",
        "obligation_catalog_digest",
    }
    for path in paths:
        source = path.read_text(encoding="utf-8")
        for token in forbidden_tokens:
            assert token not in source


def test_red_r18_pr235_routing_candidate_remains_untouched_on_main() -> None:
    path = ROOT / "src" / "malak" / "capabilities" / "_engineering_analysis.py"
    source = path.read_text(encoding="utf-8")

    forbidden_tokens = {
        "GovernedDeterministicOracleQualificationEvidenceV0",
        "MALAK-E3-DETERMINISTIC-ORACLE-QUALIFICATION-EVIDENCE/v0",
        "obligation_catalog_digest",
        "qualification_material_digest",
    }
    for token in forbidden_tokens:
        assert token not in source
