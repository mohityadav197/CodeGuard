"""Environment configuration for CodeGuard.

In GitHub Actions, GITHUB_REPOSITORY, GITHUB_TOKEN are provided automatically
by the runner; PR_NUMBER is passed explicitly by the workflow from the
pull_request event payload.
"""

from __future__ import annotations

import os
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GITHUB_WEBHOOK_SECRET = os.environ.get("GITHUB_WEBHOOK_SECRET", "")

# Model used for all three specialist agents. Groq's Llama 3.3 70B is a good
# balance of quality and speed/cost for structured-output code review.
GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")

# Cap on how many inline comments get posted per review, to avoid PR spam.
MAX_COMMENTS = int(os.environ.get("CODEGUARD_MAX_COMMENTS", "15"))

# The raw connection string as provided (e.g. by Neon): postgresql://...
# Kept as-is for tools that want a standard libpq-style URL (Alembic/psycopg2).
RAW_DATABASE_URL = os.environ.get("DATABASE_URL", "")


def _build_async_database_url(raw_url: str) -> tuple[str, dict]:
    """Convert a standard postgresql:// URL into one usable by SQLAlchemy's
    async engine (asyncpg driver), which doesn't accept `sslmode` as a URL
    query param -- it must be passed as a separate connect arg instead.
    """
    if not raw_url:
        return "", {}

    url = raw_url
    if url.startswith("postgresql://"):
        url = "postgresql+asyncpg://" + url[len("postgresql://"):]
    elif url.startswith("postgres://"):
        url = "postgresql+asyncpg://" + url[len("postgres://"):]

    parts = urlsplit(url)
    query = dict(parse_qsl(parts.query))
    connect_args: dict = {}
    if query.pop("sslmode", None) == "require":
        connect_args["ssl"] = "require"
    url = urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))
    return url, connect_args


# Async (asyncpg) URL + connect args used by the app's SQLAlchemy engine.
DATABASE_URL, DATABASE_CONNECT_ARGS = _build_async_database_url(RAW_DATABASE_URL)


class Settings:
    """Object-style view over the same environment configuration, for
    modules (e.g. the FastAPI webhook route) that prefer `settings.X`."""

    GROQ_API_KEY = GROQ_API_KEY
    GITHUB_TOKEN = GITHUB_TOKEN
    GITHUB_WEBHOOK_SECRET = GITHUB_WEBHOOK_SECRET
    GROQ_MODEL = GROQ_MODEL
    MAX_COMMENTS = MAX_COMMENTS
    RAW_DATABASE_URL = RAW_DATABASE_URL
    DATABASE_URL = DATABASE_URL
    DATABASE_CONNECT_ARGS = DATABASE_CONNECT_ARGS


settings = Settings()
