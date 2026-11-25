"""All-states build (src/urqse/data/build_state, calibrate/run_state): state table, GHSL tiles,
map projection, BEA combination areas, zone sums. No network."""

import zipfile

import numpy as np
import pytest

pd = pytest.importorskip("pandas")
gpd = pytest.importorskip("geopandas")

from shapely.geometry import box  # noqa: E402

from urqse.calibrate import run_state as rs  # noqa: E402
from urqse.data import build_state as bs  # noqa: E402


def test_state_table_covers_50_states_and_dc():
    assert len(bs.STATES) == 51 and len(set(bs.STATE_FIPS.values())) == 51
    assert bs.STATE_FIPS["IA"] == "19" and bs.FIPS_STATE["48"] == "TX"
    assert set(bs.UNSUPPORTED) <= set(bs.STATES)
    assert set(bs.UNSUPPORTED) == {"AK", "HI", "CT", "DC"}  # zero-farm counties are allowed (spec §3.11)


def test_unsupported_state_exits_with_its_reason():
    with pytest.raises(SystemExit, match="not built"):
        bs.main(["HI", "2022"])


def test_ghsl_tiles_from_tile_corners():
    # Iowa's Mollweide bounds (2026-11-24) touch R4_C11, R5_C10 and R5_C11 only
    iowa = box(-8_089_193.0, 4_831_345.0, -7_486_556.0, 5_176_865.0)
    assert set(bs.ghsl_tiles([iowa])) <= {"R4_C10", "R4_C11", "R5_C10", "R5_C11"}
    one = box(-9_000_000.0, 5_100_000.0, -8_900_000.0, 5_200_000.0)  # inside R4_C10 (x -9041..-8041 km, y 5000..6000 km)
    assert bs.ghsl_tiles([one]) == ("R4_C10",)


def test_utm_zone_at_the_middle_longitude():
    assert bs.utm_epsg(-96.6, -90.1) == 26915  # Iowa
    assert bs.utm_epsg(-106.6, -93.5) == 26914  # Texas
    assert bs.utm_epsg(-71.1, -66.9) == 26919  # Maine


def _bea_with_combo(path):
    rows = [
        "GeoFIPS,GeoName,Region,TableName,LineCode,IndustryClassification,Description,Unit,2022",
        '"51000","Virginia",5,CAEMP25N,70,...,Farm employment,Number of jobs,100',
        '" 51001","Accomack, VA",5,CAEMP25N,70,...,Farm employment,Number of jobs,10',
        '" 51919","Fairfax, Fairfax City + Falls Church, VA*",5,CAEMP25N,70,...,Farm employment,Number of jobs,5',
        '" 51949","Southampton + Franklin, VA*",5,CAEMP25N,70,...,Farm employment,Number of jobs,7',
    ]
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("CAEMP25N_VA_2001_2022.csv", "\n".join(rows))
    return path


def _va_counties():
    rows = [("51001", "Accomack", "Accomack County"), ("51059", "Fairfax", "Fairfax County"),
            ("51600", "Fairfax", "Fairfax city"), ("51610", "Falls Church", "Falls Church city"),
            ("51175", "Southampton", "Southampton County"), ("51067", "Franklin", "Franklin County"),
            ("51620", "Franklin", "Franklin city")]  # fmt: skip
    geoms = [box(i, 0, i + 1, 1) for i in range(len(rows))]
    df = gpd.GeoDataFrame(
        {"GEOID": [r[0] for r in rows], "NAME": [r[1] for r in rows], "NAMELSAD": [r[2] for r in rows],
         "STATEFP": "51", "ALAND": 1e6}, geometry=geoms, crs=4326,
    )  # fmt: skip
    return df.set_index("GEOID")


def test_bea_combinations_first_name_is_the_county_the_rest_cities(tmp_path):
    combos = bs.bea_combinations(_bea_with_combo(tmp_path / "bea.zip"), "VA", _va_counties())
    assert combos["51919"] == ("Fairfax, Fairfax City + Falls Church", ["51059", "51600", "51610"])
    assert combos["51949"][1] == ["51175", "51620"]  # Franklin city, not Franklin County
    assert "51001" not in combos


def test_state_zones_merge_combinations_and_sum_counties(tmp_path):
    zones, zone_of = bs.state_zones(_va_counties(), _bea_with_combo(tmp_path / "bea.zip"), "VA")
    assert list(zones.index) == ["51001", "51067", "51919", "51949"]
    assert zone_of["51600"] == "51919" and zone_of["51001"] == "51001"
    assert zones.loc["51919", "ALAND"] == 3e6 and zones.loc["51949", "NAME"] == "Southampton + Franklin"
    pop = pd.Series({"51001": 10.0, "51059": 100.0, "51600": 20.0, "51610": np.nan, "51175": 5.0, "51620": 7.0, "51067": 1.0})
    z = bs.to_zones(pop, zone_of)
    assert z["51919"] == 120.0 and z["51949"] == 12.0
    rent = pd.Series({"51059": 100.0, "51600": 200.0, "51175": np.nan, "51620": np.nan})
    w = pd.Series({"51059": 3.0, "51600": 1.0})
    zr = bs.to_zones(rent, zone_of, w)
    assert zr["51919"] == pytest.approx(125.0) and np.isnan(zr["51949"])


def test_fill_suppressed_signed_line_allows_negative_residual():
    v, miss = bs.fill_suppressed(np.array([50.0, np.nan]), 20.0, np.ones(2), signed=True)
    assert v[1] == -30.0 and miss.tolist() == [False, True]
    with pytest.raises(ValueError):
        bs.fill_suppressed(np.array([50.0, np.nan]), 20.0, np.ones(2))


def test_nass_cash_rent_other_counties_by_district():
    sd = "RENT, CASH, CROPLAND, NON-IRRIGATED - EXPENSE, MEASURED IN $ / ACRE"
    cols = ["SOURCE_DESC", "SHORT_DESC", "DOMAIN_DESC", "AGG_LEVEL_DESC", "STATE_ALPHA", "ASD_CODE", "COUNTY_ANSI",
            "COUNTY_NAME", "YEAR", "REFERENCE_PERIOD_DESC", "VALUE"]  # fmt: skip
    rows = [
        ("SURVEY", sd, "TOTAL", "COUNTY", "NE", "10", "001", "ADAMS", "2022", "YEAR", "200"),
        ("SURVEY", sd, "TOTAL", "COUNTY", "NE", "10", "", "OTHER (COMBINED) COUNTIES", "2022", "YEAR", "150"),
        ("SURVEY", sd, "TOTAL", "COUNTY", "NE", "20", "", "OTHER (COMBINED) COUNTIES", "2022", "YEAR", "90"),
        ("SURVEY", sd, "TOTAL", "STATE", "NE", "", "", "", "2022", "YEAR", "162"),
    ]
    s = bs.nass_series(pd.DataFrame(rows, columns=cols), sd, 2022, "SURVEY", "31")
    assert s["other_by_district"].to_dict() == {"10": 150.0, "20": 90.0}
    assert np.isnan(s["other"]) and s["state"] == 162.0


def test_lodes_neighbor_states_from_external_counties():
    assert rs.neighbor_states(["17001", "27005", "17003", "55001"]) == ("il", "mn", "wi")
    paths = rs.lodes_paths("IA", 2022, ["17001", "31001"], download=False)
    assert [p.name for p in paths] == ["ia_od_main_JT00_2022.csv.gz", "ia_od_aux_JT00_2022.csv.gz",
                                       "il_od_aux_JT00_2022.csv.gz", "ne_od_aux_JT00_2022.csv.gz"]  # fmt: skip


def test_county_flows_map_merged_counties_to_their_zone(tmp_path):
    od = pd.DataFrame({"w_geocode": ["516000000000001", "510590000000001", "510010000000001", "170010000000001"],
                       "h_geocode": ["510590000000001", "516100000000001", "516000000000001", "510010000000001"],
                       "S000": [3, 4, 5, 6]})  # fmt: skip
    path = tmp_path / "od.csv.gz"
    od.to_csv(path, index=False)
    zone_of = {"51059": "51919", "51600": "51919", "51610": "51919", "51001": "51001"}
    f = rs.county_flows([path], ["51001", "51919"], ["17001"], zone_of)
    np.testing.assert_array_equal(f, [[0, 0, 6], [5, 7, 0], [0, 0, 0]])


def test_metro_counties_keep_the_leading_zero(tmp_path):
    p = tmp_path / "cbsa.csv"
    p.write_text("CBSA,MDIV,STCOU,NAME,LSAD\n13820,,,\"Birmingham, AL\",Metropolitan Statistical Area\n"
                 "13820,,1073,\"Jefferson County, AL\",County or equivalent\n"
                 "19780,,19153,\"Polk County, IA\",County or equivalent\n"
                 "19780,,,\"Des Moines, IA\",Metropolitan Statistical Area\n")
    assert bs.read_metro_counties(p) == {"01073", "19153"}
    with pytest.raises(ValueError, match="Metropolitan"):
        bs.county_kinds(["01001"], np.array([1.0]), metro=set())


# --- metro nest build (urqse.data.build_metro) ---------------------------------------------------


def test_tract_rows_split_county_totals_and_keep_farm_jobs_on_farmland():
    from urqse.data import build_metro as bm

    county = pd.Series({"N": 1000.0, "HU": 900.0, "HA": 100.0, "TF": 50.0, "pasture_ha": 10.0, "L": 4e5,
                        "wA_obs_usd": 40_000.0, "nonfarm_earn_usd": 9e7, "pop": 2000.0, "omega": 0.6,
                        "gateway": 1.2, "cash_rent_usd_acre": 200.0, "cash_rent_filled": False,
                        "land_value_usd_acre": 9000.0, "kind": "suburb"})  # fmt: skip
    tr = pd.DataFrame({"rac": [3.0, 1.0, 0.0], "wac": [5.0, 3.0, 2.0], "wac_farm": [0.0, 2.0, 1.0],
                       "TF": [0.0, 30.0, 10.0], "pasture_ha": [1.0, 1.0, 0.0], "L": [5.0, 3.0, 2.0],
                       "cenpop": [10.0, 5.0, 5.0]}, index=["a", "b", "c"])  # fmt: skip
    out = bm.tract_rows(county, tr)
    for c in ("N", "HU", "HA", "TF", "L", "nonfarm_earn_usd", "pop"):
        assert out[c].sum() == pytest.approx(county[c])
    assert out["HA"].tolist() == pytest.approx([0.0, 200 / 3, 100 / 3])  # tract a has no cropland
    assert out["wA_obs_usd"].tolist() == [0.0, 40_000.0, 40_000.0]
    np.testing.assert_allclose(out["N"], [750.0, 250.0, 0.0])


def test_metro_counties_of_the_core(tmp_path):
    from urqse.data import build_metro as bm

    p = tmp_path / "cbsa.csv"
    p.write_text("CBSA,MDIV,STCOU,NAME,LSAD\n19780,,,\"Des Moines, IA\",Metropolitan Statistical Area\n"
                 "19780,,19153,\"Polk County, IA\",County or equivalent\n19780,,19049,\"Dallas County, IA\",County or equivalent\n"
                 "36540,,31055,\"Douglas County, NE\",County or equivalent\n36540,,19155,\"Pottawattamie, IA\",County or equivalent\n")
    assert bm.metro_counties(p, "19153", "19") == ["19049", "19153"]
    assert bm.metro_counties(p, "31055", "31") == ["31055"]  # the Iowa part of Omaha's metro is left out


def test_built_iowa_metro_adds_up_to_counties():
    from urqse.data.loaders import COUNTY_FILE, METRO_FILE, read_county, read_metro, state_dir

    d = state_dir("IA", 2022)
    if not (d / METRO_FILE).exists():
        pytest.skip("Iowa metro data not built")
    m, c = read_metro(d / METRO_FILE), read_county(d / COUNTY_FILE).set_index("fips")
    tr = m[m["nest"] == 0]
    assert len(tr) == 162 and set(tr["parent"]) == {"19049", "19077", "19099", "19121", "19153", "19181"}
    sums = tr.groupby("parent")[["N", "HU", "HA", "L", "TF"]].sum()
    np.testing.assert_allclose(sums, c.loc[sums.index, ["N", "HU", "HA", "L", "TF"]], rtol=1e-10)
    assert m["N"].sum() == pytest.approx(c["N"].sum(), rel=1e-12)


# --- overnight fixes: Connecticut neighbours, irrigated rent, LODES year, one-cluster SE ------------


def test_county_centres_fill_counties_missing_from_the_2020_file(tmp_path):
    shp = gpd.GeoDataFrame({"GEOID": ["25001", "09110"]}, geometry=[box(-71, 42, -70, 43), box(-73, 41, -72, 42)],
                           crs=4326).set_index("GEOID")  # fmt: skip
    cen = pd.DataFrame({"lat": [42.5], "lon": [-70.5], "cenpop": [1000.0]}, index=["25001"])
    pep = tmp_path / "pep.csv"
    pep.write_text("SUMLEV,STATE,COUNTY,POPESTIMATE2022\n050,25,001,1100\n050,09,110,900000\n")
    out = bs.county_centres(cen, shp, pep, 2022)
    assert out.loc["25001"].tolist() == [42.5, -70.5, 1000.0]  # the 2020 centre is kept
    assert out.loc["09110", "cenpop"] == 900000.0
    assert 41 < out.loc["09110", "lat"] < 42 and -73 < out.loc["09110", "lon"] < -72


def test_cash_rent_falls_back_to_irrigated_only_when_the_state_has_no_dryland_rent():
    cols = ["SOURCE_DESC", "SHORT_DESC", "DOMAIN_DESC", "AGG_LEVEL_DESC", "STATE_ALPHA", "ASD_CODE", "COUNTY_ANSI",
            "COUNTY_NAME", "YEAR", "REFERENCE_PERIOD_DESC", "VALUE"]  # fmt: skip
    dry = "RENT, CASH, CROPLAND, NON-IRRIGATED - EXPENSE, MEASURED IN $ / ACRE"
    wet = "RENT, CASH, CROPLAND, IRRIGATED - EXPENSE, MEASURED IN $ / ACRE"
    irrigated = [("SURVEY", wet, "TOTAL", "COUNTY", "AZ", "10", "013", "MARICOPA", "2022", "YEAR", "250"),
                 ("SURVEY", wet, "TOTAL", "STATE", "AZ", "", "", "", "2022", "YEAR", "230")]  # fmt: skip
    rent, series = bs.cash_rent(pd.DataFrame(irrigated, columns=cols), 2022, "04")
    assert series == "irrigated" and rent["state"] == 230.0 and rent["county"]["04013"] == 250.0
    both = irrigated + [("SURVEY", dry, "TOTAL", "STATE", "AZ", "", "", "", "2022", "YEAR", "60")]
    rent, series = bs.cash_rent(pd.DataFrame(both, columns=cols), 2022, "04")
    assert series == "non-irrigated" and rent["state"] == 60.0


def test_lodes_falls_back_to_the_latest_earlier_year(tmp_path, monkeypatch):
    released = {"in_od_main_JT00_2022", "in_od_aux_JT00_2022", "mi_od_aux_JT00_2021"}
    monkeypatch.setattr(bs, "url_exists", lambda url: url.rsplit("/", 1)[1].removesuffix(".csv.gz") in released)
    monkeypatch.setattr(bs, "curl", lambda url, dest: dest)
    paths = rs.lodes_paths("IN", 2022, ["26001"], shared=tmp_path)
    assert [p.name for p in paths] == ["in_od_main_JT00_2022.csv.gz", "in_od_aux_JT00_2022.csv.gz", "mi_od_aux_JT00_2021.csv.gz"]
    assert rs.lodes_years(paths)["mi_od_aux_JT00_2021.csv.gz"] == 2021
    released.discard("mi_od_aux_JT00_2021")
    with pytest.raises(FileNotFoundError, match="mi aux"):
        rs.lodes_paths("IN", 2022, ["26001"], shared=tmp_path)


def test_unroutable_pairs_get_straight_line_time_at_the_routed_speed():
    d = np.array([[1.0, 60.0, 120.0], [60.0, 1.0, 30.0], [120.0, 30.0, 1.0]])
    t = np.array([[2.0, 60.0, np.nan], [60.0, 2.0, 30.0], [np.nan, 30.0, 2.0]])  # 1 km/min where routed
    filled, miss = bs.fill_unroutable(t, d)
    assert miss.sum() == 2 and filled[0, 2] == pytest.approx(120.0) and filled[2, 0] == pytest.approx(120.0)
    np.testing.assert_array_equal(filled[~miss], t[~miss])


def test_cash_rent_stays_non_irrigated_when_neither_series_exists():
    cols = ["SOURCE_DESC", "SHORT_DESC", "DOMAIN_DESC", "AGG_LEVEL_DESC", "STATE_ALPHA", "ASD_CODE", "COUNTY_ANSI",
            "COUNTY_NAME", "YEAR", "REFERENCE_PERIOD_DESC", "VALUE"]  # fmt: skip
    rent, series = bs.cash_rent(pd.DataFrame([], columns=cols), 2022, "44")
    assert series == "non-irrigated" and np.isnan(rent["state"]) and rent["county"].empty
