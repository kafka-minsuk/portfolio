"""Spec §3.8, §12: flow steady state, stop rule, immigration conservation."""

import numpy as np
import pytest

from urqse.calibrate.invert import calibrate
from urqse.model.dynamics import ConsolidationStop, flow_matrix, simulate
from urqse.model.fundamentals import with_shocks
from urqse.model.params import Params
from urqse.synthetic import random_state


def _path(cal, data, params, *, f_shock=None, immigration=None, epsilon=None, T=60):
    f, base = cal.fundamentals, cal.baseline
    stop = ConsolidationStop(data.rural, params.epsilon if epsilon is None else epsilon, params.ss_tol)
    imm = np.zeros(T) if immigration is None else immigration
    return simulate(f, f_shock or f, params, N0=base.N, x0=base.within.x, immigration=imm, stop=stop)


def test_no_shock_path_stays_at_baseline(cal, data, params):
    path = _path(cal, data, params)
    assert path.all_converged
    np.testing.assert_allclose(path.N, np.broadcast_to(data.N, path.N.shape), rtol=1e-9)
    np.testing.assert_allclose(path.land_ratio, 1.0, rtol=1e-9)
    assert (path.stop_period, path.stop_reason) == (1, "steady_state")


def test_stop_rule_fires_on_urban_productivity_shock(cal, data, params):
    f = with_shocks(cal.fundamentals, core=data.core, a_TH=params.a_TH, core_productivity_pct=10.0)
    path = _path(cal, data, params, f_shock=f, epsilon=0.025)
    assert path.all_converged
    assert path.stop_reason == "consolidation"
    t = path.stop_period
    assert path.land_ratio[t] >= 1.025
    assert np.all(path.land_ratio[:t] < 1.025)
    # Rural residents leave along the path.
    rural = path.N[:, data.rural].sum(axis=1)
    assert rural[-1] < rural[0]


def test_population_plus_cumulative_immigration_is_conserved(cal, data, params):
    f = with_shocks(cal.fundamentals, core=data.core, a_TH=params.a_TH, core_productivity_pct=5.0)
    I = np.full(30, 2_000.0)
    path = _path(cal, data, params, f_shock=f, immigration=I, T=30)
    expected = data.N.sum() + np.concatenate([[0.0], np.cumsum(I)])
    np.testing.assert_allclose(path.N.sum(axis=1), expected, rtol=1e-12)


def test_stop_rule_reports_horizon_when_nothing_binds():
    stop = ConsolidationStop(np.array([True, False]), epsilon=0.5, ss_tol=1e-6)
    ratio = np.array([1.0, 1.1, 1.2, 1.3])
    change = np.array([0.0, 1e-2, 1e-3, 1e-4])
    assert stop.evaluate(ratio, change) == (3, "horizon")
    assert stop.evaluate(np.array([1.0, 1.1, 1.6, 1.7]), change) == (2, "consolidation")


def test_semi_closed_path_with_eta_zero_matches_closed_flows(cal, data):
    """phi only acts when eta > 0: an eta = 0 path is identical for any phi."""
    f = with_shocks(cal.fundamentals, core=data.core, a_TH=0.371, core_productivity_pct=10.0)
    a = _path(cal, data, Params(phi=0.2), f_shock=f, T=10)
    b = _path(cal, data, Params(phi=0.9), f_shock=f, T=10)
    np.testing.assert_allclose(a.N, b.N, rtol=1e-13)
    assert a.N.sum(axis=1) == pytest.approx(np.full(11, data.N.sum()), rel=1e-12)


@pytest.mark.parametrize("Z, seed", [(3, 1407190), (3, 1611395864), (6, 669652944), (4, 235653396)])
def test_flow_offsets_make_hard_random_baselines_steady(Z, seed):
    """Economies where accelerated Sinkhorn sweeps diverged or stalled."""
    data = random_state(Z, seed)
    p = Params()
    cal = calibrate(data, p)
    assert cal.flow_info.converged
    w, f = cal.baseline.within, cal.fundamentals
    np.testing.assert_allclose(flow_matrix(w.lnu, f.delta, f.tau, p.nu).T @ data.N, data.N, rtol=1e-9)
