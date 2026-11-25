"""Exact model inversion (spec §5 steps 1-7)."""

from dataclasses import dataclass

import numpy as np

from ..model import blocks, land
from ..model.dynamics import migration_cost, unit_distances
from ..model.equilibrium import Equilibrium, SolveInfo, anderson, solve_static
from ..model.fundamentals import Fundamentals
from ..model.params import Params
from ..synthetic import CountyData


@dataclass(frozen=True)
class Calibration:
    fundamentals: Fundamentals
    baseline: Equilibrium
    max_rel_error: dict
    wage_info: SolveInfo


def effective_wages(D, N, HU, HA, lam, *, tol=1e-13):
    """Step 1: ln w-tilde such that the choice block reproduces (HU, HA); geometric mean of
    non-farm wages = 1 (ARSW contraction, accelerated). Where HA = 0 there is no farm sector
    (§3.11): its entry stays 0 and is not a choice."""
    Z = N.size
    farm = HA > 0
    active = np.concatenate([np.ones(Z, bool), farm])
    lnH = np.log(np.where(active, np.concatenate([HU, HA]), 1.0))

    def step(z):
        ch = blocks.choice(D, z[:Z], z[Z:], N, lam, farm)
        H = np.where(active, np.concatenate([ch.HU, ch.HA]), 1.0)
        g = z + np.where(active, lnH - np.log(H), 0.0) / lam
        g -= g[:Z].mean()
        g[Z:] = np.where(farm, g[Z:], 0.0)
        return g, g - z

    return anderson(step, np.zeros(2 * Z), tol=tol, max_iter=5000, method="ARSW contraction anderson(m=6)")


def calibrate(data: CountyData, p: Params) -> Calibration:
    N, HU, HA, TF, omega = data.N, data.HU, data.HA, data.TF, data.omega
    if not np.isclose(N.sum(), HU.sum() + HA.sum(), rtol=1e-12):
        raise ValueError("jobs must equal resident workers (add an external zone, spec §5)")
    Z = N.size
    D = np.exp(-p.kappa_lam * data.t)

    # 1. effective wages, rescaled so job-weighted mean non-farm earnings match the data.
    z, wage_info = effective_wages(D, N, HU, HA, p.lam)
    scale = np.log(data.mean_nonfarm_wage) - np.log(np.sum(HU * np.exp(z[:Z])) / HU.sum())
    z = z + scale
    wU = np.exp(z[:Z])
    farm = HA > 0  # §3.11: no farm sector where there are no farm jobs
    if np.any(farm & ~((data.wA_obs > 0) & (TF > 0))):
        raise ValueError("a location with farm jobs needs a positive farm wage and farmland")
    wA = np.where(farm, data.wA_obs, 0.0)
    one = np.ones(Z)
    # 2. farm wedge (in utility terms, net of any land-income markup in the choice); 0 = no farm sector.
    xi_A = np.where(farm, np.exp(z[Z:] - land.choice_wage_markup(omega, p)) / np.where(farm, wA, 1.0), 0.0)
    # 3. rents and floor-supply shifters from observed floor space.
    ch = blocks.choice(D, z[:Z], z[Z:], N, p.lam, farm)
    rho = np.where(farm, blocks.farm_rent(wA, HA, np.where(farm, TF, one), p), 0.0)
    Y = (
        ch.resident_mean(wU, wA)
        + ch.resident_mean(0.0, land.operator_land_income_per_worker(wA, omega, p))
        + land.local_landlord_rebate(rho, TF, omega, N, p.varsigma)
    )
    r = blocks.floor_spending(Y, N, wU, HU, p) / data.L
    L_bar = data.L / r**p.mu
    # 4. non-farm productivity; 6. farm productivity.
    B = blocks.nonfarm_productivity(wU, r, p)
    A_farm = np.where(farm, blocks.farm_productivity(wA, np.where(farm, TF, one), np.where(farm, HA, one), p), 0.0)
    # 7. amenities, geometric mean 1; U_bar = W so the baseline solves (S) for any eta.
    #    In a metro nest (S'): ln A_k = ln N_k / lam_M + ln N_M (1/lam_R - 1/lam_M) + ... (spec §3.12).
    nest = data.nest
    lnN_eff = np.log(N) / p.lam_R
    if nest is not None and np.any(nest >= 0):
        unit, _, _ = blocks.outer_units(nest, Z)
        N_unit = np.bincount(unit, weights=N)[unit]
        inside = nest >= 0
        lnN_eff = np.where(inside, np.log(N) / p.lam_M + np.log(N_unit) * (1.0 / p.lam_R - 1.0 / p.lam_M), lnN_eff)
    lnA = lnN_eff + (1.0 - p.alpha) * np.log(r) - ch.lnPhi / p.lam
    A = np.exp(lnA - lnA.mean())
    lnu = blocks.expected_log_utility(A, r, ch.lnPhi, p)
    U_bar = float(np.exp(blocks.log_welfare(lnu, p.lam_R, nest, p.lam_M)))
    # migration costs between residence units for the path (§3.8; the baseline is its steady state)
    tau = migration_cost(unit_distances(data.dist, nest, N), p)

    f = Fundamentals(
        A=A, B=B, A_farm=A_farm, L_bar=L_bar, TF=TF.astype(float), xi_A=xi_A, omega=omega.astype(float),
        t=data.t.astype(float), tau=tau, gateway=data.gateway.astype(float),
        U_bar=U_bar, N_bar0=float(N.sum()), nest=None if nest is None else np.asarray(nest),
    )  # fmt: skip
    base = solve_static(f, p, N0=N, x0=np.concatenate([np.log(r), np.log(np.where(farm, wA, 1.0))]))
    w = base.within

    def rel(model, obs, m=one.astype(bool)):
        return float(np.max(np.abs(model[m] / obs[m] - 1.0))) if m.any() else 0.0

    no_farm_err = float(np.max(np.abs(w.HA[~farm]), initial=0.0) / HA.sum()) if HA.sum() > 0 else 0.0
    errors = {"HA": max(rel(w.HA, HA, farm), no_farm_err), "wA": rel(w.wA, wA, farm),
              "HU": rel(w.HU, HU), "N": rel(base.N, N)}  # fmt: skip
    errors = {k: errors[k] for k in ("HU", "HA", "wA", "N")}
    return Calibration(f, base, errors, wage_info)
