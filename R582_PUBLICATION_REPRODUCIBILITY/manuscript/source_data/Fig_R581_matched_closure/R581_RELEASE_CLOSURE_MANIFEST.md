# R581 true-mesh closure release manifest

Status: **RELEASE PASS**

The frozen tolerance and 7776-element true-mesh gates both passed. The plotted trajectories are
the passing true-mesh pair; no canonical/coarse trajectory is used as the release headline.

Canonical source-copy SHA-256: `4813B306F39330CCEAF819C4AB8815C55A3DF8A04726741F33ACB801B8806B9B`

| File | Bytes | SHA-256 |
|---|---:|---|
| `R581_true_mesh_control_timeseries.csv` | 303558 | `B6C0EAB603D17E9477CADAB04F6F0093D0C98261925561E510C82B9203704569` |
| `R581_true_mesh_physical_timeseries.csv` | 311513 | `22B8AE22303A850BAEA710E293992103C5783AB158B63F7E7ACD757561014AF8` |
| `R581_CONVERGENCE_SUMMARY.json` | 9474 | `4F052D61A5E025DF4BFA95C6193EBEC696730E2C0462C3B39D61E3CAAAC8FD4A` |
| `R581_matched_closure_summary.json` | 4278 | `4317F061F3BB2AA008E4195D0AEACB28C895FACCF92888A8ACF00C7EE313FFE2` |
| `R581_release_closure_comparison.csv` | 208094 | `313394276D495DE455CE90101443FD9742BD77715347862A1A6C1E557E92F528` |
| `R581_release_closure_summary.json` | 6553 | `A213CCDBADE269AD59FB8F2BBD74EAC9D5E28585CBBC6F7E42A1FD4939DC34AE` |
| `R581_release_closure_methods_lock.json` | 868 | `D2CFE5EE0E607A16E959AE725B79F2BD4CBD8D94852007CD633C02B8E81DE6DC` |

The control and physical COMSOL inputs were byte-identical copies. Only `cov_theta_surf` and
`theta_eff_R520` were changed in the physical branch. Original/raw MPH files were not modified.
The voltage difference quantifies model-closure sensitivity and does not identify deposit morphology.
