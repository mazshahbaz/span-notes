---
name: session-end
description: End-of-session routine for this repo. Run with /session-end before stopping or clearing context.
disable-model-invocation: true
---
Close this work session cleanly, so a fresh session can continue from the files alone.

1. Run `.venv/Scripts/python -m pytest -q` and show the summary line. If anything fails, stop and report; do not weaken tests.
2. Commit the work with a message naming the issue: `Verb what changed (#<issue>)`.
3. Overwrite `STATE.md` (under 3 KB): Now / Next / Blocked or waiting on Mazen / Known issues / Last measured result / Usage.
4. Push the branch and open or update the PR with `gh pr create --fill` (or `gh pr edit`), filling the PR template's What / Why / How tested sections. Leave the explain-back section for the engineer.
5. Comment a 3-line progress note on the issue: `gh issue comment <issue> --body "..."`.
6. Tell the engineer the context % used (`/context`) and suggest `/clear` before the next task.
