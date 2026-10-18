---
name: explain-back
description: Quiz the engineer on the current branch's diff before merging, so they understand what they are approving. Run with /explain-back.
disable-model-invocation: true
---
1. Read the diff: `git diff main...HEAD`.
2. Ask the engineer 3 questions they should be able to answer if they understand the change: what changed, why, and how they would know it's broken. Ask one at a time.
3. Do not give the answers until they have replied. Then correct or confirm each, briefly.
4. Offer a 3-sentence explain-back for the PR description, in their words where possible.
