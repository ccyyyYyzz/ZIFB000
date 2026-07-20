"""Build R582 Supplementary Figures S7-S9 from frozen DFT/MD evidence.

The renderer is deliberately limited to the registered electronic-energy
tables, optimized XYZ coordinates, the recoverable two-I2 delta-rho NPY, and
the registered MD carrier summary.  It never reads legacy figure rasters.
All drawing, export, and preview generation is Python-only.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import itertools
import json
import math
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import matplotlib

matplotlib.use("Agg")

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import font_manager
from matplotlib.lines import Line2D
from PIL import Image


SOURCE_DATA_DIR = Path(__file__).resolve().parent.parent
if str(SOURCE_DATA_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DATA_DIR))
from r582_font_runtime import register_termes_fonts


SCRIPT_DIR = Path(__file__).resolve().parent
MANUSCRIPT_DIR = SCRIPT_DIR.parents[1]
PROJECT_ROOT = MANUSCRIPT_DIR.parent
INPUT_DIR = SCRIPT_DIR / "registered_inputs"
OUT_DIR = MANUSCRIPT_DIR / "figures_R582"

TERMES_DIR, _TERMES_BY_ROLE, FONT_FAMILY = register_termes_fonts(font_manager)
TERMES_HASHES = {
    "texgyretermes-regular.otf": "CC3FE7C707B81428D23D54DF3EADD9228A2BF6A4D43125D94DF56F5F63134659",
    "texgyretermes-bold.otf": "2FB3E952065FA153C7E4E64E04B98B9D79225739B6025AA3F0F0782D299FF61E",
    "texgyretermes-italic.otf": "6DD103A1672E50568CD2F8A706CCD48443D44D7D073A59D2286F4E6F746575D6",
    "texgyretermes-bolditalic.otf": "1BF6AF99CB0E26C12951317032D79B96AE009551E59CCF02A5B24F325ECFEC87",
}

WIDTH_MM = 180.0
S7_HEIGHT_MM = 120.0
S8_HEIGHT_MM = 112.0
S9_HEIGHT_MM = 96.0
MM_PER_INCH = 25.4
BASE_FONT_PT = 7.2
MIN_FONT_PT = 6.5
PANEL_FONT_PT = 8.0
MATH_PARENT_PT = 9.4  # mathtext scripts render at 70%, hence >= 6.58 pt
RASTER_DPI = 600
PREVIEW_DPI = 150
FIXED_DATE = dt.datetime(2026, 7, 20, 12, 0, 0, tzinfo=dt.timezone.utc)

PALETTE = {
    "ink": "#242424",
    "graphite": "#505050",
    "neutral": "#888888",
    "light": "#D9D9D9",
    "lighter": "#F2F2F2",
    "violet": "#7765A7",
    "violet_light": "#EEEAF7",
    "amber": "#D8912B",
    "amber_light": "#F7E7CA",
    "blue": "#3B6FB6",
    "blue_light": "#DCE7F5",
    "teal": "#2A9D8F",
    "vermilion": "#D65345",
    "carbon": "#666666",
    "oxygen": "#D65345",
    "hydrogen": "#FFFFFF",
    "iodine": "#8B4B9F",
    "accumulation": "#3B82B8",
    "depletion": "#D8912B",
}

REGISTERED = {
    "S7_energy": {
        "file": "S7_single_i2_energy.csv",
        "sha256": "1FC77A716EC8E1460A671FB18AA201F8E0E46A6ECA0DB646DEB596B1587E9CB2",
        "original": "DFT/06_periodic_cp2k_single_i2_r514/workspace_snapshot/outputs/r514_status1_short/tables/sanity_final_four_site_spectrum.csv",
        "role": "accepted BSSE-corrected periodic single-I2 adsorption-energy ordering",
        "figure": "S7",
    },
    "S7_basal_xyz": {
        "file": "S7_basal.xyz",
        "sha256": "267B97A2A83633398001EF4AB9FD209987189C9E1AC522B8BC386A32DD9924C6",
        "original": "DFT/06_periodic_cp2k_single_i2_r514/workspace_snapshot/outputs/ec2_sanity_recovered_20260619/204745/cp2k_adsorption_heterogeneity/structures/basal_pristine_periodic_slab_i2_from_geo_opt_selected.xyz",
        "role": "accepted optimized basal single-I2 geometry",
        "figure": "S7",
    },
    "S7_COH_xyz": {
        "file": "S7_C-OH.xyz",
        "sha256": "EDB8116CE3FF9B409590B0455F9266D0BE0859641FDF4A2FCA6CF6EB5F57CDFB",
        "original": "DFT/06_periodic_cp2k_single_i2_r514/workspace_snapshot/outputs/ec2_sanity_recovered_20260619/204745/cp2k_adsorption_heterogeneity/structures/OH_functionalized_basal_periodic_slab_i2_from_geo_opt_selected.xyz",
        "role": "accepted optimized C-OH single-I2 geometry",
        "figure": "S7",
    },
    "S7_CO_xyz": {
        "file": "S7_C=O.xyz",
        "sha256": "94628AF41206D57EDE803877F341DCC7895275225DEB7ADD068DE8BE6A6A3648",
        "original": "DFT/06_periodic_cp2k_single_i2_r514/workspace_snapshot/outputs/ec2_sanity_recovered_20260619/204745/cp2k_adsorption_heterogeneity/structures/carbonyl_edge_periodic_ribbon_sanity_selected.xyz",
        "role": "accepted optimized C=O single-I2 geometry",
        "figure": "S7",
    },
    "S7_vacancy_xyz": {
        "file": "S7_vacancy.xyz",
        "sha256": "92905B451A1BFAC8DEDC426CAC848E05B53474C11CA566632A636C533969B9E4",
        "original": "DFT/06_periodic_cp2k_single_i2_r514/workspace_snapshot/outputs/ec2_sanity_recovered_20260619/204745/cp2k_adsorption_heterogeneity/structures/single_vacancy_periodic_slab_sanity_selected.xyz",
        "role": "accepted optimized vacancy single-I2 geometry",
        "figure": "S7",
    },
    "S8_energy": {
        "file": "S8_two_i2_energy.csv",
        "sha256": "DD5559138BF7239E267037AC4DBA32BC4BE0D2987907A1A2868330924942D3F9",
        "original": "DFT/06_periodic_cp2k_single_i2_r514/workspace_snapshot/outputs/r514_status1_short/tables/r514_2i2_coalescence_summary.csv",
        "role": "registered compact-minus-separated two-I2 electronic-energy diagnostic",
        "figure": "S8",
    },
    "S8_compact_xyz": {
        "file": "S8_compact.xyz",
        "sha256": "7438EC5CA0A722342699F3D68C8FE3E00B336D0286362D9F9F08B71105C25AED",
        "original": "DFT/06_periodic_cp2k_single_i2_r514/workspace_snapshot/outputs/r514_status1_short/structures/r514/OH_functionalized_basal_periodic_slab_near_2i2_geo_opt_selected.xyz",
        "role": "accepted optimized compact C-OH plus two-I2 geometry",
        "figure": "S8",
    },
    "S8_separated_xyz": {
        "file": "S8_separated.xyz",
        "sha256": "BADFDB452ED3697A527E54A9956387CD392E680E328836E639E2FB2A44A5F09B",
        "original": "DFT/06_periodic_cp2k_single_i2_r514/workspace_snapshot/outputs/r514_status1_short/structures/r514/OH_functionalized_basal_periodic_slab_separated_2i2_geo_opt_selected.xyz",
        "role": "accepted optimized separated C-OH plus two-I2 reference geometry",
        "figure": "S8",
    },
    "S8_delta_rho": {
        "file": "S8_delta_rho_stride2.npy",
        "sha256": "898E5619426938F607274DAD9FE5A0F7AA7AAD90B02B594D8F18B1E2DD522F6F",
        "original": "DFT/06_periodic_cp2k_single_i2_r514/workspace_snapshot/outputs/r514_2i2_density_return_20260627T003955Z/r514_2i2_density_handoff_20260627/outputs/figures_r514_2i2_density/r514_OH_near_2i2_delta_rho_stride2.npy",
        "role": "recoverable true two-I2 charge-density-difference grid",
        "figure": "S8",
    },
    "S8_cp2k_input": {
        "file": "S8_complex_edensity.inp",
        "sha256": "2F799C10680A0518720CFE708A7037F61F21B604ED2CEF5961A2852D8B668DC2",
        "original": "DFT/06_periodic_cp2k_single_i2_r514/workspace_snapshot/outputs/r514_2i2_density_return_20260627T003955Z/r514_2i2_density_handoff_20260627/cp2k_outputs/r514_2i2_density/r514_OH_near_2i2_complex_edensity.inp",
        "role": "registered CP2K cell and geometry used to map the stride-2 CDD grid",
        "figure": "S8",
    },
    "S9_ladder": {
        "file": "S9_md_ladder.csv",
        "sha256": "01DE06CA4D66719E5D614A66F3067B0916390A316C3F17C1F8A5C4E08DC832EB",
        "original": "MD/carrier_diffusivity_si_figure/R197_FigS_md_carrier_diffusivity_source_summary.csv",
        "role": "five-SOC species means, ranges and propagated block-stability values",
        "figure": "S9",
    },
    "S9_summary": {
        "file": "S9_md_summary.json",
        "sha256": "86243B41D8B5164817BC25C39CAA18E8D09161FF1CEDF4A2C26A13D865A2C79C",
        "original": "MD/carrier_diffusivity_si_figure/R197_FigS_md_carrier_diffusivity_summary.json",
        "role": "registered charge-parameterization carrier-range summary",
        "figure": "S9",
    },
    "S9_readme": {
        "file": "S9_MD_README.md",
        "sha256": "4186EA28B523A745A4CE674D9CD42AE7015215A75288B33747934EE86D21A900",
        "original": "MD/workspace_mirror/outputs/md_transport_soc_series/README.md",
        "role": "MD system definition and bounded-prior claim boundary",
        "figure": "S9",
    },
    "S9_config": {
        "file": "S9_soc_series_config.yaml",
        "sha256": "CA3EF0C933309A94899A2132CEE703413AAA6A032146DCE8250C6A27AF717F7F",
        "original": "MD/workspace_mirror/outputs/md_transport_soc_series/inputs/soc_series_config.yaml",
        "role": "temperature, SOC grid, production length and force-field notes",
        "figure": "S9",
    },
    "S9_completion": {
        "file": "S9_completion_audit.md",
        "sha256": "C20E068F58D95E2F61A4A6B3F178936FAFF02AC5EB9D1A8C654BE96E9018F6D2",
        "original": "MD/workspace_mirror/outputs/md_transport_soc_series/results/completion_audit.md",
        "role": "registered completion audit for ten long production cases",
        "figure": "S9",
    },
    "S9_viscosity_status": {
        "file": "S9_viscosity_replicate_results.json",
        "sha256": "52CDC9EF4F22CBED0FDD6E6403CE1B785CDA48893BAE4F43E5BAA02862F661EC",
        "original": "MD/workspace_mirror/outputs/md_transport_soc_series/results/viscosity_replicate_results.json",
        "role": "status record showing optional viscosity replicas are not the diffusion uncertainty",
        "figure": "S9",
    },
}

FIGURE_SPECS = {
    "S7": ("Fig_R582_SI07_single_I2_ordering", S7_HEIGHT_MM),
    "S8": ("Fig_R582_SI08_two_I2_diagnostic", S8_HEIGHT_MM),
    "S9": ("Fig_R582_SI09_md_carrier_ladder", S9_HEIGHT_MM),
}

DFT_SITE_ORDER = ["C-OH", "C=O", "basal", "vacancy"]
DFT_SITE_MAP = {
    "OH_functionalized_basal_periodic_slab": "C-OH",
    "carbonyl_edge_periodic_ribbon": "C=O",
    "basal_pristine_periodic_slab": "basal",
    "single_vacancy_periodic_slab": "vacancy",
}
DFT_XYZ_KEYS = {
    "C-OH": "S7_COH_xyz",
    "C=O": "S7_CO_xyz",
    "basal": "S7_basal_xyz",
    "vacancy": "S7_vacancy_xyz",
}

MD_ORDER = ["H2O", "NH4+", "I-", "Br-", "Zn2+", "I2", "I3-", "I2Br-"]
MD_LABELS = {
    "H2O": r"H$_2$O",
    "NH4+": r"NH$_4^+$",
    "I-": r"I$^-$",
    "Br-": r"Br$^-$",
    "Zn2+": r"Zn$^{2+}$",
    "I2": r"I$_2$",
    "I3-": r"I$_3^-$",
    "I2Br-": r"I$_2$Br$^-$",
}

CPK = {
    "C": PALETTE["carbon"],
    "O": PALETTE["oxygen"],
    "H": PALETTE["hydrogen"],
    "I": PALETTE["iodine"],
}
ATOM_SIZE = {"C": 11.0, "O": 18.0, "H": 7.0, "I": 31.0}
ATOM_MARKER = {"C": "o", "O": "s", "H": "o", "I": "H"}
COVALENT_RADIUS = {"H": 0.31, "C": 0.76, "O": 0.66, "I": 1.39}


@dataclass(frozen=True)
class Atom:
    index: int
    element: str
    xyz: np.ndarray


@dataclass
class GeometryPayload:
    key: str
    atoms_all: list[Atom]
    atoms: list[Atom]
    projected: np.ndarray
    depth: np.ndarray
    center: np.ndarray
    iodine_pairs: list[tuple[int, int]]
    bonds: list[tuple[int, int]]
    i_i_distances: list[float]
    nearest_i_o: float | None


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def project_relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(PROJECT_ROOT.resolve()).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def registered_path(key: str) -> Path:
    return INPUT_DIR / str(REGISTERED[key]["file"])


def register_font_lock() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for filename, expected in TERMES_HASHES.items():
        path = TERMES_DIR / filename
        if not path.is_file():
            raise FileNotFoundError(f"Required manuscript font missing: {path}")
        observed = sha256(path)
        if observed != expected:
            raise RuntimeError(
                f"Font hash mismatch for {filename}: expected {expected}, observed {observed}"
            )
        font_manager.fontManager.addfont(str(path))
        rows.append(
            {
                "figure": "S7-S9",
                "input_role": "exact manuscript font file",
                "original_path": path.as_posix(),
                "registered_path": "not copied; loaded directly from TeX Live",
                "bytes": path.stat().st_size,
                "sha256": observed,
                "copy_status": "direct exact-OTF registration",
                "access": "read-only",
            }
        )

    mpl.rcParams.update(
        {
            "font.family": FONT_FAMILY,
            "font.size": BASE_FONT_PT,
            "axes.labelsize": BASE_FONT_PT,
            "axes.titlesize": BASE_FONT_PT,
            "xtick.labelsize": MIN_FONT_PT,
            "ytick.labelsize": MIN_FONT_PT,
            "legend.fontsize": MIN_FONT_PT,
            "axes.linewidth": 0.70,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.facecolor": "white",
            "figure.facecolor": "white",
            "savefig.facecolor": "white",
            "svg.fonttype": "none",
            "svg.hashsalt": "R582-SI-molecular-S7-S9-Termes-v1",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "mathtext.fontset": "custom",
            "mathtext.rm": FONT_FAMILY,
            "mathtext.it": f"{FONT_FAMILY}:italic",
            "mathtext.bf": f"{FONT_FAMILY}:bold",
            "mathtext.sf": FONT_FAMILY,
            "mathtext.fallback": None,
            "legend.frameon": False,
            "xtick.major.size": 2.6,
            "ytick.major.size": 2.6,
            "xtick.major.width": 0.65,
            "ytick.major.width": 0.65,
            "lines.solid_capstyle": "round",
            "lines.solid_joinstyle": "round",
        }
    )
    return rows


def validate_registered_inputs(font_rows: list[dict[str, object]]) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for key, meta in REGISTERED.items():
        copy_path = registered_path(key)
        original_path = PROJECT_ROOT / str(meta["original"])
        expected = str(meta["sha256"])
        if not copy_path.is_file():
            raise FileNotFoundError(f"Frozen registered input missing: {copy_path}")
        observed = sha256(copy_path)
        if observed != expected:
            raise RuntimeError(
                f"Registered input changed: {copy_path}; expected {expected}, observed {observed}"
            )
        if original_path.is_file():
            original_hash = sha256(original_path)
            if original_hash != expected:
                raise RuntimeError(
                    f"Original source changed: {original_path}; expected {expected}, observed {original_hash}"
                )
            if copy_path.read_bytes() != original_path.read_bytes():
                raise RuntimeError(f"Registered copy is not byte-identical: {copy_path}")
            copy_status = "byte-identical frozen copy; original source reverified"
        else:
            # Public release snapshots intentionally do not reproduce the deep
            # workspace tree.  The local registered copy remains sufficient
            # because its expected SHA-256 is hard-coded above and the release
            # manifest binds the same bytes to the recorded original path.
            copy_status = "hash-verified frozen copy; original source path not redistributed"
        rows.append(
            {
                "figure": meta["figure"],
                "input_role": meta["role"],
                "original_path": str(meta["original"]),
                "registered_path": project_relative(copy_path),
                "bytes": copy_path.stat().st_size,
                "sha256": observed,
                "copy_status": copy_status,
                "access": "read-only",
            }
        )
    rows.extend(font_rows)
    frame = pd.DataFrame(rows)
    frame.to_csv(
        SCRIPT_DIR / "R582_SI_molecular_input_manifest.csv",
        index=False,
        lineterminator="\n",
    )
    return frame


def read_xyz(path: Path) -> list[Atom]:
    lines = path.read_text(encoding="utf-8").splitlines()
    n_atoms = int(lines[0].strip())
    atoms: list[Atom] = []
    for index, line in enumerate(lines[2 : 2 + n_atoms]):
        parts = line.split()
        if len(parts) < 4:
            raise ValueError(f"Malformed XYZ row in {path}: {line}")
        atoms.append(
            Atom(
                index=index,
                element=parts[0],
                xyz=np.array([float(v) for v in parts[1:4]], dtype=float),
            )
        )
    if len(atoms) != n_atoms:
        raise ValueError(f"XYZ atom-count mismatch for {path}")
    return atoms


def project_points(
    points: np.ndarray,
    center: np.ndarray,
    azimuth_deg: float = -34.0,
    elevation_deg: float = 21.0,
) -> tuple[np.ndarray, np.ndarray]:
    local = points - center
    az = math.radians(azimuth_deg)
    el = math.radians(elevation_deg)
    x_rot = local[:, 0] * math.cos(az) - local[:, 1] * math.sin(az)
    y_rot = local[:, 0] * math.sin(az) + local[:, 1] * math.cos(az)
    z_rot = local[:, 2]
    screen_x = x_rot
    screen_y = z_rot * math.cos(el) - y_rot * math.sin(el)
    depth = y_rot * math.cos(el) + z_rot * math.sin(el)
    return np.column_stack([screen_x, screen_y]), depth


def minimum_iodine_matching(atoms: list[Atom]) -> list[tuple[int, int]]:
    iodine = [i for i, atom in enumerate(atoms) if atom.element == "I"]
    if len(iodine) == 2:
        return [(iodine[0], iodine[1])]
    if len(iodine) != 4:
        raise ValueError(f"Expected two or four iodine atoms, found {len(iodine)}")
    a, b, c, d = iodine
    candidates = [
        [(a, b), (c, d)],
        [(a, c), (b, d)],
        [(a, d), (b, c)],
    ]
    return min(
        candidates,
        key=lambda pairs: sum(
            float(np.linalg.norm(atoms[i].xyz - atoms[j].xyz)) for i, j in pairs
        ),
    )


def build_geometry_payload(key: str, path: Path, crop_radius_A: float) -> GeometryPayload:
    atoms_all = read_xyz(path)
    iodine_xyz = np.array([atom.xyz for atom in atoms_all if atom.element == "I"])
    if iodine_xyz.shape[0] not in {2, 4}:
        raise ValueError(f"Expected two or four iodine atoms in {path}")
    iodine_center = iodine_xyz.mean(axis=0)
    carbons = [atom.xyz for atom in atoms_all if atom.element == "C"]
    nearest_carbons = sorted(
        carbons, key=lambda xyz: float(np.linalg.norm(xyz[:2] - iodine_center[:2]))
    )[:18]
    surface_z = float(np.median([xyz[2] for xyz in nearest_carbons]))
    center = np.array([iodine_center[0], iodine_center[1], surface_z], dtype=float)

    selected: list[Atom] = []
    for atom in atoms_all:
        xy_distance = float(np.linalg.norm(atom.xyz[:2] - iodine_center[:2]))
        if atom.element == "I":
            selected.append(atom)
        elif atom.element == "C" and xy_distance <= crop_radius_A:
            selected.append(atom)
        elif atom.element in {"O", "H"} and xy_distance <= crop_radius_A + 0.8:
            selected.append(atom)

    coords = np.array([atom.xyz for atom in selected], dtype=float)
    projected, depth = project_points(coords, center)
    iodine_pairs = minimum_iodine_matching(selected)

    bonds: list[tuple[int, int]] = list(iodine_pairs)
    iodine_pair_set = {tuple(sorted(pair)) for pair in iodine_pairs}
    for i, atom_i in enumerate(selected):
        for j in range(i + 1, len(selected)):
            atom_j = selected[j]
            pair = (i, j)
            if tuple(sorted(pair)) in iodine_pair_set:
                continue
            if "I" in {atom_i.element, atom_j.element}:
                continue
            if atom_i.element not in COVALENT_RADIUS or atom_j.element not in COVALENT_RADIUS:
                continue
            cutoff = 1.20 * (
                COVALENT_RADIUS[atom_i.element] + COVALENT_RADIUS[atom_j.element]
            ) + 0.18
            if float(np.linalg.norm(atom_i.xyz - atom_j.xyz)) <= cutoff:
                bonds.append(pair)

    i_i_distances = [
        float(np.linalg.norm(selected[i].xyz - selected[j].xyz)) for i, j in iodine_pairs
    ]
    oxygen_xyz = [atom.xyz for atom in atoms_all if atom.element == "O"]
    nearest_i_o: float | None = None
    if oxygen_xyz:
        nearest_i_o = min(
            float(np.linalg.norm(i_xyz - o_xyz))
            for i_xyz in iodine_xyz
            for o_xyz in oxygen_xyz
        )
    return GeometryPayload(
        key=key,
        atoms_all=atoms_all,
        atoms=selected,
        projected=projected,
        depth=depth,
        center=center,
        iodine_pairs=iodine_pairs,
        bonds=bonds,
        i_i_distances=i_i_distances,
        nearest_i_o=nearest_i_o,
    )


def common_geometry_span(payloads: Iterable[GeometryPayload]) -> tuple[float, float]:
    widths = []
    heights = []
    for payload in payloads:
        widths.append(float(np.ptp(payload.projected[:, 0])))
        heights.append(float(np.ptp(payload.projected[:, 1])))
    return max(widths) + 0.8, max(heights) + 0.8


def draw_geometry(
    ax: plt.Axes,
    payload: GeometryPayload,
    title: str,
    span: tuple[float, float] | None = None,
    annotate_i_i: bool = True,
    atom_scale: float = 1.0,
) -> None:
    for i, j in sorted(
        payload.bonds,
        key=lambda pair: float((payload.depth[pair[0]] + payload.depth[pair[1]]) / 2),
    ):
        atom_i = payload.atoms[i]
        atom_j = payload.atoms[j]
        is_iodine = atom_i.element == "I" and atom_j.element == "I"
        ax.plot(
            [payload.projected[i, 0], payload.projected[j, 0]],
            [payload.projected[i, 1], payload.projected[j, 1]],
            color=PALETTE["iodine"] if is_iodine else "#8A8A8A",
            lw=1.05 if is_iodine else 0.43,
            alpha=0.92 if is_iodine else 0.70,
            zorder=4,
        )

    depth_min = float(payload.depth.min())
    depth_span = max(1.0e-9, float(np.ptp(payload.depth)))
    for index in np.argsort(payload.depth):
        atom = payload.atoms[int(index)]
        depth_fraction = float((payload.depth[int(index)] - depth_min) / depth_span)
        size = ATOM_SIZE.get(atom.element, 10.0) * atom_scale * (0.88 + 0.20 * depth_fraction)
        edge = PALETTE["ink"]
        ax.scatter(
            [payload.projected[int(index), 0]],
            [payload.projected[int(index), 1]],
            s=size,
            marker=ATOM_MARKER.get(atom.element, "o"),
            facecolor=CPK.get(atom.element, PALETTE["neutral"]),
            edgecolor=edge,
            linewidth=0.38,
            zorder=8 + depth_fraction,
        )

    ax.set_title(title, loc="left", pad=2.0, fontweight="bold")
    if annotate_i_i:
        distances = "/".join(f"{value:.2f}" for value in payload.i_i_distances)
        ax.text(
            0.98,
            0.035,
            f"I-I {distances} Å",
            transform=ax.transAxes,
            ha="right",
            va="bottom",
            fontsize=MIN_FONT_PT,
            color=PALETTE["graphite"],
        )

    x_mid = float((payload.projected[:, 0].min() + payload.projected[:, 0].max()) / 2)
    y_mid = float((payload.projected[:, 1].min() + payload.projected[:, 1].max()) / 2)
    if span is None:
        x_span = float(np.ptp(payload.projected[:, 0])) + 0.8
        y_span = float(np.ptp(payload.projected[:, 1])) + 0.8
    else:
        x_span, y_span = span
    ax.set_xlim(x_mid - x_span / 2, x_mid + x_span / 2)
    ax.set_ylim(y_mid - y_span / 2, y_mid + y_span / 2)
    ax.set_aspect("equal", adjustable="box")
    ax.set_axis_off()


def geometry_atom_rows(figure: str, payloads: Iterable[GeometryPayload]) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for payload in payloads:
        for display_index, atom in enumerate(payload.atoms):
            rows.append(
                {
                    "figure": figure,
                    "geometry": payload.key,
                    "display_index": display_index,
                    "xyz_atom_index": atom.index,
                    "element": atom.element,
                    "x_A": atom.xyz[0],
                    "y_A": atom.xyz[1],
                    "z_A": atom.xyz[2],
                    "display_crop_only": True,
                    "coordinate_modified": False,
                }
            )
    return pd.DataFrame(rows)


def geometry_metric_rows(figure: str, payloads: Iterable[GeometryPayload]) -> pd.DataFrame:
    rows = []
    for payload in payloads:
        rows.append(
            {
                "figure": figure,
                "geometry": payload.key,
                "atoms_in_xyz": len(payload.atoms_all),
                "atoms_displayed_after_crop": len(payload.atoms),
                "I-I_distances_A": ";".join(f"{value:.12g}" for value in payload.i_i_distances),
                "nearest_I-O_A": "" if payload.nearest_i_o is None else payload.nearest_i_o,
                "projection": "orthographic azimuth=-34deg elevation=21deg",
                "bond_rule": "minimum-distance I2 pairing; non-I adjacency from covalent-radius cutoff",
            }
        )
    return pd.DataFrame(rows)


def panel_label(ax: plt.Axes, label: str, x: float = -0.10, y: float = 1.04) -> None:
    ax.text(
        x,
        y,
        label,
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=PANEL_FONT_PT,
        fontweight="bold",
        color=PALETTE["ink"],
        clip_on=False,
    )


def style_numeric_axis(ax: plt.Axes) -> None:
    ax.spines["left"].set_linewidth(0.70)
    ax.spines["bottom"].set_linewidth(0.70)
    ax.tick_params(direction="out", width=0.65, length=2.6, pad=2.0)


def build_s7() -> tuple[plt.Figure, dict[str, object], list[Path]]:
    energy = pd.read_csv(registered_path("S7_energy"))
    energy["site"] = energy["site_id"].map(DFT_SITE_MAP)
    if energy["site"].isna().any():
        raise RuntimeError("Unexpected site ID in the frozen S7 energy table")
    energy = energy.set_index("site").loc[DFT_SITE_ORDER].reset_index()
    energy["relative_to_basal_eV"] = pd.to_numeric(energy["delta_vs_basal_eV"])
    plotted_energy = energy[
        [
            "site",
            "E_ads_D3_plus_PBE_BSSE_eV",
            "relative_to_basal_eV",
            "confidence",
            "evidence",
            "paper_use",
            "source",
        ]
    ].copy()

    payloads = [
        build_geometry_payload(site, registered_path(DFT_XYZ_KEYS[site]), 5.8)
        for site in DFT_SITE_ORDER
    ]
    span = common_geometry_span(payloads)

    fig = plt.figure(figsize=(WIDTH_MM / MM_PER_INCH, S7_HEIGHT_MM / MM_PER_INCH))
    grid = fig.add_gridspec(
        2,
        3,
        left=0.090,
        right=0.990,
        bottom=0.125,
        top=0.950,
        wspace=0.26,
        hspace=0.24,
        width_ratios=[1.62, 0.70, 0.70],
    )
    ax_energy = fig.add_subplot(grid[:, 0])
    geo_axes = [
        fig.add_subplot(grid[0, 1]),
        fig.add_subplot(grid[0, 2]),
        fig.add_subplot(grid[1, 1]),
        fig.add_subplot(grid[1, 2]),
    ]

    values = plotted_energy["relative_to_basal_eV"].to_numpy(dtype=float)
    y = np.arange(len(values), dtype=float)
    colors = [
        PALETTE["amber"] if site in {"C-OH", "C=O"} else PALETTE["graphite"]
        for site in DFT_SITE_ORDER
    ]
    ax_energy.axvline(0.0, color=PALETTE["light"], lw=0.95, zorder=0)
    for yi, value, color in zip(y, values, colors):
        ax_energy.plot([0.0, value], [yi, yi], color=color, lw=1.45, zorder=2)
        ax_energy.scatter(
            [value],
            [yi],
            s=37,
            facecolor="white" if abs(value) < 1.0e-12 else color,
            edgecolor=color,
            linewidth=1.0,
            zorder=4,
        )
        label = "0" if abs(value) < 0.005 else f"{value:+.2f}"
        if value < -0.01:
            ax_energy.text(
                value - 0.018,
                yi,
                label,
                ha="right",
                va="center",
                color=PALETTE["graphite"],
            )
        elif value > 0.01:
            ax_energy.text(
                value,
                yi - 0.27,
                label,
                ha="center",
                va="bottom",
                color=PALETTE["graphite"],
            )
        else:
            ax_energy.text(
                value - 0.020,
                yi,
                label,
                ha="right",
                va="center",
                color=PALETTE["graphite"],
            )

    ax_energy.set_yticks(y, ["C-OH", "C=O", "basal", "vacancy"])
    ax_energy.invert_yaxis()
    ax_energy.set_xlim(-0.68, 0.14)
    ax_energy.set_xticks([-0.6, -0.4, -0.2, 0.0])
    ax_energy.set_xlabel(
        "relative BSSE-corrected adsorption energy,\n"
        r"$\Delta E_{\mathrm{ads}}$ versus basal (eV per I$_2$)",
        fontsize=MATH_PARENT_PT,
    )
    ax_energy.set_title(
        r"Relative single-I$_2$ adsorption-energy ordering",
        loc="left",
        pad=4.0,
        fontweight="bold",
        fontsize=MATH_PARENT_PT,
    )
    ax_energy.text(
        0.02,
        0.02,
        "finite periodic calculation; basal reference = 0",
        transform=ax_energy.transAxes,
        ha="left",
        va="bottom",
        fontsize=MIN_FONT_PT,
        color=PALETTE["graphite"],
    )
    ax_energy.tick_params(axis="y", length=0, pad=4.0)
    style_numeric_axis(ax_energy)
    panel_label(ax_energy, "a", x=-0.12, y=1.03)

    labels = ["C-OH", "C=O", "basal", "vacancy"]
    for index, (ax, payload, label) in enumerate(zip(geo_axes, payloads, labels)):
        draw_geometry(ax, payload, label, span=span, annotate_i_i=True)
        panel_label(ax, chr(ord("b") + index), x=-0.18, y=1.02)

    element_handles = [
        Line2D(
            [0],
            [0],
            marker=ATOM_MARKER[element],
            linestyle="none",
            markersize=4.0 if element != "I" else 5.0,
            markerfacecolor=CPK[element],
            markeredgecolor=PALETTE["ink"],
            markeredgewidth=0.45,
            label=element,
        )
        for element in ["C", "O", "H", "I"]
    ]
    fig.legend(
        handles=element_handles,
        loc="lower right",
        bbox_to_anchor=(0.988, 0.025),
        ncols=4,
        handletextpad=0.25,
        columnspacing=0.75,
        borderaxespad=0.0,
        fontsize=MIN_FONT_PT,
    )

    paths = []
    energy_path = SCRIPT_DIR / "R582_SI07_single_I2_energy_ordering.csv"
    atom_path = SCRIPT_DIR / "R582_SI07_geometry_atoms_displayed.csv"
    metric_path = SCRIPT_DIR / "R582_SI07_geometry_metrics.csv"
    plotted_energy.to_csv(energy_path, index=False, float_format="%.12g", lineterminator="\n")
    geometry_atom_rows("S7", payloads).to_csv(
        atom_path, index=False, float_format="%.12g", lineterminator="\n"
    )
    geometry_metric_rows("S7", payloads).to_csv(
        metric_path, index=False, float_format="%.12g", lineterminator="\n"
    )
    paths.extend([energy_path, atom_path, metric_path])
    extra = {
        "site_order": DFT_SITE_ORDER,
        "relative_energies_eV": dict(zip(DFT_SITE_ORDER, values.tolist())),
        "single_I2_CDD": "excluded because raw cubes are absent",
        "geometry_projection": "orthographic; XYZ coordinates unchanged; cropped for display",
    }
    return fig, extra, paths


def parse_cp2k_cell(path: Path) -> np.ndarray:
    vectors: dict[str, np.ndarray] = {}
    inside = False
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        stripped = line.strip()
        if stripped.upper().startswith("&CELL"):
            inside = True
            continue
        if inside and stripped.upper().startswith("&END CELL"):
            break
        if inside:
            match = re.match(
                r"^([ABC])\s+([-+0-9.Ee]+)\s+([-+0-9.Ee]+)\s+([-+0-9.Ee]+)$",
                stripped,
            )
            if match:
                vectors[match.group(1)] = np.array(
                    [float(match.group(2)), float(match.group(3)), float(match.group(4))]
                )
    if set(vectors) != {"A", "B", "C"}:
        raise RuntimeError(f"Could not parse CP2K cell vectors from {path}")
    return np.vstack([vectors["A"], vectors["B"], vectors["C"]])


def cdd_threshold_points(
    delta: np.ndarray,
    cell_vectors: np.ndarray,
    compact: GeometryPayload,
    threshold: float = 0.002,
    radius_A: float = 7.0,
) -> pd.DataFrame:
    if not np.allclose(cell_vectors, np.diag(np.diag(cell_vectors)), atol=1.0e-9):
        raise RuntimeError("CDD display renderer currently requires the registered orthorhombic cell")
    cell = np.diag(cell_vectors)
    iodine = np.array([atom.xyz for atom in compact.atoms_all if atom.element == "I"])
    center_xy = iodine[:, :2].mean(axis=0)
    rows: list[dict[str, object]] = []
    for sign, mask in [
        ("accumulation", delta >= threshold),
        ("depletion", delta <= -threshold),
    ]:
        for ix, iy, iz in np.argwhere(mask):
            xyz = np.array(
                [
                    ix * cell[0] / delta.shape[0],
                    iy * cell[1] / delta.shape[1],
                    iz * cell[2] / delta.shape[2],
                ],
                dtype=float,
            )
            # Map each thresholded voxel to the nearest periodic x/y image of
            # the unwrapped compact iodine cluster.  No values are resampled.
            xyz[0] += np.rint((center_xy[0] - xyz[0]) / cell[0]) * cell[0]
            xyz[1] += np.rint((center_xy[1] - xyz[1]) / cell[1]) * cell[1]
            if float(np.linalg.norm(xyz[:2] - center_xy)) > radius_A:
                continue
            if not (9.5 <= xyz[2] <= 18.5):
                continue
            rows.append(
                {
                    "sign": sign,
                    "ix": int(ix),
                    "iy": int(iy),
                    "iz": int(iz),
                    "delta_rho_e_A-3": float(delta[ix, iy, iz]),
                    "x_display_A": xyz[0],
                    "y_display_A": xyz[1],
                    "z_display_A": xyz[2],
                    "periodic_xy_translation_only": True,
                }
            )
    return pd.DataFrame(rows)


def draw_cdd(
    ax: plt.Axes,
    compact: GeometryPayload,
    points: pd.DataFrame,
) -> None:
    coords = points[["x_display_A", "y_display_A", "z_display_A"]].to_numpy(dtype=float)
    projected, depth = project_points(coords, compact.center)
    for sign, color, marker, size, alpha in [
        ("accumulation", PALETTE["accumulation"], "o", 7.0, 0.50),
        ("depletion", PALETTE["depletion"], "^", 10.0, 0.62),
    ]:
        mask = points["sign"].eq(sign).to_numpy()
        order = np.argsort(depth[mask])
        ax.scatter(
            projected[mask, 0][order],
            projected[mask, 1][order],
            s=size,
            marker=marker,
            facecolor=color,
            edgecolor="none",
            alpha=alpha,
            zorder=2,
        )

    for i, j in sorted(
        compact.bonds,
        key=lambda pair: float((compact.depth[pair[0]] + compact.depth[pair[1]]) / 2),
    ):
        atom_i = compact.atoms[i]
        atom_j = compact.atoms[j]
        is_iodine = atom_i.element == "I" and atom_j.element == "I"
        ax.plot(
            [compact.projected[i, 0], compact.projected[j, 0]],
            [compact.projected[i, 1], compact.projected[j, 1]],
            color=PALETTE["iodine"] if is_iodine else "#7A7A7A",
            lw=1.0 if is_iodine else 0.42,
            alpha=0.92 if is_iodine else 0.67,
            zorder=6,
        )
    depth_min = float(compact.depth.min())
    depth_span = max(1.0e-9, float(np.ptp(compact.depth)))
    for index in np.argsort(compact.depth):
        atom = compact.atoms[int(index)]
        depth_fraction = float((compact.depth[int(index)] - depth_min) / depth_span)
        ax.scatter(
            [compact.projected[int(index), 0]],
            [compact.projected[int(index), 1]],
            s=ATOM_SIZE.get(atom.element, 10.0) * 0.78 * (0.88 + 0.20 * depth_fraction),
            marker=ATOM_MARKER.get(atom.element, "o"),
            facecolor=CPK.get(atom.element, PALETTE["neutral"]),
            edgecolor=PALETTE["ink"],
            linewidth=0.34,
            zorder=9 + depth_fraction,
        )

    all_x = np.r_[projected[:, 0], compact.projected[:, 0]]
    all_y = np.r_[projected[:, 1], compact.projected[:, 1]]
    x_mid = float((all_x.min() + all_x.max()) / 2)
    x_span = float(np.ptp(all_x)) + 0.8
    ax.set_xlim(x_mid - x_span / 2, x_mid + x_span / 2)
    # Reserve a clean lower strip for the threshold and sign key instead of
    # placing either label over the atom/field evidence.
    ax.set_ylim(float(all_y.min()) - 2.0, float(all_y.max()) + 0.45)
    ax.set_aspect("equal", adjustable="box")
    ax.set_axis_off()
    ax.set_title(
        "True two-molecule charge-density difference",
        loc="left",
        pad=2.0,
        fontweight="bold",
    )
    ax.text(
        0.02,
        0.025,
        "threshold +/-0.002 e A^-3",
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=MIN_FONT_PT,
        color=PALETTE["graphite"],
    )
    handles = [
        Line2D(
            [0],
            [0],
            marker="o",
            markersize=4.0,
            linestyle="none",
            markerfacecolor=PALETTE["accumulation"],
            markeredgecolor="none",
            label="accumulation",
        ),
        Line2D(
            [0],
            [0],
            marker="^",
            markersize=4.2,
            linestyle="none",
            markerfacecolor=PALETTE["depletion"],
            markeredgecolor="none",
            label="depletion",
        ),
    ]
    ax.legend(
        handles=handles,
        loc="lower right",
        ncols=1,
        handletextpad=0.35,
        borderaxespad=0.0,
        labelspacing=0.22,
        fontsize=MIN_FONT_PT,
    )


def build_s8() -> tuple[plt.Figure, dict[str, object], list[Path]]:
    summary = pd.read_csv(registered_path("S8_energy"))
    row = summary.loc[
        summary["site_id"].eq("OH_functionalized_basal_periodic_slab")
    ].iloc[0]
    compact_delta = float(row["DeltaE_coalesce_preferred_eV"])
    energy = pd.DataFrame(
        [
            {
                "configuration": "compact",
                "relative_to_separated_eV": compact_delta,
                "source_column": "DeltaE_coalesce_preferred_eV",
                "status": row["status"],
                "interpretation": row["interpretation"],
                "claim_boundary": row["claim_boundary"],
            },
            {
                "configuration": "separated reference",
                "relative_to_separated_eV": 0.0,
                "source_column": "reference definition",
                "status": row["status"],
                "interpretation": "reference configuration",
                "claim_boundary": row["claim_boundary"],
            },
        ]
    )

    compact = build_geometry_payload("compact", registered_path("S8_compact_xyz"), 7.0)
    separated = build_geometry_payload(
        "separated reference", registered_path("S8_separated_xyz"), 7.8
    )
    span = common_geometry_span([compact, separated])

    delta = np.load(registered_path("S8_delta_rho"), allow_pickle=False)
    if delta.shape != (60, 96, 90) or delta.dtype != np.float32:
        raise RuntimeError(f"Unexpected frozen CDD array identity: {delta.shape}, {delta.dtype}")
    cell_vectors = parse_cp2k_cell(registered_path("S8_cp2k_input"))
    cdd = cdd_threshold_points(delta, cell_vectors, compact)
    if cdd.empty or set(cdd["sign"]) != {"accumulation", "depletion"}:
        raise RuntimeError("Both signs of the registered two-I2 CDD must remain visible")

    fig = plt.figure(figsize=(WIDTH_MM / MM_PER_INCH, S8_HEIGHT_MM / MM_PER_INCH))
    grid = fig.add_gridspec(
        2,
        3,
        left=0.078,
        right=0.992,
        bottom=0.125,
        top=0.950,
        wspace=0.30,
        hspace=0.24,
        width_ratios=[0.92, 0.90, 1.30],
    )
    ax_energy = fig.add_subplot(grid[:, 0])
    ax_compact = fig.add_subplot(grid[0, 1])
    ax_separated = fig.add_subplot(grid[1, 1])
    ax_cdd = fig.add_subplot(grid[:, 2])

    y = np.array([0.30, 1.10], dtype=float)
    values = energy["relative_to_separated_eV"].to_numpy(dtype=float)
    colors = [PALETTE["violet"], PALETTE["graphite"]]
    ax_energy.axvline(0.0, color=PALETTE["light"], lw=0.95, zorder=0)
    for yi, value, color in zip(y, values, colors):
        ax_energy.plot([0.0, value], [yi, yi], color=color, lw=1.6, zorder=2)
        ax_energy.scatter(
            [value],
            [yi],
            s=42,
            facecolor="white" if abs(value) < 1.0e-12 else color,
            edgecolor=color,
            linewidth=1.0,
            zorder=4,
        )
        label = "0" if abs(value) < 0.005 else f"{value:+.3f}"
        ax_energy.text(value, yi - 0.18, label, ha="center", va="bottom")
    ax_energy.set_yticks(y, ["compact", "separated\nreference"])
    ax_energy.invert_yaxis()
    ax_energy.set_ylim(1.48, -0.34)
    ax_energy.set_xlim(-0.79, 0.12)
    ax_energy.set_xticks([-0.7, -0.5, -0.3, -0.1, 0.0])
    ax_energy.set_xlabel("relative electronic energy, ΔE (eV)")
    ax_energy.set_title(
        r"Two-I$_2$ electronic-energy diagnostic",
        loc="left",
        pad=4.0,
        fontweight="bold",
        fontsize=MATH_PARENT_PT,
    )
    ax_energy.tick_params(axis="y", length=0, pad=4.0)
    style_numeric_axis(ax_energy)
    panel_label(ax_energy, "a", x=-0.14, y=1.03)

    draw_geometry(ax_compact, compact, "Compact", span=span, annotate_i_i=True)
    draw_geometry(
        ax_separated,
        separated,
        "Separated reference",
        span=span,
        annotate_i_i=True,
    )
    panel_label(ax_compact, "b", x=-0.18, y=1.02)
    panel_label(ax_separated, "c", x=-0.18, y=1.02)
    draw_cdd(ax_cdd, compact, cdd)
    panel_label(ax_cdd, "d", x=-0.10, y=1.03)

    energy_path = SCRIPT_DIR / "R582_SI08_two_I2_energy_comparison.csv"
    atom_path = SCRIPT_DIR / "R582_SI08_geometry_atoms_displayed.csv"
    metric_path = SCRIPT_DIR / "R582_SI08_geometry_metrics.csv"
    cdd_path = SCRIPT_DIR / "R582_SI08_cdd_threshold_points.csv"
    cdd_summary_path = SCRIPT_DIR / "R582_SI08_cdd_threshold_summary.csv"
    energy.to_csv(energy_path, index=False, float_format="%.12g", lineterminator="\n")
    geometry_atom_rows("S8", [compact, separated]).to_csv(
        atom_path, index=False, float_format="%.12g", lineterminator="\n"
    )
    geometry_metric_rows("S8", [compact, separated]).to_csv(
        metric_path, index=False, float_format="%.12g", lineterminator="\n"
    )
    cdd.to_csv(cdd_path, index=False, float_format="%.12g", lineterminator="\n")
    raw_positive = int((delta >= 0.002).sum())
    raw_negative = int((delta <= -0.002).sum())
    cdd_summary = pd.DataFrame(
        [
            {
                "threshold_abs_e_A-3": 0.002,
                "raw_grid_shape": "x".join(str(value) for value in delta.shape),
                "raw_accumulation_voxels": raw_positive,
                "raw_depletion_voxels": raw_negative,
                "display_accumulation_points": int(cdd["sign"].eq("accumulation").sum()),
                "display_depletion_points": int(cdd["sign"].eq("depletion").sum()),
                "display_radial_crop_A": 7.0,
                "display_z_range_A": "9.5-18.5",
                "value_interpolation": "none",
                "periodic_mapping": "nearest x/y image only; values and atom coordinates unchanged",
            }
        ]
    )
    cdd_summary.to_csv(
        cdd_summary_path, index=False, float_format="%.12g", lineterminator="\n"
    )
    paths = [energy_path, atom_path, metric_path, cdd_path, cdd_summary_path]
    extra = {
        "compact_minus_separated_eV": compact_delta,
        "CDD_definition": "rho(compact complex) - rho(C-OH surface) - rho(2I2)",
        "CDD_threshold_e_A-3": 0.002,
        "CDD_array_shape": list(delta.shape),
        "CDD_array_min": float(delta.min()),
        "CDD_array_max": float(delta.max()),
        "CDD_raw_counts": {"accumulation": raw_positive, "depletion": raw_negative},
        "CDD_display_counts": {
            "accumulation": int(cdd["sign"].eq("accumulation").sum()),
            "depletion": int(cdd["sign"].eq("depletion").sum()),
        },
        "cell_vectors_A": cell_vectors.tolist(),
        "pathway_cartoon": "excluded",
    }
    return fig, extra, paths


def md_species_color(species: str) -> str:
    if species in {"I2", "I3-", "I2Br-"}:
        return PALETTE["violet"]
    if species == "I-":
        return PALETTE["blue"]
    if species == "H2O":
        return PALETTE["teal"]
    return PALETTE["graphite"]


def draw_md_ladder(ax: plt.Axes, data: pd.DataFrame, variant: str, title: str) -> None:
    part = data.loc[data["variant"].eq(variant)].set_index("species").loc[MD_ORDER]
    y = np.arange(len(MD_ORDER), dtype=float)
    ax.axhspan(4.5, 7.5, color=PALETTE["violet_light"], alpha=0.72, zorder=0)
    open_marker = variant == "q1p0"
    marker = "D" if open_marker else "o"
    for yi, species in zip(y, MD_ORDER):
        row = part.loc[species]
        color = md_species_color(species)
        ax.hlines(
            yi,
            float(row["D_min"]),
            float(row["D_max"]),
            color=color,
            lw=1.35,
            alpha=0.34,
            zorder=2,
        )
        ax.errorbar(
            float(row["D_mean"]),
            yi,
            xerr=float(row["D_sem"]),
            fmt="none",
            ecolor=color,
            elinewidth=0.90,
            capsize=2.1,
            capthick=0.85,
            zorder=4,
        )
        ax.scatter(
            [float(row["D_mean"])],
            [yi],
            s=29,
            marker=marker,
            facecolor="white" if open_marker else color,
            edgecolor=color,
            linewidth=1.05,
            zorder=5,
        )
    ax.set_yticks(y, [MD_LABELS[species] for species in MD_ORDER])
    if not ax.yaxis_inverted():
        ax.invert_yaxis()
    ax.set_xlim(0.0, 2.15)
    ax.set_xticks([0.0, 0.5, 1.0, 1.5, 2.0])
    ax.set_title(title, loc="left", pad=4.0, fontweight="bold", fontsize=MATH_PARENT_PT)
    ax.tick_params(axis="y", length=0, pad=3.0, labelsize=MATH_PARENT_PT)
    style_numeric_axis(ax)


def build_s9() -> tuple[plt.Figure, dict[str, object], list[Path]]:
    data = pd.read_csv(registered_path("S9_ladder"))
    required = {"q0p8_ecc", "q1p0"}
    if set(data["variant"]) != required:
        raise RuntimeError("Unexpected charge variants in the frozen MD ladder")
    if set(data["species"]) != set(MD_ORDER):
        raise RuntimeError("Unexpected species set in the frozen MD ladder")
    if not (pd.to_numeric(data["n_soc"]) == 5).all():
        raise RuntimeError("Every MD ladder row must summarize five SOC compositions")
    data["display_order"] = data["species"].map({key: i for i, key in enumerate(MD_ORDER)})
    data["display_label"] = data["species"].map(MD_LABELS)
    data["range_definition"] = "minimum-maximum across five SOC compositions"
    data["D_sem_definition"] = (
        "propagated four-block within-trajectory stability; not replica uncertainty"
    )
    plotted = data.sort_values(["variant", "display_order"]).reset_index(drop=True)

    fig, axes = plt.subplots(
        1,
        2,
        figsize=(WIDTH_MM / MM_PER_INCH, S9_HEIGHT_MM / MM_PER_INCH),
        sharex=True,
        sharey=True,
    )
    fig.subplots_adjust(left=0.085, right=0.992, bottom=0.205, top=0.825, wspace=0.23)
    draw_md_ladder(axes[0], plotted, "q0p8_ecc", r"Charge-scaled, $q=0.8$ (ECC)")
    draw_md_ladder(axes[1], plotted, "q1p0", r"Formal charge, $q=1.0$")
    panel_label(axes[0], "a", x=-0.12, y=1.04)
    panel_label(axes[1], "b", x=-0.09, y=1.04)
    fig.text(
        0.5,
        0.945,
        "bulk MD: 1 M ZnI2 + 4 M NH4Br, 298.15 K; five SOC compositions",
        ha="center",
        va="top",
        fontsize=MIN_FONT_PT,
        color=PALETTE["graphite"],
    )
    fig.supxlabel(
        r"bulk self-diffusivity, $D$ ($10^{-9}$ m$^2$ s$^{-1}$)",
        x=0.54,
        y=0.085,
        fontsize=MATH_PARENT_PT,
    )

    legend_handles = [
        Line2D(
            [0],
            [0],
            marker="o",
            markersize=4.0,
            linestyle="none",
            markerfacecolor=PALETTE["graphite"],
            markeredgecolor=PALETTE["graphite"],
            label="five-composition mean",
        ),
        Line2D(
            [0, 1],
            [0, 0],
            color=PALETTE["graphite"],
            alpha=0.38,
            lw=1.35,
            label="range across five SOC compositions",
        ),
        Line2D(
            [0, 1],
            [0, 0],
            color=PALETTE["graphite"],
            lw=0.9,
            marker="|",
            markersize=6,
            label="propagated block stability",
        ),
    ]
    fig.legend(
        handles=legend_handles,
        loc="lower center",
        bbox_to_anchor=(0.54, 0.015),
        ncols=3,
        handlelength=1.7,
        handletextpad=0.45,
        columnspacing=1.15,
        borderaxespad=0.0,
        fontsize=MIN_FONT_PT,
    )

    output_path = SCRIPT_DIR / "R582_SI09_md_carrier_ladder.csv"
    plotted.to_csv(output_path, index=False, float_format="%.12g", lineterminator="\n")
    means = {
        variant: {
            species: float(
                plotted.loc[
                    plotted["variant"].eq(variant) & plotted["species"].eq(species),
                    "D_mean",
                ].iloc[0]
            )
            for species in ["I-", "I2", "I3-", "I2Br-"]
        }
        for variant in ["q0p8_ecc", "q1p0"]
    }
    for variant, values in means.items():
        if not all(values[species] < values["I-"] for species in ["I2", "I3-", "I2Br-"]):
            raise RuntimeError(f"Frozen data no longer support the bounded S9 hierarchy: {variant}")
    extra = {
        "condition": "1 M ZnI2 + 4 M NH4Br, 298.15 K",
        "SOC_points": [0.1, 0.3, 0.5, 0.7, 1.0],
        "trajectories": "one trajectory per composition and charge parameterization",
        "production_length_ns": 20.0,
        "uncertainty_boundary": (
            "D_sem is propagated within-trajectory four-block stability; not replica uncertainty"
        ),
        "iodine_carrier_means_1e-9_m2_s": means,
    }
    return fig, extra, [output_path]


def export_figure(fig: plt.Figure, stem: str, width_mm: float, height_mm: float) -> list[Path]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    base = OUT_DIR / stem
    pdf_path = base.with_suffix(".pdf")
    svg_path = base.with_suffix(".svg")
    png_path = base.with_suffix(".png")
    tiff_path = base.with_suffix(".tiff")
    preview_path = OUT_DIR / f"{stem}_{int(width_mm)}mm_preview.png"
    gray_path = OUT_DIR / f"{stem}_{int(width_mm)}mm_grayscale_preview.png"

    fig.set_size_inches(width_mm / MM_PER_INCH, height_mm / MM_PER_INCH, forward=True)
    fig.canvas.draw()
    fig.savefig(
        svg_path,
        format="svg",
        transparent=False,
        metadata={
            "Creator": "R582 deterministic Python/matplotlib renderer",
            "Date": "2026-07-20",
            "Title": stem,
        },
    )
    fig.savefig(
        pdf_path,
        format="pdf",
        transparent=False,
        metadata={
            "Title": stem,
            "Author": "",
            "Subject": "R582 supplementary molecular evidence",
            "Keywords": "",
            "Creator": "R582 deterministic Python/matplotlib renderer",
            "Producer": f"Matplotlib {mpl.__version__}",
            "CreationDate": FIXED_DATE,
            "ModDate": FIXED_DATE,
        },
    )
    fig.savefig(
        png_path,
        format="png",
        dpi=RASTER_DPI,
        transparent=False,
        metadata={"Software": "R582 deterministic Python/matplotlib renderer"},
    )
    with Image.open(png_path) as image:
        rgb = image.convert("RGB")
        rgb.save(
            png_path,
            format="PNG",
            dpi=(RASTER_DPI, RASTER_DPI),
            optimize=False,
        )
        target_width = int(round(width_mm / MM_PER_INCH * PREVIEW_DPI))
        target_height = int(round(height_mm / MM_PER_INCH * PREVIEW_DPI))
        preview = rgb.resize((target_width, target_height), Image.Resampling.LANCZOS)
        preview.save(
            preview_path,
            format="PNG",
            dpi=(PREVIEW_DPI, PREVIEW_DPI),
            optimize=False,
        )
        gray = preview.convert("L").convert("RGB")
        gray.save(
            gray_path,
            format="PNG",
            dpi=(PREVIEW_DPI, PREVIEW_DPI),
            optimize=False,
        )
        tiff_rgb = rgb.copy()
    # Write TIFF from the exact 600-dpi RGB PNG canvas.  Avoid matplotlib's
    # Windows TIFF handle, which can remain locked until figure teardown.
    tiff_tmp = tiff_path.with_name(f"{tiff_path.stem}.rgb_tmp.tiff")
    tiff_rgb.save(
        tiff_tmp,
        format="TIFF",
        dpi=(RASTER_DPI, RASTER_DPI),
        compression="tiff_lzw",
    )
    if tiff_path.exists():
        tiff_path.unlink()
    tiff_tmp.replace(tiff_path)
    plt.close(fig)
    return [svg_path, pdf_path, png_path, tiff_path, preview_path, gray_path]


def build_all(selected: list[str]) -> None:
    font_rows = register_font_lock()
    input_manifest = validate_registered_inputs(font_rows)
    input_manifest_path = SCRIPT_DIR / "R582_SI_molecular_input_manifest.csv"

    builders = {"S7": build_s7, "S8": build_s8, "S9": build_s9}
    all_outputs: list[Path] = [input_manifest_path]
    render_details: dict[str, object] = {}
    for figure in selected:
        stem, height_mm = FIGURE_SPECS[figure]
        fig, extra, source_paths = builders[figure]()
        figure_paths = export_figure(fig, stem, WIDTH_MM, height_mm)
        all_outputs.extend(source_paths)
        all_outputs.extend(figure_paths)
        render_details[figure] = {
            "stem": stem,
            "width_mm": WIDTH_MM,
            "height_mm": height_mm,
            "outputs": {
                path.suffix.lstrip(".") if "preview" not in path.stem else path.stem: {
                    "path": project_relative(path),
                    "bytes": path.stat().st_size,
                    "sha256": sha256(path),
                }
                for path in figure_paths
            },
            "source_tables": [
                {
                    "path": project_relative(path),
                    "bytes": path.stat().st_size,
                    "sha256": sha256(path),
                }
                for path in source_paths
            ],
            "extra": extra,
        }

    render_manifest_path = SCRIPT_DIR / "R582_SI_molecular_render_manifest.json"
    manifest = {
        "release": "R582",
        "figures": selected,
        "backend": "Python/matplotlib only",
        "python": __import__("sys").version.split()[0],
        "matplotlib": mpl.__version__,
        "numpy": np.__version__,
        "pandas": pd.__version__,
        "Pillow": Image.__version__,
        "font_family": "TeX Gyre Termes",
        "font_files": TERMES_HASHES,
        "base_font_pt": BASE_FONT_PT,
        "minimum_font_pt": MIN_FONT_PT,
        "panel_label_pt": PANEL_FONT_PT,
        "math_parent_pt": MATH_PARENT_PT,
        "minimum_math_script_pt": MATH_PARENT_PT * 0.70,
        "svg_fonttype": "none",
        "pdf_fonttype": 42,
        "ps_fonttype": 42,
        "raster_dpi": RASTER_DPI,
        "preview_dpi": PREVIEW_DPI,
        "input_manifest": {
            "path": project_relative(input_manifest_path),
            "rows": int(len(input_manifest)),
            "sha256": sha256(input_manifest_path),
        },
        "render_details": render_details,
        "fixed_metadata_date": "2026-07-20T12:00:00Z",
        "generative_artwork": False,
    }
    render_manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    all_outputs.append(render_manifest_path)
    for supporting_name in [
        "make_r582_si_molecular_figures.py",
        "check_r582_si_molecular_figures.py",
        "FIGURE_CONTRACTS.md",
        "CAPTIONS_DRAFT.md",
        "EVIDENCE_BOUNDARIES.md",
        "QA_NOTES.md",
        "README.md",
        "R582_SI_molecular_QA.json",
    ]:
        supporting_path = SCRIPT_DIR / supporting_name
        if supporting_path.is_file():
            all_outputs.append(supporting_path)

    output_rows = []
    for path in sorted(set(all_outputs), key=lambda item: project_relative(item)):
        output_rows.append(
            {
                "path": project_relative(path),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
                "role": (
                    "figure master or QA preview"
                    if path.parent == OUT_DIR
                    else "source, plotted data, manifest or QA record"
                ),
            }
        )
    pd.DataFrame(output_rows).to_csv(
        SCRIPT_DIR / "R582_SI_molecular_output_manifest.csv",
        index=False,
        lineterminator="\n",
        quoting=csv.QUOTE_MINIMAL,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--figure",
        choices=["S7", "S8", "S9", "all"],
        default="all",
        help="Build one figure or the complete molecular SI set.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    selected = ["S7", "S8", "S9"] if args.figure == "all" else [args.figure]
    build_all(selected)


if __name__ == "__main__":
    main()
