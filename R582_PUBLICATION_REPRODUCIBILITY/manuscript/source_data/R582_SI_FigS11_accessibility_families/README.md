# R582 Supplementary Figure S11 source bundle

This bundle displays four registered single-fibre **geometric** remaining-area families and isolates the exact fixed-inventory comparison. It does not fit, interpolate or smooth a new physical relation.

The semantic separation is mandatory:

- coloured family curves are geometric `A/A0` nodes from the registered single-fibre calculation;
- the dashed trace is only `R_theta = 1 - theta`, generated from `1 - comsol_theta_ref`, and is a comparator rather than a geometric family;
- native COMSOL bare-area accessibility is `A_bare/A0 = R_theta * T_pore` and is not available from S11 because `T_pore` is absent.

## Rebuild

From this directory:

```powershell
& "D:\Anacondar\anaconda3\python.exe" .\make_sifig_r582_s11_accessibility_families.py
```

The renderer verifies the SHA-256 identity and byte equality of both frozen CSV inputs and their registered upstream sources. It validates the geometric remaining-area identity, cross-matches every closure node to the clock table, freezes four plotted tables and requires a byte-identical second render. The semantic correction does not alter any numeric node.

## Outputs

The publication masters are written to `manuscript/figures_R582/` with stem `SIFig_R582_S11_accessibility_families`:

- editable `.svg` and `.pdf`;
- 600-dpi `.png` and opaque RGB 600-dpi `.tiff`;
- 180-mm colour and grayscale QA previews.

`R582_SIFig_S11_render_manifest.json` records input, source-table and output hashes, exact font faces, dimensions, source-node counts, the three quantity definitions and automated gates. `pdffonts_report.txt` preserves the independent PDF font listing.

## Interpretation boundary

The four geometric lines are deterministic single-fibre comparator cases under prescribed retention and placement parameters. Their segments connect registered nodes only. The dashed `R_theta` trace is a separate comparator. Neither the coloured curves nor the dashed trace is measured coverage, a reconstruction of the experimental felt or a plotted native COMSOL `A_bare/A0` closure.
