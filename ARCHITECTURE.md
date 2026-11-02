# PhotonicsAI Architecture — v0.1

> **Status: DRAFT v0.1, proposed for professor review. Not approved.**
> Diagram: [docs/diagrams/agent_workflow.mmd](docs/diagrams/agent_workflow.mmd) ·
> Artifacts: [DATA_CONTRACTS.md](DATA_CONTRACTS.md) ·
> Decisions and open questions: [DECISIONS.md](DECISIONS.md)

## 1. Confirmed requirements vs. design proposals

### 1.1 Confirmed (given by the project)

- Goal: automated optical characterization of a voltage-controlled
  liquid-crystal scattering cell, treated as a black box.
- Hardware: Meadowlark phase-only SLM (1920×1152), ALKERIA Celera camera,
  RIGOL DG812 signal generator (future control via PyVISA), Coherent Viper-V5
  532 nm laser, and the LC scattering cell. Remote access is via RustDesk.
- The optical setup is conceptually similar to Figure 2 of Rafayelyan et al.,
  *Phys. Rev. X* 10, 041037 (2020).
- Candidate characterization topics: optical response vs. applied voltage,
  temporal switching behavior, speckle statistics, and related metrics.
- **Transmission Matrix Retrieval is out of scope** (another student owns it).
- First deliverable: an architecture diagram that shows agents,
  communication, tools, workflow and feedback loops, human supervision, and
  the future platform integration boundary.
- A laboratory "Chief Orchestrator" platform exists or is planned, and this
  system must be integrable with it in the future.

### 1.2 Proposed (this document's design — subject to review)

Everything in sections 2–8 below: the component split, the communication
model, the workflow, the approval points, and the safety layering. Tools and
skills are proposed capabilities, **not installed integrations.** No
orchestration framework, LLM provider, or device SDK has been selected.

## 2. Components

| # | Component | Kind | Responsibility |
|---|---|---|---|
| 1 | Human / Researcher | Human | Defines scientific goals, reviews major decisions, and approves real-world experimental actions |
| 2 | Local Orchestrator | Deterministic software (non-LLM) | Workflow state machine, task and artifact routing, task IDs and dependencies, approval/failure/retry log, and the integration boundary to the Chief Orchestrator |
| 3 | Scientist Agent | LLM agent | Interprets objectives, reviews literature, proposes methods, defines hypotheses and success criteria |
| 4 | Experimentalist Agent | LLM agent | Turns approved methods into experiment protocols: measurements, parameters, acquisition sequences, quality checks, and planning-level capability checks |
| 5 | Coder Agent *(optional)* | LLM agent | Develops algorithmic and data-processing code in a sandbox with tests and review. Never controls devices. Not on the initial critical path |
| 6 | Executioner Agent | LLM agent (constrained) | Runs approved ExecutionRequests through abstract hardware adapters and returns MeasurementDatasets and status. Cannot bypass the Safety Gateway |
| 7 | Analyst Agent | LLM agent | Processes data, computes optical metrics, and produces plots, uncertainty estimates, and AnalysisReports |
| 8 | Scientific Reviewer Agent | LLM agent | Judges validity and evidence against the success criteria. Recommends accept, replan, or measure more |
| 9 | Hardware Safety Gateway | Deterministic software (non-LLM) | Enforces device limits and an approved command allowlist, and denies unknown or unauthorized settings. **Real execution is disabled by default** |
| — | Hardware adapters and devices | Deterministic software + physical hardware | Abstract per-device adapters (SLM, camera, signal generator) that sit behind the Safety Gateway. Interfaces are `TBD`. No software laser interface is assumed (`TBD`) |

The proposed tools (executable capabilities) and proposed skills (documented
procedures) for each agent, and their forbidden actions, are listed
separately in [AGENTS.md](AGENTS.md#part-2--scientific-agent-roles-proposed).

## 3. Communication model

- **Hub-and-spoke:** every agent talks *only* to the Local Orchestrator. There
  are no direct agent-to-agent channels. The Orchestrator is the single place
  where messages are routed, logged, and checked against the workflow state.
- **Structured artifacts over chat:** components exchange the typed artifacts
  defined in [DATA_CONTRACTS.md](DATA_CONTRACTS.md). Each artifact carries an
  ID, provenance, and a validation status, and approval references where
  applicable.
- **Core route (logical):**

  ```
  Human → Orchestrator → Scientist → Experimentalist → (approval) →
  Executioner → Safety Gateway → Hardware → Executioner → Analyst →
  Scientific Reviewer → Human
  ```

  Each "→" between agents physically passes through the Orchestrator.

| Step | From → To (via Orchestrator) | Artifact |
|---|---|---|
| 1 | Human → Scientist | `ResearchGoal` |
| 2 | Scientist → Human (review) → Experimentalist | `MethodProposal` |
| 3 | Experimentalist → Human (approval) | `ExperimentPlan` |
| 4 | Orchestrator → Executioner | `ExecutionRequest` (with an approval reference) |
| 5 | Executioner → Safety Gateway → Adapters | Validated device commands |
| 6 | Executioner → Analyst | `MeasurementDataset` |
| 7 | Analyst → Reviewer | `AnalysisReport` |
| 8 | Reviewer → Human | `ReviewDecision` (a recommendation) |
| opt | Any agent → Coder → requester | Code task / tested code (sandbox only) |

## 4. Normal workflow

1. **Goal intake.** The researcher submits a `ResearchGoal`. The Orchestrator
   assigns a task ID and opens a workflow.
2. **Method proposal.** The Scientist produces a `MethodProposal` (method,
   hypotheses, success criteria, literature references).
   **Human checkpoint H1:** the researcher reviews and accepts the scientific
   direction.
3. **Experiment planning.** The Experimentalist produces an `ExperimentPlan`
   (measurement sequence, parameter ranges, quality checks, capability check
   result).
4. **Human checkpoint H2 (mandatory):** the researcher approves or rejects the
   plan for real-world execution. The approval is recorded by the
   Orchestrator and becomes the approval reference.
5. **Execution.** The Orchestrator issues an `ExecutionRequest` that cites the
   approval. The Executioner sends each command through the **Safety
   Gateway**, which checks it against device limits and the allowlist. Only
   validated commands reach the adapters. Denials and faults go back to the
   Orchestrator.
6. **Measurement.** The Executioner returns a `MeasurementDataset` (raw data
   plus acquisition metadata and status).
7. **Analysis.** The Analyst computes metrics (for example, transmitted
   intensity vs. voltage, switching times, speckle contrast) with
   uncertainties, and produces an `AnalysisReport`.
8. **Review.** The Scientific Reviewer checks the evidence against the
   success criteria and issues a `ReviewDecision` (accept / replan / measure
   more).
9. **Human checkpoint H3:** the researcher makes the final decision on
   results and next steps.

## 5. Feedback loops

All feedback goes through the Orchestrator, which logs it as a new or
dependent task.

| Loop | Trigger | Route |
|---|---|---|
| F1: Additional measurements | Reviewer or Analyst finds insufficient data, poor SNR, or missing ranges | → Orchestrator → Experimentalist (revised plan) → **H2 again** → Executioner |
| F2: Scientific replanning | Reviewer finds the hypothesis unsupported or the method unsuitable | → Orchestrator → Scientist (revised proposal) → H1 again |
| F3: Plan revision on evidence | Scientist or Experimentalist revises after seeing results | Revised `MethodProposal` / `ExperimentPlan`, re-approved as needed |
| F4: Execution failure / denial | Safety Gateway denial, device fault, or quality-check failure | → Orchestrator (logged) → Experimentalist and/or Human; retries follow a recorded policy |
| F5: Algorithm need | Analyst or Experimentalist needs a new processing method | → Orchestrator → Coder (sandbox) → tested code → review → requester |

**Rule:** any feedback loop that leads to new real-world execution must pass
H2 again. A previous approval never covers a revised plan.

## 6. Human-in-the-loop points

| ID | Point | Required? |
|---|---|---|
| H1 | Accept the scientific direction (MethodProposal) | Proposed: required |
| H2 | Approve the ExperimentPlan for real-world execution | **Mandatory** |
| H3 | Accept the results / decide the next steps (ReviewDecision) | Proposed: required |
| H4 | Approve integrating Coder output into the analysis pipeline | Occurs only if the optional Coder is used. Then proposed: required |
| — | Emergency stop / abort at any time | Always available (mechanism TBD) |

## 7. Separation of AI reasoning and deterministic hardware control

```
  LLM reasoning layer          Deterministic control layer         Physical layer
  ───────────────────          ───────────────────────────         ──────────────
  Scientist, Experimentalist,  Local Orchestrator (state,          SLM, camera,
  Coder, Executioner,          routing, approvals)                 signal generator,
  Analyst, Reviewer       ──►  Hardware Safety Gateway       ──►   laser, LC cell
                               Hardware adapters
```

- The diagram separates three kinds of flow: agent messages / structured
  artifacts, hardware control commands (and device data returned), and
  physical paths. The simplified physical paths are optical (laser → SLM →
  LC scattering cell → camera) and electrical (RIGOL DG812 → LC cell drive
  voltage). Software reaches the physical layer only through the control
  layer.
- LLM agents produce **proposals and requests**. They never produce direct
  device I/O.
- The Executioner is the only agent that issues device-level requests, and
  only through the Safety Gateway, and only with a valid approval reference.
- The Safety Gateway is **deterministic code, not an LLM.** It uses a
  default-deny policy: any parameter or command that is not explicitly
  allowlisted and within validated limits is rejected.
- Device limits come from manufacturer specifications and lab safety rules,
  validated by the researcher. **They are not taken from LLM output or from
  literature examples.** All limits are currently `TBD`.
- **Real execution remains disabled** until hardware specifications, safety
  rules, and human approval workflows have been validated. Until then, only
  simulated or dry-run execution is allowed (to be designed later).
- Laser safety (power, shutter, interlock) is a human/lab responsibility. The
  question of whether software may control the laser at all is open (see
  [DECISIONS.md](DECISIONS.md)).

## 8. Future platform integration boundary

- The **Local Orchestrator** is the only component that will communicate with
  the laboratory's **Chief Orchestrator** platform.
- Internal agents, the Safety Gateway, and the adapters stay hidden behind
  this boundary. The external platform sees only artifacts (for example,
  `ResearchGoal` in and `ReviewDecision`/`AnalysisReport` out) and the
  workflow status.
- The integration protocol, authentication, and the delegation of authority
  (whether the Chief Orchestrator may approve or request execution) are
  `OPEN` questions.
- Local safety enforcement and human approval **cannot be bypassed** by the
  external platform.

## 9. Explicitly out of scope

- Transmission Matrix Retrieval.
- Choosing a specific orchestration/agent framework or LLM provider.
- Implementing agents, hardware adapters, SDK wrappers, or device
  communication.
- Defining numeric hardware limits.
