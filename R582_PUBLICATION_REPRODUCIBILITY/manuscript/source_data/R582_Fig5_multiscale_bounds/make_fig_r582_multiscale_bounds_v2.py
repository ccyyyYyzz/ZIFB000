"""Build R582 Figure 5 v2 with a quieter prior strip and dominant closure bounds.

Version 1 is retained unchanged.  Version 2 fixes the visual collision between
the panel-a vacancy endpoint and the panel-b I2Br- row label, and makes the
positive-electrode geometric-area/permeability panels the visual center of
gravity.  This active renderer also repairs two scientific labels without
changing any numeric value: panel a reports a BSSE-corrected adsorption-energy
ordering, and panel c reports the single-fibre geometric remaining-area ratio
A/A0 rather than the native COMSOL accessibility A_bare/A0.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image, ImageOps

import make_fig_r582_multiscale_bounds as v1


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = v1.PROJECT_ROOT
OUT_DIR = v1.OUT_DIR
OUT_BASE = OUT_DIR / "Fig_R582_multiscale_bounds_v2"
INPUT_MANIFEST_V2 = SCRIPT_DIR / "R582_Fig5_input_manifest_v2.csv"
RENDER_MANIFEST_V2 = SCRIPT_DIR / "R582_Fig5_render_manifest_v2.json"
PANEL_A_CSV_V2 = SCRIPT_DIR / "R582_Fig5_panel_a_dft_site_ordering_v2.csv"
PANEL_C_CSV_V2 = SCRIPT_DIR / "R582_Fig5_panel_c_geometric_area_families_v2.csv"

V1_RENDERER = SCRIPT_DIR / "make_fig_r582_multiscale_bounds.py"
V1_RENDERER_SHA256 = "2EE1DF3D1FC2DED4418A663BED1A70C9BF2F450057C8AA7248E1FB47E74F631E"

WIDTH_MM = 180.0
HEIGHT_MM = 125.0
MM_PER_INCH = 25.4


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def project_relative(path: Path) -> str:
    return path.resolve().relative_to(PROJECT_ROOT.resolve()).as_posix()


def validate_v1_dependency() -> None:
    observed = sha256(V1_RENDERER)
    if observed != V1_RENDERER_SHA256:
        raise RuntimeError(
            f"Frozen v1 renderer changed: expected {V1_RENDERER_SHA256}, observed {observed}"
        )


def prepare_inputs() -> tuple[
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
    float,
    float,
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
    float,
]:
    validate_v1_dependency()
    source_manifest = v1.validate_inputs().copy()
    source_manifest.loc[
        source_manifest["path_workspace_relative"].eq(project_relative(v1.DFT_INPUT)),
        "input_role",
    ] = "accepted periodic CP2K single-I2 BSSE-corrected adsorption-energy ordering"
    source_manifest.loc[
        source_manifest["path_workspace_relative"].eq(project_relative(v1.FIBER_INPUT)),
        "input_role",
    ] = "single-fibre geometric remaining-area nodes for sparse and dense placement families"
    source_manifest = pd.concat(
        [
            source_manifest,
            pd.DataFrame(
                [
                    {
                        "input_role": "frozen v1 data-validation and drawing dependency",
                        "path_workspace_relative": project_relative(V1_RENDERER),
                        "sha256": V1_RENDERER_SHA256,
                        "access": "read-only",
                    }
                ]
            ),
        ],
        ignore_index=True,
    )

    eps_endpoint = v1.get_baseline_endpoint()
    dft = v1.prepare_panel_a()
    dft_table = dft.copy()
    dft_table["evidence_role"] = "relative BSSE-corrected adsorption-energy ordering prior"
    dft_table.to_csv(
        PANEL_A_CSV_V2,
        index=False,
        float_format="%.15g",
        lineterminator="\n",
    )
    md, band_min, band_max = v1.prepare_panel_b()
    fiber = v1.prepare_panel_c()
    # The read-only upstream file uses legacy column names.  The values are a
    # geometric single-fibre area complement, not the native COMSOL
    # A_bare/A0 = R_theta*T_pore closure.  Keep the in-memory legacy columns
    # only because the frozen v1 drawing helper reads them; publish a
    # semantically explicit v2 source table.
    fiber_table = fiber.rename(
        columns={
            "accessibility": "geometric_A_over_A0",
            "theta_eff_transport": "geometric_removed_fraction",
        }
    ).copy()
    fiber_table["evidence_role"] = (
        "single-fibre geometric remaining-area comparator; distinct from native COMSOL A_bare/A0"
    )
    if not (
        (fiber_table["geometric_A_over_A0"] + fiber_table["geometric_removed_fraction"] - 1.0)
        .abs()
        .le(1e-12)
        .all()
    ):
        raise ValueError("Single-fibre geometric area-complement identity failed.")
    fiber_table.to_csv(
        PANEL_C_CSV_V2,
        index=False,
        float_format="%.15g",
        lineterminator="\n",
    )
    pore_raw, pore_zoom, pore_endpoints = v1.prepare_panel_d(eps_endpoint)
    source_manifest.to_csv(INPUT_MANIFEST_V2, index=False, lineterminator="\n")
    return (
        source_manifest,
        dft,
        md,
        band_min,
        band_max,
        fiber,
        pore_raw,
        pore_zoom,
        pore_endpoints,
        eps_endpoint,
    )


def quiet_prior_panel(ax: plt.Axes) -> None:
    """Reduce upper-strip visual weight without lowering type below 6.5 pt."""

    for spine in ("left", "bottom"):
        ax.spines[spine].set_linewidth(0.62)
        ax.spines[spine].set_color("#4F4F4F")
    ax.tick_params(width=0.58, length=2.35)


def build_figure_v2(
    dft: pd.DataFrame,
    md: pd.DataFrame,
    band_min: float,
    band_max: float,
    fiber: pd.DataFrame,
    pore_raw: pd.DataFrame,
    pore_zoom: pd.DataFrame,
    pore_endpoints: pd.DataFrame,
    eps_endpoint: float,
) -> plt.Figure:
    fig = plt.figure(figsize=(WIDTH_MM / MM_PER_INCH, HEIGHT_MM / MM_PER_INCH))
    outer = fig.add_gridspec(
        2,
        1,
        left=0.082,
        right=0.986,
        bottom=0.105,
        top=0.955,
        hspace=0.43,
        height_ratios=[0.58, 1.42],
    )
    top = outer[0].subgridspec(1, 2, wspace=0.48, width_ratios=[1.0, 1.0])
    bottom = outer[1].subgridspec(1, 2, wspace=0.34, width_ratios=[1.38, 1.0])

    ax_a = fig.add_subplot(top[0, 0])
    ax_b = fig.add_subplot(top[0, 1])
    ax_c = fig.add_subplot(bottom[0, 0])
    ax_d = fig.add_subplot(bottom[0, 1])

    v1.draw_panel_a(ax_a, dft)
    ax_a.set_title(
        "BSSE-corrected adsorption-energy ordering",
        loc="left",
        fontweight="bold",
        pad=4.0,
    )
    ax_a.set_xlabel(r"relative $\Delta E_{\mathrm{ads}}^{\mathrm{BSSE}}$ (eV I$_2^{-1}$)")
    ax_a.set_xlim(-0.67, 0.14)
    # Collision fix: the positive vacancy endpoint is placed above its marker,
    # leaving the inter-panel gutter text-free.
    vacancy_delta = float(
        dft.loc[dft["site"].eq("vacancy"), "delta_vs_basal_eV"].iloc[0]
    )
    for text in ax_a.texts:
        if text.get_text() == "+0.08":
            text.set_position((vacancy_delta, 0.22))
            text.set_ha("center")
            text.set_va("bottom")
    quiet_prior_panel(ax_a)

    v1.draw_panel_b(ax_b, md, band_min, band_max)
    ax_b.set_title("Bulk carrier mobility", loc="left", fontweight="bold", pad=4.0)
    ax_b.tick_params(axis="y", pad=1.2)
    quiet_prior_panel(ax_b)

    v1.draw_panel_c(ax_c, fiber, eps_endpoint)
    ax_c.set_title(
        "Geometric remaining-area bounds from single-fibre placement",
        loc="left",
        fontweight="bold",
        pad=5.0,
    )
    ax_c.set_ylabel(r"geometric remaining area, $A/A_0$")
    handles, labels = ax_c.get_legend_handles_labels()
    labels = [
        label.replace("sparse,", "sparse geometry,").replace("dense,", "dense geometry,")
        for label in labels
    ]
    legend = ax_c.legend(
        handles,
        labels,
        title="single-fibre comparator",
        loc="lower left",
        ncol=1,
        handlelength=1.5,
        handletextpad=0.45,
        borderaxespad=0.20,
        labelspacing=0.35,
    )
    legend.get_title().set_fontsize(v1.MIN_FONT_PT)
    for text in ax_c.texts:
        if text.get_text() == r"baseline range to $Q=120$":
            text.set_text(r"continuum $\varepsilon_s$ range to $Q=120$")
    ax_c.text(
        4.12,
        0.765,
        r"geometry only; native $A_{\mathrm{bare}}/A_0=R_\theta T_{\mathrm{pore}}$",
        ha="right",
        va="bottom",
        fontsize=v1.MIN_FONT_PT,
        color=v1.PALETTE["graphite"],
    )

    v1.draw_panel_d(ax_d, pore_raw, pore_zoom, pore_endpoints, eps_endpoint)
    ax_d.set_title(
        "Permeability bounds from pore-network placement",
        loc="left",
        fontweight="bold",
        pad=5.0,
    )
    return fig


def save_outputs_v2(fig: plt.Figure) -> list[Path]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    svg = OUT_BASE.with_suffix(".svg")
    pdf = OUT_BASE.with_suffix(".pdf")
    png = OUT_BASE.with_suffix(".png")
    tiff = OUT_BASE.with_suffix(".tiff")
    preview = OUT_DIR / "Fig_R582_multiscale_bounds_v2_180mm_preview.png"
    grayscale = OUT_DIR / "Fig_R582_multiscale_bounds_v2_grayscale_180mm.png"

    fig.savefig(svg, format="svg", metadata={"Date": None})
    fig.savefig(
        pdf,
        format="pdf",
        metadata={
            "Title": "R582 Figure 5 v2 - independent bounds on positive-electrode model inputs",
            "Author": "ZIFB R582 deterministic figure pipeline",
            "Creator": "matplotlib",
            "CreationDate": None,
            "ModDate": None,
        },
    )
    fig.savefig(
        png,
        format="png",
        dpi=600,
        metadata={"Software": "matplotlib; R582 deterministic figure pipeline v2"},
        pil_kwargs={"compress_level": 9},
    )
    fig.savefig(
        tiff,
        format="tiff",
        dpi=600,
        pil_kwargs={"compression": "tiff_lzw"},
    )
    with Image.open(tiff) as tiff_image:
        tiff_image.convert("RGB").save(
            tiff,
            format="TIFF",
            dpi=(600, 600),
            compression="tiff_lzw",
        )
    fig.savefig(
        preview,
        format="png",
        dpi=300,
        metadata={"Software": "matplotlib; R582 v2 180 mm final-size QA preview"},
        pil_kwargs={"compress_level": 9},
    )
    with Image.open(preview) as color_image:
        ImageOps.grayscale(color_image.convert("RGB")).convert("RGB").save(
            grayscale,
            format="PNG",
            dpi=(300, 300),
            compress_level=9,
        )
    return [svg, pdf, png, tiff, preview, grayscale]


def write_render_manifest_v2(
    source_manifest: pd.DataFrame,
    source_tables: list[Path],
    outputs: list[Path],
    eps_endpoint: float,
    band_min: float,
    band_max: float,
    endpoint_min: float,
    endpoint_max: float,
) -> None:
    preview_path = OUT_DIR / "Fig_R582_multiscale_bounds_v2_180mm_preview.png"
    with Image.open(preview_path) as preview:
        preview_size = list(preview.size)
    manifest = {
        "build_id": "R582_FIG5_MULTISCALE_BOUNDS_V2",
        "backend": "Python 3.11 / matplotlib 3.7.2",
        "overall_claim": "Independent molecular and mesoscale bounds on positive-electrode model inputs",
        "figure_role": "bounded priors and physical comparator families; not independent validation",
        "revision_from_v1": {
            "collision_fix": (
                "panel-a +0.08 label moved above the vacancy point; a/b use a dedicated wide gutter"
            ),
            "hierarchy_fix": (
                "a/b reduced to a quiet upper prior strip; c/d expanded as the positive-electrode hero row"
            ),
            "identity_repair": (
                "panel c is labelled as geometric A/A0; it is explicitly separated from the native "
                "COMSOL A_bare/A0 = R_theta*T_pore closure"
            ),
            "energy_label_repair": (
                "panel a is labelled as a BSSE-corrected adsorption-energy ordering"
            ),
            "numeric_values_changed": False,
        },
        "figure_size_mm": [WIDTH_MM, HEIGHT_MM],
        "preview_dpi": 300,
        "preview_pixels": preview_size,
        "font_family": "TeX Gyre Termes",
        "font_files": [str((v1.TERMES_DIR / name).name) for name in v1.TERMES_FILES],
        "base_font_pt": v1.BASE_FONT_PT,
        "minimum_font_pt": v1.MIN_FONT_PT,
        "panel_label_pt": v1.PANEL_FONT_PT,
        "input_files": source_manifest.to_dict(orient="records"),
        "source_tables": [
            {
                "path_workspace_relative": project_relative(path),
                "sha256": sha256(path),
            }
            for path in source_tables
        ],
        "output_files": [
            {
                "path_workspace_relative": project_relative(path),
                "sha256": sha256(path),
            }
            for path in outputs
        ],
        "numeric_checks": {
            "baseline_eps_s_endpoint": eps_endpoint,
            "low_end_D_eff_prior_1e9_m2_s": [band_min, band_max],
            "pore_network_K_over_K0_at_endpoint": [endpoint_min, endpoint_max],
            "dft_basal_reference_eV": 0.0,
            "single_fibre_geometric_identity": "geometric A/A0 = 1 - geometric removed fraction",
            "native_COMSOL_accessibility_identity": "A_bare/A0 = R_theta*T_pore",
            "native_COMSOL_coverage_identity": "R_theta = 1 - theta_cal",
            "native_COMSOL_transport_identity": "T_pore = (K/K0)^0.5",
        },
        "interpretation_boundaries": [
            "DFT values are relative BSSE-corrected adsorption energies for dry periodic single-I2 placements, not solution free energies or rates.",
            "MD values are force-field-limited bulk mobility priors; stability bars are not replicate SEM.",
            "Single-fibre curves report geometric A/A0 for assumed placement families; they are not the native COMSOL A_bare/A0 quantity and do not reveal deposit morphology.",
            "Pore-network curves are idealized permeability comparators, not measured pore closure.",
            "The native COMSOL identity is A_bare/A0 = R_theta*T_pore, with R_theta = 1 - theta_cal and T_pore = (K/K0)^0.5.",
            "No lower-scale panel supplies the voltage-calibrated R_theta relation.",
        ],
    }
    RENDER_MANIFEST_V2.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def main() -> None:
    v1.register_font()
    mpl.rcParams["svg.hashsalt"] = "R582-Fig5-multiscale-bounds-termes-v2"
    (
        source_manifest,
        dft,
        md,
        band_min,
        band_max,
        fiber,
        pore_raw,
        pore_zoom,
        pore_endpoints,
        eps_endpoint,
    ) = prepare_inputs()
    fig = build_figure_v2(
        dft,
        md,
        band_min,
        band_max,
        fiber,
        pore_raw,
        pore_zoom,
        pore_endpoints,
        eps_endpoint,
    )
    outputs = save_outputs_v2(fig)
    plt.close(fig)
    source_tables = [
        PANEL_A_CSV_V2,
        v1.PANEL_B_CSV,
        PANEL_C_CSV_V2,
        v1.PANEL_D_RAW_CSV,
        v1.PANEL_D_ZOOM_CSV,
        v1.PANEL_D_ENDPOINT_CSV,
        INPUT_MANIFEST_V2,
    ]
    write_render_manifest_v2(
        source_manifest,
        source_tables,
        outputs,
        eps_endpoint,
        band_min,
        band_max,
        float(pore_endpoints["K_hydraulic_rel"].min()),
        float(pore_endpoints["K_hydraulic_rel"].max()),
    )
    print(
        "Wrote R582 Figure 5 v2 with BSSE-corrected adsorption ordering and "
        "single-fibre geometric A/A0 kept distinct from native COMSOL accessibility."
    )


if __name__ == "__main__":
    main()
