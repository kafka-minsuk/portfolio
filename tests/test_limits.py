"""Spec §10: transport cut raises welfare in a closed region; semi-closure nests its limits."""

import numpy as np
import pytest

from urqse.calibrate.invert import calibrate
from urqse.model.equilibrium import solve_static
from urqse.model.fundamentals import with_shocks
from urqse.model.params import Params


@pytest.mark.parametrize("scope", ["all", "into_core"])
def test_transport_cut_raises_welfare_with_closed_population_fixed(cal, data, params, scope):
    f, base = cal.fundamentals, cal.baseline
    cut = with_shocks(f, core=data.core, a_TH=params.a_TH, travel_cut_pct=20.0, travel_cut_scope=scope)
    eq = solve_static(cut, params, N0=base.N, x0=base.within.x)
    assert eq.info.converged
    assert eq.lnW > base.lnW
    assert eq.N.sum() == pytest.approx(base.N.sum(), rel=1e-9)


def _regional_population(data, eta):
    p = Params(eta=eta)
    c = calibrate(data, p)
    f = with_shocks(c.fundamentals, core=data.core, a_TH=p.a_TH, core_productivity_pct=10.0)
    eq = solve_static(f, p, N0=c.baseline.N, x0=c.baseline.within.x)
    assert eq.info.converged
    return eq, f


def test_closed_region_holds_population_and_it_rises_with_eta(data):
    pops = [_regional_population(data, eta)[0].N_bar for eta in (0.0, 0.5, 1.0, 2.0, 5.0)]
    assert pops[0] == pytest.approx(data.N.sum(), rel=1e-9)
    assert all(b > a for a, b in zip(pops, pops[1:]))


def test_open_limit_pins_welfare_at_reference_utility(data):
    """The welfare gap shrinks roughly as 1/(1 + eta psi), so W -> U_bar as eta -> infinity."""
    gaps = []
    for eta in (0.0, 10.0, 100.0):
        eq, f = _regional_population(data, eta)
        gaps.append(abs(eq.lnW - np.log(f.U_bar)))
    assert gaps[0] > gaps[1] > gaps[2]
    assert gaps[2] < 0.05 * gaps[0]  # 1/(1 + 100 psi) with psi ~ 0.3
