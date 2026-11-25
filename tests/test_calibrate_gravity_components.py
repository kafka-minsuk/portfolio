"""PPML gravity on a sample that splits into two groups of counties with no pair between them."""

import numpy as np
import pytest

from urqse.calibrate.gravity import commuting_gravity


def test_disconnected_sample_is_identified_per_group():
    rng = np.random.default_rng(0)
    Z, k = 8, 0.05
    t = 10.0 + 40.0 * rng.random((Z, Z))
    a, b = rng.normal(size=Z), rng.normal(size=Z)
    flows = np.exp(4.0 + a[:, None] + b[None, :] - k * t)
    group = np.arange(Z) < 4
    mask = (group[:, None] == group[None, :]) & ~np.eye(Z, dtype=bool)  # pairs only within each group
    fit = commuting_gravity(flows, t, mask)
    assert fit.info.converged
    np.testing.assert_allclose(fit.kappa_lam, k, rtol=1e-8)
    full = commuting_gravity(flows, t, ~np.eye(Z, dtype=bool))  # connected: same answer as before
    np.testing.assert_allclose(full.kappa_lam, k, rtol=1e-8)


def test_a_sample_too_small_to_identify_kappa_lam_is_reported_not_estimated():
    rng = np.random.default_rng(1)
    t = 10.0 + 30.0 * rng.random((3, 3))
    flows = np.exp(3.0 - 0.05 * t)
    mask = np.zeros((3, 3), bool)
    mask[0, 1:] = True  # one origin: the short-trip sample of a 3-county state
    fit = commuting_gravity(flows, t, mask)
    assert not fit.info.converged and np.isnan(fit.kappa_lam) and "not identified" in fit.info.method


def test_an_empty_sample_is_reported_not_estimated():
    t = np.full((3, 3), 120.0)
    fit = commuting_gravity(np.ones((3, 3)), t, t <= 60.0)
    assert not fit.info.converged and np.isnan(fit.kappa_lam) and fit.n_obs == 0


def test_fallback_sample_only_when_the_headline_is_not_identified():
    from urqse.calibrate import run_state as rs
    from urqse.calibrate.gravity import GravityFit
    from urqse.model.equilibrium import SolveInfo

    def fit(ok, method="PPML"):
        return GravityFit(0.02, 0.0, 0.0, 0.0, 10, 0, 0.9, SolveInfo(ok, 3, 1e-12 if ok else 4e-7, method))

    assert rs.chosen_gravity({rs.HEADLINE_GRAVITY: fit(True)}) == rs.HEADLINE_GRAVITY
    assert rs.chosen_gravity({rs.HEADLINE_GRAVITY: fit(False, "not identified: 6 pairs, 6 parameters")}) == rs.FALLBACK_GRAVITY
    with pytest.raises(RuntimeError, match="did not converge"):
        rs.chosen_gravity({rs.HEADLINE_GRAVITY: fit(False)})
