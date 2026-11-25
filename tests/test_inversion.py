"""Spec §10: inversion reproduces data; the baseline is the equilibrium."""

from dataclasses import replace

import numpy as np
import pytest

from urqse.calibrate.invert import calibrate
from urqse.model.equilibrium import seed_x, solve_static, solve_within
from urqse.model.params import Params


def test_inversion_reproduces_jobs_and_farm_wages(data, cal, params):
    f = cal.fundamentals
    w = solve_within(f, params, data.N, seed_x(f, params, data.N))
    assert w.info.converged
    np.testing.assert_allclose(w.HU, data.HU, rtol=1e-7)
    np.testing.assert_allclose(w.HA, data.HA, rtol=1e-7)
    np.testing.assert_allclose(w.wA, data.wA_obs, rtol=1e-7)
    # Job-weighted mean non-farm earnings are rescaled to the observed mean.
    assert np.sum(w.wU * w.HU) / w.HU.sum() == pytest.approx(data.mean_nonfarm_wage, rel=1e-9)


@pytest.mark.parametrize("eta", [0.0, 2.0])
def test_baseline_is_the_equilibrium_from_a_perturbed_start(data, eta):
    p = Params(eta=eta)
    f = calibrate(data, p).fundamentals
    rng = np.random.default_rng(0)
    N0 = data.N * np.exp(rng.uniform(-0.3, 0.3, data.N.size))
    eq = solve_static(f, p, N0=N0)
    assert eq.info.converged
    assert eq.info.residual_inf <= 1e-10
    np.testing.assert_allclose(eq.N, data.N, rtol=1e-8)


def test_calibration_report_has_errors_below_tolerance(cal):
    assert all(err < 1e-7 for err in cal.max_rel_error.values())
    assert cal.wage_info.converged and cal.baseline.info.converged


def test_land_income_outside_choice_leaves_choice_side_unchanged(data):
    """With land_income_in_choice=False, land tenure changes nothing on the choice margin: the
    recovered farm wedges are the same for any omega."""
    p = Params(land_income_in_choice=False)
    by_omega = [calibrate(replace(data, omega=np.full(data.N.size, w)), p) for w in (0.0, 1.0)]
    np.testing.assert_allclose(by_omega[0].fundamentals.xi_A, by_omega[1].fundamentals.xi_A, rtol=1e-12)
    # The flag is not vacuous: letting land income into the choice moves the wedge.
    q = Params(land_income_in_choice=True)
    on = calibrate(replace(data, omega=np.ones(data.N.size)), q)
    assert np.max(np.abs(on.fundamentals.xi_A / by_omega[1].fundamentals.xi_A - 1.0)) > 0.1
