from __future__ import annotations

import ast
import importlib.util
from pathlib import Path

import pytest


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

# Caracteriza la frontera vigente: un adapter downstream no depende de
# los orquestadores upstream. No prueba ausencia de control dinámico.
RUNTIME_UPSTREAM_IMPORTS = (
    "malak.app",
    "malak.kernel",
    "malak.capabilities",
    "malak.services",
)


def _invariant_name(forbidden: tuple[str, ...]) -> str:
    if forbidden == KERNEL_FORBIDDEN:
        return "CA-I1"
    if forbidden == SECURITY_FORBIDDEN:
        return "CA-I2"
    if forbidden == RUNTIME_UPSTREAM_IMPORTS:
        return "RUNTIME-UPSTREAM-IMPORTS"
    raise ValueError("unrecognized architecture test boundary")


def _boundary_for(target: str, forbidden: tuple[str, ...]) -> str | None:
    return next(
        (
            boundary
            for boundary in forbidden
            if target == boundary or target.startswith(boundary + ".")
        ),
        None,
    )


def _import_targets(source: str, package: str):
    for node in ast.walk(ast.parse(source)):
        observed = ast.get_source_segment(source, node) or "import"
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield node.lineno, observed, alias.name
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                name = "." * node.level + (node.module or "")
                base = importlib.util.resolve_name(name, package)
            else:
                base = node.module or ""
            if base:
                yield node.lineno, observed, base
            for alias in node.names:
                if alias.name != "*":
                    yield node.lineno, observed, (
                        f"{base}.{alias.name}" if base else alias.name
                    )


def _find_violations(
    source: str,
    *,
    package: str,
    forbidden: tuple[str, ...],
    file: str = "<synthetic>",
) -> list[dict[str, object]]:
    violations = []
    for line, observed, target in _import_targets(source, package):
        boundary = _boundary_for(target, forbidden)
        if boundary:
            violations.append(
                {
                    "invariant": _invariant_name(forbidden),
                    "file": file,
                    "line": line,
                    "observed_import": observed,
                    "normalized_target": target,
                    "forbidden_boundary": boundary,
                }
            )
    return violations


def _package_for(path: Path) -> str:
    return ".".join(path.relative_to(SRC).with_suffix("").parts[:-1])


def _scan_tree(root: Path, forbidden: tuple[str, ...]) -> list[dict[str, object]]:
    violations = []
    for path in sorted(root.rglob("*.py")):
        violations.extend(
            _find_violations(
                path.read_text(encoding="utf-8"),
                package=_package_for(path),
                forbidden=forbidden,
                file=path.relative_to(ROOT).as_posix(),
            )
        )
    return violations


@pytest.mark.parametrize(
    ("source", "package", "forbidden", "boundary"),
    [
        ("import malak.runtime.mock_llm_runtime\n", "malak.kernel", KERNEL_FORBIDDEN, "malak.runtime"),
        ("from malak.providers.runtime_provider import RuntimeConversationProvider\n", "malak.kernel", KERNEL_FORBIDDEN, "malak.providers"),
        ("from malak.services import conversation_service\n", "malak.kernel", KERNEL_FORBIDDEN, "malak.services.conversation_service"),
        ("from ..runtime import mock_llm_runtime\n", "malak.kernel", KERNEL_FORBIDDEN, "malak.runtime"),
        ("from malak.runtime.ollama_runtime import OllamaRuntime\n", "malak.security", SECURITY_FORBIDDEN, "malak.runtime"),
        ("from malak.core.llm_runtime import LLMRuntime\n", "malak.security", SECURITY_FORBIDDEN, "malak.core.llm_runtime"),
        ("from ..core import llm_runtime\n", "malak.security", SECURITY_FORBIDDEN, "malak.core.llm_runtime"),
    ],
)
def test_forbidden_static_imports_are_detected(
    source: str,
    package: str,
    forbidden: tuple[str, ...],
    boundary: str,
) -> None:
    violations = _find_violations(source, package=package, forbidden=forbidden)
    assert violations[0]["forbidden_boundary"] == boundary
    assert set(violations[0]) == {
        "invariant", "file", "line", "observed_import",
        "normalized_target", "forbidden_boundary",
    }


@pytest.mark.parametrize(
    ("source", "package", "forbidden"),
    [
        ("from malak.services.planner import Planner\n", "malak.kernel", KERNEL_FORBIDDEN),
        ("import malak.runtime_tools\n", "malak.kernel", KERNEL_FORBIDDEN),
        ("import malak.runtime_tools\n", "malak.security", SECURITY_FORBIDDEN),
    ],
)
def test_allowed_neighbor_imports_are_not_rejected(
    source: str,
    package: str,
    forbidden: tuple[str, ...],
) -> None:
    assert _find_violations(source, package=package, forbidden=forbidden) == []


@pytest.mark.parametrize(
    ("relative_root", "forbidden"),
    [
        (Path("malak/kernel"), KERNEL_FORBIDDEN),
        (Path("malak/security"), SECURITY_FORBIDDEN),
    ],
)
def test_current_tree_satisfies_static_import_invariant(
    relative_root: Path,
    forbidden: tuple[str, ...],
) -> None:
    assert _scan_tree(SRC / relative_root, forbidden) == []


@pytest.mark.parametrize(
    ("source", "package", "expected_boundary"),
    [
        (
            "from malak.kernel.registry import CapabilityRegistry\n",
            "malak.runtime",
            "malak.kernel",
        ),
        (
            "from ..app.composition import build_conversation_kernel\n",
            "malak.providers",
            "malak.app",
        ),
        (
            "import malak.capabilities.conversation\n",
            "malak.runtime",
            "malak.capabilities",
        ),
        (
            "from malak.services.conversation_service import ConversationService\n",
            "malak.providers",
            "malak.services",
        ),
    ],
)
def test_upstream_import_detection_is_effective(
    source: str, package: str, expected_boundary: str
) -> None:
    """A forbidden dependency must be observable in a synthetic fixture."""
    violations = _find_violations(
        source, package=package, forbidden=RUNTIME_UPSTREAM_IMPORTS
    )
    assert violations
    assert {item["forbidden_boundary"] for item in violations} == {
        expected_boundary
    }
    assert {item["invariant"] for item in violations} == {
        "RUNTIME-UPSTREAM-IMPORTS"
    }


@pytest.mark.parametrize(
    "relative_root",
    [Path("malak/runtime"), Path("malak/providers")],
)
def test_runtime_adapters_preserve_observed_upstream_import_boundary(
    relative_root: Path,
) -> None:
    """Characterize current static imports, not every ADR-003 authority path."""
    assert _scan_tree(SRC / relative_root, RUNTIME_UPSTREAM_IMPORTS) == []
