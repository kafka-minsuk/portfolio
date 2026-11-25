"""Export a built, calibrated state for the web simulator (offline; needs pandas and geopandas).

    python -m urqse.data.export_web IA 2022

Writes docs/migration/data/{state}_{year}.json, the region document the browser model reads, and
updates docs/migration/data/regions.json, the list of regions the page offers. The document's
shape is documented once, in urqse.api (REGION DOCUMENT). The travel matrix is rounded to 0.01
minutes and distances to 0.01 km; county geometry is simplified as a coverage (shared borders stay
shared) and rounded to 0.1 km."""

import argparse
import json
from pathlib import Path

import numpy as np
import shapely

from ..api import REGION_FORMAT
from ..calibrate.run_state import state_estimates
from .build_state import STATE_NAME, read_counties, read_metro_areas, sources, state_crs, state_zones
from .loaders import (
    COUNTY_FILE, METRO_FILE, METRO_TRAVEL_FILE, TRAVEL_FILE, read_county, read_metro, read_travel, state_dir,
    to_county_data, usd_per_wage_unit,
)  # fmt: skip

ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = ROOT / "docs" / "migration" / "data"
INDEX_FILE = "regions.json"
SIMPLIFY_M = 400.0
SIMPLIFY_TRACT_M = 60.0  # tracts are small: keep more detail

CORE_LABEL = {"IA": "Polk (Des Moines)"}


def county_polygons(shp, fips, crs: int, simplify_m: float = SIMPLIFY_M) -> list:
    """Per county: a list of polygons, each a list of rings, each ring a flat [x0, y0, x1, y1, ...]
    in km. None for the external zone (not a polygon)."""
    counties = [f for f in fips if f in shp.index]
    geoms = shapely.coverage_simplify(shp.loc[counties].to_crs(crs).geometry.values, simplify_m)
    by_fips = dict(zip(counties, geoms))

    def rings(poly):
        return [np.round(np.asarray(r.coords)[:-1] / 1e3, 1).ravel().tolist() for r in (poly.exterior, *poly.interiors)]

    def polys(g):
        return [rings(p) for p in getattr(g, "geoms", [g])]

    return [polys(by_fips[f]) if f in by_fips else None for f in fips]


def region_document(state: str, year: int) -> dict:
    """The region document; with data/{state}/{year}/metro.parquet (urqse.data.build_metro) the core's
    metro is split into tracts (spec §3.12), and the state map keeps county outlines."""
    d = state_dir(state, year)
    county_df = read_county(d / COUNTY_FILE)
    metro = (d / METRO_FILE).exists()
    df = read_metro(d / METRO_FILE) if metro else county_df
    fips, t, dist = read_travel(d / (METRO_TRAVEL_FILE if metro else TRAVEL_FILE))
    data = to_county_data(df, fips, t, dist)
    src = sources(state, year)
    shared = ROOT / "data_raw" / "US"
    shp, zone_of = state_zones(read_counties(shared / src["counties"].file), shared / src["bea_emp"].file, state)
    crs = state_crs(shp)
    est = state_estimates(state, year)
    doc = {
        "format": REGION_FORMAT,
        "region": f"{state}_{year}",
        "label": f"{STATE_NAME.get(state, state)} {year}",
        "core_label": CORE_LABEL.get(state, data.names[data.core]),
        "usd_per_wage_unit": usd_per_wage_unit(df),
        "params": {k: v["value"] for k, v in est["params"].items()},
        "counties": {
            "fips": list(fips), "name": list(data.names), "kind": data.kind.tolist(),
            "x_km": data.x.tolist(), "y_km": data.y.tolist(), "N": data.N.tolist(), "HU": data.HU.tolist(),
            "HA": data.HA.tolist(), "L": data.L.tolist(), "TF": data.TF.tolist(), "wA_obs": data.wA_obs.tolist(),
            "omega": data.omega.tolist(), "gateway": data.gateway.tolist(),
        },  # fmt: skip
        "t_min": np.round(t, 2).tolist(),
        "dist_km": np.round(dist, 2).tolist(),
        "geometry": county_polygons(shp, fips, crs),
    }
    parent = df["parent"].tolist() if metro else list(fips)
    nest, metro_core, doc["metros"] = metro_nests(county_df, parent, read_metro_areas(shared / src["cbsa"].file), zone_of)
    doc["counties"] |= {"nest": nest, "metro_core": metro_core}
    if not metro:
        return doc
    # tracts in the core's metro: zones are counties + tracts; the state map draws the county view
    parents = list(dict.fromkeys(df["parent"]))
    cv = county_df.set_index("fips").loc[parents]
    doc["counties"] |= {"parent": df["parent"].tolist()}
    doc["county_view"] = {"fips": parents, "name": cv["name"].tolist(), "kind": cv["kind"].tolist(),
                          "x_km": cv["x_km"].tolist(), "y_km": cv["y_km"].tolist()}  # fmt: skip
    doc["geometry"] = county_polygons(shp, parents, crs)
    inside = df["fips"].str.len().to_numpy() == 11  # tracts
    sf = df.loc[inside, "fips"].iloc[0][:2]
    tracts = read_counties(ROOT / "data_raw" / state / "tract" / f"cb_2022_{sf}_tract_500k.zip")
    doc["metros"][0]["tracts"] = int(inside.sum())
    doc["city"] = {"geometry": county_polygons(tracts, list(np.asarray(fips)[inside]), crs, simplify_m=SIMPLIFY_TRACT_M),
                   "label": f"{CORE_LABEL.get(state, data.names[data.core])} metro area"}  # fmt: skip
    return doc


def metro_nests(county_df, parent: list, areas: dict, zone_of: dict):
    """Each Metropolitan Statistical Area (its in-state counties) is a nest (spec §3.12). Metro 0 holds
    the state's core; the others follow by resident workers. A metro's core is its county with the
    most non-farm jobs. Returns (nest label per zone, metro-core flag per zone, metro list)."""
    c = county_df[county_df["kind"] != "external"].set_index("fips")
    groups: dict = {}
    for county, (code, title) in areas.items():
        z = zone_of.get(county)
        if z in c.index:
            groups.setdefault(code, (title, set()))[1].add(z)
    main = c.index[c["kind"] == "core"][0]
    order = sorted(groups, key=lambda g: (main not in groups[g][1], -c.loc[sorted(groups[g][1]), "N"].sum()))
    metro_of, core_of, metros = {}, {}, []
    for k, g in enumerate(order):
        title, members = groups[g]
        members = sorted(members)
        core = main if main in members else c.loc[members, "HU"].idxmax()
        metro_of |= dict.fromkeys(members, k)
        core_of[k] = core
        metros.append({"id": k, "cbsa": g, "name": title.rsplit(",", 1)[0], "core": c.loc[core, "name"],
                       "counties": len(members), "tracts": 0})  # fmt: skip
    nest = [metro_of.get(p, -1) for p in parent]
    metro_core = [n >= 0 and p == core_of[n] for p, n in zip(parent, nest)]
    return nest, metro_core, metros


def index_entry(doc: dict) -> dict:
    kind = doc.get("county_view", doc["counties"])["kind"]
    n = sum(k != "external" for k in kind)
    entry = {"id": doc["region"], "label": doc["label"], "counties": n, "core_label": doc["core_label"],
             "suburbs": sum(k == "suburb" for k in kind), "rural": sum(k == "rural" for k in kind)}  # fmt: skip
    entry["metros"] = len(doc.get("metros", []))
    if "city" in doc:
        entry["tracts"] = len(doc["city"]["geometry"])
    return entry


def update_index(doc: dict, out_dir: Path = OUT_DIR) -> Path:
    """Upsert the region into regions.json (sorted by label)."""
    path = out_dir / INDEX_FILE
    regions = json.loads(path.read_text())["regions"] if path.exists() else []
    regions = sorted([r for r in regions if r["id"] != doc["region"]] + [index_entry(doc)], key=lambda r: r["label"])
    path.write_text(json.dumps({"regions": regions}, indent=1) + "\n")
    return path


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("state")
    ap.add_argument("year", type=int)
    a = ap.parse_args(argv)
    doc = region_document(a.state.upper(), a.year)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"{doc['region']}.json"
    out.write_text(json.dumps(doc, separators=(",", ":")) + "\n")
    update_index(doc)
    print(f"wrote {out.relative_to(ROOT)} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
