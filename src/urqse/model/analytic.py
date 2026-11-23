"""Two-location analytic core (spec §4): C is non-farm only, R is farm only, no cross-commuting."""

from dataclasses import dataclass, replace

import numpy as np

from .blocks import congestion_elasticities
from .equilibrium import solve_static, solve_within
from .fundamentals import Fundamentals
from .params import Params

ABSENT = 1e-8  # productivity of the missing sector in each location
NO_COMMUTE_MIN = 1e4  # travel time between C and R


def closed_form(p: Params, s: float, pi_C: float):
    """Solve the §4 linear system for (n, x) = (d ln N_bar, d ln(N_C/N_R))."""
    psi_C, psi_R = congestion_elasticities(p)
    pi_R = 1.0 - pi_C
    lr, eta = p.lam_R, p.eta
    M = np.array(
        [
            [lr * (psi_C - psi_R), 1.0 + lr * (psi_C * pi_R + psi_R * pi_C)],
            [1.0 + eta * (pi_C * psi_C + pi_R * psi_R), eta * pi_C * pi_R * (psi_C - psi_R)],
        ]
    )
    n, x = np.linalg.solve(M, np.array([lr * s, eta * pi_C * s]))
    return float(n), float(x)


@dataclass(frozen=True)
class TwoLocation:
    s: float
    pi_C: float
    n_closed_form: float
    x_closed_form: float
    n_solver: float
    x_solver: float
    converged: bool


def two_location_economy(p: Params) -> Fundamentals:
    ones = np.ones(2)
    t = np.array([[20.0, NO_COMMUTE_MIN], [NO_COMMUTE_MIN, 20.0]])
    f = Fundamentals(
        A=np.array([1.0, 1.1]), B=np.array([1.0, ABSENT]), A_farm=np.array([ABSENT, 1.0]),
        L_bar=ones, TF=ones, xi_A=ones, omega=0.5 * ones, t=t, tau=np.zeros((2, 2)),
        delta=np.zeros(2), gateway=ones, U_bar=1.0, N_bar0=2.0,
    )  # fmt: skip
    base = solve_static(f, replace(p, eta=0.0))
    return replace(f, U_bar=float(np.exp(base.lnW)))


def two_location_check(p: Params, productivity_pct: float) -> TwoLocation:
    """Compare the §4 closed form with the full solver for a non-farm productivity shock in C."""
    f = two_location_economy(p)
    base = solve_static(f, p)
    shocked = replace(f, B=f.B * np.array([1.0 + productivity_pct / 100.0, 1.0]))
    fixed_N = solve_within(shocked, p, base.N, base.within.x)
    s = float(fixed_N.lnu[0] - base.within.lnu[0])
    pi_C = float(base.N[0] / base.N_bar)
    n_cf, x_cf = closed_form(p, s, pi_C)
    new = solve_static(shocked, p, N0=base.N, x0=base.within.x)
    x_solver = float(np.log(new.N[0] / new.N[1]) - np.log(base.N[0] / base.N[1]))
    n_solver = float(np.log(new.N_bar / base.N_bar))
    ok = base.info.converged and fixed_N.info.converged and new.info.converged
    return TwoLocation(s, pi_C, n_cf, x_cf, n_solver, x_solver, ok)
