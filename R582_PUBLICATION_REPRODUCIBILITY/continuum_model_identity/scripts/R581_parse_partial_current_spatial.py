from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats


ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / "logs" / "R581_partial_current_spatial_stdout.txt"
DATA = ROOT / "outputs" / "R581_partial_current_spatial.csv"
TABLE = ROOT / "outputs" / "R581_partial_current_overlap.csv"
SUMMARY = ROOT / "outputs" / "R581_partial_current_overlap_summary.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def pearson(a: pd.Series, b: pd.Series) -> float:
    valid = np.isfinite(a) & np.isfinite(b)
    x, y = np.asarray(a[valid], float), np.asarray(b[valid], float)
    return float(np.corrcoef(x, y)[0, 1]) if len(x) >= 5 and x.std() and y.std() else np.nan


def spearman(a: pd.Series, b: pd.Series) -> float:
    valid = np.isfinite(a) & np.isfinite(b)
    x, y = np.asarray(a[valid], float), np.asarray(b[valid], float)
    return float(stats.spearmanr(x, y).statistic) if len(x) >= 5 else np.nan


lines = LOG.read_text(encoding="utf-8", errors="replace").splitlines()
headers = [line for line in lines if line.startswith("SPATIAL_HEADER,")]
rows = [line for line in lines if line.startswith("SPATIAL_ROW,")]
if len(headers) != 6 or len(set(headers)) != 1:
    raise RuntimeError(f"Expected six identical headers; found {len(headers)} / {len(set(headers))}")
section_rows = [line for line in lines if line.startswith("SECTION,")]
if len(section_rows) != 6:
    raise RuntimeError(f"Expected six SECTION records; found {len(section_rows)}")
declared_counts = [int(next(csv.reader([line]))[-1]) for line in section_rows]
if len(set(declared_counts)) != 1 or len(rows) != sum(declared_counts):
    raise RuntimeError(
        f"Spatial row mismatch: declared={declared_counts}, observed={len(rows)}"
    )
if "PROBE,OK,no_solve_no_save" not in lines:
    raise RuntimeError("Read-only completion marker absent")

header = next(csv.reader([headers[0]]))[1:]
matrix = [next(csv.reader([line]))[1:] for line in rows]
df = pd.DataFrame(matrix, columns=header)
df["time_label"] = df["time_label"].astype(str)
for column in df.columns[1:]:
    df[column] = pd.to_numeric(df[column], errors="raise")
df.to_csv(DATA, index=False, float_format="%.12g")

records: list[dict[str, float | int]] = []
for q, group in df.groupby("Q_mAh_cm2", sort=True):
    rich = group["eps_s_pos"] > group["eps_s_pos"].median()
    bare = group["j_bare_A_m2"].abs()
    solid = group["j_native_solid_A_m2"].abs()
    intensive = group["j_bare_A_m2"] / group["Av_bare_1_m"].replace(0, np.nan)
    records.append(
        {
            "Q_mAh_cm2": float(q),
            "n_nodes": int(len(group)),
            "n_positive_Av_bare": int((group["Av_bare_1_m"] > 0).sum()),
            "pearson_epss_jbare": pearson(group["eps_s_pos"], group["j_bare_A_m2"]),
            "spearman_epss_jbare": spearman(group["eps_s_pos"], group["j_bare_A_m2"]),
            "spearman_epss_intensive": spearman(group["eps_s_pos"], intensive),
            "spearman_epss_jsolid": spearman(group["eps_s_pos"], group["j_native_solid_A_m2"]),
            "spearman_epss_Avbare": spearman(group["eps_s_pos"], group["Av_bare_1_m"]),
            "frac_jbare_in_rich_half": float(bare[rich].sum() / (bare.sum() + 1e-30)),
            "frac_jsolid_in_rich_half": float(solid[rich].sum() / (solid.sum() + 1e-30)),
            "solid_share_node_sum": float(solid.sum() / (bare.sum() + solid.sum() + 1e-30)),
            "frac_nonzero_jsolid": float((solid > 1e-12).mean()),
        }
    )

out = pd.DataFrame(records)
out.to_csv(TABLE, index=False, float_format="%.12g")
summary = {
    "status": "PASS",
    "source_model_use": "read_only_sol5_dset5; no solve; no save",
    "statistic_scope": "unweighted exported points; no element or quadrature weights",
    "rich_half_definition": "eps_s_pos greater than the within-snapshot median",
    "current_fraction_definition": "sum of absolute pointwise current magnitudes within the median-defined half",
    "interpretation_limit": "metric-dependent spatial description; not a volume integral, exclusion test, or morphology measurement",
    "node_rows": int(len(df)),
    "snapshots": [float(value) for value in out["Q_mAh_cm2"]],
    "spatial_csv_sha256": sha256(DATA),
    "overlap_csv_sha256": sha256(TABLE),
    "stdout_sha256": sha256(LOG),
    "records": out.to_dict(orient="records"),
}
SUMMARY.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
print(out.to_string(index=False))
print(json.dumps({key: value for key, value in summary.items() if key != "records"}, indent=2))
