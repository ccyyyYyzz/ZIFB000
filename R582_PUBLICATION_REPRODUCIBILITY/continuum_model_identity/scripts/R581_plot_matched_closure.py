#!/usr/bin/env python3
"""Reproducible release figure for the passing R581 true-mesh closure pair.

Figure contract
---------------
Conclusion: changing only the registered accessibility relation in matched
continuum solves changes the coupled solid-inventory, accessibility and voltage
trajectories.  This is closure sensitivity, not morphology identification.

Runtime scientific inputs are deliberately limited to:
  1. outputs/R581_release_closure_comparison.csv
  2. outputs/R581_release_closure_summary.json
  3. manifests/R581_RELEASE_CLOSURE_MANIFEST.md

The connected-film marker is a registered project comparator, not an R581
fit; its value is therefore an explicit, audited constant below.  The dense-
island half-accessibility marker is derived from the frozen closure expression
in the summary.  All plotted trajectories come directly from the frozen CSV:
there is no smoothing, curve fitting or manual point movement.

The release inputs can exist only after the registered tolerance and true-mesh
comparators pass.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image


FIGURE_STEM = "Fig_R581_matched_closure"
RELEASE_STATUS = "RELEASE_READY"
WIDTH_MM = 180.0
HEIGHT_MM = 132.0
RASTER_DPI = 600
FILM_PERC_EPS = 2.2324e-3
FILM_PERC_PROVENANCE = (
    "registered geometric connected-film/percolation comparator; explicit "
    "project-contract constant, not fitted or recomputed from R581"
)

CONTROL = "#233B5D"       # dark blue
PHYSICAL = "#A94F5B"      # muted carmine
SHADOW = "#C88B91"        # light carmine, dashed
ISLAND = "#6F7651"        # olive
FILM = "#735E7C"          # muted violet
NEUTRAL = "#50555A"
GRID = "#D9DCDF"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest().upper()


def first_crossing(x: np.ndarray, y: np.ndarray, target: float) -> float | None:
    """First upward crossing by piecewise-linear interpolation."""
    finite = np.isfinite(x) & np.isfinite(y)
    x = np.asarray(x[finite], dtype=float)
    y = np.asarray(y[finite], dtype=float)
    hit = np.flatnonzero(y >= target)
    if hit.size == 0:
        return None
    i = int(hit[0])
    if i == 0:
        return float(x[0])
    x0, x1, y0, y1 = x[i - 1], x[i], y[i - 1], y[i]
    if y1 == y0:
        return float(x1)
    return float(x0 + (target - y0) * (x1 - x0) / (y1 - y0))


def interp_at(x: np.ndarray, y: np.ndarray, x_new: float) -> float:
    return float(np.interp(float(x_new), np.asarray(x, float), np.asarray(y, float)))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def approx(a: float, b: float, atol: float) -> bool:
    return bool(np.isfinite(a) and np.isfinite(b) and abs(a - b) <= atol)


def parse_closure(expression: str) -> tuple[float, float]:
    match = re.fullmatch(
        r"1-exp\(-(?P<a>[0-9.]+)\*eps_s_reg\^(?P<b>[0-9.]+)\)",
        expression.strip(),
    )
    require(match is not None, f"Unrecognized frozen closure: {expression!r}")
    return float(match.group("a")), float(match.group("b"))


def configure_matplotlib() -> str:
    mpl.use("Agg", force=True)
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
            "font.size": 7.0,
            "axes.titlesize": 7.4,
            "axes.titleweight": "bold",
            "axes.labelsize": 7.0,
            "axes.linewidth": 0.8,
            "xtick.labelsize": 6.8,
            "ytick.labelsize": 6.8,
            "xtick.major.width": 0.7,
            "ytick.major.width": 0.7,
            "xtick.major.size": 3.0,
            "ytick.major.size": 3.0,
            "legend.fontsize": 6.4,
            "legend.frameon": False,
            "lines.linewidth": 1.35,
            "svg.fonttype": "none",
            "svg.hashsalt": "R581-matched-closure-v1",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "mathtext.fontset": "dejavusans",
            "savefig.facecolor": "white",
            "figure.facecolor": "white",
        }
    )
    from matplotlib import font_manager

    return str(font_manager.findfont("Arial", fallback_to_default=True))


def style_axis(ax: mpl.axes.Axes, grid_y: bool = False) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(direction="out", color=NEUTRAL, labelcolor="#222222")
    if grid_y:
        ax.grid(axis="y", color=GRID, lw=0.55, alpha=0.8, zorder=0)


def panel_label(ax: mpl.axes.Axes, label: str, x: float = -0.13) -> None:
    ax.text(
        x,
        1.055,
        label,
        transform=ax.transAxes,
        fontsize=9.0,
        fontweight="bold",
        va="bottom",
        ha="left",
        clip_on=False,
    )


def output_record(path: Path, role: str) -> dict[str, Any]:
    return {
        "role": role,
        "path": path.name,
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def write_csv(frame: pd.DataFrame, path: Path) -> None:
    frame.to_csv(path, index=False, float_format="%.12g", lineterminator="\n")


def render(
    data: pd.DataFrame,
    summary: dict[str, Any],
    markers: dict[str, float | None],
    output_dir: Path,
) -> dict[str, Path]:
    q = data["q_mAh_cm2"].to_numpy(float)
    v_control = data["V_control_V"].to_numpy(float)
    v_physical = data["V_physical_dense_V"].to_numpy(float)
    delta_mv = 1000.0 * data["deltaV_physical_minus_control_V"].to_numpy(float)
    eps_control = data["eps_s_control"].to_numpy(float)
    eps_physical = data["eps_s_physical_dense"].to_numpy(float)
    theta_control = data["theta_control"].to_numpy(float)
    theta_physical = data["theta_physical_dense"].to_numpy(float)
    theta_shadow = data["theta_dense_shadow_on_control"].to_numpy(float)

    fig = plt.figure(figsize=(WIDTH_MM / 25.4, HEIGHT_MM / 25.4))
    outer = fig.add_gridspec(
        2,
        12,
        height_ratios=[1.08, 0.92],
        left=0.082,
        right=0.985,
        top=0.91,
        bottom=0.215,
        hspace=0.49,
        wspace=1.9,
    )
    ax_a = fig.add_subplot(outer[0, :4])
    b_grid = outer[0, 4:].subgridspec(2, 1, height_ratios=[3.0, 1.0], hspace=0.08)
    ax_b = fig.add_subplot(b_grid[0, 0])
    ax_db = fig.add_subplot(b_grid[1, 0], sharex=ax_b)
    ax_c = fig.add_subplot(outer[1, :])

    # a — accessibility response: control, a true one-way shadow, and coupled dense.
    ax_a.plot(q, theta_control, color=CONTROL, label="production control", zorder=3)
    ax_a.plot(
        q,
        theta_shadow,
        color=SHADOW,
        ls=(0, (4.0, 2.2)),
        lw=1.45,
        label="dense shadow; no feedback",
        zorder=2,
    )
    ax_a.plot(
        q,
        theta_physical,
        color=PHYSICAL,
        marker="o",
        markevery=135,
        ms=2.2,
        mec="white",
        mew=0.35,
        label="coupled dense",
        zorder=4,
    )
    ax_a.axhline(0.5, color="#AEB3B7", lw=0.65, ls=(0, (1.5, 2.0)), zorder=1)
    for key, color, marker in (
        ("q_theta_half_control", CONTROL, "s"),
        ("q_theta_half_shadow", SHADOW, "D"),
    ):
        x_cross = markers[key]
        if x_cross is not None:
            ax_a.scatter(
                [x_cross], [0.5], s=18, marker=marker, color=color,
                edgecolor="white", linewidth=0.45, zorder=6
            )
    ax_a.text(2.5, 0.522, "θ = 0.5", color=NEUTRAL, fontsize=6.2, va="bottom")
    ax_a.set(xlim=(0, 121), ylim=(0, 1.03), ylabel="accessibility loss, θ")
    ax_a.set_xticks([0, 30, 60, 90, 120])
    ax_a.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    ax_a.set_xlabel(r"capacity, $Q$ (mAh cm$^{-2}$)")
    ax_a.set_title("Accessibility response", loc="left", pad=6)
    ax_a.legend(loc="upper left", handlelength=2.5, borderaxespad=0.2)
    style_axis(ax_a, grid_y=True)
    panel_label(ax_a, "a", x=-0.18)

    # b — matched voltage hero panel and compact aligned delta axis.
    ax_b.plot(q, v_control, color=CONTROL, label="production control", zorder=3)
    ax_b.plot(
        q,
        v_physical,
        color=PHYSICAL,
        marker="o",
        markevery=135,
        ms=2.2,
        mec="white",
        mew=0.35,
        label="coupled dense",
        zorder=4,
    )
    ax_b.set(xlim=(0, 121), ylim=(1.38, 1.755), ylabel="voltage (V)")
    ax_b.set_yticks([1.4, 1.5, 1.6, 1.7])
    ax_b.set_title("Matched voltage response", loc="left", pad=6)
    ax_b.legend(loc="upper left", ncol=2, columnspacing=1.1, handlelength=2.3)
    ax_b.tick_params(labelbottom=False)
    style_axis(ax_b, grid_y=True)
    panel_label(ax_b, "b", x=-0.105)

    ax_db.axhline(0, color="#AEB3B7", lw=0.65, zorder=1)
    ax_db.plot(q, delta_mv, color=PHYSICAL, lw=1.25, zorder=3)
    ax_db.set(xlim=(0, 121), ylim=(-315, 20), ylabel="ΔV (mV)")
    ax_db.set_xticks([0, 30, 60, 90, 120])
    ax_db.set_yticks([-300, -150, 0])
    ax_db.set_xlabel(r"capacity, $Q$ (mAh cm$^{-2}$)")
    endpoint_delta = float(summary["matched_difference"]["endpoint_deltaV_mV"])
    ax_db.annotate(
        f"{endpoint_delta:.1f} mV",
        xy=(120, endpoint_delta),
        xytext=(91, -252),
        fontsize=6.3,
        color=PHYSICAL,
        fontweight="bold",
        arrowprops={"arrowstyle": "-", "color": PHYSICAL, "lw": 0.65},
        bbox={"boxstyle": "round,pad=0.18", "fc": "white", "ec": "none", "alpha": 0.88},
        ha="left",
        va="center",
    )
    style_axis(ax_db, grid_y=False)

    # c — each solve's own inventory; closure-specific markers are kept distinct.
    ax_c.plot(q, 1000 * eps_control, color=CONTROL,
              label=r"production control $\varepsilon_s$", zorder=3)
    ax_c.plot(
        q,
        1000 * eps_physical,
        color=PHYSICAL,
        marker="o",
        markevery=135,
        ms=2.2,
        mec="white",
        mew=0.35,
        label=r"coupled dense $\varepsilon_s$",
        zorder=4,
    )
    qf = float(markers["q_theta_half_control"])
    eps_cal = float(markers["eps_cal_traj"])
    island_eps = float(markers["eps_island_half"])
    film_eps = float(markers["eps_film_perc"])
    ax_c.axvline(qf, color=CONTROL, ls=(0, (1.5, 2.2)), lw=0.8, alpha=0.85, zorder=1)
    ax_c.scatter([qf], [1000 * eps_cal], s=22, marker="s", color=CONTROL,
                 edgecolor="white", linewidth=0.45, zorder=6)
    ax_c.annotate(
        f"$Q_{{\\mathrm{{f,cal}}}}$ = {qf:.2f}\n"
        f"$\\varepsilon_{{\\mathrm{{s,cal,traj}}}}^*$ = {1000 * eps_cal:.3f} × 10$^{{-3}}$",
        xy=(qf, 1000 * eps_cal),
        xytext=(73, 0.56),
        fontsize=6.1,
        color=CONTROL,
        arrowprops={"arrowstyle": "-", "color": CONTROL, "lw": 0.6},
        bbox={"boxstyle": "round,pad=0.20", "fc": "white", "ec": "none", "alpha": 0.92},
        ha="left",
        va="center",
    )
    ax_c.axhline(1000 * island_eps, color=ISLAND, ls=(0, (5, 2.2)), lw=0.85, zorder=1)
    ax_c.axhline(1000 * film_eps, color=FILM, ls=(0, (1.2, 1.8)), lw=1.0, zorder=1)
    ax_c.text(
        43, 1000 * island_eps + 0.055,
        r"$\varepsilon_{\mathrm{s,island},1/2}$ = 1.7973 × 10$^{-3}$",
        fontsize=6.1, color=ISLAND, ha="center", va="bottom",
        bbox={"fc": "white", "ec": "none", "pad": 0.35, "alpha": 0.88},
    )
    ax_c.text(
        43, 1000 * film_eps + 0.055,
        r"$\varepsilon_{\mathrm{s,film\!\!\!-\!perc}}^*$ = 2.2324 × 10$^{-3}$",
        fontsize=6.1, color=FILM, ha="center", va="bottom",
        bbox={"fc": "white", "ec": "none", "pad": 0.35, "alpha": 0.88},
    )
    for key, eps, color, marker in (
        ("q_eps_island_control", island_eps, ISLAND, "D"),
        ("q_eps_film_control", film_eps, FILM, "P"),
    ):
        q_cross = markers[key]
        if q_cross is not None:
            ax_c.scatter([q_cross], [1000 * eps], s=22, marker=marker,
                         color=color, edgecolor="white", linewidth=0.45, zorder=6)

    half_physical = markers["q_theta_half_physical"]
    summary_text = (
        "accessibility endpoint / Q(θ = 0.5)\n"
        f"control   {theta_control[-1]:.3f} / {qf:.2f}\n"
        f"shadow    {theta_shadow[-1]:.3f} / {float(markers['q_theta_half_shadow']):.2f}\n"
        f"coupled  {theta_physical[-1]:.3f} / "
        + ("not reached" if half_physical is None else f"{half_physical:.2f}")
    )
    ax_c.text(
        0.012, 0.955, summary_text,
        transform=ax_c.transAxes, fontsize=6.15, linespacing=1.25,
        ha="left", va="top", color="#26292B",
        bbox={"boxstyle": "round,pad=0.30", "fc": "white", "ec": GRID, "lw": 0.65, "alpha": 0.96},
        zorder=8,
    )
    ax_c.scatter([120, 120], [1000 * eps_control[-1], 1000 * eps_physical[-1]],
                 s=18, color=[CONTROL, PHYSICAL], edgecolor="white", linewidth=0.45, zorder=6)
    ax_c.set(xlim=(0, 121), ylim=(0, 3.42),
             ylabel=r"solid fraction, $\varepsilon_s$ (×10$^{-3}$)")
    ax_c.set_xticks([0, 30, 60, 90, 120])
    ax_c.set_yticks([0, 1, 2, 3])
    ax_c.set_xlabel(r"capacity, $Q$ (mAh cm$^{-2}$)")
    ax_c.set_title("Solid-inventory feedback and closure-specific markers", loc="left", pad=6)
    ax_c.legend(loc="lower left", bbox_to_anchor=(0.012, 0.03), ncol=2,
                columnspacing=1.1, handlelength=2.4)
    style_axis(ax_c, grid_y=True)
    panel_label(ax_c, "c", x=-0.055)

    source_hash = summary["matched_settings"]["source_copy_sha256"]
    fig.text(
        0.5,
        0.978,
        "Matched closure sensitivity on the converged 7776-element mesh",
        ha="center",
        va="top",
        fontsize=6.7,
        fontweight="bold",
        color="#356859",
    )
    fig.text(
        0.082,
        0.100,
        f"Matched source copies byte-identical (SHA-256 {source_hash[:8]}…{source_hash[-4:]}); "
        "stdR522 · live sol5 · 7776-element mesh · rtol 3e-4.",
        ha="left", va="bottom", fontsize=5.45, color=NEUTRAL,
    )
    fig.text(
        0.082,
        0.066,
        "Only cov_theta_surf and theta_eff_R520 changed to 1−exp(−35.4 ε_s^0.6222); "
        "piecewise-linear crossings; no smoothing.",
        ha="left", va="bottom", fontsize=5.45, color=NEUTRAL,
    )
    fig.text(
        0.082,
        0.032,
        "Interpretation boundary: closure sensitivity under fixed continuum settings; voltage does not identify a unique deposit morphology.",
        ha="left", va="bottom", fontsize=5.45, color=NEUTRAL,
    )

    paths = {
        "svg": output_dir / f"{FIGURE_STEM}.svg",
        "pdf": output_dir / f"{FIGURE_STEM}.pdf",
        "tiff": output_dir / f"{FIGURE_STEM}.tiff",
        "png": output_dir / f"{FIGURE_STEM}.png",
    }
    stable_date = datetime(2026, 7, 11, tzinfo=timezone.utc)
    fig.savefig(
        paths["svg"], format="svg",
        metadata={"Title": FIGURE_STEM, "Description": RELEASE_STATUS, "Date": "2026-07-11"},
    )
    fig.savefig(
        paths["pdf"], format="pdf",
        metadata={
            "Title": FIGURE_STEM,
            "Subject": RELEASE_STATUS,
            "Creator": "Python/matplotlib; R581_plot_matched_closure.py",
            "CreationDate": stable_date,
            "ModDate": stable_date,
        },
    )
    fig.savefig(paths["png"], format="png", dpi=RASTER_DPI)
    fig.savefig(
        paths["tiff"], format="tiff", dpi=RASTER_DPI,
        pil_kwargs={"compression": "tiff_lzw"},
    )
    plt.close(fig)

    # Submission rasters are flattened to an opaque white RGB canvas.
    for key, fmt in (("png", "PNG"), ("tiff", "TIFF")):
        with Image.open(paths[key]) as source:
            rgba = source.convert("RGBA")
            opaque = Image.new("RGB", rgba.size, "white")
            opaque.paste(rgba, mask=rgba.getchannel("A"))
            save_kwargs: dict[str, Any] = {"dpi": (RASTER_DPI, RASTER_DPI)}
            if fmt == "TIFF":
                save_kwargs["compression"] = "tiff_lzw"
            opaque.save(paths[key], format=fmt, **save_kwargs)
    return paths


def main() -> None:
    script_path = Path(__file__).resolve()
    base = script_path.parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--comparison",
        type=Path,
        default=base / "outputs" / "R581_release_closure_comparison.csv",
    )
    parser.add_argument(
        "--summary",
        type=Path,
        default=base / "outputs" / "R581_release_closure_summary.json",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=base / "manifests" / "R581_RELEASE_CLOSURE_MANIFEST.md",
    )
    parser.add_argument("--output-dir", type=Path, default=base / "figures")
    args = parser.parse_args()
    comparison_path = args.comparison.resolve()
    summary_path = args.summary.resolve()
    manifest_path = args.manifest.resolve()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    require(comparison_path.is_file(), f"Missing input: {comparison_path}")
    require(summary_path.is_file(), f"Missing input: {summary_path}")
    require(manifest_path.is_file(), f"Missing input: {manifest_path}")

    data = pd.read_csv(comparison_path)
    with summary_path.open("r", encoding="utf-8") as handle:
        summary = json.load(handle)
    manifest = manifest_path.read_text(encoding="utf-8")
    font_path = configure_matplotlib()

    required = [
        "q_mAh_cm2", "time_s", "V_control_V", "V_physical_dense_V",
        "deltaV_physical_minus_control_V", "eps_s_control",
        "eps_s_physical_dense", "theta_control", "theta_physical_dense",
        "theta_dense_shadow_on_control",
    ]
    require(all(c in data.columns for c in required), "Comparison CSV schema mismatch")
    require(len(data) == 1081, f"Expected 1081 rows, found {len(data)}")
    require(not data[required].isna().any().any(), "NaN in plotted comparison columns")

    q = data["q_mAh_cm2"].to_numpy(float)
    time_s = data["time_s"].to_numpy(float)
    require(np.all(np.diff(q) > 0), "Capacity grid is not strictly increasing")
    require(np.allclose(np.diff(time_s), 10.0, rtol=0, atol=1e-10), "Time grid is not 10 s")
    require(approx(q[0], 0.0, 1e-12) and approx(q[-1], 120.0, 1e-10), "Capacity extent mismatch")

    input_hashes = {
        "comparison_csv": sha256(comparison_path),
        "summary_json": sha256(summary_path),
        "matched_manifest": sha256(manifest_path),
    }
    require(input_hashes["comparison_csv"] in manifest, "Comparison SHA-256 not frozen in manifest")
    require(input_hashes["summary_json"] in manifest, "Summary SHA-256 not frozen in manifest")

    settings = summary["matched_settings"]
    require(settings["study"] == "stdR522", "Unexpected matched study")
    require(settings["solution"] == "sol5", "Unexpected live solution")
    require(settings["source_copy_sha256"] in manifest, "Source-copy hash mismatch")
    require(summary["parameter_inventory_identical"] is True, "Parameter inventories differ")
    require(summary["raw_or_original_mph_modified"] is False, "Original MPH mutation flag is not false")
    require(summary["control_reproduction_gate"]["pass"] is True, "Fresh control reproduction gate failed")
    require(summary["release_pass"] is True, "Release summary is not passing")
    require(summary["convergence_release_gate"]["pass"] is True, "Convergence release gate failed")
    require(settings["mesh_elements"] == 7776, "Release figure is not using the true mesh")
    require(approx(float(settings["rtol"]), 3e-4, 1e-12), "Unexpected release tolerance")

    expressions = settings["only_model_expression_change"]
    require(set(expressions) == {"cov_theta_surf", "theta_eff_R520"}, "Unexpected changed expressions")
    require(len(set(expressions.values())) == 1, "Changed closure expressions are not identical")
    closure_a, closure_b = parse_closure(next(iter(expressions.values())))
    eps_island_half = float((math.log(2.0) / closure_a) ** (1.0 / closure_b))

    theta_control = data["theta_control"].to_numpy(float)
    theta_shadow = data["theta_dense_shadow_on_control"].to_numpy(float)
    theta_physical = data["theta_physical_dense"].to_numpy(float)
    eps_control = data["eps_s_control"].to_numpy(float)
    eps_physical = data["eps_s_physical_dense"].to_numpy(float)

    q_half_control = first_crossing(q, theta_control, 0.5)
    q_half_shadow = first_crossing(q, theta_shadow, 0.5)
    q_half_physical = first_crossing(q, theta_physical, 0.5)
    require(q_half_control is not None and q_half_shadow is not None, "Expected half-accessibility crossing missing")
    require(q_half_physical is None, "Coupled dense unexpectedly reaches half accessibility")
    require(approx(q_half_control, summary["control"]["Q_theta_0p5_mAh_cm2"], 1e-8), "Control crossing mismatch")
    require(approx(q_half_shadow, summary["one_way_dense_shadow"]["Q_theta_0p5_mAh_cm2"], 1e-8), "Shadow crossing mismatch")

    eps_cal_traj = interp_at(q, eps_control, q_half_control)
    q_eps_island_control = first_crossing(q, eps_control, eps_island_half)
    q_eps_island_physical = first_crossing(q, eps_physical, eps_island_half)
    q_eps_film_control = first_crossing(q, eps_control, FILM_PERC_EPS)
    q_eps_film_physical = first_crossing(q, eps_physical, FILM_PERC_EPS)
    require(q_eps_island_control is not None and q_eps_film_control is not None, "Control threshold crossing missing")
    require(q_eps_island_physical is None and q_eps_film_physical is None, "Coupled dense crosses a physical comparator unexpectedly")

    recomputed_delta = data["V_physical_dense_V"].to_numpy(float) - data["V_control_V"].to_numpy(float)
    delta_error = float(np.max(np.abs(recomputed_delta - data["deltaV_physical_minus_control_V"].to_numpy(float))))
    require(delta_error <= 5e-12, f"Stored delta-V mismatch: {delta_error:g} V")
    require(approx(float(theta_control[-1]), summary["control"]["endpoint"]["theta_avg"], 1e-10), "Control endpoint mismatch")
    require(approx(float(theta_physical[-1]), summary["physical_dense"]["endpoint"]["theta_avg"], 1e-10), "Physical endpoint mismatch")

    markers: dict[str, float | None] = {
        "q_theta_half_control": q_half_control,
        "q_theta_half_shadow": q_half_shadow,
        "q_theta_half_physical": q_half_physical,
        "eps_cal_traj": eps_cal_traj,
        "eps_island_half": eps_island_half,
        "eps_film_perc": FILM_PERC_EPS,
        "q_eps_island_control": q_eps_island_control,
        "q_eps_island_physical": q_eps_island_physical,
        "q_eps_film_control": q_eps_film_control,
        "q_eps_film_physical": q_eps_film_physical,
    }

    source_data = pd.DataFrame(
        {
            "q_mAh_cm2": q,
            "time_s": time_s,
            "panel_a_theta_production_control": theta_control,
            "panel_a_theta_dense_shadow_no_feedback": theta_shadow,
            "panel_a_theta_coupled_dense": theta_physical,
            "panel_b_voltage_production_control_V": data["V_control_V"],
            "panel_b_voltage_coupled_dense_V": data["V_physical_dense_V"],
            "panel_b_deltaV_physical_minus_control_mV": 1000.0 * data["deltaV_physical_minus_control_V"],
            "panel_c_eps_s_production_control": eps_control,
            "panel_c_eps_s_coupled_dense": eps_physical,
        }
    )
    source_path = output_dir / f"{FIGURE_STEM}_source_data.csv"
    write_csv(source_data, source_path)

    threshold_rows = [
        {
            "marker_id": "Q_f_cal",
            "display_symbol": "Q_f,cal",
            "definition": "first production-control theta=0.5 crossing; piecewise-linear interpolation on common Q grid",
            "value": q_half_control,
            "unit": "mAh cm^-2",
            "control_Q_crossing_mAh_cm2": q_half_control,
            "coupled_dense_Q_crossing_mAh_cm2": np.nan,
            "provenance": "derived directly from frozen R581 comparison CSV; checked against frozen summary",
        },
        {
            "marker_id": "eps_s_cal_traj",
            "display_symbol": "eps_s,cal,traj*",
            "definition": "production-control eps_s read at Q_f,cal; not a physical-island or film threshold",
            "value": eps_cal_traj,
            "unit": "dimensionless",
            "control_Q_crossing_mAh_cm2": q_half_control,
            "coupled_dense_Q_crossing_mAh_cm2": np.nan,
            "provenance": "piecewise-linear readout from frozen R581 comparison CSV",
        },
        {
            "marker_id": "eps_s_island_half",
            "display_symbol": "eps_s,island,1/2",
            "definition": f"(ln 2/{closure_a:g})^(1/{closure_b:g}); half-accessibility of frozen dense-island relation",
            "value": eps_island_half,
            "unit": "dimensionless",
            "control_Q_crossing_mAh_cm2": q_eps_island_control,
            "coupled_dense_Q_crossing_mAh_cm2": np.nan,
            "provenance": "derived from the frozen closure expression stored in R581 summary JSON",
        },
        {
            "marker_id": "eps_s_film_perc",
            "display_symbol": "eps_s,film-perc*",
            "definition": "geometric connected-film/percolation marker; distinct from half-accessibility",
            "value": FILM_PERC_EPS,
            "unit": "dimensionless",
            "control_Q_crossing_mAh_cm2": q_eps_film_control,
            "coupled_dense_Q_crossing_mAh_cm2": np.nan,
            "provenance": FILM_PERC_PROVENANCE,
        },
    ]
    thresholds_path = output_dir / f"{FIGURE_STEM}_threshold_definitions.csv"
    write_csv(pd.DataFrame(threshold_rows), thresholds_path)

    endpoint_rows = [
        {
            "trajectory": "production control",
            "is_solved_feedback_branch": True,
            "inventory_source": "own solved eps_s(Q)",
            "endpoint_q_mAh_cm2": q[-1],
            "endpoint_theta": theta_control[-1],
            "theta_half_crossing_q_mAh_cm2": q_half_control,
            "theta_half_status": "reached",
            "endpoint_eps_s": eps_control[-1],
            "endpoint_voltage_V": data["V_control_V"].iloc[-1],
        },
        {
            "trajectory": "dense shadow; no feedback",
            "is_solved_feedback_branch": False,
            "inventory_source": "production-control eps_s(Q); one-way diagnostic only",
            "endpoint_q_mAh_cm2": q[-1],
            "endpoint_theta": theta_shadow[-1],
            "theta_half_crossing_q_mAh_cm2": q_half_shadow,
            "theta_half_status": "reached",
            "endpoint_eps_s": eps_control[-1],
            "endpoint_voltage_V": np.nan,
        },
        {
            "trajectory": "coupled dense",
            "is_solved_feedback_branch": True,
            "inventory_source": "own solved eps_s(Q)",
            "endpoint_q_mAh_cm2": q[-1],
            "endpoint_theta": theta_physical[-1],
            "theta_half_crossing_q_mAh_cm2": np.nan,
            "theta_half_status": "not reached by 120 mAh cm^-2",
            "endpoint_eps_s": eps_physical[-1],
            "endpoint_voltage_V": data["V_physical_dense_V"].iloc[-1],
        },
    ]
    endpoints_path = output_dir / f"{FIGURE_STEM}_endpoint_summary.csv"
    write_csv(pd.DataFrame(endpoint_rows), endpoints_path)

    figure_paths = render(data, summary, markers, output_dir)

    # Matplotlib quantizes physical canvas dimensions downward to whole pixels.
    expected_px = (
        int(WIDTH_MM / 25.4 * RASTER_DPI),
        int(HEIGHT_MM / 25.4 * RASTER_DPI),
    )
    raster_qa: dict[str, Any] = {}
    for key in ("png", "tiff"):
        with Image.open(figure_paths[key]) as image:
            raster_qa[key] = {
                "pixels": list(image.size),
                "dpi": [float(v) for v in image.info.get("dpi", (0, 0))],
                "mode": image.mode,
            }
            require(image.size == expected_px, f"{key.upper()} pixel dimensions mismatch")

    svg_text = figure_paths["svg"].read_text(encoding="utf-8")
    require("<text" in svg_text, "SVG contains no editable text nodes")
    require("converged 7776-element mesh" in svg_text, "SVG lacks convergence-status mark")
    require("dense shadow; no feedback" in svg_text, "SVG lacks explicit no-feedback label")

    generated = [
        output_record(source_path, "machine-readable plotted trajectories"),
        output_record(thresholds_path, "closure-specific threshold-definition table"),
        output_record(endpoints_path, "endpoint and crossing summary"),
        *[output_record(figure_paths[k], f"figure {k.upper()}") for k in ("svg", "pdf", "tiff", "png")],
    ]
    manifest_out = output_dir / f"{FIGURE_STEM}_output_manifest.csv"
    write_csv(pd.DataFrame(generated), manifest_out)

    qa_checks = {
        "release_status_visible": True,
        "runtime_scientific_input_count": 3,
        "input_hashes_frozen": True,
        "rows_1081": len(data) == 1081,
        "common_time_step_s": 10.0,
        "capacity_strictly_increasing": True,
        "missing_plotted_values": 0,
        "stored_deltaV_max_abs_error_V": delta_error,
        "control_reproduction_gate_pass": True,
        "convergence_release_gate_pass": True,
        "true_mesh_elements": 7776,
        "relative_tolerance": 3e-4,
        "parameter_inventory_identical": True,
        "source_copy_byte_identical": True,
        "shadow_explicitly_no_feedback": True,
        "coupled_dense_half_accessibility_not_reached": q_half_physical is None,
        "crossing_interpolation": "first upward crossing; piecewise-linear on the 1081-point common-Q grid",
        "smoothing_or_manual_point_movement": False,
        "statistics_or_confidence_bands": False,
        "figure_width_mm": WIDTH_MM,
        "figure_height_mm": HEIGHT_MM,
        "raster_dpi": RASTER_DPI,
        "raster_expected_pixels": list(expected_px),
        "raster_files": raster_qa,
        "svg_editable_text_nodes": True,
        "pdf_rcparam_fonttype": 42,
        "font_resolved": font_path,
        "palette_redundant_encoding": "color plus dash/marker; shadow is dashed and coupled dense carries sparse circles",
        "release_blocker": None,
    }
    metadata = {
        "analysis_id": "R581_CANONICAL_CLOSURE_REBUILD",
        "figure_id": FIGURE_STEM,
        "status": RELEASE_STATUS,
        "core_conclusion": (
            "Changing only the accessibility relation in matched continuum solves changes coupled "
            "solid-inventory, accessibility and voltage trajectories; this quantifies closure "
            "sensitivity and does not identify a unique real deposit morphology."
        ),
        "input_files": {
            "comparison_csv": {"path": str(comparison_path), "sha256": input_hashes["comparison_csv"]},
            "summary_json": {"path": str(summary_path), "sha256": input_hashes["summary_json"]},
            "matched_manifest": {"path": str(manifest_path), "sha256": input_hashes["matched_manifest"]},
        },
        "script": {"path": str(script_path), "sha256": sha256(script_path)},
        "matched_settings": settings,
        "markers": markers,
        "qa": qa_checks,
        "output_manifest": {"path": str(manifest_out), "sha256": sha256(manifest_out)},
    }
    metadata_path = output_dir / f"{FIGURE_STEM}_metadata.json"
    metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    qa_path = output_dir / f"{FIGURE_STEM}_QA.md"
    qa_lines = [
        f"# {FIGURE_STEM} QA",
        "",
        f"Status: **{RELEASE_STATUS}**",
        "",
        "## Contract result",
        "",
        "- PASS: panel a distinguishes production control, `dense shadow; no feedback`, and coupled dense.",
        "- PASS: panel b shows fresh matched voltage trajectories and aligned `Delta V`.",
        "- PASS: panel c uses each solve's own `eps_s(Q)` and distinct calibrated-trajectory, island-half, and film-percolation markers.",
        "- PASS: vector masters retain editable text; 600 dpi PNG/TIFF previews have the expected quantized pixel dimensions.",
        "- PASS: full source trajectories, threshold definitions and endpoint/crossing summaries are machine readable.",
        "- PASS: registered tighter-tolerance and 7776-element true-mesh convergence comparators passed.",
        "",
        "## Numerical traceability",
        "",
        f"- comparison SHA-256: `{input_hashes['comparison_csv']}`",
        f"- summary SHA-256: `{input_hashes['summary_json']}`",
        f"- matched-manifest SHA-256: `{input_hashes['matched_manifest']}`",
        f"- source-copy SHA-256: `{settings['source_copy_sha256']}` (byte-identical inputs)",
        f"- interpolation: {qa_checks['crossing_interpolation']}",
        f"- raster dimensions: `{expected_px[0]} x {expected_px[1]}` px at `{RASTER_DPI}` dpi",
        f"- resolved font: `{font_path}`",
        "",
        "## Interpretation boundary",
        "",
        "The figure supports causal model-closure sensitivity under fixed continuum settings. It does not identify a unique iodine-deposit morphology from voltage.",
    ]
    qa_path.write_text("\n".join(qa_lines) + "\n", encoding="utf-8")

    print(json.dumps({
        "status": RELEASE_STATUS,
        "output_dir": str(output_dir),
        "figure_files": {k: str(v) for k, v in figure_paths.items()},
        "source_data": str(source_path),
        "threshold_definitions": str(thresholds_path),
        "endpoint_summary": str(endpoints_path),
        "metadata": str(metadata_path),
        "qa": str(qa_path),
        "pixels": expected_px,
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
