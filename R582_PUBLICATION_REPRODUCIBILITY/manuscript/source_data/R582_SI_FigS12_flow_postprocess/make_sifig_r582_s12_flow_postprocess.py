#!/usr/bin/env python
"""Build R582 Supplementary Figure S12 from the registered R577 scenario.

Only the sub-grid generation contribution is rescaled through the declared
Sherwood relation.  The figure is an analytical postprocess of a solved
baseline, not a new flow-dependent boundary-layer solve or a measured law.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from r582_si_figure_tools import (
    BLUE,
    CARMINE,
    INK,
    LIGHT_BLUE,
    MID_GREY,
    NAVY,
    PALE_GREY,
    TERMES_PATHS,
    audit_text,
    configure_font,
    export_deterministic,
    sha256,
    style_axis,
)


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
FIGURE_DIR = PROJECT / "manuscript" / "figures_R582"
FIGURE_DIR.mkdir(parents=True, exist_ok=True)
STEM = "SIFig_R582_S12_flow_postprocess"
WIDTH_MM = 180.0
HEIGHT_MM = 68.0
FAMILY = configure_font(STEM)

BASELINE = HERE / "inputs" / "R577_baseline_input.csv"
REGISTERED_SWEEP = HERE / "inputs" / "R577_flow_delta_sweep.csv"
EXPECTED_SHA256 = {
    BASELINE: "3490EBDB2C5244AF9044D3422BC29FED96B57AF54F9C48AAC46BD3B1717C0335",
    REGISTERED_SWEEP: "CCC7C618B33B9489C03CA3DD5C5F1ECAF5E9AFF114A0935015FEE0F2C8CAF6DB",
}
REGISTERED_SOURCES = {
    BASELINE: "manuscript/source_data/Fig_R577_flow_delta/R577_baseline_input.csv",
    REGISTERED_SWEEP: "manuscript/source_data/Fig_R577_flow_delta/R577_flow_delta_sweep.csv",
}
PLOT_TABLE = HERE / "R582_SIFig_S12_flow_scenario.csv"
SUMMARY_TABLE = HERE / "R582_SIFig_S12_scenario_summary.csv"
INPUT_MANIFEST = HERE / "R582_SIFig_S12_input_manifest.csv"
RENDER_MANIFEST = HERE / "R582_SIFig_S12_render_manifest.json"

CSAT = 1.33
DELTA0_M = 25e-6
V_NOM_ML_MIN = 50.0
M_VALUES = (0.4, 0.5, 0.6)


def rel(path: Path) -> str:
    return path.resolve().relative_to(PROJECT.resolve()).as_posix()


def verify_inputs() -> None:
    rows = []
    for path, expected in EXPECTED_SHA256.items():
        if not path.is_file():
            raise FileNotFoundError(path)
        observed = sha256(path)
        if observed != expected:
            raise ValueError(f"Frozen input hash mismatch for {path}: {observed}")
        rows.append(
            {
                "source_key": path.stem,
                "frozen_copy": rel(path),
                "registered_source": REGISTERED_SOURCES[path],
                "size_bytes": path.stat().st_size,
                "sha256": observed,
                "used_for": (
                    "solved baseline terms and registered saturation marker"
                    if path == BASELINE
                    else "registered analytical flow sweep"
                ),
                "immutable_registered_input": True,
            }
        )
    pd.DataFrame(rows).to_csv(INPUT_MANIFEST, index=False, lineterminator="\n")


def onset_from_s(q: np.ndarray, saturation: np.ndarray, threshold: float = 1.0) -> float:
    mask = saturation >= threshold
    if not mask.any():
        return float("nan")
    index = int(np.argmax(mask))
    if index == 0:
        return float(q[0])
    q0, q1 = q[index - 1], q[index]
    s0, s1 = saturation[index - 1], saturation[index]
    return float(q0 + (threshold - s0) * (q1 - q0) / (s1 - s0))


def prepare_data() -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    verify_inputs()
    baseline = pd.read_csv(BASELINE)
    registered = pd.read_csv(REGISTERED_SWEEP)
    required_baseline = {"case_id", "q_mAh_cm2", "S_avg", "cI2_surf_tot_avg", "beta_surf_avg"}
    required_sweep = {"m_exp", "v_ratio", "flow_mL_min", "delta_ratio", "delta_um", "Q_onset", "dQ"}
    if not required_baseline.issubset(baseline.columns):
        raise ValueError(f"Baseline schema mismatch: {baseline.columns.tolist()}")
    if not required_sweep.issubset(registered.columns):
        raise ValueError(f"Sweep schema mismatch: {registered.columns.tolist()}")
    if len(baseline) != 1081 or baseline["case_id"].nunique() != 1:
        raise ValueError("The frozen baseline must contain 1081 rows from one registered case")
    if baseline["case_id"].iloc[0] != "baseline_J40_Q120":
        raise ValueError("Unexpected baseline case identity")
    if len(registered) != 120 or sorted(registered["m_exp"].unique().tolist()) != list(M_VALUES):
        raise ValueError("The registered sweep must contain 40 rows for each of three exponents")
    if not registered.groupby("m_exp").size().eq(40).all():
        raise ValueError("Unexpected per-exponent sweep length")

    baseline = baseline.sort_values("q_mAh_cm2").reset_index(drop=True)
    q = baseline["q_mAh_cm2"].to_numpy(float)
    n_scaled = baseline["cI2_surf_tot_avg"].to_numpy(float) / CSAT
    beta = baseline["beta_surf_avg"].to_numpy(float)
    s_comsol = baseline["S_avg"].to_numpy(float)
    if not np.all(np.diff(q) > 0) or not np.isfinite(np.column_stack([q, n_scaled, beta, s_comsol])).all():
        raise ValueError("Baseline contains unordered or non-finite values")
    structure = n_scaled / beta
    slope, intercept = np.polyfit(structure, s_comsol, 1)
    pi_gen = float(n_scaled[0])
    q_s0 = onset_from_s(q, s_comsol)

    def evaluate(flow_mL_min: float, exponent: float) -> tuple[float, float, float]:
        ratio = (flow_mL_min / V_NOM_ML_MIN) ** (-exponent)
        n_prime = n_scaled - pi_gen * (1.0 - ratio)
        s_prime = slope * (n_prime / beta) + intercept
        return onset_from_s(q, s_prime), ratio, DELTA0_M * ratio * 1e6

    recomputed_rows = []
    for row in registered.itertuples(index=False):
        onset, ratio, delta_um = evaluate(float(row.flow_mL_min), float(row.m_exp))
        recomputed_rows.append([onset, ratio, delta_um])
    recomputed = np.asarray(recomputed_rows, dtype=float)
    comparisons = {
        "Q_onset": recomputed[:, 0],
        "delta_ratio": recomputed[:, 1],
        "delta_um": recomputed[:, 2],
        "dQ": recomputed[:, 0] - q_s0,
    }
    for column, values in comparisons.items():
        if not np.allclose(registered[column].to_numpy(float), values, atol=2e-10, rtol=0.0):
            error = float(np.max(np.abs(registered[column].to_numpy(float) - values)))
            raise ValueError(f"Registered R577 reconstruction failed for {column}; max error={error}")

    plot = registered.sort_values(["m_exp", "flow_mL_min"]).copy()
    plot["within_declared_25_to_100_mL_min"] = plot["flow_mL_min"].between(25.0, 100.0)
    plot["evidence_class"] = "E-POST"
    plot.to_csv(PLOT_TABLE, index=False, float_format="%.12g", lineterminator="\n")

    summary_rows = [
        ["registered_baseline_Qs", q_s0, "mAh cm^-2", "solved baseline average-saturation crossing"],
        ["nominal_flow", V_NOM_ML_MIN, "mL min^-1", "delta = 25 um anchor"],
        ["nominal_delta", DELTA0_M * 1e6, "um", "declared sub-grid layer anchor"],
        ["normalization_slope", float(slope), "1", "S_COMSOL versus structural normalization"],
        ["normalization_intercept", float(intercept), "1", "S_COMSOL versus structural normalization"],
    ]
    exact_range = {}
    for exponent in M_VALUES:
        q25, _, _ = evaluate(25.0, exponent)
        q100, _, _ = evaluate(100.0, exponent)
        exact_range[str(exponent)] = {"Q_s_at_25": q25, "Q_s_at_100": q100, "span": q100 - q25}
        summary_rows.extend(
            [
                [f"Q_s_25_m{exponent:.1f}", q25, "mAh cm^-2", "analytical postprocess"],
                [f"Q_s_100_m{exponent:.1f}", q100, "mAh cm^-2", "analytical postprocess"],
                [f"Q_s_span_25_to_100_m{exponent:.1f}", q100 - q25, "mAh cm^-2", "analytical postprocess"],
            ]
        )
    summary = pd.DataFrame(summary_rows, columns=["quantity", "value", "unit", "definition"])
    summary.to_csv(SUMMARY_TABLE, index=False, float_format="%.12g", lineterminator="\n")
    audit = {
        "baseline_rows": int(len(baseline)),
        "sweep_rows": int(len(plot)),
        "m_exponents": list(M_VALUES),
        "registered_baseline_Qs_mAh_cm2": q_s0,
        "declared_primary_flow_range_mL_min": [25.0, 100.0],
        "registered_display_flow_range_mL_min": [float(plot.flow_mL_min.min()), float(plot.flow_mL_min.max())],
        "exact_primary_range_results": exact_range,
        "registered_sweep_reconstruction_pass": True,
        "evidence_class": "E-POST",
    }
    return plot, summary, audit


def make_builder(plot: pd.DataFrame, audit: dict):
    def build():
        fig, ax = plt.subplots(figsize=(WIDTH_MM / 25.4, HEIGHT_MM / 25.4))
        fig.subplots_adjust(left=0.085, right=0.975, bottom=0.205, top=0.865)
        ax.axvspan(25.0, 100.0, color=PALE_GREY, zorder=0)
        styles = {
            0.4: {"color": LIGHT_BLUE, "ls": (0, (5.0, 2.1)), "lw": 1.35},
            0.5: {"color": BLUE, "ls": (0, (2.2, 1.5)), "lw": 1.55},
            0.6: {"color": NAVY, "ls": "-", "lw": 1.75},
        }
        endpoints = []
        for exponent in M_VALUES:
            sub = plot.loc[np.isclose(plot["m_exp"], exponent)].sort_values("flow_mL_min")
            style = styles[exponent]
            ax.plot(
                sub["flow_mL_min"],
                sub["Q_onset"],
                color=style["color"],
                ls=style["ls"],
                lw=style["lw"],
                solid_capstyle="round",
                zorder=3,
            )
            endpoints.append((exponent, float(sub["Q_onset"].iloc[-1]), style["color"]))
        q_s0 = audit["registered_baseline_Qs_mAh_cm2"]
        ax.plot(50.0, q_s0, marker="o", ms=4.6, mfc=CARMINE, mec="white", mew=0.6, ls="", zorder=6)
        ax.annotate(
            f"registered baseline\n$Q_s$ = {q_s0:.2f}",
            xy=(50.0, q_s0),
            xytext=(16, -23),
            textcoords="offset points",
            ha="left",
            va="top",
            fontsize=6.5,
            color=CARMINE,
            arrowprops={"arrowstyle": "-", "color": CARMINE, "lw": 0.65},
        )
        direct_label_y = {0.4: 88.7, 0.5: 92.0, 0.6: 95.3}
        for exponent, y_end, color in endpoints:
            y_label = direct_label_y[exponent]
            ax.plot([200.0, 202.8], [y_end, y_label], color=color, lw=0.65, clip_on=False)
            ax.text(
                204.0,
                y_label,
                f"$m$ = {exponent:.1f}",
                ha="left",
                va="center",
                fontsize=7.0,
                color=color,
                fontweight="bold" if exponent == 0.6 else "normal",
            )
        ax.text(
            62.5,
            50.5,
            "declared range\n25–100 mL min$^{-1}$",
            ha="center",
            va="bottom",
            fontsize=6.5,
            color=MID_GREY,
        )
        ax.set_xlim(10, 220)
        ax.set_ylim(49, 97)
        ax.set_xticks([25, 50, 100, 150, 200])
        ax.set_yticks([50, 60, 70, 80, 90])
        ax.set_xlabel(r"Recirculation flow rate (mL min$^{-1}$)")
        ax.set_ylabel(r"Average-saturation point, $Q_s$ (mAh cm$^{-2}$)")
        ax.set_title("Analytical postprocess", loc="left", pad=4.5)
        ax.text(
            0.995,
            1.015,
            r"$\delta/\delta_0=(v/v_0)^{-m}$;  $\delta_0=25\ \mu$m at 50 mL min$^{-1}$",
            transform=ax.transAxes,
            ha="right",
            va="bottom",
            fontsize=6.5,
            color=MID_GREY,
        )
        style_axis(ax)
        text_audit = audit_text(fig, FAMILY)
        return fig, {"width_mm": WIDTH_MM, "height_mm": HEIGHT_MM, "font_audit": text_audit}

    return build


def write_manifest(outputs: dict[str, Path], qa: dict, data_audit: dict) -> None:
    bundle_files = [
        INPUT_MANIFEST,
        PLOT_TABLE,
        SUMMARY_TABLE,
        HERE / "r582_si_figure_tools.py",
        Path(__file__),
        HERE / "FIGURE_CONTRACT.md",
        HERE / "CAPTION_DRAFT.md",
        HERE / "README.md",
        HERE / "QA_NOTES.md",
    ]
    record = {
        "figure": STEM,
        "single_dominant_claim": (
            "Under the declared Sherwood relation, thinning the sub-grid diffusion layer delays the "
            "postprocessed average-saturation point."
        ),
        "evidence_class": "E-POST",
        "frozen_date": "2026-07-20",
        "final_size_mm": {"width": WIDTH_MM, "height": HEIGHT_MM},
        "font": {
            "family": FAMILY,
            "minimum_pt": 6.5,
            "registered_faces": [{"path": str(path), "sha256": sha256(path)} for path in TERMES_PATHS],
        },
        "claim_boundary": (
            "The curves rescale only the declared sub-grid generation contribution. They are not a full "
            "flow-dependent boundary-layer solve, a measured transfer law, or an additional experiment."
        ),
        "data_audit": data_audit,
        "qa": qa,
        "inputs": [
            {"path": rel(path), "size_bytes": path.stat().st_size, "sha256": expected}
            for path, expected in EXPECTED_SHA256.items()
        ],
        "figure_outputs": [
            {"path": rel(path), "size_bytes": path.stat().st_size, "sha256": sha256(path)}
            for path in outputs.values()
        ],
        "source_bundle_files": [
            {"path": rel(path), "size_bytes": path.stat().st_size, "sha256": sha256(path)}
            for path in bundle_files
        ],
    }
    RENDER_MANIFEST.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    plot, _summary, data_audit = prepare_data()
    outputs, qa = export_deterministic(
        make_builder(plot, data_audit),
        FIGURE_DIR,
        STEM,
        "Conditional flow dependence of the analytical boundary-layer scenario",
        Path(__file__).name,
        WIDTH_MM,
        HEIGHT_MM,
        FAMILY,
    )
    write_manifest(outputs, qa, data_audit)
    print(json.dumps({"figure": STEM, "outputs": {key: str(path) for key, path in outputs.items()}, "qa": qa}, indent=2))


if __name__ == "__main__":
    main()
