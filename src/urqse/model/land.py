"""Land tenure, land income routing (spec §12.1) and asset prices (spec §3.10)."""

import numpy as np

from .params import Params

HA_PER_ACRE = 0.40468564224  # exact (international acre)


def operator_land_income_per_worker(wA, omega, p: Params):
    """omega * rho * TF / HA, written with the farm-rent identity rho TF = (theta_T/theta_H) wA HA."""
    return omega * p.theta_T / p.theta_H * wA


def operator_income(wA, rho, TF, HA, omega):
    """Farm operator income per farm worker: wage plus the owner-operated share of land rent."""
    return wA + omega * rho * TF / HA


def landlord_income(rho, TF, omega):
    return (1.0 - omega) * rho * TF


def local_landlord_rebate(rho, TF, omega, N, varsigma):
    """Landlord income paid to residents of the same county, per resident."""
    return varsigma * landlord_income(rho, TF, omega) / N


def choice_wage_markup(omega, p: Params):
    """ln of the factor on the farm wage inside the job choice. Zero unless land income is
    allowed into the choice margin (§12.1 portability; default off)."""
    if not p.land_income_in_choice:
        return np.zeros_like(omega)
    return np.log1p(omega * p.theta_T / p.theta_H)


def gordon_multiple(q: float) -> float:
    """P / rho for a rent that stays constant in detrended terms: q/(1-q) = (1+g)/(i-g)."""
    return q / (1.0 - q)


def discount_from_rates(i: float, g: float) -> float:
    return (1.0 + g) / (1.0 + i)


def present_values(flow_path: np.ndarray, q: float) -> np.ndarray:
    """P_t = sum_{s>=1} q^s y_{t+s}, with y held at its last value beyond the horizon
    (Gordon terminal). flow_path has shape (T+1, ...) with rows t = 0..T."""
    P = np.empty_like(flow_path, dtype=float)
    P[-1] = flow_path[-1] * gordon_multiple(q)
    for t in range(flow_path.shape[0] - 2, -1, -1):
        P[t] = q * (flow_path[t + 1] + P[t + 1])
    return P


def household_wealth(acres: float, land_price: float, income_path: np.ndarray, q: float) -> float:
    """Land holding at its price plus the present value of an income stream received
    from the first period of income_path on."""
    return acres * land_price + income_path[0] + present_values(income_path, q)[0]
