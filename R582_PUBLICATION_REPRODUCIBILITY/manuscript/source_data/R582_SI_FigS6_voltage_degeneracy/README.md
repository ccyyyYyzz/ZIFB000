# R582 Supplementary Figure S6 source bundle

Run from this directory:

```powershell
D:\Anacondar\anaconda3\python.exe make_sifig_r582_s6_voltage_degeneracy.py
```

The script verifies all frozen inputs by SHA-256, reconstructs the registered
reduced voltage fit, cross-checks every registered degeneracy point, writes clean
plot/parameter CSV files using `R_theta_end`, and exports the figure to
`manuscript/figures_R582`.
It then performs a byte-identical second render and audits PDF/SVG fonts, exact
page size, raster dimensions and grayscale output.

The `inputs/` files are byte-identical copies of registered evidence, so their
historical `A_bare_*` headers remain unchanged. In this R582 bundle those columns
are interpreted only as the reduced, calibration-controlled factor
$R_{\theta}=1-\theta$, not as native remaining area. The latter is
$A_{\mathrm{bare}}/A_0=R_{\theta}T_{\mathrm{pore}}$. Historical source files,
raw experiments and COMSOL models are never modified.
