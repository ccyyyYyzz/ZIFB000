# R581 matched control / physical-dense branch manifest

Run date: 2026-07-11  
COMSOL: 6.3.0.290  
Python: 3.11.5 (`pandas 1.5.3`, `numpy 1.24.4`)  
Study: `stdR522`  
Live solution: `sol5`  
Mesh: `mesh1`  
Output time grid: `range(0,10,10800)`; 1081 rows

## Scope and causal contract

Both processes began from independent, byte-identical copies of the registered production model. The control changed no model expression. The physical-dense process changed only:

```text
cov_theta_surf = 1-exp(-35.4*eps_s_reg^0.6222)
theta_eff_R520 = 1-exp(-35.4*eps_s_reg^0.6222)
```

All baseline parameters, geometry, mesh, study and solver configuration remained inherited and identical. The parameter inventories are byte-identical (`SHA-256 DDFA9B1...12979`). The control dataset `dsetR581Ctrl` and physical dataset `dsetR581Phys` were each created after the fresh solve and explicitly mapped to that process's live `sol5`.

## MPH files

| Role | File | Bytes | SHA-256 |
|---|---|---:|---|
| control input copy | `inputs/R581_control_input_COPY.mph` | 889150140 | `4813B306F39330CCEAF819C4AB8815C55A3DF8A04726741F33ACB801B8806B9B` |
| physical input copy | `inputs/R581_physical_dense_input_COPY.mph` | 889150140 | `4813B306F39330CCEAF819C4AB8815C55A3DF8A04726741F33ACB801B8806B9B` |
| fresh matched control | `outputs/R581_matched_control_SOLVED.mph` | 889170873 | `B26D8FA00159C7EF90B5932886C54F285BBBD8EBA899A0F7C62AAD7D8FBC6FED` |
| fresh physical dense | `outputs/R581_matched_physical_dense_SOLVED.mph` | 889170714 | `685B9F63051A467D22727FFCFA6E39D7DE2F60A4FF5E6F7993E6398630750ECF` |

The registered original archive and all input copies remain at the original source hash. No original MPH was saved or modified.

## Executable sources

| File | SHA-256 |
|---|---|
| `scripts/R581MatchedRun.java` | `C7A09BC139B76F6A00504564CD330F99AC56FA2421ADA4A053351C0E759A9AAA` |
| `scripts/R581MatchedRun.class` | `5AED9DA09BE9EC0E9C5EFC2B3D61BCEF90B0DC9F0B51C69E32F37251CEDEFA37` |
| `scripts/R581MatchedPhysicalRun.java` | `626B7653B3F178EA358362A33F48A5485EA69DC363A5BEE63726D5DBA2D75A83` |
| `scripts/R581MatchedPhysicalRun.class` | `C74B5F6607685C1CA49B2BFB5276F572A1A55D78015E33F327C0B2BFD91E8F77` |
| `scripts/R581_parse_matched_solves.py` | `A2BE306E601E5877A1A6B42DB836346C97DEAAC5DB167CF0E507BA76CF03302B` |

## Process logs

| Process | stdout SHA-256 | stderr SHA-256 | batch-log SHA-256 |
|---|---|---|---|
| control | `AD5DD07AEA79F4494D923DC7CD2040161D8B22667FB607067DC9217541F1C1BE` | `E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855` | `A7354387F1A0110D7D4517771198A85049B2E8EB15A536485AF407BA309249E5` |
| physical dense | `1E07EC40A595071DDF9C7A6EFC6578310A6D1BE03599D02E062112931B438166` | `E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855` | `F3FE076FBA99A6C952C0EE05AA71AF54E62B93E7870D0828A9471AD8A7CDE721` |

Both stdout files end with `R581_CASE_OK`; both stderr files are empty.

## Frozen trajectories and analysis

| File | SHA-256 |
|---|---|
| `outputs/R581_matched_control_timeseries.csv` | `39BF832D215F70095B7119B0A07EC5AAEB86B18791CC2ED6D3F9DBA8AA0B70EB` |
| `outputs/R581_matched_physical_dense_timeseries.csv` | `240EE1ADE88C910194286D410C4247C83F0B9C8D82406DCC7010BC53E4EB799E` |
| `outputs/R581_matched_closure_comparison.csv` | `FA21C8B64A1272CA9A3445FBC43582A0DF349F253C0B255C1B89064FEFCAB068` |
| `outputs/R581_control_reproduction_gate.json` | `3D7280BEE90B0D148E866CB1B48DEA751741DC2EFDF340BC81165B7495670D7C` |
| `outputs/R581_matched_closure_summary.json` | `4317F061F3BB2AA008E4195D0AEACB28C895FACCF92888A8ACF00C7EE313FFE2` |
| `outputs/R581_matched_closure_methods_lock.json` | `B105EE9912FCDB934E101C59011D0C014B6BD6E0D1D8A1699651E246D0307DF0` |
| `outputs/R581_MATCHED_CLOSURE_REPORT.md` | `7171A46DA1C8CC8897723E677DD41E7E5E2878D4F460F65521F1FD6732920FA3` |
| `outputs/R581_matched_closure_output_manifest.csv` | `07C8EF24850FD4E02F5D7D50C16C92D78657F4B34C2C48E288DA26B67142DFB3` |

## Acceptance results

The fresh control passed all preregistered reproduction gates against the registered R526/R525 production trace:

- maximum absolute voltage-trace difference: `0.285066 mV` (`<=1 mV`);
- `Delta Q_s = -2.07e-6 mAh cm^-2` (`<=0.5`);
- `Delta Q_theta=0.5 = -4.80e-4 mAh cm^-2` (`<=0.5`);
- endpoint epsilon relative difference: `<1%`;
- endpoint theta absolute difference: `<0.005`;
- direct/reconstructed saturation identity: machine precision (`<=1e-6`).

Matched results:

| Metric | control | physical dense |
|---|---:|---:|
| `Q_s` (mAh cm^-2) | 83.0202 | 83.0205 |
| `Q_theta=0.5` (mAh cm^-2) | 99.5896 | not reached |
| endpoint `V` (V) | 1.728940 | 1.439405 |
| endpoint `eps_s` | 3.22421e-3 | 6.51170e-4 |
| endpoint `theta` | 0.989513 | 0.307415 |
| endpoint `K_perm_rel` | 0.956229 | 0.989099 |

The matched endpoint difference `V_physical - V_control = -289.536 mV`. On the control epsilon trajectory, the dense physical one-way shadow crosses one half at `118.6418 mAh cm^-2` and reaches `theta=0.631057`; in the coupled physical solve the feedback suppresses solid accumulation and the half-accessibility point is not reached.

This establishes a causal model-closure sensitivity under fixed continuum settings. It does not identify a unique physical morphology from voltage.

## Retained failed-launch audit

Four pre-solve launch attempts are retained in `logs/`:

1. wrapper dependency missing;
2. additional classpath not accepted by the batch class loader;
3. support-JAR route not accepted;
4. COMSOL security policy rejected environment-variable dispatch.

All four failed before `ModelUtil.load` or before any solve/save call. They affected no MPH. `run5` is the only control production run.

