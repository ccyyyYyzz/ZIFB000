# R582 figure architecture audit

**Scope.** Read-only audit of `manuscript/main.pdf` (35 pages), `manuscript/SI.pdf` (30 pages), both TeX sources, all 18 included figure masters, their Python renderers, and the deposited figure-source bundles. This is a human-readability and visual-argument audit, not another hash/compilation audit. A mechanically reproducible figure can still be a poor scientific figure.

**Backend and target.** Python/matplotlib only. The redesign contract assumes a two-column journal figure width of about 180 mm, editable text in SVG/PDF (`svg.fonttype = none`, `pdf.fonttype = 42`), 7--9 pt final-size type, and a restrained, paper-wide semantic palette.

**Non-negotiable scientific boundaries.** The ZIFB positive electrode is the protagonist. NH4Br is one representative supporting electrolyte, not the paper's subject. All legacy experimental names containing `NH4Cl`/`NH4CL` refer to operator-confirmed NH4Br under `EXP-META-001`; raw filenames remain unchanged. The continuum maps are model fields, not deposit images. The voltage-calibrated accessibility relation is not a measured morphology. No panel may imply otherwise.

## Executive verdict

The current figure set reads like an internal model-audit dossier, not a paper written for a human reader. The core evidence is present, but the visual hierarchy is inverted:

1. The main paper opens with two abstract box-and-arrow figures before showing either the modeled domain or any experimental symptom. The first experimental figure is Supplementary Fig. S6 on SI page 12. A reader must accept eleven pages of definitions before seeing why the model matters.
2. The most intuitive evidence, two-dimensional positive-electrode fields at different capacities, is already available but buried as Supplementary Fig. S8. Main Fig. 4 first averages those fields over the flow direction, removing the spatial picture that would let a reader understand the claim quickly.
3. Nine main figures carry too many jobs. Several are not main-figure claims at all: evidence provenance, an analytical flow scenario, and a two-anchor/extrapolation operating map are methods or robustness material.
4. The main figures use incompatible visual systems. Some scripts inherit serif Computer Modern-like styling and default grid lines, the newer R581 figures use compact sans serif, and the DFT composites mix vector text with rasterized labels. The same paper therefore looks assembled from several unrelated projects.
5. Native figure canvases range from 93 to 346 mm wide and are then scaled by factors of about 0.47--0.92 in TeX. Main Fig. 6 is drawn at 345.5 mm and reduced to about 163 mm; Supplementary Figs. S3--S5 are drawn at about 276 mm and reduced to about 149--152 mm. This produces nominally correct but practically unreadable labels.
6. Captions substitute for visual clarity. Main-figure captions average about 122 words (range 73--175); SI figure captions average about 109 words and reach 268 words. A figure that needs a paragraph of caveats before the reader knows what to see fails the 15-second test.
7. Disclaimers have migrated into the artwork as title lines, footers, shaded boxes, and callouts. They are scientifically necessary but visually dominant. Keep one precise boundary in the caption; do not make every panel look apologetic.
8. The current schematics use repeated cards, many arrows, decorative particles, and tiny annotations. They encode the audit trail, not the causal story. The result looks machine-assembled because every relationship is spelled out instead of being composed.
9. Main Fig. 8 gives visual authority to dashed extrapolations and to a literature rail that has no common Q coordinate. Two solved saturation anchors and one calibrated point cannot support a large phase-diagram aesthetic.
10. Supplementary Fig. S7 is a negative-electrode scenario estimate in a positive-electrode paper. It consumes a full figure and invites the wrong scope debate.

**Publication decision:** do not cosmetically restyle the existing 9 + 9 figures. Rebuild the paper around six main figures, promote selected existing evidence, and demote or delete the rest. The data are stronger than the current presentation.

## The Figure 3 issue

As currently numbered, Fig. 3 is the model-geometry schematic; the through-plane capacity map is Fig. 4 and the true two-dimensional snapshots are Supplementary Fig. S8. The user's criticism nevertheless identifies the correct structural failure: the third substantive visual should be the spatial result, not another explanatory schematic.

The recommended renumbering deliberately makes the **new Fig. 3** a set of two-dimensional fields at different areal capacities. The current Fig. 3 is simplified and merged into new Fig. 2.

The registered spatial source contains 35,970 rows: six capacities (`Q = 0, 80, 96, 100, 110, 120 mAh cm^-2`), 5,995 positive-domain nodes per snapshot, and a 55 by 109 x--y grid. Available fields are:

- free-I2 stress `S_surf`;
- retained-solid fraction `eps_s_pos`;
- calibrated accessibility loss `theta_eff` and bare-area fraction `A_bare_frac`;
- relative permeability, velocity magnitude, hydraulic pressure, and total current density `j_total_A_m2`.

A separate same-branch R581 export supplies `j_bare_A_m2`, `j_native_solid_A_m2`, and `Av_bare_1_m` at `Q = 80, 96, 100, 108, 115, 120 mAh cm^-2`, again with 5,995 nodes per snapshot.

There is **no electrical-potential field** (`phi_s`, `phi_l`, or equivalent) in the registered spatial CSVs reviewed here. `p_native_Pa` is hydraulic pressure and must never be presented as electric potential. Under the existing-export-only rule, the new Fig. 3 should show retained solid, bare accessible area, and reaction-current redistribution, with a compact saturation clock. An electric-potential map can only be added after a separately registered read-only export from a verified model copy.

## Cross-figure visual system

Use one style module for every new plot and schematic.

- Final main-figure width: 180 mm. Default height 95--145 mm; only the spatial plate may reach about 155 mm.
- Typeface: Arial, Helvetica, or DejaVu Sans fallback; 7.2 pt base, 6.5 pt minimum tick text, 8 pt bold lowercase panel letters.
- Spines: left and bottom only for quantitative plots. No default Cartesian grid. Use a few pale horizontal guides only where a quantitative comparison needs them.
- Semantic colors: control/state backbone dark navy; iodine inventory amber; accessible area teal; alternative closure muted carmine; contextual evidence grey. NH4Br receives no hero color.
- Field colors: stress uses one muted diverging map centered exactly on `S = 1`; retained solid uses one sequential map; accessible-area fraction is plotted in the intuitive direction (more area = more color); current uses one explicit log/symlog rule with masked numerical-zero values disclosed.
- A category keeps the same color in every figure. Green/red are reserved for directional gain/loss cues, not arbitrary series identity.
- No overall title inside the artwork. Use a short finding-style caption title. Panel headings state the variable or comparison, not a sentence-length conclusion.
- One shared legend or direct labels. One shared color bar per variable across capacities. Repeated legends and repeated x/y labels are removed.
- No bottom disclaimer strip, SHA string, solver name, or prose paragraph inside a main figure. Those belong in Methods, Source Data, or the caption.
- Every panel must remain readable at 100% page view, grayscale print, and color-vision-deficiency simulation.

## Current main figures: figure-by-figure verdicts

### Current Fig. 1 -- Conceptual iodine-state progression

- **Verdict:** **REDRAW + MERGE** into new Fig. 2; drop as a standalone main figure.
- **Single claim worth preserving:** saturation precedes the production half-accessibility marker, while retained solid continues to accumulate.
- **Current panel roles:** a--e are five consecutive state definitions; none is independent evidence.
- **15-second failure:** five equal cards, three mini-bars per card, two naming systems (`A_cal` and `theta_cal`), five footnotes, and a global footer force the reader to decode a legend before seeing the sequence. The large card count exaggerates a simple two-marker timeline. The bar glyphs resemble measured quantities although most lengths are schematic.
- **Specific redesign:** replace the five cards with one horizontal capacity strip. Mark `Q_s = 83.0` and `Q_f,cal = 99.6 mAh cm^-2`; place only three compact state glyphs below it: dissolved/free-I2 stress, retained solid, and remaining accessible area. Use `A_bare/A_0 = 1 - theta_cal` throughout so the visual direction is intuitive. Put the local-solid-before-average-S caveat in the caption, not a sixth visual element.
- **Panel roles after merge:** state-definition bridge in new Fig. 2b; event strip in new Fig. 2c.
- **Source:** `manuscript/source_data/Fig_R581_concept_state_progression/R581_concept_state_progression.py`; `R581_concept_state_progression_source_data.csv`; build record `R581_CONCEPT_STATE_PROGRESSION_BUILD.json`.

### Current Fig. 2 -- Evidence provenance across scales

- **Verdict:** **MOVE TO SI + REDRAW**, or replace with a one-column evidence-role table.
- **Single claim worth preserving:** lower-scale calculations constrain priors and comparators; only the continuum model generates the spatial production fields, and accessibility magnitude is voltage-calibrated.
- **Current panel roles:** DFT and MD are bounded priors; single-fibre and pore network are physical comparators; the large blue box is the continuum production branch; the orange box is calibration.
- **15-second failure:** diagonal crossing arrows, tiny italic edge labels, four unrelated source boxes, a large container, and an endpoint rail create a software-architecture diagram. The most important distinction, `solved field` versus `calibrated relation` versus `physical comparator`, is encoded by small text rather than layout.
- **Specific redesign:** in SI, use four aligned rows with columns `evidence`, `quantity supplied`, `how used`, and `what it cannot establish`. If a schematic is retained, use a left-to-right three-lane layout: priors, production model, physical comparators. No crossing arrows. The calibration arrow enters only the accessibility relation.
- **Panel roles after move:** methodological provenance only; no Results subsection should revolve around this figure.
- **Source:** `manuscript/source_data/Fig_R568_scale_provenance/R568_scale_provenance.py`; `R581_Fig_R568_scale_provenance_source_data.csv`.

### Current Fig. 3 -- Modeled system and positive-electrode domain

- **Verdict:** **REDRAW + MERGE** with the state chain as new Fig. 2.
- **Single claim worth preserving:** the continuum solve resolves a 2D positive carbon-felt domain between collector and separator, with through-plane gradients and flow along the orthogonal direction.
- **Current panel roles:** a defines cell geometry, coordinates, current, flow, and a schematic solid gradient; b maps felt to a single fibre and pore network.
- **15-second failure:** too many coordinate arrows, inconsistent line weights, pseudo-random orange particles, mixed font families, an off-canvas explanatory callout, and a second panel that jumps from device geometry to two unrelated mesoscale models. The orange particles visually assert a morphology, then prose denies that assertion.
- **Specific redesign:** new Fig. 2a should be a clean cross-section with only collector, positive felt, separator, negative side, x/y axes, and one flow arrow. Use a soft gradient or contour icon to denote a field, never particle-like deposit symbols. Put the single-fibre and network comparators in new Fig. 5 or SI. Under the geometry, new Fig. 2b shows the causal state chain `free-I2 stress -> retained solid -> remaining accessible area -> voltage response`; new Fig. 2c defines the two registered capacity markers.
- **Source:** `manuscript/source_data/Fig_R573_model_geometry/R573_model_geometry.py`; `R573_model_geometry_values.csv`.

### Current Fig. 4 -- Through-plane evolution of the production state

- **Verdict:** **REDRAW + SPLIT**. Promote the 2D evidence to new Fig. 3; retain a compact y-averaged x--Q summary in SI or as one subordinate panel.
- **Single claim worth preserving:** after average saturation, retained solid and accessibility loss become separator-facing, while the current distribution changes downstream.
- **Current panel roles:** three y-averaged heatmaps show stress, retained solid, and accessibility loss versus x and Q.
- **15-second failure:** the current plot says `2D domain` in the caption but shows only y-averaged fields. Three independent color scales, vertical event lines, a contour callout, and tiny colorbar text compete with the causal sequence. The smooth stress panel receives the same width as the much more informative accessibility field.
- **Specific redesign:** new Fig. 3 begins with a thin capacity clock marking `Q = 80`, `100`, and `120 mAh cm^-2` relative to `Q_s` and `Q_f,cal`. Below it, use three variable rows, each containing the three x--y snapshots: (i) retained-solid fraction, (ii) remaining bare-area fraction `A_bare/A_0`, and (iii) total reaction current density. A thin contour or small adjacent strip may show the native-solid current fraction derived from the registered partial-current export. Use one shared scale per row, collector/separator labels once, and one flow arrow. The y-averaged stress heatmap moves to SI because it establishes timing rather than the spatial result.
- **Data-integrity rule:** use `Q = 80/100/120` because those are exported snapshots; do not interpolate a fake `Q = 83.0202` or `99.5901` map. Label 100 as `approximately Q_f,cal`, not exactly equal. Treat numerical zero/nonpositive current explicitly rather than silently clipping it through `LogNorm`.
- **Source:** `manuscript/source_data/Fig_R545_fields/R545_spatial_fields.py`; `Fig3_baseline_spatial_long.csv`; `R581_Fig_R545_spatial_maps_source_data.csv`; `R581_Fig_R545_xQ_evolution_source_data.csv`; `R581_Fig_R545_field_definitions.csv`. Same-branch partial currents: `battery_comsol/02_outputs_core/R581_CANONICAL_CLOSURE_REBUILD/outputs/R581_partial_current_spatial.csv`, generated by `scripts/R581PartialCurrentSpatialProbe.java` and parsed by `scripts/R581_parse_partial_current_spatial.py`.

### Current Fig. 5 -- Matched true-mesh accessibility-closure sensitivity

- **Verdict:** **KEEP THE DATA + REDRAW** as new Fig. 4; combine with the key identifiability message from current Supplementary Fig. S3.
- **Single claim:** changing only the accessibility closure produces a large late-voltage divergence while leaving the saturation marker essentially unchanged; voltage alone therefore does not identify morphology.
- **Current panel roles:** a compares accessibility trajectories; b is the voltage/DeltaV hero; c tracks solid inventory and several closure-specific thresholds.
- **15-second failure:** panel c contains a textbox, two horizontal threshold lines, a vertical line, two long annotations, a legend, endpoint points, and three tiny provenance footers. The visually strongest panel is not the scientific hero; the endpoint `-288.2 mV` is easier to miss than the clutter.
- **Specific redesign:** use an asymmetric 2 by 2 layout. Panel a, compact: remaining accessible area for production control, one-way dense shadow, and coupled dense solve. Panel b, hero and twice the width: voltage trajectories with a directly labeled DeltaV inset and the `-288.2 mV` endpoint. Panel c: each branch's retained-solid trajectory with only the two physically relevant reference levels. Panel d: the accessibility--coefficient degeneracy curve from S3, visually quieter, to close the identifiability argument. Solver identity, hashes, mesh count, and tolerance stay in Methods/Source Data, not in the artwork.
- **Source:** `manuscript/source_data/Fig_R581_matched_closure/R581_plot_matched_closure.py`; `R581_release_closure_comparison.csv`; `R581_true_mesh_control_timeseries.csv`; `R581_true_mesh_physical_timeseries.csv`; `Fig_R581_matched_closure_threshold_definitions.csv`; `Fig_R581_matched_closure_endpoint_summary.csv`.

### Current Fig. 6 -- Molecular priors

- **Verdict:** **SPLIT + MOVE MOST DETAIL TO SI**; retain only two compact prior panels in new Fig. 5 if the multiscale claim remains central.
- **Single claim:** molecular calculations bound where I2 is preferentially retained and how slowly oxidized iodine carriers move; they do not supply reaction rates or a morphology.
- **Current panel roles:** a DFT site ordering; b two single-point cluster proxies; c MD diffusivity ladder.
- **15-second failure:** the 345.5-mm-wide native canvas is reduced to about 47% in the manuscript. Three unrelated x scales and three long panel subtitles create a poster strip. The cluster proxy is visually equal to the better-supported DFT and MD results. The viewer must read multiple disclaimers to know that the values are not free energies.
- **Specific redesign:** new Fig. 5a is a four-site lollipop or compact horizontal interval plot, with basal as the visible reference and one line `relative electronic energies`. New Fig. 5b shows only I-, I3-, and I2Br- as direct points with the stated within-trajectory stability bars and a shaded adopted Deff range. Move the Br-/I2 and I-/I2 cluster proxy entirely to SI; it is not necessary to the main positive-electrode argument and risks making Br- look central.
- **Source:** `manuscript/source_data/Fig_R554_molecular_priors/R554_molecular_priors.py`; `R554_molecular_prior_values.csv`; `R197_FigS_md_carrier_diffusivity_source_summary.csv`.

### Current Fig. 7 -- Physical mesoscale bounds

- **Verdict:** **KEEP THE DATA + MERGE + REDRAW** into new Fig. 5.
- **Single claim:** physically plausible deposit placement strongly changes accessibility, whereas smooth bulk permeability remains near unity over the production loading range.
- **Current panel roles:** a isolated-island accessibility families; b pore-network permeability families; c placement-overlap ranking.
- **15-second failure:** panel a uses a log x axis with many vertical thresholds and tiny labels; panel b spends most of its width far outside the production regime; panel c is an unexplained dimensionless ranking whose darkest bar attracts more attention than the mechanistic curves. The long headline again reads like a rebuttal.
- **Specific redesign:** new Fig. 5c shows accessible area versus retained-solid fraction with the production trajectory range as a pale vertical band and only sparse/dense physical limits. New Fig. 5d shows the permeability response with the production range enlarged as the main axis and the full 0--0.4 range as a small inset. Move the placement-overlap bar to SI or replace it with two directly labeled limiting geometries; do not headline an arbitrary overlap score.
- **Source:** `manuscript/source_data/Fig_R555_mesoscale_closures/R555_mesoscale_closures.py`; panel tables `R581_Fig_R555_panel_a_theta_island_source_data.csv`, `R581_Fig_R555_panel_b_permeability_source_data.csv`, and `R581_Fig_R555_panel_c_overlap_source_data.csv`; registered inputs `R531_fiber3d_accessibility_closure.csv`, `R531_network3d_curves.csv`, `R534_film_onset.csv`, `R530_retained_vs_blocking_efficiency.csv`.

### Current Fig. 8 -- J--Q organizing map

- **Verdict:** **DROP THE CURRENT COMPOSITION; REDRAW SELECTED ELEMENTS** into new Fig. 6. Move the external literature markers to SI.
- **Single claim worth preserving:** higher current advances the modeled saturation marker, and the boundary remains conditional on sparse solved anchors.
- **Current panel roles:** the left plot combines two solved saturation points, interpolation/extrapolation, and a one-anchor accessibility projection; the right rail shows unrelated literature dissolution scales.
- **15-second failure:** dashed extrapolations cover more visual territory than solved evidence, the one-anchor calibrated boundary looks like a real solved curve, and the literature rail invites direct comparison despite having no Q coordinate and different concentration/method conditions. The caveat box is needed precisely because the composition is misleading.
- **Specific redesign:** new Fig. 6 should lead with solved response curves, not a pseudo-phase diagram. Panel a shows `Q_s` versus current using only verified solved points with markers; any interpolation is a thin segment strictly between anchors. Panel b shows `Q_s` versus Deff/D0 from the validated sweep. Panel c shows standardized marker shifts by lever with marker shape encoding evidence class (solved, analytical, bounded prior), rather than one bar scale pretending all ranges are commensurate. If the J--Q view is retained, show only solved anchors and a lightly shaded interpolation envelope; no one-anchor `J_b,cal` curve. The Zhao dissolution values become a separate SI context plot or table.
- **Source:** `manuscript/source_data/Fig_R581_jq_map/R581_jq_map.py`; `R581_jq_map_anchors.csv`; `R581_jq_map_external_markers.csv`; `R581_jq_map_curve_source.csv`; `R581_jq_map_derived_parameters.csv`. Candidate lever sources requiring evidence-class preservation: `mix/data/R565_sensitivity.csv`, `mix/data/R560_phase_plane.csv`, and `mix/R528_COMSOL_manuscript/figure_source_data/Fig8_knob_sensitivity_ranked.csv`.

### Current Fig. 9 -- Analytical flow-dependent boundary-layer scenario

- **Verdict:** **MOVE TO SI + REDRAW**. It is not a main result.
- **Single claim:** within the declared Sherwood scenario, flow moves the saturation marker less than rate or Deff.
- **Current panel roles:** a analytical flow-response family; b range-span comparison.
- **15-second failure:** the 259.5-mm canvas is reduced to about 59%; the bar chart compares ranges generated by different assumptions and therefore looks more quantitative than the evidence warrants. A hypothetical sub-grid correlation occupies the final main-figure slot and dilutes the positive-electrode result.
- **Specific redesign:** retain only panel a as a compact SI robustness plot with the operating window shaded and the analytical status in the caption. Replace panel b with a small evidence-class table, or include it only in new Fig. 6 if range definitions are normalized and explicitly comparable.
- **Source:** `manuscript/source_data/Fig_R577_flow_delta/R577_flow_delta_sweep.py`; `R577_baseline_input.csv`; `R577_flow_delta_sweep.csv`.

## Current supplementary figures: figure-by-figure verdicts

### Supplementary Fig. S1 -- Periodic single-I2 DFT

- **Verdict:** **KEEP THE EVIDENCE + SPLIT + REDRAW** into two quieter SI figures or one figure with a clear quantitative hero.
- **Single claim:** within the finite-cell calculation, oxygenated sites are preferred over the basal/vacancy cases.
- **Current panel roles:** a adsorption-energy ranking; b optimized geometries; c charge-density differences; d projected DOS and I-weight summary.
- **15-second failure:** four modalities have equal visual weight, panel letters and type sizes vary, molecular labels inside imported images are rasterized and very small, and the energy bar is separated from the structures needed to interpret it. The reader sees a collage before seeing a site-ordering result.
- **Specific redesign:** S1a is the energy ranking as the hero (about 55% of the page); S1b aligns four optimized structures in the same order and scale. Put CDD and PDOS in a second figure with identical site colors, two large CDD panels, one shared legend, and one compact PDOS axis. Remove the bottom disclaimer strip and keep the 150-Ry limitation in the caption.
- **Source:** `manuscript/source_data/Fig_SI_DFT_priors/make_si_dft_figures_no_dup.py`; `SOURCE_MANIFEST.csv`; copied calculation/geometry inputs under `outputs/`; current masters under `figures/SIFig_DFT_4panel.*`.

### Supplementary Fig. S2 -- Two-I2 coalescence diagnostic

- **Verdict:** **REDRAW; DROP CURRENT PANEL c**.
- **Single claim:** the compact two-I2 C-OH configuration is lower in registered electronic energy than the separated reference within this finite-cell setup.
- **Current panel roles:** a energy comparison; b CDD geometry; c a speculative association cartoon.
- **15-second failure:** panel c looks like a demonstrated mechanism even though the text repeatedly calls it only a possible motif. The large arrow sequence overstates temporal causality, and the hatched C=O bar competes with the only fully supported C-OH comparison.
- **Specific redesign:** two-panel SI figure. Left: energy comparison with the D3-only C=O point visibly separated as incomplete/supporting. Right: the compact C-OH geometry and CDD at legible scale. Replace the mechanism cartoon with one caption sentence: the calculation does not provide a nucleation pathway or solution free energy.
- **Source:** same DFT source bundle and renderer as S1; current masters `manuscript/source_data/Fig_SI_DFT_priors/figures/SIFig_DFT_2I2_mechanism.*`.

### Supplementary Fig. S3 -- Accessibility--coefficient degeneracy

- **Verdict:** **PROMOTE THE KEY PANEL + REDRAW** as new Fig. 4d; keep the full sensitivity version in SI.
- **Single claim:** similar voltage traces can be obtained across a broad accessibility range by compensating with the effective slope coefficient.
- **Current panel roles:** a selected full-cell voltage and reduced fit; b coefficient versus endpoint accessibility.
- **15-second failure:** the central identifiability curve is visually clean, but the 276.5-mm canvas is shrunk to about 55%, and panel a carries a large legend and an endpoint line that obscure the modest fit mismatch. The title states the conclusion more strongly than the plotted conditional calculation alone.
- **Specific redesign:** in the main closure figure, use only a compact normalized degeneracy curve with the production and dense-shadow endpoints directly labeled. In SI, retain the full V(Q) trace plus residual beneath it and state the fitted window. Avoid the shaded `illustrative coefficient` band unless its bounds have a source.
- **Source:** `manuscript/source_data/Fig_R538_voltage_reanchor/R538_voltage_reanchor.py`; `representative_vq_profiles_for_article.csv`; `R532_voltage_closure.csv`; `R538_coverage_tafel_degeneracy.csv`; `R538_reanchor_summary.csv`.

### Supplementary Fig. S4 -- Conditional internal-overpotential decomposition

- **Verdict:** **DROP AS A FIGURE**; preserve the numerical output as a table or one compact SI control panel only if cited.
- **Single claim:** within this parameterization, the modeled electronic/contact drop exceeds the ionic drop and varies with thickness.
- **Current panel roles:** a stacked internal drops plus cell voltage on a secondary axis; b through-plane electronic-drop profiles.
- **15-second failure:** the dual-axis stacked bar/line panel visually invites a causal comparison between quantities on different axes. The right panel's curves terminate at different thicknesses, so their endpoints appear shifted horizontally as well as vertically. This is a conditional internal decomposition, not experimental evidence, and does not earn a full visual.
- **Specific redesign:** one SI table with thickness, ionic drop, electronic/contact drop, and cell voltage, plus a small normalized through-plane profile if needed. No dual y axis. If retained graphically, normalize x by each felt thickness so all profiles run from collector 0 to separator 1.
- **Source:** `manuscript/source_data/Fig_R537_eta_internal/R537_eta_analysis.py`; `R537_eta_export_raw.txt`; `R537_eta_internal.csv`; `R537_compression_integrated.csv`.

### Supplementary Fig. S5 -- Pore-network permeability injection

- **Verdict:** **KEEP IN SI + REDRAW COMPACTLY**.
- **Single claim:** substituting the smooth pore-network permeability closure changes the modeled endpoint voltage by only about 1.3 mV in this branch.
- **Current panel roles:** a overlapping V(Q) traces with a DeltaV inset; b relative permeability versus capacity.
- **15-second failure:** the two 276-mm panels are reduced to roughly 54%, while most of the first panel shows indistinguishable lines. The inset carries the actual result but is too small. The phrase `barely moves V` is informal and stronger than the conditional scope.
- **Specific redesign:** one compact SI panel: plot DeltaV(Q) as the hero and place the two K/K0 trajectories in a small adjacent axis. State the endpoint voltage and permeability values directly. The overlaid raw V(Q) lines can be omitted because they add no visible information.
- **Source:** `manuscript/source_data/Fig_R537_kperm_injection/R537_kperm_analysis.py`; `R537_kperm_inject_raw.txt`; `R537_kperm_injection.csv`.

### Supplementary Fig. S6 -- Existing experimental evidence

- **Verdict:** **SPLIT; PROMOTE PANELS b/d AND A REPRESENTATIVE V(Q) TRACE TO NEW FIG. 1; KEEP PANELS a/c IN SI**.
- **Single claim after split:** the existing full-cell records provide descriptive rate and feature-ordering stress tests, not independent threshold validation.
- **Current panel roles:** a composition/capacity summaries; b same-cell rate ladder plus separate markers; c thickness command brackets; d derivative-feature ordering.
- **15-second failure:** four different questions share a 2 by 2 grid, tiny footnotes encode crucial independence/proxy rules, and sparse n=1 condition points look like population trends. Because the only experimental figure is in SI, the main paper appears detached from the battery data it seeks to explain.
- **Specific redesign:** new Fig. 1 uses a representative full-cell V(Q) trace with aligned dV/dQ as the hero, the same-cell pristine CE rate ladder as a supporting panel, and the four-cycle onset/peak timing strip as a third panel. The composition series and thickness brackets remain separate SI figures because they are sparse, source-specific, and potentially misleading when connected. Never make NH4Br concentration the opening visual; it is a supporting-electrolyte boundary condition. Preserve physical-cell n, within-cell ranges, unconnected proxy markers, and `EXP-META-001` in the caption/source data.
- **Source:** `manuscript/source_data/Fig_R581_experimental_evidence/R581_experimental_evidence.py`; the four `R581_experimental_evidence_panel_*.csv` tables; `R581_experimental_evidence_input_manifest.csv`. Representative voltage source also exists at `manuscript/source_data/Fig_R538_voltage_reanchor/representative_vq_profiles_for_article.csv`.

### Supplementary Fig. S7 -- Negative-electrode CDR scenario

- **Verdict:** **DROP**.
- **Single claim:** under assumed cZn and diffusion-layer thickness, the selected current window lies below an illustrative zinc diffusion limit.
- **Current panel roles:** one scenario line, two selected-window points, one high-current point, and an assumed limit.
- **15-second failure:** the plot looks authoritative although every crucial quantity is assumed. It directs reviewer attention to the negative electrode and dendrites, which the model does not solve. A long caption is then required to retract the apparent claim.
- **Specific redesign:** replace with one sentence or a small scope table in SI. If retained for reviewer response, label it `illustrative calculation` and do not number it as a manuscript figure.
- **Source:** `manuscript/source_data/Fig_R563_cdr_minicalc/R563_cdr_minicalc.py`; `R563_cdr_minicalc_source.csv`.

### Supplementary Fig. S8 -- Two-dimensional production-model fields

- **Verdict:** **PROMOTE + REDRAW** as new main Fig. 3; keep extended variables/capacities in SI.
- **Single claim:** solid retention and accessible-area loss develop preferentially near the separator-facing side and are accompanied by reaction-current redistribution as charge proceeds.
- **Current panel roles:** four variable rows (`S`, `eps_s`, `theta_cal`, total j) across three capacities.
- **15-second failure:** this is the right evidence but the wrong composition. A 180 by 220 mm page is reduced to about 142 mm in SI; 5.5-pt ticks become roughly 4.3 pt. Twelve equally sized maps, four colorbars, rotated row labels, repeated axes, and a bottom disclaimer make the key spatial pattern look like a contact sheet. Accessibility is plotted as `loss`, so darker means worse; the reader must mentally invert it.
- **Specific redesign:** new main Fig. 3 uses three capacities and three causal rows: retained solid, remaining bare-area fraction, and total current density. A thin top state clock supplies saturation context. Extended S maps, Q=96/110 slices, permeability/velocity, and separate bare/native current maps go to SI. Use common scales across Q within each row, one colorbar per row, one collector/separator annotation, and one flow arrow. Add a direct bracket over the separator-facing region where the change initiates; do not call it a blocking front.
- **Source:** same R545 field bundle as current Fig. 4. For optional current partition, use the canonical R581 partial-current export, not the superseded R534 table.

### Supplementary Fig. S9 -- Mesoscale model geometries

- **Verdict:** **KEEP IN SI + REDRAW AS EXPLANATORY SLICES**, not dense 3D hairballs.
- **Single claim:** the single-fibre and pore-network calculations use explicit assumed geometries that define physical comparator families.
- **Current panel roles:** a isolated-island fibre surface; b full 3D pore-throat network.
- **15-second failure:** the black/yellow fibre texture and thousands of colored network segments are visually impenetrable. The views look like noisy simulation screenshots, not diagrams that explain an assumption. Axis ticks and 3D perspective add no useful information.
- **Specific redesign:** show one clean fibre cross-section with island radius/coverage definitions and one 2D network slice with pores, throats, and blocked throats directly labeled. Place a small scalar summary beside each (N or theta for the fibre; K/K0 for the network). Keep the full 3D renders only in the source bundle/gallery.
- **Source:** `manuscript/source_data/Fig_R556_mesoscale_renders/R556_mesoscale_renders.py`; `R531_fiber3d_morphology.npz`; `R531_network3d_field.npz`; `R556_input_manifest.csv`.

## Proposed six-main-figure architecture

The six figures below form one linear argument. If one is removed, a distinct evidentiary step disappears; no figure exists only to document project plumbing.

### New Fig. 1 | Existing full-cell records define the positive-electrode problem

**Core conclusion:** the available full-cell records show a late-charge voltage feature and rate-dependent utilization that motivate, but do not independently validate, a positive-electrode state model.

**Archetype:** asymmetric mixed-modality figure. **Final size:** 180 by about 115 mm.

**Panel map and roles**

- **a, methodological bridge:** a minimal cell strip that highlights the positive carbon felt; no electrolyte-composition hero treatment.
- **b, hero evidence:** selected V(Q) trace with aligned dV/dQ beneath it, showing the observed late-charge feature without fitting a morphology.
- **c, validation under a new regime:** same-cell pristine CE rate ladder; separate 40 and 400 mA cm^-2 sources remain visually unconnected.
- **d, case illustration:** four-cycle onset-to-peak timing strips against the prospective model markers.

**Evidence hierarchy:** b is the observed symptom; c establishes rate sensitivity; d tests only ordering. Composition and thickness series are SI robustness/context.

**Legend logic:** define the physical cell/file as n, distinguish within-cell cycles from independent cells, state error bars as full within-cell ranges, identify unconnected proxies, and record `EXP-META-001`. Do not use validation language.

**Matching Results topic sentence:** `Existing full-cell records locate a reproducible late-charge symptom but do not identify its positive-electrode state variable.`

**Reviewer risk:** full-cell data cannot isolate the positive electrode; n is mostly one cell per source. The figure must be framed as motivation and stress testing.

### New Fig. 2 | A state-resolved positive-electrode model separates saturation, retained solid and accessible area

**Core conclusion:** the model resolves a 2D positive-electrode domain and deliberately separates free-I2 saturation, retained-solid inventory, accessible area, and voltage response.

**Archetype:** schematic-led composite. **Final size:** 180 by about 105 mm.

**Panel map and roles**

- **a, system definition:** clean cell/domain cross-section with x/y coordinates and flow direction.
- **b, methodological bridge:** four-node causal chain `S -> eps_s -> A_bare/A0 -> V`, with the calibration entering only the accessibility node.
- **c, definition:** capacity clock marking `Q_s` and `Q_f,cal`, plus the local-versus-average distinction.

**Evidence hierarchy:** a defines where fields live; b defines what is solved versus calibrated; c defines what later figures measure. DFT, MD, single-fibre, and pore-network provenance move to SI or new Fig. 5.

**Legend logic:** one sentence per panel. One final boundary sentence says that the schematic is not deposit morphology. Do not repeat this warning inside every node.

**Matching Results topic sentence:** `The model converts charge passed into three distinct positive-electrode states rather than treating voltage rise as a direct image of deposition.`

**Reviewer risk:** pseudo-particles or a film-shaped gradient would imply morphology. Use fields/contours only.

### New Fig. 3 | Retained solid localizes near the separator as accessible area collapses and current redistributes

**Core conclusion:** across the registered production trajectory, separator-facing solid retention precedes a local loss of bare area and a redistribution of reaction current.

**Archetype:** quantitative spatial plate with one hero row. **Final size:** 180 by about 145--155 mm.

**Panel map and roles**

- **a, definition:** thin capacity clock with snapshot columns at Q=80, 100, and 120 mAh cm^-2 and the exact Qs/Qf,cal marker positions.
- **b, mechanism/localization:** x--y retained-solid maps at the three exported capacities.
- **c, functional consequence:** x--y remaining bare-area fraction maps on the same columns.
- **d, functional readout:** x--y total current-density maps; optionally add a restrained contour/inset for the native-solid current share from the canonical partial-current export.

**Evidence hierarchy:** b is the hero spatial evidence; c links inventory to accessibility; d links accessibility to current. The smooth S field and extra capacities remain SI.

**Scale rules:** common normalization across capacities within a row; explicit neutral mask for zeros; no per-panel autoscaling. Use `Q=100 approximately Q_f,cal`, not equality. Use one colorbar per row. If a signed current field is plotted, use a disclosed symlog rule; if magnitude is plotted, say `magnitude`.

**Source-data requirement:** copy the canonical R581 partial-current CSV and hash into the new figure bundle if it is used. Do not mix the superseded 2,556-node R534 spatial table with the 5,995-node registered field grid.

**Legend logic:** first sentence states the result; subsequent clauses define axes, shared scales, and the three snapshot capacities. One final sentence states that fields are model outputs and no front/morphology is identified.

**Matching Results topic sentence:** `Two-dimensional fields reveal where the modeled state changes, whereas an electrode average reveals only when it changes.`

**Reviewer risk:** the fields are largely through-plane dominated; do not inflate subtle y variation through per-snapshot normalization or smoothing.

### New Fig. 4 | Accessibility closure controls the late trajectory but is not identified by voltage

**Core conclusion:** matched solves preserve the saturation time but diverge strongly in late accessibility, solid inventory, and voltage, while the observation layer remains non-identifiable.

**Archetype:** asymmetric quantitative grid. **Final size:** 180 by about 120 mm.

**Panel map and roles**

- **a, comparison:** production, one-way shadow, and coupled-dense accessible-area trajectories.
- **b, hero evidence:** matched voltage response and DeltaV, with the endpoint difference directly labeled.
- **c, mechanism consequence:** branch-specific retained-solid trajectories with only the production midpoint and dense-island reference.
- **d, limitation:** coefficient--accessibility degeneracy curve.

**Evidence hierarchy:** b demonstrates consequence; a/c show how the consequence emerges; d prevents morphology over-interpretation.

**Legend logic:** include mesh, tolerance, and one-parameter-change statement once. Keep hashes and exact software route in Source Data/Methods. State `closure sensitivity`, never `morphology validation`.

**Matching Results topic sentence:** `A change in accessibility law leaves saturation nearly fixed yet changes the coupled late-voltage trajectory by 288 mV.`

**Reviewer risk:** the production branch is voltage-calibrated, so apparent agreement with voltage is not independent validation.

### New Fig. 5 | Independent calculations bound transport and physical closure families

**Core conclusion:** lower-scale calculations constrain placement, carrier mobility, accessibility families, and permeability, but none determines the calibrated production closure.

**Archetype:** quantitative 2 by 2 grid. **Final size:** 180 by about 125 mm.

**Panel map and roles**

- **a, bounded prior:** relative single-I2 site-energy ordering.
- **b, bounded prior:** I-, I3-, and I2Br- diffusivity points plus adopted Deff band.
- **c, physical comparator:** sparse/dense accessible-area families with the production retained-solid range shaded.
- **d, physical comparator:** pore-network K/K0 enlarged over the production range, with the full range inset.

**Evidence hierarchy:** c/d connect directly to the closure problem; a/b explain why placement and transport ranges were tested. Cluster proxies, structures, CDD, PDOS, full carrier ladder, and geometry renders remain SI.

**Legend logic:** define electronic energy versus free energy, within-trajectory bars versus replicate SEM, and physical comparator versus production calibration. NH4Br appears only as the MD baseline condition.

**Matching Results topic sentence:** `Independent molecular and mesoscale calculations bound the model inputs without supplying a parameter-free accessibility law.`

**Reviewer risk:** DFT cutoff and single-trajectory MD support tendencies/ranges only; the visual hierarchy must not imply precise thermodynamics.

### New Fig. 6 | Transport and operating levers shift the modeled saturation window

**Core conclusion:** applied current and oxidized-carrier diffusivity exert the clearest modeled leverage on the saturation marker, whereas smooth permeability and the declared flow scenario are weaker channels.

**Archetype:** quantitative grid with a compact decision summary. **Final size:** 180 by about 115 mm.

**Panel map and roles**

- **a, solved response:** Qs versus applied current, using solved markers and interpolation only between them.
- **b, solved response:** Qs versus Deff/D0 with the registered baseline marked.
- **c, ranking:** standardized marker shifts by lever; marker shape/line style encodes solved, analytical, or bounded-prior evidence rather than hiding those differences.
- **d, translational consequence:** three-node design map linking each controllable lever to inventory stress, generation stress, or accessibility. Keep it minimal and subordinate to the quantitative panels.

**Evidence hierarchy:** a/b are the quantitative hero evidence; c compares leverage without claiming equal uncertainty; d translates the mechanism. The sparse J--Q extrapolation and Zhao literature rail move to SI.

**Legend logic:** list perturbation ranges, reference values, evidence class, and whether each sweep was a full solve or postprocess. Do not call any boundary a demonstrated cell ceiling.

**Matching Results topic sentence:** `The modeled window is most sensitive to the generation-stress ratio J/Deff, not to smooth bulk permeability.`

**Reviewer risk:** old sensitivity tables mix fresh solves, inherited branches, analytical postprocesses, and priors. The new source bundle must retain evidence class visibly and exclude superseded branches.

## Main-versus-SI move map

| Current asset | New destination |
|---|---|
| Main Fig. 1 state cards | Merge into new Fig. 2b/c |
| Main Fig. 2 provenance | SI evidence-role table/diagram |
| Main Fig. 3 geometry | Redraw as new Fig. 2a |
| Main Fig. 4 x--Q maps | Compact SI summary; spatial data promoted to new Fig. 3 |
| Main Fig. 5 closure sensitivity | Redraw as new Fig. 4 |
| Main Fig. 6 molecular priors | Essential two panels in new Fig. 5; details SI |
| Main Fig. 7 mesoscale bounds | Essential two panels in new Fig. 5; details SI |
| Main Fig. 8 J--Q map | Replace with solved lever panels in new Fig. 6; literature rail SI |
| Main Fig. 9 flow scenario | SI robustness only |
| SI S1/S2 DFT detail | Redrawn SI figures |
| SI S3 degeneracy | Key panel in new Fig. 4; full analysis SI |
| SI S4 internal eta | Table or drop |
| SI S5 permeability injection | Compact SI control |
| SI S6 experimental evidence | b/d plus V(Q) promoted to new Fig. 1; a/c remain SI |
| SI S7 negative-electrode CDR | Drop |
| SI S8 2D fields | Redraw/promote to new Fig. 3 |
| SI S9 3D geometries | Redraw as 2D explanatory SI slices |

## Caption and Results synchronization rules

For every rebuilt main figure:

1. Write the one-sentence figure claim before plotting.
2. The Results subsection begins with the same claim in prose, then walks panels in evidence order rather than letter order if the hero panel is not a.
3. Caption title is a finding phrase, not `Overview of...` and not a disclaimer.
4. Panel descriptions use present tense and state what is plotted. Methods/how-generated clauses use past tense.
5. Put n, error definition, sweep type, and source-data identity in the caption. Put solver hashes and long caveats in Methods/Source Data.
6. One interpretation boundary at the end of the caption is enough. Repeating `not morphology` in the title, panel, footer, caption, and Results weakens rather than strengthens trust.
7. Aim for roughly 70--110 words per main caption. If a caption needs 150 words, the figure probably still has too many jobs.

## Priority order for rebuilding

1. **P0:** new Fig. 3 spatial plate from the registered 5,995-node exports. This answers the user's clearest readability complaint and uses evidence already present.
2. **P0:** new Fig. 1 from existing voltage/rate/feature data, with descriptive scope explicit. This fixes the absence of experimental motivation in the main paper.
3. **P0:** new Fig. 2 simplified domain/state schematic. Remove all pseudo-deposit particles and provenance spaghetti.
4. **P0:** new Fig. 4 closure/identifiability figure, with the -288.2 mV response as the hero.
5. **P1:** merge molecular and mesoscale bounds into new Fig. 5; split full detail into SI.
6. **P1:** replace J--Q extrapolation and main flow plot with evidence-class-aware lever figure 6.
7. **P1:** redraw SI S1/S2/S5/S9; delete S7 and convert S4 to a table.
8. **P2:** run final-size font, grayscale, color-vision, editable-text, and caption/source-data QA; then re-render the complete PDFs and repeat the 15-second test on every figure page.

## Acceptance gates

The redesign is not complete until all of the following are true:

- A reader can state each main figure's conclusion after 15 seconds without reading the caption.
- Every main figure has one dominant claim and one visually dominant panel/evidence row.
- The first main figure contains observed battery data, and the first spatial result is in the main paper.
- No main figure is primarily provenance, solver bookkeeping, or a hypothetical side scenario.
- No text is smaller than 6.5 pt at final placed size; panel labels are consistent.
- All text in SVG/PDF is editable except irreducible atomistic raster panels, which are explicitly inventoried.
- Every quantitative panel traces to a clean CSV/NPZ and deterministic Python script in a new source-data bundle.
- The same variable/category keeps the same color across the manuscript.
- Shared color scales are used for comparisons across capacity; zero/negative handling is explicit.
- Model fields are never described as images, fronts, films, or morphologies.
- NH4Br is visible only where it defines the representative electrolyte condition or a descriptive SI comparison.
- The main figure count is six (acceptable range five to seven), with the current 9-figure audit-report cadence removed.

## Bottom line

The paper does not need more decorative mechanism art. It needs fewer claims per page, earlier experimental motivation, and one visually decisive spatial figure. The existing registered exports already support that change. The current 2D maps should be promoted and rebuilt; the current abstract mechanism cards, provenance spaghetti, extrapolation-heavy operating map, analytical flow headline, and negative-electrode scenario should not survive as main-paper figures.
