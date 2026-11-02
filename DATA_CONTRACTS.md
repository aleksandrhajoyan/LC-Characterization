# Data Contracts — PROPOSED

> **Status: PROPOSED, not finalized.** These are *logical* contracts that
> describe what information each artifact must carry. They are not SDK- or
> framework-specific APIs, and no serialization format (JSON, YAML, database
> schema, and so on) has been chosen. Field names are illustrative.

See [ARCHITECTURE.md](ARCHITECTURE.md) for where each artifact flows.

## Common envelope (all artifacts)

| Field | Description |
|---|---|
| `artifact_id` | Unique identifier for this artifact |
| `artifact_type` | One of the types below |
| `version` | Revision number; revisions keep a link to the prior version |
| `task_id` | Orchestrator task / workflow ID |
| `parent_ids` | IDs of the artifacts this one was derived from |
| `created_by` | The producing component (agent or human) |
| `created_at` | Timestamp (time zone explicit) |
| `provenance` | Inputs, model/agent version, tools used, and references |
| `validation_status` | `draft` · `validated` · `rejected` · `superseded` |
| `approval_ref` | ID of the recorded human approval, where required (else null) |
| `notes` | Free-text remarks |

**Units rule:** every physical quantity is stored as a value **with an
explicit unit**. Unitless quantities are marked as dimensionless.

---

## 1. ResearchGoal

Producer: Human (or the future Chief Orchestrator) · Consumer: Scientist

- Scientific objective (free text) and the motivating question
- Device under test (the LC scattering cell; sample identifier if known)
- Quantities of interest (for example, response vs. voltage, switching time,
  speckle statistics)
- Constraints: time budget, allowed devices, things to avoid
- Priority and the requesting person
- Explicit exclusions (for example, Transmission Matrix Retrieval)

## 2. MethodProposal

Producer: Scientist · Consumer: Human (H1), Experimentalist

- Reference to the `ResearchGoal`
- Proposed characterization method(s) and the rationale for each
- Hypotheses
- Success criteria (measurable, with units and tolerances)
- Required observables and the expected metrics
- Literature references (citation + what was used). Values taken from
  literature are flagged `reference_only`
- Assumptions, risks, and alternatives considered
- H1 review status and `approval_ref`

## 3. ExperimentPlan

Producer: Experimentalist · Consumer: Human (H2), Orchestrator

- Reference to the `MethodProposal`
- Ordered measurement sequence (steps)
- For each step: the devices involved, parameter names, values or ranges
  **with units**, and the source of each value (`researcher`, `device_spec`,
  `literature_reference_only`, `TBD`)
- Acquisition settings (frames, repetitions, timing) with units
- Quality checks and abort conditions
- Result of the planning-level capability check, plus unresolved items
- Calibration/reference measurements required (for example, dark frames, a
  baseline with no applied voltage)
- Estimated duration
- H2 approval status and `approval_ref` (**required before execution**)

## 4. ExecutionRequest

Producer: Orchestrator (from an approved ExperimentPlan) · Consumer:
Executioner → Safety Gateway

- Reference to the `ExperimentPlan` and its **mandatory** `approval_ref`
- Concrete commands in abstract device terms (device, setting, value + unit).
  These are **not** SDK calls
- Execution mode: `dry_run` / `simulated` / `real`. `real` is **disabled**
  until validated
- Safety Gateway validation result for each command: `allowed` / `denied` +
  reason
- Retry policy and abort conditions
- Expiry: the approval is valid only for this request and plan version

## 5. MeasurementDataset

Producer: Executioner · Consumer: Analyst

- Reference to the `ExecutionRequest`
- Raw data locations/handles (images, time series) and their formats
- Acquisition metadata: the device settings actually applied (with units),
  timestamps, frame counts, and device identifiers
- Environmental and contextual notes, if available
- Execution status: `complete` / `partial` / `failed` / `aborted`, plus a log
  of denials and faults
- Data integrity information (for example, checksums)
- Raw data is immutable once recorded

## 6. AnalysisReport

Producer: Analyst · Consumer: Scientific Reviewer

- References to the `MeasurementDataset`(s) and the analysis code version
- Processing steps applied (reproducible description)
- Computed metrics with units and **uncertainty estimates**
- Plots/figures (references) with captions
- Data-quality assessment (saturation, noise, outliers, missing data)
- Comparison against the success criteria from the `MethodProposal`
- Limitations and suggested follow-up measurements

## 7. ReviewDecision

Producer: Scientific Reviewer · Consumer: Human (H3), Orchestrator

- References to the `AnalysisReport` and the success criteria
- Recommendation: `accept` / `replan` / `additional_measurements` /
  `reject`
- Evidence assessment: which criteria passed or failed, and why
- Requested follow-up work (routed through the Orchestrator)
- Confidence and caveats
- Final human decision and `approval_ref` (the Reviewer recommends; the
  human decides)

---

## Open contract questions

- Serialization format and storage location for artifacts and raw data.
- Raw-data formats from the camera and the expected data volume.
- Whether the Chief Orchestrator platform imposes its own artifact schema.
- Exact approval record structure (who, when, scope, signature mechanism).
