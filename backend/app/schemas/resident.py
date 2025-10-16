from typing import Optional

from sqlmodel import SQLModel


class ResidentCreate(SQLModel):
    name: str
    gender: str
    national_id: Optional[str] = None
    phone: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    last_paid: Optional[str] = None
    due_day: Optional[int] = None
    interval_days: Optional[int] = None


class ResidentUpdate(SQLModel):
    name: Optional[str] = None
    gender: Optional[str] = None
    national_id: Optional[str] = None
    phone: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    last_paid: Optional[str] = None
    due_day: Optional[int] = None
    interval_days: Optional[int] = None
