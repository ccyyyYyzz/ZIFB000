# R582 readability and visual-rebuild audit packet

This packet mirrors the live R581 manuscript only for adversarial editorial and
visual review. It does not replace the repository's main-branch archive. The
R582 branch will remain an audit branch until the redesigned manuscript passes
scientific, visual, citation, compilation and cold-build checks.

## Scientific boundaries

- The paper concerns the porous ZIFB positive electrode and local iodine
  handling during charge.
- NH4Br is a representative supporting electrolyte. Bromide is a supporting
  ligand/speciation participant, not the central result.
- Legacy experiment labels containing `NH4Cl` or `NH4CL` refer to NH4Br. Raw
  names and bytes remain unchanged; analysis records the correction as
  `EXP-META-001`.
- No new physical experiments are available. Evidence gaps may be addressed
  with literature anchors, new simulations or re-analysis of existing data.
- Original experiment files and original COMSOL `.mph` files are immutable and
  are not included here.
- Continuum fields are model outputs. They are not microscopy, reconstructed
  deposit morphology or evidence of a physical blocking front.
- Manuscript body and figure text use one family: TeX Gyre Termes with
  NewTX/Termes-compatible mathematics. Arial, Helvetica, DejaVu Sans and other
  figure-font substitutions fail the R582 release gate.

## Start here

1. Read `main_R581.pdf` at actual page width.
2. Inspect every PNG in `figures/`; do not judge only the standalone pixel size.
3. Compare main Fig. 3/4 with `figures/Fig_R545_spatial_maps.png`, which contains
   the Q = 80/100/120 mAh cm-2 two-dimensional fields currently buried in SI.
4. Read `audits/LANGUAGE_ARCHITECTURE_AUDIT.md` for the reverse outline,
   terminology ledger and direct rewrite examples.
5. Record decisions in GitHub issue #1.

## Accepted R582 figure candidates

These are live, source-backed candidates rather than frozen publication files.
Review their 180 mm PNG/PDF renders, captions, contracts and QA records together:

1. [`prototypes/Fig1_experimental_problem/`](prototypes/Fig1_experimental_problem/)
   — full-cell observations with an explicit positive-electrode focus.
2. [`prototypes/Fig2_domain_state_v2/`](prototypes/Fig2_domain_state_v2/)
   — domain and state relation without a decorative morphology cartoon.
3. [`prototypes/Fig3_spatial_v3/`](prototypes/Fig3_spatial_v3/)
   — the 80/100/120 mAh cm$^{-2}$ spatial hero, now using the exported native
   remaining-area field and a compact through-plane mean. The v2 directory is
   retained only as superseded provenance.
4. [`prototypes/Fig4_closure_identifiability/`](prototypes/Fig4_closure_identifiability/)
   — matched model-form sensitivity and accessibility non-identifiability.
5. [`prototypes/Fig5_positive_electrode_bounds_v2/`](prototypes/Fig5_positive_electrode_bounds_v2/)
   — quiet DFT/MD priors above the dominant accessibility and permeability
   bounds for the positive electrode.
6. [`prototypes/Fig6_operating_levers_v2/`](prototypes/Fig6_operating_levers_v2/)
   — solved current/diffusivity responses and one full-width quantitative lever
   comparison; the 80 mA cm$^{-2}$ case is explicitly right-censored.

The current six-figure scientific narrative is in
[`text/R582_MAIN_TEXT_DRAFT.md`](text/R582_MAIN_TEXT_DRAFT.md). All six
candidates have passed individual font, evidence, grayscale, source-data and
deterministic-build checks; whole-manuscript placement remains under review.

## Current visual diagnosis

The evidence hierarchy is reversed. Main Fig. 3 is a multi-scale geometry
collage, while the direct spatial evidence appears as SI Fig. S8. R582 will test
a new Figure 3 led by multi-capacity two-dimensional positive-electrode maps.
The geometry will be reduced to an orientation strip, and the full x-Q inventory
will move to SI.

## Authority hashes

| File | SHA-256 |
|---|---|
| `main_R581.tex` | `76F1FADF57003A261F22C977DC69BB7951B9C26820AAA79BC89B952494DDDB2C` |
| `SI_R581.tex` | `CC5906F04E660DCE8458542EB47FFDE4431C6A3F968628873A85F31800922DAB` |
| `refs_R581.bib` | `2814A71447D4F915B14C1C943C03CA1B2DC76412FB6A318A2FB96123403F28FC` |
| `main_R581.pdf` | `E6EDD63A5F2AB6504C294F51699DD14320B847E8329F9EFB970602D1391587B2` |
| `SI_R581.pdf` | `56D890A1FED7401A0C3E70E040C52119CD2C27B574D70DC7CF104F4C55177E22` |

## Review questions

- Can a reader state the paper's one result after scanning the title, abstract
  and six figures for two minutes?
- Does each main figure carry one claim that is visible within 15 seconds?
- Does Figure 3 make the spatial progression legible without implying a
  deposit morphology, and is the native-area/profile distinction explicit?
- Do Figures 5 and 6 preserve the positive electrode as the protagonist rather
  than promoting atomistic priors, NH4Br or workflow taxonomy?
- Does the prose describe physical objects and observations directly, or force
  the reader to decode internal audit vocabulary?
- Are necessary model boundaries stated once in the correct location rather
  than repeated as defensive disclaimers?
