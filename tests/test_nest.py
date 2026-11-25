"""Spec §3.12: a metro nest. Residents choose a county or the metro with lam_R, then a zone inside
the metro with lam_M >= lam_R. The synthetic state's core and 8 suburbs play the metro's tracts."""

from dataclasses import replace

import numpy as np
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from urqse.calibrate.invert import calibrate
from urqse.model import blocks, land
from urqse.model.dynamics import ConsolidationStop, simulate, solve_period
from urqse.model.equilibrium import solve_static
from urqse.model.fundamentals import with_shocks
from urqse.model.params import Params
from urqse.synthetic import random_state, synthetic_state


def nested(data):
    """The core and the suburbs form nest 0; rural counties stay counties."""
    return replace(data, nest=np.where(data.rural, -1, 0))


@pytest.fixture(scope="module")
def nd():
    return nested(synthetic_state())


P2 = Params(lam_M_over_R=2.0)


@pytest.fixture(scope="module")
def ncal(nd):
    cal = calibrate(nd, P2)
    assert cal.baseline.info.converged and cal.flow_info.converged
    return cal


# --- blocks --------------------------------------------------------------------------------


def test_outer_units_keep_counties_and_merge_each_nest():
    unit, U, label = blocks.outer_units(np.array([-1, 0, 0, -1, 1, 0]), 6)
    assert unit.tolist() == [0, 1, 1, 2, 3, 1] and U == 4 and label.tolist() == [-1, 0, -1, 1]


def test_nested_shares_sum_to_one_and_collapse_when_lam_M_equals_lam_R():
    rng = np.random.default_rng(1)
    lnu, nest = rng.normal(size=9), np.array([-1, 0, 0, 0, -1, 1, 1, -1, 0])
    for lam_M in (3.0, 7.0):
        assert np.exp(blocks.residence_log_shares(lnu, 3.0, nest, lam_M)).sum() == pytest.approx(1.0, rel=1e-13)
    np.testing.assert_allclose(blocks.residence_log_shares(lnu, 3.0, nest, 3.0), blocks.residence_log_shares(lnu, 3.0), rtol=1e-13)
    assert blocks.log_welfare(lnu, 3.0, nest, 3.0) == pytest.approx(blocks.log_welfare(lnu, 3.0), rel=1e-13)


def test_lam_M_below_lam_R_is_rejected():
    with pytest.raises(ValueError, match="lam_M_over_R"):
        Params(lam_M_over_R=0.9)


# --- calibration and the static equilibrium --------------------------------------------------


def test_inversion_reproduces_data_with_a_nest(nd, ncal):
    assert all(err < 1e-7 for err in ncal.max_rel_error.values()), ncal.max_rel_error
    np.testing.assert_allclose(ncal.baseline.N, nd.N, rtol=1e-9)
    assert ncal.fundamentals.tau.shape == (17, 17) and ncal.fundamentals.delta.shape == (17,)  # 16 rural + 1 nest


def test_nest_with_lam_M_equal_lam_R_equals_the_flat_model(params):
    data = synthetic_state()

    def long_run(d):
        cal = calibrate(d, params)
        f = with_shocks(cal.fundamentals, core=d.core, a_TH=params.a_TH, core_productivity_pct=10.0, travel_cut_pct=20.0)
        eq = solve_static(f, params, N0=d.N, x0=cal.baseline.within.x)
        assert eq.info.converged
        return eq.N

    np.testing.assert_allclose(long_run(nested(data)), long_run(data), rtol=1e-9)


def test_zero_shock_changes_nothing_with_a_nest(nd, ncal):
    eq = solve_static(ncal.fundamentals, P2, N0=nd.N * np.exp(0.05 * np.sin(np.arange(nd.N.size))), x0=ncal.baseline.within.x)
    assert eq.info.converged
    np.testing.assert_allclose(eq.N, nd.N, rtol=1e-8)


@pytest.fixture(scope="module")
def suburb_shock(nd, ncal):
    """A neighbourhood amenity improvement in one suburb zone inside the metro only."""
    i = int(np.nonzero(nd.kind == "suburb")[0][0])
    f = replace(ncal.fundamentals, A=ncal.fundamentals.A * np.where(np.arange(nd.N.size) == i, 1.1, 1.0))
    eq = solve_static(f, P2, N0=nd.N, x0=ncal.baseline.within.x)
    assert eq.info.converged
    return i, f, eq


def test_a_policy_inside_the_metro_moves_the_countryside(nd, suburb_shock):
    i, f, eq = suburb_shock
    assert eq.N[i] > nd.N[i]
    rural = nd.rural
    assert eq.N[rural].sum() < nd.N[rural].sum()  # the metro became more attractive as a whole
    assert eq.N.sum() == pytest.approx(nd.N.sum(), rel=1e-10)  # eta = 0


def test_a_larger_lam_M_concentrates_the_response_inside_the_metro(nd):
    i = int(np.nonzero(nd.kind == "suburb")[0][0])

    def own_gain(p):
        cal = calibrate(nd, p)
        f = replace(cal.fundamentals, A=cal.fundamentals.A * np.where(np.arange(nd.N.size) == i, 1.1, 1.0))
        eq = solve_static(f, p, N0=nd.N, x0=cal.baseline.within.x)
        return np.log(eq.N[i] / nd.N[i])

    assert own_gain(Params(lam_M_over_R=3.0)) > own_gain(Params(lam_M_over_R=1.0))


def test_income_identity_with_a_nest(suburb_shock):
    _, f, eq = suburb_shock
    w = eq.within
    out_of_region = (1.0 - P2.varsigma) * np.sum(land.landlord_income(w.rho, f.TF, f.omega))
    produced = np.sum(w.wU * w.HU) + np.sum(w.wA * w.HA) + np.sum(w.rho * f.TF)
    assert np.sum(w.Y * eq.N) + out_of_region == pytest.approx(produced, rel=1e-12)


def test_semi_closed_baseline_is_an_equilibrium_with_a_nest(nd):
    p = Params(lam_M_over_R=2.0, eta=2.0)
    cal = calibrate(nd, p)
    eq = solve_static(cal.fundamentals, p, N0=nd.N * 1.03, x0=cal.baseline.within.x)
    assert eq.info.converged
    np.testing.assert_allclose(eq.N, nd.N, rtol=1e-8)


# --- the path ------------------------------------------------------------------------------


def _path(nd, ncal, f_shock=None, imm=None, T=40):
    f = ncal.fundamentals
    return simulate(f, f_shock or f, P2, N0=ncal.baseline.N, x0=ncal.baseline.within.x,
                    immigration=np.zeros(T) if imm is None else imm,
                    stop=ConsolidationStop(nd.rural, P2.epsilon, P2.ss_tol))  # fmt: skip


def test_no_shock_path_stays_at_baseline_with_a_nest(nd, ncal):
    path = _path(nd, ncal)
    assert path.all_converged
    np.testing.assert_allclose(path.N, np.broadcast_to(nd.N, path.N.shape), rtol=1e-8)


def test_path_conserves_people_and_re_sorts_inside_the_metro(nd, ncal):
    f1 = with_shocks(ncal.fundamentals, core=nd.core_mask, a_TH=P2.a_TH, core_productivity_pct=10.0)
    imm = np.full(30, 400.0)
    path = _path(nd, ncal, f1, imm, T=30)
    assert path.all_converged
    np.testing.assert_allclose(path.N.sum(axis=1), nd.N.sum() + np.concatenate([[0.0], np.cumsum(imm)]), rtol=1e-9)
    inside = nd.nest >= 0
    t = 10  # residents inside the metro satisfy (S') at every period
    w = path.within[t]
    shares = np.exp(blocks.residence_log_shares(w.lnu, P2.lam_R, nd.nest, P2.lam_M))
    np.testing.assert_allclose(path.N[t, inside] / path.N[t, inside].sum(), shares[inside] / shares[inside].sum(), rtol=1e-7)
    no_imm = _path(nd, ncal, f1, np.zeros(30), T=30)  # arrivals are not population-weighted (VERIFY, §12.2)
    rural = no_imm.N[:, nd.rural].sum(axis=1)
    assert rural[-1] < rural[0]


def test_solve_period_without_a_nest_is_solve_within(cal, data, params):
    w, N = solve_period(cal.fundamentals, params, data.N, cal.baseline.within.x)
    np.testing.assert_array_equal(N, data.N)
    np.testing.assert_allclose(w.lnu, cal.baseline.within.lnu, rtol=1e-10)


@settings(max_examples=30, deadline=None)
@given(
    Z=st.integers(min_value=4, max_value=15),
    seed=st.integers(min_value=0, max_value=2**31 - 1),
    ratio=st.floats(min_value=1.0, max_value=4.0),
    shock=st.floats(min_value=-10.0, max_value=20.0),
)
def test_random_nested_economies(Z, seed, ratio, shock):
    data = random_state(Z, seed)
    rng = np.random.default_rng(seed)
    nest = np.full(Z, -1)
    nest[rng.choice(Z, size=int(rng.integers(2, Z)), replace=False)] = 0
    nest[data.core] = 0
    data = replace(data, nest=nest)
    p = Params(lam_M_over_R=ratio)
    cal = calibrate(data, p)
    assert all(err < 1e-7 for err in cal.max_rel_error.values())
    f = with_shocks(cal.fundamentals, core=data.core, a_TH=p.a_TH, core_productivity_pct=shock)
    eq = solve_static(f, p, N0=cal.baseline.N, x0=cal.baseline.within.x)
    assert eq.info.converged and np.all(eq.N > 0)
    assert eq.N.sum() == pytest.approx(data.N.sum(), rel=1e-9)
