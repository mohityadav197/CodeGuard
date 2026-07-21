"""CLI utility (`python -m backend.api.test_data seed`) that inserts fake
reviews/findings so the dashboard has data to show during development."""

from __future__ import annotations

import argparse
import asyncio
import random
from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.db import AsyncSessionLocal
from backend.database.models import Finding, Review

_REPOS = [
    "acme/webapp",
    "acme/api-gateway",
    "acme/mobile-app",
    "acme/infra",
    "acme/data-pipeline",
]
_AGENTS = ["bug", "security", "quality"]
_SEVERITIES = ["high", "medium", "low"]
_FILES = ["app.py", "utils/helpers.py", "src/index.js", "backend/main.py", "components/App.jsx"]
_MESSAGES = [
    "Potential null dereference on an unchecked optional value.",
    "SQL query built via string concatenation -- use parameterized queries.",
    "Function exceeds 80 lines; consider splitting for readability.",
    "Missing error handling around an external API call.",
    "Hardcoded credential found in source.",
]

_FINDINGS_PER_REVIEW = 3


async def seed_test_data(db: AsyncSession) -> tuple[int, int]:
    """Insert 5 fake reviews with 15 findings total. Returns (review_count, finding_count)."""
    review_count = 0
    finding_count = 0

    for i in range(5):
        review = Review(
            repo=random.choice(_REPOS),
            pr_number=100 + i,
            status="completed",
            total_findings=_FINDINGS_PER_REVIEW,
            created_at=datetime.now(timezone.utc) - timedelta(days=i),
        )
        db.add(review)
        await db.flush()  # populate review.id for the Finding rows below
        review_count += 1

        for _ in range(_FINDINGS_PER_REVIEW):
            db.add(
                Finding(
                    review_id=review.id,
                    agent=random.choice(_AGENTS),
                    file=random.choice(_FILES),
                    line=random.randint(1, 200),
                    severity=random.choice(_SEVERITIES),
                    message=random.choice(_MESSAGES),
                )
            )
            finding_count += 1

    await db.commit()
    return review_count, finding_count


async def _run_seed() -> None:
    async with AsyncSessionLocal() as db:
        reviews, findings = await seed_test_data(db)
    print(f"Seeded {reviews} reviews and {findings} findings")


def main() -> None:
    parser = argparse.ArgumentParser(description="CodeGuard test-data utility")
    parser.add_argument("command", choices=["seed"])
    args = parser.parse_args()

    if args.command == "seed":
        asyncio.run(_run_seed())


if __name__ == "__main__":
    main()
