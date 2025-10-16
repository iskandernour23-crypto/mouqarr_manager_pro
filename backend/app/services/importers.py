from typing import Sequence

from sqlmodel import Session, select

from ..models.common import Guest


def upsert_guests_from_rows(session: Session, rows: Sequence[Sequence[str]]) -> int:
    """Insert guests from Google Sheets rows, skipping existing names."""
    inserted = 0
    for row in rows:
        if not row or not row[0]:
            continue
        name = row[0]
        gender = row[1] if len(row) > 1 else ""
        exists = session.exec(select(Guest).where(Guest.name == name)).first()
        if exists:
            continue
        guest = Guest(name=name, gender=gender)
        session.add(guest)
        inserted += 1
    session.commit()
    return inserted
