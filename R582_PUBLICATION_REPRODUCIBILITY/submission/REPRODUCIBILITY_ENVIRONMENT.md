# R582 reproducibility environment

Frozen on 2026-07-20. Commands in the first four sections are relative to the
root of `R582_PUBLICATION_REPRODUCIBILITY` in the public release.

## Reference platform

- Microsoft Windows 11 Home, 64 bit, version 10.0.26200.
- COMSOL Multiphysics 6.3.0.290 (full-workspace numerical runs only).
- TeX Live 2024: pdfTeX 1.40.26; latexmk 4.83.
- Python 3.11.5.
- numpy 1.24.4; pandas 1.5.3; matplotlib 3.7.2; scipy 1.10.1;
  Pillow 12.2.0.

Create the minimal figure environment without relying on a workstation-specific
Python path:

```powershell
conda env create -f .\submission\environment.yml
conda activate zifb-r582-release
```

## Font and PDF-tool lock

The body uses `tgtermes` with `newtxmath`. Every active figure must use the
same four TeX Gyre Termes OTF faces. The renderers fail closed unless all four
files have these exact SHA-256 values:

| Face | File | SHA-256 |
|---|---|---|
| regular | `texgyretermes-regular.otf` | `CC3FE7C707B81428D23D54DF3EADD9228A2BF6A4D43125D94DF56F5F63134659` |
| bold | `texgyretermes-bold.otf` | `2FB3E952065FA153C7E4E64E04B98B9D79225739B6025AA3F0F0782D299FF61E` |
| italic | `texgyretermes-italic.otf` | `6DD103A1672E50568CD2F8A706CCD48443D44D7D073A59D2286F4E6F746575D6` |
| bold italic | `texgyretermes-bolditalic.otf` | `1BF6AF99CB0E26C12951317032D79B96AE009551E59CCF02A5B24F325ECFEC87` |

Discovery order is: `R582_TERMES_FONT_DIR`; then
`R582_TEXLIVE_ROOT`/`TEXLIVE_ROOT`; then `R582_KPSEWHICH` or `kpsewhich` on
`PATH`; then common TeX Live roots on drives D and C and `/usr/local/texlive`,
with installed years searched newest first. Optional tool overrides are
`R582_PDFFONTS`, `R582_PDFINFO` and `R582_KPSEWHICH`. Arial, Helvetica,
DejaVu, Liberation, Calibri, Times New Roman, matplotlib fallback and Type 3
PDF fonts are forbidden.

Example explicit configuration:

```powershell
$env:R582_TERMES_FONT_DIR = 'C:\texlive\2024\texmf-dist\fonts\opentype\public\tex-gyre'
$env:R582_PDFFONTS = 'C:\texlive\2024\bin\windows\pdffonts.exe'
$env:R582_PDFINFO = 'C:\texlive\2024\bin\windows\pdfinfo.exe'
```

## Seventeen active figure-renderer entries

Run each command from the public package root. Each renderer writes its active
PDF, SVG, PNG and TIFF to `manuscript/figures_R582`. The S7--S9 entry produces
three figures, giving 19 active figures from 17 renderer entries.

| Entry | Active figure(s) | Package-relative command |
|---:|---|---|
| 1 | Main Fig. 1 | `python .\manuscript\source_data\R582_Fig1_experimental_problem\R582_Fig1_experimental_problem.py` |
| 2 | Main Fig. 2 | `python .\manuscript\source_data\R582_Fig2_domain_state\R582_domain_state_v2.py` |
| 3 | Main Fig. 3 | `python .\manuscript\source_data\R582_Fig3_spatial_progression\make_fig_r582_spatial_progression_v3.py` |
| 4 | Main Fig. 4 | `python .\manuscript\source_data\R582_Fig4_closure_identifiability\R582_plot_closure_identifiability.py` |
| 5 | Main Fig. 5 | `python .\manuscript\source_data\R582_Fig5_multiscale_bounds\make_fig_r582_multiscale_bounds_v2.py` |
| 6 | Main Fig. 6 | `python .\manuscript\source_data\R582_Fig6_operating_levers_v2\make_fig_r582_operating_levers_v2.py` |
| 7 | SI Fig. S1 | `python .\manuscript\source_data\R582_SI_FigS1_derivative\make_sifig_r582_s1_derivative.py` |
| 8 | SI Fig. S2 | `python .\manuscript\source_data\R582_SI_FigS2_composition\make_sifig_r582_s2_composition.py` |
| 9 | SI Fig. S3 | `python .\manuscript\source_data\R582_SI_FigS3_compression\make_sifig_r582_s3_compression.py` |
| 10 | SI Fig. S4 | `python .\manuscript\source_data\R582_SI_FigS4_state_function_fields\make_fig_si_r582_s4_state_function_fields.py` |
| 11 | SI Fig. S5 | `python .\manuscript\source_data\R582_SI_FigS5_hydraulic_fields\make_fig_si_r582_s5_hydraulic_fields.py` |
| 12 | SI Fig. S6 | `python .\manuscript\source_data\R582_SI_FigS6_voltage_degeneracy\make_sifig_r582_s6_voltage_degeneracy.py` |
| 13 | SI Figs. S7--S9 | `python .\manuscript\source_data\R582_SI_molecular_bounds\make_r582_si_molecular_figures.py` |
| 14 | SI Fig. S10 | `python .\manuscript\source_data\R582_SI_FigS10_comparator_definitions\make_sifig_r582_s10_comparator_definitions.py` |
| 15 | SI Fig. S11 | `python .\manuscript\source_data\R582_SI_FigS11_accessibility_families\make_sifig_r582_s11_accessibility_families.py` |
| 16 | SI Fig. S12 | `python .\manuscript\source_data\R582_SI_FigS12_flow_postprocess\make_sifig_r582_s12_flow_postprocess.py` |
| 17 | SI Fig. S13 | `python .\manuscript\source_data\R582_SI_FigS13_smooth_permeability\make_sifig_r582_s13_smooth_permeability.py` |

Run the release-level font gate after rendering:

```powershell
python .\audit\check_font_consistency.py
```

## LaTeX build commands

From the public package root, compile the active R582 sources twice in the
cross-document order needed by `xr-hyper`:

```powershell
Push-Location .\manuscript
latexmk -norc -pdf -interaction=nonstopmode -halt-on-error -synctex=1 SI_R582.tex
latexmk -norc -pdf -interaction=nonstopmode -halt-on-error -synctex=1 main_R582.tex
latexmk -norc -pdf -interaction=nonstopmode -halt-on-error -synctex=1 SI_R582.tex
latexmk -norc -pdf -interaction=nonstopmode -halt-on-error -synctex=1 main_R582.tex
Pop-Location
```

The main paper and SI link external labels without importing the other
document's bibliography entries.

## Full-workspace-only numerical command

The following parser is not a public-package command. It applies only to the
author's full workspace, which contains the large COMSOL result tree:

```powershell
$env:ZIFB_PROJECT_ROOT = 'E:\zifb_final_9129_luck'
python "$env:ZIFB_PROJECT_ROOT\battery_comsol\02_outputs_core\R581_CANONICAL_CLOSURE_REBUILD\scripts\R581_parse_convergence.py"
```

COMSOL control and physical cases are run serially from byte-verified copies.
No original `.mph` file is opened for writing. The public release contains the
registered derived records needed by the manuscript figures, not the private
full-workspace model tree.
