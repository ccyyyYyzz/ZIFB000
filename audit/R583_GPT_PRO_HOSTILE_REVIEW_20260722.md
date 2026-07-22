# R583 hostile pre-editorial review

**Date:** 2026-07-22  
**Review mode:** editor-in-chief rejection gate  
**Article type:** invited theoretical Article for *SCIENCE CHINA Technological Sciences*  
**Scientific subject:** porous ZIFB positive electrode  

## Inspection basis and non-negotiable limit

The accessible default branch does not contain a current R583 manuscript file or the current Fig. 1/2/3/5 masters and captions. Its root still points readers to the R93 archive. I therefore do **not** claim a line-by-line or pixel-by-pixel inspection of an unavailable R583 draft. This report is a hostile architecture and house-style review based on the frozen R583 scientific boundaries supplied in the current audit chain and on the current R583 execution-QA architecture record. It does not reuse R582 results or retired model conclusions.

The following facts are treated as locked:

- the porous ZIFB positive electrode is the sole protagonist;
- the Article is theoretical and does not require new physical experiments;
- the active continuum family is finite-rate only, with 64 physical cases and 22 numerical checks;
- \(Da_\phi=0,0.01,0.1,1,10,100\), and \(Da_\phi=100\) is still finite;
- the infinite-rate/algebraic route is retired;
- Scenario A is the sole continuum accessibility relation;
- Scenario B/case 66 is only a non-continuum analytical DFT-placement upper bound in SI;
- the four current COMSOL runs are execution-QA pilots and are ineligible for manuscript or figure population;
- no continuum number may enter the paper before a separate production authorization;
- NH4Br is a representative supporting-electrolyte/speciation condition, not the scientific claim;
- visible figure text must be Times New Roman, mathematical text TeX Gyre Termes Math, at least 8 pt, 600 dpi, with no Type 3 fonts.

## Editorial ruling

**The current narrative architecture should not be sent to the invited editor.** The model scope is defensible, but the paper will be rejected if it reads as a registry of branches, cases, retired routes, numerical identities and caveats rather than as one physical argument about a porous positive electrode. The necessary repair is not polishing. Fig. 1, Fig. 2, Fig. 3 and Fig. 5 need a new reading order, and the prose must be rebuilt around observable model states rather than project governance.

---

# A. The ten most damaging reader problems

## P0-1 — The manuscript is likely organized around model administration rather than the electrode question

A first-time electrochemist does not care that the calculation contains “64 physical / 22 numerical” cases, that one route is “retired”, or that one branch is “finite-only”. Those are internal controls. If they appear before the first physical result, the paper sounds like a software release note.

**Why it fails:** the reader has to learn the project’s governance language before learning what the positive electrode does.

**Required action:** the first two pages must contain only this causal question:

> When does locally generated free iodine exceed the handling capacity of the porous positive electrode, and how does that state become retained solid and loss of accessible reaction area?

Move case counts, retired-route history, execution status and solver identities to Methods or SI. In the main text, write “finite-rate precipitation model”, “parameter sweep” and “numerical checks”. Do not write “finite-only population”, “physical population”, “production branch” or “retired route”.

## P0-2 — Fig. 3 has no defensible comparison grammar unless the columns are event-relative

An arbitrary set of areal capacities forces the reader to remember where each capacity lies relative to saturation and accessibility loss. Independent colour limits make the problem worse. A reader who spends half a minute identifying the compared states has already lost the argument.

**Why it fails:** capacity is not itself the mechanism. The mechanism is the ordering of local saturation, retained solid and functional area loss.

**Required action:** rebuild Fig. 3 as a 3 × 3 event-relative field matrix. Use actual native solution snapshots without interpolation, but label each column by both its actual \(Q\) and its event relation. The exact contract is given in Section B.

## P0-3 — Four incompatible evidence identities are at risk of being drawn as one validation chain

The Article contains four fundamentally different objects:

1. internal continuum states;
2. matched or parametric continuum calculations;
3. independent lower-scale bounds;
4. numerical checks.

The DFT-placement bound, Scenario A continuum relation, numerical controls and current execution-QA pilots are not interchangeable forms of validation.

**Why it fails:** a visually continuous “multiscale” chain suggests that DFT validates the continuum field, or that a numerical pilot supports a physical claim.

**Required action:**

- Main text: Scenario A only; no Scenario B result.
- SI S7: Scenario A labelled **sole continuum accessibility relation**; Scenario B labelled **retired non-continuum analytical upper bound**.
- DFT/analytical material: boundary prior only.
- 22 numerical cases: convergence and implementation checks only.
- four pilots: absent from manuscript, figures, captions, source-data tables and figure scripts.

## P0-4 — Fig. 1 will be rejected if it depicts a morphology that the continuum model does not resolve

Any orange clump, shell, film, covered fibre, blocked pore, throat bridge or advancing front will be read as a predicted deposit morphology. A disclaimer in the caption does not undo a visual assertion.

**Why it fails:** the graphic converts state variables into a fake microscope image.

**Required action:** Fig. 1 must show a flat positive-electrode domain and a local source–removal balance. Retained iodine must be represented as a state variable or field swatch, not as particles or crust. No coverage icon, no site-density icon and no pore blockage.

## P0-5 — The paper cannot pre-narrate production results that do not yet exist

The current four COMSOL runs are explicitly execution-QA only. They cannot populate a trend, a map, a threshold, a caption, a placeholder table or even a qualitative “as expected” sentence in Results.

**Why it fails:** a manuscript-ineligible run becomes de facto evidence as soon as its result is written into the paper, even without a number.

**Required action:** before production authorization, use an internal claim map, not manuscript prose. Any sentence whose truth depends on a continuum result must remain tagged internally as `PENDING_PRODUCTION` and must not appear in the submission PDF. The final Article may contain only independently authorized production outputs.

## P1-1 — Fig. 2 should show the state sequence, not the model inventory

If Fig. 2 is another schematic, equation board or parameter taxonomy, the reader reaches Fig. 3 without knowing the baseline temporal story.

**Why it fails:** the paper asks the reader to interpret spatial fields before showing how the averaged states are ordered along charge.

**Required action:** Fig. 2 must be the baseline charge-evolution figure. Show free-I2 saturation, retained solid and Scenario-A remaining accessibility on aligned axes, followed by the terminal response. Equations and parameter inventories belong in Methods/SI.

## P1-2 — Fig. 5 will look like a consultant report if it ranks many “levers” and “spans”

A multi-row parameter dashboard, traffic-light ranking or arrow table is not a scientific conclusion. It is an internal decision aid.

**Why it fails:** the reader sees a catalogue of knobs rather than a physical law.

**Required action:** choose one primary outcome for all 64 physical cases. The preferred quantity is the separation between the declared saturation event and the declared Scenario-A accessibility event, \(\Delta Q\). Show that quantity across the finite \(Da_\phi\) family. Put all 22 numerical checks in SI.

## P1-3 — NH4Br can still steal the paper through grammar even when it is absent from the title

A paragraph controlled by “bromide complexation”, “NH4Br concentration” or “mixed-halide speciation” makes the electrolyte appear to be the mechanism. It is not.

**Why it fails:** the positive electrode stops being the grammatical and causal subject.

**Required action:** mention the representative supporting electrolyte once in Methods and, if necessary, once in an SI parameter table. In Results, the subject must be “the positive electrode”, “the free-I2 field”, “the retained-solid field”, “the accessibility relation” or “the reaction field”. Do not place NH4Br in a main-figure title, abstract conclusion, keyword or final conclusion.

## P1-4 — The prose is vulnerable to noun stacks and machine-generated negation

Internal phrases such as “finite-only physical-case production population”, “registered event-relative state-coordinate extraction”, “non-continuum analytical DFT-placement upper-bound comparator” and “manuscript-ineligible execution-QA pilot” may be correct in an audit record. They are intolerable in a paper.

**Why it fails:** nouns replace verbs, and every sentence sounds legally qualified.

**Required action:** translate project vocabulary into physical English:

- “finite-only model” → “finite-rate model”;
- “physical cases” → “parameter sweep”;
- “numerical cases” → “numerical checks”;
- “Scenario A” → “the continuum accessibility relation” after its one Methods definition;
- “Scenario B” → “an analytical upper bound” in SI only;
- “event coordinate” → “transition capacity” or the exact physical event name;
- “registered native solnum” → omit from Results; retain in reproducibility records.

## P2-1 — Captions are likely carrying audit arguments that the figure should carry visually

A caption should not explain file provenance, branch eligibility, retired routes, exact case counts, solver status or every forbidden interpretation.

**Why it fails:** the reader must parse legal prose to understand the picture.

**Required action:** use a claim title, one sentence per panel, and one boundary sentence. Target 70–110 words. Put source identity and inference rules in Source Data/SI.

## P2-2 — The visual system will still look amateurish if every variable receives a new colour and every panel receives a heading

Five figures with unrelated palettes, filled boxes, panel subtitles, in-panel paragraphs and repeated legends will look assembled rather than authored.

**Required action:** lock one visual grammar:

- soluble/free-I2 stress: blue to amber around \(S=1\);
- retained solid: amber/brown sequential;
- remaining accessibility: teal sequential;
- current or terminal response: graphite/violet;
- numerical controls and external bounds: grey;
- no more than four chromatic colours in any figure;
- no visible text below 8 pt;
- mathematical symbols typeset consistently in TeX Gyre Termes Math.

---

# B. New five-figure narrative

The paper needs one causal sentence that survives all five figures:

> Local free-I2 stress develops first; finite-rate conversion creates retained solid; the sole continuum accessibility relation converts that inventory into loss of usable reaction area; the resulting response is spatially non-uniform and condition dependent.

## Figure 1 — What the positive electrode must handle

**Single claim:** local iodine generation and removal are separate from retained-solid inventory and accessible area.

**Layout:** two panels, 180 mm × approximately 88–95 mm.

- **a, 35% width:** flat positive-electrode domain. Current collector, porous positive felt and separator only. Mark through-plane \(x\), flow direction \(y\), one flow arrow and one current-direction arrow.
- **b, 65% width:** a local surface-level source–removal vignette. Electrochemical generation supplies free I2; complexation/transport remove it; \(S>1\) activates a finite-rate retained-solid state; the continuum accessibility relation maps retained solid to remaining active area; local current responds.

**Reader action in 10 s:** identify the positive electrode, identify the source–removal competition, and see that saturation, solid inventory and accessibility are different quantities.

**Delete:** DFT structures, NH4Br icons, Scenario labels, case counts, pressure, pore blockage, deposit particles, branch names and solver architecture.

## Figure 2 — Baseline states separate along charge

**Single claim:** the positive-electrode saturation, retained-solid and accessibility states do not evolve as one scalar.

**Layout:** asymmetric two-panel figure.

- **a, hero, approximately 65% width:** three vertically aligned traces sharing the areal-capacity axis:
  1. electrode-average free-I2 saturation ratio;
  2. electrode-average retained-solid fraction;
  3. electrode-average Scenario-A remaining accessibility.

  Use separate y-axes in stacked strips, never a triple y-axis. Mark the declared transition capacities only after production values exist.

- **b, approximately 35% width:** terminal response on the same capacity axis. Use voltage, total overpotential or another already solved manuscript output. Do not introduce a new proxy solely for the figure.

**Reader action in 10 s:** see the event ordering and connect the later terminal response to accessibility rather than treating the first saturation crossing as immediate failure.

**Move to SI:** equations, all six \(Da_\phi\) curves, mesh/time-step controls, case inventory and solver details.

## Figure 3 — Spatial progression of iodine stress and accessibility loss

**Decision:** use event-relative 2D fields. This is better than a collection of arbitrary areal capacities.

### Exact grid

A **3 × 3 matrix**, followed by one narrow quantitative profile.

### Columns

Use one baseline production case and select native solution snapshots without field interpolation:

1. **Before average saturation** — the last native solution before the declared electrode-average saturation event.
2. **Immediately after average saturation** — the first native solution after that event.
3. **Near the Scenario-A accessibility event or late charge** — the nearest native solution to the predeclared accessibility event; if that event is not reached, use the final complete solution and label it explicitly as “event not reached”.

Each heading must show:

```text
actual Q value
short event relation
```

Do not label a snapshot as equal to an event unless the native solution is exactly at that event.

### Rows

1. **Free-I2 saturation ratio, \(S_{\mathrm{I2}}\)** — the chemical/transport stress.
2. **Retained-solid fraction, \(\varepsilon_s\)** — the stored solid inventory.
3. **Scenario-A remaining accessibility field** — use the exact continuum field name and symbol; do not replace it by a related complement or geometric upper bound.

### Shared scales

- \(S_{\mathrm{I2}}\): one diverging scale across all three columns, centred exactly at \(S=1\). Blue below one, neutral at one, amber above one.
- \(\varepsilon_s\): one shared non-negative sequential scale. Use symmetric-log only if zero and several decades must coexist; state the linear region.
- remaining accessibility: one shared linear 0–1 scale, with the colourbar explicitly labelled “remaining”.

No column may autoscale independently.

### Companion plot

Below the matrix, show only the flow-direction arithmetic mean of the Scenario-A remaining-accessibility field versus through-plane position \(x\) for the three snapshots. This quantifies the spatial gradient without inventing a thresholded “affected area”.

### Reading order

1. left to right: charge/event progression;
2. top to bottom: stress → retained inventory → functional consequence;
3. bottom profile: quantify the through-plane accessibility gradient.

### Direct annotations

Use at most two:

- “local \(S>1\) first appears here”;
- “remaining accessibility decreases most strongly here”.

Do not write “film”, “coverage”, “blocked zone”, “front”, “shell”, “bridge”, “pore closure” or “deposit morphology”.

### Move to SI

- total-current maps;
- partial-current maps;
- velocity, hydraulic pressure and permeability;
- every additional capacity snapshot;
- all \(Da_\phi\) variants;
- all numerical-control fields;
- Scenario B;
- any electrical-potential map not explicitly exported for the production calculation.

**Reader action in 10 s:** say where free-I2 stress appears, where solid is retained and where usable area later decreases.

## Figure 4 — Finite-rate conversion and the sole continuum accessibility relation

**Single claim:** finite phase conversion controls how quickly supersaturation becomes retained solid, while the sole continuum accessibility relation controls how retained solid becomes functional area loss.

Keep the repaired A-only panel c. The main figure must never show Scenario B as a competing continuum result.

Recommended panel logic:

- **a:** finite-rate response across the six declared \(Da_\phi\) values;
- **b:** retained-solid evolution for a deliberately small subset of representative finite \(Da_\phi\) values, with all six values in SI if visual density is excessive;
- **c:** Scenario-A continuum accessibility relation only;
- **d:** resulting terminal or reaction response.

Use \(Da_\phi=100\) as a finite point. Do not label it “fast limit”, “instantaneous”, “algebraic” or “approximately infinite”.

**Reader action in 10 s:** distinguish phase-conversion kinetics from the inventory-to-accessibility relation.

## Figure 5 — Physical conditions control the separation between saturation and accessibility loss

**Single claim:** the physical parameter sweep changes the charge interval between the saturation event and the Scenario-A accessibility event.

### Primary outcome

Predeclare one scalar:

\[
\Delta Q = Q_{\mathrm{accessibility}}-Q_{\mathrm{saturation}}.
\]

Use the exact event definitions adopted by the model. If the accessibility event is not reached, show a right-censored observation; do not impute or extrapolate it.

### Layout

Use **six small multiples in a 2 × 3 grid**, ordered:

```text
Da_phi = 0 | 0.01 | 0.1
Da_phi = 1 | 10   | 100
```

Within every facet:

- show only the 64 manuscript-eligible physical cases;
- use the same axes and the same \(\Delta Q\) scale;
- if the physical design is a rectangular two-axis grid, use points or cells without smoothing;
- if it is not rectangular, use points grouped by the actual parameter family and do not fabricate a continuous surface;
- direct-label the baseline condition once.

Do not put the 22 numerical checks in the same matrix. They belong in SI as proof that numerical variation is smaller than the reported physical effects.

**Reader action in 10 s:** see how the physical window changes across finite phase-conversion rates.

---

# C. Publication-level Fig. 1 visual construction

## Canvas and hierarchy

- Final width: 180 mm.
- Height: 88–95 mm.
- White background.
- No outer frame.
- Panel a occupies roughly one third; panel b roughly two thirds.
- Panel labels: 10 pt bold Times New Roman.
- All other visible text: 8–9 pt Times New Roman.
- Mathematical symbols: TeX Gyre Termes Math, optically matched.
- Lines: 0.6–1.0 pt; no shadows, gradients or rounded cards.

## Panel a — domain

Draw a flat orthographic strip:

```text
current collector | porous positive carbon felt | separator
```

- felt: very pale warm grey or pale sand;
- current collector: graphite;
- separator: pale cool grey;
- one blue arrow along \(y\) for electrolyte flow;
- one graphite arrow along \(x\) for current direction;
- no negative-electrode drawing unless represented by a single pale-grey boundary label outside the active domain.

The positive felt must occupy most of the panel. The separator and collector are orientation references, not competing visual objects.

## Panel b — local physical relation, not a workflow

Use a horizontal carbon-surface line near the lower third. Above it is the local liquid phase.

1. At the surface, show a compact reaction label indicating generation of free I2.
2. From the free-I2 region, draw two outward arrows labelled “complexation” and “transport”. They are removal routes, not separate protagonists.
3. Place a thin threshold line labelled \(S_{\mathrm{I2}}=1\).
4. Below or beside it, show a small state bar for retained solid \(\varepsilon_s\), not particles.
5. To the right, show a teal remaining-area bar labelled with the exact Scenario-A continuum accessibility variable.
6. A single return arrow from remaining area to local reaction current closes the coupling.

Use solid arrows for solved coupling. Use a thin grey dashed outline only for a prescribed input or external boundary, if one is absolutely necessary.

## Colour semantics

- free-I2 stress: blue below saturation, amber above saturation;
- retained solid: amber/brown;
- remaining accessibility: teal;
- current/terminal response: graphite or muted violet;
- prescribed/supporting conditions: grey.

Do not use red/green success–failure coding.

## Must appear

- porous positive electrode;
- \(x\) and \(y\) orientation;
- free-I2 generation;
- complexation/transport removal;
- finite-rate retained-solid state;
- sole continuum accessibility relation;
- current feedback;
- one short boundary note in the caption: “The schematic represents continuum states and model couplings, not a microscopic deposit morphology.”

## Must not appear

- NH4Br molecule or bromide icon;
- DFT carbon motifs;
- Scenario B;
- site density;
- microscopic coverage;
- iodine crystals, shells, films or clumps;
- pore blockage or pressure front;
- \(Da=\infty\), fast algebraic route or route 2;
- 64/22 case counts;
- execution pilots, authorization language, file hashes or solver blocks.

---

# D. House style

## Core vocabulary

Use these terms consistently:

- porous positive electrode;
- positive carbon felt;
- local free-I2 supersaturation;
- retained solid iodine / retained-solid fraction;
- remaining accessible reaction area;
- finite-rate precipitation and dissolution;
- through-plane direction;
- flow direction;
- current redistribution;
- continuum accessibility relation;
- parameter sweep;
- numerical convergence/check;
- model prediction;
- analytical upper bound;
- representative supporting electrolyte.

Do not rename the same object to suit a new paragraph. One state, one noun, one symbol.

## Preferred verbs

Use physical verbs:

> generates, transports, complexes, approaches, exceeds, retains, accumulates, decreases, redistributes, delays, advances, shifts, remains.

Avoid promotional verbs:

> reveals, unveils, elucidates, unlocks, highlights, showcases, demonstrates unambiguously, provides unprecedented insight.

## Sentence rhythm

A Results paragraph should usually perform four actions:

1. state the observation;
2. give the comparison or number;
3. give the physical interpretation;
4. state one limitation only if it is needed at that point.

Target 18–25 words for most sentences. Do not join method, result, caveat and implication with four semicolons.

### Bad rhythm

> Under the registered finite-only physical-case architecture, the state-resolved framework, rather than assuming the retired fast algebraic route, systematically demonstrates a spatially heterogeneous accessibility-loss response that should not be interpreted as morphology.

### House-style rhythm

> The finite-rate model predicts a non-uniform loss of accessible area across the positive felt. The largest change occurs near the separator-facing side. These fields describe continuum states, not deposit morphology.

## Paragraph actions by section

### Introduction

- paragraph 1: engineering problem;
- paragraph 2: why bulk voltage or total iodine is insufficient;
- paragraph 3: missing state relation;
- final paragraph: model, questions and contribution.

Do not summarize every computational scale in the opening paragraph.

### Results

Begin every subsection with the result, not “To investigate…”, “A framework was constructed…”, or a list of parameters.

### Discussion

Discuss:

- why saturation and accessibility are distinct;
- why locality matters;
- what finite-rate phase conversion changes;
- what remains conditional on the accessibility relation;
- what future measurements could test.

Do not repeat the Methods scope ledger.

### Captions

- first sentence: claim;
- one sentence per panel;
- one interpretation boundary at the end;
- no provenance narrative.

## Governance/audit vocabulary banned from scientific prose

The following belong only in repository records, not in title, abstract, Results, figure labels or conclusion:

```text
registered
production branch
authoritative branch
release lock
ledger
manifest
identity gate
frozen output
readback
population
manuscript eligible / ineligible
execution QA
permit
authorization
canonical
route retired
case 66
native solnum
status/recovery
```

## Template/AI vocabulary to remove

```text
multiscale framework
integrated architecture
synergistic interplay
mechanistic landscape
three-node pathway
state clock
lever
rail
workflow
holistic
comprehensive
systematically elucidates
provides a new paradigm
```

## Negative-stack rule

The manuscript must not define every claim by listing five things it does not mean. State a positive scope first.

Bad:

> The field is not a micrograph, not coverage, not a blocking front and not evidence of pore closure.

Better:

> The field is the continuum retained-solid fraction. Microscopic deposit structure lies outside the model.

One boundary sentence per figure or subsection is enough.

## NH4Br rule

Use this wording once in Methods:

> The baseline uses one representative supporting electrolyte; its ligand and transport properties enter the prescribed speciation and transport relations.

The chemical composition can then be listed in a parameter table. Do not discuss an NH4Br “effect” unless the Article contains a separately authorized electrolyte-comparison study, which it currently does not.

---

# E. Directly usable language architecture

## Proposed title

**Finite-rate iodine retention and accessibility loss in porous zinc–iodine flow-battery positive electrodes**

## Abstract logic skeleton

Use seven sentences. Sentences 4–6 may be populated only after production authorization.

1. **Problem**

   > During charge, the porous positive electrode must remove free iodine from reacting carbon surfaces before local supersaturation converts dissolved inventory into retained solid.

2. **Gap**

   > Existing descriptions often combine iodine saturation, solid accumulation and loss of reaction area into one empirical state.

3. **Approach**

   > We develop a two-dimensional finite-rate model that resolves free-I2 supersaturation, retained-solid fraction and remaining accessible area separately, and couples them through one continuum accessibility relation.

4. **Baseline production result — pending**

   > [State the production-supported ordering of the saturation, retained-solid and accessibility events; insert no pilot result.]

5. **Spatial production result — pending**

   > [State where the three fields change and how the spatial pattern develops; do not name morphology.]

6. **Finite-rate/physical sweep production result — pending**

   > [State how finite \(Da_\phi\) and the physical parameter sweep change the declared event separation; report only production values.]

7. **Conclusion**

   > The analysis separates the conditions that control the onset of iodine retention from those that control its functional consequence in the positive electrode, without assigning a microscopic deposit morphology.

Do not mention NH4Br, Scenario B, the 64/22 count, pilots or numerical certificates in the abstract.

## Introduction final paragraph

> Here we develop a two-dimensional finite-rate model of the porous positive electrode in a zinc–iodine flow battery. The model resolves local free-I2 supersaturation, retained solid iodine and remaining accessible reaction area as separate states. We first establish their ordering along charge, then examine where they develop across the felt, and finally determine how finite phase-conversion kinetics and operating or transport conditions alter the interval between saturation and accessibility loss. One continuum accessibility relation is used throughout the solved model; independent molecular and analytical calculations are retained only as bounds on prescribed inputs. This structure isolates the positive-electrode mechanism while avoiding any inference of a unique microscopic deposit morphology.

## Results headings and first sentences

### 1. A finite-rate model separates iodine saturation, retention and accessibility

> The model resolves free-I2 stress, retained solid and remaining reaction area as distinct positive-electrode states rather than one loss variable.

### 2. Iodine saturation and accessibility loss occur at different charge states

> The baseline calculation shows that the first saturation event and the later accessibility response are separated along the areal-capacity axis.

### 3. The positive-electrode states develop non-uniformly across the felt

> Event-relative fields show where free-I2 stress appears, where solid iodine is retained and where remaining accessible area subsequently decreases.

### 4. Finite phase conversion controls the link between supersaturation and retained solid

> Changing the finite phase-conversion rate alters how quickly supersaturation is converted into retained inventory, while the continuum accessibility relation determines its functional consequence.

### 5. Operating and transport conditions shift the saturation-to-accessibility interval

> Across the physical parameter sweep, the separation between the declared saturation and accessibility events provides a common measure of positive-electrode response.

Do not begin any subsection with a model-construction history, a case count or “To investigate”.

## Conclusion logic skeleton

1. **Contribution**

   > This work separates free-I2 supersaturation, retained solid iodine and remaining accessible area in a finite-rate porous-positive-electrode model.

2. **Baseline production finding — pending**

   > [State the production-supported event ordering without a placeholder number.]

3. **Spatial production finding — pending**

   > [State the production-supported location and progression of the continuum fields.]

4. **Finite-rate/closure finding — pending**

   > [State what changes with finite \(Da_\phi\) and what remains controlled by the sole continuum accessibility relation.]

5. **Engineering implication**

   > The useful design distinction is between conditions that delay local free-I2 saturation and conditions that preserve accessible reaction area after iodine is retained.

6. **Boundary and future test**

   > Future electrode-resolved measurements of iodine speciation and accessible reaction area could test this state sequence; the present model does not identify a unique deposit morphology.

NH4Br, Scenario B and repository governance do not belong in the conclusion.

---

# F. Experimental material disposition

## Editorial answer

**No new experiment is required for this theoretical Article.** Adding weak or sparse experiments would make the paper less coherent, not more convincing.

## Leave entirely for a later experimental paper

- supporting-electrolyte composition series, including all NH4Br concentration comparisons;
- current-rate and coulombic-efficiency ladders;
- compression or felt-thickness records;
- cycle-to-cycle late-charge voltage and dV/dQ analysis;
- CV, CA and EIS datasets;
- visual observations of dark iodine, clumps, pressure rise, pump-line obstruction or hardware failure;
- any optical or microscopic image lacking a registered quantitative link to the continuum state;
- the detailed NH4Cl/NH4Br metadata-correction inventory.

If one sentence of external context is indispensable, use a literature citation or one neutral statement in the Introduction. Do not place an experimental panel in the five-figure core.

If a historical experimental file is cited, disclose once in Methods or Data Availability that legacy NH4Cl/NH4CL labels denote NH4Br while raw bytes and filenames remain unchanged. Do not turn the correction into a scientific result.

## Minimum theoretical validation likely to be demanded by reviewers

1. **Mesh, time-step and segment/restart convergence** using the 22 numerical checks.
2. **Current and species conservation** over the solved domain and across segment restarts.
3. **Finite-rate limiting behaviour** across all declared \(Da_\phi\) values, with \(Da_\phi=100\) explicitly retained as finite.
4. **Boundedness and positivity** of concentrations, retained-solid fraction and accessibility.
5. **Event-extraction stability** with respect to native solution indexing and restart logic.
6. **Parameter readback and unit consistency** for every production family.
7. **Sensitivity of the sole continuum accessibility relation** without promoting the retired analytical bound into a continuum alternative.
8. **Independent analytical checks of isolated subrelations** where available, clearly labelled as bounds rather than validation of continuum fields.
9. **Reproducible source data and rendering** for every main and SI figure.
10. **A declared separation between physical variation and numerical variation.** The main claim must be larger than the numerical uncertainty supporting it.

These are sufficient for a theory paper. Electrode-resolved speciation, impedance or imaging should be listed as future validation, not as a condition for this revision.

---

# G. Figure–claim–evidence–reader-action matrix

| Figure | One dominant claim | Permitted evidence | Reader action in 10 s | Excluded material |
|---|---|---|---|---|
| **1** | Local generation/removal, retained solid and accessibility are different positive-electrode states. | Equations and declared continuum couplings; no numerical result required. | Identify domain, source/removal balance and state sequence. | DFT structures, NH4Br emphasis, morphology, case codes, Scenario B. |
| **2** | Saturation, retained solid and accessibility separate along charge. | Authorized baseline production trajectories only. | Read the event ordering and connect the late terminal response to accessibility. | Pilot outputs, all-parameter overlays, numerical controls. |
| **3** | Local stress, retained solid and accessibility loss develop non-uniformly across the felt. | Authorized native 2D production fields at three event-relative snapshots. | Locate where each state first appears and how it progresses. | Current/hydraulic field inventory, arbitrary capacities, independent colour scales, morphology language. |
| **4** | Finite phase conversion and the sole continuum accessibility relation control different links in the response. | Authorized finite \(Da_\phi\) production results and Scenario-A continuum relation. | Separate phase kinetics from inventory-to-area mapping. | Infinite-rate route, Scenario B continuum curves, site-density inference. |
| **5** | Physical conditions change the saturation-to-accessibility interval across finite phase rates. | The 64 authorized physical production cases; predeclared event definitions and censoring rules. | Compare the physical operating window across the six finite \(Da_\phi\) facets. | The 22 numerical checks in the same plot, consultant ranking tables, pilots. |

---

# The three most likely rejection triggers

## 1. Submission before a separately authorized production dataset exists

This is fatal. Execution-QA pilots cannot become figures by changing a folder name or copying their scalars into a table. Any pending result written as if known will contaminate the evidence chain.

## 2. A Fig. 3 that still requires caption study to identify the compared states

Arbitrary capacities, four or five variables, independent scales and excessive annotations will make the central spatial figure unreadable. If the reader cannot say “stress first, solid next, area loss later” in ten seconds, the figure has failed.

## 3. A manuscript that visually or linguistically merges continuum physics, retired analytical bounds, numerical checks and electrolyte context

The editor will read it as a multiscale portfolio rather than one theoretical result. Scenario B, DFT placement, NH4Br and numerical controls must remain subordinate and correctly labelled. The positive electrode must remain the subject of every main figure and every Results subsection.

---

# Final pre-editorial gate

Do not send the Article to the invited editor until all of the following are true:

- Fig. 1 contains no morphology claim and no workflow boxes;
- Fig. 2 shows the baseline state sequence;
- Fig. 3 is the event-relative 3 × 3 field matrix specified above;
- Fig. 4 contains Scenario A only as a continuum relation;
- Fig. 5 uses one primary physical outcome and excludes numerical controls from the main visual;
- every main result is populated only from separately authorized production calculations;
- the abstract contains no pending qualitative claim disguised as a result;
- NH4Br appears only as a representative Methods condition;
- all audit/governance vocabulary has been removed from scientific prose;
- all visible figure text is at least 8 pt, with the required font system and no Type 3 fonts.

Until then, the manuscript is a technically controlled project record, not a publishable theoretical Article.
