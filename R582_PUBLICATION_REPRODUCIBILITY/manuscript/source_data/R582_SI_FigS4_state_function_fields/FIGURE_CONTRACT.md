# R582 Supplementary Figure S4 contract

Core conclusion: Along the registered baseline simulation, free-I2 saturation precedes the late spatial redistribution of retained solid, native remaining bare area and total reaction current.

Figure archetype: quantitative grid.

Target/output: Journal of Power Sources Supplementary Information; 180 x 142 mm; editable SVG/PDF; opaque RGB 600 dpi PNG/TIFF; 180 mm colour and grayscale QA previews.

Backend: Python/matplotlib, inherited from the registered R545 field-export workflow. Python is exclusive for rendering and visual QA.

Panel map:

- **a:** free-I2 stress `S_surf`, with one shared scale centred on `S = 1`.
- **b:** retained-solid fraction `eps_s_pos`, with one shared symlog scale.
- **c:** native remaining bare-area fraction `A_bare_frac`, with one shared linear scale. The audit-only complement `1 - theta_eff` is not substituted.
- **d:** signed total reaction-current density `j_total_A_m2`. Positive values use one shared logarithmic scale; every non-positive node is retained in the frozen source table and shown with a disclosed neutral mask.

Evidence hierarchy:

- hero evidence: the six fixed capacity columns at `Q = 0, 80, 96, 100, 110, 120 mAh cm^-2`;
- comparison evidence: fixed row-wise scales and a common coordinate frame;
- integrity control: exact node/sign inventory, input hash and deterministic rebuild.

Source data: the sole upstream numerical input is the registered `Fig3_baseline_spatial_long.csv` export with required SHA-256 `E322D0D0C4B0D5C8CB84BD5CB18D1A43CBA183EB8A5F112577686993BC8FC007`. Each capacity contains 5,995 nodes on the same 55 x 109 coordinate grid.

Statistics: none. The maps are deterministic continuum outputs, not samples or replicate summaries.

Reviewer risks and controls:

- These fields are model outputs, not microscopy, deposit morphology, coverage or a pore-blocking front.
- No electrical-potential field is read or drawn.
- `A_bare_frac` is plotted natively; `1 - theta_eff` is not relabelled as the exported field.
- No smoothing, interpolation, absolute-value operation or undisclosed clipping is permitted.
- Non-positive current nodes remain signed in source data and are disclosed by capacity.

