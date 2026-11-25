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
    assert {"AK", "HI", "CT", "DC", "NY"} <= set(bs.UNSUPPORTED)


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
