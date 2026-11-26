# PhotonicsAI — Architecture v0.2 Draft

_Recorded: 2026-11-26 · C01 · Status: PROPOSED_

## 1. Status and scientific objective

Characterize a voltage-controlled liquid-crystal (LC) scattering cell as a
black box. Candidate observables include optical response versus voltage,
switching behavior, and speckle statistics; the first metric is OPEN.

This is the current proposed architecture direction supplied by the
researcher/ChatGPT Architect for C01. Professor Nikita positively reviewed
the revised direction, as reported by the researcher. That feedback is not
blanket approval of device automation, runtime implementation, safety limits,
or experiments. No working agents, runtime code, device integration, or
validated hardware limits exist in this project.

The [v0.1 architecture](../ARCHITECTURE.md), [roles](../AGENTS.md),
[decisions](../DECISIONS.md), [contracts](../DATA_CONTRACTS.md), and existing
diagrams remain historical proposals wherever they contradict this draft.
They have not been migrated by C01. Development restrictions still apply;
this draft grants no permission to execute software or access hardware.

**Transmission Matrix Retrieval remains excluded pending clarification.**
Professor Nikita subsequently suggested a transmission-matrix experiment as
a possible planning test. This is a reported suggestion, not a confirmed
research-scope change or permission to implement or run it.

## 2. Three-agent responsibility matrix — PROPOSED

| Scientific agent | Responsibility | Main contribution and boundary |
|---|---|---|
| Scientist | Literature, hypotheses, method selection, scientific justification, interpretation of conclusions | Justifies a characterization method and interprets its scientific implications; literature values are references, not approved device settings |
| Experimentalist | Physical setup, SDK and equipment-capability knowledge; adaptation to the lab; procedure and necessary execution-code design; technical quality control and equipment troubleshooting; reuse of validated procedures | Produces a laboratory procedure and technical requirements based on verified equipment evidence; the role does not imply that SDKs or capabilities have already been verified or that execution is authorized |
| Analyst | Receives actual measurements and required metadata; independently selects justified analysis methods; reproducible calculations, statistics, and reporting | Produces reproducible analysis with uncertainty and limitations, and requests missing information; does not fabricate measurements or silently assume missing metadata |

Standalone Executioner and Scientific Reviewer are removed from the proposed
scientific core. Scientific interpretation, technical quality control, and
analysis remain explicit responsibilities of the three roles above, with
human decisions and deterministic restrictions preserved.

Codex is the **development coder**, not a runtime scientific agent. This
draft does not establish a separate runtime Coder role.

## 3. Hybrid Local Orchestrator — PROPOSED

The Local Orchestrator coordinates workflow, experiment history, important
state changes, and approvals. It facilitates external knowledge discovery
while keeping control and authorization deterministic.

Agents may directly clarify technical questions with each other. The
Orchestrator does not relay every conversational message. Clarification
cannot itself grant authorization or silently change an approved procedure;
consequential state changes and approvals belong in the coordinated record.
The exact recording boundary and mechanism remain OPEN.

No framework, concrete API, database, or LLM provider is selected here.
The reasoning/discovery mechanism and any future external Chief Orchestrator
interface remain OPEN; neither may bypass human authorization or hard limits.

## 4. Shared knowledge catalogue — PROPOSED

A shared catalogue shows what knowledge exists and who owns it:

- Scientist owns scientific-method knowledge and supporting literature.
- Experimentalist owns equipment and experimental-procedure knowledge.
- Analyst owns analysis-method knowledge.

Knowledge may support cross-role clarification without erasing ownership.
Sources and verification status must remain distinguishable. Unverified
scientific values must never become approved equipment limits. Catalogue
format, storage, update responsibilities in detail, and access mechanisms
are OPEN; no knowledge infrastructure is implemented.

## 5. Reusable experimental procedures — PROPOSED

The proposed procedure/Skill lifecycle is:

**Draft → Validated → Approved for reuse**

Keep provenance, version, applicable conditions, and verification evidence
with each procedure. Experimentalist owns procedure knowledge and reuses
validated procedures within their documented conditions. Validation criteria,
approval authority, and treatment of revisions remain OPEN; status must not
be inferred from a plausible description or a literature example.

Approval for reuse does not automatically authorize unattended execution.
Future unattended reuse is a goal requiring separate authorization and
validated enforcement, not an existing permission or implemented feature.

## 6. Safety and human-control policy

Initial real laboratory operations remain human-controlled and require
authorization. Deterministic hardware restrictions and command-level
enforcement are mandatory requirements, not implemented safeguards in this
repository. Unknown or unapproved commands/settings must not be executed.

An AI-assisted reviewer may supplement checks but cannot override hard
constraints or grant itself authority. It is not a restored standalone
Scientific Reviewer in the scientific core. The enforcement implementation,
command permissions, approval scope, and stop/abort mechanism remain OPEN.

No hardware limits have been validated and no hardware software-control
interfaces have been established by this project. Operating ranges,
connections, SDK functions, and command syntax remain TBD pending evidence.
Do not assume laser software control. Equipment limits must come from
manufacturer documentation and laboratory rules validated by the researcher,
not from generated text or scientific reference values.

## 7. Home-PC / laboratory-PC boundary

The home PC is primarily for development and offline tests when separately
authorized. The laboratory PC is a separate environment containing the
physical setup; its software, SDKs, data, and device capabilities require
inventory. A repository on the home PC proves nothing about lab readiness.

RustDesk may provide authorized remote desktop access. Its availability is
not authorization to operate equipment. No remote desktop access, device
discovery, commands, experiments, simulations, or runtime implementation are
part of C01. No sensitive connection details are needed in this draft.

## 8. Conceptual end-to-end workflow — PROPOSED

1. Human defines an LC-characterization objective; Local Orchestrator records
   the objective and important workflow state.
2. Scientist justifies a method from evidence and proposes success criteria.
3. Experimentalist adapts it to verified lab capabilities, identifies missing
   specifications, and designs the procedure and any necessary execution
   code. Scientist and Experimentalist can clarify technical details directly.
4. Human reviews the plan and explicitly authorizes any real operation.
   Missing limits or interfaces block execution; a plan is not permission.
5. A human-controlled laboratory operation, only under separately established
   restrictions and command-level enforcement, produces actual measurements
   and acquisition metadata. No execution interface is specified here.
6. Analyst checks information completeness, selects and justifies analysis,
   and reports reproducible metrics, statistics, uncertainty, and limitations.
   Missing metadata prompts clarification; additional measurements require
   a new authorized action rather than an autonomous retry.
7. Scientist interprets the conclusions; Experimentalist addresses technical
   quality issues. Human decides next steps. Orchestrator records important
   outcomes, state changes, and approvals; eligible procedures may enter the
   reuse lifecycle only with the required evidence and approval.

Historical artifact names may inform later work, but v0.1 producers,
consumers, routing rules, and H1–H4 checkpoints are not automatically adopted
as revised contracts. Their reconciliation remains OPEN.

## 9. Minimal demonstration direction — PROPOSED

The student's target is **December 5, 2026**, for a first limited
demonstration. It is not a guaranteed deadline or an approved full-system
acceptance criterion.

A candidate limited demonstration is one evidence-backed LC planning cycle:
a justified scientific method, a lab-adapted procedure exposing unknowns and
the human authorization boundary, and an Analyst-defined measurement/metadata
requirement and analysis approach. This is a proposal for review, not a
selected metric, implemented agent workflow, or authorization to simulate.
Analysis of actual data would require suitable measurements and metadata
to be supplied under separate authorization; none are currently in the repo.

The immediate prerequisite is a separately authorized laboratory-computer
inventory. The demonstration's exact scope, execution mode, input data,
observable deliverable, and measurable pass/fail criteria remain OPEN.

## 10. OPEN questions and unresolved requirements

- What equipment documentation, installed SDK/driver versions, existing
  procedures, code, and measurement data actually exist on the lab PC?
- Which LC metric and limited demonstration scenario are first, and what
  evidence and measurable criteria will establish success?
- Does the transmission-matrix suggestion concern planning only, and how
  does it relate to the retained Transmission Matrix Retrieval exclusion?
- Who validates limits and procedures, approves reuse, and authorizes each
  real operation? What evidence and conditions apply to each lifecycle stage?
- How will deterministic command checks, approvals, and abort handling work
  before any software-controlled device action is considered?
- What clarification outcomes must be recorded by the Orchestrator, and how
  will revised contracts, provenance, metadata, and experiment history work?
- What catalogue/storage formats, runtime framework/provider, and external
  discovery/integration mechanisms should later tasks adopt?
- How should historical instructions, contracts, and diagrams be migrated
  under a separately scoped documentation task?

See [CURRENT_STATE.md](../CURRENT_STATE.md) for the current handoff and the
preserved v0.1 development history.
