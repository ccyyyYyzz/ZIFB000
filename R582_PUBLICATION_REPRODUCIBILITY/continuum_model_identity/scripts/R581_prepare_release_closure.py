#!/usr/bin/env python3
"""Freeze the passing true-mesh pair into the release closure-figure schema.

This script is read-only with respect to COMSOL files. It consumes only exported
CSV/JSON/manifest files and refuses to write release inputs unless the registered
R581 convergence parser reports ``release_pass=true``.
"""

from __future__ import annotations

import copy
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd


RUN = Path(__file__).resolve().parents[1]
OUT = RUN / "outputs"
MANIFESTS = RUN / "manifests"

CONTROL = OUT / "R581_true_mesh_control_timeseries.csv"
PHYSICAL = OUT / "R581_true_mesh_physical_timeseries.csv"
CONVERGENCE = OUT / "R581_CONVERGENCE_SUMMARY.json"
MATCHED_SUMMARY = OUT / "R581_matched_closure_summary.json"
MATCHED_MANIFEST = MANIFESTS / "MATCHED_BRANCH_MANIFEST.md"

COMPARISON_OUT = OUT / "R581_release_closure_comparison.csv"
SUMMARY_OUT = OUT / "R581_release_closure_summary.json"
METHODS_OUT = OUT / "R581_release_closure_methods_lock.json"
MANIFEST_OUT = MANIFESTS / "R581_RELEASE_CLOSURE_MANIFEST.md"

CLOSURE_A = 35.4
CLOSURE_B = 0.6222


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def read_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(payload: dict, path: Path) -> None:
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
        newline="\n",
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


def main() -> None:
    for path in (CONTROL, PHYSICAL, CONVERGENCE, MATCHED_SUMMARY, MATCHED_MANIFEST):
        require(path.is_file(), f"Missing registered input: {path}")

    convergence = read_json(CONVERGENCE)
    matched = read_json(MATCHED_SUMMARY)
    require(convergence.get("release_pass") is True, "Convergence release gate did not pass")
    require(convergence["tolerance_gate"]["pass"] is True, "Tolerance gate did not pass")
    require(convergence["mesh_gate"]["pass"] is True, "True-mesh gate did not pass")
    require(not convergence["pending"] and not convergence["errors"], "Convergence audit is incomplete")
    require(matched["raw_or_original_mph_modified"] is False, "Original-MPH mutation flag is not false")
    require(matched["parameter_inventory_identical"] is True, "Parameter inventories differ")

    control = pd.read_csv(CONTROL)
    physical = pd.read_csv(PHYSICAL)
    required = {
        "time_s", "q_mAh_cm2", "voltage_V", "S_direct", "S_reconstructed",
        "eps_s_avg", "eps_s_reg_avg", "theta_avg", "A_bare_avg", "K_perm_rel_avg",
    }
    require(required.issubset(control.columns), "Control schema mismatch")
    require(required.issubset(physical.columns), "Physical schema mismatch")
    require(len(control) == len(physical) == 1081, "Expected 1081 rows per true-mesh case")
    q = control["q_mAh_cm2"].to_numpy(float)
    time_s = control["time_s"].to_numpy(float)
    require(np.allclose(q, physical["q_mAh_cm2"], rtol=0, atol=1e-9), "Q grids differ")
    require(np.allclose(time_s, physical["time_s"], rtol=0, atol=1e-9), "Time grids differ")
    require(np.all(np.diff(q) > 0), "Q grid is not strictly increasing")
    require(np.allclose(np.diff(time_s), 10.0, rtol=0, atol=1e-10), "Time step is not 10 s")
    require(float(q[0]) == 0.0 and math.isclose(float(q[-1]), 120.0, abs_tol=1e-10), "Q extent mismatch")
    require(float(np.max(np.abs(control["S_direct"] - control["S_reconstructed"]))) <= 1e-8,
            "Control stress identity failed")
    require(float(np.max(np.abs(physical["S_direct"] - physical["S_reconstructed"]))) <= 1e-8,
            "Physical stress identity failed")

    theta_shadow = 1.0 - np.exp(-CLOSURE_A * control["eps_s_reg_avg"].to_numpy(float) ** CLOSURE_B)
    delta_v = physical["voltage_V"].to_numpy(float) - control["voltage_V"].to_numpy(float)
    comparison = pd.DataFrame(
        {
            "q_mAh_cm2": q,
            "time_s": time_s,
            "V_control_V": control["voltage_V"],
            "V_physical_dense_V": physical["voltage_V"],
            "deltaV_physical_minus_control_V": delta_v,
            "eps_s_control": control["eps_s_avg"],
            "eps_s_physical_dense": physical["eps_s_avg"],
            "theta_control": control["theta_avg"],
            "theta_physical_dense": physical["theta_avg"],
            "theta_dense_shadow_on_control": theta_shadow,
            "S_control": control["S_direct"],
            "S_physical_dense": physical["S_direct"],
            "K_control": control["K_perm_rel_avg"],
            "K_physical_dense": physical["K_perm_rel_avg"],
        }
    )
    comparison.to_csv(COMPARISON_OUT, index=False, float_format="%.12g", lineterminator="\n")

    release = copy.deepcopy(matched)
    true_mesh = convergence["true_mesh"]
    release.update(
        {
            "analysis_id": "R581_TRUE_MESH_CLOSURE_RELEASE",
            "release_pass": True,
            "control": copy.deepcopy(true_mesh["control"]),
            "physical_dense": copy.deepcopy(true_mesh["physical"]),
            "matched_difference": {
                "endpoint_deltaV_mV": true_mesh["endpoint_deltaV_physical_minus_control_mV"],
                "endpoint_delta_eps_s": float(physical.iloc[-1]["eps_s_avg"] - control.iloc[-1]["eps_s_avg"]),
                "endpoint_delta_theta": float(physical.iloc[-1]["theta_avg"] - control.iloc[-1]["theta_avg"]),
                "max_abs_deltaV_mV": true_mesh["max_abs_deltaV_mV"],
            },
            "one_way_dense_shadow": {
                "Q_theta_0p5_mAh_cm2": crossing(q, theta_shadow, 0.5),
                "endpoint_theta": float(theta_shadow[-1]),
                "feedback": False,
            },
            "convergence_release_gate": {
                "pass": True,
                "tolerance_gate": convergence["tolerance_gate"],
                "mesh_gate": convergence["mesh_gate"],
                "true_mesh_element_ratio": convergence["true_mesh_element_ratio"],
                "convergence_summary_sha256": sha256(CONVERGENCE),
            },
        }
    )
    for branch, frame in (("control", control), ("physical_dense", physical)):
        release[branch]["endpoint"]["S_reconstructed"] = float(frame.iloc[-1]["S_reconstructed"])
    release["matched_settings"].update(
        {
            "control_dataset": "dsetR581CtrlMesh",
            "physical_dataset": "dsetR581PhysMesh",
            "mesh_elements": 7776,
            "mesh_vertices": 7957,
            "mesh_min_quality": 0.198,
            "rtol": 3e-4,
            "time_grid": "range(0,10,10800); 1081 exported points",
        }
    )
    write_json(release, SUMMARY_OUT)

    methods = {
        "analysis_id": release["analysis_id"],
        "scientific_inputs": [str(CONTROL), str(PHYSICAL), str(CONVERGENCE), str(MATCHED_SUMMARY)],
        "comparison": "passing 7776-element control/physical pair at rtol=3e-4",
        "dense_shadow": "1-exp(-35.4*eps_s_reg_avg^0.6222) evaluated one-way on true-mesh control",
        "crossings": "first upward crossing with piecewise-linear interpolation",
        "smoothing": False,
        "raw_or_original_mph_modified": False,
    }
    write_json(methods, METHODS_OUT)

    payloads = [CONTROL, PHYSICAL, CONVERGENCE, MATCHED_SUMMARY, COMPARISON_OUT, SUMMARY_OUT, METHODS_OUT]
    lines = [
        "# R581 true-mesh closure release manifest",
        "",
        "Status: **RELEASE PASS**",
        "",
        "The frozen tolerance and 7776-element true-mesh gates both passed. The plotted trajectories are",
        "the passing true-mesh pair; no canonical/coarse trajectory is used as the release headline.",
        "",
        f"Canonical source-copy SHA-256: `{matched['matched_settings']['source_copy_sha256']}`",
        "",
        "| File | Bytes | SHA-256 |",
        "|---|---:|---|",
    ]
    for path in payloads:
        lines.append(f"| `{path.relative_to(RUN).as_posix()}` | {path.stat().st_size} | `{sha256(path)}` |")
    lines += [
        "",
        "The control and physical COMSOL inputs were byte-identical copies. Only `cov_theta_surf` and",
        "`theta_eff_R520` were changed in the physical branch. Original/raw MPH files were not modified.",
        "The voltage difference quantifies model-closure sensitivity and does not identify deposit morphology.",
    ]
    MANIFEST_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

    print(
        "R581_RELEASE_INPUTS_OK,"
        f"deltaV_mV={true_mesh['endpoint_deltaV_physical_minus_control_mV']:.9f},"
        f"Qs_control={true_mesh['control']['Q_s_mAh_cm2']:.9f},"
        f"Qtheta_control={true_mesh['control']['Q_theta_0p5_mAh_cm2']:.9f}"
    )


if __name__ == "__main__":
    main()
