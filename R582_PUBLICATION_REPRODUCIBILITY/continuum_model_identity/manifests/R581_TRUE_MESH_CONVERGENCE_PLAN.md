# R581 true-mesh convergence plan

Prepared: 2026-07-11  
Runtime status: **MESH-ONLY PROBE PASS; CONTROL/PHYSICAL COMPILED BUT NOT RUN**  
Serial history: an existing COMSOL batch process (`PID 59276`, refined control) was active during preparation, so no COMSOL operation was launched until that process exited normally. The subsequent mesh-only probe ran with zero other COMSOL processes active.

## Why the previous `hauto=4` run is not a mesh-convergence point

The read-only discretization probe established the stored mesh state:

```text
mesh1/size: hmax=0.00134 m, hmin=6e-6 m, hgrad=1.3, hauto=5
mesh1/map1/dis1: numelem=18
mesh1/map1/dis2: numelem=18
mesh1/map1/dis3: numelem=36
mesh statistics: 1944 elements, 2035 vertices, minimum quality 0.198
```

`R581RefinedControlRun.java` changed only `hauto` to 4 before rebuilding. Its stdout still reports exactly `1944` elements. This model uses an explicit mapped mesh, so changing only the default size feature does not change the mapped element counts.

The true-mesh case therefore applies both:

```text
mesh1/size/custom = on
hmax = 0.00067 m
hmin = 3e-6 m
hgrad = 1.2
map1/dis1/numelem = 36
map1/dis2/numelem = 36
map1/dis3/numelem = 72
```

The doubled Distribution counts are the COMSOL-API-equivalent refinement needed for this mapped mesh. The element count is not guessed in advance: the mesh-only probe must prove `after_elements > 1944` before any study solve is authorized.

## Verified independent inputs

All inputs are byte copies of the already verified R581 probe input, not the original archive. The original archive is never passed to a new process and is never writable.

| Role | File | Bytes | SHA-256 |
|---|---|---:|---|
| mesh-only probe | `inputs/R581_true_mesh_probe_input_COPY.mph` | 889150140 | `4813B306F39330CCEAF819C4AB8815C55A3DF8A04726741F33ACB801B8806B9B` |
| true-mesh control | `inputs/R581_true_mesh_control_input_COPY.mph` | 889150140 | `4813B306F39330CCEAF819C4AB8815C55A3DF8A04726741F33ACB801B8806B9B` |
| true-mesh physical dense | `inputs/R581_true_mesh_physical_input_COPY.mph` | 889150140 | `4813B306F39330CCEAF819C4AB8815C55A3DF8A04726741F33ACB801B8806B9B` |

These are physically separate files. The control and physical cases never reuse the mesh-only saved model and never continue from one another.

## Prepared sources and static audit

| File | Bytes | SHA-256 | Status |
|---|---:|---|---|
| `scripts/R581TrueMeshBuildProbe.java` | 6354 | `97853394ADE8B4224A9E1C7403972560E177DBD52D8D7DB3FB5826A487256DF2` | compiled and mesh-only run passed |
| `scripts/R581TrueMeshControlRun.java` | 11115 | `8CFB647D280734D74A35B1D4DEC486B545A8DA565D1419279A24EB928FB1D933` | compiled; not run |
| `scripts/R581TrueMeshPhysicalRun.java` | 11841 | `AD4FEED05CD6C02D77CE9B54D1144937564F0EB5FEFE70F705017B445185A09D` | compiled; not run |
| `scripts/R581_audit_true_mesh_sources.py` | see live manifest | see live manifest | static validator and future probe-log parser |
| `manifests/R581_TRUE_MESH_STATIC_AUDIT.json` | see file | see file | `static_status=PASS`, runtime probe `not_run` |

The `applyTrueMeshRefinement(Model model)` method is byte-identical in the control and physical sources:

```text
SHA-256 5FE41059C78322CF834CE3C1635B69B788777B7F1ED4C645D0B4EA2A353FEA25
```

The solve classes retain `rtol=3e-4`, matching the 1944-element refined-control run. Once that run finishes, the difference between it and the true-mesh control is a mesh-only comparison rather than a mesh-plus-time-tolerance comparison.

## Mandatory serial launch guard

Run every block below only when this returns `0`:

```powershell
@(Get-Process | Where-Object { $_.ProcessName -match '^comsol' }).Count
```

If the result is nonzero, stop. Do not compile, construct the mesh, or solve concurrently with another COMSOL process.

Set paths once:

```powershell
$root = 'E:\zifb_final_9129_luck\battery_comsol\02_outputs_core\R581_CANONICAL_CLOSURE_REBUILD'
$scripts = Join-Path $root 'scripts'
$logs = Join-Path $root 'logs'
$compile = 'D:\Program Files\COMSOL\COMSOL63\Multiphysics\bin\win64\comsolcompile.exe'
$batch = 'D:\Program Files\COMSOL\COMSOL63\Multiphysics\bin\win64\comsolbatch.exe'
$python = 'D:\Anacondar\anaconda3\python.exe'
```

## Step 1 — compile only after the guard passes

```powershell
Push-Location $scripts
& $compile 'R581TrueMeshBuildProbe.java'
if ($LASTEXITCODE -ne 0) { throw 'Probe compilation failed' }
& $compile 'R581TrueMeshControlRun.java'
if ($LASTEXITCODE -ne 0) { throw 'Control compilation failed' }
& $compile 'R581TrueMeshPhysicalRun.java'
if ($LASTEXITCODE -ne 0) { throw 'Physical compilation failed' }
Pop-Location
```

Do not continue unless all three `.class` files exist, `comsolcompile.exe` returned exit code zero for each source, and the Java source hashes still match the table above. A `.class.status` file is produced by `comsolbatch` execution, not by compilation, so it is not a compile gate.

## Step 2 — mesh-only probe; no study solve

```powershell
$argsProbe = @(
  '-inputfile', (Join-Path $scripts 'R581TrueMeshBuildProbe.class'),
  '-batchlog', (Join-Path $logs 'R581_true_mesh_probe_batch.log')
)
$p = Start-Process -FilePath $batch -ArgumentList $argsProbe -Wait -PassThru -WindowStyle Hidden `
  -RedirectStandardOutput (Join-Path $logs 'R581_true_mesh_probe_stdout.txt') `
  -RedirectStandardError (Join-Path $logs 'R581_true_mesh_probe_stderr.txt')
if ($p.ExitCode -ne 0) { throw "Mesh probe failed: exit $($p.ExitCode)" }
```

The probe is allowed to:

1. load only `R581_true_mesh_probe_input_COPY.mph`;
2. verify the starting count is 1944;
3. apply the frozen size and Distribution settings;
4. build `mesh1` only;
5. save only `outputs/R581_true_mesh_probe_MESHED_ONLY.mph`;
6. print `TRUE_MESH_PROBE_OK,...,no_study_run=true`.

It contains no call to `study(...).run()`.

## Step 3 — parse and enforce the mesh gate

```powershell
& $python (Join-Path $scripts 'R581_audit_true_mesh_sources.py') `
  --probe-log (Join-Path $logs 'R581_true_mesh_probe_stdout.txt')
if ($LASTEXITCODE -ne 0) { throw 'True-mesh audit failed' }
$audit = Get-Content -Raw (Join-Path $root 'manifests\R581_TRUE_MESH_STATIC_AUDIT.json') | ConvertFrom-Json
if ($audit.runtime_probe.status -ne 'pass') { throw 'Runtime mesh gate did not pass' }
if ($audit.runtime_probe.before_elements -ne 1944) { throw 'Unexpected coarse element count' }
if ($audit.runtime_probe.after_elements -le 1944) { throw 'Element count did not increase' }
```

Also require in stdout:

```text
TRUE_MESH_SIZE,after,...hmax=0.00067...hmin=3e-6...hgrad=1.2...
TRUE_MESH_DISTRIBUTIONS,after,dis1=36,dis2=36,dis3=72
TRUE_MESH_PROBE_OK,before_elements=1944,after_elements=<greater than 1944>,...,no_study_run=true
```

If any value is absent or COMSOL normalizes the stored string unexpectedly, inspect the actual property dump before changing code. Do not authorize a solve based only on the intended source literals.

## Step 4 — true-mesh control solve, still serial

Re-run the zero-process guard, then:

```powershell
$argsControl = @(
  '-inputfile', (Join-Path $scripts 'R581TrueMeshControlRun.class'),
  '-batchlog', (Join-Path $logs 'R581_true_mesh_control_batch.log')
)
$p = Start-Process -FilePath $batch -ArgumentList $argsControl -Wait -PassThru -WindowStyle Hidden `
  -RedirectStandardOutput (Join-Path $logs 'R581_true_mesh_control_stdout.txt') `
  -RedirectStandardError (Join-Path $logs 'R581_true_mesh_control_stderr.txt')
if ($p.ExitCode -ne 0) { throw "True-mesh control failed: exit $($p.ExitCode)" }
```

Required terminal marker:

```text
R581_TRUE_MESH_CASE_OK,matched_control_true_mesh,rows=1081,...
```

The saved model must be a new file:

```text
outputs/R581_true_mesh_control_SOLVED.mph
```

## Step 5 — physical-dense solve on the identical grid, still serial

Only after the control exits and the zero-process guard passes again:

```powershell
$argsPhysical = @(
  '-inputfile', (Join-Path $scripts 'R581TrueMeshPhysicalRun.class'),
  '-batchlog', (Join-Path $logs 'R581_true_mesh_physical_batch.log')
)
$p = Start-Process -FilePath $batch -ArgumentList $argsPhysical -Wait -PassThru -WindowStyle Hidden `
  -RedirectStandardOutput (Join-Path $logs 'R581_true_mesh_physical_stdout.txt') `
  -RedirectStandardError (Join-Path $logs 'R581_true_mesh_physical_stderr.txt')
if ($p.ExitCode -ne 0) { throw "True-mesh physical solve failed: exit $($p.ExitCode)" }
```

Required terminal marker:

```text
R581_TRUE_MESH_CASE_OK,matched_physical_dense_true_mesh,rows=1081,...
```

The saved model must be:

```text
outputs/R581_true_mesh_physical_dense_SOLVED.mph
```

## Convergence acceptance after the solves

For the control, compare against the completed 1944-element, `rtol=3e-4` refined-control trajectory on the same 1081-point time grid. The provisional submission gate is:

- maximum absolute voltage-trajectory difference `<= 1 mV`;
- `|Delta Q_s| <= 0.5 mAh cm^-2`;
- `|Delta Q_theta=0.5| <= 0.5 mAh cm^-2`;
- endpoint epsilon relative difference `<= 1%`;
- endpoint theta absolute difference `<= 0.005`;
- direct/reconstructed saturation identity `<= 1e-6`;
- both true-mesh solves report the same post-build element count and mesh settings.

If the gate fails, the result is mesh-sensitive and a third grid is required; do not relabel it converged. The physical-dense result is then compared on the same true mesh to preserve the causal closure contrast.

## Current readiness statement

- Input copies: **READY and hash-verified**.
- Java sources/classes: **COMPILED; static audit PASS**.
- Mesh-only runtime proof: **PASS — 1944 to 7776 elements (4.0x), requested values read back, no study run**.
- Control/physical solves: **READY BUT NOT RUN**; they remain subject to the serial guard and must execute control first, physical second.
- Original archive and all pre-existing R581 input copies: **UNCHANGED**.
