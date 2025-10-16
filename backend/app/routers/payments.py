from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlmodel import select

from ..database import get_session
from ..models.common import Payment, Resident
from ..schemas.payment import PaymentCreate, PaymentRead
from ..services.pdf import generate_receipt
from ..utils.auth import get_current_user

router = APIRouter(prefix="/payments", tags=["payments"])


def to_read(payment: Payment) -> PaymentRead:
    return PaymentRead(**payment.dict(exclude={"created_at", "updated_at"}))


@router.get("/", response_model=List[PaymentRead])
def list_payments(session=Depends(get_session), current_user=Depends(get_current_user)):
    payments = session.exec(select(Payment)).all()
    return [to_read(payment) for payment in payments]


@router.post("/", response_model=PaymentRead)
def create_payment(data: PaymentCreate, session=Depends(get_session), current_user=Depends(get_current_user)):
    payment = Payment(**data.dict())
    session.add(payment)
    session.commit()
    session.refresh(payment)
    resident = session.get(Resident, payment.resident_id) if payment.resident_id else None
    receipt_path = generate_receipt(payment, resident_name=resident.name if resident else None)
    payment.receipt_path = str(receipt_path)
    session.add(payment)
    session.commit()
    session.refresh(payment)
    return to_read(payment)


@router.get("/{payment_id}/receipt")
def download_receipt(payment_id: int, session=Depends(get_session), current_user=Depends(get_current_user)):
    payment = session.get(Payment, payment_id)
    if not payment or not payment.receipt_path:
        raise HTTPException(status_code=404, detail="Receipt not available")
    return FileResponse(payment.receipt_path, filename=f"receipt_{payment_id}.pdf")
