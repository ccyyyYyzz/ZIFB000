# R582 Supplementary Figure S13 source bundle

Run from this directory:

```powershell
D:\Anacondar\anaconda3\python.exe make_sifig_r582_s13_smooth_permeability.py
```

The script verifies both frozen inputs by SHA-256, reparses the immutable R537
text export, cross-checks the registered table, writes clean plot and summary
tables, and exports the figure to `manuscript/figures_R582`. It then performs a
byte-identical second render and audits PDF/SVG fonts, exact page size, raster
dimensions and grayscale output.

No original COMSOL `.mph`, raw experiment or historical figure master is
opened or modified.

