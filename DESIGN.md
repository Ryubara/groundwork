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

## Built in 0.2.0

- The skill (`skills/groundwork/SKILL.md`: modes, rules, steps).
- The portable checker, `pack/.github/scripts/groundwork.py` (standard library plus PyYAML): `validate`,
  `check-title`, `check-body`, `check-docs`, `render` (and `--check`), `labels`, `settings`, `ruleset`, `hygiene`
  and `check` (drift). Tested in `tests/` and in CI.
- The pack: `conventions.yml`, the workflows (`pr`, `issue-status`, `hygiene`, `conventions`), optional CI for
  Python and Node, `CONTRIBUTING.md`, `SECURITY.md`, `.gitattributes`, `.editorconfig`.
- The pull request template and the issue forms are generated from `conventions.yml`, never hand-edited.

## Added in 0.3.0 (Coney's later conventions that any repository can use)

- `check-commits` / `check-message`: the only trailer is an AI `Co-Authored-By` with a vendor noreply address, no
  other e-mail address appears in a message, and the description's model line names every trailer's model
  (`commits.trailers`, `pull_requests.ai_use.model.names_trailer_models`). Run on every pull request and at the
  commit-msg stage.
- Generated blocks in hand-written files (`paths.blocks_in`): `commit-rules`, `maintainer-decisions`,
  `manual-paths`, rewritten by `render` and checked by `render --check`, so `AGENTS.md` never drifts from the rules.
- Pointer files (`paths.pointer_files`): `CLAUDE.md` and `GEMINI.md` hold only `@AGENTS.md` (`check-files`).
- Manual paths (`merge.manual_paths`) and `needs-maintainer`: the rules that judge agents are merged by a person.
- `pr.yml` on `pull_request_target` under four safety rules; changed files and commits read from the API.
- `ci-failure.yml`: a red default branch opens or updates one P-critical issue.
- pre-commit (file hygiene, large files, markdownlint, title, trailers, render) and markdownlint settings.
- Optional docs site: `docs.yml` (strict MkDocs build, markdownlint, actionlint, Pages deploy) and `mkdocs.yml`.
- Screenshots rule (0.4.0): a pull request whose title area is visual (`pull_requests.screenshots.areas`) carries an
  uploaded capture in its Screenshots section, or `Screenshots: none (reason)`; `check-body --title`.

## Added in 0.5.0 (Coney's issue and pull request structure)

- Issues affected (`pull_requests.issues_affected`): a `## Issues affected` section lists every other open issue the
  change partly fixes or makes out of date, one `#N: how` line each, or `None (reason)`; the coordinator updates
  those issues after the merge.
- Before and after (`pull_requests.screenshots.before_after`): a visual pull request uploads a `Before:` and an
  `After:` capture, or writes `Before: none (reason)` for something new.
- Failed first (`pull_requests.failed_first`): a pull request whose title verb is `Fix` has a `Failed first:` line in
  Testing naming the test that failed before and passes after, or `Failed first: none (reason)`.
- The task form has a required From line, an Area dropdown, a Docs page link and a "done" hint for bug fixes. The
  area labels (`A-<area>`) are generated from the title areas (`labels.families.area.from_title_areas`), synced by
  `labels`, and applied from the dropdown by the `issue-area` workflow (`groundwork.py issue-area`).
- Coney's priority and status labels for agent claims and its `Runtime:` evidence line stay in Coney.

Left in Coney, as specific to running many agents on reverse engineering: roles and identity tokens, claims and
slots, the stamped task check and review pipeline, opening pull requests only through a tool, the audit registry,
stacked pull requests and dated checklist rules.

## Planned

1. `adopt` mode's audit and plan output as a command (today the skill compares by hand and `check` reports drift).
2. More language CI templates.
3. Per-item hygiene comments (the weekly report is built; Coney also comments on each item on events).
4. Coney's deeper checks (stacked pull requests, checklists by date, review gates) stay in Coney until a second
   project wants them.
