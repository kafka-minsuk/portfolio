"""The browser boundary: JSON-shaped dict in, JSON-shaped dict out. Nothing else is called from JS."""

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
from .synthetic import synthetic_state

SCENARIO_PARAMS = (
    "alpha", "beta", "lam", "kappa_lam", "mu", "theta_T", "lam_R", "nu", "eta",
    "price_rent_ratio", "epsilon", "varsigma", "land_income_in_choice",
)  # fmt: skip
DEFAULT_SHOCKS = {
    "core_productivity_pct": 10.0,
    "farm_tfp_pct": 0.0,
    "travel_cut_pct": 0.0,
    "travel_cut_scope": "into_core",
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


def default_scenario() -> dict:
    p = Params()
    return {"params": {k: getattr(p, k) for k in SCENARIO_PARAMS}, "shocks": dict(DEFAULT_SHOCKS)}


# --- boundary parsing ----------------------------------------------------------------------


def _number(name, v):
    if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
        raise ValueError(f"{name} must be a finite number")
    return float(v)


def _parse(scenario: dict):
    if not isinstance(scenario, dict):
        raise ValueError("scenario must be an object with 'params' and 'shocks'")
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
    p = Params(**kw)
    s = dict(DEFAULT_SHOCKS, **raw_s)
    for k in ("core_productivity_pct", "farm_tfp_pct", "travel_cut_pct", "immigration_per_period"):
        s[k] = _number(k, s[k])
    if s["travel_cut_scope"] not in TRAVEL_SCOPES:
        raise ValueError(f"travel_cut_scope must be one of {TRAVEL_SCOPES}")
    if not 0.0 <= s["travel_cut_pct"] < 100.0:
        raise ValueError("travel_cut_pct must be in [0, 100)")
    if s["core_productivity_pct"] <= -100.0 or s["farm_tfp_pct"] <= -100.0:
        raise ValueError("productivity shocks must be above -100%")
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
    return 100.0 * (np.asarray(new) / np.asarray(old) - 1.0)


def _merge(infos, method) -> dict:
    return SolveInfo(
        all(i.converged for i in infos),
        sum(i.iterations for i in infos),
        max(i.residual_inf for i in infos),
        method,
    ).as_dict()


# --- run -----------------------------------------------------------------------------------


def run(scenario: dict) -> dict:
    p, s = _parse(scenario)
    data = synthetic_state()
    R, core, T = data.rural, data.core, s["periods"]
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
    )
    imm = immigration_path(s["immigration_per_period"], T)

    # Long run (S): eta as given, N_bar = N_bar0 + sum I (spec §12.2).
    N_bar_lr = f0.N_bar0 + imm.sum()
    lr = solve_static(f1, p, N_bar_base=N_bar_lr, N0=base.N * N_bar_lr / f0.N_bar0, x0=w0.x)
    w1 = lr.within
    TF = f0.TF
    totals = {
        "rural_residents_pct": _pct(lr.N[R].sum(), base.N[R].sum()),
        "land_per_farm_worker_pct": _pct(w0.HA[R].sum(), w1.HA[R].sum()),
        "farm_wage_pct": _pct((w1.wA * w0.HA)[R].sum(), (w0.wA * w0.HA)[R].sum()),
        "farmland_rent_pct": _pct((w1.rho * TF)[R].sum(), (w0.rho * TF)[R].sum()),
        "core_rent_pct": _pct(w1.r[core], w0.r[core]),
        "region_pop_pct": _pct(lr.N_bar, base.N_bar),
    }

    # Path (§3.8): t = 0 baseline, shock from t = 1.
    stop = ConsolidationStop(R, p.epsilon, p.ss_tol)
    path = simulate(f0, f1, p, N0=base.N, x0=w0.x, immigration=imm, stop=stop)
    q = p.discount
    rho_t, r_t, wA_t = path.stack("rho"), path.stack("r"), path.stack("wA")
    P = np.vstack([w0.rho * land.gordon_multiple(q), land.present_values(rho_t[1:], q)])
    farmland_index = (P[:, R] @ TF[R]) / (P[0, R] @ TF[R])
    L0 = f0.L_bar * w0.r**p.mu
    urban_index = (r_t[:, urban] @ L0[urban]) / (r_t[0, urban] @ L0[urban])

    # Wealth of a baseline rural farm operator at t = 1: owned land at its price plus the PV of
    # earnings, staying on the farm (rural farm wage) or leaving for the core (core mean income).
    acres = (f0.omega * TF)[R].sum() / w0.HA[R].sum()
    land_price = lambda P_row: (P_row[R] @ TF[R]) / TF[R].sum()  # noqa: E731
    farm_wage = (wA_t[1:, R] @ w0.HA[R]) / w0.HA[R].sum()
    core_income = path.stack("ybar")[1:, core]
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
            "leaver_pct": wealth_pct(core_income, w0.ybar[core]),
        },
        "analytic": {
            "s": two.s,
            "x_closed_form": two.x_closed_form,
            "x_solver": two.x_solver,
            "shock_pct": ANALYTIC_SHOCK_PCT,
            "converged": two.converged,
        },
    }
    return _json(out)

