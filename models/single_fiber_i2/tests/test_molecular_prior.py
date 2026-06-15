from __future__ import annotations

import math
import sys
from copy import deepcopy
from pathlib import Path

MODEL_DIR = Path(__file__).resolve().parents[1]
if str(MODEL_DIR) not in sys.path:
    sys.path.insert(0, str(MODEL_DIR))

from single_fiber_i2 import compute_site_activity_multiplier, load_params


def test_molecular_prior_disabled_gives_unity_multiplier():
    params = load_params()
    params["molecular_prior"]["enabled"] = False
    assert compute_site_activity_multiplier(params) == 1.0


def test_positive_site_fraction_and_preference_above_one_increases_multiplier():
    params = load_params()
    modified = deepcopy(params)
    modified["molecular_prior"]["enabled"] = True
    modified["molecular_prior"]["site_preference_factors"] = {"OH_functionalized_basal": 1.5}
    modified["molecular_prior"]["site_fractions"] = {"OH_functionalized_basal": 0.02}
    assert compute_site_activity_multiplier(modified) > 1.0


def test_zero_site_fractions_give_unity_multiplier():
    params = load_params()
    modified = deepcopy(params)
    modified["molecular_prior"]["enabled"] = True
    modified["molecular_prior"]["site_fractions"] = {
        key: 0.0 for key in modified["molecular_prior"]["site_fractions"]
    }
    assert compute_site_activity_multiplier(modified) == 1.0


def test_molecular_prior_multiplier_is_finite():
    params = load_params()
    params["molecular_prior"]["enabled"] = True
    value = compute_site_activity_multiplier(params)
    assert math.isfinite(value)
