
# Immutable release identity and publication checklist

- Tag: `r582-zifb-positive-electrode-reproducibility-v1`
- Release title: `R582 ZIFB positive-electrode reproducibility package v1`
- Stable tagged-directory URL: `https://github.com/ccyyyYyzz/ZIFB000/tree/r582-zifb-positive-electrode-reproducibility-v1/R582_PUBLICATION_REPRODUCIBILITY`
- Release URL: `https://github.com/ccyyyYyzz/ZIFB000/releases/tag/r582-zifb-positive-electrode-reproducibility-v1`

Neither URL is publication-valid until the approved commit is pushed, the tag is
created at that exact commit, and the release is published.

Before publication, enable GitHub release immutability for the repository. Then:

1. cold-build and verify main/SI;
2. rerun the R582 candidate builder and verifier;
3. review `DRY_RUN_RELEASE_REPORT.md` and all human-only metadata fields;
4. commit and push the approved snapshot;
5. create a draft release for `r582-zifb-positive-electrode-reproducibility-v1` and attach any final archive asset;
6. publish the release and confirm that GitHub marks it `Immutable`;
7. verify the release/tag and confirm that the tagged-directory URL already embedded
   in the manuscript Data Availability statement resolves to this exact commit.

No DOI is assigned or implied by this plan.
