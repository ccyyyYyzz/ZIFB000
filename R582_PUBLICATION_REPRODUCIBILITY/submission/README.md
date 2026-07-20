# R582 submission package — Journal of Power Sources

Working article type: **Research Paper**.  
Manuscript title: **A positive-electrode model separating iodine saturation from accessibility loss in zinc–iodine flow batteries**.

This folder contains venue-facing text and release checklists for the R582 manuscript. The porous ZIFB positive electrode is the paper’s subject. NH4Br appears only as a representative supporting electrolyte. Existing full-cell records anchor the late-charge problem but do not independently measure the modeled internal positive-electrode states.

## Current submission files

- `HIGHLIGHTS.txt` — five upload-ready lines; each is 85 characters or fewer.
- `COVER_LETTER_DRAFT.md` — science-complete JPS draft; date and signature remain human-only.
- `AUTHOR_METADATA_REQUIRED.md` — author, affiliation, correspondence, funding and portal fields that cannot be inferred.
- `CREDIT_AUTHOR_STATEMENT_TEMPLATE.md` — JPS/CRediT worksheet awaiting verified contributors.
- `DECLARATION_OF_INTEREST.md` — two-route worksheet; the journal-generated `.doc`/`.docx` remains required.
- `GENERATIVE_AI_DECLARATION_DRAFT.md` — disclosure text awaiting author approval and insertion before the references.
- `REPOSITORY_DEPOSIT_CHECKLIST.md` — data-policy, reproducibility, EXP-META-001 and public-release gates.
- `GRAPHICAL_ABSTRACT_MANUAL_SPEC.md` — optional, human-controlled graphical-abstract specification; it does not contain artwork.
- `VENUE_DECISION.md` — R582 JPS venue decision and explicit computational-evidence risk.
- `FIGURE_CAPTIONS_DRAFT.md` and `.tex` — automatically extracted, verbatim copies of the 6 main and 13 SI figure captions; valid only while their embedded source hashes match `main_R582.tex` and `SI_R582.tex`.

## Supporting files that must be refreshed at the final freeze

- `REPRODUCIBILITY_ENVIRONMENT.md` and `environment.yml` retain an earlier environment snapshot and must be reconciled with the final R582 scripts before release.

## Repository identity already locked in the manuscript

- Planned immutable tag: `r582-zifb-positive-electrode-reproducibility-v1`.
- Tagged-directory target: `https://github.com/ccyyyYyzz/ZIFB000/tree/r582-zifb-positive-electrode-reproducibility-v1/R582_PUBLICATION_REPRODUCIBILITY`.
- The exact target is already embedded in `main_R582.tex`, `SI_R582.tex` and their current PDFs; no repository placeholder remains.
- No DOI is claimed. The URL is publication-valid only after the approved tag/release is published and verified from a non-private session.

## Scientific integrity locks

- `EXP-META-001`: legacy experimental labels containing `NH4Cl` or `NH4CL` refer to experiments performed with NH4Br. Raw filenames, bytes and hashes remain unchanged; derived tables use the corrected identity.
- Original experimental records and original COMSOL `.mph` files are immutable.
- Changing the accessibility relation is reported as controlled model-form sensitivity, not identification of a film, island or pore-spanning deposit.
- Continuum fields are model outputs, not microscopy.
- No generative AI image synthesis or AI-assisted image alteration is permitted for manuscript figures or a graphical abstract.

## Upload blockers

1. Replace author, affiliation and corresponding-author placeholders with an approved definitive record.
2. Approve the CRediT roles, funding/acknowledgements, competing-interest form and AI declaration.
3. Publish the already locked tag identity, verify its exact URL/commit from a clean download and record the release date/commit SHA.
4. Reconcile the environment files and rerun the release builder/verifier after any human-metadata change. The current caption extraction already matches the current canonical source hashes.
5. Repeat main/SI cold-build, citation, source-data, visual, font, hyperlink and page-by-page PDF checks after the final human metadata is inserted.
