"""Contrato V1 de PR #328: checkpoint RED, sin modelos ni casos del piloto."""
from __future__ import annotations

import hashlib
import json
import traceback
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
    raw = json.dumps(_e3(classification="UNRESOLVED", evidence_roles={}, uncertainty_basis="INSUFFICIENT_SUPPLIED_EVIDENCE"))
    module = import_module("malak.capabilities.engineering_analyze")
    projected = json.loads(module._project_role_map(raw, _repository_evidence(), _knowledge_evidence()))["findings"][0]
    assert projected["supporting_repository_refs"] == projected["supporting_knowledge_refs"] == []
    with pytest.raises(RuntimeError, match="at least one bound evidence ref"):
        _parse(raw)


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
    with pytest.raises(ValueError, match="(?i)schema.*(byte|limit|exceed)"):
        _execute(capability)
    assert provider.calls == 0


@pytest.mark.parametrize("roles", [
    {"R1": "UNUSED"}, {"R1": "support"}, {"R1": ["SUPPORT", "LIMIT"]},
    {"R1": True}, {"R1": None}, [], "SUPPORT",
])
def test_e3_v1_invalid_role_shapes_fail_closed(roles):
    with pytest.raises(RuntimeError):
        _parse(json.dumps(_e3(evidence_roles=roles)))


@pytest.mark.parametrize("field", ["statement", "rationale"])
@pytest.mark.parametrize("ref", ["R1", "K1", "S1", "A1"])
def test_e3_v1_text_cannot_smuggle_reserved_refs(field, ref):
    with pytest.raises(RuntimeError, match="reserved"):
        _parse(json.dumps(_e3(**{field: f"Texto [{ref}]"})))


@pytest.mark.parametrize("change", [
    {"schema_id": "malak.e3.ref-role-map.v0"}, {"extra": True},
    {"summary": "Texto [S1]"}, {"uncertainties": ["Texto [S1]"]},
    {"findings": []}, {"findings": _e3()["findings"] * 17},
    {"summary": "á" * 4097}, {"uncertainties": ["á" * 2049]},
])
def test_e3_v1_invalid_envelopes_and_utf8_fail_closed(change):
    payload = _e3()
    payload.update(change)
    with pytest.raises(RuntimeError):
        _parse(json.dumps(payload, ensure_ascii=False))


def test_e3_v1_ref_budget_is_not_expanded_by_projection():
    repository = [{**_repository_evidence()[0], "ref": f"R{i}"} for i in range(1, 18)]
    with pytest.raises(RuntimeError, match="16"):
        _parse(json.dumps(_e3(evidence_roles={row["ref"]: "LIMIT" for row in repository})), repository=repository)


def test_e3_v1_duplicate_relation_coverage_is_still_rejected():
    payload = _e3()
    payload["findings"] *= 2
    with pytest.raises(RuntimeError, match="exactly once|duplicate"):
        _parse(json.dumps(payload))


def test_e3_v1_does_not_repair_the_old_overlapping_format():
    from test_e3_structured_evidence_role_binding_v0 import _role_finding
    finding = _role_finding(limiting_or_counterevidence_refs=["R1"])
    raw = json.dumps({"summary": "Legacy", "findings": [finding], "uncertainties": []})
    with pytest.raises(RuntimeError, match="schema_id"):
        _parse(raw)
    # La barrera canónica sigue rechazando exactamente el overlap original.
    module = import_module("malak.capabilities.engineering_analyze")
    with pytest.raises(RuntimeError, match="overlap"):
        module._parse_canonical_analysis(raw, repository_evidence=_repository_evidence(),
                                        knowledge_evidence=_knowledge_evidence(),
                                        allowed_relation_ids=(RELATION_ID,))


def test_e2_v1_schema_overflow_makes_zero_provider_calls(tmp_path, monkeypatch):
    module = import_module("malak.capabilities.engineering_inspect")
    builder = module._build_inspection_response_json_schema
    def oversized(*args):
        schema = json.loads(builder(*args))
        schema["description"] = "á" * 32769
        return json.dumps(schema, ensure_ascii=False)
    monkeypatch.setattr(module, "_build_inspection_response_json_schema", oversized)
    provider = RecordingProvider(json.dumps(_e2()))
    *_, capability = build_capability(tmp_path, provider=provider)
    with pytest.raises(RuntimeError, match="schema.*UTF-8"):
        execute(capability)
    assert provider.calls == 0


def test_e2_v1_empty_catalog_does_not_generate_empty_enums():
    module = import_module("malak.capabilities.engineering_inspect")
    schema = json.loads(module._build_inspection_response_json_schema([], [], []))
    refs = schema["properties"]["assertions"]["items"]["properties"]["evidence_refs"]
    assert refs["maxItems"] == 0
    assert '"enum": []' not in json.dumps(schema)


def test_e2_v1_uncertainty_without_refs_is_preserved(tmp_path):
    provider = RecordingProvider(json.dumps(_e2(assertions=[{"kind": "UNCERTAINTY", "text": "Sin evidencia suficiente.", "evidence_refs": []}])))
    *_, capability = build_capability(tmp_path, provider=provider)
    assert "UNCERTAINTY: Sin evidencia suficiente." in execute(capability)
    assert provider.calls == 1


def test_e3_v1_exhaustive_projection_preserves_selected_set_without_overlap():
    import itertools
    module = import_module("malak.capabilities.engineering_analyze")
    repository = [{**_repository_evidence()[0], "ref": f"R{i}"} for i in range(1, 4)]
    knowledge = [{**_knowledge_evidence()[0], "ref": f"K{i}"} for i in range(1, 4)]
    refs = [item["ref"] for item in repository + knowledge]
    original_catalog = json.dumps([repository, knowledge], sort_keys=True)
    for choices in itertools.product((None, "SUPPORT", "LIMIT"), repeat=len(refs)):
        roles = {ref: role for ref, role in zip(refs, choices) if role is not None}
        raw = json.dumps(_e3(evidence_roles=roles))
        projected = json.loads(module._project_role_map(raw, repository, knowledge))["findings"][0]
        support = projected["supporting_repository_refs"] + projected["supporting_knowledge_refs"]
        limits = projected["limiting_or_counterevidence_refs"]
        assert not set(support) & set(limits)
        assert set(support + limits) == set(roles)
        assert all(roles[ref] == "SUPPORT" for ref in support)
        assert all(roles[ref] == "LIMIT" for ref in limits)
    assert json.dumps([repository, knowledge], sort_keys=True) == original_catalog


# ---------------------------------------------------------------------------
# #330 / PR-B RED — E2 output contract alignment after C01 Attempt 1
# No models, no pilot cases, no retries. These tests freeze the accepted
# PR-A design against the post-merge baseline before GREEN.
# ---------------------------------------------------------------------------

def _focused_e2_capability(tmp_path, provider):
    from test_engineering_inspect import build_service
    from test_governed_engineering_evidence_focus_v0 import _focus, _make_repo

    _, reader, knowledge = _make_repo(tmp_path)
    module = import_module("malak.capabilities.engineering_inspect")
    capability = module.EngineeringInspectCapability(
        repository_reader=reader,
        knowledge_reader=knowledge,
        conversation_service=build_service(provider),
        provider_name="recording",
        model="test-model",
        evidence_focus=_focus(),
    )
    return capability


def _canonical_json(value) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _assert_safe_e2_rejection(tmp_path, raw: str, forbidden_fragments):
    provider = RecordingProvider(raw)
    capability = _focused_e2_capability(tmp_path, provider)

    with pytest.raises(RuntimeError) as caught:
        execute(capability, "Kernel")

    exc = caught.value
    public = str(exc)
    metadata = json.loads(public)

    assert metadata == {
        "authority_effect": "none",
        "output_bytes": len(raw.encode("utf-8")),
        "output_sha256": hashlib.sha256(raw.encode("utf-8")).hexdigest(),
        "reason_code": "E2_OUTPUT_CONTRACT_REJECTED",
        "validator_code": "DETERMINISTIC_VALIDATION_REJECTED",
        "validator_detail": "E2 output rejected by deterministic contract validation.",
    }

    # The registrable/public error boundary must not expose rejected content
    # through args, cause/context or the formatted traceback.
    assert exc.__cause__ is None
    assert exc.__context__ is None
    exposed = "\n".join(
        (
            public,
            repr(exc.args),
            "".join(traceback.format_exception(exc)),
        )
    )
    for fragment in forbidden_fragments:
        assert fragment not in exposed

    assert provider.calls == 1


def test_e2_contract_alignment_red_focused_prompt_mirrors_one_canonical_schema(
    tmp_path,
):
    provider = RecordingProvider(json.dumps(_e2(), ensure_ascii=False))
    capability = _focused_e2_capability(tmp_path, provider)

    execute(capability, "Kernel")

    assert provider.calls == 1
    request = provider.requests[0]
    prompt = json.loads(request.prompt)
    schema = json.loads(request.response_json_schema)

    assert set(prompt) == {"response_contract", "evidence_packet"}
    assert _canonical_json(prompt["response_contract"]) == request.response_json_schema

    evidence = prompt["evidence_packet"]
    assert "repository_evidence" in evidence
    assert "knowledge_evidence" in evidence
    assert "focus" in evidence
    assert "repository_evidence" not in prompt
    assert "knowledge_evidence" not in prompt

    summary = schema["properties"]["summary"]
    assertion_text = schema["properties"]["assertions"]["items"]["properties"]["text"]
    uncertainty = schema["properties"]["uncertainties"]["items"]

    for field in (summary, assertion_text, uncertainty):
        description = field.get("description", "")
        assert "evidence_refs" in description
        assert "R1" in description
        assert "K2" in description
        assert "S3" in description
        assert "A1" in description


def test_e2_contract_alignment_red_nonfocused_prompt_keeps_existing_packet_shape(
    tmp_path,
):
    provider = RecordingProvider(json.dumps(_e2(), ensure_ascii=False))
    *_, capability = build_capability(tmp_path, provider=provider)

    execute(capability)

    assert provider.calls == 1
    prompt = json.loads(provider.requests[0].prompt)
    assert "response_contract" not in prompt
    assert "evidence_packet" not in prompt
    assert "repository_evidence" in prompt
    assert "knowledge_evidence" in prompt


def test_e2_contract_alignment_red_combined_focused_prompt_overflow_is_pre_provider(
    tmp_path,
    monkeypatch,
):
    module = import_module("malak.capabilities.engineering_inspect")
    original = module._build_inspection_response_json_schema

    def large_but_individually_valid_schema(*args):
        schema = json.loads(original(*args))
        schema["description"] = "x" * 63500
        encoded = _canonical_json(schema)
        assert len(encoded.encode("utf-8")) < 64 * 1024
        return encoded

    monkeypatch.setattr(
        module,
        "_build_inspection_response_json_schema",
        large_but_individually_valid_schema,
    )

    provider = RecordingProvider(json.dumps(_e2(), ensure_ascii=False))
    capability = _focused_e2_capability(tmp_path, provider)

    with pytest.raises(RuntimeError, match="prompt.*UTF-8"):
        execute(capability, "Kernel")

    assert provider.calls == 0


def test_e2_contract_alignment_red_unknown_ref_cannot_escape_in_metadata(tmp_path):
    marker = "SYNTHETIC_REJECTED_CONTENT_DO_NOT_PERSIST\nFORGED_METADATA=YES"
    raw = json.dumps(
        _e2(
            assertions=[
                {
                    "kind": "OBSERVED",
                    "text": "Hecho observado.",
                    "evidence_refs": [marker],
                }
            ]
        ),
        ensure_ascii=False,
    )

    _assert_safe_e2_rejection(
        tmp_path,
        raw,
        (marker, "FORGED_METADATA=YES"),
    )


def test_e2_contract_alignment_red_long_multibyte_unknown_ref_is_not_disclosed(
    tmp_path,
):
    marker = ("Ω" * 2000) + "\nFORGED_MULTIBYTE=YES"
    raw = json.dumps(
        _e2(
            assertions=[
                {
                    "kind": "OBSERVED",
                    "text": "Hecho observado.",
                    "evidence_refs": [marker],
                }
            ]
        ),
        ensure_ascii=False,
    )

    _assert_safe_e2_rejection(
        tmp_path,
        raw,
        ("FORGED_MULTIBYTE=YES", "Ω" * 32),
    )


def test_e2_contract_alignment_red_reserved_ref_rejection_uses_safe_metadata(
    tmp_path,
):
    raw = json.dumps(
        _e2(
            assertions=[
                {
                    "kind": "OBSERVED",
                    "text": "No citar [R1] aquí.",
                    "evidence_refs": ["R1"],
                }
            ]
        ),
        ensure_ascii=False,
    )

    _assert_safe_e2_rejection(tmp_path, raw, ("No citar [R1] aquí.",))


def test_e2_contract_alignment_red_invalid_json_rejection_uses_safe_metadata(
    tmp_path,
):
    marker = "FORGED_INVALID_JSON=YES"
    raw = (
        '{"schema_id":"malak.e2.assertions.v1",'
        '"summary":"' + marker + '",'
        '"assertions":['
    )

    _assert_safe_e2_rejection(tmp_path, raw, (marker,))


def test_e2_contract_alignment_red_duplicate_key_rejection_uses_safe_metadata(
    tmp_path,
):
    marker = "FORGED_DUPLICATE_KEY\nYES"
    quoted = json.dumps(marker)
    raw = (
        '{"schema_id":"malak.e2.assertions.v1",'
        '"summary":"ok",'
        '"assertions":[{'
        '"kind":"OBSERVED",'
        '"text":"Hecho",'
        '"evidence_refs":["R1"],'
        + quoted + ':1,'
        + quoted + ':2'
        '}],'
        '"uncertainties":[]}'
    )

    _assert_safe_e2_rejection(
        tmp_path,
        raw,
        (marker, "FORGED_DUPLICATE_KEY"),
    )



@pytest.mark.parametrize(
    "field",
    ("summary", "assertion_text", "uncertainty"),
)
def test_e2_contract_alignment_surrogate_rejection_uses_safe_metadata(
    tmp_path,
    field,
):
    marker = "SYNTHETIC_REJECTED_SURROGATE"
    rejected = marker + chr(0xD800)
    payload = _e2()

    if field == "summary":
        payload["summary"] = rejected
    elif field == "assertion_text":
        payload["assertions"] = [
            {
                "kind": "OBSERVED",
                "text": rejected,
                "evidence_refs": ["R1"],
            }
        ]
    else:
        payload["uncertainties"] = [rejected]

    raw = json.dumps(payload)
    _assert_safe_e2_rejection(
        tmp_path,
        raw,
        (marker,),
    )
