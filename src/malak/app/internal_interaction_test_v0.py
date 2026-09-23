from __future__ import annotations

import re
import subprocess
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Final

from malak.app.internal_interaction import (
    InternalInteractionResult,
    InternalInteractionRunner,
    validate_internal_interaction_artifacts,
)
from malak.app.trace_view import (
    LiveTraceTextView,
    load_trace_projection,
)
from malak.observability.execution_trace_projection import (
    ExecutionTraceProjection,
)
from malak.runtime.ollama_runtime import OllamaRuntime


TASK_ID: Final[str] = "governed-self-review-bootstrap-v0"
FOCUS_ID: Final[str] = "U01"
FOCUS_LABEL: Final[str] = "U01 Core Kernel"
SCOPE: Final[str] = "Kernel"

_RUN_ID_RE: Final[re.Pattern[str]] = re.compile(
    r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$"
)
_GIT_TIMEOUT_SECONDS: Final[float] = 30.0


@dataclass(frozen=True, slots=True)
class InternalInteractionTestV0Result:
    internal_result: InternalInteractionResult
    live_projection: ExecutionTraceProjection
    replay_projection: ExecutionTraceProjection
    live_replay_equivalence: bool
    tracked_tree_clean: bool
    acceptance: str
    runtime: str
    model: str
    authority_effect: str = "none"

    def summary(self) -> dict[str, object]:
        return {
            "run_id": self.internal_result.run_id,
            "baseline_commit": self.internal_result.baseline_commit,
            "runtime": self.runtime,
            "model": self.model,
            "terminal_disposition": self.internal_result.disposition.value,
            "component_path": list(self.internal_result.component_path),
            "artifact_dir": str(self.internal_result.artifact_dir),
            "live_replay_equivalence": self.live_replay_equivalence,
            "tracked_tree_clean": self.tracked_tree_clean,
            "acceptance": self.acceptance,
            "authority_effect": self.authority_effect,
        }


class InternalInteractionTestV0Harness:
    def __init__(
        self,
        *,
        repository_root: str | Path,
        engineering,
        runtime: OllamaRuntime,
        model: str,
        output_fn: Callable[[str], None] = print,
    ) -> None:
        if repository_root is None:
            raise ValueError("repository_root is required")

        root = Path(repository_root).expanduser()
        if not root.is_dir():
            raise ValueError("repository_root must be an existing directory")
        if not (root / ".git").exists():
            raise ValueError("repository_root must be a Git repository")

        if engineering is None:
            raise TypeError("engineering is required")

        for attribute in (
            "baseline_commit",
            "kernels",
            "repository_reader",
            "knowledge_reader",
        ):
            if not hasattr(engineering, attribute):
                raise TypeError(f"engineering must expose {attribute}")

        if not isinstance(runtime, OllamaRuntime):
            raise ValueError(
                "Internal Interaction Test V0 requires OllamaRuntime"
            )

        if not isinstance(model, str) or not model.strip():
            raise ValueError("model is required")
        if model != model.strip():
            raise ValueError("model must not contain surrounding whitespace")

        if not callable(output_fn):
            raise TypeError("output_fn must be callable")

        self._repository_root = root
        self._engineering = engineering
        self._runtime = runtime
        self._model = model
        self._output_fn = output_fn

    def run(
        self,
        *,
        run_id: str,
        external_validation_refs: tuple[str, ...],
        created_at: datetime | None = None,
    ) -> InternalInteractionTestV0Result:
        self._validate_run_id(run_id)
        refs = self._validate_refs(external_validation_refs)

        branch = self._git("rev-parse", "--abbrev-ref", "HEAD")
        if branch != "main":
            raise RuntimeError(
                "Internal Interaction Test V0 requires branch main"
            )

        current_head = self._git("rev-parse", "HEAD")
        if current_head != self._engineering.baseline_commit:
            raise RuntimeError(
                "engineering baseline does not match current repository HEAD"
            )

        if not self._tracked_tree_clean():
            raise RuntimeError(
                "tracked working tree must be clean before execution"
            )

        artifact_root = (
            self._repository_root
            / "runtime"
            / "internal_interaction"
        )
        artifact_dir = artifact_root / run_id
        if artifact_dir.exists():
            raise FileExistsError(
                f"run already exists: {run_id}"
            )

        live_view = LiveTraceTextView(output_fn=self._output_fn)
        runner = InternalInteractionRunner(
            engineering=self._engineering,
            artifact_root=artifact_root,
            runtime_name=type(self._runtime).__name__,
            model=self._model,
            event_sink=live_view.append,
        )

        started_at = created_at if created_at is not None else datetime.now(UTC)
        internal_result = runner.run(
            task_id=TASK_ID,
            scope=SCOPE,
            external_validation_refs=refs,
            run_id=run_id,
            created_at=started_at,
        )

        validate_internal_interaction_artifacts(
            internal_result.artifact_dir
        )

        replay_projection = load_trace_projection(
            repository_root=self._repository_root,
            run_id=run_id,
        )
        live_projection = live_view.projection

        equivalent = live_projection == replay_projection
        tracked_clean = self._tracked_tree_clean()
        acceptance = (
            "PASS"
            if equivalent and tracked_clean
            else "INCONCLUSIVE"
        )

        return InternalInteractionTestV0Result(
            internal_result=internal_result,
            live_projection=live_projection,
            replay_projection=replay_projection,
            live_replay_equivalence=equivalent,
            tracked_tree_clean=tracked_clean,
            acceptance=acceptance,
            runtime=type(self._runtime).__name__,
            model=self._model,
            authority_effect="none",
        )

    def _git(self, *args: str) -> str:
        try:
            completed = subprocess.run(
                [
                    "git",
                    "-C",
                    str(self._repository_root),
                    *args,
                ],
                check=True,
                capture_output=True,
                text=True,
                timeout=_GIT_TIMEOUT_SECONDS,
            )
        except FileNotFoundError as exc:
            raise RuntimeError("Git executable is unavailable") from exc
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError(
                "Git preflight inspection timed out"
            ) from exc
        except subprocess.CalledProcessError as exc:
            raise RuntimeError(
                "Git preflight inspection failed"
            ) from exc
        return completed.stdout.strip()

    def _tracked_tree_clean(self) -> bool:
        status = self._git(
            "status",
            "--porcelain",
            "--untracked-files=no",
        )
        return status == ""

    @staticmethod
    def _validate_run_id(run_id: object) -> None:
        if not isinstance(run_id, str):
            raise TypeError("run_id must be a string")
        if not _RUN_ID_RE.fullmatch(run_id):
            raise ValueError("run_id is not safe for Internal Interaction Test V0")

    @staticmethod
    def _validate_refs(
        refs: object,
    ) -> tuple[str, ...]:
        if not isinstance(refs, tuple):
            raise TypeError("external_validation_refs must be a tuple")
        if not refs:
            raise ValueError(
                "external_validation_refs must not be empty"
            )

        normalized: list[str] = []
        seen: set[str] = set()
        for index, value in enumerate(refs):
            if not isinstance(value, str):
                raise TypeError(
                    f"external_validation_refs[{index}] must be a string"
                )
            if not value or value != value.strip():
                raise ValueError(
                    f"external_validation_refs[{index}] is invalid"
                )
            if any(ord(ch) < 32 or ord(ch) == 127 for ch in value):
                raise ValueError(
                    f"external_validation_refs[{index}] contains control characters"
                )
            if value in seen:
                raise ValueError(
                    f"duplicate external validation ref: {value}"
                )
            seen.add(value)
            normalized.append(value)

        return tuple(normalized)
