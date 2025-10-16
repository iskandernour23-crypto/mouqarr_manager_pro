from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

from app.models.base import TimeStampedModel


class UserBase(SQLModel):
    username: str = Field(index=True)
    role: str = Field(default="viewer")


class User(UserBase, TimeStampedModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    pw_hash: str
    last_login_at: Optional[datetime] = None


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime | None
    last_login_at: datetime | None


class UserUpdate(SQLModel):
    role: Optional[str] = None
    password: Optional[str] = None
