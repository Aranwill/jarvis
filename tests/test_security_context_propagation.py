from dataclasses import FrozenInstanceError
from datetime import datetime, timedelta, timezone

import pytest

from malak.security.context_propagation import SecurityContextEnvelope
from malak.security.contracts import SecurityContext


def _make_context() -> SecurityContext:
    issued_at = datetime(2026, 8, 15, 23, 30, tzinfo=timezone.utc)

    return SecurityContext(
        context_id="context-001",
        session_id="session-001",
        subject_id="aranwill",
        authenticated=True,
        issued_at=issued_at,
        expires_at=issued_at + timedelta(minutes=30),
        parent_context_id="context-parent",
    )


def test_envelope_preserves_exact_security_context_instance() -> None:
    context = _make_context()

    envelope = SecurityContextEnvelope(context=context)

    assert envelope.context is context


def test_envelope_preserves_complete_security_context() -> None:
    context = _make_context()

    envelope = SecurityContextEnvelope(context=context)

    assert envelope.context.context_id == context.context_id
    assert envelope.context.session_id == context.session_id
    assert envelope.context.subject_id == context.subject_id
    assert envelope.context.authenticated == context.authenticated
    assert envelope.context.issued_at == context.issued_at
    assert envelope.context.expires_at == context.expires_at
    assert envelope.context.parent_context_id == context.parent_context_id


def test_envelope_rejects_non_security_context() -> None:
    with pytest.raises(TypeError):
        SecurityContextEnvelope(context="context")


def test_envelope_is_immutable() -> None:
    envelope = SecurityContextEnvelope(context=_make_context())

    with pytest.raises(FrozenInstanceError):
        envelope.context = _make_context()