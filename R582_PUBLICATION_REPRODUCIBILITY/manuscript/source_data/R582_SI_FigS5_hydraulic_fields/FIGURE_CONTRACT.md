# R582 Supplementary Figure S5 contract

Core conclusion: In the registered baseline simulation, smooth permeability, velocity magnitude and hydraulic pressure evolve through a hydraulic transport channel that is distinct from the calibrated accessible-area relation.

Figure archetype: quantitative grid.

Target/output: Journal of Power Sources Supplementary Information; 180 x 112 mm; editable SVG/PDF; opaque RGB 600 dpi PNG/TIFF; 180 mm colour and grayscale QA previews.

Backend: Python/matplotlib, inherited from the registered R545 field-export workflow. Python is exclusive for rendering and visual QA.

Panel map:

- **a:** relative smooth permeability `K_perm_rel = K/K0`, with one shared linear scale.
- **b:** native velocity magnitude `u_native_mag_m_s`, with one shared linear scale.
- **c:** hydraulic pressure `p_native_Pa` in Pa, referenced to the registered outlet condition `p_out = 0`, with one shared linear scale.

Evidence hierarchy:

- hero evidence: the six fixed capacity columns at `Q = 0, 80, 96, 100, 110, 120 mAh cm^-2`;
- comparison evidence: fixed row-wise scales and a common coordinate frame;
- integrity control: exact node inventory, input hash and deterministic rebuild.

Source data: the sole upstream numerical input is the registered `Fig3_baseline_spatial_long.csv` export with required SHA-256 `E322D0D0C4B0D5C8CB84BD5CB18D1A43CBA183EB8A5F112577686993BC8FC007`. Each capacity contains 5,995 nodes on the same 55 x 109 coordinate grid.

Statistics: none. The maps are deterministic continuum outputs, not samples or replicate summaries.

Reviewer risks and controls:

- `p_native_Pa` is labelled only as hydraulic pressure in Pa; it is never used as electrical potential.
- The pressure reference `p_out = 0` is explicit in the artwork and caption.
- The smooth permeability field does not resolve local pore closure or blockage.
- No smoothing, interpolation or undisclosed clipping is permitted.

