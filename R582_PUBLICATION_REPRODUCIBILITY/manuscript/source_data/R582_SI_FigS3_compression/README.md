# R582 SI Figure S3 source bundle

This bundle rebuilds the physical-cell thickness brackets from frozen processed
tables. It never modifies raw experimental files and keeps the 2.0 mm
cross-batch proxy visually and analytically separate.

Rebuild from the project root:

```powershell
& 'D:\Anacondar\anaconda3\python.exe' `
  'manuscript/source_data/R582_SI_FigS3_compression/make_sifig_r582_s3_compression.py'
```

The renderer verifies both frozen SHA-256 values, cross-checks the primary 85%
rows against the sensitivity table and exports editable/vector, print and
preview formats. Output and font hashes are stored in the render manifest.

