"""The browser contract: JSON-only output, documented keys, no change without a shock."""

import json

import pytest

from urqse import api

ZERO = {
    "core_productivity_pct": 0.0,
    "farm_tfp_pct": 0.0,
    "travel_cut_pct": 0.0,
    "immigration_per_period": 0.0,
    "periods": 20,
}


@pytest.fixture(scope="module")
def default_out():
    return api.run(api.default_scenario())


def test_default_run_is_strict_json_and_converged(default_out):
    text = json.dumps(default_out, allow_nan=False)
    assert json.loads(text) == default_out
    assert default_out["calibration"]["solve"]["converged"]
    assert default_out["long_run"]["solve"]["converged"]
    assert default_out["path"]["all_converged"]
    assert default_out["analytic"]["converged"]
    assert set(default_out["units"]) >= {"N", "TF", "immigration_per_period", "period"}


def test_default_run_shape(default_out):
    Z = len(default_out["counties"])
    assert Z == 25
    assert sorted({c["kind"] for c in default_out["counties"]}) == ["core", "rural", "suburb"]
    path = default_out["path"]
    T = api.default_scenario()["shocks"]["periods"]
    assert path["t"] == list(range(T + 1))
    assert len(path["N"]) == T + 1 and all(len(row) == Z for row in path["N"])
    assert path["N"][0] == pytest.approx([c["N0"] for c in default_out["counties"]], rel=1e-12)
    assert path["stop"]["period"] in path["t"]
    assert path["land_per_worker_ratio"][0] == 1.0
    assert path["farmland_price_index"][0] == 1.0
    assert path["urban_rent_index"][0] == 1.0
    for key in ("N", "dN_pct", "wA_pct", "rho_pct", "r_pct", "HA_pct"):
        assert len(default_out["long_run"][key]) == Z


def test_urban_productivity_shock_moves_people_out_of_rural_counties(default_out):
    totals = default_out["long_run"]["totals"]
    assert totals["rural_residents_pct"] < 0
    assert totals["land_per_farm_worker_pct"] > 0
    assert totals["farmland_rent_pct"] < 0
    assert totals["core_rent_pct"] > 0
    assert abs(totals["region_pop_pct"]) < 1e-6


def test_zero_shock_changes_nothing():
    out = api.run({"shocks": ZERO})
    lr = out["long_run"]
    for key in ("dN_pct", "wA_pct", "rho_pct", "r_pct", "HA_pct"):
        assert max(abs(v) for v in lr[key]) < 1e-7
    assert all(abs(v) < 1e-7 for v in lr["totals"].values())
    assert abs(lr["welfare_pct"]) < 1e-8
    assert max(abs(v - 1.0) for v in out["path"]["farmland_price_index"]) < 1e-9
    assert out["path"]["stop"] == {"period": 1, "reason": "steady_state"}
    assert abs(out["wealth"]["stayer_pct"]) < 1e-8 and abs(out["wealth"]["leaver_pct"]) < 1e-8


@pytest.mark.parametrize(
    "scenario",
    [
        {"params": {"lam": 0.5}},
        {"params": {"nope": 1.0}},
        {"params": {"eta": float("nan")}},
        {"params": {"land_income_in_choice": 1}},
        {"shocks": {"travel_cut_scope": "sideways"}},
        {"shocks": {"periods": 2.5}},
        {"shocks": {"immigration_per_period": -1.0}},
        "not a dict",
    ],
)
def test_bad_scenarios_raise_value_error(scenario):
    with pytest.raises(ValueError):
        api.run(scenario)
