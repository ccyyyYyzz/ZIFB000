
# R582 local release-candidate dry-run report

Status: **BUILT AND HASH-VERIFIED LOCALLY; NOT COMMITTED OR PUBLISHED**

- Candidate directory: `E:\zifb_final_9129_luck\github_ZIFB000_working\R582_PUBLICATION_REPRODUCIBILITY`
- Proposed tag: `r582-zifb-positive-electrode-reproducibility-v1`
- Proposed release title: `R582 ZIFB positive-electrode reproducibility package v1`
- Exact file list, byte sizes and SHA-256 values: `FILE_SHA256_MANIFEST.csv`
- Main/SI figures: 6 + 13 = 19
- Figure assets: 76 (PDF/SVG/PNG/TIFF)
- Figure source bundles: 17
- MD identities: 10 cases, exact topology/ITP/MDP/system metadata/GROMACS logs
- CP2K exact identity records: 34
- Embedded raw acquisition files: 0
- Embedded COMSOL `.mph` files: 0
- Files above GitHub 50 MiB warning threshold: 0
- Files at or above GitHub 100 MiB hard limit: 0
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
