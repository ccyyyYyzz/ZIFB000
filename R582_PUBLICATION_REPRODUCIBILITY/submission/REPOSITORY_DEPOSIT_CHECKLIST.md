# R582 repository and data-deposit checklist

*Journal of Power Sources* applies a deposit-and-link data policy: deposit the research data in a relevant repository and cite/link the record, or state why sharing is not possible. The manuscript and SI now contain the exact planned tagged-directory URL, but that link is not publication-valid until the tag is public, versioned and independently verified.

## 1. Identifier and freeze gate

- [ ] Create a public, immutable tagged release for the exact submitted package.
- [ ] Record the repository owner/name, release title, tag, full commit SHA, public tag/release URL and release date.
- [ ] Record a DOI only if a repository has actually issued one; never manufacture or anticipate a DOI.
- [ ] Upload a SHA-256 manifest generated from the same frozen release contents.
- [x] Lock the planned tag name and insert its exact tagged-directory target in main and SI: `r582-zifb-positive-electrode-reproducibility-v1`.
- [ ] After publication, verify that the embedded URL resolves without a private login to the approved commit/tree.
- [ ] Add a formal dataset citation to `refs.bib` if required by the repository or journal.

Current local-candidate status: the R582-only candidate passes its independent manifest verifier and contains 6 main plus 13 SI figures, 17 source/QA bundles, ten MD case identities, 34 adopted CP2K identity records, continuum-model identities and `EXP-META-001`. This is a local pass, not evidence that the public tag exists.

## 2. Manuscript and submission files

- [ ] `main_R582.tex`, `SI_R582.tex`, `refs.bib` and their exact cold-built PDFs.
- [ ] Journal highlights, cover letter, declarations and final author-approved CRediT statement.
- [ ] Individual main and supplementary figure files with logical upload names.
- [ ] Editable vector masters and required portal raster versions.
- [ ] Final captions synchronized with every panel, unit, symbol and evidence class.

## 3. Quantitative source data and scripts

- [ ] One clean source-data table for every quantitative main and supplementary panel.
- [ ] Deterministic figure-generation and analysis scripts, plus execution order and expected outputs.
- [ ] Environment/package specifications and external-software versions sufficient for reproduction.
- [ ] Input/output manifests and SHA-256 hashes for each quantitative figure.
- [ ] License and third-party reuse notes for every redistributed input.

## 4. Experimental records and EXP-META-001

- [ ] Derived full-cell tables used in the paper, physical-cell identifiers and raw-source hash manifests.
- [ ] Deterministic reconstruction scripts, method locks and output manifests.
- [ ] A machine-readable `EXP-META-001` correction map stating that legacy `NH4Cl`/`NH4CL` acquisition labels refer to experiments performed with NH4Br.
- [ ] Preserve raw filenames, bytes and hashes unchanged; correct the identity only in derived displays/tables and document the transformation.
- [ ] Describe NH4Br only as the representative supporting electrolyte.

## 5. Continuum and lower-scale calculations

- [ ] Canonical COMSOL branch/input hash, software version, study/solution/dataset identities and exported trajectories.
- [ ] Matched accessibility cases, mesh/control identities, output hashes and convergence record.
- [ ] Original `.mph` files remain untouched. Deposit only verified copies when licensing and file-size limits permit; otherwise provide immutable identities, hashes, derived exports and an access route.
- [ ] DFT and MD inputs, structures/topologies, parameter files, software versions and project-specific limitations.
- [ ] Single-fiber and pore-network inputs, scripts, comparator outputs and evidence boundaries.

## 6. Scientific and visual release gates

- [ ] The porous ZIFB positive electrode remains the scientific subject in the README, metadata and graphical materials.
- [ ] No repository text upgrades full-cell anchors into independent validation of modeled internal states.
- [ ] No continuum field is described as microscopy, deposit morphology or an unexported electric-potential field.
- [ ] Figure text matches the manuscript body typeface (TeX Gyre Termes with compatible mathematics), uses no silent fallback or Type 3 fonts and remains at least 6.5 pt at placed size.
- [ ] Every figure passes final-size color and grayscale inspection.
- [ ] No generative AI or AI-assisted image tool is used to create or alter manuscript figures or the graphical abstract.
- [ ] Main and SI cold-build without unresolved citations/references, broken links or missing assets.

## 7. Final public verification

- [ ] Clone/download the public tagged release into a clean directory.
- [ ] Verify the release SHA-256 manifest.
- [ ] Rebuild the manuscript and SI from the downloaded release.
- [ ] Reproduce representative source-data/figure targets from documented commands.
- [ ] Open every public URL without relying on a private login.
- [ ] Confirm that the manuscript, portal metadata and repository use the same title, version and availability wording.
