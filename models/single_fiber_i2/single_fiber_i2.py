"""Single-fiber I2 coverage / precipitation / film-resistance model.

The model is intentionally independent of COMSOL. It supplies local closure
quantities for a macroscopic porous-media model.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

try:
    import yaml
except ImportError:  # pragma: no cover - dependency guard
    yaml = None


PARAMS_PATH = Path(__file__).with_name("params.yaml")


@dataclass(frozen=True)
class Grid:
    """Finite-volume radial grid for a cylinder per unit fiber length."""

    centers: np.ndarray
    edges: np.ndarray
    volumes: np.ndarray
    face_areas: np.ndarray


def load_params(path: str | Path = PARAMS_PATH) -> dict[str, Any]:
    """Load model parameters from YAML."""

    if yaml is None:
        raise RuntimeError("PyYAML is required to read params.yaml")
    with Path(path).open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def smoothplus(x: np.ndarray | float, eps: float) -> np.ndarray | float:
    """Differentiable positive-part approximation with concentration units."""

    return 0.5 * (np.asarray(x) + np.sqrt(np.asarray(x) ** 2 + eps**2))


def beta_i2(cI_m: np.ndarray | float, params: dict[str, Any]) -> np.ndarray | float:
    """Fast complexation factor beta_I2 = 1 + K_I2_I*cI_m + K_I2_Br*cBr."""

    comp = params["complexation"]
    trans = params["transport"]
    return (
        1.0
        + comp["K_I2_I_m3_mol"] * np.asarray(cI_m)
        + comp["K_I2_Br_m3_mol"] * trans["cBr_support_mol_m3"]
    )


def free_i2(cI2_tot: np.ndarray | float, cI_m: np.ndarray | float, params: dict[str, Any]):
    """Convert total iodine to free molecular iodine via fast complexation."""

    return np.asarray(cI2_tot) / beta_i2(cI_m, params)


def make_grid(params: dict[str, Any]) -> Grid:
    """Build a uniform radial finite-volume grid."""

    geom = params["geometry"]
    r_edges = np.linspace(geom["R_f_m"], geom["R_out_m"], int(geom["n_cells"]) + 1)
    r_centers = 0.5 * (r_edges[:-1] + r_edges[1:])
    volumes = np.pi * (r_edges[1:] ** 2 - r_edges[:-1] ** 2)
    face_areas = 2.0 * np.pi * r_edges
    return Grid(r_centers, r_edges, volumes, face_areas)


def bv_current_shape(eta_v: float, params: dict[str, Any]) -> float:
    """Dimensionless Butler-Volmer current shape."""

    ec = params["electrochemistry"]
    f_rt = ec["F_C_mol"] / (ec["R_J_mol_K"] * ec["T_K"])
    return float(
        np.exp(ec["alpha_a"] * f_rt * eta_v)
        - np.exp(-ec["alpha_c"] * f_rt * eta_v)
    )


def theta_geo(N_i2: float, eps_s_equiv: float, k_geo: float) -> float:
    """Diagnostic geometric coverage relation, not enforced in time integration."""

    N_pos = max(float(N_i2), 0.0)
    eps_pos = max(float(eps_s_equiv), 0.0)
    return float(1.0 - np.exp(-k_geo * N_pos ** (1.0 / 3.0) * eps_pos ** (2.0 / 3.0)))


def compute_site_activity_multiplier(params: dict[str, Any]) -> float:
    """Return the diagnostic molecular-prior site activity multiplier.

    The multiplier is disabled by default. When enabled, it evaluates
    1 + sum_i f_i * (S_i - 1), where f_i is a site fraction and S_i is a
    bounded molecular-prior preference factor. The current single-fiber model
    has no explicit nucleation-site-density state, so this value is reported as
    a diagnostic and is not applied to the ODEs.
    """

    prior = params.get("molecular_prior", {}) or {}
    if not bool(prior.get("enabled", False)):
        return 1.0
    factors = prior.get("site_preference_factors", {}) or {}
    fractions = prior.get("site_fractions", {}) or {}
    multiplier = 1.0
    for key, fraction in fractions.items():
        preference = factors.get(key, 1.0)
        multiplier += float(fraction) * (float(preference) - 1.0)
    return float(max(multiplier, 0.0))


def film_resistance(h_i2_m: float, params: dict[str, Any]) -> float:
    """Local I2-film resistance Rfilm_local = h_I2 / sigma_I2 [ohm m2]."""

    sigma = max(float(params["film"]["sigma_I2_S_m"]), 1e-30)
    return max(float(h_i2_m), 0.0) / sigma


def covered_local_current(eta_v: float, rfilm_ohm_m2: float, params: dict[str, Any]) -> float:
    """Solve covered-path current density without theta multiplier [A/m2]."""

    ec = params["electrochemistry"]
    j0 = ec["j0_cov_A_m2"]
    mode = str(ec.get("covered_mode", "linearized")).lower()

    if mode == "linearized":
        denom = 1.0 + max(ec["g_I_S_m2"] * rfilm_ohm_m2, 0.0)
        return j0 * bv_current_shape(eta_v, params) / denom

    if mode != "implicit":
        raise ValueError(f"Unknown covered_mode: {mode}")

    def residual(j_local: float) -> float:
        return j_local - j0 * bv_current_shape(eta_v - j_local * rfilm_ohm_m2, params)

    scale = max(abs(j0 * bv_current_shape(eta_v, params)), j0, 1.0)
    lo, hi = -10.0 * scale, 10.0 * scale
    for _ in range(12):
        if residual(lo) * residual(hi) <= 0.0:
            return float(brentq(residual, lo, hi, xtol=1e-10, rtol=1e-10, maxiter=100))
        lo *= 2.0
        hi *= 2.0
    raise RuntimeError("Could not bracket covered-path current root")


def current_split(
    eta_v: float, theta: float, h_i2_m: float, params: dict[str, Any]
) -> dict[str, float]:
    """Return bare, covered, and total current density at a trial overpotential."""

    th = float(np.clip(theta, 0.0, 1.0))
    rfilm = film_resistance(h_i2_m, params)
    ec = params["electrochemistry"]
    j_bare = (1.0 - th) * ec["j0_bare_A_m2"] * bv_current_shape(eta_v, params)
    j_cov_local = covered_local_current(eta_v, rfilm, params)
    j_cov = th * j_cov_local
    return {
        "j_bare": float(j_bare),
        "j_cov": float(j_cov),
        "j_cov_local": float(j_cov_local),
        "j_total": float(j_bare + j_cov),
        "Rfilm_local": float(rfilm),
    }


def solve_eta_for_current(i_app_fiber: float, theta: float, h_i2_m: float, params: dict[str, Any]):
    """Find eta_I such that j_total(eta_I, theta, h_I2) = i_app_fiber."""

    half_width = float(params["electrochemistry"].get("eta_bracket_V", 1.5))

    def residual(eta_v: float) -> float:
        return current_split(eta_v, theta, h_i2_m, params)["j_total"] - i_app_fiber

    lo, hi = -half_width, half_width
    for _ in range(10):
        if residual(lo) * residual(hi) <= 0.0:
            eta = float(brentq(residual, lo, hi, xtol=1e-11, rtol=1e-11, maxiter=100))
            split = current_split(eta, theta, h_i2_m, params)
            split["eta_I"] = eta
            return split
        lo *= 1.5
        hi *= 1.5
    raise RuntimeError("Could not bracket eta_I current root")


def surface_rates(cI_surf: float, cI2_tot_surf: float, theta: float, params: dict[str, Any]):
    """Compute free-I2 supersaturation and precipitation/dissolution rates."""

    comp = params["complexation"]
    pp = params["precipitation"]
    c_free = float(free_i2(cI2_tot_surf, cI_surf, params))
    supersat = float(smoothplus(c_free - comp["cI2_sat_mol_m3"], pp["smoothplus_eps_mol_m3"]))
    undersat = float(smoothplus(comp["cI2_sat_mol_m3"] - c_free, pp["smoothplus_eps_mol_m3"]))
    r_precip = pp["k_precip_sf_m_s"] * supersat
    r_diss = pp["k_diss_sf_m_s"] * float(np.clip(theta, 0.0, 1.0)) * undersat
    return {
        "cI2_surf_free": c_free,
        "supersaturation": supersat,
        "undersaturation": undersat,
        "precipitation_rate": float(r_precip),
        "dissolution_rate": float(r_diss),
    }


def initial_state(params: dict[str, Any]) -> np.ndarray:
    """Initial concentrations are set to bulk values throughout the layer."""

    n = int(params["geometry"]["n_cells"])
    trans = params["transport"]
    film = params["film"]
    cov = params["coverage"]
    c_i = np.full(n, trans["cI_bulk_mol_m3"], dtype=float)
    c_i2 = np.full(n, trans["cI2_tot_bulk_mol_m3"], dtype=float)
    return np.r_[c_i, c_i2, cov["theta_initial"], film["h_initial_m"]]


def rhs(t_s: float, y: np.ndarray, i_app_fiber: float, params: dict[str, Any]) -> np.ndarray:
    """Method-of-lines right-hand side for radial diffusion and surface states."""

    del t_s
    grid = make_grid(params)
    n = len(grid.centers)
    trans = params["transport"]
    film = params["film"]
    cov = params["coverage"]
    ec = params["electrochemistry"]

    c_i = np.maximum(y[:n], 0.0)
    c_i2 = np.maximum(y[n : 2 * n], 0.0)
    theta = float(np.clip(y[2 * n], 0.0, 1.0))
    h_i2 = float(np.clip(y[2 * n + 1], 0.0, film["h_max_m"]))

    current = solve_eta_for_current(i_app_fiber, theta, h_i2, params)
    rates = surface_rates(c_i[0], c_i2[0], theta, params)

    n_i2_echem = current["j_total"] / (2.0 * ec["F_C_mol"])
    n_i_echem = -current["j_total"] / ec["F_C_mol"]
    n_i2_solid = -rates["precipitation_rate"] + rates["dissolution_rate"]
    n_i2_surface = n_i2_echem + n_i2_solid
    n_i_surface = n_i_echem

    dc_i = _diffusion_rhs(c_i, trans["D_I_m2_s"], trans["cI_bulk_mol_m3"], n_i_surface, grid)
    dc_i2 = _diffusion_rhs(
        c_i2, trans["D_I2_tot_m2_s"], trans["cI2_tot_bulk_mol_m3"], n_i2_surface, grid
    )

    c_sat = params["complexation"]["cI2_sat_mol_m3"]
    dtheta = (
        cov["k_theta_grow_m3_mol_s"] * rates["supersaturation"] * (1.0 - theta)
        - cov["k_theta_diss_m3_mol_s"] * rates["undersaturation"] * theta
    )
    if theta <= 0.0 and dtheta < 0.0:
        dtheta = 0.0
    if theta >= 1.0 and dtheta > 0.0:
        dtheta = 0.0

    dh = film["Vm_I2_m3_mol"] * (rates["precipitation_rate"] - rates["dissolution_rate"])
    if h_i2 <= 0.0 and dh < 0.0:
        dh = 0.0
    if h_i2 >= film["h_max_m"] and dh > 0.0:
        dh = 0.0

    return np.r_[dc_i, dc_i2, dtheta, dh]


def _diffusion_rhs(c: np.ndarray, diff: float, c_bulk: float, n_surface: float, grid: Grid) -> np.ndarray:
    """Cylindrical finite-volume diffusion with inner flux and outer Dirichlet value."""

    n = len(c)
    face_flux = np.zeros(n + 1, dtype=float)
    face_flux[0] = n_surface
    for face in range(1, n):
        dr = grid.centers[face] - grid.centers[face - 1]
        face_flux[face] = -diff * (c[face] - c[face - 1]) / dr
    dr_outer = grid.edges[-1] - grid.centers[-1]
    face_flux[n] = -diff * (c_bulk - c[-1]) / dr_outer

    dc = np.empty(n, dtype=float)
    for i in range(n):
        dc[i] = -(
            grid.face_areas[i + 1] * face_flux[i + 1]
            - grid.face_areas[i] * face_flux[i]
        ) / grid.volumes[i]
    return dc


def simulate_segment(
    params: dict[str, Any],
    i_app_fiber: float,
    t_span_s: tuple[float, float],
    y0: np.ndarray | None = None,
    t_eval: np.ndarray | None = None,
):
    """Integrate one constant-current segment."""

    if y0 is None:
        y0 = initial_state(params)
    if t_eval is None:
        t_eval = np.linspace(t_span_s[0], t_span_s[1], 101)
    return solve_ivp(
        lambda t, y: rhs(t, y, i_app_fiber, params),
        t_span_s,
        y0,
        method="BDF",
        t_eval=t_eval,
        max_step=params["time"]["max_step_s"],
        rtol=1e-6,
        atol=1e-9,
    )


def diagnostics(t_s: np.ndarray, y: np.ndarray, i_app_fiber: float, params: dict[str, Any]):
    """Build output table columns requested by the closure model spec."""

    n = int(params["geometry"]["n_cells"])
    rows: list[dict[str, float]] = []
    prior = params.get("molecular_prior", {}) or {}
    site_activity = compute_site_activity_multiplier(params)
    prior_enabled = bool(prior.get("enabled", False))
    prior_mapping = str(prior.get("mapping", "none"))
    c_bulk_free = float(
        free_i2(
            params["transport"]["cI2_tot_bulk_mol_m3"],
            params["transport"]["cI_bulk_mol_m3"],
            params,
        )
    )
    for k, t_val in enumerate(t_s):
        state = y[:, k] if y.ndim == 2 else y[k, :]
        c_i = max(float(state[0]), 0.0)
        c_i2 = max(float(state[n]), 0.0)
        theta_val = float(np.clip(state[2 * n], 0.0, 1.0))
        h_val = max(float(state[2 * n + 1]), 0.0)
        current = solve_eta_for_current(i_app_fiber, theta_val, h_val, params)
        rates = surface_rates(c_i, c_i2, theta_val, params)
        film_factor = current["j_cov_local"] / (
            params["electrochemistry"]["j0_cov_A_m2"] * bv_current_shape(current["eta_I"], params)
            + 1e-300
        )
        rows.append(
            {
                "time_s": float(t_val),
                "eta_I": current["eta_I"],
                "j_total": current["j_total"],
                "j_bare": current["j_bare"],
                "j_cov": current["j_cov"],
                "theta": theta_val,
                "h_I2": h_val,
                "Rfilm_local": current["Rfilm_local"],
                "cI2_surf_free": rates["cI2_surf_free"],
                "cI2_bulk_free": c_bulk_free,
                "supersaturation": rates["supersaturation"],
                "dissolution_rate": rates["dissolution_rate"],
                "precipitation_rate": rates["precipitation_rate"],
                "film_kin_factor": float(film_factor),
                "k_precip_eff": params["precipitation"]["k_precip_sf_m_s"] * (1.0 - theta_val),
                "k_diss_eff": params["precipitation"]["k_diss_sf_m_s"] * theta_val,
                "theta_geo": theta_geo(
                    h_val / max(params["film"]["Vm_I2_m3_mol"], 1e-300),
                    params["coverage"]["eps_s_equiv"],
                    params["coverage"]["k_geo"],
                ),
                "site_activity_multiplier": site_activity,
                "molecular_prior_enabled": prior_enabled,
                "molecular_prior_mapping": prior_mapping,
            }
        )
    return rows


def simulate_charge_discharge(params: dict[str, Any] | None = None):
    """Run the default charge then discharge demonstration."""

    if params is None:
        params = load_params()
    dt = params["time"]["dt_output_s"]
    t_charge_end = params["time"]["charge_time_s"]
    t_discharge_end = t_charge_end + params["time"]["discharge_time_s"]
    t_charge = np.arange(0.0, t_charge_end + 0.5 * dt, dt)
    sol_charge = simulate_segment(params, params["current"]["i_charge_A_m2"], (0.0, t_charge_end), t_eval=t_charge)
    if not sol_charge.success:
        raise RuntimeError(sol_charge.message)

    t_discharge = np.arange(t_charge_end + dt, t_discharge_end + 0.5 * dt, dt)
    sol_discharge = simulate_segment(
        params,
        params["current"]["i_discharge_A_m2"],
        (t_charge_end, t_discharge_end),
        y0=sol_charge.y[:, -1],
        t_eval=t_discharge,
    )
    if not sol_discharge.success:
        raise RuntimeError(sol_discharge.message)

    rows = diagnostics(sol_charge.t, sol_charge.y, params["current"]["i_charge_A_m2"], params)
    rows.extend(diagnostics(sol_discharge.t, sol_discharge.y, params["current"]["i_discharge_A_m2"], params))
    return rows, sol_charge, sol_discharge
