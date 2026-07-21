"""Parses GitHub PR file `patch` strings into line-numbered diff hunks that
the review agents and GitHub's inline-comment API can both anchor to."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional

from .state import DiffFile

_HUNK_HEADER_RE = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")


@dataclass
class DiffLine:
    line_no: Optional[int]  # new-file line number; None for removed lines
    type: str  # "added" | "removed" | "context"
    content: str


@dataclass
class Hunk:
    old_start: int
    old_lines: int
    new_start: int
    new_lines: int
    lines: list[DiffLine] = field(default_factory=list)


def parse_patch(patch: Optional[str]) -> list[Hunk]:
    """Parse a unified-diff `patch` string into a list of Hunks."""
    if not patch:
        return []

    hunks: list[Hunk] = []
    current: Optional[Hunk] = None
    new_line_no = 0

    for raw_line in patch.splitlines():
        match = _HUNK_HEADER_RE.match(raw_line)
        if match:
            old_start, old_lines, new_start, new_lines = match.groups()
            current = Hunk(
                old_start=int(old_start),
                old_lines=int(old_lines or 1),
                new_start=int(new_start),
                new_lines=int(new_lines or 1),
            )
            hunks.append(current)
            new_line_no = current.new_start
            continue

        if current is None:
            continue  # stray preamble before the first hunk header

        if raw_line.startswith("\\"):
            continue  # "\ No newline at end of file"

        if raw_line.startswith("+"):
            current.lines.append(DiffLine(new_line_no, "added", raw_line[1:]))
            new_line_no += 1
        elif raw_line.startswith("-"):
            current.lines.append(DiffLine(None, "removed", raw_line[1:]))
        else:
            content = raw_line[1:] if raw_line.startswith(" ") else raw_line
            current.lines.append(DiffLine(new_line_no, "context", content))
            new_line_no += 1

    return hunks


def annotate_for_prompt(filename: str, hunks: list[Hunk]) -> str:
    """Render hunks as line-numbered text suitable for an LLM prompt.

    Each added/context line is prefixed with its real new-file line number so
    the model can reference exact line numbers in its findings.
    """
    out = [f"File: {filename}"]
    for hunk in hunks:
        out.append(f"@@ -{hunk.old_start},{hunk.old_lines} +{hunk.new_start},{hunk.new_lines} @@")
        for dl in hunk.lines:
            marker = {"added": "+", "removed": "-", "context": " "}[dl.type]
            label = f"{dl.line_no:>6}" if dl.line_no is not None else " " * 6
            out.append(f"{label} {marker} {dl.content}")
    return "\n".join(out)


def commentable_lines(hunks: list[Hunk]) -> set[int]:
    """New-file line numbers that GitHub will accept for an inline review comment."""
    return {dl.line_no for hunk in hunks for dl in hunk.lines if dl.line_no is not None}


def build_diff_files(pr_files: list[dict]) -> list[DiffFile]:
    """Turn GitHub's per-file `patch` payloads into annotated DiffFiles ready
    for the review pipeline. Shared by both the CLI/Action entrypoint and the
    webhook handler."""
    files: list[DiffFile] = []
    for pf in pr_files:
        patch = pf.get("patch")
        if not patch:
            continue  # binary files, or files GitHub didn't generate a patch for
        hunks = parse_patch(patch)
        files.append(
            DiffFile(
                filename=pf["filename"],
                annotated_diff=annotate_for_prompt(pf["filename"], hunks),
                commentable_lines=commentable_lines(hunks),
            )
        )
    return files
