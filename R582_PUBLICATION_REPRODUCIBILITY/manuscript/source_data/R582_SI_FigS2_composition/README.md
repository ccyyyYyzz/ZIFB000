# R582 SI Figure S2 source bundle

This bundle rebuilds the composition-associated cell envelope from the frozen
cell-level table. It does not read or modify raw experimental files and does not
fit a concentration-response relation.

Rebuild from the project root:

```powershell
& 'D:\Anacondar\anaconda3\python.exe' `
  'manuscript/source_data/R582_SI_FigS2_composition/make_sifig_r582_s2_composition.py'
```

The renderer verifies both registered inputs, writes the exact plotted cell
table and exports editable/vector, print and preview formats. Output and font
hashes are stored in the render manifest.

