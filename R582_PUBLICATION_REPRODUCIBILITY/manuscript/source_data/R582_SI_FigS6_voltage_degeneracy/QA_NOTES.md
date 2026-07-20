# R582 Supplementary Figure S6 QA

## Scientific and source checks

- Frozen input SHA-256 checks: **PASS** (4/4).
- Selected record: one physical file, charge cycle 20, 90 displayed points.
- Fitted interval: 72 points, 2.672333–97.540052 mAh cm$^{-2}$.
- Registered fit reconstruction: **PASS**; RMSE 7.243144 mV.
- Registered fixed contribution: 70.812528 mV.
- Registered $R_{\theta}=1-\theta$/coefficient identities and all seven source
  points: **PASS**.
- Evidence boundary: deterministic `E-POST` on registered `E-EXP/E-SIM`
  inputs. $R_{\theta}$ is a reduced calibration-controlled factor, not native
  $A_{\mathrm{bare}}/A_0=R_{\theta}T_{\mathrm{pore}}$; no morphology or
  independent-validation claim.

## Typography and export checks

- Canvas: 180.000 × 92.000 mm (**PASS**).
- Minimum text: 6.5 pt (**PASS**).
- Resolved family: TeX Gyre Termes only (**PASS**).
- PDF fonts: TeXGyreTermes Regular/Bold/Italic; no forbidden family and no
  Type 3 (**PASS**).
- SVG text remains editable and contains no font fallback (**PASS**).
- PNG/TIFF: 4252 × 2173 px at 600 dpi (**PASS**).
- Actual-size colour/grayscale previews: 2126 × 1087 px at 300 dpi (**PASS**).
- Second-render hashes: all six exported/preview files byte-identical (**PASS**).
- Accepted PDF SHA-256:
  `50C51FE9352F332CE5EC7994A31F7E1ABE279358B412A9F9DEBFB5FFF6CC752D`.

## Visual inspection

Colour and grayscale previews were inspected at the exported 180 mm size.
Panel labels, axes, the fitted-interval band, residual, direct value labels,
$R_{\theta,\mathrm{end}}$ identity and the fixed-contribution annotation are
legible with no clipping or collisions. Line style separates the full-cell
trace from the reduced fit in grayscale.
