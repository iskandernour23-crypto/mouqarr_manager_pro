from __future__ import annotations

from typing import Iterable, List

from app.models.booking import BookingCreate


def parse_sheet_rows(rows: Iterable[dict]) -> List[BookingCreate]:
    bookings: List[BookingCreate] = []
    for row in rows:
        bookings.append(
            BookingCreate(
                kind=row.get("kind", "individual"),
                resident_id=row.get("resident_id"),
                guest_id=row.get("guest_id"),
                name=row.get("name", ""),
                org=row.get("org"),
                people_count=int(row.get("people_count", 1)),
                gender=row.get("gender", "male"),
                start_date=row.get("start_date"),
                end_date=row.get("end_date"),
                plan_type=row.get("plan_type"),
                amount=float(row.get("amount", 0)),
                status=row.get("status", "pending"),
                note=row.get("note"),
            )
        )
    return bookings
