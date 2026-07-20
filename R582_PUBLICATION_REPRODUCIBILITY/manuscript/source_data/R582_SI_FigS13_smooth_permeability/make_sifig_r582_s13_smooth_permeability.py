#!/usr/bin/env python
"""Build R582 Supplementary Figure S13 from the immutable R537 export.

The matched re-solves differ only in the smooth bulk-permeability relation.
This control does not resolve or exclude local pore-throat blockage.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from r582_si_figure_tools import (
    BLUE,
    CARMINE,
    INK,
    MID_GREY,
    NAVY,
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
PROJECT = HERE.parents[2]
FIGURE_DIR = PROJECT / "manuscript" / "figures_R582"
FIGURE_DIR.mkdir(parents=True, exist_ok=True)
STEM = "SIFig_R582_S13_smooth_permeability"
WIDTH_MM = 180.0
HEIGHT_MM = 70.0
FAMILY = configure_font(STEM)

RAW_EXPORT = HERE / "inputs" / "R537_kperm_inject_raw.txt"
REGISTERED_TABLE = HERE / "inputs" / "R537_kperm_injection.csv"
EXPECTED_SHA256 = {
    RAW_EXPORT: "02BB6DCF33D90F3A08DC8C687E15F87D336064C7F2A567B47319012C51D872D1",
    REGISTERED_TABLE: "2ABD6430B0B203326FB7301D03DFE0DB7DE9CA7FFCC17EC53C96EFD0561C9E68",
}
REGISTERED_SOURCES = {
    RAW_EXPORT: "manuscript/source_data/Fig_R537_kperm_injection/R537_kperm_inject_raw.txt",
    REGISTERED_TABLE: "manuscript/source_data/Fig_R537_kperm_injection/R537_kperm_injection.csv",
}
PLOT_TABLE = HERE / "R582_SIFig_S13_smooth_permeability.csv"
SUMMARY_TABLE = HERE / "R582_SIFig_S13_summary.csv"
INPUT_MANIFEST = HERE / "R582_SIFig_S13_input_manifest.csv"
RENDER_MANIFEST = HERE / "R582_SIFig_S13_render_manifest.json"


def rel(path: Path) -> str:
    return path.resolve().relative_to(PROJECT.resolve()).as_posix()


def verify_inputs() -> None:
    rows = []
    for path, expected in EXPECTED_SHA256.items():
        if not path.is_file():
            raise FileNotFoundError(path)
        observed = sha256(path)
        if observed != expected:
            raise ValueError(f"Frozen input hash mismatch for {path}: {observed}")
        rows.append(
            {
                "source_key": path.stem,
                "frozen_copy": rel(path),
                "registered_source": REGISTERED_SOURCES[path],
                "size_bytes": path.stat().st_size,
                "sha256": observed,
                "used_for": "raw matched re-solve trace" if path == RAW_EXPORT else "registered parsed cross-check",
                "immutable_registered_input": True,
            }
        )
    pd.DataFrame(rows).to_csv(INPUT_MANIFEST, index=False, lineterminator="\n")


def parse_raw() -> dict[str, pd.DataFrame]:
    records: dict[str, list[list[float]]] = {"baseline_KC": [], "network_cpath": []}
    with RAW_EXPORT.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if not line.startswith("TR,"):
                continue
            parts = line.strip().split(",")
            if len(parts) < 6 or parts[1] not in records:
                continue
            try:
                records[parts[1]].append([float(value) if value else np.nan for value in parts[2:6]])
            except ValueError:
                continue
    result = {
        key: pd.DataFrame(values, columns=["Q", "V", "K_perm_rel", "eps_s"]).dropna().reset_index(drop=True)
        for key, values in records.items()
    }
    return result


def prepare_data() -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    verify_inputs()
    parsed = parse_raw()
    baseline = parsed["baseline_KC"]
    network = parsed["network_cpath"]
    if len(baseline) != 1081 or len(network) != 1081:
        raise ValueError(f"Expected 1081 rows per matched path, found {len(baseline)} and {len(network)}")
    if not np.allclose(baseline["Q"], network["Q"], atol=1e-12, rtol=0.0):
        raise ValueError("Matched path capacities are not aligned")
    if not np.all(np.diff(baseline["Q"].to_numpy(float)) > 0):
        raise ValueError("Capacity coordinate is not strictly ordered")

    plot = pd.DataFrame(
        {
            "Q_mAh_cm2": baseline["Q"],
            "V_baseline_KC_V": baseline["V"],
            "V_network_smooth_path_V": network["V"],
            "DeltaV_network_minus_KC_mV": 1000.0 * (network["V"] - baseline["V"]),
            "K_over_K0_baseline_KC": baseline["K_perm_rel"],
            "K_over_K0_network_smooth_path": network["K_perm_rel"],
            "eps_s_baseline_KC": baseline["eps_s"],
            "eps_s_network_smooth_path": network["eps_s"],
        }
    )
    registered = pd.read_csv(REGISTERED_TABLE)
    required = [
        "Q",
        "V_baseline_KC",
        "V_network_cpath",
        "dV_mV",
        "K_perm_rel_KC",
        "K_perm_rel_network",
        "eps_s",
    ]
    if len(registered) != 1081 or not set(required).issubset(registered.columns):
        raise ValueError("Registered R537 parsed table schema mismatch")
    comparisons = {
        "Q": plot["Q_mAh_cm2"],
        "V_baseline_KC": plot["V_baseline_KC_V"],
        "V_network_cpath": plot["V_network_smooth_path_V"],
        "dV_mV": plot["DeltaV_network_minus_KC_mV"],
        "K_perm_rel_KC": plot["K_over_K0_baseline_KC"],
        "K_perm_rel_network": plot["K_over_K0_network_smooth_path"],
        "eps_s": plot["eps_s_baseline_KC"],
    }
    max_errors = {}
    for column, values in comparisons.items():
        error = float(np.max(np.abs(registered[column].to_numpy(float) - values.to_numpy(float))))
        max_errors[column] = error
        tolerance = 5.1e-8 if column != "dV_mV" else 5.1e-5
        if error > tolerance:
            raise ValueError(f"Raw/registered reconstruction failed for {column}: {error}")

    plot["evidence_class"] = "E-SIM"
    plot.to_csv(PLOT_TABLE, index=False, float_format="%.12g", lineterminator="\n")
    delta = plot["DeltaV_network_minus_KC_mV"].to_numpy(float)
    max_index = int(np.argmax(np.abs(delta)))
    endpoint = plot.iloc[-1]
    summary_rows = [
        ["maximum_absolute_DeltaV", float(abs(delta[max_index])), "mV", float(plot.Q_mAh_cm2.iloc[max_index])],
        ["signed_DeltaV_at_max_abs", float(delta[max_index]), "mV", float(plot.Q_mAh_cm2.iloc[max_index])],
        ["endpoint_DeltaV", float(endpoint.DeltaV_network_minus_KC_mV), "mV", float(endpoint.Q_mAh_cm2)],
        ["endpoint_K_over_K0_baseline_KC", float(endpoint.K_over_K0_baseline_KC), "1", float(endpoint.Q_mAh_cm2)],
        [
            "endpoint_K_over_K0_network_smooth_path",
            float(endpoint.K_over_K0_network_smooth_path),
            "1",
            float(endpoint.Q_mAh_cm2),
        ],
        ["endpoint_eps_s_baseline_KC", float(endpoint.eps_s_baseline_KC), "1", float(endpoint.Q_mAh_cm2)],
        [
            "endpoint_eps_s_network_smooth_path",
            float(endpoint.eps_s_network_smooth_path),
            "1",
            float(endpoint.Q_mAh_cm2),
        ],
    ]
    summary = pd.DataFrame(summary_rows, columns=["quantity", "value", "unit", "Q_mAh_cm2"])
    summary.to_csv(SUMMARY_TABLE, index=False, float_format="%.12g", lineterminator="\n")
    audit = {
        "rows_per_matched_path": 1081,
        "capacity_range_mAh_cm2": [float(plot.Q_mAh_cm2.min()), float(plot.Q_mAh_cm2.max())],
        "max_abs_DeltaV_mV": float(abs(delta[max_index])),
        "max_abs_DeltaV_Q_mAh_cm2": float(plot.Q_mAh_cm2.iloc[max_index]),
        "endpoint_DeltaV_mV": float(endpoint.DeltaV_network_minus_KC_mV),
        "endpoint_K_over_K0": {
            "baseline_KC": float(endpoint.K_over_K0_baseline_KC),
            "network_smooth_path": float(endpoint.K_over_K0_network_smooth_path),
        },
        "max_abs_eps_s_response_difference": float(
            np.max(np.abs(plot.eps_s_network_smooth_path - plot.eps_s_baseline_KC))
        ),
        "raw_to_registered_max_abs_errors": max_errors,
        "raw_reconstruction_pass": True,
        "evidence_class": "E-SIM",
    }
    return plot, summary, audit


def make_builder(plot: pd.DataFrame, audit: dict):
    def build():
        fig = plt.figure(figsize=(WIDTH_MM / 25.4, HEIGHT_MM / 25.4))
        grid = fig.add_gridspec(
            1,
            12,
            left=0.075,
            right=0.985,
            bottom=0.205,
            top=0.855,
            wspace=1.8,
        )
        ax_d = fig.add_subplot(grid[0, :8])
        ax_k = fig.add_subplot(grid[0, 9:])
        q = plot["Q_mAh_cm2"].to_numpy(float)
        delta = plot["DeltaV_network_minus_KC_mV"].to_numpy(float)
        max_index = int(np.argmax(np.abs(delta)))

        ax_d.plot(q, delta, color=TEAL, lw=1.65, zorder=3)
        style_axis(ax_d, zero_line=True)
        ax_d.set_xlim(0, 123)
        ax_d.set_ylim(-0.45, 5.85)
        ax_d.set_xticks([0, 40, 80, 120])
        ax_d.set_yticks([0, 2, 4])
        ax_d.set_xlabel(r"Areal charge capacity, $Q$ (mAh cm$^{-2}$)")
        ax_d.set_ylabel(r"$\Delta V=V_{\rm network}-V_{\rm KC}$ (mV)")
        ax_d.set_title("Voltage difference from the smooth-path substitution", loc="left", pad=4.5)
        panel_label(ax_d, "a", x=-0.095)
        ax_d.plot(q[max_index], delta[max_index], marker="o", ms=4.6, mfc=CARMINE, mec="white", mew=0.6, zorder=6)
        ax_d.annotate(
            f"max |$\Delta V$| = {abs(delta[max_index]):.2f} mV",
            xy=(q[max_index], delta[max_index]),
            xytext=(-14, 13),
            textcoords="offset points",
            ha="right",
            va="bottom",
            fontsize=6.5,
            color=CARMINE,
            arrowprops={"arrowstyle": "-", "color": CARMINE, "lw": 0.6},
        )
        endpoint_delta = float(delta[-1])
        ax_d.plot(q[-1], endpoint_delta, marker="o", ms=4.2, mfc="white", mec=TEAL, mew=0.9, zorder=6)
        ax_d.annotate(
            f"endpoint {endpoint_delta:+.3f} mV",
            xy=(q[-1], endpoint_delta),
            xytext=(-12, -17),
            textcoords="offset points",
            ha="right",
            va="top",
            fontsize=6.5,
            color=INK,
            arrowprops={"arrowstyle": "-", "color": MID_GREY, "lw": 0.6},
        )

        kc = plot["K_over_K0_baseline_KC"].to_numpy(float)
        network = plot["K_over_K0_network_smooth_path"].to_numpy(float)
        ax_k.plot(q, network, color=NAVY, lw=1.55, ls="-", zorder=3)
        ax_k.plot(q, kc, color=BLUE, lw=1.35, ls=(0, (4.0, 2.0)), zorder=3)
        style_axis(ax_k)
        ax_k.set_xlim(0, 123)
        ax_k.set_ylim(0.95, 1.004)
        ax_k.set_xticks([0, 60, 120])
        ax_k.set_yticks([0.95, 0.975, 1.00])
        ax_k.set_xlabel(r"$Q$ (mAh cm$^{-2}$)")
        ax_k.set_ylabel(r"Relative permeability, $K/K_0$")
        ax_k.set_title("Smooth permeability paths", loc="left", pad=4.5)
        panel_label(ax_k, "b", x=-0.24)
        ax_k.annotate(
            f"network path  {network[-1]:.3f}",
            xy=(120, network[-1]),
            xytext=(-8, 8),
            textcoords="offset points",
            ha="right",
            va="bottom",
            fontsize=6.5,
            color=NAVY,
            arrowprops={"arrowstyle": "-", "color": NAVY, "lw": 0.6},
        )
        ax_k.annotate(
            f"KC relation  {kc[-1]:.3f}",
            xy=(120, kc[-1]),
            xytext=(-8, 7),
            textcoords="offset points",
            ha="right",
            va="bottom",
            fontsize=6.5,
            color=BLUE,
            arrowprops={"arrowstyle": "-", "color": BLUE, "lw": 0.6},
        )
        text_audit = audit_text(fig, FAMILY)
        return fig, {"width_mm": WIDTH_MM, "height_mm": HEIGHT_MM, "font_audit": text_audit}

    return build


def write_manifest(outputs: dict[str, Path], qa: dict, data_audit: dict) -> None:
    bundle_files = [
        INPUT_MANIFEST,
        PLOT_TABLE,
        SUMMARY_TABLE,
        HERE / "r582_si_figure_tools.py",
        Path(__file__),
        HERE / "FIGURE_CONTRACT.md",
        HERE / "CAPTION_DRAFT.md",
        HERE / "README.md",
        HERE / "QA_NOTES.md",
    ]
    record = {
        "figure": STEM,
        "single_dominant_claim": (
            "Substituting the pore-network-derived smooth permeability path changes voltage by at most 5.21 mV "
            "and by 1.271 mV at 120 mAh cm^-2 within the modeled loading window."
        ),
        "evidence_class": "E-SIM",
        "frozen_date": "2026-07-20",
        "final_size_mm": {"width": WIDTH_MM, "height": HEIGHT_MM},
        "font": {
            "family": FAMILY,
            "minimum_pt": 6.5,
            "registered_faces": [{"path": str(path), "sha256": sha256(path)} for path in TERMES_PATHS],
        },
        "claim_boundary": (
            "This matched control addresses only the smooth bulk-permeability relation. It does not resolve or "
            "exclude local pore-throat blockage and makes no morphology claim."
        ),
        "data_audit": data_audit,
        "qa": qa,
        "inputs": [
            {"path": rel(path), "size_bytes": path.stat().st_size, "sha256": expected}
            for path, expected in EXPECTED_SHA256.items()
        ],
        "figure_outputs": [
            {"path": rel(path), "size_bytes": path.stat().st_size, "sha256": sha256(path)}
            for path in outputs.values()
        ],
        "source_bundle_files": [
            {"path": rel(path), "size_bytes": path.stat().st_size, "sha256": sha256(path)}
            for path in bundle_files
        ],
    }
    RENDER_MANIFEST.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    plot, _summary, data_audit = prepare_data()
    outputs, qa = export_deterministic(
        make_builder(plot, data_audit),
        FIGURE_DIR,
        STEM,
        "Voltage response to replacing the smooth permeability relation",
        Path(__file__).name,
        WIDTH_MM,
        HEIGHT_MM,
        FAMILY,
    )
    write_manifest(outputs, qa, data_audit)
    print(json.dumps({"figure": STEM, "outputs": {key: str(path) for key, path in outputs.items()}, "qa": qa}, indent=2))


if __name__ == "__main__":
    main()
