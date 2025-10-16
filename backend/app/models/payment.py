from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import AuditMixin, TimeStampedModel


class PaymentBase(SQLModel):
    subject_type: str = Field(default="resident")
    subject_id: int
    amount: float
    paid_on: date
    method: str = Field(default="cash")
    note: Optional[str] = Field(default=None)
    receipt_no: Optional[str] = Field(default=None)


class Payment(PaymentBase, TimeStampedModel, AuditMixin, table=True):
    __tablename__ = "payments"

    id: Optional[int] = Field(default=None, primary_key=True)
    resident_id: Optional[int] = Field(default=None, foreign_key="residents.id")
    guest_id: Optional[int] = Field(default=None, foreign_key="guests.id")
    booking_id: Optional[int] = Field(default=None, foreign_key="bookings.id")
    resident: Optional["Resident"] = Relationship(back_populates="payments")
    guest: Optional["Guest"] = Relationship(back_populates="payments")
    booking: Optional["Booking"] = Relationship(back_populates="payments")


class PaymentCreate(PaymentBase):
    pass


class PaymentRead(PaymentBase):
    id: int
    created_at: datetime
    updated_at: datetime | None


class PaymentUpdate(SQLModel):
    subject_type: Optional[str] = None
    subject_id: Optional[int] = None
    amount: Optional[float] = None
    paid_on: Optional[date] = None
    method: Optional[str] = None
    note: Optional[str] = None
    receipt_no: Optional[str] = None
