"""Contrato de packaging para iniciar la CLI existente con `malak`.

No introduce otro runtime, ni un nuevo mecanismo de permisos.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import tomllib
from importlib import import_module
from importlib.metadata import PackageNotFoundError, distribution
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_ENTRYPOINT = "malak.app.cli:main"


def test_console_script_resolves_to_existing_cli_main() -> None:
    """El entrypoint público reutiliza main sin wrapper cognitivo."""
    project = tomllib.loads(
        (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    )["project"]
    entrypoint = project["scripts"]["malak"]
    assert entrypoint == EXPECTED_ENTRYPOINT
    module_name, attribute = entrypoint.split(":", maxsplit=1)
    assert callable(getattr(import_module(module_name), attribute))


def test_installed_console_script_starts_mock_cli(tmp_path: Path) -> None:
    """Smoke real del ejecutable cuando el paquete está instalado."""
    try:
        package = distribution("malak")
    except PackageNotFoundError:
        pytest.skip("requires pip install -e . or an installed wheel")

    entrypoints = [
        entry
        for entry in package.entry_points
        if entry.group == "console_scripts" and entry.name == "malak"
    ]
    assert len(entrypoints) == 1
    assert entrypoints[0].value == EXPECTED_ENTRYPOINT

    executable = shutil.which("malak")
    assert executable is not None, "installed malak console script is missing"

    environment = os.environ.copy()
    environment["MALAK_RUNTIME"] = "mock"
    environment["PYTHONIOENCODING"] = "utf-8"
    environment.pop("MALAK_REPOSITORY_ROOT", None)

    completed = subprocess.run(
        [executable],
        input="info\nexit\n",
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        cwd=tmp_path,
        env=environment,
        timeout=30,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    assert "Malāk CLI" in completed.stdout
    assert "Malāk Info V0" in completed.stdout
    assert "Sesión finalizada." in completed.stdout
