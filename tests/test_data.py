"""County data build (src/urqse/data): pure builder functions, schema and loader. No network."""

import subprocess
import sys
import zipfile
from pathlib import Path

import numpy as np
import pytest

pd = pytest.importorskip("pandas")
pytest.importorskip("pandera")
pytest.importorskip("pyarrow")

from urqse.calibrate.invert import calibrate  # noqa: E402
from urqse.data import build_state as bs  # noqa: E402
from urqse.data.loaders import COUNTY_FILE, TRAVEL_FILE, load_state, read_county, state_dir  # noqa: E402
from urqse.data.schema import COLUMNS, COUNTY_SCHEMA, EXTERNAL_FIPS  # noqa: E402
from urqse.model.params import Params  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


# --- reconciliation and fills ---------------------------------------------------------------


def test_reconcile_jobs_closes_with_external_zone():
    res, out, work = np.array([100.0, 50.0]), np.array([10.0, 2.0]), np.array([120.0, 40.0])
    HU_bea, HA_bea = np.array([140.0, 30.0]), np.array([10.0, 20.0])
    j = bs.reconcile_jobs(res, out, work, HU_bea, HA_bea)
    assert np.isclose(j["N"].sum(), j["HU"].sum() + j["HA"].sum(), rtol=1e-14)
    # each county keeps its BEA farm/non-farm mix and its ACS workplace headcount
    np.testing.assert_allclose(j["HA"][:2] / j["HU"][:2], HA_bea / HU_bea)
    np.testing.assert_allclose((j["HU"] + j["HA"])[:2], work)
    # external: in-commuters = 160 - (150 - 12) = 22 residents; 12 out-of-state jobs
    assert j["N"][-1] == pytest.approx(22.0)
    assert j["HU"][-1] + j["HA"][-1] == pytest.approx(12.0)


def test_reconcile_jobs_needs_cross_border_commuting():
    with pytest.raises(ValueError, match="external zone"):
        bs.reconcile_jobs(np.array([10.0]), np.array([0.0]), np.array([10.0]), np.array([5.0]), np.array([5.0]))


def test_fill_suppressed_allocates_residual_by_weight():
    v, miss = bs.fill_suppressed(np.array([10.0, np.nan, 5.0, np.nan]), 30.0, np.array([1.0, 1.0, 1.0, 3.0]))
    np.testing.assert_allclose(v, [10.0, 3.75, 5.0, 11.25])
    assert miss.tolist() == [False, True, False, True]
    same, none = bs.fill_suppressed(np.array([1.0, 2.0]), 99.0, np.ones(2))
    assert same.tolist() == [1.0, 2.0] and not none.any()
    with pytest.raises(ValueError):
        bs.fill_suppressed(np.array([10.0, np.nan]), 5.0, np.ones(2))


def test_county_kinds():
    kind = bs.county_kinds(["a", "b", "c", "d"], np.array([5.0, 9.0, 50.0, 1.0]), metro={"a", "b"})
    assert kind.tolist() == ["suburb", "core", "rural", "rural"]


# --- travel ---------------------------------------------------------------------------------


def test_travel_with_external_uses_nearest_outside_point():
    # points 0, 1 in state; 2, 3 outside
    t_pts = np.array([[0, 10, 30, 50], [11, 0, 70, 20], [31, 71, 0, 5], [52, 19, 6, 0]], float)
    t, d = bs.travel_with_external(t_pts, t_pts * 2, 2, own_t=np.array([3.0, 4.0]), own_d=np.array([6.0, 8.0]))
    assert t.shape == (3, 3)
    assert t[0, 1] == 10 and t[1, 0] == 11
    assert t[0, 2] == 30 and t[1, 2] == 20 and t[2, 0] == 31 and t[2, 1] == 19
    assert np.diag(t).tolist() == [3.0, 4.0, 3.5]
    assert d[1, 2] == 40 and d[2, 2] == 7.0


def test_own_trip_square_county():
    t_pts = np.array([[0.0, 60.0], [60.0, 0.0]])
    d_line = np.array([[0.0, 30.0], [30.0, 0.0]])  # 0.5 km per minute
    own_t, own_d, speed = bs.own_trip(np.array([400.0, 100.0]), t_pts, d_line, 2)
    assert speed == pytest.approx(0.5)
    np.testing.assert_allclose(own_d, bs.SQUARE_MEAN_DIST * np.array([20.0, 10.0]))
    np.testing.assert_allclose(own_t, own_d / 0.5)


def test_haversine_one_degree_latitude():
    assert bs.haversine_km(40.0, -93.0, 41.0, -93.0) == pytest.approx(111.2, abs=0.1)


# --- parsers --------------------------------------------------------------------------------


def _bea_zip(path):
    rows = [
        "GeoFIPS,GeoName,Region,TableName,LineCode,IndustryClassification,Description,Unit,2021,2022",
        '"19000","Iowa",4,CAEMP25N,70,...,Farm employment,Number of jobs,90,100',
        '" 19001","Adair, IA",4,CAEMP25N,70,...,Farm employment,Number of jobs,40,(D)',
        '" 19001","Adair, IA",4,CAEMP25N,80,...,Nonfarm employment,Number of jobs,400,410',
        '" 19003","Adams, IA",4,CAEMP25N,70,...,Farm employment,Number of jobs,50,"1,060"',
        '" 19003","Adams, IA",4,CAEMP25N,80,...,Nonfarm employment,Number of jobs,300,310',
        '"Note: See the included footnote file."',
    ]
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("CAEMP25N_IA_2001_2022.csv", "\n".join(rows))
        z.writestr("CAEMP25N_AK_2001_2022.csv", rows[0])
    return path


def test_read_bea_codes_and_suppression(tmp_path):
    df = bs.read_bea(_bea_zip(tmp_path / "bea.zip"), "IA", 2022, {"HA": 70, "HU": 80})
    assert df.loc["19000", "HA"] == 100
    assert np.isnan(df.loc["19001", "HA"]) and df.loc["19001", "HU"] == 410
    assert df.loc["19003", "HA"] == 1060
    assert set(df.index) == {"19000", "19001", "19003"}


def test_read_acs_keeps_state_and_its_counties(tmp_path):
    p = tmp_path / "t.dat"
    p.write_text(
        "GEO_ID|B08604_E001|B08604_M001\n0100000US|100|1\n0400000US19|30|2\n"
        "0500000US19001|10|1\n0500000US19003|20|1\n0500000US20001|99|1\n"
    )
    df = bs.read_acs(p, {"B08604_E001": "work"}, "19")
    assert df["work"].to_dict() == {"19": 30, "19001": 10, "19003": 20}


def _nass(rows):
    cols = ["SOURCE_DESC", "SHORT_DESC", "DOMAIN_DESC", "AGG_LEVEL_DESC", "STATE_ALPHA", "COUNTY_ANSI",
            "COUNTY_NAME", "YEAR", "REFERENCE_PERIOD_DESC", "VALUE"]  # fmt: skip
    return pd.DataFrame([dict(zip(cols, r)) for r in rows])


def test_nass_series_suppression_other_and_state():
    sd = "RENT, CASH, CROPLAND, NON-IRRIGATED - EXPENSE, MEASURED IN $ / ACRE"
    df = _nass([
        ("SURVEY", sd, "TOTAL", "COUNTY", "IA", "001", "ADAIR", "2022", "YEAR", "250"),
        ("SURVEY", sd, "TOTAL", "COUNTY", "IA", "003", "ADAMS", "2022", "YEAR", "(D)"),
        ("SURVEY", sd, "TOTAL", "COUNTY", "IA", "", "OTHER COUNTIES", "2022", "YEAR", "248"),
        ("SURVEY", sd, "TOTAL", "COUNTY", "IA", "005", "ALLAMAKEE", "2021", "YEAR", "1"),
        ("SURVEY", sd, "TOTAL", "STATE", "IA", "", "", "2022", "YEAR", "1,256"),
        ("SURVEY", sd, "TOTAL", "STATE", "IA", "", "", "2022", "END OF DEC", "7"),
        ("CENSUS", sd, "TOTAL", "COUNTY", "IA", "001", "ADAIR", "2022", "YEAR", "999"),
    ])  # fmt: skip
    s = bs.nass_series(df, sd, 2022, "SURVEY", "19")
    assert s["county"].loc["19001"] == 250 and np.isnan(s["county"].loc["19003"])
    assert s["suppressed"] == ["19003"]
    assert s["other"] == 248 and s["state"] == 1256
    assert "19005" not in s["county"].index


# --- rasters --------------------------------------------------------------------------------


def _raster(path, data, nodata=None):
    rasterio = pytest.importorskip("rasterio")
    from rasterio.transform import from_origin

    profile = dict(driver="GTiff", width=data.shape[1], height=data.shape[0], count=1, dtype=data.dtype,
                   crs="EPSG:5070", transform=from_origin(0, 100, 10, 10), nodata=nodata)  # fmt: skip
    with rasterio.open(path, "w", **profile) as dst:
        dst.write(data, 1)
    return path


def test_zonal_class_area_and_sum(tmp_path):
    box = pytest.importorskip("shapely.geometry").box
    classes = np.zeros((10, 10), np.uint8)
    classes[:, :5] = 1  # left half crop
    classes[:5, 5:] = 176  # top-right pasture
    left, right = box(0, 0, 50, 100), box(50, 0, 100, 100)  # 10 m pixels, 100 m square
    a = bs.zonal_class_area(_raster(tmp_path / "c.tif", classes), [left, right])
    assert a[0, 1] == 50 * 100 and a[0].sum() == 50 * 100
    assert a[1, 176] == 25 * 100 and a[1, 0] == 25 * 100
    vol = np.arange(100, dtype=np.uint32).reshape(10, 10)
    vol[0, 0] = 4294967295
    s = bs.zonal_sum([_raster(tmp_path / "v.tif", vol, nodata=4294967295)], [left, right])
    expect_left = vol[:, :5].astype(float).sum() - 4294967295
    assert s[0] == expect_left and s[1] == vol[:, 5:].astype(float).sum()


# --- schema and loader ----------------------------------------------------------------------


def _table():
    """Two counties plus the external zone, internally consistent."""
    rows = []
    for i, (fips, kind) in enumerate((("19001", "core"), ("19003", "rural"), (EXTERNAL_FIPS, "external"))):
        rows.append({c: np.nan for c in COLUMNS} | dict(
            fips=fips, name=f"zone {i}", kind=kind, lat=41.0 + i * 0.3, lon=-93.0 - i * 0.4,
            x_km=400.0 + 30 * i, y_km=4500.0 + 20 * i, L=1e6 * (3 - i), TF=1e4 * (1 + i),
            wA_obs_usd=40_000.0 + 5_000 * i, omega=0.5, gateway=1.0 if i < 2 else 0.0,
            own_time_min=15.0, own_dist_km=12.0, cash_rent_filled=False,
        ))  # fmt: skip
    df = pd.DataFrame(rows)
    df["N"] = [1000.0, 400.0, 60.0]
    df["HA"] = [20.0, 80.0, 3.0]
    df["HU"] = [1100.0, 220.0, 37.0]  # 1460 workers = 1420 county jobs + 40 out of state
    df.loc[:1, "HU_bea"] = [1500.0, 300.0]
    df.loc[:1, "nonfarm_earn_usd"] = [1500.0 * 60_000, 300.0 * 50_000]
    return df


def _write(root, df, t=None):
    d = state_dir("IA", 2022, root)
    d.mkdir(parents=True)
    df.to_parquet(d / COUNTY_FILE, index=False)
    Z = len(df)
    if t is None:
        t = 15.0 + 20.0 * np.abs(np.subtract.outer(np.arange(Z), np.arange(Z)))
    np.savez_compressed(d / TRAVEL_FILE, fips=df["fips"].to_numpy(str), t=t, dist=t.copy())
    return d


def test_schema_accepts_consistent_table():
    COUNTY_SCHEMA.validate(_table())


def test_schema_rejects_jobs_not_equal_workers():
    df = _table()
    df.loc[0, "N"] += 1.0
    with pytest.raises(Exception, match="jobs must equal resident workers"):
        COUNTY_SCHEMA.validate(df)


def test_schema_rejects_missing_external_zone_and_bad_shares():
    df = _table().iloc[:2].copy()
    df["N"] = df["HU"] + df["HA"]
    with pytest.raises(Exception, match="external zone"):
        COUNTY_SCHEMA.validate(df)
    bad = _table()
    bad.loc[1, "omega"] = 1.2
    with pytest.raises(Exception):
        COUNTY_SCHEMA.validate(bad)


def test_loader_builds_county_data_that_calibrates(tmp_path):
    _write(tmp_path, _table())
    data = load_state("IA", 2022, root=tmp_path)
    assert data.N.shape == (3,) and data.t.shape == (3, 3)
    assert data.kind[data.core] == "core" and data.kind[-1] == "external"
    mean_nonfarm = (1500 * 60_000 + 300 * 50_000) / 1800
    np.testing.assert_allclose(data.wA_obs, _table()["wA_obs_usd"] / mean_nonfarm)
    cal = calibrate(data, Params())
    assert cal.wage_info.converged and max(cal.max_rel_error.values()) < 1e-7


def test_loader_rejects_travel_rows_out_of_order(tmp_path):
    d = _write(tmp_path, _table())
    with np.load(d / TRAVEL_FILE) as z:
        t = z["t"]
    np.savez_compressed(d / TRAVEL_FILE, fips=np.array(["19003", "19001", "EXT"]), t=t, dist=t)
    with pytest.raises(ValueError, match="do not match"):
        load_state("IA", 2022, root=tmp_path)


def test_loader_rejects_nonpositive_travel(tmp_path):
    t = np.full((3, 3), 10.0)
    t[0, 0] = 0.0
    _write(tmp_path, _table(), t=t)
    with pytest.raises(ValueError, match="positive"):
        load_state("IA", 2022, root=tmp_path)


# --- the browser boundary never sees the data build ------------------------------------------


def test_bundle_excludes_data_package_and_api_needs_no_pandas(tmp_path):
    sys.path.insert(0, str(ROOT / "scripts"))
    try:
        import build_py_bundle
    finally:
        sys.path.pop(0)
    names = zipfile.ZipFile(build_py_bundle.build(tmp_path / "b.zip")).namelist()
    assert "urqse/api.py" in names and not any(n.startswith("urqse/data/") for n in names)
    assert not {"urqse/" + f for f in build_py_bundle.OFFLINE} & set(names)
    code = "import sys, urqse.api; sys.exit(int(any(m in sys.modules for m in ('pandas', 'rasterio', 'pandera'))))"
    assert subprocess.run([sys.executable, "-c", code], cwd=ROOT).returncode == 0


# --- built Iowa table (skipped until `python -m urqse.data.build_state IA 2022` has run) ------

IA_DIR = state_dir("IA", 2022)


@pytest.mark.skipif(not (IA_DIR / COUNTY_FILE).exists(), reason="Iowa data not built")
def test_iowa_build_snapshot():
    df = read_county(IA_DIR / COUNTY_FILE)
    c = df[df["kind"] != "external"]
    assert len(c) == 99 and df["fips"].iloc[-1] == EXTERNAL_FIPS
    assert c["pop"].sum() == 3_200_517  # PEP Vintage 2022, Iowa July 1 2022
    assert c["HA_bea"].sum() == 89_652 and c["HU_bea"].sum() == 2_024_343  # BEA CAEMP25N 2022 L70, L80
    assert c.loc[c["kind"] == "core", "name"].item() == "Polk"
    data = load_state("IA", 2022)
    assert data.t.shape == (100, 100) and np.isclose(data.N.sum(), data.HU.sum() + data.HA.sum())


def test_build_cli_rejects_unknown_state():
    with pytest.raises(SystemExit):
        bs.main(["ZZ", "2022"])


def test_to_number_handles_codes():
    s = bs.to_number(pd.Series(["1,234", "(D)", " 5 ", "(NA)", "-3"]))
    assert s.iloc[0] == 1234 and np.isnan(s.iloc[1]) and s.iloc[2] == 5 and np.isnan(s.iloc[3]) and s.iloc[4] == -3



def test_zero_gateway_gets_no_arrivals():
    import warnings

    from urqse.model.immigration import arrival_shares

    with warnings.catch_warnings():
        warnings.simplefilter("error")
        s = arrival_shares(np.zeros(3), np.zeros(3), np.array([1.0, 0.0, 2.0]), 2.0)
    assert s[1] == 0.0 and abs(s.sum() - 1.0) < 1e-12
