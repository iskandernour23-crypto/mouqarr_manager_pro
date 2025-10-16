from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from typing import Iterable

from app.core.config import get_settings
from app.models.booking import Booking

settings = get_settings()


def get_capacity() -> dict[str, int]:
    return {
        "male": int(settings.__dict__.get("capacity_males", 20) or 20),
        "female": int(settings.__dict__.get("capacity_females", 50) or 50),
    }


@dataclass
class OccupancySnapshot:
    gender: str
    count: int
    capacity: int
    over_capacity: bool


def calculate_daily(bookings: Iterable[Booking], target_date: date) -> list[OccupancySnapshot]:
    totals: dict[str, int] = defaultdict(int)
    for booking in bookings:
        if booking.start_date <= target_date <= booking.end_date:
            totals[booking.gender] += booking.people_count
    capacity = get_capacity()
    snapshots = []
    for gender in ("male", "female"):
        cap = capacity.get(gender, 0)
        count = totals.get(gender, 0)
        snapshots.append(
            OccupancySnapshot(
                gender=gender,
                count=count,
                capacity=cap,
                over_capacity=count > cap,
            )
        )
    return snapshots
