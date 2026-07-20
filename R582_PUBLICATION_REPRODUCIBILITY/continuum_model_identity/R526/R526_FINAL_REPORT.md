# R526 COMSOL native knob export final report

Generated: 2026-06-27T20:58:28

## What this run did

R526 reran the R525 knob gallery requirement with direct COMSOL native PlotGroup2D/Image exports. Each case fresh-loaded the R523/R520 native blockage-feedback baseline, reset baseline parameters, applied one knob, set the corrected transient time list, solved where needed, saved the solved `.mph`, and exported endpoint field images directly from COMSOL.

This corrected the earlier R526 pre-fix issue where `tlist` had not been overwritten for high-rate cases. In this run, every case log reports `TLIST_SET,...,OK`.

## Solved model archive policy

Per user instruction, successful solved `.mph` files were not deleted. They were moved from COMSOL local staging to:

`E:\cyz000\solved_mph_archive\R526_COMSOL_NATIVE_KNOB_EXPORT_TLIST_FIXED`

Successful archived `.mph`: **22**

Total archived size: **16.70 GB**

A stale pre-tlist-fix backup archive is retained separately at:

`E:\cyz000\solved_mph_archive\R526_COMSOL_NATIVE_KNOB_EXPORT`

The current official corrected archive is the `_TLIST_FIXED` folder above.

## Native export outputs

- Native COMSOL PNG panels copied into: `C:\Users\CYZ的computer\Documents\Codex\2026-06-02\i2-comsol-mph-python-models-single\outputs\R526_COMSOL_NATIVE_KNOB_EXPORT\comsol_native_user_export`
- Gallery: `C:\Users\CYZ的computer\Documents\Codex\2026-06-02\i2-comsol-mph-python-models-single\outputs\R526_COMSOL_NATIVE_KNOB_EXPORT\R526_FIGURE_GALLERY.html`
- Native image manifest: `C:\Users\CYZ的computer\Documents\Codex\2026-06-02\i2-comsol-mph-python-models-single\outputs\R526_COMSOL_NATIVE_KNOB_EXPORT\comsol_native_user_export\R526_COMSOL_NATIVE_KNOB_IMAGE_MANIFEST.csv`
- Solve status: `C:\Users\CYZ的computer\Documents\Codex\2026-06-02\i2-comsol-mph-python-models-single\outputs\R526_COMSOL_NATIVE_KNOB_EXPORT\comsol_native_user_export\R526_NATIVE_SOLVE_STATUS.csv`
- Actual E-drive `.mph` manifest: `C:\Users\CYZ的computer\Documents\Codex\2026-06-02\i2-comsol-mph-python-models-single\outputs\R526_COMSOL_NATIVE_KNOB_EXPORT\R526_SOLVED_MPH_E_ARCHIVE_MANIFEST.csv`
- QA table: `C:\Users\CYZ的computer\Documents\Codex\2026-06-02\i2-comsol-mph-python-models-single\outputs\R526_COMSOL_NATIVE_KNOB_EXPORT\R526_NATIVE_EXPORT_QA.csv`

## Run status

PASS cases: **22**

Failed cases: **1**

### Failed cases

- `Av_double_Q120` (wet_area_Av, Av 2x): solve_failed. No solved `.mph` was produced, so there was nothing to archive.

## Case summary

| case | family | knob | status | native PNG | E archive `.mph` |
|---|---|---|---|---:|---|
| `baseline_J40_Q120` | baseline | J40 Q120 | PASS | 7 | YES |
| `rate_J20_Q40` | current_density_fixed_Q | J20 Q40 | PASS | 7 | YES |
| `rate_J40_Q40` | current_density_fixed_Q | J40 Q40 | PASS | 7 | YES |
| `rate_J80_Q40` | current_density_fixed_Q | J80 Q40 | PASS | 7 | YES |
| `rate_J120_Q40` | current_density_fixed_Q | J120 Q40 | PASS | 7 | YES |
| `comp_L15_Q120` | compression_true_branch | L=1.5mm eps=0.800 | PASS | 7 | YES |
| `comp_L25_Q120` | compression_true_branch | L=2.5mm eps=0.880 | PASS | 7 | YES |
| `comp_L30_Q120` | compression_true_branch | L=3.0mm eps=0.900 | PASS | 7 | YES |
| `br_2M_Q120` | Br_support_isolated | cBr=2M | PASS | 7 | YES |
| `br_3M_Q120` | Br_support_isolated | cBr=3M | PASS | 7 | YES |
| `br_5M_Q120` | Br_support_isolated | cBr=5M | PASS | 7 | YES |
| `activity_gamma2_Q120` | activity_saltout | gamma=2 | PASS | 7 | YES |
| `activity_gamma4_Q120` | activity_saltout | gamma=4 | PASS | 7 | YES |
| `flow_25_Q120` | flow_rate | Q_flow=25 ml/min | PASS | 7 | YES |
| `flow_100_Q120` | flow_rate | Q_flow=100 ml/min | PASS | 7 | YES |
| `sigmal_10_Q120` | liquid_conductivity | sigmal=10 S/m | PASS | 7 | YES |
| `sigmal_40_Q120` | liquid_conductivity | sigmal=40 S/m | PASS | 7 | YES |
| `D_half_Q120` | diffusion_prior | D species 0.5x | PASS | 7 | YES |
| `D_double_Q120` | diffusion_prior | D species 2x | PASS | 7 | YES |
| `Av_half_Q120` | wet_area_Av | Av 0.5x | PASS | 7 | YES |
| `Av_double_Q120` | wet_area_Av | Av 2x | FAIL | 0 | NO |
| `sigmas_80_Q120` | solid_conductivity | sigmas=80 S/m | PASS | 7 | YES |
| `sigmas_320_Q120` | solid_conductivity | sigmas=320 S/m | PASS | 7 | YES |

## Exported COMSOL fields

Each successful case has 7 direct COMSOL exports: `S_surf`, `eps_s_pos`, `theta_eff`, `A_bare_frac`, `K_perm_rel`, `u_native_mag`, and `p_native`. These are endpoint fields at each case's locked target capacity/time.

## Caveat

`Av_double_Q120` failed during COMSOL solve. I did not fabricate images, reuse another case, or create a fake `.mph` archive for it. The failure is preserved in the solve-status CSV and QA table.
