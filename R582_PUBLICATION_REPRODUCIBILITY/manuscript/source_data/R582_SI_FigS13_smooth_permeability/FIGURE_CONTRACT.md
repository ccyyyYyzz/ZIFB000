# R582 Supplementary Figure S13 contract

**Core conclusion.** Replacing the baseline Kozeny–Carman smooth permeability
relation with the registered pore-network-derived smooth path changes the
modeled voltage by at most 5.214 mV and by 1.271 mV at 120 mAh cm$^{-2}$.

**Archetype.** Asymmetric quantitative two-panel control with a dominant
voltage-difference panel.

**Backend and output.** Python/matplotlib exclusively; exactly 180 mm by 70 mm.
Editable SVG and PDF plus 600 dpi PNG/TIFF and 300 dpi actual-size colour and
grayscale previews. All text uses the exact TeX Gyre Termes OTF faces used by
the `tgtermes` manuscript body; the minimum text size is 6.5 pt.

**Panel map.**

- **a, hero:** signed voltage difference, defined as the network-path re-solve
  minus the baseline Kozeny–Carman re-solve, with the maximum absolute and
  endpoint differences labelled directly.
- **b:** the two smooth relative-permeability paths, with their 120 mAh
  cm$^{-2}$ values labelled directly.

**Statistics.** These are deterministic matched simulation trajectories; no
replicate or inferential error bar applies.

**Source data.** The immutable R537 text export and its registered parsed table
are frozen under `inputs/`. The script reparses 1081 rows per path and
cross-checks every registered column before drawing.

**Reviewer risk and boundary.** This control tests only the smooth
bulk-permeability relation. It neither resolves nor excludes local pore-throat
blockage and makes no morphology or electrical-potential inference.

