import subprocess
from pathlib import Path

import malak.app.composition as composition
from malak.app.composition import build_conversation_kernel
from malak.core.conversation_registry import ConversationProviderRegistry
from malak.core.request import Request
from malak.kernel.kernel import Kernel
from malak.providers.runtime_provider import RuntimeConversationProvider
from malak.runtime.mock_llm_runtime import MockLLMRuntime
from malak.services.conversation_service import ConversationService


def build_service() -> ConversationService:
    registry = ConversationProviderRegistry()
    registry.register(
        "mock",
        RuntimeConversationProvider(MockLLMRuntime()),
    )

    return ConversationService(registry)


def test_build_conversation_kernel_returns_kernel():
    kernel = build_conversation_kernel(
        service=build_service(),
        provider_name="mock",
    )

    assert isinstance(kernel, Kernel)


def test_build_conversation_kernel_composes_conversation_path():
    kernel = build_conversation_kernel(
        service=build_service(),
        provider_name="mock",
        model="test-model",
        system_prompt="You are Malak.",
    )

    response = kernel.receive(
        Request(
            content="Hola",
            session_id="composition-test",
        )
    )

    assert response.content == "[RUNTIME] Hola"
    assert response.source == "conversation"


def _run_git(repo: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def _create_repository(repo: Path) -> str:
    repo.mkdir()
    _run_git(repo, "init")
    _run_git(repo, "config", "user.email", "tests@example.invalid")
    _run_git(repo, "config", "user.name", "Malak Tests")

    (repo / "README.md").write_text(
        "Malak test repository\n",
        encoding="utf-8",
    )
    _run_git(repo, "add", "README.md")
    _run_git(repo, "commit", "-m", "initial")

    return _run_git(repo, "rev-parse", "HEAD")


def _commit_repository_change(repo: Path) -> str:
    (repo / "README.md").write_text(
        "Malak test repository\nsecond commit\n",
        encoding="utf-8",
    )
    _run_git(repo, "add", "README.md")
    _run_git(repo, "commit", "-m", "second")

    return _run_git(repo, "rev-parse", "HEAD")


def test_build_engineering_kernel_set_exposes_exact_routes_on_one_snapshot(
    tmp_path,
) -> None:
    repo = tmp_path / "repo"
    baseline = _create_repository(repo)

    builder = getattr(
        composition,
        "build_engineering_kernel_set",
    )

    engineering = builder(
        repository_root=repo,
        service=build_service(),
        provider_name="mock",
    )

    assert engineering.baseline_commit == baseline
    assert set(engineering.kernels) == {
        "inspect",
        "analyze",
        "propose",
    }
    assert all(
        isinstance(kernel, Kernel)
        for kernel in engineering.kernels.values()
    )

    later_head = _commit_repository_change(repo)
    assert later_head != baseline

    expected_sources = {
        "inspect": "engineering_inspect",
        "analyze": "engineering_analyze",
        "propose": "engineering_propose",
    }

    for action, kernel in engineering.kernels.items():
        response = kernel.receive(
            Request(
                content="E5_SUBJECT_WITH_NO_MATCH",
                session_id=f"composition-{action}",
            )
        )

        assert response.source == expected_sources[action]
        assert f"baseline_commit: {baseline}" in response.content
        assert later_head not in response.content


def test_build_engineering_kernel_set_rejects_implicit_cwd_contract(
    tmp_path,
    monkeypatch,
) -> None:
    repo = tmp_path / "repo"
    _create_repository(repo)
    monkeypatch.chdir(repo)

    builder = getattr(
        composition,
        "build_engineering_kernel_set",
    )

    try:
        builder(
            service=build_service(),
            provider_name="mock",
        )
    except TypeError:
        pass
    else:
        raise AssertionError(
            "Engineering composition must require explicit repository_root"
        )
