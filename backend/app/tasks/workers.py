from __future__ import annotations

from datetime import date
from typing import Iterable

from sqlmodel import select

from app.core.config import get_settings
from app.db.session import session_scope
from app.models.payment import Payment
from app.models.resident import Resident
from app.services.due_dates import DueDateService

settings = get_settings()

due_service = DueDateService()


def _collect_residents() -> Iterable[Resident]:
    with session_scope() as session:
        return session.exec(select(Resident)).all()


def notify(channel: str, message: str) -> None:
    if channel == "telegram" and settings.telegram_bot and settings.telegram_chat_id:
        # placeholder for telegram integration
        pass


def check_due_dates() -> None:
    residents = _collect_residents()
    today = date.today()
    for resident in residents:
        status = due_service.compute(
            plan_type=resident.plan_type,
            start_date=resident.start_date,
            last_paid=resident.last_paid_date,
            interval_days=resident.interval_days,
            due_day=resident.due_day,
            today=today,
        )
        if status.status_label == "متأخر":
            notify("telegram", f"{resident.name} متأخر")


def weekly_digest() -> None:
    notify("telegram", "تقرير أسبوعي جاهز")


def upcoming_due_alerts() -> None:
    residents = _collect_residents()
    today = date.today()
    for resident in residents:
        status = due_service.compute(
            resident.plan_type,
            resident.start_date,
            resident.last_paid_date,
            resident.interval_days,
            resident.due_day,
            today,
        )
        if status.status_label == "خلال ٧ أيام":
            notify("telegram", f"{resident.name} يستحق الدفع خلال أسبوع")


def sync_payments() -> list[Payment]:
    with session_scope() as session:
        return session.exec(select(Payment)).all()
