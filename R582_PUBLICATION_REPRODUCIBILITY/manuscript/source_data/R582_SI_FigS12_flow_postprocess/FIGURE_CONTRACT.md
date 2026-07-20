# R582 Supplementary Figure S12 contract

**Core conclusion.** Under the declared Sherwood relation, increasing flow
thins the sub-grid diffusion layer and conditionally delays the postprocessed
average-saturation point.

**Archetype.** Single-panel quantitative hero curve.

**Backend and output.** Python/matplotlib exclusively; exactly 180 mm by 68 mm.
Editable SVG and PDF plus 600 dpi PNG/TIFF and 300 dpi actual-size colour and
grayscale previews. All text uses the exact TeX Gyre Termes OTF faces used by
the `tgtermes` manuscript body; the minimum text size is 6.5 pt.

**Evidence map.** Three directly labelled curves show the registered
$m=0.4$, 0.5 and 0.6 evaluations. The 25–100 mL min$^{-1}$ declared range is
shaded, and the common 50 mL min$^{-1}$ point anchors the registered baseline
$Q_s=83.020$ mAh cm$^{-2}$.

**Statistics.** This is a deterministic analytical scenario; sampling error,
replicate count and inferential statistics do not apply.

**Source data.** The 1081-row registered baseline and 120-row registered R577
sweep are frozen under `inputs/`. The script reconstructs every sweep row from
the baseline terms and rejects any mismatch before drawing.

**Reviewer risk and boundary.** The scenario rescales only the declared
sub-grid generation contribution through
$\delta/\delta_0=(v/v_0)^{-m}$. It is not a new flow-dependent
boundary-layer solve, a measured mass-transfer law or an experiment. No
cross-evidence lever ranking is shown.

