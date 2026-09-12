from dataclasses import dataclass
from datetime import datetime, timezone
from enum import StrEnum
from hashlib import sha256
import json

from malak.memory.episodic_admission import EpisodicMemoryCandidate


CANDIDATE_CONTENT_IDENTITY_POLICY_VERSION = (
    "episodic-candidate-content-identity/v1"
)
CANDIDATE_CONTENT_CANONICALIZATION_VERSION = (
    "episodic-memory-candidate-json/v1"
)
CANDIDATE_CONTENT_DIGEST_ALGORITHM = "sha256"
CANDIDATE_CONTENT_DOMAIN_SEPARATOR = (
    "MALAK:EPISODIC_CANDIDATE_CONTENT_IDENTITY:v1\n"
)
_CANDIDATE_CONTENT_SCHEMA = "malak.episodic_memory_candidate/v1"
_LOWERCASE_HEX = frozenset("0123456789abcdef")


def _require_string(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    return value


def _require_nonempty_string(value: str, field_name: str) -> str:
    value = _require_string(value, field_name)
    if not value:
        raise ValueError(f"{field_name} must not be empty")
    return value


def _require_candidate_id(value: str) -> str:
    value = _require_nonempty_string(value, "candidate_id")
    if value.strip() != value:
        raise ValueError("candidate_id must not contain surrounding whitespace")
    return value


def _require_digest_hex(value: str) -> str:
    value = _require_nonempty_string(value, "digest_hex")
    if any(character not in _LOWERCASE_HEX for character in value):
        raise ValueError("digest_hex must contain only lowercase hexadecimal")
    return value


@dataclass(frozen=True, slots=True)
class EpisodicCandidateContentIdentity:
    candidate_id: str
    digest_algorithm: str
    digest_hex: str
    canonicalization_version: str
    policy_version: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "candidate_id",
            _require_candidate_id(self.candidate_id),
        )
        object.__setattr__(
            self,
            "digest_algorithm",
            _require_nonempty_string(self.digest_algorithm, "digest_algorithm"),
        )
        object.__setattr__(
            self,
            "digest_hex",
            _require_digest_hex(self.digest_hex),
        )
        object.__setattr__(
            self,
            "canonicalization_version",
            _require_nonempty_string(
                self.canonicalization_version,
                "canonicalization_version",
            ),
        )
        object.__setattr__(
            self,
            "policy_version",
            _require_nonempty_string(self.policy_version, "policy_version"),
        )


class CandidateContentIdentityVerification(StrEnum):
    MATCH = "match"
    MISMATCH = "mismatch"


def _timestamp_v1(value: datetime) -> str:
    return (
        value.astimezone(timezone.utc)
        .isoformat(timespec="microseconds")
        .replace("+00:00", "Z")
    )


def _candidate_payload_v1(candidate: EpisodicMemoryCandidate) -> dict[str, object]:
    return {
        "schema": _CANDIDATE_CONTENT_SCHEMA,
        "candidate_id": candidate.candidate_id,
        "origin": {
            "session_id": candidate.origin.session_id,
            "request_id": candidate.origin.request_id,
            "request_created_at": _timestamp_v1(
                candidate.origin.request_created_at
            ),
            "provider": candidate.origin.provider,
            "model": candidate.origin.model,
        },
        "experience": {
            "user_content": candidate.experience.user_content,
            "assistant_content": candidate.experience.assistant_content,
        },
        "control": {
            "subject_scope": candidate.control.subject_scope,
            "domain": candidate.control.domain,
            "purpose": candidate.control.purpose,
            "source_authority_classification": (
                candidate.control.source_authority_classification
            ),
            "confidence_classification": candidate.control.confidence_classification,
            "sensitivity_classification": (
                candidate.control.sensitivity_classification
            ),
            "valid_from": (
                _timestamp_v1(candidate.control.valid_from)
                if candidate.control.valid_from is not None
                else None
            ),
            "valid_until": (
                _timestamp_v1(candidate.control.valid_until)
                if candidate.control.valid_until is not None
                else None
            ),
        },
        "created_at": _timestamp_v1(candidate.created_at),
    }


def _canonical_json_v1(candidate: EpisodicMemoryCandidate) -> str:
    return json.dumps(
        _candidate_payload_v1(candidate),
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def compute_episodic_candidate_content_identity(
    candidate: EpisodicMemoryCandidate,
) -> EpisodicCandidateContentIdentity:
    if not isinstance(candidate, EpisodicMemoryCandidate):
        raise TypeError("candidate must be an EpisodicMemoryCandidate")

    digest_input = (
        CANDIDATE_CONTENT_DOMAIN_SEPARATOR.encode("utf-8")
        + _canonical_json_v1(candidate).encode("utf-8")
    )
    digest_hex = sha256(digest_input).hexdigest()

    return EpisodicCandidateContentIdentity(
        candidate_id=candidate.candidate_id,
        digest_algorithm=CANDIDATE_CONTENT_DIGEST_ALGORITHM,
        digest_hex=digest_hex,
        canonicalization_version=CANDIDATE_CONTENT_CANONICALIZATION_VERSION,
        policy_version=CANDIDATE_CONTENT_IDENTITY_POLICY_VERSION,
    )


def verify_episodic_candidate_content_identity(
    candidate: EpisodicMemoryCandidate,
    identity: EpisodicCandidateContentIdentity,
) -> CandidateContentIdentityVerification:
    if not isinstance(candidate, EpisodicMemoryCandidate):
        raise TypeError("candidate must be an EpisodicMemoryCandidate")
    if not isinstance(identity, EpisodicCandidateContentIdentity):
        raise TypeError("identity must be an EpisodicCandidateContentIdentity")

    if identity.candidate_id != candidate.candidate_id:
        return CandidateContentIdentityVerification.MISMATCH
    if identity.digest_algorithm != CANDIDATE_CONTENT_DIGEST_ALGORITHM:
        return CandidateContentIdentityVerification.MISMATCH
    if (
        identity.canonicalization_version
        != CANDIDATE_CONTENT_CANONICALIZATION_VERSION
    ):
        return CandidateContentIdentityVerification.MISMATCH
    if identity.policy_version != CANDIDATE_CONTENT_IDENTITY_POLICY_VERSION:
        return CandidateContentIdentityVerification.MISMATCH

    recomputed = compute_episodic_candidate_content_identity(candidate)
    if recomputed.digest_hex != identity.digest_hex:
        return CandidateContentIdentityVerification.MISMATCH

    return CandidateContentIdentityVerification.MATCH
