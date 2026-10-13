"""Tests for the portable checker (pack/.github/scripts/groundwork.py): titles, descriptions, docs rule, rendering,
settings and ruleset shapes, and the conventions loader's refusals. GitHub itself is not called."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest
import yaml

PACK = Path(__file__).resolve().parent.parent / "pack" / ".github"
_spec = importlib.util.spec_from_file_location("groundwork", PACK / "scripts" / "groundwork.py")
gw = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gw)


@pytest.fixture()
def conv():
    return gw.load(PACK / "conventions.yml")


GOOD_BODY = """## Summary

Adds the thing.

Fixes #3

## Checklist

- [x] the thing

## Testing

- 12 passed

## AI use

- **Commits written by:** an AI
- **Model:** Claude Sonnet 5.5
"""


def test_pack_conventions_load(conv):
    assert conv["merge"]["required_checks"] == ["title", "body", "docs"]


@pytest.mark.parametrize("title", ["core: Add a thing", "docs: Fix the typo (BREAKING)"])
def test_good_titles(conv, title):
    assert gw.title_problems(conv, title) == []


@pytest.mark.parametrize(
    "title,fragment",
    [
        ("Add a thing", "does not match"),
        ("feat: Add a thing", "area 'feat'"),
        ("core: Adds a thing", "verb 'Adds'"),
        ("core: Add a thing.", "period"),
        ("core: Add " + "x" * 80, "characters"),
    ],
)
def test_bad_titles(conv, title, fragment):
    assert any(fragment in p for p in gw.title_problems(conv, title))


def test_good_body(conv):
    assert gw.body_problems(conv, GOOD_BODY) == []


def test_template_as_rendered_is_refused(conv):
    problems = gw.body_problems(conv, gw.render_template(conv))
    assert any("Summary" in p for p in problems) and any("Testing" in p for p in problems)


def test_missing_section_and_order(conv):
    assert any("missing the section ## Testing" in p for p in gw.body_problems(conv, GOOD_BODY.replace("## Testing", "## Tests")))
    swapped = GOOD_BODY.replace("## Checklist", "## X").replace("## Testing", "## Checklist").replace("## X", "## Testing")
    assert any("out of order" in p for p in gw.body_problems(conv, swapped))


def test_unticked_task_refused(conv):
    assert any("unticked" in p for p in gw.body_problems(conv, GOOD_BODY.replace("[x]", "[ ]")))


def test_local_path_refused_but_images_allowed(conv):
    assert any("path" in p for p in gw.body_problems(conv, GOOD_BODY + "\nSee C:\\work\\log.txt\n"))
    assert gw.body_problems(conv, GOOD_BODY + "\n![shot](./scratch/shot.png)\n") == []


def test_closing_line_form(conv):
    assert any("closing" in p for p in gw.body_problems(conv, GOOD_BODY.replace("Fixes #3", "Fixes: 3")))


def test_ai_use_needs_a_model_unless_a_person_wrote_it(conv):
    assert any("Model" in p for p in gw.body_problems(conv, GOOD_BODY.replace("Claude Sonnet 5.5", "n/a")))
    person = GOOD_BODY.replace("an AI", "a person").replace("Claude Sonnet 5.5", "n/a")
    assert gw.body_problems(conv, person) == []


def test_docs_rule(conv):
    assert gw.docs_problems(conv, GOOD_BODY, ["src/a.py"])
    assert gw.docs_problems(conv, GOOD_BODY, ["src/a.py", "docs/a.md"]) == []
    assert gw.docs_problems(conv, GOOD_BODY, ["tests/a.py"]) == []
    assert gw.docs_problems(conv, GOOD_BODY + "\nDocs: none\n", ["src/a.py"]) == []


def test_render_is_stable_and_forms_are_valid_yaml(conv):
    files = gw.rendered_files(conv)
    assert ".github/ISSUE_TEMPLATE/bug.yml" in files
    form = yaml.safe_load(files[".github/ISSUE_TEMPLATE/task.yml"])
    assert form["title"] == "Task: " and form["labels"] == ["task", "S-needs-triage"]
    assert [b["id"] for b in form["body"] if "id" in b] == ["summary", "done", "steps", "blocked-by"]
    assert "blank_issues_enabled: false" in files[".github/ISSUE_TEMPLATE/config.yml"]
    assert gw.rendered_files(conv) == files


def test_validate_refuses_unknown_and_inconsistent(conv):
    assert gw.validate({**conv, "typo": 1})
    bad = yaml.safe_load(yaml.safe_dump(conv))
    bad["issues"]["forms"]["bug"]["labels"] = ["nonexistent"]
    assert any("nonexistent" in p for p in gw.validate(bad))
    bad = yaml.safe_load(yaml.safe_dump(conv))
    bad["labels"]["list"].append(bad["labels"]["list"][0])
    assert any("duplicate" in p for p in gw.validate(bad))


def test_load_refuses_bad_file(tmp_path):
    path = tmp_path / "c.yml"
    path.write_text("version: 1\nrepo: [1]\n", encoding="utf-8")
    with pytest.raises(gw.ConventionsError):
        gw.load(path)


def test_ruleset_and_settings_shapes(conv):
    rs = gw.ruleset_wanted(conv)
    kinds = {r["type"] for r in rs["rules"]}
    assert {"deletion", "non_fast_forward", "pull_request", "required_linear_history", "required_status_checks"} <= kinds
    norm = gw.normalise_ruleset(rs)
    assert norm["rules"]["required_status_checks"]["contexts"] == ["body", "docs", "title"]
    assert norm["rules"]["pull_request"]["methods"] == ["squash"]
    want = gw.settings_wanted(conv)
    assert want["allow_squash_merge"] and not want["allow_merge_commit"] and not want["allow_rebase_merge"]


def test_main_exit_codes(tmp_path, capsys, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert gw.main(["--conventions", "missing.yml", "validate"]) == 2
    assert gw.main(["--conventions", str(PACK / "conventions.yml"), "validate"]) == 0
