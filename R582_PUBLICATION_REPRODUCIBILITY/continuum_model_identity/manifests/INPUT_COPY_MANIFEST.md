# R581 canonical closure rebuild — input-copy manifest

Created: 2026-07-11

Immutable source archive:

`E:\cyz000\solved_mph_archive\R526_COMSOL_NATIVE_KNOB_EXPORT_TLIST_FIXED\baseline_J40_Q120\R526_baseline_J40_Q120_solved.mph`

Expected/source SHA-256:

`4813B306F39330CCEAF819C4AB8815C55A3DF8A04726741F33ACB801B8806B9B`

| Input copy | Bytes | SHA-256 | Role |
|---|---:|---|---|
| `inputs/R581_probe_input_COPY.mph` | 889,150,140 | `4813B306F39330CCEAF819C4AB8815C55A3DF8A04726741F33ACB801B8806B9B` | Read-only solution/dataset identity probe |
| `inputs/R581_control_input_COPY.mph` | 889,150,140 | `4813B306F39330CCEAF819C4AB8815C55A3DF8A04726741F33ACB801B8806B9B` | Fresh matched control re-solve |
| `inputs/R581_physical_dense_input_COPY.mph` | 889,150,140 | `4813B306F39330CCEAF819C4AB8815C55A3DF8A04726741F33ACB801B8806B9B` | Fresh matched physical-dense closure re-solve |

All three copies matched the expected hash before any COMSOL invocation. The source archive is never passed as an input to a run and will not be written.

## R581 true-mesh convergence copies (added 2026-07-11)

These additional files were copied from the already verified `R581_probe_input_COPY.mph`, then independently rehashed. They are reserved for the mesh-only proof and the subsequent serial control/physical true-mesh solves.

| Input copy | Bytes | SHA-256 | Role |
|---|---:|---|---|
| `inputs/R581_true_mesh_probe_input_COPY.mph` | 889,150,140 | `4813B306F39330CCEAF819C4AB8815C55A3DF8A04726741F33ACB801B8806B9B` | Mesh construction and element-count proof only; no study run |
| `inputs/R581_true_mesh_control_input_COPY.mph` | 889,150,140 | `4813B306F39330CCEAF819C4AB8815C55A3DF8A04726741F33ACB801B8806B9B` | Independent true-mesh control solve after probe gate |
| `inputs/R581_true_mesh_physical_input_COPY.mph` | 889,150,140 | `4813B306F39330CCEAF819C4AB8815C55A3DF8A04726741F33ACB801B8806B9B` | Independent true-mesh physical-dense solve after probe and control gates |

The three files are physical copies rather than hard links. No solve class saves over an input path. See `manifests/R581_TRUE_MESH_CONVERGENCE_PLAN.md` and `manifests/R581_TRUE_MESH_STATIC_AUDIT.json`.
