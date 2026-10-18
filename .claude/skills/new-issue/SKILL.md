---
name: new-issue
description: Turn an idea into a well-formed GitHub issue with a measurable done-when. Run with /new-issue <idea>. Also use it whenever you want to propose new work instead of starting it.
argument-hint: [idea]
---
Turn this idea into one GitHub issue: $ARGUMENTS

1. Search first: `gh issue list --search "<keywords>" --state all`, and grep the repo for code that already does part of it. If it exists, say so and stop.
2. Draft the issue using `.github/ISSUE_TEMPLATE/task.md`: a one-line goal, "Done when" as a check that can be run, files likely touched, and size S/M/L. An L must be split into several issues.
3. Show the draft to the engineer. Only after an OK, create it: `gh issue create --title "..." --body "..." --label proposed`.
4. Never start work on it in this session, and never change other issues' priority or milestone.
