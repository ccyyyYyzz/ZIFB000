# ZIFB000 code package

Reusable code retained here:

- `models/single_fiber_i2/`: independent single-fiber iodine precipitation,
  coverage, film-resistance and closure model.
- `scripts/build_SCTS_R93_sample_article_format_alignment.py`: current manuscript
  package builder.
- `scripts/build_SCTS_R92_scts_format_compliance.py`,
  `scripts/build_SCTS_R85_submission_ordered_revision.py`,
  `scripts/build_SCTS_R84_publication_deep_revision.py`: build dependencies for
  the R93 manuscript pipeline.
- `all_project_scripts_snapshot.zip`: full snapshot of local scripts for audit
  and recovery.

Recommended smoke checks:

```powershell
python -m pytest models/single_fiber_i2/tests
python scripts/build_SCTS_R93_sample_article_format_alignment.py
```

Some scripts require Microsoft Word COM export, COMSOL, or project-specific
outputs. They are kept for provenance and should be run from the original
project root, not from an isolated package, unless paths are updated.
