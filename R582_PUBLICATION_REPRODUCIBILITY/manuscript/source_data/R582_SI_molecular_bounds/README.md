# R582 Supplementary Figures S7-S9 source bundle

This bundle rebuilds the molecular-bound supplementary artwork without
modifying original DFT/MD files or either manuscript TeX source.

## Deliverables

- `Fig_R582_SI07_single_I2_ordering`: single-I2 adsorption-energy hero plus four exact
  optimized geometries; no single-I2 CDD.
- `Fig_R582_SI08_two_I2_diagnostic`: compact/separated energy, exact
  geometries and the recoverable true two-I2 CDD; no pathway cartoon.
- `Fig_R582_SI09_md_carrier_ladder`: full eight-species ladder for q=0.8 ECC
  and q=1.0 formal charges.

Each stem has editable SVG/PDF, opaque 600-dpi RGB PNG/TIFF, a 180-mm colour
preview and a 180-mm grayscale preview under `manuscript/figures_R582/`.

## Rebuild and QA

```powershell
python manuscript/source_data/R582_SI_molecular_bounds/make_r582_si_molecular_figures.py --figure all
python manuscript/source_data/R582_SI_molecular_bounds/check_r582_si_molecular_figures.py
```

The renderer validates every frozen input and the four exact TeX Gyre Termes
OTFs before drawing. The QA script checks dimensions, editable text, minimum
font size, font-family exclusivity, Type 3 exclusion, raster mode/resolution,
scientific value preservation and the evidence-class boundaries.

## Source records

- `R582_SI_molecular_input_manifest.csv`: original-to-frozen-copy map and
  SHA-256 hashes.
- `R582_SI_molecular_output_manifest.csv`: figure and plotted-table hashes.
- `R582_SI_molecular_render_manifest.json`: backend, sizing, font and
  figure-specific render identities.
- `R582_SI_molecular_QA.json`: automated acceptance results.
- `R582_SI07_*`, `R582_SI08_*`, `R582_SI09_*`: clean plotted data, displayed
  atom coordinates, geometry metrics and CDD threshold points.
- `FIGURE_CONTRACTS.md`, `CAPTIONS_DRAFT.md`, `EVIDENCE_BOUNDARIES.md` and
  `QA_NOTES.md`: claim logic, caption text and interpretation limits.

The figures are `E-COMP` evidence only. Electronic energies are not solution
free energies or nucleation barriers; the CDD is not a reaction coordinate;
and the MD block bars are within-trajectory stability, not replicate
uncertainty. The calculations bound model inputs for the ZIFB positive
electrode and do not make the representative supporting electrolyte the
article subject.
