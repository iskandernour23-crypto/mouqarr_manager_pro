from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from slowapi.util import get_remote_address
from sqlmodel import Session, select

from app.core.config import get_settings
from app.core.deps import get_session
from app.core.rate_limit import limiter
from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])
settings = get_settings()


@router.post("/login")
@limiter.limit("5/minute")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)
) -> dict:
    user = session.exec(select(User).where(User.username == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.pw_hash):
        raise HTTPException(status_code=400, detail="INVALID_CREDENTIALS")
    user.last_login_at = datetime.utcnow()
    session.add(user)
    session.commit()
    access = create_access_token(user.username)
    refresh = create_refresh_token(user.username)
    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "bearer",
        "user": {"username": user.username, "role": user.role},
    }


@router.post("/register")
@limiter.limit("2/minute")
def register(data: dict, session: Session = Depends(get_session)) -> dict:
    if session.exec(select(User).where(User.username == data.get("username"))).first():
        raise HTTPException(status_code=409, detail="USERNAME_EXISTS")
    user = User(
        username=data["username"],
        role=data.get("role", "viewer"),
        pw_hash=hash_password(data["password"]),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"id": user.id, "username": user.username, "role": user.role}


@router.post("/refresh")
@limiter.limit("10/minute")
def refresh(token: str) -> dict:
    access = create_access_token(token)
    refresh_token = create_refresh_token(token)
    return {"access_token": access, "refresh_token": refresh_token}
