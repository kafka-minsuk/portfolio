"""Offline build of a state's metro nest (spec §3.12, proposal M7):  python -m urqse.data.build_metro IA 2022

Splits the counties of the core's Metropolitan Statistical Area (its in-state part) into census
tracts. Needs the state's county build (data/{state}/{year}/county.parquet, urqse.data.build_state).
Writes data/{state}/{year}/metro.parquet, metro_travel.npz and METRO_REPORT.md.

Tract values are the county's values split by tract shares, so tracts sum exactly to their county:
- residents N by LODES RAC (all jobs, by home block); non-farm jobs HU by LODES WAC all jobs minus
  NAICS 11 (CNS01); farm jobs HA by WAC CNS01 among tracts with CDL cropland (by cropland where the
  county has no NAICS 11 wage jobs).
- floor space L (GHSL) and farmland TF (CDL) by tract zonal sums, scaled to the county's totals.
- farm wage, owner share, gateway weight and cash rent: the county's value.
Travel times: OSRM between tract and county population centres, as in build_state."""

import argparse
import datetime as dt
import gzip
from pathlib import Path

import numpy as np
import pandas as pd

from . import build_state as bs
from .loaders import COUNTY_FILE, METRO_FILE, METRO_TRAVEL_FILE, TRAVEL_FILE, read_county, read_travel, state_dir
from .schema import EXTERNAL_FIPS, METRO_COLUMNS, METRO_SCHEMA, validate_travel

ROOT = bs.ROOT
TRACTS_URL = "https://www2.census.gov/geo/tiger/GENZ{year}/shp/cb_{year}_{sf}_tract_500k.zip"
TRACT_CENPOP_URL = "https://www2.census.gov/geo/docs/reference/cenpop2020/tract/CenPop2020_Mean_TR{sf}.txt"
LODES_AREA_URL = "https://lehd.ces.census.gov/data/lodes/LODES8/{st}/{kind}/{st}_{kind}_S000_JT00_{year}.csv.gz"
MAX_TRACTS = 400  # v1 size cap for the browser's dense solver (proposal M7 decision 4)


def metro_counties(cbsa_path: Path, core_fips: str, state_fips: str) -> list:
    """In-state counties of the Metropolitan Statistical Area that holds the core county."""
    df = pd.read_csv(cbsa_path, encoding="latin-1", dtype=str)
    df = df[df["LSAD"] == "County or equivalent"].assign(STCOU=lambda d: d["STCOU"].str.zfill(5))
    cbsa = df.loc[df["STCOU"] == core_fips, "CBSA"]
    if cbsa.empty:
        raise ValueError(f"core county {core_fips} is in no CBSA")
    members = df.loc[df["CBSA"] == cbsa.iloc[0], "STCOU"]
    return sorted(f for f in members if f.startswith(state_fips))


def lodes_by_tract(path: Path, geocode: str) -> pd.DataFrame:
    """LODES RAC or WAC (S000, JT00) summed from blocks to tracts: total jobs C000, NAICS 11 CNS01."""
    with gzip.open(path, "rt") as f:
        df = pd.read_csv(f, usecols=[geocode, "C000", "CNS01"], dtype={geocode: str})
    return df.groupby(df[geocode].str[:11])[["C000", "CNS01"]].sum()


def split(total: float, weight: np.ndarray) -> np.ndarray:
    """Split a county total over its tracts in proportion to weight (equal shares if all zero)."""
    w = np.asarray(weight, float)
    w = w if w.sum() > 0 else np.ones_like(w)
    return total * w / w.sum()


def tract_rows(county: pd.Series, tr: pd.DataFrame) -> pd.DataFrame:
    """Tract model columns from the county row and tract weights (columns rac, wac, wac_farm, TF, L, ...)."""
    out = pd.DataFrame(index=tr.index)
    out["N"] = split(county["N"], tr["rac"])
    out["HU"] = split(county["HU"], tr["wac"] - tr["wac_farm"])
    has_land = tr["TF"].to_numpy() > 0
    farm_w = np.where(has_land, tr["wac_farm"], 0.0)
    if county["HA"] > 0 and farm_w.sum() == 0:
        farm_w = np.where(has_land, tr["TF"], 0.0)  # proprietor-only farming: by cropland
    out["HA"] = split(county["HA"], farm_w) if county["HA"] > 0 else 0.0
    out["TF"] = split(county["TF"], tr["TF"])
    out["pasture_ha"] = split(county["pasture_ha"], tr["pasture_ha"])
    out["L"] = split(county["L"], tr["L"])
    out["built_volume_m3"] = out["L"] * bs.STOREY_HEIGHT_M
    out["wA_obs_usd"] = np.where(out["HA"] > 0, county["wA_obs_usd"], 0.0)
    out["farm_labour_bill_usd"] = out["wA_obs_usd"] * out["HA"]
    out["nonfarm_earn_usd"] = split(county["nonfarm_earn_usd"], out["HU"])
    out["pop"] = split(county["pop"], tr["cenpop"])
    for c in ("omega", "gateway", "cash_rent_usd_acre", "cash_rent_filled", "land_value_usd_acre", "kind"):
        out[c] = county[c]
    return out


def build_metro(state: str, year: int, raw: Path, out: Path, shared: Path = bs.SHARED_RAW) -> dict:
    sf = bs.STATE_FIPS[state]
    ddir = state_dir(state, year)
    df = read_county(ddir / COUNTY_FILE).set_index("fips")
    fips_c, t_c, d_c = read_travel(ddir / TRAVEL_FILE)
    core = df.index[df["kind"] == "core"][0]
    src = bs.sources(state, year)
    members = [f for f in metro_counties(shared / src["cbsa"].file, core, sf) if f in df.index]

    tracts = bs.read_counties(bs.curl(TRACTS_URL.format(year=2022, sf=sf), raw / "tract" / f"cb_2022_{sf}_tract_500k.zip"))
    tracts = tracts[(tracts["STATEFP"] + tracts["COUNTYFP"]).isin(members)]
    if len(tracts) > MAX_TRACTS:
        raise ValueError(f"{state}: {len(tracts)} tracts in the core's metro, above the v1 cap of {MAX_TRACTS}")
    cen = pd.read_csv(bs.curl(TRACT_CENPOP_URL.format(sf=sf), raw / "tract" / f"CenPop2020_Mean_TR{sf}.txt"),
                      encoding="utf-8-sig", dtype=str)  # fmt: skip
    cen.index = cen["STATEFP"] + cen["COUNTYFP"] + cen["TRACTCE"]
    lodes = {k: lodes_by_tract(bs.curl(LODES_AREA_URL.format(st=state.lower(), kind=k, year=year),
                                       shared / "lodes" / f"{state.lower()}_{k}_S000_JT00_{year}.csv.gz"), g)
             for k, g in (("rac", "h_geocode"), ("wac", "w_geocode"))}  # fmt: skip

    # tract weights: LODES, CDL cropland, GHSL floor space, 2020 population
    tiles = bs.ghsl_tiles(list(tracts.to_crs("ESRI:54009").geometry))
    files = {k: bs.fetch(v, raw, shared) for k, v in bs.sources(state, year, tiles).items() if k == "cdl" or k.startswith("ghsl_")}
    areas = bs.zonal_class_area(files["cdl"], list(tracts.to_crs(5070).geometry))
    w = pd.DataFrame(index=tracts.index)
    w["county"] = tracts["STATEFP"] + tracts["COUNTYFP"]
    w["rac"] = lodes["rac"]["C000"].reindex(w.index).fillna(0.0)
    w["wac"] = lodes["wac"]["C000"].reindex(w.index).fillna(0.0)
    w["wac_farm"] = lodes["wac"]["CNS01"].reindex(w.index).fillna(0.0)
    w["TF"] = areas[:, bs.CDL_CROP].sum(axis=1) / 1e4
    w["pasture_ha"] = areas[:, bs.CDL_PASTURE].sum(axis=1) / 1e4
    ghsl = [f"zip+file://{files[k]}!{files[k].stem}.tif" for k in files if k.startswith("ghsl_")]
    w["L"] = bs.zonal_sum(ghsl, list(tracts.to_crs("ESRI:54009").geometry)) / bs.STOREY_HEIGHT_M
    w["cenpop"] = pd.to_numeric(cen["POPULATION"].reindex(w.index), errors="coerce").fillna(0.0)

    rows = []
    for c in members:
        t = tract_rows(df.loc[c], w[w["county"] == c])
        t["parent"] = c
        t["name"] = [f"Tract {n}, {df.loc[c, 'name']}" for n in tracts.loc[t.index, "NAME"]]
        t["area_km2"] = tracts.loc[t.index, "ALAND"].astype(float) / 1e6
        t["lat"] = pd.to_numeric(cen["LATITUDE"].reindex(t.index))
        t["lon"] = pd.to_numeric(cen["LONGITUDE"].reindex(t.index))
        rows.append(t)
    tr = pd.concat(rows)
    no_centre = tr.index[tr["lat"].isna()]
    if len(no_centre):  # a tract with no 2020 population centre: its polygon's representative point
        pts = tracts.loc[no_centre].geometry.representative_point()
        tr.loc[no_centre, "lat"], tr.loc[no_centre, "lon"] = pts.y.to_numpy(), pts.x.to_numpy()

    outside = [f for f in df.index if f not in members and f != EXTERNAL_FIPS]
    zones = pd.concat([df.loc[outside].assign(parent=outside), tr, df.loc[[EXTERNAL_FIPS]].assign(parent=EXTERNAL_FIPS)])
    zones["nest"] = np.where(zones.index.str.len() == 11, 0, -1)
    zones.index.name = "fips"

    # travel times: OSRM between tract / county centres, plus the external zone's border counties
    shp = bs.read_counties(shared / src["counties"].file)
    st_zones, _ = bs.state_zones(shp, shared / src["bea_emp"].file, state)
    nb = bs.neighbor_counties(shp, sf, st_zones.to_crs(5070).union_all())
    cen_c = bs.county_centres(bs.read_cenpop(shared / src["cenpop"].file), shp, shared / src["pep"].file, year)
    Zin = len(zones) - 1
    pts = pd.concat([zones.iloc[:Zin][["lat", "lon"]], cen_c.loc[nb, ["lat", "lon"]]])
    t_pts, _, n_calls = bs.osrm_table(pts[["lon", "lat"]].to_numpy(), raw / "osrm")
    if np.isnan(t_pts).any():
        raise RuntimeError("OSRM returned unroutable pairs")
    lat, lon = pts["lat"].to_numpy(), pts["lon"].to_numpy()
    d_line = bs.haversine_km(lat[:, None], lon[:, None], lat[None, :], lon[None, :])
    own_t, own_d, speed = bs.own_trip(zones.iloc[:Zin]["area_km2"].to_numpy(float), t_pts, d_line, Zin)
    is_cty = zones.iloc[:Zin]["nest"].to_numpy() < 0  # counties keep the county build's own trip
    own_t = np.where(is_cty, zones.iloc[:Zin]["own_time_min"].to_numpy(float), own_t)
    own_d = np.where(is_cty, zones.iloc[:Zin]["own_dist_km"].to_numpy(float), own_d)
    zones.loc[zones.index[:Zin], "own_time_min"], zones.loc[zones.index[:Zin], "own_dist_km"] = own_t, own_d
    t, dist = bs.travel_with_external(t_pts, d_line, Zin, own_t, own_d)
    zones.loc[EXTERNAL_FIPS, ["own_time_min", "own_dist_km"]] = t[Zin, Zin], dist[Zin, Zin]

    from pyproj import Transformer

    x, y = Transformer.from_crs(4326, bs.state_crs(st_zones), always_xy=True).transform(zones["lon"].to_numpy(), zones["lat"].to_numpy())
    zones["x_km"], zones["y_km"] = x / 1e3, y / 1e3
    zones["cash_rent_filled"] = zones["cash_rent_filled"].astype(bool)
    table = METRO_SCHEMA.validate(zones.reset_index()[METRO_COLUMNS].astype({"fips": str, "name": str, "kind": str, "parent": str, "nest": int}))
    validate_travel(table["fips"].to_numpy(), t, dist)

    # tracts add up to their county
    sums = table[table["nest"] == 0].groupby("parent")[["N", "HU", "HA", "L", "TF"]].sum()
    gap = float((sums / df.loc[sums.index, ["N", "HU", "HA", "L", "TF"]].replace(0, np.nan) - 1).abs().max().max())
    if gap > 1e-9:
        raise AssertionError(f"tract sums differ from their county by {gap:.2e}")
    out.mkdir(parents=True, exist_ok=True)
    table.to_parquet(out / METRO_FILE, index=False)
    np.savez_compressed(out / METRO_TRAVEL_FILE, fips=table["fips"].to_numpy(str), t=t, dist=dist)
    meta = dict(state=state, year=year, members=members, core=core, n_tracts=int((table["nest"] == 0).sum()),
                osrm_calls=n_calls, speed=speed, gap=gap, built=dt.date.today().isoformat(),
                no_centre=list(no_centre), farm_tracts=int(((table["nest"] == 0) & (table["HA"] > 0)).sum()))  # fmt: skip
    (out / "METRO_REPORT.md").write_text(report(table, df, meta))
    return dict(table=table, t=t, dist=dist, meta=meta)


def report(table: pd.DataFrame, df: pd.DataFrame, m: dict) -> str:
    tr = table[table["nest"] == 0]
    names = ", ".join(df.loc[c, "name"] for c in m["members"])
    L = [f"# {bs.STATE_NAME[m['state']]} {m['year']} metro nest: data report", "",
         f"Built {m['built']} by `python -m urqse.data.build_metro {m['state']} {m['year']}` from the county build. "
         f"The core county {df.loc[m['core'], 'name']} ({m['core']}) is in a Metropolitan Statistical Area whose in-state "
         f"counties are {names}. They are split into {m['n_tracts']} census tracts (2022 cartographic boundary file); "
         f"the other {int((table['nest'] < 0).sum()) - 1} counties and the external zone are as in the county build.", "",
         "## How tracts get their values", "",
         "Each county total from the county build is split across its tracts, so tracts add up to their county "
         f"(largest relative gap {m['gap']:.1e}).", "",
         "| Column | Tract share |", "|---|---|",
         "| N (resident workers) | LODES8 RAC JT00 all jobs by home block, 2022 |",
         "| HU (non-farm jobs) | LODES8 WAC all jobs minus NAICS 11 (CNS01), 2022 |",
         "| HA (farm jobs) | LODES8 WAC NAICS 11 among tracts with CDL cropland; by cropland where a county has no NAICS 11 wage jobs |",
         "| TF, pasture | CDL 2022 zonal sums by tract |",
         "| L (floor space) | GHSL GHS-BUILT-V 2020 zonal sums by tract |",
         "| pop | 2020 Census tract population |",
         "| farm wage, owner share, gateway, cash rent | the county's value |", "",
         f"{m['farm_tracts']} of {m['n_tracts']} tracts have farm jobs; the rest have no farm sector (spec §3.11). "
         "`# VERIFY` LODES counts wage-and-salary jobs only, so farm proprietors are spread like hired farm jobs.", "",
         f"Travel: OSRM car times between 2020 tract and county population centres ({m['osrm_calls']} cached block "
         f"requests); a tract's own trip is the square-area proxy at {m['speed'] * 60:.1f} straight-line km/h. "
         + (f"Tracts without a population centre use their polygon's representative point: {', '.join(m['no_centre'])}." if m["no_centre"] else ""),
         "", "## Tracts", "", "| Tract | County | N | HU | HA | L m^2 | TF ha |", "|---|---|---|---|---|---|---|"]  # fmt: skip
    for r in tr.itertuples():
        L.append(f"| {r.fips} | {df.loc[r.parent, 'name']} | {r.N:,.0f} | {r.HU:,.0f} | {r.HA:,.1f} | {r.L / 1e6:,.2f}M | {r.TF:,.0f} |")
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("state")
    ap.add_argument("year", type=int)
    a = ap.parse_args(argv)
    state = a.state.upper()
    res = build_metro(state, a.year, ROOT / "data_raw" / state, state_dir(state, a.year))
    m = res["meta"]
    (ROOT / "reports" / f"{state}_{a.year}_METRO_REPORT.md").write_text((state_dir(state, a.year) / "METRO_REPORT.md").read_text())
    print(f"wrote {m['n_tracts']} tracts in {len(m['members'])} counties; {len(res['table'])} zones")


if __name__ == "__main__":
    main()
