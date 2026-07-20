# R582 Figure 3 v2 QA notes

QA date: 2026-07-20

## Data and semantic integrity

- PASS — sole spatial-field input SHA-256 is `E322D0D0C4B0D5C8CB84BD5CB18D1A43CBA183EB8A5F112577686993BC8FC007`.
- PASS — selected capacities are exactly 80, 100 and 120 mAh cm^-2.
- PASS — 5,995 unique nodes per capacity; 17,985 selected rows total; complete 55 x 109 grid at each capacity.
- PASS — no missing, non-finite or duplicate capacity-coordinate rows.
- PASS — every original column in the generated subset matches its selected source value after CSV reload.
- PASS — `A_bare_over_A0` recomputes as `1 - theta_eff` after CSV reload to within `3.33e-16`; the stored native-minus-complement difference recomputes to within `2.23e-16`.
- PASS — the maximum absolute difference between native `A_bare_frac` and `1 - theta_eff` is explicitly preserved as `6.47152905e-4`; v2 plots the requested complement and does not silently conflate the fields.
- PASS — current-sign inventory is `{80: 0, 100: 6, 120: 0}` nonpositive nodes; all six are negative and occur at Q=100.
- PASS — all positive current values fall inside the declared shared log range: observed `8.34224959e-5` to `2.16747620e4 A m^-2`, displayed range `8e-5` to `2.2e4 A m^-2`.
- PASS — nonpositive current is represented by an explicit neutral mask. No clipping, absolute-value conversion, smoothing or interpolation is used.

## Capacity clock and stage semantics

- PASS — exact `Q_s = 83.0202 mAh cm^-2` and `Q_f,cal = 99.5901 mAh cm^-2` markers are visible.
- PASS — exported snapshots at 80, 100 and 120 mAh cm^-2 are distinct from the model-anchor markers.
- PASS — the clock directly states `Q=100 approximately Q_f,cal`.
- PASS — column labels are `before mean-saturation marker`, `near calibrated half-accessibility marker` and `late charge`.

## Export and typography

- PASS — final PDF page is 180.000 x 145.000 mm, below the 155 mm target height.
- PASS — SVG declares 510.23622 x 411.023622 pt, contains 63 editable `<text>` nodes and contains no glyph-path definitions.
- PASS — PDF contains embedded CID TrueType Arial and DejaVu Sans fallback fonts; no Type 3 fonts. Extracted page text contains 649 characters.
- PASS — PNG is 2,125 x 1,712 px at 300 dpi.
- PASS — opaque RGB TIFF is 4,251 x 3,425 px at 600 dpi with LZW compression.
- PASS — 180 mm review preview is 1,062 x 856 px at 150 dpi.
- PASS — grayscale QA is a pixel-exact luminance conversion of the review preview.
- PASS — two consecutive cold renders produced identical hashes for all six visual assets.

## True-size and grayscale visual inspection

- PASS — the 15-second reading path is capacity clock -> solid retention -> remaining bare accessibility -> reaction-current redistribution.
- PASS — the three rows use fixed cross-capacity scales and remain comparable without consulting panel-specific ranges.
- PASS — warm retained-solid intensity increases, cool remaining-area intensity fades and the current distribution remains independently legible in grayscale.
- PASS — the six masked current nodes are disclosed directly below the matrix; the note is readable at 180 mm.
- PASS — collector/separator direction and one flow-y arrow are present without decorative mechanism artwork.
- PASS — long semantic row labels and the shared y-axis label do not collide.
- PASS — no element suggests microscopy, deposit morphology or a pore-blocking front.
- PASS — the v1 profile-based alternative remains intact; v2 omits the companion profile and reduces final height from 166 to 145 mm.

## Stable hashes

- v2 SVG: `A7403D981FE0D3C4C626E1AD08C46F8595151E270970B3DBDF1E1D058D18CFAE`
- v2 PDF: `0BD5C588BC20952D5BD692563D8006C466ABB3D0EDE6F4EBE6C9B7A5069BF047`
- v2 PNG: `2204D2DF45BF5D91EECE1BB4964B7842FA01F2A305E3F88C150C4169C27175E4`
- v2 TIFF: `456F3D66F7E3B34FDFEC1F9ABF93A03CB2F202968B8E98DE0FA98EC5F5D09A06`
- v2 180 mm preview: `F5DCC238C21DE269E602544195D8673426C2298F463610C325F18C3C2E384FF5`
- v2 grayscale QA: `CA1A8D63FD83A88BD555BF41591FE414959F43498CD47CAD24E2CE783982C97C`
- v2 source subset: `A34B9F03A6A2CBCC6ACDB60AE8F2E4D6E008E61FAED14AFA8CD2B01C3E272F6C`

## Preservation checks

- v1 SVG remains `08E6A909E766BF46209CD8E92BA48581A5E96079FFBFB548FB23C17E079D48F9`.
- v1 PDF remains `36323CEA48176625A733131500AA66860DC1222EE608E3E091F368B8ADA8A6DE`.
- `main.tex` and `SI.tex` were not edited by this task.
