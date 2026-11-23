"""Spec §10: random economies with Z <= 15 calibrate, solve and stay positive."""

import numpy as np
from hypothesis import given, settings
from hypothesis import strategies as st

from urqse.calibrate.invert import calibrate
from urqse.model.dynamics import ConsolidationStop, simulate
from urqse.model.equilibrium import solve_static
from urqse.model.fundamentals import with_shocks
from urqse.model.params import Params
from urqse.synthetic import random_state


@settings(max_examples=50, deadline=None)
@given(
    Z=st.integers(min_value=3, max_value=15),
    seed=st.integers(min_value=0, max_value=2**31 - 1),
    eta=st.sampled_from([0.0, 1.0]),
    theta_T=st.floats(min_value=0.15, max_value=0.6),
    shock=st.floats(min_value=-10.0, max_value=20.0),
)
def test_random_economies_converge_with_positive_values(Z, seed, eta, theta_T, shock):
    data = random_state(Z, seed)
    p = Params(eta=eta, theta_T=theta_T)
    cal = calibrate(data, p)
    assert all(err < 1e-7 for err in cal.max_rel_error.values())

    f = with_shocks(cal.fundamentals, core=data.core, a_TH=p.a_TH, core_productivity_pct=shock, travel_cut_pct=10.0)
    eq = solve_static(f, p, N0=cal.baseline.N, x0=cal.baseline.within.x)
    assert eq.info.converged and eq.info.residual_inf <= 1e-10
    w = eq.within
    for v in (eq.N, w.wU, w.wA, w.r, w.rho, w.HU, w.HA):
        assert np.all(np.isfinite(v)) and np.all(v > 0)
    if eta == 0.0:
        assert np.isclose(eq.N.sum(), data.N.sum(), rtol=1e-9)

    path = simulate(
        cal.fundamentals, f, p, N0=cal.baseline.N, x0=cal.baseline.within.x,
        immigration=np.zeros(5), stop=ConsolidationStop(data.rural, p.epsilon, p.ss_tol),
    )  # fmt: skip
    assert path.all_converged
    assert np.all(path.N > 0)
