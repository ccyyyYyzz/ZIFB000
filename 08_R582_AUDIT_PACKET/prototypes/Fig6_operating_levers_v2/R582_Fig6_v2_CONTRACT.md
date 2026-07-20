# R582 Figure 6 v2 contract

## Core conclusion

Applied current and oxidized-carrier diffusivity produce the largest shifts in
the positive-electrode averaged saturation point over the declared simulated
ranges, while solved flow rate and the linked felt-geometry branch produce much
smaller shifts.

## Figure architecture

- Archetype: quantitative grid with an asymmetric full-width hero panel.
- Target: Journal of Power Sources main figure.
- Backend: Python/matplotlib exclusively for drawing, export, preview and QA.
- Final size: 180 x 115 mm.
- Typography: exact TeX Gyre Termes OpenType family for text and math; 7.2 pt
  base, 6.5 pt minimum and 8 pt bold panel labels.
- Export: editable SVG and PDF, 400 dpi PNG, opaque 600 dpi RGB TIFF, final-size
  color preview and grayscale QA preview.

## Panel map

- **a — current response:** observed `S_avg = 1` crossings from full continuum
  simulations. Only the 20–40 mA cm^-2 interval is connected. The 80 mA cm^-2
  trajectory is displayed as an unambiguous right-censored observation,
  `Q_s > 40 mAh cm^-2`; the 120 mA cm^-2 crossing remains a separate point.
- **b — diffusivity response:** seven converged continuum simulations of `Q_s`
  versus `D_eff/D_0`, with the MD-informed range shown as a quiet band.
- **c — full-width hero:** signed `Q_s` shifts on a common baseline coordinate,
  with marker and line style distinguishing continuum simulations, an
  analytical boundary-layer scenario and the MD-informed mapped range.

## Evidence hierarchy and exclusions

- Panel c is the quantitative synthesis and receives the full lower row.
- Panels a and b retain the solved anchors needed to interpret the synthesis.
- The former lever/node/consequence table is deleted; accessibility and smooth
  permeability remain outside this main figure because they use different
  response coordinates or serve explanatory rather than quantitative roles.
- No interpolation is drawn through the censored current observation. No fit or
  extrapolation is applied to the diffusivity sweep.

## Matching Results sentence

`Applied current and oxidized-carrier diffusivity shift the averaged saturation
point far more strongly than solved flow rate or the linked felt-geometry branch
over the tested ranges.`
