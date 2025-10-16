from __future__ import annotations

from cryptography.fernet import Fernet, InvalidToken

from app.core.config import get_settings

settings = get_settings()
fernet = Fernet(settings.fernet_key.encode())


def encrypt(value: str | None) -> str | None:
    if not value:
        return None
    return fernet.encrypt(value.encode()).decode()


def decrypt(value: str | None) -> str | None:
    if not value:
        return None
    try:
        return fernet.decrypt(value.encode()).decode()
    except InvalidToken:  # pragma: no cover - indicates rotated keys
        return None
