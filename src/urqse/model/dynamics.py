"""Dynamic path (spec §3.8) with myopic logit flows, immigration (§12.2) and the
consolidation stop rule (§12.1 decision 1)."""

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


def flow_matrix(lnu, delta, tau, nu):
    """mu_{in}: share of residents of i who live in n next period (rows sum to 1)."""
    z = (lnu + delta)[None, :] - tau
    z = (z - z.max(axis=1, keepdims=True)) / nu
    e = np.exp(z)
    return e / e.sum(axis=1, keepdims=True)


def _balance_newton(N, logK, u, *, tol, max_iter=100):
    """Minimise the convex f(u) = sum_i N_i lse_n(logK_in + u_n) - N.u, whose gradient is
    mu'N - N: Newton with Armijo backtracking, globally convergent."""
    w = N / N.sum()

    def f_mu(u):
        z = logK + u[None, :]
        c = z.max(axis=1, keepdims=True)
        e = np.exp(z - c)
        s = e.sum(axis=1, keepdims=True)
        return float(w @ (np.log(s[:, 0]) + c[:, 0]) - w @ u), e / s

    f, mu = f_mu(u)
    rn = np.inf
    for k in range(max_iter + 1):
        inflow = mu.T @ w
        rn = float(np.max(np.abs(np.log(w) - np.log(inflow))))
        if rn <= tol:
            return u, SolveInfo(True, k, rn, "flow offsets newton (line search)")
        if k == max_iter or not np.isfinite(rn):
            break
        grad = inflow - w
        H = np.diag(inflow) - mu.T @ (w[:, None] * mu) + 1.0 / N.size  # ones/Z fixes the level mode
        d = np.linalg.solve(H, -grad)
        d -= d.mean()
        gnorm = float(np.max(np.abs(grad)))
        step = 1.0
        while True:
            f_new, mu_new = f_mu(u + step * d)
            armijo = f_new <= f + 1e-4 * step * (grad @ d)
            # Near the optimum f changes below float precision; then accept a step that lowers |grad|.
            flat = abs(f_new - f) <= 1e-13 * max(1.0, abs(f))
            if armijo or (flat and np.max(np.abs(mu_new.T @ w - w)) < gnorm) or step < 1e-12:
                break
            step *= 0.5
        u, f, mu = u + step * d, f_new, mu_new
    return u, SolveInfo(False, max_iter, rn, "flow offsets newton (line search)")


def calibrate_flow_offsets(N, lnu, tau, nu, *, tol=TOL_INNER):
    """delta such that N = mu(delta)' N (§5 step 8), in u = (ln u + delta)/nu with mean u = 0.
    The steady state is Sinkhorn balancing with both marginals N: Sinkhorn sweeps
    u <- ln N - ln(K'(N / K e^u)) with Anderson, and a convex Newton fallback if that stalls."""
    K = np.exp(-tau / nu)

    def sweep(u):
        G = np.log(N) - np.log(K.T @ (N / (K @ np.exp(u))))
        G -= G.mean()
        return G, G - u

    u, info = anderson(sweep, np.zeros(N.size), tol=tol, max_iter=300, method="flow offsets anderson(m=6)")
    if not info.converged:
        u, info = _balance_newton(N, -tau / nu, np.zeros(N.size), tol=tol)
    delta = nu * u - lnu
    return delta - delta.mean(), info


@dataclass(frozen=True)
class ConsolidationStop:
    """Stop at the first t >= 1 with sum_R TF / sum_R HA_t >= (1+epsilon) x baseline,
    else at the first t >= 1 whose flows leave N unchanged (steady state), else at the horizon."""

    rural: np.ndarray
    epsilon: float
    ss_tol: float

    @property
    def target_ratio(self) -> float:
        return 1.0 + self.epsilon

    def land_per_worker_ratio(self, TF, HA_path):
        with np.errstate(invalid="ignore"):  # NaN when the state has no rural county (New Jersey, Rhode Island)
            per_worker = TF[self.rural].sum() / HA_path[:, self.rural].sum(axis=1)
        return per_worker / per_worker[0]

    def evaluate(self, land_ratio, next_change):
        """land_ratio, next_change: arrays over t = 0..T. next_change[t] = max |ln N_{t+1} - ln N_t|."""
        T = land_ratio.size - 1
        hit = np.nonzero(land_ratio[1:] >= self.target_ratio)[0]
        if hit.size:
            return int(hit[0]) + 1, "consolidation"
        steady = np.nonzero(next_change[1:] < self.ss_tol)[0]
        if steady.size:
            return int(steady[0]) + 1, "steady_state"
        return T, "horizon"


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
    land_ratio: np.ndarray
    stop_period: int
    stop_reason: str
    all_converged: bool
    worst_residual: float

    def stack(self, name):
        return np.array([getattr(w, name) for w in self.within])


def simulate(
    f_base: Fundamentals,
    f_shock: Fundamentals,
    p: Params,
    *,
    N0,
    x0,
    immigration: np.ndarray,
    stop: ConsolidationStop,
) -> Path:
    """t = 0 is the baseline period (pre-shock fundamentals). The shock holds from t = 1 on.
    N_{t+1} = mu_t' N_t + I_t x arrival shares + domestic inflow (only when eta > 0)."""
    T = immigration.size
    N = np.asarray(N0, float).copy()
    x = np.asarray(x0, float)
    N_path, within, change = [], [], []
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
        N_next = flow_matrix(lnu_U, f.delta, f.tau, p.nu).T @ N_U
        I_t = immigration[min(t, T - 1)] if T else 0.0  # t = T only feeds the steady-state check
        if I_t > 0:
            # VERIFY: arrivals choose a residence unit by the flow logit (§12.2), not scaled by its
            # size, so they over-weight small units; a metro nest counts as one unit.
            N_next = N_next + I_t * arrival_shares(lnu_U, f.delta, A @ f.gateway, p.nu)
        if p.eta > 0:
            # VERIFY: semi-closed inflow N_bar_{t+1} = N_bar_t (N_bar*_t / N_bar_t)^phi (§3.8), with the
            # target (S) scaled by cumulative immigration. Inflows arrive by the residence logit
            # without gateway weights; outflows leave in proportion to residents.
            N_bar = N.sum()
            target = (f.N_bar0 + cum_I) * np.exp(p.eta * (blocks.log_welfare(w.lnu, p.lam_R, f.nest, p.lam_M) - lnU_bar))
            dom = N_bar * ((target / N_bar) ** p.phi - 1.0)
            if dom >= 0:
                N_next = N_next + dom * arrival_shares(lnu_U, f.delta, np.ones(N_U.size), p.nu)
            else:
                N_next = N_next * (1.0 + dom / N_next.sum())
        cum_I += I_t
        change.append(float(np.max(np.abs(np.log(N_next) - np.log(N_U)))))
        N = N * (N_next / N_U)[unit]  # a nest's zones keep their shares until next period's re-sorting
    HA = np.array([w.HA for w in within])
    ratio = stop.land_per_worker_ratio(f_base.TF, HA)
    period, reason = stop.evaluate(ratio, np.array(change))
    infos: list[SolveInfo] = [w.info for w in within]
    return Path(
        N=np.array(N_path),
        within=within,
        land_ratio=ratio,
        stop_period=period,
        stop_reason=reason,
        all_converged=all(i.converged for i in infos),
        worst_residual=max(i.residual_inf for i in infos),
    )
