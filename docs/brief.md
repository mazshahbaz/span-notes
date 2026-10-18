# Project brief: span-notes (bridge drawing and rehab database)

Date: 2026-10-18 · Owner: Mazen Chaaraoui · Status: active

## Problem
The engineer's Library holds hundreds of complete bridge drawing sets (new bridges and rehabs), most with no report and no cost.
Finding "a past job with rock anchors at an abutment" or "two-span steel girder rehabs with bearing replacement" today means
remembering the job or opening sets one by one, and a Class D cost for a scope has to be built from scratch each time.
A hand-built index covers type, spans and foundations for part of one collection, but not scope, special features or cost.

## Outcome (measurable)
For any drawing set in the collection, a record of its basics (type, spans, foundation, abutment, staging), its rehab scope
items and special-feature tags, each with the sheet it came from, and later an estimated cost range.
Measured by: basics agree with the existing hand-built index on at least 80 % of fields, and feature tags reach at least
80 % precision on a hand-checked sample (both thresholds are first guesses, to be tested at the spike).

## Appetite
4 weekends. This is a budget, not an estimate. When it's spent, cut scope or stop. Don't extend.

## In scope
- Reading drawing-set text already extracted in the Library (digital and OCR), read-only.
- Bridge basics, rehab scope items, special-feature tags from a controlled vocabulary with synonyms, sheet references.
- A local database and simple search over it.
- Later slice: estimated cost ranges (quantities times unit rates from the Library, escalated), calibrated on jobs with tender costs.

## Not doing (out of scope)
- Re-OCR or image reading of drawings (use the Library's text; revisit only if the spike shows text is too poor).
- Writing to the Library or to Drive.
- Engineering numbers for a deliverable: outputs are search aids and Class D ranges, marked as estimates.
- Held-out documents (excluded in every query).

## Data and governance
| Data | Owner | Where it may live | Notes |
|---|---|---|---|
| Drawing-set text, index spreadsheets | Firm / owners of the drawings | The Library db on this PC, read-only | Never copied into the repo |
| Extracted records, database, run outputs | Firm | `data/` on this PC (git-ignored) | Never committed, never in issues or PRs |
| Code, synthetic test fixtures, tag vocabulary | Engineer | This repo | This repo is public: no bridge names, contract numbers or extracted values |
Firm or client data goes in firm-controlled accounts only. Confirm with: the principal before any data leaves this PC.

## Risks and kill criteria
- OCR text of drawings may be too noisy to read spans and types. Stop if two spikes can't reach 60 % field agreement with the index.
- Feature words appear in standard notes and specs without the feature being in the job (false positives).
- Stop if the cost slice's blind error on jobs with tender costs is worse than ±50 % after one calibration pass.

## First slice (walking skeleton)
Issue #3: read basics and feature tags from about 30 sets the hand-built index describes, score field agreement, and hand-check
feature tags on 10 sets.

## Result (filled in at close)
Outcome achieved: <value> · Date closed: · Lessons: see docs/retro-final.md
