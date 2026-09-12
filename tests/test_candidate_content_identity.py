from dataclasses import FrozenInstanceError, fields, replace
from datetime import UTC, datetime, timedelta

import pytest

from malak.memory.candidate_content_identity import (
    CANDIDATE_CONTENT_CANONICALIZATION_VERSION,
    CANDIDATE_CONTENT_DIGEST_ALGORITHM,
    CANDIDATE_CONTENT_DOMAIN_SEPARATOR,
    CANDIDATE_CONTENT_IDENTITY_POLICY_VERSION,
    CandidateContentIdentityVerification,
    EpisodicCandidateContentIdentity,
    compute_episodic_candidate_content_identity,
    verify_episodic_candidate_content_identity,
)
from malak.memory.episodic_admission import (
    EpisodicAdmissionContext,
    EpisodicExperience,
    EpisodicMemoryCandidate,
    EpisodicOrigin,
)


VECTOR_A_DIGEST = "d1f3634721a53840b93c62c1331be335cd1d793a115c449c41e614b0ae2799e4"
VECTOR_B_DIGEST = "101e9168491febb2ba9d45244b911971ed154ea414cce4f272ff8e72f245aeb2"
VECTOR_C1_DIGEST = "ea2f7d8c891cacd28eac11bebd5ad1c9c39c9601e7f88ab075f46def9dcb80d9"
VECTOR_C2_DIGEST = "6b3b89a8c33fbdacbdeed4eeea45768948fb9aab00ec93a0d35c9a137ccda730"


def vector_a() -> EpisodicMemoryCandidate:
    return EpisodicMemoryCandidate(
        candidate_id="candidate-001",
        origin=EpisodicOrigin(
            session_id="session-001",
            request_id="request-001",
            request_created_at=datetime(2026, 9, 12, 12, 0, tzinfo=UTC),
            provider="ollama",
            model="qwen3:8b",
        ),
        experience=EpisodicExperience(
            user_content="Hola Malāk",
            assistant_content="Hola. ¿En qué puedo ayudarte?",
        ),
        control=EpisodicAdmissionContext(
            subject_scope="conversation",
            domain="general",
            purpose="episodic_memory_candidate",
            source_authority_classification="user_asserted",
            confidence_classification="observed",
            sensitivity_classification="internal",
            valid_from=datetime(2026, 9, 12, 12, 0, tzinfo=UTC),
            valid_until=datetime(2026, 9, 13, 12, 0, tzinfo=UTC),
        ),
        created_at=datetime(2026, 9, 12, 12, 0, 1, 123456, tzinfo=UTC),
    )


def vector_b() -> EpisodicMemoryCandidate:
    return EpisodicMemoryCandidate(
        candidate_id="candidate-002",
        origin=EpisodicOrigin(
            session_id="session-002",
            request_id="request-002",
            request_created_at=datetime(2026, 9, 12, 0, 0, tzinfo=UTC),
        ),
        experience=EpisodicExperience(user_content="", assistant_content=""),
        control=EpisodicAdmissionContext(
            subject_scope="session",
            domain="test",
            purpose="identity_vector",
        ),
        created_at=datetime(2026, 9, 12, 0, 0, tzinfo=UTC),
    )


def mutate_candidate(
    candidate: EpisodicMemoryCandidate,
    path: str,
    value: object,
) -> EpisodicMemoryCandidate:
    section, _, field_name = path.partition(".")
    if not field_name:
        return replace(candidate, **{section: value})

    nested = getattr(candidate, section)
    return replace(candidate, **{section: replace(nested, **{field_name: value})})


def test_v1_constants_are_exact() -> None:
    assert CANDIDATE_CONTENT_IDENTITY_POLICY_VERSION == (
        "episodic-candidate-content-identity/v1"
    )
    assert CANDIDATE_CONTENT_CANONICALIZATION_VERSION == (
        "episodic-memory-candidate-json/v1"
    )
    assert CANDIDATE_CONTENT_DIGEST_ALGORITHM == "sha256"
    assert CANDIDATE_CONTENT_DOMAIN_SEPARATOR == (
        "MALAK:EPISODIC_CANDIDATE_CONTENT_IDENTITY:v1\n"
    )


def test_compute_is_deterministic_and_sidecar_is_immutable() -> None:
    candidate = vector_a()

    first = compute_episodic_candidate_content_identity(candidate)
    second = compute_episodic_candidate_content_identity(candidate)

    assert first == second
    assert first.candidate_id == candidate.candidate_id
    assert first.digest_algorithm == "sha256"
    assert first.canonicalization_version == (
        "episodic-memory-candidate-json/v1"
    )
    assert first.policy_version == "episodic-candidate-content-identity/v1"
    assert len(first.digest_hex) == 64
    assert first.digest_hex == first.digest_hex.lower()
    assert set(first.digest_hex) <= set("0123456789abcdef")
    assert "computed_at" not in {field.name for field in fields(first)}

    with pytest.raises(FrozenInstanceError):
        first.digest_hex = "0" * 64  # type: ignore[misc]


def test_exact_vector_a() -> None:
    identity = compute_episodic_candidate_content_identity(vector_a())

    assert identity.digest_hex == VECTOR_A_DIGEST


def test_exact_vector_b() -> None:
    identity = compute_episodic_candidate_content_identity(vector_b())

    assert identity.digest_hex == VECTOR_B_DIGEST


def test_exact_unicode_vectors_are_distinct() -> None:
    composed = replace(
        vector_b(),
        candidate_id="candidate-unicode",
        experience=EpisodicExperience(user_content="é", assistant_content=""),
    )
    decomposed = replace(
        composed,
        experience=EpisodicExperience(user_content="e\u0301", assistant_content=""),
    )

    composed_identity = compute_episodic_candidate_content_identity(composed)
    decomposed_identity = compute_episodic_candidate_content_identity(decomposed)

    assert composed_identity.digest_hex == VECTOR_C1_DIGEST
    assert decomposed_identity.digest_hex == VECTOR_C2_DIGEST
    assert composed_identity.digest_hex != decomposed_identity.digest_hex


@pytest.mark.parametrize(
    ("path", "value"),
    [
        ("candidate_id", "candidate-999"),
        ("origin.session_id", "session-999"),
        ("origin.request_id", "request-999"),
        (
            "origin.request_created_at",
            datetime(2026, 9, 12, 12, 0, 0, 1, tzinfo=UTC),
        ),
        ("origin.provider", "provider-b"),
        ("origin.model", "model-b"),
        ("experience.user_content", "Hola Malāk!"),
        ("experience.assistant_content", "Respuesta distinta"),
        ("control.subject_scope", "session"),
        ("control.domain", "memory"),
        ("control.purpose", "identity_test"),
        ("control.source_authority_classification", "derived"),
        ("control.confidence_classification", "high"),
        ("control.sensitivity_classification", "restricted"),
        (
            "control.valid_from",
            datetime(2026, 9, 12, 11, 59, 59, 999999, tzinfo=UTC),
        ),
        (
            "control.valid_until",
            datetime(2026, 9, 13, 12, 0, 0, 1, tzinfo=UTC),
        ),
        ("created_at", datetime(2026, 9, 12, 12, 0, 1, 123457, tzinfo=UTC)),
    ],
)
def test_every_material_field_changes_digest(path: str, value: object) -> None:
    candidate = vector_a()
    changed = mutate_candidate(candidate, path, value)

    baseline = compute_episodic_candidate_content_identity(candidate)
    changed_identity = compute_episodic_candidate_content_identity(changed)

    assert changed_identity.digest_hex != baseline.digest_hex


@pytest.mark.parametrize(
    ("path", "value"),
    [
        ("origin.provider", "ollama"),
        ("origin.model", "model-a"),
        ("control.source_authority_classification", "user_asserted"),
        ("control.confidence_classification", "observed"),
        ("control.sensitivity_classification", "internal"),
        ("control.valid_from", datetime(2026, 9, 11, 23, 0, tzinfo=UTC)),
        ("control.valid_until", datetime(2026, 9, 13, 0, 0, tzinfo=UTC)),
    ],
)
def test_optional_none_to_value_changes_digest(path: str, value: object) -> None:
    candidate = vector_b()
    changed = mutate_candidate(candidate, path, value)

    assert compute_episodic_candidate_content_identity(changed).digest_hex != (
        compute_episodic_candidate_content_identity(candidate).digest_hex
    )


def test_content_whitespace_newline_and_microseconds_are_material() -> None:
    candidate = vector_b()
    variants = (
        replace(
            candidate,
            experience=EpisodicExperience(user_content=" ", assistant_content=""),
        ),
        replace(
            candidate,
            experience=EpisodicExperience(user_content="\n", assistant_content=""),
        ),
        replace(
            candidate,
            created_at=candidate.created_at + timedelta(microseconds=1),
        ),
    )
    baseline = compute_episodic_candidate_content_identity(candidate).digest_hex

    assert all(
        compute_episodic_candidate_content_identity(item).digest_hex != baseline
        for item in variants
    )


def test_verify_exact_sidecar_matches() -> None:
    candidate = vector_a()
    identity = compute_episodic_candidate_content_identity(candidate)

    assert (
        verify_episodic_candidate_content_identity(candidate, identity)
        is CandidateContentIdentityVerification.MATCH
    )


def test_verify_same_id_with_different_payload_mismatches() -> None:
    candidate = vector_a()
    identity = compute_episodic_candidate_content_identity(candidate)
    changed = replace(
        candidate,
        experience=EpisodicExperience(
            user_content=candidate.experience.user_content,
            assistant_content="substituted",
        ),
    )

    assert changed.candidate_id == candidate.candidate_id
    assert (
        verify_episodic_candidate_content_identity(changed, identity)
        is CandidateContentIdentityVerification.MISMATCH
    )


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("candidate_id", "candidate-other"),
        ("digest_algorithm", "sha512"),
        ("canonicalization_version", "episodic-memory-candidate-json/v2"),
        ("policy_version", "episodic-candidate-content-identity/v2"),
        ("digest_hex", "0" * 64),
    ],
)
def test_verify_incompatible_identity_metadata_mismatches(
    field_name: str,
    value: str,
) -> None:
    candidate = vector_a()
    identity = compute_episodic_candidate_content_identity(candidate)
    incompatible = replace(identity, **{field_name: value})

    assert (
        verify_episodic_candidate_content_identity(candidate, incompatible)
        is CandidateContentIdentityVerification.MISMATCH
    )


@pytest.mark.parametrize(
    "value",
    [None, object(), "candidate"],
)
def test_compute_rejects_wrong_candidate_type(value: object) -> None:
    with pytest.raises(TypeError):
        compute_episodic_candidate_content_identity(value)  # type: ignore[arg-type]


def test_verify_rejects_wrong_argument_types() -> None:
    candidate = vector_a()
    identity = compute_episodic_candidate_content_identity(candidate)

    with pytest.raises(TypeError):
        verify_episodic_candidate_content_identity(  # type: ignore[arg-type]
            object(), identity
        )
    with pytest.raises(TypeError):
        verify_episodic_candidate_content_identity(  # type: ignore[arg-type]
            candidate, object()
        )


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("candidate_id", ""),
        ("candidate_id", " candidate-001"),
        ("candidate_id", "candidate-001 "),
        ("digest_algorithm", ""),
        ("digest_hex", ""),
        ("canonicalization_version", ""),
        ("policy_version", ""),
    ],
)
def test_sidecar_rejects_empty_or_noncanonical_fields(
    field_name: str,
    value: str,
) -> None:
    values = {
        "candidate_id": "candidate-001",
        "digest_algorithm": "sha256",
        "digest_hex": "a" * 64,
        "canonicalization_version": "episodic-memory-candidate-json/v1",
        "policy_version": "episodic-candidate-content-identity/v1",
    }
    values[field_name] = value

    with pytest.raises(ValueError):
        EpisodicCandidateContentIdentity(**values)


@pytest.mark.parametrize("digest_hex", ["A" * 64, "g" * 64, "-" * 64, "00 zz"])
def test_sidecar_rejects_non_lowercase_hex_digest(digest_hex: str) -> None:
    with pytest.raises(ValueError):
        EpisodicCandidateContentIdentity(
            candidate_id="candidate-001",
            digest_algorithm="sha256",
            digest_hex=digest_hex,
            canonicalization_version="episodic-memory-candidate-json/v1",
            policy_version="episodic-candidate-content-identity/v1",
        )


@pytest.mark.parametrize(
    "field_name",
    [
        "candidate_id",
        "digest_algorithm",
        "digest_hex",
        "canonicalization_version",
        "policy_version",
    ],
)
def test_sidecar_rejects_non_string_fields(field_name: str) -> None:
    values = {
        "candidate_id": "candidate-001",
        "digest_algorithm": "sha256",
        "digest_hex": "a" * 64,
        "canonicalization_version": "episodic-memory-candidate-json/v1",
        "policy_version": "episodic-candidate-content-identity/v1",
    }
    values[field_name] = 1  # type: ignore[assignment]

    with pytest.raises(TypeError):
        EpisodicCandidateContentIdentity(**values)  # type: ignore[arg-type]
