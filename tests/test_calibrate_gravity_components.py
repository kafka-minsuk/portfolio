"""PPML gravity on a sample that splits into two groups of counties with no pair between them."""

import numpy as np

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
