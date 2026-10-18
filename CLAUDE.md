# span-notes: Beam calcs practice for the AI Dev Course

## Commands
- Setup: `py -3 -m venv .venv` → `.venv/Scripts/python -m pip install -r requirements-dev.txt` (on this PC a bare `python` may be the Microsoft Store stub, so use `py -3` or the venv's python)
- Test: `.venv/Scripts/python -m pytest -q` (run before every commit; CI runs the same on every PR)

## Map
- `src/`: code · `tests/`: tests (one file per module)
- `docs/brief.md`: the project brief (problem, outcome, appetite) · `docs/specs/`: specs · `docs/decisions/`: ADRs · `docs/retros/`: retros
- `reference/`: originals, read-only (hook-enforced)
- `.claude/`: settings and hooks, the reviewer subagent, and the routine skills (`/session-start`, `/session-end`, `/new-issue`, `/cycle-close`, `/explain-back`)

## Rules (each with why)
- Work on a branch and land through a PR. main is protected, so every change gets reviewed.
- One issue per session. Start with `/session-start <issue>` and end with `/session-end`, so files carry the memory, not the chat.
- Tests first. Expected values come from an independent source cited in a comment (hand calc, table, code clause). A test that copies the code's output proves nothing.
- Never change an existing test's expected value, or delete or skip a test, without the engineer's explicit OK in this session. Otherwise a failing test gets "fixed" by weakening it.
- Never edit `reference/`. Originals are the evidence (enforced by `.claude/hooks/guard.py`).
- Arithmetic lives in functions with tests, never in prose. Numbers must be reproducible.
- No new plan, roadmap or status files. Work lives in GitHub issues and the project board, status in STATE.md. That keeps one plan.
- You may propose new issues (label `proposed`), but never reprioritise or close issues yourself. The engineer owns the plan.
- Keep PRs under about 400 changed lines, so they can be read.

## Session routine
- Start: `/session-start <issue>`. It reads STATE.md, git status and the issue, then plans in plan mode.
- End: `/session-end`. Tests pass → commit → STATE.md overwritten → PR opened or updated → issue commented.

## More detail
@docs/brief.md
