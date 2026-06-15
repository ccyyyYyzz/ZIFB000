# Single-Fiber I2 Coverage / Precipitation / Film-Resistance Model

This folder contains a standalone Python model for iodine transport and surface
state evolution around one carbon fiber. It does not call COMSOL and does not
modify any `.mph` file. The intended use is to generate closure relations for a
2D porous-media macroscopic COMSOL model.

## Physical Scope

Geometry is a 1D radial cylindrical diffusion layer around a fiber:

- carbon fiber radius `R_f` [m]
- external diffusion-layer radius `R_out` [m]
- finite-volume radial cells in `r`

Transported solution species:

- `cI_m` [mol/m3]
- `cI2_tot` [mol/m3]
- optional constant `cBr_support` [mol/m3]

Fast complexation is represented by

```text
beta_I2 = 1 + K_I2_I*cI_m + K_I2_Br*cBr_support
cI2_free = cI2_tot / beta_I2
```

The electrochemical reaction is

```text
I2 + 2e- <=> 2I-
```

Positive applied fiber current density `i_app_fiber` [A/m2] is defined as charge
oxidation:

```text
2I- -> I2 + 2e-
```

At each RHS evaluation, the model solves for `eta_I` [V] such that
`j_total(eta_I, theta, h_I2) = i_app_fiber`.

## Surface Kinetics

The total current is the parallel sum of bare and covered pathways:

```text
j_bare = (1 - theta) * j0_bare * BV(eta_I)
j_cov  = theta * j_cov_local
j_total = j_bare + j_cov
```

The local film resistance is

```text
Rfilm_local = h_I2 / sigma_I2
```

Two covered-path modes are available in `params.yaml`:

```text
linearized:
  j_cov_local = j0_cov*BV(eta_I) / (1 + g_I*Rfilm_local)

implicit:
  solve j_cov_local = j0_cov*BV(eta_I - j_cov_local*Rfilm_local)
```

I2 precipitation and dissolution use smooth supersaturation and
undersaturation:

```text
cI2_supersat = smoothplus(cI2_surf_free - cI2_sat)
cI2_undersat = smoothplus(cI2_sat - cI2_surf_free)

r_precip = k_precip_sf * cI2_supersat
r_diss = k_diss_sf * theta * cI2_undersat

dh_I2/dt = Vm_I2 * (r_precip - r_diss)
```

Coverage uses a simple replaceable law:

```text
dtheta/dt =
  k_theta_grow*cI2_supersat*(1 - theta)
  - k_theta_diss*cI2_undersat*theta
```

`theta` is clipped to `[0, 1]` in diagnostics and guarded at the ODE bounds.
`h_I2` is kept nonnegative.

A diagnostic geometric coverage function is also provided:

```text
theta_geo = 1 - exp(-k_geo*N_i2^(1/3)*eps_s_equiv^(2/3))
```

It is reported but not enforced.

## Molecular Prior Diagnostic

CP2K neutral-I2 adsorption results can be loaded as a bounded molecular prior on
relative iodine-philic site activity. This is configured under
`molecular_prior` in `params.yaml`.

The default is disabled:

```text
molecular_prior.enabled = false
```

When enabled for sensitivity analysis, the model computes

```text
site_activity_multiplier =
1 + sum_i f_i*(S_i - 1)
```

where `S_i` is a bounded site preference factor and `f_i` is an assumed relative
site fraction. The CP2K values do not directly set `k_precip_i2`,
`k_diss_surf`, `theta`, or `film_kin_factor`. The current single-fiber model has
no explicit nucleation-site-density state, so the multiplier is reported as a
diagnostic output and does not alter the default ODEs.

Use this only for sensitivity analysis or shadow-variable comparison. The
molecular calculations use finite clusters with no explicit water, NH4Br,
charged iodine species, or calibrated site densities.

## Surface Flux Boundary

At `r = R_out`, Dirichlet bulk concentrations are used:

```text
cI_m = cI_bulk
cI2_tot = cI2_tot_bulk
```

At `r = R_f`, surface fluxes are

```text
N_I2_echem = j_total / (2F)
N_I_echem  = -j_total / F
N_I2_solid = -r_precip + r_diss

N_I2_surface = N_I2_echem + N_I2_solid
N_I_surface  = N_I_echem
```

Flux is positive from the fiber surface into the liquid diffusion layer.

## Outputs

The demo writes:

- `outputs/single_fiber_i2/demo_charge_discharge.csv`
- `outputs/single_fiber_i2/demo_voltage_like.png`
- `outputs/single_fiber_i2/demo_theta_h_Rfilm.png`

CSV columns include:

- `time_s`
- `eta_I`
- `j_total`
- `j_bare`
- `j_cov`
- `theta`
- `h_I2`
- `Rfilm_local`
- `cI2_surf_free`
- `cI2_bulk_free`
- `supersaturation`
- `dissolution_rate`
- `precipitation_rate`
- `film_kin_factor`
- `k_precip_eff`
- `k_diss_eff`
- `theta_geo`
- `site_activity_multiplier`
- `molecular_prior_enabled`
- `molecular_prior_mapping`

## Closure Quantities for Macroscale COMSOL

This single-fiber model is meant to provide local closures such as:

- `theta(eps_s, cI2_surf, j)`
- `Rfilm_local(theta, h)`
- `film_kin_factor`
- `k_precip_eff`
- `k_diss_eff`
- bare/covered current split: `j_bare`, `j_cov`

These can be tabulated from parameter sweeps or embedded later as reduced-order
relations in the macroscopic porous-media model.

## Run

From the repository root:

```bash
python models/single_fiber_i2/run_demo.py
pytest models/single_fiber_i2/tests
```
