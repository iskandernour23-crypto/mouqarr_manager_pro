from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import AuditMixin, TimeStampedModel


class GuestBase(SQLModel):
    name: str
    org: Optional[str] = Field(default=None)
    phone_encrypted: Optional[str] = Field(default=None, alias="phone")
    note: Optional[str] = Field(default=None)


class Guest(GuestBase, TimeStampedModel, AuditMixin, table=True):
    __tablename__ = "guests"

    id: Optional[int] = Field(default=None, primary_key=True)
    bookings: list["Booking"] = Relationship(back_populates="guest")
    payments: list["Payment"] = Relationship(back_populates="guest")


class GuestCreate(GuestBase):
    pass


class GuestRead(GuestBase):
    id: int
    created_at: datetime
    updated_at: datetime | None


class GuestUpdate(SQLModel):
    name: Optional[str] = None
    org: Optional[str] = None
    phone: Optional[str] = Field(default=None, alias="phone")
    note: Optional[str] = None
