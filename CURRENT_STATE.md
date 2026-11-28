# Current State

_Last updated: 2026-11-28 (C14A — C13A canonical reconciliation)_

## Current objective

**Current milestone: C13A PASS** — one explicitly human-approved
`celera_camera` construction succeeded; one `get_camera_list` call returned
`builtins.list`, length **1**; exactly `result[0]` was observed, yielding
**`CELERA C12SX-M s/n A0805E3B`**; ordinary process teardown completed.
C11A static verdict: **A. `LIST_RESULT_IS_SAFE_VALUE_DATA`** for post-return
observation of the materialized Python result; it does not establish or
authorize all activity inside `GetCameraList`.
C08B established that construction and OS device discovery/enumeration are
coupled on a conditional reachable native path in the inspected implementation.
The verified fact is: "During the approved C13A invocation, get_camera_list
returned one entry whose exact display-name string was 'CELERA C12SX-M s/n A0805E3B'."
Physical-device count, camera operability, and any Master/Slave mapping are
not established.

**Next technical step — OPEN, unapproved:** read-only OS/device-metadata
reconciliation to determine whether serial `A0805E3B` can be mapped to the
previously observed Windows Master or Slave device node, without
opening/selecting the camera. This next LAB step must be separately bounded
by the Architect and explicitly human-approved.
This C14A documentation checkpoint authorizes no next implementation step or
laboratory action. C06A's earlier `BLOCKED_BY_WRAPPER_BEHAVIOR` stop remains
historical evidence, not the current camera-runtime boundary.

Evidence labels used below:

- **VERIFIED:** local checks explicitly identified as such, or completed lab
  checks supplied as verified evidence in the C07, C10A, C12A, and C14A tasks.
  The lab checks were not independently repeated by Codex (ALEX).
- **REPORTED:** researcher/Architect reports without a corresponding verified
  check identified here.
- **PROPOSED:** design or candidate work, not implementation or approval.
- **UNKNOWN / NOT TESTED:** evidence or execution remains absent; no success
  is inferred from installation, import, or OS visibility.

**Architecture status: v0.2 PROPOSED.** Professor Nikita positively reviewed
the revised direction, as reported by the researcher/Architect for C01. This
is not blanket approval of runtime implementation, device automation,
validated safety limits, or experiments.

## Historical baseline — C00 / C01 (2026-11-26)

- **C00 read-only audit completed:** home Git repository on `main`, baseline HEAD
  `9455e3e` (`9455e3e4ec60d53bde708416756d591ad3bc9a44`), with a clean working
  tree as observed during C00. The remote server was not contacted.
- At that time, C00 found 13 documentation/diagram files and no runtime code,
  agents, tests, dependency manifests, SDK wrappers, or datasets. This is a
  historical observation; C04A has since added offline code and tests.
- **C01 documentation baseline:** the linked v0.2 draft records Scientist,
  Experimentalist, and Analyst as the proposed scientific core; Codex is
  the development coder, not a runtime scientific agent. Standalone
  Executioner and Scientific Reviewer are historical roles. Local
  Orchestrator coordinates significant state,
  history, and approvals while supporting direct technical clarification.
- Existing v0.1 architecture, roles, contracts, review brief, and diagrams
  are historical proposals where they contradict the supplied v0.2
  direction. They remain unchanged in C01. In particular, the old
  all-messages-through-Orchestrator rule is not the revised direction.
  Development safety and task-scope restrictions still apply.
- C01 added documentation only. C01 changes were uncommitted when verified
  locally in C04B; that is historical status, superseded by the C07 local
  repository check below.
  No hardware limits or operational software-control interfaces have been
  validated/established by this project. Initial real operations remain
  human-controlled and require authorization and deterministic restrictions.
- The home PC is primarily for development/offline tests; the lab PC is a
  separate environment. Its inventory was not performed in C01; the later
  inventory status is recorded below. No RustDesk or hardware access
  occurred in C00 or C01.
- **December 5, 2026** is the student's target for a first limited
  demonstration, not a guaranteed deadline or approved acceptance criterion.
- Transmission Matrix Retrieval remains excluded pending clarification of
  Professor Nikita's subsequent transmission-matrix planning-test suggestion;
  no scope change or experiment is authorized by that suggestion.

## Inventory evidence — C02A / C02B / C03A

The prior findings and user evidence below are recorded for handoff; C04B did
not access laboratory paths or the external SDK-source folder. C07 corrects
the workspace identity using the supplied verified laboratory history.

- **C02A historical correction — VERIFIED (supplied C07 evidence):**
  `D:\Nikita\TM benchmark` was the earlier name of the **same** laboratory
  workspace later renamed `D:\Nikita\LC characterization (Alex)`. It was
  not a separate Mkrtich project. The old path is stale historical naming
  only; earlier observations retain their original inspection scope.
- **Current LC laboratory workspace — VERIFIED (supplied C07 evidence):**
  `D:\Nikita\LC characterization (Alex)` currently contains only `AGENTS.md`.
  Its authorized path was manually updated in that file to the current name.
  Task-specific Python examples were supplied separately when needed and
  are not canonical project files in this lab workspace. The home repository
  is canonical for project/documentation; the lab workspace is the bounded
  equipment/SDK execution environment. Codex (ALEX) and Codex (LAB) are
  distinct executor contexts. C07 did not access the lab workspace.
- User visual evidence showed `raw-frame.bin`, `capture-result.json`, and
  `camera-frame.py` in a separate laboratory location. Ownership, exact
  location, format, provenance, and authorization for use remain unverified.
  They are **not LC project inputs yet**; their contents are not inferred.
- **C02B home-PC downloaded SDK-source inventory:** exactly four
  source/example files: `Blink_C_wrapper.h`, `open_SLM.py`, `open_Camera.py`,
  and `laser_control.py`. They provide interface/example evidence only.
  No DLLs, drivers, installers, LUT/calibration files, manuals, or complete
  vendor distributions were present in that downloaded folder. None of the
  four files was executed or imported; source values are not approved
  hardware limits.
- **C03A historical status:** broader inventory was deferred at C04B. The
  subsequent verified evidence is recorded below; it does not establish a
  complete laboratory inventory, operating limits, or unrestricted access.

## Laboratory capability validation — C07 baseline and C08A–C13A milestones

All **VERIFIED** laboratory facts in this section come from the completed
checks supplied in the C07, C10A, C12A, and C14A tasks, not new home-PC runtime or
hardware tests. C12A records the supplied C11A audit and C11B runtime report
without accessing the lab PC or independently repeating either check.
C14A records the supplied C13A runtime report on the same basis.

### VERIFIED — Windows device evidence

- Device Manager showed ALKERIA `Celera C12SX-M Master SuperSpeed Camera`
  and `Celera C12SX-M Slave SuperSpeed Camera`. At least the Slave explicitly
  showed "This device is working properly." Observed camera driver:
  provider Alkeria, version `1.2.3.3`, date `2013-05-02`.
- Meadowlark `SLM P1920`, manufacturer Meadowlark Optics, showed working
  properly; driver version `12.3.0.0`, date `2017-03-13`.
- `Communications Port (COM1)` exists and was shown working. Its association
  with the Viper laser is **UNKNOWN / NOT TESTED**.

### VERIFIED — installed software and native SDK inventory

Windows Installed Apps showed:

- Blink OverDrive Plus `1.1.4.851`.
- MaestroUSB3 `2.7.10`.
- VISA Shared Components `5.12.0` (64-Bit).
- VISA.NET Shared Components `5.11.0` (64-Bit).

ALKERIA SDK installation was verified at
`C:\Program Files\Alkeria\USB3\MaestroUSB3`, including native C++ and .NET
SDKs, DLLs, `.lib` files, headers, Celera examples, and SDK documentation.
This is installation evidence only; the later constructor result is recorded
below. Camera open/settings/acquisition and VISA instrument communication
remain **NOT TESTED**.

### VERIFIED — Python compatibility and native module loading

- Original inspected package:
  `C:\Users\Dell\AppData\Local\Programs\Python\Python312\Lib\site-packages\alkusb3`.
  It includes Python wrapper source, `_core.cp39-win_amd64.pyd`, and
  `CAlkUSB3-64.dll`.
- Classification: `CP39_ONLY_BINARY_PACKAGE`. No CPython 3.12 native
  extension or buildable native-extension source was found in the inspected
  package/archive. This finding is limited to the inspected material.
- Isolated environment: `C:\Users\Dell\Envs\PhotonicsAI-LC-py39`, with
  CPython `3.9.25`, Windows AMD64, and NumPy `1.26.4`. `alkusb3` was copied
  into it; source/destination package hashes matched.
- Existing Python 3.12 installations were not intentionally modified;
  Anaconda base was not targeted for modification; PATH was not modified.
- Plain `import alkusb3` succeeded and did **not** load `alkusb3._core`.
  Controlled `import alkusb3._core` subsequently succeeded, loading
  `_core.cp39-win_amd64.pyd`. No vendor function or class was invoked in
  that native-load test. Import success does not establish camera operation.

### VERIFIED — C06A static inspection and intentional stop

The wrapper exposes `device_interface.get_camera_list(self)` as an instance
method delegating to `self._obj.get_camera_list()`. The ordinary wrapper path
requires an existing native device/camera object. Static inspection did not
establish a sufficiently bounded discovery path without object construction.

**C06A status: `BLOCKED_BY_WRAPPER_BEHAVIOR`.** Actual discovery calls: **0**;
camera classes instantiated: **0**; camera acquisition: **0**; hardware query:
**0**. This was an intentional safety stop, not a software failure.

### VERIFIED — C08A-R1 static wrapper lifecycle audit

Exact inspected package:
`C:\Users\Dell\AppData\Local\Programs\Python\Python312\Lib\site-packages\alkusb3`.

- `device_interface.__init__(self, obj)` assigns `self._obj = obj`.
- `generic_camera.__init__(self, obj=None)` creates `_core.generic_camera()`
  when `obj is None`; `matrix_camera.__init__(self, obj=None)` similarly
  creates `_core.matrix_camera()` when `obj is None`.
- `celera_camera.__init__(self)` assigns `self._obj = _core.celera_camera()`.
- Python inheritance: `celera_camera -> matrix_camera -> generic_camera ->
  device_interface`. Associated native/SDK hierarchy:
  `ICeleraCamera -> IMatrixCamera -> IGenericCamera -> IDevice`.
- Python finalizers visibly clear `self._obj`; concrete native destruction
  semantics remained incompletely known.

### VERIFIED — C08B static DLL audit: construction/discovery coupling

Exact target DLL:
`C:\Program Files\Alkeria\USB3\MaestroUSB3\Libraries\C++\Lib\V100 x64\CAlkUSB3-64.dll`.
SHA-256: `93f4aa39752bcf60d9352d59fd9f8a184deda2e3246aa9d9a5f45d48d5184adf`.
The package DLL had the identical hash. Target file/product version was
`2.5.24.0`; previously observed Installed Apps version was MaestroUSB3
`2.7.10`. The reason for this version difference is not established.

Static disassembly established a conditional reachable path from
`ICeleraCamera::Create()` through native construction/global initialization
to Windows SetupAPI device discovery/enumeration, including reachable calls to:

- `SetupDiGetClassDevsW`
- `SetupDiEnumDeviceInfo`
- `SetupDiGetDeviceRegistryPropertyW`
- `SetupDiEnumDeviceInterfaces`
- `SetupDiGetDeviceInterfaceDetailW`

Construction and device discovery/enumeration are **not separable stages for
this inspected implementation**. This establishes OS discovery/enumeration on
a reachable construction path; it does not establish that every construction
opens a physical camera, performs physical USB transfers, accesses settings or
registers, starts acquisition, or creates a camera device handle.

C08B counts: vendor DLL loads/executions **0**; `alkusb3` imports **0**;
vendor constructors invoked **0**; hardware actions **0**.

### VERIFIED — C09A blocked pre-flight and C09A-PREFLIGHT-R1 correction

The initially expected interpreter
`C:\Users\Dell\Envs\PhotonicsAI-LC-py39\Scripts\python.exe` did not exist.
That attempt stopped at pre-flight: no Python process, import, constructor,
or hardware action occurred. It is not a physical experiment-log entry.

C09A-PREFLIGHT-R1 found the actual interpreter at
`C:\Users\Dell\Envs\PhotonicsAI-LC-py39\python.exe`, verified Python
`3.9.25`, and verified by filesystem check that `alkusb3` exists at
`C:\Users\Dell\Envs\PhotonicsAI-LC-py39\Lib\site-packages\alkusb3`.
No vendor import or hardware action occurred during this pre-flight.

### VERIFIED — C09A-R2 PASS: approved construction and ordinary teardown

Explicit human approval:

> APPROVE C09A exactly as specified. Construction + implicit discovery +
> ordinary process teardown are approved. No enumeration method calls,
> settings access, camera open, or acquisition.

The runtime used `C:\Users\Dell\Envs\PhotonicsAI-LC-py39\python.exe`,
Python `3.9.25`, `PYTHONDONTWRITEBYTECODE=1`, and Python `-B`.
Vendor Python processes: **1**; `celera_camera` constructor attempts: **1**.
Observed stdout:

```text
CONSTRUCTION_STARTED
CONSTRUCTION_SUCCEEDED
WRAPPER_TYPE=alkusb3.celera_camera.celera_camera
```

Stderr: **NONE**. Process exit code: **0**. Ordinary Python process teardown
completed; explicit vendor cleanup calls: **0**.

Safety counts were **0** for each: explicit `get_camera_list` calls; explicit
enumeration calls; SetCamera/open calls; settings reads; settings writes;
acquisition calls; frames captured; SLM actions; RIGOL/VISA actions; laser/COM
actions; retry attempts; environment/system changes.

This was a hardware-adjacent camera-stack runtime interaction, not a
measurement. It does not establish that a physical camera was opened, either
Master/Slave camera was selected, settings are accessible, acquisition or
frame capture works, or camera operating limits are validated.
The actual action is recorded in [EXPERIMENT_LOG.md](EXPERIMENT_LOG.md).

### VERIFIED — C11A static return-value audit

- Python `device_interface.get_camera_list(self)` returns
  `self._obj.get_camera_list()`; the native SDK signature is
  `virtual Array<String> GetCameraList()`.
- The native result is an owning value array of string values. The Python
  binding converts it into a built-in Python `list` containing built-in
  Python `str` entries.
- After the call returns, `type(result)`, `len(result)`, iteration,
  `type(entry)`, reading/printing returned display-name strings, and
  positional indices are local Python observations requiring no additional
  vendor SDK call.
- Device serial number, device camera property, name/device properties,
  `active_interfaces`, `super_speed`, and similar properties are separate
  native accesses and remain outside the approved boundary. A returned
  display-name string is distinct from a device property access.
- Vendor examples show `GetCameraList` / count / names before `SetCamera`.

**C11A verdict: A. `LIST_RESULT_IS_SAFE_VALUE_DATA`.** This finding concerns
observation **after** `GetCameraList` returns. It neither establishes nor
authorizes all internal activity inside that call, and it grants no runtime
permission to inspect returned display-name strings.

### VERIFIED — C11B PASS: approved explicit camera-list observation

The supplied C11B report records explicit human approval of one construction,
one `get_camera_list` call, return/exception, Python result type, list length,
and ordinary process teardown; no retry. The exact approval, stdout, safety
counts, and deviations are preserved in the C11B entry in
[EXPERIMENT_LOG.md](EXPERIMENT_LOG.md).

- Interpreter: `C:\Users\Dell\Envs\PhotonicsAI-LC-py39\python.exe`, Python
  `3.9.25`; `PYTHONDONTWRITEBYTECODE=1`; Python `-B`; one Python process.
- Explicit imports: **1**; constructor attempts: **1**, succeeded;
  `get_camera_list` calls: **1**, returned successfully.
- Exact result type: **`builtins.list`**; exact result length: **1**.
- Stderr: **NONE**; exit code: **0**; ordinary process teardown: **yes**;
  explicit cleanup calls: **0**; retries: **0**.
- Camera-name observations, SetCamera/open/select, property reads, settings
  reads/writes, acquisitions, frames, and other-device actions: **0** each.
- GUI/dialog/UAC: none observed at the initial check; independent continuous
  visual monitoring was not performed.

**Strict interpretation boundary:** `RESULT_LENGTH=1` means only:

> During this exact approved GetCameraList invocation, the SDK returned one Python list entry.

It does not establish that only one physical camera exists or only one
Celera device is connected, that the entry is Master or Slave, that prior OS
visibility of two Celera device entries was wrong, that a camera is defective
or unavailable, or that camera selection/open works. The relationship between
the previously observed OS device entries and this SDK result length is
**UNKNOWN**. The returned entry was not inspected. No optical measurement
was produced.

### VERIFIED — C13A PASS: approved display-name observation

Human-approved scope: one `celera_camera` construction, one `get_camera_list`
call, observation of result type and length, and only if length equals `1`,
observation of exactly `result[0]`; ordinary teardown; no retry. No
SetCamera/open/select, properties, settings, acquisition, or frame capture
was approved or performed, according to the supplied C13A report.

- Interpreter: `C:\Users\Dell\Envs\PhotonicsAI-LC-py39\python.exe`, Python
  `3.9.25`; one Python process.
- Constructor attempts: **1**, succeeded; `get_camera_list` calls: **1**, returned.
- Result type: **`builtins.list`**; result length: **1**.
- Exact returned display-name string: **`CELERA C12SX-M s/n A0805E3B`**.
- Camera-name observations: **1**; SetCamera/open/select, property reads,
  settings reads/writes, acquisitions, frames captured, retries, and
  other-device actions: **0** each.
- Stderr: **NONE**; exit code: **0**; ordinary teardown: **completed**;
  GUI/dialog/UAC: **none observed**; deviations: **none**.

The verified fact is:

> During the approved C13A invocation, get_camera_list returned one entry whose exact display-name string was 'CELERA C12SX-M s/n A0805E3B'.

This does not establish that `A0805E3B` is Master or Slave, that only one
physical camera exists, that the other previously observed Windows device
node is absent or broken, or that SetCamera/open, settings, or acquisition
will work. The mapping between the SDK-returned entry and the previously
observed Windows Master/Slave entries remains **UNKNOWN**. No optical
measurement was produced. Exact stdout and all supplied safety counts are
recorded in the single C13A entry in [EXPERIMENT_LOG.md](EXPERIMENT_LOG.md).

### UNKNOWN / NOT TESTED — remaining camera and hardware boundary

- Mapping of `A0805E3B` to the previously observed Windows Master/Slave device
  node; physical camera identity and device count are not established.
- Reason the SDK list count is `1` while two Windows Celera device entries
  were previously observed.
- SetCamera / explicit open/select.
- Property reads, including serial/model/device properties.
- Settings reads.
- Settings writes.
- Acquisition.
- Frame capture.
- Hotplug/list behavior and complete internal `GetCameraList` discovery behavior.
- Complete native destruction side effects.
- Validated hardware operating limits, including camera limits (remain `TBD`).

Exact physical USB activity and camera device-handle creation also remain
unverified. Construction/list-call success, display-name observation, and
normal process exit do not resolve these unknowns; the static reachable
discovery path is not a runtime USB trace.

Still not authorized/performed through this project: SLM pattern write,
RIGOL/VISA command, COM1 laser command, or laser state change.
[EXPERIMENT_LOG.md](EXPERIMENT_LOG.md) now contains three runtime-action entries
(C09A-R2, C11B, and C13A) and no measurement; software inventory, static audits,
and blocked pre-flight checks are not backfilled as physical experiments.

## Completed offline component — C04A

C04A created:

- [docs/MEASUREMENT_INPUT_V1.md](docs/MEASUREMENT_INPUT_V1.md)
- [src/photonicsai_analyst/__init__.py](src/photonicsai_analyst/__init__.py)
- [src/photonicsai_analyst/__main__.py](src/photonicsai_analyst/__main__.py)
- [src/photonicsai_analyst/measurement_bundle.py](src/photonicsai_analyst/measurement_bundle.py)
- [tests/test_measurement_bundle.py](tests/test_measurement_bundle.py)

This is the first deterministic offline component for the future Analyst,
with a JSON CLI and automated tests. It validates the **PROPOSED Measurement
Input v1** structure, metadata, paths, SHA-256 consistency, and 8-/16-bit
grayscale PNG containers. It does not authenticate provenance, decode pixels,
perform scientific analysis, or access camera SDKs or hardware. All generated
test data is explicitly `test_fixture`, never experimental data.

**Verified C04A test result:** 36 tests run, 34 passed, 2 skipped because
Windows link-creation privilege was unavailable, 0 failures. All 14 required
scenarios passed; mocked link/reparse rejection tests also passed. The C04B
rerun reproduced this result. Real Windows symlink/junction integration
remains unverified.

## Historical completed record — v0.1 Steps 01–08

The record below is preserved from the 2026-11-03 handoff. Review status,
pending notes, and statements about unchanged files in these entries describe
their historical steps, not the current v0.2 baseline.

**Step 01 — architecture documentation (verified by source inspection and link checks)**

- Architecture v0.1: [ARCHITECTURE.md](ARCHITECTURE.md)
- Agent workflow diagram (Mermaid source):
  [docs/diagrams/agent_workflow.mmd](docs/diagrams/agent_workflow.mmd)
- Proposed logical data contracts: [DATA_CONTRACTS.md](DATA_CONTRACTS.md)
- Facts, provisional decisions, and open questions: [DECISIONS.md](DECISIONS.md)
- Agent rules and roles: [AGENTS.md](AGENTS.md), [CLAUDE.md](CLAUDE.md)
- Project overview: [README.md](README.md)

**Step 02 — documentation review fixes (Architect review of v0.1; not a redesign)**

- AGENTS.md: proposed **tools** (executable capabilities) and **skills**
  (documented procedures) are now listed separately for each scientific
  agent, with definitions of both.
- ARCHITECTURE.md: consistency edits only. Adapter row (no laser software
  interface assumed), tools vs. skills reference, flow types and the
  simplified physical path (§7), and H4 is conditional on the optional Coder.
- Diagram: separate tools/skills on each agent; two-way H1–H4 checkpoint
  paths (H2 marked mandatory, H4 optional); distinct line styles for
  artifacts, hardware control, and physical optical/electrical paths;
  physical path Laser → SLM → LC cell → Camera and RIGOL → LC cell; laser
  software interface shown as TBD; a renewed-H2 rule for loops; and an
  in-diagram legend. The Chief Orchestrator boundary is kept.
- Claude Code rules added:
  [.claude/rules/architecture-review.md](.claude/rules/architecture-review.md),
  [.claude/rules/context-handoff.md](.claude/rules/context-handoff.md).
- The diagram source was inspected, but **visual rendering is still pending**
  (no Mermaid renderer is installed locally).

**Step 03 — visual check of the detailed diagram (reported by the researcher/Architect)**

- [agent_workflow.mmd](docs/diagrams/agent_workflow.mmd) rendered
  successfully in Mermaid Live and received the Architect's visual review.
- Finding: technically comprehensive, but too crowded for presentation
  (38 edges, many crossings, small text). It is kept unchanged as the
  technical reference.

**Step 04 — simplified professor-facing diagram (source created; not visually validated)**

- New primary review diagram:
  [docs/diagrams/professor_overview.mmd](docs/diagrams/professor_overview.mmd).
  Five layers (human and external platform → Local Orchestrator → six agents
  → Safety Gateway and adapters → optical bench), one hub-and-spoke
  artifact edge, the artifact chain and H1–H4 shown as node text, no
  `linkStyle` index rules. It is a visual simplification only: no
  components, roles, contracts, or decisions were changed.
- README marks it as the primary diagram for professor review.
- Later rendered successfully by the researcher in Mermaid Live and visually
  reviewed by the Architect: logically acceptable, but far too tall and
  narrow for presentation (PNG about 430 × 2048 px).

**Step 05 — compact landscape layout of the professor overview (rendered and reviewed; two ambiguous hardware links)**

- [professor_overview.mmd](docs/diagrams/professor_overview.mmd) now uses
  `flowchart LR`: human + Chief Orchestrator → Local Orchestrator (with
  workflow, artifact, feedback, and legend notes) → six agents → hardware
  side (Safety Gateway and adapters above a compact optical bench).
- Each agent has its own unlabeled two-way edge to the Orchestrator; no
  agent-to-agent edges. Emojis removed. Layout only: no components, roles,
  contracts, or decisions were changed.
- Later rendered successfully by the researcher in Mermaid Live and visually
  reviewed by the Architect: structurally correct overall, but with two
  ambiguous hardware connections. (1) The Executioner edge ends at the
  enclosing hardware container instead of the Safety Gateway. (2) The
  adapters edge goes to the whole optical bench, including the laser. The
  Mermaid source is kept unchanged as the editable overview.

**Step 06 — controlled-layout professor-facing SVG (created; human visual review pending)**

- New primary presentation diagram:
  [docs/diagrams/professor_overview.svg](docs/diagrams/professor_overview.svg)
  (hand-positioned SVG, viewBox 1920×1080, no scripts or external assets).
  Layout: human (top) and Chief Orchestrator (bottom, future, not
  integrated) around the Local Orchestrator, with a labeled routing bus that
  is part of the Orchestrator → six agents in a 3×2 grid, each with one
  proposed Tool and one proposed Skill → Safety Gateway, adapters, and
  optical bench. Plus a logical-workflow note and a legend.
- Both Step 05 ambiguities are resolved: the Executioner arrow ends at the
  Safety Gateway box itself, and three separate adapter arrows end only at
  the SLM, RIGOL DG812, and camera. No software link reaches the laser
  ("no software control assumed").
- Verified: well-formed XML; viewBox; all text and connectors inside the
  canvas; no text overlaps (estimated with system-font metrics); required
  components and labels present. A headless-browser preview was rendered
  by Claude Code for a layout self-check. **This is not the required human
  visual review, which is still pending.**
- Mermaid sources and all other documents are unchanged. No components,
  roles, contracts, or decisions were changed.

**Step 06 follow-up — human visual review of the SVG (reported by the researcher/Architect)**

- The researcher opened [professor_overview.svg](docs/diagrams/professor_overview.svg)
  in a browser, and the ChatGPT Architect reviewed the screenshot.
- Visual review passed. The diagram is **accepted for professor
  presentation.** The SVG was not changed.
- This is acceptance of the diagram only. **The architecture remains
  PROPOSED** and is not approved by the professor.

**Step 07 — professor review brief (created; verified by source inspection and link checks)**

- New accompanying document:
  [docs/PROFESSOR_REVIEW_BRIEF.md](docs/PROFESSOR_REVIEW_BRIEF.md):
  objective, architecture overview, one Tool and one Skill per agent (from
  AGENTS.md), a conceptual voltage-response workflow (no experiment run, no
  values specified), safety boundaries, five questions selected from
  DECISIONS.md, and review status.
- README links the brief as the accompanying document for the first
  professor review. No architecture, contracts, decisions, or diagrams were
  changed.
- The brief has not yet been reviewed by the researcher, and nothing has
  been sent to the professor.

**Step 07 follow-up — Architect content review of the brief (reported by the researcher/Architect)**

- Passed the ChatGPT Architect's content review. One gap was identified: the
  brief did not ask about the expected MVP deliverable and objective success
  criteria.

**Step 08 — final brief refinement (verified by source inspection, link checks, and word count)**

- [DECISIONS.md](DECISIONS.md#open-questions-for-professor-review): added
  **OPEN** question 12 (expected minimum working prototype after
  architecture approval, and its observable, measurable success criteria).
  It concerns the phase after the first deliverable (the architecture
  diagram). No MVP scope or evaluation criteria have been approved. All
  earlier decisions and questions, including dry-run (Q7), are unchanged.
- [docs/PROFESSOR_REVIEW_BRIEF.md](docs/PROFESSOR_REVIEW_BRIEF.md): condensed
  without structural or content changes; review question 5 now asks Q12
  instead of Q7 (dry-run stays OPEN in DECISIONS.md). Still five questions.
- The SVG remains accepted for professor presentation and was not changed.
  **The architecture remains PROPOSED.** No architecture, roles, contracts,
  or diagrams were changed. Nothing has been sent to the professor.

## Current implementation status

**IMPLEMENTED:** deterministic offline Measurement Input v1 validator, CLI,
and automated tests (C04A; C07 local working tree was clean on entry).

**NOT IMPLEMENTED:** runtime LLM agents; Local Orchestrator runtime; shared
knowledge catalogue runtime; reusable Experimental Skills runtime;
camera/SLM/RIGOL/laser adapters; hardware Safety Gateway enforcement;
pixel-level scientific analysis; real-data ingestion demonstrated with
verified LC measurements. The offline validator does not establish lab
readiness or approved hardware settings.

## Repository

**VERIFIED LOCALLY (C14A; no network access):**

- Branch: `main`; HEAD: `fd406b46d4fcfcab62e328f9d788b883cb281f63`, matching
  the required C14A checkpoint.
- Working tree clean on entry: `git status --short` and `git diff --stat`
  produced no output; no staged changes.
- C14A changes only `CURRENT_STATE.md`, `DECISIONS.md`, and `EXPERIMENT_LOG.md`.
  These documentation changes remain uncommitted. No staging, commit, push,
  fetch, pull, remote contact, lab-PC access, RustDesk, Python execution, or
  hardware action in C14A.
- Current remote contents and synchronization remain independently unverified.

**Historical local snapshot (C12A; superseded by the C14A check above):**

- Branch: `main`; HEAD: `81c07ddfa8b927ae10ed9c3bc4075eda377a9d5f`, matching
  the required C12A checkpoint.
- Working tree clean on entry: `git status --short`, `git diff --stat`, and
  `git diff` produced no output; no staged changes.
- C12A changes only `CURRENT_STATE.md`, `DECISIONS.md`, and `EXPERIMENT_LOG.md`.
  These documentation changes remain uncommitted. No staging, commit, push,
  fetch, pull, remote contact, lab-PC access, Python execution, or hardware
  action in C12A.
- Current remote contents and synchronization remain independently unverified.

**Historical local snapshot (C10A; superseded by the C12A check above):**

- Branch: `main`; HEAD: `e71cbc5c73fffcfb992b6599ae6f2e4e40827ee9`, matching
  the supplied canonical checkpoint `e71cbc5`.
- Working tree clean on entry: `git status --short`, `git diff --stat`, and
  `git diff` produced no output; no staged changes.
- C10A changes only `CURRENT_STATE.md`, `DECISIONS.md`, and `EXPERIMENT_LOG.md`.
  These documentation changes remain uncommitted. No staging, commit, push,
  fetch, pull, remote contact, lab-PC access, or hardware action in C10A.
- Current remote contents and synchronization remain independently unverified.

**Historical local snapshot (C07; superseded by the C10A check above):**

- Branch: `main`; no branch change.
- HEAD: `7ff0b3b55a0a7517f5f87332c8421b6da62c11a8`.
- Working tree clean on entry (`git status --short` produced no output);
  no staged files. The C04B uncommitted-work description below is historical.
- C07 changes only `CURRENT_STATE.md`, `DECISIONS.md`, and the new
  `EXPERIMENT_LOG.md`; no staging, commit, push, fetch, or pull.
- C07 did not contact the remote server; current remote contents and
  synchronization were not independently reverified. User-reported push
  evidence for the existing checkpoint is recorded below. The new C07
  documentation changes were uncommitted/unpublished at that snapshot.

**Historical local snapshot (C04B; superseded by later checks above):**

- Branch: `main`.
- HEAD: `9455e3e4ec60d53bde708416756d591ad3bc9a44` (the C00 baseline).
- Configured `origin`: `https://github.com/aleksandrhajoyan/LC-Characterization.git`.
- Working-tree status on entry (same paths after C04B):

  ```text
   M CURRENT_STATE.md
  ?? docs/ARCHITECTURE_V02_DRAFT.md
  ?? docs/MEASUREMENT_INPUT_V1.md
  ?? src/
  ?? tests/
  ```

- Staged files were none. C01 documentation and C04A files were uncommitted
  at that snapshot, before the later checkpoint/push reported below. C04B
  modified only this already-modified handoff and did not stage or commit
  anything.

**USER-REPORTED TERMINAL EVIDENCE:** a previous successful push reported
`9455e3e..7ff0b3b  main -> main`, establishing user-reported publication of
commit `7ff0b3b` to `origin/main`. That checkpoint contains the previously
committed C01/C04A/C04B work. An earlier reported `git push -u origin main`
also established tracking of `origin/main`. These are user terminal reports,
separate from C07's local checks: C07 did not contact the remote server or
independently reverify its current state. The new C07 documentation changes
were not included in that reported published checkpoint; their current remote
publication status is not independently verified.

## Pending

- C04A Architect review has passed. C14A verified the clean canonical local
  checkpoint `fd406b46d4fcfcab62e328f9d788b883cb281f63` on entry. Current remote
  state remains independently unverified; the C14A documentation changes
  remain uncommitted/unpublished.
- Read-only OS/device-metadata reconciliation to determine whether serial
  `A0805E3B` can be mapped to the previously observed Windows Master or Slave
  device node, without opening/selecting the camera. This next LAB step is
  **OPEN and unapproved** and must be separately bounded by the Architect
  and explicitly human-approved; completed C13A approval does not cover it.
- Any further laboratory inventory or hardware access needs its own bounded
  task authorization; the supplied checks do not grant broader permission.
- Researcher/Architect review of the
  [v0.2 draft](docs/ARCHITECTURE_V02_DRAFT.md) and resolution of its OPEN items.
- Limited demonstration scope, initial metric, input measurements/metadata,
  execution mode, and measurable success criteria for the student's target.
- Equipment/SDK documentation, validated safety limits (currently `TBD`),
  procedure validation/reuse criteria, and real-operation approval rules.
- Later reconciliation of historical roles, contracts, diagrams, and
  instructions under a separately authorized task. Historical open questions
  in [DECISIONS.md](DECISIONS.md#open-questions-for-professor-review) remain
  reference material. C07 appends operational decisions without migrating
  the historical architecture decisions or contracts.

## Known blockers and unknowns

- No validated device operating limits or implemented command-level safety
  enforcement exist yet. Native-load validation grants no hardware-action
  permission. C09A-R2 construction, C11B's success/type/length observation,
  and C13A's display-name observation were narrowly approved and completed;
  further camera escalation requires separate review and human approval.
- The mapping of `A0805E3B` to Windows Master/Slave and the reason for one SDK
  list entry versus two previously observed Windows Celera entries remain
  **UNKNOWN**. SetCamera/open/select, property reads, settings reads/writes,
  acquisition, and frame capture remain **NOT TESTED**.
- Whether the laser has (or should have) any software interface is unknown.
- The Chief Orchestrator interface is unknown.
- C02B provides source/example interface evidence only. The supplied later
  lab checks establish the specific installed software, drivers, SDK, and
  Python compatibility recorded above. Camera operation, VISA communication,
  laser interface identity, and approved operating limits remain unverified.
  PyVISA control of the RIGOL DG812 remains a plan.
- The priority of the characterization metrics has not been decided.
- Positive feedback on the direction does not establish a working system or
  permission for unattended procedure reuse. Deterministic command-level
  enforcement is required but not implemented.
- The proposed shared knowledge catalogue, role-owned knowledge, and
  Draft → Validated → Approved for reuse lifecycle have no implementation.
- Transmission-matrix planning-test scope and migration of the historical
  contracts/checkpoints remain OPEN.

## Current next technical step — OPEN, not approved

**Read-only OS/device-metadata reconciliation to determine whether serial
`A0805E3B` can be mapped to the previously observed Windows Master or Slave
device node, without opening/selecting the camera.** This next LAB step
remains **OPEN and unapproved** and must be separately bounded by the
Architect and explicitly human-approved. C13A's completed display-name
observation grants no permission for this step or other escalation.
SetCamera/open/select, property reads, settings reads/writes, acquisition,
and frame capture remain separate later stages requiring their own review
and explicit human approval. This documentation task authorizes no LAB step.

A small offline image-QC/measurement-analysis layer on validated Measurement
Input v1 bundles remains a **PROPOSED** home-PC development candidate, subject
to separate task authorization and justified scientific criteria. No next
implementation step is started by C14A. The December 5 target remains a
limited demonstration target, not a promise of full autonomy.
