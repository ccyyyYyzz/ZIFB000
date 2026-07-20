# Figure S11 QA notes

Status: **PASS**, 2026-07-20.

## Scientific and source gates

- Both frozen CSV inputs are byte-identical to their registered upstream sources; hashes are recorded in `R582_SIFig_S11_input_manifest.csv`.
- Four expected geometric families are present with five computed nodes each (20 total).
- Every closure node is cross-matched to the registered clock table by family and exact retained-solid fraction.
- Geometric `A/A0 + theta_eff_transport = 1` passes to an absolute tolerance of `2 × 10^-15`.
- Five exact shared-inventory geometric pairs are shown; no interpolation is used.
- The dashed values are verified as `R_theta = 1 - comsol_theta_ref` and labelled only as a comparator.
- Native COMSOL `A_bare/A0 = R_theta * T_pore` is explicitly not plotted because `T_pore` is absent from the S11 inventory.
- All registered numeric nodes are unchanged; only semantic labels and generated table headers were corrected.
- Original and frozen input data were not modified.

## Typography and export gates

- Resolved text family: TeX Gyre Termes only; minimum rendered text size is 6.5 pt.
- All non-ASCII figure glyphs are present in every registered TeX Gyre Termes face; no missing-glyph substitution is permitted.
- PDF fonts: `TeXGyreTermes-Regular` and `TeXGyreTermes-Bold`; no Type 3, Arial, Helvetica, DejaVu, Computer Modern, STIX or Times New Roman.
- SVG retains editable text nodes, declares TeX Gyre Termes and passes an explicit rendered-size scan with a 6.5-pt minimum.
- PDF size: 179.9999 × 96.0000 mm (target 180 × 96 mm).
- PNG/TIFF: 4252 × 2268 pixels at the 600-dpi contract; TIFF is opaque RGB.
- Colour/grayscale previews: 2126 × 1134 pixels at 300 dpi.
- Deterministic second render: all six outputs match byte-for-byte.

## Visual QA

- Inspected at the 180-mm preview size in colour and grayscale.
- Four family markers and line styles remain distinguishable without colour; the dashed `R_theta` comparator remains uniquely short-dashed.
- The geometric `A/A0` labels, `R_theta` comparator warning and native COMSOL product statement are visible without collision or clipping.
- The five exact paired comparisons and both legends remain readable; no missing-glyph placeholder is present.
- No generative artwork was used.

## Frozen master hashes

- SVG: `4393E2207C3C2B2CEC64522FA93BD45E9EB5FB250A0CCB48BC04B64F83389F31`
- PDF: `13BE70194D8CB1BED6E3E8DE40CD49B671ED69C4AC7B2F42BBD7009C518F6716`
- PNG: `33278BA55519AEABF1AE7E37749F0CFB60F05BC3926CEAAA77A3B397DD617CE4`
- TIFF: `12AB2C22BD96CAD97FF390AF68B8D0F7499BFFFE5E3BE13FFD15D0AF20444190`
- Colour preview: `3EE1522FEAC7C5BA32D956A4E85404B471CC5B0C0177B33059B7D4F2D9941E8F`
- Grayscale preview: `12309199752FBC4CB181B39B08C0435F52FD3E5C5B54A1B81AFBE8EC6007E649`
