#!/usr/bin/env python
"""Shared deterministic export and QA utilities for R582 SI figures.

The module registers the exact TeX Gyre Termes OTF faces used by the manuscript
body.  It deliberately rejects fallback font families and Type 3 PDF fonts.
"""

from __future__ import annotations

import hashlib
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.text import Text
from PIL import Image


SOURCE_DATA_DIR = Path(__file__).resolve().parent.parent
if str(SOURCE_DATA_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DATA_DIR))
from r582_font_runtime import locate_tex_tool, register_termes_fonts


TERMES_DIR, _TERMES_BY_ROLE, FONT_FAMILY = register_termes_fonts(font_manager)
TERMES_PATHS = list(_TERMES_BY_ROLE.values())
PDFFONTS = locate_tex_tool("pdffonts", TERMES_DIR)
PDFINFO = locate_tex_tool("pdfinfo", TERMES_DIR)
FIXED_TIME = datetime(2026, 7, 20, tzinfo=timezone.utc)

INK = "#20252A"
MID_GREY = "#6D7378"
LIGHT_GREY = "#D9DDE0"
PALE_GREY = "#F0F1F2"
WHITE = "#FFFFFF"
NAVY = "#254F73"
BLUE = "#3B719B"
LIGHT_BLUE = "#8CAFC7"
TEAL = "#397A78"
CARMINE = "#A94C45"
GOLD = "#B4873A"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def configure_font(hashsalt: str) -> str:
    family = FONT_FAMILY
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": [family],
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
            "legend.frameon": False,
            "svg.fonttype": "none",
            "svg.hashsalt": hashsalt,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "mathtext.fontset": "custom",
            "mathtext.rm": family,
            "mathtext.it": f"{family}:italic",
            "mathtext.bf": f"{family}:bold",
            "mathtext.cal": f"{family}:italic",
            "mathtext.sf": family,
            "mathtext.fallback": None,
            "savefig.facecolor": "white",
            "figure.facecolor": "white",
        }
    )
    return family


def style_axis(ax, zero_line: bool = False) -> None:
    ax.spines["left"].set_color(INK)
    ax.spines["bottom"].set_color(INK)
    ax.tick_params(colors=INK, direction="out", pad=2.0)
    if zero_line:
        ax.axhline(0.0, color=LIGHT_GREY, lw=0.7, zorder=0)


def panel_label(ax, label: str, x: float = -0.12, y: float = 1.04) -> None:
    ax.text(
        x,
        y,
        label,
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=8.0,
        fontweight="bold",
        color=INK,
    )


def audit_text(fig, family: str) -> dict:
    fig.canvas.draw()
    texts = [item for item in fig.findobj(match=Text) if item.get_text().strip()]
    sizes = [float(item.get_fontsize()) for item in texts]
    families = sorted({item.get_fontproperties().get_name() for item in texts})
    if not sizes or min(sizes) < 6.5 - 1e-9:
        raise ValueError(f"Figure contains text below 6.5 pt: {min(sizes) if sizes else 'none'}")
    if families != [family]:
        raise ValueError(f"Unexpected resolved font families: {families}")
    return {
        "minimum_text_pt": min(sizes),
        "resolved_font_families": families,
        "text_items": len(texts),
    }


def _save_render(
    fig,
    out_dir: Path,
    stem: str,
    title: str,
    creator: str,
    width_mm: float,
    height_mm: float,
) -> dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    base = out_dir / stem
    paths = {
        "svg": base.with_suffix(".svg"),
        "pdf": base.with_suffix(".pdf"),
        "png": base.with_suffix(".png"),
        "tiff": base.with_suffix(".tiff"),
        "preview": out_dir / f"{stem}_180mm_preview.png",
        "grayscale": out_dir / f"{stem}_180mm_preview_grayscale.png",
    }
    fig.savefig(
        paths["svg"],
        format="svg",
        metadata={"Title": title, "Creator": creator, "Date": "2026-07-20"},
    )
    fig.savefig(
        paths["pdf"],
        format="pdf",
        metadata={
            "Title": title,
            "Creator": creator,
            "Producer": "matplotlib",
            "CreationDate": FIXED_TIME,
            "ModDate": FIXED_TIME,
        },
    )
    # Raster dimensions are snapped to the nearest 600-dpi pixel while the
    # vector canvas above remains exactly the requested physical size.
    raster_width = round(width_mm / 25.4 * 600.0)
    raster_height = round(height_mm / 25.4 * 600.0)
    fig.set_size_inches(raster_width / 600.0, raster_height / 600.0, forward=True)
    fig.savefig(paths["png"], format="png", dpi=600, transparent=False)
    plt.close(fig)
    with Image.open(paths["png"]) as image:
        rgb = image.convert("RGB")
        rgb.save(paths["tiff"], format="TIFF", compression="tiff_lzw", dpi=(600, 600))
        preview_width = round(width_mm / 25.4 * 300.0)
        preview_height = round(height_mm / 25.4 * 300.0)
        preview = rgb.resize((preview_width, preview_height), Image.Resampling.LANCZOS)
        preview.save(paths["preview"], dpi=(300, 300), optimize=True)
        preview.convert("L").save(paths["grayscale"], dpi=(300, 300), optimize=True)
    return paths


def pdf_font_audit(path: Path, family: str) -> dict:
    if not PDFFONTS.is_file():
        raise FileNotFoundError(PDFFONTS)
    completed = subprocess.run(
        [str(PDFFONTS), str(path)],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    lines = [line for line in completed.stdout.splitlines()[2:] if line.strip()]
    names = sorted({line.split()[0] for line in lines})
    forbidden_tokens = ("Arial", "Helvetica", "DejaVu", "Liberation", "Calibri", "TimesNewRoman")
    forbidden = sorted({name for name in names if any(token.lower() in name.lower() for token in forbidden_tokens)})
    has_type3 = bool(re.search(r"\bType 3\b", completed.stdout))
    has_termes = any("TeXGyreTermes".lower() in name.lower() for name in names)
    if forbidden or has_type3 or not has_termes:
        raise ValueError(
            f"PDF font audit failed: names={names}, forbidden={forbidden}, Type3={has_type3}"
        )
    return {
        "font_names": names,
        "required_family": family,
        "forbidden_families": forbidden,
        "type3_present": has_type3,
        "pass": True,
    }


def pdf_size_audit(path: Path, width_mm: float, height_mm: float) -> dict:
    if not PDFINFO.is_file():
        raise FileNotFoundError(PDFINFO)
    completed = subprocess.run(
        [str(PDFINFO), str(path)],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    match = re.search(r"Page size:\s+([0-9.]+) x ([0-9.]+) pts", completed.stdout)
    if not match:
        raise ValueError("Could not parse PDF page size")
    observed = [float(match.group(1)) * 25.4 / 72.0, float(match.group(2)) * 25.4 / 72.0]
    if abs(observed[0] - width_mm) > 0.06 or abs(observed[1] - height_mm) > 0.06:
        raise ValueError(f"PDF size mismatch: expected {(width_mm, height_mm)}, observed {observed}")
    return {"expected_mm": [width_mm, height_mm], "observed_mm": observed, "pass": True}


def raster_audit(paths: dict[str, Path], width_mm: float, height_mm: float) -> dict:
    expected_600 = [round(width_mm / 25.4 * 600), round(height_mm / 25.4 * 600)]
    expected_300 = [round(width_mm / 25.4 * 300), round(height_mm / 25.4 * 300)]
    with Image.open(paths["png"]) as image:
        png_size = list(image.size)
        png_mode = image.mode
    with Image.open(paths["tiff"]) as image:
        tiff_size = list(image.size)
        tiff_mode = image.mode
    with Image.open(paths["preview"]) as image:
        preview_size = list(image.size)
        preview_mode = image.mode
    with Image.open(paths["grayscale"]) as image:
        grayscale_size = list(image.size)
        grayscale_mode = image.mode
        extrema = list(image.getextrema())
    if png_size != expected_600 or tiff_size != expected_600:
        raise ValueError(f"600 dpi raster size mismatch: png={png_size}, tiff={tiff_size}, expected={expected_600}")
    if preview_size != expected_300 or grayscale_size != expected_300:
        raise ValueError(
            f"300 dpi preview size mismatch: color={preview_size}, gray={grayscale_size}, expected={expected_300}"
        )
    if png_mode != "RGBA" or tiff_mode != "RGB" or preview_mode != "RGB" or grayscale_mode != "L":
        raise ValueError(
            f"Unexpected raster modes: png={png_mode}, tiff={tiff_mode}, preview={preview_mode}, gray={grayscale_mode}"
        )
    return {
        "expected_600dpi_pixels": expected_600,
        "png_pixels": png_size,
        "tiff_pixels": tiff_size,
        "expected_300dpi_preview_pixels": expected_300,
        "preview_pixels": preview_size,
        "grayscale_pixels": grayscale_size,
        "grayscale_mode": grayscale_mode,
        "grayscale_extrema": extrema,
        "pass": True,
    }


def svg_font_audit(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    forbidden = [token for token in ("Arial", "Helvetica", "DejaVu", "Liberation", "Calibri") if token.lower() in text.lower()]
    if forbidden or "TeX Gyre Termes" not in text:
        raise ValueError(f"SVG font audit failed: forbidden={forbidden}")
    return {"editable_text": "<text" in text, "required_family_present": True, "forbidden": forbidden, "pass": True}


def export_deterministic(
    build_figure: Callable[[], tuple[plt.Figure, dict]],
    figure_dir: Path,
    stem: str,
    title: str,
    creator: str,
    width_mm: float,
    height_mm: float,
    family: str,
) -> tuple[dict[str, Path], dict]:
    fig, build_audit = build_figure()
    first = _save_render(fig, figure_dir, stem, title, creator, width_mm, height_mm)
    with tempfile.TemporaryDirectory(prefix=f"{stem}_rerender_") as tmp:
        fig2, build_audit_2 = build_figure()
        second = _save_render(fig2, Path(tmp), stem, title, creator, width_mm, height_mm)
        if build_audit != build_audit_2:
            raise ValueError("Figure-build audit changed between deterministic renders")
        first_hashes = {key: sha256(path) for key, path in first.items()}
        second_hashes = {key: sha256(second[key]) for key in first}
        mismatches = {key: [first_hashes[key], second_hashes[key]] for key in first if first_hashes[key] != second_hashes[key]}
        if mismatches:
            raise ValueError(f"Second-render hash mismatch: {mismatches}")
    qa = {
        "build": build_audit,
        "deterministic_second_render": {"pass": True, "sha256": first_hashes},
        "pdf_fonts": pdf_font_audit(first["pdf"], family),
        "pdf_size": pdf_size_audit(first["pdf"], width_mm, height_mm),
        "raster": raster_audit(first, width_mm, height_mm),
        "svg": svg_font_audit(first["svg"]),
    }
    return first, qa
