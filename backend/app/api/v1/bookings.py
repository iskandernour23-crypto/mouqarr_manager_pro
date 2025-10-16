from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.core.deps import get_session, require_role
from app.models.booking import Booking, BookingCreate, BookingRead, BookingUpdate

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.get("/", response_model=List[BookingRead])
def list_bookings(session: Session = Depends(get_session)) -> List[BookingRead]:
    return session.exec(select(Booking)).all()


@router.post(
    "/",
    response_model=BookingRead,
    dependencies=[Depends(require_role("manager", "admin"))],
)
def create_booking(booking_in: BookingCreate, session: Session = Depends(get_session)) -> Booking:
    booking = Booking.from_orm(booking_in)
    session.add(booking)
    session.commit()
    session.refresh(booking)
    return booking


@router.get("/{booking_id}", response_model=BookingRead)
def get_booking(booking_id: int, session: Session = Depends(get_session)) -> Booking:
    booking = session.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="NOT_FOUND")
    return booking


@router.put(
    "/{booking_id}",
    response_model=BookingRead,
    dependencies=[Depends(require_role("manager", "admin"))],
)
def update_booking(
    booking_id: int, booking_in: BookingUpdate, session: Session = Depends(get_session)
) -> Booking:
    booking = session.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="NOT_FOUND")
    for key, value in booking_in.dict(exclude_unset=True).items():
        setattr(booking, key, value)
    session.add(booking)
    session.commit()
    session.refresh(booking)
    return booking


@router.delete(
    "/{booking_id}", dependencies=[Depends(require_role("manager", "admin"))]
)
def delete_booking(booking_id: int, session: Session = Depends(get_session)) -> dict[str, str]:
    booking = session.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="NOT_FOUND")
    session.delete(booking)
    session.commit()
    return {"status": "deleted"}
