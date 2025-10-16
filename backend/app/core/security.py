from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Optional

from jose import JWTError, jwt
from passlib.hash import argon2

from app.core.config import get_settings

settings = get_settings()


class TokenError(Exception):
    pass


def create_access_token(subject: str, expires_minutes: Optional[int] = None) -> str:
    expire = datetime.utcnow() + timedelta(
        minutes=expires_minutes or settings.access_token_expires_minutes
    )
    to_encode = {"sub": subject, "exp": expire}
    return jwt.encode(to_encode, settings.secret_key, algorithm="HS256")


def create_refresh_token(subject: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.refresh_token_expires_minutes)
    return jwt.encode({"sub": subject, "exp": expire, "type": "refresh"}, settings.secret_key, algorithm="HS256")


def decode_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(token, settings.secret_key, algorithms=["HS256"])
    except JWTError as exc:  # pragma: no cover - delegated to tests
        raise TokenError(str(exc)) from exc


def verify_password(plain: str, hashed: str) -> bool:
    return argon2.verify(plain, hashed)


def hash_password(password: str) -> str:
    return argon2.hash(password)
