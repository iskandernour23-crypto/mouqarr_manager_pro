from __future__ import annotations

from typing import Dict, List

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.core.deps import get_session, require_role
from app.models.setting import Setting

router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("/", response_model=Dict[str, str | None])
def get_settings_all(session: Session = Depends(get_session)) -> dict[str, str | None]:
    return {setting.key: setting.value for setting in session.exec(select(Setting)).all()}


@router.post(
    "/",
    response_model=Dict[str, str | None],
    dependencies=[Depends(require_role("admin"))],
)
def upsert_settings(payload: Dict[str, str], session: Session = Depends(get_session)) -> dict[str, str | None]:
    for key, value in payload.items():
        setting = session.get(Setting, key)
        if setting:
            setting.value = value
        else:
            session.add(Setting(key=key, value=value))
    session.commit()
    return {setting.key: setting.value for setting in session.exec(select(Setting)).all()}


@router.delete(
    "/",
    response_model=List[str],
    dependencies=[Depends(require_role("admin"))],
)
def delete_settings(keys: List[str], session: Session = Depends(get_session)) -> List[str]:
    for key in keys:
        setting = session.get(Setting, key)
        if setting:
            session.delete(setting)
    session.commit()
    return keys
