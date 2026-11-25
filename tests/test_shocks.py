"""Scenario shocks (fundamentals.with_shocks, api presets): each acts on its own fundamental and
zones, and moves the long run the way its mechanism says."""

import numpy as np
import pytest

from urqse import api
from urqse.model.equilibrium import solve_static
from urqse.model.fundamentals import with_shocks


@pytest.fixture(scope="module")
def masks(data):
    return {"metro": np.isin(data.kind, ("core", "suburb")), "rural": data.rural}


def long_run(cal, data, params, masks, **shock):
    f = with_shocks(cal.fundamentals, core=data.core_mask, a_TH=params.a_TH, **masks, **shock)
    eq = solve_static(f, params, N0=data.N, x0=cal.baseline.within.x)
    assert eq.info.converged
    return f, eq


def test_each_city_shock_touches_only_its_fundamental(cal, data, params, masks):
    f0 = cal.fundamentals
    core, metro = data.core_mask, masks["metro"]
    f, _ = long_run(cal, data, params, masks, core_floor_supply_pct=30.0)
    np.testing.assert_allclose(f.L_bar / f0.L_bar, np.where(core, 1.3, 1.0))
    f, _ = long_run(cal, data, params, masks, core_amenity_pct=10.0)
    np.testing.assert_allclose(f.A / f0.A, np.where(core, 1.1, 1.0))
    f, _ = long_run(cal, data, params, masks, metro_travel_cut_pct=25.0)
    inside = metro[:, None] & metro[None, :] & ~np.eye(data.N.size, dtype=bool)
    np.testing.assert_allclose(f.t / f0.t, np.where(inside, 0.75, 1.0))  # own trips and links out of the metro unchanged


def test_upzoning_the_core_lowers_its_rent_and_draws_residents(cal, data, params, masks):
    _, eq = long_run(cal, data, params, masks, core_floor_supply_pct=30.0)
    c = data.core
    assert eq.within.r[c] < cal.baseline.within.r[c] and eq.N[c] > data.N[c]
    assert eq.N[data.rural].sum() < data.N[data.rural].sum()


def test_amenities_draw_residents_where_they_improve(cal, data, params, masks):
    _, city = long_run(cal, data, params, masks, core_amenity_pct=10.0)
    assert city.N[data.core] > data.N[data.core]
    _, rural = long_run(cal, data, params, masks, rural_amenity_pct=10.0)
    assert rural.N[data.rural].sum() > data.N[data.rural].sum()
    assert rural.N.sum() == pytest.approx(data.N.sum(), rel=1e-10)  # eta = 0


def test_a_transit_line_inside_the_metro_raises_welfare(cal, data, params, masks):
    _, eq = long_run(cal, data, params, masks, metro_travel_cut_pct=25.0)
    assert eq.lnW > cal.baseline.lnW


def test_a_shock_without_its_zones_is_an_error(cal, data, params):
    with pytest.raises(ValueError, match="rural"):
        with_shocks(cal.fundamentals, core=data.core, a_TH=params.a_TH, rural_amenity_pct=5.0)


@pytest.mark.parametrize(
    "shock",
    [{"metro_travel_cut_pct": 100.0}, {"core_floor_supply_pct": -100.0}, {"rural_amenity_pct": "x"}],
)
def test_api_rejects_out_of_range_shocks(shock):
    with pytest.raises(ValueError):
        api.run({"region": "synthetic", "shocks": shock})


def test_zero_new_shocks_change_nothing():
    sc = api.default_scenario()
    sc["shocks"].update(core_productivity_pct=0.0, periods=10)
    lr = api.run(sc)["long_run"]
    assert max(abs(v) for v in lr["dN_pct"]) < 1e-7
