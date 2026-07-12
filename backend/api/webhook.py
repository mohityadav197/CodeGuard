import hashlib
import hmac

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from backend.config import settings
from backend.core.diff_parser import build_diff_files
from backend.core.github_client import GitHubClient
from backend.core.graph import build_graph
from backend.database.db import get_db
from backend.database.models import Finding, Review
from backend.utils.logger import setup_logger

logger = setup_logger(__name__)

router = APIRouter()


@router.post("/webhook")
async def github_webhook(request: Request, db: AsyncSession = Depends(get_db)):
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

    if action not in ("opened", "synchronize"):
        return {"status": "ignored", "action": action}

    # Never let a pipeline failure fail the webhook response -- GitHub will
    # retry a non-2xx delivery endlessly.
    try:
        repo_full_name = payload["repository"]["full_name"]
        owner, repo_name = repo_full_name.split("/", 1)
        pr_number = payload["pull_request"]["number"]

        client = GitHubClient(settings.GITHUB_TOKEN)
        pr_files = client.get_pr_files(owner, repo_name, pr_number)
        files = build_diff_files(pr_files)

        if not files:
            return {"status": "review_completed", "review_id": None, "findings_count": 0}

        graph = build_graph()
        result = graph.invoke({"files": files})
        final_findings = result.get("final_findings", [])

        review = Review(
            repo=repo_full_name,
            pr_number=pr_number,
            status="completed",
            total_findings=len(final_findings),
        )
        db.add(review)
        await db.flush()  # populate review.id for the Finding rows below

        db.add_all(
            Finding(
                review_id=review.id,
                agent=f["agent"],
                file=f["file"],
                line=f["line"],
                severity=f["severity"],
                message=f["message"],
            )
            for f in final_findings
        )
        await db.commit()

        return {
            "status": "review_completed",
            "review_id": str(review.id),
            "findings_count": len(final_findings),
        }
    except Exception:
        logger.exception("Webhook review pipeline failed for action=%s", action)
        return {"status": "error", "action": action}
