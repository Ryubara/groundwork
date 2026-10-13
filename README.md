# Groundwork

A Claude Code skill that sets up a GitHub repository the way [Coney](https://github.com/Ryubara/coney) is run
with branch protection and rulesets, labels, issue and pull request templates, CI, an optional documentation site,
hygiene and a scheduled sweep, merge settings and the repository's markdown files, all driven from one
`conventions.yml`. It interviews you first, works on a new repository or an existing one, and asks before it
changes anything outside the files.

> **Status: 0.2.0.** The skill, the portable checker and the workflow templates exist and are tested on a scratch
> repository. See [DESIGN.md](DESIGN.md) for what is built and what is planned.

## Install

```
/plugin marketplace add Ryubara/groundwork
/plugin install groundwork@groundwork
```

Then ask Claude to set up, adopt or check a repository, or run the skill (`/groundwork:groundwork`).

## Modes

- **new**: generate everything for a fresh repository.
- **adopt**: audit an existing repository, show a plan, apply only what you approve.
- **check**: report drift from `conventions.yml`, change nothing.

## Licence

MIT.
