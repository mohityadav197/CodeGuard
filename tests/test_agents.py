"""Tests for the shared specialist-agent helper (backend/agents/common.py),
using a fake LLM so no network/API key is required."""

from backend.agents import common
from backend.core.state import DiffFile, Finding, FindingList


def _diff_file(commentable_lines=None):
    return DiffFile(
        filename="app.py",
        annotated_diff="File: app.py\n@@ -1,1 +1,1 @@\n     1 +   x = 1",
        commentable_lines=commentable_lines or {1},
    )


class _FakeStructuredLLM:
    def __init__(self, result_or_error):
        self._result_or_error = result_or_error

    def invoke(self, messages):
        if isinstance(self._result_or_error, Exception):
            raise self._result_or_error
        return self._result_or_error


class _FakeLLM:
    def __init__(self, result_or_error):
        self._result_or_error = result_or_error

    def with_structured_output(self, schema):
        return _FakeStructuredLLM(self._result_or_error)


def test_analyze_file_filters_findings_outside_commentable_lines(monkeypatch):
    fake_result = FindingList(
        findings=[
            Finding(file="ignored.py", line=1, severity="high", message="in range"),
            Finding(file="ignored.py", line=99, severity="low", message="out of range"),
        ]
    )
    monkeypatch.setattr(common, "_build_llm", lambda: _FakeLLM(fake_result))

    findings = common.analyze_file("system prompt", _diff_file(commentable_lines={1}))

    assert [f.line for f in findings] == [1]
    assert findings[0].file == "app.py"  # filename is normalized to the real file


def test_analyze_file_returns_empty_list_on_llm_error(monkeypatch):
    monkeypatch.setattr(common, "_build_llm", lambda: _FakeLLM(RuntimeError("groq is down")))

    findings = common.analyze_file("system prompt", _diff_file())

    assert findings == []


def test_analyze_files_aggregates_across_multiple_files(monkeypatch):
    fake_result = FindingList(findings=[Finding(file="x", line=1, severity="low", message="issue")])
    monkeypatch.setattr(common, "_build_llm", lambda: _FakeLLM(fake_result))

    files = [_diff_file(), _diff_file()]
    findings = common.analyze_files("system prompt", files)

    assert len(findings) == 2
