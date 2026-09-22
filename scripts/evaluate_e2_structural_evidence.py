from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from malak.capabilities.engineering_inspect import EngineeringInspectCapability
from malak.core.conversation import (
    ConversationProvider,
    ConversationRequest,
    ConversationResponse,
)
from malak.core.conversation_registry import ConversationProviderRegistry
from malak.core.request import Request
from malak.infrastructure.repository_reader import GitRepositoryReader
from malak.infrastructure.repository_structure import RepositoryStructuralProjector
from malak.infrastructure.repository_structure_lookup import RepositoryStructuralLookup
from malak.knowledge.knowledge_reader import GovernedKnowledgeReader
from malak.services.conversation_service import ConversationService


CASE_SET = ROOT / "evaluations" / "e2_structural_evidence_v0" / "cases.json"
RUNNER_VERSION = "E2-STRUCTURAL-EVIDENCE-EVALUATION-RUNNER/v0"
PROVIDER_POLICY_VERSION = "E2-STRUCTURAL-EVIDENCE-DETERMINISTIC-PROVIDER/v0"
PROVIDER_POLICY = (
    b"cite-first-valid-evidence-ref-in-R-K-S-order; "
    b"no semantic scoring; no external state; no network"
)

_TOP_LEVEL_KEYS = {"schema_version", "cases"}
_CASE_KEYS = {
    "case_id",
    "subject",
    "fixture_profile",
    "comparison_class",
    "expected_a_status",
    "expected_b_status",
    "expected_structural_facts",
    "expected_total_structural_count",
    "expected_emitted_structural_count",
    "expected_context_truncated",
    "ground_truth_source",
    "ground_truth_review_status",
}
_ALLOWED_SCHEMA_VERSION = "MALAK-E2-STRUCTURAL-EVIDENCE-CASESET/v0"
_ALLOWED_FIXTURES = {"basic", "truncation"}
_ALLOWED_COMPARISON_CLASSES = {
    "STRUCTURAL_COVERAGE_GAIN",
    "NO_STRUCTURAL_ACTIVATION",
    "ABSENT",
    "TRUNCATION",
}
_ALLOWED_STATUSES = {"UNCONFIRMED", "GROUNDED"}
_ALLOWED_REVIEW_STATUS = {"OWNER_APPROVED_DESIGN"}
_SYMBOL_KEYS = {"fact_type", "module_name", "qualified_name", "kind"}
_IMPORT_KEYS = {
    "fact_type",
    "source_module",
    "target_module",
    "imported_name",
    "relative_level",
}


class DeterministicEvaluationProvider(ConversationProvider):
    def __init__(self) -> None:
        self.calls = 0
        self.requests: list[ConversationRequest] = []

    def generate(self, request: ConversationRequest) -> ConversationResponse:
        self.calls += 1
        self.requests.append(request)
        packet = json.loads(request.prompt)
        refs: list[str] = []
        for key in ("repository_evidence", "knowledge_evidence", "structural_evidence"):
            evidence = packet.get(key, [])
            if evidence:
                refs.append(str(evidence[0]["ref"]))
        citations = " ".join(f"[{ref}]" for ref in refs)
        content = "Deterministic evaluation observation"
        if citations:
            content += f" {citations}"
        return ConversationResponse(
            content=content,
            model=request.model,
            provider="evaluation",
        )


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _git(repo: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def _write(repo: Path, relative: str, content: str) -> None:
    path = repo / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _official_candidate_sha() -> str:
    return _git(ROOT, "rev-parse", "HEAD")


def _load_case_set() -> tuple[dict[str, Any], bytes]:
    raw = CASE_SET.read_bytes()
    payload = json.loads(raw.decode("utf-8"))
    if not isinstance(payload, dict) or set(payload) != _TOP_LEVEL_KEYS:
        raise ValueError("case-set top-level schema mismatch")
    if payload["schema_version"] != _ALLOWED_SCHEMA_VERSION:
        raise ValueError("unsupported case-set schema version")
    cases = payload["cases"]
    if not isinstance(cases, list) or not cases:
        raise ValueError("case-set cases must be a non-empty list")

    seen: set[str] = set()
    for case in cases:
        _validate_case(case, seen)
    return payload, raw


def _validate_case(case: Any, seen: set[str]) -> None:
    if not isinstance(case, dict) or set(case) != _CASE_KEYS:
        raise ValueError("case schema mismatch")

    case_id = case["case_id"]
    subject = case["subject"]
    fixture = case["fixture_profile"]
    comparison = case["comparison_class"]

    if not isinstance(case_id, str) or not case_id:
        raise ValueError("case_id must be non-empty")
    if case_id in seen:
        raise ValueError("duplicate case_id")
    seen.add(case_id)

    if not isinstance(subject, str) or not subject.strip():
        raise ValueError("subject must be non-empty")
    if fixture not in _ALLOWED_FIXTURES:
        raise ValueError("unsupported fixture profile")
    if comparison not in _ALLOWED_COMPARISON_CLASSES:
        raise ValueError("unsupported comparison class")
    if case["expected_a_status"] not in _ALLOWED_STATUSES:
        raise ValueError("unsupported expected A status")
    if case["expected_b_status"] not in _ALLOWED_STATUSES:
        raise ValueError("unsupported expected B status")
    if type(case["expected_total_structural_count"]) is not int:
        raise ValueError("expected_total_structural_count must be int")
    if type(case["expected_emitted_structural_count"]) is not int:
        raise ValueError("expected_emitted_structural_count must be int")
    if type(case["expected_context_truncated"]) is not bool:
        raise ValueError("expected_context_truncated must be bool")
    if not isinstance(case["ground_truth_source"], str) or not case["ground_truth_source"]:
        raise ValueError("ground_truth_source must be non-empty")
    if case["ground_truth_review_status"] not in _ALLOWED_REVIEW_STATUS:
        raise ValueError("ground truth is not independently owner-reviewed")

    expected_facts = case["expected_structural_facts"]
    if not isinstance(expected_facts, list):
        raise ValueError("expected_structural_facts must be list")
    if len(expected_facts) != case["expected_total_structural_count"]:
        raise ValueError("ground truth fact count mismatch")
    if not (0 <= case["expected_emitted_structural_count"] <= 12):
        raise ValueError("invalid expected emitted structural count")
    if case["expected_emitted_structural_count"] > len(expected_facts):
        raise ValueError("emitted count exceeds total fact count")

    for fact in expected_facts:
        _validate_expected_fact(fact)


def _validate_expected_fact(fact: Any) -> None:
    if not isinstance(fact, dict):
        raise ValueError("expected fact must be object")
    fact_type = fact.get("fact_type")
    if fact_type == "symbol":
        if set(fact) != _SYMBOL_KEYS:
            raise ValueError("symbol ground truth schema mismatch")
        if fact["kind"] not in {
            "CLASS",
            "FUNCTION",
            "ASYNC_FUNCTION",
            "METHOD",
            "ASYNC_METHOD",
        }:
            raise ValueError("unsupported symbol kind")
        return
    if fact_type == "import":
        if set(fact) != _IMPORT_KEYS:
            raise ValueError("import ground truth schema mismatch")
        if type(fact["relative_level"]) is not int:
            raise ValueError("relative_level must be int")
        return
    raise ValueError("unsupported structural fact type")


def _create_fixture(root: Path, profile: str) -> tuple[Path, str]:
    repo = root / "repo"
    repo.mkdir()

    _git(repo, "init")
    _git(repo, "config", "user.email", "evaluation@example.invalid")
    _git(repo, "config", "user.name", "Malak Evaluation")
    _git(repo, "config", "commit.gpgsign", "false")

    if profile == "basic":
        component = (
            "import os\n"
            "from malak.services import planner\n\n"
            'VALUE = "needle implementation-token"\n\n'
            "class NeedleComponent1:\n"
            "    pass\n"
        )
    elif profile == "truncation":
        component = "\n\n".join(
            f"class NeedleComponent{index}:\n    pass"
            for index in range(1, 14)
        ) + "\n"
    else:
        raise ValueError("unsupported fixture profile")

    _write(repo, "src/malak/component.py", component)
    _write(
        repo,
        "docs/governance/cognitive_constitution.md",
        "needle governing-context\n",
    )
    _write(
        repo,
        "docs/architecture/blueprint.md",
        "needle architecture-context\n",
    )
    _write(repo, "SECURITY.md", "needle security-context\n")
    _write(
        repo,
        "documents/projects/jarvis/ideas.md",
        "needle non-normative-context\n",
    )

    _git(repo, "add", ".")
    _git(repo, "commit", "--no-gpg-sign", "-m", "evaluation fixture")
    baseline = _git(repo, "rev-parse", "HEAD")
    return repo, baseline


def _service(provider: ConversationProvider) -> ConversationService:
    registry = ConversationProviderRegistry()
    registry.register("evaluation", provider)
    return ConversationService(registry)


def _execute_pair(
    repo: Path,
    subject: str,
) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    reader = GitRepositoryReader(repo)
    knowledge = GovernedKnowledgeReader(reader)
    projection = RepositoryStructuralProjector(reader).project()

    provider_a = DeterministicEvaluationProvider()
    capability_a = EngineeringInspectCapability(
        repository_reader=reader,
        knowledge_reader=knowledge,
        conversation_service=_service(provider_a),
        provider_name="evaluation",
        model="deterministic-evaluation",
    )
    output_a = capability_a.execute(
        Request(content=subject, session_id="evaluation-A")
    )

    provider_b = DeterministicEvaluationProvider()
    capability_b = EngineeringInspectCapability(
        repository_reader=reader,
        knowledge_reader=knowledge,
        structural_projection=projection,
        conversation_service=_service(provider_b),
        provider_name="evaluation",
        model="deterministic-evaluation",
    )
    output_b = capability_b.execute(
        Request(content=subject, session_id="evaluation-B")
    )

    observed_a = _observed(output_a, provider_a)
    observed_b = _observed(output_b, provider_b)

    lookup = RepositoryStructuralLookup(projection)
    all_facts: list[Any] = []
    exact = lookup.lookup_symbol(subject)
    if exact is not None:
        all_facts.append(exact)
    all_facts.extend(lookup.symbols_in_module(subject))
    all_facts.extend(lookup.imports_from(subject))
    normalized_all = [_normalize_fact(fact) for fact in all_facts]

    return observed_a, observed_b, normalized_all


def _observed(
    output: str,
    provider: DeterministicEvaluationProvider,
) -> dict[str, Any]:
    fields = _parse_output_fields(output)
    packet: dict[str, Any] | None = None
    if provider.requests:
        packet = json.loads(provider.requests[-1].prompt)

    structural = []
    if packet is not None:
        structural = [
            _normalize_packet_fact(fact)
            for fact in packet.get("structural_evidence", [])
        ]

    return {
        "baseline_commit": fields["baseline_commit"],
        "status": fields["status"],
        "repository_evidence_count": int(fields["repository_evidence_count"]),
        "knowledge_evidence_count": int(fields["knowledge_evidence_count"]),
        "structural_evidence_count": int(fields["structural_evidence_count"]),
        "repository_citation_count": int(fields["repository_citation_count"]),
        "knowledge_citation_count": int(fields["knowledge_citation_count"]),
        "structural_citation_count": int(fields["structural_citation_count"]),
        "model_inference_count": int(fields["model_inference_count"]),
        "context_truncated": fields["context_truncated"] == "true",
        "structural_facts": structural,
    }


def _parse_output_fields(output: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in output.splitlines():
        if line in {"ANALYSIS", "EVIDENCE_REFERENCES"}:
            continue
        if ": " not in line:
            continue
        key, value = line.split(": ", 1)
        if key in {
            "baseline_commit",
            "status",
            "repository_evidence_count",
            "knowledge_evidence_count",
            "structural_evidence_count",
            "repository_citation_count",
            "knowledge_citation_count",
            "structural_citation_count",
            "model_inference_count",
            "context_truncated",
        }:
            fields[key] = value

    required = {
        "baseline_commit",
        "status",
        "repository_evidence_count",
        "knowledge_evidence_count",
        "structural_evidence_count",
        "repository_citation_count",
        "knowledge_citation_count",
        "structural_citation_count",
        "model_inference_count",
        "context_truncated",
    }
    if set(fields) != required:
        raise RuntimeError("unexpected E2 observable output surface")
    return fields


def _normalize_fact(fact: Any) -> dict[str, Any]:
    if hasattr(fact, "qualified_name"):
        return {
            "fact_type": "symbol",
            "module_name": fact.module_name,
            "qualified_name": fact.qualified_name,
            "kind": fact.kind,
        }
    return {
        "fact_type": "import",
        "source_module": fact.source_module,
        "target_module": fact.target_module,
        "imported_name": fact.imported_name,
        "relative_level": fact.relative_level,
    }


def _normalize_packet_fact(fact: dict[str, Any]) -> dict[str, Any]:
    if fact["fact_type"] == "symbol":
        return {
            "fact_type": "symbol",
            "module_name": fact["module_name"],
            "qualified_name": fact["qualified_name"],
            "kind": fact["kind"],
        }
    return {
        "fact_type": "import",
        "source_module": fact["source_module"],
        "target_module": fact["target_module"],
        "imported_name": fact["imported_name"],
        "relative_level": fact["relative_level"],
    }


def _non_structural_signature(observed: dict[str, Any]) -> tuple[Any, ...]:
    return (
        observed["status"],
        observed["repository_evidence_count"],
        observed["knowledge_evidence_count"],
        observed["context_truncated"],
    )


def _evaluate_case(
    case: dict[str, Any],
    temp_root: Path,
) -> tuple[dict[str, Any], dict[str, int]]:
    repo, fixture_baseline = _create_fixture(
        temp_root,
        case["fixture_profile"],
    )
    observed_a, observed_b, all_facts = _execute_pair(
        repo,
        case["subject"],
    )

    mismatches: list[str] = []
    invalid = False

    if observed_a["baseline_commit"] != observed_b["baseline_commit"]:
        invalid = True
        mismatches.append("paired baseline mismatch")
    if observed_a["baseline_commit"] != fixture_baseline:
        invalid = True
        mismatches.append("A baseline != fixture baseline")
    if observed_b["baseline_commit"] != fixture_baseline:
        invalid = True
        mismatches.append("B baseline != fixture baseline")

    if observed_a["status"] != case["expected_a_status"]:
        mismatches.append("A status mismatch")
    if observed_b["status"] != case["expected_b_status"]:
        mismatches.append("B status mismatch")

    expected_facts = case["expected_structural_facts"]
    emitted_expected = expected_facts[
        : case["expected_emitted_structural_count"]
    ]

    if all_facts != expected_facts:
        mismatches.append("structural ground truth mismatch")
    if observed_b["structural_facts"] != emitted_expected:
        mismatches.append("emitted structural facts mismatch")
    if (
        observed_b["structural_evidence_count"]
        != case["expected_emitted_structural_count"]
    ):
        mismatches.append("emitted structural count mismatch")
    if observed_b["context_truncated"] != case["expected_context_truncated"]:
        mismatches.append("B context_truncated mismatch")

    if case["expected_total_structural_count"] == 0:
        if (
            _non_structural_signature(observed_a)
            != _non_structural_signature(observed_b)
        ):
            mismatches.append("non-structural A/B regression")

    case_result = (
        "INVALID"
        if invalid
        else ("PASS" if not mismatches else "FAIL")
    )

    structural_coverage_gain = int(
        case["expected_total_structural_count"] > 0
        and observed_a["status"] == "UNCONFIRMED"
        and observed_b["status"] == "GROUNDED"
    )
    unexpected_activation = int(
        case["expected_total_structural_count"] == 0
        and observed_b["structural_evidence_count"] > 0
    )
    structural_mismatch = int(
        "structural ground truth mismatch" in mismatches
        or "emitted structural facts mismatch" in mismatches
        or "emitted structural count mismatch" in mismatches
    )
    non_structural_regression = int(
        "non-structural A/B regression" in mismatches
    )
    invalid_baseline = int(invalid)

    result = {
        "case_id": case["case_id"],
        "case_result": case_result,
        "expected": {
            "a_status": case["expected_a_status"],
            "b_status": case["expected_b_status"],
            "total_structural_count": case[
                "expected_total_structural_count"
            ],
            "emitted_structural_count": case[
                "expected_emitted_structural_count"
            ],
            "context_truncated": case["expected_context_truncated"],
            "structural_facts": expected_facts,
        },
        "observed_a": observed_a,
        "observed_b": observed_b,
        "mismatches": mismatches,
    }
    metrics = {
        "structural_coverage_gain_count": structural_coverage_gain,
        "unexpected_structural_activation_count": unexpected_activation,
        "structural_fact_mismatch_count": structural_mismatch,
        "non_structural_regression_count": non_structural_regression,
        "invalid_paired_baseline_count": invalid_baseline,
    }
    return result, metrics


def main() -> int:
    case_set, case_bytes = _load_case_set()
    candidate_sha = _official_candidate_sha()
    runner_bytes = Path(__file__).read_bytes()

    aggregate = {
        "structural_coverage_gain_count": 0,
        "unexpected_structural_activation_count": 0,
        "structural_fact_mismatch_count": 0,
        "non_structural_regression_count": 0,
        "invalid_paired_baseline_count": 0,
    }
    case_results: list[dict[str, Any]] = []

    with tempfile.TemporaryDirectory(prefix="malak-e2-eval-") as tmp:
        tmp_root = Path(tmp)
        for index, case in enumerate(case_set["cases"]):
            case_root = tmp_root / f"case-{index + 1:02d}"
            case_root.mkdir()
            result, metrics = _evaluate_case(case, case_root)
            case_results.append(result)
            for key, value in metrics.items():
                aggregate[key] += value

    has_case_failure = any(
        item["case_result"] in {"FAIL", "INVALID"}
        for item in case_results
    )
    has_blocking_metric = any(
        aggregate[key] != 0
        for key in (
            "unexpected_structural_activation_count",
            "structural_fact_mismatch_count",
            "non_structural_regression_count",
            "invalid_paired_baseline_count",
        )
    )
    conformance = (
        "FAIL"
        if has_case_failure or has_blocking_metric
        else "PASS"
    )

    evaluation_identity = {
        "malak_baseline_sha": candidate_sha,
        "case_set_schema_version": case_set["schema_version"],
        "case_set_digest": _sha256_bytes(case_bytes),
        "runner_version": RUNNER_VERSION,
        "runner_digest": _sha256_bytes(runner_bytes),
        "provider_policy_version": PROVIDER_POLICY_VERSION,
        "provider_policy_digest": _sha256_bytes(PROVIDER_POLICY),
    }

    output = {
        "baseline_commit": candidate_sha,
        "case_count": len(case_results),
        "case_results": case_results,
        **aggregate,
        "conformance_result": conformance,
        "utility_observation": {
            "structural_coverage_gain_count": aggregate[
                "structural_coverage_gain_count"
            ],
            "interpretation": (
                "coverage observation only; conformance PASS does not imply "
                "answer quality or E3/E4 propagation approval"
            ),
            "evaluation_identity": evaluation_identity,
            "authority_effect": "none",
        },
    }
    sys.stdout.write(
        json.dumps(
            output,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
