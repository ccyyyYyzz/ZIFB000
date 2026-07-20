# R582 SI Figure S1 source bundle

This bundle deterministically rebuilds the derivative-window sensitivity
figure without modifying any experimental source file. Plotting tables remove
raw filenames and identify the independent unit as one physical cell.

Rebuild from the project root:

```powershell
& 'D:\Anacondar\anaconda3\python.exe' `
  'manuscript/source_data/R582_SI_FigS1_derivative/make_sifig_r582_s1_derivative.py'
```

The renderer verifies all frozen SHA-256 values before reading data. The PDF
and SVG are the editable masters; the TIFF is opaque RGB at 600 dpi. The
manifest records input, plot-table, font-face and output hashes.

