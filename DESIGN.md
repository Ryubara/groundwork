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

## Built so far (0.1.0)

The skill (`skills/groundwork/SKILL.md`: modes, rules, steps) and the static, portable files in `pack/`.

## Planned

1. A portable checker (title, body, labels, hygiene) so a generated repository needs nothing from Coney.
2. The workflow templates, parameterised by language and by the interview.
3. `adopt` mode's audit and plan output; `check` mode's drift report.
4. Extracting the generic parts of `conventions.yml` and `docs/guides/repo-conventions.md` into the pack.
5. Dogfooding: adopt Tether and Coney with it.
