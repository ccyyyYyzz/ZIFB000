# R582 Supplementary Figure S4 QA notes

QA date: 2026-07-20

## Scientific and source-data integrity

- **PASS** — the sole upstream input is the immutable registered field export with SHA-256 `E322D0D0C4B0D5C8CB84BD5CB18D1A43CBA183EB8A5F112577686993BC8FC007`.
- **PASS** — all six registered capacities are present: 0, 80, 96, 100, 110 and 120 mAh cm^-2. Each contains 5,995 unique nodes on the same 55 x 109 grid; coordinates span `x = 3–5 mm` and `y = 0–20 mm`.
- **PASS** — the frozen plotted-source table contains 35,970 rows and round-trips exactly through CSV. Its SHA-256 is `5043E6031E3C2910B84E9B11E7F1BBA30D62A60815B9E3AE09BFB3B8F83A03F6`.
- **PASS** — panel c reads native `A_bare_frac`; the script never replaces it with `1 - theta_eff`.
- **PASS** — panel d retains signed current information. Non-positive-node counts at ordered capacities are 248, 0, 33, 6, 0 and 0. Signed ranges are `[-4.21706102215e-5, -3.51627726587e-9]` A m^-2 at Q = 0, `[-8.33769099204e-4, -2.08901114956e-6]` A m^-2 at Q = 96, and `[-5.71642984703e-4, -1.80419252671e-4]` A m^-2 at Q = 100. The artwork uses a disclosed neutral mask and never applies an absolute value.
- **PASS** — no interpolation, smoothing, synthetic fill or undisclosed clipping is used; field cells use nearest-neighbour rendering.
- **PASS** — no electrical-potential field is read. The figure makes no morphology, microscopic coverage, blockage-front or pore-closure inference.

## Visual QA at final size

- **PASS** — the PDF page is exactly `510.236 x 402.52 pt`, corresponding to 180 x 142 mm.
- **PASS** — the 180 mm colour preview was inspected after removing a first-pass collision between row labels and repeated y-axis titles. The final row labels, tick labels, capacity headers and colour bars do not overlap.
- **PASS** — one fixed scale is used per row. The column-wise sequence remains readable in colour and grayscale: the `S = 1` transition, late retained-solid gradient, native remaining-area loss and reaction-current redistribution remain distinguishable.
- **PASS** — the neutral current mask remains visible in grayscale and is keyed by an on-art note.
- **PASS** — no decorative 3D, rainbow map, repeated legend or inferred physical object is present.

## Typography and export

- **PASS** — all four exact TeX Gyre Termes OTF files are registered directly. Base text is 7.2 pt, no explicit text is below 6.5 pt, and panel letters are 8 pt bold.
- **PASS** — `pdffonts` reports only embedded `TeXGyreTermes-Regular`, `TeXGyreTermes-Bold` and `TeXGyreTermes-Italic` CID Type 0C fonts. No Type 3, Arial, Helvetica, DejaVu, Liberation, Calibri, Times, STIX or Computer Modern font is present.
- **PASS** — the SVG contains 72 editable `<text>` nodes, declares TeX Gyre Termes and contains no forbidden fallback-family string.
- **PASS** — `pdfimages -list` reports the rasterized field layers at 600 ppi in the editable PDF master (484 x 510–511 pixels per map); vector text and axes remain editable.
- **PASS** — the PNG and TIFF are opaque RGB at 600 dpi, 4,251 x 3,354 pixels. The colour and grayscale 180 mm QA previews are RGB, 1,062 x 838 pixels at 150 dpi.
- **PASS** — a fresh second render is byte-identical for SVG, PDF, PNG, TIFF, colour preview and grayscale preview.

## Stable output hashes

- SVG: `08B70CC17C90216538CA53A46BEA99A3EE66A0F9B48DD8053BA45EA9A8DE65CF`
- PDF: `3F7DDCE22475C59A7C25D5747A83C0FED75F8C73DF8CB715A501EE463A605ADB`
- PNG: `FAF440988DD5773E9E539CE310901FABEC7A0782F3F369F94C786FF8CACD8AA7`
- TIFF: `310A6FFD5E7BD771559189A3D95575D71B1EE28D0CE822665716D6D7C564DFB2`
- 180 mm colour preview: `E19FE547A9FCE456CB55B282F42963F26940467227F12134303EAD0E647E8D49`
- 180 mm grayscale preview: `802F39E7099E517117245AE5328DA002352AA2BCF13DECF69E2E560B13248969`
