# R582 Figure 3 v2 contract

Core conclusion: Immediately after the mean-saturation marker, retained solid accumulates and calibrated bare accessibility collapses from the separator side while the total reaction-current field redistributes across the positive electrode.

Figure archetype: quantitative spatial-field grid led by a thin capacity trajectory.

Target/output: final-main-figure candidate; 180 mm wide and no more than 155 mm high; Python/matplotlib only; editable SVG text; embedded PDF TrueType fonts; 300 dpi PNG; opaque RGB 600 dpi TIFF.

## Visual argument

- **Capacity clock:** exported snapshots at 80, 100, and 120 mAh cm^-2 are located relative to the exact positive-electrode mean-saturation marker `Q_s = 83.0202 mAh cm^-2` and calibrated half-accessibility marker `Q_f,cal = 99.5901 mAh cm^-2`. The 100 mAh cm^-2 snapshot is explicitly identified as approximately `Q_f,cal`.
- **Row 1, retained-solid state:** `eps_s_pos` shown as retained solid fraction `eps_s`.
- **Row 2, intuitive accessibility direction:** `A_bare/A0 = 1 - theta_cal`, derived exactly from `theta_eff` so that high values mean more remaining accessible bare area.
- **Row 3, independent electrochemical readout:** signed `j_total_A_m2`. Positive values are shown on one shared logarithmic scale; all nonpositive values are retained as a neutral mask rather than clipped, absolutized, or discarded.

## Stage labels

- 80 mAh cm^-2: **before mean-saturation marker**.
- 100 mAh cm^-2: **near calibrated half-accessibility marker**.
- 120 mAh cm^-2: **late charge**.

## Scale contract

- `eps_s`: one symmetric-log scale shared by all three capacities, displayed in percent; linear threshold `0.001%`, range `0-6%`.
- `A_bare/A0`: one linear `0-1` scale shared by all three capacities.
- positive `j_total`: one logarithmic scale shared by all three capacities, `8e-5` to `2.2e4 A m^-2`.
- signed-current handling: six nodes at Q=100 have `j_total <= 0` (all six are negative); no nonpositive nodes occur at Q=80 or Q=120. These six nodes are plotted in neutral grey and stated directly below the matrix.
- Each map displays the sampled 55 x 109 grid without interpolation. The panel aspect is expanded for reading and is not a physical-shape rendering.

## Source-data and semantic integrity

- Sole spatial-field input: `../Fig_R545_fields/Fig3_baseline_spatial_long.csv`.
- Required SHA-256: `E322D0D0C4B0D5C8CB84BD5CB18D1A43CBA183EB8A5F112577686993BC8FC007`.
- Selected source rows: 17,985, comprising 5,995 nodes at each displayed capacity.
- `A_bare_over_A0` is generated as `1 - theta_eff`. The exported native column `A_bare_frac` is retained beside it in the v2 source subset for audit. They differ by at most `6.47152905e-4`; v2 does not silently substitute or conflate them.
- `Q_s` and `Q_f,cal` are declared production-anchor values supplied by the model audit; they are not estimated from the three displayed snapshots.
- No smoothing, interpolation, clipping, absolute-value transformation, synthetic data, or local image adjustment is used.
- These are continuum-model spatial fields, not microscopy, deposit morphology, or a pore-blocking front.

## Panel-economy decision

The v1 flow-averaged profile remains useful as an alternative, but v2 omits a companion profile. The intuitive `1-theta_cal` row already exposes separator-facing accessibility depletion within the 15-second reading path, and omitting the profile keeps the final page below 155 mm high.

## Draft legend

**Fig. 3 | Spatial progression of retained solid, remaining accessibility and reaction-current redistribution.** The capacity trajectory locates the modeled snapshots relative to the positive-electrode mean-saturation marker (`Q_s = 83.0202 mAh cm^-2`) and calibrated half-accessibility marker (`Q_f,cal = 99.5901 mAh cm^-2`). Columns show 80, 100 and 120 mAh cm^-2; the 100 mAh cm^-2 snapshot is approximately `Q_f,cal`. Rows show retained solid fraction (`eps_s`), remaining calibrated bare-area fraction (`A_bare/A0 = 1 - theta_cal`) and total reaction-current density (`j_total`). Each row uses one scale across capacities. `eps_s` uses a symmetric-log scale and positive `j_total` uses a logarithmic scale. Grey current cells retain the six nodes with `j_total <= 0` at 100 mAh cm^-2; no clipping or absolute-value transform is applied. The displayed quantities are continuum-model fields, not microscopy or inferred deposit morphology. Source data are provided with the figure.
