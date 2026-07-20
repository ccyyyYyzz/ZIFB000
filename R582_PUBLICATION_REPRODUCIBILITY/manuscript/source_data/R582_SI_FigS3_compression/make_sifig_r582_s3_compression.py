#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Render R582 Supplementary Figure S3 from frozen thickness endpoints.

The March explicit-thickness cells are connected only as a descriptive series.
The 2.0 mm standard-cell record is a cross-batch proxy and remains open and
unconnected in every panel.
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
BASE = FIGURE_DIR / "SIFig_R582_S3_compression"

PANEL_SOURCE = (
    PROJECT
    / "manuscript"
    / "source_data"
    / "Fig_R581_experimental_evidence"
    / "R581_experimental_evidence_panel_c_compression.csv"
)
SENSITIVITY_SOURCE = (
    PROJECT
    / "battery_experiment"
    / "02_processed_data"
    / "R581_COMPRESSION_EVIDENCE_REBUILD"
    / "endpoint_sensitivity.csv"
)
EXPECTED_SHA256 = {
    PANEL_SOURCE: "18CAAF72F8087C44AFCDF85F3B6476DE8EC06E72D9FA0776B6BCDC4E3C7E0D89",
    SENSITIVITY_SOURCE: "30A9D0B7E4CE2416ACA886DCB1E52B1550DF01EF4699E8AE93D3BDA49DE77BBE",
}

PRIMARY_PLOT = HERE / "R582_SIFig_S3_plot_primary_85pct.csv"
SENSITIVITY_PLOT = HERE / "R582_SIFig_S3_plot_threshold_sensitivity.csv"
INPUT_MANIFEST = HERE / "R582_SIFig_S3_input_manifest.csv"
RENDER_MANIFEST = HERE / "R582_SIFig_S3_render_manifest.json"

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
        "svg.hashsalt": "R582_SIFig_S3_compression",
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
TEAL = "#397A78"
AMBER = "#B5792A"
CARMINE = "#A94C45"
INK = "#20252A"
MID_GREY = "#6D7378"
LIGHT_GREY = "#E3E6E8"
WHITE = "#FFFFFF"
THRESHOLD_STYLE = {
    80: {"color": TEAL, "ls": (0, (1.4, 1.3)), "marker": "s", "lw": 1.0},
    85: {"color": NAVY, "ls": "-", "marker": "o", "lw": 1.3},
    90: {"color": AMBER, "ls": (0, (4.0, 1.8)), "marker": "^", "lw": 1.0},
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def rel(path: Path) -> str:
    return path.resolve().relative_to(PROJECT.resolve()).as_posix()


def as_bool(series: pd.Series) -> pd.Series:
    return series.astype(str).str.strip().str.lower().eq("true")


def verify_inputs() -> None:
    for path, expected in EXPECTED_SHA256.items():
        if not path.is_file():
            raise FileNotFoundError(path)
        observed = sha256(path)
        if observed != expected:
            raise ValueError(f"Frozen input hash mismatch for {path}: {observed}")
    pd.DataFrame(
        [
            {
                "source_key": path.stem,
                "path_workspace_relative": rel(path),
                "size_bytes": path.stat().st_size,
                "sha256": expected,
                "used_for": (
                    "primary 85% CE-qualified command brackets"
                    if path == PANEL_SOURCE
                    else "80/85/90% endpoint-definition sensitivity"
                ),
                "immutable_registered_input": True,
            }
            for path, expected in EXPECTED_SHA256.items()
        ]
    ).to_csv(INPUT_MANIFEST, index=False, lineterminator="\n")


def load_and_freeze_plot_data() -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    verify_inputs()
    primary_source = pd.read_csv(PANEL_SOURCE)
    sensitivity_source = pd.read_csv(SENSITIVITY_SOURCE)
    common = [
        "test_id",
        "thickness_mm",
        "display_label",
        "role",
        "acquisition_campaign",
        "is_cross_batch_proxy",
        "n_cell",
        "ce_threshold_pct",
        "last_passing_commanded_areal_mAh_cm2",
        "first_failing_commanded_areal_mAh_cm2",
        "endpoint_right_censored",
        "raw_sha256",
    ]
    for name, frame in [("primary", primary_source), ("sensitivity", sensitivity_source)]:
        missing = sorted(set(common) - set(frame.columns))
        if missing:
            raise ValueError(f"{name} source missing columns: {missing}")

    primary = primary_source[common + ["endpoint_interval_label", "connect_explicit_trend"]].copy()
    sensitivity = sensitivity_source[common].copy()
    primary["is_cross_batch_proxy"] = as_bool(primary["is_cross_batch_proxy"])
    primary["endpoint_right_censored"] = as_bool(primary["endpoint_right_censored"])
    sensitivity["is_cross_batch_proxy"] = as_bool(sensitivity["is_cross_batch_proxy"])
    sensitivity["endpoint_right_censored"] = as_bool(sensitivity["endpoint_right_censored"])

    if len(primary) != 4 or not primary["ce_threshold_pct"].astype(float).eq(85.0).all():
        raise ValueError("Primary table must contain four 85% threshold rows")
    if len(sensitivity) != 12 or sorted(sensitivity["ce_threshold_pct"].astype(int).unique()) != [80, 85, 90]:
        raise ValueError("Sensitivity table must contain four thicknesses by three thresholds")
    if not primary["n_cell"].astype(int).eq(1).all() or not sensitivity["n_cell"].astype(int).eq(1).all():
        raise ValueError("Every thickness condition must remain one physical cell")
    if primary["endpoint_right_censored"].any() or sensitivity["endpoint_right_censored"].any():
        raise ValueError("All displayed brackets must have observed first-fail commands")
    proxy_thicknesses = sorted(primary.loc[primary["is_cross_batch_proxy"], "thickness_mm"].astype(float))
    if proxy_thicknesses != [2.0]:
        raise ValueError(f"Unexpected cross-batch proxy set: {proxy_thicknesses}")
    explicit_thicknesses = sorted(primary.loc[~primary["is_cross_batch_proxy"], "thickness_mm"].astype(float))
    if explicit_thicknesses != [1.5, 2.5, 3.0]:
        raise ValueError(f"Unexpected explicit March thickness set: {explicit_thicknesses}")

    frozen_85 = sensitivity.loc[sensitivity["ce_threshold_pct"].astype(float).eq(85.0)].sort_values("thickness_mm")
    compare_columns = [
        "thickness_mm",
        "last_passing_commanded_areal_mAh_cm2",
        "first_failing_commanded_areal_mAh_cm2",
    ]
    if not primary.sort_values("thickness_mm")[compare_columns].reset_index(drop=True).equals(
        frozen_85[compare_columns].reset_index(drop=True)
    ):
        raise ValueError("The 85% primary panel does not match endpoint_sensitivity.csv")

    for frame in [primary, sensitivity]:
        frame.insert(0, "supporting_electrolyte", "NH4Br")
        frame["independent_unit"] = "one physical cell/file hash per thickness"
        frame["bracket_semantics"] = (
            "[highest command with within-cell median CE at or above threshold, first higher observed failure); not a CI"
        )
    primary.to_csv(PRIMARY_PLOT, index=False, float_format="%.12g", lineterminator="\n")
    sensitivity.to_csv(SENSITIVITY_PLOT, index=False, float_format="%.12g", lineterminator="\n")

    audit = {
        "physical_cells": 4,
        "n_cell_per_thickness": 1,
        "explicit_March_2025_thicknesses_mm": explicit_thicknesses,
        "cross_batch_proxy_thickness_mm": 2.0,
        "thresholds_pct": [80, 85, 90],
        "primary_threshold_pct": 85,
        "proxy_connected_to_explicit_series": False,
        "population_interval_drawn": False,
    }
    return primary, sensitivity, audit


def style_axis(ax) -> None:
    ax.spines["left"].set_color(INK)
    ax.spines["bottom"].set_color(INK)
    ax.tick_params(colors=INK, direction="out", pad=2.0)
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, color=LIGHT_GREY, lw=0.55)


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


def draw_primary(ax, primary: pd.DataFrame) -> None:
    style_axis(ax)
    add_panel_label(ax, "a")
    ax.set_title("Primary 85% CE command brackets", loc="left", pad=3.0)
    explicit = primary.loc[~primary["is_cross_batch_proxy"]].sort_values("thickness_mm")
    ax.plot(
        explicit["thickness_mm"],
        explicit["last_passing_commanded_areal_mAh_cm2"],
        color=NAVY,
        lw=1.25,
        marker="o",
        ms=4.8,
        mfc=NAVY,
        mec=WHITE,
        mew=0.55,
        zorder=3,
    )
    for row in primary.sort_values("thickness_mm").itertuples():
        x = float(row.thickness_mm)
        y_pass = float(row.last_passing_commanded_areal_mAh_cm2)
        y_fail = float(row.first_failing_commanded_areal_mAh_cm2)
        is_proxy = bool(row.is_cross_batch_proxy)
        color = CARMINE if is_proxy else NAVY
        ax.vlines(x, y_pass, y_fail, color=color, lw=1.35, zorder=4)
        ax.hlines(y_fail, x - 0.055, x + 0.055, color=color, lw=1.35, zorder=4)
        if is_proxy:
            ax.scatter(x, y_pass, s=42, marker="D", facecolor=WHITE, edgecolor=CARMINE, linewidth=1.15, zorder=6)
        ax.text(
            x + (0.08 if not is_proxy else -0.08),
            (y_pass + y_fail) / 2.0,
            ("proxy " if is_proxy else "") + str(row.endpoint_interval_label),
            ha="left" if not is_proxy else "right",
            va="center",
            fontsize=6.5,
            color=color,
        )
    ax.set_xlim(1.35, 3.18)
    ax.set_ylim(45, 168)
    ax.set_xticks([1.5, 2.0, 2.5, 3.0])
    ax.set_yticks([60, 80, 100, 120, 140, 160])
    ax.set_xlabel("Nominal felt thickness (mm)")
    ax.set_ylabel("Commanded charge capacity (mAh cm−2)")


def draw_sensitivity(ax, sensitivity: pd.DataFrame) -> None:
    style_axis(ax)
    add_panel_label(ax, "b")
    ax.set_title("Endpoint-definition sensitivity", loc="left", pad=3.0)
    explicit = sensitivity.loc[~sensitivity["is_cross_batch_proxy"]]
    for threshold in [80, 85, 90]:
        style = THRESHOLD_STYLE[threshold]
        line = explicit.loc[explicit["ce_threshold_pct"].astype(int).eq(threshold)].sort_values("thickness_mm")
        ax.plot(
            line["thickness_mm"],
            line["last_passing_commanded_areal_mAh_cm2"],
            color=style["color"],
            ls=style["ls"],
            lw=style["lw"],
            marker=style["marker"],
            ms=4.4,
            mfc=style["color"],
            mec=WHITE,
            mew=0.5,
            zorder=3 if threshold == 85 else 2,
        )
    label_y = {80: 151.0, 85: 143.0, 90: 135.0}
    for threshold in [80, 85, 90]:
        style = THRESHOLD_STYLE[threshold]
        ax.plot([3.0, 3.10], [140.0, label_y[threshold]], color=style["color"], ls=style["ls"], lw=0.7)
        ax.text(3.12, label_y[threshold], f"{threshold}%", ha="left", va="center", fontsize=6.5, color=style["color"], fontweight="bold" if threshold == 85 else "normal")

    proxy = sensitivity.loc[sensitivity["is_cross_batch_proxy"]]
    proxy_values = sorted(proxy["last_passing_commanded_areal_mAh_cm2"].astype(float).unique())
    if proxy_values != [100.0]:
        raise ValueError(f"Expected the proxy to remain at 100 for all thresholds: {proxy_values}")
    ax.scatter(2.0, 100.0, s=46, marker="D", facecolor=WHITE, edgecolor=CARMINE, linewidth=1.15, zorder=6)
    ax.text(2.0, 108.0, "proxy: 80/85/90%", ha="center", va="bottom", fontsize=6.5, color=CARMINE)
    ax.set_xlim(1.35, 3.28)
    ax.set_ylim(45, 168)
    ax.set_xticks([1.5, 2.0, 2.5, 3.0])
    ax.set_yticks([60, 80, 100, 120, 140, 160])
    ax.set_xlabel("Nominal felt thickness (mm)")
    ax.set_ylabel("Last-passing command (mAh cm−2)")


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


def build_figure(primary: pd.DataFrame, sensitivity: pd.DataFrame) -> tuple[plt.Figure, dict]:
    width_mm, height_mm = 180.0, 96.0
    fig, axes = plt.subplots(1, 2, figsize=(width_mm / 25.4, height_mm / 25.4))
    fig.subplots_adjust(left=0.080, right=0.985, bottom=0.205, top=0.810, wspace=0.31)
    draw_primary(axes[0], primary)
    draw_sensitivity(axes[1], sensitivity)
    fig.text(0.080, 0.945, "One physical cell per thickness condition", ha="left", va="top", fontsize=7.5, fontweight="bold", color=INK)
    fig.text(0.985, 0.945, "The 2.0 mm cross-batch proxy remains open and unconnected", ha="right", va="top", fontsize=6.5, color=MID_GREY)
    fig.text(0.080, 0.045, "Bracket = [highest passing command, first higher observed failure); not a confidence interval", ha="left", va="bottom", fontsize=6.5, color=MID_GREY)
    fig.text(0.985, 0.045, "Lines connect only the three March 2025 explicit-thickness cells", ha="right", va="bottom", fontsize=6.5, color=MID_GREY)
    return fig, {
        "width_mm": width_mm,
        "height_mm": height_mm,
        "font_audit": audit_figure_text(fig),
    }


def export_figure(fig: plt.Figure) -> None:
    fixed_time = datetime(2026, 7, 20, tzinfo=timezone.utc)
    title = "Protocol-bounded capacity brackets across existing felt-thickness cells"
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
            "Existing thickness cells provide descriptive protocol brackets whose ordering persists across "
            "the prespecified CE thresholds; the 2.0 mm cross-batch proxy is not part of that connected series."
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
            "Each thickness is one physical cell. The brackets are observed program intervals, not confidence "
            "intervals, and no population scaling law is inferred."
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
    primary, sensitivity, data_audit = load_and_freeze_plot_data()
    fig, figure_audit = build_figure(primary, sensitivity)
    export_figure(fig)
    write_render_manifest(figure_audit, data_audit)
    print(f"Wrote {BASE}.{{svg,pdf,png,tiff}} with deterministic source records")


if __name__ == "__main__":
    main()
