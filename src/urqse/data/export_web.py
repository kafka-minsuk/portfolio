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
from .build_state import STATE_NAME, read_counties, sources, state_crs, state_zones
from .loaders import COUNTY_FILE, TRAVEL_FILE, read_county, read_travel, state_dir, to_county_data, usd_per_wage_unit

ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = ROOT / "docs" / "migration" / "data"
INDEX_FILE = "regions.json"
SIMPLIFY_M = 400.0
CORE_LABEL = {"IA": "Polk (Des Moines)"}


def county_polygons(shp, fips, crs: int) -> list:
    """Per county: a list of polygons, each a list of rings, each ring a flat [x0, y0, x1, y1, ...]
    in km. None for the external zone (not a polygon)."""
    counties = [f for f in fips if f in shp.index]
    geoms = shapely.coverage_simplify(shp.loc[counties].to_crs(crs).geometry.values, SIMPLIFY_M)
    by_fips = dict(zip(counties, geoms))

    def rings(poly):
        return [np.round(np.asarray(r.coords)[:-1] / 1e3, 1).ravel().tolist() for r in (poly.exterior, *poly.interiors)]

    def polys(g):
        return [rings(p) for p in getattr(g, "geoms", [g])]

    return [polys(by_fips[f]) if f in by_fips else None for f in fips]


def region_document(state: str, year: int) -> dict:
    d = state_dir(state, year)
    df = read_county(d / COUNTY_FILE)
    fips, t, dist = read_travel(d / TRAVEL_FILE)
    data = to_county_data(df, fips, t, dist)
    src = sources(state, year)
    shared = ROOT / "data_raw" / "US"
    shp, _ = state_zones(read_counties(shared / src["counties"].file), shared / src["bea_emp"].file, state)
    est = state_estimates(state, year)
    return {
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
        "geometry": county_polygons(shp, fips, state_crs(shp)),
    }


def index_entry(doc: dict) -> dict:
    kind = doc["counties"]["kind"]
    n = sum(k != "external" for k in kind)
    return {"id": doc["region"], "label": doc["label"], "counties": n, "core_label": doc["core_label"],
            "suburbs": sum(k == "suburb" for k in kind), "rural": sum(k == "rural" for k in kind)}  # fmt: skip


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
