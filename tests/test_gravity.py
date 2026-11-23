"""PPML gravity (spec §7): recovers a known kappa*lam on synthetic commuting flows."""

import numpy as np
import pytest

from urqse.calibrate.gravity import commuting_gravity


def _gravity_sample(Z=12, kl=0.05, seed=0):
    rng = np.random.default_rng(seed)
    xy = rng.uniform(0, 150, (Z, 2))
    t = np.hypot(*(xy[:, None, :] - xy[None, :, :]).transpose(2, 0, 1)) + 10.0
    o, d = rng.normal(8.0, 0.5, Z), rng.normal(0.0, 0.5, Z)
    return t, np.exp(o[:, None] + d[None, :] - kl * t)


def test_ppml_recovers_kappa_lam_exactly_on_expected_flows():
    t, mean = _gravity_sample()
    for mask in (None, ~np.eye(t.shape[0], dtype=bool)):
        g = commuting_gravity(mean, t, mask)
        assert g.info.converged and g.info.residual_inf <= 1e-10
        assert g.kappa_lam == pytest.approx(0.05, rel=1e-8)


def test_ppml_recovers_kappa_lam_with_poisson_noise_and_zeros():
    t, mean = _gravity_sample(Z=15, kl=0.04, seed=1)
    flows = np.random.default_rng(2).poisson(mean / 50.0).astype(float)  # small counts, many zeros
    assert (flows == 0).any()
    g = commuting_gravity(flows, t)
    assert g.info.converged
    assert abs(g.kappa_lam - 0.04) < 4 * g.se_robust
    assert g.se_robust > 0 and g.se_cluster_origin > 0


def test_ppml_drops_an_origin_with_no_flows():
    t, mean = _gravity_sample()
    mean[3] = 0.0
    g = commuting_gravity(mean, t)
    assert g.n_obs == 11 * 12 and g.kappa_lam == pytest.approx(0.05, rel=1e-8)
