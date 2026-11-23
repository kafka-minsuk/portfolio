"""Spec §4 / §10: the two-location closed form against the full solver."""

import pytest

from urqse.model.analytic import closed_form, two_location_check
from urqse.model.blocks import congestion_elasticities
from urqse.model.params import Params


@pytest.mark.parametrize("eta", [0.0, 1.5])
def test_two_location_closed_form_matches_solver(eta):
    r = two_location_check(Params(eta=eta), productivity_pct=1.0)
    assert r.converged
    assert r.s > 0
    assert r.x_solver == pytest.approx(r.x_closed_form, rel=2e-3)
    if eta > 0:
        assert r.n_solver == pytest.approx(r.n_closed_form, rel=2e-2)
    else:
        assert abs(r.n_solver) < 1e-9


def test_closed_form_reduces_to_boxed_formula_when_closed():
    p = Params(eta=0.0)
    s, pi_C = 0.01, 0.6
    psi_C, psi_R = congestion_elasticities(p)
    boxed = p.lam_R * s / (1 + p.lam_R * (psi_C * (1 - pi_C) + psi_R * pi_C))
    n, x = closed_form(p, s, pi_C)
    assert n == 0.0
    assert x == pytest.approx(boxed, rel=1e-12)
