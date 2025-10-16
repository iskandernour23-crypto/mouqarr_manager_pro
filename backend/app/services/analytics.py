from __future__ import annotations

from datetime import date
from statistics import mean
from typing import Iterable

from app.models.booking import Booking
from app.models.payment import Payment


def income_projection(payments: Iterable[Payment]) -> dict[str, float]:
    by_plan: dict[str, list[float]] = {}
    for payment in payments:
        plan = getattr(payment, "plan_type", None) or "عام"
        by_plan.setdefault(plan, []).append(payment.amount)
    return {plan: sum(amounts) for plan, amounts in by_plan.items()}


def occupancy_forecast(bookings: Iterable[Booking], horizon_days: int = 30) -> list[dict[str, float]]:
    today = date.today()
    result: list[dict[str, float]] = []
    counts = [booking.people_count for booking in bookings]
    baseline = mean(counts) if counts else 0
    for day in range(horizon_days):
        result.append(
            {
                "date": (today.toordinal() + day),
                "occupancy": baseline,
                "confidence_low": max(baseline - 2, 0),
                "confidence_high": baseline + 2,
            }
        )
    return result


def detect_anomalies(payments: Iterable[Payment]) -> list[Payment]:
    amounts = [payment.amount for payment in payments]
    if not amounts:
        return []
    avg = mean(amounts)
    threshold = avg * 2
    return [payment for payment in payments if payment.amount > threshold]
