from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from ..database import get_session
from ..models.common import Booking
from ..schemas.booking import BookingCreate, BookingResponse, BookingUpdate
from ..services.occupancy import check_capacity_warning
from ..utils.auth import get_current_user

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.get("/", response_model=List[Booking])
def list_bookings(session=Depends(get_session), current_user=Depends(get_current_user)):
    return session.exec(select(Booking)).all()


@router.post("/", response_model=BookingResponse)
def create_booking(data: BookingCreate, session=Depends(get_session), current_user=Depends(get_current_user)):
    booking = Booking(**data.dict())
    session.add(booking)
    session.commit()
    session.refresh(booking)
    warnings = check_capacity_warning(session, booking)
    return BookingResponse(**booking.dict(), warnings=warnings)


@router.put("/{booking_id}", response_model=BookingResponse)
def update_booking(booking_id: int, data: BookingUpdate, session=Depends(get_session), current_user=Depends(get_current_user)):
    booking = session.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(booking, key, value)
    booking.updated_at = datetime.utcnow()
    session.add(booking)
    session.commit()
    session.refresh(booking)
    warnings = check_capacity_warning(session, booking)
    return BookingResponse(**booking.dict(), warnings=warnings)


@router.delete("/{booking_id}")
def delete_booking(booking_id: int, session=Depends(get_session), current_user=Depends(get_current_user)):
    booking = session.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    session.delete(booking)
    session.commit()
    return {"ok": True}
