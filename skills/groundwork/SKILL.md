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
3. **Generate.** Copy `pack/` into the repository (the skill's directory holds it; use `${CLAUDE_PLUGIN_ROOT}/pack` or
   the path you were loaded from): `.github/conventions.yml`, `.github/scripts/groundwork.py`, the workflows
   (`pr.yml`, `issue-status.yml`, `hygiene.yml`, `conventions.yml`, `ci-failure.yml`), `SECURITY.md`,
   `CONTRIBUTING.md`, `AGENTS.md` and `CLAUDE.md` (a pointer to it), `.pre-commit-config.yaml`,
   `.markdownlint.yaml`, `.markdownlint-cli2.yaml`, `.gitattributes`, `.editorconfig`,
   `.github/ISSUE_TEMPLATE/config.yml`. Add the language's CI from `pack/optional/` (`ci-python`, `ci-node`, or
   `ci-none` when there is nothing to build yet) as `.github/workflows/ci.yml` (its last job must be `build-ok`), and
   for a documentation site `docs.yml` (as `.github/workflows/docs.yml`), `mkdocs.yml` and `requirements-docs.txt`.
   Edit `conventions.yml` from the interview (areas, labels, forms, required checks, paths, manual paths, the
   trailers' noreply addresses, the sweep's cron in both the file and `hygiene.yml`; `ci-failure.yml` lists the
   workflows it watches), fill each `{{placeholder}}`, and fill `CODE_OF_CONDUCT.md` (the Contributor Covenant 2.1;
   the pack has it, with one placeholder for the enforcement contact). Then render what follows the conventions,
   including the generated blocks of `AGENTS.md` and `CONTRIBUTING.md`:
   `uv run --with pyyaml python .github/scripts/groundwork.py render`, and install the commit hooks:
   `uvx pre-commit install`.
4. **Apply settings** after confirmation, each showing what it would change first (no `--apply`) and then with it:
   `groundwork.py labels --apply`, `groundwork.py settings --apply`, `groundwork.py ruleset --apply`. The ruleset
   names the required checks, which must exist as workflow jobs (`title`, `body`, `docs`, `build-ok`); apply it
   after the first pull request has run them, or GitHub cannot offer them.
5. **Verify**: `groundwork.py check` (drift in files, labels, settings and ruleset), then open a test issue from
   each form and a test pull request with a bad title, a bad description and a good one, and confirm the checks
   refuse and pass as expected. List what was applied, and what the user still has to do by hand (anything the
   token could not change: for example Actions permissions or secrets).

## Keeping a repository this way

The checker is the enforcement: `check-title`, `check-body`, `check-docs` and `check-commits` (trailers, e-mail
addresses, the model line) run on every pull request, on `pull_request_target` so a fork's pull request is checked
the first time (`pr.yml` explains the four rules that make that safe); `render --check` fails a pull request that
edits a generated file or block by hand, and `check-files` one that grows a pointer file; pre-commit runs the title,
trailer and render checks before a commit exists; `ci-failure` opens a P-critical issue when the default branch goes
red; `issue-status` keeps labels honest, and the weekly `hygiene` sweep reports idle or malformed issues and pull
requests on one issue. `needs-maintainer` tells a tool or an agent hook that a pull request touches a manual path,
so it must not turn on auto-merge: GitHub cannot tell an agent from the person whose token it uses, so that rule is
enforced on the agent's side. To change a rule, edit `conventions.yml`, run `render`, apply what changed, and commit
them together.

See `DESIGN.md` for what is built and what is planned.
