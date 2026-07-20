# SOC MD Transport Prior Package

This package builds and analyzes local GROMACS SOC-series simulations for a
bounded ZIFB iodine-posolyte transport prior. It is a sensitivity-prior package,
not validation, and it must not be used to replace production COMSOL constants by
itself.

## Scope

- System: 1 M ZnI2 + 4 M NH4Br + water with explicit oxidized iodine carriers.
- SOC points: approximately 0.1, 0.3, 0.5, 0.7, and 1.0.
- Charge variants: `q1p0` and `q0p8_ecc`.
- Main output: `D_eff(SOC)=D_eff0*exp(-a*SOC)` from iodine-carrier diffusion
  ratios, with ECC sensitivity.
- Secondary output: Green-Kubo viscosity ratios and density sanity checks.
- Applicability warning: carrier-contact clustering is reported as a
  single-phase MD warning, not a phase-equilibrium classifier. The diagnostic
  uses carrier centers from `prod_nojump.xtc` with minimum-image distances to
  reduce PBC artifacts for polyhalide COMs.
- Viscosity cross-check setup: `prod_long.mdp` is NVT (`pcoupl = no`) with
  `nstenergy = 50`, giving pressure-tensor samples every 0.1 ps at `dt = 0.002 ps`.
  GROMACS NVT energy files do not always carry a `Volume` term, so the analysis
  falls back to the final `prod.gro`/`npt.gro` box volume for the Green-Kubo
  prefactor when needed.
- Optional viscosity replica fallback: `viscosity_replicate_plan.csv` enumerates
  3 independent NVT Green-Kubo replicas for each configured priority SOC and
  charge-scale variant. These replicas are only a noise check if single-trajectory
  pressure autocorrelation is too unstable; they are not the primary closure.

## Claim Boundary

- Polyhalide I3-/I2Br- absolute values are force-field limited.
- Use ratios, trends, block errors, density, ECC sensitivity, and literature
  anchors as bounded priors.
- Do not launch COMSOL, edit `.mph` files, or replace `D_eff`, `k_precip`, or
  `N_target` from this package alone.

## Environment

Run through the WSL micromamba environment:

```bash
/home/cyzcomputer/.local/bin/micromamba run -n zifb_md python outputs/md_transport_soc_series/scripts/record_tool_versions.py
```

Version evidence is written to:

- `outputs/md_transport_soc_series/tool_versions.txt`
- `outputs/md_transport_soc_series/results/tool_versions.json`

## Rebuild Inputs

```bash
/home/cyzcomputer/.local/bin/micromamba run -n zifb_md python outputs/md_transport_soc_series/scripts/build_soc_system.py \
  --config outputs/md_transport_soc_series/inputs/soc_series_config.yaml \
  --all \
  --out-root outputs/md_transport_soc_series/inputs/soc_series
```

## Run And Monitor

Long production runs are launched with:

```bash
powershell -NoProfile -ExecutionPolicy Bypass -File outputs/md_transport_soc_series/scripts/start_soc_long_batch_windows.ps1
```

Monitor current progress and health:

```bash
/home/cyzcomputer/.local/bin/micromamba run -n zifb_md python outputs/md_transport_soc_series/scripts/progress_soc_series.py --mode long
/home/cyzcomputer/.local/bin/micromamba run -n zifb_md python outputs/md_transport_soc_series/scripts/check_soc_health.py --mode long
```

`long_run_status_summary.json` and `long_run_health.json` count a case complete
only when `prod.gro`, `prod.xtc`, and `prod.log` progress at the configured
production length are all present.
`long_run_health.json` also records workspace disk usage (`disk.free_gb`,
`disk.used_gb`, and `disk_min_free_gb`), so overnight runs have an early warning
if trajectory or nojump analysis output could run the drive too low. The
`trajectory_disk_projection` block estimates final `prod.xtc` growth and a
conservative `analysis_nojump_allowance_gb` for the unwrapped analysis copies;
`projected_free_gb_after_prod_and_nojump` is the resulting free-space check.

The watcher/finalizer is started with:

```bash
powershell -NoProfile -ExecutionPolicy Bypass -File outputs/md_transport_soc_series/scripts/start_watch_finalize_windows.ps1
```

Watcher state is recorded in:

- `outputs/md_transport_soc_series/results/watch_finalize_status.json`

## Optional Viscosity Replicas

Generate the priority-SOC replica plan without launching new MD:

```bash
/home/cyzcomputer/.local/bin/micromamba run -n zifb_md python outputs/md_transport_soc_series/scripts/prepare_viscosity_replicates.py
```

After the source case has `npt.gro`, prepare replica directories, still without
running GROMACS:

```bash
/home/cyzcomputer/.local/bin/micromamba run -n zifb_md python outputs/md_transport_soc_series/scripts/prepare_viscosity_replicates.py --prepare
```

Run one prepared replica explicitly:

```bash
bash outputs/md_transport_soc_series/scripts/run_viscosity_replicate.sh soc050_q1p0 rep01
```

Aggregate completed replicas, or record missing-replica status tables before
they are run:

```bash
/home/cyzcomputer/.local/bin/micromamba run -n zifb_md python outputs/md_transport_soc_series/scripts/analyze_viscosity_replicates.py
```

Replica results are a Green-Kubo noise cross-check for priority SOCs, not a
replacement for iodine-carrier MSD ratios in the `D_eff(SOC)` closure.

An optional resume watcher can be left running during overnight jobs. It does
not launch duplicate production jobs: it reads `long_run_health.json`, only
targets cases marked `interrupted_or_stalled` or `not_in_production`, skips any
case with an active `mdrun` hint, and probes the per-run `.run_soc.lock` before
starting `run_soc_system.sh` from existing checkpoints.

```bash
powershell -NoProfile -ExecutionPolicy Bypass -File outputs/md_transport_soc_series/scripts/start_watch_resume_windows.ps1
```

Resume watcher state is recorded in:

- `outputs/md_transport_soc_series/results/watch_resume_status.json`

## Finalize

When all ten long production trajectories have `prod.gro`, `prod.xtc`, and
`prod.log` progress at the configured target production length, the watcher
runs:

```bash
/home/cyzcomputer/.local/bin/micromamba run -n zifb_md python outputs/md_transport_soc_series/scripts/finalize_soc_series.py --force-analysis
/home/cyzcomputer/.local/bin/micromamba run -n zifb_md python -m pytest -q outputs/md_transport_soc_series/tests
/home/cyzcomputer/.local/bin/micromamba run -n zifb_md python outputs/md_transport_soc_series/scripts/audit_completion_soc.py
```

The finalizer also writes checksum manifests:

- `outputs/md_transport_soc_series/results/artifact_manifest.json`
- `outputs/md_transport_soc_series/results/artifact_manifest.csv`

## Main Artifacts

- `outputs/md_transport_soc_series/results/soc_transport_summary.csv`
- `outputs/md_transport_soc_series/results/all_soc_diffusion_results.csv`
- `outputs/md_transport_soc_series/results/selected_soc_diffusion_results.csv`
- `outputs/md_transport_soc_series/results/closure_fit.csv`
- `outputs/md_transport_soc_series/results/closure_fit.json`
- `outputs/md_transport_soc_series/report.html`
- `outputs/md_transport_soc_series/source_notes.md`
- `outputs/md_transport_soc_series/results/completion_audit.md`
- `outputs/md_transport_soc_series/results/completion_audit.json`
- `outputs/md_transport_soc_series/results/requirements_traceability.md`
- `outputs/md_transport_soc_series/results/requirements_traceability.csv`
- `outputs/md_transport_soc_series/results/artifact_manifest.json`
- `outputs/md_transport_soc_series/results/artifact_manifest.csv`
- `outputs/md_transport_soc_series/results/long_run_status_summary.json`
- `outputs/md_transport_soc_series/results/finalize_soc_series.json`
- `outputs/md_transport_soc_series/results/watch_resume_status.json`

Figures:

- `outputs/md_transport_soc_series/figures/carrier_diffusion_throttle.png`
- `outputs/md_transport_soc_series/figures/species_diffusion_by_soc.png`
- `outputs/md_transport_soc_series/figures/viscosity_density_by_soc.png`
- `outputs/md_transport_soc_series/figures/carrier_composition.png`
- `outputs/md_transport_soc_series/figures/carrier_contact_phase_warning.png`

## Nature-Style Figures

The report PNG figures can be regenerated in a Nature-style static format with:

```bash
/home/cyzcomputer/micromamba/envs/zifb_md/bin/python outputs/md_transport_soc_series/scripts/make_nature_figures.py
```

This overwrites the report-facing PNG files in `outputs/md_transport_soc_series/figures/`
and writes matching high-resolution PNG plus editable vector PDF/SVG copies under
`outputs/md_transport_soc_series/figures/nature/`. The styling follows the practical
Nature final-artwork constraints checked from
`https://www.nature.com/nature/for-authors/final-submission`: sans-serif lettering,
double-column 183 mm layouts for multi-series graphs, 5-7 pt print-scale labels,
8 pt bold panel labels, 0.25-1 pt line weights, RGB color, quiet grids, and vector
source files for line art.

## Completion Gate

The goal is complete only when `completion_audit.json` reports `status:
"ready"`, pytest passes, all ten long cases are selected in the summary, and the
HTML report/source notes carry the force-field, literature-anchor, ECC, phase
warning, requirement-traceability, and no-COMSOL/no-.mph boundaries. The hard
transport closure gate is the long iodine-carrier diffusion ratio; Green-Kubo
viscosity is retained as a noisy cross-check subset and must provide at least
three usable long positive `mu`/Stokes-Einstein rows spanning both charge-scale
variants and at least two configured viscosity-priority SOC values.
