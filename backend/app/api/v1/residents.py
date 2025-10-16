from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.core.deps import get_session, require_role
from app.models.resident import Resident, ResidentCreate, ResidentRead, ResidentUpdate
from app.utils.crypto import decrypt, encrypt

router = APIRouter(prefix="/residents", tags=["residents"])


@router.get("/", response_model=List[ResidentRead])
def list_residents(session: Session = Depends(get_session)) -> List[ResidentRead]:
    residents = session.exec(select(Resident)).all()
    for resident in residents:
        resident.phone_encrypted = decrypt(resident.phone_encrypted)
    return residents


@router.post("/", response_model=ResidentRead, dependencies=[Depends(require_role("manager", "admin"))])
def create_resident(resident_in: ResidentCreate, session: Session = Depends(get_session)) -> Resident:
    resident = Resident.from_orm(resident_in)
    resident.phone_encrypted = encrypt(resident_in.phone_encrypted)
    session.add(resident)
    session.commit()
    session.refresh(resident)
    resident.phone_encrypted = decrypt(resident.phone_encrypted)
    return resident


@router.get("/{resident_id}", response_model=ResidentRead)
def get_resident(resident_id: int, session: Session = Depends(get_session)) -> Resident:
    resident = session.get(Resident, resident_id)
    if not resident:
        raise HTTPException(status_code=404, detail="NOT_FOUND")
    resident.phone_encrypted = decrypt(resident.phone_encrypted)
    return resident


@router.put("/{resident_id}", response_model=ResidentRead, dependencies=[Depends(require_role("manager", "admin"))])
def update_resident(resident_id: int, resident_in: ResidentUpdate, session: Session = Depends(get_session)) -> Resident:
    resident = session.get(Resident, resident_id)
    if not resident:
        raise HTTPException(status_code=404, detail="NOT_FOUND")
    update_data = resident_in.dict(exclude_unset=True, by_alias=True)
    if "phone" in update_data:
        resident.phone_encrypted = encrypt(update_data.pop("phone"))
    for key, value in update_data.items():
        setattr(resident, key, value)
    session.add(resident)
    session.commit()
    session.refresh(resident)
    resident.phone_encrypted = decrypt(resident.phone_encrypted)
    return resident


@router.delete("/{resident_id}", dependencies=[Depends(require_role("admin"))])
def delete_resident(resident_id: int, session: Session = Depends(get_session)) -> dict[str, str]:
    resident = session.get(Resident, resident_id)
    if not resident:
        raise HTTPException(status_code=404, detail="NOT_FOUND")
    session.delete(resident)
    session.commit()
    return {"status": "deleted"}
