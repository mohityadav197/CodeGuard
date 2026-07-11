"""Security-vulnerability specialist agent."""

from __future__ import annotations

from backend.core.state import ReviewState
from .common import analyze_files

SYSTEM_PROMPT = """You are an application security engineer reviewing a diff
for vulnerabilities: injection (SQL/command/template), XSS, insecure
deserialization, hardcoded secrets or credentials, missing authn/authz
checks, path traversal, SSRF, insecure cryptography, and unsafe handling of
user input. Ignore general code quality, style, and non-security bugs --
those are handled by other reviewers."""


def run(state: ReviewState) -> dict:
    findings = analyze_files(SYSTEM_PROMPT, state["files"])
    return {"security_findings": findings}
