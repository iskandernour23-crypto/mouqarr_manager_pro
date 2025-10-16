from datetime import date
from typing import Optional

from sqlmodel import SQLModel


class PaymentCreate(SQLModel):
    resident_id: Optional[int] = None
    booking_id: Optional[int] = None
    amount: float
    paid_on: date
    method: str = "cash"


class PaymentRead(SQLModel):
    id: int
    resident_id: Optional[int] = None
    booking_id: Optional[int] = None
    amount: float
    paid_on: date
    method: str
    receipt_path: Optional[str] = None
