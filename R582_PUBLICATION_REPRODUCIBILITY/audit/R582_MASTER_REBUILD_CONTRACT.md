# R582 master rebuild contract

Status: active production contract, 2026-07-20. This document supersedes the
visual and narrative architecture of R581 but does not alter the frozen R581
release. It consolidates the independent language, full-figure, and `ZIFB_W`
style audits. The hostile GPT Pro review will be added as an external challenge
record and may tighten this contract, but it may not relax the evidence rules
below.

## 1. Paper-level decision

R581 is scientifically traceable but editorially unfit for submission. It reads
as an audit dossier: definitions, provenance, solver identity, caveats, and
secondary branches repeatedly interrupt the central positive-electrode result.
The remedy is a structural rebuild, not cosmetic restyling.

R582 will make one claim:

> In the modeled ZIFB positive electrode, average free-I2 saturation precedes
> accessibility loss; the later solid-inventory and voltage trajectories depend
> strongly on how retained iodine is mapped onto accessible reaction area.

The paper will use six main figures. Existing experimental records motivate and
stress-test the modeled problem but are not described as independent validation
of positive-electrode state variables. Lower-scale calculations bound priors and
physical comparator families; they do not determine the calibrated production
closure.

### Default submission target

The production target is a **Journal of Power Sources Research Paper**, chosen
because it matches the ZIFB/ZBFB venue and argument style represented in
`ZIFB_W`. The live Elsevier guide checked on 2026-07-20 permits up to 8,000 words
excluding abstract, figures, tables, and references, and up to eight main figures;
R582 will target at most 6,500 words and six main figures. The abstract must not
exceed 200 words; keywords are limited to 1--7. A separate highlights file will
contain 3--5 bullets of at most 85 characters each. Editable LaTeX and individual
figure files are required, and the final data statement must cite/link a deposited
dataset or explain why sharing is impossible.

The journal explicitly prioritizes experimentally validated computational work.
R582 must therefore present the existing full-cell records honestly as
experimental anchors and stress tests, never disguise them as an independent
measurement of the modeled positive-electrode states, and make the remaining
validation gap visible to the editor. This is the main venue-fit risk. The figure
pipeline is programmatic and source-driven; no generative-image tool may be used
for manuscript artwork or the graphical abstract. A graphical abstract, if made,
will be constructed from the accepted vector figure grammar and registered data.

Official guide checked:
`https://www.sciencedirect.com/journal/journal-of-power-sources/publish/guide-for-authors`.

## 2. Immutable scientific and data boundaries

1. The porous ZIFB positive electrode is the scientific and grammatical subject.
2. NH4Br is one representative supporting electrolyte. Bromide is a supporting
   ligand/speciation participant, never the headline or visual hero.
3. Legacy experimental names containing `NH4Cl` or `NH4CL` denote NH4Br under
   `EXP-META-001`. Raw names and bytes remain unchanged; derived displays use the
   corrected identity and retain the metadata note.
4. No new physical experiment is available. Evidence gaps may be addressed only
   by verified literature, new simulations, or re-analysis of existing records.
5. Original experimental files and original COMSOL `.mph` files are immutable.
   New COMSOL work uses copies/new filenames, a registered study/solution/dataset,
   and input/output hashes.
6. Continuum fields are model outputs, not microscopy. No figure or sentence may
   infer a film, crystal morphology, microscopic coverage, blocking front, pore
   throat closure, or electric-potential field unless that quantity is explicitly
   exported and registered.
7. Hydraulic pressure must never be substituted for electric potential.
8. The voltage-calibrated accessibility relation is a production closure, not a
   measured morphology or parameter-free physical law.
9. `ZIFB_W` is a style corpus only. Scientific claims require sources from the
   verified `ZIFB` evidence library or the registered project evidence.

## 3. Narrative architecture

### Title

Frozen R582 title after the controlled copyedit:

> A positive-electrode model separating iodine saturation from accessibility
> loss in zinc–iodine flow batteries

The title contains neither NH4Br nor stacked promises such as “unified”,
“comprehensive”, “synergistic”, or “multiphysics”.

### Abstract

Use seven or eight sentences in this order:

1. Define the positive-electrode problem with concrete verbs.
2. State that dissolved iodine, solid I2, and accessible area are often conflated.
3. State the model and the separated states.
4. Give `Qs = 83.0 mAh cm-2` and `Qf,cal = 99.6 mAh cm-2` at
   `40 mA cm-2`.
5. Give the matched-closure result: `Delta Qs = 0.002 mAh cm-2`, no island-model
   half-accessibility by `120 mAh cm-2`, and endpoint `Delta V = -288 mV`.
6. State the pore-network result only if the redrawn panel supports the exact
   reported range.
7. State the transport/accessibility uncertainty and conditional design meaning.
8. State once that voltage does not identify morphology; do not repeat the same
   disclaimer elsewhere in the abstract.

### Main-text order

1. **Introduction** — four paragraphs: positive-electrode problem; known but
   conflicting solid-I2 behavior; why coupled in-operando states require a model;
   what this study resolves and the strongest result.
2. **Results 1: Existing records define the positive-electrode problem.** Show the
   observed late-charge symptom and rate dependence without validation language.
3. **Results 2: The model separates saturation, retained solid, and accessible
   area.** Define the domain and only the state variables needed downstream.
4. **Results 3: Spatial fields reveal where the modeled state changes.** Lead with
   the multi-capacity two-dimensional plate.
5. **Results 4: Accessibility feedback controls the late trajectory.** Present
   matched closures and identifiability.
6. **Results 5: Molecular and mesoscale calculations bound the uncertain inputs.**
   Keep only the priors/comparators that connect directly to transport or
   accessibility.
7. **Results 6: Transport and operating levers shift the modeled window.** Use
   solved anchors and visible evidence classes; no pseudo-phase-diagram authority.
8. **Discussion** — upstream/downstream separation; what voltage can and cannot
   identify; conditional design implications; one centralized limitations passage.
9. **Conclusion** — one paragraph, five to seven sentences, no new mechanism or
   future-work list.
10. **Methods** — equations, solver route, calibration, convergence, source
    identity, metadata correction, and data/code availability.

The standalone pre-Results theory chapter is removed. Essential equations move to
Methods; only the minimum variable definitions needed to read Fig. 2 remain in the
Results narrative.

## 4. Six-main-figure architecture

### Figure 1 — Existing full-cell records define the problem

Dominant claim: existing records show a late-charge voltage feature and
rate-dependent utilization that motivate, but do not independently validate, a
positive-electrode state model.

- a: minimal cell strip highlighting the positive felt.
- b, hero: representative `V(Q)` with aligned derivative or other registered
  late-charge feature readout.
- c: same-cell pristine CE/rate ladder; separate proxy sources remain unconnected.
- d: four-cycle onset/peak ordering relative to prospective model markers.

All physical-cell counts, within-cell ranges, proxy identities, and
`EXP-META-001` must remain visible in the caption/source data. Composition and
thickness comparisons remain in SI.

### Figure 2 — The model resolves distinct positive-electrode states

Dominant claim: the model deliberately separates free-I2 supersaturation,
retained-solid inventory, remaining accessible area, and voltage response.

- a: flat 2D cell/domain cross-section with collector, positive felt, separator,
  x/y coordinates, and one flow arrow.
- b: four-node chain `S -> eps_s -> A_bare/A0 -> V`; calibration enters only the
  accessible-area node.
- c: capacity strip marking `Qs = 83.0` and `Qf,cal = 99.6 mAh cm-2`, with three
  compact state glyphs.

No particles, film texture, 3D perspective, decorative molecules, crossing arrows,
or provenance boxes.

### Figure 3 — Spatial progression across areal capacity

Dominant claim: separator-facing retained solid is followed by loss of remaining
bare area and redistribution of reaction current along the registered trajectory.

- a: thin capacity clock marking exact `Qs` and `Qf,cal` plus the exported
  snapshots `Q = 80, 100, 120 mAh cm-2`; `Q=100` is labelled approximately
  `Qf,cal`, never equal to it.
- b: 2D retained-solid fraction maps.
- c, visual hero: 2D remaining bare-area fraction `A_bare/A0` maps.
- d: 2D total reaction-current magnitude/distribution maps.
- optional compact companion: y-averaged `A_bare/A0` through-plane profile only if
  it materially improves the 15-second reading.

One scale per variable is shared across capacities. Nonpositive current nodes are
masked or handled by a disclosed symlog rule, never silently clipped. Extended
`S`, extra capacities, velocity, permeability, and partial-current fields go to SI.

### Figure 4 — Accessibility closure controls the late trajectory

Dominant claim: changing only the accessibility relation barely moves saturation
but strongly changes later accessibility, retained solid, and voltage; voltage is
therefore non-identifying with respect to morphology.

- a: production, one-way shadow, and coupled-dense remaining-area trajectories.
- b, hero: matched voltage curves and `Delta V`, with `-288.2 mV` directly labelled.
- c: branch-specific retained-solid trajectories with only physically relevant
  reference levels.
- d: compact accessibility–coefficient degeneracy curve.

Solver IDs, hashes, mesh count, and tolerance remain in Methods/source data, not
inside the artwork.

### Figure 5 — Independent calculations bound transport and closure families

Dominant claim: lower-scale calculations bound placement, mobility, accessibility,
and permeability but do not supply the calibrated production relation.

- a: relative single-I2 site-energy ordering.
- b: I-, I3-, and I2Br- diffusivity points with the adopted `D_eff` range.
- c, hero: sparse/dense remaining-area families over the production solid-loading
  range.
- d: pore-network `K/K0` enlarged over the production range, with the full range
  only as an inset.

Cluster proxies, atomistic structures, CDD, PDOS, the full carrier ladder, overlap
score, and dense 3D renders remain in SI.

### Figure 6 — Transport and operating levers shift the modeled window

Dominant claim: applied current and oxidized-carrier diffusivity exert the clearest
modeled leverage on saturation; smooth permeability and the declared flow scenario
are weaker channels.

- a: `Qs` versus applied current using solved anchors; interpolate only between
  verified anchors.
- b: `Qs` versus `D_eff/D0` using the registered solved sweep.
- c: standardized marker shifts with marker shape/line style encoding full solve,
  analytical postprocess, or bounded prior.
- d: minimal three-node translation from controllable lever to generation stress,
  inventory stress, or accessibility.

Remove the one-anchor accessibility boundary and dashed extrapolation field. Move
the literature dissolution rail and analytical flow scenario to SI.

## 5. Main/SI/delete map

| R581 asset | R582 action |
|---|---|
| State-card Fig. 1 | Replace by compact Fig. 2b/c |
| Provenance Fig. 2 | SI evidence-role table |
| Geometry Fig. 3 | Replace by flat Fig. 2a |
| x–Q Fig. 4 | Compact SI timing summary |
| Closure Fig. 5 | Rebuild as main Fig. 4 |
| Molecular Fig. 6 | Keep two bounded-prior panels in Fig. 5; rest SI |
| Mesoscale Fig. 7 | Keep accessibility/permeability panels in Fig. 5; rest SI |
| J–Q Fig. 8 | Abandon composition; retain solved levers in Fig. 6 |
| Flow Fig. 9 | SI analytical robustness only |
| SI experimental Fig. S6 | Promote selected panels to Fig. 1 |
| SI 2D fields Fig. S8 | Rebuild/promote as Fig. 3 |
| SI negative-electrode CDR S7 | Delete as manuscript figure |
| SI internal-overpotential S4 | Convert to table or delete |
| SI 3D geometry S9 | Replace by explanatory 2D slices |

## 6. Language and terminology contract

Results paragraphs use the four-beat sequence: question, observation, comparison,
interpretation. A main result sentence should normally contain 15–25 words and one
claim. The scientific object, not “we” or “the framework”, is the default subject.

Preferred terms:

- `ZIFB positive electrode` then `positive electrode`;
- `NH4Br as a representative supporting electrolyte`;
- `free-I2 supersaturation` and symbol `S` after definition;
- `solid-I2 fraction` or `retained-solid inventory`;
- `remaining accessible-area fraction, A_bare/A0`;
- `calibrated accessibility relation` and `island-model variant`;
- `baseline simulation`, `matched simulation`, `operating window`, and
  `controlled model-form sensitivity`.

Remove or sharply limit:

- `registered`, `production`, `closure`, `marker`, `state clock`, `trajectory`,
  `scaffold`, `load-bearing`, `orthogonal evidence`, `physical comparator`,
  `fresh matched true-mesh`, and audit/branch vocabulary in Results;
- `It is found/seen that`, `remarkably`, `promising`, `unlock`, `shed light on`,
  `pave the way`, `complex interplay`, `holistic`, and `comprehensive framework`;
- sentence-initial caveats, repeated “does not” constructions, nested parentheses,
  stacked em dashes, and strings of three or more attributive nouns.

Use `reproduces` or `captures` only for a genuine comparison; use `indicates`,
`suggests`, or `is consistent with` for model-to-mechanism inference. Do not use
`prove`. State the calibrated-accessibility and no-morphology boundaries once in
the abstract, once at the first closure result, and once in Discussion.

## 7. Visual system

- 180 mm double-column width; 95–145 mm usual height, at most about 155 mm for the
  spatial plate.
- One manuscript-matched family everywhere: TeX Gyre Termes for body text and
  figure text, with NewTX/Termes-compatible mathematics. Plot scripts register
  the exact TeX Live OTF files and may not fall back to Arial, Helvetica,
  DejaVu Sans, or a platform default. Use a 7.2 pt base, 6.5 pt minimum ticks,
  and 8 pt bold lowercase panel labels.
- White background; left/bottom spines only; no default grid; editable SVG/PDF
  text; PDF Type 42/TrueType fonts; 600 dpi opaque RGB TIFF.
- Semantic palette: graphite control `#4D4D4D`, vermilion main relation `#D65345`,
  blue early state `#3B6FB6`, teal accessible area `#2A9D8F`, violet late state
  `#7A68A6`, amber iodine inventory `#D8912B`, muted cyan supporting context
  `#67A9B7`.
- No rainbow map, 3D decorative rendering, gloss, drop shadow, faux molecule,
  paragraph-length annotation, repeated legends, or per-snapshot autoscaling.
- One dominant visual region per main figure. Every panel must answer a named role:
  observed symptom, definition, comparison, quantitative consequence, limitation,
  or translation.

## 8. Submission gates

R582 is not frozen or described as submission-ready until all gates pass:

1. Every main figure passes a 15-second claim/comparison/encoding test at final
   placed size, in colour and grayscale.
2. No main-art text is below 6.5 pt; all vector text is editable; no Type 3 fonts.
   PDF/SVG font inspection confirms the same TeX Gyre Termes family as the
   manuscript body and reports no silent fallback.
3. Each quantitative panel has deterministic script, clean source table, input and
   output hashes, and a rendered-source manifest.
4. Main and SI captions match every plotted series, scale, capacity, unit, and
   evidence class.
5. All claims are mapped to registered evidence; citation metadata and cited
   statements pass the citation audit.
6. `NH4Cl` occurs only in the single legacy-metadata explanation or immutable raw
   filenames; all scientific displays use NH4Br.
7. Main/SI compile without errors from a clean build, cross-references resolve,
   PDFs are visually inspected page by page, and the frozen release reproduces
   from deposited sources.
8. A hostile reviewer pass, submission audit, data-availability audit, and final
   language scan report no unresolved fatal or major issue.

## 9. Implementation order

1. Rebuild Figs. 1–3 and lock the visual grammar.
2. Rebuild the closure/identifiability Fig. 4.
3. Consolidate lower-scale bounds into Fig. 5.
4. Recompute or verify the evidence-class-aware lever panels for Fig. 6.
5. Rewrite the title, abstract, Introduction, Results, Discussion, and Conclusion
   around the six-figure sequence.
6. Move equations, provenance, solver bookkeeping, secondary scenarios, and full
   sweeps to Methods/SI.
7. Rebuild SI, compile, render, and run visual/evidence/citation/cold-build QA.
8. Freeze a new release only after every gate is documented.
