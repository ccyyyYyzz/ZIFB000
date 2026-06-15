# single_fiber_i2 Closure Bridge for the 2D COMSOL Model

This bridge turns the standalone single-fiber iodine model into simple,
interpretable closure relations for the macroscopic porous-media model. It does
not call COMSOL and does not modify any `.mph` file.

## Workflow

From the repository root:

```bash
python models/single_fiber_i2/fit_closures.py
python models/single_fiber_i2/export_comsol_closures.py
```

The scripts write:

- `outputs/single_fiber_i2/closure_database.csv`
- `outputs/single_fiber_i2/closure_fits.json`
- `outputs/single_fiber_i2/comsol_closure_expressions.md`

The scan ranges live under `scan:` in `params.yaml`. They cover initial
coverage, initial film thickness, bulk `I2_tot`, bulk `I-`, supporting bromide,
current magnitude, and charge/discharge mode.

## Why Not Use parent FilmResistance Directly

The parent COMSOL `FilmResistance` style is usually a lumped serial resistance.
That is too coarse for this case because the iodine solid does not cover the
fiber uniformly from the start. A single serial resistance makes the whole
surface look covered, so it suppresses the bare pathway even when most of the
fiber is still exposed.

The single-fiber model keeps `h_I2` and `theta` separate:

```text
Rfilm_local = h_I2/sigma_I2
film_kin_factor = 1/(1 + g_eff*Rfilm_local)
```

The film resistance should act only on the covered pathway. The uncovered
surface should still react through the bare pathway.

## Why Patchy Coverage Needs Parallel Pathways

Patchy iodine coverage is an area-partitioning problem, not only a resistance
problem. The recommended current decomposition is:

```text
j_bare = (1-theta_i2)*j0_bare_i2*BV_i2(eta_I)
j_cov = theta_i2*j0_cov_i2*film_kin_factor_i2*BV_i2(eta_I)
j_total = j_bare + j_cov
```

This lets the macro model represent three effects independently:

- decreasing bare area as `theta_i2` grows
- lower covered-path kinetics through `j0_cov_i2`
- additional local film resistance through `film_kin_factor_i2`

If the current macro implementation only has one BV pathway, use the exported
`Av_try2_eff` expression as a compatibility bridge:

```text
Av_try2_eff = av0_i2*((1-theta_i2) + theta_i2*(j0_cov_i2/j0_bare_i2)*film_kin_factor_i2)
```

The explicit two-pathway form is preferred when it is practical to add it.

## Exported Parameters

The bridge can export or recommend:

- `theta_i2 = 1 - exp(-a_theta_i2*h_I2^b_theta_i2)`
- `Rfilm_local = h_I2/sigma_I2`
- `film_kin_factor_i2 = 1/(1 + g_eff_i2*Rfilm_local)`
- `k_precip_i2` for `r_precip_i2 = k_precip_i2*cI2_supersat`
- `k_diss_surf` for `r_diss_i2 = k_diss_surf*theta_i2*cI2_undersat`
- `frac_bare_current` and `frac_cov_current` for diagnostics
- `Av_try2_eff` as a reduced scalar active-area multiplier

The geometric relation

```text
theta_geo = 1 - exp(-k_geo*N_i2^(1/3)*eps_s_equiv^(2/3))
```

is kept as a diagnostic unless the macro model has a calibrated positive-solid
state such as `N_i2` or `eps_s_pos`.

## Schema

`closure_schema.json` defines the microscale-to-macroscale fields expected by a
future exporter or COMSOL parameter ingestion step:

- `av0_i2`
- `k_geo`
- `k_precip_i2`
- `k_diss_surf`
- `sigma_I2`
- `theta_model`
- `film_model`
- `notes`
