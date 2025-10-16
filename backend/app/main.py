from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import select

from .core.config import get_settings
from .database import get_session, init_db
from .models.common import Booking, Payment, Resident
from .routers import auth, bookings, guests, payments, residents, settings as settings_router
from .utils.auth import get_current_user

settings = get_settings()
app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(residents.router)
app.include_router(guests.router)
app.include_router(bookings.router)
app.include_router(payments.router)
app.include_router(settings_router.router)

scheduler = BackgroundScheduler()


def start_scheduler():
    if not scheduler.running:
        scheduler.start()


def send_due_notifications():
    with get_session() as session:
        session.exec(select(Resident)).all()
        # Placeholder: integrate email/telegram senders here


scheduler.add_job(send_due_notifications, "cron", hour=13)
scheduler.add_job(send_due_notifications, "cron", hour=22)
scheduler.add_job(send_due_notifications, "cron", day_of_week="thu", hour=9)


@app.on_event("startup")
def on_startup():
    init_db()
    start_scheduler()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/dashboard")
def dashboard(current_user=Depends(get_current_user), session=Depends(get_session)):
    today = datetime.utcnow().date()
    upcoming_bookings = session.exec(select(Booking).where(Booking.start_date >= today)).all()
    recent_payments = session.exec(select(Payment).order_by(Payment.paid_on.desc()).limit(5)).all()
    active_residents = session.exec(select(Resident).where(Resident.end_date == None)).all()  # type: ignore[comparison-overlap]
    return {
        "upcoming_bookings": upcoming_bookings,
        "recent_payments": recent_payments,
        "active_residents": len(active_residents),
    }
