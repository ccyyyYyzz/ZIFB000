#!/usr/bin/env python
"""Build R582 Figure 6: solved transport and operating levers.

The drawing uses only the compact, audited source tables stored beside this
script.  It never opens or mutates a COMSOL model.  Evidence class is encoded
visibly by marker and line style, and interpolation is restricted to declared
verified intervals.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

os.environ.setdefault("SOURCE_DATE_EPOCH", "1784505600")

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import font_manager
from matplotlib.lines import Line2D
from PIL import Image


SOURCE_DATA_DIR = Path(__file__).resolve().parent.parent
if str(SOURCE_DATA_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DATA_DIR))
from r582_font_runtime import font_hashes_by_role, register_termes_fonts


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
FIG_DIR = ROOT / "manuscript" / "figures_R582"
FIG_DIR.mkdir(parents=True, exist_ok=True)

STEM = "Fig_R582_operating_levers"
WIDTH_MM = 180.0
HEIGHT_MM = 115.0
MM_PER_INCH = 25.4
Q0 = 83.0201994718443
FIXED_DATE = datetime(2026, 7, 20, tzinfo=timezone.utc)

FONT_DIR, FONT_FILES, FONT_FAMILY = register_termes_fonts(font_manager)

COL = {
    "graphite": "#4D4D4D",
    "light_graphite": "#9A9A9A",
    "pale": "#E7E5E1",
    "vermilion": "#D65345",
    "blue": "#3B6FB6",
    "pale_blue": "#DCE7F4",
    "teal": "#2A9D8F",
    "violet": "#7A68A6",
    "amber": "#D8912B",
    "cyan": "#67A9B7",
    "white": "#FFFFFF",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest().upper()


def register_fonts() -> dict[str, str]:
    return font_hashes_by_role(FONT_FILES)


def apply_style() -> None:
    matplotlib.rcParams.update(
        {
            "font.family": FONT_FAMILY,
            "font.serif": [FONT_FAMILY],
            "font.size": 7.2,
            "font.weight": "normal",
            "axes.labelsize": 7.2,
            "axes.titlesize": 7.2,
            "axes.linewidth": 0.65,
            "axes.edgecolor": COL["graphite"],
            "axes.labelcolor": COL["graphite"],
            "xtick.labelsize": 6.5,
            "ytick.labelsize": 6.5,
            "xtick.color": COL["graphite"],
            "ytick.color": COL["graphite"],
            "xtick.major.size": 2.5,
            "ytick.major.size": 2.5,
            "xtick.major.width": 0.6,
            "ytick.major.width": 0.6,
            "xtick.direction": "out",
            "ytick.direction": "out",
            "legend.fontsize": 6.5,
            "legend.frameon": False,
            "lines.linewidth": 1.15,
            "lines.markersize": 4.2,
            "figure.facecolor": "white",
            "savefig.facecolor": "white",
            "savefig.edgecolor": "white",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "pdf.compression": 9,
            "svg.fonttype": "none",
            "svg.hashsalt": "R582_Fig6_operating_levers",
            "mathtext.fontset": "custom",
            "mathtext.rm": FONT_FAMILY,
            "mathtext.it": f"{FONT_FAMILY}:italic",
            "mathtext.bf": f"{FONT_FAMILY}:bold",
            "mathtext.cal": FONT_FAMILY,
            "mathtext.sf": FONT_FAMILY,
            "mathtext.fallback": None,
        }
    )


def load_and_validate() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    current = pd.read_csv(HERE / "R582_Fig6_current_solved.csv")
    deff = pd.read_csv(HERE / "R582_Fig6_deff_solved.csv")
    secondary = pd.read_csv(HERE / "R582_Fig6_secondary_levers.csv")
    decision = pd.read_csv(HERE / "R582_Fig6_decision_map.csv")

    np.testing.assert_allclose(
        deff["D_eff_over_D0"].to_numpy(float),
        np.array([0.5, 0.6, 0.8, 1.0, 1.2, 1.5, 2.0]),
        rtol=0,
        atol=1e-12,
    )
    if not (deff["evidence_class"] == "full_solve").all():
        raise AssertionError("Every D_eff response anchor must be a full solve")
    j80 = current.loc[current["J_mA_cm2"] == 80].iloc[0]
    if j80["relation"] != "lower_bound" or not j80["S_avg_peak"] < 1:
        raise AssertionError("The J=80 point must remain a strict lower bound")
    j20_j40 = current[current["J_mA_cm2"].isin([20, 40])]
    if len(j20_j40) != 2 or not (j20_j40["relation"] == "exact_crossing").all():
        raise AssertionError("The only connected current interval is J=20 to J=40")

    for row in decision.itertuples(index=False):
        low = 100.0 * (row.low_Q_s_mAh_cm2 - Q0) / Q0
        high = 100.0 * (row.high_Q_s_mAh_cm2 - Q0) / Q0
        if abs(low - row.low_delta_Qs_pct) > 2e-9 or abs(high - row.high_delta_Qs_pct) > 2e-9:
            raise AssertionError(f"Decision-map percentage mismatch for {row.lever}")

    krow = secondary.loc[secondary["lever"] == "smooth permeability replacement"].iloc[0]
    if not pd.isna(krow["Q_s_mAh_cm2"]):
        raise AssertionError("Permeability replacement must not be assigned a fictitious Q_s")
    return current, deff, secondary, decision


def clean_axes(ax: plt.Axes) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(pad=2)


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


def draw_current(ax: plt.Axes, current: pd.DataFrame) -> None:
    exact = current[current["relation"] == "exact_crossing"].sort_values("J_mA_cm2")
    connected = exact[exact["J_mA_cm2"].isin([20, 40])]
    ax.plot(
        connected["J_mA_cm2"],
        connected["Q_s_mAh_cm2"],
        color=COL["vermilion"],
        lw=1.25,
        zorder=2,
    )
    ax.scatter(
        exact["J_mA_cm2"],
        exact["Q_s_mAh_cm2"],
        s=21,
        marker="o",
        facecolor=COL["vermilion"],
        edgecolor=COL["white"],
        linewidth=0.55,
        zorder=3,
    )
    base = exact.loc[exact["J_mA_cm2"] == 40].iloc[0]
    ax.scatter(
        [base["J_mA_cm2"]],
        [base["Q_s_mAh_cm2"]],
        s=38,
        marker="o",
        facecolor="none",
        edgecolor=COL["graphite"],
        linewidth=0.75,
        zorder=4,
    )

    bound = current.loc[current["relation"] == "lower_bound"].iloc[0]
    bx, by = float(bound["J_mA_cm2"]), float(bound["Q_s_mAh_cm2"])
    ax.scatter(
        [bx],
        [by],
        s=30,
        marker="^",
        facecolor=COL["white"],
        edgecolor=COL["vermilion"],
        linewidth=0.9,
        zorder=4,
    )
    ax.annotate(
        "",
        xy=(bx, by + 10),
        xytext=(bx, by + 2.0),
        arrowprops=dict(arrowstyle="-|>", color=COL["vermilion"], lw=0.8, mutation_scale=6),
        zorder=3,
    )

    labels = {
        20: (2.5, 3.0, "106.3"),
        40: (2.5, 3.0, "83.0"),
        120: (-2.5, 5.0, "8.4"),
    }
    for row in exact.itertuples(index=False):
        dx, dy, txt = labels[int(row.J_mA_cm2)]
        ax.text(
            row.J_mA_cm2 + dx,
            row.Q_s_mAh_cm2 + dy,
            txt,
            ha="left" if dx > 0 else "right",
            va="bottom",
            fontsize=6.5,
            color=COL["graphite"],
        )
    ax.text(bx + 3.5, by + 3.0, ">$40$", ha="left", va="bottom", fontsize=6.5, color=COL["graphite"])
    ax.text(
        0.98,
        0.97,
        "solved markers",
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
    ax.set_ylabel(r"Modeled marker, $Q_{\rm s}$ (mAh cm$^{-2}$)")
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
        s=21,
        marker="o",
        facecolor=COL["blue"],
        edgecolor=COL["white"],
        linewidth=0.55,
        zorder=3,
    )
    idx = int(np.flatnonzero(np.isclose(x, 1.0))[0])
    ax.scatter(
        [x[idx]],
        [y[idx]],
        s=40,
        marker="o",
        facecolor="none",
        edgecolor=COL["graphite"],
        linewidth=0.75,
        zorder=4,
    )
    ax.text(x[0] + 0.04, y[0] + 3.2, "45.0", fontsize=6.5, color=COL["graphite"])
    ax.text(x[idx] + 0.04, y[idx] + 3.2, "83.0", fontsize=6.5, color=COL["graphite"])
    ax.text(x[-1] - 0.03, y[-1] - 5.0, "106.2", ha="right", fontsize=6.5, color=COL["graphite"])
    ax.text(
        1.10,
        49.0,
        "MD-bounded\nprior",
        ha="center",
        va="bottom",
        fontsize=6.5,
        color=COL["blue"],
    )
    ax.text(
        0.03,
        0.97,
        "7 solved trajectories",
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


def draw_decision_map(ax: plt.Axes, decision: pd.DataFrame) -> None:
    decision = decision.sort_values("row_order")
    labels = [
        r"$D_{\rm eff}$ solved, 0.5–2.0 $D_0$",
        r"$J$ solved, 20–40 mA cm$^{-2}$",
        r"$D_{\rm eff}$ prior, 0.8–1.4 $D_0$",
        r"flow $\delta(v)$, 25–100; $m=0.5$",
        r"felt branch, 1.5–3.0 mm",
        r"flow solved, 25–100 mL min$^{-1}$",
    ]
    colors = [COL["blue"], COL["vermilion"], COL["cyan"], COL["teal"], COL["violet"], COL["graphite"]]
    markers = ["o", "o", "^", "D", "o", "o"]
    linestyles = ["-", "-", (0, (1.3, 1.7)), (0, (3.2, 2.1)), "-", "-"]
    ycoords = np.arange(len(decision) - 1, -1, -1, dtype=float)

    ax.axvline(0, color="#8E8E8E", lw=0.75, zorder=0)
    for y, row, color, marker, ls in zip(ycoords, decision.itertuples(index=False), colors, markers, linestyles):
        low = float(row.low_delta_Qs_pct)
        high = float(row.high_delta_Qs_pct)
        ref = 0.0
        ax.annotate(
            "",
            xy=(high, y),
            xytext=(low, y),
            arrowprops=dict(
                arrowstyle="-|>",
                color=color,
                lw=1.25,
                linestyle=ls,
                mutation_scale=6.2,
                shrinkA=0,
                shrinkB=0,
            ),
            zorder=2,
        )
        face = COL["white"] if marker == "^" else color
        ax.scatter(
            [low, high],
            [y, y],
            s=22 if marker != "^" else 30,
            marker=marker,
            facecolor=face,
            edgecolor=color,
            linewidth=0.9 if marker == "^" else 0.55,
            zorder=3,
        )
        if min(low, high) < ref < max(low, high):
            ax.scatter(
                [ref],
                [y],
                s=10,
                marker=marker,
                facecolor=COL["white"] if marker == "^" else color,
                edgecolor=color,
                linewidth=0.65,
                zorder=3,
            )
        span = abs(high - low)
        span_text = f"{span:.2f}" if span < 3 else f"{span:.1f}"
        ax.text(34.0, y, span_text, ha="right", va="center", fontsize=6.5, color=COL["graphite"])

    ax.set_yticks(ycoords)
    ax.set_yticklabels(labels)
    ax.tick_params(axis="y", length=0, pad=4)
    ax.set_xlim(-50, 36)
    ax.set_ylim(-0.62, len(decision) - 0.36)
    ax.set_xticks([-40, -20, 0, 20])
    ax.set_xlabel(r"Signed shift from baseline, $\Delta Q_{\rm s}/Q_{{\rm s},0}$ (%)")
    ax.text(
        34.0,
        len(decision) - 0.12,
        "range (%)",
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

    legend = [
        Line2D([0], [0], color=COL["graphite"], lw=1.1, marker="o", markersize=3.8, label="full solve"),
        Line2D([0], [0], color=COL["graphite"], lw=1.1, ls=(0, (3.2, 2.1)), marker="D", markersize=3.4, label="analytical postprocess"),
        Line2D([0], [0], color=COL["graphite"], lw=1.0, ls=(0, (1.3, 1.7)), marker="^", markerfacecolor="white", markersize=4.2, label="bounded prior mapped"),
    ]
    ax.legend(
        handles=legend,
        loc="lower left",
        bbox_to_anchor=(-0.25, 1.015),
        ncol=3,
        handlelength=2.1,
        columnspacing=0.9,
        borderaxespad=0,
    )
    panel_label(ax, "c", -0.45)


def draw_translation(ax: plt.Axes) -> None:
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    panel_label(ax, "d", -0.08)

    ax.text(0.11, 0.97, "lever /\nclosure", fontsize=6.5, fontweight="bold", color=COL["graphite"], va="top", ha="center", linespacing=0.88)
    ax.text(0.44, 0.97, "model\nnode", fontsize=6.5, fontweight="bold", color=COL["graphite"], va="top", ha="center", linespacing=0.88)
    ax.text(0.82, 0.97, "modeled\nconsequence", fontsize=6.5, fontweight="bold", color=COL["graphite"], va="top", ha="center", linespacing=0.88)
    ax.plot([0, 1], [0.86, 0.86], color=COL["graphite"], lw=0.7, clip_on=False)

    rows = [
        ("↓$J$ or\n" + r"↑$D_{\rm eff}$", "generation stress\n" + r"$J/D_{\rm eff}$", "later\n" + r"$Q_{\rm s}$", COL["vermilion"]),
        ("felt\n" + r"$L,\varepsilon$", "inventory +\ntransport", r"small $Q_{\rm s}$" + "\nshift", COL["violet"]),
        ("accessibility", "remaining\nbare area", r"late $V$ /" + "\n" + r"$Q_{\rm f}$", COL["amber"]),
        ("smooth\n" + r"$K$", "Darcy\nchannel", r"$\Delta V_{\rm end}$" + "\n+1.27 mV", COL["teal"]),
    ]
    ys = [0.77, 0.57, 0.37, 0.17]
    for i, ((lever, node, consequence, color), y) in enumerate(zip(rows, ys)):
        ax.text(0.11, y, lever, fontsize=6.5, color=color, va="center", ha="center", linespacing=0.90)
        ax.annotate(
            "",
            xy=(0.31, y),
            xytext=(0.24, y),
            arrowprops=dict(arrowstyle="->", lw=0.65, color=COL["light_graphite"], mutation_scale=5.5),
        )
        ax.text(0.44, y, node, fontsize=6.5, color=COL["graphite"], va="center", ha="center", linespacing=0.90)
        ax.annotate(
            "",
            xy=(0.70, y),
            xytext=(0.62, y),
            arrowprops=dict(arrowstyle="->", lw=0.65, color=COL["light_graphite"], mutation_scale=5.5),
        )
        ax.text(0.82, y, consequence, fontsize=6.5, color=COL["graphite"], va="center", ha="center", linespacing=0.90)
        if i < len(rows) - 1:
            ax.plot([0, 1], [y - 0.10, y - 0.10], color=COL["pale"], lw=0.45, clip_on=False)
    ax.text(
        0.50,
        0.015,
        "positive-electrode model",
        fontsize=6.5,
        fontstyle="italic",
        color=COL["light_graphite"],
        va="bottom",
        ha="center",
    )


def build_figure(current: pd.DataFrame, deff: pd.DataFrame, decision: pd.DataFrame) -> plt.Figure:
    fig = plt.figure(figsize=(WIDTH_MM / MM_PER_INCH, HEIGHT_MM / MM_PER_INCH), dpi=100)
    top = fig.add_gridspec(1, 2, left=0.075, right=0.975, bottom=0.605, top=0.945, wspace=0.34)
    ax_a = fig.add_subplot(top[0, 0])
    ax_b = fig.add_subplot(top[0, 1])
    ax_c = fig.add_axes([0.205, 0.105, 0.435, 0.375])
    ax_d = fig.add_axes([0.685, 0.105, 0.290, 0.375])

    draw_current(ax_a, current)
    draw_deff(ax_b, deff)
    draw_decision_map(ax_c, decision)
    draw_translation(ax_d)
    return fig


def save_outputs(fig: plt.Figure) -> dict[str, Path]:
    pdf = FIG_DIR / f"{STEM}.pdf"
    svg = FIG_DIR / f"{STEM}.svg"
    png = FIG_DIR / f"{STEM}.png"
    tiff = FIG_DIR / f"{STEM}.tiff"
    preview = HERE / f"{STEM}_180mm_preview.png"
    gray = HERE / f"{STEM}_grayscale_QA.png"
    tiff_stage = HERE / f".{STEM}_600dpi_stage.png"

    pdf_meta = {
        "Title": "R582 Figure 6 - transport and operating levers",
        "Author": "ZIFB manuscript team",
        "Subject": "Modeled positive-electrode saturation marker",
        "Keywords": "ZIFB; positive electrode; transport; operating levers",
        "Creator": "deterministic matplotlib R582 figure builder",
        "Producer": "matplotlib PDF backend",
        "CreationDate": FIXED_DATE,
        "ModDate": FIXED_DATE,
    }
    svg_meta = {
        "Title": "R582 Figure 6 - transport and operating levers",
        "Description": "Evidence-class-aware modeled positive-electrode lever comparison",
        "Creator": "deterministic matplotlib R582 figure builder",
        "Date": "2026-07-20",
    }
    png_meta = {
        "Title": "R582 Figure 6 - transport and operating levers",
        "Author": "ZIFB manuscript team",
        "Creation Time": "2026-07-20T00:00:00Z",
    }

    fig.savefig(pdf, format="pdf", metadata=pdf_meta)
    fig.savefig(svg, format="svg", metadata=svg_meta)
    fig.savefig(png, format="png", dpi=400, metadata=png_meta)
    fig.savefig(preview, format="png", dpi=300, metadata=png_meta)
    fig.savefig(tiff_stage, format="png", dpi=600, metadata=png_meta)

    with Image.open(tiff_stage) as im:
        rgb = im.convert("RGB")
        rgb.save(tiff, format="TIFF", dpi=(600, 600), compression="tiff_lzw")
    tiff_stage.unlink()

    with Image.open(preview) as im:
        rgb_gray = im.convert("L").convert("RGB")
        rgb_gray.save(gray, format="PNG", dpi=(300, 300), optimize=False)

    return {"pdf": pdf, "svg": svg, "png": png, "tiff": tiff, "preview": preview, "grayscale": gray}


def write_build_record(outputs: dict[str, Path], font_hashes: dict[str, str]) -> None:
    compact_sources = sorted(HERE.glob("R582_Fig6_*.csv"))
    compact_sources = [p for p in compact_sources if p.name != "R582_Fig6_MANIFEST.csv"]
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
        "compact_source_sha256": {p.name: sha256(p) for p in compact_sources},
        "outputs_sha256": {key: sha256(path) for key, path in outputs.items()},
        "rules": {
            "current_interpolation": "only J=20 to J=40",
            "J80": "strict Q_s > 40 lower bound",
            "D_eff": "adjacent solved anchors only; no fit or extrapolation",
            "analytical_flow": "declared Sherwood postprocess; not a full solve",
            "permeability": "endpoint voltage difference only; no Q_s conversion",
        },
    }
    build_path = HERE / "R582_Fig6_BUILD.json"
    with build_path.open("w", encoding="utf-8", newline="\n") as fh:
        json.dump(record, fh, ensure_ascii=False, indent=2, sort_keys=True)
        fh.write("\n")


def write_manifest(outputs: dict[str, Path]) -> None:
    build_path = HERE / "R582_Fig6_BUILD.json"
    rows: list[tuple[str, str, str, int, str]] = []
    for path in sorted(HERE.iterdir(), key=lambda p: p.name.lower()):
        if not path.is_file() or path.name == "R582_Fig6_MANIFEST.csv" or path.name.startswith("."):
            continue
        role = "source bundle"
        if "preview" in path.name:
            role = "final-size preview"
        elif "grayscale" in path.name:
            role = "grayscale QA"
        rows.append((str(path.relative_to(ROOT)), sha256(path), path.suffix.lower(), path.stat().st_size, role))
    for key, path in sorted(outputs.items()):
        if path.parent == HERE:
            continue
        rows.append((str(path.relative_to(ROOT)), sha256(path), path.suffix.lower(), path.stat().st_size, f"figure output {key}"))
    if build_path not in [Path(ROOT / r[0]) for r in rows]:
        raise RuntimeError("Build record unexpectedly absent from manifest inputs")

    manifest = HERE / "R582_Fig6_MANIFEST.csv"
    with manifest.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh, lineterminator="\n")
        writer.writerow(["relative_path", "sha256", "extension", "bytes", "role"])
        writer.writerows(rows)


def main() -> None:
    font_hashes = register_fonts()
    apply_style()
    current, deff, _secondary, decision = load_and_validate()
    fig = build_figure(current, deff, decision)
    outputs = save_outputs(fig)
    plt.close(fig)
    write_build_record(outputs, font_hashes)
    write_manifest(outputs)
    print(f"Built {STEM} at exactly {WIDTH_MM:g} x {HEIGHT_MM:g} mm")
    for key, path in outputs.items():
        print(f"{key:10s} {path}  {sha256(path)}")


if __name__ == "__main__":
    main()
