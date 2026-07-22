# R583 v5 exactly-four execution-QA architecture review

**Date:** 2026-07-22  
**Review mode:** hostile architecture gate  
**Scope:** exactly four timing/identity execution-QA pilots only  
**Explicit exclusions:** production, figure population, manuscript population, production export, modification of any original `.mph`

## Binary ruling

**DO NOT SIGN a new exactly-four pilot authorization now.**

P1b/P2/P3/P4/P5E establish that a flat one-class Java entry can enter `main`, that the framed stdout route works at the tested sizes, that the current method-security behavior is classified, and that the COMSOL API/runtime family attestation is 6.3 with external build 6.3.0.290. They do **not** establish that the locked solution-free model can be loaded through `ModelUtil.loadCopy` without solver execution, hidden solution reuse, unexpected filesystem effects, or tag/solution-identity drift.

The next permitted authorization is therefore **one P6 no-solve model-load authorization**, not an exactly-four authorization. The four-pilot authorization may be created only after P6 passes and the clean-room v5 artifacts and release ledger below are frozen.

The existing `pilot_authorization_launcher_v4_finite_only_release2` is permanently non-signable. It binds a v3 runner, obsolete switch and `permit/v2`, while the v4 Java source expects a different switch and `permit/v3`. It must not be patched, wrapped, or used as an exporter.

---

# A. Exact preconditions still missing

A new exactly-four authorization is blocked until all of the following exist and their SHA-256 values are incorporated into one release lock:

1. **Frozen P0–P5E certificate bundle** with one canonical bundle hash. “Currently freezing” is not a frozen identity.
2. **Passing P6 no-solve model-load certificate** using the same staging, claim, status parser, frame parser and archive machinery intended for v5.
3. **Clean-room v5 Java source**, generated without copying the v4 class shell, imports, CLI parser, permit reader, filesystem helpers, reflection helpers, exporter or status logic.
4. **Fresh exactly-one-class compile** with no inner, anonymous, lambda, record or helper class output.
5. **Source and bytecode allowlist audit** showing zero direct Java filesystem I/O, zero reflection, zero network, zero subprocess, zero preference mutation and zero save/export API.
6. **v4-to-v5 scientific-algorithm transplant ledger** identifying only the case configuration, segmented solve, event selection, restart and native-solnum logic that was carried forward.
7. **Frozen v5 external launcher and validators**, including exact status parser, framed stdout parser, claim writer, directory-diff checker and archive builder.
8. **Frozen four-case manifest**, exact order, exact case-configuration digests, maximum five segments and all publication eligibility flags false.
9. **Verified model staging/locking procedure** for the sanitized solution-free model with SHA-256 `23E8F2D3D1B98B84F0221CE838C81C50C7B754474F0909D92B1374DD5F2A339B`.
10. **`R583_V5_RELEASE_LOCK.json`**, binding all certificates, sources, binaries, parsers, case manifests, model identity and exact command vector.

Until these ten objects exist, there is no signable execution identity.

---

# B. Minimal clean-room v5 architecture

## B1. Components

Only two active components are permitted:

1. `R583FourPilotRunnerV5.java` / one compiled `R583FourPilotRunnerV5.class`
2. `r583_four_pilot_launcher_v5.py`

Supporting Python modules may exist only if their hashes are individually bound by the release lock. Java may not load resources, helper classes, JARs or configuration files.

## B2. Exact Java argv

The runner accepts exactly two bare arguments:

```text
args[0] = R583_EXECUTE_AUTHORIZED_FOUR_PILOTS_V5
args[1] = permit/v5/<authorization_uuid>/<intent_sha256>/<nonce_hex>
```

The complete expected values of both arguments are compiled into the ephemeral class. Java performs exact string equality; it does not read or parse a permit file. No third argument is accepted. No parameter may begin with `--`.

The old UUID

```text
f6936bf2-6e99-4125-89a3-f5b2cff8c029
```

is included in the launcher’s permanent denylist and must not appear in the v5 source, compiled constant pool, command vector or new authorization except as a denylist entry.

## B3. Exactly-four compiled execution order

The four calls must be explicit in source, not discovered from a directory, payload, CSV, model tree or parameter sweep:

```text
runPilot(0, "J040_FD100__DA0__RA_COLLAPSED__FS_COLLAPSED")
runPilot(1, "J040_FD100__DA1__RAA__FS2")
runPilot(2, "J040_FD100__DA100__RAA__FS2")
runPilot(3, "J020_FD050__DA1__RAA__FS2")
```

The launcher independently verifies the same ordered tuple. Each pilot has a compiled case-configuration SHA-256. There is no runtime case list.

Each pilot is limited by a literal bounded loop:

```text
for segmentIndex = 0..4
```

No `while` loop may control segmentation. No pilot may execute a sixth segment. Across the run, `segments_total <= 20`.

## B4. Per-pilot model isolation

The solution-free staging model is loaded separately for every pilot:

```text
loadCopy -> identity/empty-solution gates -> configure one case -> run at most 5 segments
-> collect execution-QA scalars -> remove model
```

The runner must not reuse a solved model between cases. Fresh `loadCopy` per pilot prevents solution, event, restart, parameter and factorization state from leaking from one case into the next.

The only runner-initiated filesystem operation is the COMSOL API call `ModelUtil.loadCopy` against the compiled staging path. “Java zero file I/O” means zero use of Java standard-library file APIs and zero COMSOL save/export APIs; it does not pretend that loading an MPH through COMSOL performs no internal read.

## B5. Fixed six-record stdout stream

After argv and runtime-version gates succeed, the runner starts one stream and emits exactly six records:

```text
seq 0  RUN_META
seq 1  PILOT_RESULT  case 1
seq 2  PILOT_RESULT  case 2
seq 3  PILOT_RESULT  case 3
seq 4  PILOT_RESULT  case 4
seq 5  RUN_SUMMARY
```

If a pilot fails, its slot is emitted as `FAIL`; later slots are emitted as `NOT_RUN`. `RUN_SUMMARY` is emitted with overall failure, stdout is flushed, and the runner throws a fixed exception so COMSOL status must be `Error`. Once `RUN_META` has been emitted, the runner must attempt to close all six record slots. A VM crash or pipe failure produces a truncated stream and is rejected externally.

Failure before stream start—argv mismatch, permit mismatch or runtime version mismatch—must not create a valid stream.

### Framing

```text
@@R583V5|STREAM|BEGIN|v=1|auth=<uuid>|intent=<64hex>|records=6@@\n
@@R583V5|REC|BEGIN|seq=<n>|kind=<kind>|id=<id>|len=<decimal>|sha256=<64hex>@@\n
<payload bytes>
\n@@R583V5|REC|END|seq=<n>@@\n
...
@@R583V5|STREAM|END|records=6|payload_bytes=<decimal>|chain_sha256=<64hex>@@\n
```

Payloads are canonical UTF-8 JSON:

```text
sorted keys
no insignificant whitespace
no NaN or Infinity
no locale-dependent decimal formatting
```

Per-record digest:

```text
SHA256(
  ASCII(seq) + NUL + ASCII(kind) + NUL + UTF8(id) + NUL +
  ASCII(payload_length) + NUL + payload_bytes
)
```

The chain digest is SHA-256 over the six binary record digests in sequence order.

### Hard size limits

```text
RUN_META payload              <= 16,384 bytes
one PILOT_RESULT payload      <= 24,576 bytes
RUN_SUMMARY payload           <= 16,384 bytes
aggregate payload             <= 131,072 bytes
prefix noise                  <= 8,192 bytes
suffix noise                  <= 8,192 bytes
entire raw stdout             <= 196,608 bytes
one frame header line         <= 1,024 bytes
```

The launcher drains stdout and stderr concurrently and terminates the process if raw stdout exceeds 196,608 bytes. No production field arrays, meshes, coordinate tables or figure data are allowed in these records.

### Noise and corruption rules

- Bytes before stream begin and after stream end are archived as bounded noise.
- Any unframed byte between stream begin and stream end is fatal.
- Duplicate stream begin/end, duplicate sequence, duplicate case ID, unknown record kind, length mismatch, hash mismatch, chain mismatch, missing record, extra record, truncation or sentinel-like text in prefix/suffix noise is fatal.
- `status=Error` remains failure even when the diagnostic stream is structurally complete.

## B6. Minimal RUN_META fields

```json
{
  "schema": "R583_RUN_META_V5",
  "authorization_uuid": "...",
  "intent_sha256": "...",
  "action": "R583_EXECUTE_AUTHORIZED_FOUR_PILOTS_V5",
  "permit_version": "permit/v5",
  "probe_bundle_sha256": "...",
  "static_audit_sha256": "...",
  "runtime_comsol_version": "...",
  "external_build_attestation_sha256": "...",
  "model_sha256": "23E8F2D3D1B98B84F0221CE838C81C50C7B754474F0909D92B1374DD5F2A339B",
  "model_load_mode": "loadCopy_per_pilot",
  "case_set_sha256": "...",
  "case_ids": ["case0", "case1", "case2", "case3"],
  "max_segments_per_pilot": 5,
  "namespace": "R583_EXECUTION_QA_ONLY",
  "production_authorized": false,
  "figure_authorized": false,
  "manuscript_authorized": false
}
```

The Java record does not claim to know its own final class SHA. The external authorization envelope binds the actual class SHA; Java echoes the frozen static-audit identity instead.

## B7. Minimal PILOT_RESULT fields

```json
{
  "schema": "R583_PILOT_RESULT_V5",
  "authorization_uuid": "...",
  "ordinal": 0,
  "case_id": "...",
  "case_config_sha256": "...",
  "parameter_readback_sha256": "...",
  "status": "PASS|FAIL|NOT_RUN",
  "model_loaded": true,
  "model_saved_version": "...",
  "model_tag": "R583P0",
  "expected_study_tag": "...",
  "expected_solver_tag": "...",
  "solution_empty_before": true,
  "solution_initialized_before": false,
  "segments_executed": 1,
  "restart_count": 0,
  "run_call_count": 1,
  "segments": [
    {
      "index": 0,
      "requested_end_Q": 0.0,
      "observed_end_Q": 0.0,
      "native_solnum_first": 1,
      "native_solnum_last": 1,
      "native_solnum_count": 1,
      "termination": "EVENT|TARGET|SOLVER_END"
    }
  ],
  "event_reached": false,
  "event_Q": null,
  "native_solnum_monotone": true,
  "all_reported_scalars_finite": true,
  "solver_has_problems": false,
  "model_removed": true,
  "production_field_count": 0,
  "error_code": null
}
```

Only execution/timing/identity scalars are permitted. The exact event and native-solnum scalar names may follow the frozen v4 scientific algorithm, but no state field or production export is added.

## B8. Minimal RUN_SUMMARY fields

```json
{
  "schema": "R583_RUN_SUMMARY_V5",
  "authorization_uuid": "...",
  "intent_sha256": "...",
  "record_count": 6,
  "pilot_order": ["case0", "case1", "case2", "case3"],
  "pilots_passed": 4,
  "pilots_failed": 0,
  "pilots_not_run": 0,
  "model_load_count": 4,
  "model_remove_count": 4,
  "segments_total": 0,
  "max_segments_observed": 0,
  "run_call_count_total": 0,
  "production_field_count": 0,
  "namespace": "R583_EXECUTION_QA_ONLY",
  "production_eligible": false,
  "figure_eligible": false,
  "manuscript_eligible": false,
  "overall": "PASS_EXECUTION_QA_ONLY|FAIL_EXECUTION_QA"
}
```

The external archive, not a self-report, proves zero direct file I/O/reflection/save/export through the bound static audit.

---

# C. Safe migration of v4 scientific algorithms

## C1. What may be transplanted

Only these semantic blocks may be copied manually from v4:

1. exact case-to-parameter assignment;
2. finite-only scalar checks;
3. at-most-five-segment solve control;
4. event detection and tie-breaking;
5. restart-source selection;
6. native-solnum selection and ordering checks;
7. execution-QA scalar collection.

No complete v4 method, class shell or import block is accepted by default. Every transplanted fragment is recorded in `R583_V4_TO_V5_ALGORITHM_MAP.csv` with:

```text
v4 source SHA-256
v4 line range
semantic role
v5 line range
normalized fragment SHA-256
review disposition
```

The v5 source must contain none of the old switches, `permit/v2`, `permit/v3`, v3/v4 launcher constants, old UUID handling, file writers, exporters or reflective model access.

## C2. Java source allowlist

The source may use only:

- direct COMSOL API types required by the frozen algorithm;
- `ModelUtil.getComsolVersion`, `ModelUtil.loadCopy`, `ModelUtil.tags`, `ModelUtil.remove`;
- the exact expected model/study/solver/event/parameter methods listed in `R583_V5_COMSOL_METHOD_ALLOWLIST.json`;
- `java.lang` primitives and `StringBuilder`;
- `java.nio.charset.StandardCharsets`;
- `java.security.MessageDigest` for frame digests;
- narrowly enumerated `java.util` classes required for fixed arrays or formatting;
- `System.out` and `System.out.flush` only.

Use `Locale.ROOT` or locale-independent numeric formatting. Do not emit wall-clock time, random UUIDs, environment values or filesystem paths other than the compiled staging-model identity.

## C3. Source denylist

Reject source containing any of the following:

```text
java.nio.file
java.io.File
FileInputStream
FileOutputStream
RandomAccessFile
PrintWriter
java.net
java.lang.reflect
Class.forName
Method.invoke
Field.set
ClassLoader
URLClassLoader
ServiceLoader
ProcessBuilder
Runtime.exec
System.load
System.loadLibrary
System.getenv
System.getProperty
System.setProperty
ModelUtil.setPreference
ModelUtil.savePreferences
ModelUtil.loadPreferences
ModelUtil.showProgress(String)
Model.save
ModelUtil.load
ModelUtil.loadOnServer
ModelUtil.loadRecovery
result().export
export().run
batch().run
```

Any extra COMSOL method not in the explicit method allowlist is a build failure. The only permitted solve invocation is the exact owner/method/tag combination required by the frozen v4 scientific algorithm.

## C4. Bytecode gates

Fresh compilation must produce exactly one `.class`. Reject:

- `$` class files;
- `InnerClasses`, anonymous or local classes;
- lambda-generated classes;
- `invokedynamic`;
- native methods;
- resource access;
- forbidden package names in the constant pool;
- calls not listed in the bytecode method allowlist;
- any old switch, permit version or archived UUID in the constant pool other than the launcher denylist artifact.

The runner should use explicit `StringBuilder` operations so no compiler-generated `StringConcatFactory` invocation is needed.

The source/bytecode audit must also prove:

```text
four explicit runPilot calls
literal maximum segment count = 5
no dynamic case discovery
no save/export call
no direct file call
no reflection
no production namespace
```

---

# D. External launcher state machine and threat model

## D1. Authorization identity

The root authorization binds:

```text
authorization UUID
scope = R583_EXACTLY_FOUR_EXECUTION_QA_ONLY
ordered four case IDs and case-set SHA-256
max_segments_per_pilot = 5
production/figure/manuscript authorization = false
sanitized source-model SHA-256
per-run staging-copy SHA-256
runner source SHA-256
runner class SHA-256
launcher/validator/parser SHA-256 values
P0–P6 certificate-bundle SHA-256
static source/bytecode audit SHA-256
exact command-vector SHA-256
release-lock SHA-256
expiry and root signature identity
```

The permit argument is not a secret capability. It is an execution binding against accidental mismatch and controlled-launcher replay.

## D2. Exact state machine

```text
S0 ROOT_AUTHORIZATION_PRESENT
  -> verify signature, scope, expiry, denylist and all bound hashes
S1 VALIDATED_UNCLAIMED
  -> prepare isolated run directory
  -> copy only the sanitized solution-free model to a per-run staging path
  -> verify source SHA and staging SHA
S2 STAGED_UNCLAIMED
  -> atomically CREATE_NEW claims/<uuid>.claim.json
S3 CLAIMED_CONSUMED
  -> authorization can never be reused, even after later failure
  -> reverify every bound hash
  -> acquire read-only/no-share-write/no-share-delete handles where P6 proved compatible
S4 PRELAUNCH_LOCKED
  -> construct command as an argv array, never a shell string
  -> exact two Java args; no study/job/parameter-sweep/output-model CLI options
S5 COMSOLBATCH_RUNNING
  -> concurrently drain stdout and stderr
  -> enforce stdout hard cap
S6 PROCESS_EXITED
  -> close readers; preserve raw streams and return code
S7 STATUS_PARSED
  -> parse exact status grammar first
  -> Error: recovery may be absent; run is failure
  -> Done: require return code 0 and zero-byte recovery
S8 FRAME_VALIDATED
  -> require exact six-record stream and all field/order/hash constraints
S9 MODEL_INTEGRITY_VALIDATED
  -> hash staging model through held read handle before release
  -> rehash sanitized source model
  -> reject any new/changed MPH or unapproved file-tree delta
S10 ARCHIVED_PASS
```

Every failed transition enters one immutable failure state. Claims are never deleted or rolled back.

## D3. Exact status/recovery order

1. Wait for process exit.
2. Read raw status file.
3. Parse the complete status grammar; never search for substring `Done`.
4. If exact terminal state is `Error`, fail immediately. Recovery may be missing.
5. Only for exact `Done`, require OS return code 0 and an existing zero-byte recovery file.
6. Only then validate stdout frames.
7. Only then validate model hashes and directory deltas.

A complete diagnostic frame never overrides status `Error`.

## D4. Model immutability

- The original MPH path is absent from Java source, argv, environment and command construction.
- Python reads only the SHA-locked sanitized solution-free source and creates a per-run staging copy.
- The sanitized source and staging copy must both hash to `23E8F2D3D1B98B84F0221CE838C81C50C7B754474F0909D92B1374DD5F2A339B` before claim.
- Java uses `ModelUtil.loadCopy`, never `ModelUtil.load`.
- The batch command uses no output-model path and applies the previously verified no-save mode.
- Save, export, Model Manager write and preference APIs are absent from source and bytecode.
- Staging and sanitized-source hashes are checked again after process exit.
- Any newly created `.mph`, changed source/staging bytes, unexpected reparse point, or write/delete sharing requirement is fatal.

`loadCopy` is a useful API boundary, not sufficient proof by itself. The pre/post hash and static API exclusion are the actual immutability evidence.

## D5. Failure archive order

For any failure after claim, archive in this order:

1. root authorization and release lock;
2. immutable claim;
3. prelaunch validation and prehash ledger;
4. exact command vector and executable/class hashes;
5. raw stdout and stderr;
6. process return code;
7. raw status and exact parser result;
8. recovery presence, byte count and hash when present;
9. batch log and its hash;
10. frame parser result and partial-record diagnostics;
11. source/staging posthash and directory-tree delta;
12. terminal failure code;
13. canonical archive manifest and archive-root SHA-256.

For a failure before process spawn, missing process artifacts are recorded explicitly as `not_created`; the claim remains consumed.

## D6. Honest threat model

This design protects against accidental or workflow-level errors:

- stale or mismatched permit;
- wrong runner, launcher, parser, model copy or case set;
- regular-launcher replay;
- claim rollback after crash;
- model replacement during a controlled run;
- status substring errors;
- stdout truncation, duplication or injection;
- case-count, segment-count and namespace drift;
- accidental save/export or original-model use.

It does **not** protect against a malicious local administrator or a hostile user with sufficient local read/execute/debug privileges. Such an actor can read the class and command line, invoke COMSOL outside the launcher, alter process memory or replace trusted binaries. The `permit/v5` token must not be described as secret or as cryptographic protection against a hostile local principal.

---

# E. Mandatory P6 before exactly-four

## Decision

**Add P6. Do not enter exactly-four directly.**

Combining the first real model load with the first segmented solver/event/restart execution would make a failure uninterpretable and would consume the only exactly-four authorization before the model-load boundary had been established.

## P6 authorization scope

```text
R583_P6_LOAD_COPY_NO_SOLVE_V1
```

P6 is a separate one-shot authorization. It is not one of the four pilots and cannot run a study, solver, geometry, mesh, batch job, export or save.

## P6 Java operations

The P6 class uses the same clean-room, one-class, stream-only discipline and performs only:

1. exact argv and permit match;
2. `ModelUtil.getComsolVersion()` gate;
3. record initial `ModelUtil.tags()`;
4. `ModelUtil.loadCopy(P6_TAG, STAGING_PATH)`;
5. read `model.getComsolVersion()`;
6. record exact study and solver tag arrays expected by the frozen model identity;
7. for every expected solver sequence, record `isEmpty()` and `isInitialized()`;
8. optionally record `model.getFilePath()` as an observation, never as an immutability proof;
9. `ModelUtil.remove(P6_TAG)` in `finally`;
10. verify final `ModelUtil.tags()` returns to the initial set;
11. emit framed summary and return.

## P6 prohibited calls

```text
study.run
solver.run
runAll
continueRun
runFrom
runFromTo
createSolution
mesh.run
geometry.run
clearSolutionData
parameter mutation
save
export
batch job
```

## P6 PASS conditions

- exact status `Done`;
- return code 0;
- recovery exists and is zero bytes;
- valid complete P6 frame stream;
- runtime/API family remains 6.3 and external build attestation remains 6.3.0.290;
- one and only one `loadCopy` and one remove;
- expected model/study/solver tags match;
- every expected solver sequence reports `isEmpty() == true` before any pilot exists;
- no study or solver invocation;
- staging and sanitized-source SHA values are unchanged;
- no new `.mph` and no unapproved directory delta;
- model tag set returns to its initial value;
- no Java direct file I/O, reflection, save or export in source/bytecode.

`isInitialized()` is recorded separately and its observed value is frozen; it is not silently treated as equivalent to solution data. COMSOL documents `SolverSequence.isEmpty()` and `isInitialized()` as distinct states.

After P6 passes, its certificate is added to the P0–P6 certificate bundle and a new bundle hash is generated. Only then may root review a four-pilot authorization.

---

# F. P0-ranked COMSOL/API/event/restart distortion risks

## P0-1 — Unproven `loadCopy` boundary

P5E proves API entry, not model loading. Method security, staging-path access, model tag creation, solution-free state and remove behavior remain unproven. P6 closes this gap.

## P0-2 — Cross-pilot state contamination

Reusing one solved model can carry solution vectors, event states, parameter values, solver initialization or numerical factorization into later cases. Mandatory fix: fresh `loadCopy` and remove for each pilot.

## P0-3 — Native-solnum selection after an event or restart

COMSOL can retain multiple solution numbers around events, restarts and segmented runs. A default dataset or `solnum=auto` can select a different point from the native solver sequence. Mandatory fix: preserve the reviewed v4 native-solnum algorithm, query the solver sequence directly, emit per-segment first/last/count and reject nonmonotone or duplicate selection.

## P0-4 — Pre-event versus post-event duplicate coordinates

An event can create solutions at the same or nearly the same capacity/time on opposite sides of a state update. A nearest-value rule without a frozen side/tie-break convention can move the reported event. The v5 transplant must preserve the exact v4 side-selection and equality tolerance; no new interpolation is allowed.

## P0-5 — Study execution can regenerate or reattach solver sequences

A study run may alter solver attachment or regenerate a sequence depending on model state. The runner must freeze expected study/solver tags, verify them before and after every run call and allow only the exact run owner/method used by the reviewed algorithm.

## P0-6 — Restart source drift

A segmented continuation can restart from the wrong solution number, from the default solution, or from an already event-updated state. Every segment record must identify the restart source solnum and the resulting native solnum range. No implicit default restart is accepted.

## P0-7 — `isEmpty()` and `isInitialized()` are not synonyms

A solution sequence can be initialized without containing solved solution data. P6 and every per-pilot pre-run gate must record both. The release lock freezes the acceptable P6 observation rather than assuming both are false.

## P0-8 — Parameter units and locale

String parameters can be corrupted by unit omission, decimal locale or stale value retention. Use fixed unit-bearing expressions, locale-independent formatting, read back every changed parameter and bind the canonical readback into `parameter_readback_sha256` before the first run call.

## P0-9 — Solver completion is not scientific PASS

COMSOL status `Done` only classifies process completion. A pilot passes only if the solver problem flag is false, all required values are finite, event/native-solnum logic passes, segment count is within 1–5, the model is removed and all six records validate.

## P0-10 — Recovery/status/frame ordering

Recovery may be absent on `Error`; a zero-byte recovery is required only after exact `Done`. Frames are validated only after status acceptance. Reversing this order can convert a failed COMSOL execution into a false pilot PASS.

---

# Release lock required before any four-pilot signature

The implementation agent must generate:

```text
R583_V5_RELEASE_LOCK.json
R583_P0_P6_CERTIFICATE_BUNDLE.json
R583_V4_TO_V5_ALGORITHM_MAP.csv
R583_V5_COMSOL_METHOD_ALLOWLIST.json
R583_V5_SOURCE_BYTECODE_AUDIT.json
R583_V5_CASE_MANIFEST.json
R583_V5_STATUS_PARSER_TESTS.json
R583_V5_FRAME_PARSER_TESTS.json
```

The release lock is canonical JSON and includes SHA-256 values for every object above, the v5 Java source/class, all Python code, the sanitized model, the P6 certificate, the exact executable build attestation and the exact command vector template.

No production exporter, production field schema, figure projector or TeX token generator is part of this authorization. The external projector must continue to reject `R583_EXECUTION_QA_ONLY` artifacts categorically.

---

# Final binary verdict

**Exactly-four authorization: NOT ALLOWED.**

**Only one new authorization is allowed next: a one-shot `R583_P6_LOAD_COPY_NO_SOLVE_V1` authorization.**

After P6 passes and all v5 identities are frozen into the release lock, a separate root decision may authorize exactly the four listed execution-QA pilots. Production, figure and manuscript authorization remain false.