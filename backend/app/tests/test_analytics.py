from __future__ import annotations

from datetime import date

from app.models.booking import Booking
from app.models.payment import Payment
from app.services.analytics import detect_anomalies, income_projection, occupancy_forecast


def make_payment(amount: float) -> Payment:
    return Payment(subject_type="resident", subject_id=1, amount=amount, paid_on=date.today(), method="cash")


def test_income_projection():
    payments = [make_payment(100), make_payment(200)]
    projection = income_projection(payments)
    assert projection["عام"] == 300


def test_anomaly_detection():
    payments = [make_payment(100), make_payment(1000)]
    anomalies = detect_anomalies(payments)
    assert anomalies and anomalies[0].amount == 1000


def test_occupancy_forecast_shape():
    bookings = [
        Booking(kind="individual", name="A", people_count=2, gender="male", start_date=date.today(), end_date=date.today(), amount=0, status="active"),
    ]
    forecast = occupancy_forecast(bookings, horizon_days=3)
    assert len(forecast) == 3
