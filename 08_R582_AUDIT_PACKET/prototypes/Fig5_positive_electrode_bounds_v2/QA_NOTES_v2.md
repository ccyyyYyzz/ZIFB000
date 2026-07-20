# R582 Figure 5 v2 QA

Status: **passes source, hierarchy, collision, export, font, final-size,
grayscale and determinism gates**.

## Revision outcome

- Version 1 is preserved unchanged; its six figure assets retained their frozen
  SHA256 hashes after both v2 builds (`V1_PRESERVED=6/6`).
- The panel-a `+0.08` label was moved above the vacancy point and panels a/b now
  have a dedicated wide gutter. The value can no longer append visually to the
  panel-b `I2Br-` row label.
- Panels a/b form a quiet upper prior strip. Panels c/d form the enlarged
  positive-electrode hero row, with panel c as the widest panel.
- No scientific values, transforms or interpretation boundaries changed from
  v1.

## Build and determinism

- Renderer: `make_fig_r582_multiscale_bounds_v2.py`.
- Renderer SHA256:
  `A0F6110ED6E351A5BDEB63CC780950D9495C5D35310F1DD7A7D3207BFBDE3367`.
- Frozen v1 validation/drawing dependency SHA256:
  `89FD0810AC2F5CDC49F54B0C78F1B91526CAA934A5EFDCA30C77E318961294CD`.
- Backend: Python 3.11.5, matplotlib 3.7.2, pandas 1.5.3, numpy 1.24.4 and
  Pillow 12.2.0.
- Rebuild command:
  `D:\Anacondar\anaconda3\python.exe make_fig_r582_multiscale_bounds_v2.py`.
- Two consecutive builds produced identical hashes for all 14 generated source
  tables, manifests and outputs (`DETERMINISM_PASS=14/14`).

## Geometry and raster export

- Intended size: 180 x 125 mm.
- PDF page: 510.236 x 354.331 pt, equal to 180 x 125 mm.
- 300 dpi final-size preview: 2125 x 1476 px.
- SVG/PDF are vector masters; PNG is 600 dpi RGBA and TIFF is opaque RGB at
  600 dpi (4251 x 2952 px).
- Separate 300 dpi colour and grayscale final-size previews were visually
  inspected; all comparisons and labels remain legible without colour.

## Font and editability

- Exact TeX Live TeX Gyre Termes OTF files are registered for all text.
- Base size: 7.2 pt; minimum tick/legend/annotation size: 6.5 pt; panel labels:
  8.0 pt bold.
- PDF fonts: embedded/subset TeXGyreTermes-Regular, Bold and Italic, all
  Unicode CID OpenType; no Type 3 font.
- The repository font checker reports `pass: true` for the v2 PDF: required
  Termes present, no forbidden family and no Type 3 font.
- The repository-wide checker still exits 1 solely because the current
  `main.pdf` and `SI.pdf` contain legacy font violations; v2 is not among the
  failures.
- SVG: 65 editable text nodes, 0 raster image nodes and 92 explicit TeX Gyre
  Termes family declarations.
- Forbidden-family scan: 0 occurrences of Arial, Helvetica, DejaVu, Times New
  Roman, Liberation or Calibri.

## Visual QA

- The a/b inter-panel collision is absent in colour and grayscale at final size.
- The top strip reads as supporting priors; the lower row reads first and keeps
  the ZIFB positive electrode as the protagonist.
- Panel a retains basal carbon as the explicit zero reference.
- Panel b separates charge scaling by filled circle versus open diamond, and
  distinguishes the low-end prior band from the dashed continuum baseline.
- Panel c distinguishes placement families by marker shape as well as colour.
- Panel d magnifies the baseline permeability range while retaining a labelled
  full-network-range inset.
- No red/green-only encoding, rainbow map, 3D render, drop shadow or decorative
  mechanism art is present.

## Scientific-integrity QA

- DFT is labelled as a relative dry periodic electronic-energy placement prior,
  not a free energy, kinetic barrier, rate, population or value of N.
- MD values are force-field-limited bulk mobility priors. Error bars denote
  within-trajectory stability, not replicate SEM.
- NH4Br is identified only as the representative supporting-electrolyte
  condition; bromide is not promoted as the figure's subject.
- Sparse/dense lines connect computed single-fibre nodes; the sole added origin
  is the exact zero-solid boundary.
- Pore-network interpolation matches the registered R531 endpoint calculation;
  the inset uses raw nodes.
- No panel claims validation, observed morphology, microscopic coverage, a
  blocking front, pore-throat closure or electrical potential.
- No lower-scale panel supplies the voltage-calibrated continuum accessibility
  relation.

## Frozen v2 output hashes

| File | SHA256 |
|---|---|
| SVG | `6DE1F31C29B35F7D6390992CBD28E28417E571D893C0746DF011A306F3D78F05` |
| PDF | `3B1AC3E334E887A553F33A1F1E56C028008799F5C8D98AF00F38608F4F7EA8DC` |
| PNG | `EEA9A870A79D1009F092489E39A285EA9D0E54EB5EFBDA360F3F26E9317B79D9` |
| TIFF | `98BA5BAEBEF6716363EF3F637A78617FF42A9F57033D5CF059DC0F8E901D298F` |
| 180 mm preview | `C95312064ECBF4E333E4EF3FEE7D5C93C6A4AC8878B243E5C7CE56394A204C3B` |
| grayscale preview | `E7A272B850A797F7781AA5E86419D8F6B2135AC2E200747490DF79EA775C23F8` |

Input and source-table hashes are frozen in
`R582_Fig5_render_manifest_v2.json`.

