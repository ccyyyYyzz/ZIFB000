"""Build the compact R582 Figure 3 v2 spatial-progression candidate."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap, LogNorm, Normalize, SymLogNorm
from matplotlib import font_manager
from matplotlib.patches import Rectangle
from PIL import Image


TERMES_DIR = Path(
    r"D:\Program Files\texlive\2024\texmf-dist\fonts\opentype\public\tex-gyre"
)
TERMES_FILES = (
    "texgyretermes-regular.otf",
    "texgyretermes-bold.otf",
    "texgyretermes-italic.otf",
    "texgyretermes-bolditalic.otf",
)
for font_name in TERMES_FILES:
    font_path = TERMES_DIR / font_name
    if not font_path.is_file():
        raise FileNotFoundError(
            f"Required manuscript-matched font is missing: {font_path}"
        )
    font_manager.fontManager.addfont(font_path)

plt.rcParams["font.family"] = "TeX Gyre Termes"
plt.rcParams["mathtext.fontset"] = "custom"
plt.rcParams["mathtext.rm"] = "TeX Gyre Termes"
plt.rcParams["mathtext.it"] = "TeX Gyre Termes:italic"
plt.rcParams["mathtext.bf"] = "TeX Gyre Termes:bold"
plt.rcParams["mathtext.sf"] = "TeX Gyre Termes"
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["svg.hashsalt"] = "R582-Fig3-spatial-progression-v2-termes"
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42
plt.rcParams["font.size"] = 7.4
plt.rcParams["axes.linewidth"] = 0.65
plt.rcParams["legend.frameon"] = False
plt.rcParams["xtick.major.width"] = 0.65
plt.rcParams["ytick.major.width"] = 0.65
plt.rcParams["xtick.major.size"] = 2.6
plt.rcParams["ytick.major.size"] = 2.6


SCRIPT_DIR = Path(__file__).resolve().parent
MANUSCRIPT_DIR = SCRIPT_DIR.parents[1]
INPUT_CSV = SCRIPT_DIR.parent / "Fig_R545_fields" / "Fig3_baseline_spatial_long.csv"
OUT_DIR = MANUSCRIPT_DIR / "figures_R582"
OUT_BASE = OUT_DIR / "Fig_R582_spatial_progression_v2"
SUBSET_CSV = SCRIPT_DIR / "Fig_R582_spatial_progression_v2_source.csv"
MANIFEST_JSON = SCRIPT_DIR / "render_manifest_v2.json"

EXPECTED_SHA256 = "E322D0D0C4B0D5C8CB84BD5CB18D1A43CBA183EB8A5F112577686993BC8FC007"
DISPLAY_Q = (80.0, 100.0, 120.0)
Q_S = 83.0202
Q_F_CAL = 99.5901
WIDTH_MM = 180.0
HEIGHT_MM = 145.0
MM_PER_INCH = 25.4

REQUIRED_COLUMNS = {
    "time_label",
    "time_s",
    "Q_mAh_cm2",
    "x_m",
    "y_m",
    "eps_s_pos",
    "theta_eff",
    "A_bare_frac",
    "j_total_A_m2",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def validate_and_prepare() -> tuple[pd.DataFrame, dict]:
    source_hash = sha256(INPUT_CSV)
    if source_hash != EXPECTED_SHA256:
        raise RuntimeError(
            f"Input hash changed: expected {EXPECTED_SHA256}, observed {source_hash}."
        )

    source = pd.read_csv(INPUT_CSV)
    missing = REQUIRED_COLUMNS.difference(source.columns)
    if missing:
        raise ValueError(f"Missing required fields: {sorted(missing)}")

    selected = source.loc[
        source["Q_mAh_cm2"].isin(DISPLAY_Q),
        [
            "time_label",
            "time_s",
            "Q_mAh_cm2",
            "x_m",
            "y_m",
            "eps_s_pos",
            "theta_eff",
            "A_bare_frac",
            "j_total_A_m2",
        ],
    ].copy()
    selected = selected.sort_values(["Q_mAh_cm2", "y_m", "x_m"]).reset_index(drop=True)
    selected["A_bare_over_A0"] = 1.0 - selected["theta_eff"]
    selected["A_bare_native_minus_complement"] = (
        selected["A_bare_frac"] - selected["A_bare_over_A0"]
    )

    counts = selected.groupby("Q_mAh_cm2", sort=True).size().to_dict()
    if set(counts) != set(DISPLAY_Q) or any(counts[q] != 5_995 for q in DISPLAY_Q):
        raise ValueError(f"Unexpected capacity/node counts: {counts}")
    if selected.duplicated(["Q_mAh_cm2", "x_m", "y_m"]).any():
        raise ValueError("Duplicate capacity-coordinate rows detected.")
    if not np.isfinite(selected.select_dtypes(include=[np.number]).to_numpy()).all():
        raise ValueError("Non-finite selected or derived values detected.")

    x_values = np.sort(selected["x_m"].unique())
    y_values = np.sort(selected["y_m"].unique())
    if len(x_values) != 55 or len(y_values) != 109:
        raise ValueError(f"Expected a 55 x 109 grid; observed {len(x_values)} x {len(y_values)}.")
    if not np.isclose(x_values[[0, -1]], [0.003, 0.005]).all():
        raise ValueError("Unexpected through-plane coordinate bounds.")
    if not np.isclose(y_values[[0, -1]], [0.0, 0.020]).all():
        raise ValueError("Unexpected flow-direction coordinate bounds.")

    nonpositive = {
        int(q): int((selected.loc[selected["Q_mAh_cm2"].eq(q), "j_total_A_m2"] <= 0).sum())
        for q in DISPLAY_Q
    }
    negative = {
        int(q): int((selected.loc[selected["Q_mAh_cm2"].eq(q), "j_total_A_m2"] < 0).sum())
        for q in DISPLAY_Q
    }
    if nonpositive != {80: 0, 100: 6, 120: 0} or negative != nonpositive:
        raise ValueError(
            f"Signed-current mask changed: nonpositive={nonpositive}, negative={negative}."
        )

    positive_current = selected.loc[selected["j_total_A_m2"] > 0, "j_total_A_m2"]
    if positive_current.min() < 8.0e-5 or positive_current.max() > 2.2e4:
        raise ValueError("Positive current falls outside the declared shared log range.")
    area_discrepancy = float(selected["A_bare_native_minus_complement"].abs().max())
    if not np.isclose(area_discrepancy, 0.000647152904999948, rtol=1e-10, atol=1e-15):
        raise ValueError(f"Native/complement area discrepancy changed: {area_discrepancy}")

    # Preserve IEEE-754 round-trip precision so the two derived-area audit
    # columns can be recomputed exactly after CSV reload.
    selected.to_csv(SUBSET_CSV, index=False, float_format="%.17g")

    checks = {
        "input_sha256": source_hash,
        "selected_rows": int(len(selected)),
        "nodes_per_capacity": {str(int(q)): int(counts[q]) for q in DISPLAY_Q},
        "grid": {"x_count": int(len(x_values)), "y_count": int(len(y_values))},
        "coordinate_bounds_mm": {
            "x": [float(x_values[0] * 1e3), float(x_values[-1] * 1e3)],
            "y": [float(y_values[0] * 1e3), float(y_values[-1] * 1e3)],
        },
        "capacity_markers_mAh_cm2": {"Q_s": Q_S, "Q_f_cal": Q_F_CAL},
        "current_nonpositive_nodes": {str(k): v for k, v in nonpositive.items()},
        "current_negative_nodes": {str(k): v for k, v in negative.items()},
        "positive_current_range_A_m2": [
            float(positive_current.min()),
            float(positive_current.max()),
        ],
        "max_abs_native_A_bare_minus_1_minus_theta": area_discrepancy,
        "no_missing_or_nonfinite": True,
        "no_duplicate_capacity_coordinates": True,
    }
    return selected, checks


def matrix_at(
    frame: pd.DataFrame, q: float, field: str
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    table = (
        frame.loc[frame["Q_mAh_cm2"].eq(q)]
        .pivot(index="y_m", columns="x_m", values=field)
        .sort_index()
        .sort_index(axis=1)
    )
    return table.columns.to_numpy() * 1e3, table.index.to_numpy() * 1e3, table.to_numpy()


def style_field_axis(ax: mpl.axes.Axes, row: int, col: int) -> None:
    ax.set_xlim(3.0, 5.0)
    ax.set_ylim(0.0, 20.0)
    ax.set_xticks([3.0, 4.0, 5.0])
    ax.set_yticks([0.0, 10.0, 20.0])
    if row < 2:
        ax.set_xticklabels([])
        ax.tick_params(axis="x", length=0)
    else:
        ax.set_xticklabels(["3", "4", "5"])
    if col > 0:
        ax.set_yticklabels([])
        ax.tick_params(axis="y", length=0)
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(0.45)
        spine.set_color("#4D4D4D")
    ax.tick_params(labelsize=6.4, pad=1.4)


def add_capacity_clock(fig: mpl.figure.Figure) -> None:
    clock = fig.add_axes([0.235, 0.925, 0.70, 0.060])
    clock.set_xlim(77.0, 123.0)
    clock.set_ylim(0.0, 1.0)
    clock.set_axis_off()
    clock.annotate(
        "",
        xy=(122.5, 0.42),
        xytext=(77.5, 0.42),
        arrowprops={
            "arrowstyle": "-|>",
            "lw": 0.8,
            "color": "#6A6A6A",
            "mutation_scale": 7,
        },
    )
    clock.text(
        122.5,
        0.92,
        "capacity  $Q$  (mAh cm$^{-2}$)",
        ha="right",
        va="top",
        fontsize=6.8,
        color="#4D4D4D",
    )

    snapshot_colors = {80.0: "#315D7D", 100.0: "#B56F42", 120.0: "#5E4B8B"}
    for q in DISPLAY_Q:
        clock.plot(q, 0.42, "o", ms=4.4, color=snapshot_colors[q], mec="white", mew=0.45, zorder=4)
    clock.text(80.0, 0.12, "80", ha="center", va="top", fontsize=6.5, color=snapshot_colors[80.0])
    clock.text(
        100.0,
        0.12,
        "$Q=100\\;\\approx\\;Q_{f,\\mathrm{cal}}$",
        ha="center",
        va="top",
        fontsize=6.4,
        color=snapshot_colors[100.0],
    )
    clock.text(120.0, 0.12, "120", ha="center", va="top", fontsize=6.5, color=snapshot_colors[120.0])

    for q in (Q_S, Q_F_CAL):
        clock.plot([q, q], [0.42, 0.76], color="#272727", lw=0.7, ls=(0, (2, 1.6)))
        clock.plot(q, 0.78, marker="v", ms=3.2, color="#272727")
    clock.text(
        Q_S,
        0.84,
        "$Q_s=83.0202$",
        ha="left",
        va="bottom",
        fontsize=6.25,
        color="#272727",
    )
    clock.text(
        Q_F_CAL,
        0.84,
        "$Q_{f,\\mathrm{cal}}=99.5901$",
        ha="right",
        va="bottom",
        fontsize=6.25,
        color="#272727",
    )


def add_orientation_strip(fig: mpl.figure.Figure) -> None:
    orient = fig.add_axes([0.235, 0.866, 0.70, 0.035])
    orient.set_axis_off()
    orient.text(0.00, 0.50, "collector  x = 3 mm", ha="left", va="center", fontsize=6.6)
    orient.annotate(
        "",
        xy=(0.49, 0.50),
        xytext=(0.22, 0.50),
        xycoords="axes fraction",
        arrowprops={"arrowstyle": "-|>", "lw": 0.7, "color": "#4D4D4D", "mutation_scale": 7},
    )
    orient.text(0.52, 0.50, "separator  x = 5 mm", ha="left", va="center", fontsize=6.6)
    orient.text(0.94, 0.50, "flow y", ha="right", va="center", fontsize=6.6)
    orient.annotate(
        "",
        xy=(0.98, 0.96),
        xytext=(0.98, 0.06),
        xycoords="axes fraction",
        arrowprops={"arrowstyle": "-|>", "lw": 0.7, "color": "#4D4D4D", "mutation_scale": 7},
    )


def build_figure(frame: pd.DataFrame) -> mpl.figure.Figure:
    cmap_eps = LinearSegmentedColormap.from_list(
        "retained_solid_v2", ["#F7F7F5", "#E8C9B1", "#C98250", "#893D26", "#552319"]
    )
    cmap_bare = LinearSegmentedColormap.from_list(
        "remaining_bare_v2", ["#F7F7F5", "#C9E1DC", "#78B4AA", "#397A7E", "#173F4A"]
    )
    cmap_current = LinearSegmentedColormap.from_list(
        "current_v2", ["#F7F7F5", "#DAD9E8", "#9A94BD", "#5A548C", "#28284E"]
    )
    cmap_current.set_bad("#9E9E9E")

    fields = ("eps_s_pos", "A_bare_over_A0", "j_total_A_m2")
    norms = (
        SymLogNorm(linthresh=0.001, linscale=0.65, vmin=0.0, vmax=6.0, base=10),
        Normalize(vmin=0.0, vmax=1.0),
        LogNorm(vmin=8.0e-5, vmax=2.2e4),
    )
    cmaps = (cmap_eps, cmap_bare, cmap_current)
    row_labels = (
        "Retained solid fraction\n$\\epsilon_s$",
        "Remaining calibrated\nbare-area fraction\n$A_\\mathrm{bare}/A_0=1-\\theta_\\mathrm{cal}$",
        "Total reaction-current density\n$j_\\mathrm{total}$  (A m$^{-2}$)",
    )
    stage_titles = (
        "before mean-saturation\nmarker\n$Q=80$ mAh cm$^{-2}$",
        "near calibrated\nhalf-accessibility marker\n$Q=100$ mAh cm$^{-2}$",
        "late charge\n\n$Q=120$ mAh cm$^{-2}$",
    )

    fig = plt.figure(
        figsize=(WIDTH_MM / MM_PER_INCH, HEIGHT_MM / MM_PER_INCH), facecolor="white"
    )
    grid = fig.add_gridspec(
        3,
        4,
        left=0.235,
        right=0.945,
        bottom=0.155,
        top=0.790,
        width_ratios=[1.0, 1.0, 1.0, 0.072],
        height_ratios=[1.0, 1.0, 1.0],
        wspace=0.16,
        hspace=0.23,
    )

    axes: list[list[mpl.axes.Axes]] = [[], [], []]
    images: list[list[mpl.image.AxesImage]] = [[], [], []]
    for row, (field, cmap, norm) in enumerate(zip(fields, cmaps, norms)):
        for col, q in enumerate(DISPLAY_Q):
            ax = fig.add_subplot(grid[row, col])
            x_mm, y_mm, values = matrix_at(frame, q, field)
            if field == "eps_s_pos":
                values = values * 100.0
            elif field == "j_total_A_m2":
                values = np.ma.masked_less_equal(values, 0.0)
            image = ax.imshow(
                values,
                origin="lower",
                extent=[x_mm.min(), x_mm.max(), y_mm.min(), y_mm.max()],
                aspect="auto",
                interpolation="nearest",
                cmap=cmap,
                norm=norm,
                rasterized=True,
            )
            style_field_axis(ax, row=row, col=col)
            if row == 0:
                ax.set_title(
                    stage_titles[col],
                    fontsize=6.8,
                    fontweight="semibold",
                    pad=5.0,
                    linespacing=1.12,
                )
            axes[row].append(ax)
            images[row].append(image)

        cax = fig.add_subplot(grid[row, 3])
        colorbar = fig.colorbar(images[row][0], cax=cax)
        colorbar.outline.set_linewidth(0.45)
        colorbar.ax.tick_params(labelsize=6.1, length=2.2, width=0.55, pad=1.4)
        if row == 0:
            colorbar.set_ticks([0.0, 0.001, 0.01, 0.1, 1.0, 6.0])
            colorbar.set_ticklabels(["0", "$10^{-3}$", "$10^{-2}$", "$10^{-1}$", "1", "6"])
            colorbar.ax.set_title("%\nsymlog", fontsize=6.0, pad=2.5)
        elif row == 1:
            colorbar.set_ticks([0.0, 0.5, 1.0])
        else:
            colorbar.set_ticks([1e-4, 1e-2, 1.0, 1e2, 1e4])
            colorbar.ax.set_title("log", fontsize=6.0, pad=2.5)

    for row, text in enumerate(row_labels):
        box = axes[row][0].get_position()
        fig.text(0.133, box.y0 + box.height / 2, text, ha="center", va="center", fontsize=7.1)

    matrix_top = axes[0][0].get_position().y1
    matrix_bottom = axes[2][0].get_position().y0
    fig.text(
        0.018,
        (matrix_top + matrix_bottom) / 2,
        "Flow position  y  (mm)",
        rotation=90,
        ha="center",
        va="center",
        fontsize=7.1,
    )
    fig.text(
        (axes[2][0].get_position().x0 + axes[2][2].get_position().x1) / 2,
        matrix_bottom - 0.065,
        "Through-plane position  x  (mm)",
        ha="center",
        va="top",
        fontsize=7.1,
    )
    mask_x = 0.235
    mask_y = 0.035
    fig.add_artist(
        Rectangle(
            (mask_x, mask_y),
            0.012,
            0.014,
            transform=fig.transFigure,
            facecolor="#9E9E9E",
            edgecolor="#666666",
            linewidth=0.35,
        )
    )
    fig.text(
        mask_x + 0.018,
        mask_y + 0.007,
        "$j_\\mathrm{total}\\leq0$: 6 nodes at $Q=100$; retained as a neutral mask, not clipped or absolutized",
        ha="left",
        va="center",
        fontsize=6.25,
        color="#4D4D4D",
    )

    add_capacity_clock(fig)
    add_orientation_strip(fig)
    return fig


def export_figure(fig: mpl.figure.Figure) -> dict[str, dict]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    outputs = {
        "svg": OUT_BASE.with_suffix(".svg"),
        "pdf": OUT_BASE.with_suffix(".pdf"),
        "png": OUT_BASE.with_suffix(".png"),
        "tiff": OUT_BASE.with_suffix(".tiff"),
        "columnwidth_preview": OUT_DIR / "Fig_R582_spatial_progression_v2_columnwidth_180mm.png",
        "grayscale_qa": OUT_DIR / "Fig_R582_spatial_progression_v2_grayscale_QA.png",
    }
    fixed_timestamp = datetime(2026, 7, 20, 0, 0, 0, tzinfo=timezone.utc)
    fig.savefig(
        outputs["svg"],
        facecolor="white",
        metadata={"Date": "2026-07-20", "Creator": "R582 Python/matplotlib"},
    )
    fig.savefig(
        outputs["pdf"],
        facecolor="white",
        metadata={
            "Title": "R582 Figure 3 spatial progression v2",
            "Creator": "R582 Python/matplotlib",
            "CreationDate": fixed_timestamp,
            "ModDate": fixed_timestamp,
        },
    )
    fig.savefig(outputs["png"], dpi=300, facecolor="white")
    fig.savefig(
        outputs["tiff"],
        dpi=600,
        facecolor="white",
        pil_kwargs={"compression": "tiff_lzw"},
    )
    with Image.open(outputs["tiff"]) as tiff_image:
        tiff_image.convert("RGB").save(
            outputs["tiff"], compression="tiff_lzw", dpi=(600, 600)
        )
    fig.savefig(outputs["columnwidth_preview"], dpi=150, facecolor="white")
    plt.close(fig)

    with Image.open(outputs["columnwidth_preview"]) as preview:
        preview.convert("L").convert("RGB").save(outputs["grayscale_qa"], dpi=(150, 150))

    svg_text = outputs["svg"].read_text(encoding="utf-8")
    if "<text" not in svg_text:
        raise RuntimeError("SVG export does not contain editable text nodes.")

    metadata: dict[str, dict] = {}
    for key, path in outputs.items():
        entry = {"path": str(path), "sha256": sha256(path), "bytes": path.stat().st_size}
        if path.suffix.lower() in {".png", ".tiff"}:
            with Image.open(path) as image:
                entry["pixels"] = [int(image.width), int(image.height)]
                entry["dpi"] = [float(v) for v in image.info.get("dpi", (0.0, 0.0))]
                entry["mode"] = image.mode
        metadata[key] = entry
    metadata["svg"]["editable_text_nodes"] = svg_text.count("<text")
    return metadata


def main() -> None:
    frame, checks = validate_and_prepare()
    fig = build_figure(frame)
    outputs = export_figure(fig)
    manifest = {
        "figure": "R582 Figure 3 spatial progression v2",
        "backend": "Python/matplotlib",
        "final_size_mm": [WIDTH_MM, HEIGHT_MM],
        "source": str(INPUT_CSV),
        "checks": checks,
        "generated_source_data": {
            "subset_csv": {"path": str(SUBSET_CSV), "sha256": sha256(SUBSET_CSV)}
        },
        "outputs": outputs,
    }
    MANIFEST_JSON.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
