# R582 SI Figures S7-S9 acceptance record

Status: **PASS**.  The automated record contains 93 passing checks in
`R582_SI_molecular_QA.json`.

## Figure and font gates

- Final dimensions are exact: S7 is 180 x 120 mm, S8 is 180 x 112 mm and S9 is
  180 x 96 mm.
- Each PDF contains only embedded TeXGyreTermes Regular/Bold/Italic subsets as
  required by its text content.  No Type 3, Arial, Helvetica, DejaVu,
  Computer Modern, STIX or Times New Roman font is present.
- Every SVG retains editable `<text>` elements and every font declaration is
  TeX Gyre Termes.  The minimum ordinary text is 6.5 pt.  Mathematical parent
  text is 9.4 pt, so automatically scaled scripts are 6.58 pt rather than the
  noncompliant 5.04 pt produced by a 7.2 pt math parent.
- The four exact TeX Live OTF files and hashes are recorded in the input
  manifest. `svg.fonttype = none`, `pdf.fonttype = 42` and `ps.fonttype = 42`
  are locked in the renderer. Poppler identifies the embedded OTF subsets as
  CID Type 0C (OT); there are no Type 3 fonts.
- PNG and TIFF deliverables are opaque RGB at 600 dpi. The 150 dpi colour and
  grayscale previews preserve the exact placed dimensions.

## Evidence and image-integrity gates

- Sixteen minimal DFT/MD inputs are frozen as byte-identical copies under
  `registered_inputs/`; four font files are hash-locked in place. The input
  manifest contains 20 SHA-256 rows.
- S7 is drawn from the accepted energy CSV and four exact XYZ files. No legacy
  raster, single-I2 CDD or PDOS panel is imported.
- S8 is drawn from the accepted energy CSV, two exact XYZ files, the registered
  `(60, 96, 90)` float32 CDD array and its CP2K cell. At the fixed absolute
  threshold of 0.002 e A^-3, all 428 accumulation and 78 depletion grid points
  remain visible after value-preserving periodic display mapping. There is no
  interpolation, invented isosurface, pathway arrow or association cartoon.
- S9 retains all eight species, both charge parameterizations and all five SOC
  compositions. Range bars are composition ranges; capped bars are propagated
  within-trajectory block stability. The artwork and caption never call them
  replica uncertainty.
- Geometry coordinates are unchanged. Local cropping, fixed orthographic
  projection, minimum-distance I2 pairing and the non-I adjacency cutoff are
  recorded in clean source tables. Element colors also use distinct shapes for
  grayscale legibility.

## Visual and reproducibility gates

- Actual-size colour inspection: PASS.
- Actual-size grayscale inspection: PASS.
- Panel labels, title collisions, axes, units, legends and CDD sign key: PASS.
- Grayscale redundancy: S7 element shapes; S8 CDD circle/triangle signs; S9
  filled-circle/open-diamond parameterizations: PASS.
- Cold rerender determinism: 15 selected PDF/SVG/PNG/TIFF and plotted-data
  artifacts were byte-identical before and after a complete rerun.

## Frozen PDF hashes

- S7 PDF: `DFFBDD891CFA0F952CBD147AA1DF3D4CE335236DC6498580DDE043348D1CE7A0`
- S8 PDF: `AA1D6A287A3D80533E0D118562401A2348045171FC4066AAA59DAA32DC879372`
- S9 PDF: `C5E9E6E7F0BF2B3E47F8B74074B89E8DC7259B0DB0C7EAAF83C52AF85CC0E7C5`

Run from the project root:

```powershell
python manuscript/source_data/R582_SI_molecular_bounds/make_r582_si_molecular_figures.py --figure all
python manuscript/source_data/R582_SI_molecular_bounds/check_r582_si_molecular_figures.py
```

