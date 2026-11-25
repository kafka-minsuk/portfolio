"""Every region in docs/migration/data/regions.json runs in the browser contract with its default
scenario: calibration reproduces its data, and the long run and the path converge under the page's
gate (docs/migration/app.js TOL), so no state shows the 'did not converge' message by default."""

import json
from pathlib import Path

import pytest

from urqse import api

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "docs" / "migration" / "data"
REGIONS = [r["id"] for r in json.loads((DATA / "regions.json").read_text())["regions"]]
GATE_TOL = 1e-8


def test_every_supported_state_is_in_the_menu():
    from urqse.data.build_state import STATES, UNSUPPORTED

    assert {r.split("_")[0] for r in REGIONS} == set(STATES) - set(UNSUPPORTED)


@pytest.mark.parametrize("region", REGIONS)
def test_region_default_converges_under_the_web_gate(region):
    doc = json.loads((DATA / f"{region}.json").read_text())
    out = api.run(api.default_scenario(doc), doc)
    assert max(out["calibration"]["max_rel_error"].values()) < 1e-7
    for solve in (out["calibration"]["solve"], out["long_run"]["solve"]):
        assert solve["converged"] and solve["residual_inf"] <= GATE_TOL
    assert out["path"]["all_converged"] and out["path"]["worst_residual"] <= GATE_TOL
    # the path closes the utility gap: matched (0.1%), or nearly so at the horizon in states whose
    # counties are far apart (Nevada: 2.4% left after 400 periods)
    P = out["path"]
    gap = P["utility_gap"][P["stop"]["period"]]
    assert gap < 0.03 and (P["stop"]["reason"] == "utility_matched") == (gap < P["gap_tol"])
