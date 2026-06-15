"""Export COMSOL-ready closure expressions from fitted single-fiber scans."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from fit_closures import FITS_PATH, fit_closure_models, run_scan, write_csv, write_json
from fit_closures import DATABASE_PATH
from single_fiber_i2 import load_params


ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "outputs" / "single_fiber_i2"
REPORT_PATH = OUT_DIR / "comsol_closure_expressions.md"


def main() -> None:
    params = load_params()
    fits = load_or_create_fits(params)
    report = build_report(fits, params)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(report, encoding="utf-8")
    print(f"Wrote {REPORT_PATH}")


def load_or_create_fits(params: dict[str, Any]) -> dict[str, Any]:
    if FITS_PATH.exists():
        return json.loads(FITS_PATH.read_text(encoding="utf-8"))
    rows = run_scan(params)
    write_csv(rows, DATABASE_PATH)
    fits = fit_closure_models(rows, params)
    write_json(fits, FITS_PATH)
    return fits


def build_report(fits: dict[str, Any], params: dict[str, Any]) -> str:
    theta = fits["theta_model"]
    film = fits["film_model"]
    precip = fits["precipitation_model"]
    diss = fits["dissolution_model"]
    split = fits["current_split_model"]
    rec = fits["recommended_parameters"]

    a_theta = theta["a_theta_m_neg_b"]
    b_theta = theta["b_theta"]
    g_eff = film["g_eff_S_m2"]
    k_precip = precip["k_precip_i2_m_s"]
    k_diss = diss["k_diss_surf_m_s"]
    sigma = rec["sigma_I2_S_m"]
    j0_bare = split["j0_bare_A_m2"]
    j0_cov = split["j0_cov_A_m2"]
    smooth_eps = params["precipitation"]["smoothplus_eps_mol_m3"]

    lines = [
        "# COMSOL Closure Expressions from single_fiber_i2",
        "",
        "This report converts the standalone single-fiber scan into algebraic closures for the macroscopic 2D COMSOL model. Units are SI unless noted.",
        "",
        "## Recommended Parameters",
        "",
        "| Parameter | Value | Unit | Meaning |",
        "|---|---:|---|---|",
        f"| `a_theta_i2` | `{a_theta:.8e}` | `m^(-b_theta_i2)` | theta(h) prefactor |",
        f"| `b_theta_i2` | `{b_theta:.8g}` | `1` | theta(h) exponent |",
        f"| `g_eff_i2` | `{g_eff:.8e}` | `S/m^2` | effective covered-film kinetic factor coefficient |",
        f"| `sigma_I2` | `{sigma:.8e}` | `S/m` | local I2 film conductivity |",
        f"| `k_precip_i2` | `{k_precip:.8e}` | `m/s` | precipitation coefficient |",
        f"| `k_diss_surf` | `{k_diss:.8e}` | `m/s` | dissolution coefficient multiplying theta |",
        f"| `j0_bare_i2` | `{j0_bare:.8e}` | `A/m^2` | bare-path exchange current scale |",
        f"| `j0_cov_i2` | `{j0_cov:.8e}` | `A/m^2` | covered-path exchange current scale |",
        f"| `cI2_smooth` | `{smooth_eps:.8e}` | `mol/m^3` | smooth positive-part regularization |",
        "",
        "## COMSOL Variables: Direct Copy Candidates",
        "",
        "Use these expressions when the macroscopic model carries `h_I2`, `cI_m`, `cI2_tot`, and the local supporting-ion concentration or constant `cBr_support`.",
        "",
        "```text",
        "beta_I2 = 1 + K_I2_I*cI_m + K_I2_Br*cBr_support",
        "cI2_free = cI2_tot/beta_I2",
        "cI2_supersat = 0.5*((cI2_free-cI2_sat)+sqrt((cI2_free-cI2_sat)^2+cI2_smooth^2))",
        "cI2_undersat = 0.5*((cI2_sat-cI2_free)+sqrt((cI2_sat-cI2_free)^2+cI2_smooth^2))",
        "Rfilm_local = max(h_I2,0)/sigma_I2",
        "theta_i2_raw = 1 - exp(-a_theta_i2*max(h_I2,0)^b_theta_i2)",
        "theta_i2 = min(1,max(0,theta_i2_raw))",
        "film_kin_factor_i2 = 1/(1 + g_eff_i2*Rfilm_local)",
        "r_precip_i2 = k_precip_i2*cI2_supersat",
        "r_diss_i2 = k_diss_surf*theta_i2*cI2_undersat",
        "```",
        "",
        "If COMSOL does not accept `max()`/`min()` in the target field, replace them with COMSOL's smoothed step or clamp operators used elsewhere in the model.",
        "",
        "## Recommended Replacement for Av_try2_eff",
        "",
        "If the existing macro model has only one iodine BV pathway and uses `Av_try2_eff` as a scalar active-area multiplier, use this reduced expression:",
        "",
        "```text",
        "Av_try2_eff = av0_i2*((1-theta_i2) + theta_i2*(j0_cov_i2/j0_bare_i2)*film_kin_factor_i2)",
        "```",
        "",
        "This preserves the bare/covered parallel-path current to first order when the base macro BV expression uses `j0_bare_i2`.",
        "",
        "If the macro model can represent two pathways explicitly, prefer the parallel current form instead of folding everything into `Av_try2_eff`:",
        "",
        "```text",
        "j_bare_i2 = (1-theta_i2)*j0_bare_i2*BV_i2(eta_I)",
        "j_cov_i2 = theta_i2*j0_cov_i2*film_kin_factor_i2*BV_i2(eta_I)",
        "j_i2_total = j_bare_i2 + j_cov_i2",
        "```",
        "",
        "## Current Split Diagnostics",
        "",
        "These are useful for plotting and checking the macro model, but they are not required if the two-pathway current is implemented directly.",
        "",
        "```text",
        "frac_bare_current = ((1-theta_i2)*j0_bare_i2)/((1-theta_i2)*j0_bare_i2 + theta_i2*j0_cov_i2*film_kin_factor_i2)",
        "frac_cov_current = (theta_i2*j0_cov_i2*film_kin_factor_i2)/((1-theta_i2)*j0_bare_i2 + theta_i2*j0_cov_i2*film_kin_factor_i2)",
        "```",
        "",
        "## Fit Quality Summary",
        "",
        f"- Theta model: `{theta['expression']}`, status `{theta['status']}`, fit rows `{theta['fit_rows']}`, R2 `{theta['r2']}`.",
        f"- Film model: `{film['expression']}`, fit rows `{film['fit_rows']}`, RMSE `{film['rmse']}`.",
        f"- Precipitation model: `{precip['expression']}`, fit rows `{precip['fit_rows']}`, RMSE `{precip['rmse_mol_m2_s']}` mol/m2/s.",
        f"- Dissolution model: `{diss['expression']}`, fit rows `{diss['fit_rows']}`, RMSE `{diss['rmse_mol_m2_s']}` mol/m2/s.",
        f"- Current split RMSE: bare `{split['rmse_frac_bare']}`, covered `{split['rmse_frac_cov']}`.",
        "",
        "## Diagnostic Only",
        "",
        "- `theta_geo = 1 - exp(-k_geo*N_i2^(1/3)*eps_s_equiv^(2/3))` is a geometric diagnostic unless the macro model has a calibrated `N_i2` or `eps_s_pos` state.",
        "- The scalar `Av_try2_eff` expression is a compatibility bridge. It is less informative than explicit bare/covered parallel currents.",
        "- The fitted `theta_i2` expression should not replace a macro coverage transport equation if that equation already tracks history-dependent nucleation/growth.",
        "",
        f"Source database: `{fits['source_database']}`",
    ]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
