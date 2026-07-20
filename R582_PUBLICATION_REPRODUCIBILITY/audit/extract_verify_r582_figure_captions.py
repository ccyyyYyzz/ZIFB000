#!/usr/bin/env python3
"""Extract R582 figure captions verbatim and verify the submission bundle.

Only ``figure``/``figure*`` environments are considered. Table captions are
intentionally excluded. The generated Markdown and TeX files contain marker
blocks whose contents are compared character-for-character with the current
authoritative main and SI sources.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path


SCRIPT = Path(__file__).resolve()


def locate_layout() -> tuple[Path, Path, Path]:
    """Return manuscript, submission and audit roots in either supported layout."""

    parent = SCRIPT.parents[1]
    canonical = parent
    packaged = parent / "manuscript"
    if all((canonical / name).is_file() for name in ("main_R582.tex", "SI_R582.tex")):
        return canonical, canonical / "submission", canonical / "audit_R582"
    if all((packaged / name).is_file() for name in ("main_R582.tex", "SI_R582.tex")):
        return packaged, parent / "submission", SCRIPT.parent
    raise FileNotFoundError(
        "Cannot locate active R582 TeX sources under "
        f"{canonical} or {packaged}"
    )


MANUSCRIPT, SUBMISSION, AUDIT = locate_layout()
MAIN = MANUSCRIPT / "main_R582.tex"
SI = MANUSCRIPT / "SI_R582.tex"
OUT_MD = SUBMISSION / "FIGURE_CAPTIONS_DRAFT.md"
OUT_TEX = SUBMISSION / "FIGURE_CAPTIONS_DRAFT.tex"
QA_JSON = AUDIT / "R582_CAPTION_EXTRACTION_QA.json"

EXPECTED_MAIN_LABELS = [
    "fig:experimental-problem",
    "fig:domain-state",
    "fig:spatial-progression",
    "fig:closure-identifiability",
    "fig:multiscale-bounds",
    "fig:operating-levers",
]

EXPECTED_SI_LABELS = [
    "fig:si-derivative",
    "fig:si-composition",
    "fig:si-compression",
    "fig:si-state-fields",
    "fig:si-hydraulic-fields",
    "fig:si-voltage-degeneracy",
    "fig:si-single-i2",
    "fig:si-two-i2",
    "fig:si-md-ladder",
    "fig:si-comparator-definitions",
    "fig:si-accessibility-families",
    "fig:si-flow-postprocess",
    "fig:si-permeability",
]


@dataclass(frozen=True)
class Caption:
    source: str
    number: int
    label: str
    text: str


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def _escaped(text: str, index: int) -> bool:
    slashes = 0
    cursor = index - 1
    while cursor >= 0 and text[cursor] == "\\":
        slashes += 1
        cursor -= 1
    return bool(slashes % 2)


def _balanced_argument(text: str, command_end: int) -> tuple[str, int]:
    """Return the content and end index for a command whose opening brace ended at command_end."""
    depth = 1
    cursor = command_end
    while cursor < len(text):
        char = text[cursor]
        if char == "{" and not _escaped(text, cursor):
            depth += 1
        elif char == "}" and not _escaped(text, cursor):
            depth -= 1
            if depth == 0:
                return text[command_end:cursor], cursor + 1
        cursor += 1
    raise ValueError("Unbalanced caption braces")


def extract_figure_captions(path: Path, source: str) -> list[Caption]:
    text = path.read_text(encoding="utf-8")
    begin_re = re.compile(r"\\begin\{(figure\*?)\}")
    captions: list[Caption] = []
    cursor = 0

    while True:
        begin = begin_re.search(text, cursor)
        if begin is None:
            break
        environment = begin.group(1)
        end_token = rf"\end{{{environment}}}"
        end = text.find(end_token, begin.end())
        if end < 0:
            raise ValueError(f"Missing {end_token} in {path}")
        block_end = end + len(end_token)
        block = text[begin.start():block_end]

        caption_matches = list(re.finditer(r"\\caption\{", block))
        if len(caption_matches) != 1:
            raise ValueError(
                f"Expected one caption in {source} figure {len(captions) + 1}; "
                f"found {len(caption_matches)}"
            )
        body, _ = _balanced_argument(block, caption_matches[0].end())

        labels = re.findall(r"\\label\{([^{}]+)\}", block)
        if len(labels) != 1:
            raise ValueError(
                f"Expected one label in {source} figure {len(captions) + 1}; found {labels}"
            )

        captions.append(Caption(source, len(captions) + 1, labels[0], body))
        cursor = block_end

    return captions


def marker(caption: Caption, comment: str, end: bool = False) -> str:
    state = "END_CAPTION" if end else "BEGIN_CAPTION"
    return (
        f"{comment} {state} source={caption.source} number={caption.number} "
        f"label={caption.label}"
    )


def render_markdown(main_caps: list[Caption], si_caps: list[Caption], hashes: dict[str, str]) -> str:
    lines = [
        "# Figure captions — R582 generated submission copy",
        "",
        (
            "> AUTO-GENERATED FROM THE CURRENT AUTHORITATIVE SOURCES. "
            f"`main_R582.tex` SHA-256 `{hashes['main_R582.tex']}`; "
            f"`SI_R582.tex` SHA-256 `{hashes['SI_R582.tex']}`."
        ),
        "",
        "> Caption bodies below are copied verbatim. Regenerate after every source-caption edit.",
        "",
        "## Main manuscript",
        "",
    ]
    for cap in main_caps:
        lines.extend(
            [
                f"### Figure {cap.number} (`{cap.label}`)",
                "",
                marker(cap, "<!--" ) + " -->",
                cap.text,
                marker(cap, "<!--", end=True) + " -->",
                "",
            ]
        )

    lines.extend(["## Supplementary Information", ""])
    for cap in si_caps:
        lines.extend(
            [
                f"### Supplementary Figure S{cap.number} (`{cap.label}`)",
                "",
                marker(cap, "<!--") + " -->",
                cap.text,
                marker(cap, "<!--", end=True) + " -->",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def render_tex(main_caps: list[Caption], si_caps: list[Caption], hashes: dict[str, str]) -> str:
    preamble = rf"""\documentclass[11pt]{{article}}
\usepackage[utf8]{{inputenc}}
\usepackage[T1]{{fontenc}}
\usepackage{{amsmath,amssymb,amsfonts}}
\usepackage{{tgtermes}}
\usepackage{{newtxmath}}
\usepackage[version=4]{{mhchem}}
\usepackage{{siunitx}}
\usepackage[margin=1in]{{geometry}}
\emergencystretch=2em
\DeclareSIUnit{{\Molar}}{{M}}
\newcommand{{\epss}}{{\varepsilon_{{\mathrm{{s}}}}}}
\newcommand{{\Rtheta}}{{R_{{\theta}}}}
\newcommand{{\Tpore}}{{T_{{\mathrm{{pore}}}}}}
\begin{{document}}
\section*{{Figure captions}}
% AUTO-GENERATED FROM CURRENT SOURCES. main_R582.tex SHA-256 {hashes['main_R582.tex']}; SI_R582.tex SHA-256 {hashes['SI_R582.tex']}.
% Caption bodies are verbatim source extractions. Regenerate after every source-caption edit.
\section*{{Main manuscript}}
"""
    blocks = [preamble]
    for cap in main_caps:
        blocks.extend(
            [
                rf"\noindent\textbf{{Figure {cap.number}.}}\begingroup\space",
                marker(cap, "%"),
                cap.text,
                marker(cap, "%", end=True),
                r"\par\endgroup\medskip",
                "",
            ]
        )

    blocks.extend([r"\section*{Supplementary Information}", ""])
    for cap in si_caps:
        blocks.extend(
            [
                rf"\noindent\textbf{{Supplementary Figure S{cap.number}.}}\begingroup\space",
                marker(cap, "%"),
                cap.text,
                marker(cap, "%", end=True),
                r"\par\endgroup\medskip",
                "",
            ]
        )
    blocks.append(r"\end{document}")
    return "\n".join(blocks).rstrip() + "\n"


def write_text(path: Path, text: str) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def parse_marked(path: Path, comment: str) -> list[Caption]:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    start_re = re.compile(
        rf"^{re.escape(comment)} BEGIN_CAPTION source=(main|si) number=(\d+) label=(\S+)"
        + (r" -->" if comment == "<!--" else "")
        + r"\n?$"
    )
    records: list[Caption] = []
    index = 0
    while index < len(lines):
        match = start_re.match(lines[index])
        if match is None:
            index += 1
            continue
        source, number_text, label = match.groups()
        number = int(number_text)
        end_line = (
            f"{comment} END_CAPTION source={source} number={number} label={label}"
            + (" -->" if comment == "<!--" else "")
        )
        index += 1
        body_lines: list[str] = []
        while index < len(lines) and lines[index].rstrip("\r\n") != end_line:
            body_lines.append(lines[index])
            index += 1
        if index >= len(lines):
            raise ValueError(f"Missing marker {end_line} in {path}")
        body = "".join(body_lines)
        if body.endswith("\n"):
            body = body[:-1]
        records.append(Caption(source, number, label, body))
        index += 1
    return records


def validate_order(captions: list[Caption], expected: list[str], source: str) -> None:
    actual = [caption.label for caption in captions]
    if actual != expected:
        raise AssertionError(f"{source} figure order mismatch: {actual}")
    if [caption.number for caption in captions] != list(range(1, len(expected) + 1)):
        raise AssertionError(f"{source} numbering is not consecutive")


def main() -> None:
    if not SUBMISSION.is_dir():
        raise FileNotFoundError(f"Submission directory is missing: {SUBMISSION}")
    if not AUDIT.is_dir():
        raise FileNotFoundError(f"Audit directory is missing: {AUDIT}")
    source_hashes = {
        "main_R582.tex": sha256(MAIN),
        "SI_R582.tex": sha256(SI),
    }
    main_caps = extract_figure_captions(MAIN, "main")
    si_caps = extract_figure_captions(SI, "si")

    if len(main_caps) != 6 or len(si_caps) != 13:
        raise AssertionError(
            f"Expected 6 main and 13 SI figures; found {len(main_caps)} and {len(si_caps)}"
        )
    validate_order(main_caps, EXPECTED_MAIN_LABELS, "main")
    validate_order(si_caps, EXPECTED_SI_LABELS, "si")

    write_text(OUT_MD, render_markdown(main_caps, si_caps, source_hashes))
    write_text(OUT_TEX, render_tex(main_caps, si_caps, source_hashes))

    expected = main_caps + si_caps
    md_records = parse_marked(OUT_MD, "<!--")
    tex_records = parse_marked(OUT_TEX, "%")
    if md_records != expected:
        raise AssertionError("Markdown caption bodies differ from authoritative sources")
    if tex_records != expected:
        raise AssertionError("TeX caption bodies differ from authoritative sources")

    final_source_hashes = {
        "main_R582.tex": sha256(MAIN),
        "SI_R582.tex": sha256(SI),
    }
    if final_source_hashes != source_hashes:
        raise AssertionError("A source changed during caption extraction; rerun required")

    qa = {
        "status": "PASS",
        "source_sha256": source_hashes,
        "counts": {"main": len(main_caps), "si": len(si_caps), "total": len(expected)},
        "main_label_order": [caption.label for caption in main_caps],
        "si_label_order": [caption.label for caption in si_caps],
        "verbatim_comparison": {
            "markdown_vs_sources": True,
            "tex_vs_sources": True,
            "comparison_rule": "exact Unicode text after LF newline normalization; outer caption braces excluded",
        },
        "exp_meta_001_retained": any("EXP-META-001" in caption.text for caption in expected),
        "output_sha256": {
            str(OUT_MD.relative_to(SUBMISSION.parent)): sha256(OUT_MD),
            str(OUT_TEX.relative_to(SUBMISSION.parent)): sha256(OUT_TEX),
        },
    }
    write_text(QA_JSON, json.dumps(qa, indent=2, ensure_ascii=False) + "\n")

    print("PASS: extracted and matched 6 main + 13 SI figure captions")
    print(f"PASS: main order = {qa['main_label_order']}")
    print(f"PASS: SI order = {qa['si_label_order']}")
    print(f"PASS: EXP-META-001 retained = {qa['exp_meta_001_retained']}")
    print(f"main_R582.tex SHA-256 {source_hashes['main_R582.tex']}")
    print(f"SI_R582.tex SHA-256 {source_hashes['SI_R582.tex']}")
    for output, digest in qa["output_sha256"].items():
        print(f"{output} SHA-256 {digest}")


if __name__ == "__main__":
    main()
