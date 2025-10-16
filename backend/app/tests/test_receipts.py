from __future__ import annotations

from app.utils.receipts import generate_receipt


def test_generate_receipt_bytes():
    payload = {"الاسم": "اختبار", "المبلغ": "100"}
    pdf_bytes = generate_receipt(payload)
    assert pdf_bytes.startswith(b"%PDF")
