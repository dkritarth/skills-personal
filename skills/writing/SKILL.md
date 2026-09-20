---
name: writing
version: 0.2.0
description: Track manuscript draft revisions across sessions. Maintains an append-only journal (.writing-journal.md) backed by git history to compare planned edits against actual changes, surface trajectory drift, and keep research drafts aligned.
license: MIT
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion]
disable-model-invocation: true
---

# Writing

Persistent intent tracking for research manuscripts and proof drafts across multiple editing sessions.

This skill tracks forward intent via `.writing-journal.md`. At the start of every session, it inspects the journal and git diffs to generate a brief comparing where the draft was planned to go versus where recent edits actually went.

## Comparison to other skills

- `academic-humanizer` and `research-paper-writing`: Stateless single-pass prose editors. They refine clarity and tone for current text without tracking history across sessions. Use `writing` to plan and track direction, then hand text to `academic-humanizer` for prose polishing.
- Retrospective diff tools: Summarize past commits after they happen. `writing` tracks future intent, checking git diffs against previously stated plans to catch unannounced changes in direction.

## When to use

- Resuming work on an existing paper, proof, or grant draft with an active `.writing-journal.md`.
- Starting the first tracked session on a multi-session draft.
- Checking whether planned edits match earlier intentions before making changes.

## When not to use

- Single-pass prose or grammar polish. Use `academic-humanizer`.
- Drafting a completely new outline from scratch with no prior history.
- Disposable one-off documents like emails or quick abstracts.

## Journal storage: `.writing-journal.md`

- Location: `<draft-root>/.writing-journal.md` directly alongside the manuscript. Keep it in git with the paper repository.
- Format: Append-only markdown. Entries follow `reference/journal-entry-template.md`:
  - ISO-8601 UTC timestamp heading.
  - What changed: one sentence on substantive structural or technical edits (not a diff dump).
  - Why: reason for the change.
  - Stated direction: next planned steps, concrete enough to test in subsequent sessions.
- Do not edit historical entries. If correcting a past error, append a new entry explaining the correction.
- Drift detection outcomes:
  1. Aligned: Recent git changes match stated direction. Proceed to edits.
  2. Drifted: Git changes diverge from earlier direction. Alert the user before editing: note the discrepancy and ask whether this is an intentional pivot.
  3. No signal: Document is uncommitted or untouched in git since the last timestamp. Flag this as unverified drift risk.

## Process

1. Check for `<draft-root>/.writing-journal.md`. If missing, run `scripts/init_journal.sh <draft-root>` and note that tracking begins now.
2. Gather history by running `scripts/gather_context.sh <manuscript-path> [n-commits]`. Inspect the journal and git commit logs for the file.
3. Formulate the trajectory brief: Summarize previous planned steps, actual git diffs, and alignment status. Present this brief before making edits.
4. If drifted, ask the user to clarify whether to adopt the new direction or return to the original plan.
5. Apply the requested manuscript edits:
   - For prose refinement, use `academic-humanizer`.
   - For LaTeX compilation errors or bibliography format, use `latex`.
   - For symbolic and algebraic proof verification, use `math`.
6. Record the session outcome by running `scripts/append_entry.sh <draft-root> "<what>" "<why>" "<direction>"` with specific, testable next steps.

## Scripts

Plain bash scripts located in `scripts/`:

- `init_journal.sh <draft-root>`: Creates the journal file with header if absent.
- `gather_context.sh <manuscript-path> [n-commits]`: Outputs the journal content and recent git diffs.
- `append_entry.sh <draft-root> <what> <why> <direction>`: Appends an entry and fails if the journal file is missing.
