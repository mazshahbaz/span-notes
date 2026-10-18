# span-notes: Beam calcs practice for the AI Dev Course

Runs on the **workbench** (`.claude/workbench.json`; manual: `/workbench`). Tiers, autopilot, review rules and gates follow MASTER.md.

## Commands
- Setup: `py -3 -m venv .venv` → `.venv/Scripts/python -m pip install -r requirements-dev.txt` (on this PC a bare `python` is the Microsoft Store stub, so use `py -3` or the venv's python)
- Test: `.venv/Scripts/python -m pytest -q` (CI runs the same on every PR, and it's a required check)

## Map
- `src/`: code · `tests/`: tests (one file per module)
- `docs/brief.md`: the project brief · `docs/specs/`: phase specs, hardened at harden · `docs/decisions/`: ADRs · `docs/retros/`: retros
- `reference/`: originals, read-only (hook-enforced)

## Rules (each with why)
- Work on a branch and land through a PR. main is protected, so every change gets reviewed.
- Every issue has a tier (`tier:spike|normal|critical`). Spikes are fast and never merge; normal work gets tests for what's costly plus one review pass. That keeps speed where mistakes are cheap.
- Expected values in tests come from an independent cited source (hand calc, beam table, code clause), never the code's own output, so tests prove something.
- Never change an existing test's expected value, or delete or skip a test, without the engineer's explicit OK. Otherwise a failing test gets "fixed" by weakening it.
- No new plan, roadmap or status files: issues, the board and STATE.md hold the plan, so there's one plan.
- Propose new issues (label `proposed`), but never reprioritise or close them. The engineer owns the plan.

## Routine
- Hands-off: `/workbench:run <issue>` (spec → spike → keep/harden/drop → hardened spec → tests → one review → PR).
- Step by step: `/workbench:session-start <issue>` … `/workbench:session-end`.
- New work: `/workbench:new-issue <idea>` · Progress: `/workbench:status` · Before merging: `/workbench:explain-back`.

## More detail
@docs/brief.md
