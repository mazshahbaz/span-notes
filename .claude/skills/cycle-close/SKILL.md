---
name: cycle-close
description: Close a cycle (milestone) or run the weekly retro. Run with /cycle-close [milestone] when all the milestone's issues have landed, or weekly for a retro.
argument-hint: [milestone]
disable-model-invocation: true
---
Close the cycle $ARGUMENTS (or, with no argument, draft this week's retro).

1. Gather: `gh issue list --milestone "$ARGUMENTS" --state all`, merged PRs (`gh pr list --state merged --limit 30`), `CHANGELOG.md`, `STATE.md`.
2. Measure: run the full test suite and any measurement the brief or milestone names. Report the number against its target.
3. Draft `docs/retros/<date>-<milestone>.md` from `docs/retros/000-template.md`: Proven / Built but not proven / Cut / Rules broken / Usage / Next / Lessons to promote.
4. Draft the CHANGELOG entry (Added / Changed / Fixed / Removed / Measured) and propose the version tag.
5. Show everything to the engineer. Only after an OK: commit, `git tag vX.Y.0`, `git push --tags`, and close the milestone.
6. List any lesson that should become a hook, a test or a CLAUDE.md rule, as proposed issues (use /new-issue).
