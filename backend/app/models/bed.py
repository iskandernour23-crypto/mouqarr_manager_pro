from __future__ import annotations

from typing import Optional

from sqlmodel import Field, SQLModel

from app.models.base import AuditMixin, TimeStampedModel


class BedBase(SQLModel):
    label: str
    gender: str = Field(default="male")


class Bed(BedBase, TimeStampedModel, AuditMixin, table=True):
    __tablename__ = "beds"

    id: Optional[int] = Field(default=None, primary_key=True)


class BedCreate(BedBase):
    pass


class BedRead(BedBase):
    id: int


class BedUpdate(SQLModel):
    label: Optional[str] = None
    gender: Optional[str] = None
