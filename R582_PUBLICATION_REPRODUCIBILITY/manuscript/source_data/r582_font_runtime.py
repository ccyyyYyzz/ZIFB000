#!/usr/bin/env python3
"""Fail-closed TeX Gyre Termes and TeX Live tool discovery for R582 figures.

The manuscript body is set with ``tgtermes`` and ``newtxmath``.  Every active
figure therefore registers the same four TeX Gyre Termes OTF faces.  Discovery
is portable, but font identity is not negotiable: every face must match the
frozen SHA-256 below.  No system-font or matplotlib fallback is permitted.
"""

from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
from pathlib import Path
from typing import Mapping


FONT_FILENAMES: dict[str, str] = {
    "regular": "texgyretermes-regular.otf",
    "bold": "texgyretermes-bold.otf",
    "italic": "texgyretermes-italic.otf",
    "bolditalic": "texgyretermes-bolditalic.otf",
}

# Exact faces used for the frozen R582 figure set.  These values are also
# recorded by the molecular-figure renderer and must never be weakened to a
# family-name-only check.
FONT_SHA256: dict[str, str] = {
    "regular": "CC3FE7C707B81428D23D54DF3EADD9228A2BF6A4D43125D94DF56F5F63134659",
    "bold": "2FB3E952065FA153C7E4E64E04B98B9D79225739B6025AA3F0F0782D299FF61E",
    "italic": "6DD103A1672E50568CD2F8A706CCD48443D44D7D073A59D2286F4E6F746575D6",
    "bolditalic": "1BF6AF99CB0E26C12951317032D79B96AE009551E59CCF02A5B24F325ECFEC87",
}

FONT_SHA256_BY_FILENAME: dict[str, str] = {
    FONT_FILENAMES[role]: digest for role, digest in FONT_SHA256.items()
}

FONT_RELATIVE_DIR = Path("texmf-dist/fonts/opentype/public/tex-gyre")
COMMON_TEXLIVE_ROOTS = (
    Path("D:/Program Files/texlive"),
    Path("C:/Program Files/texlive"),
    Path("D:/texlive"),
    Path("C:/texlive"),
    Path("/usr/local/texlive"),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def _split_env_paths(value: str) -> list[Path]:
    return [Path(item).expanduser() for item in value.split(os.pathsep) if item.strip()]


def _candidate_font_dirs(root: Path) -> list[Path]:
    root = root.expanduser()
    candidates: list[Path] = []
    if root.name.casefold() == "tex-gyre":
        candidates.append(root)
    candidates.append(root / FONT_RELATIVE_DIR)
    if root.is_dir():
        year_dirs = sorted(
            (item for item in root.iterdir() if item.is_dir() and item.name.isdigit()),
            key=lambda item: int(item.name),
            reverse=True,
        )
        candidates.extend(item / FONT_RELATIVE_DIR for item in year_dirs)
    return candidates


def _validate_font_dir(directory: Path) -> dict[str, Path]:
    paths = {role: directory / filename for role, filename in FONT_FILENAMES.items()}
    missing = [str(path) for path in paths.values() if not path.is_file()]
    if missing:
        raise FileNotFoundError(
            "Required TeX Gyre Termes faces are incomplete in "
            f"{directory}: {', '.join(missing)}"
        )
    mismatches = []
    for role, path in paths.items():
        observed = sha256(path)
        expected = FONT_SHA256[role]
        if observed != expected:
            mismatches.append(f"{path.name}: expected {expected}, observed {observed}")
    if mismatches:
        raise RuntimeError(
            "TeX Gyre Termes face hash mismatch; unpinned font bytes are forbidden: "
            + "; ".join(mismatches)
        )
    return {role: path.resolve() for role, path in paths.items()}


def _bundle_from_kpsewhich(executable: Path) -> tuple[Path, dict[str, Path]]:
    found: dict[str, Path] = {}
    for role, filename in FONT_FILENAMES.items():
        result = subprocess.run(
            [str(executable), filename],
            capture_output=True,
            text=True,
            check=False,
        )
        candidate = Path(result.stdout.strip()) if result.returncode == 0 and result.stdout.strip() else None
        if candidate is None or not candidate.is_file():
            raise FileNotFoundError(f"{executable} did not resolve {filename}")
        found[role] = candidate.resolve()
    directories = {path.parent for path in found.values()}
    if len(directories) != 1:
        raise RuntimeError(
            "kpsewhich resolved TeX Gyre Termes faces from different directories; "
            "mixed font installations are forbidden"
        )
    directory = directories.pop()
    return directory, _validate_font_dir(directory)


def discover_termes_fonts() -> tuple[Path, dict[str, Path]]:
    """Find the exact frozen Termes faces in documented priority order."""
    explicit_font_dir = os.environ.get("R582_TERMES_FONT_DIR")
    if explicit_font_dir:
        directory = Path(explicit_font_dir).expanduser()
        return directory.resolve(), _validate_font_dir(directory)

    explicit_roots = os.environ.get("R582_TEXLIVE_ROOT") or os.environ.get("TEXLIVE_ROOT")
    if explicit_roots:
        errors: list[str] = []
        for root in _split_env_paths(explicit_roots):
            for directory in _candidate_font_dirs(root):
                try:
                    return directory.resolve(), _validate_font_dir(directory)
                except (FileNotFoundError, RuntimeError) as exc:
                    errors.append(str(exc))
        raise FileNotFoundError(
            "R582_TEXLIVE_ROOT/TEXLIVE_ROOT did not contain the four pinned TeX Gyre "
            "Termes faces. " + " | ".join(errors)
        )

    explicit_kpsewhich = os.environ.get("R582_KPSEWHICH")
    if explicit_kpsewhich:
        executable = Path(explicit_kpsewhich).expanduser()
        if not executable.is_file():
            raise FileNotFoundError(f"R582_KPSEWHICH is not a file: {executable}")
        return _bundle_from_kpsewhich(executable)

    rejected: list[str] = []
    detected = shutil.which("kpsewhich.exe") or shutil.which("kpsewhich")
    if detected:
        try:
            return _bundle_from_kpsewhich(Path(detected))
        except (FileNotFoundError, RuntimeError) as exc:
            rejected.append(f"kpsewhich {detected}: {exc}")

    seen: set[Path] = set()
    for root in COMMON_TEXLIVE_ROOTS:
        for directory in _candidate_font_dirs(root):
            resolved = directory.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            try:
                return resolved, _validate_font_dir(resolved)
            except (FileNotFoundError, RuntimeError) as exc:
                rejected.append(str(exc))

    raise FileNotFoundError(
        "The four hash-pinned TeX Gyre Termes OTF faces could not be found. Set "
        "R582_TERMES_FONT_DIR or R582_TEXLIVE_ROOT. Arial, Helvetica, DejaVu, "
        "Liberation, Calibri, Times New Roman and matplotlib fallback are forbidden. "
        + " | ".join(rejected)
    )


def register_termes_fonts(font_manager) -> tuple[Path, dict[str, Path], str]:
    """Discover, hash-check and register all four exact faces with matplotlib."""
    directory, paths = discover_termes_fonts()
    for path in paths.values():
        font_manager.fontManager.addfont(str(path))
    family = font_manager.FontProperties(fname=str(paths["regular"])).get_name()
    if family != "TeX Gyre Termes":
        raise RuntimeError(f"Unexpected pinned font family name: {family!r}")
    for role, properties in {
        "regular": {"weight": "normal", "style": "normal"},
        "bold": {"weight": "bold", "style": "normal"},
        "italic": {"weight": "normal", "style": "italic"},
        "bolditalic": {"weight": "bold", "style": "italic"},
    }.items():
        resolved = Path(
            font_manager.findfont(
                font_manager.FontProperties(family=family, **properties),
                fallback_to_default=False,
            )
        ).resolve()
        if sha256(resolved) != FONT_SHA256[role]:
            raise RuntimeError(
                f"matplotlib resolved {role} text outside the pinned TeX Gyre Termes "
                f"face: {resolved}"
            )
    return directory, paths, family


def _texlive_year_roots(font_dir: Path | None) -> list[Path]:
    roots: list[Path] = []
    if font_dir is not None:
        for ancestor in font_dir.resolve().parents:
            if ancestor.name.isdigit() and ancestor.parent.name.casefold() == "texlive":
                roots.append(ancestor)
                break
    for root in COMMON_TEXLIVE_ROOTS:
        if not root.is_dir():
            continue
        roots.extend(
            sorted(
                (item for item in root.iterdir() if item.is_dir() and item.name.isdigit()),
                key=lambda item: int(item.name),
                reverse=True,
            )
        )
    return roots


def locate_tex_tool(name: str, font_dir: Path | None = None) -> Path:
    """Locate a required TeX/Poppler executable without a workstation lock."""
    env_name = f"R582_{name.upper()}"
    explicit = os.environ.get(env_name)
    if explicit:
        path = Path(explicit).expanduser()
        if not path.is_file():
            raise FileNotFoundError(f"{env_name} is not a file: {path}")
        return path.resolve()

    detected = shutil.which(f"{name}.exe") or shutil.which(name)
    if detected and Path(detected).is_file():
        return Path(detected).resolve()

    suffixes = (".exe", ".cmd", "") if os.name == "nt" else ("",)
    for year_root in _texlive_year_roots(font_dir):
        bin_root = year_root / "bin"
        if not bin_root.is_dir():
            continue
        for platform_dir in sorted(item for item in bin_root.iterdir() if item.is_dir()):
            for suffix in suffixes:
                candidate = platform_dir / f"{name}{suffix}"
                if candidate.is_file():
                    return candidate.resolve()
    raise FileNotFoundError(
        f"Required tool {name!r} was not found. Set {env_name}, add it to PATH, "
        "or set R582_TEXLIVE_ROOT."
    )


def font_hashes_by_role(paths: Mapping[str, Path]) -> dict[str, str]:
    """Return verified font hashes for build manifests."""
    hashes = {role: sha256(path) for role, path in paths.items()}
    if hashes != FONT_SHA256:
        raise RuntimeError(f"Pinned TeX Gyre Termes hash set changed: {hashes}")
    return hashes
