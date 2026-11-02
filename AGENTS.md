# AGENTS.md

This file has two parts:

1. **Development-agent rules:** instructions for AI coding assistants (Claude
   Code, Codex, Cursor, and others) working on this repository.
2. **Scientific agent roles:** the *proposed* PhotonicsAI runtime agents, with
   their responsibilities, proposed tools, proposed skills, and forbidden
   actions.

For the full design, see [ARCHITECTURE.md](ARCHITECTURE.md). For the current
status, see [CURRENT_STATE.md](CURRENT_STATE.md).

---

## Part 1 — Development-agent rules

### Working model

- A separate **Architect** (currently a ChatGPT session supervised by the
  researcher) owns design decisions. The development agent implements or
  documents only the step it has been explicitly authorized to do.
- Do not redesign the architecture on your own. If you have a concern, report
  it; do not apply it silently.
- Do not start the next step or chunk on your own.

### Before any change

1. Read [CURRENT_STATE.md](CURRENT_STATE.md), [ARCHITECTURE.md](ARCHITECTURE.md),
   [DECISIONS.md](DECISIONS.md), and [DATA_CONTRACTS.md](DATA_CONTRACTS.md).
2. Inspect any file before editing it. Preserve valuable existing content and
   report conflicts instead of overwriting.
3. Modify only the files the current task explicitly lists.

### Project rules

- **Facts vs. proposals:** keep confirmed facts separate from proposed design.
  Mark proposals as `PROPOSED`, `PROVISIONAL`, or `OPEN`.
- **No invented specifics:** do not invent SDK function names, device APIs, or
  hardware safety limits. Unknown values stay marked `TBD`.
- **Literature values are not settings:** parameters from scientific papers
  (voltages, frequencies, laser powers, exposure times, and so on) are
  references only. They are never approved hardware settings.
- **Framework-neutral:** do not introduce or assume a specific
  orchestration/agent framework until [DECISIONS.md](DECISIONS.md) records one.
- **No new dependencies, configuration, or abstractions** unless explicitly
  authorized.
- **Transmission Matrix Retrieval is out of scope.** Do not implement it.

### Forbidden actions for development agents

- Connecting to, or sending commands to, any laboratory device (SLM, camera,
  signal generator, laser, LC cell), including through RustDesk.
- Running laser or signal-generator commands of any kind.
- Implementing hardware control or SDK wrappers before this is authorized.
- Installing dependencies.
- Committing, tagging, pushing, merging, deploying, or publishing, unless the
  researcher gives a separate, explicit instruction to do so.
- Deleting or restructuring unrelated files.

### After any change, report

- The exact files you created or modified.
- The verification commands you ran and their results.
- Confirmation that you stayed within scope.
- Any conflicts or unknowns you found.

---

## Part 2 — Scientific agent roles (PROPOSED)

The tools and skills listed below are **proposed interfaces and capabilities,
not confirmed installed integrations.** None has been installed, implemented,
or written yet. Agents communicate only through the Local Orchestrator, using
structured artifacts (see [DATA_CONTRACTS.md](DATA_CONTRACTS.md)).

**Tools vs. skills**

- **Tool:** an executable capability, callable interface, or software
  utility. It *does* something (for example, runs code or retrieves a paper).
- **Skill:** a documented scientific or operational procedure that guides
  *how* an agent solves a problem (for example, how to estimate the
  uncertainty of a switching time).

A skill may use several tools. A tool gives no authority beyond the agent's
responsibility.

### Non-LLM components

| Component | Responsibility |
|---|---|
| **Human / Researcher** | Defines scientific goals, reviews major decisions, and approves every real-world experimental action. |
| **Local Orchestrator** | Deterministic workflow engine. Manages workflow states, routes tasks and artifacts, tracks task IDs and dependencies, records approvals, failures, and retries, and hosts the future Chief Orchestrator integration boundary. |
| **Hardware Safety Gateway** | Deterministic enforcement layer. Validates commands against approved device limits and an allowlist, and denies unknown or unauthorized settings. Real execution stays disabled until specifications, safety rules, and approval workflows are validated. |

### LLM agents

#### Scientist

- **Responsibility:** Interprets research goals, reviews literature, proposes
  characterization methods, and defines hypotheses and success criteria.
- **Proposed tools:** literature search and retrieval; project knowledge base
  (read access); reference/citation manager.
- **Proposed skills:** characterization-method selection for a black-box LC
  scattering cell; hypothesis formulation; definition of measurable success
  criteria; critical appraisal of literature evidence.
- **Forbidden:** specifying device settings as approved; treating literature
  values as hardware settings; accessing hardware.

#### Experimentalist

- **Responsibility:** Turns approved method proposals into experiment
  protocols: measurements, parameters, acquisition sequences, and quality
  checks. Checks device capability at the planning level.
- **Proposed tools:** read-only device-capability profile (built from the
  documented specifications; values `TBD`); ExperimentPlan template and
  completeness checker.
- **Proposed skills:** protocol design (for example, voltage-response sweeps,
  time-resolved switching measurements, speckle acquisition); parameter
  planning with explicit units and value sources; design of calibration and
  reference measurements (for example, dark frames and zero-voltage
  baselines); quality-check and abort-condition design.
- **Forbidden:** approving its own plan; accessing hardware; treating
  literature values as limits.

#### Coder *(optional)*

- **Responsibility:** Develops algorithmic and data-processing components
  when a task needs them.
- **Proposed tools:** file editing in a sandbox; sandboxed code execution;
  test runner.
- **Proposed skills:** test-first implementation of data-processing
  algorithms; preparing code and test evidence for H4 review.
- **Forbidden:** controlling laboratory devices; running outside the sandbox;
  integrating code without passing tests and H4 approval.

#### Executioner

- **Responsibility:** Executes validated, human-approved ExecutionRequests
  through abstract hardware adapters. Returns measurement artifacts and
  execution status.
- **Proposed tools:** abstract device-adapter interfaces, reachable only
  through the Safety Gateway (no SDK calls defined); acquisition sequencer;
  execution logger.
- **Proposed skills:** step-by-step execution of an approved acquisition
  sequence; pre-run checklist verification (approval reference, plan
  version); fault, denial, and abort handling.
- **Forbidden:** bypassing the Safety Gateway; changing approved parameters;
  executing anything that lacks a valid approval reference.

#### Analyst

- **Responsibility:** Processes measurements, computes optical metrics, and
  produces plots, summaries, uncertainty estimates, and reports.
- **Proposed tools:** Python, NumPy, SciPy, image-processing utilities,
  signal-processing utilities, plotting library.
- **Proposed skills:** analysis of optical response vs. applied voltage;
  temporal switching analysis; speckle statistics analysis; uncertainty
  estimation; data-quality assessment (saturation, noise, outliers).
- **Forbidden:** changing raw data; accessing hardware; triggering new
  measurements directly (requests go through the Orchestrator).

#### Scientific Reviewer

- **Responsibility:** Evaluates result validity and evidence against the
  success criteria. Recommends acceptance, replanning, or additional
  measurements.
- **Proposed tools:** read-only access to artifacts, datasets, and reports;
  statistical checking utilities.
- **Proposed skills:** evaluating evidence against success criteria; checking
  validity and reproducibility; formulating an accept / replan /
  additional-measurement recommendation with its rationale.
- **Forbidden:** making the final acceptance decision (the human does);
  accessing hardware.

### Forbidden actions for all runtime agents

- Communicating with other agents directly instead of through the Orchestrator.
- Sending any command to hardware except through Executioner → Safety Gateway
  → adapter.
- Approving their own outputs where human approval is required.
- Inventing device capabilities, limits, or SDK calls.
- Performing Transmission Matrix Retrieval.
