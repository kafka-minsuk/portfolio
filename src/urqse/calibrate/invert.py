"""Exact model inversion (spec §5 steps 1-8)."""

from dataclasses import dataclass

import numpy as np

from ..model import blocks, land
from ..model.dynamics import calibrate_flow_offsets, migration_cost
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
    flow_info: SolveInfo


def effective_wages(D, N, HU, HA, lam, *, tol=1e-13):
    """Step 1: ln w-tilde such that the choice block reproduces (HU, HA); geometric mean of
    non-farm wages = 1 (ARSW contraction, accelerated)."""
    Z = N.size
    lnH = np.log(np.concatenate([HU, HA]))

    def step(z):
        ch = blocks.choice(D, z[:Z], z[Z:], N, lam)
        g = z + (lnH - np.log(np.concatenate([ch.HU, ch.HA]))) / lam
        g -= g[:Z].mean()
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
    wA = data.wA_obs
    # 2. farm wedge (in utility terms, net of any land-income markup in the choice).
    xi_A = np.exp(z[Z:] - land.choice_wage_markup(omega, p)) / wA
    # 3. rents and floor-supply shifters from observed floor space.
    ch = blocks.choice(D, z[:Z], z[Z:], N, p.lam)
    rho = blocks.farm_rent(wA, HA, TF, p)
    Y = (
        ch.resident_mean(wU, wA)
        + ch.resident_mean(0.0, land.operator_land_income_per_worker(wA, omega, p))
        + land.local_landlord_rebate(rho, TF, omega, N, p.varsigma)
    )
    r = blocks.floor_spending(Y, N, wU, HU, p) / data.L
    L_bar = data.L / r**p.mu
    # 4. non-farm productivity; 6. farm productivity.
    B = blocks.nonfarm_productivity(wU, r, p)
    A_farm = blocks.farm_productivity(wA, TF, HA, p)
    # 7. amenities, geometric mean 1; U_bar = W so the baseline solves (S) for any eta.
    lnA = np.log(N) / p.lam_R + (1.0 - p.alpha) * np.log(r) - ch.lnPhi / p.lam
    A = np.exp(lnA - lnA.mean())
    lnu = blocks.expected_log_utility(A, r, ch.lnPhi, p)
    U_bar = float(np.exp(blocks.log_welfare(lnu, p.lam_R)))
    # 8. flow offsets so N is a steady state of the path.
    tau = migration_cost(data.dist, p)
    delta, flow_info = calibrate_flow_offsets(N, lnu, tau, p.nu)

    f = Fundamentals(
        A=A, B=B, A_farm=A_farm, L_bar=L_bar, TF=TF.astype(float), xi_A=xi_A, omega=omega.astype(float),
        t=data.t.astype(float), tau=tau, delta=delta, gateway=data.gateway.astype(float),
        U_bar=U_bar, N_bar0=float(N.sum()),
    )  # fmt: skip
    base = solve_static(f, p, N0=N, x0=np.concatenate([np.log(r), np.log(wA)]))
    w = base.within

    def rel(model, obs):
        return float(np.max(np.abs(model / obs - 1.0)))

    errors = {"HU": rel(w.HU, HU), "HA": rel(w.HA, HA), "wA": rel(w.wA, wA), "N": rel(base.N, N)}
    return Calibration(f, base, errors, wage_info, flow_info)
