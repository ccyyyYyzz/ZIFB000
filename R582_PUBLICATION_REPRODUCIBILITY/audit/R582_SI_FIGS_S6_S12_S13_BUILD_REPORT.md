# R582 SI Figures S6, S12 and S13 — build and acceptance report

Date: 2026-07-20  
Backend: Python/matplotlib only  
Status: **ACCEPTED FOR `SI_R582.tex` INTEGRATION**

## Scope and non-interference

Only new R582 figure/source-bundle files were created. No original COMSOL
`.mph`, raw experiment, historical figure master, `main_R582.tex` or SI TeX
source was opened for writing. All frozen inputs are byte-identical copies of
registered evidence and are verified before every render.

## Accepted outputs

| SI figure | accepted PDF | size | PDF SHA-256 |
|---|---|---:|---|
| S6, voltage degeneracy | `manuscript/figures_R582/SIFig_R582_S6_voltage_degeneracy.pdf` | 180 × 92 mm | `50C51FE9352F332CE5EC7994A31F7E1ABE279358B412A9F9DEBFB5FFF6CC752D` |
| S12, analytical flow postprocess | `manuscript/figures_R582/SIFig_R582_S12_flow_postprocess.pdf` | 180 × 68 mm | `9DD4C93227FCB2081E7FBEA790968773466A2EA497F6A28D43DAA2D951307822` |
| S13, smooth-permeability control | `manuscript/figures_R582/SIFig_R582_S13_smooth_permeability.pdf` | 180 × 70 mm | `AEE930E0DE59779E3BEE25599527AB62FF1DF919058776F7EDEF8DC2D070E10C` |

Each stem also has editable SVG, 600 dpi PNG/TIFF, a 300 dpi 180-mm colour
preview and a 300 dpi grayscale preview in `manuscript/figures_R582`.

## Scientific reconstruction checks

### S6

- One selected physical full-cell file, charge cycle 20, 90 displayed points.
- The reduced fit uses 72 points from 2.672333 to 97.540052 mAh cm$^{-2}$.
- Registered coefficients were reconstructed exactly within $2\times10^{-9}$:
  $c_0=1.335541$ V, $c_1=9.819008\times10^{-4}$ V per
  (mAh cm$^{-2}$), and $b_{\rm eff}=0.136224$ V.
- RMSE = 7.243144 mV; fixed accessibility-related contribution =
  70.812528 mV.
- All seven registered reduced-accessibility/coefficient points satisfy the
  constant-contribution identity. Here
  $R_{\theta,\mathrm{end}}=1-\theta_{\mathrm{end}}$; it is not the native
  $A_{\mathrm{bare}}/A_0=R_\theta T_{\mathrm{pore}}$. The figure makes only
  an identifiability claim.

### S12

- Registered baseline: 1081 ordered rows, canonical
  `baseline_J40_Q120` case.
- Registered R577 scenario: 120 rows (40 per $m=0.4$, 0.5 and 0.6).
- Every registered $Q_s$, $\delta/\delta_0$, $\delta$ and $\Delta Q$ value was
  regenerated from the frozen baseline within absolute tolerance
  $2\times10^{-10}$.
- All curves cross the registered baseline $Q_s=83.020199$ mAh cm$^{-2}$ at
  50 mL min$^{-1}$. For $m=0.5$, the exact 25–100 mL min$^{-1}$ scenario
  moves $Q_s$ from 74.991523 to 88.732903 mAh cm$^{-2}$.
- The panel is explicitly labelled “Analytical postprocess”; no solved-flow,
  measured-law or cross-evidence ranking claim is made.

### S13

- The immutable R537 text export was reparsed into 1081 ordered rows for each
  matched re-solve. Every registered parsed column was reconstructed to
  floating-point precision.
- Maximum $|\Delta V|=5.2144$ mV at 117.44444 mAh cm$^{-2}$; endpoint
  $\Delta V=+1.2710$ mV at 120 mAh cm$^{-2}$.
- Endpoint $K/K_0=0.956287$ for the baseline Kozeny–Carman relation and
  0.982496 for the network-derived smooth path.
- This is a smooth bulk-permeability control only. No local pore blockage,
  morphology or electrical-potential inference is present.

## Typography, deterministic export and visual QA

- All three figures resolve exclusively to TeX Gyre Termes Regular, Bold and
  Italic, using the exact TeX Live OTF faces matched to the `tgtermes` body.
- Minimum text size is 6.5 pt in every figure.
- PDF audit: fonts embedded; no Arial, Helvetica, DejaVu, Liberation, Calibri,
  Times New Roman or Type 3 fonts.
- SVG audit: editable `<text>` retained; no forbidden fallback family.
- PDF page dimensions and 600/300 dpi pixel dimensions match the declared
  physical canvases.
- A second independent render of all PDF/SVG/PNG/TIFF/preview outputs is
  byte-identical for every figure.
- Colour and grayscale 180-mm previews were visually inspected. Panel/direct
  labels are unclipped and non-overlapping; dashed/solid encodings remain
  distinguishable without colour.

## Source bundles and captions

- `manuscript/source_data/R582_SI_FigS6_voltage_degeneracy/`
- `manuscript/source_data/R582_SI_FigS12_flow_postprocess/`
- `manuscript/source_data/R582_SI_FigS13_smooth_permeability/`

Each bundle contains frozen inputs, input manifest, clean plotted-source and
summary/parameter tables, renderer, exact-font export utility, figure contract,
caption draft, README, QA notes and a machine-readable render manifest with
hashes for every input, source-bundle record and output.
