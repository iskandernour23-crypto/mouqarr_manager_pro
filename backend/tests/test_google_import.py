from sqlmodel import Session, delete, select

from app.database import engine, init_db
from app.models.common import Guest
from app.services.importers import upsert_guests_from_rows


def setup_module(module):
    init_db()
    with Session(engine) as session:
        session.exec(delete(Guest))
        session.commit()


def test_upsert_guests():
    rows = [["أحمد", "male"], ["ليلى", "female"], ["أحمد", "male"]]
    with Session(engine) as session:
        inserted = upsert_guests_from_rows(session, rows)
        assert inserted == 2
        guests = session.exec(select(Guest)).all()
        assert len(guests) == 2
