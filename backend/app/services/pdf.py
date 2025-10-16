from pathlib import Path
from typing import Optional

from fpdf import FPDF

from ..core.config import get_settings
from ..models.common import Payment

settings = get_settings()

FONT_PATH = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")


def generate_receipt(payment: Payment, resident_name: Optional[str] = None) -> Path:
    receipts_dir = Path("backend/receipts")
    receipts_dir.mkdir(parents=True, exist_ok=True)
    file_path = receipts_dir / f"payment_{payment.id}.pdf"
    pdf = FPDF()
    pdf.add_page()
    if FONT_PATH.exists():
        pdf.add_font("DejaVu", "", str(FONT_PATH), uni=True)
        pdf.set_font("DejaVu", size=16)
    else:
        pdf.set_font("Helvetica", size=16)
    pdf.multi_cell(0, 10, txt=settings.app_name)
    if FONT_PATH.exists():
        pdf.set_font("DejaVu", size=12)
    else:
        pdf.set_font("Helvetica", size=12)
    pdf.multi_cell(0, 8, txt=f"رقم الإيصال: {payment.id}")
    if resident_name:
        pdf.multi_cell(0, 8, txt=f"المقيم: {resident_name}")
    pdf.multi_cell(0, 8, txt=f"المبلغ: {payment.amount}")
    pdf.multi_cell(0, 8, txt=f"تاريخ الدفع: {payment.paid_on}")
    pdf.output(str(file_path))
    return file_path
