from __future__ import annotations

import csv
import hashlib
import json
import shutil
import zipfile
from dataclasses import dataclass, asdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "ZIFB000"
OUTPUTS = ROOT / "outputs"


@dataclass
class CopiedItem:
    src: str
    dst: str
    category: str
    bytes: int
    sha256: str
    note: str


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def rm_tree(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)


def ensure_dirs() -> None:
    rm_tree(OUT)
    for p in [
        OUT / "00_START_HERE",
        OUT / "01_MANUSCRIPT_SCTS_R93",
        OUT / "02_FIGURES",
        OUT / "02_FIGURES" / "main_figures",
        OUT / "02_FIGURES" / "si_figures",
        OUT / "02_FIGURES" / "submission_600dpi",
        OUT / "03_MODEL_CODE",
        OUT / "03_MODEL_CODE" / "models",
        OUT / "03_MODEL_CODE" / "scripts",
        OUT / "03_MODEL_CODE" / "tests",
        OUT / "04_MECHANISM_EVIDENCE",
        OUT / "04_MECHANISM_EVIDENCE" / "molecular_surface",
        OUT / "04_MECHANISM_EVIDENCE" / "single_fiber",
        OUT / "04_MECHANISM_EVIDENCE" / "comsol_porous_electrode",
        OUT / "04_MECHANISM_EVIDENCE" / "parameter_arguments",
        OUT / "04_MECHANISM_EVIDENCE" / "fullcell_fit_decision",
        OUT / "05_GPT_AND_COAUTHOR_REVIEW",
        OUT / "06_RECORD_INDEX",
        OUT / "07_LEGACY_NOT_PRIMARY",
        OUT / "08_GITHUB_RELEASE_LIGHT",
    ]:
        p.mkdir(parents=True, exist_ok=True)


def copy_file(src: Path, dst: Path, category: str, items: list[CopiedItem], note: str = "") -> bool:
    if not src.exists() or not src.is_file():
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        shutil.copy2(src, dst)
    except OSError as exc:
        skipped = OUT / "06_RECORD_INDEX" / "skipped_copy_errors.log"
        skipped.parent.mkdir(parents=True, exist_ok=True)
        with skipped.open("a", encoding="utf-8") as f:
            f.write(f"{src} -> {dst}: {exc}\n")
        return False
    items.append(
        CopiedItem(
            src=str(src.relative_to(ROOT)) if src.is_relative_to(ROOT) else str(src),
            dst=str(dst.relative_to(OUT)),
            category=category,
            bytes=dst.stat().st_size,
            sha256=sha256(dst),
            note=note,
        )
    )
    return True


def register_existing(path: Path, category: str, items: list[CopiedItem], note: str = "") -> None:
    if not path.exists() or not path.is_file():
        return
    items.append(
        CopiedItem(
            src=str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path),
            dst=str(path.relative_to(OUT)) if path.is_relative_to(OUT) else str(path),
            category=category,
            bytes=path.stat().st_size,
            sha256=sha256(path),
            note=note,
        )
    )


def copy_tree_filtered(src: Path, dst: Path, category: str, items: list[CopiedItem], suffixes: set[str] | None = None, max_mb: float | None = None, note: str = "") -> None:
    if not src.exists():
        return
    for p in src.rglob("*"):
        if not p.is_file():
            continue
        if suffixes is not None and p.suffix.lower() not in suffixes:
            continue
        if max_mb is not None and p.stat().st_size > max_mb * 1024 * 1024:
            continue
        rel = p.relative_to(src)
        copy_file(p, dst / rel, category, items, note)


def zip_dir(src: Path, dst: Path, include_root_name: bool = True) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(src.rglob("*")):
            if p.is_file():
                arc = p.relative_to(src.parent if include_root_name else src)
                zf.write(p, str(arc).replace("\\", "/"))


def output_inventory() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for d in sorted(OUTPUTS.iterdir(), key=lambda p: p.stat().st_mtime if p.exists() else 0, reverse=True):
        if not d.is_dir():
            continue
        files = [p for p in d.rglob("*") if p.is_file()]
        total = sum(p.stat().st_size for p in files)
        final = d / "final_status.md"
        status_text = ""
        if final.exists():
            try:
                status_text = final.read_text(encoding="utf-8", errors="replace").splitlines()[0][:200]
            except Exception:
                status_text = "final_status unreadable"
        name = d.name
        if name.startswith("SCTS_R93"):
            classification = "CURRENT_MANUSCRIPT_OR_SAMPLE"
        elif name.startswith("SCTS_R9") or name.startswith("SCTS_R8") or name.startswith("SCTS_"):
            classification = "SUPERSEDED_MANUSCRIPT_HISTORY"
        elif name.startswith("ZIFB_R5") or name.startswith("ZIFB_R6") or name.startswith("ZIFB_paper_figure"):
            classification = "USEFUL_MECHANISM_SYNTHESIS"
        elif name.startswith("ZIFB_R1") or name.startswith("ZIFB_R2"):
            classification = "FOUNDATIONAL_MECHANISM_HISTORY"
        elif "GPT_analysis_package" in name:
            classification = "GPT_REVIEW_HISTORY"
        elif "cp2k" in name.lower() or "molecular" in name.lower():
            classification = "MOLECULAR_EVIDENCE"
        elif "COMSOL" in name or "comsol" in name:
            classification = "COMSOL_EVIDENCE"
        else:
            classification = "INDEX_ONLY"
        rows.append(
            {
                "name": name,
                "files": len(files),
                "MB": round(total / 1024 / 1024, 3),
                "last_write_time": d.stat().st_mtime,
                "classification": classification,
                "final_status_head": status_text,
            }
        )
    return rows


def write_inventory(rows: list[dict[str, object]]) -> None:
    csv_path = OUT / "06_RECORD_INDEX" / "all_outputs_inventory.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else [])
        w.writeheader()
        w.writerows(rows)
    (OUT / "06_RECORD_INDEX" / "all_outputs_inventory.json").write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")


def copy_curated_materials(items: list[CopiedItem]) -> None:
    r93 = OUTPUTS / "SCTS_R93_sample_article_format_alignment"
    manuscript_files = [
        "SCTS_ZIFB_sample_format_aligned_R93.md",
        "SCTS_ZIFB_sample_format_aligned_R93.docx",
        "pdf_proof/SCTS_ZIFB_sample_format_aligned_R93.pdf",
        "Supporting_Information_R93.md",
        "Supporting_Information_R93.docx",
        "pdf_proof/Supporting_Information_R93.pdf",
        "R93_changes_from_R92.md",
        "SCTS_sample_article_format_lessons_R93.md",
        "R93_QA_summary.json",
        "final_status.md",
    ]
    for rel in manuscript_files:
        copy_file(r93 / rel, OUT / "01_MANUSCRIPT_SCTS_R93" / rel.replace("/", "_"), "current_manuscript", items)
    for rel in [
        "package/GPT_PRO_REVIEW_PACKET_R93_SAMPLE_FORMAT.zip",
        "package/SCTS_R93_SAMPLE_FORMAT_ALIGNMENT_FULL.zip",
        "package/SCTS_R93_FIGURES_NATIVE_600DPI.zip",
        "GPT_PRO_REVIEW_PROMPT_R93_CN.md",
    ]:
        copy_file(r93 / rel, OUT / "05_GPT_AND_COAUTHOR_REVIEW" / Path(rel).name, "review_packet", items)

    main_figs = {
        "Fig1_R67_local_iodine_failure_framework.png": "Fig1_mechanism_overview.png",
        "SI_Fig_molecular_surface_evidence_R64.png": "Fig2_molecular_surface_prior.png",
        "Fig2_single_fiber_closure_bridge_R64.png": "Fig3_single_fiber_closure.png",
        "Fig3_R69_COMSOL_state_evolution.png": "Fig4_COMSOL_time_evolution.png",
        "Fig4_COMSOL_axis_profile_fields_R64.png": "Fig5_spatial_localization_fields.png",
        "Fig5_R67_parameter_mechanism_matrix.png": "Fig6_parameter_mechanism_matrix.png",
        "Graphical_Abstract_R65.png": "Graphical_Abstract.png",
    }
    for src_name, dst_name in main_figs.items():
        copy_file(r93 / "figures" / src_name, OUT / "02_FIGURES" / "main_figures" / dst_name, "main_figure", items)
        copy_file(r93 / "submission_figures_600dpi" / src_name, OUT / "02_FIGURES" / "submission_600dpi" / dst_name, "submission_figure", items)
    si_names = [
        "SI_Fig_true_COMSOL_cloudmaps_R64.png",
        "SI_Fig_precipitation_dissolution_boundary_R64.png",
        "SI_dense_Fig3_CAP_RATE_time_evolution_R64.png",
        "SI_dense_Fig5_parameter_family_curves_R64.png",
        "SI_dense_Fig6_parameter_fingerprint_R64.png",
        "Fig6_R67_evidence_boundary_falsification.png",
    ]
    for name in si_names:
        copy_file(r93 / "figures" / name, OUT / "02_FIGURES" / "si_figures" / name, "si_figure", items)

    copy_tree_filtered(ROOT / "models" / "single_fiber_i2", OUT / "03_MODEL_CODE" / "models" / "single_fiber_i2", "single_fiber_code", items, note="Complete single-fiber model and closure bridge.")
    copy_tree_filtered(ROOT / "tests", OUT / "03_MODEL_CODE" / "tests", "tests", items, suffixes={".py"}, note="Local tests retained.")
    selected_scripts = [
        "build_SCTS_R84_publication_deep_revision.py",
        "build_SCTS_R85_submission_ordered_revision.py",
        "build_SCTS_R92_scts_format_compliance.py",
        "build_SCTS_R93_sample_article_format_alignment.py",
        "organize_ZIFB000_project_archive.py",
    ]
    for name in selected_scripts:
        copy_file(ROOT / "scripts" / name, OUT / "03_MODEL_CODE" / "scripts" / name, "curated_script", items)
    zip_dir(ROOT / "scripts", OUT / "03_MODEL_CODE" / "all_project_scripts_snapshot.zip")
    register_existing(OUT / "03_MODEL_CODE" / "all_project_scripts_snapshot.zip", "code_archive", items, "All scripts snapshot.")

    evidence_dirs = {
        "molecular_surface": [
            OUTPUTS / "cp2k_molecular" / "molecular_layer_v2_solvated_surface_residence",
            OUTPUTS / "cp2k_molecular" / "molecular_layer_v2b_complete_i2_aggregation",
        ],
        "single_fiber": [OUTPUTS / "single_fiber_i2", OUTPUTS / "SCTS_R93_sample_article_format_alignment"],
        "comsol_porous_electrode": [
            OUTPUTS / "ZIFB_R13_local_iodine_handling_mechanism_reset",
            OUTPUTS / "ZIFB_R14_local_handling_evidence_hardening",
            OUTPUTS / "ZIFB_R15_physics_first_iodine_failure_mechanism_lock",
            OUTPUTS / "ZIFB_R25_simulation_led_mechanism_evidence_lock",
            OUTPUTS / "COMSOL_native_iodine_mechanism_visualization",
            OUTPUTS / "COMSOL_native_mechanism_review_R2",
        ],
        "parameter_arguments": [
            OUTPUTS / "ZIFB_R59_professor_level_interpretive_synthesis",
            OUTPUTS / "ZIFB_R60_parameter_by_parameter_mechanistic_argument",
            OUTPUTS / "ZIFB_R61_parameter_visual_data_explanation",
        ],
        "fullcell_fit_decision": [
            OUTPUTS / "ZIFB_R20_fullcell_observable_layer_repair",
            OUTPUTS / "ZIFB_R21_component_library_fullcell_refit",
            OUTPUTS / "ZIFB_R22M_pure_mechanism_state_space_fullcell_fit",
            OUTPUTS / "ZIFB_R23_overnight_mechanistic_fullcell_rescue_matrix",
            OUTPUTS / "ZIFB_R24_full-cell_mechanism_reset",
            OUTPUTS / "ZIFB_R25_simulation_led_mechanism_evidence_lock",
        ],
    }
    for category, dirs in evidence_dirs.items():
        for d in dirs:
            if not d.exists():
                continue
            target = OUT / "04_MECHANISM_EVIDENCE" / category / d.name
            copy_tree_filtered(d, target, category, items, suffixes={".md", ".csv", ".json", ".png"}, max_mb=8, note="Curated evidence file.")


def write_readmes(items: list[CopiedItem], rows: list[dict[str, object]]) -> None:
    total_mb = sum(x.bytes for x in items) / 1024 / 1024
    useful_dirs = [r for r in rows if r["classification"] in {"CURRENT_MANUSCRIPT_OR_SAMPLE", "USEFUL_MECHANISM_SYNTHESIS", "FOUNDATIONAL_MECHANISM_HISTORY", "MOLECULAR_EVIDENCE", "COMSOL_EVIDENCE"}]
    (OUT / "README.md").write_text(
        f"""# ZIFB000 curated project archive

This folder is the cleaned, useful archive for the zinc-iodine flow-battery
iodine-failure project. It separates the publishable manuscript, figures,
mechanism evidence and reusable code from the many exploratory historical
outputs.

## Start here

1. `01_MANUSCRIPT_SCTS_R93/` contains the current SCTS-oriented manuscript,
   PDF proof and Supporting Information.
2. `02_FIGURES/` contains the main figures, SI figures and 600-dpi submission
   figure files.
3. `03_MODEL_CODE/` contains the reusable single-fiber iodine model, closure
   code, manuscript-build scripts and a snapshot of all project scripts.
4. `04_MECHANISM_EVIDENCE/` contains curated evidence from molecular surface
   calculations, single-fiber closures, COMSOL porous-electrode mechanism
   outputs, parameter-by-parameter arguments and full-cell-fit decision records.
5. `05_GPT_AND_COAUTHOR_REVIEW/` contains a ready-made GPT/coauthor review
   packet.
6. `06_RECORD_INDEX/` contains an inventory of all output directories, including
   superseded or index-only work.
7. `07_LEGACY_NOT_PRIMARY/` explains what should not be used as primary evidence.
8. `08_GITHUB_RELEASE_LIGHT/` is the lightweight GitHub-facing release subset.

## Current scientific position

The manuscript is simulation-led and mechanism-led. The central claim is that
local iodine-handling failure in porous positive carbon felt can convert iodine
from soluble redox inventory into neutral-I2 supersaturation, solid iodine,
surface-state loss, localization, clumping and hydraulic/electrochemical
instability.

The project does **not** claim NH4Br optimization, a production design map,
measured microscopic coverage, an exact pressure threshold, or old EIS/full-cell
curves as direct proof of film/contact growth.

## Archive statistics

- Copied useful files: {len(items)}
- Curated archive size: {total_mb:.1f} MB
- Output directories indexed: {len(rows)}
- Useful/current directories detected in inventory: {len(useful_dirs)}

## Most important files

- Manuscript PDF: `01_MANUSCRIPT_SCTS_R93/pdf_proof_SCTS_ZIFB_sample_format_aligned_R93.pdf`
- Manuscript DOCX: `01_MANUSCRIPT_SCTS_R93/SCTS_ZIFB_sample_format_aligned_R93.docx`
- Main figures: `02_FIGURES/main_figures/`
- Single-fiber model: `03_MODEL_CODE/models/single_fiber_i2/`
- Record inventory: `06_RECORD_INDEX/all_outputs_inventory.csv`
""",
        encoding="utf-8",
    )
    (OUT / "00_START_HERE" / "USEFUL_CONTENT_MAP.md").write_text(
        """# Useful content map

## Directly useful for submission

- `01_MANUSCRIPT_SCTS_R93/`
- `02_FIGURES/main_figures/`
- `02_FIGURES/submission_600dpi/`
- `05_GPT_AND_COAUTHOR_REVIEW/GPT_PRO_REVIEW_PACKET_R93_SAMPLE_FORMAT.zip`

## Directly useful for mechanism defense

- Molecular prior: `04_MECHANISM_EVIDENCE/molecular_surface/`
- Single-fiber closure bridge: `03_MODEL_CODE/models/single_fiber_i2/` and
  `04_MECHANISM_EVIDENCE/single_fiber/`
- COMSOL porous-electrode evidence:
  `04_MECHANISM_EVIDENCE/comsol_porous_electrode/`
- Parameter-by-parameter mechanism argument:
  `04_MECHANISM_EVIDENCE/parameter_arguments/`

## Useful as caution / decision record

- Full-cell fitting attempts and decision to keep the manuscript
  simulation-led: `04_MECHANISM_EVIDENCE/fullcell_fit_decision/`
- Superseded manuscript history is indexed but not copied wholesale:
  `06_RECORD_INDEX/all_outputs_inventory.csv`
""",
        encoding="utf-8",
    )
    (OUT / "07_LEGACY_NOT_PRIMARY" / "README_legacy_not_primary.md").write_text(
        """# Legacy / not-primary materials

These materials are not deleted, but they should not be used as the primary
paper evidence:

1. Old full-cell curve fitting branches. They were useful for deciding claim
   boundaries but were not robust enough to support a quantitative validation
   claim.
2. Old EIS/CV archive processing. Archived EIS is not treated as proof or
   disproof of iodine film/contact growth.
3. Superseded SCTS manuscript packages R64-R92. R93 is the current preferred
   manuscript version.
4. Large COMSOL/MPR/MPH intermediate files. They remain in the original project
   tree or external drives and are indexed only when not needed for the curated
   archive.
""",
        encoding="utf-8",
    )
    (OUT / "03_MODEL_CODE" / "README_CODE_PACKAGE.md").write_text(
        """# ZIFB000 code package

Reusable code retained here:

- `models/single_fiber_i2/`: independent single-fiber iodine precipitation,
  coverage, film-resistance and closure model.
- `scripts/build_SCTS_R93_sample_article_format_alignment.py`: current manuscript
  package builder.
- `scripts/build_SCTS_R92_scts_format_compliance.py`,
  `scripts/build_SCTS_R85_submission_ordered_revision.py`,
  `scripts/build_SCTS_R84_publication_deep_revision.py`: build dependencies for
  the R93 manuscript pipeline.
- `all_project_scripts_snapshot.zip`: full snapshot of local scripts for audit
  and recovery.

Recommended smoke checks:

```powershell
python -m pytest models/single_fiber_i2/tests
python scripts/build_SCTS_R93_sample_article_format_alignment.py
```

Some scripts require Microsoft Word COM export, COMSOL, or project-specific
outputs. They are kept for provenance and should be run from the original
project root, not from an isolated package, unless paths are updated.
""",
        encoding="utf-8",
    )
    (OUT / "08_GITHUB_RELEASE_LIGHT" / "README_GITHUB_RELEASE.md").write_text(
        """# Lightweight GitHub release subset

The GitHub repository should contain:

- README and content map.
- Current manuscript Markdown and key PDF proof.
- Main figure PNGs.
- Single-fiber model code.
- Current manuscript-build scripts.
- Output inventory and final status.

Large historical outputs, raw MPR/MPH files and superseded manuscript packages
are not pushed by default. They are indexed locally and can be restored from the
working directory or external drives.
""",
        encoding="utf-8",
    )
    with (OUT / "06_RECORD_INDEX" / "copied_useful_files_manifest.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(asdict(items[0]).keys()) if items else [])
        w.writeheader()
        for item in items:
            w.writerow(asdict(item))
    (OUT / "06_RECORD_INDEX" / "copied_useful_files_manifest.json").write_text(
        json.dumps([asdict(x) for x in items], indent=2, ensure_ascii=False), encoding="utf-8"
    )


def make_release_subset(items: list[CopiedItem]) -> None:
    release = OUT / "08_GITHUB_RELEASE_LIGHT" / "repo_files"
    release.mkdir(parents=True, exist_ok=True)
    for rel in [
        "README.md",
        "00_START_HERE/USEFUL_CONTENT_MAP.md",
        "01_MANUSCRIPT_SCTS_R93/SCTS_ZIFB_sample_format_aligned_R93.md",
        "01_MANUSCRIPT_SCTS_R93/final_status.md",
        "01_MANUSCRIPT_SCTS_R93/R93_changes_from_R92.md",
        "01_MANUSCRIPT_SCTS_R93/SCTS_sample_article_format_lessons_R93.md",
        "01_MANUSCRIPT_SCTS_R93/pdf_proof_SCTS_ZIFB_sample_format_aligned_R93.pdf",
        "02_FIGURES/main_figures/Fig1_mechanism_overview.png",
        "02_FIGURES/main_figures/Fig2_molecular_surface_prior.png",
        "02_FIGURES/main_figures/Fig3_single_fiber_closure.png",
        "02_FIGURES/main_figures/Fig4_COMSOL_time_evolution.png",
        "02_FIGURES/main_figures/Fig5_spatial_localization_fields.png",
        "02_FIGURES/main_figures/Fig6_parameter_mechanism_matrix.png",
        "03_MODEL_CODE/README_CODE_PACKAGE.md",
        "06_RECORD_INDEX/all_outputs_inventory.csv",
        "06_RECORD_INDEX/copied_useful_files_manifest.csv",
        "07_LEGACY_NOT_PRIMARY/README_legacy_not_primary.md",
    ]:
        src = OUT / rel
        if src.exists():
            copy_file(src, release / rel, "github_release_light", items, "GitHub light release file.")
    copy_tree_filtered(OUT / "03_MODEL_CODE" / "models" / "single_fiber_i2", release / "models" / "single_fiber_i2", "github_release_light", items)
    for p in (OUT / "03_MODEL_CODE" / "scripts").glob("*.py"):
        copy_file(p, release / "scripts" / p.name, "github_release_light", items)
    zip_dir(release, OUT / "ZIFB000_github_release_light.zip", include_root_name=False)
    zip_dir(OUT, ROOT / "ZIFB000_curated_archive.zip", include_root_name=True)


def main() -> None:
    ensure_dirs()
    rows = output_inventory()
    write_inventory(rows)
    items: list[CopiedItem] = []
    copy_curated_materials(items)
    write_readmes(items, rows)
    make_release_subset(items)
    # Refresh manifest after release subset adds files.
    with (OUT / "06_RECORD_INDEX" / "copied_useful_files_manifest.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(asdict(items[0]).keys()) if items else [])
        w.writeheader()
        for item in items:
            w.writerow(asdict(item))
    (OUT / "06_RECORD_INDEX" / "copied_useful_files_manifest.json").write_text(
        json.dumps([asdict(x) for x in items], indent=2, ensure_ascii=False), encoding="utf-8"
    )
    final = {
        "archive": str(OUT),
        "curated_zip": str(ROOT / "ZIFB000_curated_archive.zip"),
        "github_release_zip": str(OUT / "ZIFB000_github_release_light.zip"),
        "copied_files": len(items),
        "copied_mb": round(sum(x.bytes for x in items) / 1024 / 1024, 3),
        "indexed_output_dirs": len(rows),
    }
    (OUT / "00_START_HERE" / "FINAL_ORGANIZATION_STATUS.json").write_text(json.dumps(final, indent=2, ensure_ascii=False), encoding="utf-8")
    (OUT / "00_START_HERE" / "FINAL_ORGANIZATION_STATUS.md").write_text(
        f"""# ZIFB000 organization status

Status: LOCAL_CURATED_ARCHIVE_CREATED

- Curated folder: `{OUT}`
- Curated zip: `{ROOT / 'ZIFB000_curated_archive.zip'}`
- GitHub-light release zip: `{OUT / 'ZIFB000_github_release_light.zip'}`
- Copied useful files: {final['copied_files']}
- Copied useful size: {final['copied_mb']} MB
- Indexed output directories: {final['indexed_output_dirs']}

Next step: push the lightweight release subset in
`08_GITHUB_RELEASE_LIGHT/repo_files/` to `ccyyyYyzz/ZIFB000`.
""",
        encoding="utf-8",
    )
    print(json.dumps(final, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
