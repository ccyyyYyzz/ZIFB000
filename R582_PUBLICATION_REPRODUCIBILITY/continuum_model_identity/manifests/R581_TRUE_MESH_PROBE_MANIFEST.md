# R581 true-mesh build-probe manifest

Run date: 2026-07-11  
COMSOL: 6.3.0.290  
Mode: load verified copy, mutate mesh settings, build `mesh1`, inspect statistics, save a new meshed-only file  
Study/solution execution: **none**

## Immutable input copy

| File | Bytes | SHA-256 |
|---|---:|---|
| `inputs/R581_true_mesh_probe_input_COPY.mph` | 889150140 | `4813B306F39330CCEAF819C4AB8815C55A3DF8A04726741F33ACB801B8806B9B` |

The input hash equals the registered production-source hash. The probe saves only to a different output path.

## Source, compiled classes and audit helper

| File | Bytes | SHA-256 |
|---|---:|---|
| `scripts/R581TrueMeshBuildProbe.java` | 6354 | `97853394ADE8B4224A9E1C7403972560E177DBD52D8D7DB3FB5826A487256DF2` |
| `scripts/R581TrueMeshBuildProbe.class` | 7859 | `A2CB5BA4776B23BEC948DD17805DCE5A1D15BACF5ED42BF26AAE3F89A67CA8F4` |
| `scripts/R581TrueMeshControlRun.java` | 11115 | `8CFB647D280734D74A35B1D4DEC486B545A8DA565D1419279A24EB928FB1D933` |
| `scripts/R581TrueMeshControlRun.class` | 14452 | `5E3698EFE42C45604292A71A43CE4AFAD6E2272A79D25DE3EC16690DE819F83A` |
| `scripts/R581TrueMeshPhysicalRun.java` | 11841 | `AD4FEED05CD6C02D77CE9B54D1144937564F0EB5FEFE70F705017B445185A09D` |
| `scripts/R581TrueMeshPhysicalRun.class` | 15062 | `76240BBCEC6369289EAEBBE1872483FCDDD279D8F4330AF1503C24C56CEF8B53` |
| `scripts/R581_audit_true_mesh_sources.py` | 6877 | `C14E5CECC01A48B918224D161CCE4D81F20CC50F42AD568909999BAE8D062E5E` |

All three Java sources compiled successfully with COMSOL 6.3 `comsolcompile.exe`. The control and physical `applyTrueMeshRefinement` method bodies are byte-identical, SHA-256:

`5FE41059C78322CF834CE3C1635B69B788777B7F1ED4C645D0B4EA2A353FEA25`

## Process logs

| File | Bytes | SHA-256 |
|---|---:|---|
| `logs/R581_true_mesh_probe_stdout.txt` | 1031 | `DE214F00C987CBE3B73E0ACF08F916197EC4561D3AFC3B057D9A75D8118B4928` |
| `logs/R581_true_mesh_probe_stderr.txt` | 0 | `E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855` |
| `logs/R581_true_mesh_probe_batch.log` | 542 | `6A8B30F049F1B660A3555BE48F60B354AB62DDC7E9BEC867EB6AE9C6F9605C75` |

The process exit code was `0`, stderr is empty, and no other COMSOL process was active when it launched.

## Explicit before/after mesh result

| Quantity | Before | After |
|---|---:|---:|
| elements | 1944 | 7776 |
| vertices | 2035 | 7957 |
| minimum quality | 0.198 | 0.198 |
| mean quality | 0.3224 | 0.3224 |
| `size/custom` | off | on |
| `hmax` (m) | 0.00134 | 0.00067 |
| `hmin` (m) | 6.0e-6 | 3e-6 |
| `hgrad` | 1.3 | 1.2 |
| `map1/dis1/numelem` | 18 | 36 |
| `map1/dis2/numelem` | 18 | 36 |
| `map1/dis3/numelem` | 36 | 72 |

The element count increased by exactly `4.0x`. This is expected for doubling both mapped directions of the two-dimensional mesh; the value was measured rather than assumed.

Terminal marker:

```text
TRUE_MESH_PROBE_OK,before_elements=1944,after_elements=7776,ratio=4.0,no_study_run=true
```

## Meshed-only output

| File | Bytes | SHA-256 |
|---|---:|---|
| `outputs/R581_true_mesh_probe_MESHED_ONLY.mph` | 889452878 | `C8D1AA670D7E2FFAB2E7B2B4117EA1E9283357DD16A4DAA71234B40AB410D877` |

This output is an audit artifact only. It is not an input to either solve. The control and physical runs each start from their own baseline-hash copy and reconstruct the identical grid independently.

## Gate status

- True element-count change: **PASS**.
- Requested custom size values stored and read back: **PASS**.
- Mapped Distribution refinement stored and read back: **PASS**.
- Mesh quality did not degrade by the reported metrics: **PASS**.
- No study run / no solution run: **PASS**.
- No input or original MPH saved over: **PASS**.
- True-mesh control and physical source/class readiness: **COMPILED, NOT RUN**.

The next authorized operation is the true-mesh control solve, followed only after its exit by the true-mesh physical solve. They must remain serial.

