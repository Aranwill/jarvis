from __future__ import annotations

import json
from importlib import import_module
from types import SimpleNamespace

import pytest

from malak.app.internal_interaction_test_v0 import InternalInteractionTestV0Harness
from malak.core.conversation import (
    ConversationProvider,
    ConversationRequest,
    ConversationResponse,
)
from malak.core.conversation_registry import ConversationProviderRegistry
from malak.core.request import Request
from malak.runtime.mock_llm_runtime import MockLLMRuntime
from malak.runtime.ollama_runtime import OllamaRuntime
from malak.services.conversation_context import InMemoryConversationContext
from malak.services.conversation_service import ConversationService


class _FakeHTTPResponse:
    def __init__(self, payload: dict[str, object]) -> None:
        self._raw = json.dumps(payload).encode("utf-8")

    def __enter__(self) -> "_FakeHTTPResponse":
        return self

    def __exit__(self, *args: object) -> None:
        return None

    def read(self, size: int = -1) -> bytes:
        if size < 0:
            return self._raw
        return self._raw[:size]


class _RecordingProvider(ConversationProvider):
    def __init__(self) -> None:
        self.request: ConversationRequest | None = None

    def generate(self, request: ConversationRequest) -> ConversationResponse:
        self.request = request
        return ConversationResponse(
            content="ok",
            model=request.model,
            provider="recording",
        )


def _contract(
    *,
    context_window_tokens: int = 8192,
    max_output_tokens: int = 2048,
    thinking_enabled: bool = False,
):
    module = import_module("malak.runtime.runtime_generation_contract")
    return module.RuntimeGenerationContract(
        context_window_tokens=context_window_tokens,
        max_output_tokens=max_output_tokens,
        thinking_enabled=thinking_enabled,
    )


def _ollama_payload(
    monkeypatch: pytest.MonkeyPatch,
    request: ConversationRequest,
    *,
    response_payload: dict[str, object] | None = None,
) -> dict[str, object]:
    captured: dict[str, object] = {}

    def fake_urlopen(
        http_request: object,
        timeout: float,
    ) -> _FakeHTTPResponse:
        captured["request"] = http_request
        return _FakeHTTPResponse(
            response_payload
            or {
                "model": "qwen3.5:9b",
                "done": True,
                "done_reason": "stop",
                "prompt_eval_count": 100,
                "eval_count": 100,
                "message": {
                    "role": "assistant",
                    "content": "ok",
                },
            }
        )

    monkeypatch.setattr(
        "malak.runtime.ollama_runtime.urlopen",
        fake_urlopen,
    )

    OllamaRuntime(keep_alive=0).generate(request)

    http_request = captured["request"]
    return json.loads(http_request.data.decode("utf-8"))


def test_generation_contract_red_r01_invalid_token_budgets_rejected() -> None:
    module = import_module("malak.runtime.runtime_generation_contract")
    contract_type = module.RuntimeGenerationContract

    invalid_cases = (
        {"context_window_tokens": 0, "max_output_tokens": 1},
        {"context_window_tokens": -1, "max_output_tokens": 1},
        {"context_window_tokens": True, "max_output_tokens": 1},
        {"context_window_tokens": 8192, "max_output_tokens": 0},
        {"context_window_tokens": 8192, "max_output_tokens": -1},
        {"context_window_tokens": 8192, "max_output_tokens": True},
    )

    for values in invalid_cases:
        with pytest.raises((TypeError, ValueError)):
            contract_type(
                **values,
                thinking_enabled=False,
            )


def test_generation_contract_red_r02_output_budget_must_be_below_context() -> None:
    module = import_module("malak.runtime.runtime_generation_contract")
    contract_type = module.RuntimeGenerationContract

    for max_output_tokens in (8192, 9000):
        with pytest.raises(ValueError):
            contract_type(
                context_window_tokens=8192,
                max_output_tokens=max_output_tokens,
                thinking_enabled=False,
            )


def test_generation_contract_red_r03_ollama_maps_request_contract(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    contract = _contract()
    request = ConversationRequest(
        prompt="bounded request",
        model="qwen3.5:9b",
        generation_contract=contract,
    )

    payload = _ollama_payload(monkeypatch, request)

    assert payload["options"] == {
        "num_ctx": 8192,
        "num_predict": 2048,
    }
    assert payload["think"] is False
    assert payload["truncate"] is False
    assert payload["shift"] is False


def test_generation_contract_red_r04_generic_request_remains_unchanged(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    request = ConversationRequest(
        prompt="generic request",
        model="qwen3.5:9b",
    )

    payload = _ollama_payload(
        monkeypatch,
        request,
        response_payload={
            "model": "qwen3.5:9b",
            "message": {
                "role": "assistant",
                "content": "generic response",
            },
        },
    )

    assert "options" not in payload
    assert "think" not in payload
    assert "truncate" not in payload
    assert "shift" not in payload


def test_generation_contract_red_r05_context_replace_preserves_contract() -> None:
    contract = _contract()

    registry = ConversationProviderRegistry()
    provider = _RecordingProvider()
    registry.register("recording", provider)

    context = InMemoryConversationContext()
    context.record_exchange(
        session_id="session-A",
        user_content="first",
        assistant_content="answer",
    )
    service = ConversationService(registry, context=context)

    request = ConversationRequest(
        prompt="second",
        model="test-model",
        generation_contract=contract,
    )

    service.generate(
        request,
        provider="recording",
        session_id="session-A",
    )

    assert provider.request is not None
    assert provider.request.generation_contract is contract


def test_generation_contract_red_r06_mock_fails_closed() -> None:
    contract = _contract()
    runtime = MockLLMRuntime()

    with pytest.raises(
        RuntimeError,
        match="generation contract",
    ):
        runtime.generate(
            ConversationRequest(
                prompt="bounded request",
                model="mock-model",
                generation_contract=contract,
            )
        )


def test_generation_contract_red_r07_provenance_binds_exact_options(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    contract = _contract()
    runtime = OllamaRuntime(
        base_url="http://127.0.0.1:11434",
        keep_alive=0,
    )

    def fake_introspection(
        *,
        path: str,
        method: str,
        payload: dict[str, object] | None = None,
    ) -> dict[str, object]:
        if path == "/api/version":
            return {"version": "0.33.3"}
        if path == "/api/tags":
            return {
                "models": [
                    {
                        "name": "qwen3.5:9b",
                        "model": "qwen3.5:9b",
                        "digest": "a" * 64,
                    }
                ]
            }
        if path == "/api/show":
            return {
                "model_info": {
                    "qwen35.context_length": 262144,
                }
            }
        raise AssertionError(path)

    monkeypatch.setattr(
        runtime,
        "_read_introspection_json",
        fake_introspection,
    )

    provenance = runtime.capture_provenance(
        "qwen3.5:9b",
        generation_contract=contract,
    )

    assert dict(provenance.generation_options) == {
        "context_window_tokens": 8192,
        "max_output_tokens": 2048,
        "thinking_enabled": False,
        "input_truncation_allowed": False,
        "history_shift_allowed": False,
    }


def test_generation_contract_red_r08_self_review_requires_engineering_contract(
    tmp_path,
) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / ".git").mkdir()

    engineering = SimpleNamespace(
        baseline_commit="deadbeef",
        kernels={},
        repository_reader=object(),
        knowledge_reader=object(),
    )

    with pytest.raises(
        (TypeError, ValueError),
        match="generation contract",
    ):
        InternalInteractionTestV0Harness(
            repository_root=repo,
            engineering=engineering,
            runtime=OllamaRuntime(),
            model="qwen3.5:9b",
        )


def test_generation_contract_red_r09_length_exhaustion_fails_closed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    contract = _contract()
    request = ConversationRequest(
        prompt="bounded request",
        model="qwen3.5:9b",
        generation_contract=contract,
    )

    with pytest.raises(
        RuntimeError,
        match="length|budget",
    ):
        _ollama_payload(
            monkeypatch,
            request,
            response_payload={
                "model": "qwen3.5:9b",
                "done": True,
                "done_reason": "length",
                "prompt_eval_count": 100,
                "eval_count": 2048,
                "message": {
                    "role": "assistant",
                    "content": "partial",
                },
            },
        )


def test_generation_contract_red_r10_incomplete_response_fails_closed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    contract = _contract()
    request = ConversationRequest(
        prompt="bounded request",
        model="qwen3.5:9b",
        generation_contract=contract,
    )

    with pytest.raises(
        RuntimeError,
        match="incomplete|done",
    ):
        _ollama_payload(
            monkeypatch,
            request,
            response_payload={
                "model": "qwen3.5:9b",
                "done": False,
                "done_reason": "",
                "prompt_eval_count": 100,
                "eval_count": 100,
                "message": {
                    "role": "assistant",
                    "content": "partial",
                },
            },
        )


def test_generation_contract_red_r11_disabled_thinking_is_enforced(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    contract = _contract(thinking_enabled=False)
    request = ConversationRequest(
        prompt="bounded request",
        model="qwen3.5:9b",
        generation_contract=contract,
    )

    with pytest.raises(
        RuntimeError,
        match="thinking|generation contract",
    ):
        _ollama_payload(
            monkeypatch,
            request,
            response_payload={
                "model": "qwen3.5:9b",
                "done": True,
                "done_reason": "stop",
                "prompt_eval_count": 100,
                "eval_count": 100,
                "message": {
                    "role": "assistant",
                    "content": "final",
                    "thinking": "hidden reasoning must not be accepted here",
                },
            },
        )


def test_generation_contract_red_r12_structured_output_coexists_with_contract(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    contract = _contract()
    schema = '{"additionalProperties":false,"type":"object"}'

    request = ConversationRequest(
        prompt="structured bounded request",
        model="qwen3.5:9b",
        response_json_schema=schema,
        generation_contract=contract,
    )

    payload = _ollama_payload(
        monkeypatch,
        request,
        response_payload={
            "model": "qwen3.5:9b",
            "done": True,
            "done_reason": "stop",
            "prompt_eval_count": 100,
            "eval_count": 100,
            "message": {
                "role": "assistant",
                "content": "{}",
            },
        },
    )

    assert payload["format"] == json.loads(schema)
    assert payload["options"] == {
        "num_ctx": 8192,
        "num_predict": 2048,
    }
    assert payload["think"] is False
    assert payload["truncate"] is False
    assert payload["shift"] is False


def test_generation_contract_red_r13_composition_reuses_same_contract(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    contract = _contract()
    module = import_module("malak.app.composition")

    reader = SimpleNamespace(baseline_commit="abc")
    knowledge = SimpleNamespace(baseline_commit="abc")
    structural = SimpleNamespace(baseline_commit="abc")
    seen: list[object] = []

    monkeypatch.setattr(
        module,
        "GitRepositoryReader",
        lambda _: reader,
    )
    monkeypatch.setattr(
        module,
        "GovernedKnowledgeReader",
        lambda _: knowledge,
    )
    monkeypatch.setattr(
        module,
        "RepositoryStructuralProjector",
        lambda _: SimpleNamespace(project=lambda: structural),
    )

    def constructor(name: str):
        def build(**kwargs):
            seen.append(kwargs["generation_contract"])
            return SimpleNamespace(name=name)
        return build

    monkeypatch.setattr(
        module,
        "EngineeringInspectCapability",
        constructor("engineering_inspect"),
    )
    monkeypatch.setattr(
        module,
        "EngineeringAnalyzeCapability",
        constructor("engineering_analyze"),
    )
    monkeypatch.setattr(
        module,
        "EngineeringProposeCapability",
        constructor("engineering_propose"),
    )
    monkeypatch.setattr(
        module,
        "_build_fixed_kernel",
        lambda capability: capability,
    )

    class _Focus:
        pass

    monkeypatch.setattr(
        module,
        "GovernedEngineeringEvidenceFocus",
        _Focus,
    )

    engineering = module.build_engineering_kernel_set(
        repository_root="unused",
        service=object(),
        provider_name="recording",
        model="qwen3.5:9b",
        generation_contract=contract,
    )

    focused = engineering.with_evidence_focus(_Focus())

    assert engineering.generation_contract is contract
    assert focused.generation_contract is contract
    assert len(seen) == 6
    assert all(item is contract for item in seen)


def test_generation_contract_red_r14_inspect_empty_content_stays_fail_closed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = import_module("malak.capabilities.engineering_inspect")

    bundle = SimpleNamespace(
        repository_evidence=(
            {
                "ref": "R1",
                "path": "src/malak/example.py",
                "blob_sha": "abc",
                "line_number": 1,
                "line": "Kernel",
            },
        ),
        knowledge_evidence=(
            {
                "ref": "K1",
                "path": "docs/governance/example.md",
                "blob_sha": "def",
                "source_class": "GOVERNING",
                "authority_class": "normative",
                "line_number": 1,
                "line": "Kernel",
            },
        ),
        repository_match_count=1,
        knowledge_match_count=1,
        repository_skipped_unreadable=0,
        context_truncated=False,
    )

    monkeypatch.setattr(
        module,
        "collect_engineering_evidence",
        lambda **_: bundle,
    )

    class _EmptyService:
        def generate(self, request, provider):
            return ConversationResponse(
                content="   ",
                model=request.model,
                provider=provider,
            )

    capability = module.EngineeringInspectCapability(
        repository_reader=SimpleNamespace(baseline_commit="abc"),
        knowledge_reader=SimpleNamespace(baseline_commit="abc"),
        structural_projection=None,
        conversation_service=_EmptyService(),
        provider_name="recording",
        model="qwen3.5:9b",
    )

    with pytest.raises(
        RuntimeError,
        match="model response is empty",
    ):
        capability.execute(
            Request(
                content="Kernel",
                session_id="session-A",
            )
        )
