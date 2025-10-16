from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class ActivityLog(SQLModel, table=True):
    __tablename__ = "activity_logs"

    id: Optional[int] = Field(default=None, primary_key=True)
    actor: Optional[str] = None
    action: str
    entity: Optional[str] = None
    entity_id: Optional[int] = None
    at: datetime = Field(default_factory=datetime.utcnow)
    meta: Optional[str] = None
