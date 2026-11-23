"""Calibrate a built state on real data (milestone M3) and write the calibration report.

    python -m urqse.calibrate.run_state IA 2022 [--snapshot]

Reads data/{state}/{year}/ (built by urqse.data.build_state) and LODES OD files (downloaded once
into data_raw/{state}/lodes/). Writes data/{state}/{year}/calibrated.npz (git-ignored), the
tracked state estimates (calibrate/estimates/{state}_{year}.json), reports/{state}_{year}_CALIBRATION.md
and its xi_A map; --snapshot also rewrites the pinned numbers in tests/snapshots/."""

import argparse
import json
from dataclasses import asdict
from pathlib import Path

import numpy as np
import pandas as pd

from ..data import build_state as bs
from ..data.loaders import COUNTY_FILE, TRAVEL_FILE, read_county, read_travel, state_dir, to_county_data
from ..model.params import Params
from . import checks
from .gravity import commuting_gravity
from .invert import calibrate

ROOT = Path(__file__).resolve().parents[3]
ESTIMATES_DIR = Path(__file__).resolve().parent / "estimates"
SNAPSHOT_DIR = ROOT / "tests" / "snapshots"
LODES_URL = "https://lehd.ces.census.gov/data/lodes/LODES8/{st}/od/{st}_od_{part}_JT00_{year}.csv.gz"
NEIGHBOR_STATES = {"IA": ("il", "mn", "mo", "ne", "sd", "wi")}
EARN_YEARS = 5  # multi-year mean of farm earnings for the theta_T robustness row


# --- tracked state estimates ---------------------------------------------------------------


def state_params(state: str, year: int, **overrides) -> Params:
    """Params() with the state's estimated values (estimates/{state}_{year}.json) on top. The
    global defaults, and so the web app's synthetic scenario, are untouched."""
    est = json.loads((ESTIMATES_DIR / f"{state.upper()}_{year}.json").read_text())
    return Params(**{k: v["value"] for k, v in est["params"].items()}, **overrides)


# --- LODES ---------------------------------------------------------------------------------


def lodes_paths(state: str, year: int, raw: Path) -> list:
    st = state.lower()
    parts = [(st, "main"), (st, "aux")] + [(nb, "aux") for nb in NEIGHBOR_STATES[state]]
    return [
        bs.curl(LODES_URL.format(st=s, part=part, year=year), raw / "lodes" / f"{s}_od_{part}_JT00_{year}.csv.gz")
        for s, part in parts
    ]


def county_flows(paths, fips, ext_counties) -> np.ndarray:
    """LODES JT00 block OD (S000 = all jobs) summed to residence x workplace zones. In-state
    counties keep their index; the out-of-state counties of the external zone map to the last
    index; every other block pair is dropped. Rows = residence (h), columns = workplace (w)."""
    Z = len(fips) + 1
    zone = {f: k for k, f in enumerate(fips)} | {f: Z - 1 for f in ext_counties}
    flows = np.zeros((Z, Z))
    for path in paths:
        od = pd.read_csv(path, usecols=["w_geocode", "h_geocode", "S000"], dtype={"w_geocode": str, "h_geocode": str})
        h = od["h_geocode"].str[:5].map(zone)
        w = od["w_geocode"].str[:5].map(zone)
        keep = h.notna() & w.notna()
        np.add.at(flows, (h[keep].to_numpy(int), w[keep].to_numpy(int)), od.loc[keep, "S000"].to_numpy(float))
    return flows


def gravity_specs(flows, t) -> dict:
    Z = flows.shape[0]
    own = np.eye(Z, dtype=bool)
    instate = np.zeros((Z, Z), bool)
    instate[:-1, :-1] = True
    ext_ext = np.zeros((Z, Z), bool)
    ext_ext[-1, -1] = True
    masks = {
        "in-state, off-diagonal (headline)": instate & ~own,
        "in-state, own-county flows included": instate,
        "in-state, off-diagonal, t <= 90 min": instate & ~own & (t <= 90.0),
        "in-state, off-diagonal, t <= 60 min": instate & ~own & (t <= 60.0),
        "with external zone, off-diagonal": ~own,
        "with external zone, own-county included": ~ext_ext,
    }
    return {name: commuting_gravity(flows, t, m) for name, m in masks.items()}


# --- pipeline ------------------------------------------------------------------------------


def farm_earnings_mean(zip_path, state, year, fips, n_years=EARN_YEARS):
    years = range(year - n_years + 1, year + 1)
    cols = [bs.read_bea(zip_path, state, y, {"e": 370})["e"].reindex(fips) for y in years]
    return 1e3 * pd.concat(cols, axis=1).mean(axis=1).to_numpy(float), (years[0], years[-1])  # BEA $000


def theta_T_table(df, wA_bill_usd, earn_mean) -> dict:
    """theta_T by county under four definitions of the labour bill (report §3). Dollars."""
    rent_bill = df["cash_rent_usd_acre"].to_numpy(float) * df["TF"].to_numpy(float) / checks.HA_PER_ACRE
    E = df["farm_earn_usd"].to_numpy(float)
    omega = df["omega"].to_numpy(float)
    labour = {
        "model wage bill wA_obs x HA (spec §5 literal)": wA_bill_usd,
        "BEA farm earnings as labour": E,
        "BEA farm earnings net of owner-operators' land rent (chosen)": E - omega * rent_bill,
        "same, 5-year mean farm earnings": earn_mean - omega * rent_bill,
    }
    return {
        name: {
            "county": checks.theta_T_from_rents(rent_bill, lab),
            "state": float(checks.theta_T_from_rents(rent_bill.sum(), lab.sum())),
        }
        for name, lab in labour.items()
    }


CHOSEN_THETA = "BEA farm earnings net of owner-operators' land rent (chosen)"
HEADLINE_GRAVITY = "in-state, off-diagonal (headline)"


def run(state: str, year: int, raw: Path, ddir: Path) -> dict:
    df = read_county(ddir / COUNTY_FILE)
    fips_all, t, dist = read_travel(ddir / TRAVEL_FILE)
    data = to_county_data(df, fips_all, t, dist)
    counties = (df["kind"] != "external").to_numpy()
    cdf = df[counties].reset_index(drop=True)
    fips = cdf["fips"].tolist()
    usd = float(cdf["nonfarm_earn_usd"].sum() / cdf["HU_bea"].sum())  # $ per model wage unit

    files = {k: bs.fetch(v, raw) for k, v in bs.sources(state, year).items() if k in ("counties", "bea_farm")}
    shp = bs.read_counties(files["counties"])
    sf = bs.STATE_FIPS[state]
    ext_counties = bs.neighbor_counties(shp, sf, shp.loc[fips].to_crs(5070).union_all())

    # 4. kappa*lam by PPML on LODES
    flows = county_flows(lodes_paths(state, year, raw), fips, ext_counties)
    gravity = gravity_specs(flows, t)
    kl = gravity[HEADLINE_GRAVITY]

    # 3. theta_T from rent shares
    wA_bill_usd = data.wA_obs[counties] * data.HA[counties] * usd
    earn_mean, earn_years = farm_earnings_mean(files["bea_farm"], state, year, fips)
    theta = theta_T_table(cdf, wA_bill_usd, earn_mean)
    theta_hat = theta[CHOSEN_THETA]["state"]

    # 1. inversion: default params, and the state estimates
    p0 = Params()
    p_state = Params(kappa_lam=kl.kappa_lam, theta_T=theta_hat)
    cal0, cal = calibrate(data, p0), calibrate(data, p_state)

    # 2. over-identification: model rho vs NASS cash rents (published counties only)
    pub = ~cdf["cash_rent_filled"].to_numpy(bool)
    obs = cdf["cash_rent_usd_acre"].to_numpy(float)
    TF = cdf["TF"].to_numpy(float)
    overid = {}
    for label, c, p in (("theta_T = 0.40 (default)", cal0, p0), (f"theta_T = {theta_hat:.3f} (estimated)", cal, p_state)):
        model = checks.rent_usd_per_acre(c.baseline.within.rho[counties], usd)
        o = checks.overid(model[pub], obs[pub], TF[pub])
        o["model"] = model
        o["theta_T"] = p.theta_T
        overid[label] = o
    # how much of the level gap is the job scaling (ACS headcount / BEA jobs) in HA
    scale = (cdf["HA"] / cdf["HA_bea"]).to_numpy(float)
    unscaled = overid["theta_T = 0.40 (default)"]["model"] / scale
    unscaled_ratio = float(np.sum(unscaled[pub] * TF[pub]) / np.sum(obs[pub] * TF[pub]))

    return dict(
        state=state, year=year, df=df, cdf=cdf, data=data, usd=usd, counties=counties, shp=shp, fips=fips,
        flows=flows, gravity=gravity, theta=theta, theta_hat=theta_hat, earn_years=earn_years,
        p0=p0, p_state=p_state, cal0=cal0, cal=cal, overid=overid, pub=pub, scale=scale,
        unscaled_ratio=unscaled_ratio, ext_counties=ext_counties,
        earn_2022_over_mean=float(cdf["farm_earn_usd"].sum() / earn_mean.sum()),
    )  # fmt: skip


def snapshot(r) -> dict:
    """The pinned real-data numbers (tests/test_snapshot_iowa.py)."""
    f, w = r["cal"].fundamentals, r["cal"].baseline.within
    c = r["counties"]
    o = r["overid"]["theta_T = 0.40 (default)"]
    return {
        "kappa_lam": r["gravity"][HEADLINE_GRAVITY].kappa_lam,
        "kappa_lam_own_included": r["gravity"]["in-state, own-county flows included"].kappa_lam,
        "theta_T": r["theta_hat"],
        "overid_corr": o["corr"],
        "overid_level_ratio": o["level_ratio"],
        "xi_A_median": float(np.median(f.xi_A[c])),
        "xi_A_sum_log": float(np.sum(np.log(f.xi_A[c]))),
        "B_sum_log": float(np.sum(np.log(f.B))),
        "A_sum_log": float(np.sum(np.log(f.A))),
        "wU_core": float(w.wU[r["data"].core]),
        "U_bar": float(f.U_bar),
        "lodes_total_flows": float(r["flows"].sum()),
    }


def save_calibrated(r, path: Path):
    f, w = r["cal"].fundamentals, r["cal"].baseline.within
    np.savez_compressed(
        path, fips=r["df"]["fips"].to_numpy(str), params=json.dumps(asdict(r["p_state"])),
        **asdict(f), N=r["cal"].baseline.N, wU=w.wU, wA=w.wA, r=w.r, rho=w.rho,
        usd_per_wage_unit=r["usd"],
    )  # fmt: skip


def write_estimates(r, path: Path):
    g = r["gravity"][HEADLINE_GRAVITY]
    est = {
        "state": r["state"],
        "year": r["year"],
        "params": {
            "kappa_lam": {
                "value": g.kappa_lam,
                "se_cluster_origin": g.se_cluster_origin,
                "source": f"PPML on LODES8 OD JT00 {r['year']} county pairs, in-state, off-diagonal, "
                "origin + destination FE, OSRM car minutes (urqse.calibrate.run_state)",
                "verify": True,
            },
            "theta_T": {
                "value": r["theta_hat"],
                "source": f"state rent share: NASS {r['year']} non-irrigated cash rent x CDL cropland over "
                "(BEA CAINC45 farm earnings + rent paid to non-operator landlords) (spec §5 step 5)",
                "verify": True,
            },
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(est, indent=2) + "\n")


def main(argv=None):
    from .report import write_report

    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("state")
    ap.add_argument("year", type=int)
    ap.add_argument("--snapshot", action="store_true", help="rewrite tests/snapshots/{state}_{year}.json")
    a = ap.parse_args(argv)
    state = a.state.upper()
    ddir = state_dir(state, a.year)
    r = run(state, a.year, ROOT / "data_raw" / state, ddir)
    save_calibrated(r, ddir / "calibrated.npz")
    write_estimates(r, ESTIMATES_DIR / f"{state}_{a.year}.json")
    write_report(r, ROOT / "reports")
    if a.snapshot:
        SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
        (SNAPSHOT_DIR / f"{state}_{a.year}.json").write_text(json.dumps(snapshot(r), indent=2) + "\n")
    print(f"calibrated {state} {a.year}: kappa*lam = {r['gravity'][HEADLINE_GRAVITY].kappa_lam:.4f}, "
          f"theta_T = {r['theta_hat']:.3f}")  # fmt: skip


if __name__ == "__main__":
    main()
