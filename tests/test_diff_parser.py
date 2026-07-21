"""Tests for diff parsing and line-number mapping."""

from pathlib import Path

from backend.core.diff_parser import annotate_for_prompt, commentable_lines, parse_patch

FIXTURE = Path(__file__).parent / "fixtures" / "sample.diff"


def test_parse_patch_line_numbers():
    patch = FIXTURE.read_text()
    hunks = parse_patch(patch)

    assert len(hunks) == 1
    hunk = hunks[0]
    assert (hunk.old_start, hunk.old_lines) == (1, 5)
    assert (hunk.new_start, hunk.new_lines) == (1, 10)

    added = [dl for dl in hunk.lines if dl.type == "added"]
    assert [dl.line_no for dl in added] == [5, 6, 8, 9, 10]
    assert added[0].content == "    if b == 0:"


def test_commentable_lines_covers_full_new_range():
    hunks = parse_patch(FIXTURE.read_text())
    assert commentable_lines(hunks) == set(range(1, 11))


def test_annotate_for_prompt_includes_filename_and_markers():
    hunks = parse_patch(FIXTURE.read_text())
    text = annotate_for_prompt("app.py", hunks)
    assert "File: app.py" in text
    assert "+     if b == 0:" in text


def test_empty_patch_returns_no_hunks():
    assert parse_patch(None) == []
    assert parse_patch("") == []
