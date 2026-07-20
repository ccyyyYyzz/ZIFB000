# R582 main-TeX integration QA

Date: 2026-07-20  
Status: **PASS for scientific-text integration, cold build, references, figures, fonts, caption synchronization and visual layout. The exact planned tag URL is embedded; only publication of that tag and human-supplied metadata remain.**

## Scope and immutability

- Audited the current cold-built `manuscript/main_R582.tex`, `manuscript/main_R582.pdf` and `manuscript/highlights_R582.txt` after the Data Availability identity was frozen.
- Integrated the R582 scientific text, evidence-identity corrections and verified method citations without altering protected legacy manuscript files or original evidence.
- Did not edit `manuscript/main.tex`, `manuscript/SI.tex` or `manuscript/main.pdf`. `manuscript/refs.bib` was extended with five verified method references used by R582.
- Current protected-file SHA-256 values at hand-off:
  - `main.tex`: `65E0D63F0B0D57BF5FCC82BC02432637B438B4010481A2E1210891A1A252E82A`
  - `SI.tex`: `72FE4B26800DF18D42B1467F25B993FA639922427397F46B2B46E7F2BDE20B37`
  - `refs.bib`: `5CFD59B79994E43C90C0B1E5BFDB0002593C9343DA2E2526AC2BEB84C52B4D20`
  - `main.pdf`: `0AEF202B2F74B7919898DC3210260B7B8E61986387CF66DE9099843AE1FC3DA1`

## Manuscript structure

- Article/natbib/siunitx/mhchem toolchain retained.
- Body font: `tgtermes`; mathematics: `newtxmath`.
- Latest title, 187-word abstract, seven keywords, Introduction, six Methods-summary subsections, six Results-and-discussion subsections, Conclusions and Data availability are present.
- Main figures are included once each, in the required order and at `width=\textwidth`:
  1. `Fig_R582_experimental_problem.pdf`
  2. `Fig_R582_domain_state_v2.pdf`
  3. `Fig_R582_spatial_progression_v3.pdf`
  4. `Fig_R582_closure_identifiability.pdf`
  5. `Fig_R582_multiscale_bounds_v2.pdf`
  6. `Fig_R582_operating_levers_v2.pdf`
- Figure pages are interleaved with their Results subsections (PDF pages 6, 7, 8, 10, 11 and 12), preventing a float backlog.
- Figure 3 caption names the registered native `A_bare/A0` field, retains the six signed negative-current nodes as a neutral mask, and makes no morphology inference.
- Figure 6 contains panels a--c only; no panel-d caption or claim remains.
- `EXP-META-001` occurs exactly once, in Methods. The sole legacy `NH4Cl` token occurs only in that correction sentence.
- `NH4Br` is described as the representative supporting electrolyte; the porous ZIFB positive electrode remains the subject.
- Data Availability contains the exact planned tag target
  `https://github.com/ccyyyYyzz/ZIFB000/tree/r582-zifb-positive-electrode-reproducibility-v1/R582_PUBLICATION_REPRODUCIBILITY`.
  No repository placeholder remains, and the manuscript truthfully states that no repository DOI had been assigned at submission. Public tag resolution is still a release operation.

## Caption synchronization

- Figure 1: synchronized to the calibrated-model provenance: derivative landmarks did not set $Q_s$ or $Q_{f,\mathrm{cal}}$, while $Q_{f,\mathrm{cal}}$ belongs to a voltage-calibrated branch and the overlay is not independent validation.
- Figure 2: `CAPTION_DRAFT_v2.md`.
- Figure 3: `CAPTION_DRAFT_v3.md`.
- Figure 4: `Fig_R582_closure_identifiability_CAPTION.md`.
- Figure 5: synchronized to the repaired v2 artwork: panel a reports BSSE-corrected adsorption-energy ordering and panel c reports geometric single-fibre $A/A_0$, distinct from native continuum $A_{\mathrm{bare}}/A_0=R_\theta T_{\mathrm{pore}}$.
- Figure 6: synchronized to `R582_Fig6_v2_CAPTION.md`; all cross-matrix superlatives were removed and the comparison is restricted to the displayed operating/transport variables and ranges.

## Cold compile and references

Command run from `manuscript/`:

```powershell
& 'D:\Program Files\texlive\2024\bin\windows\latexmk.exe' -C main_R582.tex
& 'D:\Program Files\texlive\2024\bin\windows\latexmk.exe' -pdf -interaction=nonstopmode -halt-on-error -file-line-error main_R582.tex
```

- Exit code: 0.
- Final PDF: 17 US-letter pages, 469,089 bytes, PDF 1.5.
- Final log scan: 0 undefined citations, 0 undefined references, 0 LaTeX/natbib warnings, 0 overfull boxes, 0 underfull boxes and 0 errors.
- Unique cited keys: 39.
- Unique bibliography keys: 116.
- Cited keys absent from `refs.bib`: 0.
- `main_R582.tex` SHA-256: `8AE9FF4F244E9D5AB2308D88E3B1E98BC5C9E946931F2CD7EF6A9CAA7D3E606D`.
- `main_R582.pdf` SHA-256: `5662806744E1B989808FDAD316F1C7C52433937048DDB129C4F291AB45CCCD1B`.

## Font gate

`pdffonts manuscript/main_R582.pdf` reports 28 embedded/subset font rows.

- Main text: TeX Gyre Termes regular/bold/italic.
- Main-figure text: embedded TeX Gyre Termes regular/bold/italic.
- Mathematics: newtx families.
- The sole non-Termes text face is embedded SFTT1095 for the literal `\texttt{NH4Cl}` metadata token.
- Arial: 0.
- Helvetica: 0.
- DejaVu: 0.
- Times New Roman: 0.
- Type 3: 0.

The complete main/SI + 19-active-figure result is frozen in `R582_FINAL_FONT_GATE.json` with 21 records, `failures=[]`, SHA-256 `0284E505C719A62AB0E0FE45A13A57E055D6E91F302EA236A82F9A5F775B6753`.

## Figure identities

| Figure | PDF SHA-256 |
|---|---|
| Fig. 1 | `5C22E28071F9BC1B5FBAAB62E38FB2628F6D3D22A69162E366E752E6C86A7E16` |
| Fig. 2 v2 | `64254BD25A0324739665DACA8D82F4FBD1177791F58071FA032850845BBAF6A7` |
| Fig. 3 v3 | `50282811313DD953A5014B4DC68A09AD46E05173ECD029F655FDAA85A25CDA10` |
| Fig. 4 | `073F1E40D5E54FB8BD47955AEEE5A5D27BC33C4BF6B2320609DFDBAAE8D10F4F` |
| Fig. 5 v2 | `9FD7827DAB7446688CA04C4818D2DE2EB54BA6A3670B87BD0D0273330C817491` |
| Fig. 6 v2 | `459C497BA4C1EE7FBD02121DE01601793618D4E79BFD7B3208B8776EDD28D256` |

Provenance note: the actual Fig. 1 PDF hash agrees with `R582_Fig1_build.json`, `R582_Fig1_QA.md` and `ROOT_ACCEPTANCE.md`. Its derived tables now state the exact calibration boundary rather than the earlier blanket independence claim.

## Visual PDF QA

- The pre-metadata 17-page manuscript had already received a complete Poppler page-by-page review. After inserting the tag identity, pages 13--14 were rerendered at 160 dpi and inspected; the Data Availability split, hyperlink, author-metadata placeholders and bibliography transition are clean. Temporary render files were removed after inspection.
- No clipping, overlap, missing glyph, broken reference, stranded one-line page, unreadable caption or incorrect figure order remains.
- The six artwork fonts visually match the Termes manuscript face.
- PDF annotation inspection confirms that the wrapped hyperlink on page 13 resolves to the exact planned tagged-directory URL.

## Highlights

`highlights_R582.txt` SHA-256: `FD9600E5D4FD78BC9E1BBFF5E0B626B84E272C0DCE9F27A8766C646B0C40FAB0`.

Character counts are 77, 68, 76, 68 and 73; all five lines satisfy the 85-character limit.

## Intentionally unresolved human/release metadata

No project-verified facts were available for the author list/order, affiliations, corresponding-author contact, CRediT allocation, funding/grants/facility acknowledgements or author-approved disclosure text. Explicit visible placeholders are retained for the author/CRediT/funding fields; none was guessed. The repository identity is no longer a placeholder: its exact tag URL is frozen in the source and PDF, but the tag must still be published and verified publicly. No DOI is claimed.
