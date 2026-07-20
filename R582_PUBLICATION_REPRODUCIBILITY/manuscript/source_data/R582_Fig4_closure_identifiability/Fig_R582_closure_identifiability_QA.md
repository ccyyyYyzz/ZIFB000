# Fig_R582_closure_identifiability QA

Status: **PROTOTYPE QA PASS**

## Scientific contract

- PASS — matched $Q_s$ values are `82.890294316` and `82.892359092 mAh cm^-2` (`Delta = 0.002064776 mAh cm^-2`).
- PASS — the coupled-island minus baseline endpoint voltage difference is `-288.156257160 mV`.
- PASS — panel a uses `R_theta = 1 - theta`; it does not relabel this observation-layer factor as native `A_bare/A0`.
- PASS — panel c uses each solved branch's own solid inventory and only the baseline and island `R_theta=0.5` references.
- PASS — panel d reconstructs the fixed `70.812528227 mV` voltage contribution from every registered source point.
- PASS — no deposit image, film, pore blockage, or unique morphology is encoded or inferred.

## Evidence identity (source package only)

- Production authority: `PB-R526-J40-Q120-DSET5-v1`; input MPH SHA-256 `4813B306F39330CCEAF819C4AB8815C55A3DF8A04726741F33ACB801B8806B9B`; `stdR522/sol5/dset5`.
- Matched true-mesh control: `dsetR581CtrlMesh`; physical branch: `dsetR581PhysMesh`; study `stdR522`, solution `sol5`, `7776` elements, `rtol=0.0003`.
- Parameter inventories are identical; the release summary records that no raw/original MPH file was modified.

## Typography and export

- PASS — figure family is `TeX Gyre Termes`; regular font SHA-256 `CC3FE7C707B81428D23D54DF3EADD9228A2BF6A4D43125D94DF56F5F63134659`.
- PASS — SVG contains `70` editable `<text>` nodes and explicitly declares TeX Gyre Termes.
- PASS — PDF font table contains TeX Gyre Termes and no Type 3 font. Tool: `D:\Program Files\texlive\2024\bin\windows\pdffonts.EXE`.
- PASS — PDF page is `179.9999 × 117.9999 mm`.
- PASS — 600-dpi PNG/TIFF dimensions are approximately `4252 × 2787 px`; both are opaque RGB.
- PASS — 180-mm preview and grayscale QA are `2126 × 1394 px` at 300 dpi.
- PASS — all labels/ticks use configured base sizes of 6.5 pt or larger; mathematical super/subscripts follow the manuscript's Termes math styling.
- PASS — colors are redundantly encoded by line style or marker; the grayscale preview is provided for visual inspection.

## Determinism

- PASS — `svg` is byte-identical across two independent renders.
- PASS — `pdf` is byte-identical across two independent renders.
- PASS — `png` is byte-identical across two independent renders.
- PASS — `tiff` is byte-identical across two independent renders.
- PASS — `preview` is byte-identical across two independent renders.
- PASS — `grayscale` is byte-identical across two independent renders.

## PDF font table

```text
name                                 type              encoding         emb sub uni object ID
------------------------------------ ----------------- ---------------- --- --- --- ---------
CCVYUO+TeXGyreTermes-Bold            CID Type 0C (OT)  Identity-H       yes yes yes     19  0
CCVYUO+TeXGyreTermes-Italic          CID Type 0C (OT)  Identity-H       yes yes yes     26  0
CCVYUO+TeXGyreTermes-Regular         CID Type 0C (OT)  Identity-H       yes yes yes     33  0
```
