from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.core.deps import get_session, require_role
from app.models.booking import Booking
from app.models.payment import Payment
from app.services.analytics import detect_anomalies, income_projection, occupancy_forecast

router = APIRouter(prefix="/analytics", tags=["analytics"], dependencies=[Depends(require_role("manager", "admin"))])


@router.get("/overview")
def analytics_overview(session: Session = Depends(get_session)) -> Dict[str, Any]:
    bookings = session.exec(select(Booking)).all()
    payments = session.exec(select(Payment)).all()
    return {
        "income": income_projection(payments),
        "occupancy_forecast": occupancy_forecast(bookings),
        "anomalies": [payment.id for payment in detect_anomalies(payments)],
    }
