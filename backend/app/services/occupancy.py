from datetime import date, timedelta
from typing import Dict

from sqlmodel import Session, func, select

from ..core.config import get_settings
from ..models.common import Booking

settings = get_settings()


def occupancy_on(session: Session, target_date: date) -> Dict[str, int]:
    result = session.exec(
        select(Booking.gender, func.sum(Booking.people_count))
        .where(Booking.start_date <= target_date, Booking.end_date >= target_date)
        .group_by(Booking.gender)
    ).all()
    data = {"male": 0, "female": 0}
    for gender, count in result:
        if gender and gender.lower().startswith("m"):
            data["male"] = int(count or 0)
        elif gender and gender.lower().startswith("f"):
            data["female"] = int(count or 0)
    return data


def check_capacity_warning(session: Session, booking: Booking) -> Dict[str, bool]:
    warnings: Dict[str, bool] = {"capacity": False}
    for day in range((booking.end_date - booking.start_date).days + 1):
        day_date = booking.start_date + timedelta(days=day)
        occ = occupancy_on(session, day_date)
        if booking.gender and booking.gender.lower().startswith("m"):
            occ["male"] += booking.people_count
            if occ["male"] > settings.capacity_males:
                warnings["capacity"] = True
        elif booking.gender and booking.gender.lower().startswith("f"):
            occ["female"] += booking.people_count
            if occ["female"] > settings.capacity_females:
                warnings["capacity"] = True
    return warnings
