#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Build R582 main Figure 1 from immutable registered records.

The figure motivates a positive-electrode model with existing full-cell data.
It does not treat full-cell features as an independent validation of model
markers or as evidence of deposit morphology.

All drawing, exports, and grayscale QA are produced with Python. The script
reads only registered processed tables and writes only to the isolated R582
source-data and figure directories.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.lines import Line2D
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle
import numpy as np
import pandas as pd
from PIL import Image


# Match the manuscript's tgtermes + newtxmath Times family. Register all four
# TeX Gyre Termes faces explicitly so headless matplotlib does not substitute.
TERMES_DIR = Path(
    r"D:\Program Files\texlive\2024\texmf-dist\fonts\opentype\public\tex-gyre"
)
TERMES_PATHS = [
    TERMES_DIR / "texgyretermes-regular.otf",
    TERMES_DIR / "texgyretermes-bold.otf",
    TERMES_DIR / "texgyretermes-italic.otf",
    TERMES_DIR / "texgyretermes-bolditalic.otf",
]
if not all(path.is_file() for path in TERMES_PATHS):
    missing = [str(path) for path in TERMES_PATHS if not path.is_file()]
    raise FileNotFoundError(f"Required TeX Gyre Termes font faces are missing: {missing}")
for font_path in TERMES_PATHS:
    font_manager.fontManager.addfont(str(font_path))
FONT_FAMILY = font_manager.FontProperties(fname=str(TERMES_PATHS[0])).get_name()
if FONT_FAMILY != "TeX Gyre Termes":
    raise RuntimeError(f"Unexpected manuscript font family: {FONT_FAMILY}")

# Editable text, manuscript-matched serif typography, and final-size settings.
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = [FONT_FAMILY]
plt.rcParams["mathtext.fontset"] = "custom"
plt.rcParams["mathtext.rm"] = FONT_FAMILY
plt.rcParams["mathtext.it"] = f"{FONT_FAMILY}:italic"
plt.rcParams["mathtext.bf"] = f"{FONT_FAMILY}:bold"
plt.rcParams["mathtext.cal"] = f"{FONT_FAMILY}:italic"
plt.rcParams["mathtext.sf"] = FONT_FAMILY
plt.rcParams["mathtext.fallback"] = None
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["svg.hashsalt"] = "R582_Fig1_experimental_problem"
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams.update(
    {
        "font.size": 7.2,
        "axes.labelsize": 7.2,
        "axes.titlesize": 7.5,
        "axes.titleweight": "bold",
        "axes.linewidth": 0.8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "xtick.labelsize": 6.5,
        "ytick.labelsize": 6.5,
        "xtick.major.size": 2.7,
        "ytick.major.size": 2.7,
        "xtick.major.width": 0.7,
        "ytick.major.width": 0.7,
        "legend.fontsize": 6.5,
        "legend.frameon": False,
        "axes.unicode_minus": False,
        "savefig.facecolor": "white",
        "figure.facecolor": "white",
    }
)


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
FIGURE_DIR = PROJECT / "manuscript" / "figures_R582"
FIGURE_DIR.mkdir(parents=True, exist_ok=True)
BASE = FIGURE_DIR / "Fig_R582_experimental_problem"

VQ_SOURCE = (
    PROJECT
    / "manuscript"
    / "source_data"
    / "Fig_R538_voltage_reanchor"
    / "representative_vq_profiles_for_article.csv"
)
RATE_SOURCE = (
    PROJECT
    / "manuscript"
    / "source_data"
    / "Fig_R581_experimental_evidence"
    / "R581_experimental_evidence_panel_b_rate.csv"
)
TIMING_SOURCE = (
    PROJECT
    / "manuscript"
    / "source_data"
    / "Fig_R581_experimental_evidence"
    / "R581_experimental_evidence_panel_d_g4.csv"
)
DVDQ_SOURCE = (
    PROJECT
    / "battery_experiment"
    / "02_processed_data"
    / "R581_G4_DVDQ_REBUILD"
    / "dvdq_curves_all_windows.csv"
)
MARKER_SOURCE = (
    PROJECT
    / "manuscript"
    / "source_data"
    / "Fig_R568_scale_provenance"
    / "R581_Fig_R568_scale_provenance_source_data.csv"
)

EXPECTED_SHA256 = {
    VQ_SOURCE: "150AFD09C0AE8FEE58A8DFE1CCC412378CB1F7893075F54BDFFD8DE0AED3D1F1",
    RATE_SOURCE: "9A30CDCA03BB870931AA0A8C91E8C7F0AE1265EA5FA71EAE5F2A5EDDA75BB517",
    TIMING_SOURCE: "05E38C4702EFC34BF0AD2F5558D5CACC90808157C3AF8C46CED73F58F93C3AF7",
    DVDQ_SOURCE: "AAADD2779474FE74C1F0F4BC472633B113967905CA2BCE2EF97FAF8F0CA7D2DE",
    MARKER_SOURCE: "4CB61A67545F55B5FEF66F91B420300030BA8B771BB38400B088C75B35E8106C",
}


# Paper-wide semantic palette.
NAVY = "#243B53"
BLUE = "#3B6FB6"
TEAL = "#2A9D8F"
AMBER = "#D8912B"
CARMINE = "#C65D57"
GRAPHITE = "#4D4D4D"
MID_GREY = "#7B858C"
LIGHT_GREY = "#D6DADD"
PALE_GREY = "#EEF0F2"
PALE_AMBER = "#F7E9CF"
PALE_TEAL = "#DCEFEB"
WHITE = "#FFFFFF"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def require_frozen_inputs() -> None:
    for path, expected in EXPECTED_SHA256.items():
        if not path.is_file():
            raise FileNotFoundError(path)
        observed = sha256(path)
        if observed != expected:
            raise RuntimeError(
                f"Frozen input hash mismatch for {path}: expected {expected}, observed {observed}"
            )


def workspace_relative(path: Path) -> str:
    return path.relative_to(PROJECT).as_posix()


def add_panel_label(ax, label: str, x: float = -0.08, y: float = 1.06) -> None:
    ax.text(
        x,
        y,
        label,
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=8.2,
        fontweight="bold",
        color="#111111",
        clip_on=False,
    )


def style_axis(ax) -> None:
    ax.spines["left"].set_color(GRAPHITE)
    ax.spines["bottom"].set_color(GRAPHITE)
    ax.tick_params(colors=GRAPHITE, direction="out")
    ax.xaxis.label.set_color(GRAPHITE)
    ax.yaxis.label.set_color(GRAPHITE)


def read_and_derive():
    require_frozen_inputs()

    vq_all = pd.read_csv(VQ_SOURCE)
    vq_selected = vq_all.loc[
        (vq_all["figure"] == "01_baseline_standard_controls")
        & (vq_all["display_sample"] == "Pristine")
        & (vq_all["direction"] == "charge")
        & (vq_all["pair_index"] == 20)
    ].copy()
    if len(vq_selected) != 90:
        raise RuntimeError(f"Expected 90 registered representative V(Q) points, found {len(vq_selected)}")
    vq_selected["Q_mAh_cm2"] = vq_selected["segment_capacity_mAh"] / 4.0
    vq_selected = vq_selected.sort_values("Q_mAh_cm2")

    dvdq_all = pd.read_csv(DVDQ_SOURCE)
    dvdq = dvdq_all.loc[
        (dvdq_all["pair_index"] == 20)
        & np.isclose(dvdq_all["window_mAh_cm2"], 10.25)
    ].copy()
    if len(dvdq) != 475:
        raise RuntimeError(f"Expected 475 frozen primary-window dV/dQ points, found {len(dvdq)}")
    dvdq = dvdq.sort_values("Q_mAh_cm2")

    # Identity/alignment audit: the exact derivative table and the registered
    # article trace are the same file/cycle. The latter is a sparse display
    # export, so rapid endpoint curvature can differ under linear resampling.
    source_names = vq_selected["FileName"].drop_duplicates().tolist()
    derivative_names = dvdq["FileName"].drop_duplicates().tolist()
    if source_names != derivative_names:
        raise RuntimeError("Representative V(Q) and frozen derivative table do not share file identity")
    vq_interp = np.interp(
        dvdq["Q_mAh_cm2"].to_numpy(),
        vq_selected["Q_mAh_cm2"].to_numpy(),
        vq_selected["voltage_v"].to_numpy(),
    )
    residual = vq_interp - dvdq["voltage_raw_interp_V"].to_numpy()
    mean_abs_residual_v = float(np.mean(np.abs(residual)))
    max_abs_residual_v = float(np.max(np.abs(residual)))
    if mean_abs_residual_v > 0.005 or max_abs_residual_v > 0.040:
        raise RuntimeError("Registered display trace and derivative-table voltage failed alignment audit")

    timing = pd.read_csv(TIMING_SOURCE)
    if set(timing["pair_index"].astype(int)) != {20, 21, 22, 23} or len(timing) != 12:
        raise RuntimeError("Expected four cycles by three prespecified derivative windows")
    timing_primary = timing.loc[timing["window_role"] == "primary"].copy()
    if len(timing_primary) != 4:
        raise RuntimeError("Expected one primary derivative estimate for each of four cycles")

    pair20 = timing_primary.loc[timing_primary["pair_index"] == 20]
    if len(pair20) != 1:
        raise RuntimeError("Missing unique pair-20 primary timing record")
    onset_q = float(pair20.iloc[0]["rise_onset_Q_mAh_cm2"])
    peak_q = float(pair20.iloc[0]["peak_Q_mAh_cm2"])
    if not np.isclose(onset_q, 52.0) or not np.isclose(peak_q, 95.0):
        raise RuntimeError("Frozen representative feature coordinates changed")

    marker_table = pd.read_csv(MARKER_SOURCE)
    marker_values = marker_table.loc[
        marker_table["record_type"] == "anchor", ["item_id", "value"]
    ].set_index("item_id")["value"]
    q_s = float(marker_values.loc["Q_s"])
    q_f = float(marker_values.loc["Q_f_cal"])

    # Clean Figure 1b source table.
    vq_out = dvdq[
        [
            "Q_mAh_cm2",
            "voltage_raw_interp_V",
            "voltage_smooth_V",
            "dVdQ_V_per_mAh_cm2",
        ]
    ].copy()
    vq_out.insert(0, "pair_index", 20)
    vq_out["current_density_mA_cm2"] = float(pair20.iloc[0]["current_density_mA_cm2"])
    vq_out["savgol_window_mAh_cm2"] = 10.25
    vq_out["savgol_polynomial_order"] = 3
    vq_out["grid_spacing_mAh_cm2"] = 0.25
    vq_out["rise_onset_Q_mAh_cm2"] = onset_q
    vq_out["peak_Q_mAh_cm2"] = peak_q
    vq_out["Q_s_model_mAh_cm2"] = q_s
    vq_out["Q_f_cal_model_mAh_cm2"] = q_f
    vq_out["independent_unit"] = "one physical cell/file; cycle 20 is representative"
    vq_out["model_markers_fitted_to_data"] = False
    vq_out["raw_file_sha256"] = str(pair20.iloc[0]["raw_sha256"])
    vq_out.to_csv(HERE / "R582_Fig1b_selected_vq_dvdq.csv", index=False, float_format="%.9g")

    # Clean Figure 1c source table.
    rate = pd.read_csv(RATE_SOURCE)
    rate_out = rate[
        [
            "source_id",
            "material_identity",
            "rate_evidence_role",
            "commanded_current_density_mA_cm2",
            "n_cell",
            "n_cycle",
            "ce_pct_median",
            "ce_pct_min",
            "ce_pct_max",
            "connect_to_pristine_ladder",
            "independent_unit",
            "cycle_summary",
            "population_interval",
            "raw_sha256",
        ]
    ].copy()
    rate_out.to_csv(HERE / "R582_Fig1c_rate_ladder.csv", index=False, float_format="%.9g")

    # Clean Figure 1d source table, retaining all prespecified windows.
    timing_out = timing[
        [
            "pair_index",
            "target_areal_capacity_mAh_cm2",
            "current_density_mA_cm2",
            "window_mAh_cm2",
            "window_role",
            "rise_onset_Q_mAh_cm2",
            "peak_Q_mAh_cm2",
            "peak_dVdQ_V_per_mAh_cm2",
            "peak_right_censored",
            "independent_file_count",
            "repeated_cycle_count_in_file",
            "independent_unit",
            "population_interval",
            "model_markers_fitted_to_data",
            "raw_sha256",
        ]
    ].copy()
    timing_out["Q_s_model_mAh_cm2"] = q_s
    timing_out["Q_f_cal_model_mAh_cm2"] = q_f
    timing_out["onset_before_Q_s"] = timing_out["rise_onset_Q_mAh_cm2"] < q_s
    timing_out["peak_after_Q_f_cal"] = timing_out["peak_Q_mAh_cm2"] > q_f
    timing_out.to_csv(HERE / "R582_Fig1d_feature_timing.csv", index=False, float_format="%.9g")

    # The methodological strip is schematic; this table makes its vocabulary explicit.
    cell_strip = pd.DataFrame(
        [
            (1, "positive current collector", "context", False),
            (2, "positive carbon felt", "model focus", True),
            (3, "separator", "context", False),
            (4, "negative side", "full-cell context", False),
            (5, "negative current collector", "context", False),
        ],
        columns=["display_order", "component", "figure_role", "highlighted"],
    )
    cell_strip["geometry_status"] = "schematic; not to scale"
    cell_strip.to_csv(HERE / "R582_Fig1a_cell_strip.csv", index=False)

    manifest_rows = []
    roles = {
        VQ_SOURCE: "registered representative V(Q) identity and sparse display-trace cross-check",
        RATE_SOURCE: "same-cell pristine CE ladder plus unconnected 40/400 markers",
        TIMING_SOURCE: "four-cycle feature positions across prespecified derivative windows",
        DVDQ_SOURCE: "frozen 0.25-grid voltage and cubic Savitzky-Golay derivative for cycle 20",
        MARKER_SOURCE: "exact baseline-model Q_s and Q_f,cal coordinates",
    }
    for path, expected in EXPECTED_SHA256.items():
        manifest_rows.append(
            {
                "source_key": path.stem,
                "path_workspace_relative": workspace_relative(path),
                "size_bytes": path.stat().st_size,
                "sha256": expected,
                "used_for": roles[path],
                "immutable_registered_input": True,
            }
        )
    pd.DataFrame(manifest_rows).to_csv(HERE / "R582_Fig1_input_manifest.csv", index=False)

    audit = {
        "representative_pair_index": 20,
        "registered_sparse_vq_rows": int(len(vq_selected)),
        "frozen_derivative_rows": int(len(dvdq)),
        "sparse_vs_derivative_mean_abs_voltage_residual_V": mean_abs_residual_v,
        "sparse_vs_derivative_max_abs_voltage_residual_V": max_abs_residual_v,
        "primary_rise_onset_mAh_cm2": onset_q,
        "primary_derivative_peak_mAh_cm2": peak_q,
        "Q_s_model_mAh_cm2": q_s,
        "Q_f_cal_model_mAh_cm2": q_f,
    }
    return vq_out, rate_out, timing_out, timing_primary, q_s, q_f, audit


def draw_cell_strip(ax) -> None:
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_title("Full-cell record, positive-electrode focus", loc="left", pad=3)
    add_panel_label(ax, "a", x=-0.12, y=1.05)

    y0, h = 0.35, 0.30
    # Minimal flat cross-section; no particle/deposit morphology is depicted.
    components = [
        (0.08, 0.045, GRAPHITE, None),
        (0.125, 0.34, PALE_AMBER, "////"),
        (0.465, 0.055, PALE_TEAL, None),
        (0.520, 0.34, PALE_GREY, None),
        (0.860, 0.045, GRAPHITE, None),
    ]
    for x, w, color, hatch in components:
        ax.add_patch(
            Rectangle(
                (x, y0),
                w,
                h,
                facecolor=color,
                edgecolor=GRAPHITE,
                linewidth=0.65,
                hatch=hatch,
            )
        )

    # Voltage measurement bridge.
    x_left, x_right, y_wire = 0.102, 0.882, 0.83
    ax.plot([x_left, x_left, 0.43], [y0 + h, y_wire, y_wire], color=GRAPHITE, lw=0.75)
    ax.plot([0.57, x_right, x_right], [y_wire, y_wire, y0 + h], color=GRAPHITE, lw=0.75)
    ax.add_patch(Circle((0.50, y_wire), 0.07, facecolor=WHITE, edgecolor=GRAPHITE, linewidth=0.75))
    ax.text(0.50, y_wire, "V", ha="center", va="center", fontsize=7.2, fontweight="bold", color=NAVY)

    ax.plot([0.15, 0.44], [y0 - 0.03, y0 - 0.03], color=AMBER, lw=1.0)
    ax.text(
        0.295,
        0.07,
        "positive felt\nmodel focus",
        ha="center",
        va="bottom",
        fontsize=6.5,
        color=AMBER,
        fontweight="bold",
    )
    ax.text(
        0.492,
        y0 + h / 2,
        "separator",
        ha="center",
        va="center",
        rotation=90,
        fontsize=6.5,
        color=TEAL,
    )
    ax.text(0.69, y0 + h / 2, "negative side", ha="center", va="center", fontsize=6.5, color=MID_GREY)


def draw_model_markers(ax, q_s: float, q_f: float) -> None:
    ax.axvline(q_s, color=BLUE, ls=(0, (3.0, 2.0)), lw=0.9, zorder=1)
    ax.axvline(q_f, color=TEAL, ls=(0, (1.1, 1.6)), lw=1.1, zorder=1)


def draw_voltage_hero(ax_v, ax_d, vq, q_s, q_f) -> None:
    q = vq["Q_mAh_cm2"].to_numpy()
    v_raw = vq["voltage_raw_interp_V"].to_numpy()
    v_smooth = vq["voltage_smooth_V"].to_numpy()
    derivative = vq["dVdQ_V_per_mAh_cm2"].to_numpy()
    onset_q = float(vq["rise_onset_Q_mAh_cm2"].iloc[0])
    peak_q = float(vq["peak_Q_mAh_cm2"].iloc[0])

    ax_v.set_title("Representative charge at 40 mA cm$^{-2}$", loc="left", pad=3)
    add_panel_label(ax_v, "b", x=-0.065, y=1.06)
    ax_v.axvspan(onset_q, peak_q, color=PALE_AMBER, alpha=0.55, lw=0, zorder=0)
    ax_v.plot(q, v_raw, color=LIGHT_GREY, lw=0.65, zorder=2)
    ax_v.plot(q, v_smooth, color=NAVY, lw=1.45, zorder=3)
    draw_model_markers(ax_v, q_s, q_f)
    ax_v.set_xlim(0, 120)
    ax_v.set_ylim(1.335, 1.505)
    ax_v.set_ylabel("Cell voltage (V)")
    ax_v.set_yticks([1.35, 1.40, 1.45, 1.50])
    ax_v.tick_params(axis="x", labelbottom=False, bottom=False)
    style_axis(ax_v)

    ax_v.text(
        (onset_q + peak_q) / 2,
        1.495,
        "voltage-rise feature",
        ha="center",
        va="top",
        color=AMBER,
        fontsize=6.5,
        fontweight="bold",
    )
    ax_v.text(q_s - 1.2, 1.339, "$Q_s$\n83.0", ha="right", va="bottom", fontsize=6.5, color=BLUE)
    ax_v.text(q_f + 1.2, 1.339, "$Q_{f,\mathrm{cal}}$\n99.6", ha="left", va="bottom", fontsize=6.5, color=TEAL)

    ax_d.axhline(0, color=LIGHT_GREY, lw=0.7, zorder=0)
    positive = np.maximum(derivative, 0)
    ax_d.fill_between(q, 0, positive, color=PALE_AMBER, alpha=0.95, lw=0, zorder=1)
    ax_d.plot(q, derivative, color=AMBER, lw=1.2, zorder=2)
    draw_model_markers(ax_d, q_s, q_f)

    onset_y = float(np.interp(onset_q, q, derivative))
    peak_y = float(np.interp(peak_q, q, derivative))
    ax_d.plot(onset_q, onset_y, marker="o", ms=4.0, mfc=BLUE, mec=WHITE, mew=0.55, zorder=4)
    ax_d.plot(peak_q, peak_y, marker="^", ms=4.8, mfc=WHITE, mec=AMBER, mew=1.0, zorder=4)
    ax_d.annotate(
        "rise onset",
        xy=(onset_q, onset_y),
        xytext=(onset_q - 5.0, onset_y + 0.0026),
        ha="right",
        va="bottom",
        fontsize=6.5,
        color=BLUE,
        arrowprops=dict(arrowstyle="-", color=BLUE, lw=0.65, shrinkA=1, shrinkB=2),
    )
    ax_d.annotate(
        "maximum",
        xy=(peak_q, peak_y),
        xytext=(peak_q - 4.5, peak_y + 0.0007),
        ha="right",
        va="bottom",
        fontsize=6.5,
        color=AMBER,
        arrowprops=dict(arrowstyle="-", color=AMBER, lw=0.65, shrinkA=1, shrinkB=2),
    )
    ax_d.set_xlim(0, 120)
    ax_d.set_ylim(-0.011, 0.0072)
    ax_d.set_yticks([-0.010, 0.000, 0.005])
    ax_d.set_ylabel("")
    ax_d.text(
        0.008,
        0.96,
        "$dV/dQ$\n(V mAh$^{-1}$ cm$^2$)",
        transform=ax_d.transAxes,
        ha="left",
        va="top",
        fontsize=6.5,
        color=GRAPHITE,
    )
    ax_d.set_xlabel("Areal capacity (mAh cm$^{-2}$)")
    ax_d.set_xticks(np.arange(0, 121, 20))
    style_axis(ax_d)


def draw_rate_panel(ax, rate) -> None:
    ax.set_title("Pristine rate ladder", loc="left", pad=3)
    add_panel_label(ax, "c", x=-0.16, y=1.035)
    style_axis(ax)

    ladder = rate.loc[rate["connect_to_pristine_ladder"] == True].copy()  # noqa: E712
    ladder = ladder.sort_values("commanded_current_density_mA_cm2")
    x = ladder["commanded_current_density_mA_cm2"].to_numpy()
    y = ladder["ce_pct_median"].to_numpy()
    yerr = np.vstack(
        [
            y - ladder["ce_pct_min"].to_numpy(),
            ladder["ce_pct_max"].to_numpy() - y,
        ]
    )
    ax.errorbar(
        x,
        y,
        yerr=yerr,
        fmt="o-",
        color=NAVY,
        mfc=BLUE,
        mec=WHITE,
        mew=0.55,
        ms=4.2,
        lw=1.2,
        ecolor=BLUE,
        elinewidth=0.75,
        capsize=0,
        zorder=3,
    )

    separate = rate.loc[rate["rate_evidence_role"] == "cross_protocol_pristine_40_marker"].iloc[0]
    ax.errorbar(
        float(separate["commanded_current_density_mA_cm2"]),
        float(separate["ce_pct_median"]),
        yerr=np.array(
            [
                [float(separate["ce_pct_median"] - separate["ce_pct_min"])],
                [float(separate["ce_pct_max"] - separate["ce_pct_median"])],
            ]
        ),
        fmt="D",
        color=TEAL,
        mfc=TEAL,
        mec=WHITE,
        mew=0.6,
        ms=4.8,
        ecolor=TEAL,
        elinewidth=0.8,
        zorder=4,
    )

    proxy = rate.loc[rate["rate_evidence_role"] == "P350C_positive_N_pristine_proxy"].iloc[0]
    ax.errorbar(
        float(proxy["commanded_current_density_mA_cm2"]),
        float(proxy["ce_pct_median"]),
        yerr=np.array(
            [
                [float(proxy["ce_pct_median"] - proxy["ce_pct_min"])],
                [float(proxy["ce_pct_max"] - proxy["ce_pct_median"])],
            ]
        ),
        fmt="X",
        color=CARMINE,
        mfc=CARMINE,
        mec=WHITE,
        mew=0.55,
        ms=5.2,
        ecolor=CARMINE,
        elinewidth=0.8,
        zorder=4,
    )

    ax.axhline(95, color=LIGHT_GREY, lw=0.8, ls=(0, (3, 2)), zorder=0)
    ax.text(397, 95.25, "95% CE reference", ha="right", va="bottom", fontsize=6.5, color=MID_GREY)
    ax.text(182, 99.55, "same cell", ha="center", va="bottom", fontsize=6.5, color=NAVY, fontweight="bold")
    ax.annotate(
        "separate\npristine cell",
        xy=(40, float(separate["ce_pct_median"])),
        xytext=(58, 91.9),
        ha="left",
        va="top",
        fontsize=6.5,
        color=TEAL,
        arrowprops=dict(arrowstyle="-", color=TEAL, lw=0.7, shrinkA=1, shrinkB=2),
    )
    ax.annotate(
        "P350C+ proxy",
        xy=(400, float(proxy["ce_pct_median"])),
        xytext=(385, 84.2),
        ha="right",
        va="top",
        fontsize=6.5,
        color=CARMINE,
        arrowprops=dict(arrowstyle="-", color=CARMINE, lw=0.7, shrinkA=1, shrinkB=2),
    )

    ax.set_xlim(25, 415)
    ax.set_ylim(80, 101)
    ax.set_xticks([40, 160, 280, 400])
    ax.set_yticks([80, 85, 90, 95, 100])
    ax.set_xlabel("Current density (mA cm$^{-2}$)")
    ax.set_ylabel("Coulombic efficiency (%)")


def draw_timing_panel(ax, timing, timing_primary, q_s, q_f) -> None:
    ax.set_title("Feature timing across four cycles", loc="left", pad=3)
    add_panel_label(ax, "d", x=-0.065, y=1.05)
    style_axis(ax)
    draw_model_markers(ax, q_s, q_f)

    cycles = [20, 21, 22, 23]
    y_positions = {cycle: 3 - i for i, cycle in enumerate(cycles)}
    for cycle in cycles:
        sub = timing.loc[timing["pair_index"] == cycle].copy()
        primary = timing_primary.loc[timing_primary["pair_index"] == cycle].iloc[0]
        y = y_positions[cycle]

        onset_min = float(sub["rise_onset_Q_mAh_cm2"].min())
        onset_max = float(sub["rise_onset_Q_mAh_cm2"].max())
        peak_min = float(sub["peak_Q_mAh_cm2"].min())
        peak_max = float(sub["peak_Q_mAh_cm2"].max())
        onset = float(primary["rise_onset_Q_mAh_cm2"])
        peak = float(primary["peak_Q_mAh_cm2"])

        ax.hlines(y, onset, peak, color=GRAPHITE, lw=0.9, zorder=1)
        ax.hlines(y, onset_min, onset_max, color=BLUE, lw=3.2, alpha=0.26, zorder=2)
        ax.hlines(y, peak_min, peak_max, color=AMBER, lw=3.2, alpha=0.30, zorder=2)
        ax.plot(onset, y, marker="o", ms=4.1, mfc=BLUE, mec=WHITE, mew=0.55, zorder=4)
        ax.plot(peak, y, marker="^", ms=4.8, mfc=WHITE, mec=AMBER, mew=1.0, zorder=4)

    ax.set_xlim(47, 120)
    ax.set_ylim(-0.65, 3.65)
    ax.set_xticks([50, 70, 90, 110])
    ax.set_yticks([3, 2, 1, 0])
    ax.set_yticklabels(["20", "21", "22", "23"])
    ax.set_ylabel("Cycle")
    ax.set_xlabel("Feature capacity (mAh cm$^{-2}$)")

    ax.text(q_s - 0.8, 3.50, "$Q_s$", ha="right", va="top", fontsize=6.5, color=BLUE)
    ax.text(q_f + 0.8, 3.50, "$Q_{f,\mathrm{cal}}$", ha="left", va="top", fontsize=6.5, color=TEAL)

    legend_handles = [
        Line2D([], [], marker="o", ls="", ms=4.1, mfc=BLUE, mec=WHITE, mew=0.55, label="onset"),
        Line2D([], [], marker="^", ls="", ms=4.8, mfc=WHITE, mec=AMBER, mew=1.0, label="maximum"),
        Line2D([], [], color=GRAPHITE, alpha=0.35, lw=3.0, label="three-window range"),
    ]
    ax.legend(
        handles=legend_handles,
        loc="upper right",
        bbox_to_anchor=(1.0, 1.18),
        ncol=3,
        columnspacing=0.9,
        handletextpad=0.35,
        borderaxespad=0,
        fontsize=6.5,
    )


def build_figure(vq, rate, timing, timing_primary, q_s, q_f):
    width_mm, height_mm = 180.0, 115.0
    fig = plt.figure(figsize=(width_mm / 25.4, height_mm / 25.4))
    outer = fig.add_gridspec(
        3,
        12,
        left=0.075,
        right=0.985,
        bottom=0.125,
        top=0.955,
        wspace=1.05,
        hspace=0.80,
        height_ratios=[0.92, 1.12, 1.12],
    )

    ax_a = fig.add_subplot(outer[0, 0:4])
    ax_c = fig.add_subplot(outer[1:3, 0:4])
    b_grid = outer[0:2, 4:12].subgridspec(2, 1, height_ratios=[1.45, 1.0], hspace=0.05)
    ax_bv = fig.add_subplot(b_grid[0, 0])
    ax_bd = fig.add_subplot(b_grid[1, 0], sharex=ax_bv)
    ax_d = fig.add_subplot(outer[2, 4:12])

    draw_cell_strip(ax_a)
    draw_voltage_hero(ax_bv, ax_bd, vq, q_s, q_f)
    draw_rate_panel(ax_c, rate)
    draw_timing_panel(ax_d, timing, timing_primary, q_s, q_f)
    return fig, width_mm, height_mm


def export_figure(fig) -> None:
    title = "Existing full-cell records define the positive-electrode problem"
    creator = "R582_Fig1_experimental_problem.py"
    fixed_time = datetime(2026, 7, 20, tzinfo=timezone.utc)
    fig.savefig(
        BASE.with_suffix(".svg"),
        format="svg",
        metadata={"Title": title, "Creator": creator, "Date": "2026-07-20"},
    )
    fig.savefig(
        BASE.with_suffix(".pdf"),
        format="pdf",
        metadata={
            "Title": title,
            "Creator": creator,
            "Producer": "matplotlib",
            "CreationDate": fixed_time,
            "ModDate": fixed_time,
        },
    )
    fig.savefig(BASE.with_suffix(".png"), format="png", dpi=600)
    fig.savefig(
        BASE.with_suffix(".tiff"),
        format="tiff",
        dpi=600,
        pil_kwargs={"compression": "tiff_lzw"},
    )
    plt.close(fig)

    # Python-only grayscale rendering for print-safety inspection.
    with Image.open(BASE.with_suffix(".png")) as image:
        grey = image.convert("L")
        grey.save(
            FIGURE_DIR / "Fig_R582_experimental_problem_grayscale_QA.png",
            dpi=(300, 300),
            optimize=True,
        )


def write_build_record(width_mm: float, height_mm: float, audit: dict) -> None:
    outputs = [
        BASE.with_suffix(".svg"),
        BASE.with_suffix(".pdf"),
        BASE.with_suffix(".png"),
        BASE.with_suffix(".tiff"),
        FIGURE_DIR / "Fig_R582_experimental_problem_grayscale_QA.png",
        HERE / "R582_Fig1a_cell_strip.csv",
        HERE / "R582_Fig1b_selected_vq_dvdq.csv",
        HERE / "R582_Fig1c_rate_ladder.csv",
        HERE / "R582_Fig1d_feature_timing.csv",
        HERE / "R582_Fig1_input_manifest.csv",
    ]
    record = {
        "figure": "Fig_R582_experimental_problem",
        "core_conclusion": (
            "Existing full-cell records show a voltage-rise feature and rate-dependent utilization "
            "that motivate, but do not independently validate, a positive-electrode state model."
        ),
        "archetype": "asymmetric mixed-modality figure",
        "backend": "Python/matplotlib only",
        "font_audit": {
            "manuscript_text_family": "TeX Gyre Termes (tgtermes equivalent)",
            "resolved_matplotlib_family": FONT_FAMILY,
            "mathtext_configuration": "custom TeX Gyre Termes rm/it/bf/cal/sf; no fallback",
            "fallback_used": False,
            "registered_faces": [
                {"file": path.name, "sha256": sha256(path)} for path in TERMES_PATHS
            ],
        },
        "final_size_mm": {"width": width_mm, "height": height_mm},
        "statistical_unit": (
            "physical cell/file; cycles are repeated measures within one cell; full cycle ranges are descriptive"
        ),
        "derivative_method": (
            "registered 0.25 mAh cm^-2 grid; cubic Savitzky-Golay derivative; "
            "10.25 mAh cm^-2 primary window; 5.25 and 15.25 mAh cm^-2 sensitivity windows"
        ),
        "interpretation_boundary": (
            "full-cell voltage features are descriptive and model markers were not fitted to these traces"
        ),
        "metadata_correction": (
            "EXP-META-001: legacy NH4Cl/NH4CL labels denote NH4Br; raw names and bytes remain unchanged"
        ),
        "alignment_audit": audit,
        "inputs": [
            {
                "path": workspace_relative(path),
                "sha256": expected,
            }
            for path, expected in EXPECTED_SHA256.items()
        ],
        "generator": {
            "path": workspace_relative(Path(__file__).resolve()),
            "sha256": sha256(Path(__file__).resolve()),
        },
        "outputs": [
            {
                "path": workspace_relative(path),
                "size_bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
            for path in outputs
        ],
    }
    (HERE / "R582_Fig1_build.json").write_text(
        json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def main() -> None:
    vq, rate, timing, timing_primary, q_s, q_f, audit = read_and_derive()
    fig, width_mm, height_mm = build_figure(vq, rate, timing, timing_primary, q_s, q_f)
    export_figure(fig)
    write_build_record(width_mm, height_mm, audit)
    print(f"Wrote {BASE}.{{svg,pdf,png,tiff}} and isolated source-data/QA records")


if __name__ == "__main__":
    main()
