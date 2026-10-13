---
name: groundwork
description: Use when the user wants to set up, adopt or check a GitHub repository's conventions: rulesets and branch protection, labels, issue and pull request templates, CI workflows, MkDocs, hygiene and the sweep, merge settings, and the repository markdown files. Works on a new repository or an existing one, and interviews the user first.
---

# groundwork

Sets a repository up the way Coney is run (the reference: https://github.com/Ryubara/coney, its
`.github/conventions.yml` and `docs/guides/repo-conventions.md`). One file, `.github/conventions.yml`, is the
source of truth for every rule a program can check; the templates, labels, rulesets and workflows follow it.

## Modes

Ask which one, unless the user said:

- **new**: an empty or fresh repository. Interview, generate everything, apply the settings.
- **adopt**: an existing repository. Audit what is there against the pack, show a plan (what is missing, what
  differs, what would change), and apply only what the user approves. Never overwrite a file or a setting
  silently; show the diff first.
- **check**: no changes. Compare the repository to its `conventions.yml` and report the drift.

## Rules for you

- **Ask before every outward-facing change**: creating or changing a ruleset, branch protection, labels, merge
  settings, secrets, a schedule, or pushing. Show the exact `gh` commands or API calls first.
- Work on a branch and open a pull request for files in an existing repository; do not push to its default
  branch.
- Take wording and structure from the reference, but never copy project-specific text (names, domain rules,
  legal text). Replace each `{{placeholder}}` in `pack/` from the interview, and ask when you cannot tell.
- Prefer enforcement to instruction: a rule that a check, ruleset or hook can enforce goes there, not only in a
  guide.

## Steps

1. **Look first.** `gh repo view`, the default branch, existing `.github/`, workflows, labels, rulesets
   (`gh api repos/{owner}/{repo}/rulesets`), the language and build files, docs. Say what you found.
2. **Interview** (one short round, with sensible defaults offered): project name and one-line purpose;
   language and build tool; default branch; merge style (squash only is the reference); auto-merge on or off;
   commit and pull request title format (the reference: `area: Verb the rest`, areas you choose); labels
   (areas, kinds, status); issue forms (bug, task); whether to use a documentation site (MkDocs) and where it
   deploys; hygiene and a scheduled pull request sweep; required checks; licence and security contact; who may
   decide what (the "maintainer decisions" list).
3. **Generate** from `pack/` and the reference: `.github/conventions.yml`, issue forms, the pull request
   template, workflows (title/body checks, build, docs, hygiene, issue status), `CONTRIBUTING.md`,
   `SECURITY.md`, `CODE_OF_CONDUCT.md` (the Contributor Covenant), `.gitattributes`, `.editorconfig`,
   `mkdocs.yml` if wanted, and the labels file.
4. **Apply settings** with `gh` after confirmation: the ruleset for the default branch (no direct pushes,
   required checks, linear history if squash-only), merge options, labels, the schedule.
5. **Verify**: run the generated checks locally where possible, list what was applied, and what the user still
   has to do by hand (anything the token could not change).

See `DESIGN.md` for what is built and what is planned.
