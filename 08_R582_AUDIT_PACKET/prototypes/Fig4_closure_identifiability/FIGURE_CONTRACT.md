# R582 Figure 4 contract

**Core conclusion.** Changing only the accessibility relation leaves the modeled
average-saturation capacity nearly unchanged but strongly alters the subsequent
remaining area, retained-solid inventory, and voltage; the voltage observation
layer therefore does not select a unique deposit morphology.

**Figure archetype.** Asymmetric quantitative grid with one hero panel.

**Target/output.** Two-column manuscript figure, exactly 180 mm wide and 118 mm
high. Python/matplotlib is the exclusive drawing, preview, export, and visual-QA
backend. The typeface is TeX Gyre Termes, matching the NewTX/Times manuscript
body, with Times New Roman allowed only as a documented fallback.

**Panel map.**

- **a — comparison:** remaining accessible-area fraction for the calibrated
  baseline, a one-way island-model shadow evaluated on the baseline inventory,
  and the coupled island-model variant. A compact callout reports the matched
  saturation-marker difference.
- **b — hero evidence:** matched voltage trajectories with an aligned
  island-minus-baseline voltage difference and the endpoint value labelled
  directly.
- **c — mechanistic consequence:** each solved branch's retained-solid
  trajectory, with only the baseline half-area inventory and the island-model
  half-area inventory shown as references.
- **d — identifiability limit:** accessibility–coefficient pairs that reproduce
  the same selected voltage contribution.

**Evidence hierarchy.** Panel b is the dominant consequence. Panels a and c show
how the divergence arises. Panel d prevents the voltage divergence from being
misread as morphology identification.

**Statistics.** These are deterministic model trajectories and a deterministic
reduced observation-layer calculation. No sampling error, replicate count, or
inferential statistic applies; no error bars are drawn.

**Source data.** The matched trajectories, release summary, marker definitions,
and reduced voltage-degeneracy tables are registered R581/R538 assets. The build
script copies only plotted columns into clean R582 tables and records SHA-256
hashes for every input, derived table, and export.

**Image integrity.** No smoothing, curve fitting, interpolation of the matched
trajectories, or manual point movement is used. The smooth curve in panel d is
an analytic evaluation of the constant voltage-contribution relation recovered
from the registered source table. Raster exports are flattened to opaque RGB.

**Reviewer risk.** The calibrated baseline is not independent voltage
validation, the island-model variant is a geometric relation rather than an
observed morphology, and the one-way shadow is not a feedback solve. These
identities are stated once in the caption/source package without turning the
artwork into an audit diagram.

