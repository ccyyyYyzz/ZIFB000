# R582 main Figure 1 prototype: release QA

**Status:** PASS as an isolated figure/source-data prototype.  
**Figure:** `Fig_R582_experimental_problem`  
**Scope:** deterministic Python script, registered-input manifest, clean derived CSVs,
SVG/PDF/600-dpi TIFF/PNG and grayscale QA preview. No manuscript, SI, raw experimental file,
original analysis output or COMSOL file was modified.

## 1. Figure contract

**Core conclusion.** Existing full-cell records show a voltage-rise feature and rate-dependent
utilization that motivate, but do not independently validate, a positive-electrode state model.

**Archetype.** Asymmetric mixed-modality figure at exactly 180 x 115 mm.

**Evidence hierarchy.** Panel b is the hero observation. Panel c establishes the descriptive
rate dependence. Panel d tests feature ordering and estimator sensitivity. Panel a only locates
the positive carbon felt within the full-cell measurement.

**Panel map.**

- **a, methodological bridge:** a flat, not-to-scale cell strip highlights the positive felt.
  No particles, film, crystal morphology or supporting-electrolyte hero treatment is shown.
- **b, hero observation:** registered cycle-20 full-cell voltage and its registered derivative
  share one capacity axis. The thin grey trace is the raw-interpolated voltage; the dark trace is
  the cubic Savitzky-Golay smooth; amber is `dV/dQ`. The vertical model markers were not fitted to
  the trace.
- **c, supporting observation:** the line connects only the same-cell pristine 80--360
  mA cm^-2 ladder. The 40 mA cm^-2 pristine cell and 400 mA cm^-2 P350C-positive proxy use
  different shapes and remain unconnected.
- **d, ordering audit:** four cycles from one physical cell are shown separately. Circles and
  open triangles are the primary-window onset and maximum. Pale spans show the extrema across
  the three prespecified derivative windows; they are estimator-sensitivity ranges, not
  confidence intervals.

**Reviewer risk controlled.** These are full-cell observations, so they cannot isolate the
positive electrode. The model markers are prospective coordinates rather than fitted or
experimentally validated thresholds. No panel infers deposit morphology.

## 2. Derivative admissibility and alignment

The derivative was retained because a defensible registered source exists. It was not digitized
from a plot and was not reconstructed from a raster image.

- Physical file/cell: one registered pristine full-cell file; representative `pair_index = 20`.
- Frozen processing: interpolation to a 0.25 mAh cm^-2 grid followed by a cubic Savitzky-Golay
  derivative.
- Primary window: 10.25 mAh cm^-2 (41 grid points).
- Prespecified sensitivity windows: 5.25 and 15.25 mAh cm^-2.
- Registered primary features for cycle 20: onset at 52.0 and maximum at 95.0 mAh cm^-2.
- Exact displayed model markers: `Q_s = 83.0202` and `Q_f,cal = 99.5901 mAh cm^-2`.
- The registered sparse article V(Q) export and frozen derivative table have identical file and
  cycle identities. Linear cross-alignment gives a mean absolute voltage residual of 3.14 mV;
  the 37.9 mV maximum occurs where the sparse display trace undersamples rapid endpoint
  curvature. The plotted voltage and derivative therefore come together from the denser frozen
  processed table.

Primary-window onsets for cycles 20--23 are 52.00, 50.75, 51.75 and 89.25 mAh cm^-2;
maxima are 95.00, 92.00, 106.75 and 114.00 mAh cm^-2. Across all three windows, 11/12 onsets
precede `Q_s`, while maxima span 92.0--115.25 mAh cm^-2 and fall on both sides of `Q_f,cal`.
This is descriptive within one cell and cannot estimate between-cell reproducibility.

## 3. Statistical and independence QA

| Panel | Independent unit | Repeated observations | Displayed range | Inferential statistics |
|---|---|---|---|---|
| b | one physical cell/file | representative cycle 20 | none | none |
| c | one physical cell/file per source | 1--4 sequential cycles | full within-cell cycle min--max | none |
| d | one physical cell/file | four cycles, each under three windows | estimator-window extrema | none |

The 40 mA cm^-2 marker is a separate pristine capacity-limit cell. The 400 mA cm^-2 marker is
a P350C-positive/pristine-negative proxy. Neither is connected to the pristine 80--360
mA cm^-2 ladder. The latter ends above the prespecified 95% CE reference and is right-censored
with respect to a pristine rate-failure current.

## 4. Frozen source trace

| Registered input | SHA-256 | Figure role |
|---|---|---|
| `Fig_R538_voltage_reanchor/representative_vq_profiles_for_article.csv` | `150AFD09C0AE8FEE58A8DFE1CCC412378CB1F7893075F54BDFFD8DE0AED3D1F1` | representative trace identity and sparse-trace cross-check |
| `Fig_R581_experimental_evidence/R581_experimental_evidence_panel_b_rate.csv` | `9A30CDCA03BB870931AA0A8C91E8C7F0AE1265EA5FA71EAE5F2A5EDDA75BB517` | pristine ladder and separate markers |
| `Fig_R581_experimental_evidence/R581_experimental_evidence_panel_d_g4.csv` | `05E38C4702EFC34BF0AD2F5558D5CACC90808157C3AF8C46CED73F58F93C3AF7` | four-cycle feature metrics |
| `R581_G4_DVDQ_REBUILD/dvdq_curves_all_windows.csv` | `AAADD2779474FE74C1F0F4BC472633B113967905CA2BCE2EF97FAF8F0CA7D2DE` | frozen voltage/derivative curve |
| `Fig_R568_scale_provenance/R581_Fig_R568_scale_provenance_source_data.csv` | `4CB61A67545F55B5FEF66F91B420300030BA8B771BB38400B088C75B35E8106C` | exact model-marker coordinates |

The script rejects any input whose hash differs. The five public-facing clean tables contain
schematic vocabulary, 475 V(Q)/dV/dQ rows, 10 rate rows, 12 timing rows and the full input
manifest. Raw experimental filenames are not rewritten.

## 5. Typeface audit

The figure follows the manuscript's `tgtermes + newtxmath` Times family rather than a generic
sans-serif journal template.

- Matplotlib explicitly registers `texgyretermes-regular.otf`, `-bold.otf`, `-italic.otf` and
  `-bolditalic.otf`.
- Resolved text family: **TeX Gyre Termes**.
- Mathtext uses the same family for roman, italic, bold, calligraphic and sans slots, with fallback
  disabled.
- PDF font inventory: only `TeXGyreTermes-Regular`, `TeXGyreTermes-Italic` and
  `TeXGyreTermes-Bold`; all three are embedded, subsetted and Unicode mapped.
- SVG audit: 69 editable `<text>` nodes, zero embedded `<image>` nodes, and 81 explicit
  `TeX Gyre Termes` declarations. Searches return zero Arial, DejaVu and Times New Roman entries.
- Minimum displayed type is 6.5 pt; axis labels are 7.2 pt, titles 7.5 pt and panel letters
  8.2 pt bold at final size.

## 6. Export and visual QA

| Check | Result |
|---|---|
| Final vector size | SVG `510.236220 x 325.984252 pt`; PDF `510.236 x 325.984 pt` = 180 x 115 mm |
| Raster size | PNG/TIFF `4251 x 2716 px`, 600 dpi, RGBA; TIFF uses LZW compression |
| Editable text | PASS: SVG text retained; PDF text selectable and fonts embedded |
| Clipping/overlap | PASS after original-size inspection; no title, axis label, legend or annotation collision |
| Grayscale | PASS: model markers retain dash/dot coding; proxy roles retain connection and marker-shape coding; onset/maximum retain filled-circle/open-triangle coding; positive felt retains hatch coding |
| Color dependence | PASS: no comparison depends on hue alone and no red/green-only distinction is used |
| Decorative or unsupported morphology | PASS: flat cell strip only; no particles, films, pore blockage or crystal motifs |
| Supporting electrolyte hierarchy | PASS: NH4Br is absent from the artwork and remains only a representative-condition/data-provenance fact |

The final colored and grayscale PNGs were inspected at original resolution after the font rebuild.
The hero curve remains dominant, the four panel conclusions survive grayscale, and all text is
readable at the declared final dimensions.

## 7. Determinism and release hashes

Two consecutive final builds produced byte-identical SVG, PDF, PNG, TIFF, grayscale preview,
four clean panel CSVs, input manifest and build JSON.

| Deliverable | SHA-256 |
|---|---|
| `Fig_R582_experimental_problem.svg` | `B708363F4D9E6676954C958F95ABB2322CF9F7CE2052425A4D6F6606EEC608CF` |
| `Fig_R582_experimental_problem.pdf` | `5C22E28071F9BC1B5FBAAB62E38FB2628F6D3D22A69162E366E752E6C86A7E16` |
| `Fig_R582_experimental_problem.png` | `E5EC8B4F7D38656A5B320B592BDCB61D9A80DF6648A1E4E08151B9316A82F862` |
| `Fig_R582_experimental_problem.tiff` | `3EF4AECC79B8EB7A6BCF937E087B4AEA40196F964FA5D795A64C8F8DC5948F37` |
| `Fig_R582_experimental_problem_grayscale_QA.png` | `B00FB05E100AC5ED63BD0768BD012F7CE47A9B75C84FEC322479C9C676D3673B` |
| `R582_Fig1b_selected_vq_dvdq.csv` | `E7206402E8C476FC0128A362827581EA73C6CE1138FB9B4BF84F626880FA88B0` |
| `R582_Fig1c_rate_ladder.csv` | `5F5888BBB7BAF770CAEA86446D1AE5FA4D4ED6AF0538194AE88A0D097B6CAF2E` |
| `R582_Fig1d_feature_timing.csv` | `ECE0C448303953120F8D4E9D22DF056FDD711A5207E1D8195B4CB6BCBB0D0189` |
| `R582_Fig1_input_manifest.csv` | `5316172F02007DD5FC622E9BD474A381C13DE21175F839D536D435FD63E85676` |
| `R582_Fig1_build.json` | `9A1AC1BCB5C985627486F50EFB334FB60A3B7059E9AF516C6653985AAD5E2857` |

## 8. Integration boundary

This package is not inserted into the manuscript. Integration should preserve the physical-cell
unit, full within-cell range semantics, unconnected 40/400 markers, primary/sensitivity-window
distinction, and the statement that the model markers were not fitted to the voltage traces.
`EXP-META-001` should appear once in the experimental-data provenance or caption/source-data note:
legacy `NH4Cl/NH4CL` labels denote NH4Br, while raw names and bytes remain unchanged.
