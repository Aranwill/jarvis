"""Contrato V1 de PR #328: checkpoint RED, sin modelos ni casos del piloto."""
from __future__ import annotations

import json
from importlib import import_module

import pytest

from test_engineering_inspect import RecordingProvider, build_capability, execute
from test_e3_structured_evidence_role_binding_v0 import (
    RELATION_ID, _capability, _execute, _repository_evidence, _knowledge_evidence,
)


def _e2(**updates):
    payload = {
        "schema_id": "malak.e2.assertions.v1",
        "summary": "Inspección acotada.",
        "assertions": [{"kind": "OBSERVED", "text": "Implementación observada.", "evidence_refs": ["R1"]}],
        "uncertainties": ["La semántica requiere evaluación adicional."],
    }
    payload.update(updates)
    return payload


def _e3(**finding_updates):
    finding = {
        "relation_id": RELATION_ID,
        "classification": "ALIGNED",
        "statement": "Implementación relacionada con la especificación.",
        "rationale": "Las evidencias seleccionadas describen esa relación.",
        "evidence_roles": {"K1": "SUPPORT", "R1": "SUPPORT"},
        "uncertainty_basis": "NONE",
    }
    finding.update(finding_updates)
    return {"schema_id": "malak.e3.ref-role-map.v1", "summary": "Análisis acotado.", "findings": [finding], "uncertainties": []}


def _parse(raw, repository=None, knowledge=None):
    return import_module("malak.capabilities.engineering_analyze")._parse_analysis(
        raw,
        repository_evidence=_repository_evidence() if repository is None else repository,
        knowledge_evidence=_knowledge_evidence() if knowledge is None else knowledge,
        allowed_relation_ids=(RELATION_ID,),
    )


def test_e2_v1_renders_valid_assertions_without_wire_json(tmp_path):
    provider = RecordingProvider(json.dumps(_e2(), ensure_ascii=False))
    *_, capability = build_capability(tmp_path, provider=provider)
    rendered = execute(capability)
    analysis = rendered.split("\nANALYSIS\n", 1)[1].split("\nEVIDENCE_REFERENCES", 1)[0]
    assert "OBSERVED" in analysis and "[R1]" in analysis
    assert '"schema_id"' not in analysis
    assert "La semántica requiere evaluación adicional." in analysis
    assert provider.calls == 1 and provider.requests[0].history == ()
    assert "authority_effect: none" in rendered


def test_e2_v1_schema_contains_only_available_refs(tmp_path):
    provider = RecordingProvider(json.dumps(_e2()))
    *_, capability = build_capability(tmp_path, provider=provider)
    execute(capability)
    request = provider.requests[0]
    assert request.response_json_schema is not None
    schema = json.loads(request.response_json_schema)
    assert schema["properties"]["schema_id"]["const"] == "malak.e2.assertions.v1"
    assert set(schema["required"]) == {"schema_id", "summary", "assertions", "uncertainties"}
    assert schema["additionalProperties"] is False
    packet = json.loads(request.prompt)
    allowed = {e["ref"] for group in ("repository_evidence", "knowledge_evidence", "structural_evidence") for e in packet[group]}
    refs = schema["properties"]["assertions"]["items"]["properties"]["evidence_refs"]
    assert set(refs["items"]["enum"]) == allowed
    assert not any(ref.startswith("S") for ref in allowed)
    assert "[S#]" not in request.system_prompt


@pytest.mark.parametrize("change", [
    {"schema_id": "malak.e2.assertions.v0"},
    {"extra": True},
    {"summary": "Conclusión [R1]"},
    {"summary": "Conclusión [S1]"},
    {"uncertainties": ["Limitación [A1]"]},
    {"assertions": [{"kind": "OBSERVED", "text": "Hecho", "evidence_refs": ["S1"]}]},
    {"assertions": [{"kind": "OBSERVED", "text": "Hecho", "evidence_refs": ["K1"]}]},
    {"assertions": [{"kind": "KNOWLEDGE_CONTEXT", "text": "Contexto", "evidence_refs": ["R1"]}]},
    {"assertions": [{"kind": "INTERPRETATION", "text": "Inferencia", "evidence_refs": []}]},
    {"assertions": [{"kind": "OBSERVED", "text": "Hecho", "evidence_refs": ["R1", "R1"]}]},
    {"assertions": [{"kind": "OBSERVED", "text": "á" * 2049, "evidence_refs": ["R1"]}]},
    {"summary": "á" * 4097},
    {"uncertainties": ["á" * 2049]},
    {"uncertainties": ["Límite"] * 17},
    {"assertions": _e2()["assertions"] * 17},
    {"assertions": "invalid"},
    {"assertions": [{"kind": "OBSERVED", "text": "Hecho", "evidence_refs": [True]}]},
    {"assertions": [{"kind": "OBSERVED", "text": "Hecho", "evidence_refs": ["R1"], "extra": 1}]},
])
def test_e2_v1_rejects_invalid_without_retry(tmp_path, change):
    provider = RecordingProvider(json.dumps(_e2(**change), ensure_ascii=False))
    *_, capability = build_capability(tmp_path, provider=provider)
    with pytest.raises(RuntimeError):
        execute(capability)
    assert provider.calls == 1


@pytest.mark.parametrize("raw", [
    '{"schema_id":"malak.e2.assertions.v1","summary":"Uno","summary":"Dos","assertions":[],"uncertainties":[]}',
    '{"schema_id":"malak.e2.assertions.v1","summary":NaN,"assertions":[],"uncertainties":[]}',
    '{"schema_id":"malak.e2.assertions.v1",',
    'Texto libre que antes se aceptaba.',
])
def test_e2_v1_rejects_malformed_and_legacy_without_fallback(tmp_path, raw):
    provider = RecordingProvider(raw)
    *_, capability = build_capability(tmp_path, provider=provider)
    with pytest.raises(RuntimeError):
        execute(capability)
    assert provider.calls == 1


def test_e3_v1_projects_roles_and_preserves_text_and_classification():
    payload = _e3()
    finding = _parse(json.dumps(payload)).findings[0]
    assert finding.classification == payload["findings"][0]["classification"]
    assert finding.statement == payload["findings"][0]["statement"]
    assert finding.rationale == payload["findings"][0]["rationale"]
    assert finding.supporting_repository_refs == ("R1",)
    assert finding.supporting_knowledge_refs == ("K1",)
    assert finding.limiting_or_counterevidence_refs == ()


def test_e3_v1_limit_is_not_silently_promoted_to_support():
    payload = _e3(classification="UNRESOLVED", evidence_roles={"R1": "LIMIT"}, uncertainty_basis="INSUFFICIENT_SUPPLIED_EVIDENCE")
    finding = _parse(json.dumps(payload)).findings[0]
    assert finding.supporting_repository_refs == ()
    assert finding.supporting_knowledge_refs == ()
    assert finding.limiting_or_counterevidence_refs == ("R1",)
    assert finding.classification == "UNRESOLVED"
    assert finding.uncertainty_basis == "INSUFFICIENT_SUPPLIED_EVIDENCE"


def test_e3_v1_omission_does_not_add_implicit_support():
    finding = _parse(json.dumps(_e3(classification="UNRESOLVED", evidence_roles={}, uncertainty_basis="INSUFFICIENT_SUPPLIED_EVIDENCE"))).findings[0]
    assert finding.evidence_refs == ()
    assert finding.supporting_repository_refs == finding.supporting_knowledge_refs == ()


def test_e3_v1_projection_uses_bundle_order_not_model_order():
    repository = _repository_evidence() + [{**_repository_evidence()[0], "ref": "R2"}]
    payload = _e3(evidence_roles={"R2": "SUPPORT", "K1": "SUPPORT", "R1": "SUPPORT"})
    finding = _parse(json.dumps(payload), repository=repository).findings[0]
    assert finding.supporting_repository_refs == ("R1", "R2")


def test_e3_v1_rejects_unknown_refs_after_decoding_version():
    with pytest.raises(RuntimeError, match="(?i)(unknown|not allowed|unavailable).*(ref|evidence)|(ref|evidence).*(unknown|not allowed|unavailable)"):
        _parse(json.dumps(_e3(evidence_roles={"R1": "SUPPORT", "K1": "SUPPORT", "R999": "LIMIT"})))


def test_e3_v1_duplicate_role_key_is_rejected_before_projection():
    raw = json.dumps(_e3()).replace('"K1": "SUPPORT"', '"K1":"SUPPORT","K1":"LIMIT"')
    with pytest.raises(RuntimeError, match="(?i)(duplicate|strict JSON)"):
        _parse(raw)


def test_e3_v1_schema_uses_sparse_exclusive_roles(tmp_path):
    provider, capability = _capability(tmp_path, response=json.dumps(_e3()))
    try:
        _execute(capability)
    except RuntimeError:
        # El baseline rechaza V1; igualmente se inspecciona el request real.
        pass
    request = provider.requests[0]
    schema = json.loads(request.response_json_schema)
    assert schema["properties"]["schema_id"]["const"] == "malak.e3.ref-role-map.v1"
    finding = schema["properties"]["findings"]["items"]
    assert "evidence_roles" in finding["required"]
    assert "supporting_repository_refs" not in finding["properties"]
    roles = finding["properties"]["evidence_roles"]
    assert roles["additionalProperties"] is False and roles["maxProperties"] == 16
    assert not roles.get("required")
    packet = json.loads(request.prompt)
    allowed = {e["ref"] for group in ("repository_evidence", "knowledge_evidence") for e in packet[group]}
    assert set(roles["properties"]) == allowed
    assert all(set(item["enum"]) == {"SUPPORT", "LIMIT"} for item in roles["properties"].values())
    assert provider.calls == 1 and request.history == ()


def test_e3_v1_real_capability_keeps_canonical_output(tmp_path):
    provider, capability = _capability(tmp_path, response=json.dumps(_e3()))
    rendered = _execute(capability)
    assert "supporting_repository_refs: [R1]" in rendered
    assert "supporting_knowledge_refs: [K1]" in rendered
    assert "semantic_assurance: NOT_VERIFIED" in rendered
    assert "authority_effect: none" in rendered
    assert '"evidence_roles"' not in rendered
    assert provider.calls == 1


def test_e3_v1_empty_catalog_has_no_empty_enum():
    module = import_module("malak.capabilities.engineering_analyze")
    schema = json.loads(module._build_relation_response_json_schema((RELATION_ID,), (), ()))
    roles = schema["properties"]["findings"]["items"]["properties"]["evidence_roles"]
    assert roles["properties"] == {} and roles["additionalProperties"] is False
    assert '"enum": []' not in json.dumps(schema)


def test_e3_v1_schema_overflow_fails_before_generation(tmp_path, monkeypatch):
    module = import_module("malak.capabilities.engineering_analyze")
    build = module._build_relation_response_json_schema
    # Inyección sólo en test; valida el guard sobre el schema efectivo, no el sizing teórico.
    def oversized(*args):
        schema = json.loads(build(*args))
        schema["description"] = "x" * 65537
        return json.dumps(schema, separators=(",", ":"))
    monkeypatch.setattr(module, "_build_relation_response_json_schema", oversized)
    provider, capability = _capability(tmp_path, response=json.dumps(_e3()))
    with pytest.raises(RuntimeError, match="(?i)schema.*(byte|limit|exceed)"):
        _execute(capability)
    assert provider.calls == 0
