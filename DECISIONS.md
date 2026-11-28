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

## Operational decisions — 2026-11-26 (C07-STATE-CHECKPOINT)

The earlier entries are preserved as the historical v0.1 decision record.
The current architecture direction remains **PROPOSED v0.2** in
[docs/ARCHITECTURE_V02_DRAFT.md](docs/ARCHITECTURE_V02_DRAFT.md); positive
professor feedback is reported, not blanket implementation or experiment
approval. In particular, A7 describes the earlier documentation-only phase;
C04A has since added an offline validator and tests. P9 does not negate the
later vendor SDK inventory below or select a runtime framework. These dated
operational decisions do not migrate the historical architecture or contracts.
Laboratory facts below are supplied verified C07 evidence, not checks repeated
on the home PC. See [CURRENT_STATE.md](CURRENT_STATE.md) for the full boundary.

### C07-D1 — Preserve home/lab role separation

**Date:** 2026-11-26. **Status: ACCEPTED operational boundary.**

The home repository is the canonical project/documentation source. The lab
workspace is the bounded equipment/SDK execution environment. Codex (ALEX)
and Codex (LAB) are distinct executor contexts; evidence or authorization in
one does not imply unrestricted execution authority in the other.

Historical naming correction: `D:\Nikita\TM benchmark` was the earlier name
of the same workspace now named `D:\Nikita\LC characterization (Alex)`, not
a separate Mkrtich project. The old path is stale historical naming only.
The current lab folder contains only `AGENTS.md`, manually updated to the
current authorized path; separately supplied task examples are not canonical
files there.

### C07-D2 — Use isolated CPython 3.9 for the legacy ALKERIA binding

**Date:** 2026-11-26. **Status: ACCEPTED compatibility decision.**

The inspected vendor binding contains `_core.cp39-win_amd64.pyd` and was
classified `CP39_ONLY_BINARY_PACKAGE`. No compatible CP312 binary or
buildable native-extension source was found in the inspected package/archive.
Use the isolated lab environment `C:\Users\Dell\Envs\PhotonicsAI-LC-py39`
(verified CPython 3.9.25, Windows AMD64, NumPy 1.26.4); copied package hashes
matched the source.

Constraints: do not replace existing Python 3.12, do not modify Anaconda
base unnecessarily, and do not modify global PATH. Existing Python 3.12
installations were not intentionally modified, Anaconda base was not targeted,
and PATH was not modified during the supplied validation sequence. Native
module loading establishes software compatibility only, not camera operation.

### C07-D3 — Escalate camera access in separately approved stages

**Date:** 2026-11-26. **Status: ACCEPTED operational boundary.**

Completed sequence: OS/device visibility → SDK inventory → Python wrapper
inspection → isolated Python 3.9 compatibility environment → plain wrapper
import → native `_core` load. Plain `import alkusb3` did not load the native
module; controlled `import alkusb3._core` loaded it successfully. No vendor
function or class was invoked in that native-load test.

Camera construction, enumeration, and acquisition remain separately approved
stages, none performed. Before any further camera hardware call, the
Architect must define and the human must explicitly approve the minimum
camera-object construction test and its allowed observations. That test is
**not already approved**. Installation and import success grant no hardware
permission.

### C07-D4 — Stop C06A discovery before hardware

**Date:** 2026-11-26. **Status: ACCEPTED stop; future procedure OPEN.**

Static inspection found `device_interface.get_camera_list(self)` to be an
instance method delegating to `self._obj.get_camera_list()`, requiring an
existing native device/camera object in the ordinary wrapper path. A
sufficiently bounded discovery path without construction was not established.

C06A is `BLOCKED_BY_WRAPPER_BEHAVIOR`: discovery calls 0, camera classes
instantiated 0, acquisition 0, hardware query 0. This was an intentional
safety stop, not a software failure. Do not bypass this boundary without a
separately reviewed procedure and explicit human approval of its scope.

## Operational decisions — 2026-11-28 (C10A camera milestone reconciliation)

Source: supplied verified, Architect-reviewed C08A-R1, C08B, C09A pre-flight,
and C09A-R2 evidence; not laboratory checks repeated by Codex (ALEX).
The C07 decisions above are preserved as historical knowledge and approval
status at that checkpoint. C10A-D1 and C10A-D2 supersede C07-D3's assumptions
about construction/discovery separation and its pending construction test.
No historical decision is rewritten as if these findings were already known.

### C10A-D1 — Treat native construction and discovery as coupled

**Date:** 2026-11-28. **Status: ACCEPTED implementation-specific finding.**

C08B static disassembly established a conditional reachable path from
`ICeleraCamera::Create()` through native construction/global initialization
to OS device discovery/enumeration via Windows SetupAPI. Construction and
enumeration are not separate stages for the exact inspected implementation.
The inspected `CAlkUSB3-64.dll` (file/product version `2.5.24.0`) had SHA-256
`93f4aa39752bcf60d9352d59fd9f8a184deda2e3246aa9d9a5f45d48d5184adf`;
the package DLL hash matched. Previously observed Installed Apps version
MaestroUSB3 `2.7.10` is a separate observation; the difference is unexplained.

This is a reachable OS discovery path, not evidence that every construction
opens a physical camera, transfers USB data, accesses settings/registers,
starts acquisition, or creates a camera device handle. Complete native
destruction side effects also remain unverified. C08B executed no vendor DLL,
imported no `alkusb3`, invoked no vendor constructor, and took no hardware action.

### C10A-D2 — Record the completed, narrowly approved C09A runtime action

**Date:** 2026-11-28 (records execution on 2026-11-26).
**Status: ACCEPTED completed action within approved scope.**

Explicit human approval was:

> APPROVE C09A exactly as specified. Construction + implicit discovery +
> ordinary process teardown are approved. No enumeration method calls,
> settings access, camera open, or acquisition.

The initial C09A pre-flight stopped because the expected `Scripts\python.exe`
path did not exist; no Python process, import, constructor, or hardware action
occurred. C09A-PREFLIGHT-R1 found
`C:\Users\Dell\Envs\PhotonicsAI-LC-py39\python.exe` (Python `3.9.25`) and
the environment's `Lib\site-packages\alkusb3` by filesystem check, without
vendor import or hardware action. These pre-flights are not physical experiments.

C09A-R2 used that interpreter with `PYTHONDONTWRITEBYTECODE=1` and Python
`-B`: one vendor Python process, one `celera_camera` constructor attempt,
`CONSTRUCTION_SUCCEEDED`, wrapper type `alkusb3.celera_camera.celera_camera`,
no stderr, exit code `0`. Ordinary process teardown completed; explicit vendor
cleanup calls were `0`. All reported explicit enumeration, open, settings,
acquisition, frame, other-device, retry, and environment/system-change counts
were `0`. See [EXPERIMENT_LOG.md](EXPERIMENT_LOG.md) for the one runtime-action
entry; no measurement was produced.

### C10A-D3 — Keep further camera escalation separately reviewed and approved

**Date:** 2026-11-28. **Status: ACCEPTED approval boundary; next step OPEN.**

Successful construction does not authorize or establish an explicit
`get_camera_list` result, list contents/count, Master/Slave identity through
the SDK, SetCamera / camera selection/open, settings access, acquisition,
frame capture, or validated camera operating limits. Future camera escalation
remains separately reviewed by the Architect and explicitly human-approved.

The next open decision is Architect definition + explicit human approval of
the minimum explicit read-only camera-list observation, if scientifically/
technically justified, with no SetCamera/open/settings/acquisition. This C10A
documentation task grants no approval for that step or any hardware action.

## Operational decisions — 2026-11-28 (C12A C11A/C11B canonical reconciliation)

Source: supplied completed C11A static audit and approved C11B runtime report;
neither was independently repeated by Codex (ALEX). The earlier decisions
remain the historical record of knowledge and approval at their checkpoints.
C11B completes only the success/type/length observation described below,
superseding C10A-D3's pending status for that narrow action. It does not
approve further runtime work or change the proposed architecture.

### C12A-D1 — Bound C11A's safe value-data finding to post-return observation

**Date:** 2026-11-28. **Status: ACCEPTED implementation-specific static finding.**

C11A verdict: **A. `LIST_RESULT_IS_SAFE_VALUE_DATA`**.
`device_interface.get_camera_list(self)` returns
`self._obj.get_camera_list()`; the native signature is
`virtual Array<String> GetCameraList()`. Its owning array of string values is
converted by the binding into a built-in Python `list` of built-in Python
`str` entries. After return, result/entry types, length, iteration,
positional indices, and reading/printing the returned display-name strings
are local Python observations requiring no additional vendor SDK call.
Vendor examples show `GetCameraList` / count / names before `SetCamera`.

This finding neither establishes nor authorizes all activity inside
`GetCameraList`. Device serial number, device camera property, name/device
properties, `active_interfaces`, `super_speed`, and similar properties are
separate native accesses outside the approved boundary. Static safety of
post-return string observation is not runtime approval to perform it.

### C12A-D2 — Record the explicitly approved, completed C11B observation

**Date:** 2026-11-28. **Status: ACCEPTED completed action within approved scope.**

The exact human approval was:

> APPROVE C11B exactly as specified: one celera_camera construction, one get_camera_list call, observe only return/exception, Python result type, and list length; no camera names, SetCamera/open, properties/settings, or acquisition. Ordinary process teardown approved. No retry.

C11B used `C:\Users\Dell\Envs\PhotonicsAI-LC-py39\python.exe`, Python
`3.9.25`, `PYTHONDONTWRITEBYTECODE=1`, and `-B`. One Python process, one
explicit import, one constructor attempt (succeeded), and one
`get_camera_list` call (returned successfully) produced **`builtins.list`,
length `1`**. Stderr: none; exit code: `0`; ordinary process teardown: yes;
explicit cleanup calls and retries: `0`. No names, camera open/selection,
property/settings access, acquisition, or frame capture occurred, according
to the supplied report. See the single C11B entry in
[EXPERIMENT_LOG.md](EXPERIMENT_LOG.md) for stdout, counts, deviations, and
monitoring limitations. This was a hardware-adjacent runtime action; no
optical measurement was produced.

### C12A-D3 — Keep SDK list length separate from physical-device identification

**Date:** 2026-11-28. **Status: ACCEPTED interpretation boundary.**

`RESULT_LENGTH=1` means only:

> During this exact approved GetCameraList invocation, the SDK returned one Python list entry.

It does not establish physical-camera count, connected-Celera count, Master
or Slave identity, an error in prior OS visibility of two Celera device
entries, camera defect/unavailability, or successful selection/open.
**No Master/Slave mapping is established.** The relationship between the
previous OS device entries and this SDK result length remains **UNKNOWN**.
The returned display-name string was not inspected.

### C12A-D4 — Keep display-name observation and later stages separately approved

**Date:** 2026-11-28. **Status: ACCEPTED approval boundary; next decision OPEN.**

The next open decision is Architect definition + explicit human approval of
whether to observe the already-materialized display-name string from one
future controlled `GetCameraList` result. That runtime step remains **OPEN
and unapproved**. C11A's static finding and C11B's completed approval grant
no permission for the future call or display-name observation.

SetCamera/select/open, serial/model/device properties, settings reads,
settings writes, acquisition, and frame capture remain separate later
stages requiring their own review and explicit human approval. Hotplug/list
behavior and validated hardware operating limits remain unknown/not tested.
C12A authorizes no runtime step or laboratory action.
