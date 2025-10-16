from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic import BaseSettings, Field, validator


class Settings(BaseSettings):
    app_name: str = "Mouqarr Flex Manager"
    debug: bool = False
    database_url: str = Field(
        default=f"sqlite:///{(Path(__file__).resolve().parents[2] / 'data.db').as_posix()}"
    )
    frontend_url: str = Field(default="http://localhost:5173", env="FRONTEND_URL")
    access_token_expires_minutes: int = 30
    refresh_token_expires_minutes: int = 60 * 24 * 14
    secret_key: str = Field(default="change-this", env="SECRET_KEY")
    hmac_secret: str = Field(default="change-hmac", env="HMAC_SECRET")
    fernet_key: str = Field(default="".ljust(44, "a"), env="FERNET_KEY")
    cors_origins: List[str] = Field(default_factory=list, env="CORS_ORIGINS")
    default_interval_days: int = Field(default=30, env="DEFAULT_INTERVAL_DAYS")
    clamp_monthly_to_28: bool = Field(default=True, env="CLAMP_MONTHLY_TO_28")
    smtp_host: str | None = Field(default=None, env="SMTP_HOST")
    smtp_port: int = Field(default=587, env="SMTP_PORT")
    smtp_username: str | None = Field(default=None, env="SMTP_USERNAME")
    smtp_password: str | None = Field(default=None, env="SMTP_PASSWORD")
    telegram_bot: str | None = Field(default=None, env="TELEGRAM_BOT")
    telegram_chat_id: str | None = Field(default=None, env="TELEGRAM_CHAT_ID")
    google_sheet_id: str | None = Field(default=None, env="GOOGLE_SHEET_ID")
    google_service_account_json: str | None = Field(
        default=None, env="GOOGLE_SA_JSON_PATH"
    )
    feature_flags: List[str] = Field(default_factory=list, env="FEATURE_FLAGS")
    sync_queue_max: int = Field(default=100, env="SYNC_QUEUE_MAX")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @validator("cors_origins", pre=True)
    def split_cors(cls, value: str | List[str]) -> List[str]:
        if isinstance(value, str):
            return [v.strip() for v in value.split(",") if v.strip()]
        return value

    @property
    def allow_prophet(self) -> bool:
        return "ENABLE_PROPHET" in self.feature_flags

    @property
    def enable_webhooks(self) -> bool:
        return "ENABLE_WEBHOOKS" in self.feature_flags

    @property
    def enable_sync(self) -> bool:
        return "ENABLE_SYNC" in self.feature_flags


@lru_cache
def get_settings() -> Settings:
    return Settings()
