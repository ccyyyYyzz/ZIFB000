from __future__ import annotations

import importlib.util
import json
import re
import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
R84_SCRIPT = ROOT / "scripts" / "build_SCTS_R84_publication_deep_revision.py"
OUT = ROOT / "outputs" / "SCTS_R85_submission_ordered_revision"
FIG = OUT / "figures"
PDF = OUT / "pdf_proof"
PKG = OUT / "package"

spec = importlib.util.spec_from_file_location("r84", R84_SCRIPT)
r84 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(r84)


SHORT_ABSTRACT = """Zinc-iodine flow batteries offer high aqueous energy density, but neutral iodine can also become a solid foulant in porous positive carbon felt. Here we identify this transition as a local iodine-handling failure. The decisive state is not total iodine inventory in the tank, but whether fiber-scale free-I2 generation exceeds local removal by complexation, diffusion, flow renewal, dissolution and accessible carbon surface. We connect this balance across molecular, fiber and porous-electrode scales. Molecular carbon-surface calculations provide bounded priors for iodine residence near graphitic and functional motifs. A radial single-fiber model converts local precipitation into closures for surface accessibility, iodine-film attenuation, precipitation/dissolution and bare/covered current partition. COMSOL postprocessing then shows that capacity-oriented operation accumulates solid iodine inventory and surface-state loss, whereas rate-oriented operation first produces high free-I2 supersaturation. Spatial fields indicate broad iodine stress, so visible clumps and pressure symptoms are interpreted as localization or pore-throat amplification rather than uniform mean porosity loss. The framework yields testable coordinates for iodine failure: local generation/removal balance, free-I2 supersaturation, cumulative supersaturation dose, solid inventory, surface accessibility and localized blockage risk."""


ORDERED_INTRO = """## 1 Introduction

Redox flow batteries are attractive for long-duration storage because they separate power conversion from tank-scale energy capacity and allow aqueous, serviceable cell architectures [1-3]. Within this broad family, zinc-iodine chemistry is especially attractive because iodine-rich electrolytes can support high energy density while zinc remains inexpensive and abundant. High-energy zinc-polyiodide operation was demonstrated with ambipolar electrolyte chemistry [4]. Subsequent work showed that polyiodide and bromide complexation can unlock iodide capacity [5], that self-healing and single-flow architectures can extend cycle life [6,7], that robust electrolytes and modified carbon electrodes can improve practical operation [8,9], and that high-voltage or dendrite-suppressed Zn-I systems are possible with additional ion-management strategies [10]. Degradation studies further show that excessive charging can produce coupled chemical, electrochemical and transport failure in Zn-I cells [11]. In parallel, porous-electrode optimization, iodine-equilibrium measurements and redox-flow electrode modelling have clarified how electrode structure, compression, active area, transport length and electrolyte speciation affect flow-cell performance [12-18]. More recent complexation and ion-interception strategies continue to improve iodine utilization and cycle life [19,20].

These advances make the Zn-I system technologically compelling, but they also expose a distinctive failure problem. Iodine is not only a soluble redox carrier. During charge it passes through neutral I2, polyiodide and mixed-halide species; it can reside near carbon surfaces; it can cross a free-I2 saturation boundary; and it can form solid deposits that cover fibers, bridge pore throats or enter poorly renewed regions of the felt. Practical observations of dark solid iodine, clumps, flow obstruction, pressure rise and pump-line failure therefore point to a physical conversion of iodine from mobile redox inventory into a local solid/morphology state.

This paper starts from that physical conversion. The central proposition is that iodine failure in a Zn-I flow battery is a local iodine-handling failure of the porous positive carbon felt. The tank can remain chemically buffered while the fiber-scale interface crosses a free-I2 supersaturation boundary. At that interface, current generates neutral iodine at a flux proportional to the local current density. Removal is supplied by complexation, diffusion, flow renewal, dissolution and the still-accessible carbon surface. When the source exceeds the local handling capacity, the relevant state variables are free-I2 supersaturation, cumulative supersaturation dose, solid iodine inventory, surface accessibility, film attenuation and localization.

This framing is deliberately different from three simpler explanations. It is not a purely global electrolyte-depletion story, because total iodide or bromide inventory can remain large while local free iodine exceeds saturation. It is not a single film-resistance story, because coverage, film attenuation, precipitation/dissolution and bare/covered current split are distinct physical links. It is also not a generic porous-electrode voltage-fitting story, because full-cell voltage mixes open-circuit potential, zinc-side polarization, membrane/electrolyte resistance, terminal concentration polarization and positive-electrode iodine loss. A useful mechanism must therefore follow iodine from molecular residence to fiber-scale precipitation, porous-electrode fields and morphology-scale blockage.

Carbon felt amplifies the importance of locality. Compression, permeability, tortuosity, wetting, active area and flow distribution determine where reaction occurs and how quickly species are renewed. In a Zn-I positive felt these structural variables also determine where neutral iodine first forms, how long it remains near carbon, where solid iodine can nucleate, and whether a small mean solid fraction becomes harmlessly distributed or dangerously localized. This is why a continuum field and a visible clump should not be treated as contradictory: they describe different levels of the same chain.

We build the mechanism with three connected modelling levels and one interpretation layer. First, molecular surface calculations test whether iodine residence near representative carbon motifs is chemically plausible. These calculations are used only as bounded surface priors, not as fitted macroscopic kinetic constants. Second, a standalone single-fiber model resolves radial transport, fast complexation, surface generation/consumption, precipitation/dissolution, coverage and local film attenuation. This model exports closures rather than replacing the porous-electrode model with a black-box voltage term. Third, COMSOL porous-electrode postprocessing maps the local state variables under capacity- and rate-oriented operation. Finally, mean-field versus localized-blockage analysis explains why hydraulic symptoms require morphology amplification beyond a uniform mean porosity loss.

The contribution is a mechanism framework rather than an optimization recipe. It identifies where each parameter family enters the iodine-failure chain: accessible carbon area changes the local source term, flow and diffusivity change removal, speciation and saturation move the free-I2 gate, precipitation and dissolution control solid inventory and recovery, compression and localization control hydraulic amplification, and ASR controls voltage loss without necessarily changing iodine phase stability. This chain provides a cleaner basis for experiments and design decisions than a single empirical failure threshold.
"""


def patched_manuscript() -> str:
    md = r84.manuscript_text()
    md = re.sub(r"## Abstract\n\n.*?\n\n\*\*Keywords:", "## Abstract\n\n" + SHORT_ABSTRACT + "\n\n**Keywords:", md, flags=re.S)
    md = re.sub(r"## 1 Introduction\n\n.*?\n\n!\[Fig1_R67_local_iodine_failure_framework.png\]", ORDERED_INTRO + "\n![Fig1_R67_local_iodine_failure_framework.png]", md, flags=re.S)
    return md


def cover_letter() -> str:
    return f"""# Cover letter draft for Science China Technological Sciences

Dear Editors,

We are pleased to submit the invited manuscript entitled "{r84.TITLE}" for consideration in *Science China Technological Sciences*.

**Research background.** Zinc-iodine flow batteries are promising aqueous energy-storage systems because iodine-rich electrolytes can provide high charge density while zinc and flow-cell hardware remain comparatively low cost. A persistent technological obstacle is that neutral iodine can transform from soluble redox inventory into solid deposits, clumps, pore blockage and hydraulic/electrochemical instability in the porous positive carbon felt.

**Innovation.** The manuscript reframes this problem as a local iodine-handling failure. Instead of treating the failure as a bulk iodine-inventory limit, an empirical voltage residual or a single film-resistance term, we connect molecular carbon-surface priors, a radial single-fiber precipitation/coverage model and COMSOL porous-electrode state fields into one source-removal-supersaturation-solid-blockage chain. The analysis separates capacity-driven cumulative solid inventory from rate-driven free-I2 generation/removal imbalance and explains why pressure symptoms require localization or pore-throat amplification beyond uniform mean porosity loss.

**Significance.** The work provides experimentally testable coordinates for Zn-I failure: local generation/removal balance, free-I2 supersaturation, cumulative supersaturation dose, solid iodine inventory, closure-derived surface accessibility and localization-driven hydraulic risk. These coordinates can guide phase identification, pressure tracing, interrupted-charge imaging, reference-electrode studies and future porous-electrode/clump models.

The manuscript is intended as a mechanism-oriented Article for the technological-sciences readership. It does not claim an optimized additive recipe, a production operating map, direct measured surface coverage or a quantified pressure cutoff. These boundaries are stated explicitly so that the mechanistic claims remain falsifiable and useful.

Sincerely,

[Corresponding author name]

[Affiliation]

[Email]
"""


def compliance_note() -> str:
    return """# R85 SCTS compliance and submission note

Public author guidance checked:

- Springer submission guidelines: https://link.springer.com/journal/11431/submission-guidelines
- Science China author center: https://www.sciengine.com/SCTS/authorCenter?scroll=section_1
- Instructions for Authors PDF: https://media.springer.com/full/springer-instructions-for-authors-assets/pdf/11431_SCTS%20Instructions%20for%20authors-20230608.pdf

R85 corrections relative to R84:

- Abstract shortened to a compact purpose-method-result-conclusion form and contains no citations, equations or figure references.
- Introduction now starts from broad redox-flow context and introduces references in numerical order.
- Cover letter now explicitly states research background, innovation and significance, matching the SCTS author-instruction emphasis.
- Main text retains five numbered figures cited in order.
- Claim boundaries are retained: no direct surface-coverage measurement, no numerical pressure cutoff, no additive optimization and no production operating map.
"""


def citation_order_audit(md: str) -> dict[str, object]:
    seen: list[int] = []
    for m in re.finditer(r"\[([0-9,\-\s]+)\]", md):
        token = m.group(1)
        vals: list[int] = []
        for part in token.replace(" ", "").split(","):
            if not part:
                continue
            if "-" in part:
                a, b = part.split("-", 1)
                if a.isdigit() and b.isdigit():
                    vals.extend(range(int(a), int(b) + 1))
            elif part.isdigit():
                vals.append(int(part))
        for v in vals:
            if v not in seen:
                seen.append(v)
    expected = list(range(1, 21))
    return {
        "first_appearance_order": seen,
        "expected_1_to_20": expected,
        "is_ordered_prefix": seen[:20] == expected,
        "missing": [x for x in expected if x not in seen],
    }


def ensure_dirs() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    for p in [OUT, FIG, PDF, PKG]:
        p.mkdir(parents=True, exist_ok=True)


def write_files() -> None:
    (OUT / "SCTS_ZIFB_submission_ordered_revision_R85.md").write_text(patched_manuscript(), encoding="utf-8")
    (OUT / "Supporting_Information_R85.md").write_text(r84.si_text(), encoding="utf-8")
    (OUT / "separate_figure_captions_R85.md").write_text(r84.figure_captions(), encoding="utf-8")
    (OUT / "cover_letter_SCTS_invited_R85.md").write_text(cover_letter(), encoding="utf-8")
    (OUT / "highlights_R85.md").write_text(r84.highlights(), encoding="utf-8")
    (OUT / "R85_SCTS_compliance_note.md").write_text(compliance_note(), encoding="utf-8")
    (OUT / "R85_figure_interpretation_ledger.md").write_text(r84.figure_interpretation_ledger(), encoding="utf-8")
    (OUT / "GPT_PRO_REVIEW_PROMPT_R85_CN.md").write_text(r84.gpt_prompt_cn(), encoding="utf-8")
    (OUT / "R85_author_fill_in_sheet.md").write_text(
        """# Author fill-in sheet before SCTS upload

- Full author list:
- Affiliations:
- Corresponding author:
- Email:
- ORCID IDs if required:
- Equal contribution statement if any:
- Funding:
- Acknowledgements:
- Conflict of interest statement:
- Data/code availability final wording:
- Article type confirmed with invited editor:
- Reference-manager check completed:
- Final PDF proof checked page by page:
""",
        encoding="utf-8",
    )


def audits(checks: dict[str, object], pdf_checks: dict[str, object]) -> dict[str, object]:
    md = (OUT / "SCTS_ZIFB_submission_ordered_revision_R85.md").read_text(encoding="utf-8")
    body = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", md)
    forbidden = [
        "workflow",
        "dashboard",
        "EIS proves",
        "EIS disproves",
        "validated operating map",
        "optimized NH4Br",
        "measured coverage",
        "exact pressure threshold",
        "full-cell proves",
        "Q*/i* fitted",
        "parameter-free",
        "production design claim",
        "550C best",
    ]
    abstract = re.search(r"## Abstract\n\n(.*?)\n\n\*\*Keywords:", md, re.S).group(1)
    citation_audit = citation_order_audit(md)
    q = {
        "word_count_rough": len(re.findall(r"[A-Za-z0-9_+./-]+", body)),
        "abstract_words": len(re.findall(r"[A-Za-z0-9_+./-]+", abstract)),
        "references": len(re.findall(r"^\[\d+\]", md, re.M)),
        "main_figures": len(re.findall(r"!\[Fig", md)),
        "forbidden_counts": {pat: len(re.findall(re.escape(pat), md, re.I)) for pat in forbidden},
        "citation_order": citation_audit,
        "docx": checks,
        "pdf": pdf_checks,
    }
    (OUT / "R85_QA_summary.json").write_text(json.dumps(q, indent=2), encoding="utf-8")
    clean_forbidden = all(v == 0 for v in q["forbidden_counts"].values())
    no_blank = not pdf_checks["manuscript"]["blank_pages"] and not pdf_checks["supporting_information"]["blank_pages"]
    status = "PASS" if clean_forbidden and no_blank and citation_audit["is_ordered_prefix"] else "PARTIAL"
    (OUT / "R85_submission_revision_audit.md").write_text(
        f"""# R85 submission ordered revision audit

## Corrections beyond R84

- Shortened abstract to {q['abstract_words']} words.
- Rewrote the Introduction so citations first appear in numerical order.
- Added SCTS compliance note based on the official author instructions.
- Strengthened cover letter around research background, innovation and significance.
- Preserved R84's deeper parameter-by-parameter reasoning and multiscale evidence chain.

## Structural QA

- Rough word count: {q['word_count_rough']}
- Main figures: {q['main_figures']}
- References: {q['references']}
- Manuscript PDF pages: {pdf_checks['manuscript']['pages']}
- SI PDF pages: {pdf_checks['supporting_information']['pages']}
- Blank pages: {'NO' if no_blank else 'YES'}
- Citation first-appearance order: {citation_audit['first_appearance_order'][:25]}
- Citation order 1-20: {'PASS' if citation_audit['is_ordered_prefix'] else 'FAIL'}

## Forbidden wording scan

""" + "\n".join(f"- {k}: {v}" for k, v in q["forbidden_counts"].items()) + "\n",
        encoding="utf-8",
    )
    (OUT / "final_status.md").write_text(
        f"""SCTS R85 submission ordered revision: {status}
Manuscript Markdown: SCTS_ZIFB_submission_ordered_revision_R85.md
Manuscript DOCX: SCTS_ZIFB_submission_ordered_revision_R85.docx
Manuscript PDF proof: pdf_proof/SCTS_ZIFB_submission_ordered_revision_R85.pdf
Supporting Information DOCX: Supporting_Information_R85.docx
Supporting Information PDF proof: pdf_proof/Supporting_Information_R85.pdf
Abstract words: {q['abstract_words']}
Rough word count: {q['word_count_rough']}
Main figures: {q['main_figures']}
References: {q['references']}
Citation order check: {'PASS' if citation_audit['is_ordered_prefix'] else 'FAIL'}
Parameter-by-parameter reasoning retained: YES
Molecular modelling integrated: YES
Single-fiber closure integrated: YES
COMSOL time-evolution interpretation retained: YES
PDF visual proof generated: YES
Manuscript PDF pages: {pdf_checks['manuscript']['pages']}
SI PDF pages: {pdf_checks['supporting_information']['pages']}
Blank pages detected: {'NO' if no_blank else 'YES'}
Ready for GPT Pro/coauthor scientific review: YES
Ready for senior-author line editing: YES
Ready for direct one-click SCTS upload: NO
Reason: author metadata, funding, reference-manager verification and final human proof are still required.
""",
        encoding="utf-8",
    )
    return q


def package_outputs() -> None:
    full = PKG / "SCTS_R85_SUBMISSION_ORDERED_REVISION_FULL.zip"
    gpt = PKG / "GPT_PRO_REVIEW_PACKET_R85_SUBMISSION_ORDERED_REVISION.zip"
    with zipfile.ZipFile(full, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(OUT.rglob("*")):
            if p.is_file() and "package" not in p.relative_to(OUT).parts:
                zf.write(p, str(p.relative_to(OUT)).replace("\\", "/"))
    wanted = [
        "SCTS_ZIFB_submission_ordered_revision_R85.md",
        "SCTS_ZIFB_submission_ordered_revision_R85.docx",
        "Supporting_Information_R85.md",
        "Supporting_Information_R85.docx",
        "pdf_proof/SCTS_ZIFB_submission_ordered_revision_R85.pdf",
        "pdf_proof/Supporting_Information_R85.pdf",
        "pdf_proof/manuscript_contact_sheet_R85.png",
        "pdf_proof/supporting_information_contact_sheet_R85.png",
        "separate_figure_captions_R85.md",
        "cover_letter_SCTS_invited_R85.md",
        "R85_SCTS_compliance_note.md",
        "R85_submission_revision_audit.md",
        "R85_QA_summary.json",
        "GPT_PRO_REVIEW_PROMPT_R85_CN.md",
        "final_status.md",
    ]
    with zipfile.ZipFile(gpt, "w", zipfile.ZIP_DEFLATED) as zf:
        for rel in wanted:
            p = OUT / rel
            if p.exists():
                zf.write(p, rel.replace("\\", "/"))
        for p in sorted(FIG.glob("*.png")):
            zf.write(p, f"figures/{p.name}")


def main() -> None:
    ensure_dirs()
    # Repoint the R84 helper module to the R85 directories.
    r84.OUT = OUT
    r84.FIG = FIG
    r84.PDF = PDF
    r84.PKG = PKG
    r84.copy_figures()
    write_files()
    checks = {
        "manuscript": r84.markdown_to_docx(OUT / "SCTS_ZIFB_submission_ordered_revision_R85.md", OUT / "SCTS_ZIFB_submission_ordered_revision_R85.docx", r84.MAIN_FIGS),
        "supporting_information": r84.markdown_to_docx(OUT / "Supporting_Information_R85.md", OUT / "Supporting_Information_R85.docx", r84.SI_FIGS),
    }
    r84.export_pdf(OUT / "SCTS_ZIFB_submission_ordered_revision_R85.docx", PDF / "SCTS_ZIFB_submission_ordered_revision_R85.pdf")
    r84.export_pdf(OUT / "Supporting_Information_R85.docx", PDF / "Supporting_Information_R85.pdf")
    pdf_checks = {
        "manuscript": r84.pdf_qa(PDF / "SCTS_ZIFB_submission_ordered_revision_R85.pdf", "manuscript"),
        "supporting_information": r84.pdf_qa(PDF / "Supporting_Information_R85.pdf", "supporting_information"),
    }
    for old, new in [
        (PDF / "manuscript_contact_sheet_R84.png", PDF / "manuscript_contact_sheet_R85.png"),
        (PDF / "supporting_information_contact_sheet_R84.png", PDF / "supporting_information_contact_sheet_R85.png"),
    ]:
        if old.exists():
            old.replace(new)
    q = audits(checks, pdf_checks)
    package_outputs()
    print((OUT / "final_status.md").read_text(encoding="utf-8"))
    print(json.dumps({"out": str(OUT), "qa": q}, indent=2))


if __name__ == "__main__":
    main()
