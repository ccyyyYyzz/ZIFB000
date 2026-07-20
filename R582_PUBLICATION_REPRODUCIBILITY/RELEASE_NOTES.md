
# R582 ZIFB positive-electrode reproducibility package v1

This tag freezes the publication-facing R582 evidence and reproducibility package for
*A positive-electrode model separating iodine saturation from accessibility loss in
zinc--iodine flow batteries*.

The scientific subject is the porous ZIFB positive electrode. NH4Br is one
representative supporting electrolyte, not the organizing subject of the work.
`EXP-META-001` records the operator-confirmed correction that legacy NH4Cl/NH4CL
labels denote NH4Br while preserving raw filenames and hashes.

## Included

- exact main-manuscript and Supplementary Information TeX/PDF snapshots;
- six main and thirteen supplementary figures in PDF, SVG, PNG and TIFF;
- plotted source tables, deterministic renderers, manifests and QA records;
- exact ten-case GROMACS topology/protocol/log identities and adopted single-I2 CP2K
  input/output identities;
- continuum-model scripts, exported tables, branch identities and registered hashes;
- citation, language, layout, font and release-integrity audit records.

## Availability boundary

Raw acquisition files, molecular trajectories and original solved COMSOL `.mph`
files are not duplicated in this lightweight Git repository. Their registered
identities, SHA-256 hashes and reproduction boundaries are documented in the package.
No deposit morphology, microscopic coverage or unexported electrical-potential field
is inferred. No repository DOI is assigned or claimed.

## Verify

From `R582_PUBLICATION_REPRODUCIBILITY/`, run:

```powershell
python tools/verify_release.py .
```

The intended immutable tag is `r582-zifb-positive-electrode-reproducibility-v1`. The tagged package URL is
https://github.com/ccyyyYyzz/ZIFB000/tree/r582-zifb-positive-electrode-reproducibility-v1/R582_PUBLICATION_REPRODUCIBILITY.
