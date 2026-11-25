"""Spec §3.11: locations without a farm sector (no farm jobs in the data). The farm job option is
absent there (xi_A = 0): H_A, w_A and rho are 0, and every other invariant still holds."""

from dataclasses import replace

import numpy as np
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from urqse.calibrate.invert import calibrate
from urqse.model import blocks, land
from urqse.model.dynamics import ConsolidationStop, simulate
from urqse.model.equilibrium import commuting_kernels, solve_static
from urqse.model.fundamentals import with_shocks
from urqse.model.params import Params
from urqse.synthetic import random_state, synthetic_state


def without_farms(data, idx, tiny=0.0):
    """Move the farm jobs of counties `idx` to non-farm (jobs = workers still holds). tiny > 0
    keeps that share of them as farm jobs instead (the limit check)."""
    idx = np.asarray(idx)
    HA, HU, wA, TF = data.HA.copy(), data.HU.copy(), data.wA_obs.copy(), data.TF.copy()
    keep = tiny * HA[idx]
    HU[idx] += HA[idx] - keep
    HA[idx] = keep
    if tiny == 0.0:
        wA[idx] = 0.0
    return replace(data, HA=HA, HU=HU, wA_obs=wA, TF=TF)


@pytest.fixture(scope="module")
def nf_data():
    data = synthetic_state()
    return without_farms(data, [data.core, 6, 0])  # the core, a suburb and a rural county


@pytest.fixture(scope="module")
def nf_cal(nf_data, params):
    cal = calibrate(nf_data, params)
    assert cal.baseline.info.converged and cal.wage_info.converged
    return cal


def test_inversion_reproduces_data_with_no_farm_counties(nf_data, nf_cal):
    assert all(err < 1e-7 for err in nf_cal.max_rel_error.values()), nf_cal.max_rel_error
    f, w = nf_cal.fundamentals, nf_cal.baseline.within
    none = nf_data.HA == 0
    assert none.sum() == 3
    assert np.all(f.xi_A[none] == 0) and np.all(f.A_farm[none] == 0)
    assert np.all(w.HA[none] == 0) and np.all(w.wA[none] == 0) and np.all(w.rho[none] == 0)
    assert np.all(f.xi_A[~none] > 0) and np.all(w.HA[~none] > 0)


def test_zero_shock_changes_nothing(nf_data, nf_cal, params):
    eq = solve_static(nf_cal.fundamentals, params, N0=nf_data.N, x0=nf_cal.baseline.within.x)
    assert eq.info.converged
    np.testing.assert_allclose(eq.N, nf_data.N, rtol=1e-9)
    np.testing.assert_allclose(eq.within.HA, nf_cal.baseline.within.HA, rtol=1e-9, atol=1e-12)


@pytest.fixture(scope="module")
def nf_shocked(nf_data, nf_cal, params):
    f = with_shocks(nf_cal.fundamentals, core=nf_data.core, a_TH=params.a_TH, core_productivity_pct=10.0, farm_tfp_pct=5.0)
    eq = solve_static(f, params, N0=nf_data.N, x0=nf_cal.baseline.within.x)
    assert eq.info.converged
    return f, eq


def test_no_farm_counties_stay_without_farm_jobs_after_a_shock(nf_data, nf_shocked):
    f, eq = nf_shocked
    none = nf_data.HA == 0
    assert np.all(eq.within.HA[none] == 0) and np.all(eq.within.rho[none] == 0)
    assert np.isclose(eq.N.sum(), nf_data.N.sum(), rtol=1e-9)  # eta = 0
    for v in (eq.N, eq.within.wU, eq.within.r, eq.within.HU):
        assert np.all(np.isfinite(v)) and np.all(v > 0)


def test_identities_hold_with_no_farm_counties(nf_data, nf_shocked, params):
    f, eq = nf_shocked
    w = eq.within
    farm = nf_data.HA > 0
    np.testing.assert_allclose(w.rho[farm] * f.TF[farm] / (w.wA[farm] * w.HA[farm]), params.theta_T / params.theta_H, rtol=1e-13)
    resident_income = np.sum(w.Y * eq.N)
    out_of_region = (1.0 - params.varsigma) * np.sum(land.landlord_income(w.rho, f.TF, f.omega))
    produced = np.sum(w.wU * w.HU) + np.sum(w.wA * w.HA) + np.sum(w.rho * f.TF)
    assert resident_income + out_of_region == pytest.approx(produced, rel=1e-12)


def test_homogeneity_with_no_farm_counties(nf_data, nf_cal, params):
    f, w = nf_cal.fundamentals, nf_cal.baseline.within
    farm = blocks.farm_mask(f.xi_A)
    D, _ = commuting_kernels(f, params)
    lnwtA = np.log(np.where(farm, w.wA * f.xi_A, 1.0))

    def allocation(c):
        ch = blocks.choice(D, np.log(c * w.wU), np.log(c) + lnwtA, nf_data.N, params.lam, farm)
        lnu = blocks.expected_log_utility(f.A, c * w.r, ch.lnPhi, params)
        return ch.HU, ch.HA, blocks.residence_log_shares(lnu, params.lam_R)

    for a, b in zip(allocation(1.0), allocation(3.7)):
        np.testing.assert_allclose(a, b, rtol=1e-11, atol=1e-12)


def test_no_farm_sector_is_the_limit_of_a_vanishing_one(params):
    """A county with a tiny farm sector behaves like one with none: the long-run response to the
    same shock converges as the farm share goes to 0."""
    data = synthetic_state()
    idx = [data.core, 6, 0]

    def long_run(d):
        cal = calibrate(d, params)
        f = with_shocks(cal.fundamentals, core=d.core, a_TH=params.a_TH, core_productivity_pct=10.0)
        eq = solve_static(f, params, N0=d.N, x0=cal.baseline.within.x)
        assert eq.info.converged
        return np.log(eq.N / d.N)

    exact = long_run(without_farms(data, idx))
    gaps = [np.max(np.abs(long_run(without_farms(data, idx, tiny)) - exact)) for tiny in (1e-2, 1e-4)]
    assert gaps[1] < gaps[0] and gaps[1] < 1e-4


def test_path_conserves_population_plus_immigration(nf_data, nf_cal, params):
    f0 = nf_cal.fundamentals
    f1 = with_shocks(f0, core=nf_data.core, a_TH=params.a_TH, core_productivity_pct=10.0)
    imm = np.full(20, 500.0)
    path = simulate(f0, f1, params, N0=nf_cal.baseline.N, x0=nf_cal.baseline.within.x, immigration=imm,
                    stop=ConsolidationStop(nf_data.rural, params.epsilon, params.ss_tol))  # fmt: skip
    assert path.all_converged
    np.testing.assert_allclose(path.N.sum(axis=1), nf_data.N.sum() + np.concatenate([[0.0], np.cumsum(imm)]), rtol=1e-9)
    assert np.all(path.stack("HA")[:, nf_data.HA == 0] == 0)


@settings(max_examples=30, deadline=None)
@given(
    Z=st.integers(min_value=3, max_value=15),
    seed=st.integers(min_value=0, max_value=2**31 - 1),
    share=st.floats(min_value=0.1, max_value=0.6),
    shock=st.floats(min_value=-10.0, max_value=20.0),
)
def test_random_economies_with_no_farm_counties(Z, seed, share, shock):
    data = random_state(Z, seed)
    rng = np.random.default_rng(seed)
    idx = rng.choice(Z, size=max(1, int(share * Z)), replace=False)
    data = without_farms(data, idx)
    if not (data.HA > 0).any():
        return
    p = Params()
    cal = calibrate(data, p)
    assert all(err < 1e-7 for err in cal.max_rel_error.values())
    f = with_shocks(cal.fundamentals, core=data.core, a_TH=p.a_TH, core_productivity_pct=shock)
    eq = solve_static(f, p, N0=cal.baseline.N, x0=cal.baseline.within.x)
    assert eq.info.converged
    assert np.all(eq.within.HA[data.HA == 0] == 0) and np.all(eq.within.HA[data.HA > 0] > 0)
    assert np.isclose(eq.N.sum(), data.N.sum(), rtol=1e-9)
