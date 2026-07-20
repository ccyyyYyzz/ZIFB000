# R582 Figure 5 v2 contract

## Core conclusion

Independent molecular and mesoscale calculations bound four inputs or physical
comparators for the ZIFB positive-electrode model: dry single-I2
BSSE-corrected adsorption-energy ordering, bulk carrier mobility,
placement-dependent geometric remaining area and smooth pore-network
permeability. The single-fibre quantity is $A/A_0$, not the native COMSOL
$A_{\mathrm{bare}}/A_0=R_{\theta}T_{\mathrm{pore}}$. None of these lower-scale
calculations supplies the voltage-calibrated $R_{\theta}$ relation used by the
continuum baseline.

## Evidence chain

| Panel | Question | Evidence role | Interpretation boundary |
|---|---|---|---|
| a | Which dry carbon sites have the more favourable one-I2 adsorption-energy ordering? | Periodic CP2K relative BSSE-corrected adsorption-energy prior | Not a solution free energy, rate, nucleation barrier, population or value of N |
| b | What bulk mobility scale do iodide and the two oxidized iodine carriers occupy? | Five-SOC, force-field-limited MD prior under two charge scalings | Not experimental validation, deposited-phase transport or a replacement for the production constant |
| c | How strongly can assumed sparse versus dense placement change the geometric remaining-area ratio A/A0? | Single-fibre geometric comparator families | Not native COMSOL A_bare/A0, observed morphology, microscopic coverage or a calibrated R_theta law |
| d | How much does an idealized pore network change hydraulic permeability over the modeled solid-loading range? | Six-law permeability envelope | Not measured pore closure, a local blockage map or electrical potential |

## Composition and hierarchy

- Archetype: asymmetric two-row quantitative figure.
- Upper prior strip: compact panels a and b, separated by a dedicated gutter.
- Positive-electrode hero row: enlarged panels c and d, with panel c receiving
  the widest plotting area because placement-to-geometric-area uncertainty is
  the central comparison.
- The panel-a `+0.08` value sits above the vacancy marker, so it cannot read as
  part of the panel-b `I2Br-` row label.
- Figure size: 180 x 125 mm.
- Backend: Python/matplotlib for drawing and final-size QA.
- Typeface: exact TeX Gyre Termes OTF throughout; 7.2 pt base, 6.5 pt minimum
  and 8 pt bold panel labels.

## Hard exclusions

- No claim that DFT determines N, that MD validates D_eff, or that either
  single-fibre family identifies the deposited morphology.
- No identification of single-fibre geometric $A/A_0$ with native COMSOL
  $A_{\mathrm{bare}}/A_0$. The latter equals $R_{\theta}T_{\mathrm{pore}}$,
  with $R_{\theta}=1-\theta_{\mathrm{cal}}$ and
  $T_{\mathrm{pore}}=(K/K_0)^{1/2}$.
- No claim of observed morphology, microscopic coverage, a blocking front,
  pore-throat closure or electrical potential.
- NH4Br appears only as the representative supporting-electrolyte condition of
  the MD calculation; bromide is neither the visual nor narrative protagonist.
- The figure is an input-bounding and comparator figure, not an independent
  validation figure.

## Fifteen-second test

The reader should first see that assumed placement changes positive-electrode
geometric remaining area far more strongly than smooth permeability over the
modeled range, and then recognize the BSSE-corrected adsorption-energy ordering
and mobility scale as bounded upstream priors.
