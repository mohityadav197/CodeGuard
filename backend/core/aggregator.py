"""Dedupes and caps findings from the three specialist agents, then formats
the result as GitHub inline review comments plus a summary."""

from __future__ import annotations

from backend.config import MAX_COMMENTS
from .state import Finding, ReviewState

_SEVERITY_RANK = {"high": 0, "medium": 1, "low": 2}
_SEVERITY_LABEL = {"high": "\U0001F534 High", "medium": "\U0001F7E1 Medium", "low": "\U0001F535 Low"}
_CATEGORY_LABEL = {"bug": "Bug", "security": "Security", "quality": "Quality"}


def _dedupe(tagged: list[tuple[str, Finding]]) -> list[tuple[str, Finding]]:
    """Collapse findings that land on the same file/line, keeping the
    highest-severity one and noting every category that flagged it."""
    by_location: dict[tuple[str, int], list[tuple[str, Finding]]] = {}
    for category, finding in tagged:
        by_location.setdefault((finding.file, finding.line), []).append((category, finding))

    merged: list[tuple[str, Finding]] = []
    for group in by_location.values():
        group.sort(key=lambda cf: _SEVERITY_RANK[cf[1].severity])
        category, finding = group[0]
        if len(group) > 1:
            categories = ", ".join(sorted({c for c, _ in group}))
            finding = finding.model_copy(update={"message": f"[{categories}] {finding.message}"})
        merged.append((category, finding))
    return merged


def run(state: ReviewState) -> dict:
    tagged = (
        [("bug", f) for f in state.get("bug_findings", [])]
        + [("security", f) for f in state.get("security_findings", [])]
        + [("quality", f) for f in state.get("quality_findings", [])]
    )

    merged = _dedupe(tagged)
    merged.sort(key=lambda cf: (_SEVERITY_RANK[cf[1].severity], cf[1].file, cf[1].line))
    top = merged[:MAX_COMMENTS]

    comments = [
        {
            "path": finding.file,
            "line": finding.line,
            "body": f"**{_SEVERITY_LABEL[finding.severity]} · {_CATEGORY_LABEL[category]}**\n\n{finding.message}",
        }
        for category, finding in top
    ]

    # The same deduped/capped findings, shaped for DB persistence (used by
    # the webhook handler to create Finding rows) rather than GitHub comments.
    final_findings = [
        {
            "agent": category,
            "file": finding.file,
            "line": finding.line,
            "severity": finding.severity,
            "message": finding.message,
        }
        for category, finding in top
    ]

    counts = {
        "bug": len(state.get("bug_findings", [])),
        "security": len(state.get("security_findings", [])),
        "quality": len(state.get("quality_findings", [])),
    }
    omitted = len(merged) - len(top)
    summary_lines = [
        "**CodeGuard automated review**",
        f"- Bugs: {counts['bug']}  ·  Security: {counts['security']}  ·  Quality: {counts['quality']}",
    ]
    if omitted > 0:
        summary_lines.append(f"- {omitted} additional lower-priority finding(s) omitted for brevity.")
    if not top:
        summary_lines.append("- No issues found. \U0001F389")

    return {"summary": "\n".join(summary_lines), "comments": comments, "final_findings": final_findings}
