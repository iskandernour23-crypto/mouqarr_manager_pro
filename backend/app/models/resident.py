from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import AuditMixin, TimeStampedModel


class ResidentBase(SQLModel):
    name: str = Field(index=True)
    status: str = Field(default="active", index=True)
    start_date: date
    plan_type: str = Field(default="شهري")
    amount: float
    due_day: Optional[int] = Field(default=None)
    interval_days: Optional[int] = Field(default=None)
    last_paid_date: Optional[date] = Field(default=None)
    phone_encrypted: Optional[str] = Field(default=None, alias="phone")
    note: Optional[str] = Field(default=None)


class Resident(ResidentBase, TimeStampedModel, AuditMixin, table=True):
    __tablename__ = "residents"

    id: Optional[int] = Field(default=None, primary_key=True)
    bookings: list["Booking"] = Relationship(back_populates="resident")
    payments: list["Payment"] = Relationship(back_populates="resident")


class ResidentCreate(ResidentBase):
    pass


class ResidentRead(ResidentBase):
    id: int
    created_at: datetime
    updated_at: datetime | None


class ResidentUpdate(SQLModel):
    name: Optional[str] = None
    status: Optional[str] = None
    start_date: Optional[date] = None
    plan_type: Optional[str] = None
    amount: Optional[float] = None
    due_day: Optional[int] = None
    interval_days: Optional[int] = None
    last_paid_date: Optional[date] = None
    phone: Optional[str] = Field(default=None, alias="phone")
    note: Optional[str] = None
