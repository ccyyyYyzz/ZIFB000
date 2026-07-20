# R582 SI Figure S3 QA

Status: source, semantic and visual review passed; release hashes are recorded
in `R582_SIFig_S3_render_manifest.json` and the determinism record.

- Both frozen input hashes verified before rendering.
- The primary panel contains exactly four 85% rows and matches the independently
  loaded 85% rows of `endpoint_sensitivity.csv` for thickness, last pass and
  first fail.
- The sensitivity table contains exactly 4 thicknesses × 3 thresholds
  (80/85/90%). No endpoint is right-censored.
- Every thickness has `n_cell=1`; no cycle is treated as an independent
  replicate and no population interval is drawn.
- Only the 1.5/2.5/3.0 mm March 2025 explicit cells are connected. The 2.0 mm
  proxy is open and unconnected in both panels.
- Brackets are labelled as observed program intervals, not confidence
  intervals. No pore law, morphology or universal thickness law is inferred.
- TeX Gyre Termes is loaded from the four declared OTF faces; the renderer
  rejects text below 6.5 pt or a resolved fallback family.
- Colour and grayscale previews were inspected at 180 mm. Thresholds remain
  separable by line style and marker shape.
- `pdffonts` passed: the PDF contains only embedded, subset
  TeXGyreTermes-Regular/Bold CID fonts; no Type 3 or forbidden family.
- The TIFF is opaque RGB, 4251 × 2267 pixels, with 600 dpi metadata.
- Two consecutive complete renders reproduced identical hashes for SVG, PDF,
  PNG, TIFF and both previews. Exact values are frozen in
  `DETERMINISM_QA.json`.
