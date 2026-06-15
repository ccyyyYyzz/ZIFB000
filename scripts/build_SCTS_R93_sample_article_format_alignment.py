from __future__ import annotations

import importlib.util
import json
import re
import shutil
import zipfile
from pathlib import Path

import pdfplumber


ROOT = Path(__file__).resolve().parents[1]
R92 = ROOT / "outputs" / "SCTS_R92_scts_format_compliance"
OUT = ROOT / "outputs" / "SCTS_R93_sample_article_format_alignment"
FIG = OUT / "figures"
FIG600 = OUT / "submission_figures_600dpi"
PDF = OUT / "pdf_proof"
PKG = OUT / "package"
SAMPLE = OUT / "sample_SCTS_article_s11431-025-3268-3.pdf"

R92_SCRIPT = ROOT / "scripts" / "build_SCTS_R92_scts_format_compliance.py"
spec = importlib.util.spec_from_file_location("r92", R92_SCRIPT)
r92 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(r92)
r84 = r92.r84


MAIN_FIGS_R93 = [
    "Fig1_R67_local_iodine_failure_framework.png",
    "SI_Fig_molecular_surface_evidence_R64.png",
    "Fig2_single_fiber_closure_bridge_R64.png",
    "Fig3_R69_COMSOL_state_evolution.png",
    "Fig4_COMSOL_axis_profile_fields_R64.png",
    "Fig5_R67_parameter_mechanism_matrix.png",
]

SI_FIGS_R93 = [
    "SI_Fig_true_COMSOL_cloudmaps_R64.png",
    "SI_Fig_precipitation_dissolution_boundary_R64.png",
    "SI_dense_Fig3_CAP_RATE_time_evolution_R64.png",
    "SI_dense_Fig5_parameter_family_curves_R64.png",
    "SI_dense_Fig6_parameter_fingerprint_R64.png",
    "Fig6_R67_evidence_boundary_falsification.png",
]


def ensure_dirs() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    for path in [OUT, FIG, FIG600, PDF, PKG]:
        path.mkdir(parents=True, exist_ok=True)


def copy_inputs() -> None:
    for src_dir, dst_dir in [(R92 / "figures", FIG), (R92 / "submission_figures_600dpi", FIG600)]:
        for p in src_dir.glob("*"):
            if p.is_file():
                shutil.copy2(p, dst_dir / p.name)
    downloads_pdf = Path.home() / "Downloads" / "s11431-025-3268-3.pdf"
    already_copied = ROOT / "outputs" / "SCTS_R93_sample_article_format_benchmark" / "sample_SCTS_article_s11431-025-3268-3.pdf"
    if downloads_pdf.exists():
        shutil.copy2(downloads_pdf, SAMPLE)
    elif already_copied.exists():
        shutil.copy2(already_copied, SAMPLE)


def extract_sample_text() -> dict[str, object]:
    if not SAMPLE.exists():
        return {"sample_found": False}
    full_parts: list[str] = []
    meta: dict[str, object] = {"sample_found": True, "pages": 0, "page_sizes": []}
    with pdfplumber.open(SAMPLE) as doc:
        meta["pages"] = len(doc.pages)
        for i, page in enumerate(doc.pages, start=1):
            meta["page_sizes"].append({"page": i, "width_pt": page.width, "height_pt": page.height})
            full_parts.append(page.extract_text(x_tolerance=2, y_tolerance=3) or "")
    full = "\n".join(full_parts)
    (OUT / "sample_article_full_text_extracted.txt").write_text(full, encoding="utf-8")
    headings = []
    for line in full.splitlines():
        s = line.strip()
        if re.match(r"^(Abstract|Keywords|Citation|[1-9]\s+[A-Z]|Acknowledgements|References)", s):
            headings.append(s)
    meta["detected_headings"] = headings[:80]
    fig_count = len(re.findall(r"\bFigure\s+\d+|\bFig\.\s*\d+", full))
    meta["approx_figure_mentions"] = fig_count
    return meta


def write_sample_analysis(meta: dict[str, object]) -> None:
    found = "YES" if meta.get("sample_found") else "NO"
    pages = meta.get("pages", "not available")
    headings = "\n".join(f"- {h}" for h in meta.get("detected_headings", [])[:20])
    (OUT / "SCTS_sample_article_format_lessons_R93.md").write_text(
        f"""# SCTS sample-article format lessons used in R93

Sample article provided by the user: `s11431-025-3268-3.pdf`

Sample found: {found}
Sample pages: {pages}

## What is directly transferable

The sample is a final typeset SCTS article, so its two-column layout, running
headers, article number, received/accepted dates and DOI line should not be
manually copied into a submission manuscript. Those elements are production
typesetting.

The transferable lessons are structural and rhetorical:

1. The paper opens with a compact title, author block, single-paragraph abstract,
   keywords and a citation line.
2. The main text proceeds linearly from problem framing to method, validation,
   application and discussion/conclusion.
3. Figures are not decorative; each figure advances the argument and is discussed
   immediately in the surrounding text.
4. Captions are explanatory, not merely file labels.
5. The last section summarizes what the method explains, what remains limited
   and why the approach is useful.

## R93 changes made from R92

1. Added an explicit `Article type: Research Paper` line near the title block.
2. Moved the molecular surface-prior figure from SI into the main manuscript as
   Figure 2, because the paper claims a multiscale chain beginning at molecular
   iodine residence.
3. Renumbered the main figure sequence so the argument now reads:
   Figure 1 mechanism overview; Figure 2 molecular surface prior; Figure 3
   single-fiber closure; Figure 4 time-resolved porous-electrode state evolution;
   Figure 5 spatial/localization fields; Figure 6 parameter-family mechanism map.
4. Kept the SCTS submission format from R92: A4, 10 pt text and 1.5 line spacing.
5. Did not mimic the published two-column layout, because that is not the
   requested submission format in the author instructions.

## Detected sample headings

{headings}
""",
        encoding="utf-8",
    )


def renumber_existing_figures(md: str) -> str:
    for old, new in [(5, 6), (4, 5), (3, 4), (2, 3)]:
        md = re.sub(rf"\bFigure {old}\b", f"Figure {new}", md)
        md = re.sub(rf"\*\*Figure {old}\.", f"**Figure {new}.", md)
        md = re.sub(rf"\bFig\. {old}\b", f"Fig. {new}", md)
    return md


def build_manuscript_markdown() -> str:
    md = (R92 / "SCTS_ZIFB_SCTS_format_R92.md").read_text(encoding="utf-8")
    md = md.replace(
        "\n**Authors:** [Author names]",
        "\n**Article type:** Research Paper\n\n**Authors:** [Author names]",
        1,
    )
    md = renumber_existing_figures(md)
    insert = """
![SI_Fig_molecular_surface_evidence_R64.png](figures/SI_Fig_molecular_surface_evidence_R64.png)

**Figure 2. Molecular surface prior for iodine residence on carbon motifs.** Finite graphitic and oxygenated carbon motifs are used only to bound the plausibility and relative strength of local I2 residence. The molecular layer supports patchy residence and nucleation as chemically reasonable, but it is not used to fit full-cell voltage, precipitation rate constants, film conductivity or pore-blockage thresholds.
"""
    md = md.replace("\n### 2.3 The single-fiber model", insert + "\n### 2.3 The single-fiber model", 1)
    md = md.replace(
        "The first modelling level asks whether iodine has a plausible tendency to reside near carbon surfaces.",
        "The first modelling level asks whether iodine has a plausible tendency to reside near carbon surfaces (Figure 2).",
        1,
    )
    md = md.replace(
        "The important conclusion is not that one functional group uniquely controls the battery.",
        "The important conclusion from Figure 2 is not that one functional group uniquely controls the battery.",
        1,
    )
    md = md.replace(
        "The closure scan contains 720 single-fiber rows.",
        "The closure scan contains 720 single-fiber rows and is summarized in Figure 3.",
        1,
    )
    return md


def build_si_markdown() -> str:
    si = (R92 / "Supporting_Information_R92.md").read_text(encoding="utf-8")
    si = si.replace("## S1 Molecular surface evidence", "## S1 Expanded molecular surface-note boundary")
    si = si.replace(
        "![SI_Fig_molecular_surface_evidence_R64.png](figures/SI_Fig_molecular_surface_evidence_R64.png)\n\n",
        "",
        1,
    )
    si = si.replace(
        "The molecular calculations are retained as bounded surface priors.",
        "The molecular calculations are shown in the main text as Figure 2 and retained here as a boundary statement. They are retained as bounded surface priors.",
        1,
    )
    return si


def audit_text(md: str, docx_format: dict[str, object], pdf_checks: dict[str, object], docx_checks: dict[str, object], sample_meta: dict[str, object]) -> dict[str, object]:
    audit = r92.audit_text(md)
    audit["docx_format"] = docx_format
    audit["pdf"] = pdf_checks
    audit["docx"] = docx_checks
    audit["sample_article"] = sample_meta
    audit["main_figure_count"] = len(re.findall(r"^\*\*Figure\s+\d+\.", md, re.M))
    audit["has_molecular_main_figure"] = "Figure 2. Molecular surface prior" in md
    return audit


def write_r93_reports(audit: dict[str, object]) -> None:
    (OUT / "R93_changes_from_R92.md").write_text(
        f"""# R93 changes from R92

R93 is a sample-article format-alignment revision based on the SCTS paper
provided by the user. It does not replace the journal's author instructions;
instead, it uses the sample article to improve manuscript flow and figure logic.

Main changes:

1. Added Article type: Research Paper near the title block.
2. Promoted molecular surface evidence from SI to main Figure 2.
3. Renumbered the main figure chain to six figures.
4. Removed the duplicate molecular image from SI and kept a boundary note.
5. Kept R92 SCTS submission geometry: A4, 10 pt, 1.5 line spacing.
6. Preserved all claim boundaries: no NH4Br optimization, no production design
   claim, no measured coverage claim and no exact pressure-threshold claim.

QA summary:

- Title words: {audit['title_words']} / 20
- Abstract words: {audit['abstract_words']}
- Keywords: {audit['keyword_count']}
- References: {audit['references']}
- Main figures: {audit['main_figure_count']}
- Molecular main figure present: {audit['has_molecular_main_figure']}
- Citation order pass: {audit['citation_order']['is_ordered_prefix']}
""",
        encoding="utf-8",
    )
    (OUT / "GPT_PRO_REVIEW_PROMPT_R93_CN.md").write_text(
        """# 给 GPT Pro / 合作者的 R93 审稿提示

请按照 Science China Technological Sciences 的 Research Paper 风格审稿。

本版 R93 已参考用户提供的 SCTS 样文，不是复制最终两栏排版，而是吸收其论文组织方式：

1. 主文现在按 Figure 1-6 建立机制链：总览 -> 分子表面先验 -> 单纤维闭合 -> 时间演化 -> 空间/局部化 -> 参数家族。
2. 请重点判断这个图链是否像一篇论文，而不是模型报告。
3. 请逐段检查 Results 是否每段都有明确问题、图中证据、物理解释和限制。
4. 请检查 Discussion 是否把分子模拟、单纤维模型、COMSOL、局部化堵塞和参数影响收束到一个中心 thesis。
5. 请特别找过度承诺：NH4Br optimization、production design、measured coverage、exact pressure threshold、old EIS proof、full-cell validation。
6. 如果你认为还不像 SCTS 文章，请指出应该合并/移动/删除的具体段落和图。
""",
        encoding="utf-8",
    )


def package_outputs() -> list[dict[str, object]]:
    full = PKG / "SCTS_R93_SAMPLE_FORMAT_ALIGNMENT_FULL.zip"
    gpt = PKG / "GPT_PRO_REVIEW_PACKET_R93_SAMPLE_FORMAT.zip"
    figs = PKG / "SCTS_R93_FIGURES_NATIVE_600DPI.zip"
    with zipfile.ZipFile(figs, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(FIG600.glob("*.png")):
            zf.write(p, p.name)
    with zipfile.ZipFile(full, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(OUT.rglob("*")):
            if p.is_file() and "package" not in p.relative_to(OUT).parts:
                zf.write(p, str(p.relative_to(OUT)).replace("\\", "/"))
    wanted = [
        "SCTS_ZIFB_sample_format_aligned_R93.md",
        "SCTS_ZIFB_sample_format_aligned_R93.docx",
        "pdf_proof/SCTS_ZIFB_sample_format_aligned_R93.pdf",
        "Supporting_Information_R93.md",
        "Supporting_Information_R93.docx",
        "pdf_proof/Supporting_Information_R93.pdf",
        "pdf_proof/manuscript_contact_sheet_R93.png",
        "pdf_proof/supporting_information_contact_sheet_R93.png",
        "SCTS_sample_article_format_lessons_R93.md",
        "R93_changes_from_R92.md",
        "GPT_PRO_REVIEW_PROMPT_R93_CN.md",
        "R93_QA_summary.json",
        "final_status.md",
    ]
    with zipfile.ZipFile(gpt, "w", zipfile.ZIP_DEFLATED) as zf:
        for rel in wanted:
            p = OUT / rel
            if p.exists():
                zf.write(p, rel.replace("\\", "/"))
        if SAMPLE.exists():
            zf.write(SAMPLE, SAMPLE.name)
        for p in sorted(FIG600.glob("*.png")):
            zf.write(p, f"submission_figures_600dpi/{p.name}")
    checks = []
    for p in [full, gpt, figs]:
        with zipfile.ZipFile(p) as zf:
            checks.append({"file": p.name, "entries": len(zf.namelist()), "testzip_bad": zf.testzip()})
    return checks


def main() -> None:
    ensure_dirs()
    copy_inputs()
    sample_meta = extract_sample_text()
    write_sample_analysis(sample_meta)

    md = build_manuscript_markdown()
    si = build_si_markdown()
    (OUT / "SCTS_ZIFB_sample_format_aligned_R93.md").write_text(md, encoding="utf-8")
    (OUT / "Supporting_Information_R93.md").write_text(si, encoding="utf-8")

    r84.OUT = OUT
    r84.FIG = FIG
    r84.PDF = PDF
    r84.PKG = PKG
    docx_checks = {
        "manuscript": r84.markdown_to_docx(
            OUT / "SCTS_ZIFB_sample_format_aligned_R93.md",
            OUT / "SCTS_ZIFB_sample_format_aligned_R93.docx",
            MAIN_FIGS_R93,
        ),
        "supporting_information": r84.markdown_to_docx(
            OUT / "Supporting_Information_R93.md",
            OUT / "Supporting_Information_R93.docx",
            SI_FIGS_R93,
        ),
    }
    docx_format = r92.set_scts_docx_format(OUT / "SCTS_ZIFB_sample_format_aligned_R93.docx")
    r92.set_scts_docx_format(OUT / "Supporting_Information_R93.docx")
    r84.export_pdf(OUT / "SCTS_ZIFB_sample_format_aligned_R93.docx", PDF / "SCTS_ZIFB_sample_format_aligned_R93.pdf")
    r84.export_pdf(OUT / "Supporting_Information_R93.docx", PDF / "Supporting_Information_R93.pdf")
    pdf_checks = {
        "manuscript": r84.pdf_qa(PDF / "SCTS_ZIFB_sample_format_aligned_R93.pdf", "manuscript"),
        "supporting_information": r84.pdf_qa(PDF / "Supporting_Information_R93.pdf", "supporting_information"),
    }
    for old, new in [
        (PDF / "manuscript_contact_sheet_R84.png", PDF / "manuscript_contact_sheet_R93.png"),
        (PDF / "supporting_information_contact_sheet_R84.png", PDF / "supporting_information_contact_sheet_R93.png"),
    ]:
        if old.exists():
            old.replace(new)
    audit = audit_text(md, docx_format, pdf_checks, docx_checks, sample_meta)
    (OUT / "R93_QA_summary.json").write_text(json.dumps(audit, indent=2, ensure_ascii=False), encoding="utf-8")
    write_r93_reports(audit)
    zip_checks = package_outputs()
    (OUT / "R93_zip_integrity_check.json").write_text(json.dumps(zip_checks, indent=2), encoding="utf-8")
    no_blank = not pdf_checks["manuscript"]["blank_pages"] and not pdf_checks["supporting_information"]["blank_pages"]
    clean_forbidden = all(v == 0 for v in audit["forbidden_counts"].values())
    status = "PASS" if no_blank and clean_forbidden and audit["has_molecular_main_figure"] else "PARTIAL"
    (OUT / "final_status.md").write_text(
        f"""SCTS R93 sample-article format alignment: {status}
Sample article analyzed: {'YES' if sample_meta.get('sample_found') else 'NO'}
Manuscript Markdown: SCTS_ZIFB_sample_format_aligned_R93.md
Manuscript DOCX: SCTS_ZIFB_sample_format_aligned_R93.docx
Manuscript PDF proof: pdf_proof/SCTS_ZIFB_sample_format_aligned_R93.pdf
Supporting Information DOCX: Supporting_Information_R93.docx
Supporting Information PDF proof: pdf_proof/Supporting_Information_R93.pdf
GPT review zip: package/GPT_PRO_REVIEW_PACKET_R93_SAMPLE_FORMAT.zip
Full submission zip: package/SCTS_R93_SAMPLE_FORMAT_ALIGNMENT_FULL.zip
Figures zip: package/SCTS_R93_FIGURES_NATIVE_600DPI.zip
Title words: {audit['title_words']} / 20
Abstract words: {audit['abstract_words']}
Keywords: {audit['keyword_count']}
References: {audit['references']}
Main figures: {audit['main_figure_count']}
Molecular evidence promoted to main Figure 2: {'YES' if audit['has_molecular_main_figure'] else 'NO'}
Citation order check: {'PASS' if audit['citation_order']['is_ordered_prefix'] else 'FAIL'}
A4/10pt/1.5 spacing: {docx_format}
Manuscript PDF pages: {pdf_checks['manuscript']['pages']}
SI PDF pages: {pdf_checks['supporting_information']['pages']}
Blank pages detected: {'NO' if no_blank else 'YES'}
Forbidden wording scan: {'PASS' if clean_forbidden else 'CHECK'}
Ready for GPT Pro/coauthor scientific review: YES
Ready for senior-author line editing: YES
Ready for direct one-click SCTS upload: NO
Reason direct upload is still blocked: author names, affiliations, corresponding-author email, funding, author contributions, conflict-of-interest confirmation and final human proof must be completed by the authors.
""",
        encoding="utf-8",
    )
    print((OUT / "final_status.md").read_text(encoding="utf-8"))
    print(json.dumps({"zip_checks": zip_checks, "out": str(OUT)}, indent=2))


if __name__ == "__main__":
    main()
