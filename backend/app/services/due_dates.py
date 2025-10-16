from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Optional

from app.core.config import get_settings

settings = get_settings()


@dataclass
class DueStatus:
    next_due: date
    status_label: str
    days_remaining: int


PLAN_MONTHLY = "شهري"
PLAN_SEMI = "نصف شهري"
PLAN_DAILY = "يومي"


class DueDateService:
    def __init__(self, clamp_to_28: bool = True, default_interval: int = 30) -> None:
        self.clamp_to_28 = clamp_to_28
        self.default_interval = default_interval

    def next_due(self, plan_type: str, start_date: date, last_paid: Optional[date], interval_days: Optional[int], due_day: Optional[int]) -> date:
        base_date = last_paid or start_date
        if plan_type == PLAN_MONTHLY:
            month = base_date.month + 1
            year = base_date.year + (month - 1) // 12
            month = (month - 1) % 12 + 1
            day = due_day or base_date.day
            if self.clamp_to_28:
                day = min(day, 28)
            try:
                return date(year, month, day)
            except ValueError:
                # fallback for months with fewer days
                return date(year, month, 28)
        interval = interval_days or self.default_interval
        return base_date + timedelta(days=interval)

    def classify(self, due_date: date, today: Optional[date] = None) -> DueStatus:
        today = today or date.today()
        delta = (due_date - today).days
        if delta < 0:
            label = "متأخر"
        elif delta == 0:
            label = "اليوم"
        elif delta <= 7:
            label = "خلال ٧ أيام"
        else:
            label = "لاحقاً"
        return DueStatus(next_due=due_date, status_label=label, days_remaining=delta)

    def compute(self, plan_type: str, start_date: date, last_paid: Optional[date], interval_days: Optional[int], due_day: Optional[int], today: Optional[date] = None) -> DueStatus:
        next_due = self.next_due(plan_type, start_date, last_paid, interval_days, due_day)
        return self.classify(next_due, today=today)


def get_due_service() -> DueDateService:
    clamp = settings.clamp_monthly_to_28
    default_interval = settings.default_interval_days
    return DueDateService(clamp_to_28=clamp, default_interval=default_interval)
