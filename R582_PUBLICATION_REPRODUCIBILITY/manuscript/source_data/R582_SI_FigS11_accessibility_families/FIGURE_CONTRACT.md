# Figure S11 contract

- **Core conclusion:** At fixed retained-solid fraction, the prescribed placement-density assumption changes the single-fibre geometric remaining-area fraction `A/A0` substantially.
- **Evidence class:** `E-COMP`.
- **Archetype:** quantitative hero panel with an exact-node companion.
- **Backend:** Python/matplotlib only, following the established R582 figure workflow.
- **Final size:** 180 × 96 mm.
- **Hero evidence:** panel a shows all four registered single-fibre geometric families and all 20 computed nodes.
- **Exact comparator:** panel b shows the five retained-solid nodes shared by the `phi_ppt = 0.005`, `n_n = 10^11 m^-2` and `n_n = 10^13 m^-2` geometric families.
- **Source data:** registered closure and clock CSVs, retained as byte-identical frozen copies.
- **Statistics:** not applicable; these are deterministic comparator nodes, not experimental replicates.
- **Line policy:** connect computed nodes only; no new interpolation or fitted family curve.
- **Reference policy:** the dashed trace is only the calibrated comparator `R_theta = 1 - theta`, evaluated as `1 - comsol_theta_ref` at registered abscissae. It is neither a geometric `A/A0` family nor native COMSOL `A_bare/A0`.
- **Native COMSOL policy:** the native bare-area quantity is `A_bare/A0 = R_theta * T_pore`. `T_pore` is not present in the S11 node inventory, so native `A_bare/A0` is not plotted or inferred here.
- **Numeric-node policy:** the correction changes semantic labels and generated table headers only; all registered numeric family and comparator nodes remain unchanged.
- **Export contract:** editable SVG/PDF, 600-dpi PNG, opaque RGB 600-dpi TIFF, and 300-dpi colour and grayscale 180-mm previews.
- **Typography:** the four exact TeX Gyre Termes OTF faces used by the manuscript; 7.2-pt base, 6.5-pt minimum at the rendered-glyph level, no fallback or Type 3 font.
- **Reviewer boundary:** the figure does not show measured coverage, inferred morphology, a deposit image, native COMSOL bare-area accessibility or validation of the calibrated comparator.

## Panel map

- **a:** full registered family inventory as geometric remaining area `A/A0` versus retained-solid fraction `epsilon_s`, with the separate dashed `R_theta` comparator explicitly identified.
- **b:** exact shared-inventory geometric `A/A0` pairs with no interpolation. The largest registered paired difference is 0.3094 at `epsilon_s = 3.3909568 × 10^-3`.

Panel b is retained because it makes the fixed-inventory geometric comparison explicit rather than asking the reader to infer it from curves with partly non-overlapping inventory ranges.
