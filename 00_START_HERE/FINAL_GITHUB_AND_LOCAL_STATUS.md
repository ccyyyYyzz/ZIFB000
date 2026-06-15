# Final GitHub and local status

Status: LOCAL_ARCHIVE_CREATED_AND_GITHUB_PUSHED

- GitHub repository: https://github.com/ccyyyYyzz/ZIFB000
- Branch: `main`
- Commits pushed:
  - `7fb858f` Curate ZIFB000 manuscript and model archive
  - `175ccbb` Record ZIFB000 upload status
- Local curated folder: `ZIFB000/`
- Local curated zip: `ZIFB000_curated_archive.zip`
- GitHub-light zip: `ZIFB000/ZIFB000_github_release_light.zip`

Remote files verified through GitHub API:

- `README.md`
- `00_START_HERE/GITHUB_UPLOAD_STATUS.md`
- `01_MANUSCRIPT_SCTS_R93/final_status.md`
- `models/single_fiber_i2/single_fiber_i2.py`

Validation note:

The current bundled Python runtime lacks `pytest` and `scipy`, and the system `python` resolves to `C:\Python34\python.exe`, which also lacks `numpy`, `scipy`, `pandas`, `yaml` and `pytest`. Automated model tests were therefore not rerun in this runtime. The organized source files, file manifests, Git commits and remote file reads were verified.
