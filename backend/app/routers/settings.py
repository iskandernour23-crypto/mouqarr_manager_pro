from typing import Dict

from fastapi import APIRouter, Depends
from sqlmodel import select

from ..database import get_session
from ..models.common import Setting
from ..utils.auth import require_admin

router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("/")
def list_settings(session=Depends(get_session), current_user=Depends(require_admin)) -> Dict[str, str]:
    settings = session.exec(select(Setting)).all()
    return {item.key: item.value for item in settings}


@router.post("/")
def upsert_settings(data: Dict[str, str], session=Depends(get_session), current_user=Depends(require_admin)):
    for key, value in data.items():
        setting = session.get(Setting, key)
        if setting:
            setting.value = value
            session.add(setting)
        else:
            session.add(Setting(key=key, value=value))
    session.commit()
    return {"ok": True}
