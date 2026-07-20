#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Render R582 Supplementary Figure S2 from frozen cell-level summaries.

Physical cells are the visible units. Sequential cycles define within-cell
ranges only; no concentration-response fit or population interval is drawn.
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
BASE = FIGURE_DIR / "SIFig_R582_S2_composition"

SOURCE_DIR = PROJECT / "manuscript" / "source_data" / "Fig_R581_experimental_evidence"
COMPOSITION_SOURCE = SOURCE_DIR / "R581_experimental_evidence_panel_a_composition.csv"
UPSTREAM_MANIFEST = SOURCE_DIR / "R581_experimental_evidence_input_manifest.csv"
EXPECTED_SHA256 = {
    COMPOSITION_SOURCE: "2C02F4571A5D5B584A8F9B654783DD5A07380E37198A571583D046877BE46389",
    UPSTREAM_MANIFEST: "0279B9AE6298707464B79661170A59B4F1B33CD3390C23CA6C63AEC47DA6096C",
}

PLOT_CSV = HERE / "R582_SIFig_S2_plot_cells.csv"
INPUT_MANIFEST = HERE / "R582_SIFig_S2_input_manifest.csv"
RENDER_MANIFEST = HERE / "R582_SIFig_S2_render_manifest.json"

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
        "svg.hashsalt": "R582_SIFig_S2_composition",
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
SKY = "#72A5C3"
INK = "#20252A"
MID_GREY = "#6D7378"
LIGHT_GREY = "#E3E6E8"
WHITE = "#FFFFFF"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def rel(path: Path) -> str:
    return path.resolve().relative_to(PROJECT.resolve()).as_posix()


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
                    "six physical-cell medians and full within-cell sequential-cycle ranges"
                    if path == COMPOSITION_SOURCE
                    else "upstream frozen-source and hash provenance"
                ),
                "immutable_registered_input": True,
            }
            for path, expected in EXPECTED_SHA256.items()
        ]
    ).to_csv(INPUT_MANIFEST, index=False, lineterminator="\n")


def load_and_freeze_plot_data() -> tuple[pd.DataFrame, dict]:
    verify_inputs()
    source = pd.read_csv(COMPOSITION_SOURCE)
    required = [
        "concentration_M",
        "cell_id",
        "target_command_mAh_cm2",
        "n_run_files",
        "n_pairs",
        "delivered_median_mAh_cm2",
        "delivered_min_mAh_cm2",
        "delivered_max_mAh_cm2",
        "ce_median_pct",
        "raw_sha256s",
        "n_cell",
        "cell_endpoint_median_mAh_cm2",
        "cell_endpoint_min_mAh_cm2",
        "cell_endpoint_max_mAh_cm2",
        "n_right_censored_85pct",
        "plot_x",
    ]
    missing = sorted(set(required) - set(source.columns))
    if missing:
        raise ValueError(f"Composition source missing columns: {missing}")

    expected_cells = {0: 1, 1: 1, 2: 1, 3: 2, 4: 1}
    observed_cells = (
        source.groupby("concentration_M", sort=True)["n_cell"].first().astype(int).to_dict()
    )
    if observed_cells != expected_cells:
        raise ValueError(f"Unexpected physical-cell count map: {observed_cells}")
    if len(source) != 6 or source["cell_id"].nunique() != 6:
        raise ValueError("S2 must contain exactly six physical-cell summaries")
    if not source["population_interval"].astype(str).eq("none").all():
        raise ValueError("Population intervals are not permitted for this sparse cell series")
    if source.loc[source["concentration_M"].ne(3), "n_right_censored_85pct"].astype(int).ne(0).any():
        raise ValueError("Unexpected censoring outside the 3 M condition")
    if not source.loc[source["concentration_M"].eq(3), "n_right_censored_85pct"].astype(int).eq(1).all():
        raise ValueError("The frozen 3 M condition must record one right-censored cell endpoint")

    plot = source[required].copy()
    plot.insert(0, "supporting_electrolyte", "NH4Br")
    plot["independent_unit"] = "physical cell after conservative continuation stitching"
    plot["range_semantics"] = "full within-cell sequential-cycle range; not between-cell uncertainty"
    plot["fit_drawn"] = False
    plot.to_csv(PLOT_CSV, index=False, float_format="%.12g", lineterminator="\n")
    audit = {
        "physical_cells": 6,
        "n_cell_by_concentration_M": expected_cells,
        "n_pairs_by_cell": {
            str(row.cell_id): int(row.n_pairs) for row in plot.itertuples()
        },
        "right_censored_cells_by_condition": {"3 M": 1},
        "sequential_cycles_used_as_independent_replicates": False,
        "concentration_fit_drawn": False,
    }
    return plot, audit


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


def build_figure(plot: pd.DataFrame) -> tuple[plt.Figure, dict]:
    width_mm, height_mm = 180.0, 82.0
    fig, ax = plt.subplots(figsize=(width_mm / 25.4, height_mm / 25.4))
    fig.subplots_adjust(left=0.085, right=0.985, bottom=0.235, top=0.800)
    ax.spines["left"].set_color(INK)
    ax.spines["bottom"].set_color(INK)
    ax.tick_params(colors=INK, direction="out", pad=2.0)
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, color=LIGHT_GREY, lw=0.55)

    for row in plot.itertuples():
        x = float(row.plot_x)
        y_lo = float(row.delivered_min_mAh_cm2)
        y_hi = float(row.delivered_max_mAh_cm2)
        y_mid = float(row.delivered_median_mAh_cm2)
        ax.vlines(x, y_lo, y_hi, color=SKY, linewidth=1.25, zorder=2)
        ax.hlines([y_lo, y_hi], x - 0.035, x + 0.035, color=SKY, linewidth=0.9, zorder=2)
        ax.scatter(x, y_mid, s=34, marker="o", facecolor=NAVY, edgecolor=WHITE, linewidth=0.65, zorder=4)
        if int(row.concentration_M) == 3:
            label = "cell A" if str(row.cell_id).endswith("A") else "cell B"
            offset = 5.2 if str(row.cell_id).endswith("A") else -5.2
            va = "bottom" if offset > 0 else "top"
            ax.text(x, y_mid + offset, label, ha="center", va=va, fontsize=6.5, color=NAVY)

    for concentration, group in plot.groupby("concentration_M", sort=True):
        median = float(group["cell_endpoint_median_mAh_cm2"].iloc[0])
        n_cell = int(group["n_cell"].iloc[0])
        ax.hlines(median, float(concentration) - 0.20, float(concentration) + 0.20, color=INK, linewidth=1.55, zorder=3)
        label = f"{n_cell} cell" if n_cell == 1 else f"{n_cell} cells"
        ax.text(float(concentration), 158.0, label, ha="center", va="top", fontsize=6.5, color=INK)

    ax.set_xlim(-0.45, 4.45)
    ax.set_ylim(25.0, 162.0)
    ax.set_xticks([0, 1, 2, 3, 4])
    ax.set_yticks([40, 80, 120, 160])
    ax.set_xlabel("NH4Br concentration (M)")
    ax.set_ylabel("Cell capacity envelope (mAh cm−2)")
    ax.set_title("Physical-cell summaries; no fitted concentration law", loc="left", pad=4.0)

    fig.text(
        0.085,
        0.930,
        "One marker per physical cell",
        ha="left",
        va="top",
        fontsize=7.5,
        fontweight="bold",
        color=INK,
    )
    fig.text(
        0.985,
        0.930,
        "3 M: one of two endpoints is right-censored",
        ha="right",
        va="top",
        fontsize=6.5,
        color=MID_GREY,
    )
    fig.text(
        0.085,
        0.045,
        "Point: within-cell median   Vertical range: full sequential-cycle range   Black bar: condition median",
        ha="left",
        va="bottom",
        fontsize=6.5,
        color=MID_GREY,
    )
    fig.text(
        0.985,
        0.045,
        "Ranges are descriptive, not population intervals",
        ha="right",
        va="bottom",
        fontsize=6.5,
        color=MID_GREY,
    )
    return fig, {
        "width_mm": width_mm,
        "height_mm": height_mm,
        "font_audit": audit_figure_text(fig),
    }


def export_figure(fig: plt.Figure) -> None:
    fixed_time = datetime(2026, 7, 20, tzinfo=timezone.utc)
    title = "Cell-level descriptive capacity envelope across NH4Br conditions"
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
            "The existing physical-cell records define a descriptive composition-associated capacity envelope, "
            "not a fitted NH4Br concentration law."
        ),
        "evidence_class": "E-EXP",
        "frozen_date": "2026-07-20",
        "final_size_mm": {"width": figure_audit["width_mm"], "height": figure_audit["height_mm"]},
        "font": {
            "family": FONT_FAMILY,
            "base_pt": 7.2,
            "minimum_pt": 6.5,
            "registered_faces": [{"path": str(path), "sha256": sha256(path)} for path in TERMES_PATHS],
            **figure_audit["font_audit"],
        },
        "statistical_boundary": (
            "Physical cells are the independent units; sequential cycles produce within-cell ranges only. "
            "No population interval, significance test, optimum or concentration-response fit is supported."
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
    plot, data_audit = load_and_freeze_plot_data()
    fig, figure_audit = build_figure(plot)
    export_figure(fig)
    write_render_manifest(figure_audit, data_audit)
    print(f"Wrote {BASE}.{{svg,pdf,png,tiff}} with deterministic source records")


if __name__ == "__main__":
    main()
