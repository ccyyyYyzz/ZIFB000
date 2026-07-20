# R582 Supplementary Figure S13 QA

## Scientific and source checks

- Frozen input SHA-256 checks: **PASS** (2/2).
- Immutable text export parsed to 1081 ordered rows for each matched path.
- Capacity coordinates aligned exactly; raw-to-registered column checks:
  **PASS** within documented text-format precision.
- Maximum absolute voltage difference: 5.2144 mV at
  117.44444 mAh cm$^{-2}$.
- Endpoint voltage difference: +1.2710 mV at 120 mAh cm$^{-2}$.
- Endpoint $K/K_0$: 0.956287 (baseline Kozeny–Carman) and 0.982496
  (network-derived smooth path).
- Evidence boundary: deterministic `E-SIM`; smooth bulk permeability only, no
  local-blockage, morphology or electrical-potential inference.

## Typography and export checks

- Canvas: 180.000 × 70.000 mm (**PASS**).
- Minimum text: 6.5 pt (**PASS**).
- Resolved family: TeX Gyre Termes only (**PASS**).
- PDF fonts: TeXGyreTermes Regular/Bold/Italic; no forbidden family and no
  Type 3 (**PASS**).
- SVG editable text and no font fallback (**PASS**).
- PNG/TIFF: 4252 × 1654 px at 600 dpi (**PASS**).
- Actual-size colour/grayscale previews: 2126 × 827 px at 300 dpi (**PASS**).
- Second-render hashes: all six exported/preview files byte-identical (**PASS**).
- Accepted PDF SHA-256:
  `AEE930E0DE59779E3BEE25599527AB62FF1DF919058776F7EDEF8DC2D070E10C`.

## Visual inspection

Colour and grayscale previews were inspected at the exported 180 mm size.
The dominant $\Delta V$ trajectory, maximum and endpoint annotations are
legible. Solid/dashed line encoding separates the two smooth permeability paths
in grayscale, and all direct labels and panel labels are free of clipping.

