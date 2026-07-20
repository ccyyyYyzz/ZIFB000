#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Render R582 Supplementary Figure S1 from frozen derivative records.

The four displayed cycles are sequential measurements from one physical cell.
They are never treated as independent replicates.  Every prespecified
Savitzky--Golay window is drawn on the same axes and derivative scale.
"""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.text import Text
import numpy as np
import pandas as pd
from PIL import Image


SOURCE_DATA_DIR = Path(__file__).resolve().parent.parent
if str(SOURCE_DATA_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DATA_DIR))
from r582_font_runtime import register_termes_fonts


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
FIGURE_DIR = PROJECT / "manuscript" / "figures_R582"
FIGURE_DIR.mkdir(parents=True, exist_ok=True)
BASE = FIGURE_DIR / "SIFig_R582_S1_derivative"

CURVES_SOURCE = (
    PROJECT
    / "battery_experiment"
    / "02_processed_data"
    / "R581_G4_DVDQ_REBUILD"
    / "dvdq_curves_all_windows.csv"
)
METRICS_SOURCE = CURVES_SOURCE.with_name("dvdq_metrics_by_cycle_and_window.csv")
ELIGIBLE_SOURCE = CURVES_SOURCE.with_name("eligible_cycles.csv")
EXPECTED_SHA256 = {
    CURVES_SOURCE: "AAADD2779474FE74C1F0F4BC472633B113967905CA2BCE2EF97FAF8F0CA7D2DE",
    METRICS_SOURCE: "7BB07D8E335B3E164C1E2BA1E42BF14FD6917E6A63CAFCBEC5F13BD0E7D5ECE3",
    ELIGIBLE_SOURCE: "1DFB2A1A857A27C017B360020865373DF9E018CA95B39CF596F231CBB6420D50",
}

CURVES_PLOT = HERE / "R582_SIFig_S1_plot_curves.csv"
LANDMARKS_PLOT = HERE / "R582_SIFig_S1_plot_landmarks.csv"
INPUT_MANIFEST = HERE / "R582_SIFig_S1_input_manifest.csv"
RENDER_MANIFEST = HERE / "R582_SIFig_S1_render_manifest.json"

TERMES_DIR, _TERMES_BY_ROLE, FONT_FAMILY = register_termes_fonts(font_manager)
TERMES_PATHS = list(_TERMES_BY_ROLE.values())

plt.rcParams.update(
    {
        "font.family": "serif",
        "font.serif": [FONT_FAMILY],
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
        "axes.unicode_minus": True,
        "svg.fonttype": "none",
        "svg.hashsalt": "R582_SIFig_S1_derivative",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "mathtext.fontset": "custom",
        "mathtext.rm": FONT_FAMILY,
        "mathtext.it": f"{FONT_FAMILY}:italic",
        "mathtext.bf": f"{FONT_FAMILY}:bold",
        "mathtext.cal": f"{FONT_FAMILY}:italic",
        "mathtext.sf": FONT_FAMILY,
        "mathtext.fallback": None,
        "savefig.facecolor": "white",
        "figure.facecolor": "white",
    }
)

NAVY = "#254F73"
CARMINE = "#A94C45"
TEAL = "#397A78"
INK = "#20252A"
MID_GREY = "#6D7378"
LIGHT_GREY = "#D9DDE0"
WHITE = "#FFFFFF"
WINDOW_STYLE = {
    5.25: {"color": CARMINE, "ls": (0, (1.4, 1.3)), "lw": 0.95},
    10.25: {"color": NAVY, "ls": "-", "lw": 1.25},
    15.25: {"color": TEAL, "ls": (0, (4.0, 1.8)), "lw": 1.00},
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def rel(path: Path) -> str:
    return path.resolve().relative_to(PROJECT.resolve()).as_posix()


def require_columns(frame: pd.DataFrame, columns: list[str], label: str) -> None:
    missing = sorted(set(columns) - set(frame.columns))
    if missing:
        raise ValueError(f"{label} missing columns: {missing}")


def verify_inputs() -> None:
    for path, expected in EXPECTED_SHA256.items():
        if not path.is_file():
            raise FileNotFoundError(path)
        observed = sha256(path)
        if observed != expected:
            raise ValueError(f"Frozen input hash mismatch for {path}: {observed}")
    manifest = pd.DataFrame(
        [
            {
                "source_key": path.stem,
                "path_workspace_relative": rel(path),
                "size_bytes": path.stat().st_size,
                "sha256": expected,
                "used_for": {
                    CURVES_SOURCE: "all eligible late-charge derivative curves",
                    METRICS_SOURCE: "prespecified onset and maximum coordinates",
                    ELIGIBLE_SOURCE: "one-cell cycle inclusion identity",
                }[path],
                "immutable_registered_input": True,
            }
            for path, expected in EXPECTED_SHA256.items()
        ]
    )
    manifest.to_csv(INPUT_MANIFEST, index=False, lineterminator="\n")


def load_and_freeze_plot_data() -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    verify_inputs()
    curves = pd.read_csv(CURVES_SOURCE)
    metrics = pd.read_csv(METRICS_SOURCE)
    eligible = pd.read_csv(ELIGIBLE_SOURCE)
    require_columns(
        curves,
        ["FileName", "pair_index", "window_mAh_cm2", "Q_mAh_cm2", "dVdQ_V_per_mAh_cm2"],
        "derivative curves",
    )
    require_columns(
        metrics,
        [
            "FileName",
            "pair_index",
            "independent_file_count",
            "repeated_cycle_count_in_file",
            "window_mAh_cm2",
            "primary_estimator",
            "rise_onset_Q_mAh_cm2",
            "peak_Q_mAh_cm2",
            "peak_dVdQ_V_per_mAh_cm2",
            "peak_right_censored",
        ],
        "derivative landmarks",
    )
    require_columns(eligible, ["FileName", "pair_index", "clean_for_curve", "StandardStrict"], "eligible cycles")

    cycles = [20, 21, 22, 23]
    windows = [5.25, 10.25, 15.25]
    eligible_ids = sorted(
        eligible.loc[
            eligible["clean_for_curve"].astype(str).str.lower().eq("true")
            & eligible["StandardStrict"].astype(str).str.lower().eq("true"),
            "pair_index",
        ].astype(int)
    )
    if eligible_ids != cycles:
        raise ValueError(f"Unexpected eligible cycle set: {eligible_ids}")
    if sorted(curves["pair_index"].unique().astype(int).tolist()) != cycles:
        raise ValueError("Curve cycle set differs from the frozen eligible set")
    if sorted(curves["window_mAh_cm2"].unique().astype(float).tolist()) != windows:
        raise ValueError("Curve window set differs from the three prespecified windows")
    if sorted(metrics["pair_index"].unique().astype(int).tolist()) != cycles or len(metrics) != 12:
        raise ValueError("Landmark table must contain four cycles by three windows")
    if curves["FileName"].nunique() != 1 or metrics["FileName"].nunique() != 1 or eligible["FileName"].nunique() != 1:
        raise ValueError("S1 must remain a one-physical-cell display")
    if not metrics["independent_file_count"].astype(int).eq(1).all():
        raise ValueError("Independent-file count must remain one")
    if not metrics["repeated_cycle_count_in_file"].astype(int).eq(4).all():
        raise ValueError("Repeated-cycle count must remain four")
    if metrics["peak_right_censored"].astype(str).str.lower().eq("true").any():
        raise ValueError("Unexpected right-censored maximum in the registered S1 metrics")

    curve_plot = curves[
        ["pair_index", "window_mAh_cm2", "Q_mAh_cm2", "dVdQ_V_per_mAh_cm2"]
    ].copy()
    curve_plot.insert(0, "cell_id", "G4_pristine_cell")
    curve_plot.insert(1, "supporting_electrolyte", "NH4Br")
    curve_plot["dVdQ_mV_per_mAh_cm2"] = 1000.0 * curve_plot["dVdQ_V_per_mAh_cm2"]
    curve_plot.to_csv(CURVES_PLOT, index=False, float_format="%.12g", lineterminator="\n")

    landmark_plot = metrics[
        [
            "pair_index",
            "window_mAh_cm2",
            "primary_estimator",
            "rise_onset_Q_mAh_cm2",
            "peak_Q_mAh_cm2",
            "peak_dVdQ_V_per_mAh_cm2",
            "peak_right_censored",
        ]
    ].copy()
    landmark_plot.insert(0, "cell_id", "G4_pristine_cell")
    landmark_plot.insert(1, "supporting_electrolyte", "NH4Br")
    landmark_plot["peak_dVdQ_mV_per_mAh_cm2"] = 1000.0 * landmark_plot[
        "peak_dVdQ_V_per_mAh_cm2"
    ]
    landmark_plot.to_csv(LANDMARKS_PLOT, index=False, float_format="%.12g", lineterminator="\n")

    audit = {
        "physical_cells": 1,
        "sequential_cycles": cycles,
        "prespecified_windows_mAh_cm2": windows,
        "curve_rows": int(len(curve_plot)),
        "landmark_rows": int(len(landmark_plot)),
        "display_Q_range_mAh_cm2": [40.0, 120.0],
        "shared_derivative_range_mV_per_mAh_cm2": [-35.0, 14.0],
        "independent_unit": "one physical cell; cycles are repeated measures",
    }
    return curve_plot, landmark_plot, audit


def style_axis(ax) -> None:
    ax.spines["left"].set_color(INK)
    ax.spines["bottom"].set_color(INK)
    ax.tick_params(colors=INK, direction="out", pad=2.0)
    ax.axhline(0.0, color=LIGHT_GREY, lw=0.7, zorder=0)


def add_panel_label(ax, label: str) -> None:
    ax.text(
        -0.105,
        1.055,
        label,
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=8.0,
        fontweight="bold",
        color=INK,
    )


def adjusted_label_positions(values: dict[float, float]) -> dict[float, float]:
    ordered = sorted(values, key=lambda key: values[key])
    result: dict[float, float] = {}
    lower, upper, gap = -31.0, 10.5, 4.2
    cursor = lower
    for key in ordered:
        target = max(values[key], cursor)
        result[key] = min(target, upper)
        cursor = result[key] + gap
    if result[ordered[-1]] > upper:
        shift = result[ordered[-1]] - upper
        result = {key: value - shift for key, value in result.items()}
    if result[ordered[0]] < lower:
        shift = lower - result[ordered[0]]
        result = {key: value + shift for key, value in result.items()}
    return result


def draw_cycle(ax, cycle: int, curves: pd.DataFrame, landmarks: pd.DataFrame, label: str) -> None:
    style_axis(ax)
    add_panel_label(ax, label)
    ax.set_title(f"Cycle {cycle}", loc="left", pad=3.0)
    sub = curves.loc[curves["pair_index"].astype(int).eq(cycle)]
    end_values: dict[float, float] = {}
    end_points: dict[float, tuple[float, float]] = {}
    for window in [5.25, 10.25, 15.25]:
        style = WINDOW_STYLE[window]
        line = sub.loc[sub["window_mAh_cm2"].astype(float).eq(window)].sort_values("Q_mAh_cm2")
        ax.plot(
            line["Q_mAh_cm2"],
            line["dVdQ_mV_per_mAh_cm2"],
            color=style["color"],
            ls=style["ls"],
            lw=style["lw"],
            solid_capstyle="round",
            zorder=2 if window != 10.25 else 3,
        )
        row = landmarks.loc[
            landmarks["pair_index"].astype(int).eq(cycle)
            & landmarks["window_mAh_cm2"].astype(float).eq(window)
        ].iloc[0]
        onset_q = float(row["rise_onset_Q_mAh_cm2"])
        peak_q = float(row["peak_Q_mAh_cm2"])
        q_values = line["Q_mAh_cm2"].to_numpy(float)
        y_values = line["dVdQ_mV_per_mAh_cm2"].to_numpy(float)
        onset_y = float(np.interp(onset_q, q_values, y_values))
        peak_y = float(np.interp(peak_q, q_values, y_values))
        ax.plot(onset_q, onset_y, marker="o", ms=3.7, mfc=WHITE, mec=style["color"], mew=0.9, ls="", zorder=5)
        ax.plot(peak_q, peak_y, marker="^", ms=4.3, mfc=style["color"], mec=WHITE, mew=0.45, ls="", zorder=6)
        tail = line.loc[line["Q_mAh_cm2"] >= line["Q_mAh_cm2"].max() - 0.5]
        end_y = float(tail["dVdQ_mV_per_mAh_cm2"].mean())
        end_x = float(line["Q_mAh_cm2"].max())
        end_values[window] = end_y
        end_points[window] = (end_x, end_y)

    label_y = adjusted_label_positions(end_values)
    for window in [5.25, 10.25, 15.25]:
        style = WINDOW_STYLE[window]
        x0, y0 = end_points[window]
        ax.plot([x0, 121.4], [y0, label_y[window]], color=style["color"], lw=0.65, ls=style["ls"], clip_on=False)
        ax.text(
            122.0,
            label_y[window],
            f"{window:.2f}",
            ha="left",
            va="center",
            fontsize=6.5,
            color=style["color"],
            fontweight="bold" if window == 10.25 else "normal",
        )

    ax.set_xlim(40.0, 130.0)
    ax.set_ylim(-35.0, 14.0)
    ax.set_xticks([40, 60, 80, 100, 120])
    ax.set_yticks([-30, -15, 0, 12])


def audit_figure_text(fig) -> dict:
    fig.canvas.draw()
    texts = [item for item in fig.findobj(match=Text) if item.get_text().strip()]
    sizes = [float(item.get_fontsize()) for item in texts]
    families = sorted({item.get_fontproperties().get_name() for item in texts})
    if min(sizes) < 6.5 - 1e-9:
        raise ValueError(f"Figure contains text below 6.5 pt: {min(sizes)}")
    if families != [FONT_FAMILY]:
        raise ValueError(f"Unexpected resolved font families: {families}")
    return {"minimum_text_pt": min(sizes), "resolved_font_families": families, "text_items": len(texts)}


def build_figure(curves: pd.DataFrame, landmarks: pd.DataFrame) -> tuple[plt.Figure, dict]:
    width_mm, height_mm = 180.0, 122.0
    fig, axes = plt.subplots(2, 2, figsize=(width_mm / 25.4, height_mm / 25.4), sharex=True, sharey=True)
    fig.subplots_adjust(left=0.083, right=0.985, bottom=0.145, top=0.885, wspace=0.18, hspace=0.28)
    for ax, cycle, label in zip(axes.ravel(), [20, 21, 22, 23], ["a", "b", "c", "d"]):
        draw_cycle(ax, cycle, curves, landmarks, label)
    axes[0, 0].set_ylabel("dV/dQ (mV per mAh cm−2)")
    axes[1, 0].set_ylabel("dV/dQ (mV per mAh cm−2)")
    axes[1, 0].set_xlabel("Areal charge capacity, Q (mAh cm−2)")
    axes[1, 1].set_xlabel("Areal charge capacity, Q (mAh cm−2)")
    fig.text(0.083, 0.955, "One physical cell; four sequential charge cycles", ha="left", va="top", fontsize=7.5, fontweight="bold", color=INK)
    fig.text(0.985, 0.955, "window (mAh cm−2)", ha="right", va="top", fontsize=6.5, color=MID_GREY)
    fig.text(0.083, 0.035, "Open circle: threshold onset   Filled triangle: registered search-window maximum", ha="left", va="bottom", fontsize=6.5, color=MID_GREY)
    fig.text(0.985, 0.035, "All panels share the same derivative scale", ha="right", va="bottom", fontsize=6.5, color=MID_GREY)
    font_audit = audit_figure_text(fig)
    return fig, {"width_mm": width_mm, "height_mm": height_mm, "font_audit": font_audit}


def export_figure(fig: plt.Figure) -> None:
    fixed_time = datetime(2026, 7, 20, tzinfo=timezone.utc)
    title = "Derivative-window sensitivity across sequential cycles of one cell"
    creator = Path(__file__).name
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
    fig.savefig(BASE.with_suffix(".png"), format="png", dpi=600, transparent=False)
    plt.close(fig)

    with Image.open(BASE.with_suffix(".png")) as image:
        rgb = image.convert("RGB")
        rgb.save(BASE.with_suffix(".tiff"), format="TIFF", compression="tiff_lzw", dpi=(600, 600))
        preview_width = round(180.0 / 25.4 * 300.0)
        preview_height = round(rgb.height * preview_width / rgb.width)
        preview = rgb.resize((preview_width, preview_height), Image.Resampling.LANCZOS)
        preview.save(FIGURE_DIR / f"{BASE.name}_180mm_preview.png", dpi=(300, 300), optimize=True)
        preview.convert("L").save(
            FIGURE_DIR / f"{BASE.name}_180mm_preview_grayscale.png",
            dpi=(300, 300),
            optimize=True,
        )


def write_render_manifest(figure_audit: dict, data_audit: dict) -> None:
    figure_outputs = [
        BASE.with_suffix(".svg"),
        BASE.with_suffix(".pdf"),
        BASE.with_suffix(".png"),
        BASE.with_suffix(".tiff"),
        FIGURE_DIR / f"{BASE.name}_180mm_preview.png",
        FIGURE_DIR / f"{BASE.name}_180mm_preview_grayscale.png",
    ]
    bundle_outputs = sorted(
        path for path in HERE.iterdir() if path.is_file() and path.resolve() != RENDER_MANIFEST.resolve()
    )
    record = {
        "figure": BASE.name,
        "single_dominant_claim": (
            "The late-charge derivative feature is distributed across sequential cycles, and its reported "
            "coordinates depend on the prespecified derivative window."
        ),
        "evidence_class": "E-EXP",
        "frozen_date": "2026-07-20",
        "final_size_mm": {"width": figure_audit["width_mm"], "height": figure_audit["height_mm"]},
        "font": {
            "family": FONT_FAMILY,
            "base_pt": 7.2,
            "minimum_pt": 6.5,
            "panel_label_pt": 8.0,
            "registered_faces": [{"path": str(path), "sha256": sha256(path)} for path in TERMES_PATHS],
            **figure_audit["font_audit"],
        },
        "statistical_boundary": (
            "One physical cell; cycles 20-23 are sequential repeated measures and are not independent replicates."
        ),
        "display_boundary": (
            "The plotted Q range is the late-charge interval 40-120 mAh cm^-2; all curve rows remain in the plot table."
        ),
        "metadata_normalization": "Derived labels use NH4Br under EXP-META-001; immutable raw bytes are untouched.",
        "data_audit": data_audit,
        "inputs": [
            {"path": rel(path), "size_bytes": path.stat().st_size, "sha256": expected}
            for path, expected in EXPECTED_SHA256.items()
        ],
        "figure_outputs": [
            {"path": rel(path), "size_bytes": path.stat().st_size, "sha256": sha256(path)}
            for path in figure_outputs
        ],
        "source_bundle_files": [
            {"path": rel(path), "size_bytes": path.stat().st_size, "sha256": sha256(path)}
            for path in bundle_outputs
        ],
    }
    RENDER_MANIFEST.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    curves, landmarks, data_audit = load_and_freeze_plot_data()
    fig, figure_audit = build_figure(curves, landmarks)
    export_figure(fig)
    write_render_manifest(figure_audit, data_audit)
    print(f"Wrote {BASE}.{{svg,pdf,png,tiff}} with deterministic source records")


if __name__ == "__main__":
    main()
