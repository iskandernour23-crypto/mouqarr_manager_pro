from __future__ import annotations

from datetime import date

from app.services.due_dates import DueDateService, PLAN_MONTHLY


def test_due_date_classification_overdue():
    service = DueDateService()
    status = service.compute(PLAN_MONTHLY, date(2024, 1, 1), date(2024, 2, 1), None, 28, today=date(2024, 3, 5))
    assert status.status_label == "متأخر"
    assert status.next_due.day == 28
