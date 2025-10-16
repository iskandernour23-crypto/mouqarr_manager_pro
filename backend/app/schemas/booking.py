from datetime import date
from typing import Optional

from sqlmodel import SQLModel

from ..models.common import Booking


class BookingCreate(SQLModel):
    resident_id: Optional[int] = None
    guest_id: Optional[int] = None
    start_date: date
    end_date: date
    people_count: int = 1
    gender: Optional[str] = None
    status: str = "confirmed"


class BookingUpdate(SQLModel):
    resident_id: Optional[int] = None
    guest_id: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    people_count: Optional[int] = None
    gender: Optional[str] = None
    status: Optional[str] = None


class BookingResponse(Booking, SQLModel):
    warnings: Optional[dict] = None
