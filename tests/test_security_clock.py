from datetime import datetime, timedelta, timezone

from malak.security.clock import Clock, SystemClock


def _read_time(clock: Clock) -> datetime:
    return clock.now()


def test_system_clock_returns_datetime() -> None:
    assert isinstance(SystemClock().now(), datetime)


def test_system_clock_returns_timezone_aware_datetime() -> None:
    current_time = SystemClock().now()

    assert current_time.tzinfo is not None
    assert current_time.utcoffset() is not None


def test_system_clock_returns_utc_datetime() -> None:
    current_time = SystemClock().now()

    assert current_time.utcoffset() == timedelta(0)


def test_clock_boundary_supports_deterministic_substitution() -> None:
    fixed_time = datetime(2026, 8, 15, 22, 30, tzinfo=timezone.utc)

    class FixedClock:
        def now(self) -> datetime:
            return fixed_time

    assert _read_time(FixedClock()) == fixed_time