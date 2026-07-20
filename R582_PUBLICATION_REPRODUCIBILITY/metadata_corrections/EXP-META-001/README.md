# NH4Cl → NH4Br operator-confirmed metadata correction

The legacy acquisition filenames and condition labels containing `NH4Cl` or
`NH4CL` are metadata-entry errors. The project owner/experimenter confirmed on
2026-07-11 that all affected experiments were prepared with `NH4Br`.

Raw `.ndax` files and filenames are preserved byte-for-byte. The accompanying
manifests record the original path, immutable SHA-256 hash, normalized display
label, duplicate/copy relationships, and the basis for the correction. The
normalization is used only when interpreting or displaying experimental
conditions; it does not alter the raw files or make an excluded/incomplete file
eligible for analysis.

Generated files:

- `NH4CL_TO_NH4BR_PATH_MANIFEST.csv`: every matching project path.
- `NH4CL_TO_NH4BR_UNIQUE_FILE_MANIFEST.csv`: one row per unique SHA-256.
- `manifest_summary.json`: counts and validation status.

Generator:

`battery_experiment/05_source_code/tools/R581_build_nh4br_metadata_correction_manifest.py`

