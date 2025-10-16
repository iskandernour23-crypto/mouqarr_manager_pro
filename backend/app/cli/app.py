from __future__ import annotations

import json
from pathlib import Path

import typer
from sqlmodel import select

from app.db.session import init_db, session_scope
from app.models.payment import Payment
from app.utils.receipts import generate_receipt

cli = typer.Typer(help="Mouqarr Flex Manager CLI")


@cli.command()
def init_db_command() -> None:
    """Initialize database tables."""
    init_db()
    typer.echo("Database initialized")


@cli.command()
def demo() -> None:
    typer.echo("Demo data loading not implemented yet")


@cli.command()
def report(days: int = typer.Argument(30)) -> None:
    with session_scope() as session:
        payments = session.exec(select(Payment)).all()
    typer.echo(json.dumps([payment.dict() for payment in payments][-days:]))


@cli.command()
def receipt(payment_id: int, output: Path) -> None:
    with session_scope() as session:
        payment = session.get(Payment, payment_id)
        if not payment:
            raise typer.BadParameter("Payment not found")
        pdf_bytes = generate_receipt(
            {
                "رقم الإيصال": payment.receipt_no or str(payment.id),
                "المبلغ": f"{payment.amount:.2f}",
                "التاريخ": payment.paid_on.isoformat(),
            }
        )
    output.write_bytes(pdf_bytes)
    typer.echo(f"Receipt saved to {output}")


if __name__ == "__main__":
    cli()
