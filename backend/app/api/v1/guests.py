from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.core.deps import get_session, require_role
from app.models.guest import Guest, GuestCreate, GuestRead, GuestUpdate
from app.utils.crypto import decrypt, encrypt

router = APIRouter(prefix="/guests", tags=["guests"])


@router.get("/", response_model=List[GuestRead])
def list_guests(session: Session = Depends(get_session)) -> List[GuestRead]:
    guests = session.exec(select(Guest)).all()
    for guest in guests:
        guest.phone_encrypted = decrypt(guest.phone_encrypted)
    return guests


@router.post("/", response_model=GuestRead, dependencies=[Depends(require_role("manager", "admin"))])
def create_guest(guest_in: GuestCreate, session: Session = Depends(get_session)) -> Guest:
    guest = Guest.from_orm(guest_in)
    guest.phone_encrypted = encrypt(guest_in.phone_encrypted)
    session.add(guest)
    session.commit()
    session.refresh(guest)
    guest.phone_encrypted = decrypt(guest.phone_encrypted)
    return guest


@router.get("/{guest_id}", response_model=GuestRead)
def get_guest(guest_id: int, session: Session = Depends(get_session)) -> Guest:
    guest = session.get(Guest, guest_id)
    if not guest:
        raise HTTPException(status_code=404, detail="NOT_FOUND")
    guest.phone_encrypted = decrypt(guest.phone_encrypted)
    return guest


@router.put("/{guest_id}", response_model=GuestRead, dependencies=[Depends(require_role("manager", "admin"))])
def update_guest(guest_id: int, guest_in: GuestUpdate, session: Session = Depends(get_session)) -> Guest:
    guest = session.get(Guest, guest_id)
    if not guest:
        raise HTTPException(status_code=404, detail="NOT_FOUND")
    data = guest_in.dict(exclude_unset=True, by_alias=True)
    if "phone" in data:
        guest.phone_encrypted = encrypt(data.pop("phone"))
    for key, value in data.items():
        setattr(guest, key, value)
    session.add(guest)
    session.commit()
    session.refresh(guest)
    guest.phone_encrypted = decrypt(guest.phone_encrypted)
    return guest


@router.delete("/{guest_id}", dependencies=[Depends(require_role("admin"))])
def delete_guest(guest_id: int, session: Session = Depends(get_session)) -> dict[str, str]:
    guest = session.get(Guest, guest_id)
    if not guest:
        raise HTTPException(status_code=404, detail="NOT_FOUND")
    session.delete(guest)
    session.commit()
    return {"status": "deleted"}
