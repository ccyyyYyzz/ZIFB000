# R582 Supplementary Figure S5 QA notes

QA date: 2026-07-20

## Scientific and source-data integrity

- **PASS** — the sole upstream input is the immutable registered field export with SHA-256 `E322D0D0C4B0D5C8CB84BD5CB18D1A43CBA183EB8A5F112577686993BC8FC007`.
- **PASS** — all six registered capacities are present: 0, 80, 96, 100, 110 and 120 mAh cm^-2. Each contains 5,995 unique nodes on the same 55 x 109 grid; coordinates span `x = 3–5 mm` and `y = 0–20 mm`.
- **PASS** — the frozen plotted-source table contains 35,970 rows and round-trips exactly through CSV. Its SHA-256 is `E242684B8CA6940A9CB9EC04DE2CE4C8368B19BE0F4A62F6B5F73C0FC31DE6BD`.
- **PASS** — the displayed global source ranges are `K/K0 = 0.410216681747–1`, `|u| = 0.00814557623663–0.0219932065029 m s^-1`, and hydraulic pressure `p = 0–9627.89127035 Pa`.
- **PASS** — every capacity contains exactly 55 `p = 0` outlet-reference nodes. The artwork and caption explicitly state the registered `p_out = 0` reference.
- **PASS** — pressure is labelled only as hydraulic pressure in Pa. No electrical-potential field is read or drawn.
- **PASS** — no interpolation, smoothing, synthetic fill or undisclosed clipping is used; field cells use nearest-neighbour rendering.
- **PASS** — the smooth permeability display is not interpreted as local pore closure or blockage.

## Visual QA at final size

- **PASS** — the PDF page is exactly `510.236 x 317.48 pt`, corresponding to 180 x 112 mm.
- **PASS** — the 180 mm colour preview was inspected after removing a first-pass collision between row labels and repeated y-axis titles and removing redundant colour-bar headings. The final row labels, tick labels, capacity headers and colour bars do not overlap.
- **PASS** — one fixed linear scale is used per row. The late Q = 120 permeability/velocity redistribution and the hydraulic-pressure gradient remain readable in colour and grayscale.
- **PASS** — the pressure-reference sentence remains readable at final placed size and cannot be mistaken for an electrical-potential label.
- **PASS** — no decorative 3D, rainbow map, repeated legend or inferred physical object is present.

## Typography and export

- **PASS** — all four exact TeX Gyre Termes OTF files are registered directly. Base text is 7.2 pt, no explicit text is below 6.5 pt, and panel letters are 8 pt bold.
- **PASS** — `pdffonts` reports only embedded `TeXGyreTermes-Regular`, `TeXGyreTermes-Bold` and `TeXGyreTermes-Italic` CID Type 0C fonts. No Type 3, Arial, Helvetica, DejaVu, Liberation, Calibri, Times, STIX or Computer Modern font is present.
- **PASS** — the SVG contains 59 editable `<text>` nodes, declares TeX Gyre Termes and contains no forbidden fallback-family string.
- **PASS** — `pdfimages -list` reports the rasterized field layers at 600 ppi in the editable PDF master (484 x 500 pixels per map); vector text and axes remain editable.
- **PASS** — the PNG and TIFF are opaque RGB at 600 dpi, 4,251 x 2,645 pixels. The colour and grayscale 180 mm QA previews are RGB, 1,062 x 661 pixels at 150 dpi.
- **PASS** — a fresh second render is byte-identical for SVG, PDF, PNG, TIFF, colour preview and grayscale preview.

## Stable output hashes

- SVG: `8334866A4A713D0793D1D2CD6F711D3D894A32A24A9DEC29F5EEDBC5A1A84E2F`
- PDF: `09E409A9A671C7F01FD118154014D4E938CE62F9A34AE51E4A0AB90F0D2AE3AB`
- PNG: `C1B5BFD2FE221804CC6B08866227B190AC741D11156FA5762841686E473539E9`
- TIFF: `3113A68CDE482B8DD994F31AE708070CE3966468961AC48594E8F43F72948DB1`
- 180 mm colour preview: `9BDE0E4A1BBE061D4D4C35FDF7100D7BF94C61B1EB84EC07D702FF9D66AD115F`
- 180 mm grayscale preview: `73B0A2AE4CA00918574AED6AEDF17A1BDECDDD2389890E907DA7F5D005BC1362`
