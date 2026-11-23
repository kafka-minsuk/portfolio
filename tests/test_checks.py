"""Farmland-rent checks (spec §5 step 5) on synthetic data: model rents equal the formula, and
theta_T estimated from model rents returns the theta_T used."""


import numpy as np
import pytest

from urqse.calibrate import checks
from urqse.calibrate.invert import calibrate
from urqse.model.params import Params


def test_model_rent_is_the_formula_and_theta_T_is_recovered(data):
    for theta in (0.25, 0.40, 0.6):
        p = Params(theta_T=theta)
        w = calibrate(data, p).baseline.within
        np.testing.assert_allclose(w.rho, theta / (1 - theta) * w.wA * w.HA / data.TF, rtol=1e-12)
        est = checks.theta_T_from_rents(w.rho * data.TF, w.wA * w.HA)
        np.testing.assert_allclose(est, theta, rtol=1e-12)
        assert checks.theta_T_from_rents((w.rho * data.TF).sum(), (w.wA * w.HA).sum()) == pytest.approx(theta)


def test_rent_units_hectare_to_acre():
    # 1 wage unit per hectare at 50,000 $ per unit = 50,000 x 0.40469 $ per acre
    assert checks.rent_usd_per_acre(1.0, 50_000.0) == pytest.approx(20_234.282112)


def test_overid_statistics_on_a_proportional_model():
    obs = np.array([150.0, 200.0, 260.0, 300.0])
    o = checks.overid(0.8 * obs, obs, np.array([1.0, 2.0, 3.0, 4.0]), n_outliers=2)
    assert o["corr"] == pytest.approx(1.0) and o["slope_log"] == pytest.approx(1.0)
    assert o["level_ratio"] == pytest.approx(0.8) and o["median_ratio"] == pytest.approx(0.8)
    assert o["sd_log_ratio"] == pytest.approx(0.0, abs=1e-12)


def test_overid_flags_the_outlier():
    obs = np.linspace(150, 300, 10)
    model = obs.copy()
    model[6] *= 3.0
    assert checks.overid(model, obs, np.ones(10), n_outliers=1)["outliers"][0] == 6
