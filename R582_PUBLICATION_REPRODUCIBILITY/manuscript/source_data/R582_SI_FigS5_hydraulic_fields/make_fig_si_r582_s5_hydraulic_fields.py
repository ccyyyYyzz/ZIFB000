"""Build R582 Supplementary Figure S5 from the registered hydraulic-field export."""

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
from matplotlib.colors import LinearSegmentedColormap, Normalize
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
OUT_STEM = "Fig_SI_R582_S5_hydraulic_fields"
SOURCE_CSV = SCRIPT_DIR / f"{OUT_STEM}_source.csv"
INPUT_MANIFEST = SCRIPT_DIR / "R582_SI_FigS5_input_manifest.csv"
RENDER_MANIFEST = SCRIPT_DIR / "render_manifest.json"
PDFFONTS_REPORT = SCRIPT_DIR / "pdffonts_report.txt"
TEMP_DIR = SCRIPT_DIR / ".determinism_tmp"

EXPECTED_INPUT_SHA256 = "E322D0D0C4B0D5C8CB84BD5CB18D1A43CBA183EB8A5F112577686993BC8FC007"
DISPLAY_Q = (0.0, 80.0, 96.0, 100.0, 110.0, 120.0)
EXPECTED_NODES = 5_995
WIDTH_MM = 180.0
HEIGHT_MM = 112.0
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
    "K_perm_rel",
    "u_native_mag_m_s",
    "p_native_Pa",
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
            "svg.hashsalt": "R582-SI-FigS5-hydraulic-fields-termes",
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
    if selected["K_perm_rel"].min() <= 0.0 or selected["K_perm_rel"].max() > 1.0:
        raise ValueError("Relative permeability falls outside its declared positive range.")
    if selected["u_native_mag_m_s"].min() < 0.0:
        raise ValueError("Velocity magnitude cannot be negative.")
    if selected["p_native_Pa"].min() != 0.0:
        raise ValueError("Registered pressure export no longer contains the p_out = 0 reference.")
    outlet_counts = {
        str(int(q)): int(
            selected.loc[selected["Q_mAh_cm2"].eq(q), "p_native_Pa"].eq(0.0).sum()
        )
        for q in DISPLAY_Q
    }
    if outlet_counts != {str(int(q)): 55 for q in DISPLAY_Q}:
        raise ValueError(f"Unexpected p_out=0 node inventory: {outlet_counts}")

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

    ranges = {
        field: [float(selected[field].min()), float(selected[field].max())]
        for field in ("K_perm_rel", "u_native_mag_m_s", "p_native_Pa")
    }
    capacity_ranges = {
        str(int(q)): {
            field: [
                float(selected.loc[selected["Q_mAh_cm2"].eq(q), field].min()),
                float(selected.loc[selected["Q_mAh_cm2"].eq(q), field].max()),
            ]
            for field in ("K_perm_rel", "u_native_mag_m_s", "p_native_Pa")
        }
        for q in DISPLAY_Q
    }
    return selected, {
        "upstream_sha256": observed_hash,
        "frozen_source_sha256": sha256(SOURCE_CSV),
        "rows": int(len(selected)),
        "nodes_per_capacity": {str(int(q)): int(counts[q]) for q in DISPLAY_Q},
        "grid": {"x_count": 55, "y_count": 109},
        "coordinate_bounds_mm": {"x": [3.0, 5.0], "y": [0.0, 20.0]},
        "global_field_ranges": ranges,
        "capacity_field_ranges": capacity_ranges,
        "p_out_zero_nodes_per_capacity": outlet_counts,
        "pressure_semantics": "hydraulic pressure in Pa; registered p_out = 0",
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
    if row < 2:
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
    cmap_perm = LinearSegmentedColormap.from_list(
        "s5_permeability", ["#F7F7F5", "#DAD9E8", "#9A94BD", "#5E4B8B"]
    )
    cmap_velocity = LinearSegmentedColormap.from_list(
        "s5_velocity", ["#F7F7F5", "#C8DCE7", "#6F9EBB", "#315D7D"]
    )
    cmap_pressure = LinearSegmentedColormap.from_list(
        "s5_pressure", ["#F7F7F5", "#D2DBD7", "#879C95", "#3F5852"]
    )

    rows = (
        {
            "field": "K_perm_rel",
            "label": "Smooth relative permeability\n$K/K_0$",
            "cmap": cmap_perm,
            "norm": Normalize(vmin=0.40, vmax=1.00),
            "ticks": [0.4, 0.6, 0.8, 1.0],
            "ticklabels": ["0.4", "0.6", "0.8", "1.0"],
        },
        {
            "field": "u_native_mag_m_s",
            "label": "Velocity magnitude\n$|u|$ (m s$^{-1}$)",
            "cmap": cmap_velocity,
            "norm": Normalize(vmin=0.008, vmax=0.022),
            "ticks": [0.008, 0.012, 0.016, 0.020],
            "ticklabels": ["0.008", "0.012", "0.016", "0.020"],
        },
        {
            "field": "p_native_Pa",
            "label": "Hydraulic pressure\n$p$ (Pa; $p_\\mathrm{out}=0$)",
            "cmap": cmap_pressure,
            "norm": Normalize(vmin=0.0, vmax=10_000.0),
            "ticks": [0.0, 2500.0, 5000.0, 7500.0, 10_000.0],
            "ticklabels": ["0", "2500", "5000", "7500", "10000"],
        },
    )

    fig = plt.figure(
        figsize=(WIDTH_MM / MM_PER_INCH, HEIGHT_MM / MM_PER_INCH),
        facecolor="white",
    )
    grid = fig.add_gridspec(
        3,
        7,
        left=0.185,
        right=0.952,
        bottom=0.155,
        top=0.805,
        width_ratios=[1, 1, 1, 1, 1, 1, 0.075],
        height_ratios=[1, 1, 1],
        wspace=0.13,
        hspace=0.22,
    )

    axes: list[list[mpl.axes.Axes]] = [[] for _ in rows]
    for row_index, spec in enumerate(rows):
        image = None
        for column_index, q in enumerate(DISPLAY_Q):
            ax = fig.add_subplot(grid[row_index, column_index])
            matrix = field_matrix(frame, q, spec["field"])
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
            raise RuntimeError("No hydraulic-field image was created.")
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
        0.963,
        "Areal capacity  $Q$  (mAh cm$^{-2}$)",
        fontsize=7.2,
        fontweight="semibold",
        ha="center",
        va="top",
    )
    fig.text(
        0.565,
        0.887,
        "$x$: collector (3 mm) to separator (5 mm);   flow coordinate $y$: 0 to 20 mm",
        fontsize=6.5,
        color="#4D4D4D",
        ha="center",
        va="center",
    )
    fig.text(
        0.565,
        0.074,
        "Through-plane position  $x$  (mm)",
        fontsize=7.0,
        ha="center",
        va="center",
    )
    fig.text(
        0.565,
        0.026,
        "Pressure is hydraulic (Pa) with the registered outlet reference $p_\\mathrm{out}=0$; no electrical-potential field is shown.",
        fontsize=6.5,
        color="#4D4D4D",
        ha="center",
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
            "Title": "R582 Supplementary Figure S5 hydraulic fields",
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
        "figure": "R582 Supplementary Figure S5 hydraulic fields",
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
            "pressure_field": "p_native_Pa; hydraulic pressure in Pa; p_out = 0",
            "electrical_potential_fields_used": False,
            "local_pore_closure_or_blockage_inference": False,
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
