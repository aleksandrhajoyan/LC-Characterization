# PhotonicsAI

PhotonicsAI is a **proposed** multi-agent AI system for the automated optical
characterization of a voltage-controlled liquid-crystal (LC) scattering cell,
treated as a black box.

> **Status:** Architecture v0.1 — documentation only, awaiting professor review.
> No code, AI agents, or laboratory-device integrations have been implemented.

## Purpose

Help a researcher plan, run, analyze, and review optical characterization
experiments on an LC scattering cell. Example metrics include optical response
versus applied voltage, temporal switching behavior, and speckle statistics.
Every action on real hardware stays under human approval and deterministic
safety enforcement.

## Current scope

- **In scope (this phase):** the architecture design, agent responsibilities,
  communication routes, logical data contracts, and the workflow diagram for
  professor review.
- **Out of scope:**
  - **Transmission Matrix Retrieval.** Another student is responsible for it.
  - Implementing agents, hardware control, or SDK wrappers (later phases,
    pending approval).
  - Choosing a specific orchestration framework.

## Laboratory setup (confirmed)

| Device | Model |
|---|---|
| Spatial light modulator | Meadowlark phase-only SLM, 1920×1152 |
| Camera | ALKERIA Celera |
| Signal generator | RIGOL DG812 (future control via PyVISA) |
| Laser | Coherent Viper-V5, 532 nm |
| Sample | Voltage-controlled liquid-crystal scattering cell |
| Remote access | RustDesk |

The optical setup is conceptually similar to Figure 2 in Rafayelyan et al.,
"Large-Scale Optical Reservoir Computing for Spatiotemporal Chaotic Systems
Prediction", *Physical Review X* 10, 041037 (2020).

## Documentation index

| Document | Contents |
|---|---|
| [CURRENT_STATE.md](CURRENT_STATE.md) | Project status and handoff. **Start here when resuming.** |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Architecture v0.1: components, communication, workflow, safety, integration boundary |
| [docs/PROFESSOR_REVIEW_BRIEF.md](docs/PROFESSOR_REVIEW_BRIEF.md) | **Accompanying document for the first professor architecture review:** concise brief (objective, agents, example workflow, safety, review questions) |
| [docs/diagrams/professor_overview.svg](docs/diagrams/professor_overview.svg) | **Primary presentation diagram for professor review:** hand-positioned 1920×1080 SVG (visually reviewed and accepted for presentation by the Architect) |
| [docs/diagrams/professor_overview.mmd](docs/diagrams/professor_overview.mmd) | Editable Mermaid version of the high-level overview |
| [docs/diagrams/agent_workflow.mmd](docs/diagrams/agent_workflow.mmd) | Detailed agent workflow diagram (technical reference: all routes, feedback loops, legend) |
| [DATA_CONTRACTS.md](DATA_CONTRACTS.md) | Proposed logical artifacts exchanged between components |
| [DECISIONS.md](DECISIONS.md) | Confirmed facts, provisional decisions, and open questions |
| [AGENTS.md](AGENTS.md) | Rules for development agents, plus the scientific agents' roles and tool boundaries |
| [CLAUDE.md](CLAUDE.md) | Claude Code entry point (imports AGENTS.md) |

To view the SVG, open it directly in a browser (Chrome, Edge) or any
SVG-capable viewer. To render a Mermaid diagram, paste the `.mmd` file into
<https://mermaid.live> or use any Mermaid-capable Markdown viewer.
