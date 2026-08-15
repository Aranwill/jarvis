from datetime import datetime, timedelta, timezone

from malak.security.clock import Clock
from malak.security.context_validator import SecurityContextValidator
from malak.security.contracts import SecurityContext


class FixedClock:
    def __init__(self, current_time: datetime) -> None:
        self._current_time = current_time

    def now(self) -> datetime:
        return self._current_time


def _make_context(
    *,
    issued_at: datetime,
    expires_at: datetime,
) -> SecurityContext:
    return SecurityContext(
        context_id="context-001",
        session_id="session-001",
        subject_id="aranwill",
        authenticated=True,
        issued_at=issued_at,
        expires_at=expires_at,
    )


def _validate(
    clock: Clock,
    context: SecurityContext,
) -> bool:
    return SecurityContextValidator(clock).is_valid(context)


def test_context_is_valid_before_expiration() -> None:
    now = datetime(2026, 8, 15, 22, 30, tzinfo=timezone.utc)

    context = _make_context(
        issued_at=now - timedelta(minutes=10),
        expires_at=now + timedelta(minutes=10),
    )

    assert _validate(FixedClock(now), context) is True


def test_context_is_expired_exactly_at_expiration() -> None:
    expires_at = datetime(2026, 8, 15, 22, 30, tzinfo=timezone.utc)

    context = _make_context(
        issued_at=expires_at - timedelta(minutes=20),
        expires_at=expires_at,
    )

    assert _validate(FixedClock(expires_at), context) is False


def test_context_is_expired_after_expiration() -> None:
    expires_at = datetime(2026, 8, 15, 22, 30, tzinfo=timezone.utc)

    context = _make_context(
        issued_at=expires_at - timedelta(minutes=20),
        expires_at=expires_at,
    )

    assert (
        _validate(
            FixedClock(expires_at + timedelta(seconds=1)),
            context,
        )
        is False
    )


def test_validator_uses_injected_clock() -> None:
    fixed_now = datetime(2026, 8, 15, 22, 30, tzinfo=timezone.utc)

    context = _make_context(
        issued_at=fixed_now - timedelta(minutes=10),
        expires_at=fixed_now + timedelta(minutes=10),
    )

    assert _validate(FixedClock(fixed_now), context) is True


def test_context_is_invalid_before_issued_at() -> None:
    issued_at = datetime(2026, 8, 15, 22, 30, tzinfo=timezone.utc)

    context = _make_context(
        issued_at=issued_at,
        expires_at=issued_at + timedelta(minutes=30),
    )

    assert (
        _validate(
            FixedClock(issued_at - timedelta(seconds=1)),
            context,
        )
        is False
    )


def test_context_is_valid_exactly_at_issued_at() -> None:
    issued_at = datetime(2026, 8, 15, 22, 30, tzinfo=timezone.utc)

    context = _make_context(
        issued_at=issued_at,
        expires_at=issued_at + timedelta(minutes=30),
    )

    assert _validate(FixedClock(issued_at), context) is True