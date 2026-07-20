#!/usr/bin/env python3
"""Fail-closed verifier for the R582 publication reproducibility candidate."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from pathlib import Path


GITHUB_WARNING_BYTES = 50 * 1024 * 1024
GITHUB_HARD_BYTES = 100 * 1024 * 1024
FORBIDDEN_SUFFIXES = {".mph", ".ndax", ".mpr", ".aux", ".fls", ".fdb_latexmk", ".blg", ".bbl"}
SECRET_PATTERNS = {
    "private_key": re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "github_token": re.compile(rb"(?:ghp|github_pat)_[A-Za-z0-9_]{20,}"),
    "aws_access_key": re.compile(rb"AKIA[0-9A-Z]{16}"),
    "openai_key": re.compile(rb"sk-[A-Za-z0-9_-]{24,}"),
    "google_api_key": re.compile(rb"AIza[0-9A-Za-z_-]{30,}"),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def parse_figures(tex_path: Path) -> list[str]:
    text = tex_path.read_text(encoding="utf-8")
    return [
        Path(match).stem
        for match in re.findall(r"\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}", text)
    ]


def fail(message: str) -> None:
    raise RuntimeError(message)


def verify(root: Path) -> dict[str, object]:
    root = root.resolve()
    manifest = root / "FILE_SHA256_MANIFEST.csv"
    if not manifest.is_file():
        fail(f"Missing manifest: {manifest}")
    with manifest.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    listed = {row["relative_path"] for row in rows}
    actual = {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file() and path.name != "FILE_SHA256_MANIFEST.csv"
    }
    if listed != actual:
        fail(f"Manifest coverage mismatch; missing={sorted(actual-listed)}, extra={sorted(listed-actual)}")
    for row in rows:
        path = root / row["relative_path"]
        if path.stat().st_size != int(row["bytes"]):
            fail(f"Size mismatch: {row['relative_path']}")
        if sha256(path) != row["sha256"].upper():
            fail(f"SHA-256 mismatch: {row['relative_path']}")

    forbidden = []
    transient_logs = []
    secret_hits = []
    warning_files = []
    hard_files = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root).as_posix()
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            forbidden.append(relative)
        if path.suffix.lower() == ".log" and not relative.startswith("molecular_models/md_soc_series/cases/"):
            transient_logs.append(relative)
        if path.stat().st_size > GITHUB_WARNING_BYTES:
            warning_files.append(relative)
        if path.stat().st_size >= GITHUB_HARD_BYTES:
            hard_files.append(relative)
        if path.stat().st_size <= 20 * 1024 * 1024:
            data = path.read_bytes()
            for label, pattern in SECRET_PATTERNS.items():
                if pattern.search(data):
                    secret_hits.append(f"{relative}:{label}")
    if forbidden:
        fail(f"Forbidden suffixes present: {forbidden}")
    if transient_logs:
        fail(f"Unexpected non-MD logs present: {transient_logs}")
    if hard_files:
        fail(f"GitHub >=100 MiB blocker(s): {hard_files}")
    if secret_hits:
        fail(f"Secret-pattern hit(s): {secret_hits}")

    main_figures = parse_figures(root / "manuscript" / "main_R582.tex")
    si_figures = parse_figures(root / "manuscript" / "SI_R582.tex")
    if len(main_figures) != 6 or len(si_figures) != 13 or len(set(main_figures + si_figures)) != 19:
        fail(f"Unexpected live-figure identity: main={len(main_figures)}, SI={len(si_figures)}")
    for stem in main_figures + si_figures:
        for suffix in (".pdf", ".svg", ".png", ".tiff"):
            if not (root / "manuscript" / "figures_R582" / f"{stem}{suffix}").is_file():
                fail(f"Missing figure format: {stem}{suffix}")

    md_manifest = root / "molecular_models" / "md_soc_series" / "MD_CASE_IDENTITY_MANIFEST.csv"
    with md_manifest.open(encoding="utf-8", newline="") as handle:
        md_rows = list(csv.DictReader(handle))
    cases = sorted({row["case"] for row in md_rows if row["case"] != "all"})
    if len(cases) != 10:
        fail(f"Expected 10 MD cases, found {len(cases)}")
    for case in cases:
        case_root = root / "molecular_models" / "md_soc_series" / "cases" / case
        if not (case_root / "topol.top").is_file():
            fail(f"Missing topol.top: {case}")
        if len(list(case_root.glob("*.itp"))) != 6:
            fail(f"Expected six local ITP files: {case}")
        if len(list((case_root / "mdp").glob("*.mdp"))) != 4:
            fail(f"Expected four stage MDP files: {case}")
        if len(list((case_root / "logs").glob("*.log"))) != 9:
            fail(f"Expected nine GROMACS logs: {case}")

    cp2k_manifest = (
        root
        / "molecular_models"
        / "cp2k_single_i2"
        / "CP2K_SINGLE_I2_IDENTITY_MANIFEST.csv"
    )
    with cp2k_manifest.open(encoding="utf-8", newline="") as handle:
        cp2k_rows = list(csv.DictReader(handle))
    if len(cp2k_rows) != 34:
        fail(f"Expected 34 CP2K identity records, found {len(cp2k_rows)}")
    for row in cp2k_rows:
        path = root / row["package_path"]
        if not path.is_file() or path.stat().st_size != int(row["bytes"]) or sha256(path) != row["sha256"]:
            fail(f"CP2K identity mismatch: {row['record_id']}")

    digest = json.loads((root / "PACKAGE_DIGESTS.json").read_text(encoding="utf-8"))
    content_rows = [
        row
        for row in rows
        if row["relative_path"] not in {"PACKAGE_DIGESTS.json"}
    ]
    root_digest = hashlib.sha256()
    for row in sorted(content_rows, key=lambda value: value["relative_path"]):
        root_digest.update(
            f"{row['relative_path']}\0{row['bytes']}\0{row['sha256']}\n".encode("utf-8")
        )
    observed = root_digest.hexdigest().upper()
    if observed != digest["content_root_sha256"]:
        fail(f"Content-root mismatch: {observed} != {digest['content_root_sha256']}")

    return {
        "status": "PASS",
        "root": str(root),
        "manifested_files": len(rows),
        "manifested_bytes": sum(int(row["bytes"]) for row in rows),
        "main_figures": len(main_figures),
        "si_figures": len(si_figures),
        "md_cases": len(cases),
        "cp2k_identity_records": len(cp2k_rows),
        "files_over_50_mib": warning_files,
        "files_at_or_over_100_mib": hard_files,
        "secret_pattern_hits": secret_hits,
        "content_root_sha256": observed,
    }


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    print(json.dumps(verify(root), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
