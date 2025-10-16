from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.core.deps import get_session, require_role
from app.core.security import hash_password
from app.models.user import User, UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[UserRead], dependencies=[Depends(require_role("admin"))])
def list_users(session: Session = Depends(get_session)) -> List[UserRead]:
    return session.exec(select(User)).all()


@router.post(
    "/",
    response_model=UserRead,
    dependencies=[Depends(require_role("admin"))],
)
def create_user(user_in: UserCreate, session: Session = Depends(get_session)) -> User:
    if session.exec(select(User).where(User.username == user_in.username)).first():
        raise HTTPException(status_code=409, detail="USERNAME_EXISTS")
    user = User(username=user_in.username, role=user_in.role, pw_hash=hash_password(user_in.password))
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.put(
    "/{user_id}",
    response_model=UserRead,
    dependencies=[Depends(require_role("admin"))],
)
def update_user(user_id: int, user_in: UserUpdate, session: Session = Depends(get_session)) -> User:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="NOT_FOUND")
    data = user_in.dict(exclude_unset=True)
    if "password" in data:
        user.pw_hash = hash_password(data.pop("password"))
    for key, value in data.items():
        setattr(user, key, value)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.delete(
    "/{user_id}", dependencies=[Depends(require_role("admin"))]
)
def delete_user(user_id: int, session: Session = Depends(get_session)) -> dict[str, str]:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="NOT_FOUND")
    session.delete(user)
    session.commit()
    return {"status": "deleted"}
