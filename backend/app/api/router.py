from __future__ import annotations

from fastapi import APIRouter

from app.api.v1 import analytics, auth, beds, bookings, guests, logs, payments, residents, settings, users, webhooks

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(residents.router)
api_router.include_router(guests.router)
api_router.include_router(bookings.router)
api_router.include_router(payments.router)
api_router.include_router(beds.router)
api_router.include_router(settings.router)
api_router.include_router(users.router)
api_router.include_router(analytics.router)
api_router.include_router(webhooks.router)
api_router.include_router(logs.router)
