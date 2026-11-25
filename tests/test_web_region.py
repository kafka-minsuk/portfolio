"""Regions in the browser contract: the synthetic default is unchanged, and the tracked Iowa
region document (docs/migration/data/IA_2022.json) runs, converges and reports real units."""

import json
from pathlib import Path

import numpy as np
import pytest

from urqse import api
from urqse.model.params import Params

ROOT = Path(__file__).resolve().parents[1]
DOC = json.loads((ROOT / "docs" / "migration" / "data" / "IA_2022.json").read_text())
SYNTHETIC_SNAPSHOT = ROOT / "tests" / "snapshots" / "synthetic_default.json"
GATE_TOL = 1e-8  # docs/migration/app.js TOL: results are hidden above it
ZERO = {"core_productivity_pct": 0.0, "farm_tfp_pct": 0.0, "travel_cut_pct": 0.0, "periods": 20}


def assert_same(got, want, path="out"):
    if isinstance(want, dict):
        assert set(got) == set(want), path
        for k in want:
            assert_same(got[k], want[k], f"{path}.{k}")
    elif isinstance(want, list):
        assert len(got) == len(want), path
        for i, (g, w) in enumerate(zip(got, want)):
            assert_same(g, w, f"{path}[{i}]")
    elif isinstance(want, float) and not isinstance(got, bool):
        assert got == pytest.approx(want, rel=1e-12, abs=1e-15), path
    else:
        assert got == want, path


@pytest.fixture(scope="module")
def iowa():
    return api.run(api.default_scenario(DOC), DOC)


def test_synthetic_default_matches_the_pinned_output():
    """Pinned before regions existed; adding regions must not move a synthetic number."""
    assert_same(api.run(api.default_scenario()), json.loads(SYNTHETIC_SNAPSHOT.read_text()))
    assert api.default_scenario()["region"] == "synthetic"


def test_region_defaults_layer_estimates_over_params():
    sc = api.default_scenario(DOC)
    assert sc["region"] == "IA_2022"
    assert sc["params"]["kappa_lam"] == DOC["params"]["kappa_lam"]
    assert sc["params"]["theta_T"] == DOC["params"]["theta_T"]
    p = Params()
    for k in set(api.SCENARIO_PARAMS) - set(DOC["params"]):
        assert sc["params"][k] == getattr(p, k), k
    assert api.default_scenario()["params"]["kappa_lam"] == p.kappa_lam == 0.08


def test_region_document_shape():
    """Iowa carries a metro nest: 94 counties outside Des Moines' metro area, its 162 tracts, the
    external zone; the state map keeps 99 counties + the external zone."""
    data = api.county_data(DOC)
    Z = len(data.names)
    assert Z == 256 and data.t.shape == data.dist.shape == (Z, Z)
    assert (data.nest == 0).sum() == 162 and data.names[data.core].endswith("Polk")
    assert data.kind[-1] == "external"
    cv = DOC["county_view"]
    assert len(cv["fips"]) == 100 and cv["name"][cv["kind"].index("core")] == "Polk"
    assert len(DOC["geometry"]) == 100 and DOC["geometry"][-1] is None and all(g for g in DOC["geometry"][:-1])
    assert len(DOC["city"]["geometry"]) == 162 and all(DOC["city"]["geometry"])


def test_state_view_is_the_sum_of_the_tracts(iowa):
    city, cv = iowa["city"], iowa["counties"]
    assert len(cv) == 100 and len(city["zones"]) == 162
    polk = next(c for c in cv if c["name"] == "Polk")
    tracts = [i for i, z in enumerate(city["zones"]) if z["county_index"] == polk["id"]]
    assert polk["tracts"] == len(tracts) == 112
    assert sum(city["long_run"]["N"][i] for i in tracts) == pytest.approx(iowa["long_run"]["N"][polk["id"]], rel=1e-12)
    assert sum(city["zones"][i]["N0"] for i in tracts) == pytest.approx(polk["N0"], rel=1e-12)
    T = len(iowa["path"]["t"])
    assert len(city["path"]["N"]) == T and len(city["path"]["N"][0]) == 162


def test_iowa_default_converges_under_the_web_gate(iowa):
    assert json.loads(json.dumps(iowa, allow_nan=False)) == iowa
    for solve in (iowa["calibration"]["solve"], iowa["long_run"]["solve"]):
        assert solve["converged"] and solve["residual_inf"] <= GATE_TOL
    assert iowa["path"]["all_converged"] and iowa["path"]["worst_residual"] <= GATE_TOL
    assert max(iowa["calibration"]["max_rel_error"].values()) < 1e-7
    assert iowa["region"]["core_label"] == "Polk (Des Moines)"


def test_iowa_levels_agree_with_the_percent_totals(iowa):
    lv, tot = iowa["levels"], iowa["long_run"]["totals"]
    pct = lambda pair: 100.0 * (pair[1] / pair[0] - 1.0)  # noqa: E731
    assert pct(lv["rural_residents"]) == pytest.approx(tot["rural_residents_pct"], rel=1e-9)
    assert pct(lv["land_per_farm_worker_acres"]) == pytest.approx(tot["land_per_farm_worker_pct"], rel=1e-9)
    assert pct(lv["farm_wage_usd"]) == pytest.approx(tot["farm_wage_pct"], rel=1e-9)
    assert pct(lv["farmland_rent_usd_acre"]) == pytest.approx(tot["farmland_rent_pct"], rel=1e-9)
    # report §3: model rent at the estimated theta_T sits at the NASS level (154 to 304 $/acre)
    assert 150 < lv["farmland_rent_usd_acre"][0] < 320


def test_iowa_zero_shock_changes_nothing():
    sc = api.default_scenario(DOC)
    sc["shocks"].update(ZERO)
    lr = api.run(sc, DOC)["long_run"]
    for key in ("dN_pct", "wA_pct", "rho_pct", "r_pct", "HA_pct"):
        assert max(abs(v) for v in lr[key]) < 1e-7
    assert all(abs(v) < 1e-7 for v in lr["totals"].values())


@pytest.mark.parametrize(
    "scenario, doc",
    [
        ({"region": "IA_2022"}, None),
        ({"region": "IA_2022"}, {**DOC, "region": "XX_1999"}),
        ({"region": "IA_2022"}, {**DOC, "format": 0}),
        ({"region": "synthetic", "extra": 1}, None),
    ],
)
def test_bad_regions_raise_value_error(scenario, doc):
    with pytest.raises(ValueError):
        api.run(scenario, doc)


def test_document_matches_the_built_state():
    """The exported arrays are the built state's, up to the documented travel-matrix rounding."""
    pytest.importorskip("pandas")
    from urqse.calibrate.run_state import state_params
    from urqse.data.loaders import METRO_FILE, load_metro, state_dir

    if not (state_dir("IA", 2022) / METRO_FILE).exists():
        pytest.skip("Iowa metro data not built")
    built, doc = load_metro("IA", 2022), api.county_data(DOC)
    np.testing.assert_array_equal(doc.nest, built.nest)
    assert built.names == doc.names and list(built.kind) == list(doc.kind)
    for k in ("x", "y", "N", "HU", "HA", "L", "TF", "wA_obs", "omega", "gateway"):
        np.testing.assert_array_equal(getattr(doc, k), getattr(built, k), err_msg=k)
    np.testing.assert_allclose(doc.t, built.t, atol=0.005 + 1e-12)
    np.testing.assert_allclose(doc.dist, built.dist, atol=0.005 + 1e-12)
    p = state_params("IA", 2022)
    assert DOC["params"] == {"kappa_lam": p.kappa_lam, "theta_T": p.theta_T}
    # the rounding moves the headline totals by well under 0.001 percentage points
    full = {**DOC, "t_min": built.t.tolist(), "dist_km": built.dist.tolist()}
    sc = api.default_scenario(DOC)
    got, want = api.run(sc, DOC)["long_run"]["totals"], api.run(sc, full)["long_run"]["totals"]
    for k in want:
        assert got[k] == pytest.approx(want[k], abs=1e-3), k
