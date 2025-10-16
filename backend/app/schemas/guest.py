from typing import Optional

from sqlmodel import SQLModel


class GuestCreate(SQLModel):
    name: str
    gender: str
    phone: Optional[str] = None


class GuestUpdate(SQLModel):
    name: Optional[str] = None
    gender: Optional[str] = None
    phone: Optional[str] = None
