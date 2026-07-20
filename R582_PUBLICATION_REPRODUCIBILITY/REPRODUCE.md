
# Reproduction and audit order

## 1. Verify the snapshot

Run `python tools/verify_release.py .`. The verifier checks every SHA-256 entry,
the 19-figure identity, MD/CP2K manifests, forbidden-file rules, and GitHub size limits.

## 2. Rebuild the figures

Each directory under `manuscript/source_data/` retains its deterministic Python
entry point and local source tables. Run a renderer from the package root using the
environment declared under `submission/`. The directory layout matches the active
workspace layout, so outputs are written to `manuscript/figures_R582/`.

`submission/REPRODUCIBILITY_ENVIRONMENT.md` gives the unambiguous package-relative
command for all 17 active renderer entries (19 figures; one entry produces S7--S9),
the font-discovery environment variables, and the exact four-face SHA-256 lock.

The renderers require the four TeX Gyre Termes OTF files distributed by TeX Live;
the shared runtime validates every face against the frozen hashes before matplotlib
registration. This font family matches the `tgtermes` manuscript body. Do not
substitute Arial, Helvetica, DejaVu, Liberation, Calibri, Times New Roman or a Type 3
fallback.

## 3. Compile the documents

With TeX Live 2024 or later, from `manuscript/`:

```powershell
latexmk -norc -pdf -interaction=nonstopmode -halt-on-error SI_R582.tex
latexmk -norc -pdf -interaction=nonstopmode -halt-on-error main_R582.tex
latexmk -norc -pdf -interaction=nonstopmode -halt-on-error SI_R582.tex
latexmk -norc -pdf -interaction=nonstopmode -halt-on-error main_R582.tex
```

Auxiliary and log files are generated locally and are intentionally absent from the
release.

## 4. MD identity and result boundary

`molecular_models/md_soc_series/cases/` contains all ten executed cases. Each case
includes the exact `topol.top`, all six local `.itp` files, all four stage `.mdp`
files, generated `mdout.mdp`, system metadata, preprocessing logs and the non-empty
GROMACS EM/NVT/NPT/production logs. `MD_CASE_IDENTITY_MANIFEST.csv` binds every copy
to its original workspace-relative path and SHA-256.

The trajectories, checkpoints and energy files are not duplicated in this compact
Git repository. The original artifact manifests and selected derived tables are under
`molecular_models/md_soc_series/results/`. These calculations provide a bulk,
force-field-dependent carrier-mobility prior. The five SOC compositions are different
conditions, and contiguous trajectory blocks are not independent replicates.

## 5. CP2K identity and result boundary

`molecular_models/cp2k_single_i2/CP2K_SINGLE_I2_IDENTITY_MANIFEST.csv` identifies
the adopted C-OH, C=O, basal and vacancy geometry/energy records. Exact CP2K inputs
and outputs are copied below `records/` without modification. CP2K basis and potential
libraries remain standard external runtime dependencies.

The resulting finite-periodic-cell electronic energies are placement tendencies;
they are not solution free energies, site populations, nucleation barriers or a
reaction coordinate.

## 6. Continuum-model boundary

The package contains scripts, manifests and small exported derived tables. Original
COMSOL `.mph` files are excluded. A full rerun therefore requires COMSOL 6.3 and the
immutable model copy whose byte size and SHA-256 are recorded in the included model
identity manifests. Never overwrite the original model; operate on a copied file and
save every result under a new name.

## 7. Experimental metadata boundary

No raw `.ndax` acquisition file is included. `EXP-META-001` records the immutable
hash and legacy name for every affected raw-file identity. It corrects only the
display/analysis identity from legacy NH4Cl/NH4CL to NH4Br; it does not rename raw
files or create new experimental evidence.
