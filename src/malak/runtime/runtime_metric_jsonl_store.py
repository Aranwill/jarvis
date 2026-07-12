from __future__ import annotations

import json
from datetime import datetime
from json import JSONDecodeError
from pathlib import Path
from typing import Any

from malak.runtime.runtime_metric_sample import RuntimeMetricSample


class JsonlRuntimeMetricStore:
    """
    Persistent JSONL store for runtime metric samples.

    Each line contains one serialized RuntimeMetricSample.
    Prompts and generated responses are intentionally excluded.
    """

    def __init__(
        self,
        file_path: str | Path,
    ) -> None:
        self._file_path = Path(file_path)

    def append(
        self,
        sample: RuntimeMetricSample,
    ) -> None:
        self._file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        serialized_sample = json.dumps(
            _sample_to_dict(sample),
            ensure_ascii=False,
            separators=(",", ":"),
        )

        with self._file_path.open(
            mode="a",
            encoding="utf-8",
            newline="\n",
        ) as file:
            file.write(serialized_sample)
            file.write("\n")

    def list_all(self) -> list[RuntimeMetricSample]:
        if not self._file_path.exists():
            return []

        samples: list[RuntimeMetricSample] = []

        with self._file_path.open(
            mode="r",
            encoding="utf-8",
        ) as file:
            for line_number, raw_line in enumerate(
                file,
                start=1,
            ):
                line = raw_line.strip()

                if not line:
                    continue

                try:
                    payload = json.loads(line)
                except JSONDecodeError as exc:
                    raise RuntimeError(
                        "Invalid runtime metric JSON "
                        f"at line {line_number}"
                    ) from exc

                if not isinstance(payload, dict):
                    raise RuntimeError(
                        "Invalid runtime metric payload "
                        f"at line {line_number}"
                    )

                try:
                    sample = _sample_from_dict(payload)
                except (KeyError, TypeError, ValueError) as exc:
                    raise RuntimeError(
                        "Invalid runtime metric sample "
                        f"at line {line_number}"
                    ) from exc

                samples.append(sample)

        return samples

    def list_by_model(
        self,
        model: str,
    ) -> list[RuntimeMetricSample]:
        normalized_model = model.strip()

        if not normalized_model:
            raise ValueError("model must not be empty")

        return [
            sample
            for sample in self.list_all()
            if sample.model == normalized_model
        ]


def _sample_to_dict(
    sample: RuntimeMetricSample,
) -> dict[str, Any]:
    return {
        "model": sample.model,
        "captured_at": sample.captured_at.isoformat(),
        "timeout_seconds": sample.timeout_seconds,
        "keep_alive": sample.keep_alive,
        "total_duration_seconds": sample.total_duration_seconds,
        "load_duration_seconds": sample.load_duration_seconds,
        "prompt_eval_count": sample.prompt_eval_count,
        "prompt_eval_duration_seconds": (
            sample.prompt_eval_duration_seconds
        ),
        "eval_count": sample.eval_count,
        "eval_duration_seconds": sample.eval_duration_seconds,
        "tokens_per_second": sample.tokens_per_second,
    }


def _sample_from_dict(
    payload: dict[str, Any],
) -> RuntimeMetricSample:
    captured_at_value = payload["captured_at"]

    if not isinstance(captured_at_value, str):
        raise TypeError("captured_at must be a string")

    captured_at = datetime.fromisoformat(captured_at_value)

    if (
        captured_at.tzinfo is None
        or captured_at.utcoffset() is None
    ):
        raise ValueError(
            "captured_at must include timezone information"
        )

    model = payload["model"]
    timeout_seconds = payload["timeout_seconds"]
    keep_alive = payload["keep_alive"]

    if not isinstance(model, str) or not model.strip():
        raise ValueError("model must not be empty")

    if (
        not isinstance(timeout_seconds, (int, float))
        or isinstance(timeout_seconds, bool)
        or timeout_seconds <= 0
    ):
        raise ValueError(
            "timeout_seconds must be greater than zero"
        )

    if not isinstance(keep_alive, (int, str)):
        raise TypeError(
            "keep_alive must be an integer or string"
        )

    return RuntimeMetricSample(
        model=model,
        captured_at=captured_at,
        timeout_seconds=float(timeout_seconds),
        keep_alive=keep_alive,
        total_duration_seconds=_optional_number(
            payload.get("total_duration_seconds")
        ),
        load_duration_seconds=_optional_number(
            payload.get("load_duration_seconds")
        ),
        prompt_eval_count=_optional_int(
            payload.get("prompt_eval_count")
        ),
        prompt_eval_duration_seconds=_optional_number(
            payload.get("prompt_eval_duration_seconds")
        ),
        eval_count=_optional_int(
            payload.get("eval_count")
        ),
        eval_duration_seconds=_optional_number(
            payload.get("eval_duration_seconds")
        ),
        tokens_per_second=_optional_number(
            payload.get("tokens_per_second")
        ),
    )


def _optional_number(
    value: object,
) -> float | None:
    if value is None:
        return None

    if isinstance(value, bool):
        raise TypeError("boolean is not a valid number")

    if isinstance(value, (int, float)):
        return float(value)

    raise TypeError("value must be numeric or null")


def _optional_int(
    value: object,
) -> int | None:
    if value is None:
        return None

    if isinstance(value, bool):
        raise TypeError("boolean is not a valid integer")

    if isinstance(value, int) and value >= 0:
        return value

    raise TypeError(
        "value must be a non-negative integer or null"
    )