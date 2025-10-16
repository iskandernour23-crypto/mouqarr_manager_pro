from __future__ import annotations

from datetime import date

from app.services.google_import import parse_sheet_rows


def test_parse_sheet_rows():
    rows = [
        {
            "name": "ضيف",
            "start_date": date.today(),
            "end_date": date.today(),
            "people_count": 3,
        }
    ]
    bookings = parse_sheet_rows(rows)
    assert bookings[0].name == "ضيف"
    assert bookings[0].people_count == 3
