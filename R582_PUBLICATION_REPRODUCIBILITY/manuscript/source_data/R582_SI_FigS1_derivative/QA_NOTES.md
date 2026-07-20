# R582 SI Figure S1 QA

Status: source, semantic and visual review passed; release hashes are recorded
in `R582_SIFig_S1_render_manifest.json` and the determinism record.

- Frozen input hashes verified before rendering.
- One unique physical-cell record retained; eligible cycles are exactly
  20–23; windows are exactly 5.25/10.25/15.25 mAh cm−2.
- All 5,709 registered curve rows and all 12 landmark rows are preserved in
  plotted source tables; no best cycle is selected.
- Axes are identical across the four panels. Negative and terminal derivative
  excursions remain signed and visible.
- Filled triangles use the registered maximum-search interval, not the visual
  maximum of any boundary fluctuation.
- TeX Gyre Termes is loaded from the four declared OTF faces; the renderer
  rejects text below 6.5 pt or a resolved fallback family.
- Colour and grayscale previews were inspected at 180 mm. The three windows
  remain separable by line style and direct labels.
- `pdffonts` passed: the PDF contains only embedded, subset
  TeXGyreTermes-Regular/Bold CID fonts; no Type 3 or forbidden family.
- The TIFF is opaque RGB, 4251 × 2881 pixels, with 600 dpi metadata.
- Two consecutive complete renders reproduced identical hashes for SVG, PDF,
  PNG, TIFF and both previews. Exact values are frozen in
  `DETERMINISM_QA.json`.
