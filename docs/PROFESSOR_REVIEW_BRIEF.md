# PhotonicsAI — Professor Review Brief (Architecture v0.1)

> **Status: PROPOSED — not approved by the professor.** This brief adds no
> new design decisions. No runtime code, AI agents, or laboratory
> integrations exist.

**Diagram:** [professor_overview.svg](diagrams/professor_overview.svg) (open in
a browser).

## 1. Project objective

PhotonicsAI is a **proposed** multi-agent system for the automated optical
characterization of a voltage-controlled liquid-crystal (LC) scattering cell,
treated as a black box. Candidate topics: optical response vs. applied
voltage, temporal switching behavior, and speckle statistics.

Setup: Meadowlark phase-only SLM (1920×1152), ALKERIA Celera camera, RIGOL
DG812 signal generator (future control via PyVISA), Coherent Viper-V5 532 nm
laser, and the LC scattering cell, conceptually similar to Fig. 2 of
Rafayelyan et al., *Phys. Rev. X* 10, 041037 (2020).

**Transmission Matrix Retrieval is out of scope** (another student is
responsible for it).

## 2. Architecture overview (PROPOSED)

| Component | Kind | Role |
|---|---|---|
| Human / Researcher | Human | Defines goals, reviews major decisions, approves every real-world action |
| Local Orchestrator | Deterministic (non-LLM) | Workflow state, artifact routing, task dependencies, log of approvals, failures, retries |
| Scientist | LLM agent | Interprets goals, reviews literature, proposes methods, hypotheses, success criteria |
| Experimentalist | LLM agent | Turns an accepted method into an experiment protocol; planning-level capability check |
| Executioner | LLM agent (constrained) | Runs approved ExecutionRequests, only through the Safety Gateway |
| Analyst | LLM agent | Processes data, computes optical metrics with uncertainties, writes reports |
| Scientific Reviewer | LLM agent | Judges evidence against success criteria; recommends accept / replan / measure more |
| Coder *(optional)* | LLM agent | Sandboxed data-processing code with tests; never controls devices |
| Hardware Safety Gateway | Deterministic (non-LLM) | Enforces validated device limits and a command allowlist; default-deny |
| Hardware adapters | Deterministic | SLM, signal generator, camera; interfaces `TBD`. No laser software interface assumed |
| Chief Orchestrator *(future)* | External lab platform | Not integrated; connects only through the Local Orchestrator; interface and authority `OPEN` |

**Why agents communicate only through the Orchestrator.** Agents never talk
directly; they exchange typed artifacts
([DATA_CONTRACTS.md](../DATA_CONTRACTS.md)) through the Orchestrator, giving:

- **Traceability:** each artifact carries an ID, version, provenance, and
  validation status.
- **Enforced checkpoints:** no step can skip a recorded human approval.
- **Auditability:** one deterministic place routes, logs, and checks every
  message.
- **A clean integration boundary:** the Chief Orchestrator sees only
  artifacts and status; agents and hardware stay hidden.

Full details: [ARCHITECTURE.md](../ARCHITECTURE.md).

## 3. Agents, Tools, and Skills (PROPOSED)

A **Tool** is an executable capability (it *does* something). A **Skill** is a
documented scientific or operational procedure (it guides *how*). One example
of each is shown; full lists are in
[AGENTS.md](../AGENTS.md#part-2--scientific-agent-roles-proposed). **None is
installed or implemented.**

| Agent | Responsibility | Example Tool | Example Skill |
|---|---|---|---|
| Scientist | Methods, hypotheses, success criteria | Literature search and retrieval | Characterization-method selection for a black-box LC scattering cell |
| Experimentalist | Experiment protocols and parameters | ExperimentPlan template and completeness checker | Protocol design (e.g., voltage-response sweeps) |
| Executioner | Executes approved requests via the Gateway | Acquisition sequencer | Pre-run checklist (approval reference, plan version) |
| Analyst | Metrics, uncertainties, reports | Python, NumPy, SciPy | Optical-response vs. voltage analysis |
| Scientific Reviewer | Evidence vs. success criteria | Statistical checking utilities | Accept / replan / additional-measurement recommendation |
| Coder *(optional)* | Sandboxed data-processing code | Test runner (sandboxed) | Test-first implementation of data-processing algorithms |

## 4. Example research workflow (conceptual)

> **Conceptual only.** No experiment has been executed; voltage ranges,
> limits, and device commands are `TBD`.

**Goal:** *"Characterize the optical response of the LC cell as a function of
applied voltage."* Every hand-off passes through the Local Orchestrator.

| # | Artifact | Produced by | Contents (conceptual) | Human checkpoint |
|---|---|---|---|---|
| 1 | `ResearchGoal` | Researcher | Objective, device, constraints, exclusions | — |
| 2 | `MethodProposal` | Scientist | Method, hypotheses, measurable success criteria; literature values flagged as references only | **H1** (proposed) |
| 3 | `ExperimentPlan` | Experimentalist | Measurement sequence, parameters with units (`TBD`), calibration, quality checks, abort conditions | **H2 (mandatory)** |
| 4 | `ExecutionRequest` | Orchestrator | Abstract commands citing the H2 approval, each checked by the Safety Gateway | — |
| 5 | `MeasurementDataset` | Executioner | Immutable raw camera data, applied settings, timestamps, status | — |
| 6 | `AnalysisReport` | Analyst | Response vs. voltage with uncertainties, data quality, comparison with success criteria | — |
| 7 | `ReviewDecision` | Scientific Reviewer | Accept / replan / additional measurements / reject, with evidence | **H3** (proposed): researcher decides |

Requests for more data return via the Orchestrator to the Experimentalist;
any new real measurement needs a revised plan and **renewed H2 approval**.
Optional Coder output needs **H4** review before integration.

## 5. Scientific and hardware safety

- **Human approval:** H2 is mandatory for every real run, including after
  feedback loops; a previous approval never covers a revised plan.
- **Deterministic Hardware Safety Gateway:** non-LLM code between the
  Executioner and all devices. LLM agents never perform direct device I/O.
- **Default-deny:** any command or parameter not allowlisted and within
  validated limits is rejected.
- **Real execution disabled** until hardware specifications, safety rules,
  and approval workflows are validated. Device limits are `TBD` and will come
  from manufacturer specifications and lab rules, never LLM output or
  literature.
- **Laser:** no software control is assumed; laser safety remains a
  human/lab responsibility.

## 6. Questions for professor review

Selected from [DECISIONS.md](../DECISIONS.md#open-questions-for-professor-review)
(original numbers in brackets):

1. **Agent-role boundaries [Q1]:** Is the agent split right? For a first
   prototype, should the Scientist and Experimentalist merge, or the Analyst
   and Reviewer?
2. **Local vs. Chief Orchestrator [Q6]:** What interface, protocol, and
   authority will the Chief Orchestrator integration have? May it approve
   execution?
3. **Initial metrics [Q2]:** Which characterization metrics are the priority
   for the first study (response vs. voltage, switching dynamics, speckle
   statistics, or others)?
4. **Human approvals [Q3]:** Which human checkpoints are mandatory beyond H2,
   and who may grant approvals?
5. **Prototype and success criteria [Q12]:** What is the expected minimum
   working prototype after architecture approval, and what observable,
   measurable criteria will determine whether it is successful? (The
   diagram is the first deliverable; this concerns the next phase. No MVP
   scope or criteria have been set.)

## 7. Review status

| Item | Status |
|---|---|
| Presentation diagram | Accepted for presentation (Architect visual review) |
| Architecture v0.1 | **PROPOSED**, awaiting professor feedback |
| Runtime implementation | **NOT STARTED** (no code, agents, or device integrations) |

References: [ARCHITECTURE.md](../ARCHITECTURE.md) · [AGENTS.md](../AGENTS.md) ·
[DATA_CONTRACTS.md](../DATA_CONTRACTS.md) · [DECISIONS.md](../DECISIONS.md)
