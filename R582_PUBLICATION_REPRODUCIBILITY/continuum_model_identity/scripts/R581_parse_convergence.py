#!/usr/bin/env python3
"""Parse and gate R581 tolerance and true-mesh convergence trajectories.

The script is intentionally progressive: it parses every completed case, reports
missing cases as pending, and declares a release pass only when both the tighter-
tolerance pair and the 4x-element true-mesh pair pass the frozen gates.  It never
opens or modifies an MPH file.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd


RUN = Path(r"E:\zifb_final_9129_luck\battery_comsol\02_outputs_core\R581_CANONICAL_CLOSURE_REBUILD")
LOGS = RUN / "logs"
OUT = RUN / "outputs"
MANIFESTS = RUN / "manifests"

EXPECTED_COLUMNS = [
    "case_id", "time_s", "q_mAh_cm2", "voltage_V", "S_direct",
    "S_reconstructed", "cI2_surf_free_avg_mol_m3",
    "cI2_surf_tot_avg_mol_m3", "beta_surf_avg",
    "cI_minus_surf_avg_mol_m3", "eps_s_avg", "eps_s_reg_avg",
    "theta_avg", "A_bare_avg", "K_perm_rel_avg", "D_rel_avg",
    "eps_l_eff_avg", "Rfilm_avg_ohm_m2", "R_precip_avg", "R_diss_avg",
]

CASES = {
    "tolerance_control": {
        "log": LOGS / "R581_refined_control_stdout.txt",
        "case_id": "matched_control_refined",
        "marker": "R581_CASE_OK,matched_control_refined",
        "csv": OUT / "R581_tolerance_control_timeseries.csv",
        "mph": OUT / "R581_matched_control_REFINED_SOLVED.mph",
        "mesh_elements": 1944,
        "rtol": 3e-4,
    },
    "tolerance_physical": {
        "log": LOGS / "R581_refined_physical_stdout.txt",
        "case_id": "matched_physical_dense_refined",
        "marker": "R581_CASE_OK,matched_physical_dense_refined",
        "csv": OUT / "R581_tolerance_physical_timeseries.csv",
        "mph": OUT / "R581_matched_physical_dense_REFINED_SOLVED.mph",
        "mesh_elements": 1944,
        "rtol": 3e-4,
    },
    "mesh_control": {
        "log": LOGS / "R581_true_mesh_control_stdout.txt",
        "case_id": "matched_control_true_mesh",
        "marker": "R581_TRUE_MESH_CASE_OK,matched_control_true_mesh",
        "csv": OUT / "R581_true_mesh_control_timeseries.csv",
        "mph": OUT / "R581_true_mesh_control_SOLVED.mph",
        "mesh_elements": 7776,
        "rtol": 3e-4,
    },
    "mesh_physical": {
        "log": LOGS / "R581_true_mesh_physical_stdout.txt",
        "case_id": "matched_physical_dense_true_mesh",
        "marker": "R581_TRUE_MESH_CASE_OK,matched_physical_dense_true_mesh",
        "csv": OUT / "R581_true_mesh_physical_timeseries.csv",
        "mph": OUT / "R581_true_mesh_physical_dense_SOLVED.mph",
        "mesh_elements": 7776,
        "rtol": 3e-4,
    },
}

BASE_CONTROL = OUT / "R581_matched_control_timeseries.csv"
BASE_PHYSICAL = OUT / "R581_matched_physical_dense_timeseries.csv"
SUMMARY_JSON = OUT / "R581_CONVERGENCE_SUMMARY.json"
REPORT_MD = OUT / "R581_CONVERGENCE_REPORT.md"
METHODS_JSON = OUT / "R581_convergence_methods_lock.json"
MANIFEST_CSV = OUT / "R581_convergence_output_manifest.csv"

GATES = {
    "max_abs_deltaV_endpoint_change_mV": 2.0,
    "max_abs_Qs_change_mAh_cm2": 0.25,
    "max_abs_control_Qtheta0p5_change_mAh_cm2": 0.50,
    "max_abs_endpoint_theta_change": 0.010,
    "max_rel_endpoint_eps_change": 0.10,
    "max_S_identity_abs": 1e-8,
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest().upper()


def write_json(payload: dict, path: Path) -> None:
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8", newline="\n",
    )


def crossing(x: np.ndarray, y: np.ndarray, level: float) -> float | None:
    finite = np.isfinite(x) & np.isfinite(y)
    x, y = x[finite], y[finite]
    hit = np.flatnonzero(y >= level)
    if hit.size == 0:
        return None
    i = int(hit[0])
    if i == 0:
        return float(x[0])
    x0, x1 = float(x[i - 1]), float(x[i])
    y0, y1 = float(y[i - 1]), float(y[i])
    return x1 if y1 == y0 else x0 + (level - y0) * (x1 - x0) / (y1 - y0)


def parse_stdout(spec: dict) -> tuple[pd.DataFrame, dict]:
    path = spec["log"]
    text = path.read_text(encoding="utf-8", errors="replace")
    if spec["marker"] not in text:
        raise ValueError(f"missing terminal marker in {path}")
    header: list[str] | None = None
    rows: list[list[str]] = []
    for raw in text.splitlines():
        if raw.startswith("CSV_HEADER,"):
            header = next(csv.reader([raw]))[1:]
        elif raw.startswith("CSV_ROW,"):
            rows.append(next(csv.reader([raw]))[1:])
    if header != EXPECTED_COLUMNS:
        raise ValueError(f"unexpected header in {path}: {header}")
    if len(rows) != 1081 or any(len(row) != len(header) for row in rows):
        raise ValueError(f"expected 1081 complete rows in {path}, got {len(rows)}")
    frame = pd.DataFrame(rows, columns=header)
    if set(frame["case_id"].unique()) != {spec["case_id"]}:
        raise ValueError(f"unexpected case id in {path}: {frame['case_id'].unique()}")
    for column in header[1:]:
        frame[column] = pd.to_numeric(frame[column], errors="raise")
    if not np.all(np.diff(frame["time_s"].to_numpy(float)) > 0):
        raise ValueError(f"non-monotonic time grid in {path}")
    frame.to_csv(spec["csv"], index=False, float_format="%.12g", lineterminator="\n")
    provenance = {
        "stdout": {"path": str(path), "sha256": sha256(path)},
        "timeseries": {"path": str(spec["csv"]), "sha256": sha256(spec["csv"])},
        "mesh_elements": spec["mesh_elements"],
        "rtol": spec["rtol"],
    }
    if spec["mph"].exists():
        provenance["solved_mph"] = {
            "path": str(spec["mph"]), "bytes": spec["mph"].stat().st_size,
            "sha256": sha256(spec["mph"]),
        }
    else:
        raise FileNotFoundError(spec["mph"])
    return frame, provenance


def metrics(frame: pd.DataFrame) -> dict:
    q = frame["q_mAh_cm2"].to_numpy(float)
    s = frame["S_direct"].to_numpy(float)
    theta = frame["theta_avg"].to_numpy(float)
    endpoint_cols = [
        "q_mAh_cm2", "voltage_V", "S_direct", "eps_s_avg", "theta_avg",
        "A_bare_avg", "K_perm_rel_avg",
    ]
    return {
        "rows": int(len(frame)),
        "Q_s_mAh_cm2": crossing(q, s, 1.0),
        "Q_theta_0p5_mAh_cm2": crossing(q, theta, 0.5),
        "Q_theta_0p9_mAh_cm2": crossing(q, theta, 0.9),
        "endpoint": {key: float(frame.iloc[-1][key]) for key in endpoint_cols},
        "S_identity_max_abs": float(
            np.max(np.abs(frame["S_direct"] - frame["S_reconstructed"]))
        ),
    }


def load_base(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path)
    if len(frame) != 1081:
        raise ValueError(f"base rows in {path}: {len(frame)}")
    return frame


def pair_summary(control: pd.DataFrame, physical: pd.DataFrame) -> dict:
    qc = control["q_mAh_cm2"].to_numpy(float)
    qp = physical["q_mAh_cm2"].to_numpy(float)
    if not np.allclose(qc, qp, rtol=0, atol=1e-9):
        raise ValueError("control and physical Q grids differ")
    cm, pm = metrics(control), metrics(physical)
    delta = physical["voltage_V"].to_numpy(float) - control["voltage_V"].to_numpy(float)
    return {
        "control": cm,
        "physical": pm,
        "endpoint_deltaV_physical_minus_control_mV": float(1000.0 * delta[-1]),
        "max_abs_deltaV_mV": float(1000.0 * np.max(np.abs(delta))),
    }


def safe_abs(a: float | None, b: float | None) -> float | None:
    if a is None or b is None:
        return None
    return abs(float(a) - float(b))


def rel_change(a: float, b: float) -> float:
    denom = max(abs(float(a)), 1e-30)
    return abs(float(b) - float(a)) / denom


def compare_pairs(reference: dict, candidate: dict, comparator: str) -> dict:
    rc, rp = reference["control"], reference["physical"]
    cc, cp = candidate["control"], candidate["physical"]
    values = {
        "endpoint_deltaV_change_mV": abs(
            candidate["endpoint_deltaV_physical_minus_control_mV"]
            - reference["endpoint_deltaV_physical_minus_control_mV"]
        ),
        "control_Qs_change_mAh_cm2": safe_abs(rc["Q_s_mAh_cm2"], cc["Q_s_mAh_cm2"]),
        "physical_Qs_change_mAh_cm2": safe_abs(rp["Q_s_mAh_cm2"], cp["Q_s_mAh_cm2"]),
        "control_Qtheta0p5_change_mAh_cm2": safe_abs(
            rc["Q_theta_0p5_mAh_cm2"], cc["Q_theta_0p5_mAh_cm2"]
        ),
        "control_endpoint_theta_change": abs(
            cc["endpoint"]["theta_avg"] - rc["endpoint"]["theta_avg"]
        ),
        "physical_endpoint_theta_change": abs(
            cp["endpoint"]["theta_avg"] - rp["endpoint"]["theta_avg"]
        ),
        "control_endpoint_eps_rel_change": rel_change(
            rc["endpoint"]["eps_s_avg"], cc["endpoint"]["eps_s_avg"]
        ),
        "physical_endpoint_eps_rel_change": rel_change(
            rp["endpoint"]["eps_s_avg"], cp["endpoint"]["eps_s_avg"]
        ),
    }
    checks = {
        "deltaV": values["endpoint_deltaV_change_mV"] <= GATES["max_abs_deltaV_endpoint_change_mV"],
        "control_Qs": values["control_Qs_change_mAh_cm2"] <= GATES["max_abs_Qs_change_mAh_cm2"],
        "physical_Qs": values["physical_Qs_change_mAh_cm2"] <= GATES["max_abs_Qs_change_mAh_cm2"],
        "control_Qtheta0p5": values["control_Qtheta0p5_change_mAh_cm2"] <= GATES["max_abs_control_Qtheta0p5_change_mAh_cm2"],
        "control_theta_endpoint": values["control_endpoint_theta_change"] <= GATES["max_abs_endpoint_theta_change"],
        "physical_theta_endpoint": values["physical_endpoint_theta_change"] <= GATES["max_abs_endpoint_theta_change"],
        "control_eps_endpoint": values["control_endpoint_eps_rel_change"] <= GATES["max_rel_endpoint_eps_change"],
        "physical_eps_endpoint": values["physical_endpoint_eps_rel_change"] <= GATES["max_rel_endpoint_eps_change"],
        "S_identity": max(
            cc["S_identity_max_abs"], cp["S_identity_max_abs"]
        ) <= GATES["max_S_identity_abs"],
    }
    return {
        "comparator": comparator, "values": values, "checks": checks,
        "pass": bool(all(checks.values())),
    }


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    base_control, base_physical = load_base(BASE_CONTROL), load_base(BASE_PHYSICAL)
    base = pair_summary(base_control, base_physical)
    parsed: dict[str, pd.DataFrame] = {}
    provenance: dict[str, dict] = {}
    pending: list[str] = []
    errors: dict[str, str] = {}
    for name, spec in CASES.items():
        if not spec["log"].exists() or spec["marker"] not in spec["log"].read_text(
            encoding="utf-8", errors="replace"
        ):
            pending.append(name)
            continue
        try:
            parsed[name], provenance[name] = parse_stdout(spec)
        except Exception as exc:  # retain a complete audit instead of partial silent failure
            errors[name] = f"{type(exc).__name__}: {exc}"

    tolerance = None
    tolerance_gate = None
    if {"tolerance_control", "tolerance_physical"} <= parsed.keys():
        tolerance = pair_summary(parsed["tolerance_control"], parsed["tolerance_physical"])
        tolerance_gate = compare_pairs(base, tolerance, "tighter tolerance vs canonical")

    mesh = None
    mesh_gate = None
    if {"mesh_control", "mesh_physical"} <= parsed.keys():
        mesh = pair_summary(parsed["mesh_control"], parsed["mesh_physical"])
        if tolerance is None:
            errors["mesh_comparator"] = "true mesh exists but tighter-tolerance reference pair is incomplete"
        else:
            mesh_gate = compare_pairs(tolerance, mesh, "7776-element mesh vs 1944-element mesh at rtol=3e-4")

    release_pass = bool(
        not pending and not errors and tolerance_gate and tolerance_gate["pass"]
        and mesh_gate and mesh_gate["pass"]
    )
    payload = {
        "analysis_id": "R581_CONVERGENCE_GATE",
        "analysis_date": "2026-07-11",
        "canonical": base,
        "tighter_tolerance": tolerance,
        "true_mesh": mesh,
        "tolerance_gate": tolerance_gate,
        "mesh_gate": mesh_gate,
        "gates": GATES,
        "pending": pending,
        "errors": errors,
        "provenance": provenance,
        "true_mesh_element_ratio": 4.0,
        "release_pass": release_pass,
    }
    write_json(payload, SUMMARY_JSON)
    write_json(
        {
            "python": sys.version.split()[0], "pandas": pd.__version__,
            "numpy": np.__version__, "crossing": "first upward crossing with linear interpolation",
            "comparison_design": "canonical -> tighter tolerance; tighter tolerance -> 4x-element mesh",
            "gates": GATES,
        },
        METHODS_JSON,
    )

    lines = [
        "# R581 convergence report", "",
        f"Release pass: **{release_pass}**", "",
        f"Pending cases: {', '.join(pending) if pending else 'none'}", "",
    ]
    if errors:
        lines += ["## Errors", ""] + [f"- {k}: {v}" for k, v in errors.items()] + [""]
    for title, pair, gate in [
        ("Tighter-tolerance pair", tolerance, tolerance_gate),
        ("True-mesh pair", mesh, mesh_gate),
    ]:
        lines += [f"## {title}", ""]
        if pair is None:
            lines += ["Not complete.", ""]
            continue
        lines += [
            f"- endpoint delta V (physical-control): {pair['endpoint_deltaV_physical_minus_control_mV']:.6f} mV",
            f"- control Qs: {pair['control']['Q_s_mAh_cm2']:.6f} mAh cm^-2",
            f"- control Qtheta=0.5: {pair['control']['Q_theta_0p5_mAh_cm2']:.6f} mAh cm^-2",
            f"- physical Qs: {pair['physical']['Q_s_mAh_cm2']:.6f} mAh cm^-2",
            f"- physical Qtheta=0.5: {pair['physical']['Q_theta_0p5_mAh_cm2']}",
            f"- gate pass: {gate['pass'] if gate else False}", "",
        ]
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

    generated = [SUMMARY_JSON, METHODS_JSON, REPORT_MD] + [
        spec["csv"] for name, spec in CASES.items() if name in parsed
    ]
    manifest_rows = [
        {"path": str(path), "bytes": path.stat().st_size, "sha256": sha256(path)}
        for path in generated
    ]
    pd.DataFrame(manifest_rows).to_csv(MANIFEST_CSV, index=False, lineterminator="\n")
    print(f"R581_CONVERGENCE_STATUS,release_pass={str(release_pass).lower()},pending={len(pending)},errors={len(errors)}")
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
