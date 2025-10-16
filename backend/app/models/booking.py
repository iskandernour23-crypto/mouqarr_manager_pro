from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import AuditMixin, TimeStampedModel


class BookingBase(SQLModel):
    kind: str = Field(default="individual")
    resident_id: Optional[int] = Field(default=None, foreign_key="residents.id")
    guest_id: Optional[int] = Field(default=None, foreign_key="guests.id")
    name: str
    org: Optional[str] = Field(default=None)
    people_count: int = Field(default=1)
    gender: str = Field(default="male")
    start_date: date
    end_date: date
    plan_type: Optional[str] = Field(default=None)
    amount: float = 0
    status: str = Field(default="active")
    note: Optional[str] = Field(default=None)


class Booking(BookingBase, TimeStampedModel, AuditMixin, table=True):
    __tablename__ = "bookings"

    id: Optional[int] = Field(default=None, primary_key=True)
    resident: Optional["Resident"] = Relationship(back_populates="bookings")
    guest: Optional["Guest"] = Relationship(back_populates="bookings")
    payments: list["Payment"] = Relationship(back_populates="booking")


class BookingCreate(BookingBase):
    pass


class BookingRead(BookingBase):
    id: int
    created_at: datetime
    updated_at: datetime | None


class BookingUpdate(SQLModel):
    kind: Optional[str] = None
    resident_id: Optional[int] = None
    guest_id: Optional[int] = None
    name: Optional[str] = None
    org: Optional[str] = None
    people_count: Optional[int] = None
    gender: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    plan_type: Optional[str] = None
    amount: Optional[float] = None
    status: Optional[str] = None
    note: Optional[str] = None
