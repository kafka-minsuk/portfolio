"""Real-data regression snapshot (CLAUDE.md): the Iowa 2022 calibration reproduces the pinned
numbers in tests/snapshots/IA_2022.json. Skips on a fresh clone (data/ and data_raw/ are not
tracked). Regenerate on purpose with `python -m urqse.calibrate.run_state IA 2022 --snapshot`."""

import json
from pathlib import Path

import pytest

pytest.importorskip("pandas")
pytest.importorskip("geopandas")

from urqse.calibrate import run_state as rs  # noqa: E402
from urqse.data.loaders import COUNTY_FILE, state_dir  # noqa: E402
from urqse.model.params import Params  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = json.loads((ROOT / "tests" / "snapshots" / "IA_2022.json").read_text())
RAW = ROOT / "data_raw" / "IA"
IA_NEIGHBOR_COUNTIES = ["17", "27", "29", "31", "46", "55"]  # IL MN MO NE SD WI: one county each is enough
LODES = rs.lodes_paths("IA", 2022, [f + "001" for f in IA_NEIGHBOR_COUNTIES], download=False)
HAVE_DATA = (state_dir("IA", 2022) / COUNTY_FILE).exists() and all(p.exists() for p in LODES)


@pytest.mark.skipif(not HAVE_DATA, reason="Iowa data or LODES downloads not present")
def test_iowa_calibration_snapshot():
    r = rs.run("IA", 2022, RAW, state_dir("IA", 2022))
    assert all(err < 1e-7 for err in r["cal"].max_rel_error.values())
    assert r["cal"].baseline.info.converged
    assert all(g.info.converged for g in r["gravity"].values())
    # spec §12.1 income routing: labour + owner rent + landlord rent = w_A H_A + rho T^F
    assert abs(r["accounts"]["identity_rel"]) < 1e-12
    got = rs.snapshot(r)
    assert set(got) == set(SNAPSHOT)
    for k, v in SNAPSHOT.items():
        assert got[k] == pytest.approx(v, rel=1e-6, abs=1e-9), k


def test_state_params_layer_estimates_over_untouched_defaults():
    p = rs.state_params("IA", 2022)
    assert p.kappa_lam == pytest.approx(SNAPSHOT["kappa_lam"], rel=1e-12)
    assert p.theta_T == pytest.approx(SNAPSHOT["theta_T"], rel=1e-12)
    assert Params().kappa_lam == 0.08 and Params().theta_T == 0.40
