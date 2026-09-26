from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RuntimeGenerationContract:
    context_window_tokens: int
    max_output_tokens: int
    thinking_enabled: bool

    def __post_init__(self) -> None:
        for field_name in (
            "context_window_tokens",
            "max_output_tokens",
        ):
            value = getattr(self, field_name)
            if type(value) is not int:
                raise TypeError(f"{field_name} must be an integer")
            if value <= 0:
                raise ValueError(f"{field_name} must be greater than zero")

        if type(self.thinking_enabled) is not bool:
            raise TypeError("thinking_enabled must be a boolean")

        if self.max_output_tokens >= self.context_window_tokens:
            raise ValueError(
                "max_output_tokens must be lower than context_window_tokens"
            )

    def to_generation_options(self) -> dict[str, object]:
        return {
            "context_window_tokens": self.context_window_tokens,
            "max_output_tokens": self.max_output_tokens,
            "thinking_enabled": self.thinking_enabled,
            "input_truncation_allowed": False,
            "history_shift_allowed": False,
        }
