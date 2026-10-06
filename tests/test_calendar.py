from datetime import date

from dti import calendar


def test_thanksgiving_week():
    # Thu 11/26/26 is Thanksgiving; Fri 11/27 is a half-day.
    assert not calendar.is_trading_day(date(2026, 11, 26))
    assert calendar.next_trading_day(date(2026, 11, 25)) == date(2026, 11, 27)
    assert calendar.is_half_day(date(2026, 11, 27))
    assert not calendar.is_half_day(date(2026, 11, 25))


def test_weekend_rollover():
    # Fri 10/9/26 -> Mon 10/12/26 (Columbus Day: NYSE open)
    assert calendar.next_trading_day(date(2026, 10, 9)) == date(2026, 10, 12)
    assert calendar.prev_trading_day(date(2026, 10, 12)) == date(2026, 10, 9)


def test_trading_days_ahead_skips_holidays():
    days = calendar.trading_days_ahead(date(2026, 12, 23), 3)
    assert days == [date(2026, 12, 24), date(2026, 12, 28), date(2026, 12, 29)]
