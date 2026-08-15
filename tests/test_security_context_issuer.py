from datetime import datetime, timedelta, timezone

import pytest

from malak.security.clock import Clock
from malak.security.context_issuer import SecurityContextIssuer


class FixedClock:
    def __init__(self, current_time: datetime) -> None:
        self._current_time = current_time

    def now(self) -> datetime:
        return self._current_time


def test_issuer_creates_security_context_with_expected_lifecycle() -> None:
    now = datetime(2026, 8, 15, 23, 0, tzinfo=timezone.utc)

    issuer = SecurityContextIssuer(FixedClock(now))

    context = issuer.issue(
        session_id="session-001",
        subject_id="aranwill",
        authenticated=True,
        lifetime=timedelta(minutes=30),
    )

    assert context.context_id
    assert context.session_id == "session-001"
    assert context.subject_id == "aranwill"
    assert context.authenticated is True
    assert context.issued_at == now
    assert context.expires_at == now + timedelta(minutes=30)
    assert context.parent_context_id is None


def test_issuer_preserves_parent_context_id() -> None:
    now = datetime(2026, 8, 15, 23, 0, tzinfo=timezone.utc)

    issuer = SecurityContextIssuer(FixedClock(now))

    context = issuer.issue(
        session_id="session-001",
        subject_id="aranwill",
        authenticated=True,
        lifetime=timedelta(minutes=30),
        parent_context_id="context-parent",
    )

    assert context.parent_context_id == "context-parent"


@pytest.mark.parametrize(
    "lifetime",
    [
        timedelta(0),
        timedelta(seconds=-1),
    ],
)
def test_issuer_rejects_non_positive_lifetime(
    lifetime: timedelta,
) -> None:
    now = datetime(2026, 8, 15, 23, 0, tzinfo=timezone.utc)

    issuer = SecurityContextIssuer(FixedClock(now))

    with pytest.raises(ValueError):
        issuer.issue(
            session_id="session-001",
            subject_id="aranwill",
            authenticated=True,
            lifetime=lifetime,
        )


def test_issuer_uses_injected_clock() -> None:
    fixed_now = datetime(2026, 8, 15, 23, 0, tzinfo=timezone.utc)

    issuer = SecurityContextIssuer(FixedClock(fixed_now))

    context = issuer.issue(
        session_id="session-001",
        subject_id="aranwill",
        authenticated=True,
        lifetime=timedelta(minutes=5),
    )

    assert context.issued_at == fixed_now