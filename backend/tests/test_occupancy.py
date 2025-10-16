from datetime import date

from sqlmodel import Session, delete

from app.database import engine, init_db
from app.models.common import Booking
from app.services.occupancy import occupancy_on


def setup_module(module):
    init_db()
    with Session(engine) as session:
        session.exec(delete(Booking))
        session.commit()
        session.add(Booking(start_date=date(2024, 1, 1), end_date=date(2024, 1, 10), people_count=5, gender="male"))
        session.add(Booking(start_date=date(2024, 1, 5), end_date=date(2024, 1, 7), people_count=3, gender="female"))
        session.commit()


def test_occupancy_on_day():
    with Session(engine) as session:
        result = occupancy_on(session, date(2024, 1, 6))
        assert result["male"] == 5
        assert result["female"] == 3
