# R581 read-only COMSOL identity probe

Run date: 2026-07-11  
COMSOL: 6.3.0.290  
Mode: load and evaluate only; no study run and no model save

## Immutable input

| File | Bytes | SHA-256 |
|---|---:|---|
| `inputs/R581_probe_input_COPY.mph` | 889150140 | `4813B306F39330CCEAF819C4AB8815C55A3DF8A04726741F33ACB801B8806B9B` |

The copy hash equals the registered source model hash. The original `.mph` was never opened for writing.

## Probe source and logs

| File | Bytes | SHA-256 |
|---|---:|---|
| `scripts/R581IdentityProbe.java` | 5763 | `1F4AA3761632ACDCF7C21A810B4D89D3459C94E3BFF08C7A12C8C4729B82AEC9` |
| `scripts/R581IdentityProbe.class` | 8434 | `5E846E0AAE330603849C5136722A7FA53FCA9D6EB79E8316BDEA46061D7D50B6` |
| `logs/R581_identity_probe_stdout.txt` | 10631 | `41C7BFB15FECF7563D6066F5FF25FFBB0D00E40DAC039D40306810BDE29BF81F` |
| `logs/R581_identity_probe_stderr.txt` | 0 | `E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855` |
| `logs/R581_identity_probe_batch.log` | 372 | `6AE939C7CBE8FF786E9F7D13EF875D4731966AF947EB57C33EB1D8E9BB240AE7` |

## Explicit identity result

- Studies: `std1`, `stdR522`.
- Solutions: `sol1` through `sol6`.
- `dset5` is a `Solution` dataset whose `solution` property is explicitly `sol5`.
- `dset4` also maps to `sol5`; both reproduce the same 1081-point production trajectory.
- Production endpoint from `dset5/sol5` at `Q=120 mAh cm^-2`:
  - `V = 1.72887516175 V`
  - `S_direct = 1.75902930702`
  - `cI2_surf_free = 0.779836326114 mol m^-3`
  - `cI2_surf_tot = 431.972080433 mol m^-3`
  - `beta_I2_surf_dyn = 553.940306264`
  - `eps_s = 3.21926062394e-3`
  - `theta_eff_R520 = 0.989509871859`
  - `A_bare = 0.0104314717782`
  - `K_perm_rel_R520 = 0.956287030170`
- Stored production closure:
  - `cov_theta_surf = 1-exp(-k_geo*N_i2_pos^(1/3)*eps_s_reg^(2/3))`
  - `theta_eff_R520 = cov_theta_surf`
- Parameters checked directly: `i_app=400 A m^-2`, `cI2_sat0=1.33 mol m^-3`, `gamma_I2_saltout=3`.
- Terminal marker in stdout: `PROBE,OK,no_solve_no_save`.

This manifest establishes branch identity only. It does not make the existing saved trajectory a fresh control re-solve; that is a separate R581 gate.

