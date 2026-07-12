from __future__ import annotations

import json
from json import JSONDecodeError
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from malak.core.conversation import (
    ConversationRequest,
    ConversationResponse,
)
from malak.core.llm_runtime import LLMRuntime
from malak.runtime.runtime_metrics import RuntimeMetrics


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
    ) -> None:
        normalized_base_url = base_url.strip().rstrip("/")

        if not normalized_base_url:
            raise ValueError("base_url must not be empty")

        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be greater than zero")

        self._base_url = normalized_base_url
        self._timeout_seconds = timeout_seconds
        self._keep_alive = keep_alive
        self._last_metrics: RuntimeMetrics | None = None

    @property
    def last_metrics(self) -> RuntimeMetrics | None:
        """
        Metrics from the most recent successfully decoded Ollama response.

        These metrics are diagnostic and are not persisted by the runtime.
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

        payload: dict[str, Any] = {
            "model": model,
            "prompt": request.prompt,
            "stream": False,
            "keep_alive": self._keep_alive,
        }

        if request.system_prompt is not None:
            payload["system"] = request.system_prompt

        encoded_payload = json.dumps(payload).encode("utf-8")

        http_request = Request(
            url=f"{self._base_url}/api/generate",
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
                raw_response = http_response.read()

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

        generated_content = response_payload.get("response")

        if not isinstance(generated_content, str):
            raise RuntimeError(
                "Ollama response does not contain a valid response field"
            )

        response_model = response_payload.get("model")

        if not isinstance(response_model, str) or not response_model:
            response_model = model

        self._last_metrics = RuntimeMetrics.from_ollama_payload(
            model=response_model,
            payload=response_payload,
        )

        return ConversationResponse(
            content=generated_content,
            model=response_model,
            provider="ollama",
        )