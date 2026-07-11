"""Shared helpers for the three specialist review agents.

Each specialist agent calls Groq once per changed file, asking for structured
findings, then filters out anything that doesn't anchor to a real
commentable line in that file's diff.
"""

from __future__ import annotations

import logging

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq

from backend.config import GROQ_API_KEY, GROQ_MODEL
from backend.core.state import DiffFile, Finding, FindingList

logger = logging.getLogger(__name__)

_COMMON_INSTRUCTIONS = """

You are reviewing a single file's diff from a GitHub pull request. Each line
in the diff is prefixed with its real line number in the new version of the
file, followed by a `+` (added), `-` (removed), or ` ` (unchanged context)
marker. Only raise findings against lines marked `+`, and always use the
exact line number shown -- never a line number that doesn't appear in the
diff. If there are no genuine issues, return an empty findings list. Do not
raise more than one finding for the same underlying issue.
"""


def _build_llm():
    return ChatGroq(model=GROQ_MODEL, api_key=GROQ_API_KEY, temperature=0)


def analyze_file(system_prompt: str, file: DiffFile) -> list[Finding]:
    structured_llm = _build_llm().with_structured_output(FindingList)

    messages = [
        SystemMessage(content=system_prompt + _COMMON_INSTRUCTIONS),
        HumanMessage(content=file["annotated_diff"]),
    ]

    try:
        result = structured_llm.invoke(messages)
    except Exception:
        logger.exception("LLM call failed for file %s", file["filename"])
        return []

    findings = result.findings if isinstance(result, FindingList) else []
    valid_lines = file["commentable_lines"]
    return [
        f.model_copy(update={"file": file["filename"]})
        for f in findings
        if f.line in valid_lines
    ]


def analyze_files(system_prompt: str, files: list[DiffFile]) -> list[Finding]:
    findings: list[Finding] = []
    for file in files:
        findings.extend(analyze_file(system_prompt, file))
    return findings
