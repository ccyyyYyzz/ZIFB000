# R582 citation audit baseline

Date: 2026-07-20  
Canonical scope: `main_R582.tex`, `SI_R582.tex`, and `refs.bib`

## Local integrity scan

The citation-verifier local scan was rerun against the current canonical R582
sources, followed by an independent union/key/DOI check.

- Main text: 39 unique citation keys, 45 citation occurrences.
- Supplementary Information: 24 unique citation keys, 25 occurrences.
- Union: 44 unique cited keys.
- Bibliography: 116 unique entries and no duplicate BibTeX keys.
- Missing cited keys: 0.
- Placeholder/TODO citation markers: 0.
- Duplicate DOI groups: 0.
- Cited entries without a DOI field: 0.
- Currently unused bibliography entries: 72. `unsrtnat` prints only the 44
  cited entries, so these retained anchors do not enter the submitted PDF.

## DOI identity verification

`verify_cited_dois_crossref.py` now reads `main_R582.tex` and `SI_R582.tex`
directly. All 44 active cited entries passed DOI/title/year identity verification
on 2026-07-20 (`PASS 44`, `WARN 0`, `FAIL 0`). `Park2021` was checked against
the publisher-linked KCI record because chemical-title punctuation lowers the
automated similarity score. `Tichter2020` is an institutional Refubium DOI not
indexed by Crossref and was checked against the official repository record.
Machine-readable and Markdown results are saved as
`CITATION_DOI_CROSSREF_AUDIT.json` and `CITATION_DOI_CROSSREF_AUDIT.md`.

## Content-level boundaries retained in the canonical sources

1. Confined solid-iodine hosts are not used as evidence that retained solid
   necessarily removes accessibility. Published confined-host results include
   retained iodine without performance loss.
2. Voltage and continuum fields are not used to infer a unique film, island,
   coverage, or pore-blocking morphology. The retained-solid-to-accessibility
   relation remains a calibrated model closure.
3. `Jang2021` supports an iodine-film-associated impedance effect only within
   the paper's actual system and conditions.
4. The four `Zhao2022` dissolution rates remain separated by concentration and
   measurement method. They are external kinetic scales, not a validation band
   or measured ceiling for this cell.
5. The filename errors recorded in `R576_anchor_table.md` remain quarantined:
   the file formerly named `ChemRev_Bazant2022.pdf` is Bui et al., and the file
   formerly named `Davies1952.pdf` is Katzin and Gebert (1955). Filenames are
   not citation authority.
6. Operando and spectroscopic work in other iodine hosts or cell architectures
   is used only as qualitative context unless the quantity and conditions are
   explicitly comparable.
7. Negative-electrode, shuttle, and phase-separation studies remain
   competing-pathway boundaries, not positive-electrode validation.

## Freeze status

The canonical citation chain is closed for the current R582 snapshot. The exact
tag URL `r582-zifb-positive-electrode-reproducibility-v1` is already embedded in
main and SI, with no repository placeholder and no invented DOI. Publication and
public resolution of that tag remain release operations. Any later insertion of
human author metadata requires a fresh citation/log/font/hash gate, even if the
scientific citations do not change.
