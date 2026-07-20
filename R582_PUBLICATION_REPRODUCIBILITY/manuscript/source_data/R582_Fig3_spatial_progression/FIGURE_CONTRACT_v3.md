# R582 Figure 3 v3 contract

Core conclusion: As charge progresses beyond the electrode-average saturation point, retained solid increases, the native remaining-area field falls most strongly near the separator, and the reaction-current field redistributes across the positive electrode.

Figure archetype: a quantitative 3 x 3 spatial-field plate led by a capacity rail and followed by one compact through-plane profile. Final size is 180 x 155 mm.

## Visual argument

- The capacity rail places exported snapshots at 80, 100 and 120 mAh cm^-2 relative to the exact model coordinates `Q_s = 83.0202 mAh cm^-2` and `Q_f,cal = 99.5901 mAh cm^-2`.
- Row 1 shows the exported retained-solid fraction, `eps_s_pos`.
- Row 2 shows the exported native remaining bare-area fraction, `A_bare_frac`, labelled `A_bare/A0`.
- Row 3 shows signed total reaction-current density, `j_total_A_m2`. Positive values share one logarithmic scale. The six negative nodes at Q=100 are retained as a neutral mask.
- The lower panel is the arithmetic mean of native `A_bare_frac` over the uniformly sampled flow coordinate `y`, plotted against the through-plane coordinate `x` for all three capacities.

## Semantic boundaries

- v3 does not replace native `A_bare_frac` with `1 - theta_eff`. Both quantities and their difference remain in the source bundle for audit; their maximum pointwise discrepancy is `6.47152905e-4`.
- The exact six negative values span `-5.71642984703e-4` to `-1.80419252671e-4 A m^-2`. They are neither clipped nor converted to magnitudes.
- The maps are direct continuum-model exports on a 55 x 109 grid. No interpolation, smoothing, morphology reconstruction, coverage inference or pore-blocking-front claim is permitted.
- `Q_s` and `Q_f,cal` are registered production anchors, not estimates derived from the three displayed snapshots.

## Shared-scale contract

- retained solid: one 0--6% symmetric-logarithmic scale;
- remaining bare area: one linear 0--1 scale;
- positive reaction current: one logarithmic scale spanning the observed positive range;
- identical 3--5 mm through-plane and 0--20 mm flow domains in all maps.

## Typography and output contract

All visible text is rendered from the exact TeX Gyre Termes OTF files used by the manuscript's `tgtermes` body. No fallback family is allowed. Minimum visible type is 6.5 pt. Required outputs are editable-text SVG, embedded-font PDF, 300 dpi PNG, opaque 600 dpi TIFF, 180 mm review preview and grayscale QA image. Two consecutive renders must be byte-identical.

