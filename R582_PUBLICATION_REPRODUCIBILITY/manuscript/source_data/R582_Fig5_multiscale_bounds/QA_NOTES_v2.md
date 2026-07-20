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
- Panel a now names the plotted quantity as a BSSE-corrected adsorption-energy
  ordering. Panel c now names the plotted single-fibre quantity as geometric
  $A/A_0$ and explicitly separates it from native COMSOL
  $A_{\mathrm{bare}}/A_0=R_{\theta}T_{\mathrm{pore}}$.
- No numeric value or numeric transform changed from v1. The scientific
  quantity identities and their interpretation boundary were corrected.

## Build and determinism

- Renderer: `make_fig_r582_multiscale_bounds_v2.py`.
- Renderer SHA256:
  `018C44532E28767F0D91177606138B1C6F6F5BEB221D57EB5551EAD7D64DAF40`.
- Frozen v1 validation/drawing dependency SHA256:
  `2EE1DF3D1FC2DED4418A663BED1A70C9BF2F450057C8AA7248E1FB47E74F631E`.
- Backend: Python 3.11.5, matplotlib 3.7.2, pandas 1.5.3, numpy 1.24.4 and
  Pillow 12.2.0.
- Rebuild command:
  `D:\Anacondar\anaconda3\python.exe make_fig_r582_multiscale_bounds_v2.py`.
- Two consecutive builds produced identical hashes for all 14 generated source
  tables, manifests and outputs; including the unchanged renderer in the audit
  gives `DETERMINISM_PASS=15/15`.

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
- Programmatic artist inspection resolves every visible text object to TeX Gyre
  Termes. Assigned sizes are 6.5, 7.2 and 8.0 pt: 7.2 pt base, 6.5 pt minimum
  and 8.0 pt bold panel labels.
- PDF fonts: embedded/subset TeXGyreTermes-Regular, Bold and Italic, all
  Unicode CID OpenType; no Type 3 font.
- SVG: 67 editable text nodes, 0 raster image nodes and 97 explicit TeX Gyre
  Termes family declarations.
- Forbidden-family scan: 0 occurrences of Arial, Helvetica, DejaVu, Times New
  Roman, Liberation or Calibri.

## Visual QA

- The a/b inter-panel collision is absent in colour and grayscale at final size.
- The top strip reads as supporting priors; the lower row reads first and keeps
  the ZIFB positive electrode as the protagonist.
- Panel a retains basal carbon as the explicit zero reference and identifies
  the ordering as BSSE-corrected adsorption energies.
- Panel b separates charge scaling by filled circle versus open diamond, and
  distinguishes the low-end prior band from the dashed continuum baseline.
- Panel c labels its axis as geometric $A/A_0$, distinguishes placement
  families by marker shape as well as colour, and carries a non-overlapping
  note separating it from native COMSOL $A_{\mathrm{bare}}/A_0$.
- Panel d magnifies the baseline permeability range while retaining a labelled
  full-network-range inset.
- No red/green-only encoding, rainbow map, 3D render, drop shadow or decorative
  mechanism art is present.

## Scientific-integrity QA

- DFT is labelled as a relative dry periodic BSSE-corrected adsorption-energy
  ordering, not a solution free energy, kinetic barrier, rate, population or
  value of N.
- MD values are force-field-limited bulk mobility priors. Error bars denote
  within-trajectory stability, not replicate SEM.
- NH4Br is identified only as the representative supporting-electrolyte
  condition; bromide is not promoted as the figure's subject.
- Sparse/dense lines connect computed single-fibre geometric-area nodes; the
  sole added origin is the exact zero-solid boundary. The publication source
  table `R582_Fig5_panel_c_geometric_area_families_v2.csv` uses
  `geometric_A_over_A0` and `geometric_removed_fraction`; all values match the
  legacy upstream complements exactly. The BSSE-qualified panel-a table is
  separately versioned as `R582_Fig5_panel_a_dft_site_ordering_v2.csv`.
- Pore-network interpolation matches the registered R531 endpoint calculation;
  the inset uses raw nodes.
- No panel claims validation, observed morphology, microscopic coverage, a
  blocking front, pore-throat closure or electrical potential.
- The active figure, caption, contract, provenance and render manifest all
  distinguish geometric $A/A_0$ from native COMSOL
  $A_{\mathrm{bare}}/A_0=R_{\theta}T_{\mathrm{pore}}$, with
  $R_{\theta}=1-\theta_{\mathrm{cal}}$ and
  $T_{\mathrm{pore}}=(K/K_0)^{1/2}$.
- No lower-scale panel supplies the voltage-calibrated $R_{\theta}$ relation.

## Frozen v2 output hashes

| File | SHA256 |
|---|---|
| SVG | `3F84E48B5D8BC00C6D2D5E83140F6926590BEC4D4FDC56470513A8802A9B0B38` |
| PDF | `9FD7827DAB7446688CA04C4818D2DE2EB54BA6A3670B87BD0D0273330C817491` |
| PNG | `65BCB3C99C1567454AB2F166A6E7EDF2BE1D14DD6ED63A475BF062FDF0623F8B` |
| TIFF | `97A2821BA2727111CA22D516CA7F1DDB624C22116A0484CA080F04692487FBC9` |
| 180 mm preview | `BA5BC6B0905DDD94A0F5CC805249796EC92B738C36307D1BCDD6B116F265FABF` |
| grayscale preview | `1270A028D289AF3C6DAEB2C1B1E50F67FB68E66E6B6BC3F109F85B334BFD3A49` |

Input and source-table hashes are frozen in
`R582_Fig5_render_manifest_v2.json`.
