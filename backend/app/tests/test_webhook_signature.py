from __future__ import annotations

import hmac
import json

from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.main import app

client = TestClient(app)
settings = get_settings()


def test_webhook_signature():
    payload = {"hello": "world"}
    body = json.dumps(payload).encode()
    signature = hmac.new(settings.hmac_secret.encode(), body, "sha256").hexdigest()
    response = client.post("/api/webhooks/incoming/test", data=body, headers={"x-signature": signature})
    assert response.status_code == 200
    assert response.json()["data"] == payload
