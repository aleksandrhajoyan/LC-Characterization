# Decisions Log

> **The architecture is NOT approved.** v0.1 is a proposal awaiting professor
> review.

Statuses: **ACCEPTED** = a confirmed fact or scope boundary given by the
project. **PROVISIONAL** = a proposed design choice, open to change.
**OPEN** = a question that has not been resolved.

## Accepted facts and scope boundaries

| ID | Item |
|---|---|
| A1 | Project goal: a multi-agent AI system for automated optical characterization of a voltage-controlled LC scattering cell, treated as a black box. |
| A2 | Hardware: Meadowlark phase-only SLM 1920×1152; ALKERIA Celera camera; RIGOL DG812 signal generator (future PyVISA control); Coherent Viper-V5 532 nm laser; LC scattering cell. Remote access via RustDesk. |
| A3 | Optical setup conceptually similar to Fig. 2 of Rafayelyan et al., *Phys. Rev. X* 10, 041037 (2020). |
| A4 | **Transmission Matrix Retrieval is OUT OF SCOPE**; another student is responsible for it. |
| A5 | First deliverable: an architecture diagram (agents, communication, tools, workflow and feedback, human supervision, integration boundary). |
| A6 | The system must be integrable in the future with the lab's Chief Orchestrator platform. |
| A7 | Current phase is documentation only. No agents, code, or device integrations. |

## Provisional architectural decisions

| ID | Decision | Rationale |
|---|---|---|
| P1 | Nine components: Human, Local Orchestrator, Scientist, Experimentalist, Coder (optional), Executioner, Analyst, Scientific Reviewer, and Hardware Safety Gateway. | Separates scientific reasoning, planning, execution, analysis, and review. |
| P2 | The Local Orchestrator is deterministic (non-LLM) and is the hub for all agent communication. | Auditable routing, state, and approvals. |
| P3 | Agents exchange structured artifacts ([DATA_CONTRACTS.md](DATA_CONTRACTS.md)) rather than free chat. | Traceability and validation. |
| P4 | A deterministic Hardware Safety Gateway with a default-deny policy sits between the Executioner and all devices. | LLM output must never reach hardware unchecked. |
| P5 | Real execution stays disabled until specifications, safety rules, and approval workflows are validated. | Safety. |
| P6 | Mandatory human approval (H2) before any real-world execution, including after feedback loops. | Human supervision of physical actions. |
| P7 | The Coder is optional, sandboxed, and never controls devices. | Not on the initial critical path; limits risk. |
| P8 | The Local Orchestrator is the only integration point with the Chief Orchestrator. | A clean, replaceable boundary. |
| P9 | No orchestration framework, LLM provider, or SDK is chosen yet. | Avoids premature lock-in. |

## Open questions for professor review

1. Is the agent split right? For example, should the Scientist and
   Experimentalist merge, or should the Analyst and Reviewer merge, for a
   first prototype?
2. Which characterization metrics are the priority for the first study
   (response vs. voltage, switching dynamics, speckle statistics, or others)?
3. Which human checkpoints are mandatory beyond H2? Who may grant approvals?
4. Which devices may software control at all? In particular, the laser:
   should it be monitored only, or never controlled by software?
5. Who defines and validates the hardware safety limits (LC cell voltage and
   frequency, laser power, SLM, camera exposure)? Where are the device
   specifications documented?
6. What interface, protocol, and authority will the Chief Orchestrator
   integration have? May it approve execution?
7. Is a simulated or dry-run execution mode expected before real execution?
8. Data management: where are raw data stored, and what formats and
   retention rules apply?
9. Are there constraints on LLM providers or on running models locally?
10. How should operation over RustDesk (remote access) relate to on-site
    supervision during real experiments?
11. Is there an interface with the Transmission Matrix Retrieval work (shared
    data or setup time) that should be coordinated?
12. What is the expected minimum working prototype after architecture
    approval, and what observable, measurable criteria will determine whether
    that prototype is successful? The first requested deliverable is already
    the architecture diagram (A5); this question concerns the subsequent
    implementation phase. No MVP scope or evaluation criteria have been
    approved yet.
