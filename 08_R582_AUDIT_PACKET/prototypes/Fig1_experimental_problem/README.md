# R582 Figure 1 source bundle

This isolated bundle rebuilds the proposed main Figure 1 from immutable registered
experimental/model-marker tables. It does not edit `main.tex`, `SI.tex`, raw experimental
files, or any pre-existing output.

The visual argument is deliberately limited: existing full-cell records show a voltage-rise
feature and rate-dependent utilization that motivate a positive-electrode state model. They do
not independently validate the model markers or identify a deposit morphology. The ZIFB
positive electrode is the focus; supporting-electrolyte composition is not used as a main-panel
comparison.

Run from the project root with the project Python environment:

```powershell
python manuscript/source_data/R582_Fig1_experimental_problem/R582_Fig1_experimental_problem.py
```

The script verifies five frozen input hashes before reading data. It then regenerates the clean
panel tables, input manifest, build record, editable SVG, PDF, 600-dpi PNG/TIFF, and a Python-made
grayscale QA preview. Two consecutive builds are byte-identical.

Typography follows the manuscript body: all four TeX Gyre Termes faces are registered explicitly,
and matplotlib mathtext uses the same family without fallback. Detailed source, font, statistics,
format, and grayscale checks are recorded in `R582_Fig1_QA.md` and
`R582_Fig1_build.json`.

`EXP-META-001` remains in force: legacy experimental labels containing `NH4Cl` or `NH4CL`
refer to NH4Br. Raw names and bytes are unchanged, and the correction is not turned into a
composition comparison in this figure.

