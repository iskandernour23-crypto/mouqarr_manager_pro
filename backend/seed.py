from datetime import date, timedelta

from sqlmodel import Session, delete

from app.database import engine, init_db
from app.models.common import Booking, Guest, Payment, Resident


def run():
    init_db()
    with Session(engine) as session:
        session.exec(delete(Booking))
        session.exec(delete(Payment))
        session.exec(delete(Resident))
        session.exec(delete(Guest))
        session.commit()

        resident = Resident(name="محمد علي", gender="male", start_date=date.today(), due_day=15, interval_days=30)
        session.add(resident)
        session.commit()
        session.refresh(resident)

        guest = Guest(name="جمعية الرفاه", gender="female")
        session.add(guest)
        session.commit()
        session.refresh(guest)

        booking = Booking(
            resident_id=resident.id,
            guest_id=guest.id,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=3),
            people_count=10,
            gender="female",
        )
        session.add(booking)

        payment = Payment(resident_id=resident.id, amount=500.0, paid_on=date.today(), method="cash")
        session.add(payment)

        session.commit()


if __name__ == "__main__":
    run()
