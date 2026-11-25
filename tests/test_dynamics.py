"""Spec §3.8, §12: the path ends where utility matches across regions (the long run), immigration
conservation."""

from dataclasses import replace

import numpy as np
import pytest

from urqse.calibrate.invert import calibrate
from urqse.model import blocks
from urqse.model.dynamics import flow_matrix, simulate
from urqse.model.equilibrium import solve_static
from urqse.model.fundamentals import with_shocks
from urqse.model.params import Params
from urqse.synthetic import random_state


def _path(cal, data, params, *, f_shock=None, immigration=None, T=60):
    f, base = cal.fundamentals, cal.baseline
    imm = np.zeros(T) if immigration is None else immigration
    return simulate(f, f_shock or f, params, N0=base.N, x0=base.within.x, immigration=imm, rural=data.rural)


def test_no_shock_path_stays_at_baseline(cal, data, params):
    path = _path(cal, data, params)
    assert path.all_converged
    np.testing.assert_allclose(path.N, np.broadcast_to(data.N, path.N.shape), rtol=1e-9)
    np.testing.assert_allclose(path.land_ratio, 1.0, rtol=1e-9)
    assert (path.stop_period, path.stop_reason) == (1, "utility_matched")


@pytest.fixture(scope="module")
def shocked(cal, data, params):
    f = with_shocks(cal.fundamentals, core=data.core, a_TH=params.a_TH, core_productivity_pct=10.0)
    return f, solve_static(f, params, N0=data.N, x0=cal.baseline.within.x)


def test_the_path_ends_at_the_long_run(cal, data, params, shocked):
    f, lr = shocked
    path = _path(cal, data, params, f_shock=f, T=400)
    assert path.all_converged and lr.info.converged
    assert path.stop_reason == "utility_matched"
    t = path.stop_period
    assert path.utility_gap[t] < params.gap_tol <= path.utility_gap[1]
    assert t == path.N.shape[0] - 1  # nothing changes after utility matches
    np.testing.assert_allclose(path.N[t], lr.N, rtol=5 * params.gap_tol)
    rural = path.N[:, data.rural].sum(axis=1)
    assert rural[-1] < rural[0]  # rural residents leave along the path


def test_moving_costs_set_the_speed_not_the_end(cal, data, params, shocked):
    f, lr = shocked
    ends = {}
    for tau0 in (0.5, 1.5):
        p = replace(params, tau0=tau0)
        c = calibrate(data, p)
        g = with_shocks(c.fundamentals, core=data.core, a_TH=p.a_TH, core_productivity_pct=10.0)
        path = _path(c, data, p, f_shock=g, T=400)
        assert path.stop_reason == "utility_matched"
        ends[tau0] = path
    assert ends[0.5].stop_period < ends[1.5].stop_period
    for path in ends.values():
        np.testing.assert_allclose(path.N[-1], lr.N, rtol=5 * params.gap_tol)


def test_the_path_reports_the_horizon_before_utility_matches(cal, data, params, shocked):
    path = _path(cal, data, params, f_shock=shocked[0], T=5)
    assert (path.stop_period, path.stop_reason) == (5, "horizon")
    assert path.utility_gap[5] > params.gap_tol


def test_population_plus_cumulative_immigration_is_conserved(cal, data, params):
    f = with_shocks(cal.fundamentals, core=data.core, a_TH=params.a_TH, core_productivity_pct=5.0)
    I = np.full(30, 2_000.0)
    path = _path(cal, data, params, f_shock=f, immigration=I, T=30)
    expected = data.N.sum() + np.concatenate([[0.0], np.cumsum(I)])
    np.testing.assert_allclose(path.N.sum(axis=1), expected, rtol=1e-12)


def test_semi_closed_path_with_eta_zero_matches_closed_flows(cal, data):
    """phi only acts when eta > 0: an eta = 0 path is identical for any phi."""
    f = with_shocks(cal.fundamentals, core=data.core, a_TH=0.371, core_productivity_pct=10.0)
    a = _path(cal, data, Params(phi=0.2), f_shock=f, T=10)
    b = _path(cal, data, Params(phi=0.9), f_shock=f, T=10)
    np.testing.assert_allclose(a.N, b.N, rtol=1e-13)
    assert a.N.sum(axis=1) == pytest.approx(np.full(11, data.N.sum()), rel=1e-12)


@pytest.mark.parametrize("Z, seed", [(3, 1407190), (3, 1611395864), (6, 669652944), (4, 235653396)])
def test_every_calibrated_baseline_is_a_steady_state(Z, seed):
    """No flow offsets to calibrate: residents in the long run (S) stay put under the flows."""
    data = random_state(Z, seed)
    p = Params()
    cal = calibrate(data, p)
    w, f = cal.baseline.within, cal.fundamentals
    mu = flow_matrix(w.lnu, f.tau, p.lam_R)
    np.testing.assert_allclose(mu.sum(axis=1), 1.0, rtol=1e-12)
    assert np.all(mu >= 0)
    np.testing.assert_allclose(mu.T @ data.N, data.N, rtol=1e-9)


def test_flows_are_stationary_exactly_at_the_residence_logit():
    rng = np.random.default_rng(3)
    Z = 8
    lnu = rng.normal(size=Z)
    d = rng.uniform(5.0, 300.0, size=(Z, Z))
    tau = 1.0 + np.log((d + d.T) / 2.0)
    np.fill_diagonal(tau, 0.0)
    N = np.exp(blocks.residence_log_shares(lnu, 3.0))
    mu = flow_matrix(lnu, tau, 3.0)
    np.testing.assert_allclose(mu.T @ N, N, rtol=1e-12)
    off = N * 1.1 ** np.arange(Z)
    assert not np.allclose(mu.T @ off, off)
