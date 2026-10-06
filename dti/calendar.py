"""NYSE trading calendar helpers (holidays, half-days, next/previous session)."""

from datetime import date, timedelta
from functools import lru_cache

import pandas_market_calendars as mcal

_LOOKAHEAD_DAYS = 14


@lru_cache(maxsize=1)
def _nyse():
    return mcal.get_calendar("NYSE")


def _sessions(start: date, end: date) -> list[date]:
    return [ts.date() for ts in _nyse().valid_days(start, end)]


def is_trading_day(d: date) -> bool:
    return d in _sessions(d, d)


def next_trading_day(d: date) -> date:
    """First session strictly after d (e.g. for "tomorrow's earnings")."""
    return _sessions(d + timedelta(days=1), d + timedelta(days=_LOOKAHEAD_DAYS))[0]


def prev_trading_day(d: date) -> date:
    """Last session strictly before d (e.g. for "prior day after-hours earnings")."""
    return _sessions(d - timedelta(days=_LOOKAHEAD_DAYS), d - timedelta(days=1))[-1]


def trading_days_ahead(d: date, n: int) -> list[date]:
    """The next n sessions after d."""
    return _sessions(d + timedelta(days=1), d + timedelta(days=n * 2 + _LOOKAHEAD_DAYS))[:n]


def is_half_day(d: date) -> bool:
    """True for early-close sessions (1pm ET close)."""
    sched = _nyse().schedule(d, d)
    if sched.empty:
        return False
    return bool(_nyse().early_closes(sched).shape[0])
