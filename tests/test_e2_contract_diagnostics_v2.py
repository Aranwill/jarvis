"""RED de #334: contratos prospectivos sintéticos; cero modelos/casos del piloto."""
from __future__ import annotations

import hashlib
import json
import traceback
from importlib import import_module

import pytest

from test_engineering_inspect import RecordingProvider, build_capability, execute
from test_e2_e3_contract_reliability_v1 import _focused_e2_capability


def _payload(**updates):
    value = {
        "schema_id": "malak.e2.assertions.v1",
        "summary": "Inspección acotada.",
        "assertions": [{
            "kind": "OBSERVED", "text": "Hecho observado.",
            "evidence_refs": ["R1"],
        }],
        "uncertainties": [],
    }
    value.update(updates)
    return value


def _wire(**updates):
    return json.dumps(_payload(**updates), ensure_ascii=True)


def _assertion(**updates):
    value = _payload()["assertions"][0]
    value.update(updates)
    return [value]


def _error(tmp_path, raw, *, focused=True):
    tmp_path.mkdir(parents=True, exist_ok=True)
    provider = RecordingProvider(raw)
    if focused:
        capability = _focused_e2_capability(tmp_path, provider)
        subject = "Kernel"
    else:
        *_, capability = build_capability(tmp_path, provider=provider)
        subject = "needle"
    with pytest.raises(RuntimeError) as caught:
        execute(capability, subject)
    assert provider.calls == 1  # ningún retry/repair ni segunda generación
    error = caught.value
    assert error.__cause__ is None and error.__context__ is None
    assert len(str(error).encode("utf-8")) < 1024
    metadata = json.loads(str(error))
    assert set(metadata) == {
        "authority_effect", "output_bytes", "output_sha256", "output_encoding",
        "reason_code", "validator_code", "validator_detail",
        "validator_subcode", "validator_field",
    }
    assert metadata["authority_effect"] == "none"
    assert metadata["reason_code"] == "E2_OUTPUT_CONTRACT_REJECTED"
    assert metadata["validator_code"] == "DETERMINISTIC_VALIDATION_REJECTED"
    assert metadata["validator_detail"] == "E2 output rejected by deterministic contract validation."
    try:
        encoded = raw.encode("utf-8")
    except UnicodeEncodeError:
        assert metadata["output_encoding"] == "INVALID_UTF8"
        assert metadata["output_bytes"] is None
        assert metadata["output_sha256"] is None
    else:
        assert metadata["output_encoding"] == "UTF8"
        assert metadata["output_bytes"] == len(encoded)
        assert metadata["output_sha256"] == hashlib.sha256(encoded).hexdigest()
    return metadata, error


@pytest.mark.parametrize("raw,subcode,field", [
    pytest.param(raw,code,field,id=f"{code}-{field}")
    for raw,code,field in [
    ("", "OUTPUT_EMPTY", "output"),
    ("x" * 65537, "OUTPUT_LIMIT", "output"),
    ("\ud800", "OUTPUT_INVALID_UNICODE", "output"),
    ('{"summary":', "JSON_SYNTAX", "output"),
    ('{"secret_unknown_key":1,"secret_unknown_key":2}', "JSON_DUPLICATE_KEYS", "output"),
    ('{"summary":NaN}', "JSON_NONFINITE", "output"),
    ('[]', "ROOT_TYPE", "output"),
    (_wire(secret_unknown_key=True), "EXACT_KEYS", "output"),
    (_wire(schema_id="secret_schema"), "SCHEMA_ID", "schema_id"),
    (_wire(summary=None), "TEXT_TYPE", "summary"),
    (_wire(summary=" "), "TEXT_EMPTY", "summary"),
    (_wire(summary="line\nsecret_payload"), "TEXT_CONTROL", "summary"),
    (_wire(summary="secret\u200bpayload"), "TEXT_CONTROL", "summary"),
    (_wire(summary="secret_payload R777"), "TEXT_RESERVED_REF", "summary"),
    (_wire(summary="á" * 4097), "TEXT_UTF8_BYTES", "summary"),
    (_wire(summary="\ud800"), "TEXT_INVALID_UNICODE", "summary"),
    (_wire(assertions=[{}] * 17), "ASSERTIONS_LIMIT", "assertions"),
    (_wire(assertions={}), "ASSERTIONS_TYPE", "assertions"),
    (_wire(assertions=[1]), "ASSERTION_TYPE", "assertions"),
    (_wire(assertions=_assertion(secret_unknown_key=True)), "EXACT_KEYS", "assertions"),
    (_wire(assertions=_assertion(kind="secret_kind")), "ASSERTION_KIND", "assertions[].kind"),
    (_wire(assertions=_assertion(text=" ")), "TEXT_EMPTY", "assertions[].text"),
    (_wire(assertions=_assertion(text=False)), "TEXT_TYPE", "assertions[].text"),
    (_wire(assertions=_assertion(evidence_refs="R1")), "REFS_TYPE", "assertions[].evidence_refs"),
    (_wire(assertions=_assertion(evidence_refs=["R1"] * 17)), "REFS_LIMIT", "assertions[].evidence_refs"),
    (_wire(assertions=_assertion(evidence_refs=[False])), "REF_TYPE", "assertions[].evidence_refs"),
    (_wire(assertions=_assertion(evidence_refs=["R1", "R1"])), "DUPLICATE_REFS", "assertions[].evidence_refs"),
    (_wire(assertions=_assertion(evidence_refs=["secret_unknown_ref"])), "UNKNOWN_REF", "assertions[].evidence_refs"),
    (_wire(assertions=_assertion(evidence_refs=[])), "MISSING_REFS", "assertions[].evidence_refs"),
    (_wire(assertions=_assertion(evidence_refs=["K1"])), "REF_ROLE", "assertions[].evidence_refs"),
    (_wire(assertions=_assertion(kind="KNOWLEDGE_CONTEXT", evidence_refs=["R1"])), "REF_ROLE", "assertions[].evidence_refs"),
    (_wire(uncertainties=["x"] * 17), "UNCERTAINTIES_LIMIT", "uncertainties"),
    (_wire(uncertainties="secret_payload"), "UNCERTAINTIES_TYPE", "uncertainties"),
    (_wire(uncertainties=[None]), "TEXT_TYPE", "uncertainties[]"),
    (_wire(uncertainties=["\ud800"]), "TEXT_INVALID_UNICODE", "uncertainties[]"),
]])
def test_rejections_are_distinguishable_without_rejected_content(tmp_path, raw, subcode, field):
    metadata, error = _error(tmp_path, raw)
    assert (metadata["validator_subcode"], metadata["validator_field"]) == (subcode, field)
    public = "\n".join((str(error), repr(error.args), "".join(traceback.format_exception(error))))
    for forbidden in ("secret_unknown_key", "secret_schema", "secret_payload", "secret_kind", "secret_unknown_ref", "R777"):
        assert forbidden not in public


def test_causal_diagnostic_collapse_is_closed_for_two_schema_permitted_failures(tmp_path):
    missing, _ = _error(tmp_path / "missing", _wire(assertions=_assertion(evidence_refs=[])))
    wrong_role, _ = _error(tmp_path / "role", _wire(assertions=_assertion(evidence_refs=["K1"])))
    # El baseline ya rechaza ambos, pero pierde la diferencia. No se cambia aceptación.
    assert missing["validator_subcode"] == "MISSING_REFS"
    assert wrong_role["validator_subcode"] == "REF_ROLE"
    assert missing["validator_subcode"] != wrong_role["validator_subcode"]


def test_nonfocused_rejection_uses_the_same_safe_taxonomy(tmp_path):
    metadata, _ = _error(tmp_path, _wire(summary="R777"), focused=False)
    assert (metadata["validator_subcode"], metadata["validator_field"]) == ("TEXT_RESERVED_REF", "summary")


@pytest.mark.parametrize("function,expected", [
    ("_parse_inspection_assertions", "UNCLASSIFIED"),
    ("_validate_model_evidence_refs", "RENDER_REF"),
])
def test_unclassified_and_renderer_failures_do_not_leak(tmp_path, monkeypatch, function, expected):
    module = import_module("malak.capabilities.engineering_inspect")

    def fail(*args, **kwargs):
        raise RuntimeError("secret_payload")

    monkeypatch.setattr(module, function, fail)
    metadata, error = _error(tmp_path, _wire())
    assert (metadata["validator_subcode"], metadata["validator_field"]) == (expected, "output")
    assert "secret_payload" not in "".join(traceback.format_exception(error))


def _schema(repository, knowledge, structural):
    module = import_module("malak.capabilities.engineering_inspect")
    return json.loads(module._build_inspection_response_json_schema(
        repository, knowledge, structural, focused=True,
    ))


def test_focused_schema_excludes_missing_and_wrong_role_refs_by_kind():
    schema = _schema([{"ref": "R1"}], [{"ref": "K1"}], [{"ref": "S1"}])
    items = schema["properties"]["assertions"]["items"]
    branches = {b["properties"]["kind"]["const"]: b for b in items["anyOf"]}
    expected = {
        "OBSERVED": (["R1"], 1),
        "KNOWLEDGE_CONTEXT": (["K1"], 1),
        "INTERPRETATION": (["R1", "K1", "S1"], 1),
        "UNCERTAINTY": (["R1", "K1", "S1"], 0),
    }
    assert set(branches) == set(expected)
    for kind, (refs, minimum) in expected.items():
        branch = branches[kind]
        # Cada alternativa conserva el envelope completo por sí misma.
        assert branch["type"] == "object"
        assert branch["additionalProperties"] is False
        assert set(branch["required"]) == {"kind", "text", "evidence_refs"}
        assert branch["properties"]["text"] == items["properties"]["text"]
        ref_schema = branch["properties"]["evidence_refs"]
        assert ref_schema["type"] == "array"
        assert ref_schema["minItems"] == minimum
        assert ref_schema["maxItems"] == 16
        assert ref_schema["uniqueItems"] is True
        assert ref_schema["items"]["enum"] == refs


@pytest.mark.parametrize("repository,knowledge,structural,expected", [
    ([], [], [], {"UNCERTAINTY"}),
    ([{"ref": "R1"}], [], [], {"OBSERVED", "INTERPRETATION", "UNCERTAINTY"}),
    ([], [{"ref": "K1"}], [], {"KNOWLEDGE_CONTEXT", "INTERPRETATION", "UNCERTAINTY"}),
    ([], [], [{"ref": "S1"}], {"INTERPRETATION", "UNCERTAINTY"}),
])
def test_focused_schema_omits_impossible_grounded_kinds(repository, knowledge, structural, expected):
    schema = _schema(repository, knowledge, structural)
    branches = schema["properties"]["assertions"]["items"]["anyOf"]
    assert {b["properties"]["kind"]["const"] for b in branches} == expected
    assert '"enum": []' not in json.dumps(schema)
    if not repository + knowledge + structural:
        refs = branches[0]["properties"]["evidence_refs"]
        assert refs["minItems"] == refs["maxItems"] == 0


def test_focused_effective_request_is_canonical_and_exposes_full_text_law(tmp_path):
    provider = RecordingProvider(_wire())
    capability = _focused_e2_capability(tmp_path, provider)
    execute(capability, "Kernel")
    request = provider.requests[0]
    packet = json.loads(request.prompt)
    schema = json.loads(request.response_json_schema)
    canonical = json.dumps(packet["response_contract"], ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    assert canonical == request.response_json_schema
    assert "anyOf" in schema["properties"]["assertions"]["items"]
    fields = [schema["properties"]["summary"], schema["properties"]["assertions"]["items"]["properties"]["text"], schema["properties"]["uncertainties"]["items"]]
    for field in fields:
        text = field["description"]
        for token in ("UTF-8", "whitespace", "control", "format", "surrogate", "evidence_refs"):
            assert token in text
    assert provider.calls == 1 and request.history == ()
    assert len(request.prompt.encode("utf-8")) <= 65536


@pytest.mark.parametrize("focused", [False, True])
@pytest.mark.parametrize("assertions", [
    [],
    [{"kind": "UNCERTAINTY", "text": "Sin soporte.", "evidence_refs": []}],
    [{"kind": "OBSERVED", "text": "Hecho.", "evidence_refs": ["R1"]}],
    [{"kind": "KNOWLEDGE_CONTEXT", "text": "Contexto.", "evidence_refs": ["K1"]}],
    [{"kind": "INTERPRETATION", "text": "Relación.", "evidence_refs": ["R1", "K1"]}],
])
def test_valid_outputs_remain_accepted_with_one_call(tmp_path, focused, assertions):
    provider = RecordingProvider(_wire(assertions=assertions))
    if focused:
        capability = _focused_e2_capability(tmp_path, provider)
        subject = "Kernel"
    else:
        *_, capability = build_capability(tmp_path, provider=provider)
        subject = "needle"
    rendered = execute(capability, subject)
    assert "authority_effect: none" in rendered
    assert provider.calls == 1
    if not focused:
        request = provider.requests[0]
        assert "response_contract" not in json.loads(request.prompt)
        assert "anyOf" not in json.loads(request.response_json_schema)["properties"]["assertions"]["items"]
