import json

import pytest

from malak.runtime.runtime_metric_store import InMemoryRuntimeMetricStore
from malak.core.conversation import ConversationMessage
from malak.core.conversation import ConversationRequest
from malak.runtime.ollama_runtime import OllamaRuntime


class FakeHTTPResponse:
    def __init__(self, payload: dict[str, object]) -> None:
        self._payload = payload
        self._raw_payload = json.dumps(payload).encode("utf-8")
        self.read_sizes: list[int] = []

    def __enter__(self) -> "FakeHTTPResponse":
        return self

    def __exit__(self, *args: object) -> None:
        return None

    def read(self, size: int = -1) -> bytes:
        self.read_sizes.append(size)

        if size < 0:
            return self._raw_payload

        return self._raw_payload[:size]


def test_ollama_runtime_generates_conversation_response(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, object] = {}

    def fake_urlopen(
        request: object,
        timeout: float,
    ) -> FakeHTTPResponse:
        captured["request"] = request
        captured["timeout"] = timeout

        return FakeHTTPResponse(
            {
                "model": "qwen3.5:9b",
                "message": {
                    "role": "assistant",
                    "content": "Respuesta generada por Ollama.",
                },
            }
        )

    monkeypatch.setattr(
        "malak.runtime.ollama_runtime.urlopen",
        fake_urlopen,
    )

    runtime = OllamaRuntime(
        base_url="http://localhost:11434/",
        timeout_seconds=30.0,
        keep_alive=0,
    )

    response = runtime.generate(
        ConversationRequest(
            prompt="Hola Malak",
            model="qwen3.5:9b",
            system_prompt="Responde de forma breve.",
            history=(
                ConversationMessage(
                    role="user",
                    content="Pregunta anterior",
                ),
                ConversationMessage(
                    role="assistant",
                    content="Respuesta anterior",
                ),
            ),
        )
    )

    http_request = captured["request"]
    request_payload = json.loads(http_request.data.decode("utf-8"))

    assert http_request.full_url == "http://localhost:11434/api/chat"
    assert http_request.get_method() == "POST"
    assert captured["timeout"] == 30.0

    assert request_payload == {
        "model": "qwen3.5:9b",
        "messages": [
            {
                "role": "system",
                "content": "Responde de forma breve.",
            },
            {
                "role": "user",
                "content": "Pregunta anterior",
            },
            {
                "role": "assistant",
                "content": "Respuesta anterior",
            },
            {
                "role": "user",
                "content": "Hola Malak",
            },
        ],
        "stream": False,
        "keep_alive": 0,
    }

    assert response.content == "Respuesta generada por Ollama."
    assert response.model == "qwen3.5:9b"
    assert response.provider == "ollama"


def test_ollama_runtime_requires_model() -> None:
    runtime = OllamaRuntime()

    request = ConversationRequest(
        prompt="Hola Malak",
        model=None,
    )

    with pytest.raises(
        ValueError,
        match="model",
    ):
        runtime.generate(request)


def test_ollama_runtime_rejects_empty_prompt() -> None:
    runtime = OllamaRuntime()

    request = ConversationRequest(
        prompt="   ",
        model="qwen3.5:9b",
    )

    with pytest.raises(
        ValueError,
        match="prompt",
    ):
        runtime.generate(request)


def test_ollama_runtime_rejects_response_without_content(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_urlopen(
        request: object,
        timeout: float,
    ) -> FakeHTTPResponse:
        return FakeHTTPResponse(
            {
                "model": "qwen3.5:9b",
                "message": {
                    "role": "assistant",
                },
            }
        )

    monkeypatch.setattr(
        "malak.runtime.ollama_runtime.urlopen",
        fake_urlopen,
    )

    runtime = OllamaRuntime(
        keep_alive=0,
    )

    with pytest.raises(
        RuntimeError,
        match="message",
    ):
        runtime.generate(
            ConversationRequest(
                prompt="Hola Malak",
                model="qwen3.5:9b",
            )
        )

def test_ollama_runtime_captures_execution_metrics(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_urlopen(
        request: object,
        timeout: float,
    ) -> FakeHTTPResponse:
        return FakeHTTPResponse(
            {
                "model": "qwen3.5:9b",
                "message": {
                    "role": "assistant",
                    "content": "Respuesta con telemetría.",
                },
                "total_duration": 15_000_000_000,
                "load_duration": 3_000_000_000,
                "prompt_eval_count": 120,
                "prompt_eval_duration": 2_000_000_000,
                "eval_count": 200,
                "eval_duration": 10_000_000_000,
            }
        )

    monkeypatch.setattr(
        "malak.runtime.ollama_runtime.urlopen",
        fake_urlopen,
    )

    runtime = OllamaRuntime()

    runtime.generate(
        ConversationRequest(
            prompt="Hola Malak",
            model="qwen3.5:9b",
        )
    )

    metrics = runtime.last_metrics

    assert metrics is not None
    assert metrics.model == "qwen3.5:9b"
    assert metrics.total_duration_ns == 15_000_000_000
    assert metrics.total_duration_seconds == 15.0
    assert metrics.load_duration_seconds == 3.0
    assert metrics.prompt_eval_count == 120
    assert metrics.prompt_eval_duration_seconds == 2.0
    assert metrics.eval_count == 200
    assert metrics.eval_duration_seconds == 10.0
    assert metrics.tokens_per_second == 20.0

def test_ollama_runtime_appends_metric_sample_to_store(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_urlopen(
        request: object,
        timeout: float,
    ) -> FakeHTTPResponse:
        return FakeHTTPResponse(
            {
                "model": "qwen3.5:9b",
                "message": {
                    "role": "assistant",
                    "content": "Respuesta registrada.",
                },
                "total_duration": 15_000_000_000,
                "load_duration": 3_000_000_000,
                "prompt_eval_count": 120,
                "prompt_eval_duration": 2_000_000_000,
                "eval_count": 200,
                "eval_duration": 10_000_000_000,
            }
        )

    monkeypatch.setattr(
        "malak.runtime.ollama_runtime.urlopen",
        fake_urlopen,
    )

    store = InMemoryRuntimeMetricStore()

    runtime = OllamaRuntime(
        timeout_seconds=600.0,
        keep_alive=0,
        metric_store=store,
    )

    runtime.generate(
        ConversationRequest(
            prompt="Hola Malak",
            model="qwen3.5:9b",
        )
    )

    samples = store.list_by_model("qwen3.5:9b")

    assert len(samples) == 1

    sample = samples[0]

    assert sample.model == "qwen3.5:9b"
    assert sample.timeout_seconds == 600.0
    assert sample.keep_alive == 0
    assert sample.total_duration_seconds == 15.0
    assert sample.load_duration_seconds == 3.0
    assert sample.prompt_eval_count == 120
    assert sample.eval_count == 200
    assert sample.tokens_per_second == 20.0
    assert sample.captured_at.tzinfo is not None
@pytest.mark.parametrize(
    "max_request_bytes",
    (0, -1),
)
def test_ollama_runtime_rejects_invalid_max_request_bytes(
    max_request_bytes: int,
) -> None:
    with pytest.raises(
        ValueError,
        match="max_request_bytes",
    ):
        OllamaRuntime(
            max_request_bytes=max_request_bytes,
        )


@pytest.mark.parametrize(
    "max_response_bytes",
    (0, -1),
)
def test_ollama_runtime_rejects_invalid_max_response_bytes(
    max_response_bytes: int,
) -> None:
    with pytest.raises(
        ValueError,
        match="max_response_bytes",
    ):
        OllamaRuntime(
            max_response_bytes=max_response_bytes,
        )


def test_ollama_runtime_allows_request_at_exact_byte_limit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    request = ConversationRequest(
        prompt="Hola Malak",
        model="qwen3.5:9b",
    )

    expected_payload = {
        "model": "qwen3.5:9b",
        "messages": [
            {
                "role": "user",
                "content": "Hola Malak",
            },
        ],
        "stream": False,
        "keep_alive": 0,
    }

    encoded_payload = json.dumps(expected_payload).encode("utf-8")

    called = False

    def fake_urlopen(
        request: object,
        timeout: float,
    ) -> FakeHTTPResponse:
        nonlocal called
        called = True

        return FakeHTTPResponse(
            {
                "model": "qwen3.5:9b",
                "message": {
                    "role": "assistant",
                    "content": "OK",
                },
            }
        )

    monkeypatch.setattr(
        "malak.runtime.ollama_runtime.urlopen",
        fake_urlopen,
    )

    runtime = OllamaRuntime(
        keep_alive=0,
        max_request_bytes=len(encoded_payload),
    )

    response = runtime.generate(request)

    assert called is True
    assert response.content == "OK"


def test_ollama_runtime_rejects_request_above_byte_limit_before_urlopen(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    request = ConversationRequest(
        prompt="Hola Malak",
        model="qwen3.5:9b",
    )

    expected_payload = {
        "model": "qwen3.5:9b",
        "messages": [
            {
                "role": "user",
                "content": "Hola Malak",
            },
        ],
        "stream": False,
        "keep_alive": 0,
    }

    encoded_payload = json.dumps(expected_payload).encode("utf-8")

    called = False

    def fake_urlopen(
        request: object,
        timeout: float,
    ) -> FakeHTTPResponse:
        nonlocal called
        called = True
        raise AssertionError("urlopen must not be called")

    monkeypatch.setattr(
        "malak.runtime.ollama_runtime.urlopen",
        fake_urlopen,
    )

    runtime = OllamaRuntime(
        keep_alive=0,
        max_request_bytes=len(encoded_payload) - 1,
    )

    with pytest.raises(
        RuntimeError,
        match="max_request_bytes",
    ):
        runtime.generate(request)

    assert called is False


def test_ollama_runtime_allows_response_at_exact_byte_limit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    response_payload = {
        "model": "qwen3.5:9b",
        "message": {
            "role": "assistant",
            "content": "Respuesta acotada.",
        },
    }

    raw_response = json.dumps(response_payload).encode("utf-8")
    fake_response = FakeHTTPResponse(response_payload)

    def fake_urlopen(
        request: object,
        timeout: float,
    ) -> FakeHTTPResponse:
        return fake_response

    monkeypatch.setattr(
        "malak.runtime.ollama_runtime.urlopen",
        fake_urlopen,
    )

    runtime = OllamaRuntime(
        max_response_bytes=len(raw_response),
    )

    response = runtime.generate(
        ConversationRequest(
            prompt="Hola Malak",
            model="qwen3.5:9b",
        )
    )

    assert response.content == "Respuesta acotada."
    assert fake_response.read_sizes == [len(raw_response) + 1]


def test_ollama_runtime_rejects_response_above_byte_limit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    response_payload = {
        "model": "qwen3.5:9b",
        "message": {
            "role": "assistant",
            "content": "Respuesta demasiado grande.",
        },
    }

    raw_response = json.dumps(response_payload).encode("utf-8")
    fake_response = FakeHTTPResponse(response_payload)

    def fake_urlopen(
        request: object,
        timeout: float,
    ) -> FakeHTTPResponse:
        return fake_response

    monkeypatch.setattr(
        "malak.runtime.ollama_runtime.urlopen",
        fake_urlopen,
    )

    max_response_bytes = len(raw_response) - 1

    runtime = OllamaRuntime(
        max_response_bytes=max_response_bytes,
    )

    with pytest.raises(
        RuntimeError,
        match="max_response_bytes",
    ):
        runtime.generate(
            ConversationRequest(
                prompt="Hola Malak",
                model="qwen3.5:9b",
            )
        )

    assert fake_response.read_sizes == [max_response_bytes + 1]



def test_analyze_structured_output_red_s02_ollama_maps_schema_to_format(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, object] = {}

    def fake_urlopen(
        request: object,
        timeout: float,
    ) -> FakeHTTPResponse:
        captured["request"] = request
        return FakeHTTPResponse(
            {
                "model": "qwen3.5:9b",
                "message": {
                    "role": "assistant",
                    "content": '{"summary":"ok","findings":[],"uncertainties":[]}',
                },
            }
        )

    monkeypatch.setattr(
        "malak.runtime.ollama_runtime.urlopen",
        fake_urlopen,
    )

    schema = '{"additionalProperties":false,"type":"object"}'
    request = ConversationRequest(
        prompt="Return structured output.",
        model="qwen3.5:9b",
    )
    object.__setattr__(
        request,
        "response_json_schema",
        schema,
    )

    OllamaRuntime().generate(request)

    http_request = captured["request"]
    payload = json.loads(http_request.data.decode("utf-8"))

    assert payload["format"] == json.loads(schema)


def test_analyze_structured_output_red_s05_generic_ollama_request_has_no_format(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, object] = {}

    def fake_urlopen(
        request: object,
        timeout: float,
    ) -> FakeHTTPResponse:
        captured["request"] = request
        return FakeHTTPResponse(
            {
                "model": "qwen3.5:9b",
                "message": {
                    "role": "assistant",
                    "content": "plain response",
                },
            }
        )

    monkeypatch.setattr(
        "malak.runtime.ollama_runtime.urlopen",
        fake_urlopen,
    )

    OllamaRuntime().generate(
        ConversationRequest(
            prompt="Return a plain response.",
            model="qwen3.5:9b",
        )
    )

    http_request = captured["request"]
    payload = json.loads(http_request.data.decode("utf-8"))

    assert "format" not in payload

# ---------------------------------------------------------------------------
# E3 Governed Local Ollama Assessor Experiment V0 — PR-B1 causal RED
# GLOAE-R02..R08.  Estos tests congelan la frontera de trust del runtime
# existente; no ejecutan red real ni Ollama.
# ---------------------------------------------------------------------------


class _RawHTTPResponse:
    def __init__(
        self,
        raw_payload: bytes,
        *,
        final_url: str | None = None,
    ) -> None:
        self._raw_payload = raw_payload
        self._final_url = final_url
        self.read_sizes: list[int] = []

    def __enter__(self) -> "_RawHTTPResponse":
        return self

    def __exit__(self, *args: object) -> None:
        return None

    def read(self, size: int = -1) -> bytes:
        self.read_sizes.append(size)
        if size < 0:
            return self._raw_payload
        return self._raw_payload[:size]

    def geturl(self) -> str | None:
        return self._final_url


def _patch_b1_transport(
    monkeypatch: pytest.MonkeyPatch,
    responder: object,
) -> None:
    """
    Permite que los tests RED sobrevivan al cambio esperado de urlopen global
    a un opener privado. No concede red real.
    """

    class _FakeOpener:
        def open(
            self,
            request: object,
            timeout: float,
        ) -> object:
            return responder(request, timeout)  # type: ignore[operator]

    monkeypatch.setattr(
        "malak.runtime.ollama_runtime.urlopen",
        responder,
    )
    monkeypatch.setattr(
        "malak.runtime.ollama_runtime.build_opener",
        lambda *handlers: _FakeOpener(),
        raising=False,
    )


def test_ollama_runtime_red_r02_uses_private_proxy_free_transport(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from urllib.request import HTTPRedirectHandler, ProxyHandler

    captured: dict[str, object] = {}

    class _FakeOpener:
        def open(
            self,
            request: object,
            timeout: float,
        ) -> FakeHTTPResponse:
            captured["request"] = request
            captured["timeout"] = timeout
            return FakeHTTPResponse(
                {
                    "model": "qwen3.5:9b",
                    "message": {
                        "role": "assistant",
                        "content": "direct transport",
                    },
                }
            )

    def fake_build_opener(*handlers: object) -> _FakeOpener:
        captured["handlers"] = handlers
        return _FakeOpener()

    def forbidden_global_urlopen(*args: object, **kwargs: object) -> object:
        raise AssertionError(
            "global urlopen inherits process proxy/redirect policy"
        )

    monkeypatch.setenv("HTTP_PROXY", "http://127.0.0.1:65530")
    monkeypatch.setenv("HTTPS_PROXY", "http://127.0.0.1:65531")
    monkeypatch.setenv("ALL_PROXY", "http://127.0.0.1:65532")
    monkeypatch.setattr(
        "malak.runtime.ollama_runtime.build_opener",
        fake_build_opener,
        raising=False,
    )
    monkeypatch.setattr(
        "malak.runtime.ollama_runtime.urlopen",
        forbidden_global_urlopen,
    )

    response = OllamaRuntime().generate(
        ConversationRequest(
            prompt="Hola Malak",
            model="qwen3.5:9b",
        )
    )

    handlers = captured["handlers"]
    proxy_handlers = [
        handler
        for handler in handlers
        if isinstance(handler, ProxyHandler)
    ]
    redirect_handlers = [
        handler
        for handler in handlers
        if isinstance(handler, HTTPRedirectHandler)
    ]

    assert len(proxy_handlers) == 1
    assert proxy_handlers[0].proxies == {}
    assert len(redirect_handlers) == 1
    assert (
        redirect_handlers[0].redirect_request(
            None,
            None,
            302,
            "Found",
            {},
            "http://remote.invalid/api/chat",
        )
        is None
    )
    assert response.content == "direct transport"


@pytest.mark.parametrize(
    "status_code",
    (301, 302, 307, 308),
)
def test_ollama_runtime_red_r03_chat_redirect_status_fails_closed(
    monkeypatch: pytest.MonkeyPatch,
    status_code: int,
) -> None:
    from urllib.error import HTTPError

    def responder(
        request: object,
        timeout: float,
    ) -> object:
        raise HTTPError(
            request.full_url,  # type: ignore[attr-defined]
            status_code,
            "redirect",
            {"Location": "http://remote.invalid/api/chat"},
            None,
        )

    _patch_b1_transport(monkeypatch, responder)

    with pytest.raises(RuntimeError, match="HTTP status"):
        OllamaRuntime().generate(
            ConversationRequest(
                prompt="Hola Malak",
                model="qwen3.5:9b",
            )
        )


def test_ollama_runtime_red_r03_chat_rejects_followed_redirect_final_url(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def responder(
        request: object,
        timeout: float,
    ) -> _RawHTTPResponse:
        return _RawHTTPResponse(
            json.dumps(
                {
                    "model": "qwen3.5:9b",
                    "message": {
                        "role": "assistant",
                        "content": "should not be accepted",
                    },
                }
            ).encode("utf-8"),
            final_url="http://remote.invalid/api/chat",
        )

    _patch_b1_transport(monkeypatch, responder)

    with pytest.raises(RuntimeError, match="redirect|final URL|URL"):
        OllamaRuntime().generate(
            ConversationRequest(
                prompt="Hola Malak",
                model="qwen3.5:9b",
            )
        )


def test_ollama_runtime_red_r03_introspection_rejects_followed_redirect_final_url(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def responder(
        request: object,
        timeout: float,
    ) -> _RawHTTPResponse:
        return _RawHTTPResponse(
            b'{"version":"0.34.4"}',
            final_url="http://remote.invalid/api/version",
        )

    _patch_b1_transport(monkeypatch, responder)

    with pytest.raises(RuntimeError, match="redirect|final URL|URL"):
        OllamaRuntime()._read_introspection_json(
            path="/api/version",
            method="GET",
        )


@pytest.mark.parametrize(
    "raw_payload",
    (
        b'{"version":"0.34.4","version":"evil"}',
        b'{"version":"0.34.4","extra":NaN}',
        b"\xff",
        b"[]",
    ),
)
def test_ollama_runtime_red_r04_introspection_outer_json_is_strict(
    monkeypatch: pytest.MonkeyPatch,
    raw_payload: bytes,
) -> None:
    def responder(
        request: object,
        timeout: float,
    ) -> _RawHTTPResponse:
        return _RawHTTPResponse(
            raw_payload,
            final_url=request.full_url,  # type: ignore[attr-defined]
        )

    _patch_b1_transport(monkeypatch, responder)

    with pytest.raises(RuntimeError):
        OllamaRuntime()._read_introspection_json(
            path="/api/version",
            method="GET",
        )


@pytest.mark.parametrize(
    "raw_payload",
    (
        (
            b'{"model":"qwen3.5:9b","model":"qwen3.5:9b",'
            b'"message":{"role":"assistant","content":"ok"}}'
        ),
        (
            b'{"model":"qwen3.5:9b","extra":NaN,'
            b'"message":{"role":"assistant","content":"ok"}}'
        ),
        b"\xff",
        b"[]",
    ),
)
def test_ollama_runtime_red_r04_chat_outer_json_is_strict(
    monkeypatch: pytest.MonkeyPatch,
    raw_payload: bytes,
) -> None:
    def responder(
        request: object,
        timeout: float,
    ) -> _RawHTTPResponse:
        return _RawHTTPResponse(
            raw_payload,
            final_url=request.full_url,  # type: ignore[attr-defined]
        )

    _patch_b1_transport(monkeypatch, responder)

    with pytest.raises(RuntimeError):
        OllamaRuntime().generate(
            ConversationRequest(
                prompt="Hola Malak",
                model="qwen3.5:9b",
            )
        )


@pytest.mark.parametrize(
    ("raw_model", "include_model"),
    (
        (None, False),
        (None, True),
        ("", True),
        (" qwen3.5:9b", True),
        (123, True),
        ("other-model:latest", True),
    ),
)
def test_ollama_runtime_red_r05_r08_requires_exact_raw_response_model(
    monkeypatch: pytest.MonkeyPatch,
    raw_model: object,
    include_model: bool,
) -> None:
    payload: dict[str, object] = {
        "message": {
            "role": "assistant",
            "content": "must not cross identity boundary",
        },
    }
    if include_model:
        payload["model"] = raw_model

    def responder(
        request: object,
        timeout: float,
    ) -> FakeHTTPResponse:
        return FakeHTTPResponse(payload)

    _patch_b1_transport(monkeypatch, responder)

    runtime = OllamaRuntime()

    with pytest.raises(RuntimeError, match="model"):
        runtime.generate(
            ConversationRequest(
                prompt="Hola Malak",
                model="qwen3.5:9b",
            )
        )

    assert runtime.last_metrics is None


def test_ollama_runtime_red_r07_duplicate_raw_model_fails_before_response(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    raw_payload = (
        b'{"model":"qwen3.5:9b","model":"qwen3.5:9b",'
        b'"message":{"role":"assistant","content":"duplicate identity"}}'
    )

    def responder(
        request: object,
        timeout: float,
    ) -> _RawHTTPResponse:
        return _RawHTTPResponse(
            raw_payload,
            final_url=request.full_url,  # type: ignore[attr-defined]
        )

    _patch_b1_transport(monkeypatch, responder)

    runtime = OllamaRuntime()

    with pytest.raises(RuntimeError):
        runtime.generate(
            ConversationRequest(
                prompt="Hola Malak",
                model="qwen3.5:9b",
            )
        )

    assert runtime.last_metrics is None
