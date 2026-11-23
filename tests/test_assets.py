"""Spec §3.10 / §10: Gordon terminal value and path prices."""

import numpy as np
import pytest

from urqse.model import land
from urqse.model.params import Params


def test_constant_rent_prices_at_gordon_value():
    i, g, rho = 0.05, 0.02, 250.0
    q = land.discount_from_rates(i, g)
    P = land.present_values(np.full((40, 3), rho), q)
    np.testing.assert_allclose(P, rho * (1 + g) / (i - g), rtol=1e-12)


def test_price_rent_ratio_pins_the_discount():
    p = Params(price_rent_ratio=36.0)
    assert land.gordon_multiple(p.discount) == pytest.approx(36.0, rel=1e-13)


def test_price_anticipates_a_future_rent_drop():
    q = Params().discount
    rho = np.array([100.0, 100.0, 100.0, 80.0, 80.0])
    P = land.present_values(rho, q)
    assert P[-1] == pytest.approx(80.0 * land.gordon_multiple(q))
    expected0 = q * 100 + q**2 * 100 + q**3 * 80 + q**4 * 80 + q**4 * 80 * land.gordon_multiple(q)
    assert P[0] == pytest.approx(expected0, rel=1e-13)
