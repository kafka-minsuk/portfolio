"""Calibrate a built state on real data (milestone M3) and write the calibration report.

    python -m urqse.calibrate.run_state IA 2022 [--snapshot]

Reads data/{state}/{year}/ (built by urqse.data.build_state) and LODES OD files (downloaded once
into data_raw/US/lodes/: the state's main and aux files and the aux files of the states that hold
the external zone's counties). Writes data/{state}/{year}/calibrated.npz (git-ignored), the
tracked state estimates (calibrate/estimates/{state}_{year}.json), reports/{state}_{year}_CALIBRATION.md
and its xi_A map; --snapshot also rewrites the pinned numbers in tests/snapshots/."""

import argparse
import json
from dataclasses import asdict, replace
from pathlib import Path

import numpy as np
import pandas as pd

from ..data import build_state as bs
from ..data.loaders import COUNTY_FILE, TRAVEL_FILE, read_county, read_travel, state_dir, to_county_data, usd_per_wage_unit
from ..model import land
from ..model.params import Params
from . import checks
from .gravity import commuting_gravity
from .invert import calibrate

ROOT = Path(__file__).resolve().parents[3]
ESTIMATES_DIR = Path(__file__).resolve().parent / "estimates"
SNAPSHOT_DIR = ROOT / "tests" / "snapshots"
LODES_URL = "https://lehd.ces.census.gov/data/lodes/LODES8/{st}/od/{st}_od_{part}_JT00_{year}.csv.gz"
EARN_YEARS = 5  # multi-year mean of BEA farm earnings for the M3 theta_T comparison row


# --- tracked state estimates ---------------------------------------------------------------


def state_estimates(state: str, year: int) -> dict:
    return json.loads((ESTIMATES_DIR / f"{state.upper()}_{year}.json").read_text())


def state_params(state: str, year: int, **overrides) -> Params:
    """Params() with the state's estimated values (estimates/{state}_{year}.json) on top. The
    global defaults, and so the web app's synthetic scenario, are untouched."""
    est = state_estimates(state, year)
    return Params(**{k: v["value"] for k, v in est["params"].items()}, **overrides)


# --- LODES ---------------------------------------------------------------------------------


def neighbor_states(ext_counties) -> tuple:
    """Postal codes (lower case) of the states that hold the external zone's counties."""
    return tuple(sorted({bs.FIPS_STATE[f[:2]].lower() for f in ext_counties}))


LODES_FALLBACK_YEARS = 3  # a state LODES has not released for the year uses its latest earlier year


def lodes_paths(state: str, year: int, ext_counties, shared: Path = bs.SHARED_RAW, download: bool = True) -> list:
    """OD files for the state and its neighbours. Where LODES has no file for `year` (Michigan has
    no 2022 release), the latest of the LODES_FALLBACK_YEARS earlier years is used.
    # VERIFY: commuting in an earlier year stands in for the base year for that state."""
    st = state.lower()
    parts = [(st, "main"), (st, "aux")] + [(nb, "aux") for nb in neighbor_states(ext_counties)]

    def path(s, part, y):
        return shared / "lodes" / f"{s}_od_{part}_JT00_{y}.csv.gz"

    if not download:
        return [path(s, part, year) for s, part in parts]
    out = []
    for s, part in parts:
        for y in range(year, year - LODES_FALLBACK_YEARS - 1, -1):
            if path(s, part, y).exists() or bs.url_exists(LODES_URL.format(st=s, part=part, year=y)):
                out.append(bs.curl(LODES_URL.format(st=s, part=part, year=y), path(s, part, y)))
                break
        else:
            raise FileNotFoundError(f"no LODES {s} {part} file for {year} or the {LODES_FALLBACK_YEARS} years before")
    return out


def lodes_years(paths) -> dict:
    """{file stem: year} for every LODES file that is not from the base year."""
    return {p.name: int(p.name.rsplit("_", 1)[1][:4]) for p in paths}


def county_flows(paths, fips, ext_counties, zone_of=None) -> np.ndarray:
    """LODES JT00 block OD (S000 = all jobs) summed to residence x workplace zones. In-state
    counties keep their zone's index (`zone_of` maps a county to a merged BEA zone); the out-of-state
    counties of the external zone map to the last index; every other block pair is dropped.
    Rows = residence (h), columns = workplace (w)."""
    Z = len(fips) + 1
    index = {f: k for k, f in enumerate(fips)}
    zone = {c: index[z] for c, z in (zone_of or {}).items() if z in index} | index | {f: Z - 1 for f in ext_counties}
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


def theta_T_table(df, earn_mean) -> dict:
    """theta_T by county under each definition of the farm labour bill (report §4). Dollars.
    Counties without a farm sector (spec §3.11) have no rent bill and a NaN county theta_T."""
    farm = df["HA"].to_numpy(float) > 0
    rent_bill = np.where(farm, df["cash_rent_usd_acre"].to_numpy(float) * df["TF"].to_numpy(float) / checks.HA_PER_ACRE, 0.0)
    E = df["farm_earn_usd"].to_numpy(float)
    omega = df["omega"].to_numpy(float)
    jobs = df["HA_bea"].to_numpy(float)
    per_ws_job = jobs / (jobs - df["HA_prop_bea"].to_numpy(float))  # every farm job at the wage-job rate
    labour = {
        CHOSEN_THETA: df["wA_obs_usd"].to_numpy(float) * df["HA"].to_numpy(float),
        "same, single-year compensation per farm wage job": df["farm_comp_usd"].to_numpy(float) * per_ws_job,
        "CoA hired labour expense per farm wage job, all farm jobs": df["hired_labor_coa_usd"].to_numpy(float) * per_ws_job,
        "M3: BEA farm earnings as labour": E,
        M3_THETA: E - omega * rent_bill,
        "M3: same, 5-year mean farm earnings": earn_mean - omega * rent_bill,
    }
    return {
        name: {
            "county": checks.theta_T_from_rents(rent_bill, lab),
            "state": float(checks.theta_T_from_rents(rent_bill.sum(), lab.sum())),
        }
        for name, lab in labour.items()
    }


def farm_income_accounts(cal, data, counties, usd, E) -> dict:
    """Spec §12.1 income routing on the calibrated baseline, state totals in $: farm labour (hired
    and operator wages), owner-operated land rent, landlord rent, against BEA farm earnings E
    (wages + proprietors' income). The identity labour + owner rent + landlord rent = w_A H_A + rho T^F
    holds by construction; the comparison with E shows what wA_obs already contains."""
    w = cal.baseline.within
    c = counties & (data.HA > 0)  # farm income only where there is a farm sector (spec §3.11)
    HA, TF, omega = data.HA[c], data.TF[c], data.omega[c]
    operator = land.operator_income(w.wA[c], w.rho[c], TF, HA, omega) * HA * usd
    labour = w.wA[c] * HA * usd
    owner_rent = operator - labour
    landlord = land.landlord_income(w.rho[c], TF, omega) * usd
    identity = (operator.sum() + landlord.sum()) / ((w.wA[c] * HA + w.rho[c] * TF).sum() * usd) - 1.0
    return dict(labour=labour.sum(), owner_rent=owner_rent.sum(), landlord=landlord.sum(),
                operator=operator.sum(), E=float(np.sum(E)), identity_rel=float(identity),
                operator_over_E=float(operator.sum() / np.sum(E)))  # fmt: skip


CHOSEN_THETA = "farm labour bill wA_obs x HA (chosen; spec §5 literal)"
M3_THETA = "M3: BEA farm earnings net of owner-operators' land rent (M3 choice)"
HEADLINE_GRAVITY = "in-state, off-diagonal (headline)"
# A state too small for the headline (Delaware: 3 counties, 6 pairs for 6 parameters) uses the
# sample with own-county flows.  # VERIFY: own-county times are the area proxy (report §5).
FALLBACK_GRAVITY = "in-state, own-county flows included"


def chosen_gravity(gravity: dict) -> str:
    return HEADLINE_GRAVITY if gravity[HEADLINE_GRAVITY].info.converged else FALLBACK_GRAVITY


def overid_runs(cal0, cal, p0, p, counties, cdf, usd, pub) -> dict:
    obs = cdf["cash_rent_usd_acre"].to_numpy(float)
    TF = cdf["TF"].to_numpy(float)
    out = {}
    for label, c, q in (("theta_T = 0.40 (default)", cal0, p0), (f"theta_T = {p.theta_T:.3f} (estimated)", cal, p)):
        model = checks.rent_usd_per_acre(c.baseline.within.rho[counties], usd)
        o = checks.overid(model[pub], obs[pub], TF[pub])
        o["model"] = model
        o["theta_T"] = q.theta_T
        out[label] = o
    return out


def run(state: str, year: int, raw: Path, ddir: Path, shared: Path = bs.SHARED_RAW) -> dict:
    df = read_county(ddir / COUNTY_FILE)
    fips_all, t, dist = read_travel(ddir / TRAVEL_FILE)
    data = to_county_data(df, fips_all, t, dist)
    counties = (df["kind"] != "external").to_numpy()
    cdf = df[counties].reset_index(drop=True)
    fips = cdf["fips"].tolist()
    usd = usd_per_wage_unit(df)  # $ per model wage unit (non-farm earnings per non-farm worker)

    files = {k: bs.fetch(v, raw, shared) for k, v in bs.sources(state, year).items() if k in ("counties", "bea_farm", "bea_emp")}
    shp = bs.read_counties(files["counties"])
    sf = bs.STATE_FIPS[state]
    zones, zone_of = bs.state_zones(shp, files["bea_emp"], state)
    ext_counties = bs.neighbor_counties(shp, sf, zones.loc[fips].to_crs(5070).union_all())

    # 4. kappa*lam by PPML on LODES
    lodes = lodes_paths(state, year, ext_counties, shared)
    lodes_fallback = {k: v for k, v in lodes_years(lodes).items() if v != year}
    flows = county_flows(lodes, fips, ext_counties, zone_of)
    gravity = gravity_specs(flows, t)
    used = chosen_gravity(gravity)
    kl = gravity[used]
    if not kl.info.converged:
        raise ValueError(f"{state}: kappa*lam is not identified by the headline or the fallback sample")

    # 3. theta_T from rent shares
    earn_mean, earn_years = farm_earnings_mean(files["bea_farm"], state, year, fips)
    theta = theta_T_table(cdf, earn_mean)
    theta_hat = theta[CHOSEN_THETA]["state"]

    # 1. inversion: default params, and the state estimates
    p0 = Params()
    p_state = Params(kappa_lam=kl.kappa_lam, theta_T=theta_hat)
    cal0, cal = calibrate(data, p0), calibrate(data, p_state)

    # 2. over-identification: model rho vs NASS cash rents (published counties only)
    pub = ~cdf["cash_rent_filled"].to_numpy(bool) & (cdf["HA"].to_numpy(float) > 0)  # published rent, farm sector
    overid = overid_runs(cal0, cal, p0, p_state, counties, cdf, usd, pub)
    obs = cdf["cash_rent_usd_acre"].to_numpy(float)
    TF = cdf["TF"].to_numpy(float)
    bill = cdf["farm_labour_bill_usd"].to_numpy(float)
    corr_log_farmland = float(np.corrcoef(np.log(bill[pub] / cdf["farmland_census_ha"].to_numpy(float)[pub]), np.log(obs[pub]))[0, 1])
    E = cdf["farm_earn_usd"].to_numpy(float)
    accounts = farm_income_accounts(cal, data, counties, usd, E)

    # M3 for comparison: wA_obs = BEA farm earnings per BEA job, wage unit per BEA non-farm job.
    # Skipped where a county's BEA farm earnings are not positive (they are net of expenses).
    usd_m3 = float(cdf["nonfarm_earn_usd"].sum() / cdf["HU_bea"].sum())
    wA_m3 = df["wA_bea_earn_usd"].to_numpy(float).copy()
    wA_m3[~counties] = E.sum() / cdf["HA_bea"].sum()
    m3 = None
    if np.all(wA_m3 > 0) and 0.0 < theta[M3_THETA]["state"] < 1.0:
        data_m3 = replace(data, wA_obs=wA_m3 / usd_m3)
        p_m3 = Params(kappa_lam=kl.kappa_lam, theta_T=theta[M3_THETA]["state"])
        cal0_m3, cal_m3 = calibrate(data_m3, p0), calibrate(data_m3, p_m3)
        scale = (cdf["HA"] / cdf["HA_bea"]).to_numpy(float)
        overid_m3 = overid_runs(cal0_m3, cal_m3, p0, p_m3, counties, cdf, usd_m3, pub)
        m3 = dict(
            data=data_m3, p=p_m3, cal0=cal0_m3, cal=cal_m3, overid=overid_m3, usd=usd_m3, scale=scale,
            accounts=farm_income_accounts(cal_m3, data_m3, counties, usd_m3, E),
            unscaled_ratio=float(np.sum((overid_m3["theta_T = 0.40 (default)"]["model"] / scale * TF)[pub])
                                 / np.sum((obs * TF)[pub])),
        )  # fmt: skip

    return dict(
        state=state, year=year, df=df, cdf=cdf, data=data, usd=usd, counties=counties, shp=zones, fips=fips,
        flows=flows, gravity=gravity, theta=theta, theta_hat=theta_hat, earn_years=earn_years,
        p0=p0, p_state=p_state, cal0=cal0, cal=cal, overid=overid, pub=pub, m3=m3, accounts=accounts,
        corr_log_farmland=corr_log_farmland, ext_counties=ext_counties, lodes_fallback=lodes_fallback, gravity_used=used, neighbor_states=neighbor_states(ext_counties),
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
        "wA_obs_state_usd": float((r["cdf"]["wA_obs_usd"] * r["cdf"]["HA"]).sum() / r["cdf"]["HA"].sum()),
        "theta_T_county_max": float(r["theta"][CHOSEN_THETA]["county"].max()),
    }


def save_calibrated(r, path: Path):
    f, w = r["cal"].fundamentals, r["cal"].baseline.within
    np.savez_compressed(
        path, fips=r["df"]["fips"].to_numpy(str), params=json.dumps(asdict(r["p_state"])),
        **asdict(f), N=r["cal"].baseline.N, wU=w.wU, wA=w.wA, r=w.r, rho=w.rho,
        usd_per_wage_unit=r["usd"],
    )  # fmt: skip


def write_estimates(r, path: Path):
    g = r["gravity"][r["gravity_used"]]
    est = {
        "state": r["state"],
        "year": r["year"],
        "params": {
            "kappa_lam": {
                "value": g.kappa_lam,
                "se_cluster_origin": g.se_cluster_origin,
                "source": f"PPML on LODES8 OD JT00 {r['year']} county pairs, "
                + ("in-state, off-diagonal, " if r["gravity_used"] == HEADLINE_GRAVITY else f"{r['gravity_used']} (headline not identified), ")
                + "origin + destination FE, OSRM car minutes (urqse.calibrate.run_state)"
                + (f"; earlier-year LODES files: {', '.join(sorted(r['lodes_fallback']))}" if r.get("lodes_fallback") else ""),
                "verify": True,
            },
            "theta_T": {
                "value": r["theta_hat"],
                "source": f"state rent share: NASS {r['year']} non-irrigated cash rent x CDL cropland over "
                "(that rent bill + farm labour bill wA_obs x HA) (spec §5 step 5); labour bill = BEA farm "
                "compensation per farm wage job, 5-year mean, x BEA farm jobs (urqse.data.build_state)",
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
    print(f"calibrated {state} {a.year}: kappa*lam = {r['gravity'][r['gravity_used']].kappa_lam:.4f}, "
          f"theta_T = {r['theta_hat']:.3f}")  # fmt: skip


if __name__ == "__main__":
    main()
