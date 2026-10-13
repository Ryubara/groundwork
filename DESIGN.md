# Groundwork design

## Goal

Create a repository exactly like Coney is set up, quickly, by a skill that works with the user at the start,
and keep it that way afterwards. Works on a new repository and on an existing one.

## What Coney has that Groundwork must cover

| Area | Coney's source | Groundwork output |
|---|---|---|
| Rules as data | `.github/conventions.yml`, read by `coney-tools` | `conventions.yml` plus a small portable checker (no dependency on `coney-tools`) |
| Commit and PR titles | `area: Verb the rest`, areas, verbs, 72 columns | a title check in `pr.yml`, with the areas from the interview |
| PR description | a template with required sections, `Docs: none` escape | the template and a body check |
| Issues | forms (`bug.yml`, `task.yml`), no blank issues, status labels | the forms and the label set |
| Labels | defined in `conventions.yml`, synced | a labels file and a sync step |
| Rulesets | `main` protected, required checks, squash only | `gh api` calls, shown first |
| CI | build, python, docs, pr, hygiene, issue-status workflows | the workflows that apply to the language |
| Docs | MkDocs site, strict build, deploy | optional `mkdocs.yml` and `docs.yml` |
| Hygiene | `repo-hygiene` audit and a scheduled sweep | a scheduled workflow and the audit script |
| Markdown files | `CONTRIBUTING`, `SECURITY`, `CODE_OF_CONDUCT`, README | templates in `pack/` |
| Maintainer decisions | `owner_decisions` list in `conventions.yml` | asked in the interview |

## Built so far (0.2.0)

- The skill (`skills/groundwork/SKILL.md`: modes, rules, steps).
- The portable checker, `pack/.github/scripts/groundwork.py` (standard library plus PyYAML): `validate`,
  `check-title`, `check-body`, `check-docs`, `render` (and `--check`), `labels`, `settings`, `ruleset`, `hygiene`
  and `check` (drift). Tested in `tests/` and in CI.
- The pack: `conventions.yml`, the workflows (`pr`, `issue-status`, `hygiene`, `conventions`), optional CI for
  Python and Node, `CONTRIBUTING.md`, `SECURITY.md`, `.gitattributes`, `.editorconfig`.
- The pull request template and the issue forms are generated from `conventions.yml`, never hand-edited.

## Planned

1. `adopt` mode's audit and plan output as a command (today the skill compares by hand and `check` reports drift).
2. Optional MkDocs files and a docs workflow; more language CI templates.
3. Per-item hygiene comments (the weekly report is built; Coney also comments on each item on events).
4. Coney's deeper checks (stacked pull requests, checklists by date, review gates) stay in Coney until a second
   project wants them.
