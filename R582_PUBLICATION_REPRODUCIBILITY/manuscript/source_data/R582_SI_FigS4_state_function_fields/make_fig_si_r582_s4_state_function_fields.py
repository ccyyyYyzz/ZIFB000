"""Build R582 Supplementary Figure S4 from the registered continuum-field export."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import font_manager
from matplotlib.colors import LinearSegmentedColormap, LogNorm, Normalize, SymLogNorm, TwoSlopeNorm
from matplotlib.patches import Rectangle
from PIL import Image


SOURCE_DATA_DIR = Path(__file__).resolve().parent.parent
if str(SOURCE_DATA_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DATA_DIR))
from r582_font_runtime import FONT_FILENAMES, locate_tex_tool, register_termes_fonts


SCRIPT_DIR = Path(__file__).resolve().parent
MANUSCRIPT_DIR = SCRIPT_DIR.parents[1]
WORKSPACE_ROOT = MANUSCRIPT_DIR.parent
INPUT_CSV = SCRIPT_DIR.parent / "Fig_R545_fields" / "Fig3_baseline_spatial_long.csv"
OUT_DIR = MANUSCRIPT_DIR / "figures_R582"
OUT_STEM = "Fig_SI_R582_S4_state_function_fields"
SOURCE_CSV = SCRIPT_DIR / f"{OUT_STEM}_source.csv"
INPUT_MANIFEST = SCRIPT_DIR / "R582_SI_FigS4_input_manifest.csv"
RENDER_MANIFEST = SCRIPT_DIR / "render_manifest.json"
PDFFONTS_REPORT = SCRIPT_DIR / "pdffonts_report.txt"
TEMP_DIR = SCRIPT_DIR / ".determinism_tmp"

EXPECTED_INPUT_SHA256 = "E322D0D0C4B0D5C8CB84BD5CB18D1A43CBA183EB8A5F112577686993BC8FC007"
DISPLAY_Q = (0.0, 80.0, 96.0, 100.0, 110.0, 120.0)
EXPECTED_NODES = 5_995
WIDTH_MM = 180.0
HEIGHT_MM = 142.0
MM_PER_INCH = 25.4
FIXED_DATE = datetime(2026, 7, 20, 0, 0, 0, tzinfo=timezone.utc)

TERMES_DIR, _TERMES_BY_ROLE, FONT_FAMILY = register_termes_fonts(font_manager)
TERMES_FILES = tuple(FONT_FILENAMES.values())
PDFFONTS = locate_tex_tool("pdffonts", TERMES_DIR)

REQUIRED_COLUMNS = (
    "time_label",
    "time_s",
    "Q_mAh_cm2",
    "x_m",
    "y_m",
    "S_surf",
    "eps_s_pos",
    "theta_eff",
    "A_bare_frac",
    "j_total_A_m2",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def workspace_path(path: Path) -> str:
    return path.resolve().relative_to(WORKSPACE_ROOT.resolve()).as_posix()


def configure_fonts() -> None:
    mpl.rcParams.update(
        {
            "font.family": FONT_FAMILY,
            "font.size": 7.2,
            "axes.labelsize": 7.0,
            "axes.titlesize": 6.8,
            "axes.linewidth": 0.55,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "xtick.labelsize": 6.5,
            "ytick.labelsize": 6.5,
            "xtick.major.width": 0.55,
            "ytick.major.width": 0.55,
            "xtick.major.size": 2.3,
            "ytick.major.size": 2.3,
            "legend.frameon": False,
            "mathtext.fontset": "custom",
            "mathtext.rm": FONT_FAMILY,
            "mathtext.it": f"{FONT_FAMILY}:italic",
            "mathtext.bf": f"{FONT_FAMILY}:bold",
            "mathtext.sf": FONT_FAMILY,
            "mathtext.fallback": None,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
            "svg.hashsalt": "R582-SI-FigS4-state-function-fields-termes",
            "figure.facecolor": "white",
            "savefig.facecolor": "white",
            "savefig.bbox": None,
            "savefig.pad_inches": 0.0,
        }
    )


def validate_and_freeze_source() -> tuple[pd.DataFrame, dict]:
    observed_hash = sha256(INPUT_CSV)
    if observed_hash != EXPECTED_INPUT_SHA256:
        raise RuntimeError(
            f"Registered input changed: expected {EXPECTED_INPUT_SHA256}, observed {observed_hash}."
        )

    source = pd.read_csv(INPUT_CSV, float_precision="round_trip")
    missing = sorted(set(REQUIRED_COLUMNS).difference(source.columns))
    if missing:
        raise ValueError(f"Missing required fields: {missing}")

    observed_q = tuple(sorted(source["Q_mAh_cm2"].unique().astype(float)))
    if observed_q != DISPLAY_Q:
        raise ValueError(f"Unexpected capacity inventory: {observed_q}")

    selected = source.loc[:, REQUIRED_COLUMNS].copy()
    selected = selected.sort_values(["Q_mAh_cm2", "y_m", "x_m"]).reset_index(drop=True)
    counts = selected.groupby("Q_mAh_cm2", sort=True).size().to_dict()
    expected_counts = {q: EXPECTED_NODES for q in DISPLAY_Q}
    if counts != expected_counts:
        raise ValueError(f"Unexpected node inventory: {counts}")
    if selected.duplicated(["Q_mAh_cm2", "x_m", "y_m"]).any():
        raise ValueError("Duplicate capacity-coordinate rows detected.")
    numeric = selected.select_dtypes(include=[np.number])
    if not np.isfinite(numeric.to_numpy()).all():
        raise ValueError("Missing or non-finite values detected.")

    x_values = np.sort(selected["x_m"].unique())
    y_values = np.sort(selected["y_m"].unique())
    if len(x_values) != 55 or len(y_values) != 109:
        raise ValueError(f"Expected 55 x 109 grid, observed {len(x_values)} x {len(y_values)}.")
    if not np.array_equal(x_values[[0, -1]], np.array([0.003, 0.005])):
        raise ValueError("Unexpected through-plane coordinate bounds.")
    if not np.array_equal(y_values[[0, -1]], np.array([0.0, 0.020])):
        raise ValueError("Unexpected flow-coordinate bounds.")

    nonpositive_counts: dict[str, int] = {}
    negative_ranges: dict[str, list[float] | None] = {}
    for q in DISPLAY_Q:
        values = selected.loc[selected["Q_mAh_cm2"].eq(q), "j_total_A_m2"]
        nonpositive = values.loc[values.le(0.0)]
        nonpositive_counts[str(int(q))] = int(len(nonpositive))
        negative_ranges[str(int(q))] = (
            [float(nonpositive.min()), float(nonpositive.max())]
            if len(nonpositive)
            else None
        )
    expected_nonpositive = {"0": 248, "80": 0, "96": 33, "100": 6, "110": 0, "120": 0}
    if nonpositive_counts != expected_nonpositive:
        raise ValueError(f"Signed-current inventory changed: {nonpositive_counts}")

    selected.to_csv(SOURCE_CSV, index=False, float_format="%.17g", lineterminator="\n")
    reloaded = pd.read_csv(SOURCE_CSV, float_precision="round_trip")
    pd.testing.assert_frame_equal(selected, reloaded, check_exact=True, check_dtype=False)

    manifest_rows = pd.DataFrame(
        [
            {
                "role": "immutable_registered_upstream_export",
                "workspace_relative_path": workspace_path(INPUT_CSV),
                "sha256": observed_hash,
                "bytes": INPUT_CSV.stat().st_size,
                "status": "read_only; byte identity required before rendering",
            },
            {
                "role": "frozen_plotted_source_table",
                "workspace_relative_path": workspace_path(SOURCE_CSV),
                "sha256": sha256(SOURCE_CSV),
                "bytes": SOURCE_CSV.stat().st_size,
                "status": "derived column subset; IEEE-754 round-trip verified",
            },
        ]
    )
    manifest_rows.to_csv(INPUT_MANIFEST, index=False, lineterminator="\n")

    positive_current = selected.loc[selected["j_total_A_m2"].gt(0.0), "j_total_A_m2"]
    return selected, {
        "upstream_sha256": observed_hash,
        "frozen_source_sha256": sha256(SOURCE_CSV),
        "rows": int(len(selected)),
        "nodes_per_capacity": {str(int(q)): int(counts[q]) for q in DISPLAY_Q},
        "grid": {"x_count": 55, "y_count": 109},
        "coordinate_bounds_mm": {"x": [3.0, 5.0], "y": [0.0, 20.0]},
        "nonpositive_current_counts": nonpositive_counts,
        "nonpositive_current_ranges_A_m2": negative_ranges,
        "positive_current_range_A_m2": [
            float(positive_current.min()),
            float(positive_current.max()),
        ],
        "native_A_bare_range": [
            float(selected["A_bare_frac"].min()),
            float(selected["A_bare_frac"].max()),
        ],
        "round_trip_source_check": True,
        "no_missing_nonfinite_or_duplicate_nodes": True,
    }


def field_matrix(frame: pd.DataFrame, q: float, field: str) -> np.ndarray:
    table = (
        frame.loc[frame["Q_mAh_cm2"].eq(q)]
        .pivot(index="y_m", columns="x_m", values=field)
        .sort_index()
        .sort_index(axis=1)
    )
    if table.shape != (109, 55):
        raise ValueError(f"Unexpected {field} matrix at Q={q}: {table.shape}")
    return table.to_numpy()


def style_map_axis(ax: mpl.axes.Axes, row: int, col: int) -> None:
    ax.set_xlim(3.0, 5.0)
    ax.set_ylim(0.0, 20.0)
    ax.set_xticks([3.0, 4.0, 5.0])
    ax.set_yticks([0.0, 10.0, 20.0])
    if row < 3:
        ax.set_xticklabels([])
        ax.tick_params(axis="x", length=0)
    if col > 0:
        ax.set_yticklabels([])
        ax.tick_params(axis="y", length=0)
    ax.tick_params(labelsize=6.5, pad=1.1)
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(0.45)
        spine.set_color("#5A5A5A")


def build_figure(frame: pd.DataFrame) -> mpl.figure.Figure:
    cmap_stress = LinearSegmentedColormap.from_list(
        "s4_stress", ["#315D7D", "#A9C6D4", "#F7F7F5", "#EBC7A8", "#B56F42"]
    )
    cmap_solid = LinearSegmentedColormap.from_list(
        "s4_solid", ["#F7F7F5", "#EDD9BC", "#D8912B", "#7E4817"]
    )
    cmap_bare = LinearSegmentedColormap.from_list(
        "s4_bare", ["#F7F7F5", "#C9E1DC", "#78B4AA", "#397A7E", "#173F4A"]
    )
    cmap_current = LinearSegmentedColormap.from_list(
        "s4_current", ["#F7F7F5", "#DAD9E8", "#9A94BD", "#5A548C", "#28284E"]
    )
    cmap_current.set_bad("#9E9E9E")

    positive_current = frame.loc[frame["j_total_A_m2"].gt(0.0), "j_total_A_m2"]
    rows = (
        {
            "field": "S_surf",
            "label": "Free-I$_2$ stress\n$S$",
            "cmap": cmap_stress,
            "norm": TwoSlopeNorm(vmin=0.18, vcenter=1.0, vmax=1.80),
            "transform": lambda x: x,
            "ticks": [0.2, 0.6, 1.0, 1.4, 1.8],
            "ticklabels": ["0.2", "0.6", "1.0", "1.4", "1.8"],
            "scale_note": "$S=1$",
        },
        {
            "field": "eps_s_pos",
            "label": "Retained-solid fraction\n$\\epsilon_s$ (%)",
            "cmap": cmap_solid,
            "norm": SymLogNorm(linthresh=0.001, linscale=0.70, vmin=0.0, vmax=6.0, base=10),
            "transform": lambda x: x * 100.0,
            "ticks": [0.0, 0.001, 0.01, 0.1, 1.0, 6.0],
            "ticklabels": ["0", "$10^{-3}$", "$10^{-2}$", "$10^{-1}$", "1", "6"],
            "scale_note": "symlog",
        },
        {
            "field": "A_bare_frac",
            "label": "Remaining bare area\n$A_\\mathrm{bare}/A_0$",
            "cmap": cmap_bare,
            "norm": Normalize(vmin=0.0, vmax=1.0),
            "transform": lambda x: x,
            "ticks": [0.0, 0.25, 0.5, 0.75, 1.0],
            "ticklabels": ["0", "0.25", "0.5", "0.75", "1"],
            "scale_note": "native field",
        },
        {
            "field": "j_total_A_m2",
            "label": "Total reaction current\n$j_\\mathrm{total}$ (A m$^{-2}$)",
            "cmap": cmap_current,
            "norm": LogNorm(vmin=float(positive_current.min()), vmax=2.20e4),
            "transform": lambda x: np.ma.masked_less_equal(x, 0.0),
            "ticks": [1e-8, 1e-4, 1.0, 1e4],
            "ticklabels": ["$10^{-8}$", "$10^{-4}$", "$10^{0}$", "$10^{4}$"],
            "scale_note": "positive: log",
        },
    )

    fig = plt.figure(
        figsize=(WIDTH_MM / MM_PER_INCH, HEIGHT_MM / MM_PER_INCH),
        facecolor="white",
    )
    grid = fig.add_gridspec(
        4,
        7,
        left=0.185,
        right=0.952,
        bottom=0.135,
        top=0.835,
        width_ratios=[1, 1, 1, 1, 1, 1, 0.075],
        height_ratios=[1, 1, 1, 1],
        wspace=0.13,
        hspace=0.20,
    )

    axes: list[list[mpl.axes.Axes]] = [[] for _ in rows]
    for row_index, spec in enumerate(rows):
        image = None
        for column_index, q in enumerate(DISPLAY_Q):
            ax = fig.add_subplot(grid[row_index, column_index])
            matrix = field_matrix(frame, q, spec["field"])
            matrix = spec["transform"](matrix)
            image = ax.imshow(
                matrix,
                origin="lower",
                extent=[3.0, 5.0, 0.0, 20.0],
                aspect="auto",
                interpolation="nearest",
                cmap=spec["cmap"],
                norm=spec["norm"],
                rasterized=True,
            )
            style_map_axis(ax, row=row_index, col=column_index)
            if row_index == 0:
                ax.set_title(f"{int(q)}", fontsize=6.8, fontweight="semibold", pad=3.0)
            axes[row_index].append(ax)

        if image is None:
            raise RuntimeError("No field image was created.")
        cax = fig.add_subplot(grid[row_index, 6])
        colorbar = fig.colorbar(image, cax=cax)
        colorbar.set_ticks(spec["ticks"])
        colorbar.set_ticklabels(spec["ticklabels"])
        colorbar.outline.set_linewidth(0.45)
        colorbar.ax.tick_params(labelsize=6.5, length=2.0, width=0.5, pad=1.2)

    for row_index, (spec, row_axes) in enumerate(zip(rows, axes)):
        position = row_axes[0].get_position()
        fig.text(
            0.013,
            position.y1 + 0.004,
            chr(ord("a") + row_index),
            fontsize=8.0,
            fontweight="bold",
            ha="left",
            va="top",
        )
        fig.text(
            0.090,
            position.y0 + position.height / 2,
            spec["label"],
            fontsize=7.0,
            ha="center",
            va="center",
            linespacing=1.10,
        )

    fig.text(
        0.565,
        0.965,
        "Areal capacity  $Q$  (mAh cm$^{-2}$)",
        fontsize=7.2,
        fontweight="semibold",
        ha="center",
        va="top",
    )
    fig.text(
        0.565,
        0.902,
        "$x$: collector (3 mm) to separator (5 mm);   flow coordinate $y$: 0 to 20 mm",
        fontsize=6.5,
        color="#4D4D4D",
        ha="center",
        va="center",
    )
    fig.text(
        0.565,
        0.077,
        "Through-plane position  $x$  (mm)",
        fontsize=7.0,
        ha="center",
        va="center",
    )
    fig.add_artist(
        Rectangle(
            (0.187, 0.024),
            0.012,
            0.013,
            transform=fig.transFigure,
            facecolor="#9E9E9E",
            edgecolor="#666666",
            linewidth=0.35,
        )
    )
    fig.text(
        0.205,
        0.0305,
        "$j_\\mathrm{total}\\leq0$: neutral mask; node counts by $Q$ = 248, 0, 33, 6, 0, 0; signed values retained in source",
        fontsize=6.5,
        color="#4D4D4D",
        ha="left",
        va="center",
    )
    return fig


def render_bundle(output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "svg": output_dir / f"{OUT_STEM}.svg",
        "pdf": output_dir / f"{OUT_STEM}.pdf",
        "png_600dpi": output_dir / f"{OUT_STEM}.png",
        "tiff_600dpi": output_dir / f"{OUT_STEM}.tiff",
        "preview_180mm": output_dir / f"{OUT_STEM}_180mm_preview.png",
        "grayscale_180mm": output_dir / f"{OUT_STEM}_grayscale_180mm.png",
    }
    fig = build_figure(FRAME_FOR_RENDER)
    fig.savefig(
        paths["svg"],
        dpi=600,
        facecolor="white",
        bbox_inches=None,
        metadata={"Date": "2026-07-20", "Creator": "R582 Python/matplotlib"},
    )
    fig.savefig(
        paths["pdf"],
        dpi=600,
        facecolor="white",
        bbox_inches=None,
        metadata={
            "Title": "R582 Supplementary Figure S4 state and function fields",
            "Creator": "R582 Python/matplotlib",
            "CreationDate": FIXED_DATE,
            "ModDate": FIXED_DATE,
        },
    )
    fig.savefig(
        paths["png_600dpi"],
        dpi=600,
        facecolor="white",
        bbox_inches=None,
        pil_kwargs={"compress_level": 9},
    )
    fig.savefig(
        paths["tiff_600dpi"],
        dpi=600,
        facecolor="white",
        bbox_inches=None,
        pil_kwargs={"compression": "tiff_lzw"},
    )
    fig.savefig(
        paths["preview_180mm"],
        dpi=150,
        facecolor="white",
        bbox_inches=None,
        pil_kwargs={"compress_level": 9},
    )
    plt.close(fig)

    with Image.open(paths["png_600dpi"]) as image:
        image.convert("RGB").save(
            paths["png_600dpi"], dpi=(600, 600), compress_level=9
        )
    with Image.open(paths["tiff_600dpi"]) as image:
        image.convert("RGB").save(
            paths["tiff_600dpi"], dpi=(600, 600), compression="tiff_lzw"
        )
    with Image.open(paths["preview_180mm"]) as image:
        rgb = image.convert("RGB")
        rgb.save(paths["preview_180mm"], dpi=(150, 150), compress_level=9)
        rgb.convert("L").convert("RGB").save(
            paths["grayscale_180mm"], dpi=(150, 150), compress_level=9
        )
    return paths


def inspect_outputs(paths: dict[str, Path]) -> tuple[dict, str]:
    svg_text = paths["svg"].read_text(encoding="utf-8")
    if "<text" not in svg_text:
        raise RuntimeError("SVG lacks editable text nodes.")
    forbidden_svg = [
        name
        for name in ("Arial", "Helvetica", "DejaVu", "Liberation", "Calibri", "Times New Roman")
        if name.lower() in svg_text.lower()
    ]
    if forbidden_svg:
        raise RuntimeError(f"Forbidden SVG font family found: {forbidden_svg}")
    if "TeX Gyre Termes" not in svg_text:
        raise RuntimeError("SVG does not declare TeX Gyre Termes.")

    if not PDFFONTS.is_file():
        raise FileNotFoundError(PDFFONTS)
    completed = subprocess.run(
        [str(PDFFONTS), str(paths["pdf"])],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    report = completed.stdout
    forbidden_pdf = [
        name
        for name in ("Arial", "Helvetica", "DejaVu", "Liberation", "Calibri", "Times", "STIX", "ComputerModern")
        if name.lower() in report.lower()
    ]
    if forbidden_pdf or "Type 3" in report or "TeXGyreTermes" not in report:
        raise RuntimeError(
            f"PDF font gate failed; forbidden={forbidden_pdf}, Type3={'Type 3' in report}.\n{report}"
        )
    PDFFONTS_REPORT.write_text(report, encoding="utf-8", newline="\n")

    records: dict[str, dict] = {}
    for key, path in paths.items():
        record: dict[str, object] = {
            "workspace_relative_path": workspace_path(path),
            "sha256": sha256(path),
            "bytes": path.stat().st_size,
        }
        if path.suffix.lower() in {".png", ".tiff"}:
            with Image.open(path) as image:
                record.update(
                    {
                        "pixels": [int(image.width), int(image.height)],
                        "dpi": [float(v) for v in image.info.get("dpi", (0.0, 0.0))],
                        "mode": image.mode,
                    }
                )
        records[key] = record
    records["svg"]["editable_text_nodes"] = svg_text.count("<text")
    return records, report


def check_determinism(official: dict[str, Path]) -> dict[str, bool]:
    if TEMP_DIR.exists():
        shutil.rmtree(TEMP_DIR)
    comparison = render_bundle(TEMP_DIR)
    result = {key: sha256(official[key]) == sha256(comparison[key]) for key in official}
    shutil.rmtree(TEMP_DIR)
    if not all(result.values()):
        raise RuntimeError(f"Byte-level determinism failed: {result}")
    return result


FRAME_FOR_RENDER: pd.DataFrame


def main() -> None:
    global FRAME_FOR_RENDER
    configure_fonts()
    FRAME_FOR_RENDER, checks = validate_and_freeze_source()
    official = render_bundle(OUT_DIR)
    determinism = check_determinism(official)
    outputs, _ = inspect_outputs(official)
    manifest = {
        "figure": "R582 Supplementary Figure S4 state and function fields",
        "backend": "Python/matplotlib only",
        "fixed_build_date": "2026-07-20T00:00:00Z",
        "final_size_mm": [WIDTH_MM, HEIGHT_MM],
        "font_contract": {
            "family": "TeX Gyre Termes",
            "registered_otf_files": list(TERMES_FILES),
            "base_size_pt": 7.2,
            "minimum_size_pt": 6.5,
            "panel_label_size_pt": 8.0,
            "pdf_fonttype": 42,
            "svg_fonttype": "none",
        },
        "input": {
            "workspace_relative_path": workspace_path(INPUT_CSV),
            "sha256": EXPECTED_INPUT_SHA256,
            "immutable": True,
        },
        "source_bundle": {
            "script": {
                "workspace_relative_path": workspace_path(Path(__file__)),
                "sha256": sha256(Path(__file__)),
            },
            "frozen_source_csv": {
                "workspace_relative_path": workspace_path(SOURCE_CSV),
                "sha256": sha256(SOURCE_CSV),
            },
            "input_manifest": {
                "workspace_relative_path": workspace_path(INPUT_MANIFEST),
                "sha256": sha256(INPUT_MANIFEST),
            },
            "pdffonts_report": {
                "workspace_relative_path": workspace_path(PDFFONTS_REPORT),
                "sha256": sha256(PDFFONTS_REPORT),
            },
        },
        "checks": checks,
        "render_semantics": {
            "capacities_mAh_cm2": list(DISPLAY_Q),
            "interpolation": "nearest; no smoothing",
            "native_remaining_area": "A_bare_frac",
            "current_nonpositive_handling": "neutral mask; signed values retained in source",
            "electrical_potential_fields_used": False,
            "morphology_or_coverage_inference": False,
        },
        "deterministic_second_render_byte_identical": determinism,
        "outputs": outputs,
    }
    RENDER_MANIFEST.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(manifest, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
