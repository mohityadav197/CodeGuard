import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.api.serializers import finding_to_dict, review_to_dict
from backend.auth.jwt_handler import get_current_user
from backend.database.db import get_db
from backend.database.models import Finding, Review, User
from backend.utils.logger import setup_logger

logger = setup_logger(__name__)

router = APIRouter(prefix="/api")

# Finding.severity is stored using the review pipeline's own vocabulary
# (high/medium/low), but the dashboard wants the critical/warning/info
# vocabulary -- normalize (and accept either, for older/seeded rows).
_SEVERITY_ALIASES = {
    "critical": "critical",
    "high": "critical",
    "warning": "warning",
    "medium": "warning",
    "info": "info",
    "low": "info",
}


@router.get("/health")
async def health():
    return {"status": "CodeGuard is running", "version": "1.0.0"}


@router.get("/reviews")
async def get_reviews(
    repo: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        query = select(Review)
        count_query = select(func.count()).select_from(Review)
        if repo:
            query = query.where(Review.repo == repo)
            count_query = count_query.where(Review.repo == repo)

        query = query.order_by(Review.created_at.desc()).limit(limit).offset(offset)

        reviews = (await db.execute(query)).scalars().all()
        total = (await db.execute(count_query)).scalar_one()
    except Exception:
        logger.exception("Failed to fetch reviews")
        raise HTTPException(status_code=500, detail="Failed to fetch reviews")

    return {
        "reviews": [review_to_dict(r) for r in reviews],
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.get("/reviews/{review_id}")
async def get_review(
    review_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        result = await db.execute(
            select(Review).options(selectinload(Review.findings)).where(Review.id == review_id)
        )
        review = result.scalar_one_or_none()
    except Exception:
        logger.exception("Failed to fetch review %s", review_id)
        raise HTTPException(status_code=500, detail="Failed to fetch review")

    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")

    data = review_to_dict(review)
    data["findings"] = [finding_to_dict(f) for f in review.findings]
    return data


@router.get("/stats")
async def get_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        total_reviews = (await db.execute(select(func.count()).select_from(Review))).scalar_one()
        total_findings = (await db.execute(select(func.count()).select_from(Finding))).scalar_one()

        agent_rows = (
            await db.execute(select(Finding.agent, func.count()).group_by(Finding.agent))
        ).all()
        findings_by_agent = {agent: count for agent, count in agent_rows}

        severity_rows = (
            await db.execute(select(Finding.severity, func.count()).group_by(Finding.severity))
        ).all()
        findings_by_severity = {"critical": 0, "warning": 0, "info": 0}
        for severity, count in severity_rows:
            key = _SEVERITY_ALIASES.get((severity or "").lower())
            if key:
                findings_by_severity[key] += count

        top_repo_rows = (
            await db.execute(
                select(Review.repo, func.count().label("review_count"))
                .group_by(Review.repo)
                .order_by(func.count().desc())
                .limit(5)
            )
        ).all()
        top_repos = [{"repo": repo, "review_count": count} for repo, count in top_repo_rows]

        since = datetime.now(timezone.utc) - timedelta(days=7)
        activity_rows = (
            await db.execute(
                select(func.date(Review.created_at), func.count())
                .where(Review.created_at >= since)
                .group_by(func.date(Review.created_at))
                .order_by(func.date(Review.created_at))
            )
        ).all()
        recent_activity = [{"date": str(date), "count": count} for date, count in activity_rows]
    except Exception:
        logger.exception("Failed to compute stats")
        raise HTTPException(status_code=500, detail="Failed to compute stats")

    return {
        "total_reviews": total_reviews,
        "total_findings": total_findings,
        "findings_by_agent": findings_by_agent,
        "findings_by_severity": findings_by_severity,
        "top_repos": top_repos,
        "recent_activity": recent_activity,
    }


@router.get("/repos")
async def get_repos(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        rows = (
            await db.execute(
                select(Review.repo, func.count().label("review_count"))
                .group_by(Review.repo)
                .order_by(func.count().desc())
            )
        ).all()
    except Exception:
        logger.exception("Failed to fetch repos")
        raise HTTPException(status_code=500, detail="Failed to fetch repos")

    return {"repos": [{"repo": repo, "review_count": count} for repo, count in rows]}
