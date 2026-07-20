# Project truth — zinc–iodine positive-electrode manuscript

Last updated: 2026-07-11

## Active sources of truth

- Main manuscript: `E:\zifb_final_9129_luck\manuscript\main.tex`
- Supplementary Information: `E:\zifb_final_9129_luck\manuscript\SI.tex`
- Bibliography: `E:\zifb_final_9129_luck\manuscript\refs.bib`
- Figures used by the manuscript: `E:\zifb_final_9129_luck\manuscript\figures\`
- Active contribution type: a mechanistic modeling framework for the positive electrode, supported by bounded lower-scale priors and descriptive/external-consistency experiments. It is not a parameter-free bottom-up prediction.
- Scientific protagonist: the zinc–iodine flow-battery (ZIFB) positive electrode and its coupled interfacial transport, iodine deposition, accessibility loss, and pore-scale feedback. `NH4Br` is only the representative supporting electrolyte used in the present experiments/model parameterization; neither ammonium bromide nor bromide is the paper's central contribution.
- Working venue: Electrochimica Acta. The evidence supports a rigorous computational/electrochemical-engineering contribution with descriptive existing-data context, but it does not independently validate the positive-electrode thresholds or morphology at the level needed for the higher-risk Journal of Power Sources positioning.

## Non-negotiable project constraints

1. No new physical experiments are possible or required. Evidence gaps may be closed only by literature anchors, new simulations, or reanalysis of existing data.
2. Original experimental files are immutable. Raw filenames and acquisition metadata are preserved exactly.
3. Original COMSOL `.mph` files are immutable. Any new solve must start from a verified copy, save to a new file, and record source/output SHA-256 hashes, command, COMSOL version, study, solution, dataset, and exported time series.
4. `E:\ns_mc_gan_gi_code` is outside this project and remains read-only/out of scope.
5. Bromide is a supporting/accommodating ligand and `NH4Br` is a representative supporting electrolyte, not the redox protagonist. Titles, abstracts, figure headlines, and conclusions must remain centred on the ZIFB positive electrode; electrolyte-specific observations are conditions or bounded supporting evidence only.
6. Every experimental filename or condition field labelled `NH4Cl` is an operator-confirmed metadata error; the electrolyte actually used was `NH4Br`. Raw names remain unchanged and normalized labels must be documented as an explicit metadata correction.
7. A clean-looking PDF is not sufficient. Submission readiness requires a cold reproducible build, correct float order, complete metadata, a frozen source-data package, and claim-to-evidence closure.

## Literature and writing-corpus roles

- Zotero collection `ZIFB` (collection key `3JJWXDL3`) is the project literature/evidence pool. Entries may support scientific statements only after item-level bibliographic and claim-level verification.
- Zotero collection `ZIFB_W` (collection key `QI8BAEXB`, 25 top-level items observed on 2026-07-11) is the Zhao/Wu group writing-pattern corpus. It is used for argument architecture, paragraph function, figure narration, and prose rhythm—not as automatic evidence for this manuscript.
- The local mirror and derived reading cards are in `E:\zifb_final_9129_luck\ZhaoWu_writing_corpus\`; its style guide may shape presentation but cannot override the evidence hierarchy or introduce unsupported claims.

## Canonical scientific interpretation

- Authoritative production branch: `PB-R526-J40-Q120-DSET5-v1`, input MPH SHA-256 `4813B306F39330CCEAF819C4AB8815C55A3DF8A04726741F33ACB801B8806B9B`, study `stdR522`, solution `sol5`, dataset `dset5`. The read-only R581 probe explicitly confirmed `dset5 -> sol5` and reproduced the 1081-point endpoint (`V=1.72887516175 V`, `eps_s=3.21926062394e-3`, `theta=0.989509871859`) without solving or saving.
- The registered continuum temperature is `293.15 K`; the separate MD prior was run at `298.15 K`. Earlier manuscript statements that assigned `298 K` to the COMSOL solve are superseded.
- The exact `E0'=0.548 V`, `i0=5e4 A m^-2`, `alpha_a=alpha_c=1`, `kappa_l=20 S m^-1`, `c_ref=120 mol m^-3`, `delta=25 um`, native-solid Tafel parameters, auxiliary phase-transfer rates, seed and smoothing values are prescribed, empirical or numerical model inputs, not independently identified present-electrolyte properties. In particular, the COMSOL description calling `20 S m^-1` measured is not supported by a raw conductivity record and must not be repeated as provenance.
- The MD carrier prior contains one 20 ns production trajectory per SOC/charge case. Its four-block statistic is within-trajectory stability, not an independent-replica SEM; all 18 planned viscosity-replica rows are missing energy outputs and are not results.
- The registered averaged-saturation marker is the surface-effective crossing, with
  `S_base = gamma_salt * (Pi_inv + Pi_gen) / beta_intra = c_f / c_sat_eff`.
- A read-only COMSOL feature-tree audit establishes the actual state route. The only transported iodine-species field is the lumped oxidized pool `cO = cBr2`; `cR = max(c_floor, cR0 - 3*cO)` is an algebraic stoichiometric inventory, not a second transported field. The active positive-electrode currents are the bare-carbon Butler--Volmer feature `tcd/pce2/per1` and the native deposited-species anodic-Tafel feature `tcd/pce2/per_i2s_tafel`. The latter uses `i0_i2s_phase = 0.05 A m^-2 * max(S_local-1,0)` and `Aa=118 mV`; it advances the feedback solid `eps_s_pos`.
- On canonical `sol5/dset5`, the native-solid path carries `0.5516%` of integrated charge and `27.994%` of endpoint positive current. It produces `eps_s=3.21926e-3`. The parallel smooth ODE tracker ends at only `eps_s_i2=1.08328e-6` (a factor `2972` lower) and must never be described as the reported retained-solid inventory. It enters the transported-pool balance through its phase-transfer rates but does not drive the parallel `N_i2` state. `dN_i2/dt=kappa_N*(N_target_i2-N_i2)` evolves independently and supplies the calibrated accessibility closure.
- The implemented bare-path equilibrium potential is `E0' + gamma_a RT/(2F) ln[max(c_f,c_floor)/(c_ref/beta)] + eta_tank`. Since `c_f=cO/beta`, it is an empirical total-oxidized-pool Nernst-like relation away from the floor, not a full `I2/I-` activity equation. Generic concentration reaction orders are zero.
- The production branch gives interpolated `Q_s = 83.0202 mAh cm^-2` and calibrated `Q_f,cal = 99.5901 mAh cm^-2`; endpoint values are `V=1.728875 V`, `eps_s=3.21926e-3`, and `theta_cal=0.989510`.
- The current production accessibility relation is voltage-calibrated. At its half-accessibility trajectory crossing, `eps_s,cal,traj* = 1.18572e-4`; this is closure/trajectory-specific and must never be presented as a parameter-free mesoscale material threshold or experimental failure point.
- The physical single-fibre island closure is a separate closure with a separate half-coverage solid fraction. Its outputs must not be assigned the production closure's `Q_f` without a same-branch coupled solve.
- Registered physical thresholds are `eps_s,island,1/2 = 1.7973e-3` for the fitted dense-island expression and `eps_s,film-perc* = 2.2324e-3` for geometric film percolation. The latter is not a half-accessibility definition.
- The pore-network result supports only that smooth bulk permeability remains near unity over the modeled operating load. It does not prove that discrete local pore blockage, a connected deposit, or a film is absent.
- Existing voltage data do not uniquely identify deposit morphology. The defensible conclusion is that the current fixed-parameter model needs a stronger effective connected-blockage response than the isolated-island closure to reproduce the late-rise branch; the actual morphology remains unresolved.
- R581 fresh matched solves quantify that closure sensitivity. The canonical-mesh control reproduces R526 within the predeclared gates. The convergence-qualified 7,776-element pair at `rtol=3e-4` gives control `Q_s=82.8903`, `Q_f,cal=99.4637`, endpoint `V=1.728364 V`, `eps_s=3.15236e-3`, `theta_cal=0.989982`; changing only `cov_theta_surf` and `theta_eff_R520` to the dense physical-island expression gives `Q_s=82.8924`, no half-accessibility crossing by `120 mAh cm^-2`, endpoint `V=1.440208 V`, `eps_s=6.58584e-4`, and `theta_island=0.309081`. The matched endpoint difference is `-288.156 mV`. Both tolerance and true-mesh gates pass. This is a model-closure sensitivity, not morphology identification.
- On the true-mesh control solid-inventory trajectory, the dense physical one-way shadow crosses one half at `118.6927 mAh cm^-2` and ends at `theta=0.625898`. The coupled physical solve ends at `0.309081` because accessibility feedback changes the solid-inventory trajectory; shadow and coupled curves must never be conflated.

## Canonical terminology

- `Q_s`: registered electrode-averaged saturation marker (`S_base = 1`); not the first local solid-forming event.
- `Q_f,cal`: half-accessibility marker of the voltage-calibrated production closure.
- `theta_cal(eps_s)`: calibrated production accessibility loss.
- `theta_island(eps_s)`: physical single-fibre island accessibility loss.
- `eps_s,cal*` and `eps_s,island*`: distinct half-accessibility solid fractions; never use one symbol for both.
- `external-consistency check`: comparison that is not a fit and not a validation.
- `descriptive experimental trend`: an observed trend lacking independent cell-level replication or a prespecified estimator.

## Evidence hierarchy

1. Immutable raw experiment files or solved-model copies with hashes.
2. Deterministic, versioned scripts plus machine-readable exported tables.
3. Frozen per-figure source-data tables.
4. Figures and narrative.

When levels disagree, the higher level wins and the lower level must be regenerated.

## Current release status

- Status: submission-package reconstruction; the true-mesh closure pair and release figure are complete. Cold-build/PDF QA, release-archive freezing, graphical-abstract handling and external author/repository metadata remain open.
- The R580 closure-provenance figure is retired because it compares different solution branches and mixes postprocessed and coupled trajectories.
- `R580_REMEDIATION_REPORT.md` and the attached pasted copy are historical handoff records, not release evidence. Their claim that the R533 traces form a `same-solve` causal comparison is superseded by the R581 branch audit and matched rebuild.
- Main/SI formulas, experimental provenance, the NH4Br correction, citation roles and figures have been synchronized. The old R566 closure-ablation panel is retired and replaced by the convergence-gated `Fig_R581_matched_closure`.
- The NH4Cl-to-NH4Br correction is now machine-readable at `battery_experiment/02_processed_data/R581_NH4BR_METADATA_CORRECTION/`: 114 project paths, 39 unique file hashes, zero raw-file modifications.
