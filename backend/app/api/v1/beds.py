from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.core.deps import get_session, require_role
from app.models.bed import Bed, BedCreate, BedRead, BedUpdate

router = APIRouter(prefix="/beds", tags=["beds"])


@router.get("/", response_model=List[BedRead])
def list_beds(session: Session = Depends(get_session)) -> List[BedRead]:
    return session.exec(select(Bed)).all()


@router.post(
    "/",
    response_model=BedRead,
    dependencies=[Depends(require_role("manager", "admin"))],
)
def create_bed(bed_in: BedCreate, session: Session = Depends(get_session)) -> Bed:
    bed = Bed.from_orm(bed_in)
    session.add(bed)
    session.commit()
    session.refresh(bed)
    return bed


@router.put(
    "/{bed_id}",
    response_model=BedRead,
    dependencies=[Depends(require_role("manager", "admin"))],
)
def update_bed(bed_id: int, bed_in: BedUpdate, session: Session = Depends(get_session)) -> Bed:
    bed = session.get(Bed, bed_id)
    if not bed:
        raise HTTPException(status_code=404, detail="NOT_FOUND")
    for key, value in bed_in.dict(exclude_unset=True).items():
        setattr(bed, key, value)
    session.add(bed)
    session.commit()
    session.refresh(bed)
    return bed


@router.delete(
    "/{bed_id}", dependencies=[Depends(require_role("manager", "admin"))]
)
def delete_bed(bed_id: int, session: Session = Depends(get_session)) -> dict[str, str]:
    bed = session.get(Bed, bed_id)
    if not bed:
        raise HTTPException(status_code=404, detail="NOT_FOUND")
    session.delete(bed)
    session.commit()
    return {"status": "deleted"}
