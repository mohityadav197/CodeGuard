"""Shared data structures for the LangGraph review pipeline."""

from __future__ import annotations

from typing import Literal, TypedDict

from pydantic import BaseModel, Field

Severity = Literal["low", "medium", "high"]
Category = Literal["bug", "security", "quality"]


class Finding(BaseModel):
    """A single review finding anchored to a file/line in the PR diff."""

    file: str = Field(description="Exact file path as given in the diff")
    line: int = Field(description="New-file line number this finding applies to")
    severity: Severity
    message: str = Field(description="Concise, actionable explanation of the issue")


class FindingList(BaseModel):
    """Wrapper so an LLM can return structured output as `{"findings": [...]}`."""

    findings: list[Finding] = Field(default_factory=list)


class DiffFile(TypedDict):
    filename: str
    annotated_diff: str
    commentable_lines: set[int]


class ReviewState(TypedDict, total=False):
    files: list[DiffFile]
    bug_findings: list[Finding]
    security_findings: list[Finding]
    quality_findings: list[Finding]
    summary: str
    comments: list[dict]
    final_findings: list[dict]
