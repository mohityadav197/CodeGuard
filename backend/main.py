"""FastAPI app entry point (routers, middleware, DB startup) and CLI for
running the CodeGuard review pipeline directly (--dry-run / Action mode)."""

from __future__ import annotations

import argparse
import logging
import os
import sys
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from backend import config
from backend.api.routes import router as api_router
from backend.api.webhook import router as webhook_router
from backend.auth.routes import router as auth_router
from backend.config import settings
from backend.core.diff_parser import build_diff_files
from backend.core.github_client import GitHubClient
from backend.core.graph import build_graph
from backend.database.db import init_db

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="CodeGuard", description="AI Code Review Agent")

app.add_middleware(SessionMiddleware, secret_key=settings.JWT_SECRET)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
app.include_router(webhook_router)
app.include_router(auth_router)


@app.on_event("startup")
async def startup():
    await init_db()


def run_pipeline(owner: str, repo: str, pr_number: int, token: str, dry_run: bool) -> int:
    client = GitHubClient(token)

    try:
        pr_files = client.get_pr_files(owner, repo, pr_number)
    except Exception:
        logger.exception("Failed to fetch PR #%s files from GitHub", pr_number)
        return 0  # non-blocking: don't fail the Action over a transient API error

    files = build_diff_files(pr_files)
    if not files:
        logger.info("No reviewable file diffs found on PR #%s; nothing to do.", pr_number)
        return 0

    graph = build_graph()
    result = graph.invoke({"files": files})

    summary = result.get("summary", "")
    comments = result.get("comments", [])

    if dry_run:
        print(summary)
        print()
        for c in comments:
            print(f"{c['path']}:{c['line']}\n{c['body']}\n")
        return 0

    try:
        client.post_review(owner, repo, pr_number, summary, comments)
    except Exception:
        logger.exception("Failed to post review to PR #%s", pr_number)
        return 0

    logger.info("Posted review with %d inline comment(s) on PR #%s", len(comments), pr_number)
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="CodeGuard multi-agent PR reviewer")
    parser.add_argument("--dry-run", action="store_true", help="Print findings instead of posting to GitHub")
    parser.add_argument("--owner", help="Repo owner (required for --dry-run)")
    parser.add_argument("--repo", help="Repo name (required for --dry-run)")
    parser.add_argument("--pr", type=int, help="PR number (required for --dry-run)")
    args = parser.parse_args(argv)

    if not config.GROQ_API_KEY:
        logger.error("GROQ_API_KEY is not set")
        return 1

    if args.dry_run:
        if not (args.owner and args.repo and args.pr):
            logger.error("--dry-run requires --owner, --repo, and --pr")
            return 1
        owner, repo, pr_number = args.owner, args.repo, args.pr
    else:
        repo_full = os.environ.get("GITHUB_REPOSITORY", "")
        pr_number_str = os.environ.get("PR_NUMBER", "")
        if "/" not in repo_full or not pr_number_str:
            logger.error("GITHUB_REPOSITORY and PR_NUMBER env vars are required outside --dry-run")
            return 1
        owner, repo = repo_full.split("/", 1)
        pr_number = int(pr_number_str)

    if not config.GITHUB_TOKEN:
        logger.error("GITHUB_TOKEN is not set")
        return 1

    return run_pipeline(owner, repo, pr_number, config.GITHUB_TOKEN, args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
