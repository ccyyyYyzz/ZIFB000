# ZIFB positive-electrode modeling and reproducibility archive

This repository supports the manuscript *A positive-electrode model separating
iodine saturation from accessibility loss in zinc--iodine flow batteries*.

The scientific subject is the porous **zinc--iodine flow-battery (ZIFB) positive
electrode**. The work separates three quantities that a full-cell voltage does not
identify independently: free-I2 saturation, retained solid-I2 inventory, and the
remaining calibrated electrochemically accessible area.

NH4Br is one representative supporting electrolyte in the studied condition; it is
not the organizing subject of the paper. Bromide enters only through the declared
supporting/speciation treatment, while the modeled faradaic couple is I2/I-.

## Current publication package

`R582_PUBLICATION_REPRODUCIBILITY/` is the authoritative local publication-facing
candidate. It contains:

- exact R582 manuscript and Supplementary Information sources and PDFs;
- the six main and thirteen SI figures in vector and raster formats;
- plotted source data, deterministic figure scripts, manifests and QA records;
- exact MD topology/protocol/log identities for five SOC compositions under two
  charge parameterizations;
- exact adopted single-I2 CP2K input/output identities;
- small positive-electrode continuum-model scripts, exports and identity records;
- journal-facing submission files and deterministic SHA-256 verification tools.

Run the packaged verifier before using the snapshot:

```powershell
python R582_PUBLICATION_REPRODUCIBILITY/tools/verify_release.py R582_PUBLICATION_REPRODUCIBILITY
```

## Experimental metadata correction

Legacy acquisition filenames and condition fields containing `NH4Cl` or `NH4CL`
are metadata-entry errors. The project owner/experimenter confirmed that all affected
experiments used NH4Br. Raw filenames and file hashes remain unchanged; the processed
identity correction is registered as `EXP-META-001` in the R582 package.

No raw experimental acquisition file is stored in this lightweight repository.

## Evidence boundary

The registered spatial exports support only the fields they explicitly contain.
Neither deposit morphology nor microscopic coverage is inferred from those exports,
and electrical potential is not claimed where it was not exported. Molecular and
mesoscale calculations provide bounded priors or comparators rather than independent
validation of internal continuum states.

Original COMSOL `.mph` files are excluded. The package records their relevant byte
sizes and SHA-256 identities, and all COMSOL work must be performed on copied files.
The unrelated `E:/ns_mc_gan_gi_code` project is outside scope.

## Repository history

Directories predating R582 are retained only as historical records. They are not the
authority for the current manuscript, claims, figure set or data-availability text.
Use the R582 package and its manifests for publication review.

## Release identity

The publication package is frozen under the release-specific tag
`r582-zifb-positive-electrode-reproducibility-v1`. At that tag, the R582 directory is
the authoritative publication-facing snapshot. The exact tree/release URLs and
verification procedure are documented inside
`R582_PUBLICATION_REPRODUCIBILITY/RELEASE_PLAN.md`. No repository DOI is claimed.
