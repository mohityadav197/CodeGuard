"""Code-quality/maintainability specialist agent."""

from __future__ import annotations

from backend.core.state import ReviewState
from .common import analyze_files

SYSTEM_PROMPT = """You are a pragmatic senior engineer reviewing a diff for
code quality: unclear naming, dead code, needless duplication, missing or
misleading comments, overly complex functions, and violations of the
surrounding code's existing conventions. Only flag things that meaningfully
hurt readability or maintainability -- do not nitpick trivial style
preferences. Ignore correctness bugs and security issues -- those are
handled by other reviewers."""


def run(state: ReviewState) -> dict:
    findings = analyze_files(SYSTEM_PROMPT, state["files"])
    return {"quality_findings": findings}
