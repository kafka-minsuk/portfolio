"""Dynamic path (spec §3.8): residents meet homes in other residence units and move to better ones,
so the path ends where utility matches across regions, the long run (S). Immigration (§12.2)."""

from dataclasses import dataclass

import numpy as np

from . import blocks
from .equilibrium import TOL_INNER, TOL_OUTER, SolveInfo, Within, anderson, solve_within
from .fundamentals import Fundamentals
from .immigration import arrival_shares
from .params import Params


def migration_cost(dist_km, p: Params):
    """tau_in = tau0 + tau1 ln d_in, tau_ii = 0."""
    off = ~np.eye(dist_km.shape[0], dtype=bool)
    tau = np.zeros_like(dist_km, dtype=float)
    tau[off] = p.tau0 + p.tau1 * np.log(dist_km[off])
    return tau


def unit_aggregation(nest, N):
    """(U, Z) weights that average a zone quantity over each residence unit by residents N
    (identity without a nest), and the unit of each zone (spec §3.12)."""
    unit, U, _ = blocks.outer_units(nest, N.size)
    A = np.zeros((U, N.size))
    A[unit, np.arange(N.size)] = N
    return A / A.sum(axis=1, keepdims=True), unit


def unit_distances(dist_km, nest, N):
    """Distance between residence units: zone distances, resident-weighted inside a nest.
    # VERIFY: a placeholder for migration costs into and out of a metro nest."""
    A, _ = unit_aggregation(nest, N)
    return A @ dist_km @ A.T


def flow_matrix(lnu, tau, lam_R):
    """mu_in: share of residents of unit i who live in n next period (rows sum to 1). A resident of i
    meets a home in n at the symmetric rate exp(-tau_in) and takes it if it is better, a binary logit
    at lam_R. Detailed balance holds where N_n is proportional to u_n^lam_R, so the steady state is
    the long run (S): tau sets how fast people move, never where they end up."""
    meet = np.exp(-tau)
    np.fill_diagonal(meet, 0.0)
    meet /= max(1.0, float(meet.sum(axis=1).max()))  # keep every stay share >= 0
    gain = lam_R * (lnu[None, :] - lnu[:, None])
    mu = meet * 0.5 * (1.0 + np.tanh(gain / 2.0))  # = meet / (1 + exp(-gain)), without overflow
    np.fill_diagonal(mu, 1.0 - mu.sum(axis=1))
    return mu


def utility_gap(lnu, N, lam_R) -> float:
    """How far residents are from the long run (S), in log utility: the spread across residence units
    of ln u_n - ln N_n / lam_R, which (S) makes equal everywhere. 0.001 is 0.1% of utility."""
    g = lnu - np.log(N) / lam_R
    return float(g.max() - g.min())


def solve_period(f: Fundamentals, p: Params, N, x, *, tol=TOL_INNER):
    """The within-period block given residents N. With a metro nest, the nest's residents first
    re-sort across its zones by (S') at the nest's total (spec §3.12: moving inside a metro is
    instant, moving between residence units follows the flows). Returns (Within, N)."""
    N = np.asarray(N, float)
    if f.nest is None or not np.any(np.asarray(f.nest) >= 0):
        return solve_within(f, p, N, x, tol=tol), N
    nest = np.asarray(f.nest)
    inside = nest >= 0
    unit, _, _ = blocks.outer_units(nest, N.size)
    lnN_unit = np.log(np.bincount(unit, weights=N))[unit[inside]]
    psi = float(np.mean(blocks.congestion_elasticities(p)))
    warm = {"x": np.asarray(x, float)}

    def with_inside(y):
        Nz = N.copy()
        Nz[inside] = np.exp(y)
        return Nz

    def step(y):
        w = solve_within(f, p, with_inside(y), warm["x"], tol=tol)
        if not w.info.converged:
            return np.full_like(y, np.nan), np.full_like(y, np.nan)
        warm["x"] = w.x
        lnu_U = blocks.unit_log_values(w.lnu, nest, p.lam_M)
        y_new = lnN_unit + p.lam_M * (w.lnu[inside] - lnu_U[unit[inside]])
        res = y_new - y
        return y + res / (1.0 + p.lam_M * psi), res

    y, info = anderson(step, np.log(N[inside]), tol=TOL_OUTER, max_iter=300, method="nest sorting anderson(m=6)")
    Nz = with_inside(y)
    w = solve_within(f, p, Nz, warm["x"], tol=tol)
    ok = info.converged and w.info.converged
    sort_info = SolveInfo(ok, info.iterations + w.info.iterations, max(info.residual_inf, w.info.residual_inf), info.method)
    return Within(**{**w.__dict__, "info": sort_info}), Nz


@dataclass(frozen=True)
class Path:
    N: np.ndarray  # (T+1, Z)
    within: list  # Within per period
    land_ratio: np.ndarray  # rural farmland per farm worker / baseline, per period
    utility_gap: np.ndarray  # utility_gap per period
    stop_period: int
    stop_reason: str  # "utility_matched" or "horizon"
    all_converged: bool
    worst_residual: float

    def stack(self, name):
        return np.array([getattr(w, name) for w in self.within])


def land_per_worker_ratio(TF, HA_path, rural):
    with np.errstate(invalid="ignore"):  # NaN when the state has no rural county (New Jersey, Rhode Island)
        per_worker = TF[rural].sum() / HA_path[:, rural].sum(axis=1)
    return per_worker / per_worker[0]


def simulate(f_base: Fundamentals, f_shock: Fundamentals, p: Params, *, N0, x0, immigration: np.ndarray, rural) -> Path:
    """t = 0 is the baseline period (pre-shock fundamentals). The shock holds from t = 1 on.
    N_{t+1} = mu_t' N_t + I_t x arrival shares + domestic inflow (only when eta > 0).
    Stops at the first t >= 1 whose utility gap is below p.gap_tol, else at the horizon. Once utility
    matches and no more immigrants arrive nothing changes, so the path ends there (fewer rows)."""
    T = immigration.size
    N = np.asarray(N0, float).copy()
    x = np.asarray(x0, float)
    N_path, within, gaps = [], [], []
    cum_I = 0.0
    lnU_bar = np.log(f_base.U_bar)
    for t in range(T + 1):
        f = f_base if t == 0 else f_shock
        w, N = solve_period(f, p, N, x)
        x = w.x
        N_path.append(N)
        within.append(w)
        # Flows and arrivals move people between residence units (zones, or a whole metro nest).
        A, unit = unit_aggregation(f.nest, N)
        N_U = np.bincount(unit, weights=N)
        lnu_U = blocks.unit_log_values(w.lnu, f.nest, p.lam_M)
        gap = utility_gap(lnu_U, N_U, p.lam_R)
        if p.eta > 0:
            # VERIFY: semi-closed inflow N_bar_{t+1} = N_bar_t (N_bar*_t / N_bar_t)^phi (§3.8), with the
            # target (S) scaled by cumulative immigration. Inflows arrive by the residence logit;
            # outflows leave in proportion to residents.
            lnW = blocks.log_welfare(w.lnu, p.lam_R, f.nest, p.lam_M)
            gap = max(gap, abs(lnW - lnU_bar - np.log(N.sum() / (f.N_bar0 + cum_I)) / p.eta))  # vs the outside
        gaps.append(gap)
        if t == T or (t >= 1 and gap < p.gap_tol and not immigration[t:].any()):
            break
        N_next = flow_matrix(lnu_U, f.tau, p.lam_R).T @ N_U
        I_t = immigration[t]
        if I_t > 0:
            N_next = N_next + I_t * arrival_shares(lnu_U, p.lam_R, A @ f.gateway)
        if p.eta > 0:
            N_bar = N.sum()
            target = (f.N_bar0 + cum_I) * np.exp(p.eta * (lnW - lnU_bar))
            dom = N_bar * ((target / N_bar) ** p.phi - 1.0)
            if dom >= 0:
                N_next = N_next + dom * arrival_shares(lnu_U, p.lam_R, np.ones(N_U.size))
            else:
                N_next = N_next * (1.0 + dom / N_next.sum())
        cum_I += I_t
        N = N * (N_next / N_U)[unit]  # a nest's zones keep their shares until next period's re-sorting
    gaps = np.array(gaps)
    hit = np.nonzero(gaps[1:] < p.gap_tol)[0]
    period, reason = (int(hit[0]) + 1, "utility_matched") if hit.size else (T, "horizon")
    infos: list[SolveInfo] = [w.info for w in within]
    return Path(
        N=np.array(N_path),
        within=within,
        land_ratio=land_per_worker_ratio(f_base.TF, np.array([w.HA for w in within]), rural),
        utility_gap=gaps,
        stop_period=period,
        stop_reason=reason,
        all_converged=all(i.converged for i in infos),
        worst_residual=max(i.residual_inf for i in infos),
    )
