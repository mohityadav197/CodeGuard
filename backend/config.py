"""Environment configuration for CodeGuard.

In GitHub Actions, GITHUB_REPOSITORY, GITHUB_TOKEN are provided automatically
by the runner; PR_NUMBER is passed explicitly by the workflow from the
pull_request event payload.
"""

from __future__ import annotations

import os

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


class Settings:
    """Object-style view over the same environment configuration, for
    modules (e.g. the FastAPI webhook route) that prefer `settings.X`."""

    GROQ_API_KEY = GROQ_API_KEY
    GITHUB_TOKEN = GITHUB_TOKEN
    GITHUB_WEBHOOK_SECRET = GITHUB_WEBHOOK_SECRET
    GROQ_MODEL = GROQ_MODEL
    MAX_COMMENTS = MAX_COMMENTS


settings = Settings()
