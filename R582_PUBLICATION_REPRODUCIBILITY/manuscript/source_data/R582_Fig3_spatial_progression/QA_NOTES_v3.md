# R582 Figure 3 v3 QA notes

QA date: 2026-07-20

## Data and semantic integrity

- PASS — sole input SHA-256 is `E322D0D0C4B0D5C8CB84BD5CB18D1A43CBA183EB8A5F112577686993BC8FC007`.
- PASS — selected capacities are exactly 80, 100 and 120 mAh cm^-2, with 5,995 unique nodes per capacity and no missing, non-finite or duplicated coordinate rows.
- PASS — v3 plots native `A_bare_frac` directly. The separately computed `1 - theta_eff` is audit-only; the maximum native-minus-complement discrepancy is recorded as `6.47152905e-4`.
- PASS — current-sign inventory is `{80: 0, 100: 6, 120: 0}` negative nodes. The six exact negative values lie between `-5.71642984703e-4` and `-1.80419252671e-4 A m^-2` and appear only as a neutral mask.
- PASS — no interpolation, smoothing, clipping, absolute-value transform or synthetic fill is used.
- PASS — the lower profile is the arithmetic mean of the same native field over the 109 uniformly sampled flow positions at each of 55 through-plane positions.

## Capacity and visual semantics

- PASS — exact production anchors `Q_s = 83.0202` and `Q_f,cal = 99.5901 mAh cm^-2` are distinct from exported snapshots.
- PASS — human-readable stage labels avoid internal audit terminology.
- PASS — collector, separator and flow directions are explicit.
- PASS — one fixed scale per row supports direct cross-capacity comparison.
- PASS — true-size colour and grayscale inspection preserves the 15-second reading path: capacity -> retained solid -> remaining area -> reaction redistribution -> through-plane profile.
- PASS — no graphic element implies microscopy, deposit shape, unique coverage geometry or a resolved pore-blocking front.

## Typography, export and determinism

- PASS — final page is exactly 180 x 155 mm.
- PASS — every explicit font size is at least 6.5 pt.
- PASS — the renderer registers the manuscript-matched TeX Gyre Termes Regular, Bold, Italic and Bold Italic OTF files directly.
- PASS — `pdffonts` reports only embedded TeXGyreTermes Regular, Bold and Italic; no Type 3, Arial, Helvetica, DejaVu, Liberation, Calibri or Times New Roman font is present.
- PASS — SVG contains 73 editable text nodes and no text-to-path conversion.
- PASS — PNG is 2,125 x 1,830 px at 300 dpi; opaque RGB TIFF is 4,251 x 3,661 px at 600 dpi.
- PASS — two consecutive renders after the final line-style and label changes produced byte-identical hashes for all six visual outputs.

## Stable hashes

- SVG: `8FB54702A0610B4BF6E6E1D46B8C554F11929569E104995FFD83C9F0691DC847`
- PDF: `50282811313DD953A5014B4DC68A09AD46E05173ECD029F655FDAA85A25CDA10`
- PNG: `8488DEA6C2D3CF7D2292359BE04308C449CF3B3A8DF80E89A929131E8FFE75D7`
- TIFF: `4DD8192B59F7B16DD43AEE4B6A068D7C7522B8C00391AE3E24633D452D2FD6B8`
- 180 mm preview: `7B071FE67277B04E4048E00041175CF16B79ED69BB83123E7C21EA90EEC6AC47`
- grayscale QA: `645BC8DF7C1998005CDA9E760A2827CB26C9F07FE5EC763D973C4589B12FA0EE`
- source subset: `9BF270D14155441D68B300E0FAAAF50E9DAB84DFA4B7EEAB28C231085FCB283C`

