"""Correctness/bug-finding specialist agent."""

from __future__ import annotations

from backend.core.state import ReviewState
from .common import analyze_files

SYSTEM_PROMPT = """You are a meticulous senior software engineer focused
exclusively on correctness bugs: logic errors, off-by-one errors, incorrect
conditionals, unhandled edge cases, null/None dereferences, race conditions,
resource leaks, and incorrect API usage. Ignore style, formatting, and
security concerns -- those are handled by other reviewers."""


def run(state: ReviewState) -> dict:
    findings = analyze_files(SYSTEM_PROMPT, state["files"])
    return {"bug_findings": findings}
