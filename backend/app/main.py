from __future__ import annotations

from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.middleware import SlowAPIMiddleware

from app.api.router import api_router
from app.core.config import get_settings
from app.core.rate_limit import limiter
from app.db.session import init_db
from app.tasks.scheduler import register_jobs

settings = get_settings()
scheduler = AsyncIOScheduler()


@asynccontextmanager
def lifespan(app: FastAPI):
    init_db()
    register_jobs(scheduler)
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

if settings.cors_origins or settings.frontend_url:
    origins = settings.cors_origins or [settings.frontend_url]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix="/api")


@app.get("/health")
@limiter.limit("10/minute")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ready")
@limiter.limit("10/minute")
def ready() -> dict[str, str]:
    return {"status": "ready"}
