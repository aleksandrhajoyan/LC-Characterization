# Architecture review rules

These rules apply to any change that touches the PhotonicsAI architecture:
components, agent roles, tools/skills, communication routes, human
checkpoints, safety boundaries, data contracts, or diagrams.

## Review gate

- An architecture change needs explicit review by **both** the Architect and
  the researcher before it counts as part of the design. If a task does not
  authorize a change, propose it in the task report instead of editing.
- Anything not yet approved by the professor stays `PROPOSED` (or
  `PROVISIONAL` in [DECISIONS.md](../../DECISIONS.md)). Reviewing,
  documenting, or polishing a design does not change its approval status.

## Facts stay facts

- Confirmed facts (`ACCEPTED` in DECISIONS.md) must not quietly turn into
  assumptions. Do not weaken their wording, hedge them, or move them under a
  "proposed" heading.
- The reverse also holds: a proposal or assumption must not quietly turn into
  a fact. If you are unsure about a statement's status, mark it `OPEN` and
  raise it.

## Cross-document consistency

Every documentation change must stay consistent with:

- [AGENTS.md](../../AGENTS.md): roles, tools, skills, and forbidden actions
- [ARCHITECTURE.md](../../ARCHITECTURE.md): components, routes, checkpoints,
  and layers
- [DECISIONS.md](../../DECISIONS.md): statuses and open questions
- [DATA_CONTRACTS.md](../../DATA_CONTRACTS.md): artifact names and fields

If an edit to one of these documents would contradict another that you are
not allowed to change in the current task, stop and report the conflict.

## Diagram validation honesty

- Reading or checking `.mmd` source is **source inspection**, not visual
  validation.
- Say a diagram is "visually validated" only after it has actually been
  rendered and looked at. Otherwise, state that visual validation is pending.
- Do not install a renderer just to validate a diagram unless the task
  authorizes it.
