from fastapi import APIRouter, Request, HTTPException
import hmac, hashlib
from backend.config import settings

router = APIRouter()


@router.post("/webhook")
async def github_webhook(request: Request):
    """Receives GitHub PR webhook events and triggers review pipeline."""
    body = await request.body()
    signature = request.headers.get("X-Hub-Signature-256", "")

    # Verify webhook signature
    if settings.GITHUB_WEBHOOK_SECRET:
        expected = "sha256=" + hmac.new(
            settings.GITHUB_WEBHOOK_SECRET.encode(),
            body, hashlib.sha256
        ).hexdigest()
        if not hmac.compare_digest(signature, expected):
            raise HTTPException(status_code=403, detail="Invalid signature")

    payload = await request.json()
    action = payload.get("action")

    if action in ("opened", "synchronize"):
        # TODO: trigger review pipeline async
        pr = payload.get("pull_request", {})
        return {"status": "review_triggered", "pr": pr.get("number")}

    return {"status": "ignored", "action": action}
