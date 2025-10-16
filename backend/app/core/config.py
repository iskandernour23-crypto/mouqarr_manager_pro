from functools import lru_cache
from pathlib import Path
from typing import List, Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Mouqarr Flex Manager"
    secret_key: str = "super-secret-key"
    access_token_expire_minutes: int = 60 * 24
    sqlite_path: Path = Path("./backend/app.db")

    default_interval_days: int = 30
    clamp_monthly_to_28: bool = True
    capacity_males: int = 20
    capacity_females: int = 50

    smtp_host: Optional[str] = None
    smtp_port: int = 587
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None
    smtp_use_tls: bool = True

    telegram_bot_token: Optional[str] = None
    telegram_chat_id: Optional[str] = None

    google_service_account_json: Optional[Path] = None
    google_sheet_id: Optional[str] = None

    cors_allow_origins: List[str] = ["http://localhost:5173", "http://localhost:3000"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
