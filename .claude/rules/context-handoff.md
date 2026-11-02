# Context handoff rules

## Main handoff document

[CURRENT_STATE.md](../../CURRENT_STATE.md) is the main handoff document. A new
session should be able to resume from it plus the documents it links to.

## Updating CURRENT_STATE.md

- Keep it concise: the current objective, completed steps, pending items,
  blockers and unknowns, and the next step. Put detail in the linked
  documents, not here.
- Record a step as completed **only after it has been verified.** If a step
  was only partly verified, say exactly what is still unverified (for
  example, "Mermaid source inspected; visual rendering pending").
- Never record an unreviewed result as reviewed or approved. Approval status
  changes only when the Architect, researcher, or professor actually gives
  that approval.
- Every completed task ends with exactly **one** next recommended step.

## Decision statuses

[DECISIONS.md](../../DECISIONS.md) uses three statuses. Keep them distinct:

| Status | Meaning |
|---|---|
| `ACCEPTED` | Confirmed fact or scope boundary given by the project |
| `PROVISIONAL` | Proposed design choice, open to change |
| `OPEN` | Unresolved question |

## Scope of edits

- Update only the documents the current task needs. Do not rewrite or reformat
  unrelated documents after every task "for consistency".
