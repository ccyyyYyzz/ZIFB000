#!/usr/bin/env python
"""Build R582 Supplementary Figure S6 from frozen registered evidence.

The calculation reproduces the registered reduced observation-layer fit and
then evaluates the constant-voltage reduced-accessibility--coefficient
relation.  Here R_theta = 1 - theta is a calibration-controlled factor; it is
not the native remaining-area fraction A_bare/A0 = R_theta*T_pore.  The result
is an identifiability diagnostic, not a morphology inference or an independent
positive-electrode validation.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from r582_si_figure_tools import (
    CARMINE,
    INK,
    LIGHT_GREY,
    MID_GREY,
    NAVY,
    PALE_GREY,
    TEAL,
    TERMES_PATHS,
    WHITE,
    audit_text,
    configure_font,
    export_deterministic,
    panel_label,
    sha256,
    style_axis,
)


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
FIGURE_DIR = PROJECT / "manuscript" / "figures_R582"
FIGURE_DIR.mkdir(parents=True, exist_ok=True)
STEM = "SIFig_R582_S6_voltage_degeneracy"
WIDTH_MM = 180.0
HEIGHT_MM = 92.0
FAMILY = configure_font(STEM)

INPUTS = {
    "selected_full_cell_voltage": HERE / "inputs" / "representative_vq_profiles_for_article.csv",
    "registered_accessibility_trajectory": HERE / "inputs" / "R532_voltage_closure.csv",
    "registered_degeneracy_points": HERE / "inputs" / "R538_coverage_tafel_degeneracy.csv",
    "registered_fit_summary": HERE / "inputs" / "R538_reanchor_summary.csv",
}
EXPECTED_SHA256 = {
    "selected_full_cell_voltage": "150AFD09C0AE8FEE58A8DFE1CCC412378CB1F7893075F54BDFFD8DE0AED3D1F1",
    "registered_accessibility_trajectory": "26BC169951755169F4AF198E3CBD0CFEAB8F2E81542AE0658519F833A2D5F5B1",
    "registered_degeneracy_points": "023A2EDD74DF449D5F30CA808A97C92A45A721A50B24AE51BF7A78733563C605",
    "registered_fit_summary": "DD783E5B5FE7CC6A8B795904610BC5BA320041F16066C827ED6D9C325DA513B7",
}
REGISTERED_SOURCES = {
    "selected_full_cell_voltage": "manuscript/source_data/Fig_R538_voltage_reanchor/representative_vq_profiles_for_article.csv",
    "registered_accessibility_trajectory": "manuscript/source_data/Fig_R538_voltage_reanchor/R532_voltage_closure.csv",
    "registered_degeneracy_points": "manuscript/source_data/Fig_R538_voltage_reanchor/R538_coverage_tafel_degeneracy.csv",
    "registered_fit_summary": "manuscript/source_data/Fig_R538_voltage_reanchor/R538_reanchor_summary.csv",
}

FIT_TABLE = HERE / "R582_SIFig_S6_voltage_fit.csv"
CURVE_TABLE = HERE / "R582_SIFig_S6_degeneracy_curve.csv"
POINT_TABLE = HERE / "R582_SIFig_S6_degeneracy_points.csv"
PARAMETER_TABLE = HERE / "R582_SIFig_S6_parameter_table.csv"
INPUT_MANIFEST = HERE / "R582_SIFig_S6_input_manifest.csv"
RENDER_MANIFEST = HERE / "R582_SIFig_S6_render_manifest.json"


def rel(path: Path) -> str:
    return path.resolve().relative_to(PROJECT.resolve()).as_posix()


def require_columns(frame: pd.DataFrame, columns: list[str], label: str) -> None:
    missing = sorted(set(columns) - set(frame.columns))
    if missing:
        raise ValueError(f"{label} missing columns: {missing}")


def verify_inputs() -> None:
    rows = []
    uses = {
        "selected_full_cell_voltage": "selected pristine full-cell charge trace",
        "registered_accessibility_trajectory": (
            "historical A_bare_comsol column used as the reduced calibration-controlled R_theta(Q) factor"
        ),
        "registered_degeneracy_points": "registered parameter-pair cross-checks",
        "registered_fit_summary": "registered fit and voltage-contribution cross-checks",
    }
    for key, path in INPUTS.items():
        if not path.is_file():
            raise FileNotFoundError(path)
        observed = sha256(path)
        if observed != EXPECTED_SHA256[key]:
            raise ValueError(f"Frozen input hash mismatch for {key}: {observed}")
        rows.append(
            {
                "source_key": key,
                "frozen_copy": rel(path),
                "registered_source": REGISTERED_SOURCES[key],
                "size_bytes": path.stat().st_size,
                "sha256": observed,
                "used_for": uses[key],
                "immutable_registered_input": True,
            }
        )
    pd.DataFrame(rows).to_csv(INPUT_MANIFEST, index=False, lineterminator="\n")


def summary_lookup(summary: pd.DataFrame, quantity: str) -> float:
    row = summary.loc[summary["quantity"].eq(quantity), "value"]
    if len(row) != 1:
        raise ValueError(f"Expected one summary value for {quantity}")
    return float(row.iloc[0])


def prepare_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, dict]:
    verify_inputs()
    raw = pd.read_csv(INPUTS["selected_full_cell_voltage"], low_memory=False)
    closure = pd.read_csv(INPUTS["registered_accessibility_trajectory"])
    registered_points = pd.read_csv(INPUTS["registered_degeneracy_points"])
    summary = pd.read_csv(INPUTS["registered_fit_summary"])
    require_columns(
        raw,
        [
            "display_sample",
            "display_condition",
            "FileName",
            "pair_index",
            "direction",
            "segment_capacity_mAh",
            "voltage_v",
            "figure",
        ],
        "full-cell voltage source",
    )
    require_columns(
        closure,
        ["q_mAh_cm2", "A_bare_comsol"],
        "historical reduced-factor trajectory",
    )
    require_columns(
        registered_points,
        ["theta_end", "A_bare_end", "bT_needed_V", "tafel_mV_dec", "physical"],
        "degeneracy source",
    )
    require_columns(summary, ["quantity", "value"], "fit summary")

    selected = raw.loc[
        raw["figure"].eq("01_baseline_standard_controls")
        & raw["display_sample"].eq("Pristine")
        & raw["direction"].eq("charge")
    ].copy()
    if len(selected) != 90 or selected["FileName"].nunique() != 1:
        raise ValueError("Selected voltage trace must contain 90 points from one physical file")
    if selected["pair_index"].astype(int).unique().tolist() != [20]:
        raise ValueError("Unexpected selected charge-cycle identity")
    selected["Q_mAh_cm2"] = selected["segment_capacity_mAh"].astype(float) / 4.0
    selected = selected.sort_values("Q_mAh_cm2").reset_index(drop=True)
    q = selected["Q_mAh_cm2"].to_numpy(float)
    voltage = selected["voltage_v"].to_numpy(float)
    peak_index = int(np.argmax(voltage))
    q_peak = float(q[peak_index])
    fit_mask = (q >= 2.0) & (q <= q_peak)
    q_fit = q[fit_mask]
    v_fit_data = voltage[fit_mask]

    if len(closure) != 1081 or not np.all(np.diff(closure["q_mAh_cm2"].to_numpy(float)) > 0):
        raise ValueError("Registered accessibility trajectory must have 1081 strictly ordered rows")
    # The frozen historical column name is retained byte-for-byte upstream.
    # Its R582 role is the reduced calibration-controlled factor R_theta(Q),
    # not the native remaining area A_bare/A0 = R_theta*T_pore.
    r_theta_fit = np.interp(q_fit, closure["q_mAh_cm2"], closure["A_bare_comsol"])
    design = np.column_stack([np.ones_like(q_fit), q_fit, np.log(1.0 / r_theta_fit)])
    coefficients, *_ = np.linalg.lstsq(design, v_fit_data, rcond=None)
    c0, c1, b_eff = [float(value) for value in coefficients]
    fitted = design @ coefficients
    residual_mV = 1000.0 * (fitted - v_fit_data)
    rmse_mV = float(np.sqrt(np.mean(residual_mV**2)))
    access_contribution_mV = float(
        1000.0
        * b_eff
        * (np.log(1.0 / r_theta_fit[-1]) - np.log(1.0 / r_theta_fit[0]))
    )
    drift_contribution_mV = float(1000.0 * c1 * (q_fit[-1] - q_fit[0]))

    expected = {
        "reanchored_c0": c0,
        "reanchored_c1": c1,
        "reanchored_bT": b_eff,
        "R_access_mV": access_contribution_mV,
        "R_drift_mV": drift_contribution_mV,
        "rmse_mV": rmse_mV,
        "Qpeak": q_peak,
    }
    for quantity, observed in expected.items():
        registered = summary_lookup(summary, quantity)
        if not math.isclose(observed, registered, rel_tol=0.0, abs_tol=2e-9):
            raise ValueError(f"Registered fit mismatch for {quantity}: {observed} versus {registered}")

    if not np.allclose(
        registered_points["theta_end"].to_numpy(float)
        + registered_points["A_bare_end"].to_numpy(float),
        1.0,
        atol=1e-12,
        rtol=0.0,
    ):
        raise ValueError("Registered degeneracy theta/R_theta identity failed")
    reconstructed = 1000.0 * registered_points["bT_needed_V"].to_numpy(float) * np.log(
        1.0 / registered_points["A_bare_end"].to_numpy(float)
    )
    if not np.allclose(reconstructed, access_contribution_mV, atol=2e-9, rtol=0.0):
        raise ValueError("Registered degeneracy points do not preserve the fixed voltage contribution")
    if not np.allclose(
        registered_points["tafel_mV_dec"].to_numpy(float),
        1000.0 * math.log(10.0) * registered_points["bT_needed_V"].to_numpy(float),
        atol=2e-9,
        rtol=0.0,
    ):
        raise ValueError("Registered coefficient conversion failed")

    fit_table = pd.DataFrame(
        {
            "Q_mAh_cm2": q,
            "observed_full_cell_voltage_V": voltage,
            "in_registered_fit_interval": fit_mask,
            "reduced_fit_voltage_V": np.nan,
            "fit_minus_observed_mV": np.nan,
        }
    )
    fit_table.loc[fit_mask, "reduced_fit_voltage_V"] = fitted
    fit_table.loc[fit_mask, "fit_minus_observed_mV"] = residual_mV
    fit_table.to_csv(FIT_TABLE, index=False, float_format="%.12g", lineterminator="\n")

    r_theta_grid = np.linspace(
        float(registered_points["A_bare_end"].min()),
        float(registered_points["A_bare_end"].max()),
        401,
    )
    coefficient_v = (access_contribution_mV / 1000.0) / np.log(1.0 / r_theta_grid)
    curve = pd.DataFrame(
        {
            "R_theta_end": r_theta_grid,
            "theta_end": 1.0 - r_theta_grid,
            "effective_coefficient_V": coefficient_v,
            "effective_coefficient_mV_per_decade": 1000.0 * math.log(10.0) * coefficient_v,
            "fixed_selected_voltage_contribution_mV": access_contribution_mV,
        }
    )
    curve.to_csv(CURVE_TABLE, index=False, float_format="%.12g", lineterminator="\n")
    points = registered_points.rename(
        columns={
            "A_bare_end": "R_theta_end",
            "bT_needed_V": "effective_coefficient_V",
            "tafel_mV_dec": "effective_coefficient_mV_per_decade",
        }
    ).copy()
    points["fixed_selected_voltage_contribution_mV"] = access_contribution_mV
    points.to_csv(POINT_TABLE, index=False, float_format="%.12g", lineterminator="\n")

    parameters = pd.DataFrame(
        [
            ["fit_Q_min_observed", float(q_fit[0]), "mAh cm^-2", "first selected point satisfying Q >= 2"],
            ["fit_Q_max", q_peak, "mAh cm^-2", "selected trace maximum"],
            ["c0", c0, "V", "reduced observation-layer intercept"],
            ["c1", c1, "V per (mAh cm^-2)", "reduced observation-layer linear coefficient"],
            ["b_eff", b_eff, "V", "reduced observation-layer accessibility coefficient"],
            ["RMSE", rmse_mV, "mV", "fit residual root-mean-square"],
            ["DeltaV_access_selected", access_contribution_mV, "mV", "fixed contribution used for degeneracy curve"],
            ["DeltaV_linear_selected", drift_contribution_mV, "mV", "linear contribution over fitted points"],
        ],
        columns=["quantity", "value", "unit", "definition"],
    )
    parameters.to_csv(PARAMETER_TABLE, index=False, float_format="%.12g", lineterminator="\n")
    audit = {
        "selected_trace_points": int(len(selected)),
        "physical_files": int(selected["FileName"].nunique()),
        "selected_cycle": 20,
        "fit_points": int(fit_mask.sum()),
        "fit_Q_observed_mAh_cm2": [float(q_fit[0]), float(q_fit[-1])],
        "peak_Q_mAh_cm2": q_peak,
        "peak_voltage_V": float(voltage[peak_index]),
        "RMSE_mV": rmse_mV,
        "fixed_accessibility_voltage_contribution_mV": access_contribution_mV,
        "registered_point_identity_pass": True,
        "evidence_class": "E-POST on E-EXP/E-SIM inputs",
    }
    return fit_table, curve, points, parameters, audit


def make_builder(fit_table: pd.DataFrame, curve: pd.DataFrame, points: pd.DataFrame, audit: dict):
    def build():
        fig = plt.figure(figsize=(WIDTH_MM / 25.4, HEIGHT_MM / 25.4))
        grid = fig.add_gridspec(
            2,
            12,
            left=0.078,
            right=0.985,
            bottom=0.145,
            top=0.895,
            hspace=0.10,
            wspace=1.55,
            height_ratios=[2.45, 1.0],
        )
        ax_v = fig.add_subplot(grid[0, :5])
        ax_r = fig.add_subplot(grid[1, :5], sharex=ax_v)
        ax_d = fig.add_subplot(grid[:, 6:])

        q = fit_table["Q_mAh_cm2"].to_numpy(float)
        observed = fit_table["observed_full_cell_voltage_V"].to_numpy(float)
        mask = fit_table["in_registered_fit_interval"].astype(bool).to_numpy()
        q_fit = q[mask]
        fit = fit_table.loc[mask, "reduced_fit_voltage_V"].to_numpy(float)
        residual = fit_table.loc[mask, "fit_minus_observed_mV"].to_numpy(float)

        ax_v.axvspan(2.0, audit["peak_Q_mAh_cm2"], color=PALE_GREY, zorder=0)
        ax_v.plot(q, observed, color=CARMINE, lw=1.25, label="selected full-cell charge", zorder=3)
        ax_v.plot(q_fit, fit, color=NAVY, lw=1.45, ls=(0, (4.0, 2.0)), label="reduced fit", zorder=4)
        ax_v.set_ylabel("Voltage (V)")
        ax_v.set_ylim(1.33, 1.505)
        ax_v.set_yticks([1.35, 1.40, 1.45, 1.50])
        ax_v.tick_params(labelbottom=False)
        ax_v.set_title("Selected full-cell charge and fitted interval", loc="left", pad=4.0)
        ax_v.legend(loc="upper left", fontsize=6.5, handlelength=2.1, borderaxespad=0.2)
        style_axis(ax_v)
        panel_label(ax_v, "a", x=-0.18)
        ax_v.text(
            0.98,
            0.07,
            "shaded: fitted points",
            transform=ax_v.transAxes,
            ha="right",
            va="bottom",
            fontsize=6.5,
            color=MID_GREY,
        )

        ax_r.plot(q_fit, residual, color=NAVY, lw=1.05)
        style_axis(ax_r, zero_line=True)
        ax_r.set_xlim(0, 120)
        ax_r.set_ylim(-20, 20)
        ax_r.set_yticks([-15, 0, 15])
        ax_r.set_xticks([0, 40, 80, 120])
        ax_r.set_ylabel("Fit − data\n(mV)")
        ax_r.set_xlabel(r"Areal charge capacity, $Q$ (mAh cm$^{-2}$)")
        ax_r.text(
            0.98,
            0.91,
            f"RMSE = {audit['RMSE_mV']:.2f} mV",
            transform=ax_r.transAxes,
            ha="right",
            va="top",
            fontsize=6.5,
            color=INK,
        )

        ax_d.plot(
            curve["R_theta_end"],
            curve["effective_coefficient_mV_per_decade"],
            color=TEAL,
            lw=1.85,
            zorder=3,
        )
        ax_d.scatter(
            points["R_theta_end"],
            points["effective_coefficient_mV_per_decade"],
            s=16,
            facecolor=WHITE,
            edgecolor=TEAL,
            linewidth=0.8,
            zorder=5,
        )
        label_rows = [
            (points.iloc[-1], (12, 7), "0.014 → 38"),
            (points.loc[(points["R_theta_end"] - 0.37).abs().idxmin()], (8, 8), "0.37 → 164"),
            (points.iloc[0], (-10, -15), "0.60 → 319"),
        ]
        for row, offset, label in label_rows:
            ax_d.annotate(
                label,
                xy=(float(row["R_theta_end"]), float(row["effective_coefficient_mV_per_decade"])),
                xytext=offset,
                textcoords="offset points",
                ha="left" if offset[0] >= 0 else "right",
                va="bottom" if offset[1] >= 0 else "top",
                fontsize=6.5,
                color=INK,
                arrowprops={"arrowstyle": "-", "color": MID_GREY, "lw": 0.6},
            )
        ax_d.set_xlim(0.0, 0.62)
        ax_d.set_ylim(0, 345)
        ax_d.set_xticks([0.0, 0.2, 0.4, 0.6])
        ax_d.set_yticks([0, 100, 200, 300])
        ax_d.set_xlabel(r"Reduced accessibility factor, $R_{\theta,\rm end}$")
        ax_d.set_ylabel(r"Effective coefficient (mV dec$^{-1}$)")
        ax_d.set_title("One voltage contribution, multiple reduced-factor pairs", loc="left", pad=4.0)
        style_axis(ax_d)
        panel_label(ax_d, "b", x=-0.13)
        ax_d.text(
            0.98,
            0.04,
            f"fixed selected contribution = {audit['fixed_accessibility_voltage_contribution_mV']:.1f} mV",
            transform=ax_d.transAxes,
            ha="right",
            va="bottom",
            fontsize=6.5,
            color=MID_GREY,
        )
        ax_d.text(
            0.02,
            0.04,
            r"$R_{\theta,\rm end}=1-\theta_{\rm end}$",
            transform=ax_d.transAxes,
            ha="left",
            va="bottom",
            fontsize=6.5,
            color=MID_GREY,
        )
        text_audit = audit_text(fig, FAMILY)
        return fig, {"width_mm": WIDTH_MM, "height_mm": HEIGHT_MM, "font_audit": text_audit}

    return build


def write_documents(outputs: dict[str, Path], qa: dict, data_audit: dict) -> None:
    output_records = [
        {"path": rel(path), "size_bytes": path.stat().st_size, "sha256": sha256(path)}
        for path in outputs.values()
    ]
    bundle_files = [
        INPUT_MANIFEST,
        FIT_TABLE,
        CURVE_TABLE,
        POINT_TABLE,
        PARAMETER_TABLE,
        HERE / "r582_si_figure_tools.py",
        Path(__file__),
        HERE / "FIGURE_CONTRACT.md",
        HERE / "CAPTION_DRAFT.md",
        HERE / "README.md",
        HERE / "QA_NOTES.md",
    ]
    manifest = {
        "figure": STEM,
        "single_dominant_claim": (
            "The selected voltage contribution can be reproduced by multiple reduced accessibility-factor/"
            "coefficient pairs, so voltage does not uniquely identify native remaining area."
        ),
        "evidence_class": "E-POST on E-EXP/E-SIM inputs",
        "frozen_date": "2026-07-20",
        "final_size_mm": {"width": WIDTH_MM, "height": HEIGHT_MM},
        "font": {
            "family": FAMILY,
            "minimum_pt": 6.5,
            "registered_faces": [{"path": str(path), "sha256": sha256(path)} for path in TERMES_PATHS],
        },
        "claim_boundary": (
            "R_theta,end = 1 - theta_end is the reduced calibration-controlled accessibility factor, not native "
            "A_bare/A0; the native relation is A_bare/A0 = R_theta*T_pore. This reduced observation-layer result "
            "is neither an independent validation nor a deposit-morphology inference."
        ),
        "data_audit": data_audit,
        "qa": qa,
        "inputs": [
            {"path": rel(path), "size_bytes": path.stat().st_size, "sha256": EXPECTED_SHA256[key]}
            for key, path in INPUTS.items()
        ],
        "figure_outputs": output_records,
        "source_bundle_files": [
            {"path": rel(path), "size_bytes": path.stat().st_size, "sha256": sha256(path)}
            for path in bundle_files
        ],
    }
    RENDER_MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    fit, curve, points, _parameters, data_audit = prepare_data()
    outputs, qa = export_deterministic(
        make_builder(fit, curve, points, data_audit),
        FIGURE_DIR,
        STEM,
        "Full-cell voltage fit and accessibility-coefficient degeneracy",
        Path(__file__).name,
        WIDTH_MM,
        HEIGHT_MM,
        FAMILY,
    )
    write_documents(outputs, qa, data_audit)
    print(json.dumps({"figure": STEM, "outputs": {key: str(path) for key, path in outputs.items()}, "qa": qa}, indent=2))


if __name__ == "__main__":
    main()
