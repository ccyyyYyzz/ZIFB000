# R582 Journal of Power Sources submission-text build report

Date: 2026-07-20  
Scope: `manuscript/submission/*` text plus caption-extraction QA under `manuscript/audit_R582`; no manuscript, SI, bibliography, figure, source-data or evidence file was edited.

## Source and claim validation

Authoritative source snapshot used for this build:

- `manuscript/main_R582.tex`: SHA-256 `8AE9FF4F244E9D5AB2308D88E3B1E98BC5C9E946931F2CD7EF6A9CAA7D3E606D`.
- `manuscript/main_R582.pdf`: SHA-256 `5662806744E1B989808FDAD316F1C7C52433937048DDB129C4F291AB45CCCD1B` (17 pages).
- `manuscript/SI_R582.tex`: SHA-256 `8BDC18C71088398E0E9B1A55359FA3FDF688DE536B49C2C6C497EA34C47F6C1C`.
- `manuscript/SI_R582.pdf`: SHA-256 `67C3AB505395721303D691DE9EF75D2B82CD32FCA48C65C90D2DF343BC46B1DD` (26 pages).
- `manuscript/refs.bib`: SHA-256 `5CFD59B79994E43C90C0B1E5BFDB0002593C9343DA2E2526AC2BEB84C52B4D20`.

| Submission claim | Main-text anchor | Result |
|---|---|---|
| 40 mA cm−2; 83.0 and 99.6 mAh cm−2 | line 34; detailed at 162 | PASS |
| Matched saturation shift 0.002 mAh cm−2 | line 34; detailed 0.0021 at 192 | PASS |
| No 50% matched accessibility loss within 120 mAh cm−2 | lines 34 and 205 | PASS |
| Matched terminal-voltage reduction 288 mV | line 34; detailed −288.2 mV at 199 and 207 | PASS |
| Applied current and oxidized-iodine diffusivity give large, directionally interpretable shifts over the selected simulated ranges | lines 34 and 242–244 | PASS |
| Full-cell records are device-scale anchors, not internal-state validation | lines 34, 48 and 143 | PASS |
| `EXP-META-001`: legacy `NH4Cl` labels mean NH4Br; raw identity preserved | line 60 | PASS |
| NH4Br is a representative supporting electrolyte | line 65 | PASS |

No author, affiliation, funding, ORCID, conflict, repository DOI or reviewer identity was inferred. The exact planned tag URL is inherited verbatim from the canonical main/SI; no DOI is claimed.

## Venue checks

The official *Journal of Power Sources* Guide for Authors was rechecked on 2026-07-20: <https://www.sciencedirect.com/journal/journal-of-power-sources/publish/guide-for-authors>.

- Highlights: 5 bullets; character counts including bullet and space are 79, 70, 78, 70 and 75 (limit: 85).
- Cover letter: 292 words after removing the Markdown heading and bracketed placeholders; below the journal’s ideal one-page length and contains no funding, author declaration or reviewer nomination. Its operating-variable sentence is explicitly limited to the selected simulated ranges.
- Graphical abstract: specification only; no artwork created. The optional canvas and no-generative-AI constraints match the guide.
- Competing interests: no unsupported no-conflict assertion; the required Elsevier `.doc`/`.docx` route is explicit.
- AI use: a transparent draft names the tools, purposes, author oversight and absence of generative-image synthesis; author approval and insertion before the references remain required.
- Data policy: the exact planned tag/directory link is now present in main/SI and the checklist. Public tag/commit resolution, checksums and clean-download verification remain required; no DOI is invented.
- Visual gate: the repository checklist requires manuscript-matched figure typography, no fallback/Type 3 fonts, a 6.5 pt minimum and color/grayscale inspection.

## Figure-caption extraction and synchronization

- A balanced-brace parser inspected only `figure`/`figure*` environments; table captions were excluded.
- Extracted counts: 6 main figures and 13 supplementary figures, total 19.
- Main order: `experimental-problem`, `domain-state`, `spatial-progression`, `closure-identifiability`, `multiscale-bounds`, `operating-levers`.
- SI order: derivative, composition, compression, six-capacity state fields, hydraulic fields, voltage degeneracy, single-I2, two-I2, MD ladder, comparator definitions, accessibility families, flow postprocess and smooth permeability.
- Both Markdown and TeX caption bodies match the authoritative source strings exactly after LF newline normalization and removal of only the outer `\caption{...}` braces.
- Titles, panel order, units and all source qualifiers are unchanged. `EXP-META-001` is retained verbatim in Supplementary Figure S1.
- Standalone TeX cold compilation passed in four pages with no warning, undefined reference, overfull box or underfull box. Its text uses TeX Gyre Termes with NewTX mathematics and contains no Type 3 font.
- Machine-readable result: `audit_R582/R582_CAPTION_EXTRACTION_QA.json` (`status: PASS`).
- Current caption source hashes are the canonical TeX hashes above; generated Markdown SHA-256 is `3D2BB38BE6F4C20FD293281DD4817D20FD2A19772B435A0A35C461372D7E07B2`, generated TeX SHA-256 is `E97CCF55A3F1D60E443E805867CA20B3E4EB20DD2D6AC1D074F7C82E2EC85D7B`, and the QA JSON SHA-256 is `2592B49C179E6BF656FCC98738529C13101E5D30A494DD8D2B5ADAB0D9ED92F1`.

## Files changed

| File | SHA-256 |
|---|---|
| `submission/HIGHLIGHTS.txt` | `17E1DD481F7C286F18A512A40469D37510C267F63D1778E202629A5C3FCE0F07` |
| `submission/COVER_LETTER_DRAFT.md` | `CADD64453225CFED61FE51FA6EA60EA1EBE2926360EE7BF893C945F2FA94DA35` |
| `submission/DECLARATION_OF_INTEREST.md` | `CAC82F3841693917761D338A4D59B328271E0EB5137D74A1A6082423BF6447E6` |
| `submission/GENERATIVE_AI_DECLARATION_DRAFT.md` | `1CA70A1A71B41E5E04F71884121C49FA3045AAFEF0663B6F5A8FEEEF9AF3D3B2` |
| `submission/AUTHOR_METADATA_REQUIRED.md` | `D5F265733707F78A981AD2BD6941B4B3286B646FC7B39FC357CFF96483377520` |
| `submission/CREDIT_AUTHOR_STATEMENT_TEMPLATE.md` | `0B1BCEB94527D21D90544FEAB7B5CC540FA4895E5E571608332221F18A3B654C` |
| `submission/REPOSITORY_DEPOSIT_CHECKLIST.md` | `7816184C91D507A1F3C33559996FE8C9CCF27603F77A9BDE8D8DA3A98AC324D9` |
| `submission/README.md` | `220CC0A80F066B83F82D943A2A3C42B8468381FE670B109F72EE50C697B40463` |
| `submission/VENUE_DECISION.md` | `249712FD681D748DE512F6A7DD9AB46B91C4501F6AEE7090C853FBA0E66A6E2E` |
| `submission/GRAPHICAL_ABSTRACT_MANUAL_SPEC.md` | `BC19CA360FBB4729AAA7E191EFACF646261EBED18DFD0F961ACAFCF7671B637A` |
| `submission/FIGURE_CAPTIONS_DRAFT.md` | `3D2BB38BE6F4C20FD293281DD4817D20FD2A19772B435A0A35C461372D7E07B2` |
| `submission/FIGURE_CAPTIONS_DRAFT.tex` | `E97CCF55A3F1D60E443E805867CA20B3E4EB20DD2D6AC1D074F7C82E2EC85D7B` |
| `audit_R582/extract_verify_r582_figure_captions.py` | `68F5FCC1B2193C41E367A8EB44BA0D0D41D8D8001364ED20066EC71BC6C1C0CE` |
| `audit_R582/R582_CAPTION_EXTRACTION_QA.json` | `2592B49C179E6BF656FCC98738529C13101E5D30A494DD8D2B5ADAB0D9ED92F1` |
| `audit_R582/R582_FINAL_FONT_GATE.json` | `0284E505C719A62AB0E0FE45A13A57E055D6E91F302EA236A82F9A5F775B6753` |
| `audit_R582/R582_JPS_SUBMISSION_TEXT_PACKAGE_BUILD_REPORT.md` | This report; self-hash omitted to avoid a recursive checksum. |

## Residual human-only fields

- Definitive author names/order, affiliations, corresponding-author contact and optional ORCIDs.
- Author-approved CRediT assignments.
- Verified funding/grant and sponsor-role statement, or confirmed no-specific-funding wording.
- Acknowledgements and permission from named individuals.
- Competing-interest responses from every author and the journal-generated Word declaration.
- Author approval of the AI-use statement and confirmation of exact tools/uses.
- Cover-letter date and corresponding-author signature block.
- Preprint/related-work disclosure and suggested/opposed reviewers if applicable in the portal.
- Publication verification of the already selected tag URL, full commit SHA/release date and DOI only if actually issued.

## Remaining technical gates outside this task

The caption copies are current for the hashes recorded above and must be regenerated if either source changes. `REPRODUCIBILITY_ENVIRONMENT.md`/`environment.yml` still require reconciliation with the final R582 scripts. Main/SI cold compilation, language/format, font, citation-key, DOI-identity and changed-page PDF checks pass for the current snapshot. Data Availability contains the exact planned tag URL and no placeholder, but the public tag/release still must be published and independently verified. Final author/disclosure metadata, public deposit and portal upload remain outside this text-only task.

Readiness: the JPS submission-side prose is scientifically aligned and mechanically current, but upload remains blocked by verified human metadata and publication of the already locked repository identity. The top venue risk is the journal’s expectation of experimental validation for computational work; the highest-leverage final action is to publish and clean-download-verify the complete R582 release without strengthening the existing full-cell evidence claim.
