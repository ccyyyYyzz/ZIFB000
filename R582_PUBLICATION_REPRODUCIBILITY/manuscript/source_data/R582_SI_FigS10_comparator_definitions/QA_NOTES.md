# Figure S10 QA notes

Status: **PASS**, 2026-07-20.

## Scientific and source gates

- Four frozen inputs are byte-identical to their registered upstream objects; their SHA-256 values are recorded in `R582_SIFig_S10_input_manifest.csv`.
- The displayed fibre quantities are restricted to `r_f`, derived `r_out`, `L_z` and script-defined constants/boundaries.
- Panel b contains exactly 225 registered central-slice nodes and 420 exact in-slice throats. No node or throat was invented.
- Initial-radius line width is the only network field encoding. `phi`, `r_new` and `flux` are excluded.
- The registered fibre height/coverage arrays are excluded. No measured or inferred deposit morphology is drawn.
- Original data and scripts were not modified.

## Typography and export gates

- Resolved text family: TeX Gyre Termes only; minimum text size 6.5 pt.
- PDF fonts: `TeXGyreTermes-Regular`, `TeXGyreTermes-Italic` and `TeXGyreTermes-Bold`; no Type 3, Arial, Helvetica, DejaVu, Computer Modern, STIX or Times New Roman.
- SVG retains editable text nodes and declares TeX Gyre Termes.
- PDF size: 179.9999 × 103.9999 mm (target 180 × 104 mm).
- PNG/TIFF: 4252 × 2457 pixels at the 600-dpi contract; TIFF is opaque RGB.
- Colour/grayscale previews: 2126 × 1228 pixels at 300 dpi.
- Deterministic second render: all six outputs match byte-for-byte.

## Visual QA

- Inspected at the 180-mm preview size in colour and grayscale.
- The carbon fibre, electrolyte annulus, boundary faces, exact network connectivity and rule block remain distinguishable in grayscale.
- No label collision, clipping, missing-glyph placeholder or cross-panel scale ambiguity remains after the second layout pass.
- No generative artwork was used.

## Frozen master hashes

- SVG: `2ACE764008A1B3B2BAE9DD0654B31593580A68F6F2CD78CBCAF985A467C5549B`
- PDF: `1FE265E8E602ACE61792EA4F44979945DBECDA1B02B9A6F01A84C775990723A5`
- PNG: `8B5B12616C391A4122603B88F0FB27319CFA94C8E7CCBF241352010E16D9FF63`
- TIFF: `21628FF6A156CA89491C1CF8EEA07B23448E3D136C7E07D625D62B1C06D54C91`
