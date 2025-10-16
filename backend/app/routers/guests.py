from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from ..database import get_session
from ..models.common import Guest
from ..schemas.guest import GuestCreate, GuestUpdate
from ..utils.auth import get_current_user

router = APIRouter(prefix="/guests", tags=["guests"])


@router.get("/", response_model=List[Guest])
def list_guests(session=Depends(get_session), current_user=Depends(get_current_user)):
    return session.exec(select(Guest)).all()


@router.post("/", response_model=Guest)
def create_guest(data: GuestCreate, session=Depends(get_session), current_user=Depends(get_current_user)):
    guest = Guest(**data.dict())
    session.add(guest)
    session.commit()
    session.refresh(guest)
    return guest


@router.put("/{guest_id}", response_model=Guest)
def update_guest(guest_id: int, data: GuestUpdate, session=Depends(get_session), current_user=Depends(get_current_user)):
    guest = session.get(Guest, guest_id)
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(guest, key, value)
    guest.updated_at = datetime.utcnow()
    session.add(guest)
    session.commit()
    session.refresh(guest)
    return guest


@router.delete("/{guest_id}")
def delete_guest(guest_id: int, session=Depends(get_session), current_user=Depends(get_current_user)):
    guest = session.get(Guest, guest_id)
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")
    session.delete(guest)
    session.commit()
    return {"ok": True}
