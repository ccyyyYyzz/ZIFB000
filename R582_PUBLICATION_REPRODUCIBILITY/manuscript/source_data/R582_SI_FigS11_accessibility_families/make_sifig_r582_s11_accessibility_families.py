#!/usr/bin/env python
"""Build R582 Supplementary Figure S11 from registered single-fibre nodes."""

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
    PDFFONTS,
    TEAL,
    TERMES_PATHS,
    audit_text,
    configure_font,
    export_deterministic,
    panel_label,
    sha256,
    style_axis,
)


HERE = Path(__file__).resolve().parent
MANUSCRIPT_DIR = HERE.parents[1]
WORKSPACE_ROOT = HERE.parents[2]
FIGURE_DIR = MANUSCRIPT_DIR / "figures_R582"
STEM = "SIFig_R582_S11_accessibility_families"
WIDTH_MM = 180.0
HEIGHT_MM = 96.0

INPUTS = {
    "closure": HERE / "inputs" / "R531_fiber3d_accessibility_closure.csv",
    "clock": HERE / "inputs" / "R531_fiber3d_clock.csv",
}
UPSTREAM = {
    "closure": WORKSPACE_ROOT / "fiber/data/R531_fiber3d_accessibility_closure.csv",
    "clock": WORKSPACE_ROOT / "fiber/data/R531_fiber3d_clock.csv",
}
EXPECTED_SHA256 = {
    "closure": "77C9242308B9BEBC5E6EAF2519964D511229D49A4F245BE82CC1DB2ADE32AB45",
    "clock": "91D6B8DC78E2E4C7629311B7E776B6F549A56670FFDC50306C8CD092015F21DE",
}

INPUT_MANIFEST = HERE / "R582_SIFig_S11_input_manifest.csv"
PLOT_TABLE = HERE / "R582_SIFig_S11_accessibility_nodes.csv"
REFERENCE_TABLE = HERE / "R582_SIFig_S11_calibrated_reference_nodes.csv"
SHARED_TABLE = HERE / "R582_SIFig_S11_shared_inventory_pairs.csv"
FAMILY_TABLE = HERE / "R582_SIFig_S11_family_definitions.csv"
RENDER_MANIFEST = HERE / "R582_SIFig_S11_render_manifest.json"
PDFFONTS_REPORT = HERE / "pdffonts_report.txt"
LAST_RENDER_LOG = HERE / "last_render.log"

FAMILY_ORDER = ["washable", "baseline_lowNn", "baseline_comsol", "retained_highNn"]
DISPLAY = {
    "washable": "0.001; 1e13 per m²",
    "baseline_lowNn": "0.005; 1e11 per m²",
    "baseline_comsol": "0.005; 1e13 per m²",
    "retained_highNn": "0.020; 1e14 per m²",
}
EXPECTED_DEFINITIONS = {
    "washable": (1e-3, 1e13),
    "baseline_lowNn": (5e-3, 1e11),
    "baseline_comsol": (5e-3, 1e13),
    "retained_highNn": (2e-2, 1e14),
}

FAMILY = configure_font("R582-SI-FigS11-accessibility-families-termes")


def rel(path: Path) -> str:
    return path.resolve().relative_to(WORKSPACE_ROOT.resolve()).as_posix()


def validate_input_identity() -> pd.DataFrame:
    rows = []
    roles = {
        "closure": "registered single-fibre geometric remaining-area nodes",
        "clock": "registered family parameter definitions and matching nodes",
    }
    for key in INPUTS:
        frozen = INPUTS[key]
        upstream = UPSTREAM[key]
        if not frozen.is_file() or not upstream.is_file():
            raise FileNotFoundError(f"Missing {key}: frozen={frozen}, upstream={upstream}")
        expected = EXPECTED_SHA256[key]
        frozen_hash = sha256(frozen)
        upstream_hash = sha256(upstream)
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
    closure = pd.read_csv(INPUTS["closure"], float_precision="round_trip")
    clock = pd.read_csv(INPUTS["clock"], float_precision="round_trip")
    required_closure = {
        "eps_s",
        "theta_geo",
        "accessibility",
        "theta_eff_transport",
        "label",
        "one_minus_theta_geo",
        "comsol_theta_ref",
    }
    required_clock = {"label", "phi_ppt", "n_n_m2", "eps_s", "accessibility", "theta_eff_transport"}
    if not required_closure.issubset(closure.columns):
        raise ValueError(f"Closure fields changed: {closure.columns.tolist()}")
    if not required_clock.issubset(clock.columns):
        raise ValueError(f"Clock fields changed: {clock.columns.tolist()}")
    if len(closure) != 20 or set(closure["label"]) != set(FAMILY_ORDER):
        raise ValueError("Unexpected geometric remaining-area family inventory")
    if closure.groupby("label").size().to_dict() != {key: 5 for key in FAMILY_ORDER}:
        raise ValueError("Each registered family must contain exactly five nodes")
    if closure.duplicated(["label", "eps_s"]).any():
        raise ValueError("Duplicate family/inventory node")
    if not np.isfinite(closure.select_dtypes(include=[np.number]).to_numpy()).all():
        raise ValueError("Non-finite registered geometric remaining-area value")
    if not np.allclose(
        closure["accessibility"].to_numpy(float) + closure["theta_eff_transport"].to_numpy(float),
        1.0,
        rtol=0.0,
        atol=2e-15,
    ):
        raise ValueError("Geometric remaining-area/loss identity failed")

    merged = closure.merge(
        clock[["label", "eps_s", "phi_ppt", "n_n_m2", "accessibility"]],
        on=["label", "eps_s"],
        suffixes=("_closure", "_clock"),
        validate="one_to_one",
    )
    if len(merged) != len(closure) or not np.allclose(
        merged["accessibility_closure"], merged["accessibility_clock"], rtol=0.0, atol=2e-15
    ):
        raise ValueError("Closure nodes do not match the registered clock")

    family_rows = []
    for label in FAMILY_ORDER:
        unique = clock.loc[clock["label"].eq(label), ["phi_ppt", "n_n_m2"]].drop_duplicates()
        if len(unique) != 1:
            raise ValueError(f"Non-unique definition for {label}")
        phi = float(unique["phi_ppt"].iloc[0])
        n_n = float(unique["n_n_m2"].iloc[0])
        expected_phi, expected_n = EXPECTED_DEFINITIONS[label]
        if not math.isclose(phi, expected_phi, rel_tol=0.0, abs_tol=1e-15):
            raise ValueError(f"Unexpected phi_ppt for {label}: {phi}")
        if not math.isclose(n_n, expected_n, rel_tol=0.0, abs_tol=1.0):
            raise ValueError(f"Unexpected placement density for {label}: {n_n}")
        family_rows.append(
            {
                "source_label": label,
                "phi_ppt": phi,
                "n_n_m2": n_n,
                "display_label": DISPLAY[label],
                "evidence_class": "E-COMP",
            }
        )
    families = pd.DataFrame(family_rows)
    families.to_csv(FAMILY_TABLE, index=False, float_format="%.12g", lineterminator="\n")

    plot = merged[
        [
            "label",
            "phi_ppt",
            "n_n_m2",
            "eps_s",
            "accessibility_closure",
            "theta_eff_transport",
            "theta_geo",
            "one_minus_theta_geo",
        ]
    ].rename(
        columns={
            "label": "source_label",
            "accessibility_closure": "geometric_remaining_area_A_over_A0",
        }
    )
    plot["display_label"] = plot["source_label"].map(DISPLAY)
    plot["evidence_class"] = "E-COMP single-fibre computed node"
    plot["line_semantics"] = "connect registered nodes only; no fitted family curve"
    plot["family_order"] = plot["source_label"].map({name: i for i, name in enumerate(FAMILY_ORDER)})
    plot = plot.sort_values(["family_order", "eps_s"]).drop(columns="family_order").reset_index(drop=True)
    plot.to_csv(PLOT_TABLE, index=False, float_format="%.17g", lineterminator="\n")

    reference = (
        closure[["eps_s", "comsol_theta_ref"]]
        .drop_duplicates()
        .sort_values("eps_s")
        .reset_index(drop=True)
    )
    duplicate_check = closure.groupby("eps_s")["comsol_theta_ref"].nunique()
    if (duplicate_check > 1).any():
        raise ValueError("Calibrated reference differs across duplicate inventory nodes")
    reference["R_theta_comparator"] = 1.0 - reference["comsol_theta_ref"]
    reference["evidence_label"] = (
        "R_theta = 1 - theta comparator sampled at registered nodes; "
        "not native COMSOL A_bare/A0"
    )
    reference.to_csv(REFERENCE_TABLE, index=False, float_format="%.17g", lineterminator="\n")

    low = plot.loc[
        plot["source_label"].eq("baseline_lowNn"),
        ["eps_s", "geometric_remaining_area_A_over_A0"],
    ].rename(columns={"geometric_remaining_area_A_over_A0": "geometric_A_over_A0_n_n_1e11"})
    base = plot.loc[
        plot["source_label"].eq("baseline_comsol"),
        ["eps_s", "geometric_remaining_area_A_over_A0"],
    ].rename(columns={"geometric_remaining_area_A_over_A0": "geometric_A_over_A0_n_n_1e13"})
    shared = low.merge(base, on="eps_s", how="inner", validate="one_to_one").sort_values("eps_s")
    if len(shared) != 5:
        raise ValueError(f"Expected five exact shared-inventory pairs, observed {len(shared)}")
    shared["difference_low_minus_high_density"] = (
        shared["geometric_A_over_A0_n_n_1e11"]
        - shared["geometric_A_over_A0_n_n_1e13"]
    )
    shared["phi_ppt_both"] = 5e-3
    shared["comparison_semantics"] = "exact shared computed node; no interpolation"
    shared.to_csv(SHARED_TABLE, index=False, float_format="%.17g", lineterminator="\n")

    audit = {
        "families": 4,
        "nodes_per_family": {key: 5 for key in FAMILY_ORDER},
        "total_computed_nodes": 20,
        "shared_inventory_pairs": len(shared),
        "shared_eps_s_range": [float(shared["eps_s"].min()), float(shared["eps_s"].max())],
        "max_exact_shared_node_difference_geometric_A_over_A0": float(
            shared["difference_low_minus_high_density"].max()
        ),
        "line_policy": "connect registered nodes only; no interpolation or fitted family curve",
        "geometric_curve_definition": (
            "registered single-fibre geometry remaining-area fraction A/A0"
        ),
        "reference_comparator_definition": (
            "R_theta = 1 - theta, computed from comsol_theta_ref and displayed dashed; "
            "not a geometric A/A0 family and not native COMSOL A_bare/A0"
        ),
        "native_comsol_definition": (
            "A_bare/A0 = R_theta * T_pore; not plotted because T_pore is not part of the S11 nodes"
        ),
        "numeric_node_values_changed": False,
        "morphology_inference": False,
        "input_rows": {"closure": len(closure), "clock": len(clock)},
    }
    return plot, reference, shared, input_manifest, audit


def make_builder(plot: pd.DataFrame, reference: pd.DataFrame, shared: pd.DataFrame, audit: dict):
    styles = {
        "washable": {"color": TEAL, "marker": "o", "ls": (0, (3.5, 1.7))},
        "baseline_lowNn": {"color": BLUE, "marker": "s", "ls": "-"},
        "baseline_comsol": {"color": GOLD, "marker": "D", "ls": "-"},
        "retained_highNn": {"color": CARMINE, "marker": "^", "ls": (0, (5.0, 1.8))},
    }

    def build():
        fig = plt.figure(figsize=(WIDTH_MM / 25.4, HEIGHT_MM / 25.4), facecolor="white")
        grid = fig.add_gridspec(
            1,
            12,
            left=0.075,
            right=0.985,
            bottom=0.300,
            top=0.82,
            wspace=1.0,
        )
        ax_all = fig.add_subplot(grid[0, :8])
        ax_pair = fig.add_subplot(grid[0, 8:])

        for label in FAMILY_ORDER:
            group = plot.loc[plot["source_label"].eq(label)].sort_values("eps_s")
            style = styles[label]
            ax_all.plot(
                group["eps_s"],
                group["geometric_remaining_area_A_over_A0"],
                color=style["color"],
                marker=style["marker"],
                ls=style["ls"],
                lw=1.25,
                markersize=4.0,
                markerfacecolor="white",
                markeredgewidth=0.8,
                label=DISPLAY[label],
                zorder=3,
            )
        ax_all.plot(
            reference["eps_s"],
            reference["R_theta_comparator"],
            color=MID_GREY,
            lw=1.1,
            ls=(0, (2.2, 1.7)),
            label="Rθ = 1 − θ comparator (not geometric A/A0)",
            zorder=2,
        )
        ax_all.set_xscale("log")
        ax_all.set_xlim(5e-5, 2e-2)
        ax_all.set_xticks([1e-4, 1e-3, 1e-2], labels=["0.0001", "0.001", "0.01"])
        ax_all.set_ylim(0.0, 1.02)
        ax_all.set_yticks([0.0, 0.25, 0.50, 0.75, 1.0])
        ax_all.set_xlabel("Retained-solid fraction")
        ax_all.set_ylabel("Geometric remaining area, A/A0")
        ax_all.set_title("Geometric single-fibre families", loc="left", pad=4.0)
        ax_all.grid(axis="y", color=LIGHT_GREY, linewidth=0.55, zorder=0)
        style_axis(ax_all)
        panel_label(ax_all, "a", x=-0.07)
        ax_all.legend(
            loc="upper left",
            bbox_to_anchor=(0.0, -0.14),
            ncol=2,
            fontsize=6.5,
            title="Precipitation fraction; placement density",
            title_fontsize=6.5,
            handlelength=2.2,
            columnspacing=1.0,
            labelspacing=0.35,
            borderaxespad=0.0,
        )

        for row in shared.itertuples(index=False):
            ax_pair.plot(
                [row.geometric_A_over_A0_n_n_1e13, row.geometric_A_over_A0_n_n_1e11],
                [row.eps_s, row.eps_s],
                color=LIGHT_GREY,
                lw=1.0,
                zorder=1,
            )
        ax_pair.scatter(
            shared["geometric_A_over_A0_n_n_1e11"],
            shared["eps_s"],
            s=20,
            marker="s",
            facecolor="white",
            edgecolor=BLUE,
            linewidth=0.9,
            label="1e11 per m²",
            zorder=3,
        )
        ax_pair.scatter(
            shared["geometric_A_over_A0_n_n_1e13"],
            shared["eps_s"],
            s=20,
            marker="D",
            facecolor="white",
            edgecolor=GOLD,
            linewidth=0.9,
            label="1e13 per m²",
            zorder=3,
        )
        max_row = shared.loc[shared["difference_low_minus_high_density"].idxmax()]
        ax_pair.annotate(
            rf"exact difference = {max_row['difference_low_minus_high_density']:.3f}",
            xy=(
                0.5
                * (
                    max_row["geometric_A_over_A0_n_n_1e11"]
                    + max_row["geometric_A_over_A0_n_n_1e13"]
                ),
                max_row["eps_s"],
            ),
            xytext=(0.61, 7.2e-3),
            fontsize=6.5,
            color=INK,
            ha="left",
            va="center",
            arrowprops={"arrowstyle": "-", "color": MID_GREY, "lw": 0.65},
        )
        ax_pair.set_yscale("log")
        ax_pair.set_xlim(0.52, 1.005)
        ax_pair.set_ylim(2.5e-4, 1.05e-2)
        ax_pair.set_yticks([1e-3, 1e-2], labels=["0.001", "0.01"])
        ax_pair.set_xticks([0.6, 0.8, 1.0])
        ax_pair.set_xlabel("Geometric A/A0")
        ax_pair.set_ylabel("Retained-solid fraction")
        ax_pair.set_title("Exact paired nodes", loc="left", pad=4.0)
        ax_pair.grid(axis="x", color=LIGHT_GREY, linewidth=0.55, zorder=0)
        style_axis(ax_pair)
        panel_label(ax_pair, "b", x=-0.22)
        ax_pair.text(
            0.03,
            0.96,
            "Both: precipitation fraction 0.005",
            transform=ax_pair.transAxes,
            ha="left",
            va="top",
            fontsize=6.5,
            color=MID_GREY,
        )
        ax_pair.legend(
            loc="lower left",
            fontsize=6.5,
            title="Placement density",
            title_fontsize=6.5,
            handlelength=1.1,
            labelspacing=0.35,
            borderaxespad=0.2,
        )

        fig.suptitle(
            "Single-fibre geometry spans distinct remaining-area responses",
            x=0.52,
            y=0.96,
            fontsize=8.0,
            fontweight="bold",
        )
        fig.text(
            0.985,
            0.060,
            "Curves are geometric A/A0 nodes; dashed is the Rθ = 1 − θ comparator only.",
            ha="right",
            va="bottom",
            fontsize=6.5,
            color=MID_GREY,
        )
        fig.text(
            0.985,
            0.025,
            "Native COMSOL bare-area fraction = Rθ × pore transmissivity (not plotted).",
            ha="right",
            va="bottom",
            fontsize=6.5,
            color=MID_GREY,
        )
        text_audit = audit_text(fig, FAMILY)
        return fig, {
            "width_mm": WIDTH_MM,
            "height_mm": HEIGHT_MM,
            "font_audit": text_audit,
            "computed_family_nodes": audit["total_computed_nodes"],
            "shared_exact_pairs": audit["shared_inventory_pairs"],
            "fitted_family_curves": 0,
            "interpolated_family_points": 0,
        }

    return build


def write_manifest(outputs: dict[str, Path], qa: dict, audit: dict, input_manifest: pd.DataFrame) -> None:
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
        PLOT_TABLE,
        REFERENCE_TABLE,
        SHARED_TABLE,
        FAMILY_TABLE,
        HERE / "r582_si_figure_tools.py",
        Path(__file__),
        PDFFONTS_REPORT,
    ]
    manifest = {
        "figure": STEM,
        "single_dominant_claim": (
            "At fixed retained-solid fraction, the prescribed placement-density assumption can change "
            "the computed geometric remaining area A/A0 substantially."
        ),
        "archetype": "quantitative grid with exact-node companion",
        "evidence_class": "E-COMP",
        "backend": "Python/matplotlib only",
        "frozen_date": "2026-07-20",
        "final_size_mm": {"width": WIDTH_MM, "height": HEIGHT_MM},
        "font": {
            "family": FAMILY,
            "minimum_pt": 6.5,
            "registered_faces": [{"path": str(path), "sha256": sha256(path)} for path in TERMES_PATHS],
        },
        "claim_boundary": (
            "These are deterministic single-fibre comparator families under prescribed placement and retention "
            "parameters. The plotted families are geometric A/A0 curves; the dashed R_theta = 1 - theta "
            "trace is a comparator only. Neither is native COMSOL A_bare/A0, which equals R_theta * T_pore. "
            "The figure is not measured coverage or reconstructed felt morphology."
        ),
        "data_audit": audit,
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
    plot, reference, shared, input_manifest, audit = prepare_data()
    outputs, qa = export_deterministic(
        make_builder(plot, reference, shared, audit),
        FIGURE_DIR,
        STEM,
        "Geometric remaining-area families with a separate R-theta comparator",
        Path(__file__).name,
        WIDTH_MM,
        HEIGHT_MM,
        FAMILY,
    )
    write_manifest(outputs, qa, audit, input_manifest)
    report = {"figure": STEM, "outputs": {k: str(v) for k, v in outputs.items()}, "qa": qa}
    rendered_report = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    LAST_RENDER_LOG.write_text(rendered_report, encoding="utf-8", newline="\n")
    print(rendered_report, end="")


if __name__ == "__main__":
    main()
