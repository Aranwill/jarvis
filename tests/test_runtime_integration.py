from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from malak.capabilities._engineering_analysis import ANALYZE_RESPONSE_JSON_SCHEMA
from malak.capabilities.engineering_analyze import EngineeringAnalyzeCapability
from malak.core.conversation import ConversationRequest
from malak.core.conversation_registry import ConversationProviderRegistry
from malak.core.request import Request
from malak.infrastructure.repository_reader import GitRepositoryReader
from malak.knowledge.knowledge_reader import GovernedKnowledgeReader
from malak.providers.runtime_provider import RuntimeConversationProvider
from malak.runtime.mock_llm_runtime import MockLLMRuntime
from malak.runtime.ollama_runtime import OllamaRuntime
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


def _make_engineering_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Malak Test")
    _git(repo, "config", "commit.gpgsign", "false")

    _write(
        repo,
        "src/malak/component.py",
        'VALUE = "needle implementation"\n',
    )
    _write(
        repo,
        "docs/governance/cognitive_constitution.md",
        "needle governed knowledge\n",
    )
    _write(
        repo,
        "docs/architecture/blueprint.md",
        "needle architecture context\n",
    )
    _write(
        repo,
        "SECURITY.md",
        "needle security context\n",
    )
    _git(repo, "add", ".")
    _git(repo, "commit", "--no-gpg-sign", "-m", "baseline")
    return repo


def test_conversation_flow_through_provider_and_runtime() -> None:
    runtime = MockLLMRuntime()
    provider = RuntimeConversationProvider(runtime)

    registry = ConversationProviderRegistry()
    registry.register("mock", provider)

    service = ConversationService(registry)

    request = ConversationRequest(
        prompt="Hola Malak",
        model="deepseek-coder-v2",
        system_prompt="Responde como runtime de prueba.",
    )

    response = service.generate(
        request=request,
        provider="mock",
    )

    assert response.content == "[RUNTIME] Hola Malak"
    assert response.model == "deepseek-coder-v2"
    assert response.provider == "runtime"
    assert registry.list() == ["mock"]


def test_analyze_structured_output_green_e2e_reaches_ollama_format_and_parser(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, object] = {}

    def fake_urlopen(
        request: object,
        timeout: float,
    ) -> _FakeHTTPResponse:
        captured["request"] = request
        captured["timeout"] = timeout
        return _FakeHTTPResponse(
            {
                "model": "qwen3.5:9b",
                "message": {
                    "role": "assistant",
                    "content": json.dumps(
                        {
                            "summary": "Grounded engineering analysis.",
                            "findings": [
                                {
                                    "classification": "ALIGNED",
                                    "statement": (
                                        "Implementation aligns with governed knowledge."
                                    ),
                                    "rationale": (
                                        "Repository and knowledge evidence support it."
                                    ),
                                    "evidence_refs": ["R1", "K1"],
                                }
                            ],
                            "uncertainties": [],
                        }
                    ),
                },
            }
        )

    monkeypatch.setattr(
        "malak.runtime.ollama_runtime.urlopen",
        fake_urlopen,
    )

    repo = _make_engineering_repo(tmp_path)
    repository_reader = GitRepositoryReader(repo)
    knowledge_reader = GovernedKnowledgeReader(repository_reader)

    runtime = OllamaRuntime(
        base_url="http://localhost:11434",
        timeout_seconds=30.0,
        keep_alive=0,
    )
    registry = ConversationProviderRegistry()
    registry.register(
        "ollama",
        RuntimeConversationProvider(runtime),
    )
    service = ConversationService(registry)

    capability = EngineeringAnalyzeCapability(
        repository_reader=repository_reader,
        knowledge_reader=knowledge_reader,
        conversation_service=service,
        provider_name="ollama",
        model="qwen3.5:9b",
    )

    result = capability.execute(
        Request(
            content="needle",
            session_id="session-A",
        )
    )

    http_request = captured["request"]
    payload = json.loads(http_request.data.decode("utf-8"))

    assert payload["format"] == json.loads(ANALYZE_RESPONSE_JSON_SCHEMA)
    assert payload["stream"] is False
    assert payload["keep_alive"] == 0
    assert captured["timeout"] == 30.0

    assert "status: GROUNDED" in result
    assert "classification=ALIGNED" in result
    assert "authority_effect: none" in result
