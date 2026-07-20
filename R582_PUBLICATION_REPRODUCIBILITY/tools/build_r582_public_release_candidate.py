#!/usr/bin/env python3
"""Build the local R582 publication-facing reproducibility candidate.

The build is whitelist-only.  It copies derived/public artifacts, exact model
identity records, and small reproducibility inputs into the local GitHub clone.
It never copies raw experimental acquisition files or COMSOL ``.mph`` files,
and it performs no git, GitHub, DOI, or network operation.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


BUILD_VERSION = "1.0.0-rc"
PACKAGE_NAME = "R582_PUBLICATION_REPRODUCIBILITY"
TAG_NAME = "r582-zifb-positive-electrode-reproducibility-v1"
RELEASE_TITLE = "R582 ZIFB positive-electrode reproducibility package v1"
REPOSITORY_URL = "https://github.com/ccyyyYyzz/ZIFB000"
TAG_TREE_URL = f"{REPOSITORY_URL}/tree/{TAG_NAME}/{PACKAGE_NAME}"
RELEASE_URL = f"{REPOSITORY_URL}/releases/tag/{TAG_NAME}"

GITHUB_WARNING_BYTES = 50 * 1024 * 1024
GITHUB_HARD_BYTES = 100 * 1024 * 1024

MAIN_SOURCE_BUNDLES = {
    "Fig_R582_experimental_problem": "R582_Fig1_experimental_problem",
    "Fig_R582_domain_state_v2": "R582_Fig2_domain_state",
    "Fig_R582_spatial_progression_v3": "R582_Fig3_spatial_progression",
    "Fig_R582_closure_identifiability": "R582_Fig4_closure_identifiability",
    "Fig_R582_multiscale_bounds_v2": "R582_Fig5_multiscale_bounds",
    "Fig_R582_operating_levers_v2": "R582_Fig6_operating_levers_v2",
}

SI_SOURCE_BUNDLES = {
    "SIFig_R582_S1_derivative": "R582_SI_FigS1_derivative",
    "SIFig_R582_S2_composition": "R582_SI_FigS2_composition",
    "SIFig_R582_S3_compression": "R582_SI_FigS3_compression",
    "Fig_SI_R582_S4_state_function_fields": "R582_SI_FigS4_state_function_fields",
    "Fig_SI_R582_S5_hydraulic_fields": "R582_SI_FigS5_hydraulic_fields",
    "SIFig_R582_S6_voltage_degeneracy": "R582_SI_FigS6_voltage_degeneracy",
    "Fig_R582_SI07_single_I2_ordering": "R582_SI_molecular_bounds",
    "Fig_R582_SI08_two_I2_diagnostic": "R582_SI_molecular_bounds",
    "Fig_R582_SI09_md_carrier_ladder": "R582_SI_molecular_bounds",
    "SIFig_R582_S10_comparator_definitions": "R582_SI_FigS10_comparator_definitions",
    "SIFig_R582_S11_accessibility_families": "R582_SI_FigS11_accessibility_families",
    "SIFig_R582_S12_flow_postprocess": "R582_SI_FigS12_flow_postprocess",
    "SIFig_R582_S13_smooth_permeability": "R582_SI_FigS13_smooth_permeability",
}

FIGURE_FORMATS = (".pdf", ".svg", ".png", ".tiff")
MD_CASES = [
    f"soc{soc}_{charge}-long"
    for soc in ("010", "030", "050", "070", "100")
    for charge in ("q0p8_ecc", "q1p0")
]
MD_REQUIRED_ITP = {
    "i2.itp",
    "i2br.itp",
    "i3.itp",
    "ions_scaled.itp",
    "local_spce_atomtypes.itp",
    "nh4.itp",
}
MD_REQUIRED_MDP = {"em.mdp", "npt_long.mdp", "nvt_long.mdp", "prod_long.mdp"}
MD_GROMACS_LOGS = (
    "editconf.log",
    "grompp_em.log",
    "grompp_npt.log",
    "grompp_nvt.log",
    "grompp_prod.log",
    "em.log",
    "nvt.log",
    "npt.log",
    "prod.log",
)

CP2K_BASE_REL = Path(
    "DFT/06_periodic_cp2k_single_i2_r514/workspace_snapshot/outputs/"
    "ec2_sanity_recovered_20260619/204745/cp2k_adsorption_heterogeneity"
)
CP2K_RECORDS = [
    ("reference", "reference", "cp2k_inputs/sp/i2_reference_d3_sp.inp"),
    ("reference", "reference", "cp2k_outputs/sp/i2_reference_d3_sp.out"),
    ("basal", "geometry", "structures/basal_pristine_periodic_slab_i2_from_geo_opt_selected.xyz"),
    ("basal", "bare_sp", "cp2k_inputs/sp/basal_pristine_periodic_slab_bare_surface_d3_sp.inp"),
    ("basal", "bare_sp", "cp2k_outputs/sp/basal_pristine_periodic_slab_bare_surface_d3_sp.out"),
    ("basal", "complex_sp", "cp2k_inputs/sp/basal_pristine_periodic_slab_complex_d3_sp_from_geo_opt.inp"),
    ("basal", "complex_sp", "cp2k_outputs/sp/basal_pristine_periodic_slab_complex_d3_sp_from_geo_opt.out"),
    ("basal", "bsse", "cp2k_inputs/bsse/basal_pristine_periodic_slab_pbe_bsse_counterpoise_from_geo_opt.inp"),
    ("basal", "bsse", "cp2k_outputs/bsse/basal_pristine_periodic_slab_pbe_bsse_counterpoise_from_geo_opt.out"),
    ("C-OH", "geometry", "structures/OH_functionalized_basal_periodic_slab_i2_from_geo_opt_selected.xyz"),
    ("C-OH", "bare_sp", "cp2k_inputs/sp/OH_functionalized_basal_periodic_slab_bare_surface_d3_sp.inp"),
    ("C-OH", "bare_sp", "cp2k_outputs/sp/OH_functionalized_basal_periodic_slab_bare_surface_d3_sp.out"),
    ("C-OH", "complex_sp", "cp2k_inputs/sp/OH_functionalized_basal_periodic_slab_complex_d3_sp_from_geo_opt.inp"),
    ("C-OH", "complex_sp", "cp2k_outputs/sp/OH_functionalized_basal_periodic_slab_complex_d3_sp_from_geo_opt.out"),
    ("C-OH", "bsse", "cp2k_inputs/bsse/OH_functionalized_basal_periodic_slab_pbe_bsse_counterpoise_from_geo_opt.inp"),
    ("C-OH", "bsse", "cp2k_outputs/bsse/OH_functionalized_basal_periodic_slab_pbe_bsse_counterpoise_from_geo_opt.out"),
    ("C=O", "geometry", "structures/carbonyl_edge_periodic_ribbon_sanity_selected.xyz"),
    ("C=O", "geo_opt", "cp2k_inputs/sanity/geo_opt/carbonyl_sanity_end_on_O_vertical_geo_opt.inp"),
    ("C=O", "geo_opt", "cp2k_outputs/sanity/geo_opt/carbonyl_sanity_end_on_O_vertical_geo_opt.out"),
    ("C=O", "bare_sp", "cp2k_inputs/sanity/sp/carbonyl_edge_periodic_ribbon_sanity_bare_surface_sp.inp"),
    ("C=O", "bare_sp", "cp2k_outputs/sanity/sp/carbonyl_edge_periodic_ribbon_sanity_bare_surface_sp.out"),
    ("C=O", "complex_sp", "cp2k_inputs/sanity/sp/carbonyl_edge_periodic_ribbon_sanity_optimized_complex_sp.inp"),
    ("C=O", "complex_sp", "cp2k_outputs/sanity/sp/carbonyl_edge_periodic_ribbon_sanity_optimized_complex_sp.out"),
    ("C=O", "bsse", "cp2k_inputs/sanity/bsse/carbonyl_edge_periodic_ribbon_sanity_optimized_bsse.inp"),
    ("C=O", "bsse", "cp2k_outputs/sanity/bsse/carbonyl_edge_periodic_ribbon_sanity_optimized_bsse.out"),
    ("vacancy", "geometry", "structures/single_vacancy_periodic_slab_sanity_selected.xyz"),
    ("vacancy", "geo_opt", "cp2k_inputs/sanity/geo_opt/single_vacancy_sanity_bs_smear_geo_opt.inp"),
    ("vacancy", "geo_opt", "cp2k_outputs/sanity/geo_opt/single_vacancy_sanity_bs_smear_geo_opt.out"),
    ("vacancy", "bare_sp", "cp2k_inputs/sanity/sp/single_vacancy_periodic_slab_sanity_bare_surface_sp.inp"),
    ("vacancy", "bare_sp", "cp2k_outputs/sanity/sp/single_vacancy_periodic_slab_sanity_bare_surface_sp.out"),
    ("vacancy", "complex_sp", "cp2k_inputs/sanity/sp/single_vacancy_periodic_slab_sanity_optimized_complex_sp.inp"),
    ("vacancy", "complex_sp", "cp2k_outputs/sanity/sp/single_vacancy_periodic_slab_sanity_optimized_complex_sp.out"),
    ("vacancy", "bsse", "cp2k_inputs/sanity/bsse/single_vacancy_periodic_slab_sanity_optimized_bsse.inp"),
    ("vacancy", "bsse", "cp2k_outputs/sanity/bsse/single_vacancy_periodic_slab_sanity_optimized_bsse.out"),
]

SECRET_PATTERNS = {
    "private_key": re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "github_token": re.compile(rb"(?:ghp|github_pat)_[A-Za-z0-9_]{20,}"),
    "aws_access_key": re.compile(rb"AKIA[0-9A-Z]{16}"),
    "openai_key": re.compile(rb"sk-[A-Za-z0-9_-]{24,}"),
    "google_api_key": re.compile(rb"AIza[0-9A-Za-z_-]{30,}"),
}


def locate_workspace() -> Path:
    env = os.environ.get("ZIFB_PROJECT_ROOT")
    candidates = [Path(env)] if env else []
    candidates.extend(Path(__file__).resolve().parents)
    for candidate in candidates:
        if (
            (candidate / "manuscript" / "main_R582.tex").is_file()
            and (candidate / "github_ZIFB000_working" / ".git").exists()
        ):
            return candidate.resolve()
    raise RuntimeError(
        "Cannot locate the ZIFB workspace. Set ZIFB_PROJECT_ROOT to the project root."
    )


ROOT = locate_workspace()
MANUSCRIPT = ROOT / "manuscript"
REPO = ROOT / "github_ZIFB000_working"
TARGET = REPO / PACKAGE_NAME
STAGING = REPO / f".{PACKAGE_NAME}.staging"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def workspace_rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def package_rel(path: Path) -> str:
    return path.resolve().relative_to(STAGING.resolve()).as_posix()


def assert_safe_build_path(path: Path) -> None:
    resolved = path.resolve()
    repo = REPO.resolve()
    if resolved.parent != repo or resolved.name not in {
        PACKAGE_NAME,
        f".{PACKAGE_NAME}.staging",
    }:
        raise RuntimeError(f"Refusing unsafe package reset: {resolved}")


def safe_reset(path: Path) -> None:
    assert_safe_build_path(path)
    for attempt in range(8):
        if not path.exists():
            return
        try:
            shutil.rmtree(path)
            return
        except PermissionError:
            if attempt == 7:
                raise
            # Windows scanners or a concurrent read-only verifier can hold a
            # file handle briefly.  Retry only this generated, path-validated
            # package directory; never widen the deletion scope.
            time.sleep(0.5 * (attempt + 1))


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def copy_one(source: Path, destination: Path, provenance: list[dict[str, object]]) -> None:
    if not source.is_file():
        raise FileNotFoundError(source)
    size = source.stat().st_size
    if size >= GITHUB_HARD_BYTES:
        raise RuntimeError(f"GitHub hard-limit file excluded: {source} ({size} bytes)")
    digest = sha256(source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    copied_digest = sha256(destination)
    if copied_digest != digest:
        raise RuntimeError(f"Copy hash mismatch: {source}")
    provenance.append(
        {
            "source_workspace_path": workspace_rel(source),
            "package_path": package_rel(destination),
            "bytes": size,
            "sha256": digest,
        }
    )


def parse_figures(tex_path: Path) -> list[str]:
    text = tex_path.read_text(encoding="utf-8")
    return [
        Path(match).stem
        for match in re.findall(r"\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}", text)
    ]


def include_source_file(path: Path) -> bool:
    lowered_parts = {part.lower() for part in path.parts}
    lowered_name = path.name.lower()
    if "__pycache__" in lowered_parts or path.suffix.lower() in {".pyc", ".pyo", ".log"}:
        return False
    if any(token in lowered_name for token in ("preview", "grayscale")):
        return False
    if lowered_name in {"thumbs.db", ".ds_store"}:
        return False
    return True


def include_active_bundle_file(bundle: str, path: Path) -> bool:
    """Retain only the active version where a working bundle contains revisions."""
    if not include_source_file(path):
        return False
    name = path.name
    if bundle == "R582_Fig2_domain_state":
        return "v2" in name.lower() or name == "R582_domain_state_v2.py"
    if bundle == "R582_Fig3_spatial_progression":
        return "v3" in name.lower()
    if bundle == "R582_Fig5_multiscale_bounds":
        if name == "make_fig_r582_multiscale_bounds.py":
            return True  # hash-locked import dependency of the active v2 renderer
        return "v2" in name.lower() or name == "EVIDENCE_AND_PROVENANCE.md"
    return True


def copy_tree_filtered(
    source_root: Path,
    destination_root: Path,
    provenance: list[dict[str, object]],
    predicate=include_source_file,
) -> None:
    if not source_root.is_dir():
        raise FileNotFoundError(source_root)
    for source in sorted(source_root.rglob("*")):
        if source.is_file() and predicate(source):
            copy_one(source, destination_root / source.relative_to(source_root), provenance)


def build_readme() -> str:
    return f"""
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

This snapshot is prepared for the immutable tag `{TAG_NAME}` and release title
`{RELEASE_TITLE}`. No DOI is claimed. `RELEASE_PLAN.md` records the exact tagged-tree
and release URLs. The tagged-tree URL identifies this package only when the tag
resolves to the manifest-verified commit; `BUILD_METADATA.json` retains the factual
pre-publication assembly state.
"""


def build_reproduce() -> str:
    return """
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
"""


def build_release_plan() -> str:
    return f"""
# Immutable release identity and publication checklist

- Tag: `{TAG_NAME}`
- Release title: `{RELEASE_TITLE}`
- Stable tagged-directory URL: `{TAG_TREE_URL}`
- Release URL: `{RELEASE_URL}`

Neither URL is publication-valid until the approved commit is pushed, the tag is
created at that exact commit, and the release is published.

Before publication, enable GitHub release immutability for the repository. Then:

1. cold-build and verify main/SI;
2. rerun the R582 candidate builder and verifier;
3. review `DRY_RUN_RELEASE_REPORT.md` and all human-only metadata fields;
4. commit and push the approved snapshot;
5. create a draft release for `{TAG_NAME}` and attach any final archive asset;
6. publish the release and confirm that GitHub marks it `Immutable`;
7. verify the release/tag and confirm that the tagged-directory URL already embedded
   in the manuscript Data Availability statement resolves to this exact commit.

No DOI is assigned or implied by this plan.
"""


def build_data_availability() -> str:
    return f"""
# Data Availability status

Status: `tag_url_embedded_pending_publication_verification` until the immutable tag
and release resolve publicly. No URL placeholder remains in the manuscript.

## Ready-to-paste text after publication and URL verification

The processed source data underlying all main and supplementary figures, figure-
generation code, manuscript and Supplementary Information sources, and the registered
model input/output identities are available in the immutable R582 reproducibility
release at {TAG_TREE_URL}. Legacy experimental records labelled NH4Cl correspond to
NH4Br under the operator-confirmed metadata correction EXP-META-001; raw filenames and
hashes are preserved in the release manifest. Original experimental acquisition files
and COMSOL model files are not duplicated in the lightweight Git repository; their
registered identities and SHA-256 hashes are provided for traceability.

The manuscript already embeds this exact tagged URL. It becomes an active public
record only when the tag resolves to the manifest-verified release commit. No DOI is
available or claimed.
"""


def build_release_notes() -> str:
    return f"""
# {RELEASE_TITLE}

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

The intended immutable tag is `{TAG_NAME}`. The tagged package URL is
{TAG_TREE_URL}.
"""


def build_candidate() -> dict[str, object]:
    main_tex = MANUSCRIPT / "main_R582.tex"
    si_tex = MANUSCRIPT / "SI_R582.tex"
    main_figures = parse_figures(main_tex)
    si_figures = parse_figures(si_tex)
    if main_figures != list(MAIN_SOURCE_BUNDLES):
        raise RuntimeError(f"Unexpected main figure order: {main_figures}")
    if si_figures != list(SI_SOURCE_BUNDLES):
        raise RuntimeError(f"Unexpected SI figure order: {si_figures}")

    safe_reset(STAGING)
    STAGING.mkdir(parents=True)
    provenance: list[dict[str, object]] = []
    figure_rows: list[dict[str, object]] = []

    for name in ("main_R582.tex", "main_R582.pdf", "SI_R582.tex", "SI_R582.pdf", "refs.bib"):
        copy_one(MANUSCRIPT / name, STAGING / "manuscript" / name, provenance)

    figure_source = MANUSCRIPT / "figures_R582"
    for document, figures, bundle_map in (
        ("main", main_figures, MAIN_SOURCE_BUNDLES),
        ("SI", si_figures, SI_SOURCE_BUNDLES),
    ):
        for sequence, stem in enumerate(figures, start=1):
            row: dict[str, object] = {
                "document": document,
                "sequence": sequence,
                "stem": stem,
                "source_bundle": bundle_map[stem],
            }
            for extension in FIGURE_FORMATS:
                source = figure_source / f"{stem}{extension}"
                destination = STAGING / "manuscript" / "figures_R582" / source.name
                copy_one(source, destination, provenance)
                key = extension.lstrip(".")
                row[f"{key}_bytes"] = source.stat().st_size
                row[f"{key}_sha256"] = sha256(source)
            figure_rows.append(row)

    source_root = MANUSCRIPT / "source_data"
    for bundle in sorted(set(MAIN_SOURCE_BUNDLES.values()) | set(SI_SOURCE_BUNDLES.values())):
        copy_tree_filtered(
            source_root / bundle,
            STAGING / "manuscript" / "source_data" / bundle,
            provenance,
            predicate=lambda path, bundle=bundle: include_active_bundle_file(bundle, path),
        )

    # Minimal derived dependency closure for renderers that intentionally read
    # registered upstream bundles rather than duplicating the input locally.
    renderer_dependencies = [
        "manuscript/source_data/r582_font_runtime.py",
        "manuscript/source_data/Fig_R538_voltage_reanchor/representative_vq_profiles_for_article.csv",
        "manuscript/source_data/Fig_R581_experimental_evidence/R581_experimental_evidence_panel_b_rate.csv",
        "manuscript/source_data/Fig_R581_experimental_evidence/R581_experimental_evidence_panel_c_compression.csv",
        "manuscript/source_data/Fig_R581_experimental_evidence/R581_experimental_evidence_panel_d_g4.csv",
        "battery_experiment/02_processed_data/R581_G4_DVDQ_REBUILD/dvdq_curves_all_windows.csv",
        "battery_experiment/02_processed_data/R581_G4_DVDQ_REBUILD/dvdq_metrics_by_cycle_and_window.csv",
        "battery_experiment/02_processed_data/R581_G4_DVDQ_REBUILD/eligible_cycles.csv",
        "battery_experiment/02_processed_data/R581_COMPRESSION_EVIDENCE_REBUILD/endpoint_sensitivity.csv",
        "manuscript/source_data/Fig_R568_scale_provenance/R581_Fig_R568_scale_provenance_source_data.csv",
        "manuscript/source_data/Fig_R581_matched_closure/R581_release_closure_comparison.csv",
        "manuscript/source_data/Fig_R581_matched_closure/R581_release_closure_summary.json",
        "manuscript/source_data/Fig_R581_matched_closure/Fig_R581_matched_closure_threshold_definitions.csv",
        "manuscript/source_data/Fig_R581_matched_closure/Fig_R581_matched_closure_endpoint_summary.csv",
        "manuscript/source_data/Fig_R581_matched_closure/R581_RELEASE_CLOSURE_MANIFEST.md",
        "manuscript/source_data/Fig_R538_voltage_reanchor/R538_coverage_tafel_degeneracy.csv",
        "manuscript/source_data/Fig_R538_voltage_reanchor/R538_reanchor_summary.csv",
        "manuscript/notes/project_truth.md",
        "manuscript/source_data/R582_Fig6_operating_levers/make_fig_r582_operating_levers.py",
        "manuscript/source_data/R582_Fig6_operating_levers/R582_Fig6_current_solved.csv",
        "manuscript/source_data/R582_Fig6_operating_levers/R582_Fig6_deff_solved.csv",
        "manuscript/source_data/R582_Fig6_operating_levers/R582_Fig6_secondary_levers.csv",
        "manuscript/source_data/R582_Fig6_operating_levers/R582_Fig6_decision_map.csv",
        "manuscript/source_data/R582_Fig6_operating_levers/R582_Fig6_input_manifest.csv",
        "manuscript/source_data/Fig_R573_model_geometry/R573_model_geometry_values.csv",
        "manuscript/source_data/Fig_R581_concept_state_progression/R581_concept_state_progression_source_data.csv",
        "manuscript/source_data/Fig_R581_concept_state_progression/R581_CONCEPT_STATE_PROGRESSION_BUILD.json",
        "manuscript/source_data/Fig_R545_fields/Fig3_baseline_spatial_long.csv",
        "manuscript/source_data/Fig_R581_experimental_evidence/R581_experimental_evidence_panel_a_composition.csv",
        "manuscript/source_data/Fig_R581_experimental_evidence/R581_experimental_evidence_input_manifest.csv",
        "DFT/06_periodic_cp2k_single_i2_r514/workspace_snapshot/outputs/r514_status1_short/tables/sanity_final_four_site_spectrum.csv",
        "MD/carrier_diffusivity_si_figure/R197_FigS_md_carrier_diffusivity_source_summary.csv",
        "MD/carrier_diffusivity_si_figure/R197_FigS_md_carrier_diffusivity_summary.json",
        "fiber/data/R531_fiber3d_clock.csv",
        "fiber/data/R531_fiber3d_accessibility_closure.csv",
        "fiber/scripts/R531_fiber3d.py",
        "pore_system/scripts/R531_network3d.py",
        "manuscript/source_data/Fig_R556_mesoscale_renders/R531_fiber3d_morphology.npz",
        "manuscript/source_data/Fig_R556_mesoscale_renders/R531_network3d_field.npz",
        "pore_system/data/R531_network3d_curves.csv",
        "pore_system/data/R531_network3d_thresholds.csv",
    ]
    dependency_rows: list[dict[str, object]] = []
    for relative in renderer_dependencies:
        source = ROOT / relative
        destination = STAGING / relative
        copy_one(source, destination, provenance)
        dependency_rows.append(
            {
                "source_workspace_path": relative,
                "package_path": relative,
                "bytes": source.stat().st_size,
                "sha256": sha256(source),
                "status": "included_exact_copy",
            }
        )
    write_csv(
        STAGING / "RENDER_DEPENDENCY_MANIFEST.csv",
        ["source_workspace_path", "package_path", "bytes", "sha256", "status"],
        dependency_rows,
    )

    copy_tree_filtered(MANUSCRIPT / "submission", STAGING / "submission", provenance)

    audit_names = {
        "check_font_consistency.py",
        "check_r582_language_and_format.py",
        "CITATION_AUDIT_BASELINE.md",
        "CITATION_DOI_CROSSREF_AUDIT.json",
        "CITATION_DOI_CROSSREF_AUDIT.md",
        "R582_FINAL_CITATION_EVIDENCE_AUDIT.md",
        "R582_FINAL_CITATION_EVIDENCE_AUDIT.csv",
        "R582_FINAL_FONT_GATE.json",
        "R582_JPS_SUBMISSION_TEXT_PACKAGE_BUILD_REPORT.md",
        "R582_MAIN_TEX_INTEGRATION_QA.md",
        "R582_MASTER_REBUILD_CONTRACT.md",
        "R582_PUBLIC_RELEASE_CANDIDATE_DRY_RUN.md",
        "R582_CAPTION_EXTRACTION_QA.json",
        "R582_RELEASE_BLACKBOX_REPRODUCTION_AUDIT.md",
        "R582_RELEASE_BLACKBOX_REPRODUCTION_AUDIT.json",
        "R582_RELEASE_BLACKBOX_REPRODUCTION_AUDIT.csv",
        "R582_SENTENCE_CITATION_AUDIT.csv",
        "R582_SENTENCE_CITATION_AUDIT.md",
        "R582_SI_FIGS_S6_S12_S13_BUILD_REPORT.md",
        "R582_SI_INTEGRATION_QA.md",
        "extract_verify_r582_figure_captions.py",
        "verify_cited_dois_crossref.py",
    }
    audit_root = MANUSCRIPT / "audit_R582"
    for name in sorted(audit_names):
        source = audit_root / name
        if source.is_file():
            copy_one(source, STAGING / "audit" / name, provenance)

    correction_source = (
        ROOT / "battery_experiment" / "02_processed_data" / "R581_NH4BR_METADATA_CORRECTION"
    )
    copy_tree_filtered(
        correction_source,
        STAGING / "metadata_corrections" / "EXP-META-001",
        provenance,
    )
    correction_tool = (
        ROOT
        / "battery_experiment"
        / "05_source_code"
        / "tools"
        / "R581_build_nh4br_metadata_correction_manifest.py"
    )
    copy_one(
        correction_tool,
        STAGING / "metadata_corrections" / "EXP-META-001" / "build_manifest.py",
        provenance,
    )

    md_output = ROOT / "MD" / "workspace_mirror" / "outputs" / "md_transport_soc_series"
    md_runs = ROOT / "MD" / "workspace_mirror" / "work" / "md_transport_soc_series" / "runs"
    md_target = STAGING / "molecular_models" / "md_soc_series"
    md_rows: list[dict[str, object]] = []

    def copy_md(source: Path, destination: Path, case: str, role: str) -> None:
        copy_one(source, destination, provenance)
        md_rows.append(
            {
                "case": case,
                "role": role,
                "source_workspace_path": workspace_rel(source),
                "package_path": package_rel(destination),
                "bytes": source.stat().st_size,
                "sha256": sha256(source),
            }
        )

    md_support = [
        (md_output / "README.md", md_target / "README_SOURCE.md"),
        (md_output / "inputs" / "soc_series_config.yaml", md_target / "soc_series_config.yaml"),
        (md_output / "results" / "artifact_manifest.csv", md_target / "results" / "artifact_manifest.csv"),
        (md_output / "results" / "artifact_manifest.json", md_target / "results" / "artifact_manifest.json"),
        (md_output / "results" / "completion_audit.md", md_target / "results" / "completion_audit.md"),
        (md_output / "results" / "completion_audit.json", md_target / "results" / "completion_audit.json"),
        (md_output / "results" / "requirements_traceability.md", md_target / "results" / "requirements_traceability.md"),
        (md_output / "results" / "requirements_traceability.csv", md_target / "results" / "requirements_traceability.csv"),
        (md_output / "results" / "tool_versions.json", md_target / "results" / "tool_versions.json"),
        (md_output / "results" / "all_soc_diffusion_results.csv", md_target / "results" / "all_soc_diffusion_results.csv"),
        (md_output / "results" / "selected_soc_diffusion_results.csv", md_target / "results" / "selected_soc_diffusion_results.csv"),
        (md_output / "results" / "soc_transport_summary.csv", md_target / "results" / "soc_transport_summary.csv"),
    ]
    for source, destination in md_support:
        copy_md(source, destination, "all", "series_record")
    for source in sorted((ROOT / "MD" / "manifests").glob("*")):
        if source.is_file():
            copy_md(source, md_target / "source_manifests" / source.name, "all", "source_manifest")

    for case in MD_CASES:
        case_root = md_runs / case
        if not case_root.is_dir():
            raise FileNotFoundError(case_root)
        destination_root = md_target / "cases" / case
        copy_md(case_root / "topol.top", destination_root / "topol.top", case, "topology")
        itp_files = sorted(case_root.glob("*.itp"))
        if {path.name for path in itp_files} != MD_REQUIRED_ITP:
            raise RuntimeError(f"Unexpected ITP identity for {case}: {[p.name for p in itp_files]}")
        for source in itp_files:
            copy_md(source, destination_root / source.name, case, "topology_include")
        mdp_files = sorted((case_root / "mdp").glob("*.mdp"))
        if {path.name for path in mdp_files} != MD_REQUIRED_MDP:
            raise RuntimeError(f"Unexpected MDP identity for {case}: {[p.name for p in mdp_files]}")
        for source in mdp_files:
            copy_md(source, destination_root / "mdp" / source.name, case, "stage_protocol")
        for name, role in (("mdout.mdp", "compiled_protocol"), ("system_metadata.json", "system_metadata")):
            copy_md(case_root / name, destination_root / name, case, role)
        for name in MD_GROMACS_LOGS:
            source = case_root / name
            if not source.is_file() or source.stat().st_size == 0:
                raise RuntimeError(f"Missing/non-empty GROMACS log required for {case}: {source}")
            copy_md(source, destination_root / "logs" / name, case, "gromacs_log")

    write_csv(
        md_target / "MD_CASE_IDENTITY_MANIFEST.csv",
        ["case", "role", "source_workspace_path", "package_path", "bytes", "sha256"],
        md_rows,
    )

    cp2k_base = ROOT / CP2K_BASE_REL
    cp2k_target = STAGING / "molecular_models" / "cp2k_single_i2"
    cp2k_rows: list[dict[str, object]] = []
    for number, (site, stage, relative) in enumerate(CP2K_RECORDS, start=1):
        source = cp2k_base / Path(relative)
        destination = cp2k_target / "records" / Path(relative)
        copy_one(source, destination, provenance)
        if source.suffix.lower() == ".out":
            tail = source.read_bytes()[-65536:]
            if b"PROGRAM ENDED" not in tail:
                raise RuntimeError(f"CP2K output does not terminate cleanly: {source}")
        cp2k_rows.append(
            {
                "record_id": f"CP2K-SI-{number:03d}",
                "site": site,
                "stage": stage,
                "source_workspace_path": workspace_rel(source),
                "package_path": package_rel(destination),
                "bytes": source.stat().st_size,
                "sha256": sha256(source),
                "status": "adopted_exact_copy",
            }
        )
    spectrum = (
        ROOT
        / "DFT"
        / "06_periodic_cp2k_single_i2_r514"
        / "workspace_snapshot"
        / "outputs"
        / "r514_status1_short"
        / "tables"
        / "sanity_final_four_site_spectrum.csv"
    )
    copy_one(spectrum, cp2k_target / "sanity_final_four_site_spectrum.csv", provenance)
    write_csv(
        cp2k_target / "CP2K_SINGLE_I2_IDENTITY_MANIFEST.csv",
        [
            "record_id",
            "site",
            "stage",
            "source_workspace_path",
            "package_path",
            "bytes",
            "sha256",
            "status",
        ],
        cp2k_rows,
    )

    continuum_target = STAGING / "continuum_model_identity"
    closure = ROOT / "battery_comsol" / "02_outputs_core" / "R581_CANONICAL_CLOSURE_REBUILD"
    copy_tree_filtered(closure / "manifests", continuum_target / "manifests", provenance)
    for source in sorted((closure / "scripts").iterdir()):
        if source.is_file() and source.suffix.lower() in {".py", ".java"}:
            copy_one(source, continuum_target / "scripts" / source.name, provenance)
    for source in sorted((closure / "outputs").iterdir()):
        if source.is_file() and source.suffix.lower() in {".csv", ".json", ".md"}:
            copy_one(source, continuum_target / "outputs" / source.name, provenance)
    r520_script = (
        ROOT
        / "battery_comsol"
        / "02_outputs_core"
        / "R520_BLOCKAGE_FEEDBACK_NATIVE"
        / "scripts"
        / "R520BuildBlockageFeedbackNative.java"
    )
    copy_one(r520_script, continuum_target / "scripts" / r520_script.name, provenance)
    r526 = ROOT / "battery_comsol" / "02_outputs_core" / "R526_COMSOL_NATIVE_KNOB_EXPORT"
    for relative in (
        "R526_FINAL_REPORT.md",
        "R526_NATIVE_EXPORT_QA.csv",
        "R526_SOLVED_MPH_E_ARCHIVE_MANIFEST.csv",
        "comsol_native_user_export/R526_NATIVE_SOLVE_STATUS.csv",
        "comsol_native_user_export/R526_SOLVED_MPH_ARCHIVE_MANIFEST.csv",
        "scripts/R526NativeKnobImageExport.java",
        "scripts/R526StudyProbe.java",
    ):
        source = r526 / relative
        copy_one(source, continuum_target / "R526" / relative, provenance)

    copy_one(
        Path(__file__),
        STAGING / "tools" / "build_r582_public_release_candidate.py",
        provenance,
    )
    verifier_source = Path(__file__).with_name("verify_r582_public_release_candidate.py")
    copy_one(verifier_source, STAGING / "tools" / "verify_release.py", provenance)

    write_text(STAGING / "README.md", build_readme())
    write_text(STAGING / "REPRODUCE.md", build_reproduce())
    write_text(STAGING / "RELEASE_PLAN.md", build_release_plan())
    write_text(STAGING / "DATA_AVAILABILITY_STATUS.md", build_data_availability())
    write_text(STAGING / "RELEASE_NOTES.md", build_release_notes())

    figure_fields = ["document", "sequence", "stem", "source_bundle"]
    for extension in FIGURE_FORMATS:
        key = extension.lstrip(".")
        figure_fields.extend((f"{key}_bytes", f"{key}_sha256"))
    write_csv(STAGING / "FIGURE_RELEASE_MANIFEST.csv", figure_fields, figure_rows)

    # Rehash every live source after copying. This detects concurrent regeneration.
    for row in provenance:
        source = ROOT / str(row["source_workspace_path"])
        if not source.is_file() or source.stat().st_size != int(row["bytes"]):
            raise RuntimeError(f"Source drift after copy: {source}")
        if sha256(source) != str(row["sha256"]):
            raise RuntimeError(f"Source hash drift after copy: {source}")
    write_csv(
        STAGING / "SOURCE_TO_PACKAGE_MANIFEST.csv",
        ["source_workspace_path", "package_path", "bytes", "sha256"],
        provenance,
    )

    forbidden = [
        path
        for path in STAGING.rglob("*")
        if path.is_file() and path.suffix.lower() in {".mph", ".ndax", ".mpr"}
    ]
    if forbidden:
        raise RuntimeError(f"Forbidden raw/model file copied: {forbidden[0]}")

    secret_hits: list[dict[str, str]] = []
    for path in sorted(STAGING.rglob("*")):
        if not path.is_file() or path.stat().st_size > 20 * 1024 * 1024:
            continue
        data = path.read_bytes()
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(data):
                secret_hits.append({"path": package_rel(path), "pattern": label})
    if secret_hits:
        raise RuntimeError(f"Secret-pattern hit(s): {secret_hits}")

    build_metadata = {
        "build_version": BUILD_VERSION,
        "built_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "package_name": PACKAGE_NAME,
        "status": "local_release_candidate_not_published",
        "proposed_tag": TAG_NAME,
        "proposed_release_title": RELEASE_TITLE,
        "proposed_tag_tree_url": TAG_TREE_URL,
        "proposed_release_url": RELEASE_URL,
        "main_figure_count": len(main_figures),
        "si_figure_count": len(si_figures),
        "figure_format_count": len(figure_rows) * len(FIGURE_FORMATS),
        "source_bundle_count": len(set(MAIN_SOURCE_BUNDLES.values()) | set(SI_SOURCE_BUNDLES.values())),
        "md_case_count": len(MD_CASES),
        "cp2k_identity_record_count": len(cp2k_rows),
        "raw_experimental_files_embedded": 0,
        "mph_files_embedded": 0,
        "doi": None,
    }
    write_text(STAGING / "BUILD_METADATA.json", json.dumps(build_metadata, indent=2))

    content_rows: list[dict[str, object]] = []
    for path in sorted(STAGING.rglob("*")):
        if not path.is_file() or path.name in {"FILE_SHA256_MANIFEST.csv", "PACKAGE_DIGESTS.json"}:
            continue
        content_rows.append(
            {
                "relative_path": package_rel(path),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
    root_digest = hashlib.sha256()
    for row in sorted(content_rows, key=lambda value: str(value["relative_path"])):
        root_digest.update(
            f"{row['relative_path']}\0{row['bytes']}\0{row['sha256']}\n".encode("utf-8")
        )
    digest_record = {
        "algorithm": "SHA-256",
        "canonical_record": "relative_path\\0bytes\\0sha256\\n sorted by UTF-8 path",
        "excludes": ["FILE_SHA256_MANIFEST.csv", "PACKAGE_DIGESTS.json"],
        "content_root_sha256": root_digest.hexdigest().upper(),
        "content_root_file_count": len(content_rows),
        "content_root_bytes": sum(int(row["bytes"]) for row in content_rows),
    }
    write_text(STAGING / "PACKAGE_DIGESTS.json", json.dumps(digest_record, indent=2))
    digest_path = STAGING / "PACKAGE_DIGESTS.json"
    manifest_rows = content_rows + [
        {
            "relative_path": "PACKAGE_DIGESTS.json",
            "bytes": digest_path.stat().st_size,
            "sha256": sha256(digest_path),
        }
    ]
    manifest_rows.sort(key=lambda value: str(value["relative_path"]))
    write_csv(
        STAGING / "FILE_SHA256_MANIFEST.csv",
        ["relative_path", "bytes", "sha256"],
        manifest_rows,
    )

    large_warning = [row for row in manifest_rows if int(row["bytes"]) > GITHUB_WARNING_BYTES]
    large_hard = [row for row in manifest_rows if int(row["bytes"]) >= GITHUB_HARD_BYTES]
    if large_hard:
        raise RuntimeError(f"GitHub hard-limit blocker in package: {large_hard}")

    report = f"""
# R582 local release-candidate dry-run report

Status: **BUILT AND HASH-VERIFIED LOCALLY; NOT COMMITTED OR PUBLISHED**

- Candidate directory: `{TARGET}`
- Proposed tag: `{TAG_NAME}`
- Proposed release title: `{RELEASE_TITLE}`
- Exact file list, byte sizes and SHA-256 values: `FILE_SHA256_MANIFEST.csv`
- Main/SI figures: {len(main_figures)} + {len(si_figures)} = {len(figure_rows)}
- Figure assets: {len(figure_rows) * len(FIGURE_FORMATS)} (PDF/SVG/PNG/TIFF)
- Figure source bundles: {build_metadata['source_bundle_count']}
- MD identities: {len(MD_CASES)} cases, exact topology/ITP/MDP/system metadata/GROMACS logs
- CP2K exact identity records: {len(cp2k_rows)}
- Embedded raw acquisition files: 0
- Embedded COMSOL `.mph` files: 0
- Files above GitHub 50 MiB warning threshold: {len(large_warning)}
- Files at or above GitHub 100 MiB hard limit: {len(large_hard)}
- Secret-pattern hits: 0
- Exact content-root SHA-256: `PACKAGE_DIGESTS.json`

## Remaining publication gates

1. Confirm final author list, affiliations, corresponding author, CRediT, funding and acknowledgements.
2. Cold-compile the final main/SI, rerun this builder and rerun `tools/verify_release.py`.
3. Confirm all final audit reports and submission files were frozen after the cold build.
4. Confirm that the Data Availability URL embedded in main/SI resolves to the tagged commit
   immediately after publication.
5. Enable GitHub release immutability, commit/push only with root-task approval, create a draft
   release, attach any approved archive, publish, and confirm the `Immutable` badge.
6. No DOI exists; do not add one unless a real repository deposit assigns it.
"""
    write_text(STAGING / "DRY_RUN_RELEASE_REPORT.md", report)

    # Report must itself be covered; regenerate digest and manifest once after adding it.
    content_rows = []
    for path in sorted(STAGING.rglob("*")):
        if not path.is_file() or path.name in {"FILE_SHA256_MANIFEST.csv", "PACKAGE_DIGESTS.json"}:
            continue
        content_rows.append(
            {"relative_path": package_rel(path), "bytes": path.stat().st_size, "sha256": sha256(path)}
        )
    root_digest = hashlib.sha256()
    for row in sorted(content_rows, key=lambda value: str(value["relative_path"])):
        root_digest.update(
            f"{row['relative_path']}\0{row['bytes']}\0{row['sha256']}\n".encode("utf-8")
        )
    digest_record.update(
        {
            "content_root_sha256": root_digest.hexdigest().upper(),
            "content_root_file_count": len(content_rows),
            "content_root_bytes": sum(int(row["bytes"]) for row in content_rows),
        }
    )
    write_text(STAGING / "PACKAGE_DIGESTS.json", json.dumps(digest_record, indent=2))
    digest_path = STAGING / "PACKAGE_DIGESTS.json"
    manifest_rows = content_rows + [
        {"relative_path": "PACKAGE_DIGESTS.json", "bytes": digest_path.stat().st_size, "sha256": sha256(digest_path)}
    ]
    manifest_rows.sort(key=lambda value: str(value["relative_path"]))
    write_csv(STAGING / "FILE_SHA256_MANIFEST.csv", ["relative_path", "bytes", "sha256"], manifest_rows)

    safe_reset(TARGET)
    STAGING.rename(TARGET)
    return {
        "status": "built_local_candidate",
        "target": str(TARGET),
        "files_manifested": len(manifest_rows),
        "bytes_manifested": sum(int(row["bytes"]) for row in manifest_rows),
        "content_root_sha256": digest_record["content_root_sha256"],
        "main_figures": len(main_figures),
        "si_figures": len(si_figures),
        "md_cases": len(MD_CASES),
        "cp2k_records": len(cp2k_rows),
        "over_50_mib": len([row for row in manifest_rows if int(row["bytes"]) > GITHUB_WARNING_BYTES]),
        "at_or_over_100_mib": len([row for row in manifest_rows if int(row["bytes"]) >= GITHUB_HARD_BYTES]),
    }


def main() -> int:
    result = build_candidate()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
