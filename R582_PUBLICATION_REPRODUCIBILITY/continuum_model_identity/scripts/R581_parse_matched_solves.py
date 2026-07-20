#!/usr/bin/env python3
"""Parse and gate R581 COMSOL stdout trajectories.

The COMSOL Java sandbox emits the full trajectory to stdout.  This parser
converts only CSV_HEADER/CSV_ROW records into deterministic tables, verifies
the fresh control against the registered R526/R525 production trajectory, and
builds the matched control/physical-dense comparison without touching any MPH.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(r"E:\zifb_final_9129_luck")
RUN = ROOT / "battery_comsol/02_outputs_core/R581_CANONICAL_CLOSURE_REBUILD"
CONTROL_STDOUT = RUN / "logs/R581_matched_control_run5_stdout.txt"
PHYSICAL_STDOUT = RUN / "logs/R581_matched_physical_dense_stdout.txt"
CONTROL_MPH = RUN / "outputs/R581_matched_control_SOLVED.mph"
PHYSICAL_MPH = RUN / "outputs/R581_matched_physical_dense_SOLVED.mph"
HISTORICAL = (
    ROOT
    / "battery_comsol/02_outputs_core/R526_COMSOL_NATIVE_KNOB_EXPORT"
    / "R526_GPT_REVIEW_BUNDLE_STAGE/data/R525_all_timeseries.csv"
)
OUT = RUN / "outputs"

EXPECTED_COLUMNS = [
    "case_id",
    "time_s",
    "q_mAh_cm2",
    "voltage_V",
    "S_direct",
    "S_reconstructed",
    "cI2_surf_free_avg_mol_m3",
    "cI2_surf_tot_avg_mol_m3",
    "beta_surf_avg",
    "cI_minus_surf_avg_mol_m3",
    "eps_s_avg",
    "eps_s_reg_avg",
    "theta_avg",
    "A_bare_avg",
    "K_perm_rel_avg",
    "D_rel_avg",
    "eps_l_eff_avg",
    "Rfilm_avg_ohm_m2",
    "R_precip_avg",
    "R_diss_avg",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest().upper()


def interp_crossing(x: np.ndarray, y: np.ndarray, level: float) -> float | None:
    finite = np.isfinite(x) & np.isfinite(y)
    x = x[finite]
    y = y[finite]
    hit = np.flatnonzero(y >= level)
    if hit.size == 0:
        return None
    i = int(hit[0])
    if i == 0:
        return float(x[0])
    x0, x1 = float(x[i - 1]), float(x[i])
    y0, y1 = float(y[i - 1]), float(y[i])
    if y1 == y0:
        return x1
    return x0 + (level - y0) * (x1 - x0) / (y1 - y0)


def parse_stdout(path: Path, expected_case: str) -> tuple[pd.DataFrame, dict]:
    if not path.exists():
        raise FileNotFoundError(path)
    header = None
    rows: list[list[str]] = []
    parameters: list[dict[str, str]] = []
    metadata: list[dict[str, str]] = []
    ok_marker = False
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for raw in handle:
            line = raw.rstrip("\r\n")
            if line.startswith("CSV_HEADER,"):
                parsed = next(csv.reader([line]))
                header = parsed[1:]
            elif line.startswith("CSV_ROW,"):
                rows.append(next(csv.reader([line]))[1:])
            elif line.startswith("PARAMETER,"):
                parts = line.split(",", 3)
                parameters.append(
                    {
                        "name": parts[1] if len(parts) > 1 else "",
                        "value": parts[2] if len(parts) > 2 else "",
                        "description": parts[3] if len(parts) > 3 else "",
                    }
                )
            elif line.startswith(("CLOSURE_", "STUDY_FEATURE,", "DATASET_MAPPING,", "MODEL_TAGS,")):
                key, _, value = line.partition(",")
                metadata.append({"record": key, "value": value})
            elif line.startswith("R581_CASE_OK,"):
                ok_marker = True

    if header != EXPECTED_COLUMNS:
        raise ValueError(f"Unexpected header in {path}: {header}")
    if not rows:
        raise ValueError(f"No CSV_ROW records in {path}")
    if any(len(row) != len(header) for row in rows):
        bad = [i for i, row in enumerate(rows) if len(row) != len(header)][:5]
        raise ValueError(f"Malformed rows in {path}: {bad}")
    if not ok_marker:
        raise ValueError(f"Missing R581_CASE_OK marker in {path}")

    frame = pd.DataFrame(rows, columns=header)
    if set(frame["case_id"].unique()) != {expected_case}:
        raise ValueError(f"Unexpected case ID in {path}: {frame['case_id'].unique()}")
    for column in header[1:]:
        frame[column] = pd.to_numeric(frame[column], errors="raise")
    if len(frame) != 1081:
        raise ValueError(f"Expected 1081 rows, found {len(frame)} in {path}")
    if not np.all(np.diff(frame["time_s"].to_numpy()) > 0):
        raise ValueError(f"Non-monotonic time in {path}")
    return frame, {"parameters": parameters, "metadata": metadata}


def trajectory_metrics(frame: pd.DataFrame) -> dict:
    q = frame["q_mAh_cm2"].to_numpy(float)
    s = frame["S_direct"].to_numpy(float)
    theta = frame["theta_avg"].to_numpy(float)
    return {
        "rows": int(len(frame)),
        "Q_s_mAh_cm2": interp_crossing(q, s, 1.0),
        "Q_theta_0p5_mAh_cm2": interp_crossing(q, theta, 0.5),
        "Q_theta_0p9_mAh_cm2": interp_crossing(q, theta, 0.9),
        "endpoint": {
            key: float(frame.iloc[-1][key])
            for key in [
                "q_mAh_cm2",
                "voltage_V",
                "S_direct",
                "S_reconstructed",
                "eps_s_avg",
                "theta_avg",
                "A_bare_avg",
                "K_perm_rel_avg",
            ]
        },
        "S_identity_max_abs": float(
            np.max(np.abs(frame["S_direct"] - frame["S_reconstructed"]))
        ),
    }


def historical_control() -> pd.DataFrame:
    hist = pd.read_csv(HISTORICAL)
    hist = hist.loc[hist["case_id"].eq("baseline_J40_Q120")].copy()
    if len(hist) != 1081:
        raise ValueError(f"Historical baseline rows={len(hist)}, expected 1081")
    return hist


def control_gate(control: pd.DataFrame) -> tuple[dict, bool]:
    hist = historical_control()
    if not np.allclose(
        control["q_mAh_cm2"].to_numpy(float),
        hist["q_mAh_cm2"].to_numpy(float),
        rtol=0,
        atol=1e-9,
    ):
        raise ValueError("Fresh control and historical production Q grids differ")

    pairs = {
        "voltage_V": "voltage_V",
        "S_direct": "S_avg",
        "eps_s_avg": "eps_s_avg",
        "theta_avg": "theta_avg",
        "A_bare_avg": "A_bare_avg",
        "K_perm_rel_avg": "K_perm_rel_avg",
        "D_rel_avg": "D_rel_avg",
    }
    max_abs = {
        new: float(np.nanmax(np.abs(control[new].to_numpy(float) - hist[old].to_numpy(float))))
        for new, old in pairs.items()
    }
    fresh = trajectory_metrics(control)
    hq = hist["q_mAh_cm2"].to_numpy(float)
    historical_metrics = {
        "Q_s_mAh_cm2": interp_crossing(hq, hist["S_avg"].to_numpy(float), 1.0),
        "Q_theta_0p5_mAh_cm2": interp_crossing(hq, hist["theta_avg"].to_numpy(float), 0.5),
        "endpoint": {
            "voltage_V": float(hist.iloc[-1]["voltage_V"]),
            "eps_s_avg": float(hist.iloc[-1]["eps_s_avg"]),
            "theta_avg": float(hist.iloc[-1]["theta_avg"]),
        },
    }
    eps_ref = abs(historical_metrics["endpoint"]["eps_s_avg"])
    checks = {
        "max_abs_voltage_le_1mV": max_abs["voltage_V"] <= 1e-3,
        "delta_Qs_le_0p5": abs(fresh["Q_s_mAh_cm2"] - historical_metrics["Q_s_mAh_cm2"]) <= 0.5,
        "delta_Qtheta_le_0p5": abs(fresh["Q_theta_0p5_mAh_cm2"] - historical_metrics["Q_theta_0p5_mAh_cm2"]) <= 0.5,
        "endpoint_eps_rel_le_1pct": abs(
            fresh["endpoint"]["eps_s_avg"] - historical_metrics["endpoint"]["eps_s_avg"]
        )
        / eps_ref
        <= 0.01,
        "endpoint_theta_abs_le_0p005": abs(
            fresh["endpoint"]["theta_avg"] - historical_metrics["endpoint"]["theta_avg"]
        )
        <= 0.005,
        "S_identity_le_1e-6": fresh["S_identity_max_abs"] <= 1e-6,
    }
    result = {
        "fresh": fresh,
        "historical": historical_metrics,
        "max_abs_trace_difference": max_abs,
        "checks": checks,
        "pass": bool(all(checks.values())),
    }
    return result, result["pass"]


def write_csv(frame: pd.DataFrame, path: Path) -> None:
    frame.to_csv(path, index=False, float_format="%.12g", lineterminator="\n")


def write_json(payload: dict, path: Path) -> None:
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_inventory(meta: dict, prefix: str) -> tuple[Path, Path]:
    p_params = OUT / f"R581_{prefix}_parameter_inventory.csv"
    p_meta = OUT / f"R581_{prefix}_model_metadata.csv"
    pd.DataFrame(meta["parameters"]).to_csv(p_params, index=False, lineterminator="\n")
    pd.DataFrame(meta["metadata"]).to_csv(p_meta, index=False, lineterminator="\n")
    return p_params, p_meta


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("control", "full"), default="full")
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)

    control, control_meta = parse_stdout(CONTROL_STDOUT, "matched_control")
    control_csv = OUT / "R581_matched_control_timeseries.csv"
    write_csv(control, control_csv)
    control_params, control_model_meta = write_inventory(control_meta, "matched_control")
    gate, passed = control_gate(control)
    gate["input_files"] = {
        "stdout": {"path": str(CONTROL_STDOUT), "sha256": sha256(CONTROL_STDOUT)},
        "solved_mph": {"path": str(CONTROL_MPH), "sha256": sha256(CONTROL_MPH)},
        "historical_csv": {"path": str(HISTORICAL), "sha256": sha256(HISTORICAL)},
    }
    gate_json = OUT / "R581_control_reproduction_gate.json"
    write_json(gate, gate_json)
    if not passed:
        print(json.dumps(gate["checks"], indent=2), file=sys.stderr)
        return 2

    if args.mode == "control":
        print(f"CONTROL_GATE_PASS,{gate_json}")
        return 0

    physical, physical_meta = parse_stdout(PHYSICAL_STDOUT, "matched_physical_dense")
    physical_csv = OUT / "R581_matched_physical_dense_timeseries.csv"
    write_csv(physical, physical_csv)
    physical_params, physical_model_meta = write_inventory(physical_meta, "matched_physical_dense")

    if control_meta["parameters"] != physical_meta["parameters"]:
        raise ValueError("Baseline parameter inventories differ between matched processes")
    q_control = control["q_mAh_cm2"].to_numpy(float)
    q_physical = physical["q_mAh_cm2"].to_numpy(float)
    if not np.allclose(q_control, q_physical, rtol=0, atol=1e-9):
        raise ValueError("Matched trajectories do not share the same Q grid")

    comparison = pd.DataFrame(
        {
            "q_mAh_cm2": q_control,
            "time_s": control["time_s"],
            "V_control_V": control["voltage_V"],
            "V_physical_dense_V": physical["voltage_V"],
            "deltaV_physical_minus_control_V": physical["voltage_V"] - control["voltage_V"],
            "eps_s_control": control["eps_s_avg"],
            "eps_s_physical_dense": physical["eps_s_avg"],
            "theta_control": control["theta_avg"],
            "theta_physical_dense": physical["theta_avg"],
            "theta_dense_shadow_on_control": 1.0
            - np.exp(-35.4 * np.power(control["eps_s_reg_avg"].to_numpy(float), 0.6222)),
            "S_control": control["S_direct"],
            "S_physical_dense": physical["S_direct"],
            "K_perm_control": control["K_perm_rel_avg"],
            "K_perm_physical_dense": physical["K_perm_rel_avg"],
        }
    )
    comparison_csv = OUT / "R581_matched_closure_comparison.csv"
    write_csv(comparison, comparison_csv)

    c_metrics = trajectory_metrics(control)
    p_metrics = trajectory_metrics(physical)
    shadow_qhalf = interp_crossing(
        q_control,
        comparison["theta_dense_shadow_on_control"].to_numpy(float),
        0.5,
    )
    summary = {
        "analysis_id": "R581_CANONICAL_CLOSURE_REBUILD",
        "analysis_date": "2026-07-11",
        "matched_settings": {
            "source_copy_sha256": "4813B306F39330CCEAF819C4AB8815C55A3DF8A04726741F33ACB801B8806B9B",
            "study": "stdR522",
            "solution": "sol5",
            "control_dataset": "dsetR581Ctrl",
            "physical_dataset": "dsetR581Phys",
            "time_grid": "range(0,10,10800) inherited and audited",
            "only_model_expression_change": {
                "cov_theta_surf": "1-exp(-35.4*eps_s_reg^0.6222)",
                "theta_eff_R520": "1-exp(-35.4*eps_s_reg^0.6222)",
            },
        },
        "control_reproduction_gate": gate,
        "control": c_metrics,
        "physical_dense": p_metrics,
        "one_way_dense_shadow": {
            "Q_theta_0p5_mAh_cm2": shadow_qhalf,
            "endpoint_theta": float(comparison.iloc[-1]["theta_dense_shadow_on_control"]),
            "feedback": False,
        },
        "matched_difference": {
            "endpoint_deltaV_mV": float(
                1000.0
                * (p_metrics["endpoint"]["voltage_V"] - c_metrics["endpoint"]["voltage_V"])
            ),
            "max_abs_deltaV_mV": float(
                1000.0 * comparison["deltaV_physical_minus_control_V"].abs().max()
            ),
            "endpoint_delta_eps_s": float(
                p_metrics["endpoint"]["eps_s_avg"] - c_metrics["endpoint"]["eps_s_avg"]
            ),
            "endpoint_delta_theta": float(
                p_metrics["endpoint"]["theta_avg"] - c_metrics["endpoint"]["theta_avg"]
            ),
        },
        "identity_gate_pass": bool(
            c_metrics["S_identity_max_abs"] <= 1e-6
            and p_metrics["S_identity_max_abs"] <= 1e-6
        ),
        "parameter_inventory_identical": True,
        "raw_or_original_mph_modified": False,
    }
    summary_json = OUT / "R581_matched_closure_summary.json"
    write_json(summary, summary_json)

    methods = {
        "analysis_id": "R581_CANONICAL_CLOSURE_REBUILD",
        "python": sys.version.split()[0],
        "pandas": pd.__version__,
        "numpy": np.__version__,
        "crossing_estimator": "first upward level crossing; linear interpolation on common 10 s/Q grid; no extrapolation",
        "S_direct": "aveop1(cI2_surf_free/cI2_sat)",
        "S_reconstructed": "aveop1(gamma_I2_saltout*cI2_surf_tot/(beta_I2_surf_dyn*cI2_sat0))",
        "identity_tolerance": 1e-6,
        "control_acceptance": {
            "max_abs_voltage_V": 1e-3,
            "max_abs_Qs_mAh_cm2": 0.5,
            "max_abs_Qtheta_mAh_cm2": 0.5,
            "max_rel_endpoint_eps_s": 0.01,
            "max_abs_endpoint_theta": 0.005,
        },
    }
    methods_json = OUT / "R581_matched_closure_methods_lock.json"
    write_json(methods, methods_json)

    report = OUT / "R581_MATCHED_CLOSURE_REPORT.md"
    qf_c = c_metrics["Q_theta_0p5_mAh_cm2"]
    qf_p = p_metrics["Q_theta_0p5_mAh_cm2"]
    report.write_text(
        "# R581 matched closure comparison\n\n"
        "The fresh control passed every predeclared reproduction gate against the registered R526/R525 production trajectory. "
        "The physical-dense solve began from an independent byte-identical copy and changed only `cov_theta_surf` and `theta_eff_R520` to "
        "`1-exp(-35.4*eps_s_reg^0.6222)`. Both solves used `stdR522`, live `sol5`, and independent datasets mapped explicitly to `sol5`.\n\n"
        f"- Control: `Q_s={c_metrics['Q_s_mAh_cm2']:.4f}` and `Q_theta=0.5={qf_c:.4f}` mAh cm^-2; endpoint "
        f"`V={c_metrics['endpoint']['voltage_V']:.6f} V`, `eps_s={c_metrics['endpoint']['eps_s_avg']:.6g}`, "
        f"`theta={c_metrics['endpoint']['theta_avg']:.6f}`.\n"
        f"- Physical dense: `Q_s={p_metrics['Q_s_mAh_cm2']:.4f}` and "
        + (f"`Q_theta=0.5={qf_p:.4f}` mAh cm^-2" if qf_p is not None else "`Q_theta=0.5` not reached")
        + f"; endpoint `V={p_metrics['endpoint']['voltage_V']:.6f} V`, `eps_s={p_metrics['endpoint']['eps_s_avg']:.6g}`, "
        f"`theta={p_metrics['endpoint']['theta_avg']:.6f}`.\n"
        f"- Matched endpoint voltage difference (physical minus control): `{summary['matched_difference']['endpoint_deltaV_mV']:.3f} mV`.\n"
        f"- One-way dense shadow on the control epsilon trajectory: `Q_theta=0.5={shadow_qhalf:.4f} mAh cm^-2`, endpoint "
        f"`theta={summary['one_way_dense_shadow']['endpoint_theta']:.6f}`; this is postprocessing without feedback.\n"
        f"- Maximum direct/reconstructed saturation mismatch: control `{c_metrics['S_identity_max_abs']:.3e}`, physical `{p_metrics['S_identity_max_abs']:.3e}`.\n\n"
        "Interpretation is closure-conditional. This comparison quantifies the consequence of one accessibility-expression change inside the fixed continuum model; it does not identify the real deposit morphology.\n",
        encoding="utf-8",
        newline="\n",
    )

    output_paths = [
        control_csv,
        physical_csv,
        comparison_csv,
        gate_json,
        summary_json,
        methods_json,
        report,
        control_params,
        control_model_meta,
        physical_params,
        physical_model_meta,
    ]
    manifest = pd.DataFrame(
        [
            {"path": str(path), "bytes": path.stat().st_size, "sha256": sha256(path)}
            for path in output_paths
        ]
    )
    manifest.to_csv(OUT / "R581_matched_closure_output_manifest.csv", index=False, lineterminator="\n")
    print(f"FULL_GATE_PASS,{summary_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

