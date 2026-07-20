# R582 Figure 3 v3 source bundle

Run `python make_fig_r582_spatial_progression_v3.py` from any working directory. The script verifies the sole spatial input before writing outputs.

## Input and plotted quantities

The only field input is `../Fig_R545_fields/Fig3_baseline_spatial_long.csv`, required SHA-256 `E322D0D0C4B0D5C8CB84BD5CB18D1A43CBA183EB8A5F112577686993BC8FC007`.

| Source field | Display | Treatment |
|---|---|---|
| `eps_s_pos` | retained solid fraction | multiplied by 100 only for the percent color scale |
| `A_bare_frac` | native remaining bare-area fraction | plotted directly, with no substitution |
| `j_total_A_m2` | total reaction-current density | positive values on one log scale; negative values retained as a neutral mask |

The generated `Fig_R582_spatial_progression_v3_source.csv` contains all 17,985 selected rows, the native `A_bare_frac`, the separately computed `one_minus_theta_eff`, and `A_bare_native_minus_one_minus_theta`. The discrepancy column is audit-only and is not plotted.

The lower profile is an arithmetic group mean of `A_bare_frac` at each `x_m` over the 109 uniformly sampled `y_m` values. It is a summary of the same exported field, not an additional simulation or fit.

## Generated records

- `render_manifest_v3.json`: input hash, row/grid checks, current-sign inventory, dimensions and output hashes.
- `FIGURE_CONTRACT_v3.md`: claim, scale and interpretation limits.
- `CAPTION_DRAFT_v3.md`: manuscript-ready legend.
- `QA_NOTES_v3.md`: semantic, typographic, visual and reproducibility checks.
- `ROOT_ACCEPTANCE_v3.md`: root-agent promotion decision.

Visual assets are written to `../../figures_R582/` with stem `Fig_R582_spatial_progression_v3`. Earlier versions are preserved only as provenance and must not be used in the R582 manuscript.

