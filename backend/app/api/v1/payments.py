from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlmodel import Session, select

from app.core.deps import get_session, require_role
from app.models.payment import Payment, PaymentCreate, PaymentRead, PaymentUpdate
from app.utils.receipts import generate_receipt

router = APIRouter(prefix="/payments", tags=["payments"])


@router.get("/", response_model=List[PaymentRead])
def list_payments(session: Session = Depends(get_session)) -> List[PaymentRead]:
    return session.exec(select(Payment)).all()


@router.post(
    "/",
    response_model=PaymentRead,
    dependencies=[Depends(require_role("manager", "admin"))],
)
def create_payment(payment_in: PaymentCreate, session: Session = Depends(get_session)) -> Payment:
    payment = Payment.from_orm(payment_in)
    session.add(payment)
    session.commit()
    session.refresh(payment)
    return payment


@router.get("/{payment_id}", response_model=PaymentRead)
def get_payment(payment_id: int, session: Session = Depends(get_session)) -> Payment:
    payment = session.get(Payment, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="NOT_FOUND")
    return payment


@router.put(
    "/{payment_id}",
    response_model=PaymentRead,
    dependencies=[Depends(require_role("manager", "admin"))],
)
def update_payment(
    payment_id: int, payment_in: PaymentUpdate, session: Session = Depends(get_session)
) -> Payment:
    payment = session.get(Payment, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="NOT_FOUND")
    for key, value in payment_in.dict(exclude_unset=True).items():
        setattr(payment, key, value)
    session.add(payment)
    session.commit()
    session.refresh(payment)
    return payment


@router.delete(
    "/{payment_id}", dependencies=[Depends(require_role("manager", "admin"))]
)
def delete_payment(payment_id: int, session: Session = Depends(get_session)) -> dict[str, str]:
    payment = session.get(Payment, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="NOT_FOUND")
    session.delete(payment)
    session.commit()
    return {"status": "deleted"}


@router.get("/{payment_id}/receipt")
def download_receipt(payment_id: int, session: Session = Depends(get_session)) -> StreamingResponse:
    payment = session.get(Payment, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="NOT_FOUND")
    payload = {
        "رقم الإيصال": payment.receipt_no or str(payment.id),
        "المبلغ": f"{payment.amount:.2f}",
        "التاريخ": payment.paid_on.isoformat(),
        "الملاحظة": payment.note or "",
    }
    pdf_bytes = generate_receipt(payload)
    return StreamingResponse(iter([pdf_bytes]), media_type="application/pdf")
