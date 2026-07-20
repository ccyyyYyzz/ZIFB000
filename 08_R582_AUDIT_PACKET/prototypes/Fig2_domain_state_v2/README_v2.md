# R582 Figure 2 v2

The v2 composition replaces the rounded-card flowchart with an editorial, unboxed state rail and a thin capacity rail. It preserves all v1 variables, registered geometry, and displayed marker values while leaving the v1 files unchanged.

Build:

```powershell
python manuscript/source_data/R582_Fig2_domain_state/R582_domain_state_v2.py
```

Primary outputs are `manuscript/figures_R582/Fig_R582_domain_state_v2.{svg,pdf,png,tiff}`. The script also writes a 180-mm preview, grayscale QA preview, source table, font audit, and deterministic build manifest.
