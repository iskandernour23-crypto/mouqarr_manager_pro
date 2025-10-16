from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class TimeStampedModel(SQLModel):
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime | None = Field(default=None, nullable=True)


class AuditMixin(SQLModel):
    created_by: Optional[str] = Field(default=None, foreign_key="users.username")
    updated_by: Optional[str] = Field(default=None, foreign_key="users.username")
