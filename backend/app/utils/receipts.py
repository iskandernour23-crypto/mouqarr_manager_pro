from __future__ import annotations

from pathlib import Path
from io import BytesIO

from arabic_reshaper import ArabicReshaper
from bidi.algorithm import get_display
from fpdf import FPDF

reshaper = ArabicReshaper({"delete_harakat": False})
DEFAULT_FONT = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")


def arabic(text: str) -> str:
    return get_display(reshaper.reshape(text))


def generate_receipt(payment_info: dict[str, str]) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    if DEFAULT_FONT.exists():
        pdf.add_font("DejaVu", "", fname=str(DEFAULT_FONT), uni=True)
        pdf.set_font("DejaVu", size=14)
    else:  # pragma: no cover - depends on environment
        pdf.set_font("Helvetica", size=14)
    pdf.cell(200, 10, txt=arabic("إيصال دفع"), ln=True, align="C")
    for key, value in payment_info.items():
        pdf.multi_cell(0, 10, txt=f"{arabic(key)} : {arabic(value)}", align="R")
    buffer = BytesIO()
    pdf.output(buffer)
    return buffer.getvalue()
