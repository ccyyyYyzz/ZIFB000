#!/usr/bin/env python3
"""Fast, conservative language/format gate for the active R582 manuscript.

This is not a grammar checker. It catches journal-limit violations and the
project-specific vocabulary regressions identified by the R582 audits. Run it
from any working directory; paths are resolved relative to this file.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


SCRIPT = Path(__file__).resolve()


def locate_manuscript_root() -> Path:
    """Support both manuscript/audit_R582 and release-root/audit layouts."""

    candidates = (SCRIPT.parents[1], SCRIPT.parents[1] / "manuscript")
    for candidate in candidates:
        if all((candidate / name).is_file() for name in ("main_R582.tex", "SI_R582.tex")):
            return candidate
    searched = ", ".join(str(candidate) for candidate in candidates)
    raise FileNotFoundError(f"Cannot locate active R582 TeX sources; searched: {searched}")


ROOT = locate_manuscript_root()
MAIN = ROOT / "main_R582.tex"
SI = ROOT / "SI_R582.tex"


WATCH_TERMS = [
    "registered",
    "production",
    "closure",
    "marker",
    "calibrated",
    "trajectory",
    "state clock",
    "scaffold",
    "load-bearing",
    "orthogonal evidence",
    "physical comparator",
    "fresh matched true-mesh",
    "does not",
    "rather than",
]

BAN_PHRASES = [
    "it is found that",
    "it can be clearly seen that",
    "synergistic interplay",
    "spatiotemporal evolution pathway",
    "comprehensive framework",
    "holistic framework",
    "pave the way",
    "shed light on",
    "unambiguously proves",
    "definitively establish",
]


def strip_comments(tex: str) -> str:
    return re.sub(r"(?<!\\)%.*", "", tex)


def extract_command(tex: str, command: str) -> str:
    match = re.search(rf"\\{re.escape(command)}\s*\{{", tex)
    if not match:
        return ""
    depth = 1
    i = match.end()
    start = i
    while i < len(tex) and depth:
        if tex[i] == "{" and (i == 0 or tex[i - 1] != "\\"):
            depth += 1
        elif tex[i] == "}" and (i == 0 or tex[i - 1] != "\\"):
            depth -= 1
        i += 1
    return tex[start : i - 1] if depth == 0 else ""


def tex_to_words(tex: str) -> list[str]:
    tex = strip_comments(tex)
    tex = re.sub(r"\\begin\{(?:equation|align|table|figure).*?\\end\{(?:equation|align|table|figure).*?\}", " ", tex, flags=re.S)
    tex = re.sub(r"\\(?:citep|citet|ref|eqref|label|includegraphics)(?:\[[^]]*\])?\{[^}]*\}", " ", tex)
    tex = re.sub(r"\\[A-Za-z@]+\*?(?:\[[^]]*\])?", " ", tex)
    tex = tex.replace("{", " ").replace("}", " ").replace("~", " ")
    return re.findall(r"[A-Za-z]+(?:[-'][A-Za-z]+)*|\d+(?:\.\d+)?", tex)


def count_literal(text: str, phrase: str) -> int:
    return len(re.findall(re.escape(phrase), text, flags=re.I))


def has_explicit_nh4_mapping(tex: str) -> bool:
    """Require the immutable-raw-label correction to be stated, not implied."""
    clean = re.sub(r"\s+", " ", strip_comments(tex))
    return bool(
        re.search(r"NH4Cl.{0,500}NH4Br", clean, flags=re.I)
        or re.search(r"NH4Br.{0,500}NH4Cl", clean, flags=re.I)
    )


def main() -> int:
    main_tex = MAIN.read_text(encoding="utf-8")
    si_tex = SI.read_text(encoding="utf-8")
    clean_main = strip_comments(main_tex)
    lower_main = clean_main.lower()

    title = extract_command(clean_main, "title")
    abstract_match = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", clean_main, flags=re.S)
    abstract = abstract_match.group(1) if abstract_match else ""
    abstract_words = tex_to_words(abstract)
    main_words = tex_to_words(clean_main)

    figure_count = len(re.findall(r"\\begin\{figure\*?\}", clean_main))
    keyword_match = re.search(r"\\textbf\{Keywords:\}\s*(.*?)(?:\n\n|\\section)", clean_main, flags=re.S)
    keyword_text = keyword_match.group(1) if keyword_match else ""
    keyword_count = 0 if not keyword_text else len([x for x in keyword_text.split(";") if x.strip()])

    hard_failures: list[str] = []
    if not abstract_words:
        hard_failures.append("abstract is missing or empty")
    if len(abstract_words) > 200:
        hard_failures.append(f"abstract has {len(abstract_words)} words (>200 JPS limit)")
    if figure_count != 6:
        hard_failures.append(f"active R582 main text has {figure_count} figures (expected exactly 6)")
    if figure_count > 8:
        hard_failures.append(f"main text has {figure_count} figures (>8 JPS limit)")
    if keyword_count != 7:
        hard_failures.append(f"active R582 keyword count is {keyword_count} (expected exactly 7)")
    if keyword_count and not 1 <= keyword_count <= 7:
        hard_failures.append(f"keyword count is {keyword_count} (must be 1-7)")
    if "nh4br" in title.lower() or "nh4cl" in title.lower():
        hard_failures.append("title gives the supporting electrolyte headline status")
    if count_literal(clean_main, "NH4Cl") > 1:
        hard_failures.append("NH4Cl appears more than once in main.tex")
    for phrase in BAN_PHRASES:
        n = count_literal(clean_main, phrase)
        if n:
            hard_failures.append(f"banned phrase '{phrase}' occurs {n} time(s)")
    if "\\usepackage{tgtermes}" not in clean_main:
        hard_failures.append("main_R582.tex does not load the locked tgtermes body font")
    if "\\usepackage{newtxmath}" not in clean_main:
        hard_failures.append("main_R582.tex does not load the locked newtxmath family")
    if "EXP-META-001" not in clean_main or not has_explicit_nh4_mapping(clean_main):
        hard_failures.append("main_R582.tex does not state the explicit NH4Cl-to-NH4Br metadata correction")
    clean_si = strip_comments(si_tex)
    if "\\usepackage{tgtermes}" not in clean_si:
        hard_failures.append("SI_R582.tex does not load the locked tgtermes body font")
    if "\\usepackage{newtxmath}" not in clean_si:
        hard_failures.append("SI_R582.tex does not load the locked newtxmath family")
    if "EXP-META-001" not in clean_si or not has_explicit_nh4_mapping(clean_si):
        hard_failures.append("SI_R582.tex does not state the explicit NH4Cl-to-NH4Br metadata correction")

    sentence_candidates = re.split(r"(?<=[.!?])\s+(?=[A-Z\\])", re.sub(r"\s+", " ", clean_main))
    long_sentences = []
    for sentence in sentence_candidates:
        n_words = len(tex_to_words(sentence))
        if n_words > 35:
            long_sentences.append({"words": n_words, "start": sentence[:180].strip()})

    report = {
        "files": {"main": str(MAIN), "si": str(SI)},
        "journal_gate": {
            "target": "Journal of Power Sources Research Paper",
            "abstract_words": len(abstract_words),
            "approximate_main_words_including_tex_front_back_matter": len(main_words),
            "main_figures": figure_count,
            "keywords": keyword_count,
        },
        "watch_term_counts_main": {term: count_literal(clean_main, term) for term in WATCH_TERMS},
        "nh4_identity_counts": {
            "main_NH4Br": count_literal(clean_main, "NH4Br"),
            "main_NH4Cl": count_literal(clean_main, "NH4Cl"),
            "si_NH4Br": count_literal(si_tex, "NH4Br"),
            "si_NH4Cl": count_literal(si_tex, "NH4Cl"),
        },
        "long_sentences_over_35_words": long_sentences,
        "hard_failures": hard_failures,
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if hard_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
