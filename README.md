# span-notes

Beam calcs practice for the AI Dev Course

Status: active · Started 2026-10-18 · Owner: Mazen Chaaraoui

## Install and test
```bash
py -3 -m venv .venv
```
```bash
.venv/Scripts/python -m pip install -r requirements-dev.txt
```
```bash
.venv/Scripts/python -m pytest -q
```

## Where things are
| Path | Holds |
|---|---|
| `docs/brief.md` | Why this project exists, the outcome number, the appetite |
| `docs/specs/` | One spec per feature, with acceptance checks |
| `docs/decisions/` | Architecture decision records (ADRs) |
| `STATE.md` | Where the work stands now |
| `CHANGELOG.md` | What changed in each release |
| `.claude/` | How Claude works in this repo: settings, hooks, skills, reviewer agent |

Made with the AI Dev Course starter kit.
