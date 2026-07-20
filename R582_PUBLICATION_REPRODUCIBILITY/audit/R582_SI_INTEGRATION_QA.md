# R582 Supplementary Information integration QA

Date: 2026-07-20  
Scope: `manuscript/SI_R582.tex`, its compiled PDF, and the 13 registered SI figure PDFs referenced by it.  
Status: **PASS for scientific/technical integration, current cold build and rendered layout.** The exact planned tag URL is embedded; public tag resolution and human author metadata remain.

## Frozen candidate identity

- Source: `manuscript/SI_R582.tex`
- Source SHA-256: `8BDC18C71088398E0E9B1A55359FA3FDF688DE536B49C2C6C497EA34C47F6C1C`
- PDF: `manuscript/SI_R582.pdf`
- PDF SHA-256: `67C3AB505395721303D691DE9EF75D2B82CD32FCA48C65C90D2DF343BC46B1DD`
- PDF size: 922,460 bytes
- PDF extent: 26 US-letter pages
- Structure: 8 numbered sections, 13 registered figures, 18 registered tables and 31 captions

## Identity and evidence checks

- `EXP-META-001` occurs at the first experimental-provenance statement. The only `NH4Cl` token in the SI is in that correction statement: every legacy filename/condition field carrying that label denotes NH4Br; raw names, bytes and hashes remain unchanged and derived labels use NH4Br.
- NH4Br is treated only as a representative supporting electrolyte. The positive electrode remains the paper's subject.
- Continuum identities are kept distinct throughout: `R_theta = 1 - theta_cal`, `T_pore = (K/K0)^(1/2)`, and native `A_bare/A0 = R_theta T_pore`.
- `Q_f,cal` is defined by `<theta_cal> = 0.5` (equivalently `<R_theta> = 0.5`), never by halving the native product.
- Figure S11 semantics are locked: coloured curves are single-fibre geometric `A/A0`; the dashed curve is the `R_theta` comparator; native `A_bare/A0` is not plotted because `T_pore` is absent. Figure S11 SHA-256 is `13BE70194D8CB1BED6E3E8DE40CD49B671ED69C4AC7B2F42BBD7009C518F6716`.
- Figure S7 and Table S13 now use the same quantity and terminology: the plot is labelled **BSSE-corrected adsorption-energy ordering** with axis `Delta E_ads (eV)`, and the table's first numeric column is **BSSE-corrected adsorption energy (eV)**. Both are kept separate from the compact-versus-separated relative electronic-energy diagnostic. Figure S7 SHA-256 is `FE1D6FCCB1FCF062D39FA60404E3944366BD4791C104C2E0A1B5C662C8A6AD8D`.
- Derivative landmarks are explicitly excluded from calibration of `Q_s` and `Q_f,cal`; the SI identifies `Q_f,cal` as belonging to the pre-existing voltage-calibrated continuum branch and states that reuse of the same full-cell trace in the reduced observation-layer fit is not independent validation.
- The scan-ranking conclusion is restricted to the selected variables carried into main Figure 6. The SI separately reports that `gamma_salt = 2--4` spans a larger total response, while identifying this range as an E-LIT/PRES prior rather than a fitted law or experimental axis.
- Method statements now cite the primary sources for Savitzky--Golay processing, velocity-rescale and canonical-rescale thermostats, PME electrostatics, and the ALPB implicit-solvent model; the compiled SI contains 24 references.
- No original `.mph`, raw experimental file or external project tree was modified.
- Section S8.2 contains the exact planned tagged-directory URL
  `https://github.com/ccyyyYyzz/ZIFB000/tree/r582-zifb-positive-electrode-reproducibility-v1/R582_PUBLICATION_REPRODUCIBILITY`;
  no repository placeholder or future-tense promise remains. The source states that no repository DOI had been assigned at submission.

## Compilation and structural QA

Cold build command:

```text
D:\Program Files\texlive\2024\bin\windows\latexmk.exe -C SI_R582.tex
D:\Program Files\texlive\2024\bin\windows\latexmk.exe -pdf -interaction=nonstopmode -halt-on-error SI_R582.tex
```

Final `SI_R582.log` scan: zero `Overfull`, `Underfull`, `Warning:`, undefined reference/citation, missing-character or float-only-page warnings. Counts were independently read from the source labels/captions.

## Font and visual QA

- Body font: `tgtermes`; mathematics: `newtxmath`.
- `audit_R582/check_font_consistency.py` passed for the main PDF, SI PDF and every referenced main/SI figure: TeX Gyre Termes present, no forbidden family and no Type 3 font.
- All 26 pages were rendered at 110 dpi to `manuscript/tmp/pdfs/SI_R582_release_candidate/` and reviewed as contact sheets and at page resolution for dense tables and the repaired comparator figures.
- The contents list fits page 1. Subsection barriers and flexible floats keep headings and lead text before their objects. The former blank/orphan page before Table S16 is removed; the scan matrix and its S7 heading/definitions share one landscape page. No visible clipping, overlap or nearly empty carryover page remains.
- Colour/grayscale review preserved line-style and marker redundancy in the registered plots; figure fonts match the manuscript family.
- After the release-identity insertion, page 24 was rerendered at 160 dpi and inspected; Table S18 and S8.2 remain unclipped and legible. PDF annotation inspection confirms the exact planned tagged-directory target. Temporary render files were removed after inspection.

## Remaining human/release gates

1. Replace the verified-author/affiliation placeholders with approved human metadata.
2. Publish `r582-zifb-positive-electrode-reproducibility-v1`, verify that the embedded tagged-directory URL resolves to the approved commit, and record the commit SHA/release date. Add a DOI only if one is actually issued.
3. Rebuild the main manuscript and SI together after any author/disclosure metadata insertion, then rerun citation, log, font, hyperlink and hash gates. An immutable tag must never be moved; use a new versioned tag if its contents need to change.

No unresolved scientific or technical SI blocker was found in this integration pass.
