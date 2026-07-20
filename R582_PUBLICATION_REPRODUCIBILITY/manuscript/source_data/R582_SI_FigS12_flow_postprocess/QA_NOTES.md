# R582 Supplementary Figure S12 QA

## Scientific and source checks

- Frozen input SHA-256 checks: **PASS** (2/2).
- Registered baseline: 1081 ordered rows, one `baseline_J40_Q120` case.
- Registered analytical sweep: 120 rows, 40 for each of $m=0.4$, 0.5 and 0.6.
- Row-by-row reconstruction of $Q_s$, $\delta/\delta_0$, $\delta$ and
  $\Delta Q$: **PASS** (absolute tolerance $2\times10^{-10}$).
- Registered nominal point: $Q_s=83.020199$ mAh cm$^{-2}$ at
  50 mL min$^{-1}$.
- Declared primary range: 25–100 mL min$^{-1}$; for $m=0.5$,
  $Q_s=74.991523$–88.732903 mAh cm$^{-2}$.
- Evidence boundary: deterministic analytical `E-POST`; no new solve,
  measured-law or experimental claim.

## Typography and export checks

- Canvas: 180.000 × 68.000 mm (**PASS**).
- Minimum text: 6.5 pt (**PASS**).
- Resolved family: TeX Gyre Termes only (**PASS**).
- PDF fonts: TeXGyreTermes Regular/Bold/Italic; no forbidden family and no
  Type 3 (**PASS**).
- SVG editable text and no font fallback (**PASS**).
- PNG/TIFF: 4252 × 1606 px at 600 dpi (**PASS**).
- Actual-size colour/grayscale previews: 2126 × 803 px at 300 dpi (**PASS**).
- Second-render hashes: all six exported/preview files byte-identical (**PASS**).
- Accepted PDF SHA-256:
  `9DD4C93227FCB2081E7FBEA790968773466A2EA497F6A28D43DAA2D951307822`.

## Visual inspection

Colour and grayscale previews were inspected at the exported 180 mm size.
The shaded primary range, nominal anchor and all three direct labels are clear.
Deliberate line-style differences preserve curve identity in grayscale; labels
have leader lines and no collision or clipping.

