from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.core.deps import get_session, require_role
from app.models.activity_log import ActivityLog

router = APIRouter(prefix="/logs", tags=["logs"], dependencies=[Depends(require_role("manager", "admin"))])


@router.get("/", response_model=List[ActivityLog])
def list_logs(session: Session = Depends(get_session)) -> List[ActivityLog]:
    return session.exec(select(ActivityLog)).all()
