from __future__ import annotations

import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Final, Protocol

from malak.runtime.runtime_generation_contract import RuntimeGenerationContract


_MAX_RESPONSE_JSON_SCHEMA_BYTES: Final = 64 * 1024


def _reject_duplicate_json_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_nonfinite_json(value: str):
    raise ValueError(f"non-finite JSON constant is not allowed: {value}")


@dataclass(frozen=True)
class ConversationMessage:
    role: str
    content: str


    def __post_init__(self) -> None:
        if self.role not in {"user", "assistant"}:
            raise ValueError("role must be 'user' or 'assistant'")


@dataclass(frozen=True)
class ConversationRequest:
    prompt: str
    model: str | None = None
    system_prompt: str | None = None
    history: tuple[ConversationMessage, ...] = ()
    response_json_schema: str | None = None
    generation_contract: RuntimeGenerationContract | None = None

    def __post_init__(self) -> None:
        contract = self.generation_contract
        if contract is not None and not isinstance(
            contract,
            RuntimeGenerationContract,
        ):
            raise TypeError(
                "generation_contract must be a RuntimeGenerationContract"
            )

        schema = self.response_json_schema
        if schema is None:
            return
        if not isinstance(schema, str):
            raise TypeError("response_json_schema must be a string")
        if not schema or schema.strip() != schema:
            raise ValueError(
                "response_json_schema must be a non-empty trimmed string"
            )
        try:
            encoded = schema.encode("utf-8")
        except UnicodeEncodeError as exc:
            raise ValueError(
                "response_json_schema must be valid UTF-8 text"
            ) from exc
        if len(encoded) > _MAX_RESPONSE_JSON_SCHEMA_BYTES:
            raise ValueError(
                "response_json_schema exceeds hard UTF-8 byte limit"
            )
        try:
            payload = json.loads(
                schema,
                object_pairs_hook=_reject_duplicate_json_keys,
                parse_constant=_reject_nonfinite_json,
            )
        except (json.JSONDecodeError, ValueError, TypeError, RecursionError) as exc:
            raise ValueError(
                "response_json_schema must be strict JSON"
            ) from exc
        if not isinstance(payload, dict):
            raise ValueError(
                "response_json_schema JSON root must be an object"
            )
        canonical = json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
        if len(canonical.encode("utf-8")) > _MAX_RESPONSE_JSON_SCHEMA_BYTES:
            raise ValueError(
                "response_json_schema exceeds hard UTF-8 byte limit"
            )
        object.__setattr__(self, "response_json_schema", canonical)


@dataclass(frozen=True)
class ConversationResponse:
    content: str
    model: str | None = None
    provider: str | None = None


class ConversationProvider(ABC):
    @abstractmethod
    def generate(self, request: ConversationRequest) -> ConversationResponse:
        raise NotImplementedError