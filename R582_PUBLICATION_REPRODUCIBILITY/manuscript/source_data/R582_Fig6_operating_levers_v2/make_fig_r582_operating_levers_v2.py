#!/usr/bin/env python
"""Build the three-panel R582 Figure 6 v2 without changing v1."""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

os.environ.setdefault("SOURCE_DATE_EPOCH", "1784505600")
sys.dont_write_bytecode = True

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from PIL import Image


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
V1_DIR = HERE.parent / "R582_Fig6_operating_levers"
V1_SCRIPT = V1_DIR / "make_fig_r582_operating_levers.py"
FIG_DIR = ROOT / "manuscript" / "figures_R582"
FIG_DIR.mkdir(parents=True, exist_ok=True)

STEM = "Fig_R582_operating_levers_v2"
WIDTH_MM = 180.0
HEIGHT_MM = 115.0
MM_PER_INCH = 25.4
FIXED_DATE = datetime(2026, 7, 20, tzinfo=timezone.utc)


def load_v1_module():
    spec = importlib.util.spec_from_file_location("r582_fig6_v1_builder", V1_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import verified v1 builder: {V1_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


V1 = load_v1_module()
COL = V1.COL


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest().upper()


def panel_label(ax: plt.Axes, label: str, x: float = -0.15) -> None:
    ax.text(
        x,
        1.075,
        label,
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=8.0,
        fontweight="bold",
        color="#222222",
        clip_on=False,
    )


def clean_axes(ax: plt.Axes) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(pad=2)


def draw_current(ax: plt.Axes, current: pd.DataFrame) -> None:
    exact = current[current["relation"] == "exact_crossing"].sort_values("J_mA_cm2")
    connected = exact[exact["J_mA_cm2"].isin([20, 40])]

    ax.plot(
        connected["J_mA_cm2"],
        connected["Q_s_mAh_cm2"],
        color=COL["vermilion"],
        lw=1.3,
        zorder=2,
    )
    ax.scatter(
        exact["J_mA_cm2"],
        exact["Q_s_mAh_cm2"],
        s=22,
        marker="o",
        facecolor=COL["vermilion"],
        edgecolor="white",
        linewidth=0.55,
        zorder=3,
    )

    baseline = exact.loc[exact["J_mA_cm2"] == 40].iloc[0]
    ax.scatter(
        [baseline["J_mA_cm2"]],
        [baseline["Q_s_mAh_cm2"]],
        s=40,
        marker="o",
        facecolor="none",
        edgecolor=COL["graphite"],
        linewidth=0.8,
        zorder=4,
    )

    censored = current.loc[current["relation"] == "lower_bound"].iloc[0]
    cx = float(censored["J_mA_cm2"])
    cy = float(censored["Q_s_mAh_cm2"])
    ax.scatter(
        [cx],
        [cy],
        s=32,
        marker="^",
        facecolor="white",
        edgecolor=COL["vermilion"],
        linewidth=1.0,
        zorder=4,
    )
    ax.annotate(
        "",
        xy=(cx, cy + 18),
        xytext=(cx, cy + 2.5),
        arrowprops=dict(
            arrowstyle="-|>",
            color=COL["vermilion"],
            lw=0.9,
            mutation_scale=6.5,
        ),
        zorder=3,
    )
    ax.text(cx + 4.0, cy + 13.2, r"$Q_{\rm s}>40$", ha="left", va="center", fontsize=6.5, color=COL["graphite"])
    ax.text(cx + 4.0, cy + 6.3, "right-censored", ha="left", va="center", fontsize=6.5, color=COL["light_graphite"])

    labels = {
        20: (2.5, 3.0, "106.3"),
        40: (2.5, 3.0, "83.0"),
        120: (-2.5, 5.0, "8.4"),
    }
    for row in exact.itertuples(index=False):
        dx, dy, text = labels[int(row.J_mA_cm2)]
        ax.text(
            row.J_mA_cm2 + dx,
            row.Q_s_mAh_cm2 + dy,
            text,
            ha="left" if dx > 0 else "right",
            va="bottom",
            fontsize=6.5,
            color=COL["graphite"],
        )

    ax.text(
        0.98,
        0.97,
        "full simulations",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=6.5,
        color=COL["light_graphite"],
    )
    ax.set_xlim(10, 128)
    ax.set_ylim(0, 120)
    ax.set_xticks([20, 40, 80, 120])
    ax.set_yticks([0, 40, 80, 120])
    ax.set_xlabel(r"Applied current, $J$ (mA cm$^{-2}$)")
    ax.set_ylabel(r"Averaged saturation point, $Q_{\rm s}$ (mAh cm$^{-2}$)")
    clean_axes(ax)
    panel_label(ax, "a", -0.16)


def draw_deff(ax: plt.Axes, deff: pd.DataFrame) -> None:
    x = deff["D_eff_over_D0"].to_numpy(float)
    y = deff["Q_s_mAh_cm2"].to_numpy(float)
    ax.axvspan(0.8, 1.4, color=COL["pale_blue"], alpha=0.68, lw=0, zorder=0)
    ax.plot(x, y, color=COL["blue"], lw=1.3, zorder=2)
    ax.scatter(
        x,
        y,
        s=22,
        marker="o",
        facecolor=COL["blue"],
        edgecolor="white",
        linewidth=0.55,
        zorder=3,
    )
    base_idx = int(np.flatnonzero(np.isclose(x, 1.0))[0])
    ax.scatter(
        [x[base_idx]],
        [y[base_idx]],
        s=40,
        marker="o",
        facecolor="none",
        edgecolor=COL["graphite"],
        linewidth=0.8,
        zorder=4,
    )
    ax.text(x[0] + 0.04, y[0] + 3.2, "45.0", fontsize=6.5, color=COL["graphite"])
    ax.text(x[base_idx] + 0.04, y[base_idx] + 3.2, "83.0", fontsize=6.5, color=COL["graphite"])
    ax.text(x[-1] - 0.03, y[-1] - 5.0, "106.2", ha="right", fontsize=6.5, color=COL["graphite"])
    ax.text(
        1.10,
        50.0,
        "MD-informed\nrange",
        ha="center",
        va="bottom",
        fontsize=6.5,
        color=COL["blue"],
    )
    ax.text(
        0.03,
        0.97,
        "full simulations",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=6.5,
        color=COL["light_graphite"],
    )
    ax.set_xlim(0.42, 2.08)
    ax.set_ylim(38, 120)
    ax.set_xticks([0.5, 1.0, 1.5, 2.0])
    ax.set_yticks([40, 60, 80, 100, 120])
    ax.set_xlabel(r"Oxidized-carrier diffusivity, $D_{\rm eff}/D_0$")
    ax.set_ylabel(r"$Q_{\rm s}$ (mAh cm$^{-2}$)")
    clean_axes(ax)
    panel_label(ax, "b", -0.16)


def draw_summary(ax: plt.Axes, decision: pd.DataFrame) -> None:
    decision = decision.sort_values("row_order")
    labels = [
        r"Oxidized-carrier $D_{\rm eff}$  (0.5–2.0 $D_0$)",
        r"Applied current $J$  (20–40 mA cm$^{-2}$)",
        r"MD-informed $D_{\rm eff}$  (0.8–1.4 $D_0$)",
        r"Flow-dependent $\delta(v)$  (25–100; $m=0.5$)",
        r"Linked felt geometry  (1.5–3.0 mm)",
        r"Flow rate  (25–100 mL min$^{-1}$)",
    ]
    colors = [
        COL["blue"],
        COL["vermilion"],
        COL["cyan"],
        COL["teal"],
        COL["violet"],
        COL["graphite"],
    ]
    markers = ["o", "o", "^", "D", "o", "o"]
    line_styles = ["-", "-", (0, (1.3, 1.7)), (0, (3.2, 2.1)), "-", "-"]
    ycoords = np.arange(len(decision) - 1, -1, -1, dtype=float)

    ax.axvline(0, color="#8E8E8E", lw=0.75, zorder=0)
    for y, row, color, marker, line_style in zip(
        ycoords, decision.itertuples(index=False), colors, markers, line_styles
    ):
        low = float(row.low_delta_Qs_pct)
        high = float(row.high_delta_Qs_pct)
        ax.annotate(
            "",
            xy=(high, y),
            xytext=(low, y),
            arrowprops=dict(
                arrowstyle="-|>",
                color=color,
                lw=1.3,
                linestyle=line_style,
                mutation_scale=6.3,
                shrinkA=0,
                shrinkB=0,
            ),
            zorder=2,
        )
        face = "white" if marker == "^" else color
        ax.scatter(
            [low, high],
            [y, y],
            s=22 if marker != "^" else 31,
            marker=marker,
            facecolor=face,
            edgecolor=color,
            linewidth=0.95 if marker == "^" else 0.55,
            zorder=3,
        )
        if min(low, high) < 0 < max(low, high):
            ax.scatter(
                [0],
                [y],
                s=10,
                marker=marker,
                facecolor=face,
                edgecolor=color,
                linewidth=0.65,
                zorder=3,
            )
        span = abs(high - low)
        span_text = f"{span:.2f}" if span < 3 else f"{span:.1f}"
        ax.text(34.0, y, span_text, ha="right", va="center", fontsize=6.5, color=COL["graphite"])

    ax.set_yticks(ycoords)
    ax.set_yticklabels(labels)
    ax.tick_params(axis="y", length=0, pad=5)
    ax.set_xlim(-50, 36)
    ax.set_ylim(-0.62, len(decision) - 0.36)
    ax.set_xticks([-40, -20, 0, 20])
    ax.set_xlabel(r"Shift in averaged saturation point, $\Delta Q_{\rm s}/Q_{{\rm s},0}$ (%)")
    ax.text(
        34.0,
        len(decision) - 0.12,
        "span (%)",
        ha="right",
        va="bottom",
        fontsize=6.5,
        fontweight="bold",
        color=COL["graphite"],
    )
    for y in ycoords[:-1]:
        ax.axhline(y - 0.5, color=COL["pale"], lw=0.45, zorder=0)
    clean_axes(ax)
    ax.spines["left"].set_visible(False)

    handles = [
        Line2D([0], [0], color=COL["graphite"], lw=1.1, marker="o", markersize=3.8, label="continuum simulation"),
        Line2D([0], [0], color=COL["graphite"], lw=1.1, ls=(0, (3.2, 2.1)), marker="D", markersize=3.4, label="analytical scenario"),
        Line2D([0], [0], color=COL["graphite"], lw=1.0, ls=(0, (1.3, 1.7)), marker="^", markerfacecolor="white", markersize=4.2, label="MD-informed range"),
    ]
    ax.legend(
        handles=handles,
        loc="lower left",
        bbox_to_anchor=(-0.26, 1.015),
        ncol=3,
        handlelength=2.1,
        columnspacing=1.0,
        borderaxespad=0,
    )
    panel_label(ax, "c", -0.33)


def build_figure(current: pd.DataFrame, deff: pd.DataFrame, decision: pd.DataFrame) -> plt.Figure:
    fig = plt.figure(figsize=(WIDTH_MM / MM_PER_INCH, HEIGHT_MM / MM_PER_INCH), dpi=100)
    top = fig.add_gridspec(
        1,
        2,
        left=0.075,
        right=0.975,
        bottom=0.605,
        top=0.945,
        wspace=0.34,
    )
    ax_a = fig.add_subplot(top[0, 0])
    ax_b = fig.add_subplot(top[0, 1])
    ax_c = fig.add_axes([0.255, 0.105, 0.720, 0.375])

    draw_current(ax_a, current)
    draw_deff(ax_b, deff)
    draw_summary(ax_c, decision)
    return fig


def save_outputs(fig: plt.Figure) -> dict[str, Path]:
    outputs = {
        "pdf": FIG_DIR / f"{STEM}.pdf",
        "svg": FIG_DIR / f"{STEM}.svg",
        "png": FIG_DIR / f"{STEM}.png",
        "tiff": FIG_DIR / f"{STEM}.tiff",
        "preview": HERE / f"{STEM}_180mm_preview.png",
        "grayscale": HERE / f"{STEM}_grayscale_QA.png",
    }
    pdf_meta = {
        "Title": "R582 Figure 6 v2 - transport and operating levers",
        "Author": "ZIFB manuscript team",
        "Subject": "Positive-electrode averaged saturation point",
        "Keywords": "ZIFB; positive electrode; transport; operating levers",
        "Creator": "deterministic matplotlib R582 Figure 6 v2 builder",
        "Producer": "matplotlib PDF backend",
        "CreationDate": FIXED_DATE,
        "ModDate": FIXED_DATE,
    }
    svg_meta = {
        "Title": "R582 Figure 6 v2 - transport and operating levers",
        "Description": "Simulated positive-electrode operating-lever comparison",
        "Creator": "deterministic matplotlib R582 Figure 6 v2 builder",
        "Date": "2026-07-20",
    }
    png_meta = {
        "Title": "R582 Figure 6 v2 - transport and operating levers",
        "Author": "ZIFB manuscript team",
        "Creation Time": "2026-07-20T00:00:00Z",
    }

    fig.savefig(outputs["pdf"], format="pdf", metadata=pdf_meta)
    fig.savefig(outputs["svg"], format="svg", metadata=svg_meta)

    png_stage = HERE / f".{STEM}_400dpi_stage.png"
    tiff_stage = HERE / f".{STEM}_600dpi_stage.png"
    preview_stage = HERE / f".{STEM}_300dpi_stage.png"
    fig.savefig(png_stage, format="png", dpi=400, metadata=png_meta)
    fig.savefig(tiff_stage, format="png", dpi=600, metadata=png_meta)
    fig.savefig(preview_stage, format="png", dpi=300, metadata=png_meta)

    with Image.open(png_stage) as im:
        im.convert("RGB").save(outputs["png"], format="PNG", dpi=(400, 400), optimize=False)
    with Image.open(tiff_stage) as im:
        im.convert("RGB").save(outputs["tiff"], format="TIFF", dpi=(600, 600), compression="tiff_lzw")
    with Image.open(preview_stage) as im:
        rgb = im.convert("RGB")
        rgb.save(outputs["preview"], format="PNG", dpi=(300, 300), optimize=False)
        rgb.convert("L").convert("RGB").save(
            outputs["grayscale"], format="PNG", dpi=(300, 300), optimize=False
        )
    for stage in (png_stage, tiff_stage, preview_stage):
        stage.unlink()
    return outputs


def write_build(outputs: dict[str, Path], font_hashes: dict[str, str]) -> None:
    dependencies = [
        V1_SCRIPT,
        V1_DIR / "R582_Fig6_current_solved.csv",
        V1_DIR / "R582_Fig6_deff_solved.csv",
        V1_DIR / "R582_Fig6_secondary_levers.csv",
        V1_DIR / "R582_Fig6_decision_map.csv",
        V1_DIR / "R582_Fig6_input_manifest.csv",
    ]
    record = {
        "figure": STEM,
        "build_date_fixed": "2026-07-20T00:00:00Z",
        "backend": "Python/matplotlib",
        "matplotlib_version": matplotlib.__version__,
        "canvas_mm": [WIDTH_MM, HEIGHT_MM],
        "base_font_pt": 7.2,
        "minimum_font_pt": 6.5,
        "font_family": "TeX Gyre Termes",
        "font_files_sha256": font_hashes,
        "read_only_dependencies_sha256": {
            str(path.relative_to(ROOT)): sha256(path) for path in dependencies
        },
        "outputs_sha256": {key: sha256(path) for key, path in outputs.items()},
        "integrity_rules": {
            "J80": "right-censored at Q=40; displayed only as Q_s > 40",
            "current_connection": "only J=20 to J=40",
            "D_eff_connection": "adjacent simulated points only; no fit or extrapolation",
            "analytical_flow": "analytical boundary-layer scenario, not a continuum simulation",
            "v1": "read-only and preserved",
        },
    }
    path = HERE / "R582_Fig6_v2_BUILD.json"
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        json.dump(record, fh, ensure_ascii=False, indent=2, sort_keys=True)
        fh.write("\n")


def write_manifest(outputs: dict[str, Path]) -> None:
    rows: list[tuple[str, str, str, int, str]] = []
    for path in sorted(HERE.iterdir(), key=lambda p: p.name.lower()):
        if not path.is_file() or path.name == "R582_Fig6_v2_MANIFEST.csv" or path.name.startswith("."):
            continue
        role = "v2 source bundle"
        if "180mm_preview" in path.name:
            role = "v2 final-size color preview"
        elif "grayscale_QA" in path.name:
            role = "v2 grayscale QA preview"
        rows.append(
            (
                str(path.relative_to(ROOT)),
                sha256(path),
                path.suffix.lower(),
                path.stat().st_size,
                role,
            )
        )
    for key, path in sorted(outputs.items()):
        if path.parent == HERE:
            continue
        rows.append(
            (
                str(path.relative_to(ROOT)),
                sha256(path),
                path.suffix.lower(),
                path.stat().st_size,
                f"v2 figure output {key}",
            )
        )
    manifest = HERE / "R582_Fig6_v2_MANIFEST.csv"
    with manifest.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh, lineterminator="\n")
        writer.writerow(["relative_path", "sha256", "extension", "bytes", "role"])
        writer.writerows(rows)


def main() -> None:
    font_hashes = V1.register_fonts()
    V1.apply_style()
    current, deff, _secondary, decision = V1.load_and_validate()
    fig = build_figure(current, deff, decision)
    outputs = save_outputs(fig)
    plt.close(fig)
    write_build(outputs, font_hashes)
    write_manifest(outputs)
    print(f"Built {STEM} at exactly {WIDTH_MM:g} x {HEIGHT_MM:g} mm")
    for key, path in outputs.items():
        print(f"{key:10s} {path}  {sha256(path)}")


if __name__ == "__main__":
    main()
