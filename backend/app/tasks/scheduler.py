from __future__ import annotations

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.tasks import workers


def register_jobs(scheduler: AsyncIOScheduler) -> None:
    scheduler.add_job(workers.check_due_dates, "cron", day="13,22", hour=8)
    scheduler.add_job(workers.weekly_digest, "cron", day_of_week="thu", hour=9)
    scheduler.add_job(workers.upcoming_due_alerts, "interval", hours=24)
