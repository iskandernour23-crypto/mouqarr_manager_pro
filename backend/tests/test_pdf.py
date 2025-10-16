from datetime import date

from app.services.pdf import generate_receipt
from app.models.common import Payment


def test_generate_receipt():
    payment = Payment(id=1, amount=100.0, paid_on=date(2024, 1, 1))
    receipt = generate_receipt(payment, resident_name="محمد")
    assert receipt.exists()
