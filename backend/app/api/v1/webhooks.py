from __future__ import annotations

import hmac
import json

from fastapi import APIRouter, Depends, Header, HTTPException, Request, status

from app.core.config import get_settings
from app.core.deps import require_role

settings = get_settings()
router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/", dependencies=[Depends(require_role("manager", "admin"))])
async def trigger_outgoing(payload: dict) -> dict:
    if not settings.enable_webhooks:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="DISABLED")
    return {"status": "queued", "payload": payload}


@router.post("/incoming/{name}")
async def handle_incoming(
    name: str,
    request: Request,
    x_signature: str | None = Header(default=None, convert_underscores=False),
) -> dict:
    body = await request.body()
    digest = hmac.new(settings.hmac_secret.encode(), body, "sha256").hexdigest()
    if x_signature != digest:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="INVALID")
    data = json.loads(body.decode()) if body else {}
    return {"status": "accepted", "name": name, "data": data}
