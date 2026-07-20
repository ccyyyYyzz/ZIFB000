# R582 Supplementary Figure S12 source bundle

Run from this directory:

```powershell
D:\Anacondar\anaconda3\python.exe make_sifig_r582_s12_flow_postprocess.py
```

The script verifies the frozen baseline and R577 sweep by SHA-256, reconstructs
all 120 registered analytical evaluations, writes plot and summary tables, and
exports the figure to `manuscript/figures_R582`. It then performs a
byte-identical second render and audits PDF/SVG fonts, exact page size, raster
dimensions and grayscale output.

The `inputs/` files are byte-identical registered copies. No COMSOL `.mph`, raw
experiment or historical figure master is opened or modified.

