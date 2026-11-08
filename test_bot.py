from datetime import datetime, timezone

from bot import countdown_text, parse_release_date


def test_parse_release_date_normalizes_utc():
    assert parse_release_date("2026-11-19T01:00:00+01:00") == datetime(2026, 11, 19, tzinfo=timezone.utc)


def test_countdown_text():
    now = datetime(2026, 11, 18, 23, 59, 0, tzinfo=timezone.utc)
    assert countdown_text(now) == "0 days, 0 hours, 1 minutes, and 0 seconds"


def test_countdown_after_release():
    now = datetime(2026, 11, 20, tzinfo=timezone.utc)
    assert countdown_text(now) == "GTA 6 is out now! 🎉"
