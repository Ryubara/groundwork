"""Tests for the checks added from Coney's later conventions: commit trailers, the model line against the trailers,
generated blocks in hand-written files, pointer files and manual paths. GitHub itself is not called."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

PACK = Path(__file__).resolve().parent.parent / "pack"
_spec = importlib.util.spec_from_file_location("groundwork_additions", PACK / ".github" / "scripts" / "groundwork.py")
gw = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gw)


@pytest.fixture()
def conv():
    return gw.load(PACK / ".github" / "conventions.yml")


AI_MSG = "core: Add the thing\n\nWhy it matters.\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\n"


def test_ai_trailer_passes(conv):
    assert gw.commit_problems(conv, AI_MSG) == []


def test_plain_message_without_trailers_passes(conv):
    assert gw.commit_problems(conv, "core: Add the thing\n\nA body.\n") == []


@pytest.mark.parametrize(
    ("message", "fragment"),
    [
        ("t: Add x\n\nCo-Authored-By: Someone <someone@example.com>\n", "must read"),
        ("t: Add x\n\nSigned-off-by: A <noreply@anthropic.com>\n", "not allowed"),
        ("t: Add x\n\nMail me at me@example.com about it.\n", "e-mail address"),
    ],
)
def test_bad_trailers_and_emails_refused(conv, message, fragment):
    problems = gw.commit_problems(conv, message)
    assert problems and any(fragment in p for p in problems)


def test_prose_last_paragraph_is_not_trailers(conv):
    assert gw.split_trailers("t: Add x\n\nNote: this line is prose\nand so is this one.\n") == []


BODY = """## Summary

Adds it.

## Checklist

- [x] it

## Testing

- 3 passed

## Screenshots

Screenshots: none (no visual change)

## AI use

- **Commits written by:** an AI
- **Model:** {model}
"""


def test_model_line_must_name_trailer_models(conv):
    commits = [("abc1234567890", AI_MSG)]
    assert gw.commits_problems(conv, commits, BODY.format(model="Claude Opus 5.5")) == []
    problems = gw.commits_problems(conv, commits, BODY.format(model="Claude Sonnet 5.5"))
    assert problems and "Claude Opus 5.5" in problems[0]


def test_read_commits_handles_slurped_pages(tmp_path):
    pages = [[{"sha": "a" * 40, "commit": {"message": "m1"}}], [{"sha": "b" * 40, "commit": {"message": "m2"}}]]
    path = tmp_path / "commits.json"
    path.write_text(json.dumps(pages), encoding="utf-8")
    assert gw.read_commits(str(path)) == [("a" * 40, "m1"), ("b" * 40, "m2")]


def test_blocks_render_and_are_idempotent(conv):
    text = (PACK / "AGENTS.md").read_text(encoding="utf-8")
    once = gw.render_blocks_in(conv, text)
    assert "Verbs: Add, Fix" in once and "noreply@anthropic.com" in once and "Maintainer decisions" in once
    assert ".claude/hooks/" in once
    assert gw.render_blocks_in(conv, once) == once
    for line in once.splitlines():
        assert len(line) <= 120, line


def test_unknown_block_is_refused(conv):
    with pytest.raises(gw.ConventionsError):
        gw.render_blocks_in(conv, "<!-- conventions:begin nope -->\n<!-- conventions:end -->")


def test_pointer_files(conv, tmp_path):
    (tmp_path / "CLAUDE.md").write_text("# CLAUDE.md\n\n@AGENTS.md\n", encoding="utf-8")
    assert gw.pointer_problems(conv, tmp_path) == []
    (tmp_path / "GEMINI.md").write_text("@AGENTS.md\n\nAlso do this.\n", encoding="utf-8")
    assert any("GEMINI.md" in p for p in gw.pointer_problems(conv, tmp_path))


def test_manual_paths(conv):
    assert gw.manual_matches(conv, ["src/a.py", ".claude/hooks/guard.py", "AGENTS.md"]) == [
        ".claude/hooks/guard.py",
        "AGENTS.md",
    ]
    assert gw.manual_matches(conv, ["src/a.py", "docs/x.md"]) == []


def test_commit_msg_title_lets_tool_titles_pass(conv, tmp_path, capsys):
    msg = tmp_path / "COMMIT_EDITMSG"
    msg.write_text("fixup! core: Add x\n# comment\n", encoding="utf-8")
    assert gw.main(["--conventions", str(PACK / ".github" / "conventions.yml"), "check-title", "--commit-msg", str(msg)]) == 0
    msg.write_text("added stuff\n", encoding="utf-8")
    assert gw.main(["--conventions", str(PACK / ".github" / "conventions.yml"), "check-title", "--commit-msg", str(msg)]) == 1


SHOT_BODY = "## Summary\n\nx\n\n## Screenshots\n\n{shots}\n"


def visual(conv):
    conv["pull_requests"]["screenshots"]["areas"] = ["ui"]
    return conv


def test_screenshots_rule_off_without_areas(conv):
    assert gw.screenshot_problems(conv, "ui: Add the menu", SHOT_BODY.format(shots="")) == []


def test_screenshots_rule_needs_an_upload_or_a_reasoned_none(conv):
    conv = visual(conv)
    assert gw.screenshot_problems(conv, "ui: Add the menu", SHOT_BODY.format(shots="nothing"))
    upload = "![menu](https://github.com/user-attachments/assets/abc-123)"
    assert gw.screenshot_problems(conv, "ui: Add the menu", SHOT_BODY.format(shots=upload)) == []
    assert gw.screenshot_problems(conv, "ui: Add the menu", SHOT_BODY.format(shots="Screenshots: none (rules only)")) == []
    assert gw.screenshot_problems(conv, "ui: Add the menu", SHOT_BODY.format(shots="Screenshots: none"))
    assert gw.screenshot_problems(conv, "core: Add rules", SHOT_BODY.format(shots="")) == []


def test_local_image_is_not_an_upload(conv):
    conv = visual(conv)
    assert gw.screenshot_problems(conv, "ui: Add x", SHOT_BODY.format(shots="![x](./shots/menu.png)"))
