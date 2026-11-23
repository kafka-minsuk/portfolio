"""Equilibrium solvers (spec §3.7, §6.2): a within-period fixed point in x = (ln r, ln wA) given N,
and an outer fixed point in ln N, both by damped iteration plus safeguarded Anderson."""

from dataclasses import asdict, dataclass

import numpy as np

from . import blocks, land
from .fundamentals import Fundamentals
from .params import Params

TOL_INNER = 1e-11
TOL_OUTER = 1e-10


@dataclass(frozen=True)
class SolveInfo:
    converged: bool
    iterations: int
    residual_inf: float
    method: str

    def as_dict(self) -> dict:
        return asdict(self)


def anderson(step, x0, *, tol, max_iter=500, m=6, damping=1.0, method="anderson"):
    """Safeguarded Anderson acceleration (type II, Walker & Ni 2011).

    step(x) -> (g, res): g is the (possibly preconditioned) fixed-point map, res = G(x) - x
    is the residual of the undamped map that the stop test reads. History is cleared whenever
    the residual grows, and an extrapolation that leaves the finite domain is replaced by a
    plain damped step from the last finite iterate."""

    def finite(g, res):
        return bool(np.all(np.isfinite(g)) and np.all(np.isfinite(res)))

    with np.errstate(all="ignore"):
        x = np.array(x0, dtype=float)
        g, res = step(x)
        if not finite(g, res):
            return x, SolveInfo(False, 0, float("nan"), method)
        xs, fs = [], []
        prev = np.inf
        for k in range(max_iter):
            rn = float(np.max(np.abs(res)))
            if rn <= tol:
                return x, SolveInfo(True, k, rn, method)
            if rn > prev:
                xs, fs = [], []
            prev = rn
            f = g - x
            xs.append(x)
            fs.append(f)
            if len(xs) > m + 1:
                xs.pop(0)
                fs.pop(0)
            x_new = x + damping * f
            if len(xs) > 1:
                dX = np.diff(np.array(xs), axis=0).T
                dF = np.diff(np.array(fs), axis=0).T
                gamma = np.linalg.lstsq(dF, f, rcond=None)[0]
                x_new = x_new - (dX + damping * dF) @ gamma
            g_new, res_new = step(x_new)
            if not finite(g_new, res_new):
                xs, fs = [], []
                x_new = x + damping * f
                g_new, res_new = step(x_new)
                if not finite(g_new, res_new):
                    return x, SolveInfo(False, k + 1, float("nan"), method)
            x, g, res = x_new, g_new, res_new
        rn = float(np.max(np.abs(res)))
        return x, SolveInfo(rn <= tol, max_iter, rn, method)


# --- within period (given N) -------------------------------------------------------------


@dataclass(frozen=True)
class Within:
    x: np.ndarray
    wU: np.ndarray
    wA: np.ndarray
    r: np.ndarray
    rho: np.ndarray
    HU: np.ndarray
    HA: np.ndarray
    ybar: np.ndarray  # expected wage income of a resident
    Y: np.ndarray  # wage + land income received by a resident
    lnPhi: np.ndarray
    lnu: np.ndarray
    info: SolveInfo


def commuting_kernels(f: Fundamentals, p: Params):
    D = np.exp(-p.kappa_lam * f.t)
    return D, D * D


def _evaluate(f, p, D, N, x):
    Z = f.Z
    r, wA = np.exp(x[:Z]), np.exp(x[Z:])
    wU = blocks.nonfarm_wage(f.B, r, p)
    ln_wtA = x[Z:] + np.log(f.xi_A) + land.choice_wage_markup(f.omega, p)
    ch = blocks.choice(D, np.log(wU), ln_wtA, N, p.lam)
    rho = blocks.farm_rent(wA, ch.HA, f.TF, p)
    ybar = ch.resident_mean(wU, wA)
    Y = (
        ybar
        + ch.resident_mean(0.0, land.operator_land_income_per_worker(wA, f.omega, p))
        + land.local_landlord_rebate(rho, f.TF, f.omega, N, p.varsigma)
    )
    E = blocks.floor_spending(Y, N, wU, ch.HU, p)
    return ch, wU, wA, r, rho, ybar, Y, E


def _within_step(f, p, D, D2, N):
    Z = f.Z
    log_wA_const = np.log(p.theta_H * f.A_farm) + p.theta_T * np.log(f.TF)

    def step(x):
        ch, wU, wA, r, rho, ybar, Y, E = _evaluate(f, p, D, N, x)
        G = np.concatenate([np.log(blocks.floor_rent(E, f.L_bar, p)), log_wA_const - p.theta_T * np.log(ch.HA)])
        res = G - x
        # Diagonal preconditioner from the own-derivatives of G (same fixed points as G).
        sU, sA = ch.own_shares(D2, N)
        com_share = p.k_com * wU * ch.HU / E
        e_r = -com_share * p.k_com * (1.0 + p.lam * (1.0 - sU)) / (1.0 + p.mu)
        e_A = -p.theta_T * p.lam * (1.0 - sA)
        return x + res / (1.0 - np.concatenate([e_r, e_A])), res

    return step


def within_from_x(f: Fundamentals, p: Params, N, x, info: SolveInfo) -> Within:
    D, _ = commuting_kernels(f, p)
    ch, wU, wA, r, rho, ybar, Y, _ = _evaluate(f, p, D, N, x)
    lnu = blocks.expected_log_utility(f.A, r, ch.lnPhi, p)
    return Within(x, wU, wA, r, rho, ch.HU, ch.HA, ybar, Y, ch.lnPhi, lnu, info)


def solve_within(f: Fundamentals, p: Params, N, x0, *, tol=TOL_INNER, max_iter=500) -> Within:
    D, D2 = commuting_kernels(f, p)
    x, info = anderson(_within_step(f, p, D, D2, N), x0, tol=tol, max_iter=max_iter, method="inner anderson(m=6)")
    return within_from_x(f, p, N, x, info)


def seed_x(f: Fundamentals, p: Params, N) -> np.ndarray:
    """Positive seed: r = 1, wA = theta_H A_farm (TF / (0.1 N))^theta_T."""
    wA = blocks.farm_wage(f.A_farm, f.TF, 0.1 * N, p)
    return np.concatenate([np.zeros(f.Z), np.log(wA)])


# --- long run (residence + semi-closure) -------------------------------------------------


@dataclass(frozen=True)
class Equilibrium:
    N: np.ndarray
    within: Within
    lnW: float
    N_bar: float
    info: SolveInfo


def solve_static(
    f: Fundamentals,
    p: Params,
    *,
    N_bar_base: float | None = None,
    N0=None,
    x0=None,
    tol=TOL_OUTER,
    tol_inner=None,
    max_iter=300,
) -> Equilibrium:
    """Solve (L), (Z), (F), (R), (S). The region holds N_bar_base (default N_bar0) residents
    times (W/U_bar)^eta. The outer residual carries eta times the inner error, so the inner
    tolerance tightens with eta."""
    tol_inner = TOL_INNER / max(1.0, p.eta) if tol_inner is None else tol_inner
    N_bar_base = f.N_bar0 if N_bar_base is None else N_bar_base
    N0 = np.full(f.Z, N_bar_base / f.Z) if N0 is None else np.asarray(N0, float)
    warm = {"x": seed_x(f, p, N0) if x0 is None else np.asarray(x0, float)}
    psi = float(np.mean(blocks.congestion_elasticities(p)))
    pre_dev, pre_level = 1.0 + p.lam_R * psi, 1.0 + p.eta * psi
    lnU_bar = np.log(f.U_bar)

    def step(y):
        w = solve_within(f, p, np.exp(y), warm["x"], tol=tol_inner)
        if not w.info.converged:
            return np.full_like(y, np.nan), np.full_like(y, np.nan)
        warm["x"] = w.x
        lnW = blocks.log_welfare(w.lnu, p.lam_R)
        y_new = np.log(N_bar_base) + p.eta * (lnW - lnU_bar) + blocks.residence_log_shares(w.lnu, p.lam_R)
        res = y_new - y
        level = res.mean()
        return y + (res - level) / pre_dev + level / pre_level, res

    y, info = anderson(step, np.log(N0), tol=tol, max_iter=max_iter, method="outer anderson(m=6), inner warm-started")
    N = np.exp(y)
    w = solve_within(f, p, N, warm["x"], tol=tol_inner)
    lnW = blocks.log_welfare(w.lnu, p.lam_R)
    converged = info.converged and w.info.converged
    info = SolveInfo(converged, info.iterations, max(info.residual_inf, w.info.residual_inf), info.method)
    return Equilibrium(N, w, lnW, float(N.sum()), info)
