#!/usr/bin/env python3
"""Build R582 main Figure 4: accessibility closure and identifiability.

The script is deterministic and Python-only. It reads registered R581 matched
true-mesh trajectories and the registered R538 reduced observation-layer
degeneracy table, validates their identities, writes clean plotted-source CSVs,
and exports an exact-size 180 mm figure plus true-size and grayscale QA renders.

No original experiment or COMSOL model file is opened or modified.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import matplotlib as mpl

mpl.use("Agg", force=True)
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd
from PIL import Image


FIGURE_STEM = "Fig_R582_closure_identifiability"
WIDTH_MM = 180.0
HEIGHT_MM = 118.0
RASTER_DPI = 600
PREVIEW_DPI = 300
STABLE_DATE = datetime(2026, 7, 20, tzinfo=timezone.utc)

# Locked ZIFB_W visual grammar.
GRAPHITE = "#4D4D4D"
VERMILION = "#D65345"
BLUE = "#3B6FB6"
TEAL = "#2A9D8F"
VIOLET = "#7A68A6"
AMBER = "#D8912B"
NEUTRAL = "#6F6F6F"
GUIDE = "#E4E1DC"
WHITE = "#FFFFFF"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def write_csv(frame: pd.DataFrame, path: Path) -> None:
    frame.to_csv(path, index=False, float_format="%.12g", lineterminator="\n")


def relative_path(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def lookup_summary(frame: pd.DataFrame, quantity: str) -> float:
    rows = frame.loc[frame["quantity"].eq(quantity), "value"]
    require(len(rows) == 1, f"Expected one summary value for {quantity!r}")
    return float(rows.iloc[0])


def lookup_marker(frame: pd.DataFrame, marker_id: str) -> pd.Series:
    rows = frame.loc[frame["marker_id"].eq(marker_id)]
    require(len(rows) == 1, f"Expected one marker row for {marker_id!r}")
    return rows.iloc[0]


def parse_production_authority(project_truth: str) -> dict[str, str]:
    pattern = re.compile(
        r"Authoritative production branch:\s*`(?P<branch>[^`]+)`,\s*"
        r"input MPH SHA-256\s*`(?P<sha>[A-Fa-f0-9]{64})`,\s*"
        r"study\s*`(?P<study>[^`]+)`,\s*solution\s*`(?P<solution>[^`]+)`,\s*"
        r"dataset\s*`(?P<dataset>[^`]+)`"
    )
    match = pattern.search(project_truth)
    require(match is not None, "Could not parse production authority from project truth")
    parsed = match.groupdict()
    parsed["sha"] = parsed["sha"].upper()
    return parsed


def discover_termes_fonts() -> tuple[str, dict[str, Path], str | None]:
    """Register TeX Gyre Termes; permit Times New Roman only as fallback."""
    filenames = {
        "regular": "texgyretermes-regular.otf",
        "bold": "texgyretermes-bold.otf",
        "italic": "texgyretermes-italic.otf",
        "bolditalic": "texgyretermes-bolditalic.otf",
    }
    found: dict[str, Path] = {}

    kpsewhich = shutil.which("kpsewhich")
    if kpsewhich:
        for role, filename in filenames.items():
            result = subprocess.run(
                [kpsewhich, filename], capture_output=True, text=True, check=False
            )
            candidate = Path(result.stdout.strip()) if result.stdout.strip() else None
            if candidate and candidate.is_file():
                found[role] = candidate.resolve()

    search_roots = [
        Path("D:/Program Files/texlive"),
        Path("C:/texlive"),
    ]
    if len(found) != len(filenames):
        for root in search_roots:
            if not root.exists():
                continue
            for role, filename in filenames.items():
                if role in found:
                    continue
                matches = sorted(root.glob(f"*/texmf-dist/fonts/opentype/public/tex-gyre/{filename}"))
                if matches:
                    found[role] = matches[-1].resolve()

    if len(found) == len(filenames):
        for path in found.values():
            font_manager.fontManager.addfont(str(path))
        family = font_manager.FontProperties(fname=str(found["regular"])).get_name()
        require(family == "TeX Gyre Termes", f"Unexpected Termes family name: {family}")
        return family, found, None

    windows_fonts = Path("C:/Windows/Fonts")
    fallback_files = {
        "regular": windows_fonts / "times.ttf",
        "bold": windows_fonts / "timesbd.ttf",
        "italic": windows_fonts / "timesi.ttf",
        "bolditalic": windows_fonts / "timesbi.ttf",
    }
    require(
        all(path.is_file() for path in fallback_files.values()),
        "Neither TeX Gyre Termes nor the allowed Times New Roman fallback is available",
    )
    for path in fallback_files.values():
        font_manager.fontManager.addfont(str(path))
    family = font_manager.FontProperties(fname=str(fallback_files["regular"])).get_name()
    return family, fallback_files, "TeX Gyre Termes unavailable; used Times New Roman fallback"


def configure_matplotlib() -> dict[str, Any]:
    family, font_paths, fallback_note = discover_termes_fonts()
    mpl.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": [family],
            "font.size": 7.2,
            "axes.titlesize": 7.4,
            "axes.titleweight": "bold",
            "axes.labelsize": 7.0,
            "axes.linewidth": 0.8,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "xtick.labelsize": 6.6,
            "ytick.labelsize": 6.6,
            "xtick.major.width": 0.7,
            "ytick.major.width": 0.7,
            "xtick.major.size": 2.8,
            "ytick.major.size": 2.8,
            "legend.fontsize": 6.7,
            "legend.frameon": False,
            "lines.linewidth": 1.35,
            "svg.fonttype": "none",
            "svg.hashsalt": "R582-Fig4-closure-identifiability-v1",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "mathtext.fontset": "custom",
            "mathtext.rm": family,
            "mathtext.it": f"{family}:italic",
            "mathtext.bf": f"{family}:bold",
            "mathtext.sf": family,
            "axes.unicode_minus": True,
            "figure.facecolor": WHITE,
            "savefig.facecolor": WHITE,
            "savefig.transparent": False,
        }
    )
    return {
        "family": family,
        "font_paths": {role: str(path) for role, path in font_paths.items()},
        "font_sha256": {role: sha256(path) for role, path in font_paths.items()},
        "fallback_note": fallback_note,
    }


def style_axis(ax: mpl.axes.Axes, guides: bool = True) -> None:
    ax.tick_params(direction="out", color=GRAPHITE, labelcolor="#252525")
    ax.spines["left"].set_color(GRAPHITE)
    ax.spines["bottom"].set_color(GRAPHITE)
    if guides:
        ax.grid(axis="y", color=GUIDE, lw=0.45, alpha=0.9, zorder=0)
    ax.set_axisbelow(True)


def add_panel_label(ax: mpl.axes.Axes, label: str, x: float) -> None:
    ax.text(
        x,
        1.055,
        label,
        transform=ax.transAxes,
        fontsize=8.3,
        fontweight="bold",
        ha="left",
        va="bottom",
        clip_on=False,
    )


def build_derived_tables(
    comparison: pd.DataFrame,
    summary: dict[str, Any],
    thresholds: pd.DataFrame,
    degeneracy: pd.DataFrame,
    reanchor: pd.DataFrame,
    source_dir: Path,
) -> dict[str, Path]:
    q = comparison["q_mAh_cm2"].to_numpy(float)
    a_control = 1.0 - comparison["theta_control"].to_numpy(float)
    a_shadow = 1.0 - comparison["theta_dense_shadow_on_control"].to_numpy(float)
    a_coupled = 1.0 - comparison["theta_physical_dense"].to_numpy(float)
    a0_control, a0_shadow, a0_coupled = a_control[0], a_shadow[0], a_coupled[0]
    trajectories = pd.DataFrame(
        {
            "Q_mAh_cm2": q,
            "A_bare_over_A0_baseline": a_control / a0_control,
            "A_bare_over_A0_one_way_island_shadow": a_shadow / a0_shadow,
            "A_bare_over_A0_coupled_island": a_coupled / a0_coupled,
            "V_baseline_V": comparison["V_control_V"].to_numpy(float),
            "V_coupled_island_V": comparison["V_physical_dense_V"].to_numpy(float),
            "deltaV_island_minus_baseline_mV": 1000.0
            * comparison["deltaV_physical_minus_control_V"].to_numpy(float),
            "eps_s_baseline": comparison["eps_s_control"].to_numpy(float),
            "eps_s_coupled_island": comparison["eps_s_physical_dense"].to_numpy(float),
        }
    )

    qf_row = lookup_marker(thresholds, "Q_f_cal")
    eps_cal_row = lookup_marker(thresholds, "eps_s_cal_traj")
    eps_island_row = lookup_marker(thresholds, "eps_s_island_half")
    references = pd.DataFrame(
        [
            {
                "reference_id": "baseline_half_area_capacity",
                "value": float(qf_row["value"]),
                "unit": str(qf_row["unit"]),
                "meaning": "first baseline accessibility-loss crossing at theta=0.5",
                "source_marker_id": str(qf_row["marker_id"]),
            },
            {
                "reference_id": "baseline_half_area_solid_fraction",
                "value": float(eps_cal_row["value"]),
                "unit": str(eps_cal_row["unit"]),
                "meaning": "baseline solid-I2 fraction read at the baseline half-area capacity",
                "source_marker_id": str(eps_cal_row["marker_id"]),
            },
            {
                "reference_id": "island_model_half_area_solid_fraction",
                "value": float(eps_island_row["value"]),
                "unit": str(eps_island_row["unit"]),
                "meaning": "half-area reference of the registered dense island relation",
                "source_marker_id": str(eps_island_row["marker_id"]),
            },
        ]
    )

    access_voltage_v = lookup_summary(reanchor, "R_access_mV") / 1000.0
    theta_grid = np.linspace(float(degeneracy["theta_end"].min()), float(degeneracy["theta_end"].max()), 301)
    area_grid = 1.0 - theta_grid
    b_t = access_voltage_v / np.log(1.0 / area_grid)
    degeneracy_curve = pd.DataFrame(
        {
            "theta_end": theta_grid,
            "A_bare_end_over_A0": area_grid,
            "effective_coefficient_V": b_t,
            "effective_slope_mV_dec": b_t * math.log(10.0) * 1000.0,
            "fixed_accessibility_voltage_contribution_mV": access_voltage_v * 1000.0,
        }
    ).sort_values("A_bare_end_over_A0")
    degeneracy_points = degeneracy.rename(
        columns={
            "A_bare_end": "A_bare_end_over_A0",
            "bT_needed_V": "effective_coefficient_V",
            "tafel_mV_dec": "effective_slope_mV_dec",
        }
    ).copy()
    degeneracy_points["fixed_accessibility_voltage_contribution_mV"] = access_voltage_v * 1000.0

    q_s_control = float(summary["control"]["Q_s_mAh_cm2"])
    q_s_coupled = float(summary["physical_dense"]["Q_s_mAh_cm2"])
    endpoints = pd.DataFrame(
        [
            {
                "series": "baseline simulation",
                "feedback_solve": True,
                "inventory_source": "own solved eps_s(Q)",
                "Q_s_mAh_cm2": q_s_control,
                "Q_half_area_mAh_cm2": float(summary["control"]["Q_theta_0p5_mAh_cm2"]),
                "endpoint_A_bare_over_A0": float(trajectories["A_bare_over_A0_baseline"].iloc[-1]),
                "endpoint_eps_s": float(comparison["eps_s_control"].iloc[-1]),
                "endpoint_voltage_V": float(comparison["V_control_V"].iloc[-1]),
            },
            {
                "series": "one-way island shadow",
                "feedback_solve": False,
                "inventory_source": "baseline eps_s(Q)",
                "Q_s_mAh_cm2": q_s_control,
                "Q_half_area_mAh_cm2": float(summary["one_way_dense_shadow"]["Q_theta_0p5_mAh_cm2"]),
                "endpoint_A_bare_over_A0": float(trajectories["A_bare_over_A0_one_way_island_shadow"].iloc[-1]),
                "endpoint_eps_s": float(comparison["eps_s_control"].iloc[-1]),
                "endpoint_voltage_V": np.nan,
            },
            {
                "series": "coupled island-model variant",
                "feedback_solve": True,
                "inventory_source": "own solved eps_s(Q)",
                "Q_s_mAh_cm2": q_s_coupled,
                "Q_half_area_mAh_cm2": np.nan,
                "endpoint_A_bare_over_A0": float(trajectories["A_bare_over_A0_coupled_island"].iloc[-1]),
                "endpoint_eps_s": float(comparison["eps_s_physical_dense"].iloc[-1]),
                "endpoint_voltage_V": float(comparison["V_physical_dense_V"].iloc[-1]),
            },
        ]
    )

    paths = {
        "trajectories": source_dir / f"{FIGURE_STEM}_trajectories.csv",
        "reference_levels": source_dir / f"{FIGURE_STEM}_reference_levels.csv",
        "degeneracy_curve": source_dir / f"{FIGURE_STEM}_degeneracy_curve.csv",
        "degeneracy_points": source_dir / f"{FIGURE_STEM}_degeneracy_source_points.csv",
        "endpoint_summary": source_dir / f"{FIGURE_STEM}_endpoint_summary.csv",
    }
    write_csv(trajectories, paths["trajectories"])
    write_csv(references, paths["reference_levels"])
    write_csv(degeneracy_curve, paths["degeneracy_curve"])
    write_csv(degeneracy_points, paths["degeneracy_points"])
    write_csv(endpoints, paths["endpoint_summary"])
    return paths


def create_figure(
    trajectories: pd.DataFrame,
    references: pd.DataFrame,
    degeneracy_curve: pd.DataFrame,
    degeneracy_points: pd.DataFrame,
    summary: dict[str, Any],
    reanchor: pd.DataFrame,
) -> mpl.figure.Figure:
    q = trajectories["Q_mAh_cm2"].to_numpy(float)
    a_control = trajectories["A_bare_over_A0_baseline"].to_numpy(float)
    a_shadow = trajectories["A_bare_over_A0_one_way_island_shadow"].to_numpy(float)
    a_coupled = trajectories["A_bare_over_A0_coupled_island"].to_numpy(float)
    v_control = trajectories["V_baseline_V"].to_numpy(float)
    v_coupled = trajectories["V_coupled_island_V"].to_numpy(float)
    delta_mv = trajectories["deltaV_island_minus_baseline_mV"].to_numpy(float)
    eps_control = 1000.0 * trajectories["eps_s_baseline"].to_numpy(float)
    eps_coupled = 1000.0 * trajectories["eps_s_coupled_island"].to_numpy(float)

    def ref_value(reference_id: str) -> float:
        rows = references.loc[references["reference_id"].eq(reference_id), "value"]
        require(len(rows) == 1, f"Missing derived reference {reference_id}")
        return float(rows.iloc[0])

    fig = plt.figure(figsize=(WIDTH_MM / 25.4, HEIGHT_MM / 25.4))
    grid = fig.add_gridspec(
        2,
        12,
        height_ratios=[1.30, 0.82],
        left=0.075,
        right=0.985,
        top=0.885,
        bottom=0.120,
        hspace=0.50,
        wspace=1.65,
    )
    ax_a = fig.add_subplot(grid[0, :4])
    b_grid = grid[0, 4:].subgridspec(2, 1, height_ratios=[2.85, 1.08], hspace=0.08)
    ax_b = fig.add_subplot(b_grid[0, 0])
    ax_db = fig.add_subplot(b_grid[1, 0], sharex=ax_b)
    ax_c = fig.add_subplot(grid[1, :7])
    ax_d = fig.add_subplot(grid[1, 8:])

    baseline_style = dict(color=VERMILION, lw=1.55, zorder=4)
    shadow_style = dict(color=BLUE, lw=1.35, ls=(0, (4.0, 2.2)), zorder=3)
    coupled_style = dict(
        color=GRAPHITE,
        lw=1.40,
        marker="s",
        markevery=180,
        ms=2.25,
        mec=WHITE,
        mew=0.35,
        zorder=4,
    )

    # a — intuitive remaining-area direction.
    ax_a.plot(q, a_control, **baseline_style)
    ax_a.plot(q, a_shadow, **shadow_style)
    ax_a.plot(q, a_coupled, **coupled_style)
    for value, color, marker, dy in (
        (a_control[-1], VERMILION, "o", 0.035),
        (a_shadow[-1], BLUE, "D", -0.015),
        (a_coupled[-1], GRAPHITE, "s", 0.020),
    ):
        ax_a.scatter([q[-1]], [value], s=16, marker=marker, color=color,
                     edgecolor=WHITE, linewidth=0.45, zorder=6, clip_on=False)
        ax_a.text(115.5, value + dy, f"{value:.3f}", color=color, fontsize=6.5,
                  ha="right", va="center")
    q_s_control = float(summary["control"]["Q_s_mAh_cm2"])
    q_s_coupled = float(summary["physical_dense"]["Q_s_mAh_cm2"])
    delta_q_s = abs(q_s_coupled - q_s_control)
    ax_a.plot([0.055, 0.12], [0.095, 0.095], transform=ax_a.transAxes,
              color=AMBER, lw=1.3, solid_capstyle="round", clip_on=False)
    ax_a.text(0.145, 0.095,
              rf"$\Delta Q_{{\mathrm{{s}}}}={delta_q_s:.3f}$ mAh cm$^{{-2}}$",
              transform=ax_a.transAxes, color=AMBER, fontsize=6.5,
              ha="left", va="center")
    ax_a.set(xlim=(0, 121), ylim=(-0.02, 1.035),
             xlabel=r"areal capacity, $Q$ (mAh cm$^{-2}$)",
             ylabel=r"remaining area, $A_{\mathrm{bare}}/A_0$")
    ax_a.set_xticks([0, 40, 80, 120])
    ax_a.set_yticks([0, 0.5, 1.0])
    ax_a.set_title("Remaining accessible area", loc="left", pad=5)
    style_axis(ax_a)
    add_panel_label(ax_a, "a", -0.20)

    # b — dominant matched voltage response and aligned difference.
    ax_b.plot(q, v_control, **baseline_style)
    ax_b.plot(q, v_coupled, **coupled_style)
    ax_b.scatter([q[-1]], [v_control[-1]], s=18, marker="o", color=VERMILION,
                 edgecolor=WHITE, linewidth=0.45, zorder=6, clip_on=False)
    ax_b.scatter([q[-1]], [v_coupled[-1]], s=18, marker="s", color=GRAPHITE,
                 edgecolor=WHITE, linewidth=0.45, zorder=6, clip_on=False)
    ax_b.text(117.0, v_control[-1] - 0.010, f"{v_control[-1]:.3f} V",
              color=VERMILION, fontsize=6.5, ha="right", va="top")
    ax_b.text(117.0, v_coupled[-1] + 0.010, f"{v_coupled[-1]:.3f} V",
              color=GRAPHITE, fontsize=6.5, ha="right", va="bottom")
    ax_b.set(xlim=(0, 121), ylim=(1.385, 1.755), ylabel="voltage (V)")
    ax_b.set_yticks([1.4, 1.5, 1.6, 1.7])
    ax_b.tick_params(labelbottom=False)
    ax_b.set_title("Matched voltage response", loc="left", pad=5)
    style_axis(ax_b)
    add_panel_label(ax_b, "b", -0.095)

    ax_db.axhline(0.0, color="#B9B5AF", lw=0.65, zorder=1)
    ax_db.fill_between(q, delta_mv, 0.0, color=VIOLET, alpha=0.10, linewidth=0, zorder=1)
    ax_db.plot(q, delta_mv, color=VIOLET, lw=1.45, zorder=4)
    endpoint_delta = float(summary["matched_difference"]["endpoint_deltaV_mV"])
    ax_db.scatter([q[-1]], [endpoint_delta], s=18, color=VIOLET,
                  edgecolor=WHITE, linewidth=0.45, zorder=6, clip_on=False)
    ax_db.annotate(
        f"{endpoint_delta:.1f} mV",
        xy=(q[-1], endpoint_delta),
        xytext=(99.0, -230.0),
        color=VIOLET,
        fontsize=7.0,
        fontweight="bold",
        ha="left",
        va="center",
        arrowprops={"arrowstyle": "-", "color": VIOLET, "lw": 0.75},
    )
    ax_db.text(2.5, -56, "island − baseline", color=NEUTRAL, fontsize=6.5,
               ha="left", va="center")
    ax_db.set(xlim=(0, 121), ylim=(-315, 18),
              xlabel=r"areal capacity, $Q$ (mAh cm$^{-2}$)",
              ylabel=r"$\Delta V$ (mV)")
    ax_db.set_xticks([0, 30, 60, 90, 120])
    ax_db.set_yticks([-300, -150, 0])
    style_axis(ax_db, guides=False)

    # c — separate solved solid inventories; only two relevant reference levels.
    ax_c.plot(q, eps_control, **baseline_style)
    ax_c.plot(q, eps_coupled, **coupled_style)
    ax_c.scatter([q[-1]], [eps_control[-1]], s=18, marker="o", color=VERMILION,
                 edgecolor=WHITE, linewidth=0.45, zorder=6, clip_on=False)
    ax_c.scatter([q[-1]], [eps_coupled[-1]], s=18, marker="s", color=GRAPHITE,
                 edgecolor=WHITE, linewidth=0.45, zorder=6, clip_on=False)
    eps_mid = 1000.0 * ref_value("baseline_half_area_solid_fraction")
    eps_island = 1000.0 * ref_value("island_model_half_area_solid_fraction")
    ax_c.axhline(eps_mid, color=VERMILION, lw=0.75, ls=(0, (1.5, 2.0)), alpha=0.75)
    ax_c.axhline(eps_island, color=BLUE, lw=0.85, ls=(0, (4.0, 2.2)), alpha=0.82)
    ax_c.text(3.0, eps_mid + 0.10,
              rf"baseline half-area inventory  {eps_mid:.3f} × 10$^{{-3}}$",
              color=VERMILION, fontsize=6.5, ha="left", va="bottom")
    ax_c.text(3.0, eps_island + 0.10,
              rf"island half-area reference  {eps_island:.3f} × 10$^{{-3}}$",
              color=BLUE, fontsize=6.5, ha="left", va="bottom")
    ax_c.text(116.0, eps_control[-1], f"{eps_control[-1]:.3f}",
              color=VERMILION, fontsize=6.5, ha="right", va="bottom")
    ax_c.text(116.0, eps_coupled[-1], f"{eps_coupled[-1]:.3f}",
              color=GRAPHITE, fontsize=6.5, ha="right", va="bottom")
    ax_c.set(xlim=(0, 121), ylim=(-0.03, 3.36),
             xlabel=r"areal capacity, $Q$ (mAh cm$^{-2}$)",
             ylabel=r"solid-I$_2$ fraction, $\varepsilon_s$ (×10$^{-3}$)")
    ax_c.set_xticks([0, 40, 80, 120])
    ax_c.set_yticks([0, 1, 2, 3])
    ax_c.set_title("Retained solid inventory", loc="left", pad=5)
    style_axis(ax_c)
    add_panel_label(ax_c, "c", -0.12)

    # d — a compact accessibility–coefficient degeneracy curve.
    x_curve = degeneracy_curve["A_bare_end_over_A0"].to_numpy(float)
    y_curve = degeneracy_curve["effective_slope_mV_dec"].to_numpy(float)
    ax_d.plot(x_curve, y_curve, color=TEAL, lw=1.50, zorder=3)
    ax_d.scatter(
        degeneracy_points["A_bare_end_over_A0"],
        degeneracy_points["effective_slope_mV_dec"],
        s=14,
        facecolor=WHITE,
        edgecolor=TEAL,
        linewidth=0.8,
        zorder=5,
    )
    baseline_point = degeneracy_points.loc[
        degeneracy_points["A_bare_end_over_A0"].idxmin()
    ]
    shadow_endpoint = float(a_shadow[-1])
    island_idx = (degeneracy_points["A_bare_end_over_A0"] - shadow_endpoint).abs().idxmin()
    island_point = degeneracy_points.loc[island_idx]
    ax_d.scatter([baseline_point["A_bare_end_over_A0"]],
                 [baseline_point["effective_slope_mV_dec"]],
                 s=24, marker="o", color=VERMILION, edgecolor=WHITE,
                 linewidth=0.55, zorder=7)
    ax_d.scatter([island_point["A_bare_end_over_A0"]],
                 [island_point["effective_slope_mV_dec"]],
                 s=26, marker="D", color=BLUE, edgecolor=WHITE,
                 linewidth=0.55, zorder=7)
    ax_d.annotate(
        "baseline calibration",
        xy=(float(baseline_point["A_bare_end_over_A0"]),
            float(baseline_point["effective_slope_mV_dec"])),
        xytext=(0.085, 72),
        color=VERMILION,
        fontsize=6.5,
        ha="left",
        va="bottom",
        arrowprops={"arrowstyle": "-", "color": VERMILION, "lw": 0.65},
    )
    ax_d.annotate(
        "island reference",
        xy=(float(island_point["A_bare_end_over_A0"]),
            float(island_point["effective_slope_mV_dec"])),
        xytext=(0.43, 132),
        color=BLUE,
        fontsize=6.5,
        ha="left",
        va="top",
        arrowprops={"arrowstyle": "-", "color": BLUE, "lw": 0.65},
    )
    access_mv = lookup_summary(reanchor, "R_access_mV")
    ax_d.text(0.025, 0.965, f"fixed voltage contribution: {access_mv:.1f} mV",
              transform=ax_d.transAxes, color=NEUTRAL, fontsize=6.5,
              ha="left", va="top")
    ax_d.set(xlim=(0, 0.64), ylim=(0, 340),
             xlabel=r"end-of-charge area, $A_{\mathrm{bare}}/A_0$",
             ylabel=r"effective slope (mV dec$^{-1}$)")
    ax_d.set_xticks([0, 0.2, 0.4, 0.6])
    ax_d.set_yticks([0, 100, 200, 300])
    ax_d.set_title("Accessibility–coefficient trade-off", loc="left", pad=5)
    style_axis(ax_d)
    add_panel_label(ax_d, "d", -0.18)

    handles = [
        Line2D([0], [0], color=VERMILION, lw=1.7),
        Line2D([0], [0], color=BLUE, lw=1.45, ls=(0, (4.0, 2.2))),
        Line2D([0], [0], color=GRAPHITE, lw=1.5, marker="s", ms=3.0,
               markerfacecolor=GRAPHITE, markeredgecolor=WHITE, markeredgewidth=0.45),
    ]
    labels = [
        "calibrated baseline",
        "one-way island shadow",
        "coupled island-model variant",
    ]
    fig.legend(handles, labels, loc="upper center", bbox_to_anchor=(0.61, 0.985),
               ncol=3, handlelength=2.7, columnspacing=1.35, borderaxespad=0.0)
    return fig


def save_figure_bundle(fig: mpl.figure.Figure, output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "svg": output_dir / f"{FIGURE_STEM}.svg",
        "pdf": output_dir / f"{FIGURE_STEM}.pdf",
        "png": output_dir / f"{FIGURE_STEM}.png",
        "tiff": output_dir / f"{FIGURE_STEM}.tiff",
        "preview": output_dir / f"{FIGURE_STEM}_preview_180mm.png",
        "grayscale": output_dir / f"{FIGURE_STEM}_grayscale_180mm.png",
    }
    fig.savefig(
        paths["svg"],
        format="svg",
        metadata={"Title": FIGURE_STEM, "Description": "R582 main Figure 4", "Date": "2026-07-20"},
    )
    fig.savefig(
        paths["pdf"],
        format="pdf",
        metadata={
            "Title": FIGURE_STEM,
            "Subject": "Accessibility closure and voltage identifiability",
            "Creator": "Python/matplotlib; R582_plot_closure_identifiability.py",
            "CreationDate": STABLE_DATE,
            "ModDate": STABLE_DATE,
        },
    )
    fig.savefig(paths["png"], format="png", dpi=RASTER_DPI, facecolor=WHITE)
    fig.savefig(
        paths["tiff"], format="tiff", dpi=RASTER_DPI, facecolor=WHITE,
        pil_kwargs={"compression": "tiff_lzw"}
    )
    plt.close(fig)

    # Force opaque RGB and create exact 180-mm 300-dpi QA previews in Python.
    expected_preview = (
        int(round(WIDTH_MM / 25.4 * PREVIEW_DPI)),
        int(round(HEIGHT_MM / 25.4 * PREVIEW_DPI)),
    )
    for key, fmt in (("png", "PNG"), ("tiff", "TIFF")):
        with Image.open(paths[key]) as source:
            rgb = source.convert("RGB")
            kwargs: dict[str, Any] = {"dpi": (RASTER_DPI, RASTER_DPI)}
            if fmt == "TIFF":
                kwargs["compression"] = "tiff_lzw"
            rgb.save(paths[key], format=fmt, **kwargs)
    with Image.open(paths["png"]) as source:
        preview = source.convert("RGB").resize(expected_preview, Image.Resampling.LANCZOS)
        preview.save(paths["preview"], format="PNG", dpi=(PREVIEW_DPI, PREVIEW_DPI))
        gray = preview.convert("L").convert("RGB")
        gray.save(paths["grayscale"], format="PNG", dpi=(PREVIEW_DPI, PREVIEW_DPI))
    return paths


def locate_executable(name: str) -> Path | None:
    detected = shutil.which(name)
    if detected and Path(detected).suffix.lower() == ".exe":
        return Path(detected)
    candidate = Path(f"D:/Program Files/texlive/2024/bin/windows/{name}.exe")
    return candidate if candidate.is_file() else None


def inspect_pdf_fonts(pdf_path: Path) -> dict[str, Any]:
    exe = locate_executable("pdffonts")
    require(exe is not None, "pdffonts executable unavailable for Type 3 QA")
    result = subprocess.run([str(exe), str(pdf_path)], capture_output=True, text=True, check=True)
    output = result.stdout
    return {
        "executable": str(exe),
        "raw_output": output.strip(),
        "type3_present": bool(re.search(r"\bType\s*3\b", output, flags=re.IGNORECASE)),
        "termes_present": "TeXGyreTermes" in output.replace(" ", ""),
    }


def inspect_pdf_size(pdf_path: Path) -> dict[str, float | str]:
    exe = locate_executable("pdfinfo")
    require(exe is not None, "pdfinfo executable unavailable for page-size QA")
    result = subprocess.run([str(exe), str(pdf_path)], capture_output=True, text=True, check=True)
    match = re.search(r"Page size:\s*([0-9.]+) x ([0-9.]+) pts", result.stdout)
    require(match is not None, "Could not parse PDF page size")
    width_pt, height_pt = float(match.group(1)), float(match.group(2))
    return {
        "executable": str(exe),
        "width_pt": width_pt,
        "height_pt": height_pt,
        "width_mm": width_pt * 25.4 / 72.0,
        "height_mm": height_pt * 25.4 / 72.0,
    }


def inspect_raster(path: Path, expected_dpi: int) -> dict[str, Any]:
    with Image.open(path) as image:
        dpi = image.info.get("dpi", (None, None))
        return {
            "mode": image.mode,
            "width_px": image.size[0],
            "height_px": image.size[1],
            "dpi_x": None if dpi[0] is None else float(dpi[0]),
            "dpi_y": None if dpi[1] is None else float(dpi[1]),
            "expected_dpi": expected_dpi,
        }


def render_once(
    derived_paths: dict[str, Path],
    summary: dict[str, Any],
    reanchor: pd.DataFrame,
    output_dir: Path,
) -> dict[str, Path]:
    fig = create_figure(
        pd.read_csv(derived_paths["trajectories"]),
        pd.read_csv(derived_paths["reference_levels"]),
        pd.read_csv(derived_paths["degeneracy_curve"]),
        pd.read_csv(derived_paths["degeneracy_points"]),
        summary,
        reanchor,
    )
    return save_figure_bundle(fig, output_dir)


def file_records(
    paths: Iterable[tuple[str, str, Path]], project_root: Path
) -> pd.DataFrame:
    records = []
    for category, role, path in paths:
        records.append(
            {
                "category": category,
                "role": role,
                "path": relative_path(path, project_root),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
    return pd.DataFrame(records)


def main() -> None:
    script_path = Path(__file__).resolve()
    source_dir = script_path.parent
    manuscript_dir = script_path.parents[2]
    project_root = script_path.parents[3]
    closure_dir = source_dir.parent / "Fig_R581_matched_closure"
    reanchor_dir = source_dir.parent / "Fig_R538_voltage_reanchor"

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--comparison", type=Path, default=closure_dir / "R581_release_closure_comparison.csv")
    parser.add_argument("--release-summary", type=Path, default=closure_dir / "R581_release_closure_summary.json")
    parser.add_argument("--thresholds", type=Path, default=closure_dir / "Fig_R581_matched_closure_threshold_definitions.csv")
    parser.add_argument("--endpoint-source", type=Path, default=closure_dir / "Fig_R581_matched_closure_endpoint_summary.csv")
    parser.add_argument("--release-manifest", type=Path, default=closure_dir / "R581_RELEASE_CLOSURE_MANIFEST.md")
    parser.add_argument("--degeneracy", type=Path, default=reanchor_dir / "R538_coverage_tafel_degeneracy.csv")
    parser.add_argument("--reanchor-summary", type=Path, default=reanchor_dir / "R538_reanchor_summary.csv")
    parser.add_argument("--project-truth", type=Path, default=manuscript_dir / "notes" / "project_truth.md")
    parser.add_argument("--source-dir", type=Path, default=source_dir)
    parser.add_argument("--figure-dir", type=Path, default=manuscript_dir / "figures_R582")
    args = parser.parse_args()

    input_paths = {
        "matched comparison": args.comparison.resolve(),
        "release summary": args.release_summary.resolve(),
        "marker definitions": args.thresholds.resolve(),
        "R581 endpoint source": args.endpoint_source.resolve(),
        "release manifest": args.release_manifest.resolve(),
        "degeneracy source points": args.degeneracy.resolve(),
        "reanchor summary": args.reanchor_summary.resolve(),
        "project truth": args.project_truth.resolve(),
    }
    for role, path in input_paths.items():
        require(path.is_file(), f"Missing {role}: {path}")

    out_source = args.source_dir.resolve()
    out_figure = args.figure_dir.resolve()
    out_source.mkdir(parents=True, exist_ok=True)
    out_figure.mkdir(parents=True, exist_ok=True)

    comparison = pd.read_csv(input_paths["matched comparison"])
    thresholds = pd.read_csv(input_paths["marker definitions"])
    endpoint_source = pd.read_csv(input_paths["R581 endpoint source"])
    degeneracy = pd.read_csv(input_paths["degeneracy source points"])
    reanchor = pd.read_csv(input_paths["reanchor summary"])
    summary = json.loads(input_paths["release summary"].read_text(encoding="utf-8"))
    release_manifest_text = input_paths["release manifest"].read_text(encoding="utf-8")
    project_truth_text = input_paths["project truth"].read_text(encoding="utf-8")
    authority = parse_production_authority(project_truth_text)

    required_columns = {
        "q_mAh_cm2", "V_control_V", "V_physical_dense_V",
        "deltaV_physical_minus_control_V", "eps_s_control",
        "eps_s_physical_dense", "theta_control", "theta_physical_dense",
        "theta_dense_shadow_on_control",
    }
    require(required_columns.issubset(comparison.columns), "Matched comparison schema mismatch")
    require(len(comparison) == 1081, f"Expected 1081 matched rows, found {len(comparison)}")
    require(not comparison[list(required_columns)].isna().any().any(), "NaN in plotted matched columns")
    q = comparison["q_mAh_cm2"].to_numpy(float)
    require(np.all(np.diff(q) > 0), "Capacity grid is not strictly increasing")
    require(abs(q[0]) < 1e-12 and abs(q[-1] - 120.0) < 1e-9, "Capacity range is not 0–120")
    require(summary.get("release_pass") is True, "R581 release gate is not passing")
    require(summary.get("parameter_inventory_identical") is True, "Matched parameter inventories differ")
    require(summary.get("raw_or_original_mph_modified") is False, "Original-MPH mutation gate failed")
    require(summary["convergence_release_gate"]["pass"] is True, "Convergence release gate failed")
    settings = summary["matched_settings"]
    require(settings["mesh_elements"] == 7776, "Matched solve is not the 7776-element true mesh")
    require(abs(float(settings["rtol"]) - 3e-4) < 1e-12, "Matched tolerance mismatch")
    require(settings["source_copy_sha256"].upper() == authority["sha"], "Production/matched source SHA mismatch")
    require(authority["sha"] in release_manifest_text, "Source SHA absent from release manifest")

    require({"theta_end", "A_bare_end", "bT_needed_V", "tafel_mV_dec"}.issubset(degeneracy.columns),
            "Degeneracy source schema mismatch")
    require(np.allclose(degeneracy["theta_end"] + degeneracy["A_bare_end"], 1.0, atol=1e-12),
            "Degeneracy theta/area identity failed")
    access_mv = lookup_summary(reanchor, "R_access_mV")
    reconstructed_mv = 1000.0 * degeneracy["bT_needed_V"].to_numpy(float) * np.log(
        1.0 / degeneracy["A_bare_end"].to_numpy(float)
    )
    require(np.allclose(reconstructed_mv, access_mv, rtol=0, atol=1e-9),
            "Degeneracy rows do not preserve the registered voltage contribution")
    reconstructed_tafel = 1000.0 * math.log(10.0) * degeneracy["bT_needed_V"].to_numpy(float)
    require(np.allclose(reconstructed_tafel, degeneracy["tafel_mV_dec"], rtol=0, atol=1e-9),
            "Degeneracy coefficient conversion failed")

    # Cross-check the endpoint source without plotting it directly.
    require(set(endpoint_source["trajectory"]) == {
        "production control", "dense shadow; no feedback", "coupled dense"
    }, "Unexpected R581 endpoint-source identities")
    require(abs(float(summary["matched_difference"]["endpoint_deltaV_mV"]) + 288.15625716) < 1e-6,
            "Release endpoint voltage difference changed unexpectedly")

    font_info = configure_matplotlib()
    derived_paths = build_derived_tables(
        comparison, summary, thresholds, degeneracy, reanchor, out_source
    )
    figure_paths = render_once(derived_paths, summary, reanchor, out_figure)

    # Byte-for-byte second render to prove deterministic exports.
    with tempfile.TemporaryDirectory(prefix="r582_fig4_det_", dir=out_source) as temp_name:
        temp_paths = render_once(derived_paths, summary, reanchor, Path(temp_name))
        deterministic = {
            key: sha256(figure_paths[key]) == sha256(temp_paths[key])
            for key in figure_paths
        }
    require(all(deterministic.values()), f"Determinism check failed: {deterministic}")

    pdf_fonts = inspect_pdf_fonts(figure_paths["pdf"])
    pdf_size = inspect_pdf_size(figure_paths["pdf"])
    svg_text = figure_paths["svg"].read_text(encoding="utf-8")
    svg_text_nodes = len(re.findall(r"<text\b", svg_text))
    svg_termes = "TeX Gyre Termes" in svg_text
    require(svg_text_nodes >= 20, f"Too few editable SVG text nodes: {svg_text_nodes}")
    require(svg_termes, "SVG does not retain TeX Gyre Termes family declarations")
    require(not pdf_fonts["type3_present"], "Type 3 font detected in PDF")
    require(pdf_fonts["termes_present"], "TeX Gyre Termes not detected in PDF font table")
    require(abs(float(pdf_size["width_mm"]) - WIDTH_MM) < 0.05, "PDF width is not 180 mm")
    require(abs(float(pdf_size["height_mm"]) - HEIGHT_MM) < 0.05, "PDF height is not 118 mm")

    raster_qa = {
        "png_600dpi": inspect_raster(figure_paths["png"], RASTER_DPI),
        "tiff_600dpi": inspect_raster(figure_paths["tiff"], RASTER_DPI),
        "preview_300dpi": inspect_raster(figure_paths["preview"], PREVIEW_DPI),
        "grayscale_300dpi": inspect_raster(figure_paths["grayscale"], PREVIEW_DPI),
    }
    expected_600 = (
        int(round(WIDTH_MM / 25.4 * RASTER_DPI)),
        int(round(HEIGHT_MM / 25.4 * RASTER_DPI)),
    )
    expected_300 = (
        int(round(WIDTH_MM / 25.4 * PREVIEW_DPI)),
        int(round(HEIGHT_MM / 25.4 * PREVIEW_DPI)),
    )
    for key in ("png_600dpi", "tiff_600dpi"):
        item = raster_qa[key]
        require(item["mode"] == "RGB", f"{key} is not opaque RGB")
        require(abs(item["width_px"] - expected_600[0]) <= 1 and abs(item["height_px"] - expected_600[1]) <= 1,
                f"{key} dimensions mismatch")
    for key in ("preview_300dpi", "grayscale_300dpi"):
        item = raster_qa[key]
        require(item["mode"] == "RGB", f"{key} is not RGB")
        require((item["width_px"], item["height_px"]) == expected_300,
                f"{key} dimensions mismatch")

    q_s_control = float(summary["control"]["Q_s_mAh_cm2"])
    q_s_coupled = float(summary["physical_dense"]["Q_s_mAh_cm2"])
    delta_q_s = q_s_coupled - q_s_control
    endpoint_delta = float(summary["matched_difference"]["endpoint_deltaV_mV"])

    caption_path = out_source / f"{FIGURE_STEM}_CAPTION.md"
    caption = (
        "**Figure 4 | Accessibility relation controls the late charge response.** "
        "**a,** Remaining accessible-area fraction for the calibrated baseline, a one-way "
        "island-model shadow evaluated on the baseline solid inventory, and the fully coupled "
        f"island-model variant. The matched simulations give $Q_s={q_s_control:.3f}$ and "
        f"${q_s_coupled:.3f}$ mAh cm$^{{-2}}$. **b,** Voltage trajectories and the "
        f"island-minus-baseline difference, which reaches ${endpoint_delta:.1f}$ mV at "
        "120 mAh cm$^{-2}$. **c,** Each solved branch's solid-I$_2$ fraction; horizontal "
        "lines mark the baseline and island-model half-area inventories. **d,** "
        "Accessibility–coefficient pairs that reproduce the same selected voltage contribution. "
        "This controlled model-form sensitivity does not identify deposit morphology.\n"
    )
    caption_path.write_text(caption, encoding="utf-8", newline="\n")

    metadata = {
        "figure_id": FIGURE_STEM,
        "status": "PROTOTYPE_QA_PASS",
        "core_conclusion": (
            "Changing only the accessibility relation barely changes average saturation but "
            "strongly changes later remaining area, retained-solid inventory, and voltage; "
            "the voltage observation layer is non-identifying for morphology."
        ),
        "production_authority": {
            "branch_id": authority["branch"],
            "input_mph_sha256": authority["sha"],
            "study": authority["study"],
            "solution": authority["solution"],
            "dataset": authority["dataset"],
        },
        "matched_true_mesh": {
            "control_case_id": "matched_control_true_mesh",
            "control_dataset": settings["control_dataset"],
            "physical_case_id": "matched_physical_dense_true_mesh",
            "physical_dataset": settings["physical_dataset"],
            "study": settings["study"],
            "solution": settings["solution"],
            "mesh_elements": settings["mesh_elements"],
            "rtol": settings["rtol"],
            "only_model_expression_change": settings["only_model_expression_change"],
            "parameter_inventory_identical": summary["parameter_inventory_identical"],
            "raw_or_original_mph_modified": summary["raw_or_original_mph_modified"],
        },
        "headline_values": {
            "Q_s_baseline_mAh_cm2": q_s_control,
            "Q_s_coupled_island_mAh_cm2": q_s_coupled,
            "delta_Q_s_mAh_cm2": delta_q_s,
            "endpoint_deltaV_island_minus_baseline_mV": endpoint_delta,
            "baseline_endpoint_eps_s": float(comparison["eps_s_control"].iloc[-1]),
            "coupled_island_endpoint_eps_s": float(comparison["eps_s_physical_dense"].iloc[-1]),
        },
        "font": font_info,
        "export": {
            "width_mm": WIDTH_MM,
            "height_mm": HEIGHT_MM,
            "raster_dpi": RASTER_DPI,
            "preview_dpi": PREVIEW_DPI,
        },
        "determinism": deterministic,
    }
    metadata_path = out_source / f"{FIGURE_STEM}_build_metadata.json"
    metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    qa_path = out_source / f"{FIGURE_STEM}_QA.md"
    qa_lines = [
        f"# {FIGURE_STEM} QA",
        "",
        "Status: **PROTOTYPE QA PASS**",
        "",
        "## Scientific contract",
        "",
        f"- PASS — matched $Q_s$ values are `{q_s_control:.9f}` and `{q_s_coupled:.9f} mAh cm^-2` "
        f"(`Delta = {delta_q_s:.9f} mAh cm^-2`).",
        f"- PASS — the coupled-island minus baseline endpoint voltage difference is `{endpoint_delta:.9f} mV`.",
        "- PASS — panel a uses the intuitive remaining-area direction `A_bare/A0`; the one-way shadow and coupled solve are not conflated.",
        "- PASS — panel c uses each solved branch's own solid inventory and only the baseline half-area and island half-area references.",
        f"- PASS — panel d reconstructs the fixed `{access_mv:.9f} mV` voltage contribution from every registered source point.",
        "- PASS — no deposit image, film, pore blockage, or unique morphology is encoded or inferred.",
        "",
        "## Evidence identity (source package only)",
        "",
        f"- Production authority: `{authority['branch']}`; input MPH SHA-256 `{authority['sha']}`; "
        f"`{authority['study']}/{authority['solution']}/{authority['dataset']}`.",
        f"- Matched true-mesh control: `{settings['control_dataset']}`; physical branch: `{settings['physical_dataset']}`; "
        f"study `{settings['study']}`, solution `{settings['solution']}`, `{settings['mesh_elements']}` elements, `rtol={settings['rtol']}`.",
        "- Parameter inventories are identical; the release summary records that no raw/original MPH file was modified.",
        "",
        "## Typography and export",
        "",
        f"- PASS — figure family is `{font_info['family']}`; regular font SHA-256 `{font_info['font_sha256']['regular']}`.",
        f"- PASS — SVG contains `{svg_text_nodes}` editable `<text>` nodes and explicitly declares TeX Gyre Termes.",
        f"- PASS — PDF font table contains TeX Gyre Termes and no Type 3 font. Tool: `{pdf_fonts['executable']}`.",
        f"- PASS — PDF page is `{pdf_size['width_mm']:.4f} × {pdf_size['height_mm']:.4f} mm`.",
        f"- PASS — 600-dpi PNG/TIFF dimensions are approximately `{expected_600[0]} × {expected_600[1]} px`; both are opaque RGB.",
        f"- PASS — 180-mm preview and grayscale QA are `{expected_300[0]} × {expected_300[1]} px` at 300 dpi.",
        "- PASS — all labels/ticks use configured base sizes of 6.5 pt or larger; mathematical super/subscripts follow the manuscript's Termes math styling.",
        "- PASS — colors are redundantly encoded by line style or marker; the grayscale preview is provided for visual inspection.",
        "",
        "## Determinism",
        "",
    ]
    qa_lines.extend(f"- PASS — `{key}` is byte-identical across two independent renders." for key in figure_paths)
    qa_lines.extend(
        [
            "",
            "## PDF font table",
            "",
            "```text",
            pdf_fonts["raw_output"],
            "```",
        ]
    )
    qa_path.write_text("\n".join(qa_lines) + "\n", encoding="utf-8")

    contract_path = out_source / "FIGURE_CONTRACT.md"
    require(contract_path.is_file(), "Missing figure contract")
    manifest_entries: list[tuple[str, str, Path]] = []
    manifest_entries.extend(("input", role, path) for role, path in input_paths.items())
    manifest_entries.extend(("derived", role, path) for role, path in derived_paths.items())
    manifest_entries.extend(("figure", role, path) for role, path in figure_paths.items())
    manifest_entries.extend(
        [
            ("build", "deterministic Python renderer", script_path),
            ("documentation", "figure contract", contract_path),
            ("documentation", "caption draft", caption_path),
            ("documentation", "build metadata", metadata_path),
            ("documentation", "QA report", qa_path),
        ]
    )
    manifest = file_records(manifest_entries, project_root)
    manifest_path = out_source / f"{FIGURE_STEM}_source_manifest.csv"
    write_csv(manifest, manifest_path)

    print(json.dumps({
        "status": "PROTOTYPE_QA_PASS",
        "figure": {key: str(path) for key, path in figure_paths.items()},
        "source_data": {key: str(path) for key, path in derived_paths.items()},
        "caption": str(caption_path),
        "qa": str(qa_path),
        "manifest": str(manifest_path),
        "font_family": font_info["family"],
        "delta_Qs_mAh_cm2": delta_q_s,
        "endpoint_deltaV_mV": endpoint_delta,
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
