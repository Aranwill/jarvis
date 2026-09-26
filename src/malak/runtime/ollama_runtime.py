from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from json import JSONDecodeError
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from malak.core.conversation import (
    ConversationRequest,
    ConversationResponse,
)
from malak.core.llm_runtime import LLMRuntime
from malak.runtime.runtime_metric_sample import RuntimeMetricSample
from malak.runtime.runtime_metric_sink import RuntimeMetricSink
from malak.runtime.runtime_metrics import RuntimeMetrics
from malak.runtime.runtime_provenance import (
    RUNTIME_MODEL_PROVENANCE_SCHEMA,
    RuntimeModelProvenance,
)


class OllamaRuntime(LLMRuntime):
    """
    Local Ollama runtime implementation.

    The runtime sends non-streaming requests to Ollama and unloads the
    model after each completed generation by default, preserving resources
    for subsequent model executions.
    """

    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        timeout_seconds: float = 600.0,
        keep_alive: int | str = 0,
        metric_store: RuntimeMetricSink | None = None,
        max_request_bytes: int = 4 * 1024 * 1024,
        max_response_bytes: int = 16 * 1024 * 1024,
    ) -> None:
        normalized_base_url = base_url.strip().rstrip("/")

        if not normalized_base_url:
            raise ValueError("base_url must not be empty")

        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be greater than zero")

        if (
            isinstance(max_request_bytes, bool)
            or not isinstance(max_request_bytes, int)
            or max_request_bytes <= 0
        ):
            raise ValueError(
                "max_request_bytes must be a positive integer"
            )

        if (
            isinstance(max_response_bytes, bool)
            or not isinstance(max_response_bytes, int)
            or max_response_bytes <= 0
        ):
            raise ValueError(
                "max_response_bytes must be a positive integer"
            )

        self._base_url = normalized_base_url
        self._timeout_seconds = timeout_seconds
        self._keep_alive = keep_alive
        self._metric_store = metric_store
        self._max_request_bytes = max_request_bytes
        self._max_response_bytes = max_response_bytes
        self._last_metrics: RuntimeMetrics | None = None

    def capture_provenance(
        self,
        model: str,
    ) -> RuntimeModelProvenance:
        requested_model = model.strip() if isinstance(model, str) else ""
        if not requested_model:
            raise ValueError("model is required for provenance capture")
        if requested_model != model:
            raise ValueError(
                "model must not contain surrounding whitespace"
            )

        version_payload = self._read_introspection_json(
            path="/api/version",
            method="GET",
        )
        version = version_payload.get("version")
        runtime_version = (
            version
            if isinstance(version, str) and version.strip() == version and version
            else None
        )

        tags_payload = self._read_introspection_json(
            path="/api/tags",
            method="GET",
        )
        models = tags_payload.get("models")
        if not isinstance(models, list):
            raise RuntimeError(
                "Ollama tags response does not contain a valid models list"
            )

        resolved_model: str | None = None
        model_digest: str | None = None
        for item in models:
            if not isinstance(item, dict):
                continue
            names = tuple(
                value
                for value in (
                    item.get("name"),
                    item.get("model"),
                )
                if isinstance(value, str)
            )
            if requested_model not in names:
                continue
            resolved_model = requested_model
            digest = item.get("digest")
            if isinstance(digest, str):
                if re.fullmatch(r"[0-9a-f]{64}", digest):
                    model_digest = f"sha256:{digest}"
                elif re.fullmatch(
                    r"sha256:[0-9a-f]{64}",
                    digest,
                ):
                    model_digest = digest
            break

        declared_context_window: int | None = None
        context_window_source = "unavailable"
        if resolved_model is not None:
            try:
                show_payload = self._read_introspection_json(
                    path="/api/show",
                    method="POST",
                    payload={"model": resolved_model},
                )
            except RuntimeError:
                show_payload = {}

            model_info = show_payload.get("model_info")
            if isinstance(model_info, dict):
                context_candidates = [
                    value
                    for key, value in model_info.items()
                    if (
                        isinstance(key, str)
                        and (
                            key == "context_length"
                            or key.endswith(".context_length")
                        )
                        and type(value) is int
                        and value > 0
                    )
                ]
                if context_candidates:
                    unique_candidates = set(context_candidates)
                    if len(unique_candidates) == 1:
                        declared_context_window = context_candidates[0]
                        context_window_source = "ollama:model_info"

        if resolved_model is None:
            identity_strength = "UNAVAILABLE"
            provenance_status = "UNAVAILABLE"
        elif model_digest is None:
            identity_strength = "TAG_ONLY"
            provenance_status = "PARTIAL"
        else:
            identity_strength = "TAG_DIGEST_BOUND"
            provenance_status = "READY"

        return RuntimeModelProvenance(
            schema=RUNTIME_MODEL_PROVENANCE_SCHEMA,
            captured_at=datetime.now(UTC),
            runtime_class="OllamaRuntime",
            provider="ollama",
            requested_model=requested_model,
            resolved_model=resolved_model,
            model_digest=model_digest,
            model_identity_strength=identity_strength,
            runtime_version=runtime_version,
            declared_context_window=declared_context_window,
            context_window_source=context_window_source,
            generation_options={},
            timeout_seconds=self._timeout_seconds,
            keep_alive=self._keep_alive,
            max_request_bytes=self._max_request_bytes,
            max_response_bytes=self._max_response_bytes,
            provenance_status=provenance_status,
            authority_effect="none",
        )

    def _read_introspection_json(
        self,
        *,
        path: str,
        method: str,
        payload: dict[str, object] | None = None,
    ) -> dict[str, object]:
        encoded_payload: bytes | None = None
        if payload is not None:
            encoded_payload = json.dumps(
                payload,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
            if len(encoded_payload) > self._max_request_bytes:
                raise RuntimeError(
                    "Ollama introspection request exceeded "
                    "max_request_bytes"
                )

        headers = {"Accept": "application/json"}
        if encoded_payload is not None:
            headers["Content-Type"] = "application/json"

        request = Request(
            url=f"{self._base_url}{path}",
            data=encoded_payload,
            headers=headers,
            method=method,
        )

        try:
            with urlopen(
                request,
                timeout=self._timeout_seconds,
            ) as response:
                raw = response.read(self._max_response_bytes + 1)
                if len(raw) > self._max_response_bytes:
                    raise RuntimeError(
                        "Ollama introspection response exceeded "
                        "max_response_bytes"
                    )
        except HTTPError as exc:
            raise RuntimeError(
                f"Ollama introspection returned HTTP status {exc.code}"
            ) from exc
        except URLError as exc:
            raise RuntimeError(
                "Unable to reach Ollama for provenance introspection"
            ) from exc
        except TimeoutError as exc:
            raise RuntimeError(
                "Ollama provenance introspection timed out"
            ) from exc

        try:
            decoded = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, JSONDecodeError) as exc:
            raise RuntimeError(
                "Ollama provenance introspection returned invalid JSON"
            ) from exc

        if not isinstance(decoded, dict):
            raise RuntimeError(
                "Ollama provenance introspection payload is invalid"
            )
        return decoded

    @property
    def last_metrics(self) -> RuntimeMetrics | None:
        """
        Metrics from the most recent successfully decoded Ollama response.

        These metrics are diagnostic and are not persisted by the runtime
        unless a metric store was explicitly injected.
        """

        return self._last_metrics

    def generate(
        self,
        request: ConversationRequest,
    ) -> ConversationResponse:
        model = request.model.strip() if request.model else ""
        prompt = request.prompt.strip()

        if not model:
            raise ValueError("model is required")

        if not prompt:
            raise ValueError("prompt must not be empty")

        self._last_metrics = None

        messages: list[dict[str, str]] = []

        if request.system_prompt is not None:
            messages.append(
                {
                    "role": "system",
                    "content": request.system_prompt,
                }
            )

        for message in request.history:
            messages.append(
                {
                    "role": message.role,
                    "content": message.content,
                }
            )

        messages.append(
            {
                "role": "user",
                "content": request.prompt,
            }
        )

        payload: dict[str, Any] = {
            "model": model,
            "messages": messages,
            "stream": False,
            "keep_alive": self._keep_alive,
        }

        if request.response_json_schema is not None:
            try:
                schema_payload = json.loads(
                    request.response_json_schema,
                )
            except (json.JSONDecodeError, TypeError, RecursionError) as exc:
                raise RuntimeError(
                    "structured output schema is not valid JSON"
                ) from exc
            if not isinstance(schema_payload, dict):
                raise RuntimeError(
                    "structured output schema root must be an object"
                )
            payload["format"] = schema_payload

        encoded_payload = json.dumps(payload).encode("utf-8")

        if len(encoded_payload) > self._max_request_bytes:
            raise RuntimeError(
                "Ollama request exceeded "
                f"max_request_bytes ({self._max_request_bytes} bytes)"
            )

        http_request = Request(
            url=f"{self._base_url}/api/chat",
            data=encoded_payload,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            method="POST",
        )

        try:
            with urlopen(
                http_request,
                timeout=self._timeout_seconds,
            ) as http_response:
                raw_response = http_response.read(
                    self._max_response_bytes + 1
                )

                if len(raw_response) > self._max_response_bytes:
                    raise RuntimeError(
                        "Ollama response exceeded "
                        f"max_response_bytes "
                        f"({self._max_response_bytes} bytes)"
                    )

        except HTTPError as exc:
            raise RuntimeError(
                f"Ollama returned HTTP status {exc.code}"
            ) from exc

        except URLError as exc:
            raise RuntimeError(
                f"Unable to connect to Ollama at {self._base_url}"
            ) from exc

        except TimeoutError as exc:
            raise RuntimeError(
                f"Ollama request exceeded {self._timeout_seconds} seconds"
            ) from exc

        try:
            response_payload = json.loads(raw_response.decode("utf-8"))

        except (UnicodeDecodeError, JSONDecodeError) as exc:
            raise RuntimeError(
                "Ollama returned an invalid JSON response"
            ) from exc

        if not isinstance(response_payload, dict):
            raise RuntimeError(
                "Ollama returned an invalid response payload"
            )

        message_payload = response_payload.get("message")

        if not isinstance(message_payload, dict):
            raise RuntimeError(
                "Ollama response does not contain a valid message field"
            )

        generated_content = message_payload.get("content")

        if not isinstance(generated_content, str):
            raise RuntimeError(
                "Ollama response does not contain a valid message content field"
            )

        response_model = response_payload.get("model")

        if not isinstance(response_model, str) or not response_model:
            response_model = model

        metrics = RuntimeMetrics.from_ollama_payload(
            model=response_model,
            payload=response_payload,
        )

        self._last_metrics = metrics

        if self._metric_store is not None:
            sample = RuntimeMetricSample.from_runtime_metrics(
                metrics=metrics,
                timeout_seconds=self._timeout_seconds,
                keep_alive=self._keep_alive,
            )

            self._metric_store.append(sample)

        return ConversationResponse(
            content=generated_content,
            model=response_model,
            provider="ollama",
        )
