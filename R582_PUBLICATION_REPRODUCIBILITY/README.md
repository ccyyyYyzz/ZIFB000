
# R582 ZIFB positive-electrode reproducibility package

This directory is the local release candidate for the manuscript
*A positive-electrode model separating iodine saturation from accessibility loss in
zinc--iodine flow batteries*.

The scientific subject is the porous **ZIFB positive electrode**. NH4Br is one
representative supporting electrolyte and is not the organizing subject of the work.
Bromide participates only through the declared supporting/speciation treatment; the
modeled faradaic couple is I2/I-.

Legacy experimental filenames and condition labels containing `NH4Cl` or `NH4CL`
are metadata-entry errors. The project owner confirmed that all affected experiments
used NH4Br. Raw filenames and hashes remain unchanged; the correction is registered
as `EXP-META-001` under `metadata_corrections/EXP-META-001/`.

## Contents

- `manuscript/`: exact R582 TeX, bibliography and compiled PDFs used for this snapshot.
- `manuscript/figures_R582/`: exactly six main and thirteen SI figures in PDF, SVG,
  PNG and TIFF.
- `manuscript/source_data/`: plotted tables, registered derived inputs, deterministic
  renderers, manifests, captions, contracts and QA records for all 19 figures.
- `molecular_models/md_soc_series/`: the ten exact 5-SOC x 2-parameterization MD
  identities, including per-case topology, all local ITP/MDP files and GROMACS logs.
- `molecular_models/cp2k_single_i2/`: the adopted single-I2 CP2K input/output and
  geometry identities for C-OH, C=O, basal and vacancy calculations.
- `continuum_model_identity/`: small scripts, exported tables and manifests that
  identify the selected positive-electrode continuum branch. No `.mph` is embedded.
- `metadata_corrections/EXP-META-001/`: the operator-confirmed NH4Cl-to-NH4Br
  metadata mapping and immutable raw-file hashes; no raw acquisition file is included.
- `submission/` and `audit/`: journal-facing supporting files and release QA records.
- `FILE_SHA256_MANIFEST.csv` and `PACKAGE_DIGESTS.json`: package integrity records.

## Scope boundary

The release supports separation of free-I2 saturation, retained solid-I2 inventory
and calibrated accessibility loss. It does not identify deposit morphology, coverage
or an electrical-potential field unless that quantity is explicitly present in a
registered export. Molecular and mesoscale calculations are bounded priors or
comparators, not independent validation of internal continuum states.

Raw experimental acquisition files and original COMSOL `.mph` files are deliberately
excluded. Their identities are recorded by SHA-256 where they enter the evidence
chain. The unrelated `E:/ns_mc_gan_gi_code` project is outside scope.

## Verify

From this directory:

```powershell
python tools/verify_release.py .
```

See `REPRODUCE.md` for figure, manuscript, MD and CP2K reproduction boundaries.

## Release identity

This snapshot is prepared for the immutable tag `r582-zifb-positive-electrode-reproducibility-v1` and release title
`R582 ZIFB positive-electrode reproducibility package v1`. No DOI is claimed. `RELEASE_PLAN.md` records the exact tagged-tree
and release URLs. The tagged-tree URL identifies this package only when the tag
resolves to the manifest-verified commit; `BUILD_METADATA.json` retains the factual
pre-publication assembly state.
