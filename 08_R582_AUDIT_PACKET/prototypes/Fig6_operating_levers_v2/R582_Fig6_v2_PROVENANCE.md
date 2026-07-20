# Figure 6 v2 evidence and provenance

## Scientific scope

Figure 6 v2 uses the same registered quantitative evidence as v1 but changes the
visual argument to an `a/b` solved-response row plus one full-width quantitative
summary. The former explanatory lever/node/consequence table is absent.
Accessibility and smooth-permeability results are not placed on the common
`Q_s` axis because they either address a later event or use endpoint voltage as
the registered response. This prevents unlike output coordinates from being
presented as a single ranking.

The figure concerns the modeled ZIFB positive electrode. NH4Br remains a
representative supporting electrolyte, and no experimental file labelled
NH4Cl/NH4Br is used. No new experimental result, original COMSOL model, electric
potential field, morphology or blockage interpretation enters the figure.

## Current-density evidence and censoring

| `J` (mA cm^-2) | result | status |
|---:|---:|---|
| 20 | `Q_s = 106.31983154928193 mAh cm^-2` | observed crossing; full-capacity continuum simulation |
| 40 | `Q_s = 83.0201994718443 mAh cm^-2` | observed crossing; registered reference simulation |
| 80 | `Q_s > 40 mAh cm^-2` | right-censored at the simulated endpoint; `S_avg,peak = 0.923523703675` |
| 120 | `Q_s = 8.391444702684929 mAh cm^-2` | observed crossing in the separate fixed-capacity simulation |

Right-censoring means only that the crossing occurs, if at all, beyond the
available `Q = 40 mAh cm^-2` trajectory. Panel a therefore uses an open triangle
at the censoring capacity, an upward arrow and the explicit text `Q_s > 40`; it
does not plot an exact 80 mA cm^-2 crossing. Only the 20–40 mA cm^-2 interval is
connected and only that interval enters the panel-c current comparison.

## Diffusivity evidence

| `D_eff/D_0` | 0.5 | 0.6 | 0.8 | 1.0 | 1.2 | 1.5 | 2.0 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| `Q_s` (mAh cm^-2) | 45.03434 | 57.36042 | 73.13147 | 83.02020 | 89.97184 | 97.49001 | 106.20486 |

All seven points are converged continuum simulations. The line connects adjacent
conditions without fitting or extrapolation. The MD-informed range is
`0.8–1.4 D_0`; its upper mapped value,
`Q_s = 94.98395635541873 mAh cm^-2`, is linearly interpolated strictly within the
simulated `1.2–1.5 D_0` interval.

## Panel-c ranges

- `D_eff/D_0 = 0.5–2.0`, continuum simulations:
  `Delta Q_s/Q_s,0 = -45.75496%` to `+27.92653%`.
- `J = 20–40 mA cm^-2`, continuum simulations:
  `+28.06502%` to `0%` as current increases.
- MD-informed `D_eff/D_0 = 0.8–1.4`:
  `-11.91123%` to `+14.41066%` after mapping through the simulated response.
- Analytical flow-dependent boundary layer, 25–100 mL min^-1 and `m = 0.5`:
  `-9.67075%` to `+6.88110%`. This is an analytical scenario applied to the
  solved baseline, not a continuum re-simulation or experiment.
- Linked felt geometry, 1.5–3.0 mm:
  `-0.76463%` to `+1.53770%`. Thickness and porosity change together.
- Full simulated flow rate, 25–100 mL min^-1:
  `-0.23636%` to `+0.10496%`.

All percentages use `Q_s,0 = 83.0201994718443 mAh cm^-2`. The shared coordinate
compares response magnitude over declared ranges; marker and line styles retain
the difference between continuum simulations, the analytical scenario and the
MD-informed mapped range.

## Threshold method

An observed crossing is calculated only when adjacent samples bracket
`S_avg = 1`:

`Q_s = Q_0 + (1 - S_0)(Q_1 - Q_0)/(S_1 - S_0)`.

If no bracket exists, the result is reported as censored. No curve fit, capacity
extrapolation or interpolation through the censored current condition is used.

## Registered source hashes

- Consolidated continuum trajectories:
  `744A36AC0EB8E785E61FEAB24F2CA699484134D30F8D77E532E03DB90917E90F`.
- Cleaned full-capacity current trajectories:
  `597D4A33CA96DDBDF89C29137EEBAB3673D9F3AB727D127EA60F70A4758F85AC`.
- Fixed-capacity current trajectories:
  `2F191549168DB185E5E321439344AD134595178E4C673AEB0C4ACE29DA8AF506`.
- Additional diffusivity-grid trajectories:
  `71C462DB57C7539C87140ED4322510989B625EF0BC34A00F401D5FD4DCF50430`.
- Analytical-flow baseline input:
  `3490EBDB2C5244AF9044D3422BC29FED96B57AF54F9C48AAC46BD3B1717C0335`.

The v2 build reads the v1 compact evidence tables without modifying them. The
exact dependency and output hashes are recorded in
`R582_Fig6_v2_BUILD.json`; the final bundle inventory is in
`R582_Fig6_v2_MANIFEST.csv`.
