from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

KERNEL_FORBIDDEN = (
    "malak.runtime",
    "malak.providers",
    "malak.services.conversation_service",
)
SECURITY_FORBIDDEN = (
    "malak.runtime",
    "malak.providers",
    "malak.core.llm_runtime",
)


def _find_violations(
    source: str,
    *,
    package: str,
    forbidden: tuple[str, ...],
    file: str = "<synthetic>",
) -> list[dict[str, object]]:
    raise NotImplementedError("RED: static import detector not implemented")


def _scan_tree(root: Path, forbidden: tuple[str, ...]) -> list[dict[str, object]]:
    raise NotImplementedError("RED: repository scan not implemented")


def _assert_boundary(source: str, package: str, forbidden: tuple[str, ...], boundary: str) -> None:
    violations = _find_violations(source, package=package, forbidden=forbidden)
    assert violations
    assert violations[0]["forbidden_boundary"] == boundary


def test_kernel_detects_absolute_runtime_import() -> None:
    _assert_boundary(
        "import malak.runtime.mock_llm_runtime\n",
        "malak.kernel",
        KERNEL_FORBIDDEN,
        "malak.runtime",
    )


def test_kernel_detects_provider_from_import() -> None:
    _assert_boundary(
        "from malak.providers.runtime_provider import RuntimeConversationProvider\n",
        "malak.kernel",
        KERNEL_FORBIDDEN,
        "malak.providers",
    )


def test_kernel_detects_conversation_service_from_parent_package() -> None:
    _assert_boundary(
        "from malak.services import conversation_service\n",
        "malak.kernel",
        KERNEL_FORBIDDEN,
        "malak.services.conversation_service",
    )


def test_kernel_detects_relative_runtime_import() -> None:
    _assert_boundary(
        "from ..runtime import mock_llm_runtime\n",
        "malak.kernel",
        KERNEL_FORBIDDEN,
        "malak.runtime",
    )


def test_kernel_allows_planner() -> None:
    assert not _find_violations(
        "from malak.services.planner import Planner\n",
        package="malak.kernel",
        forbidden=KERNEL_FORBIDDEN,
    )


def test_security_detects_runtime_import() -> None:
    _assert_boundary(
        "from malak.runtime.ollama_runtime import OllamaRuntime\n",
        "malak.security",
        SECURITY_FORBIDDEN,
        "malak.runtime",
    )


def test_security_detects_llm_runtime_import() -> None:
    _assert_boundary(
        "from malak.core.llm_runtime import LLMRuntime\n",
        "malak.security",
        SECURITY_FORBIDDEN,
        "malak.core.llm_runtime",
    )


def test_security_detects_relative_llm_runtime_import() -> None:
    _assert_boundary(
        "from ..core import llm_runtime\n",
        "malak.security",
        SECURITY_FORBIDDEN,
        "malak.core.llm_runtime",
    )


def test_similar_namespace_is_not_rejected() -> None:
    source = "import malak.runtime_tools\n"
    assert not _find_violations(source, package="malak.kernel", forbidden=KERNEL_FORBIDDEN)
    assert not _find_violations(source, package="malak.security", forbidden=SECURITY_FORBIDDEN)


def test_kernel_tree_satisfies_static_import_invariant() -> None:
    assert _scan_tree(SRC / "malak" / "kernel", KERNEL_FORBIDDEN) == []


def test_security_tree_satisfies_static_import_invariant() -> None:
    assert _scan_tree(SRC / "malak" / "security", SECURITY_FORBIDDEN) == []
