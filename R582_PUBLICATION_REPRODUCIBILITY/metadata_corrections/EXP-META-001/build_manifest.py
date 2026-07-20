#!/usr/bin/env python3
"""Build an auditable NH4Cl -> NH4Br metadata-correction manifest.

This script never renames or modifies raw files. It records the legacy label,
the operator-confirmed chemistry, immutable-file hashes, and duplicate/copy
relationships for every matching NDAX path under 01_raw_experiment_files.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import defaultdict
from datetime import date
from pathlib import Path


CONFIRMATION_DATE = "2026-07-11"
CORRECTION_BASIS = (
    "operator-confirmed metadata correction: all experimental labels containing "
    "NH4Cl/NH4CL refer to cells prepared with NH4Br; raw names are preserved"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def corrected_label(value: str) -> str:
    return re.sub(r"NH4Cl", "NH4Br", value, flags=re.IGNORECASE)


def path_role(relative_path: Path) -> str:
    text = str(relative_path).lower()
    if "ndax_curated_active" in text:
        return "canonical_curated_active"
    if "removed_duplicates_or_incomplete" in text:
        return "excluded_duplicate_or_incomplete"
    if "ndax_by_category" in text or "ndax_by_condition" in text:
        return "organizational_copy"
    return "other_raw_view"


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    project_root = Path(__file__).resolve().parents[3]
    raw_root = project_root / "battery_experiment" / "01_raw_experiment_files"
    output_root = (
        project_root
        / "battery_experiment"
        / "02_processed_data"
        / "R581_NH4BR_METADATA_CORRECTION"
    )

    candidates = sorted(
        path
        for path in raw_root.rglob("*.ndax")
        if re.search(r"NH4Cl", path.name, flags=re.IGNORECASE)
    )
    if not candidates:
        raise RuntimeError(f"No NH4Cl-labelled NDAX files found under {raw_root}")

    rows: list[dict[str, object]] = []
    paths_by_hash: dict[str, list[Path]] = defaultdict(list)
    size_by_hash: dict[str, int] = {}

    for path in candidates:
        digest = sha256(path)
        relative = path.relative_to(project_root)
        role = path_role(relative)
        paths_by_hash[digest].append(relative)
        size_by_hash[digest] = path.stat().st_size
        rows.append(
            {
                "relative_path": str(relative),
                "path_role": role,
                "original_filename": path.name,
                "normalized_display_filename": corrected_label(path.name),
                "legacy_label": "NH4Cl/NH4CL",
                "operator_confirmed_actual_chemistry": "NH4Br",
                "correction_type": "operator-confirmed metadata correction",
                "confirmation_date": CONFIRMATION_DATE,
                "raw_file_renamed_or_modified": "no",
                "bytes": path.stat().st_size,
                "sha256": digest,
                "correction_basis": CORRECTION_BASIS,
            }
        )

    full_fields = list(rows[0].keys())
    write_csv(output_root / "NH4CL_TO_NH4BR_PATH_MANIFEST.csv", rows, full_fields)

    unique_rows: list[dict[str, object]] = []
    for digest, duplicate_paths in sorted(paths_by_hash.items()):
        ordered = sorted(
            duplicate_paths,
            key=lambda value: (
                0 if "ndax_curated_active" in str(value).lower() else 1,
                str(value).lower(),
            ),
        )
        canonical = ordered[0]
        unique_rows.append(
            {
                "canonical_relative_path": str(canonical),
                "original_filename": canonical.name,
                "normalized_display_filename": corrected_label(canonical.name),
                "operator_confirmed_actual_chemistry": "NH4Br",
                "correction_type": "operator-confirmed metadata correction",
                "confirmation_date": CONFIRMATION_DATE,
                "bytes": size_by_hash[digest],
                "sha256": digest,
                "number_of_project_paths_with_same_hash": len(ordered),
                "all_project_paths_with_same_hash": " | ".join(map(str, ordered)),
                "raw_file_renamed_or_modified": "no",
                "correction_basis": CORRECTION_BASIS,
            }
        )

    unique_fields = list(unique_rows[0].keys())
    write_csv(output_root / "NH4CL_TO_NH4BR_UNIQUE_FILE_MANIFEST.csv", unique_rows, unique_fields)

    curated = [row for row in rows if row["path_role"] == "canonical_curated_active"]
    excluded = [
        row for row in rows if row["path_role"] == "excluded_duplicate_or_incomplete"
    ]
    summary = {
        "generated_on": str(date.today()),
        "confirmation_date": CONFIRMATION_DATE,
        "raw_root": str(raw_root),
        "matching_project_paths": len(rows),
        "unique_file_hashes": len(unique_rows),
        "canonical_curated_active_paths": len(curated),
        "excluded_duplicate_or_incomplete_paths": len(excluded),
        "organizational_or_other_copy_paths": len(rows) - len(curated) - len(excluded),
        "raw_files_modified": False,
        "correction_basis": CORRECTION_BASIS,
    }
    output_root.mkdir(parents=True, exist_ok=True)
    (output_root / "manifest_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    assert all("nh4cl" not in str(row["normalized_display_filename"]).lower() for row in rows)
    assert all(row["raw_file_renamed_or_modified"] == "no" for row in rows)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

