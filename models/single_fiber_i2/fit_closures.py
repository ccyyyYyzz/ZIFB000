"""Scan the single-fiber model and fit interpretable macro closures."""

from __future__ import annotations

import copy
import csv
import itertools
import json
from pathlib import Path
from typing import Any

import numpy as np
from scipy.optimize import minimize_scalar

from single_fiber_i2 import (
    diagnostics,
    initial_state,
    load_params,
    simulate_segment,
    smoothplus,
)


ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "outputs" / "single_fiber_i2"
DATABASE_PATH = OUT_DIR / "closure_database.csv"
FITS_PATH = OUT_DIR / "closure_fits.json"


def main() -> None:
    params = load_params()
    rows = run_scan(params)
    write_csv(rows, DATABASE_PATH)
    fits = fit_closure_models(rows, params)
    write_json(fits, FITS_PATH)
    print(f"Wrote {DATABASE_PATH}")
    print(f"Wrote {FITS_PATH}")


def run_scan(params: dict[str, Any]) -> list[dict[str, float | str | int]]:
    """Run the parameter scan configured in params.yaml."""

    scan = params["scan"]
    keys = [
        "theta_init",
        "h_I2_init",
        "cI2_tot_bulk",
        "cI_bulk",
        "cBr_support",
        "i_app_fiber",
        "mode",
    ]
    rows: list[dict[str, float | str | int]] = []
    case_id = 0
    for values in itertools.product(*(scan[key] for key in keys)):
        case = dict(zip(keys, values))
        case_id += 1
        case_rows = run_case(params, case, case_id)
        rows.extend(case_rows)
    return rows


def run_case(
    base_params: dict[str, Any], case: dict[str, Any], case_id: int
) -> list[dict[str, float | str | int]]:
    """Run one constant-current closure case and attach macro features."""

    params = copy.deepcopy(base_params)
    params["geometry"]["n_cells"] = int(params["scan"].get("n_cells", params["geometry"]["n_cells"]))
    params["time"]["max_step_s"] = float(params["scan"].get("max_step_s", params["time"]["max_step_s"]))
    params["coverage"]["theta_initial"] = float(case["theta_init"])
    params["film"]["h_initial_m"] = float(case["h_I2_init"])
    params["transport"]["cI2_tot_bulk_mol_m3"] = float(case["cI2_tot_bulk"])
    params["transport"]["cI_bulk_mol_m3"] = float(case["cI_bulk"])
    params["transport"]["cBr_support_mol_m3"] = float(case["cBr_support"])

    current_mag = abs(float(case["i_app_fiber"]))
    mode = str(case["mode"]).lower()
    if mode == "charge":
        i_app = current_mag
    elif mode == "discharge":
        i_app = -current_mag
    else:
        raise ValueError(f"Unknown scan mode: {mode}")

    duration = float(params["scan"]["duration_s"])
    dt = float(params["scan"]["dt_output_s"])
    t_eval = np.arange(0.0, duration + 0.5 * dt, dt)
    y0 = initial_state(params)
    n = int(params["geometry"]["n_cells"])
    y0[2 * n] = float(case["theta_init"])
    y0[2 * n + 1] = float(case["h_I2_init"])

    sol = simulate_segment(params, i_app, (0.0, duration), y0=y0, t_eval=t_eval)
    if not sol.success:
        raise RuntimeError(f"Scan case {case_id} failed: {sol.message}")

    diag_rows = diagnostics(sol.t, sol.y, i_app, params)
    sup_history = cumulative_trapezoid([row["time_s"] for row in diag_rows], [row["supersaturation"] for row in diag_rows])
    enriched: list[dict[str, float | str | int]] = []
    for row, history in zip(diag_rows, sup_history):
        c_undersat = float(
            smoothplus(
                params["complexation"]["cI2_sat_mol_m3"] - row["cI2_surf_free"],
                params["precipitation"]["smoothplus_eps_mol_m3"],
            )
        )
        frac_bare = safe_ratio(row["j_bare"], row["j_total"])
        frac_cov = safe_ratio(row["j_cov"], row["j_total"])
        enriched.append(
            {
                "case_id": case_id,
                "mode": mode,
                "theta_init": float(case["theta_init"]),
                "h_I2_init_m": float(case["h_I2_init"]),
                "cI2_tot_bulk_mol_m3": float(case["cI2_tot_bulk"]),
                "cI_bulk_mol_m3": float(case["cI_bulk"]),
                "cBr_support_mol_m3": float(case["cBr_support"]),
                "i_app_fiber_A_m2": i_app,
                "eps_s_pos": eps_s_pos_from_h(row["h_I2"], params),
                "supersaturation_history_mol_s_m3": history,
                "cI2_undersaturation": c_undersat,
                "frac_bare_current": frac_bare,
                "frac_cov_current": frac_cov,
                **row,
            }
        )
    return enriched


def fit_closure_models(rows: list[dict[str, Any]], params: dict[str, Any]) -> dict[str, Any]:
    """Fit the requested simple, interpretable closure forms."""

    h = arr(rows, "h_I2")
    theta = arr(rows, "theta")
    rfilm = arr(rows, "Rfilm_local")
    film_factor = arr(rows, "film_kin_factor")
    supersat = arr(rows, "supersaturation")
    undersat = arr(rows, "cI2_undersaturation")
    r_precip = arr(rows, "precipitation_rate")
    r_diss = arr(rows, "dissolution_rate")
    theta_init = arr(rows, "theta_init")

    theta_fit = fit_theta_h(h, theta, theta_init)
    film_fit = fit_film_factor(rfilm, film_factor, params)
    precip_fit = fit_rate_constant(supersat, r_precip, fallback=params["precipitation"]["k_precip_sf_m_s"])
    diss_fit = fit_rate_constant(theta * undersat, r_diss, fallback=params["precipitation"]["k_diss_sf_m_s"])
    split_fit = current_split_metrics(rows, film_fit["g_eff_S_m2"], params)

    return {
        "schema_version": "1.0",
        "source_database": DATABASE_PATH.relative_to(ROOT).as_posix(),
        "n_rows": len(rows),
        "theta_model": theta_fit,
        "film_model": film_fit,
        "precipitation_model": {
            "expression": "r_precip = k_precip_i2*cI2_supersat",
            "k_precip_i2_m_s": precip_fit["k"],
            "rmse_mol_m2_s": precip_fit["rmse"],
            "fit_rows": precip_fit["fit_rows"],
        },
        "dissolution_model": {
            "expression": "r_diss = k_diss_surf*theta*cI2_undersat",
            "k_diss_surf_m_s": diss_fit["k"],
            "rmse_mol_m2_s": diss_fit["rmse"],
            "fit_rows": diss_fit["fit_rows"],
        },
        "current_split_model": split_fit,
        "recommended_parameters": {
            "av0_i2_1_m": None,
            "k_geo": params["coverage"]["k_geo"],
            "k_precip_i2_m_s": precip_fit["k"],
            "k_diss_surf_m_s": diss_fit["k"],
            "sigma_I2_S_m": params["film"]["sigma_I2_S_m"],
            "g_eff_S_m2": film_fit["g_eff_S_m2"],
            "j0_bare_A_m2": params["electrochemistry"]["j0_bare_A_m2"],
            "j0_cov_A_m2": params["electrochemistry"]["j0_cov_A_m2"],
        },
        "notes": [
            "Fits are algebraic closures derived from the standalone single-fiber scan.",
            "The theta(h_I2) fit uses rows with theta_init near zero to avoid mixing arbitrary initial coverage with film thickness.",
            "Use the current split expressions when the macroscale model can represent bare and covered pathways separately.",
        ],
    }


def fit_theta_h(h: np.ndarray, theta: np.ndarray, theta_init: np.ndarray) -> dict[str, Any]:
    """Fit theta = 1 - exp(-a*h^b) by log-linearizing."""

    mask = (
        np.isfinite(h)
        & np.isfinite(theta)
        & (h > 0.0)
        & (theta > 1.0e-8)
        & (theta < 0.98)
        & (theta_init < 1.0e-12)
    )
    if np.count_nonzero(mask) < 3:
        mask = np.isfinite(h) & np.isfinite(theta) & (h > 0.0) & (theta > 1.0e-8) & (theta < 0.98)
    if np.count_nonzero(mask) < 3:
        return {
            "expression": "theta = 1 - exp(-a_theta*h_I2^b_theta)",
            "a_theta_m_neg_b": 0.0,
            "b_theta": 1.0,
            "r2": None,
            "fit_rows": int(np.count_nonzero(mask)),
            "status": "insufficient nonzero theta/h data; keep as diagnostic",
        }

    x = np.log(h[mask])
    y = np.log(-np.log(1.0 - np.clip(theta[mask], 1.0e-12, 1.0 - 1.0e-12)))
    b_theta, log_a = np.polyfit(x, y, 1)
    a_theta = float(np.exp(log_a))
    pred = 1.0 - np.exp(-a_theta * h[mask] ** b_theta)
    return {
        "expression": "theta = 1 - exp(-a_theta*h_I2^b_theta)",
        "a_theta_m_neg_b": a_theta,
        "b_theta": float(b_theta),
        "r2": r2_score(theta[mask], pred),
        "fit_rows": int(np.count_nonzero(mask)),
        "status": "fit",
    }


def fit_film_factor(rfilm: np.ndarray, factor: np.ndarray, params: dict[str, Any]) -> dict[str, Any]:
    """Fit film_kin_factor = 1/(1 + g_eff*Rfilm_local)."""

    mask = np.isfinite(rfilm) & np.isfinite(factor) & (factor > 0.0) & (factor <= 1.05)
    if np.count_nonzero(mask) < 2:
        g_eff = float(params["electrochemistry"]["g_I_S_m2"])
        rmse = 0.0
    else:
        r = rfilm[mask]
        y = factor[mask]

        def objective(g_eff: float) -> float:
            pred = 1.0 / (1.0 + g_eff * r)
            return float(np.mean((pred - y) ** 2))

        result = minimize_scalar(objective, bounds=(0.0, 1.0e8), method="bounded")
        g_eff = float(result.x)
        rmse = float(np.sqrt(objective(g_eff)))

    return {
        "expression": "film_kin_factor_eff = 1/(1 + g_eff*Rfilm_local)",
        "g_eff_S_m2": g_eff,
        "rmse": rmse,
        "fit_rows": int(np.count_nonzero(mask)),
    }


def fit_rate_constant(x: np.ndarray, rate: np.ndarray, fallback: float) -> dict[str, Any]:
    """Fit rate = k*x through the origin."""

    mask = np.isfinite(x) & np.isfinite(rate) & (np.abs(x) > 1.0e-16)
    if np.count_nonzero(mask) == 0:
        return {"k": float(fallback), "rmse": 0.0, "fit_rows": 0}
    x_fit = x[mask]
    rate_fit = rate[mask]
    denom = float(np.dot(x_fit, x_fit))
    k = float(np.dot(x_fit, rate_fit) / denom) if denom > 0.0 else float(fallback)
    pred = k * x_fit
    rmse = float(np.sqrt(np.mean((pred - rate_fit) ** 2)))
    return {"k": k, "rmse": rmse, "fit_rows": int(np.count_nonzero(mask))}


def current_split_metrics(rows: list[dict[str, Any]], g_eff: float, params: dict[str, Any]) -> dict[str, Any]:
    """Evaluate the analytic current-split closure against the raw database."""

    j0_bare = params["electrochemistry"]["j0_bare_A_m2"]
    j0_cov = params["electrochemistry"]["j0_cov_A_m2"]
    errors_bare = []
    errors_cov = []
    for row in rows:
        theta = float(row["theta"])
        rfilm = float(row["Rfilm_local"])
        cov_factor = 1.0 / (1.0 + g_eff * rfilm)
        denom = (1.0 - theta) * j0_bare + theta * j0_cov * cov_factor
        if abs(denom) < 1.0e-30:
            continue
        pred_bare = (1.0 - theta) * j0_bare / denom
        pred_cov = theta * j0_cov * cov_factor / denom
        errors_bare.append(pred_bare - float(row["frac_bare_current"]))
        errors_cov.append(pred_cov - float(row["frac_cov_current"]))
    return {
        "frac_bare_expression": "((1-theta)*j0_bare)/((1-theta)*j0_bare + theta*j0_cov*film_kin_factor_eff)",
        "frac_cov_expression": "(theta*j0_cov*film_kin_factor_eff)/((1-theta)*j0_bare + theta*j0_cov*film_kin_factor_eff)",
        "j0_bare_A_m2": j0_bare,
        "j0_cov_A_m2": j0_cov,
        "rmse_frac_bare": rmse(errors_bare),
        "rmse_frac_cov": rmse(errors_cov),
        "fit_rows": len(errors_bare),
    }


def eps_s_pos_from_h(h_i2_m: float, params: dict[str, Any]) -> float:
    """Map local film thickness to a positive-solid volume fraction in the shell."""

    geom = params["geometry"]
    r_f = float(geom["R_f_m"])
    r_out = float(geom["R_out_m"])
    h_pos = max(float(h_i2_m), 0.0)
    film_area = np.pi * ((r_f + h_pos) ** 2 - r_f**2)
    shell_area = np.pi * (r_out**2 - r_f**2)
    return float(film_area / shell_area)


def cumulative_trapezoid(time_s: list[float], values: list[float]) -> list[float]:
    """Cumulative trapezoid integral without requiring scipy.integrate helper."""

    out = [0.0]
    for i in range(1, len(time_s)):
        dt = float(time_s[i]) - float(time_s[i - 1])
        out.append(out[-1] + 0.5 * dt * (float(values[i]) + float(values[i - 1])))
    return out


def safe_ratio(num: float, denom: float) -> float:
    if abs(float(denom)) < 1.0e-300:
        return 0.0
    return float(num) / float(denom)


def arr(rows: list[dict[str, Any]], key: str) -> np.ndarray:
    return np.array([float(row[key]) for row in rows], dtype=float)


def rmse(values: list[float]) -> float | None:
    if not values:
        return None
    data = np.array(values, dtype=float)
    return float(np.sqrt(np.mean(data**2)))


def r2_score(y_true: np.ndarray, y_pred: np.ndarray) -> float | None:
    ss_res = float(np.sum((y_true - y_pred) ** 2))
    ss_tot = float(np.sum((y_true - np.mean(y_true)) ** 2))
    if ss_tot <= 0.0:
        return None
    return 1.0 - ss_res / ss_tot


def write_csv(rows: list[dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError("No closure scan rows to write")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_json(data: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)


if __name__ == "__main__":
    main()
