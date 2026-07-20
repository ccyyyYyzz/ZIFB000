from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / "logs" / "R581_state_route_probe_stdout.txt"
OUT = ROOT / "outputs" / "R581_state_route_probe.csv"
SUMMARY = ROOT / "outputs" / "R581_state_route_summary.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


lines = LOG.read_text(encoding="utf-8", errors="replace").splitlines()
header_lines = [line for line in lines if line.startswith("ROUTE_HEADER,")]
rows = [line for line in lines if line.startswith("ROUTE_ROW,")]
if len(header_lines) != 1:
    raise RuntimeError(f"Expected one ROUTE_HEADER; found {len(header_lines)}")
if len(rows) != 1081:
    raise RuntimeError(f"Expected 1081 ROUTE_ROW lines; found {len(rows)}")
if "PROBE,OK,no_solve_no_save" not in lines:
    raise RuntimeError("Read-only completion marker absent")

header = next(csv.reader([header_lines[0]]))[1:]
matrix = [next(csv.reader([line]))[1:] for line in rows]
df = pd.DataFrame(matrix, columns=header).apply(pd.to_numeric, errors="raise")
if not np.all(np.diff(df["Q_mAh_cm2"].to_numpy()) >= 0):
    raise RuntimeError("Capacity grid is not monotone")

OUT.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUT, index=False, float_format="%.12g")

q = df["Q_mAh_cm2"].to_numpy()
j_bare = df["j_bare_geom_A_m2"].to_numpy()
j_phase = df["j_i2s_geom_A_m2"].to_numpy()
j_total = df["j_positive_geom_A_m2"].to_numpy()
phase_fraction = np.divide(j_phase, j_total, out=np.zeros_like(j_phase), where=np.abs(j_total) > 1e-12)
charge_phase_fraction = float(np.trapz(j_phase, q) / np.trapz(j_total, q))

summary = {
    "status": "PASS",
    "source_model_use": "read_only_sol5_dset5; no solve; no save",
    "rows": int(len(df)),
    "output_csv": str(OUT),
    "output_csv_sha256": sha256(OUT),
    "endpoint": {key: float(df.iloc[-1][key]) for key in df.columns},
    "phase_current_fraction_endpoint": float(phase_fraction[-1]),
    "phase_current_fraction_max": float(np.nanmax(phase_fraction)),
    "phase_charge_fraction_trapezoidal_over_Q": charge_phase_fraction,
    "feedback_to_parallel_ode_solid_ratio_endpoint": float(
        df.iloc[-1]["eps_s_feedback_avg"] / df.iloc[-1]["eps_s_ode_avg"]
    ),
    "stdout_sha256": sha256(LOG),
}
SUMMARY.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
print(json.dumps(summary, indent=2))
