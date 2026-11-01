# AGENTS.md -- {{project_name}}

{{one_line_purpose}}

## Layout

{{where things live: source, tests, docs, tools}}

## Build and test

{{the commands that build and test, and the checks to run before a pull request}}

## Rules (never broken)

<!-- conventions:begin maintainer-decisions -->
<!-- conventions:end -->

## Commits and pull requests

Every rule a program checks is a key of `.github/conventions.yml`, the one source. The blocks below are generated
from it (`groundwork.py render`): edit the file, not the block.

<!-- conventions:begin commit-rules -->
<!-- conventions:end -->

Work happens on branches, one pull request per change, squash-merged; the default branch takes no direct pushes.

<!-- conventions:begin manual-paths -->
<!-- conventions:end -->
