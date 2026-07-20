# R582 Supplementary Figure S5 source bundle

Run `python make_fig_si_r582_s5_hydraulic_fields.py` from any working directory. The script resolves all paths relative to itself, verifies the immutable upstream SHA-256 before reading, writes a frozen plotted-source CSV and input manifest, renders the complete export bundle twice, and requires byte-identical visual outputs.

The plotting backend is exclusively Python/matplotlib. The exact TeX Gyre Termes Regular, Bold, Italic and Bold Italic OTF files are registered directly from TeX Live. No platform font lookup is allowed.

Primary outputs are written to `manuscript/figures_R582` with stem `Fig_SI_R582_S5_hydraulic_fields`. This directory contains the script, figure contract, caption draft, input manifest, frozen plotted-source CSV, render manifest, `pdffonts` report and QA notes.

