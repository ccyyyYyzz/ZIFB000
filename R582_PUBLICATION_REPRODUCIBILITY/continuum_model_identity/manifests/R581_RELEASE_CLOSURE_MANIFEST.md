# R581 true-mesh closure release manifest

Status: **RELEASE PASS**

The frozen tolerance and 7776-element true-mesh gates both passed. The plotted trajectories are
the passing true-mesh pair; no canonical/coarse trajectory is used as the release headline.

Canonical source-copy SHA-256: `4813B306F39330CCEAF819C4AB8815C55A3DF8A04726741F33ACB801B8806B9B`

| File | Bytes | SHA-256 |
|---|---:|---|
| `outputs/R581_true_mesh_control_timeseries.csv` | 303558 | `B6C0EAB603D17E9477CADAB04F6F0093D0C98261925561E510C82B9203704569` |
| `outputs/R581_true_mesh_physical_timeseries.csv` | 311513 | `22B8AE22303A850BAEA710E293992103C5783AB158B63F7E7ACD757561014AF8` |
| `outputs/R581_CONVERGENCE_SUMMARY.json` | 9282 | `FAD9E58A3A755AA4D1E19A51013CAC64BB2C6F8DFFBB6D57A90519730127948B` |
| `outputs/R581_matched_closure_summary.json` | 4278 | `4317F061F3BB2AA008E4195D0AEACB28C895FACCF92888A8ACF00C7EE313FFE2` |
| `outputs/R581_release_closure_comparison.csv` | 208094 | `313394276D495DE455CE90101443FD9742BD77715347862A1A6C1E557E92F528` |
| `outputs/R581_release_closure_summary.json` | 6553 | `B2579CDB8488AEFBDC113D2674AAE3F3F07D9A75863A8018D34D906C8BC52132` |
| `outputs/R581_release_closure_methods_lock.json` | 960 | `A3F16E8DAF4747DE510236C1926485D27A05911778471DB36BFC29414A377ADD` |

The control and physical COMSOL inputs were byte-identical copies. Only `cov_theta_surf` and
`theta_eff_R520` were changed in the physical branch. Original/raw MPH files were not modified.
The voltage difference quantifies model-closure sensitivity and does not identify deposit morphology.
