"""Shared dict serializers for API responses, so routes don't duplicate
model-to-JSON conversion logic (in particular UUID -> str)."""

from __future__ import annotations

from backend.database.models import Finding, Review


def review_to_dict(review: Review) -> dict:
    return {
        "id": str(review.id),
        "repo": review.repo,
        "pr_number": review.pr_number,
        "status": review.status,
        "total_findings": review.total_findings,
        "created_at": review.created_at,
    }


def finding_to_dict(finding: Finding) -> dict:
    return {
        "id": str(finding.id),
        "agent": finding.agent,
        "file": finding.file,
        "line": finding.line,
        "severity": finding.severity,
        "message": finding.message,
        "suggestion": finding.suggestion,
        "created_at": finding.created_at,
    }
