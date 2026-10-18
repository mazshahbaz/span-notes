# 001: Read bridge basics and feature tags from drawing sets

Issue: #3 · Tier: spike · Date: 2026-10-18 · Appetite: 90 min spike, then harden

## Phase spec (loose: aims the work, doesn't design it)

**Outcome:** for a drawing set in the Library, produce one record (basics, scope items, feature tags, each with its sheet)
without opening the PDF.

**In scope:**
- Read page text from the Library db (read-only, held-out excluded).
- Basics: type, number of spans, span arrangement, max span, foundation, abutment, staged.
- Feature tags from a first vocabulary with synonyms; scope items from rehab sheet titles and notes.
- Score basics against the existing hand-built index of the collection.

**No-gos (out of scope):**
- Re-OCR or image reading; costs; any write to the Library or Drive; data in the repo.

**Rough acceptance checks** (approximate; tightened at harden):
- Basics agree with the hand-built index on at least 80 % of fields over about 30 sets (source: the index spreadsheet in the
  Library, an independent hand entry).
- Feature tags at least 80 % precision on 10 sets checked by hand against the sheets (source: hand check, recorded locally in data/).

**Risks / rabbit holes:**
- OCR noise in dimension strings; span arrangement may only be readable from the GA elevation.
- Standard notes mention features not in the job: tag only from job-specific sheets and titles, or weight by sheet type.
- Hand-built index may itself have errors: log disagreements for review rather than assume the extractor is wrong.
