# Figure S10 contract

- **Core conclusion:** The single-fibre and pore-network calculations use explicit idealized model domains, not reconstructed experimental-felt morphology.
- **Evidence class:** `E-COMP`.
- **Archetype:** schematic-led composite with the registered network slice as the larger panel.
- **Backend:** Python/matplotlib only, following the established R582 figure workflow.
- **Final size:** 180 × 104 mm.
- **Hero evidence:** panel b shows every node and throat in the exact registered `z = 7` network slice; line width maps registered initial throat radius `r0`.
- **Supporting evidence:** panel a gives orthographic cross-sectional and axial definitions of the cylindrical single-fibre unit cell.
- **Source data:** byte-registered NPZ objects plus byte-identical copies of the model-definition scripts; plotted definitions are frozen as CSV tables.
- **Statistics:** not applicable; the figure defines deterministic computational comparators.
- **Export contract:** editable SVG/PDF, 600-dpi PNG, opaque RGB 600-dpi TIFF, and 300-dpi colour and grayscale 180-mm previews.
- **Typography:** the four exact TeX Gyre Termes OTF faces used by the manuscript; 7.2-pt base, 6.5-pt minimum, 8-pt panel labels, no fallback or Type 3 font.
- **Reviewer boundary:** no deposit-height field, coverage mask, solved field, updated throat radius, flux field, blockage front, pseudo-observed texture, 3D perspective, gloss or reconstructed felt image is displayed.

## Panel map

- **a:** prescribed cylindrical single-fibre unit cell with `r_f = 7.50 µm`, `r_out = 19.36 µm`, `L_z = 150 µm`, `epsilon = 0.85`, normalized outer concentration boundary and wall-state boundary rules. No wall mask is visualized.
- **b:** exact central slice of the registered `15 × 15 × 15` pore network, with 225 displayed nodes, 420 in-slice throats, normalized inlet/outlet Dirichlet values and the registered conductance/allocation equations.

Covering either panel would remove a distinct definition needed to interpret the single-fibre or pore-network comparator; no decorative panel is retained.
