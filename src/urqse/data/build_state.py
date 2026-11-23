"""Offline build of one state's county table (spec §8):  python -m urqse.data.build_state IA 2022

Downloads go to data_raw/{state}/ and are reused when present, so a rerun is offline.
Outputs go to data/{state}/{year}/: county.parquet, travel.npz and REPORT.md.
Only Iowa 2022 has been built and checked; other states need their own source vintages."""

import argparse
import datetime as dt
import gzip
import hashlib
import json
import re
import subprocess
import sys
import time
import zipfile
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from .loaders import COUNTY_FILE, TRAVEL_FILE, state_dir
from .schema import COLUMNS, COUNTY_SCHEMA, EXTERNAL_FIPS, validate_travel

ROOT = Path(__file__).resolve().parents[3]
STATE_FIPS = {"IA": "19"}
STATE_NAME = {"IA": "Iowa"}

ACRE_HA = 0.40468564224  # exact (international acre)
STOREY_HEIGHT_M = 3.0  # floor space = building volume / storey height. source=GHSL GHS-BUILT-V is volume only  # VERIFY
# Mean distance between two uniform points in a unit square (Ghosh 1951): used for the own-county trip.
SQUARE_MEAN_DIST = 0.521405433
# CDL legend (NASS CDL metadata, 2022): crop, hay and fallow classes vs. grassland/pasture.
CDL_CROP = np.r_[1:62, 66:78, 204:255]  # 1-61 crops/hay/fallow, 66-77 tree crops, 204-254 double crops
CDL_PASTURE = np.array([62, 176])  # 62 pasture/grass (legacy), 176 grassland/pasture
NEIGHBOR_BUFFER_M = 1_000.0  # out-of-state counties within 1 km of the state count as adjacent
OSRM = "https://router.project-osrm.org/table/v1/driving"
OSRM_MAX_COORDS = 100  # public demo server limit (HTTP 400 "TooBig" above 100, tested 2026-11-23)
NASS_INDEX = "https://www.nass.usda.gov/datasets"
NASS_BASE = "https://www.nass.usda.gov/sites/default/files/datasets/"


# GHSL 1000 km tiles covering the state (row = 9000 km north edge down, col = 18041 km west edge east).
GHSL_TILES = {"IA": ("R4_C10", "R4_C11", "R5_C10", "R5_C11")}


@dataclass(frozen=True)
class Source:
    name: str
    url: str
    file: str  # path under data_raw/{state}/
    vintage: str


def sources(state: str, year: int) -> dict:
    s = STATE_FIPS[state]
    acs = f"https://www2.census.gov/programs-surveys/acs/summary_file/{year}/table-based-SF/data/5YRData/"
    ghsl = (
        "https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/"
        "GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/"
    )
    out = [
        Source("pep", "https://www2.census.gov/programs-surveys/popest/datasets/2020-2022/counties/totals/co-est2022-alldata.csv",
               "co-est2022-alldata.csv", "Census PEP Vintage 2022, July 1 2022 estimates"),
        Source("cbsa", "https://www2.census.gov/programs-surveys/popest/datasets/2020-2023/metro/totals/cbsa-est2023-alldata.csv",
               "cbsa-est2023-alldata.csv", "Census PEP Vintage 2023 CBSA file (OMB July 2023 delineations)"),
        Source("cenpop", "https://www2.census.gov/geo/docs/reference/cenpop2020/county/CenPop2020_Mean_CO.txt",
               "CenPop2020_Mean_CO.txt", "2020 Census centers of population, county"),
        Source("counties", "https://www2.census.gov/geo/tiger/GENZ2022/shp/cb_2022_us_county_500k.zip",
               "cb_2022_us_county_500k.zip", "Census cartographic boundary file 2022, 1:500k"),
        Source("bea_emp", "https://apps.bea.gov/regional/zip/CAEMP25N.zip", "bea_CAEMP25N.zip",
               "BEA CAEMP25N (formerly CAINC25N), released 2023-11-16"),
        Source("bea_farm", "https://apps.bea.gov/regional/zip/CAINC45.zip", "bea_CAINC45.zip",
               "BEA CAINC45, released 2023-11-16"),
        Source("bea_earn", "https://apps.bea.gov/regional/zip/CAINC5N.zip", "bea_CAINC5N.zip",
               "BEA CAINC5N, file dated 2026-01-14"),
        Source("cdl", f"https://nassgeodata.gmu.edu/axis2/services/CDLService/GetCDLFile?year={year}&fips={s}",
               f"CDL_{year}_{s}.tif", f"USDA NASS Cropland Data Layer {year}, 30 m, clipped to state FIPS {s}"),
    ]
    for t in ("b08007", "b08604", "b05005"):
        out.append(Source(f"acs_{t}", f"{acs}acsdt5y{year}-{t}.dat", f"acs/acsdt5y{year}-{t}.dat",
                          f"ACS {year - 4}-{year} 5-year, table-based summary file {t.upper()}"))
    for rc in GHSL_TILES[state]:
        f = f"GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_{rc}.zip"
        out.append(Source(f"ghsl_{rc}", ghsl + f, f"ghsl/{f}", "GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide"))
    return {x.name: x for x in out}  # fmt: skip


# --- downloads -----------------------------------------------------------------------------


def curl(url: str, dest: Path) -> Path:
    """Fetch once; an existing file is reused. curl, not urllib, for the macOS certificate store."""
    if dest.exists() and dest.stat().st_size > 0:
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_name(dest.name + ".part")
    subprocess.run(["curl", "-sSfL", "--retry", "3", "-o", str(tmp), url], check=True)
    tmp.replace(dest)
    return dest


def fetch(src: Source, raw: Path) -> Path:
    if src.name == "cdl":  # the CropScape service returns XML naming the GeoTIFF to download
        dest = raw / src.file
        if not dest.exists():
            xml = curl(src.url, raw / (src.file + ".xml")).read_text()
            curl(re.search(r"<returnURL>(.*?)</returnURL>", xml).group(1), dest)
        return dest
    return curl(src.url, raw / src.file)


def fetch_nass_economics(raw: Path, state: str) -> tuple[Path, str]:
    """Quick Stats bulk economics file, filtered to the state and cached (the full file is ~0.6 GB)."""
    cached = sorted(raw.glob(f"qs.economics_*_{state}.tsv.gz"))
    if cached:
        return cached[-1], cached[-1].name.replace(f"_{state}.tsv.gz", ".txt.gz")
    full = sorted(raw.glob("qs.economics_????????.txt.gz"))
    if not full:
        index = curl(NASS_INDEX, raw / "nass_datasets_index.html").read_text(errors="replace")
        name = sorted(set(re.findall(r"qs\.economics_\d{8}\.txt\.gz", index)))[-1]
        full = [curl(NASS_BASE + name, raw / name)]
    src = full[-1]
    out = raw / src.name.replace(".txt.gz", f"_{state}.tsv.gz")
    tmp = out.with_name(out.name + ".part")
    tag = f"\t{state}\t"
    with gzip.open(src, "rt", encoding="utf-8", errors="replace") as f, gzip.open(tmp, "wt") as o:
        o.write(f.readline())
        for line in f:
            if tag in line:
                o.write(line)
    tmp.replace(out)
    return out, src.name


# --- parsers (pure: file in, table out) ----------------------------------------------------


def to_number(s: pd.Series) -> pd.Series:
    """Published cells to float; suppression codes such as (D), (NA), (Z) become NaN."""
    return pd.to_numeric(s.astype(str).str.strip().str.replace(",", "", regex=False), errors="coerce")


def read_bea(zip_path: Path, state: str, year: int, lines: dict) -> pd.DataFrame:
    """BEA regional CSV: one column per requested LineCode, rows = 5-digit GeoFIPS (state row kept)."""
    with zipfile.ZipFile(zip_path) as z:
        member = next(n for n in z.namelist() if re.search(rf"_{state}_\d{{4}}_\d{{4}}\.csv$", n))
        df = pd.read_csv(z.open(member), encoding="latin-1", dtype=str)
    df["GeoFIPS"] = df["GeoFIPS"].str.strip(' "')
    df = df[df["GeoFIPS"].str.fullmatch(r"\d{5}", na=False)]
    df["LineCode"] = df["LineCode"].str.strip()
    out = {name: to_number(df[df["LineCode"] == str(code)].set_index("GeoFIPS")[str(year)])
           for name, code in lines.items()}  # fmt: skip
    return pd.DataFrame(out)


def read_acs(path: Path, columns: dict, state_fips: str) -> pd.DataFrame:
    """ACS table-based summary file (pipe-delimited, all geographies); rows = 5-digit FIPS for
    counties and 2-digit FIPS for the state row."""
    df = pd.read_csv(path, sep="|", dtype=str, usecols=["GEO_ID", *columns])
    county = df["GEO_ID"].str.fullmatch(rf"0500000US{state_fips}\d{{3}}")
    st = df["GEO_ID"] == f"0400000US{state_fips}"
    df = df[county | st]
    df.index = df["GEO_ID"].str.slice(9)
    return pd.DataFrame({name: to_number(df[c]) for c, name in columns.items()})


def read_pep(path: Path, state_fips: str, year: int) -> pd.Series:
    df = pd.read_csv(path, encoding="latin-1", dtype=str)
    df = df[df["STATE"] == state_fips]
    fips = np.where(df["SUMLEV"] == "040", state_fips, df["STATE"] + df["COUNTY"])
    return pd.Series(to_number(df[f"POPESTIMATE{year}"]).to_numpy(), index=fips, name="pop")


def read_metro_counties(path: Path) -> set:
    df = pd.read_csv(path, encoding="latin-1", dtype=str)
    metro = set(df.loc[df["LSAD"] == "Metropolitan Statistical Area", "CBSA"])
    rows = df[(df["LSAD"] == "County or equivalent") & df["CBSA"].isin(metro)]
    return set(rows["STCOU"])


def read_cenpop(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, encoding="utf-8-sig", dtype={"STATEFP": str, "COUNTYFP": str})
    df.index = df["STATEFP"] + df["COUNTYFP"]
    return df.rename(columns={"LATITUDE": "lat", "LONGITUDE": "lon", "POPULATION": "cenpop"})[["lat", "lon", "cenpop"]]


def read_counties(path: Path):
    import geopandas as gpd

    return gpd.read_file(f"zip://{path}").set_index("GEOID").sort_index()


def _one_period(x: pd.DataFrame) -> pd.DataFrame:
    """Census rows are 'END OF DEC' at some levels and 'YEAR' at others; keep one period per level,
    preferring the annual one."""
    periods = set(x["REFERENCE_PERIOD_DESC"])
    return x[x["REFERENCE_PERIOD_DESC"] == "YEAR"] if len(periods) > 1 and "YEAR" in periods else x


def nass_series(df: pd.DataFrame, short_desc: str, year: int, source: str, state_fips: str) -> dict:
    """County values plus the published state and 'other (combined) counties' values."""
    x = df[(df["SHORT_DESC"] == short_desc) & (df["YEAR"] == str(year)) & (df["SOURCE_DESC"] == source)
           & (df["DOMAIN_DESC"] == "TOTAL")]  # fmt: skip
    cty = _one_period(x[(x["AGG_LEVEL_DESC"] == "COUNTY") & x["COUNTY_ANSI"].fillna("").str.fullmatch(r"\d{3}")])
    other = _one_period(x[(x["AGG_LEVEL_DESC"] == "COUNTY") & (x["COUNTY_NAME"].str.contains("OTHER", na=False))])
    st = _one_period(x[x["AGG_LEVEL_DESC"] == "STATE"])
    values = pd.Series(to_number(cty["VALUE"]).to_numpy(), index=state_fips + cty["COUNTY_ANSI"])
    return {
        "county": values[~values.index.duplicated()],
        "suppressed": sorted(state_fips + cty.loc[to_number(cty["VALUE"]).isna().to_numpy(), "COUNTY_ANSI"]),
        "other": float(to_number(other["VALUE"]).iloc[0]) if len(other) else np.nan,
        "state": float(to_number(st["VALUE"]).iloc[0]) if len(st) else np.nan,
    }


def read_nass(path: Path) -> pd.DataFrame:
    cols = ["SOURCE_DESC", "SHORT_DESC", "DOMAIN_DESC", "AGG_LEVEL_DESC", "STATE_ALPHA", "COUNTY_ANSI",
            "COUNTY_NAME", "YEAR", "REFERENCE_PERIOD_DESC", "VALUE"]  # fmt: skip
    return pd.read_csv(path, sep="\t", dtype=str, usecols=cols)


# --- pure transforms -----------------------------------------------------------------------


def fill_suppressed(values: np.ndarray, total: float, weight: np.ndarray):
    """Give suppressed (NaN) cells the published total minus the disclosed sum, split by weight."""
    values = np.asarray(values, float)
    miss = np.isnan(values)
    if not miss.any():
        return values, miss
    residual = total - values[~miss].sum()
    if not np.isfinite(residual) or residual < 0 or weight[miss].sum() <= 0:
        raise ValueError(f"cannot allocate residual {residual} over {miss.sum()} suppressed cells")
    out = values.copy()
    out[miss] = residual * weight[miss] / weight[miss].sum()
    return out, miss


def reconcile_jobs(workers_res, workers_out, workers_work, HU_bea, HA_bea) -> dict:
    """Jobs = resident workers (spec §5) with one external zone appended as the last entry.

    BEA counts jobs (multiple job holders and part-time proprietors counted once per job); ACS
    counts workers by their main job. Each county's BEA farm/non-farm job mix is scaled to its
    ACS worker count by place of work. The external zone holds out-of-state residents who work
    in the state (N) and in-state residents who work out of state (jobs), so that
        sum(N) + N_ext = sum(workers_res) + in-commuters = sum(workers_work) + out-commuters = sum(H).
    Out-of-state jobs are split by the in-state farm share."""
    scale = workers_work / (HU_bea + HA_bea)
    HU, HA = HU_bea * scale, HA_bea * scale
    in_commuters = workers_work.sum() - (workers_res.sum() - workers_out.sum())
    out_commuters = workers_out.sum()
    if in_commuters <= 0 or out_commuters <= 0:
        raise ValueError("external zone needs positive in- and out-commuting")
    farm_share = HA.sum() / workers_work.sum()
    return {
        "N": np.append(workers_res, in_commuters),
        "HU": np.append(HU, out_commuters * (1.0 - farm_share)),
        "HA": np.append(HA, out_commuters * farm_share),
        "scale": scale,
    }


def county_kinds(fips, HU, metro: set) -> np.ndarray:
    """core = the metro county with the most non-farm jobs; suburb = other metro counties;
    rural = non-metro. # VERIFY: a single core is a model simplification for a multi-metro state."""
    is_metro = np.array([f in metro for f in fips])
    kind = np.where(is_metro, "suburb", "rural").astype(object)
    kind[int(np.argmax(np.where(is_metro, HU, -np.inf)))] = "core"
    return kind


def haversine_km(lat1, lon1, lat2, lon2):
    p1, p2 = np.radians(lat1), np.radians(lat2)
    a = np.sin((p2 - p1) / 2) ** 2 + np.cos(p1) * np.cos(p2) * np.sin(np.radians(lon2 - lon1) / 2) ** 2
    return 2 * 6371.0088 * np.arcsin(np.sqrt(a))


def travel_with_external(t_pts, d_pts, n_in: int, own_t, own_d):
    """(n_in + n_out) point matrices -> (n_in + 1) zone matrices. The external zone is the nearest
    out-of-state point from each county (and from it to each county); its own entry is the median
    own-county entry."""
    Z = n_in + 1
    t = np.empty((Z, Z))
    d = np.empty((Z, Z))
    for m, pts in ((t, t_pts), (d, d_pts)):
        m[:n_in, :n_in] = pts[:n_in, :n_in]
        m[:n_in, n_in] = pts[:n_in, n_in:].min(axis=1)
        m[n_in, :n_in] = pts[n_in:, :n_in].min(axis=0)
    t[n_in, n_in], d[n_in, n_in] = np.median(own_t), np.median(own_d)
    idx = np.arange(n_in)
    t[idx, idx], d[idx, idx] = own_t, own_d
    return t, d


def own_trip(area_km2, t_pts, d_straight, n_in: int):
    """Own-county trip: mean distance between two random points in a square of the county's area,
    at the median effective (straight-line km per OSRM minute) speed between in-state counties.
    # VERIFY: geometric proxy, not observed within-county commute times."""
    dist = SQUARE_MEAN_DIST * np.sqrt(area_km2)
    off = ~np.eye(n_in, dtype=bool)
    speed = np.median(d_straight[:n_in, :n_in][off] / t_pts[:n_in, :n_in][off])
    return dist / speed, dist, float(speed)


# --- rasters -------------------------------------------------------------------------------


def _labelled_blocks(path, geoms, rows=1024):
    """Yield (labels, values, valid) row blocks over the geometries' window; label 0 = outside."""
    import rasterio
    from rasterio.features import rasterize
    from rasterio.windows import Window, from_bounds

    with rasterio.open(path) as src:
        b = np.array([g.bounds for g in geoms])
        win = from_bounds(b[:, 0].min(), b[:, 1].min(), b[:, 2].max(), b[:, 3].max(), src.transform)
        c0, r0 = max(0, int(np.floor(win.col_off))), max(0, int(np.floor(win.row_off)))
        c1 = min(src.width, int(np.ceil(win.col_off + win.width)))
        r1 = min(src.height, int(np.ceil(win.row_off + win.height)))
        win = Window(c0, r0, c1 - c0, r1 - r0)
        shapes = [(g, i + 1) for i, g in enumerate(geoms)]
        for r0 in range(int(win.row_off), int(win.row_off + win.height), rows):
            w = Window(win.col_off, r0, win.width, min(rows, int(win.row_off + win.height) - r0))
            vals = src.read(1, window=w)
            lab = rasterize(shapes, out_shape=vals.shape, transform=src.window_transform(w), fill=0, dtype="int32")
            valid = np.ones(vals.shape, bool) if src.nodata is None else vals != src.nodata
            yield lab, vals, valid, abs(src.transform.a * src.transform.e)


def windows_overlap(path, geoms) -> bool:
    import rasterio

    with rasterio.open(path) as src:
        b = np.array([g.bounds for g in geoms])
        r = src.bounds
        return not (b[:, 2].max() <= r.left or b[:, 0].min() >= r.right or b[:, 3].max() <= r.bottom or b[:, 1].min() >= r.top)


def zonal_class_area(path, geoms, nclass=256) -> np.ndarray:
    """(len(geoms), nclass) area in m^2 of each class value inside each geometry (pixel centres)."""
    out = np.zeros((len(geoms) + 1, nclass))
    for lab, vals, valid, px in _labelled_blocks(path, geoms):
        k = lab[valid].astype(np.int64) * nclass + vals[valid]
        out += np.bincount(k, minlength=out.size).reshape(out.shape) * px
    return out[1:]


def zonal_sum(paths, geoms) -> np.ndarray:
    """Sum of valid pixel values inside each geometry, over non-overlapping tiles."""
    out = np.zeros(len(geoms) + 1)
    for path in paths:
        if not windows_overlap(path, geoms):
            continue
        for lab, vals, valid, _ in _labelled_blocks(path, geoms):
            out += np.bincount(lab[valid], weights=vals[valid].astype(float), minlength=out.size)
    return out[1:]


# --- travel times --------------------------------------------------------------------------


def osrm_table(lonlat: np.ndarray, cache: Path):
    """Durations (min) and road distances (km) between all points, in blocks the server accepts.
    Each block is one cached request."""
    n = len(lonlat)
    size = OSRM_MAX_COORDS // 2
    blocks = [np.arange(i, min(i + size, n)) for i in range(0, n, size)]
    t = np.full((n, n), np.nan)
    d = np.full((n, n), np.nan)
    for a in blocks:
        for b in blocks:
            idx = np.unique(np.concatenate([a, b]))
            coords = ";".join(f"{lonlat[i, 0]:.6f},{lonlat[i, 1]:.6f}" for i in idx)
            src = ";".join(str(int(np.searchsorted(idx, i))) for i in a)
            dst = ";".join(str(int(np.searchsorted(idx, i))) for i in b)
            url = f"{OSRM}/{coords}?sources={src}&destinations={dst}&annotations=duration,distance"
            path = cache / f"osrm_{hashlib.sha1(url.encode()).hexdigest()[:16]}.json"
            if not path.exists():
                time.sleep(1.0)  # be polite to the public demo server
            r = json.loads(curl(url, path).read_text())
            if r.get("code") != "Ok":
                path.unlink()
                raise RuntimeError(f"OSRM error: {r}")
            t[np.ix_(a, b)] = np.array(r["durations"], float) / 60.0
            d[np.ix_(a, b)] = np.array(r["distances"], float) / 1000.0
    return t, d, len(blocks) ** 2


# --- assembly ------------------------------------------------------------------------------


def build(state: str, year: int, raw: Path, out: Path) -> dict:
    sf = STATE_FIPS[state]
    src = sources(state, year)
    files = {k: fetch(v, raw) for k, v in src.items()}
    nass_path, nass_name = fetch_nass_economics(raw, state)
    gaps = []

    shp = read_counties(files["counties"])
    fips = sorted(shp.index[shp["STATEFP"] == sf])
    Z = len(fips)
    st_geom = shp.loc[fips].to_crs(5070).union_all()

    # BEA jobs and earnings
    emp = read_bea(files["bea_emp"], state, year, {"HA_bea": 70, "HU_bea": 80, "HA_prop_bea": 50, "jobs_bea": 10})
    farm = read_bea(files["bea_farm"], state, year, {"farm_earn": 370})
    earn = read_bea(files["bea_earn"], state, year, {"nonfarm_earn": 82, "farm_earn_cainc5n": 81})
    st = f"{sf}000"
    bea = pd.concat([emp, farm, earn], axis=1)
    # ACS workers and recent immigrants; PEP population
    acs = pd.concat([
        read_acs(files["acs_b08007"], {"B08007_E001": "workers_res", "B08007_E005": "workers_out_state"}, sf),
        read_acs(files["acs_b08604"], {"B08604_E001": "workers_work"}, sf),
        read_acs(files["acs_b05005"], {"B05005_E004": "fb_recent"}, sf),
    ], axis=1)  # fmt: skip
    pep = read_pep(files["pep"], sf, year)
    cen = read_cenpop(files["cenpop"])

    df = pd.DataFrame(index=pd.Index(fips, name="fips"))
    df["name"] = shp.loc[fips, "NAME"]
    df["area_km2"] = shp.loc[fips, "ALAND"].astype(float) / 1e6
    df["pop"] = pep.reindex(fips)
    for c in ("workers_res", "workers_out_state", "workers_work", "fb_recent"):
        df[c] = acs[c].reindex(fips)
    for c in ("HU_bea", "HA_bea", "HA_prop_bea"):
        df[c] = bea[c].reindex(fips)
    df["farm_earn_usd"] = bea["farm_earn"].reindex(fips) * 1e3
    df["nonfarm_earn_usd"] = bea["nonfarm_earn"].reindex(fips) * 1e3

    # rasters: farmland (CDL) and floor space (GHSL)
    geoms_cdl = list(shp.loc[fips].to_crs(5070).geometry)
    areas = zonal_class_area(files["cdl"], geoms_cdl)
    df["TF"] = areas[:, CDL_CROP].sum(axis=1) / 1e4
    df["pasture_ha"] = areas[:, CDL_PASTURE].sum(axis=1) / 1e4
    cdl_total_ha = areas.sum() / 1e4
    geoms_ghsl = list(shp.loc[fips].to_crs("ESRI:54009").geometry)
    df["built_volume_m3"] = zonal_sum([f"zip+file://{files[k]}!{files[k].stem}.tif" for k in src if k.startswith("ghsl_")], geoms_ghsl)
    df["L"] = df["built_volume_m3"] / STOREY_HEIGHT_M

    # BEA suppression (none for IA 2022, but the rule is here): residual of the state total by farmland
    for c, w in (("HA_bea", "TF"), ("HU_bea", "pop"), ("farm_earn_usd", "TF"), ("nonfarm_earn_usd", "pop")):
        total = {"HA_bea": bea.loc[st, "HA_bea"], "HU_bea": bea.loc[st, "HU_bea"],
                 "farm_earn_usd": bea.loc[st, "farm_earn"] * 1e3, "nonfarm_earn_usd": bea.loc[st, "nonfarm_earn"] * 1e3}[c]  # fmt: skip
        df[c], miss = fill_suppressed(df[c].to_numpy(), total, df[w].to_numpy())
        gaps += [dict(var=c, fips=f, rule=f"state total minus disclosed counties, split by {w}") for f in np.array(fips)[miss]]

    # NASS: tenure, land values, cash rents
    nass = read_nass(nass_path)
    owned = nass_series(nass, "AG LAND, OWNED, IN FARMS - ACRES", 2022, "CENSUS", sf)
    rented = nass_series(nass, "AG LAND, RENTED FROM OTHERS, IN FARMS - ACRES", 2022, "CENSUS", sf)
    farmland = nass_series(nass, "FARM OPERATIONS - ACRES OPERATED", 2022, "CENSUS", sf)
    cropland = nass_series(nass, "AG LAND, CROPLAND - ACRES", 2022, "CENSUS", sf)
    value = nass_series(nass, "AG LAND, INCL BUILDINGS - ASSET VALUE, MEASURED IN $ / ACRE", 2022, "CENSUS", sf)
    rent = nass_series(nass, "RENT, CASH, CROPLAND, NON-IRRIGATED - EXPENSE, MEASURED IN $ / ACRE", year, "SURVEY", sf)
    df["owned_acres"] = owned["county"].reindex(fips)
    df["rented_acres"] = rented["county"].reindex(fips)
    df["farmland_census_ha"] = farmland["county"].reindex(fips) * ACRE_HA
    df["cropland_census_ha"] = cropland["county"].reindex(fips) * ACRE_HA
    df["land_value_usd_acre"] = value["county"].reindex(fips)
    # tenure identity: land in farms = owned + rented from others
    for a, b in (("owned_acres", "rented_acres"), ("rented_acres", "owned_acres")):
        m = df[a].isna() & df[b].notna() & df["farmland_census_ha"].notna()
        df.loc[m, a] = df.loc[m, "farmland_census_ha"] / ACRE_HA - df.loc[m, b]
        gaps += [dict(var=a, fips=f, rule="land in farms minus the other tenure (Census of Ag identity)") for f in df.index[m]]
    df["omega"] = df["owned_acres"] / (df["owned_acres"] + df["rented_acres"])
    state_omega = owned["state"] / (owned["state"] + rented["state"])
    m = df["omega"].isna()
    df.loc[m, "omega"] = state_omega
    gaps += [dict(var="omega", fips=f, rule="state owner share") for f in df.index[m]]
    df["cash_rent_usd_acre"] = rent["county"].reindex(fips)
    df["cash_rent_filled"] = df["cash_rent_usd_acre"].isna()
    fill = rent["other"] if np.isfinite(rent["other"]) else rent["state"]
    rule = "NASS 'other (combined) counties' value" if np.isfinite(rent["other"]) else "NASS state value"
    gaps += [dict(var="cash_rent_usd_acre", fips=f, rule=f"not published; {rule} = {fill:g} $/acre")
             for f in df.index[df["cash_rent_filled"]]]  # fmt: skip
    df["cash_rent_usd_acre"] = df["cash_rent_usd_acre"].fillna(fill)
    for name, s in (("land_value_usd_acre", value), ("owned_acres", owned), ("rented_acres", rented)):
        gaps += [dict(var=name, fips=f, rule="(D) in Census of Ag; see fills above") for f in s["suppressed"]]

    # jobs = workers with the external zone
    jobs = reconcile_jobs(*(df[c].to_numpy(float) for c in ("workers_res", "workers_out_state", "workers_work", "HU_bea", "HA_bea")))
    df["wA_obs_usd"] = df["farm_earn_usd"] / df["HA_bea"]
    df["wU_obs_usd"] = df["nonfarm_earn_usd"] / df["HU_bea"]
    bad_wA = df.index[~(df["wA_obs_usd"] > 0)]
    if len(bad_wA):
        raise ValueError(f"non-positive farm earnings per job in {list(bad_wA)}; needs a documented rule")
    df["gateway"] = (df["fb_recent"] / df["workers_res"]) / (df["fb_recent"].sum() / df["workers_res"].sum())
    df["kind"] = county_kinds(fips, df["HU_bea"].to_numpy(), read_metro_counties(files["cbsa"]))

    # locations: population centres, projected (UTM 15N) for x/y
    df["lat"], df["lon"] = cen.loc[fips, "lat"], cen.loc[fips, "lon"]
    nb = shp[(shp["STATEFP"] != sf)].to_crs(5070)
    nb = nb[nb.intersects(st_geom.buffer(NEIGHBOR_BUFFER_M))]
    nb_fips = sorted(nb.index)
    pts = cen.loc[fips + nb_fips]
    t_pts, d_road, n_calls = osrm_table(pts[["lon", "lat"]].to_numpy(), raw / "osrm")
    if np.isnan(t_pts).any():
        raise RuntimeError("OSRM returned unroutable pairs")
    d_line = haversine_km(pts["lat"].to_numpy()[:, None], pts["lon"].to_numpy()[:, None],
                          pts["lat"].to_numpy()[None, :], pts["lon"].to_numpy()[None, :])  # fmt: skip
    own_t, own_d, speed = own_trip(df["area_km2"].to_numpy(), t_pts, d_line, Z)
    df["own_time_min"], df["own_dist_km"] = own_t, own_d
    t, dist = travel_with_external(t_pts, d_line, Z, own_t, own_d)

    # external zone row
    w_nb = cen.loc[nb_fips, "cenpop"].to_numpy(float)
    ext = {c: np.nan for c in df.columns}
    ext.update(
        name="External (out-of-state commuting)", kind="external", cash_rent_filled=False,
        lat=float(np.average(cen.loc[nb_fips, "lat"], weights=w_nb)), lon=float(np.average(cen.loc[nb_fips, "lon"], weights=w_nb)),
        own_time_min=t[Z, Z], own_dist_km=dist[Z, Z], gateway=0.0,
    )  # fmt: skip
    df = pd.concat([df, pd.DataFrame([ext], index=pd.Index([EXTERNAL_FIPS], name="fips"))])
    df["N"], df["HU"], df["HA"] = jobs["N"], jobs["HU"], jobs["HA"]
    cty = df.index != EXTERNAL_FIPS
    # VERIFY: the external zone's floor space, farmland, farm earnings and tenure are state averages
    # per worker / per farm job; nothing about it is observed beyond the commuter counts.
    df.loc[EXTERNAL_FIPS, "L"] = df.loc[cty, "L"].sum() / df.loc[cty, "N"].sum() * df.loc[EXTERNAL_FIPS, "N"]
    df.loc[EXTERNAL_FIPS, "TF"] = df.loc[cty, "TF"].sum() / df.loc[cty, "HA"].sum() * df.loc[EXTERNAL_FIPS, "HA"]
    df.loc[EXTERNAL_FIPS, "wA_obs_usd"] = df.loc[cty, "farm_earn_usd"].sum() / df.loc[cty, "HA_bea"].sum()
    df.loc[EXTERNAL_FIPS, "omega"] = df.loc[cty, "owned_acres"].sum() / (df.loc[cty, "owned_acres"].sum() + df.loc[cty, "rented_acres"].sum())

    from pyproj import Transformer

    x, y = Transformer.from_crs(4326, 26915, always_xy=True).transform(df["lon"].to_numpy(), df["lat"].to_numpy())
    df["x_km"], df["y_km"] = x / 1e3, y / 1e3

    table = COUNTY_SCHEMA.validate(df.reset_index()[COLUMNS].astype({"fips": str, "name": str, "kind": str, "cash_rent_filled": bool}))
    validate_travel(table["fips"].to_numpy(), t, dist)
    out.mkdir(parents=True, exist_ok=True)
    table.to_parquet(out / COUNTY_FILE, index=False)
    np.savez_compressed(out / TRAVEL_FILE, fips=table["fips"].to_numpy(str), t=t, dist=dist)

    official = {
        "pop": pep.get(sf), "workers_res": acs.loc[sf, "workers_res"], "workers_work": acs.loc[sf, "workers_work"],
        "workers_out_state": acs.loc[sf, "workers_out_state"], "fb_recent": acs.loc[sf, "fb_recent"],
        "HU_bea": bea.loc[st, "HU_bea"], "HA_bea": bea.loc[st, "HA_bea"], "HA_prop_bea": bea.loc[st, "HA_prop_bea"],
        "farm_earn_usd": bea.loc[st, "farm_earn"] * 1e3, "nonfarm_earn_usd": bea.loc[st, "nonfarm_earn"] * 1e3,
        "farm_earn_cainc5n_usd": bea.loc[st, "farm_earn_cainc5n"] * 1e3, "jobs_bea": bea.loc[st, "jobs_bea"],
        "owned_acres": owned["state"], "rented_acres": rented["state"], "farmland_census_ha": farmland["state"] * ACRE_HA,
        "cropland_census_ha": cropland["state"] * ACRE_HA, "cash_rent_usd_acre": rent["state"],
        "land_value_usd_acre": value["state"],
    }  # fmt: skip
    meta = dict(state=state, year=year, sources=src, nass_file=nass_name, gaps=gaps, official=official,
                neighbors=nb_fips, osrm_calls=n_calls, speed_km_per_min=speed, cdl_total_ha=cdl_total_ha,
                scale=jobs["scale"], road_over_line=float(np.median(d_road[:Z, :Z][~np.eye(Z, dtype=bool)] / d_line[:Z, :Z][~np.eye(Z, dtype=bool)])),
                raw=raw, built=dt.date.today().isoformat())  # fmt: skip
    (out / "REPORT.md").write_text(report(table, t, meta))
    return dict(table=table, t=t, dist=dist, meta=meta)


# --- report --------------------------------------------------------------------------------


def _fmt(v, digits=0):
    return "n/a" if v is None or not np.isfinite(v) else f"{v:,.{digits}f}"


def report(table: pd.DataFrame, t: np.ndarray, meta: dict) -> str:
    c = table[table["kind"] != "external"]
    e = table[table["kind"] == "external"].iloc[0]
    o = meta["official"]
    raw = meta["raw"]
    L = []
    L += [f"# {STATE_NAME[meta['state']]} {meta['year']} county data: validation report", "",
          f"Built {meta['built']} by `python -m urqse.data.build_state {meta['state']} {meta['year']}`. "
          f"{len(c)} counties plus one external zone. Outputs: `county.parquet` (one row per zone, schema in "
          "`src/urqse/data/schema.py`) and `travel.npz` (`fips`, `t` minutes, `dist` km, rows in table order).", ""]
    L += ["## Sources", "", "| Item | Vintage | File (data_raw) | Retrieved | URL |", "|---|---|---|---|---|"]
    for s in meta["sources"].values():
        p = raw / s.file
        got = dt.date.fromtimestamp(p.stat().st_mtime).isoformat() if p.exists() else "missing"
        L.append(f"| {s.name} | {s.vintage} | `{s.file}` | {got} | {s.url} |")
    L.append(f"| nass | Quick Stats bulk economics file `{meta['nass_file']}` (Census of Agriculture 2022; "
             f"Cash Rents Survey {meta['year']}) | `{meta['nass_file']}` (filtered copy `*_{meta['state']}.tsv.gz`) | "
             f"see file | {NASS_BASE}{meta['nass_file']} |")
    L.append(f"| osrm | OSRM public demo server, car profile (OSM data as served on the build date) | `osrm/*.json` "
             f"({meta['osrm_calls']} cached block requests; the server caps a table at {OSRM_MAX_COORDS} coordinates) | "
             f"{meta['built']} | {OSRM} |")
    L += ["", "## County sums against published state totals", "",
          "| Column | Sum of counties | Published state value | Difference |", "|---|---|---|---|"]
    for col, label in (("pop", "PEP population"), ("workers_res", "ACS workers by residence"),
                       ("workers_work", "ACS workers by workplace"), ("workers_out_state", "ACS workers working out of state"),
                       ("HU_bea", "BEA non-farm employment (L80)"), ("HA_bea", "BEA farm employment (L70)"),
                       ("HA_prop_bea", "BEA farm proprietors (L50)"), ("farm_earn_usd", "BEA farm earnings $ (CAINC45 L370)"),
                       ("nonfarm_earn_usd", "BEA non-farm earnings $ (CAINC5N L82)"), ("fb_recent", "ACS foreign born entered 2010+"),
                       ("owned_acres", "CoA owned acres"), ("rented_acres", "CoA rented-from-others acres"),
                       ("farmland_census_ha", "CoA land in farms, ha"), ("cropland_census_ha", "CoA total cropland, ha")):  # fmt: skip
        s, v = c[col].sum(), o[col]
        L.append(f"| {label} | {_fmt(s)} | {_fmt(v)} | {_fmt(100 * (s / v - 1), 3)}% |")
    L += ["", "## Model columns", "",
          f"- **N, HU, HA (jobs = resident workers).** Each county's BEA farm and non-farm job counts are scaled to its ACS "
          f"count of workers by place of work (scale factor min {np.min(meta['scale']):.3f}, median {np.median(meta['scale']):.3f}, "
          f"max {np.max(meta['scale']):.3f}; BEA counts jobs, ACS counts people by main job). "
          f"Sum N = {_fmt(table['N'].sum())} = sum HU + HA = {_fmt(table['HU'].sum() + table['HA'].sum())}. "
          f"Farm jobs after scaling: {_fmt(c['HA'].sum())} (BEA {_fmt(c['HA_bea'].sum())}). `# VERIFY` the scaling: part-time "
          "farm proprietors with an off-farm main job are counted once, in proportion to the county mix.",
          f"- **External zone.** Residents = out-of-state workers commuting in "
          f"(ACS workplace total minus in-state residents working in state) = {_fmt(e['N'])}. Jobs = in-state residents working "
          f"out of state = {_fmt(e['HU'] + e['HA'])}, split by the state farm share (HA = {_fmt(e['HA'])}). Location: the "
          f"{len(meta['neighbors'])} out-of-state counties within {NEIGHBOR_BUFFER_M / 1e3:g} km of the state "
          f"({', '.join(meta['neighbors'])}); travel time from a county to the zone is the OSRM time to the nearest of them. "
          "Floor space, farmland, farm earnings and owner share are state averages scaled to its workers / farm jobs; "
          "gateway weight 0 (immigrants settle in-state). `# VERIFY` all of these are conventions, not data, and `log(0)` "
          "in `immigration.arrival_shares` needs handling in M3.",
          f"- **TF (farmland, ha).** CDL {meta['year']} crop, hay, fallow and tree-crop classes (codes 1-61, 66-77, 204-254), "
          f"pixel-centre zonal sums on the 30 m Albers grid. State: {_fmt(c['TF'].sum())} ha vs Census of Agriculture "
          f"cropland {_fmt(o['cropland_census_ha'])} ha and land in farms {_fmt(o['farmland_census_ha'])} ha; county ratio "
          f"TF / CoA cropland {(c['TF'] / c['cropland_census_ha']).min():.2f} to {(c['TF'] / c['cropland_census_ha']).max():.2f}. "
          f"Grassland/pasture (codes 62, 176) is kept separately (`pasture_ha`, {_fmt(c['pasture_ha'].sum())} ha). "
          f"County area covered by CDL pixels: {_fmt(meta['cdl_total_ha'])} ha vs land area {_fmt(c['area_km2'].sum() * 100)} ha "
          "(the difference is water). `# VERIFY` whether pasture belongs in T^F for livestock counties.",
          f"- **L (floor space, m^2).** GHSL GHS-BUILT-V 2020 epoch building volume / {STOREY_HEIGHT_M:g} m storey height "
          f"(`# VERIFY` storey height; 2020 is the nearest epoch to {meta['year']}). State volume {_fmt(c['built_volume_m3'].sum() / 1e9, 2)} km^3.",
          f"- **wA_obs_usd.** CAINC45 farm earnings (L370) / CAEMP25N farm employment (L70): state "
          f"{_fmt(e['wA_obs_usd'])} $ per farm job; county range {_fmt(c['wA_obs_usd'].min())} to {_fmt(c['wA_obs_usd'].max())}. "
          f"The loader divides by state non-farm earnings per non-farm job ({_fmt(c['nonfarm_earn_usd'].sum() / c['HU_bea'].sum())} $). "
          f"`# VERIFY` vintage mismatch: CAINC45/CAEMP25N on the BEA site are the 2023-11-16 release, CAINC5N is the 2026 "
          f"file; CAINC5N's revised {meta['year']} farm earnings are {_fmt(o['farm_earn_cainc5n_usd'])} $ vs CAINC45 "
          f"{_fmt(o['farm_earn_usd'])} $. Single-year {meta['year']} farm income is volatile; a multi-year mean may suit M3 better. `# VERIFY` BEA farm earnings are proprietors' income plus farm wages, so they include owner-operators' returns to owned land and capital; read as a wage, wA_obs overstates farm labour earnings in high-rent counties (spec §12.1 separates operator land income).",
          f"- **omega.** Census of Agriculture 2022 owned / (owned + rented from others) acres in farms. "
          f"State {_fmt(e['omega'], 3)}, county range {_fmt(c['omega'].min(), 3)} to {_fmt(c['omega'].max(), 3)}.",
          f"- **cash_rent_usd_acre.** NASS Cash Rents Survey {meta['year']}, non-irrigated cropland. State {_fmt(o['cash_rent_usd_acre'])} $/acre.",
          f"- **land_value_usd_acre.** Census of Agriculture 2022 estimated market value of land and buildings per acre "
          f"(NASS does not publish annual county land values). State {_fmt(o['land_value_usd_acre'])} $/acre.",
          "- **gateway.** ACS foreign born who entered 2010 or later per resident worker, relative to the state ratio "
          "(mean 1 over workers). `# VERIFY` against spec §12.2 once the arrival block is calibrated. "
          f"{int((c['gateway'] == 0).sum())} counties have no recent foreign born in the ACS sample "
          f"({', '.join(c.loc[c['gateway'] == 0, 'name'])}), so their gateway weight is 0 (log(0) in arrival_shares).",
          f"- **kind.** core = the metropolitan county with the most non-farm jobs ({c.loc[c['kind'] == 'core', 'name'].iloc[0]}); "
          f"suburb = other counties in a Metropolitan Statistical Area (OMB 2023) ({(c['kind'] == 'suburb').sum()}); "
          f"rural = the rest ({(c['kind'] == 'rural').sum()}). `# VERIFY` one core for a multi-metro state.",
          f"- **Travel time t (min).** OSRM car durations between 2020 population-weighted county centres, as routed (not "
          f"symmetrised). Off-diagonal median {np.median(t[:-1, :-1][~np.eye(len(c), dtype=bool)]):.1f} min. Own-county "
          f"time = {SQUARE_MEAN_DIST:.4f} x sqrt(land area) at the median effective speed of {meta['speed_km_per_min'] * 60:.1f} "
          f"straight-line km/h between counties (median {_fmt(c['own_time_min'].min(), 1)} to {_fmt(c['own_time_min'].max(), 1)} min). "
          f"`# VERIFY` the own-county proxy. `dist` is great-circle km (road/straight median ratio {meta['road_over_line']:.2f}).", ""]
    L += ["## Suppressed cells and fills", ""]
    if meta["gaps"]:
        L += ["| Variable | County | Rule |", "|---|---|---|"]
        name = dict(zip(table["fips"], table["name"]))
        L += [f"| {g['var']} | {g['fips']} {name.get(g['fips'], '')} | {g['rule']} |" for g in meta["gaps"]]
    else:
        L.append("None.")
    L += ["", "No BEA (D) cells for this state and year: CAEMP25N L50/70/80, CAINC45 L370 and CAINC5N L82 are published "
          "for every county. Census of Agriculture tenure and value cells are all published.", "",
          "## Coverage gaps and caveats", "",
          "- ACS is the 5-year period estimate ending in the base year (no 1-year data for small counties); BEA and PEP are "
          "single-year. The external zone inherits ACS sampling error in the commuter totals.",
          "- The Census API now requires a key, so ACS comes from the table-based summary files instead (same estimates).",
          "- LODES (for the M3 PPML of kappa*lambda) and IRS SOI migration flows are not part of this build.",
          "- Census of Agriculture is quinquennial (2022 matches the base year); the cash-rent survey is annual for Iowa.",
          "- No satellite population layer (GHS-POP) is used; census counts drive calibration (spec §8).", ""]
    L += ["## County table", "",
          "| FIPS | Name | Kind | N | HU | HA | TF ha | L m^2 | wA $ | omega | rent $/ac |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in table.itertuples():
        L.append(f"| {r.fips} | {r.name} | {r.kind} | {_fmt(r.N)} | {_fmt(r.HU)} | {_fmt(r.HA)} | {_fmt(r.TF)} | "
                 f"{_fmt(r.L / 1e6, 2)}M | {_fmt(r.wA_obs_usd)} | {_fmt(r.omega, 3)} | {_fmt(r.cash_rent_usd_acre)}"
                 f"{'*' if r.cash_rent_filled else ''} |")
    L += ["", "`*` filled, see above.", ""]
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("state")
    ap.add_argument("year", type=int)
    ap.add_argument("--raw", type=Path, default=None, help="download cache (default data_raw/{state})")
    ap.add_argument("--out", type=Path, default=None, help="output dir (default data/{state}/{year})")
    a = ap.parse_args(argv)
    state = a.state.upper()
    if state not in STATE_FIPS:
        sys.exit(f"no source configuration for {state}; add it to STATE_FIPS / GHSL_TILES")
    res = build(state, a.year, a.raw or ROOT / "data_raw" / state, a.out or state_dir(state, a.year))
    tb = res["table"]
    if a.out is None:  # data/ is git-ignored; keep a tracked copy of the report
        tracked = ROOT / "reports" / f"{state}_{a.year}_REPORT.md"
        tracked.parent.mkdir(exist_ok=True)
        tracked.write_text((state_dir(state, a.year) / "REPORT.md").read_text())
    print(f"wrote {len(tb)} zones; N={tb['N'].sum():,.0f}  HU={tb['HU'].sum():,.0f}  HA={tb['HA'].sum():,.0f}")


if __name__ == "__main__":
    main()
