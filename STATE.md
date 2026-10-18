# STATE (overwrite each session; keep under 3 KB)

Updated: 2026-10-18 · Branch: 2-brief · Milestone: none yet

## Now
- Project repurposed: bridge drawing and rehab database read from the Library (brief + spec 001 in PR #7, review 0 must-fix).
- #3 spike done. Decision: DROP rules for basics, HARDEN rules for feature tags, spike 2 (model reading) proposed.

## Next
1. Engineer merges PR #7.
2. Engineer decides spike 2's reader: API key on this PC, or in-session agents (~3M tokens for 425 sets, estimate).
3. Harden feature tags (#3 / #4): fix 'bolted splice', add missed tags, per-tag precision, engineer hand-check of 10 sets.

## Blocked / waiting on Mazen
- #3 needs-mazen: reader/cost decision for spike 2; abutment definition for rehabs (existing vs after work).
- Repo is public: data stays in data/ (git-ignored). Consider making it private.

## Known issues
- 16 of 425 sets have no usable text (failed OCR in the Library), logged K-030.
- Board has no Review column (K-032).

## Last measured result
- Basics by rules: 55 % (416 sets). Model, first 3 sheets: 78 % right when answered, 84 % answered (30 sets).
- Feature tags by rules: 80 % precision (10 sets, agent check, VERIFY).
Rules: one issue per session (/workbench:session-start <n> ... /workbench:session-end); WIP limit 2; tests first with cited expected values, never weaken a test; branch + PR only; propose new work as issues, don't create plan files; hand off at ~55% context.
