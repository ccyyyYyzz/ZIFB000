from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

MODEL_DIR = Path(__file__).resolve().parents[1]
if str(MODEL_DIR) not in sys.path:
    sys.path.insert(0, str(MODEL_DIR))

from single_fiber_i2 import load_params, solve_eta_for_current, simulate_charge_discharge


def test_current_root_matches_i_app_within_tolerance():
    params = load_params()
    target = params["current"]["i_charge_A_m2"]
    result = solve_eta_for_current(target, theta=0.35, h_i2_m=2.5e-8, params=params)
    assert abs(result["j_total"] - target) < 1e-7


def test_demo_theta_stays_in_unit_interval():
    params = load_params()
    rows, _, _ = simulate_charge_discharge(params)
    theta = np.array([row["theta"] for row in rows])
    assert np.all(theta >= -1e-10)
    assert np.all(theta <= 1.0 + 1e-10)


def test_demo_h_i2_nonnegative():
    params = load_params()
    rows, _, _ = simulate_charge_discharge(params)
    h_i2 = np.array([row["h_I2"] for row in rows])
    assert np.all(h_i2 >= -1e-15)


def test_no_nan_in_demo_run():
    params = load_params()
    rows, _, _ = simulate_charge_discharge(params)
    for row in rows:
        for value in row.values():
            if isinstance(value, (int, float, np.floating)):
                assert math.isfinite(value)
