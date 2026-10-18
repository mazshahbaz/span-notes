---
name: session-start
description: Start-of-session routine for this repo. Run with /session-start <issue-number> at the beginning of every work session.
argument-hint: [issue-number]
disable-model-invocation: true
---
Start a work session on issue $ARGUMENTS.

1. Read `STATE.md`. Run `git status` and `git log --oneline -5`.
2. Read the issue: `gh issue view $ARGUMENTS` (if `gh` is not available, ask the engineer to paste it).
3. Read any spec or ADR the issue names (`docs/specs/`, `docs/decisions/`).
4. If on `main`, propose a branch name `$ARGUMENTS-<short-slug>` and create it with `git switch -c` after the engineer agrees. If the issue is a parallel lane, propose a worktree instead: `git worktree add ../<repo>-$ARGUMENTS -b $ARGUMENTS-<slug>`.
5. Summarise in 5 lines: where the project stands, what the issue needs, its "done when", the files it touches, and the risks.
6. Propose a plan with the tests first (expected values from independent sources). Do not edit anything until the engineer approves the plan.
