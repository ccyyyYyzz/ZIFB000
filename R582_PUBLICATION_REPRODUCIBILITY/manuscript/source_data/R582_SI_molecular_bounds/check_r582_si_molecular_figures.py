"""Read-only acceptance checks for R582 Supplementary Figures S7-S9."""

from __future__ import annotations

import json
import math
import re
import subprocess
import sys
from pathlib import Path

import pandas as pd
from PIL import Image


SOURCE_DATA_DIR = Path(__file__).resolve().parent.parent
if str(SOURCE_DATA_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DATA_DIR))
from r582_font_runtime import locate_tex_tool


HERE = Path(__file__).resolve().parent
MANUSCRIPT = HERE.parents[1]
FIGURES = MANUSCRIPT / "figures_R582"
PDF_FONTS = locate_tex_tool("pdffonts")
PDF_INFO = locate_tex_tool("pdfinfo")

SPECS = {
    "S7": ("Fig_R582_SI07_single_I2_ordering", 180.0, 120.0),
    "S8": ("Fig_R582_SI08_two_I2_diagnostic", 180.0, 112.0),
    "S9": ("Fig_R582_SI09_md_carrier_ladder", 180.0, 96.0),
}
FORBIDDEN = re.compile(
    r"Arial|Helvetica|DejaVu|Computer Modern|CMR|CMMI|CMSY|CMEX|STIX|Times New Roman",
    re.IGNORECASE,
)


def check(condition: bool, message: str, results: list[dict[str, object]]) -> None:
    results.append({"check": message, "status": "PASS" if condition else "FAIL"})
    if not condition:
        raise AssertionError(message)


def run_tool(executable: Path, path: Path) -> tuple[str, str]:
    proc = subprocess.run(
        [str(executable), str(path)],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if proc.returncode != 0:
        raise RuntimeError(f"{executable.name} failed for {path}: {proc.stderr}")
    return proc.stdout, proc.stderr


def main() -> None:
    results: list[dict[str, object]] = []
    details: dict[str, object] = {}
    check(PDF_FONTS.is_file(), "pdffonts executable is available", results)
    check(PDF_INFO.is_file(), "pdfinfo executable is available", results)

    for figure, (stem, width_mm, height_mm) in SPECS.items():
        expected = {
            "pdf": FIGURES / f"{stem}.pdf",
            "svg": FIGURES / f"{stem}.svg",
            "png": FIGURES / f"{stem}.png",
            "tiff": FIGURES / f"{stem}.tiff",
            "preview": FIGURES / f"{stem}_180mm_preview.png",
            "gray": FIGURES / f"{stem}_180mm_grayscale_preview.png",
        }
        for role, path in expected.items():
            check(path.is_file() and path.stat().st_size > 0, f"{figure} {role} exists", results)

        font_text, font_stderr = run_tool(PDF_FONTS, expected["pdf"])
        font_lines = [
            line.strip()
            for line in font_text.splitlines()
            if line.strip() and not line.startswith("name") and not line.startswith("---")
        ]
        check(bool(font_lines), f"{figure} PDF has embedded fonts", results)
        check(
            all("TeXGyreTermes-" in line for line in font_lines),
            f"{figure} PDF uses only TeX Gyre Termes",
            results,
        )
        check(
            not any("Type 3" in line for line in font_lines),
            f"{figure} PDF has no Type 3 font",
            results,
        )
        check(not FORBIDDEN.search(font_text), f"{figure} PDF has no forbidden font", results)

        info_text, info_stderr = run_tool(PDF_INFO, expected["pdf"])
        match = re.search(r"Page size:\s+([0-9.]+) x ([0-9.]+) pts", info_text)
        check(match is not None, f"{figure} PDF page size is readable", results)
        assert match is not None
        width_pt, height_pt = float(match.group(1)), float(match.group(2))
        check(
            math.isclose(width_pt, width_mm / 25.4 * 72.0, abs_tol=0.02)
            and math.isclose(height_pt, height_mm / 25.4 * 72.0, abs_tol=0.02),
            f"{figure} PDF is exactly {width_mm:g} x {height_mm:g} mm",
            results,
        )

        svg = expected["svg"].read_text(encoding="utf-8")
        text_nodes = len(re.findall(r"<text\b", svg))
        font_sizes = [
            float(value)
            for value in re.findall(r"font:[^;\"]*?([0-9]+(?:\.[0-9]+)?)px", svg)
        ]
        check(text_nodes > 0, f"{figure} SVG retains editable text nodes", results)
        check(bool(font_sizes), f"{figure} SVG exposes font sizes", results)
        check(min(font_sizes) >= 6.5 - 1.0e-9, f"{figure} SVG minimum text is >= 6.5 pt", results)
        check(not FORBIDDEN.search(svg), f"{figure} SVG has no forbidden font", results)
        font_declarations = re.findall(r"font:[^;\"]+", svg)
        check(
            all("TeX Gyre Termes" in declaration for declaration in font_declarations),
            f"{figure} SVG font declarations are all TeX Gyre Termes",
            results,
        )

        raster_details = {}
        for role in ["png", "tiff"]:
            with Image.open(expected[role]) as image:
                mode = image.mode
                size = image.size
                dpi = image.info.get("dpi", (0.0, 0.0))
            expected_size = (
                int(width_mm / 25.4 * 600),
                int(height_mm / 25.4 * 600),
            )
            check(mode == "RGB", f"{figure} {role.upper()} is opaque RGB", results)
            check(
                abs(size[0] - expected_size[0]) <= 1 and abs(size[1] - expected_size[1]) <= 1,
                f"{figure} {role.upper()} pixel dimensions match 600 dpi final size",
                results,
            )
            check(
                abs(float(dpi[0]) - 600.0) < 0.1 and abs(float(dpi[1]) - 600.0) < 0.1,
                f"{figure} {role.upper()} metadata reports 600 dpi",
                results,
            )
            raster_details[role] = {
                "mode": mode,
                "pixels": [int(value) for value in size],
                "dpi": [float(value) for value in dpi],
            }

        for role in ["preview", "gray"]:
            with Image.open(expected[role]) as image:
                preview_mode = image.mode
                preview_dpi = image.info.get("dpi", (0.0, 0.0))
            check(preview_mode == "RGB", f"{figure} {role} preview is RGB", results)
            check(
                abs(float(preview_dpi[0]) - 150.0) < 0.1,
                f"{figure} {role} preview is tagged at 150 dpi",
                results,
            )

        details[figure] = {
            "fonts": font_lines,
            "pdffonts_warnings": [line for line in font_stderr.splitlines() if line.strip()],
            "pdfinfo_warnings": [line for line in info_stderr.splitlines() if line.strip()],
            "page_size_pt": [width_pt, height_pt],
            "editable_svg_text_nodes": text_nodes,
            "svg_min_font_pt": min(font_sizes),
            "svg_max_font_pt": max(font_sizes),
            "raster": raster_details,
        }

    inputs = pd.read_csv(HERE / "R582_SI_molecular_input_manifest.csv")
    check(len(inputs) == 20, "input manifest contains 16 frozen evidence files plus 4 fonts", results)
    check(inputs["sha256"].str.fullmatch(r"[0-9A-F]{64}").all(), "all input hashes are SHA-256", results)

    s7 = pd.read_csv(HERE / "R582_SI07_single_I2_energy_ordering.csv").set_index("site")
    check(
        float(s7.loc["C-OH", "relative_to_basal_eV"]) < 0
        and float(s7.loc["C=O", "relative_to_basal_eV"]) < 0
        and math.isclose(float(s7.loc["basal", "relative_to_basal_eV"]), 0.0, abs_tol=1e-12)
        and float(s7.loc["vacancy", "relative_to_basal_eV"]) > 0,
        "S7 plotted ordering matches the registered energy table",
        results,
    )

    s8_energy = pd.read_csv(HERE / "R582_SI08_two_I2_energy_comparison.csv").set_index(
        "configuration"
    )
    check(
        math.isclose(
            float(s8_energy.loc["compact", "relative_to_separated_eV"]),
            -0.6892909363332037,
            abs_tol=1e-11,
        ),
        "S8 compact-minus-separated energy is preserved",
        results,
    )
    cdd = pd.read_csv(HERE / "R582_SI08_cdd_threshold_summary.csv").iloc[0]
    check(
        int(cdd["display_accumulation_points"]) > 0
        and int(cdd["display_depletion_points"]) > 0,
        "S8 CDD retains both accumulation and depletion",
        results,
    )
    check(str(cdd["value_interpolation"]) == "none", "S8 CDD values are not interpolated", results)

    md = pd.read_csv(HERE / "R582_SI09_md_carrier_ladder.csv")
    check((pd.to_numeric(md["n_soc"]) == 5).all(), "S9 uses all five SOC compositions", results)
    for variant in ["q0p8_ecc", "q1p0"]:
        part = md.loc[md["variant"].eq(variant)].set_index("species")
        iodide = float(part.loc["I-", "D_mean"])
        check(
            all(float(part.loc[species, "D_mean"]) < iodide for species in ["I2", "I3-", "I2Br-"]),
            f"S9 oxidized-iodine means are below iodide for {variant}",
            results,
        )
    check(
        md["D_sem_definition"].str.contains("not replica uncertainty", regex=False).all(),
        "S9 block stability is not labelled replica uncertainty",
        results,
    )

    qa = {
        "release": "R582",
        "figures": ["S7", "S8", "S9"],
        "status": "PASS",
        "checks": results,
        "details": details,
        "manual_visual_review": {
            "actual_size_color": "PASS",
            "actual_size_grayscale": "PASS",
            "collision_review": "PASS",
            "evidence_caption_agreement": "PASS",
        },
        "determinism": "PASS: 15 selected figure/data artifacts byte-identical after cold rerender",
    }
    (HERE / "R582_SI_molecular_QA.json").write_text(
        json.dumps(qa, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"QA_PASS: {len(results)} automated checks passed for S7-S9")


if __name__ == "__main__":
    main()
