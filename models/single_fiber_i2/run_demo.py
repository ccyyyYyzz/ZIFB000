"""Run the single-fiber I2 charge/discharge demonstration."""

from __future__ import annotations

from pathlib import Path

from postprocess import plot_theta_h_rfilm, plot_voltage_like, write_csv
from single_fiber_i2 import compute_site_activity_multiplier, load_params, simulate_charge_discharge


def main() -> None:
    params = load_params()
    rows, _, _ = simulate_charge_discharge(params)
    root = Path(__file__).resolve().parents[2]
    out_dir = root / "outputs" / "single_fiber_i2"
    csv_path = write_csv(rows, out_dir / "demo_charge_discharge.csv")
    voltage_path = plot_voltage_like(rows, out_dir / "demo_voltage_like.png")
    film_path = plot_theta_h_rfilm(rows, out_dir / "demo_theta_h_Rfilm.png")
    prior = params.get("molecular_prior", {}) or {}
    print(f"Wrote {csv_path}")
    print(f"Wrote {voltage_path}")
    print(f"Wrote {film_path}")
    print(f"Molecular prior enabled: {bool(prior.get('enabled', False))}")
    print(f"Molecular prior mapping: {prior.get('mapping', 'none')}")
    print(f"Site activity multiplier: {compute_site_activity_multiplier(params):.6g}")


if __name__ == "__main__":
    main()
