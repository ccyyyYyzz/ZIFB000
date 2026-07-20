#!/usr/bin/env python3
"""Verify the user-mandated manuscript/figure font-family consistency.

The R582 body uses TeX Gyre Termes (`tgtermes`) with NewTX mathematics. New
figure text must use the exact TeX Gyre Termes OTF files. The final manuscript
PDF must not retain Arial/Helvetica/DejaVu/Liberation text from legacy figures.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from pathlib import Path


SCRIPT = Path(__file__).resolve()
ACTIVE_TEX_NAMES = ("main_R582.tex", "SI_R582.tex")
ACTIVE_PDF_NAMES = ("main_R582.pdf", "SI_R582.pdf")
EXPECTED_FIGURES = 19
EXPECTED_RECORDS = len(ACTIVE_PDF_NAMES) + EXPECTED_FIGURES
FORBIDDEN = (
    "Arial",
    "Helvetica",
    "DejaVu",
    "Liberation",
    "Calibri",
    "TimesNewRoman",
    "Times New Roman",
    "NimbusRoman",
)
BODY_REQUIRED = "TeXGyreTermes"
FIGURE_REQUIRED = "TeXGyreTermes"


def locate_manuscript_root() -> Path:
    """Support both manuscript/audit_R582 and release-root/audit layouts."""

    candidates = (SCRIPT.parents[1], SCRIPT.parents[1] / "manuscript")
    for candidate in candidates:
        if all((candidate / name).is_file() for name in ACTIVE_TEX_NAMES):
            return candidate
    searched = ", ".join(str(candidate) for candidate in candidates)
    raise FileNotFoundError(f"Cannot locate active R582 manuscript sources; searched: {searched}")


def locate_pdffonts() -> Path:
    candidates: list[Path] = []
    configured = os.environ.get("R582_PDFFONTS") or os.environ.get("PDFFONTS")
    if configured:
        candidates.append(Path(configured))
    discovered = shutil.which("pdffonts")
    if discovered:
        candidates.append(Path(discovered))
    for year in (2026, 2025, 2024, 2023):
        candidates.extend(
            (
                Path(fr"D:\Program Files\texlive\{year}\bin\windows\pdffonts.exe"),
                Path(fr"D:\texlive\{year}\bin\windows\pdffonts.exe"),
                Path(fr"C:\texlive\{year}\bin\windows\pdffonts.exe"),
            )
        )
    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve()
    searched = ", ".join(str(candidate) for candidate in candidates) or "PATH"
    raise FileNotFoundError(f"pdffonts was not found; searched: {searched}")


MANUSCRIPT = locate_manuscript_root()
PDFFONTS = locate_pdffonts()


def report_path(path: Path) -> str:
    """Use layout-independent paths so canonical and packaged audits match."""

    return path.resolve().relative_to(MANUSCRIPT.resolve()).as_posix()


def pdf_font_rows(path: Path) -> list[dict[str, str]]:
    completed = subprocess.run(
        [str(PDFFONTS), str(path)],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    rows: list[dict[str, str]] = []
    pattern = re.compile(
        r"^(?P<name>\S+)\s+(?P<type>.+?)\s+(?P<encoding>\S+)\s+"
        r"(?P<embedded>yes|no)\s+(?P<subset>yes|no)\s+(?P<unicode>yes|no)\s+"
        r"\d+\s+\d+\s*$"
    )
    for line in completed.stdout.splitlines()[2:]:
        match = pattern.match(line.strip())
        if match:
            rows.append(match.groupdict())
    return rows


def inspect_pdf(path: Path, require_body: bool) -> dict:
    rows = pdf_font_rows(path)
    names = [row["name"] for row in rows]
    forbidden = sorted({name for name in names if any(x.lower() in name.lower() for x in FORBIDDEN)})
    required = BODY_REQUIRED if require_body else FIGURE_REQUIRED
    has_required = any(required.lower() in name.lower() for name in names)
    has_type3 = any("type 3" in row["type"].lower() for row in rows)
    unembedded = sorted({row["name"] for row in rows if row["embedded"] != "yes"})
    unsubsets = sorted({row["name"] for row in rows if row["subset"] != "yes"})
    unexpected = [] if require_body else sorted(
        {name for name in names if FIGURE_REQUIRED.lower() not in name.lower()}
    )
    return {
        "path": report_path(path),
        "fonts": sorted(set(names)),
        "required_termes_present": has_required,
        "forbidden_families": forbidden,
        "unexpected_figure_families": unexpected,
        "unembedded_fonts": unembedded,
        "unsubset_fonts": unsubsets,
        "type3_present": has_type3,
        "pass": (
            bool(rows)
            and has_required
            and not forbidden
            and not unexpected
            and not unembedded
            and not unsubsets
            and not has_type3
        ),
    }


def main() -> int:
    records: list[dict] = []
    layout_errors: list[str] = []
    for name in ACTIVE_PDF_NAMES:
        path = MANUSCRIPT / name
        if not path.is_file():
            records.append({
                "path": report_path(path),
                "fonts": [],
                "required_termes_present": False,
                "forbidden_families": [],
                "unexpected_figure_families": [],
                "unembedded_fonts": [],
                "unsubset_fonts": [],
                "type3_present": False,
                "pass": False,
                "error": "active manuscript PDF is missing",
            })
        else:
            records.append(inspect_pdf(path, require_body=True))

    figure_dir = MANUSCRIPT / "figures_R582"
    # Audit only figures actually referenced by the active R582 TeX sources.
    # Historical alternatives remain in the directory for provenance and are
    # intentionally excluded from the submission font gate.
    referenced: set[Path] = set()
    for tex_name in ACTIVE_TEX_NAMES:
        tex_path = MANUSCRIPT / tex_name
        if not tex_path.is_file():
            continue
        tex = tex_path.read_text(encoding="utf-8")
        for match in re.finditer(r"\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}", tex):
            raw = match.group(1)
            candidate = Path(raw)
            if candidate.suffix.lower() != ".pdf":
                candidate = candidate.with_suffix(".pdf")
            if not candidate.is_absolute():
                candidate = figure_dir / candidate.name
            referenced.add(candidate.resolve())
    if len(referenced) != EXPECTED_FIGURES:
        layout_errors.append(
            f"Expected {EXPECTED_FIGURES} unique referenced figure PDFs, found {len(referenced)}"
        )
    for path in sorted(referenced):
        if not path.is_file():
            records.append({
                "path": report_path(path),
                "fonts": [],
                "required_termes_present": False,
                "forbidden_families": [],
                "unexpected_figure_families": [],
                "unembedded_fonts": [],
                "unsubset_fonts": [],
                "type3_present": False,
                "pass": False,
                "error": "referenced figure PDF is missing",
            })
        else:
            records.append(inspect_pdf(path, require_body=False))

    if len(records) != EXPECTED_RECORDS:
        layout_errors.append(f"Expected {EXPECTED_RECORDS} PDF records, found {len(records)}")
    failures = [record["path"] for record in records if not record["pass"]]
    failures.extend(layout_errors)
    payload = {
        "manuscript_layout": "main_R582.tex + SI_R582.tex + figures_R582/",
        "pdffonts_tool": "Poppler pdffonts",
        "expected_records": EXPECTED_RECORDS,
        "record_count": len(records),
        "records": records,
        "layout_errors": layout_errors,
        "failures": failures,
    }
    serialized = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    Path(__file__).with_name("R582_FINAL_FONT_GATE.json").write_text(
        serialized,
        encoding="utf-8",
        newline="\n",
    )
    print(serialized, end="")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
