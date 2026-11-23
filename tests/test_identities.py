"""Accounting identities and invariants (spec §10, CLAUDE.md)."""

import numpy as np
import pytest

from urqse.model import blocks, land
from urqse.model.equilibrium import commuting_kernels, solve_static
from urqse.model.fundamentals import with_shocks


@pytest.fixture(scope="module")
def shocked(cal, data, params):
    f = with_shocks(cal.fundamentals, core=data.core, a_TH=params.a_TH, core_productivity_pct=10.0)
    eq = solve_static(f, params, N0=data.N, x0=cal.baseline.within.x)
    assert eq.info.converged
    return f, eq


def test_farm_rent_identity(shocked, params):
    f, eq = shocked
    w = eq.within
    np.testing.assert_allclose(w.rho * f.TF / (w.wA * w.HA), params.theta_T / params.theta_H, rtol=1e-13)


def test_income_equals_wages_plus_land_rent_by_ownership_rule(shocked, params):
    f, eq = shocked
    w = eq.within
    resident_income = np.sum(w.Y * eq.N)
    out_of_region = (1.0 - params.varsigma) * np.sum(land.landlord_income(w.rho, f.TF, f.omega))
    produced = np.sum(w.wU * w.HU) + np.sum(w.wA * w.HA) + np.sum(w.rho * f.TF)
    assert resident_income + out_of_region == pytest.approx(produced, rel=1e-12)


def test_operator_income_is_value_added_per_worker_under_full_ownership(params):
    A_farm, TF, HA = np.array([1.3, 0.7]), np.array([100.0, 40.0]), np.array([9.0, 2.5])
    wA = blocks.farm_wage(A_farm, TF, HA, params)
    rho = blocks.farm_rent(wA, HA, TF, params)
    V = blocks.farm_value_added(A_farm, HA, TF, params)
    np.testing.assert_allclose(land.operator_income(wA, rho, TF, HA, omega=1.0), V / HA, rtol=1e-13)
    np.testing.assert_allclose(land.operator_income(wA, rho, TF, HA, omega=0.0), wA, rtol=1e-13)


def test_allocations_are_homogeneous_of_degree_zero_in_wages_and_rents(cal, data, params):
    f, w = cal.fundamentals, cal.baseline.within
    D, _ = commuting_kernels(f, params)
    c = 3.7
    lnwtA = np.log(w.wA * f.xi_A)

    def allocation(scale):
        ch = blocks.choice(D, np.log(scale * w.wU), np.log(scale) + lnwtA, data.N, params.lam)
        lnu = blocks.expected_log_utility(f.A, scale * w.r, ch.lnPhi, params)
        rho = blocks.farm_rent(scale * w.wA, ch.HA, f.TF, params)
        return ch.HU, ch.HA, blocks.residence_log_shares(lnu, params.lam_R), rho / scale

    for a, b in zip(allocation(1.0), allocation(c)):
        np.testing.assert_allclose(a, b, rtol=1e-11, atol=1e-12)
