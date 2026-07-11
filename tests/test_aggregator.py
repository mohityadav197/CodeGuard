from backend.core import aggregator
from backend.core.state import Finding


def _finding(file, line, severity, message):
    return Finding(file=file, line=line, severity=severity, message=message)


def test_dedupes_same_file_line_keeping_highest_severity():
    state = {
        "bug_findings": [_finding("a.py", 10, "low", "minor bug")],
        "security_findings": [_finding("a.py", 10, "high", "sql injection")],
        "quality_findings": [],
    }

    result = aggregator.run(state)

    assert len(result["comments"]) == 1
    body = result["comments"][0]["body"]
    assert "sql injection" in body
    assert "bug, security" in body


def test_caps_comment_volume(monkeypatch):
    monkeypatch.setattr(aggregator, "MAX_COMMENTS", 2)
    findings = [_finding("a.py", i, "high", f"issue {i}") for i in range(5)]
    state = {"bug_findings": findings, "security_findings": [], "quality_findings": []}

    result = aggregator.run(state)

    assert len(result["comments"]) == 2
    assert "3 additional" in result["summary"]


def test_summary_reports_no_issues_found():
    state = {"bug_findings": [], "security_findings": [], "quality_findings": []}

    result = aggregator.run(state)

    assert result["comments"] == []
    assert "No issues found" in result["summary"]
