# Experiment Log

Three hardware-adjacent camera-stack runtime interactions are recorded below
(C09A-R2, C11B, and C13A). No optical measurement has been produced.

This append-oriented log is reserved for REAL physical/hardware experimental
actions and measurements, including the explicitly approved C09A-R2, C11B,
and C13A camera-stack runtime interactions. Software inventory, package
inspection, environment setup, and import/native-load validation are not
experiment entries and are not backfilled here. C06A stopped before hardware;
it produced no experiment.

Entries must record what actually happened, not intended or simulated
results. Distinguish intended action from actual action; do not invent missing
measurements, settings, data, or success. Mark unknown information `TBD` and
inapplicable fields `N/A` with a reason. Record physical quantities with units
and the source of settings; literature values are not approved settings.
Append corrections with the entry reference and preserve the original record.
An entry or this template does not authorize an action.

## Reusable entry template — not an experiment entry

Copy and complete only for an actual authorized hardware action. Replace
placeholders with the observed record, including denied, aborted, or partial
outcomes where applicable.

```text
Entry ID: <unique identifier>
Date/time and timezone: <actual time, UTC offset, and named timezone>
Operator: <actual operator>
Procedure/version: <identifier and version>
Approval/reference: <recorded human approval and authorized scope>
Equipment: <actual equipment and identifiers, if known>
Sample: <actual sample identifier>
Intended action: <approved planned action>
Actual action: <what was actually done, including any stop>
Parameters with units: <actual values, units, and setting sources>
Files/data produced: <actual paths/references, or none with reason>
Observed result: <observations; distinguish from interpretation>
QC checks: <checks actually performed and outcomes>
Uncertainty / limitations: <known uncertainty, missing evidence, limitations>
Deviations: <departures from procedure, or none observed>
Safety notes: <actual checks, denials, faults, or stop conditions>
Status: <actual completion/partial/aborted/denied outcome and reason>
```

## Physical experiment entries

<!-- Append actual entries here; the template above is not an entry. -->

### C09A-R2 — camera-stack construction runtime interaction (not a measurement)

- **Entry ID:** C09A-R2.
- **Date/time and timezone:** 2026-11-26; exact execution time not captured in
  the supplied report; Asia/Yerevan (+04:00).
- **Operator:** Aleksandr Hajoyan, human-approved execution via Codex (LAB).
- **Procedure/version:** `C09A-R2-CAMERA-CONSTRUCTION-IMPLICIT-DISCOVERY`.
- **Approval/reference:** explicit C09A human approval:

  > APPROVE C09A exactly as specified. Construction + implicit discovery +
  > ordinary process teardown are approved. No enumeration method calls,
  > settings access, camera open, or acquisition.

- **Equipment:** ALKERIA Celera camera stack; exact camera unit selection
  not performed.
- **Sample:** N/A — no optical measurement or sample interaction.
- **Intended action:** one `celera_camera` construction with already-known
  implicit SDK discovery, no explicit enumeration/open/settings/acquisition.
- **Actual action:** one constructor attempt succeeded; wrapper type was
  observed; process exited normally with ordinary Python process teardown.
  Explicit vendor cleanup calls: `0`.
- **Runtime:** `C:\Users\Dell\Envs\PhotonicsAI-LC-py39\python.exe`, Python
  `3.9.25`; `PYTHONDONTWRITEBYTECODE=1`; Python `-B`; vendor Python processes:
  `1`; constructor attempts: `1`.
- **Parameters with units:** N/A — no camera operating parameter was read or
  changed.
- **Files/data produced:** none.
- **Observed result:** stdout:

  ```text
  CONSTRUCTION_STARTED
  CONSTRUCTION_SUCCEEDED
  WRAPPER_TYPE=alkusb3.celera_camera.celera_camera
  ```

  Stderr: none. Process exit code: `0`.
- **QC checks:** single attempt, no retry; explicit prohibited-call counts
  remained zero, based on the supplied execution report.
- **Uncertainty / limitations:** the implicit constructor path is statically
  known to include a conditional reachable path to OS discovery/enumeration;
  exact physical USB activity and complete native teardown effects remain
  unverified. Success does not establish physical camera open, Master/Slave
  selection, settings access, acquisition, frame capture, or validated
  camera operating limits.
- **Deviations:** none from approved runtime scope, based on the supplied
  execution report.
- **Safety notes:** each reported count was `0`: explicit `get_camera_list`
  calls; explicit enumeration calls; SetCamera/open calls; settings reads;
  settings writes; acquisition calls; frames captured; SLM actions; RIGOL/VISA
  actions; laser/COM actions; retry attempts; environment/system changes.
- **Status:** completed successfully within approved narrow scope; no
  measurement produced. This entry records supplied verified evidence and
  does not authorize further action.

### C11B — explicit camera-list runtime observation (not a measurement)

- **Entry ID:** C11B.
- **Date/time and timezone:** 2026-11-28; exact execution time not captured in
  the supplied report; Asia/Yerevan (+04:00).
- **Operator:** Aleksandr Hajoyan, human-approved execution via Codex (LAB).
- **Procedure/version:** `C11B-MINIMUM-EXPLICIT-CAMERA-LIST-RUNTIME`.
- **Approval/reference:** explicit C11B human approval:

  > APPROVE C11B exactly as specified: one celera_camera construction, one get_camera_list call, observe only return/exception, Python result type, and list length; no camera names, SetCamera/open, properties/settings, or acquisition. Ordinary process teardown approved. No retry.

- **Equipment:** ALKERIA Celera camera stack; exact physical unit
  corresponding to the returned entry not identified.
- **Sample:** N/A — no optical measurement or sample interaction.
- **Intended action:** one `celera_camera` constructor + one explicit
  `get_camera_list` (`GetCameraList`) call; observe only return/exception,
  Python result type, and list length; ordinary process teardown approved.
- **Actual action:** one constructor attempt succeeded; one
  `get_camera_list` call returned `builtins.list`, length `1`. Ordinary
  process teardown completed; explicit cleanup calls: `0`.
- **Runtime:** `C:\Users\Dell\Envs\PhotonicsAI-LC-py39\python.exe`, Python
  `3.9.25`; `PYTHONDONTWRITEBYTECODE=1`; Python `-B`; Python processes: `1`;
  explicit imports: `1`; constructor attempts: `1`; `get_camera_list` calls: `1`.
- **Parameters with units:** N/A — no camera operating parameter was read
  or changed.
- **Files/data produced:** none; no measurement produced.
- **Observed result:** exact stdout:

  ```text
  CONSTRUCTION_STARTED
  CONSTRUCTION_SUCCEEDED
  GET_CAMERA_LIST_STARTED
  GET_CAMERA_LIST_RETURNED
  RESULT_TYPE=builtins.list
  RESULT_LENGTH=1
  ```

  Stderr: **NONE**. Process exit code: `0`. GUI/dialog/UAC: none observed at
  the initial check; independent continuous visual monitoring was not performed.
- **QC checks:** one process, one constructor attempt, one `get_camera_list`
  call, zero retries; constructor succeeded and call returned successfully,
  based on the supplied report.
- **Uncertainty / limitations:** returned entry not inspected; returned
  display-name string and physical camera identity unknown; no Master/Slave
  mapping established. The relationship to previously observed OS
  Master/Slave device entries is **UNKNOWN**. Internal discovery behavior and
  hotplug/list behavior are not fully characterized. `RESULT_LENGTH=1` means
  only: "During this exact approved GetCameraList invocation, the SDK returned
  one Python list entry." It does not establish physical-camera count,
  connected-Celera count, Master/Slave identity, an error in earlier OS
  visibility, camera defect/unavailability, or successful camera selection/open.
  C11A's post-return value-data finding does not establish or authorize all
  activity inside `GetCameraList`.
- **Deviations:** workspace root was listed before reading `AGENTS.md`;
  the listing showed only `AGENTS.md`. Python version was verified via
  executable metadata rather than launching an additional Python process.
- **Safety notes:** each reported count was `0`: camera-name observations;
  SetCamera/open/select; property reads; settings reads; settings writes;
  acquisitions; frames captured; explicit cleanup calls; SLM actions;
  RIGOL/VISA actions; laser/COM actions; retries; project modifications;
  persistent environment/system changes; Git operations. These counts refer
  to the C11B execution report, not this C12A documentation reconciliation.
- **Status:** completed successfully within approved scope; no measurement
  produced. This entry records supplied evidence, not a repeated runtime
  test, and grants no approval for further runtime action. Future observation
  of a returned display-name string remains OPEN and unapproved.

### C13A — conditional camera display-name observation (not an optical measurement)

- **Entry ID:** C13A.
- **Date/time and timezone:** 2026-11-28, exact time not captured,
  Asia/Yerevan (+04:00).
- **Operator:** TBD — not specified in the supplied C13A facts.
- **Procedure/version:** C13A; further version identifier not supplied (TBD).
- **Approval/reference:** supplied human-approved C13A scope: one
  `celera_camera` construction; one `get_camera_list` call; observe result
  type and length; only if length equals `1`, observe exactly `result[0]`;
  ordinary teardown; no retry. No SetCamera/open/select, properties,
  settings, acquisition, or frame capture.
- **Equipment:** ALKERIA Celera camera stack; SDK-returned display name
  `CELERA C12SX-M s/n A0805E3B`; Windows Master/Slave mapping **UNKNOWN**.
- **Sample:** N/A — no optical measurement or sample interaction.
- **Intended action:** the single constructor/list call and conditional
  display-name observation within the approved scope above.
- **Actual action:** one constructor attempt succeeded; one
  `get_camera_list` call returned; result type and length were observed;
  because length was `1`, exactly `result[0]` was observed once. Ordinary
  teardown completed; no retry. No camera was selected/opened. No
  acquisition occurred.
- **Runtime:** executable `C:\Users\Dell\Envs\PhotonicsAI-LC-py39\python.exe`;
  Python `3.9.25`; process count: `1`; constructor attempts: `1`, succeeded;
  `get_camera_list` calls: `1`, returned.
- **Parameters with units:** N/A — no operating parameter was changed;
  property reads and settings reads/writes were `0`.
- **Files/data produced:** none; files modified: `0` in the C13A runtime.
  No measurement produced.
- **Observed result:** `builtins.list`, length `1`; exact display-name
  string: `CELERA C12SX-M s/n A0805E3B`. Exact stdout:

  ```text
  CONSTRUCTION_STARTED
  CONSTRUCTION_SUCCEEDED
  GET_CAMERA_LIST_STARTED
  GET_CAMERA_LIST_RETURNED
  RESULT_TYPE=builtins.list
  RESULT_LENGTH=1
  DISPLAY_NAME=CELERA C12SX-M s/n A0805E3B
  ```

  Stderr: **NONE**. Exit code: `0`. Ordinary teardown: completed.
  GUI/dialog/UAC: none observed.
- **QC checks:** one process, one successful constructor, one returned
  `get_camera_list` call, one conditional camera-name observation, zero
  retries, based on the supplied C13A report.
- **Uncertainty / limitations:** during the approved C13A invocation,
  `get_camera_list` returned one entry whose exact display-name string was
  `CELERA C12SX-M s/n A0805E3B`. This does not establish that `A0805E3B` is
  Master or Slave, that only one physical camera exists, or that the other
  previously observed Windows device node is absent or broken. The mapping
  between this SDK-returned entry and the Windows Master/Slave device
  entries remains **UNKNOWN**, as does the reason for one SDK entry versus
  two previously observed Windows entries. SetCamera/open/select,
  properties, settings, acquisition, and frame capture remain untested;
  successful display-name observation does not establish camera operability.
- **Deviations:** none.
- **Safety notes:** camera-name observations: `1`. Each reported count was
  `0`: SetCamera/open/select; property reads; settings reads; settings
  writes; acquisitions; frames captured; retries; SLM; RIGOL/VISA;
  laser/COM; files modified; persistent environment/system changes;
  Git operations. These counts refer to the C13A runtime, not this C14A
  documentation reconciliation.
- **Status:** **PASS**, completed within approved scope; hardware-adjacent
  runtime action, not an optical measurement. This entry records supplied
  evidence and grants no further runtime approval. C13A completes the narrow
  display-name observation listed as pending at the C11B checkpoint; the
  historical C11B record is preserved.
