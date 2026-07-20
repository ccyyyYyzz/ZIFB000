# R582 SI Figure S2 QA

Status: source, semantic and visual review passed; release hashes are recorded
in `R582_SIFig_S2_render_manifest.json` and the determinism record.

- Frozen panel and upstream-manifest hashes verified before rendering.
- Exactly six unique physical-cell summaries retained; physical-cell counts by
  concentration are exactly 1/1/1/2/1.
- The plot table contains no raw filename. Its electrolyte label is NH4Br and
  the metadata normalization is linked to `EXP-META-001`.
- Marker means physical cell; vertical segment means full sequential-cycle
  range; black bar means condition median. No population interval is drawn.
- The two 3 M cells remain separate. The condition-level source records one
  right-censored endpoint and the artwork states this without inventing an
  unregistered censor marker.
- No line, fit, optimum or dose-response law is drawn.
- TeX Gyre Termes is loaded from the four declared OTF faces; the renderer
  rejects text below 6.5 pt or a resolved fallback family.
- Colour and grayscale previews were inspected at 180 mm.
- `pdffonts` passed: the PDF contains only embedded, subset
  TeXGyreTermes-Regular/Bold CID fonts; no Type 3 or forbidden family.
- The TIFF is opaque RGB, 4251 × 1937 pixels, with 600 dpi metadata.
- Two consecutive complete renders reproduced identical hashes for SVG, PDF,
  PNG, TIFF and both previews. Exact values are frozen in
  `DETERMINISM_QA.json`.
