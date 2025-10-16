from fastapi import APIRouter, Depends

from ..utils.auth import ensure_default_admin, login

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token")
async def token(payload=Depends(login), _=Depends(ensure_default_admin)):
    return payload
