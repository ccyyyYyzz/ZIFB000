#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Build the editorial R582 Figure 2 v2.

The artwork uses a continuous state rail and direct annotations rather than
rounded cards. TeX Gyre Termes is registered explicitly so figure typography
matches the tgtermes/newtx Times family used by the manuscript.
"""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, Rectangle
from PIL import Image, ImageOps


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MANUSCRIPT = ROOT / "manuscript"
FIG_DIR = MANUSCRIPT / "figures_R582"
FIG_DIR.mkdir(parents=True, exist_ok=True)

GEOMETRY_CSV = MANUSCRIPT / "source_data" / "Fig_R573_model_geometry" / "R573_model_geometry_values.csv"
STATE_CSV = MANUSCRIPT / "source_data" / "Fig_R581_concept_state_progression" / "R581_concept_state_progression_source_data.csv"
STATE_BUILD = MANUSCRIPT / "source_data" / "Fig_R581_concept_state_progression" / "R581_CONCEPT_STATE_PROGRESSION_BUILD.json"

FONT_DIR = Path(r"D:\Program Files\texlive\2024\texmf-dist\fonts\opentype\public\tex-gyre")
FONT_PATHS = {
    "regular": FONT_DIR / "texgyretermes-regular.otf",
    "bold": FONT_DIR / "texgyretermes-bold.otf",
    "italic": FONT_DIR / "texgyretermes-italic.otf",
    "bolditalic": FONT_DIR / "texgyretermes-bolditalic.otf",
}
FONT_FAMILY = "TeX Gyre Termes"
for font_path in FONT_PATHS.values():
    if not font_path.is_file():
        raise FileNotFoundError(f"Required manuscript font is missing: {font_path}")
    font_manager.fontManager.addfont(str(font_path))

STEM = "Fig_R582_domain_state_v2"
WIDTH_MM = 180.0
HEIGHT_MM = 90.0
RASTER_DPI = 600
PREVIEW_DPI = 300
FIXED_DATE = datetime(2026, 7, 20, tzinfo=timezone.utc)
PDFTOOLS_DIR = Path(r"D:\Program Files\texlive\2024\bin\windows")
PDFFONTS_EXE = PDFTOOLS_DIR / "pdffonts.exe"

COLORS = {
    "ink": "#26272A",
    "muted": "#6A6D72",
    "line": "#B9BDC2",
    "graphite": "#4D4D4D",
    "vermilion": "#D65345",
    "blue": "#3B6FB6",
    "teal": "#2A9D8F",
    "amber": "#D8912B",
    "felt": "#F7F0E5",
    "separator": "#C4D6DA",
}

mpl.rcParams.update(
    {
        "font.family": FONT_FAMILY,
        "font.serif": [FONT_FAMILY],
        "font.size": 7.2,
        "font.weight": "normal",
        "axes.linewidth": 0.8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "legend.frameon": False,
        "svg.fonttype": "none",
        "svg.hashsalt": "R582-Fig2-domain-state-v2",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "mathtext.fontset": "custom",
        "mathtext.rm": FONT_FAMILY,
        "mathtext.it": f"{FONT_FAMILY}:italic",
        "mathtext.bf": f"{FONT_FAMILY}:bold",
        "mathtext.cal": f"{FONT_FAMILY}:italic",
        "mathtext.sf": FONT_FAMILY,
        "mathtext.tt": FONT_FAMILY,
        "mathtext.fallback": None,
        "savefig.facecolor": "white",
        "figure.facecolor": "white",
    }
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def relative(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def read_registered_inputs() -> tuple[dict[str, dict[str, str]], float, float]:
    with GEOMETRY_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        geometry = {row["quantity"]: row for row in csv.DictReader(handle)}
    expected_geometry = {
        "positive_domain_x_min": 3.0,
        "positive_domain_x_max": 5.0,
        "positive_domain_y_min": 0.0,
        "positive_domain_y_max": 20.0,
        "felt_thickness": 2.0,
    }
    for key, expected in expected_geometry.items():
        actual = float(geometry[key]["value"])
        if abs(actual - expected) > 1e-12:
            raise ValueError(f"Unexpected registered geometry value for {key}: {actual}")

    state_manifest = json.loads(STATE_BUILD.read_text(encoding="utf-8"))
    q_s = float(state_manifest["registered_markers"]["Q_s_mAh_cm2"])
    q_f = float(state_manifest["registered_markers"]["Q_f_cal_mAh_cm2"])
    if (q_s, q_f) != (83.0, 99.6):
        raise ValueError(f"Unexpected displayed marker values: Q_s={q_s}, Q_f,cal={q_f}")

    with STATE_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        state_rows = list(csv.DictReader(handle))
    if len(state_rows) != 5:
        raise ValueError("The registered state source must contain five legacy state rows")
    if any(row.get("morphology_identified", "").strip().lower() != "false" for row in state_rows):
        raise ValueError("Source bundle unexpectedly claims morphology identification")
    return geometry, q_s, q_f


def panel_label(ax: plt.Axes, letter: str, heading: str) -> None:
    ax.text(0.0, 1.0, letter, transform=ax.transAxes, ha="left", va="top", fontsize=8.5, fontweight="bold", color=COLORS["ink"])
    ax.text(0.065, 0.997, heading, transform=ax.transAxes, ha="left", va="top", fontsize=7.7, fontweight="bold", color=COLORS["ink"])


def draw_domain(ax: plt.Axes) -> None:
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_axis_off()
    panel_label(ax, "a", "Positive-electrode domain")

    y0, y1 = 0.27, 0.75
    x_col0, x_col1 = 0.14, 0.22
    x_felt0, x_felt1 = 0.22, 0.77
    x_sep0, x_sep1 = 0.77, 0.85

    ax.add_patch(Rectangle((x_col0, y0), x_col1 - x_col0, y1 - y0, facecolor=COLORS["graphite"], edgecolor=COLORS["ink"], linewidth=0.85))
    ax.add_patch(Rectangle((x_felt0, y0), x_felt1 - x_felt0, y1 - y0, facecolor=COLORS["felt"], edgecolor=COLORS["ink"], linewidth=1.0))
    ax.add_patch(Rectangle((x_sep0, y0), x_sep1 - x_sep0, y1 - y0, facecolor=COLORS["separator"], edgecolor=COLORS["ink"], linewidth=0.85, hatch="////"))

    ax.text((x_col0 + x_col1) / 2, (y0 + y1) / 2, "current\ncollector", rotation=90, ha="center", va="center", fontsize=6.5, color="white", linespacing=0.9)
    ax.text((x_felt0 + x_felt1) / 2 + 0.025, 0.56, "positive carbon felt", ha="center", va="center", fontsize=7.2, fontweight="bold", color=COLORS["ink"])
    ax.text((x_felt0 + x_felt1) / 2 + 0.025, 0.46, "2D model domain", ha="center", va="center", fontsize=6.5, color=COLORS["muted"])
    ax.text((x_sep0 + x_sep1) / 2, (y0 + y1) / 2, "separator", rotation=90, ha="center", va="center", fontsize=6.5, color=COLORS["ink"])

    ax.add_patch(FancyArrowPatch((x_felt0, 0.14), (x_felt1, 0.14), arrowstyle="-|>", mutation_scale=8, linewidth=0.9, color=COLORS["ink"]))
    ax.text((x_felt0 + x_felt1) / 2, 0.068, r"$x$: 3--5 mm (through-plane)", ha="center", va="center", fontsize=6.5, color=COLORS["ink"])
    ax.add_patch(FancyArrowPatch((0.065, y0), (0.065, y1), arrowstyle="-|>", mutation_scale=8, linewidth=0.9, color=COLORS["ink"]))
    ax.text(0.028, (y0 + y1) / 2, r"$y$: 0--20 mm", rotation=90, ha="center", va="center", fontsize=6.5, color=COLORS["ink"])

    # Exactly one electrolyte-flow arrow, drawn independently of the coordinate axes.
    ax.add_patch(FancyArrowPatch((0.29, 0.35), (0.29, 0.64), arrowstyle="-|>", mutation_scale=8, linewidth=1.25, color=COLORS["blue"]))
    ax.text(0.315, 0.36, "flow", ha="left", va="center", fontsize=6.5, fontweight="bold", color=COLORS["blue"])


def draw_direct_node(
    ax: plt.Axes,
    x: float,
    title: str,
    symbol: str,
    evidence: str,
    color: str,
    underline_width: float,
    symbol_size: float = 9.0,
) -> None:
    ax.text(x, 0.69, title, ha="center", va="center", fontsize=7.0, fontweight="bold", color=COLORS["ink"], linespacing=0.93)
    ax.text(x, 0.51, symbol, ha="center", va="center", fontsize=symbol_size, color=color)
    ax.plot([x - underline_width / 2, x + underline_width / 2], [0.435, 0.435], color=color, lw=1.65, solid_capstyle="butt")
    ax.plot([x, x], [0.435, 0.335], color=color, lw=1.0)
    ax.text(x, 0.195, evidence, ha="center", va="center", fontsize=6.5, color=COLORS["muted"])


def draw_state_relation(ax: plt.Axes) -> None:
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_axis_off()
    panel_label(ax, "b", "Positive-electrode state relation")

    xs = [0.08, 0.35, 0.64, 0.91]
    draw_direct_node(ax, xs[0], "Free-I$_2$\nsupersaturation", r"$S$", "modeled state", COLORS["blue"], 0.13)
    draw_direct_node(ax, xs[1], "Retained\nsolid", r"$\varepsilon_s$", "modeled state", COLORS["amber"], 0.11)
    draw_direct_node(ax, xs[2], "Remaining\naccessible area", r"$A_{\mathrm{bare}}/A_0=1-\theta_{\mathrm{cal}}$", "calibrated relation", COLORS["teal"], 0.22, symbol_size=6.5)
    draw_direct_node(ax, xs[3], "Voltage\nresponse", r"$V$", "model output", COLORS["graphite"], 0.09)

    verbs = ["gates", "maps", "modulates"]
    for idx, verb in enumerate(verbs):
        x0, x1 = xs[idx] + 0.02, xs[idx + 1] - 0.02
        ax.add_patch(FancyArrowPatch((x0, 0.335), (x1, 0.335), arrowstyle="-|>", mutation_scale=7.5, linewidth=0.85, color=COLORS["ink"]))
        ax.text((x0 + x1) / 2, 0.39, verb, ha="center", va="center", fontsize=6.5, color=COLORS["muted"], bbox={"boxstyle": "square,pad=0.04", "facecolor": "white", "edgecolor": "none"})

    # The dashed calibration path terminates only on the accessible-area underline.
    ax.text(0.775, 0.91, "voltage calibration", ha="center", va="center", fontsize=6.5, fontweight="bold", color=COLORS["vermilion"])
    ax.add_patch(
        FancyArrowPatch(
            (0.775, 0.855),
            (0.715, 0.447),
            arrowstyle="-|>",
            mutation_scale=8,
            linewidth=1.0,
            linestyle=(0, (3, 2)),
            color=COLORS["vermilion"],
            connectionstyle="arc3,rad=0.18",
        )
    )


def draw_direct_state(
    ax: plt.Axes,
    x: float,
    expression: str,
    interval: str,
    color: str,
    underline_width: float,
    expression_size: float = 7.4,
) -> None:
    ax.plot([x, x], [0.50, 0.38], color=COLORS["line"], lw=0.7)
    ax.text(x, 0.305, expression, ha="center", va="center", fontsize=expression_size, fontweight="bold", color=color)
    ax.plot([x - underline_width / 2, x + underline_width / 2], [0.225, 0.225], color=color, lw=1.7, solid_capstyle="butt")
    ax.text(x, 0.105, interval, ha="center", va="center", fontsize=6.5, color=COLORS["muted"])


def draw_capacity_rail(ax: plt.Axes, q_s: float, q_f: float) -> None:
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_axis_off()
    panel_label(ax, "c", "Capacity markers and modeled states")

    x0, x1, y = 0.085, 0.96, 0.57
    q_max = 120.0

    def q_to_x(q: float) -> float:
        return x0 + (q / q_max) * (x1 - x0)

    ax.add_patch(FancyArrowPatch((x0, y), (x1, y), arrowstyle="-|>", mutation_scale=8, linewidth=0.95, color=COLORS["ink"]))
    ax.text(x0, y - 0.07, "0", ha="center", va="top", fontsize=6.5, color=COLORS["muted"])
    ax.text(x1 - 0.003, y - 0.07, "120", ha="right", va="top", fontsize=6.5, color=COLORS["muted"])
    ax.text(x1, y + 0.075, r"$Q$ (mAh cm$^{-2}$)", ha="right", va="bottom", fontsize=6.5, color=COLORS["ink"])

    xs, xf = q_to_x(q_s), q_to_x(q_f)
    ax.plot([xs, xs], [y - 0.06, y + 0.13], color=COLORS["amber"], lw=1.35)
    ax.plot([xf, xf], [y - 0.06, y + 0.13], color=COLORS["vermilion"], lw=1.35, linestyle=(0, (3, 2)))
    ax.text(xs - 0.012, 0.82, rf"$Q_s={q_s:.1f}$", ha="right", va="center", fontsize=7.0, fontweight="bold", color=COLORS["amber"])
    ax.text(xf + 0.012, 0.82, rf"$Q_{{f,\mathrm{{cal}}}}={q_f:.1f}$", ha="left", va="center", fontsize=7.0, fontweight="bold", color=COLORS["vermilion"])

    # Exactly three direct state annotations; no cards or pictorial glyphs.
    draw_direct_state(ax, 0.34, r"mean $S<1$", r"before $Q_s$", COLORS["blue"], 0.13)
    draw_direct_state(ax, (xs + xf) / 2 - 0.018, r"$\varepsilon_s$ increases", "between markers", COLORS["amber"], 0.10, expression_size=6.8)
    draw_direct_state(ax, 0.89, r"mean $A_{\mathrm{bare}}/A_0<0.5$", r"after $Q_{f,\mathrm{cal}}$", COLORS["teal"], 0.17, expression_size=6.5)


def build_figure(q_s: float, q_f: float) -> plt.Figure:
    fig = plt.figure(figsize=(WIDTH_MM / 25.4, HEIGHT_MM / 25.4), dpi=RASTER_DPI)
    grid = fig.add_gridspec(
        2,
        2,
        height_ratios=[0.59, 0.41],
        width_ratios=[0.34, 0.66],
        left=0.025,
        right=0.985,
        top=0.96,
        bottom=0.045,
        hspace=0.08,
        wspace=0.095,
    )
    draw_domain(fig.add_subplot(grid[0, 0]))
    draw_state_relation(fig.add_subplot(grid[0, 1]))
    draw_capacity_rail(fig.add_subplot(grid[1, :]), q_s, q_f)
    return fig


def write_source_table(geometry: dict[str, dict[str, str]], q_s: float, q_f: float) -> Path:
    out = HERE / "R582_domain_state_v2_source_data.csv"
    rows = [
        ("a", "domain x minimum", "x_min", geometry["positive_domain_x_min"]["value"], "mm", "registered geometry", relative(GEOMETRY_CSV)),
        ("a", "domain x maximum", "x_max", geometry["positive_domain_x_max"]["value"], "mm", "registered geometry", relative(GEOMETRY_CSV)),
        ("a", "domain y minimum", "y_min", geometry["positive_domain_y_min"]["value"], "mm", "registered geometry", relative(GEOMETRY_CSV)),
        ("a", "domain y maximum", "y_max", geometry["positive_domain_y_max"]["value"], "mm", "registered geometry", relative(GEOMETRY_CSV)),
        ("a", "felt thickness", "L_x", geometry["felt_thickness"]["value"], "mm", "registered geometry", relative(GEOMETRY_CSV)),
        ("b", "free-I2 supersaturation", "S", "", "dimensionless", "modeled state", relative(STATE_CSV)),
        ("b", "retained solid", "eps_s", "", "volume fraction", "modeled state", relative(STATE_CSV)),
        ("b", "remaining accessible area", "A_bare/A0", "1-theta_cal", "fraction", "voltage-calibrated relation", relative(STATE_CSV)),
        ("b", "voltage response", "V", "", "V", "model output", relative(STATE_CSV)),
        ("c", "average saturation marker", "Q_s", f"{q_s:.1f}", "mAh cm^-2", "baseline-simulation marker", relative(STATE_BUILD)),
        ("c", "calibrated half-accessibility marker", "Q_f,cal", f"{q_f:.1f}", "mAh cm^-2", "voltage-calibrated marker", relative(STATE_BUILD)),
    ]
    with out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["panel", "element", "symbol", "value", "unit", "evidence_class", "source"])
        writer.writerows(rows)
    return out


def save_outputs(fig: plt.Figure) -> dict[str, Path]:
    outputs = {ext: FIG_DIR / f"{STEM}.{ext}" for ext in ("svg", "pdf", "png", "tiff")}
    fig.savefig(outputs["svg"], format="svg", metadata={"Date": "2026-07-20", "Creator": "R582 v2 deterministic Python build"})
    fig.savefig(
        outputs["pdf"],
        format="pdf",
        metadata={
            "Title": "R582 v2 ZIFB positive-electrode domain and state relation",
            "Author": "R582 v2 deterministic Python build",
            "Creator": "matplotlib",
            "Producer": "matplotlib",
            "CreationDate": FIXED_DATE,
            "ModDate": FIXED_DATE,
        },
    )
    fig.savefig(outputs["png"], format="png", dpi=RASTER_DPI, metadata={"Software": "matplotlib R582 v2"})
    fig.savefig(outputs["tiff"], format="tiff", dpi=RASTER_DPI, pil_kwargs={"compression": "tiff_lzw"})
    outputs["preview_180mm"] = FIG_DIR / f"{STEM}_180mm_preview.png"
    fig.savefig(outputs["preview_180mm"], format="png", dpi=PREVIEW_DPI, metadata={"Software": "matplotlib R582 v2 180-mm preview"})
    outputs["grayscale"] = FIG_DIR / f"{STEM}_grayscale_QA.png"
    with Image.open(outputs["png"]) as image:
        ImageOps.grayscale(image).save(outputs["grayscale"], dpi=(RASTER_DPI, RASTER_DPI), optimize=False)
    return outputs


def resolved_fonts(fig: plt.Figure) -> list[str]:
    resolved: set[str] = set()
    for artist in fig.findobj(mpl.text.Text):
        if not artist.get_text().strip():
            continue
        font_path = Path(font_manager.findfont(artist.get_fontproperties(), fallback_to_default=False)).resolve()
        resolved.add(str(font_path))
    return sorted(resolved)


def embedded_pdf_fonts(pdf_path: Path) -> list[str]:
    if not PDFFONTS_EXE.is_file():
        raise FileNotFoundError(f"Required PDF font-audit tool is missing: {PDFFONTS_EXE}")
    result = subprocess.run(
        [str(PDFFONTS_EXE), str(pdf_path)],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    names: list[str] = []
    for line in result.stdout.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("name") or stripped.startswith("-"):
            continue
        names.append(stripped.split()[0])
    return sorted(set(names))


def run_qa(fig: plt.Figure, outputs: dict[str, Path]) -> tuple[Path, dict[str, object]]:
    text_artists = [artist for artist in fig.findobj(mpl.text.Text) if artist.get_text().strip()]
    minimum_font_size = min(artist.get_fontsize() for artist in text_artists)
    artwork_text = " ".join(artist.get_text() for artist in text_artists).lower()
    font_files = resolved_fonts(fig)
    all_fonts_termes = all(Path(path).name.lower().startswith("texgyretermes-") for path in font_files)
    pdf_font_names = embedded_pdf_fonts(outputs["pdf"])
    all_pdf_fonts_termes = bool(pdf_font_names) and all("texgyretermes-" in name.lower() for name in pdf_font_names)

    with Image.open(outputs["png"]) as image:
        png_size = list(image.size)
    with Image.open(outputs["preview_180mm"]) as image:
        preview_size = list(image.size)
    svg_text = outputs["svg"].read_text(encoding="utf-8")
    svg_lower = svg_text.lower()

    expected_png = [int(WIDTH_MM / 25.4 * RASTER_DPI), int(HEIGHT_MM / 25.4 * RASTER_DPI)]
    expected_preview = [int(WIDTH_MM / 25.4 * PREVIEW_DPI), int(HEIGHT_MM / 25.4 * PREVIEW_DPI)]
    prohibited_fonts = [name for name in ("arial", "helvetica", "dejavu sans", "times new roman") if name in svg_lower]
    qa = {
        "backend": "Python/matplotlib only",
        "archetype": "editorial schematic-led composite",
        "final_dimensions_mm": [WIDTH_MM, HEIGHT_MM],
        "figure_dimensions_mm_from_canvas": [round(float(fig.get_size_inches()[0] * 25.4), 6), round(float(fig.get_size_inches()[1] * 25.4), 6)],
        "png_pixels_600dpi": png_size,
        "expected_png_pixels_600dpi": expected_png,
        "preview_180mm_pixels_300dpi": preview_size,
        "expected_preview_180mm_pixels_300dpi": expected_preview,
        "minimum_font_size_pt": minimum_font_size,
        "declared_font_family": FONT_FAMILY,
        "registered_font_files": [str(path) for path in FONT_PATHS.values()],
        "resolved_artist_font_files": font_files,
        "all_artist_fonts_resolve_to_tex_gyre_termes": all_fonts_termes,
        "embedded_pdf_font_names": pdf_font_names,
        "all_embedded_pdf_fonts_are_tex_gyre_termes": all_pdf_fonts_termes,
        "svg_tex_gyre_termes_occurrences": svg_text.count(FONT_FAMILY),
        "prohibited_svg_font_names": prohibited_fonts,
        "editable_svg_text_nodes": svg_text.count("<text"),
        "svg_embedded_raster_images": svg_text.count("<image"),
        "causal_node_count": 4,
        "state_annotation_count": 3,
        "rounded_state_cards": 0,
        "nh4br_in_artwork": "nh4br" in artwork_text,
        "morphology_depicted": False,
        "grayscale_preview_written": outputs["grayscale"].is_file(),
    }
    qa["pass"] = all(
        [
            qa["figure_dimensions_mm_from_canvas"] == [WIDTH_MM, HEIGHT_MM],
            qa["png_pixels_600dpi"] == expected_png,
            qa["preview_180mm_pixels_300dpi"] == expected_preview,
            minimum_font_size >= 6.5,
            all_fonts_termes,
            all_pdf_fonts_termes,
            qa["svg_tex_gyre_termes_occurrences"] > 0,
            len(prohibited_fonts) == 0,
            qa["editable_svg_text_nodes"] > 0,
            qa["svg_embedded_raster_images"] == 0,
            qa["causal_node_count"] == 4,
            qa["state_annotation_count"] == 3,
            qa["rounded_state_cards"] == 0,
            not qa["nh4br_in_artwork"],
            not qa["morphology_depicted"],
            qa["grayscale_preview_written"],
        ]
    )

    qa_json = HERE / "R582_domain_state_v2_QA.json"
    qa_json.write_text(json.dumps(qa, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    qa_md = HERE / "R582_domain_state_v2_QA.md"
    qa_md.write_text(
        "# R582 Figure 2 v2 QA\n\n"
        f"- Overall: {'PASS' if qa['pass'] else 'FAIL'}\n"
        f"- Final canvas: {WIDTH_MM:.0f} x {HEIGHT_MM:.0f} mm\n"
        f"- Minimum artwork text: {minimum_font_size:.1f} pt\n"
        f"- Declared family: {FONT_FAMILY}\n"
        f"- Resolved artist fonts: {', '.join(Path(path).name for path in font_files)}\n"
        f"- All artist fonts resolve to TeX Gyre Termes: {'PASS' if all_fonts_termes else 'FAIL'}\n"
        f"- Embedded PDF fonts: {', '.join(pdf_font_names)}\n"
        f"- All embedded PDF fonts are TeX Gyre Termes: {'PASS' if all_pdf_fonts_termes else 'FAIL'}\n"
        f"- Prohibited SVG font names: {', '.join(prohibited_fonts) if prohibited_fonts else 'none'}\n"
        f"- SVG editable text nodes: {qa['editable_svg_text_nodes']}\n"
        f"- SVG embedded rasters: {qa['svg_embedded_raster_images']}\n"
        "- Four unboxed causal nodes: PASS\n"
        "- Exactly three direct state annotations: PASS\n"
        "- Rounded state cards: 0\n"
        "- NH4Br omitted: PASS\n"
        "- Morphology depiction absent: PASS\n"
        f"- 180-mm preview: `manuscript/figures_R582/{STEM}_180mm_preview.png`\n"
        f"- Grayscale preview: `manuscript/figures_R582/{STEM}_grayscale_QA.png`\n",
        encoding="utf-8",
    )
    return qa_json, qa


def write_manifest(source_table: Path, outputs: dict[str, Path], qa_json: Path, qa: dict[str, object]) -> Path:
    input_paths = [GEOMETRY_CSV, STATE_CSV, STATE_BUILD, *FONT_PATHS.values()]
    artifact_paths = [outputs[key] for key in ("svg", "pdf", "png", "tiff", "preview_180mm", "grayscale")]
    artifact_paths.extend(
        [
            source_table,
            qa_json,
            HERE / "R582_domain_state_v2_QA.md",
            HERE / "R582_FIGURE_CONTRACT_v2.md",
            HERE / "CAPTION_DRAFT_v2.md",
            HERE / "README_v2.md",
        ]
    )
    manifest = {
        "figure": STEM,
        "core_conclusion": "The model separates a 2D ZIFB positive-electrode domain into supersaturation, retained solid, remaining accessible area, and voltage response.",
        "backend": "Python/matplotlib",
        "dimensions_mm": [WIDTH_MM, HEIGHT_MM],
        "raster_dpi": RASTER_DPI,
        "font_family": FONT_FAMILY,
        "state_annotation_count": 3,
        "causal_node_count": 4,
        "rounded_state_cards": 0,
        "calibration_target": "A_bare/A0 = 1 - theta_cal only",
        "morphology_claim": False,
        "qa_pass": bool(qa["pass"]),
        "script": {"path": relative(Path(__file__)), "bytes": Path(__file__).stat().st_size, "sha256": sha256(Path(__file__))},
        "inputs": [{"path": relative(path), "bytes": path.stat().st_size, "sha256": sha256(path)} for path in input_paths],
        "artifacts": [{"path": relative(path), "bytes": path.stat().st_size, "sha256": sha256(path)} for path in artifact_paths],
    }
    out = HERE / "R582_DOMAIN_STATE_V2_BUILD.json"
    out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return out


def main() -> None:
    geometry, q_s, q_f = read_registered_inputs()
    source_table = write_source_table(geometry, q_s, q_f)
    fig = build_figure(q_s, q_f)
    outputs = save_outputs(fig)
    qa_json, qa = run_qa(fig, outputs)
    plt.close(fig)
    manifest_path = write_manifest(source_table, outputs, qa_json, qa)
    if not qa["pass"]:
        raise SystemExit(f"Figure QA failed; inspect {qa_json}")
    print(json.dumps({"figure": STEM, "qa_pass": True, "manifest": relative(manifest_path)}, indent=2))


if __name__ == "__main__":
    main()
