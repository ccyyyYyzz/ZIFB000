#!/usr/bin/env python
"""Build R582 Supplementary Figure S10 from registered comparator definitions.

The artwork is deliberately orthographic and definition-only.  It does not
render the registered deposit-height/coverage arrays, the solved hydraulic
field, or a pore-blocking front.  Every displayed model node and throat is an
exact member of the central z-index slice stored in the registered network NPZ.
"""

from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.collections import LineCollection
from matplotlib.patches import Circle, Rectangle

from r582_si_figure_tools import (
    BLUE,
    CARMINE,
    GOLD,
    INK,
    LIGHT_BLUE,
    LIGHT_GREY,
    MID_GREY,
    NAVY,
    PALE_GREY,
    PDFINFO,
    PDFFONTS,
    TEAL,
    TERMES_PATHS,
    audit_text,
    configure_font,
    export_deterministic,
    panel_label,
    sha256,
)


HERE = Path(__file__).resolve().parent
MANUSCRIPT_DIR = HERE.parents[1]
WORKSPACE_ROOT = HERE.parents[2]
FIGURE_DIR = MANUSCRIPT_DIR / "figures_R582"
STEM = "SIFig_R582_S10_comparator_definitions"
WIDTH_MM = 180.0
HEIGHT_MM = 104.0

INPUTS = {
    "fiber_npz": HERE / "inputs" / "R531_fiber3d_morphology.npz",
    "network_npz": HERE / "inputs" / "R531_network3d_field.npz",
    "fiber_script": HERE / "inputs" / "R531_fiber3d.py",
    "network_script": HERE / "inputs" / "R531_network3d.py",
}
UPSTREAM = {
    "fiber_npz": WORKSPACE_ROOT
    / "manuscript/source_data/Fig_R556_mesoscale_renders/R531_fiber3d_morphology.npz",
    "network_npz": WORKSPACE_ROOT
    / "manuscript/source_data/Fig_R556_mesoscale_renders/R531_network3d_field.npz",
    "fiber_script": WORKSPACE_ROOT / "fiber/scripts/R531_fiber3d.py",
    "network_script": WORKSPACE_ROOT / "pore_system/scripts/R531_network3d.py",
}
EXPECTED_SHA256 = {
    "fiber_npz": "072AB9F898149FABDABFF757BA7A831E2252B295D044B78214343A6AABE5864E",
    "network_npz": "5FE65C09B47C0481F37AFA62435D91AA61064736B741258764ECDC3DF8AC7AF3",
    "fiber_script": "9037F64EA515B1A9BA5DE68EF91FAB231A4E0840AD8ACCBF12F57E793F4791B4",
    "network_script": "6A2B51CE5E19E6A96A4B2B6ECED71CFB24B10FA447B819B9F49BBD3199EA7787",
}

INPUT_MANIFEST = HERE / "R582_SIFig_S10_input_manifest.csv"
PARAMETER_TABLE = HERE / "R582_SIFig_S10_model_definition.csv"
NODE_TABLE = HERE / "R582_SIFig_S10_network_slice_nodes.csv"
EDGE_TABLE = HERE / "R582_SIFig_S10_network_slice_edges.csv"
RULE_TABLE = HERE / "R582_SIFig_S10_model_rules.csv"
RENDER_MANIFEST = HERE / "R582_SIFig_S10_render_manifest.json"
PDFFONTS_REPORT = HERE / "pdffonts_report.txt"

EPSILON = 0.85
SPECIFIC_AREA_M_INV = 4.0e4
LATTICE_SPACING_UM = 60.0
R_MIN_UM = 0.50
CENTRAL_Z_INDEX = 7

FAMILY = configure_font("R582-SI-FigS10-comparator-definitions-termes")


def rel(path: Path) -> str:
    return path.resolve().relative_to(WORKSPACE_ROOT.resolve()).as_posix()


def validate_input_identity() -> pd.DataFrame:
    rows = []
    roles = {
        "fiber_npz": "registered single-fibre geometry field",
        "network_npz": "registered pore-network geometry/connectivity field",
        "fiber_script": "registered single-fibre model definition",
        "network_script": "registered pore-network model definition",
    }
    for key in INPUTS:
        frozen = INPUTS[key]
        upstream = UPSTREAM[key]
        if not frozen.is_file() or not upstream.is_file():
            raise FileNotFoundError(f"Missing {key}: frozen={frozen}, upstream={upstream}")
        frozen_hash = sha256(frozen)
        upstream_hash = sha256(upstream)
        expected = EXPECTED_SHA256[key]
        if frozen_hash != expected or upstream_hash != expected:
            raise RuntimeError(
                f"Input identity failed for {key}: expected={expected}, "
                f"frozen={frozen_hash}, upstream={upstream_hash}"
            )
        if frozen.read_bytes() != upstream.read_bytes():
            raise RuntimeError(f"Frozen copy is not byte-identical for {key}")
        rows.append(
            {
                "role": roles[key],
                "upstream_workspace_path": rel(upstream),
                "frozen_workspace_path": rel(frozen),
                "bytes": frozen.stat().st_size,
                "sha256": frozen_hash,
                "status": "read-only frozen copy; byte-identical to registered upstream",
            }
        )
    manifest = pd.DataFrame(rows)
    manifest.to_csv(INPUT_MANIFEST, index=False, lineterminator="\n")
    return manifest


def prepare_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, dict]:
    input_manifest = validate_input_identity()

    # Only scalar domain definitions are read from the fibre NPZ.  The height
    # and covered arrays are intentionally not loaded into the plotted tables.
    with np.load(INPUTS["fiber_npz"], allow_pickle=False) as source:
        required = {"r_f", "L_z", "height", "covered", "a_um", "theta_geo", "label"}
        if not required.issubset(source.files):
            raise ValueError(f"Fibre NPZ fields changed: {source.files}")
        r_f_m = float(source["r_f"])
        l_z_m = float(source["L_z"])
        ignored_fibre_fields = ["height", "covered", "a_um", "theta_geo", "label"]
    if not math.isclose(r_f_m, 7.5e-6, rel_tol=0.0, abs_tol=1e-15):
        raise ValueError(f"Unexpected fibre radius: {r_f_m}")
    if not math.isclose(l_z_m, 150e-6, rel_tol=0.0, abs_tol=1e-15):
        raise ValueError(f"Unexpected segment length: {l_z_m}")
    r_out_m = r_f_m / math.sqrt(1.0 - EPSILON)

    with np.load(INPUTS["network_npz"], allow_pickle=False) as source:
        required = {"phi", "nx", "ny", "nz", "e0", "e1", "r0", "r_new", "flux"}
        if not required.issubset(source.files):
            raise ValueError(f"Network NPZ fields changed: {source.files}")
        nx, ny, nz = (int(source[name]) for name in ("nx", "ny", "nz"))
        e0 = source["e0"].astype(int)
        e1 = source["e1"].astype(int)
        r0 = source["r0"].astype(float)
        ignored_network_fields = ["phi", "r_new", "flux"]
    if (nx, ny, nz) != (15, 15, 15):
        raise ValueError(f"Unexpected network shape: {(nx, ny, nz)}")
    node_count = nx * ny * nz
    if len(e0) != 9450 or len(e1) != 9450 or len(r0) != 9450:
        raise ValueError("Unexpected throat inventory")
    if e0.min() < 0 or e1.max() >= node_count:
        raise ValueError("Network edge references an out-of-range node")

    coords = np.array(np.unravel_index(np.arange(node_count), (nx, ny, nz))).T
    delta = np.abs(coords[e1] - coords[e0])
    if not np.all(delta.sum(axis=1) == 1):
        raise ValueError("Registered network includes a non-nearest-neighbour throat")
    central_nodes = np.flatnonzero(coords[:, 2] == CENTRAL_Z_INDEX)
    central_node_set = set(central_nodes.tolist())
    central_edges = np.array(
        [i for i, (a, b) in enumerate(zip(e0, e1)) if a in central_node_set and b in central_node_set],
        dtype=int,
    )
    if len(central_nodes) != 225 or len(central_edges) != 420:
        raise ValueError(
            f"Unexpected central-slice inventory: nodes={len(central_nodes)}, edges={len(central_edges)}"
        )

    nodes = pd.DataFrame(
        {
            "node_id": central_nodes,
            "x_index": coords[central_nodes, 0],
            "y_index": coords[central_nodes, 1],
            "z_index": coords[central_nodes, 2],
        }
    )
    nodes["boundary_role"] = np.where(
        nodes["x_index"].eq(0),
        "inlet_dirichlet_phi_1",
        np.where(nodes["x_index"].eq(nx - 1), "outlet_dirichlet_phi_0", "interior"),
    )
    nodes.to_csv(NODE_TABLE, index=False, lineterminator="\n")

    axes = np.argmax(delta[central_edges], axis=1)
    edges = pd.DataFrame(
        {
            "edge_index": central_edges,
            "node_0": e0[central_edges],
            "node_1": e1[central_edges],
            "x0_index": coords[e0[central_edges], 0],
            "y0_index": coords[e0[central_edges], 1],
            "x1_index": coords[e1[central_edges], 0],
            "y1_index": coords[e1[central_edges], 1],
            "z_index": CENTRAL_Z_INDEX,
            "axis": np.where(axes == 0, "x", "y"),
            "r0_um": r0[central_edges] * 1e6,
        }
    )
    edges.to_csv(EDGE_TABLE, index=False, float_format="%.12g", lineterminator="\n")

    definitions = pd.DataFrame(
        [
            ["single_fibre", "fibre radius", r_f_m * 1e6, "um", "r_f from registered NPZ"],
            ["single_fibre", "unit-cell outer radius", r_out_m * 1e6, "um", "r_f/sqrt(1-epsilon)"],
            ["single_fibre", "segment length", l_z_m * 1e6, "um", "L_z from registered NPZ"],
            ["single_fibre", "porosity", EPSILON, "1", "EPS in registered model script"],
            ["single_fibre", "specific area", SPECIFIC_AREA_M_INV, "m^-1", "A_S in registered model script"],
            ["pore_network", "nodes x", nx, "count", "nx from registered NPZ"],
            ["pore_network", "nodes y", ny, "count", "ny from registered NPZ"],
            ["pore_network", "nodes z", nz, "count", "nz from registered NPZ"],
            ["pore_network", "total throats", len(e0), "count", "e0/e1 from registered NPZ"],
            ["pore_network", "lattice spacing", LATTICE_SPACING_UM, "um", "L_THROAT in registered model script"],
            ["pore_network", "porosity", EPSILON, "1", "EPS in registered model script"],
            ["pore_network", "minimum throat radius", R_MIN_UM, "um", "R_MIN in registered model script"],
            ["display_slice", "z index", CENTRAL_Z_INDEX, "index", "exact central slice"],
            ["display_slice", "nodes", len(nodes), "count", "exact central-slice nodes"],
            ["display_slice", "throats", len(edges), "count", "exact in-slice throats"],
        ],
        columns=["model", "quantity", "value", "unit", "definition_source"],
    )
    definitions.to_csv(PARAMETER_TABLE, index=False, float_format="%.12g", lineterminator="\n")

    rules = pd.DataFrame(
        [
            ["single_fibre", "outer concentration boundary", "c = 1 at r_out"],
            ["single_fibre", "bare wall", "c = 0 at a bare wall node"],
            ["single_fibre", "covered wall", "zero normal flux at a covered wall node"],
            ["single_fibre", "periodicity", "theta and z are periodic"],
            ["single_fibre", "placement", "uniform-random Poisson sites; N = round(n_n A_surf)"],
            ["single_fibre", "assigned cap size", "a = (3 V_s / (2 pi N))^(1/3)"],
            ["pore_network", "Dirichlet drop", "phi = 1 at x = 0; phi = 0 at x = 14"],
            ["pore_network", "conductance", "g_h proportional to r^4/l; g_i proportional to r^2/l"],
            ["pore_network", "allocation", "V_s,k = V_total w_k / sum(w)"],
            ["pore_network", "radius update", "r_new,k^2 = max(r_0,k^2 - V_s,k/(pi l), r_min^2)"],
            [
                "pore_network",
                "tested weights",
                "1; 2 pi r_0 l; 1/r_0^2; abs(q_0); exp[x/(0.3 n_x)]; registered strong-site draw",
            ],
        ],
        columns=["model", "rule", "registered_definition"],
    )
    rules.to_csv(RULE_TABLE, index=False, lineterminator="\n")

    audit = {
        "fibre": {
            "r_f_um": r_f_m * 1e6,
            "r_out_um": r_out_m * 1e6,
            "L_z_um": l_z_m * 1e6,
            "porosity": EPSILON,
            "ignored_npz_fields": ignored_fibre_fields,
        },
        "network": {
            "shape": [nx, ny, nz],
            "total_nodes": node_count,
            "total_throats": len(e0),
            "central_slice_z_index": CENTRAL_Z_INDEX,
            "slice_nodes": len(nodes),
            "slice_throats": len(edges),
            "r0_um_range_in_slice": [float(edges["r0_um"].min()), float(edges["r0_um"].max())],
            "ignored_npz_fields": ignored_network_fields,
        },
        "visual_boundary": (
            "No deposit height, coverage mask, solved pressure/potential field, updated throat radius, "
            "flux field, blockage front, or reconstructed felt image is displayed."
        ),
    }
    return definitions, nodes, edges, rules, audit


def _clean_definition_axis(ax) -> None:
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)


def make_builder(definitions: pd.DataFrame, nodes: pd.DataFrame, edges: pd.DataFrame, audit: dict):
    r_f = float(definitions.loc[definitions["quantity"].eq("fibre radius"), "value"].iloc[0])
    r_out = float(definitions.loc[definitions["quantity"].eq("unit-cell outer radius"), "value"].iloc[0])
    l_z = float(definitions.loc[definitions["quantity"].eq("segment length"), "value"].iloc[0])

    def build():
        fig = plt.figure(figsize=(WIDTH_MM / 25.4, HEIGHT_MM / 25.4), facecolor="white")
        outer = fig.add_gridspec(
            1,
            2,
            left=0.045,
            right=0.985,
            bottom=0.135,
            top=0.845,
            width_ratios=[0.82, 1.28],
            wspace=0.17,
        )
        left = outer[0, 0].subgridspec(2, 1, height_ratios=[1.05, 0.82], hspace=0.34)
        right = outer[0, 1].subgridspec(2, 1, height_ratios=[1.0, 0.40], hspace=0.22)
        ax_cross = fig.add_subplot(left[0, 0])
        ax_side = fig.add_subplot(left[1, 0])
        ax_network = fig.add_subplot(right[0, 0])
        ax_rules = fig.add_subplot(right[1, 0])

        # (a) Exact concentric unit-cell definition; no deposit field is drawn.
        ax_cross.add_patch(Circle((0, 0), r_out, facecolor="#EAF1F4", edgecolor=BLUE, lw=0.9))
        ax_cross.add_patch(Circle((0, 0), r_f, facecolor="#4E555B", edgecolor=INK, lw=0.8))
        ax_cross.annotate(
            "",
            xy=(r_f, 0),
            xytext=(0, 0),
            arrowprops={"arrowstyle": "<->", "color": INK, "lw": 0.7, "shrinkA": 0, "shrinkB": 0},
        )
        ax_cross.text(
            r_f * 0.52,
            1.5,
            r"$r_f=7.50\,\mu$m",
            color="white",
            ha="center",
            va="bottom",
            fontsize=6.5,
        )
        angle = math.radians(43.0)
        endpoint = (r_out * math.cos(angle), r_out * math.sin(angle))
        ax_cross.annotate(
            "",
            xy=endpoint,
            xytext=(0, 0),
            arrowprops={"arrowstyle": "<->", "color": BLUE, "lw": 0.7, "shrinkA": 0, "shrinkB": 0},
        )
        ax_cross.text(
            endpoint[0] * 0.75,
            endpoint[1] * 0.75 + 1.5,
            r"$r_{out}=19.36\,\mu$m",
            color=NAVY,
            ha="left",
            va="bottom",
            fontsize=6.5,
        )
        ax_cross.text(0, -2.0, "carbon fibre", color="white", ha="center", va="center", fontsize=6.5)
        ax_cross.text(0, -r_out + 2.2, r"electrolyte annulus; $c=1$ at $r_{out}$", ha="center", va="bottom", fontsize=6.5)
        ax_cross.set_xlim(-23, 23)
        ax_cross.set_ylim(-22, 22)
        ax_cross.set_aspect("equal")
        _clean_definition_axis(ax_cross)
        ax_cross.set_title("Single-fibre cylindrical unit cell", loc="left", pad=4.0)
        panel_label(ax_cross, "a", x=-0.12, y=1.04)

        ax_side.add_patch(Rectangle((0, -r_out), l_z, 2 * r_out, facecolor="#EAF1F4", edgecolor=BLUE, lw=0.8))
        ax_side.add_patch(Rectangle((0, -r_f), l_z, 2 * r_f, facecolor="#4E555B", edgecolor=INK, lw=0.7))
        ax_side.annotate(
            "",
            xy=(l_z, r_out + 5),
            xytext=(0, r_out + 5),
            arrowprops={"arrowstyle": "<->", "color": INK, "lw": 0.7, "shrinkA": 0, "shrinkB": 0},
        )
        ax_side.text(l_z / 2, r_out + 7, r"$L_z=150\,\mu$m; $z$ periodic", ha="center", va="bottom", fontsize=6.5)
        ax_side.text(l_z / 2, 0, "carbon fibre", color="white", ha="center", va="center", fontsize=6.5)
        ax_side.text(
            l_z / 2,
            -r_out - 7.0,
            "wall mask: bare node $c=0$; covered node has zero normal flux",
            ha="center",
            va="top",
            fontsize=6.5,
        )
        ax_side.text(
            l_z / 2,
            -r_out - 14.0,
            "placement rule (not drawn): Poisson sites; "
            + r"$N=\mathrm{round}(n_n A_{surf})$"
            + "\n"
            + r"assigned volume per site is $V_s/N$",
            ha="center",
            va="top",
            fontsize=6.5,
            linespacing=1.05,
        )
        ax_side.set_xlim(-4, l_z + 4)
        ax_side.set_ylim(-46, 35)
        ax_side.set_aspect("equal")
        _clean_definition_axis(ax_side)

        # (b) Every line/node below is an exact registered central-slice object.
        segments = np.stack(
            [
                edges[["x0_index", "y0_index"]].to_numpy(float),
                edges[["x1_index", "y1_index"]].to_numpy(float),
            ],
            axis=1,
        )
        radii = edges["r0_um"].to_numpy(float)
        line_widths = 0.35 + 1.25 * (radii - radii.min()) / (radii.max() - radii.min())
        ax_network.axvspan(-0.48, 0.35, color="#DDEAF2", zorder=0)
        ax_network.axvspan(13.65, 14.48, color="#F2E8D5", zorder=0)
        ax_network.add_collection(LineCollection(segments, colors=LIGHT_BLUE, linewidths=line_widths, zorder=1))
        interior = nodes["boundary_role"].eq("interior")
        inlet = nodes["boundary_role"].eq("inlet_dirichlet_phi_1")
        outlet = nodes["boundary_role"].eq("outlet_dirichlet_phi_0")
        ax_network.scatter(
            nodes.loc[interior, "x_index"],
            nodes.loc[interior, "y_index"],
            s=5.0,
            facecolor="white",
            edgecolor=MID_GREY,
            linewidth=0.35,
            zorder=2,
        )
        ax_network.scatter(
            nodes.loc[inlet, "x_index"],
            nodes.loc[inlet, "y_index"],
            s=10,
            facecolor=BLUE,
            edgecolor=NAVY,
            linewidth=0.4,
            zorder=3,
        )
        ax_network.scatter(
            nodes.loc[outlet, "x_index"],
            nodes.loc[outlet, "y_index"],
            s=10,
            facecolor=GOLD,
            edgecolor="#765721",
            linewidth=0.4,
            zorder=3,
        )
        ax_network.annotate(
            "imposed through-plane drop",
            xy=(11.4, 14.65),
            xytext=(2.6, 14.65),
            ha="center",
            va="center",
            fontsize=6.5,
            arrowprops={"arrowstyle": "->", "color": INK, "lw": 0.8},
        )
        ax_network.text(0, 14.9, r"inlet $\phi=1$", color=NAVY, ha="left", va="bottom", fontsize=6.5)
        ax_network.text(14, 14.9, r"outlet $\phi=0$", color="#765721", ha="right", va="bottom", fontsize=6.5)
        ax_network.set_xlim(-0.55, 14.55)
        ax_network.set_ylim(-0.55, 15.5)
        ax_network.set_aspect("equal")
        ax_network.set_xticks([0, 7, 14])
        ax_network.set_yticks([0, 7, 14])
        ax_network.set_xlabel("Through-plane node index, $x$")
        ax_network.set_ylabel("Transverse node index, $y$")
        ax_network.set_title("Registered central slice of the pore network", loc="left", pad=4.0)
        panel_label(ax_network, "b", x=-0.11, y=1.04)
        ax_rules.axis("off")
        ax_rules.text(
            0.0,
            0.95,
            r"Exact slice: $z=7$; 225 nodes; 420 throats; line width maps registered initial radius $r_0$.",
            ha="left",
            va="top",
            fontsize=6.5,
            color=MID_GREY,
        )
        ax_rules.text(
            0.0,
            0.69,
            r"Solve: $g_h$ scales with $r^4/\ell$; $g_i$ scales with $r^2/\ell$; $\ell=60\,\mu$m.",
            ha="left",
            va="top",
            fontsize=6.5,
            color=INK,
        )
        ax_rules.text(
            0.0,
            0.43,
            r"Allocation: $V_{s,k}=V_{total}w_k/\mathrm{sum}(w)$; $r_{new,k}^2=\max(r_{0,k}^2-V_{s,k}/\pi\ell,\ r_{min}^2)$.",
            ha="left",
            va="top",
            fontsize=6.5,
            color=INK,
        )
        ax_rules.text(
            0.0,
            0.17,
            r"Tested $w_k$: uniform; surface area; small throat; current path; collector bias; registered strong-site draw.",
            ha="left",
            va="top",
            fontsize=6.5,
            color=INK,
        )

        fig.suptitle(
            "Comparator domains are prescribed, not reconstructed from felt images",
            x=0.515,
            y=0.965,
            fontsize=8.0,
            fontweight="bold",
        )
        fig.text(
            0.515,
            0.035,
            "Flat definition only: no deposit field, coverage map, blockage front or reconstructed felt morphology is shown.",
            ha="center",
            va="bottom",
            fontsize=6.5,
            color=MID_GREY,
        )
        text_audit = audit_text(fig, FAMILY)
        return fig, {
            "width_mm": WIDTH_MM,
            "height_mm": HEIGHT_MM,
            "font_audit": text_audit,
            "slice_nodes": audit["network"]["slice_nodes"],
            "slice_throats": audit["network"]["slice_throats"],
            "rendered_fibre_fields": ["r_f", "r_out", "L_z"],
            "rendered_network_fields": ["e0", "e1", "r0", "nx", "ny", "nz"],
            "excluded_fields": {
                "fibre": audit["fibre"]["ignored_npz_fields"],
                "network": audit["network"]["ignored_npz_fields"],
            },
        }

    return build


def write_manifest(outputs: dict[str, Path], qa: dict, data_audit: dict, input_manifest: pd.DataFrame) -> None:
    font_report = subprocess.run(
        [str(PDFFONTS), str(outputs["pdf"])],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    ).stdout
    PDFFONTS_REPORT.write_text(font_report, encoding="utf-8", newline="\n")
    source_files = [
        INPUT_MANIFEST,
        PARAMETER_TABLE,
        NODE_TABLE,
        EDGE_TABLE,
        RULE_TABLE,
        HERE / "r582_si_figure_tools.py",
        Path(__file__),
        PDFFONTS_REPORT,
    ]
    manifest = {
        "figure": STEM,
        "single_dominant_claim": (
            "The single-fibre and pore-network calculations use explicit idealized model domains, "
            "not reconstructed experimental-felt morphology."
        ),
        "archetype": "schematic-led composite",
        "evidence_class": "E-COMP",
        "backend": "Python/matplotlib only",
        "frozen_date": "2026-07-20",
        "final_size_mm": {"width": WIDTH_MM, "height": HEIGHT_MM},
        "font": {
            "family": FAMILY,
            "minimum_pt": 6.5,
            "registered_faces": [{"path": str(path), "sha256": sha256(path)} for path in TERMES_PATHS],
        },
        "claim_boundary": data_audit["visual_boundary"],
        "data_audit": data_audit,
        "qa": qa,
        "inputs": input_manifest.to_dict(orient="records"),
        "figure_outputs": [
            {"path": rel(path), "bytes": path.stat().st_size, "sha256": sha256(path)}
            for path in outputs.values()
        ],
        "source_bundle_files": [
            {"path": rel(path), "bytes": path.stat().st_size, "sha256": sha256(path)}
            for path in source_files
        ],
        "original_data_mutated": False,
    }
    RENDER_MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    definitions, nodes, edges, _rules, data_audit = prepare_data()
    outputs, qa = export_deterministic(
        make_builder(definitions, nodes, edges, data_audit),
        FIGURE_DIR,
        STEM,
        "Flat definitions of the single-fibre and pore-network comparator models",
        Path(__file__).name,
        WIDTH_MM,
        HEIGHT_MM,
        FAMILY,
    )
    input_manifest = pd.read_csv(INPUT_MANIFEST)
    write_manifest(outputs, qa, data_audit, input_manifest)
    print(json.dumps({"figure": STEM, "outputs": {k: str(v) for k, v in outputs.items()}, "qa": qa}, indent=2))


if __name__ == "__main__":
    main()
