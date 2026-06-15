"""Post-processing helpers for the single-fiber I2 model."""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt


def write_csv(rows: list[dict[str, float]], path: str | Path) -> Path:
    """Write diagnostic rows to CSV."""

    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError("No rows to write")
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return out


def plot_voltage_like(rows: list[dict[str, float]], path: str | Path) -> Path:
    """Plot eta_I and current split versus time."""

    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    time_h = [row["time_s"] / 3600.0 for row in rows]
    fig, ax1 = plt.subplots(figsize=(8.0, 4.8))
    ax1.plot(time_h, [row["eta_I"] for row in rows], color="#1f77b4", label="eta_I")
    ax1.set_xlabel("time [h]")
    ax1.set_ylabel("eta_I [V]", color="#1f77b4")
    ax1.tick_params(axis="y", labelcolor="#1f77b4")

    ax2 = ax1.twinx()
    ax2.plot(time_h, [row["j_bare"] for row in rows], color="#d62728", linestyle="--", label="j_bare")
    ax2.plot(time_h, [row["j_cov"] for row in rows], color="#2ca02c", linestyle=":", label="j_cov")
    ax2.plot(time_h, [row["j_total"] for row in rows], color="#111111", linewidth=1.2, label="j_total")
    ax2.set_ylabel("current density [A/m2]")
    lines = ax1.get_lines() + ax2.get_lines()
    ax1.legend(lines, [line.get_label() for line in lines], loc="best")
    ax1.grid(True, alpha=0.25)
    fig.tight_layout()
    fig.savefig(out, dpi=180)
    plt.close(fig)
    return out


def plot_theta_h_rfilm(rows: list[dict[str, float]], path: str | Path) -> Path:
    """Plot coverage, film thickness, and local film resistance."""

    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    time_h = [row["time_s"] / 3600.0 for row in rows]
    fig, axes = plt.subplots(3, 1, figsize=(8.0, 7.2), sharex=True)
    axes[0].plot(time_h, [row["theta"] for row in rows], color="#6a3d9a")
    axes[0].set_ylabel("theta [-]")
    axes[0].set_ylim(-0.02, 1.02)
    axes[1].plot(time_h, [1e9 * row["h_I2"] for row in rows], color="#ff7f00")
    axes[1].set_ylabel("h_I2 [nm]")
    axes[2].plot(time_h, [row["Rfilm_local"] for row in rows], color="#006d77")
    axes[2].set_ylabel("Rfilm [ohm m2]")
    axes[2].set_xlabel("time [h]")
    for ax in axes:
        ax.grid(True, alpha=0.25)
    fig.tight_layout()
    fig.savefig(out, dpi=180)
    plt.close(fig)
    return out
