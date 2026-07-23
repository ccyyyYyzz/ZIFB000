# R583 V13R6 phase-off architecture emergency red-team

**Date:** 2026-07-23  
**Review mode:** hostile production-architecture gate  
**Scope:** phase-off event backbone, pre-onset replay, branch restart and regression prevention only  
**Explicit exclusions:** no production authorization, no COMSOL execution, no manuscript/model/runner/figure mutation, no physical experiment

## Binding verdict

# **ACCEPT the proposed V13R6 correction.**

It is the only correction described here that restores the frozen campaign topology. V13R5 is architecturally invalid because it instantiates the finite/accessibility graph before the first-local event. The fact that the phase source is numerically zero while `S<1` is not an acceptable substitute for graph absence. An active conditional graph can still alter residual assembly, Jacobian evaluation, scaling, consistent initialization, Newton damping and accepted-step history; the observed pre-current approach to `S=1`, step collapse and the earlier fractional-power failure are direct warnings that this distinction is operational, not semantic.

Acceptance applies to the **architecture only**. Production remains **NO-GO** until every P0 gate below passes and a successor worker/static/mutation/governance package is frozen.

---

# 1. Does `productionSpec(..., true)` restore the frozen graph?

## Verdict: yes, but only if `true` selects the canonical static phase-off builder

For every own-event backbone and every pre-onset physical replay, `productionSpec(segment, true)` must produce the same active model graph as the frozen phase-off policy and the released pilot:

```text
phase_route = 0
Da_phi      = 0
RA_route    = 0
q_phi       = identically zero
R_A         = identically one
A_v         = a_v0
finite phase-conversion graph absent
Scenario-A/Scenario-B accessibility graph absent
```

This must be a **structural graph selection**, not a late parameter override applied to an already instantiated active graph. The worker must construct the phase-off spec from the canonical backbone template and copy only the outer-node quantities that genuinely define the event trajectory, such as current, `f_D`, `f_sat`, geometry and other frozen physical inputs.

The correction is rejected at runtime if `productionSpec(..., true)` merely sets `phase_route`, `Da_phi` and `RA_route` values while leaving active residual/Jacobian dependencies on `g_delta`, `delta_eps`, `RA_A`, `RA_B`, `kappa`, finite `q_phi`, or branch-only state variables.

V13R5 demonstrates why value-level dormancy is insufficient. `q_phi=0` below onset did not prevent the active graph from entering a numerically invalid domain. The frozen requirement is **branch graph absent before event**, not merely **branch output currently zero**.

---

# 2. Logical branch identity versus runtime backbone identity

## Verdict: no scientific conflict, but the metadata vocabulary must be corrected

A runtime readback of

```text
Da_phi = 0
phase_route = 0
RA_route = 0
```

is fully consistent with a logical post-event branch whose registered configuration is

```text
Da_phi = 1
RA_route = Scenario A
```

because the event is deliberately generated on a common phase-off backbone. The event is not a `Da_phi=1` or Scenario-A event. It is the first-local `max ln(S)=0` event for the branch's **outer physical node**, before the finite/accessibility graphs are instantiated.

The proposed metadata must therefore avoid the misleading field name `event_source_Da_phi=1`. Use two explicit namespaces:

```text
logical_post_event_Da_phi
logical_post_event_RA_route
logical_post_event_phase_route

runtime_backbone_Da_phi       = 0
runtime_backbone_RA_route     = 0
runtime_backbone_phase_route  = 0
runtime_backbone_graph_id     = R583_PHASE_OFF_BACKBONE_V2
```

Also record:

```text
event_source_kind = COMMON_PHASE_OFF_BACKBONE
logical_case_id
outer_node_id
current
f_D
f_sat
post_event_branch_spec_sha256
```

Calling the event state a "Scenario-A event source" would be scientifically false. Scenario A begins only in the continuation instantiated from that state.

---

# 3. Must pre-onset `PHYSICAL_NATIVE_REPLAY` also be phase-off?

## Verdict: yes, without exception

Every replay whose requested state lies at or before the native event-after state must use:

```text
productionSpec(segment, true)
```

A pre-onset replay under `phase_route=1` would reconstruct the state with a different residual/Jacobian graph from the one that generated the archived native backbone. Even if the replay converged to numerically similar field values, it would not be the same state provenance and could reactivate the same fractional-power/Newton-path defect found in V13R4/R5.

Required split:

```text
pre-onset and event-state replay:
    canonical phase-off graph

post-event branch execution/replay:
    exact registered finite/accessibility graph
    initialized only from that branch's own native event-after raw U
```

No replay may infer graph choice from a numerical test such as `S<1`, `eps_s=0`, or `q_phi=0`. Graph choice is static and role-based.

---

# 4. Post-event branch restart

The proposed restart rule is accepted:

1. generate the event on the canonical phase-off backbone;
2. retain the exact adjacent native `stepbefore` and `stepafter` pair;
3. require event-after to be the terminal native state of the event-backbone unit;
4. instantiate the registered finite/accessibility branch only after that state;
5. initialize the continuation from its own event-after raw `U`;
6. use no interpolation, projection, nearest-state substitution, smoothing, clamping or algebraic repair.

The continuation ledger must distinguish:

```text
seed_raw_U_sha256
first_shared_raw_U_sha256
seed_bitwise_equal
post_event_branch_spec_sha256
post_event_parameter_readback_sha256
post_event_active_graph_sha256
```

If COMSOL performs a consistent-initialization operation after the graph switch, record its output separately. It must not overwrite or relabel the archived event-after seed. The paper campaign must be able to distinguish:

```text
phase-off event-after state
post-switch consistent-initialization state
first accepted post-event native state
```

Collapsing those three identities into one record is a P0 provenance failure.

---

# 5. V17 and V24 own-event units under the common off graph

## Verdict: keep them

The own-event requirement still makes sense, but its justification is now provenance and anti-regression, not a claim that `delta_eps` or the accessibility route changes pre-onset physics.

For V17 and V24:

- each own-event unit begins with a fresh solution-free `loadCopy`;
- each constructs the exact canonical phase-off graph;
- each preserves its own execution-unit, case and outer-node identity;
- each extracts its own native first-local event;
- each continuation consumes only its own event-after raw-`U` identity;
- borrowed PU11/base hashes remain forbidden;
- the logical numerical variant is activated only after the event state.

Required metadata:

```text
logical_numerical_variant_id = 17 | 24
event_backbone_variant_dependency = NONE
event_source_kind = COMMON_PHASE_OFF_BACKBONE
own_event_execution_unit_id
borrowed_event_state = false
logical_post_event_delta_eps = 1e-9
logical_post_event_RA_route = A | FIXED_ONE
```

The event-backbone output must never be described as evidence that `delta_eps=1e-9` or the fixed-area route changes onset. Those quantities are absent from the active pre-onset graph.

Because V17, V24 and their corresponding base outer node use the same active phase-off graph, current, `f_D` and `f_sat`, any event-state discrepancy is a numerical/provenance diagnostic rather than physical sensitivity. Exact graph hashes and event brackets must agree. Bitwise raw-`U` equality should be required if deterministic execution has already been frozen; otherwise any non-bitwise discrepancy requires a documented deterministic-repeatability disposition before production authorization.

---

# 6. Startup output microgrid

## Verdict: retain it unchanged

Keep the exact startup output requests:

```text
0
0.05
0.10
0.15
0.20
0.25 s
```

The coarse `0 -> 0.25 s` request independently exposed a Newton-domain overshoot. Removing the microgrid at the same time as restoring the phase-off graph would change two numerical controls in one emergency repair and would destroy causal attribution.

The microgrid is permitted only as a frozen numerical startup protocol:

- no smoothing;
- no clamping;
- no altered physical equation;
- no synthetic state inserted into event extraction;
- event detection still uses exact accepted native states;
- all event backbones and pre-onset replays use the same startup schedule;
- the applied-current ramp remains separately read back as beginning at `t=8 s`.

An event or near-event condition before the applied-current ramp is a P0 initial-state/graph failure unless a separately frozen campaign specification explicitly defines an initially supersaturated electrode. No such exception is part of the stated V13R6 policy.

---

# 7. Minimum machine-verifiable P0 assertions

Production must be refused if any assertion below fails.

## P0-1 — Static call-site gate

The source and bytecode audit must prove:

```text
all OWN_EVENT_BACKBONE call sites:
    productionSpec(backboneSegment, true)

all PHYSICAL_NATIVE_REPLAY states at or before event-after:
    productionSpec(segment, true)

all post-event finite/accessibility continuations:
    branch-specific productionSpec(..., false) or an exact registered active-spec builder
```

The boolean at backbone/replay call sites must be a literal constant in bytecode, not a CLI field, manifest value, environment setting or dynamically computed condition. Any reachable `false` path for pre-onset roles is fatal.

## P0-2 — Canonical graph-hash gate

For every own-event backbone and pre-onset replay:

```text
runtime_backbone_graph_sha256 == frozen_phase_off_graph_sha256
active_equation_feature_sha256 == frozen_phase_off_feature_sha256
active_dependency_graph_sha256 == frozen_phase_off_dependency_sha256
```

The active dependency graph must contain no path from:

```text
delta_eps
g_delta
RA_A
RA_B
kappa
finite q_phi
branch-only accessibility variables
```

to any pre-onset residual, Jacobian, mass matrix, initial condition, event expression, variable scaling or solver-dependent expression.

## P0-3 — Exact runtime readback gate

Every backbone/replay must emit and match:

```text
phase_route = 0
Da_phi = 0
RA_route = 0
q_phi expression/status = identically zero
R_A expression/status = identically one
A_v expression/status = a_v0
```

The exact current, `f_D`, `f_sat`, geometry and event-domain selection must still match the logical outer node.

## P0-4 — Event-definition gate

The only event is:

```text
first upward crossing of max_positive_electrode ln(S) = 0
```

Require:

- exact event-expression hash;
- exact positive-electrode selection hash;
- exactly one upward native pair;
- adjacent native `stepbefore` and `stepafter` identities;
- `max_lnS_stepbefore < 0`;
- `max_lnS_stepafter >= 0`;
- no earlier qualifying native state;
- event-after is the event-unit terminal native state;
- no average-saturation, accessibility or phase-activation event substituted.

## P0-5 — No pre-current event gate

Require:

```text
event_time >= applied_current_ramp_start_time
event_Q > 0
```

and exact readback:

```text
applied_current_ramp_start_time = 8 s
```

Any crossing or near-terminal step collapse before applied current is treated as an initial-state, graph-selection or solver-domain defect, not a valid physical event.

## P0-6 — Replay provenance gate

Every pre-onset replay record must bind:

```text
snapshot_role
source_backbone_unit_id
source_native_solnum
source_raw_U_sha256
runtime_backbone_graph_sha256
replay_initial_raw_U_sha256
no_interpolation = true
no_repair = true
```

A replay generated under any active branch graph is fatal.

## P0-7 — Branch-switch and seed gate

For every continuation:

```text
own_event_source_unit_id matches
seed_raw_U_sha256 matches own event-after
first_shared_raw_U_sha256 matches seed bitwise
logical post-event Da_phi readback matches registry
logical post-event RA_route readback matches registry
logical post-event phase_route readback matches registry
active post-event graph hash matches registry
```

No borrowed source, cross-route substitution or nearest state is permitted.

## P0-8 — V17/V24 own-event gate

Both numerical variants must have:

```text
fresh_loadCopy = true
runtime phase-off graph = canonical
own native event = present and unique
borrowed event hash = absent
post-event delta_eps = 1e-9
post-event route = exact logical route
```

Any attempt to classify their common event backbone as a `delta_eps` sensitivity result is evidence-class leakage.

## P0-9 — Startup protocol gate

Read back and hash:

```text
startup requested times = [0, 0.05, 0.10, 0.15, 0.20, 0.25] s
current ramp start = 8 s
startup smoothing = absent
clamping = absent
fractional-power repair = absent
```

The native accepted-step ledger must remain finite and must not show evaluation of an inactive branch expression. If `g_delta` or another finite/accessibility expression is evaluated before the event, the graph-absence gate has failed regardless of final values.

## P0-10 — State separation gate

Archive separate hashes/identities for:

```text
event stepbefore native state
event stepafter native state
post-switch consistent-initialization state, if any
first accepted post-event native state
```

No record may silently relabel one as another.

## P0-11 — Model immutability and mutation gate

Require:

- fresh `loadCopy` from the locked solution-free staging copy;
- original `.mph` path absent from worker inputs;
- source/staging pre/post SHA-256 unchanged;
- no save/export/model-manager write path;
- model-tree mutation diff limited to the frozen parameter/run allowlist;
- no unexpected model feature creation or deletion;
- model removed after each execution unit.

## P0-12 — Status, stream and archive gate

Require:

- exact terminal-status parsing;
- `Done` only with return code 0 and zero-byte recovery;
- framed stdout complete and hash-valid;
- unit/segment counts match the successor topology;
- batch log archived;
- all runtime graph/spec readbacks present;
- canonical failure archive on any rejection;
- claim remains consumed after failure.

## P0-13 — Governance supersession gate

V13R5 and any worker/static/release-lock artifact that permits active-route backbones or active-route pre-onset replay must be explicitly superseded by hash. No production authorization may bind to a mixed R5/R6 identity.

---

# 8. Red-team rejection conditions specific to the correction

Reject V13R6 immediately if any of the following is observed:

1. `productionSpec(..., true)` changes only parameter values but does not remove branch features from the active graph.
2. Metadata reports `event_source_Da_phi=1` without explicitly classifying it as a logical post-event branch value.
3. A pre-onset replay uses `false`, an active route, or a runtime condition to choose its graph.
4. V17 or V24 borrows a PU11/base event state.
5. A V17/V24 event difference is interpreted as regularization or accessibility physics.
6. The startup microgrid is removed, smoothed, or replaced while the route correction is being validated.
7. Any event occurs before the current ramp and is accepted as physical.
8. `g_delta` or the accessibility graph appears in a pre-onset residual/Jacobian dependency record.
9. The event-after seed is reconstructed rather than taken from the terminal native state.
10. The worker reports success because `q_phi=0` or `R_A=1` at converged points while the active graph remains present.

---

# Final release status

```text
V13R6 architecture correction: ACCEPTED
V13R5 active-route topology: REJECTED AND MUST BE SUPERSEDED
Production authorization: NO-GO
```

The correction restores the campaign's declared causal topology: a common static phase-off backbone generates the first-local event; finite phase conversion and accessibility are instantiated only from the native event state. It does not authorize production. Worker, static, graph-absence, mutation, restart, status/recovery, archive and governance gates must all pass under one frozen V13R6 identity before any production authorization can be created.
