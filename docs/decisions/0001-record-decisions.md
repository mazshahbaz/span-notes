# 0001: Record architecture decisions

Date: 2026-10-18 · Status: accepted

## Context
Decisions get made in chat sessions and then forgotten. A later session (or a later you) re-decides them, or undoes them without knowing why they were made.

## Decision
Every decision that changes how the project is built (a library, a data format, a method, a boundary) gets a short ADR in `docs/decisions/`, numbered in order. An accepted ADR is never edited. A change of mind gets a new ADR that supersedes it.

## Consequences
- The "why" survives across sessions and machines.
- Claude reads the ADRs before proposing changes in the same area.
- It costs about 10 minutes per decision.
