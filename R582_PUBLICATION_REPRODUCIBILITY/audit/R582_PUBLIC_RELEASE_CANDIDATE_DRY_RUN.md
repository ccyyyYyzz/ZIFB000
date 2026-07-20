# R582 public reproducibility release-candidate dry run

Date: 2026-07-20  
Status: **LOCAL CONTENT GATES PASS; FINAL REBUILD/TAG PUBLICATION PENDING**

No commit, push, merge, tag, release or DOI action is asserted by this report.

## Locked release identity

- Tag: `r582-zifb-positive-electrode-reproducibility-v1`
- Title: `R582 ZIFB positive-electrode reproducibility package v1`
- Tagged directory:
  `https://github.com/ccyyyYyzz/ZIFB000/tree/r582-zifb-positive-electrode-reproducibility-v1/R582_PUBLICATION_REPRODUCIBILITY`
- Release page:
  `https://github.com/ccyyyYyzz/ZIFB000/releases/tag/r582-zifb-positive-electrode-reproducibility-v1`

The tagged-directory target is already embedded in the current main/SI sources
and PDFs. No repository placeholder remains and no DOI is claimed. The URL is
not publication-valid until the approved tag exists and resolves publicly.

## Canonical manuscript snapshot

| Object | SHA-256 |
|---|---|
| `main_R582.tex` | `8AE9FF4F244E9D5AB2308D88E3B1E98BC5C9E946931F2CD7EF6A9CAA7D3E606D` |
| `main_R582.pdf` | `5662806744E1B989808FDAD316F1C7C52433937048DDB129C4F291AB45CCCD1B` |
| `SI_R582.tex` | `8BDC18C71088398E0E9B1A55359FA3FDF688DE536B49C2C6C497EA34C47F6C1C` |
| `SI_R582.pdf` | `67C3AB505395721303D691DE9EF75D2B82CD32FCA48C65C90D2DF343BC46B1DD` |
| `refs.bib` | `5CFD59B79994E43C90C0B1E5BFDB0002593C9343DA2E2526AC2BEB84C52B4D20` |

## Locally verified content boundary

The canonical builder is `build_r582_public_release_candidate.py`; the
independent verifier is `verify_r582_public_release_candidate.py`. The latest
local candidate contained:

- 6 main and 13 SI active figures;
- 17 active source/QA bundles and their renderer dependencies;
- ten exact MD case identity bundles;
- 34 adopted single-I2 CP2K input/output/geometry identity records;
- continuum-model identities, scripts, derived exports and an access boundary;
- the bounded R582 README and `EXP-META-001` correction manifest.

Original experimental acquisitions, all original COMSOL `.mph` files, molecular
trajectories, LaTeX auxiliaries, secrets and files at or above GitHub's 100 MiB
hard limit are excluded. NH4Br remains a representative supporting electrolyte;
the porous ZIFB positive electrode remains the subject.

The independent verifier passed the local candidate with no files above 50 MiB,
no files at or above 100 MiB and no secret-pattern hits. Because this audit refresh
changes packaged QA records, the canonical builder and verifier must be rerun once
more before the release commit is frozen; earlier package byte counts and content-
root digests must not be treated as final.

## Remaining gates

1. Obtain verified author, affiliation, corresponding-author, CRediT, funding,
   acknowledgements and disclosure metadata without invention.
2. Rerun the release builder and verifier after the final human-metadata/cold-build
   freeze; record the new manifest and content-root digest.
3. Review the exact Git diff, then commit/push/merge only the approved R582 package.
4. Publish the locked tag/release and verify both URLs without a private login;
   record the full commit SHA and release date.
5. Confirm release immutability. Never move the tag; publish a new versioned tag if
   later source changes are required.
6. Add a DOI only if a real repository deposit issues one.
