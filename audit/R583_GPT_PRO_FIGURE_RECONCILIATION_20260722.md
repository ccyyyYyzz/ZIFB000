# R583 corrected figure-architecture reconciliation

**Date:** 2026-07-22  
**Review mode:** second-round editor-in-chief reconciliation  
**Scope:** narrative and figure architecture only  
**Hard exclusions:** no manuscript edit, no model edit, no runner edit, no figure build, no production value, no QA-pilot result

## Editorial decision

**Choose Architecture A, but only in the corrected form A\*.**

A\* is:

1. clean positive-electrode mechanism;
2. baseline scalar trajectories around the only declared event, the first-local upward crossing of \(\max_{\mathrm{positive\ electrode}}S=1\);
3. a three-column event-relative native-field matrix;
4. one reference-point phase-off/fixed-area/full matched-control figure;
5. the exact 4 × 7 current–\(f_D\) maps.

The independent DFT/MD/analytical-accessibility/pore-network comparator moves in full to SI. Cases 59–65 remain SI-only. The 22 numerical variants remain SI-only. The four execution-QA pilots remain absent from every manuscript object.

**Reject Architecture B.** Its spatial difference fields would add a new export and an exact cross-solve matching burden while giving the reader a more abstract second spatial figure. Without interpolation, native solution coordinates from the full and fixed-area solves may not align exactly. The same accessibility-feedback effect is already isolated by the matched scalar trajectories in Fig. 4 and by \(\max|\eta_{\mathrm{full}}-\eta_{\mathrm{fixed}}|\) in Fig. 5. B spends main-text space on a harder-to-read duplicate.

---

# 1. Explicit corrections to the previous hostile review

The following previous recommendations are withdrawn without qualification.

## Withdrawn 1 — electrode-average saturation event

There is no such declared event in R583. The only implemented physical event is:

> **first-local onset:** the first upward crossing of \(\max_{\mathrm{positive\ electrode}}S=1\), represented by the exact native `stepbefore` and `stepafter` states.

All main-text event language must use **first local supersaturation onset** or **first-local \(S=1\) crossing**. Do not write average saturation, mean saturation, averaged onset or electrode-average event.

## Withdrawn 2 — accessibility event and \(\Delta Q\) between two events

Scenario-A accessibility is a continuous relation \(R_A(\varepsilon_s)\). No 5% loss line, half-accessibility point or other accessibility threshold is declared as a physical event. Therefore:

- do not define \(Q_{\mathrm{accessibility}}\);
- do not define \(\Delta Q=Q_{\mathrm{accessibility}}-Q_{\mathrm{loc}}\);
- do not use a colour boundary, contour or caption that implies an accessibility threshold;
- do not convert a display choice into a mechanism coordinate.

Fixed post-onset states such as \(Q_{\mathrm{loc}}+0.5\) and \(Q_{\mathrm{loc}}+1\) are allowed because they are predeclared sampling roles, not new physical events.

## Withdrawn 3 — six-\(Da_\phi\) facets over the 64 physical rows

The active physical design is not a six-\(Da_\phi\) Cartesian campaign. The main physical map is the complete 4-current × 7-\(f_D\) outer grid at \(Da_\phi=1\) and \(f_{\mathrm{sat}}=2\), with Scenario-A full and \(R_A=1\) matched branches. The four additional finite-\(Da_\phi\) reference cases and three \(f_{\mathrm{sat}}\) reference cases are SI-only.

Accordingly:

- no six-facet main figure;
- no claim that 64 rows span six full \(Da_\phi\) planes;
- \(Da_\phi=100\) remains a finite-rate SI reference point, never a fast, infinite or algebraic limit;
- cases 59–65 do not enter a main panel by implication, inset or caption.

## Retained recommendations

The following earlier conclusions remain valid:

- the porous positive electrode is the only protagonist;
- Fig. 1 must not depict deposit morphology;
- event-relative 2D fields are the correct central visual device;
- Scenario A is the sole continuum accessibility relation;
- Scenario B is a retired non-continuum analytical upper bound in SI only;
- lower-scale calculations are independent bounds, not continuum validation;
- QA pilots must not enter the scientific evidence chain;
- governance, authorization and registry language must stay out of the paper.

---

# 2. Final five-figure order

| Figure | One claim | Main evidence | Reader action in 10 seconds |
|---|---|---|---|
| **Fig. 1 — Local iodine handling in the porous positive electrode** | Local free-I2 generation, removal, finite-rate retention and Scenario-A accessibility are separate model relations. | Clean domain/mechanism schematic only. | Locate the positive felt and identify the sequence source/removal → retained solid → remaining accessibility → reaction response. |
| **Fig. 2 — Baseline states around first-local onset** | The baseline scalar states do not collapse onto one trajectory at the first-local \(S=1\) crossing. | Baseline native scalar trajectories and exact `stepbefore`/`stepafter` event bracket. | See what changes before, at and after local onset without treating accessibility as a threshold. |
| **Fig. 3 — Event-relative spatial progression** | The location of free-I2 stress, retained solid and reduced Scenario-A accessibility changes across the exact pre-onset/onset/post-onset states. | Native \(\ln S\), \(\varepsilon_s\) and \(R_A\) fields. | Read left-to-right in charge state and top-to-bottom in physical sequence. |
| **Fig. 4 — Phase conversion and accessibility feedback are separable** | Turning phase conversion off and fixing \(R_A=1\) affect different parts of the scalar response. | One designated reference point: phase-off, Scenario-A full and matched fixed-area trajectories. | Distinguish finite phase conversion from accessibility feedback. |
| **Fig. 5 — Current and transport control onset and the one-unit post-onset response** | The complete 4 × 7 current–\(f_D\) plane separates onset timing from retained solid, remaining accessibility and the functional effect of accessibility feedback. | Four exact direct maps from the 28 outer nodes. | Compare the same physical grid in all four panels; no invented score or threshold. |

This sequence is stronger than both original options because it keeps the native-field figure as the main visual result, uses controls only after the reader understands the baseline state, and ends with the complete physical map rather than a lower-scale comparator.

---

# 3. Figure 1 contract

## Claim

> The porous positive electrode has a local free-I2 source–removal problem; finite-rate retained solid and Scenario-A accessibility are downstream states, not synonyms for supersaturation.

## Layout

Two panels, approximately 35:65 width.

### Panel a — domain

Flat orthographic strip only:

```text
current collector | porous positive carbon felt | separator
```

Show:

- through-plane coordinate \(x\);
- flow coordinate \(y\);
- one flow arrow;
- one current-direction arrow;
- the positive felt as the dominant visual object.

### Panel b — local model relation

Use one carbon-surface line and four compact visual states:

1. free-I2 generation at the reacting surface;
2. complexation and transport as outward removal routes;
3. finite-rate change in retained-solid state \(\varepsilon_s\) once \(S>1\);
4. Scenario-A remaining accessibility \(R_A(\varepsilon_s)\), followed by local reaction response.

This must read as a physical relation, not a workflow. Use direct labels beside the objects; do not use rounded process boxes.

## Must not appear

- NH4Br or bromide icon;
- DFT structure;
- Scenario B;
- site density, site population or microscopic coverage;
- crystals, films, shells, clumps, bridges or blocked pores;
- pressure or permeability;
- 64P/22N counts;
- route names, case numbers, solver nodes or authorization language.

## Caption boundary

Use one sentence only:

> The schematic represents continuum states and implemented model couplings, not a microscopic deposit morphology.

---

# 4. Figure 2 contract — baseline stacked trajectories

## Claim

> The baseline free-I2, retained-solid and accessibility responses evolve differently around the first-local onset.

## Layout

One full-width stack of four aligned strips sharing the areal-capacity axis:

1. \(\max_{\mathrm{positive\ electrode}}\ln S\);
2. the predeclared positive-electrode retained-solid scalar, preferably a COMSOL volume average or integral-derived mean rather than an unweighted node mean;
3. the predeclared positive-electrode Scenario-A \(R_A\) scalar;
4. the selected terminal response, \(\eta\), voltage or another already registered scalar.

Do not use multiple y-axes on one plotting area. Each strip has its own y-axis and the same x-limits.

## Event display

The event is a native-step bracket, not a fitted line:

```text
stepbefore: max S < 1
stepafter:  max S >= 1
```

Display two thin vertical markers joined by a small bracket labelled **first local onset**. If the two native capacities are visually indistinguishable at final size, show one shaded sliver whose edges are the exact `stepbefore` and `stepafter` capacities.

Do not plot an accessibility threshold. Do not annotate a 5% line. Do not call \(Q_{\mathrm{loc}}+1\) an accessibility event.

## Move to SI

- all additional \(Da_\phi\) and \(f_{\mathrm{sat}}\) reference-point trajectories;
- all 22 numerical variants;
- solver, restart and native-solution diagnostics;
- complete case inventory.

---

# 5. Figure 3 contract — exact 3 × 3 matrix

## Decision: three columns, not four

Use the three roles:

1. \(Q_{\mathrm{loc}}-2\);
2. \(Q_{\mathrm{loc}}\);
3. \(Q_{\mathrm{loc}}+1\).

Move \(Q_{\mathrm{loc}}+0.5\) to SI with identical row order and colour scales.

### Why three columns

- Three columns map directly to **before onset / onset / one unit after onset**.
- Four columns make the two post-onset states look equally fundamental even though +0.5 is a sampling role, not an event.
- Four columns shrink each field by roughly one quarter and make an 8 pt typography floor harder to maintain.
- The +0.5 state remains scientifically useful for finite-rate development and therefore belongs in the extended SI field plate.
- Fig. 4 already shows the continuous scalar trajectory; Fig. 3 does not need two intermediate post-onset snapshots.

Retain four columns only in SI.

## Exact matrix

| | Column 1 | Column 2 | Column 3 |
|---|---|---|---|
| **Heading line 1** | actual native \(Q\) | actual native \(Q\) | actual native \(Q\) |
| **Heading line 2** | \(Q_{\mathrm{loc}}-2\): before first-local onset | \(Q_{\mathrm{loc}}\): first-local crossing role | \(Q_{\mathrm{loc}}+1\): one unit after onset |
| **Row 1** | \(\ln S\) | \(\ln S\) | \(\ln S\) |
| **Row 2** | \(\varepsilon_s\) | \(\varepsilon_s\) | \(\varepsilon_s\) |
| **Row 3** | \(R_A\) | \(R_A\) | \(R_A\) |

The renderer must print the actual native capacity. A role name is not a substitute for the actual \(Q\).

The `Qloc` metadata must explicitly state whether the displayed native state is `stepbefore` or `stepafter`. Do not silently reinterpret an existing production role. If the current schema does not carry this field, add it before rendering.

## Row meanings

### Row 1 — local free-I2 stress

Label:

> Local supersaturation, \(\ln S\)

Use one shared diverging scale across all displayed columns, centred exactly at \(\ln S=0\). Use the symmetric range determined from the maximum absolute \(\ln S\) across all four registered baseline roles, including the SI-only +0.5 role, so the main and SI plates use the same scale.

Colour semantics:

- blue: \(\ln S<0\);
- neutral: \(\ln S=0\);
- amber: \(\ln S>0\).

Do not draw an interpolated zero contour. If a location marker is needed at the onset state, mark the exact native argmax node with one small open symbol and label it **first local crossing**.

### Row 2 — retained solid

Label:

> Retained-solid fraction, \(\varepsilon_s\)

Use one shared non-negative sequential scale, zero to the global maximum over all four registered baseline roles. Do not autoscale columns. Start with a linear scale. Do not switch to logarithmic or symlogarithmic scaling after inspecting which choice creates a more dramatic picture; any non-linear scale must be frozen in the figure contract before final rendering and used identically in main and SI.

### Row 3 — Scenario-A remaining accessibility

Label:

> Remaining accessibility, \(R_A\)

Use one shared linear scale from the global minimum over all four registered baseline roles to 1.0. The colourbar must show the actual minimum and 1.0. Use white or very pale neutral at \(R_A=1\) and progressively stronger teal as remaining accessibility decreases. This makes loss visible without inventing a threshold.

Do not plot Scenario B, geometric coverage, \(1-R_A\) threshold zones or any site-population bound in this row.

## Geometry and labels

- same domain and aspect in every cell;
- collector and separator labelled once above the matrix;
- flow direction labelled once;
- x/y tick labels only on the outer axes;
- one colourbar per row;
- no repeated legends;
- no in-panel paragraph;
- at most two direct annotations in the entire figure.

Permitted annotations:

- **first local crossing** at the exact native argmax node;
- **largest decrease in remaining accessibility** only if it is a direct statement of the displayed field, not a morphology inference.

Forbidden words in the figure and caption:

```text
film
coverage
front
blocked zone
shell
bridge
pore closure
crystal
morphology
```

The caption may state positively:

> These maps are continuum state fields on the positive-electrode domain.

One final boundary sentence may add:

> They do not resolve microscopic deposit structure.

## Ten-second reading order

1. left to right: pre-onset → first local onset → one unit post-onset;
2. top to bottom: free-I2 stress → retained solid → remaining accessibility;
3. colourbars: one scale per physical quantity, no panel-specific rescaling.

A reader should be able to say:

> Local supersaturation appears first; retained solid and the Scenario-A accessibility response develop afterwards and are spatially non-uniform.

The exact final wording must be based on authorized production fields, not the QA pilots.

---

# 6. Figure 4 contract — what stays and what moves to SI

## Main Figure 4 stays

Use one designated reference operating point and exactly three existing main-eligible calculations:

1. reference phase-off case;
2. Scenario-A full case;
3. matched \(R_A=1\) fixed-area control at the same outer node.

No cases 59–65 enter the main figure.

## One claim

> Finite phase conversion and accessibility feedback alter different parts of the positive-electrode response.

## Recommended 2 × 2 layout

### a — local supersaturation trajectory

Plot \(\max\ln S\) against actual areal capacity for phase-off, fixed-area and full cases. Mark each first-local onset with its native step bracket. This panel identifies what phase conversion changes upstream.

### b — retained-solid trajectory

Plot the registered positive-electrode retained-solid scalar. The phase-off case should remain visible as the zero reference rather than disappearing from the legend.

### c — Scenario-A accessibility trajectory

Plot the registered positive-electrode \(R_A\) scalar. Full Scenario A is the active relation. The fixed-area and phase-off references remain at \(R_A=1\) by construction and should be shown as a quiet reference line rather than two visually dominant duplicate curves.

### d — accessibility-feedback consequence

Plot the signed difference

\[
\eta_{\mathrm{full}}-\eta_{\mathrm{fixed}}
\]

for the predeclared \(\Delta Q=Q-Q_{\mathrm{loc,full}}\) interval 0–1. This \(\Delta Q\) is a coordinate offset from the only physical event, not a second event or threshold. State the alignment source explicitly: the full Scenario-A branch's \(Q_{\mathrm{loc}}\).

Do not add a fourth model relation, a Scenario-B curve or a finite-\(Da_\phi\) inset.

## Entire lower-scale comparator moves to SI

Move the completed DFT/MD/analytical-accessibility/pore-network figure to SI as one independent-bounds figure. Its caption must begin:

> Independent calculations bound prescribed inputs and analytical comparison ranges; they do not validate continuum state fields.

SI S7 must continue to label:

- Scenario A: **sole continuum accessibility relation**;
- Scenario B: **retired non-continuum analytical DFT-placement upper bound**.

No arrow should visually connect Scenario B into a continuum solve.

---

# 7. Figure 5 contract — strong conclusion without an accessibility threshold

## One claim

> The current–\(f_D\) plane separates the timing of first-local supersaturation from the retained-solid, accessibility and functional responses one capacity unit later.

This is a stronger and more defensible conclusion than an arbitrary threshold map. It compares four continuous, predeclared readouts on the same complete 4 × 7 physical grid.

## Exact 2 × 2 map layout

All panels use:

- x-axis: the seven exact \(f_D\) values;
- y-axis: the four exact applied currents;
- \(Da_\phi=1\) and \(f_{\mathrm{sat}}=2\), stated once above the figure;
- one cell per solved outer node;
- no interpolation, smoothing, contouring or fitted surface;
- one outline around the designated baseline cell.

### a — first-local onset capacity

\[
Q_{\mathrm{loc}}
\]

This is the exact native first-local crossing coordinate. Lower values mean earlier onset. Use a sequential scale reversed so earlier onset is visually stronger, but retain the actual \(Q_{\mathrm{loc}}\) units and values.

### b — retained solid one unit after onset

\[
\varepsilon_s(Q_{\mathrm{loc}}+1)
\]

Use the exact registered positive-electrode scalar. Higher values receive stronger colour.

### c — Scenario-A remaining accessibility one unit after onset

\[
R_A(Q_{\mathrm{loc}}+1)
\]

Use the continuous value. Lower remaining accessibility receives stronger colour. No 5% line, no thresholded affected area and no binary pass/fail cells.

### d — functional effect of accessibility feedback

\[
\max_{0\leq\Delta Q\leq1}
\left|\eta_{\mathrm{full}}-\eta_{\mathrm{fixed}}\right|
\]

This is a matched-control response metric, not an accessibility threshold. The source table must also retain the signed difference and the exact \(Q\) at which the maximum absolute value occurs.

## Why this figure has a strong conclusion

The strength comes from **common coordinates and causal ordering**, not from inventing a score:

1. panel a asks when local supersaturation first appears;
2. panel b asks how much solid is retained after a fixed post-onset interval;
3. panel c asks how much Scenario-A accessibility remains at the same interval;
4. panel d asks how strongly accessibility feedback changes the terminal response over that interval.

The final Results sentence should describe the actual pattern after production, for example in this grammatical form:

> Across the current–transport plane, [condition] advances first-local onset, whereas [condition] controls the one-unit post-onset retained-solid and accessibility response.

Do not prefill the bracketed physics before production.

## Missing or censored nodes

If any outer node does not reach \(Q_{\mathrm{loc}}\) or does not contain a complete \(Q_{\mathrm{loc}}+1\) state:

- show the cell as NA with a neutral hatch;
- state the exact reason in source data;
- do not impute, extrapolate or replace it with an endpoint value.

---

# 8. Production-schema additions that do not enlarge 64P/22N

These are metadata and deterministic exports from the existing production states. They add no physical case.

## Event identity

```text
event_definition_id = first_local_maxS_upcross_v1
Q_stepbefore
Q_stepafter
native_solnum_stepbefore
native_solnum_stepafter
max_lnS_stepbefore
max_lnS_stepafter
event_reached
```

The main manuscript may call the event \(Q_{\mathrm{loc}}\), but the source data must preserve the exact native bracket.

## Snapshot identity

For every field role:

```text
snapshot_role
snapshot_actual_Q
snapshot_deltaQ_from_Qloc
snapshot_native_solnum
snapshot_event_side = pre | stepbefore | stepafter | post
snapshot_time
```

The Qloc field cannot be rendered until `snapshot_event_side` is explicit.

## Field identity

```text
case_id
outer_node_id
branch_role = scenario_A_full | RA_fixed_control | phase_off_reference
J
f_D
Da_phi
f_sat
x
y
lnS
eps_s
R_A
grid_shape
grid_coordinate_sha256
field_units
field_min
field_max
argmax_lnS_x
argmax_lnS_y
argmax_lnS_value
```

Store raw native values. Colour-scale ranges belong in a separate deterministic figure-source manifest.

## Scalar trajectory identity

Use COMSOL positive-electrode integrals or volume averages, not unweighted exported-node means:

```text
Q
native_solnum
max_lnS_pos
integral_eps_s_pos
mean_eps_s_pos
integral_R_A_pos
mean_R_A_pos
eta
terminal_voltage_if_used
```

Store both numerator and normalization volume when a mean is reported.

## Matched-control alignment

```text
matched_pair_id
full_case_id
fixed_case_id
phase_off_case_id
alignment_event_source = scenario_A_full_Qloc
DeltaQ_from_full_Qloc
paired_Q
paired_native_grid_sha256
eta_full
eta_fixed
delta_eta_signed
```

If the full and fixed branches do not share an exact native Q grid, the production projector must use the already predeclared matching rule. Do not silently interpolate merely to fill Fig. 4d or Fig. 5d. The source table must record the number of exact paired samples used.

## Fig. 5 node summary

```text
Qloc_reached
Qloc
Qloc_plus_1_available
actual_Q_for_plus_1
eps_s_at_plus_1
R_A_at_plus_1
max_abs_delta_eta_0_to_1
signed_delta_eta_at_abs_max
Q_at_abs_max
paired_sample_count
censor_reason
```

## Evidence namespace

Every scientific source row must carry an internal namespace flag so pilot material cannot leak through a merge:

```text
evidence_namespace = production | numerical_QA | execution_QA
manuscript_allowed = true | false
figure_allowed = true | false
```

Only `production` rows may populate the five main figures. The paper itself must not display these governance labels.

## Not required

Because A\* is selected, do **not** add the spatial matched-control difference export proposed by Architecture B. It is unnecessary for the five-figure argument.

---

# 9. Main-text language rules

Use physical English:

```text
first local supersaturation onset
local free-I2 stress
retained-solid fraction
Scenario-A remaining accessibility
phase-off reference
matched fixed-area control
current–transport plane
one unit after onset
accessibility feedback
```

Do not use in the paper:

```text
active physical row
outer node
event backbone
campaign
registered
production schema
manuscript eligible
SI-only case 59–65
QA pilot
population
route retired
hash-registered
```

Translate internal identities into physical sentences.

Bad:

> The registered 56-row outer-node production population was projected at four event-relative roles.

Use:

> We evaluated the complete current–transport grid at four native states referenced to the first local supersaturation onset.

Bad:

> The A-only closure was retained while the B branch was retired to an SI comparator.

Use:

> All continuum simulations use Scenario A. A separate analytical upper bound is reported in the Supplementary Information.

Bad:

> The matched control validates the accessibility mechanism.

Use:

> The matched fixed-area calculation isolates the response produced by accessibility feedback within the model.

NH4Br belongs in the Methods condition statement and parameter table only. It does not belong in a figure title, Results heading, abstract conclusion or concluding design claim.

---

# 10. Final rejection risks

## Risk 1 — relabelling the only event

Any use of average saturation, mean onset or an accessibility event would contradict the frozen campaign and make the paper look reconstructed after seeing the output.

## Risk 2 — turning the independent comparator into validation

If DFT/MD/Scenario B/pore-network panels remain in the main causal chain, reviewers will read them as validation of the continuum relation. They are not.

## Risk 3 — presenting Fig. 5 as a dashboard rather than one physical comparison

Four maps are acceptable only because they use the same complete 4 × 7 grid and follow one sequence: onset → retained solid → remaining accessibility → matched-control consequence. Adding scores, ranks, traffic-light coding, SI-only finite-\(Da_\phi\) points or numerical variants would turn the figure back into a consultant report.

---

# Final ruling

**Adopt A\*.**

- Main Fig. 3 uses three columns: \(Q_{\mathrm{loc}}-2\), \(Q_{\mathrm{loc}}\), \(Q_{\mathrm{loc}}+1\).
- The +0.5 field remains in SI on the same scales.
- Main Fig. 4 contains only the phase-off, Scenario-A full and matched fixed-area reference trajectories.
- Cases 59–65 and all 22 numerical variants remain in SI.
- The completed independent comparator moves entirely to SI.
- Main Fig. 5 is the exact, unsmoothed 4 × 7 map set with no accessibility threshold.
- No new physical case, event, threshold or production value is introduced.
