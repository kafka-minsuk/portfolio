"""The browser boundary: JSON-shaped dict in, JSON-shaped dict out. Nothing else is called from JS.

Regions. "synthetic" (the default) is built in (urqse.synthetic). A real region comes as a REGION
DOCUMENT, passed to default_scenario() and run() as `region_doc`. It is written offline by
`python -m urqse.data.export_web {state} {year}` to docs/migration/data/{region}.json and has this
shape (Z = counties + the external zone, which is last and has kind "external"):

    format             REGION_FORMAT
    region             id, e.g. "IA_2022"; scenario["region"] must match it
    label, core_label  display names, e.g. "Iowa 2022", "Polk (Des Moines)"
    usd_per_wage_unit  dollars per model wage unit (state non-farm earnings per non-farm worker)
    params             estimated Params fields, layered over Params() (e.g. kappa_lam, theta_T)
    counties           columns of length Z: fips, name, kind (core|suburb|rural|external), x_km,
                       y_km, N, HU, HA, L, TF (ha), wA_obs (wage units), omega, gateway
    t_min, dist_km     Z x Z travel time (minutes) and distance (km), residence rows
    geometry           entries for the map only (not read here): a list of polygons, each a list
                       of rings [x0, y0, x1, y1, ...] in km in the x_km / y_km frame; null for the
                       external zone. One per county (Z, or C with a metro nest)

A region with a metro nest (spec §3.12, urqse.data.build_metro) has census tracts among its zones:
    counties.nest      Z ints: 0 = a tract of the metro nest, -1 = a county or the external zone
    counties.parent    Z FIPS: a tract's county (a county's own FIPS; "EXT")
    county_view        the state map's units, C = distinct parents in order of first appearance:
                       fips, name, kind, x_km, y_km
    city               geometry: one entry per nest zone, in zone order (the tract map)
run() then reports the state view summed to counties in the usual fields and the tracts under "city".
"""

import math

import numpy as np

from .calibrate.invert import calibrate
from .model import land
from .model.analytic import two_location_check
from .model.dynamics import ConsolidationStop, simulate
from .model.equilibrium import SolveInfo, solve_static
from .model.fundamentals import TRAVEL_SCOPES, with_shocks
from .model.immigration import immigration_path
from .model.params import Params
from .synthetic import CountyData, synthetic_state

SYNTHETIC = "synthetic"
REGION_FORMAT = 1

SCENARIO_PARAMS = (
    "alpha", "beta", "lam", "kappa_lam", "mu", "theta_T", "lam_R", "nu", "eta",
    "price_rent_ratio", "epsilon", "varsigma", "land_income_in_choice", "lam_M_over_R",
)  # fmt: skip
DEFAULT_SHOCKS = {
    "core_productivity_pct": 10.0,
    "farm_tfp_pct": 0.0,
    "travel_cut_pct": 0.0,
    "travel_cut_scope": "into_core",
    "core_floor_supply_pct": 0.0,
    "core_amenity_pct": 0.0,
    "metro_travel_cut_pct": 0.0,
    "rural_amenity_pct": 0.0,
    "immigration_per_period": 0.0,
    "periods": 60,
}
MAX_PERIODS = 400
UNITS = {
    "N": "workers (persons)",
    "TF": "hectares",
    "immigration_per_period": "persons per period",
    "period": "years",  # VERIFY: migration costs are set for a ~3% annual gross county move rate
    "wages": "mean non-farm earnings = 1",
    "pct": "percent change from the baseline",
}


def default_scenario(region_doc: dict | None = None) -> dict:
    """The region's defaults: Params() for the synthetic state, Params() with the region's estimates
    on top for a region document."""
    p = Params(**_region_params(region_doc))
    region = region_doc["region"] if region_doc else SYNTHETIC
    return {"region": region, "params": {k: getattr(p, k) for k in SCENARIO_PARAMS}, "shocks": dict(DEFAULT_SHOCKS)}


# --- regions -------------------------------------------------------------------------------


def _region_params(doc) -> dict:
    return dict(doc["params"]) if doc else {}


def county_data(doc: dict) -> CountyData:
    """CountyData from a region document (shape in the module docstring)."""
    if doc.get("format") != REGION_FORMAT:
        raise ValueError(f"region document format must be {REGION_FORMAT}")
    c = doc["counties"]
    col = lambda k: np.asarray(c[k], dtype=float)  # noqa: E731
    kind = np.asarray(c["kind"], dtype=str)
    nest = np.asarray(c["nest"], int) if "nest" in c else None
    cores = {p for p, k in zip(c.get("parent", c["fips"]), kind) if k == "core"}
    if len(cores) != 1:
        raise ValueError("a region needs exactly one core county")
    return CountyData(
        names=list(c["name"]), kind=kind, x=col("x_km"), y=col("y_km"), N=col("N"), HU=col("HU"),
        HA=col("HA"), L=col("L"), TF=col("TF"), wA_obs=col("wA_obs"), mean_nonfarm_wage=1.0,
        omega=col("omega"), gateway=col("gateway"), dist=np.asarray(doc["dist_km"], float),
        t=np.asarray(doc["t_min"], float), nest=nest,
    )  # fmt: skip


def _region(scenario: dict, doc):
    region = scenario.get("region", SYNTHETIC)
    if region == SYNTHETIC:
        return synthetic_state(), None
    if not doc or doc.get("region") != region:
        raise ValueError(f"region {region!r} needs its region document")
    return county_data(doc), doc


# --- boundary parsing ----------------------------------------------------------------------


def _number(name, v):
    if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
        raise ValueError(f"{name} must be a finite number")
    return float(v)


def _parse(scenario: dict, doc=None):
    if set(scenario) - {"region", "params", "shocks"}:
        raise ValueError("scenario keys are 'region', 'params' and 'shocks'")
    raw_p = scenario.get("params") or {}
    raw_s = scenario.get("shocks") or {}
    unknown = (set(raw_p) - set(SCENARIO_PARAMS)) | (set(raw_s) - set(DEFAULT_SHOCKS))
    if unknown:
        raise ValueError("unknown scenario keys: " + ", ".join(sorted(unknown)))
    kw = {}
    for k, v in raw_p.items():
        if k == "land_income_in_choice":
            if not isinstance(v, bool):
                raise ValueError("land_income_in_choice must be true or false")
            kw[k] = v
        else:
            kw[k] = _number(k, v)
    p = Params(**{**_region_params(doc), **kw})
    s = dict(DEFAULT_SHOCKS, **raw_s)
    PCT = ("core_productivity_pct", "farm_tfp_pct", "travel_cut_pct", "core_floor_supply_pct", "core_amenity_pct",
           "metro_travel_cut_pct", "rural_amenity_pct")
    for k in (*PCT, "immigration_per_period"):
        s[k] = _number(k, s[k])
    if s["travel_cut_scope"] not in TRAVEL_SCOPES:
        raise ValueError(f"travel_cut_scope must be one of {TRAVEL_SCOPES}")
    for k in ("travel_cut_pct", "metro_travel_cut_pct"):
        if not 0.0 <= s[k] < 100.0:
            raise ValueError(f"{k} must be in [0, 100)")
    if any(s[k] <= -100.0 for k in ("core_productivity_pct", "farm_tfp_pct", "core_floor_supply_pct", "core_amenity_pct", "rural_amenity_pct")):
        raise ValueError("productivity, floor-supply and amenity shocks must be above -100%")
    if s["immigration_per_period"] < 0:
        raise ValueError("immigration_per_period must be >= 0")
    periods = s["periods"]
    if isinstance(periods, bool) or not isinstance(periods, (int, float)) or periods != int(periods):
        raise ValueError("periods must be an integer")
    if not 1 <= periods <= MAX_PERIODS:
        raise ValueError(f"periods must be in [1, {MAX_PERIODS}]")
    s["periods"] = int(periods)
    return p, s


# --- output helpers ------------------------------------------------------------------------


def _json(v):
    """numpy -> plain Python; non-finite floats -> None."""
    if isinstance(v, dict):
        return {k: _json(x) for k, x in v.items()}
    if isinstance(v, (list, tuple, np.ndarray)):
        return [_json(x) for x in v]
    if isinstance(v, (bool, np.bool_)):
        return bool(v)
    if isinstance(v, (int, np.integer)):
        return int(v)
    if isinstance(v, (float, np.floating)):
        v = float(v)
        return v if math.isfinite(v) else None
    return v


def _pct(new, old):
    """Percent change; NaN (null in JSON) where old is 0, e.g. farm values without a farm sector."""
    with np.errstate(divide="ignore", invalid="ignore"):
        return 100.0 * (np.asarray(new) / np.asarray(old) - 1.0)


def _merge(infos, method) -> dict:
    return SolveInfo(
        all(i.converged for i in infos),
        sum(i.iterations for i in infos),
        max(i.residual_inf for i in infos),
        method,
    ).as_dict()


# --- run -----------------------------------------------------------------------------------


def run(scenario: dict, region_doc: dict | None = None) -> dict:
    if not isinstance(scenario, dict):
        raise ValueError("scenario must be an object with 'params' and 'shocks'")
    data, doc = _region(scenario, region_doc)
    p, s = _parse(scenario, doc)
    R, core, T = data.rural, data.core_mask, s["periods"]  # core: the core county's zone(s)
    urban = ~R

    cal = calibrate(data, p)
    f0, base = cal.fundamentals, cal.baseline
    w0 = base.within
    f1 = with_shocks(
        f0,
        core=core,
        a_TH=p.a_TH,
        core_productivity_pct=s["core_productivity_pct"],
        farm_tfp_pct=s["farm_tfp_pct"],
        travel_cut_pct=s["travel_cut_pct"],
        travel_cut_scope=s["travel_cut_scope"],
        core_floor_supply_pct=s["core_floor_supply_pct"],
        core_amenity_pct=s["core_amenity_pct"],
        metro_travel_cut_pct=s["metro_travel_cut_pct"],
        rural_amenity_pct=s["rural_amenity_pct"],
        metro=np.isin(data.kind, ("core", "suburb")),
        rural=R,
    )
    imm = immigration_path(s["immigration_per_period"], T)

    # Long run (S): eta as given, N_bar = N_bar0 + sum I (spec §12.2).
    N_bar_lr = f0.N_bar0 + imm.sum()
    lr = solve_static(f1, p, N_bar_base=N_bar_lr, N0=base.N * N_bar_lr / f0.N_bar0, x0=w0.x)
    w1 = lr.within
    TF = f0.TF
    L0 = f0.L_bar * w0.r**p.mu
    totals = {
        "rural_residents_pct": _pct(lr.N[R].sum(), base.N[R].sum()),
        "land_per_farm_worker_pct": _pct(w0.HA[R].sum(), w1.HA[R].sum()),
        "farm_wage_pct": _pct((w1.wA * w0.HA)[R].sum(), (w0.wA * w0.HA)[R].sum()),
        "farmland_rent_pct": _pct((w1.rho * TF)[R].sum(), (w0.rho * TF)[R].sum()),
        "core_rent_pct": _pct(w1.r[core] @ L0[core], w0.r[core] @ L0[core]),  # floor-space weighted
        "region_pop_pct": _pct(lr.N_bar, base.N_bar),
    }

    # Path (§3.8): t = 0 baseline, shock from t = 1.
    stop = ConsolidationStop(R, p.epsilon, p.ss_tol)
    path = simulate(f0, f1, p, N0=base.N, x0=w0.x, immigration=imm, stop=stop)
    q = p.discount
    rho_t, r_t, wA_t = path.stack("rho"), path.stack("r"), path.stack("wA")
    P = np.vstack([w0.rho * land.gordon_multiple(q), land.present_values(rho_t[1:], q)])
    farmland_index = (P[:, R] @ TF[R]) / (P[0, R] @ TF[R])
    urban_index = (r_t[:, urban] @ L0[urban]) / (r_t[0, urban] @ L0[urban])

    # Wealth of a baseline rural farm operator at t = 1: owned land at its price plus the PV of
    # earnings, staying on the farm (rural farm wage) or leaving for the core (core mean income).
    acres = (f0.omega * TF)[R].sum() / w0.HA[R].sum()
    land_price = lambda P_row: (P_row[R] @ TF[R]) / TF[R].sum()  # noqa: E731
    farm_wage = (wA_t[1:, R] @ w0.HA[R]) / w0.HA[R].sum()
    Nc = path.N[1:, core]
    core_income = (path.stack("ybar")[1:, core] * Nc).sum(axis=1) / Nc.sum(axis=1)  # resident-weighted
    hold = np.ones(T)

    def wealth_pct(income, income0):
        new = land.household_wealth(acres, land_price(P[1]), income, q)
        old = land.household_wealth(acres, land_price(P[0]), income0 * hold, q)
        return _pct(new, old)

    # §4 is a first-order result, so it is checked at a small fixed shock, not the scenario's
    ANALYTIC_SHOCK_PCT = 1.0
    two = two_location_check(p, ANALYTIC_SHOCK_PCT)

    counties = [
        {
            "id": i, "name": data.names[i], "x": data.x[i], "y": data.y[i], "kind": data.kind[i],
            "N0": data.N[i], "HU0": data.HU[i], "HA0": data.HA[i], "TF": TF[i], "omega": f0.omega[i],
        }
        for i in range(f0.Z)
    ]  # fmt: skip
    out = {
        "units": UNITS,
        "scenario": {"params": {k: getattr(p, k) for k in SCENARIO_PARAMS}, "shocks": s},
        "counties": counties,
        "calibration": {
            "max_rel_error": cal.max_rel_error,
            "xi_A": f0.xi_A,
            "solve": _merge([cal.wage_info, cal.flow_info, base.info], "ARSW wages + flow offsets + static check"),
        },
        "long_run": {
            "N": lr.N,
            "dN_pct": _pct(lr.N, base.N),
            "wA_pct": _pct(w1.wA, w0.wA),
            "rho_pct": _pct(w1.rho, w0.rho),
            "r_pct": _pct(w1.r, w0.r),
            "HA_pct": _pct(w1.HA, w0.HA),
            "welfare_pct": 100.0 * math.expm1(lr.lnW - base.lnW),
            "totals": totals,
            "solve": lr.info.as_dict(),
        },
        "path": {
            "t": list(range(T + 1)),
            "N": path.N,
            "rural_share": path.N[:, R].sum(axis=1) / path.N.sum(axis=1),
            "land_per_worker_ratio": path.land_ratio,
            "target_ratio": stop.target_ratio,
            "farmland_price_index": farmland_index,
            "urban_rent_index": urban_index,
            "stop": {"period": path.stop_period, "reason": path.stop_reason},
            "all_converged": path.all_converged and cal.flow_info.converged,
            "worst_residual": path.worst_residual,
        },
        "wealth": {
            "stayer_pct": wealth_pct(farm_wage, (w0.wA[R] @ w0.HA[R]) / w0.HA[R].sum()),
            "leaver_pct": wealth_pct(core_income, w0.ybar[core] @ base.N[core] / base.N[core].sum()),
        },
        "analytic": {
            "s": two.s,
            "x_closed_form": two.x_closed_form,
            "x_solver": two.x_solver,
            "shock_pct": ANALYTIC_SHOCK_PCT,
            "converged": two.converged,
        },
    }
    if doc:
        out.update(_real_units(doc, data, base, lr, R))
    if doc and data.nest is not None:
        out = _county_view(out, doc, data, f0, base, lr, path)
    return _json(out)


def _county_view(out: dict, doc: dict, data, f0, base, lr, path) -> dict:
    """A region with a metro nest: the per-zone results move under "city" (its tracts only), and the
    usual per-county fields are replaced by sums over each county's zones (spec §3.12), so the state
    map reads them as before. Rates are weighted: farm wage by farm jobs, farmland rent by farmland,
    floor rent by baseline floor space, owner share by farmland."""
    c = doc["counties"]
    cv = doc["county_view"]
    units = list(cv["fips"])
    idx = {u: k for k, u in enumerate(units)}
    member = np.array([idx[pf] for pf in c["parent"]])
    M = np.zeros((len(units), data.N.size))
    M[member, np.arange(data.N.size)] = 1.0
    w0, w1 = base.within, lr.within
    TF = f0.TF

    def wmean(v, wt):
        with np.errstate(divide="ignore", invalid="ignore"):
            return (M @ (v * wt)) / (M @ wt)

    L0 = data.L  # baseline floor space (observed; equals L_bar r0^mu at the calibrated baseline)
    inside = data.nest >= 0
    zone_lr = out["long_run"]
    city = {
        "zones": [z | {"parent": c["parent"][i], "county_index": int(member[i])} for i, z in enumerate(out["counties"]) if inside[i]],
        "long_run": {k: np.asarray(zone_lr[k])[inside] for k in ("N", "dN_pct", "wA_pct", "rho_pct", "r_pct", "HA_pct")},
        "path": {"N": np.asarray(path.N)[:, inside]},
        "real": {k: np.asarray(v)[inside] for k, v in out["real"].items()} if "real" in out else {},
    }
    N0, N1 = M @ base.N, M @ lr.N
    HA0, HA1 = M @ w0.HA, M @ w1.HA
    wA0, wA1 = wmean(w0.wA, w0.HA), wmean(w1.wA, w0.HA)
    rho0, rho1 = wmean(w0.rho, TF), wmean(w1.rho, TF)
    r0, r1 = wmean(w0.r, L0), wmean(w1.r, L0)
    out["counties"] = [
        {"id": k, "name": cv["name"][k], "x": cv["x_km"][k], "y": cv["y_km"][k], "kind": cv["kind"][k],
         "N0": float((M @ data.N)[k]), "HU0": float((M @ data.HU)[k]), "HA0": float((M @ data.HA)[k]),
         "TF": float((M @ TF)[k]), "omega": float(wmean(f0.omega, TF)[k]) if (M @ TF)[k] > 0 else float(f0.omega[member == k][0]),
         "tracts": int((inside & (member == k)).sum())}
        for k in range(len(units))
    ]  # fmt: skip
    out["long_run"] |= {"N": N1, "dN_pct": _pct(N1, N0), "HA_pct": _pct(HA1, HA0), "wA_pct": _pct(wA1, wA0),
                        "rho_pct": _pct(rho1, rho0), "r_pct": _pct(r1, r0)}  # fmt: skip
    out["path"]["N"] = np.asarray(path.N) @ M.T
    if "real" in out:
        usd, acre = doc["usd_per_wage_unit"], land.HA_PER_ACRE
        out["real"] = {"fips": units, "TF_acres": (M @ TF) / acre, "rent0_usd_acre": rho0 * usd * acre,
                       "rent_usd_acre": rho1 * usd * acre, "wA0_usd": wA0 * usd, "wA_usd": wA1 * usd}  # fmt: skip
    out["city"] = city
    return out


def _real_units(doc, data, base, lr, R) -> dict:
    """Levels in real-world units for a real region: persons, acres, dollars. Region totals use
    every zone (the external zone included); rural totals use rural counties only."""
    usd, acre = doc["usd_per_wage_unit"], land.HA_PER_ACRE
    w0, w1, TF, HA0 = base.within, lr.within, data.TF, base.within.HA
    rent_acre = lambda w: w.rho * usd * acre  # noqa: E731

    def levels(f):
        return [f(base, w0), f(lr, w1)]

    region = {
        "id": doc["region"], "label": doc["label"], "core_label": doc["core_label"], "usd_per_wage_unit": usd,
        "units": {"rent_usd_acre": "US$ per acre per year, model farmland rent", "wA_usd": "US$ per farm worker per year",
                  "TF_acres": "acres", "levels": "[baseline, long run]"},
    }  # fmt: skip
    return {
        "region": region,
        "levels": {
            "rural_residents": levels(lambda e, w: e.N[R].sum()),
            "region_residents": levels(lambda e, w: e.N_bar),
            "land_per_farm_worker_acres": levels(lambda e, w: TF[R].sum() / w.HA[R].sum() / acre),
            "farm_wage_usd": levels(lambda e, w: (w.wA * HA0)[R].sum() / HA0[R].sum() * usd),
            "farmland_rent_usd_acre": levels(lambda e, w: (rent_acre(w) * TF)[R].sum() / TF[R].sum()),
        },
        "real": {
            "fips": doc["counties"]["fips"],
            "TF_acres": TF / acre,
            "rent0_usd_acre": rent_acre(w0),
            "rent_usd_acre": rent_acre(w1),
            "wA0_usd": w0.wA * usd,
            "wA_usd": w1.wA * usd,
        },
    }

