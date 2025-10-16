from datetime import date, datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class TimestampMixin(SQLModel):
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class ResidentBase(SQLModel):
    name: str
    gender: str
    national_id: Optional[str] = None
    phone: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    last_paid: Optional[date] = None
    due_day: Optional[int] = None
    interval_days: Optional[int] = None


class Resident(ResidentBase, TimestampMixin, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class GuestBase(SQLModel):
    name: str
    gender: str
    phone: Optional[str] = None


class Guest(GuestBase, TimestampMixin, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class Bed(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    label: str
    resident_id: Optional[int] = Field(default=None, foreign_key="resident.id")


class BookingBase(SQLModel):
    resident_id: Optional[int] = Field(default=None, foreign_key="resident.id")
    guest_id: Optional[int] = Field(default=None, foreign_key="guest.id")
    start_date: date
    end_date: date
    people_count: int = 1
    gender: Optional[str] = None
    status: str = Field(default="confirmed")


class Booking(BookingBase, TimestampMixin, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class PaymentBase(SQLModel):
    resident_id: Optional[int] = Field(default=None, foreign_key="resident.id")
    booking_id: Optional[int] = Field(default=None, foreign_key="booking.id")
    amount: float
    paid_on: date
    method: str = "cash"
    receipt_path: Optional[str] = None


class Payment(PaymentBase, TimestampMixin, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class Setting(SQLModel, table=True):
    key: str = Field(primary_key=True)
    value: str


class UserBase(SQLModel):
    username: str
    full_name: Optional[str] = None
    role: str = Field(default="user")


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
