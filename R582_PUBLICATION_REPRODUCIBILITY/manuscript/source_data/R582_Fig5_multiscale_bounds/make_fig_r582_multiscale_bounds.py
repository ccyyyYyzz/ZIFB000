"""Build R582 Figure 5: independent molecular and mesoscale bounds.

The figure is a deterministic, Python/matplotlib-only visual argument.  It
combines four registered lower-scale evidence classes without treating any of
them as an independent validation or a bottom-up replacement for the
voltage-calibrated accessibility relation used by the continuum model.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import font_manager
from matplotlib.lines import Line2D
from PIL import Image, ImageOps


SOURCE_DATA_DIR = Path(__file__).resolve().parent.parent
if str(SOURCE_DATA_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DATA_DIR))
from r582_font_runtime import FONT_FILENAMES, register_termes_fonts


SCRIPT_DIR = Path(__file__).resolve().parent
MANUSCRIPT_DIR = SCRIPT_DIR.parents[1]
PROJECT_ROOT = MANUSCRIPT_DIR.parent
OUT_DIR = MANUSCRIPT_DIR / "figures_R582"
OUT_BASE = OUT_DIR / "Fig_R582_multiscale_bounds"

DFT_INPUT = (
    PROJECT_ROOT
    / "DFT"
    / "06_periodic_cp2k_single_i2_r514"
    / "workspace_snapshot"
    / "outputs"
    / "r514_status1_short"
    / "tables"
    / "sanity_final_four_site_spectrum.csv"
)
MD_INPUT = (
    PROJECT_ROOT
    / "MD"
    / "carrier_diffusivity_si_figure"
    / "R197_FigS_md_carrier_diffusivity_source_summary.csv"
)
MD_RANGE_INPUT = (
    PROJECT_ROOT
    / "MD"
    / "carrier_diffusivity_si_figure"
    / "R197_FigS_md_carrier_diffusivity_summary.json"
)
FIBER_INPUT = PROJECT_ROOT / "fiber" / "data" / "R531_fiber3d_clock.csv"
PORE_INPUT = PROJECT_ROOT / "pore_system" / "data" / "R531_network3d_curves.csv"
PORE_THRESHOLD_INPUT = (
    PROJECT_ROOT / "pore_system" / "data" / "R531_network3d_thresholds.csv"
)
BASELINE_INPUT = (
    MANUSCRIPT_DIR
    / "source_data"
    / "Fig_R581_matched_closure"
    / "R581_release_closure_summary.json"
)

INPUT_HASHES = {
    DFT_INPUT: "1FC77A716EC8E1460A671FB18AA201F8E0E46A6ECA0DB646DEB596B1587E9CB2",
    MD_INPUT: "01DE06CA4D66719E5D614A66F3067B0916390A316C3F17C1F8A5C4E08DC832EB",
    MD_RANGE_INPUT: "86243B41D8B5164817BC25C39CAA18E8D09161FF1CEDF4A2C26A13D865A2C79C",
    FIBER_INPUT: "91D6B8DC78E2E4C7629311B7E776B6F549A56670FFDC50306C8CD092015F21DE",
    PORE_INPUT: "734503DB22CF7EDBE32521D823CC7E3ECCB2E8F8137DBF65B6160230379BBB17",
    PORE_THRESHOLD_INPUT: "FA3B9CA51C69832C5A1DE4AF5E650B314F3D5F504CF730874C01E5ABCEFAC3DF",
    BASELINE_INPUT: "A213CCDBADE269AD59FB8F2BBD74EAC9D5E28585CBBC6F7E42A1FD4939DC34AE",
}

INPUT_ROLES = {
    DFT_INPUT: "accepted periodic CP2K single-I2 site-energy ordering",
    MD_INPUT: "five-SOC bulk-MD carrier diffusivity means and stability bars",
    MD_RANGE_INPUT: "formal-charge carrier-proxy range used as the low-end D_eff prior",
    FIBER_INPUT: "single-fibre accessibility nodes for sparse and dense placement families",
    PORE_INPUT: "six pore-network hydraulic-permeability placement laws",
    PORE_THRESHOLD_INPUT: "linearly interpolated permeability values at the baseline endpoint",
    BASELINE_INPUT: "frozen baseline solid-I2 endpoint used to delimit the modeled range",
}

TERMES_DIR, _TERMES_BY_ROLE, FONT_FAMILY = register_termes_fonts(font_manager)
TERMES_FILES = tuple(FONT_FILENAMES.values())

WIDTH_MM = 180.0
HEIGHT_MM = 125.0
MM_PER_INCH = 25.4
BASE_FONT_PT = 7.2
MIN_FONT_PT = 6.5
PANEL_FONT_PT = 8.0

PALETTE = {
    "graphite": "#4D4D4D",
    "ink": "#242424",
    "light": "#D9D9D9",
    "lighter": "#EEEEEE",
    "vermilion": "#D65345",
    "blue": "#3B6FB6",
    "teal": "#2A9D8F",
    "violet": "#7A68A6",
    "amber": "#D8912B",
    "cyan": "#67A9B7",
}

PANEL_A_CSV = SCRIPT_DIR / "R582_Fig5_panel_a_dft_site_ordering.csv"
PANEL_B_CSV = SCRIPT_DIR / "R582_Fig5_panel_b_md_diffusivity.csv"
PANEL_C_CSV = SCRIPT_DIR / "R582_Fig5_panel_c_accessibility_families.csv"
PANEL_D_RAW_CSV = SCRIPT_DIR / "R582_Fig5_panel_d_permeability_raw.csv"
PANEL_D_ZOOM_CSV = SCRIPT_DIR / "R582_Fig5_panel_d_permeability_zoom.csv"
PANEL_D_ENDPOINT_CSV = SCRIPT_DIR / "R582_Fig5_panel_d_endpoint_summary.csv"
INPUT_MANIFEST_CSV = SCRIPT_DIR / "R582_Fig5_input_manifest.csv"
RENDER_MANIFEST_JSON = SCRIPT_DIR / "R582_Fig5_render_manifest.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def project_relative(path: Path) -> str:
    return path.resolve().relative_to(PROJECT_ROOT.resolve()).as_posix()


def register_font() -> None:
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
            "svg.hashsalt": "R582-Fig5-multiscale-bounds-termes-v1",
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


def validate_inputs() -> pd.DataFrame:
    rows = []
    for path, expected in INPUT_HASHES.items():
        if not path.is_file():
            raise FileNotFoundError(f"Required read-only source is missing: {path}")
        observed = sha256(path)
        if observed != expected:
            raise RuntimeError(
                f"Input changed: {project_relative(path)}; expected {expected}, observed {observed}"
            )
        rows.append(
            {
                "input_role": INPUT_ROLES[path],
                "path_workspace_relative": project_relative(path),
                "sha256": observed,
                "access": "read-only",
            }
        )
    manifest = pd.DataFrame(rows)
    manifest.to_csv(INPUT_MANIFEST_CSV, index=False, lineterminator="\n")
    return manifest


def prepare_panel_a() -> pd.DataFrame:
    source = pd.read_csv(DFT_INPUT)
    required = {
        "site_id",
        "label",
        "E_ads_D3_plus_PBE_BSSE_eV",
        "delta_vs_basal_eV",
        "confidence",
        "paper_use",
        "source",
    }
    if not required.issubset(source.columns):
        raise ValueError(f"DFT table is missing: {sorted(required.difference(source.columns))}")
    if len(source) != 4 or set(source["confidence"]) != {"high"}:
        raise ValueError("The accepted four-site DFT spectrum changed.")

    name_map = {
        "OH_functionalized_basal_periodic_slab": "C-OH",
        "carbonyl_edge_periodic_ribbon": "C=O",
        "basal_pristine_periodic_slab": "basal",
        "single_vacancy_periodic_slab": "vacancy",
    }
    out = source[
        [
            "site_id",
            "E_ads_D3_plus_PBE_BSSE_eV",
            "delta_vs_basal_eV",
            "confidence",
            "paper_use",
            "source",
        ]
    ].copy()
    out["site"] = out["site_id"].map(name_map)
    if out["site"].isna().any():
        raise ValueError("Unexpected DFT site identifier.")
    out["evidence_role"] = "relative periodic electronic-energy placement prior"
    order = {"C-OH": 0, "C=O": 1, "basal": 2, "vacancy": 3}
    out["display_order"] = out["site"].map(order)
    out = out.sort_values("display_order").reset_index(drop=True)
    if not np.allclose(
        out["delta_vs_basal_eV"].to_numpy(),
        [-0.5951218941418805, -0.4456350366497152, 0.0, 0.08413405676355457],
        rtol=0,
        atol=1e-12,
    ):
        raise ValueError("Accepted DFT relative ordering changed.")
    out.to_csv(PANEL_A_CSV, index=False, float_format="%.15g", lineterminator="\n")
    return out


def prepare_panel_b() -> tuple[pd.DataFrame, float, float]:
    source = pd.read_csv(MD_INPUT)
    required = {"variant", "species", "D_mean", "D_sem", "D_min", "D_max", "n_soc"}
    if not required.issubset(source.columns):
        raise ValueError(f"MD table is missing: {sorted(required.difference(source.columns))}")
    selected = source.loc[
        source["variant"].isin(["q0p8_ecc", "q1p0"])
        & source["species"].isin(["I-", "I3-", "I2Br-"]),
        ["variant", "species", "D_mean", "D_sem", "D_min", "D_max", "n_soc"],
    ].copy()
    if len(selected) != 6 or set(selected["n_soc"].astype(int)) != {5}:
        raise ValueError("Expected two charge variants for three species and five SOC boxes.")
    selected["charge_scaling"] = selected["variant"].map(
        {"q0p8_ecc": "q=0.8 ECC", "q1p0": "q=1.0 formal charges"}
    )
    selected["uncertainty_definition"] = (
        "propagated four-block within-trajectory stability; not independent-replicate SEM"
    )
    selected["evidence_role"] = "force-field-limited bulk mobility prior"
    order = {"I-": 0, "I3-": 1, "I2Br-": 2}
    variant_order = {"q1p0": 0, "q0p8_ecc": 1}
    selected["display_order"] = selected["species"].map(order)
    selected["variant_order"] = selected["variant"].map(variant_order)
    selected = selected.sort_values(["display_order", "variant_order"]).reset_index(drop=True)

    with MD_RANGE_INPUT.open("r", encoding="utf-8") as handle:
        range_source = json.load(handle)
    formal = next(row for row in range_source["ranges"] if row["variant"] == "q1p0")
    band_min = float(formal["carrier_proxy_min"])
    band_max = float(formal["carrier_proxy_max"])
    if not np.allclose(
        [band_min, band_max],
        [0.4247422118830672, 0.6642746646066889],
        rtol=0,
        atol=1e-12,
    ):
        raise ValueError("The formal-charge carrier-proxy prior range changed.")
    selected["low_end_D_eff_prior_min_1e9_m2_s"] = band_min
    selected["low_end_D_eff_prior_max_1e9_m2_s"] = band_max
    selected.to_csv(PANEL_B_CSV, index=False, float_format="%.15g", lineterminator="\n")
    return selected, band_min, band_max


def prepare_panel_c() -> pd.DataFrame:
    source = pd.read_csv(FIBER_INPUT)
    required = {"label", "phi_ppt", "n_n_m2", "eps_s", "accessibility", "theta_eff_transport"}
    if not required.issubset(source.columns):
        raise ValueError(f"Fibre table is missing: {sorted(required.difference(source.columns))}")
    selected = source.loc[
        source["label"].isin(["baseline_lowNn", "retained_highNn"]),
        [
            "label",
            "phi_ppt",
            "n_n_m2",
            "Q_mAh_cm2",
            "eps_s",
            "accessibility",
            "theta_eff_transport",
        ],
    ].copy()
    if len(selected) != 10:
        raise ValueError("Expected five computed nodes in each physical placement family.")
    selected["family"] = selected["label"].map(
        {"baseline_lowNn": "sparse placement", "retained_highNn": "dense placement"}
    )
    selected["point_role"] = "computed single-fibre node"
    origin = pd.DataFrame(
        [
            {
                "label": "baseline_lowNn",
                "phi_ppt": 0.005,
                "n_n_m2": 1.0e11,
                "Q_mAh_cm2": 0.0,
                "eps_s": 0.0,
                "accessibility": 1.0,
                "theta_eff_transport": 0.0,
                "family": "sparse placement",
                "point_role": "zero-solid boundary by definition",
            },
            {
                "label": "retained_highNn",
                "phi_ppt": 0.020,
                "n_n_m2": 1.0e14,
                "Q_mAh_cm2": 0.0,
                "eps_s": 0.0,
                "accessibility": 1.0,
                "theta_eff_transport": 0.0,
                "family": "dense placement",
                "point_role": "zero-solid boundary by definition",
            },
        ]
    )
    out = pd.concat([origin, selected], ignore_index=True)
    out["evidence_role"] = "physical single-fibre accessibility comparator"
    out = out.sort_values(["family", "eps_s"]).reset_index(drop=True)
    if set(out.loc[out["eps_s"] > 0, "n_n_m2"].astype(float)) != {1.0e11, 1.0e14}:
        raise ValueError("Sparse/dense placement densities changed.")
    if not np.allclose(out["accessibility"] + out["theta_eff_transport"], 1.0, atol=1e-12):
        raise ValueError("Accessibility complement identity failed.")
    out.to_csv(PANEL_C_CSV, index=False, float_format="%.15g", lineterminator="\n")
    return out


def prepare_panel_d(
    eps_endpoint: float,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    source = pd.read_csv(PORE_INPUT)
    thresholds = pd.read_csv(PORE_THRESHOLD_INPUT)
    required = {"law", "eps_s", "K_hydraulic_rel"}
    if not required.issubset(source.columns):
        raise ValueError(f"Pore table is missing: {sorted(required.difference(source.columns))}")
    laws = sorted(source["law"].unique())
    if len(laws) != 6 or set(laws) != set(thresholds["law"]):
        raise ValueError("Expected the six registered pore-network placement laws.")

    raw = source[["law", "retained_pore_fraction", "eps_s", "K_hydraulic_rel"]].copy()
    raw["evidence_role"] = "physical pore-network permeability comparator"
    raw.to_csv(PANEL_D_RAW_CSV, index=False, float_format="%.15g", lineterminator="\n")

    eps_grid = np.linspace(0.0, eps_endpoint, 121)
    zoom_rows = []
    endpoint_rows = []
    threshold_eps = float(thresholds["f_at_comsol"].iloc[0]) * 0.85
    if not np.isclose(threshold_eps, 3.22e-3, rtol=0, atol=1e-15):
        raise ValueError(f"Registered pore-network link point changed: {threshold_eps}")
    for law in laws:
        group = raw.loc[raw["law"].eq(law)].sort_values("eps_s")
        k_grid = np.interp(eps_grid, group["eps_s"], group["K_hydraulic_rel"])
        for eps_s, k_value in zip(eps_grid, k_grid):
            zoom_rows.append(
                {
                    "law": law,
                    "eps_s": eps_s,
                    "K_hydraulic_rel_linear_interpolation": k_value,
                    "interpolation_scope": "between the registered zero and first nonzero network nodes",
                }
            )
        k_endpoint = float(k_grid[-1])
        threshold_value = float(
            thresholds.loc[thresholds["law"].eq(law), "K_hydraulic_at_comsol_eps_s"].iloc[0]
        )
        threshold_recomputed = float(
            np.interp(threshold_eps, group["eps_s"], group["K_hydraulic_rel"])
        )
        if not np.isclose(threshold_recomputed, threshold_value, rtol=0, atol=2e-10):
            raise ValueError(
                f"Registered link-point interpolation mismatch for {law}: "
                f"{threshold_recomputed} vs {threshold_value}"
            )
        endpoint_rows.append(
            {
                "law": law,
                "eps_s_endpoint": eps_endpoint,
                "K_hydraulic_rel": k_endpoint,
                "registered_link_eps_s": threshold_eps,
                "K_hydraulic_rel_at_registered_link": threshold_recomputed,
                "source_check": "registered 0.00322 link value reproduced; plotted at exact frozen endpoint",
            }
        )
    zoom = pd.DataFrame(zoom_rows)
    endpoints = pd.DataFrame(endpoint_rows)
    if not np.allclose(
        [endpoints["K_hydraulic_rel"].min(), endpoints["K_hydraulic_rel"].max()],
        [0.9814684469568599, 0.9918265360078787],
        rtol=0,
        atol=2e-10,
    ):
        raise ValueError("Pore-network endpoint envelope changed.")
    zoom.to_csv(PANEL_D_ZOOM_CSV, index=False, float_format="%.15g", lineterminator="\n")
    endpoints.to_csv(
        PANEL_D_ENDPOINT_CSV, index=False, float_format="%.15g", lineterminator="\n"
    )
    return raw, zoom, endpoints


def get_baseline_endpoint() -> float:
    with BASELINE_INPUT.open("r", encoding="utf-8") as handle:
        release = json.load(handle)
    value = float(
        release["control_reproduction_gate"]["historical"]["endpoint"]["eps_s_avg"]
    )
    if not np.isclose(value, 3.21926062394e-3, rtol=0, atol=1e-15):
        raise ValueError(f"Frozen baseline endpoint changed: {value}")
    return value


def style_axis(ax: plt.Axes) -> None:
    ax.tick_params(direction="out", colors=PALETTE["ink"], pad=2.2)
    ax.spines["left"].set_color(PALETTE["ink"])
    ax.spines["bottom"].set_color(PALETTE["ink"])
    ax.xaxis.label.set_color(PALETTE["ink"])
    ax.yaxis.label.set_color(PALETTE["ink"])


def panel_label(ax: plt.Axes, label: str, x: float = -0.12, y: float = 1.08) -> None:
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


def draw_panel_a(ax: plt.Axes, data: pd.DataFrame) -> None:
    y = np.arange(len(data))[::-1]
    values = data["delta_vs_basal_eV"].to_numpy()
    sites = data["site"].tolist()
    colors = [
        PALETTE["amber"],
        PALETTE["amber"],
        PALETTE["graphite"],
        PALETTE["graphite"],
    ]
    for yi, value, color, site in zip(y, values, colors, sites):
        ax.plot([0.0, value], [yi, yi], color=color, lw=1.35, zorder=1)
        face = "white" if site == "basal" else color
        ax.scatter(
            [value],
            [yi],
            s=24,
            facecolor=face,
            edgecolor=color,
            linewidth=0.9,
            zorder=2,
        )
        offset = -0.024 if value <= 0 else 0.022
        ax.text(
            value + offset,
            yi,
            f"{value:+.2f}" if not np.isclose(value, 0) else "0",
            ha="right" if value <= 0 else "left",
            va="center",
            fontsize=MIN_FONT_PT,
            color=PALETTE["ink"],
        )
    ax.axvline(0, color=PALETTE["light"], lw=0.8, zorder=0)
    ax.set_yticks(y)
    ax.set_yticklabels(["C-OH", "C=O", "basal", "vacancy"])
    ax.set_xlim(-0.67, 0.16)
    ax.set_ylim(-0.55, 3.55)
    ax.set_xticks([-0.6, -0.4, -0.2, 0.0])
    ax.set_xlabel(r"relative electronic energy, $\Delta E_{\mathrm{ads}}$ (eV I$_2^{-1}$)")
    ax.set_title("Single-I$_2$ placement prior", loc="left", fontweight="bold", pad=5)
    panel_label(ax, "a")
    style_axis(ax)


def draw_panel_b(ax: plt.Axes, data: pd.DataFrame, band_min: float, band_max: float) -> None:
    species_order = ["I-", "I3-", "I2Br-"]
    species_labels = {"I-": "I$^-$", "I3-": "I$_3^-$", "I2Br-": "I$_2$Br$^-$"}
    y_base = {species: 2 - index for index, species in enumerate(species_order)}
    style = {
        "q0p8_ecc": {"marker": "o", "mfc": PALETTE["blue"], "mec": PALETTE["blue"], "offset": 0.10},
        "q1p0": {"marker": "D", "mfc": "white", "mec": PALETTE["graphite"], "offset": -0.10},
    }
    ax.axvspan(band_min, band_max, color=PALETTE["amber"], alpha=0.14, lw=0, zorder=0)
    ax.axvline(0.50, color=PALETTE["amber"], lw=0.8, ls=(0, (2.2, 1.7)), zorder=0)
    for variant, group in data.groupby("variant", sort=False):
        cfg = style[variant]
        for _, row in group.iterrows():
            yi = y_base[row["species"]] + cfg["offset"]
            color = PALETTE["graphite"] if row["species"] == "I-" else PALETTE["violet"]
            mfc = cfg["mfc"] if variant == "q0p8_ecc" else "white"
            mec = color if variant == "q0p8_ecc" else PALETTE["graphite"]
            ax.errorbar(
                row["D_mean"],
                yi,
                xerr=row["D_sem"],
                fmt=cfg["marker"],
                ms=4.0,
                mfc=mfc if row["species"] == "I-" else (PALETTE["violet"] if variant == "q0p8_ecc" else "white"),
                mec=mec,
                mew=0.8,
                ecolor=color,
                elinewidth=0.8,
                capsize=1.7,
                capthick=0.8,
                zorder=3,
            )
    ax.text(
        (band_min + band_max) / 2,
        2.48,
        "low-end $D_{\mathrm{eff}}$ prior",
        ha="center",
        va="center",
        fontsize=MIN_FONT_PT,
        color="#8B631A",
    )
    legend_handles = [
        Line2D(
            [0],
            [0],
            marker="o",
            color="none",
            markerfacecolor=PALETTE["graphite"],
            markeredgecolor=PALETTE["graphite"],
            markersize=4.0,
            label="filled circle: $q=0.8$ ECC",
        ),
        Line2D(
            [0],
            [0],
            marker="D",
            color="none",
            markerfacecolor="white",
            markeredgecolor=PALETTE["graphite"],
            markersize=3.7,
            label="open diamond: $q=1.0$ formal",
        ),
    ]
    ax.legend(
        handles=legend_handles,
        loc="lower right",
        ncol=1,
        handletextpad=0.35,
        borderaxespad=0.15,
        labelspacing=0.3,
    )
    ax.set_yticks([2, 1, 0])
    ax.set_yticklabels([species_labels[s] for s in species_order])
    ax.set_xlim(0.35, 1.34)
    ax.set_ylim(-0.47, 2.63)
    ax.set_xticks([0.4, 0.6, 0.8, 1.0, 1.2])
    ax.set_xlabel(r"bulk self-diffusivity, $D$ ($10^{-9}$ m$^2$ s$^{-1}$)")
    ax.set_title("Carrier-mobility prior", loc="left", fontweight="bold", pad=5)
    panel_label(ax, "b")
    style_axis(ax)


def draw_panel_c(ax: plt.Axes, data: pd.DataFrame, eps_endpoint: float) -> None:
    styles = {
        "sparse placement": {"color": PALETTE["teal"], "marker": "o", "label": r"sparse, $N=10^{11}$ m$^{-2}$"},
        "dense placement": {"color": PALETTE["violet"], "marker": "^", "label": r"dense, $N=10^{14}$ m$^{-2}$"},
    }
    ax.axvspan(0.0, eps_endpoint * 1e3, color=PALETTE["blue"], alpha=0.055, lw=0, zorder=0)
    ax.axvline(
        eps_endpoint * 1e3,
        color=PALETTE["blue"],
        lw=0.9,
        ls=(0, (2.4, 1.8)),
        zorder=1,
    )
    for family, cfg in styles.items():
        group = data.loc[data["family"].eq(family)].sort_values("eps_s")
        within = group.loc[group["eps_s"] <= 4.2e-3]
        ax.plot(
            within["eps_s"] * 1e3,
            within["accessibility"],
            color=cfg["color"],
            lw=1.45,
            marker=cfg["marker"],
            ms=4.1,
            mec="white",
            mew=0.45,
            label=cfg["label"],
            zorder=3,
        )
    ax.axhline(0.5, color=PALETTE["light"], lw=0.7, zorder=0)
    ax.text(
        eps_endpoint * 1e3 - 0.05,
        1.012,
        r"baseline range to $Q=120$",
        ha="right",
        va="bottom",
        fontsize=MIN_FONT_PT,
        color=PALETTE["blue"],
    )
    ax.legend(
        loc="lower left",
        ncol=1,
        handlelength=1.5,
        handletextpad=0.45,
        borderaxespad=0.20,
        labelspacing=0.35,
    )
    ax.set_xlim(0.0, 4.2)
    ax.set_ylim(0.24, 1.045)
    ax.set_xticks([0, 1, 2, 3, 4])
    ax.set_yticks([0.3, 0.5, 0.7, 0.9, 1.0])
    ax.set_xlabel(r"solid-I$_2$ fraction, $\varepsilon_s$ ($10^{-3}$)")
    ax.set_ylabel(r"remaining accessible area, $A_{\mathrm{bare}}/A_0$")
    ax.set_title("Single-fibre accessibility comparators", loc="left", fontweight="bold", pad=5)
    panel_label(ax, "c", x=-0.10, y=1.07)
    style_axis(ax)


def draw_panel_d(
    ax: plt.Axes,
    raw: pd.DataFrame,
    zoom: pd.DataFrame,
    endpoints: pd.DataFrame,
    eps_endpoint: float,
) -> None:
    pivot = zoom.pivot(index="eps_s", columns="law", values="K_hydraulic_rel_linear_interpolation")
    eps = pivot.index.to_numpy()
    k_min = pivot.min(axis=1).to_numpy()
    k_max = pivot.max(axis=1).to_numpy()
    k_median = pivot.median(axis=1).to_numpy()
    ax.fill_between(
        eps * 1e3,
        k_min,
        k_max,
        color=PALETTE["cyan"],
        alpha=0.27,
        linewidth=0,
        label="six-law envelope",
        zorder=1,
    )
    ax.plot(eps * 1e3, k_median, color=PALETTE["graphite"], lw=1.25, zorder=2)
    end_min = float(endpoints["K_hydraulic_rel"].min())
    end_max = float(endpoints["K_hydraulic_rel"].max())
    ax.plot(
        [eps_endpoint * 1e3, eps_endpoint * 1e3],
        [end_min, end_max],
        color=PALETTE["blue"],
        lw=1.2,
        zorder=3,
    )
    ax.plot(
        [eps_endpoint * 1e3 - 0.055, eps_endpoint * 1e3 + 0.055],
        [end_min, end_min],
        color=PALETTE["blue"],
        lw=1.2,
        zorder=3,
    )
    ax.plot(
        [eps_endpoint * 1e3 - 0.055, eps_endpoint * 1e3 + 0.055],
        [end_max, end_max],
        color=PALETTE["blue"],
        lw=1.2,
        zorder=3,
    )
    ax.text(
        eps_endpoint * 1e3 - 0.06,
        0.9791,
        f"{end_min:.3f}-{end_max:.3f}",
        ha="right",
        va="bottom",
        fontsize=MIN_FONT_PT,
        color=PALETTE["blue"],
    )
    ax.axhline(1.0, color=PALETTE["light"], lw=0.7, zorder=0)
    ax.set_xlim(0.0, 3.48)
    ax.set_ylim(0.978, 1.0018)
    ax.set_xticks([0, 1, 2, 3])
    ax.set_yticks([0.98, 0.99, 1.00])
    ax.set_xlabel(r"solid-I$_2$ fraction, $\varepsilon_s$ ($10^{-3}$)")
    ax.set_ylabel(r"relative permeability, $K/K_0$")
    ax.set_title("Pore-network permeability", loc="left", fontweight="bold", pad=5)
    panel_label(ax, "d", x=-0.15, y=1.07)
    style_axis(ax)

    full = raw.pivot(index="eps_s", columns="law", values="K_hydraulic_rel")
    full_eps = full.index.to_numpy()
    full_min = full.min(axis=1).to_numpy()
    full_max = full.max(axis=1).to_numpy()
    full_median = full.median(axis=1).to_numpy()
    inset = ax.inset_axes([0.10, 0.12, 0.47, 0.43])
    inset.fill_between(full_eps, full_min, full_max, color=PALETTE["cyan"], alpha=0.25, lw=0)
    inset.plot(full_eps, full_median, color=PALETTE["graphite"], lw=0.9)
    inset.set_xlim(0, 0.425)
    inset.set_ylim(0, 1.02)
    inset.set_xticks([0, 0.2, 0.4])
    inset.set_yticks([0, 0.5, 1.0])
    inset.tick_params(labelsize=MIN_FONT_PT, direction="out", pad=1.3, length=2.1, width=0.55)
    inset.spines["top"].set_visible(False)
    inset.spines["right"].set_visible(False)
    inset.spines["left"].set_linewidth(0.55)
    inset.spines["bottom"].set_linewidth(0.55)
    inset.set_title("full network range", fontsize=MIN_FONT_PT, loc="left", pad=2.5)


def build_figure(
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
    grid = fig.add_gridspec(
        2,
        12,
        left=0.082,
        right=0.986,
        bottom=0.105,
        top=0.955,
        hspace=0.50,
        wspace=1.20,
        height_ratios=[0.82, 1.18],
    )
    ax_a = fig.add_subplot(grid[0, 0:6])
    ax_b = fig.add_subplot(grid[0, 6:12])
    ax_c = fig.add_subplot(grid[1, 0:7])
    ax_d = fig.add_subplot(grid[1, 7:12])

    draw_panel_a(ax_a, dft)
    draw_panel_b(ax_b, md, band_min, band_max)
    draw_panel_c(ax_c, fiber, eps_endpoint)
    draw_panel_d(ax_d, pore_raw, pore_zoom, pore_endpoints, eps_endpoint)
    return fig


def save_outputs(fig: plt.Figure) -> list[Path]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    svg = OUT_BASE.with_suffix(".svg")
    pdf = OUT_BASE.with_suffix(".pdf")
    png = OUT_BASE.with_suffix(".png")
    tiff = OUT_BASE.with_suffix(".tiff")
    preview = OUT_DIR / "Fig_R582_multiscale_bounds_180mm_preview.png"
    grayscale = OUT_DIR / "Fig_R582_multiscale_bounds_grayscale_180mm.png"

    fig.savefig(svg, format="svg", metadata={"Date": None})
    fig.savefig(
        pdf,
        format="pdf",
        metadata={
            "Title": "R582 Figure 5 - independent molecular and mesoscale bounds",
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
        metadata={"Software": "matplotlib; R582 deterministic figure pipeline"},
        pil_kwargs={"compress_level": 9},
    )
    fig.savefig(
        tiff,
        format="tiff",
        dpi=600,
        pil_kwargs={"compression": "tiff_lzw"},
    )
    # Matplotlib's TIFF writer retains an alpha channel even on a white canvas.
    # Re-save through Pillow so the journal deliverable is explicitly opaque RGB.
    with Image.open(tiff) as tiff_image:
        opaque_tiff = tiff_image.convert("RGB")
        opaque_tiff.save(
            tiff,
            format="TIFF",
            dpi=(600, 600),
            compression="tiff_lzw",
        )
    fig.savefig(
        preview,
        format="png",
        dpi=300,
        metadata={"Software": "matplotlib; 180 mm final-size QA preview"},
        pil_kwargs={"compress_level": 9},
    )
    with Image.open(preview) as color_image:
        gray = ImageOps.grayscale(color_image.convert("RGB")).convert("RGB")
        gray.save(
            grayscale,
            format="PNG",
            dpi=(300, 300),
            compress_level=9,
        )
    return [svg, pdf, png, tiff, preview, grayscale]


def write_render_manifest(
    source_manifest: pd.DataFrame,
    source_tables: list[Path],
    outputs: list[Path],
    eps_endpoint: float,
    band_min: float,
    band_max: float,
    endpoint_min: float,
    endpoint_max: float,
) -> None:
    with Image.open(OUT_DIR / "Fig_R582_multiscale_bounds_180mm_preview.png") as preview:
        preview_size = list(preview.size)
    manifest = {
        "build_id": "R582_FIG5_MULTISCALE_BOUNDS_V1",
        "backend": "Python 3.11 / matplotlib 3.7.2",
        "figure_role": "bounded priors and physical comparator families; not independent validation",
        "figure_size_mm": [WIDTH_MM, HEIGHT_MM],
        "preview_dpi": 300,
        "preview_pixels": preview_size,
        "font_family": "TeX Gyre Termes",
        "font_files": [str((TERMES_DIR / name).name) for name in TERMES_FILES],
        "base_font_pt": BASE_FONT_PT,
        "minimum_font_pt": MIN_FONT_PT,
        "panel_label_pt": PANEL_FONT_PT,
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
            "accessibility_identity": "A_bare/A0 = 1 - theta_eff_transport",
        },
        "interpretation_boundaries": [
            "DFT values are relative periodic electronic energies, not solution free energies or rates.",
            "MD values are force-field-limited bulk mobility priors; stability bars are not replicate SEM.",
            "Single-fibre curves are assumed placement-family comparators, not observed deposit morphology.",
            "Pore-network curves are idealized permeability comparators, not measured pore closure.",
            "No lower-scale panel supplies the voltage-calibrated continuum accessibility relation.",
        ],
    }
    RENDER_MANIFEST_JSON.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def main() -> None:
    register_font()
    source_manifest = validate_inputs()
    eps_endpoint = get_baseline_endpoint()
    dft = prepare_panel_a()
    md, band_min, band_max = prepare_panel_b()
    fiber = prepare_panel_c()
    pore_raw, pore_zoom, pore_endpoints = prepare_panel_d(eps_endpoint)
    fig = build_figure(
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
    outputs = save_outputs(fig)
    plt.close(fig)
    source_tables = [
        PANEL_A_CSV,
        PANEL_B_CSV,
        PANEL_C_CSV,
        PANEL_D_RAW_CSV,
        PANEL_D_ZOOM_CSV,
        PANEL_D_ENDPOINT_CSV,
        INPUT_MANIFEST_CSV,
    ]
    write_render_manifest(
        source_manifest,
        source_tables,
        outputs,
        eps_endpoint,
        band_min,
        band_max,
        float(pore_endpoints["K_hydraulic_rel"].min()),
        float(pore_endpoints["K_hydraulic_rel"].max()),
    )
    print("Wrote R582 Figure 5 molecular/mesoscale bounds bundle.")


if __name__ == "__main__":
    main()
