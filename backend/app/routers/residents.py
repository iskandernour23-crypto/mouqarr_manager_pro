from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from ..database import get_session
from ..models.common import Resident
from ..schemas.resident import ResidentCreate, ResidentUpdate
from ..utils.auth import get_current_user

router = APIRouter(prefix="/residents", tags=["residents"])


@router.get("/", response_model=List[Resident])
def list_residents(session=Depends(get_session), current_user=Depends(get_current_user)):
    return session.exec(select(Resident)).all()


@router.post("/", response_model=Resident)
def create_resident(data: ResidentCreate, session=Depends(get_session), current_user=Depends(get_current_user)):
    resident = Resident(**data.dict())
    session.add(resident)
    session.commit()
    session.refresh(resident)
    return resident


@router.get("/{resident_id}", response_model=Resident)
def get_resident(resident_id: int, session=Depends(get_session), current_user=Depends(get_current_user)):
    resident = session.get(Resident, resident_id)
    if not resident:
        raise HTTPException(status_code=404, detail="Resident not found")
    return resident


@router.put("/{resident_id}", response_model=Resident)
def update_resident(resident_id: int, data: ResidentUpdate, session=Depends(get_session), current_user=Depends(get_current_user)):
    resident = session.get(Resident, resident_id)
    if not resident:
        raise HTTPException(status_code=404, detail="Resident not found")
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(resident, key, value)
    resident.updated_at = datetime.utcnow()
    session.add(resident)
    session.commit()
    session.refresh(resident)
    return resident


@router.delete("/{resident_id}")
def delete_resident(resident_id: int, session=Depends(get_session), current_user=Depends(get_current_user)):
    resident = session.get(Resident, resident_id)
    if not resident:
        raise HTTPException(status_code=404, detail="Resident not found")
    session.delete(resident)
    session.commit()
    return {"ok": True}
