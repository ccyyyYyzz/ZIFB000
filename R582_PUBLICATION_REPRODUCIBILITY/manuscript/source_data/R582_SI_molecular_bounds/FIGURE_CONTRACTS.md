# R582 SI molecular-figure contracts

Backend is Python/matplotlib only for drawing, export and visual QA.  Target
output is Journal of Power Sources supplementary artwork at 180 mm width,
with editable SVG/PDF masters and opaque 600-dpi RGB PNG/TIFF derivatives.
All labels use the four explicitly registered TeX Gyre Termes OTF files that
match the manuscript body; the base size is 7.2 pt, no text is below 6.5 pt,
and panel letters are 8 pt bold.

## Figure S7 — single-I2 ordering

- Core conclusion: Within the declared BSSE-corrected periodic adsorption-energy
  calculation, the tested C-OH and C=O motifs lie below basal carbon, whereas
  the tested vacancy lies slightly above basal carbon.
- Archetype: asymmetric mixed-modality figure.
- Final size: 180 x 120 mm.
- Panel map:
  - a: hero lollipop plot of BSSE-corrected adsorption energy relative to the
    basal calculation; at least half of the drawable width.
  - b-e: exact optimized XYZ geometries in the same site order.
- Hero evidence: registered four-site energy table.
- Validation/support: matching registered XYZ structures; display bonds are
  distance-based adjacency guides, not bond-order calculations.
- Statistics: none; deterministic calculations, no sampling error bars.
- Reviewer risk: adsorption-energy ordering must not be described as solution free
  energy, adsorption population, or a nucleation barrier.  Single-I2 CDD is
  excluded because the raw fields are absent.

## Figure S8 — two-I2 diagnostic

- Core conclusion: The tested compact C-OH two-I2 configuration is lower in
  registered electronic energy than the separated reference within the
  declared periodic calculation.
- Archetype: asymmetric mixed-modality figure.
- Final size: 180 x 112 mm.
- Panel map:
  - a: compact-versus-separated relative electronic-energy comparison.
  - b-c: exact optimized compact and separated XYZ geometries.
  - d: thresholded points from the recoverable true two-I2 charge-density-
    difference NPY, overlaid on the registered compact geometry.
- Hero evidence: registered coalescence-energy table.
- Validation/support: exact compact/separated structures and the independently
  returned CDD grid.
- Statistics: none; deterministic calculations.
- Image integrity: CDD values are not smoothed, interpolated or fabricated.
  Points are retained only when delta-rho >= +0.002 or <= -0.002 e A^-3;
  one periodic x translation is used solely to display the compact cluster
  continuously.  Accumulation/depletion retain distinct color and marker
  shape.  No pathway arrow or reaction coordinate is drawn.
- Reviewer risk: the result is not a solution equilibrium, association free
  energy, nucleation pathway, or kinetic barrier.

## Figure S9 — MD carrier ladder

- Core conclusion: The five-composition means of the oxidized-iodine carrier
  mobilities are below iodide in both tested charge parameterizations, while
  absolute diffusivities remain force-field dependent.
- Archetype: quantitative grid with shared axes.
- Final size: 180 x 96 mm.
- Panel map:
  - a: q = 0.8 ECC carrier ladder.
  - b: q = 1.0 formal-charge carrier ladder.
- Hero evidence: species-resolved five-SOC means and ranges from the registered
  source summary.
- Robustness evidence: the two charge parameterizations and the within-
  trajectory block-stability bars.
- Statistics: each SOC composition has one trajectory.  Thin spans are the
  min-max range across five different SOC compositions; capped bars are the
  propagated four-block within-trajectory stability measure.  Neither is
  replica uncertainty or a population confidence interval.
- Reviewer risk: the bulk-MD values are a bounded mobility prior, not porous-
  electrode effective diffusivity and not validation of a continuum constant.
  NH4Br appears once in the condition line and is not the visual organizer.
