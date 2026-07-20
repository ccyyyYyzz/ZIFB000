# R582 public-release black-box reproduction audit

**Verdict: PASS.** The independently copied public package passed its own verifier, all 17 renderer entry points, all four packaged audit entry points, exact regeneration of all 76 publication-format figure files, the 21-record font gate, and cold compilation of the main text and SI.

## Audited snapshot and boundary

- Package content-root SHA-256: `D020B80B54108517CF143B6BA39C2AB969CF92E9BFA969A82AB37BF9F7EC51CF`.
- `FILE_SHA256_MANIFEST.csv`: 721 manifested files, 118,938,824 bytes. The canonical content-root calculation excludes the manifest and `PACKAGE_DIGESTS.json`, so its internal scope is 720 files and 118,938,473 bytes.
- Fresh scratch: `E:\zifb_final_9129_luck\manuscript\audit_R582\release_repro_scratch_FINAL_20260720_152438\R582_PUBLICATION_REPRODUCIBILITY`.
- `verify_release.py`: PASS for 6 main and 13 SI figures, 10 MD cases, 34 CP2K identity records, no file over 50 MiB, and no secret-pattern hit.
- `EXP-META-001` is retained: legacy `NH4Cl`/`NH4CL` experiment labels are operator-confirmed metadata-entry errors for cells prepared with NH4Br. The 114 matching paths/39 unique hashes remain immutable; raw files and filenames were not rewritten.
- The canonical manuscript, canonical source data, public candidate, Git worktree, and original COMSOL files were not modified. All executions and generated files stayed in the scratch copy.
- The package verifier was run before any renderer, compiler, or audit entry point could mutate generated records.

## Renderer and artifact result

- Renderers: **17/17 PASS**.
- Publication figures: **19/19 reproduced**.
- PDF/SVG/PNG/TIFF outputs: **76/76 byte-exact SHA-256 matches** against both the frozen candidate files and `FIGURE_RELEASE_MANIFEST.csv`.
- Scratch-external project reads blocked or attempted: **0**.
- Renderer-local unique package paths opened (sum across entry points): **407**; the exact path arrays and subprocess commands are preserved in the JSON report.

| Entry | Figures | Exit | Time (s) | Package paths | Exact hashes | Font |
|---|---|---:|---:|---:|---:|---|
| `main_1` | Fig_R582_experimental_problem | 0 | 16.204 | 20 | 4/4 | PASS |
| `main_2` | Fig_R582_domain_state_v2 | 0 | 10.798 | 18 | 4/4 | PASS |
| `main_3` | Fig_R582_spatial_progression_v3 | 0 | 20.142 | 11 | 4/4 | PASS |
| `main_4` | Fig_R582_closure_identifiability | 0 | 22.240 | 32 | 4/4 | PASS |
| `main_5` | Fig_R582_multiscale_bounds_v2 | 0 | 17.689 | 29 | 4/4 | PASS |
| `main_6` | Fig_R582_operating_levers_v2 | 0 | 13.879 | 25 | 4/4 | PASS |
| `si_1` | SIFig_R582_S1_derivative | 0 | 12.711 | 20 | 4/4 | PASS |
| `si_2` | SIFig_R582_S2_composition | 0 | 10.308 | 18 | 4/4 | PASS |
| `si_3` | SIFig_R582_S3_compression | 0 | 10.765 | 19 | 4/4 | PASS |
| `si_4` | Fig_SI_R582_S4_state_function_fields | 0 | 58.148 | 19 | 4/4 | PASS |
| `si_5` | Fig_SI_R582_S5_hydraulic_fields | 0 | 40.335 | 19 | 4/4 | PASS |
| `si_6` | SIFig_R582_S6_voltage_degeneracy | 0 | 16.366 | 25 | 4/4 | PASS |
| `si_7_9` | Fig_R582_SI07_single_I2_ordering, Fig_R582_SI08_two_I2_diagnostic, Fig_R582_SI09_md_carrier_ladder | 0 | 32.166 | 61 | 12/12 | PASS |
| `si_10` | SIFig_R582_S10_comparator_definitions | 0 | 19.975 | 26 | 4/4 | PASS |
| `si_11` | SIFig_R582_S11_accessibility_families | 0 | 15.927 | 23 | 4/4 | PASS |
| `si_12` | SIFig_R582_S12_flow_postprocess | 0 | 14.641 | 21 | 4/4 | PASS |
| `si_13` | SIFig_R582_S13_smooth_permeability | 0 | 14.973 | 21 | 4/4 | PASS |

## Font identity

- Packaged gate records: **21/21**; failures: **0**.
- All 19 active figure PDFs contain embedded, subset TeX Gyre Termes and no Type 3 or forbidden Arial/Helvetica/DejaVu/Liberation/Calibri/Times New Roman/Nimbus Roman family.
- All 19 SVG masters retain editable text, explicitly declare TeX Gyre Termes, and contain no forbidden fallback family.
- Main and SI body text uses TeX Gyre Termes; NewTX mathematics and SFTT monospace are the expected non-body families.
- The renderer trace records the actual TeX Gyre Termes OTF runtime files; no renderer read project data outside the fresh scratch.

## Cold LaTeX reproduction

- `main_R582.tex`: exit 0; 17 pages; 469089 bytes; log findings 0; hyperlinks 3/3; normalized PDF content match `True`. Raw SHA-256 candidate `5662806744E1B989808FDAD316F1C7C52433937048DDB129C4F291AB45CCCD1B`, cold build `24E7001CF97DE72F911DA491139EB276619C8414B4299F440094000DA9A90FA4`.
- `SI_R582.tex`: exit 0; 26 pages; 922460 bytes; log findings 0; hyperlinks 1/1; normalized PDF content match `True`. Raw SHA-256 candidate `67C3AB505395721303D691DE9EF75D2B82CD32FCA48C65C90D2DF343BC46B1DD`, cold build `17B5D257F33D368653338EB023824908EFBC2139121FEC56ED05AFB6B6B68F4B`.

Raw document PDF hashes may differ because pdfTeX refreshes `/CreationDate`, `/ModDate`, and the trailer `/ID`. Removing only those metadata fields makes each cold build byte-identical to its frozen candidate PDF; page count, size, resources, fonts, layout, and hyperlinks are unchanged.

## Packaged audit entry points

- `audit/check_r582_language_and_format.py`: exit 0 in 0.223 s.
- `audit/extract_verify_r582_figure_captions.py`: exit 0 in 0.231 s.
- `audit/verify_cited_dois_crossref.py`: exit 0 in 1.505 s.
- `audit/check_font_consistency.py`: exit 0 in 1.677 s.

The font gate is fail-closed at 21 PDF records/19 figures; the language gate is fail-closed on both TeX files, 6 main figures, and 7 keywords; caption extraction resolves package `manuscript/`, `submission/`, and `audit/`; DOI verification is fail-closed at 44 cited keys.

## Interpretation

This audit establishes standalone computational reproducibility of the published plotting layer and document build from the public package. COMSOL was not rerun because the release intentionally exposes frozen solved/exported evidence rather than proprietary solver binaries; no new physical experiment was introduced. Earlier scratch directories are retained as discovery evidence and are not part of the final PASS verdict.

Machine-readable detail: the JSON contains every renderer-local package path opened, subprocess command, 76 artifact hashes, the complete 21-record font gate, compiler-log scans, hyperlink output, and the final package-manifest delta. The CSV is the compact 17-entry renderer ledger.
