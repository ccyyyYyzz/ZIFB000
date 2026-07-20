# R582 Supplementary Figure S10 source bundle

This bundle replaces the legacy glossy 3D fibre/network rendering with a flat, auditable definition figure. It reads registered comparator objects only and leaves every upstream file unchanged.

## Rebuild

From this directory:

```powershell
& "D:\Anacondar\anaconda3\python.exe" .\make_sifig_r582_s10_comparator_definitions.py
```

The renderer first verifies the SHA-256 identity and byte equality of every frozen input and its registered upstream source. It then freezes the displayed scalar definitions, 225 central-slice nodes, 420 central-slice throats and model rules as CSV files. A second complete render must match the first byte-for-byte in all six output formats.

## Outputs

The publication masters are written to `manuscript/figures_R582/` with stem `SIFig_R582_S10_comparator_definitions`:

- editable `.svg` and `.pdf`;
- 600-dpi `.png` and opaque RGB 600-dpi `.tiff`;
- 180-mm colour and grayscale QA previews.

`R582_SIFig_S10_render_manifest.json` records input, source-table and output hashes, exact font faces, dimensions and all automated gates. `pdffonts_report.txt` preserves the independent PDF font listing.

## Deliberate exclusions

The fibre NPZ fields `height`, `covered`, `a_um`, `theta_geo` and `label` are not rendered. The network NPZ fields `phi`, `r_new` and `flux` are not rendered. The artwork therefore contains no deposit morphology, coverage image, solved field, pore-blocking front, pseudo-microscopy texture, shadow, gloss or 3D perspective.
