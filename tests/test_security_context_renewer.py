from datetime import datetime, timedelta, timezone

import pytest

from malak.security.clock import Clock
from malak.security.context_issuer import SecurityContextIssuer
from malak.security.context_renewer import SecurityContextRenewer
from malak.security.context_validator import SecurityContextValidator
from malak.security.contracts import SecurityContext


class FixedClock:
    def __init__(self, current_time: datetime) -> None:
        self._current_time = current_time

    def now(self) -> datetime:
        return self._current_time


def _make_context(
    *,
    context_id: str,
    issued_at: datetime,
    expires_at: datetime,
) -> SecurityContext:
    return SecurityContext(
        context_id=context_id,
        session_id="session-001",
        subject_id="aranwill",
        authenticated=True,
        issued_at=issued_at,
        expires_at=expires_at,
    )


def _make_renewer(clock: Clock) -> SecurityContextRenewer:
    return SecurityContextRenewer(
        validator=SecurityContextValidator(clock),
        issuer=SecurityContextIssuer(clock),
    )


def test_renewer_creates_descendant_from_valid_context() -> None:
    now = datetime(2026, 8, 15, 23, 30, tzinfo=timezone.utc)

    original = _make_context(
        context_id="context-original",
        issued_at=now - timedelta(minutes=10),
        expires_at=now + timedelta(minutes=10),
    )

    renewed = _make_renewer(FixedClock(now)).renew(
        original,
        lifetime=timedelta(minutes=30),
    )

    assert renewed.context_id != original.context_id
    assert renewed.parent_context_id == original.context_id
    assert renewed.session_id == original.session_id
    assert renewed.subject_id == original.subject_id
    assert renewed.authenticated == original.authenticated
    assert renewed.issued_at == now
    assert renewed.expires_at == now + timedelta(minutes=30)


def test_renewer_rejects_expired_context() -> None:
    expires_at = datetime(2026, 8, 15, 23, 30, tzinfo=timezone.utc)

    original = _make_context(
        context_id="context-original",
        issued_at=expires_at - timedelta(minutes=20),
        expires_at=expires_at,
    )

    with pytest.raises(ValueError):
        _make_renewer(FixedClock(expires_at)).renew(
            original,
            lifetime=timedelta(minutes=30),
        )


def test_renewer_preserves_original_context() -> None:
    now = datetime(2026, 8, 15, 23, 30, tzinfo=timezone.utc)

    original = _make_context(
        context_id="context-original",
        issued_at=now - timedelta(minutes=10),
        expires_at=now + timedelta(minutes=10),
    )

    original_snapshot = original

    _make_renewer(FixedClock(now)).renew(
        original,
        lifetime=timedelta(minutes=30),
    )

    assert original == original_snapshot
    assert original.context_id == "context-original"
    assert original.parent_context_id is None