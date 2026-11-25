"""Closed-form model blocks: choice (L), non-farm frontier (Z), farm (F), floor (R), residence (S)."""

import math
from dataclasses import dataclass

import numpy as np

from .params import Params


def logsumexp(v: np.ndarray) -> float:
    c = float(np.max(v))
    return c + math.log(float(np.sum(np.exp(v - c))))


# --- non-farm production (Z) -------------------------------------------------------------


def nonfarm_wage(B, r, p: Params):
    return p.beta * B ** (1.0 / p.beta) * ((1.0 - p.beta) / r) ** p.k_com


def nonfarm_productivity(wU, r, p: Params):
    return (wU / p.beta) ** p.beta * (r / (1.0 - p.beta)) ** (1.0 - p.beta)


# --- farm production (F) -----------------------------------------------------------------


def farm_wage(A_farm, TF, HA, p: Params):
    return p.theta_H * A_farm * (TF / HA) ** p.theta_T


def farm_productivity(wA, TF, HA, p: Params):
    return wA * (HA / TF) ** p.theta_T / p.theta_H


def farm_value_added(A_farm, HA, TF, p: Params):
    return A_farm * HA**p.theta_H * TF**p.theta_T


def farm_rent(wA, HA, TF, p: Params):
    return p.theta_T / p.theta_H * wA * HA / TF


# --- floor space (R) ---------------------------------------------------------------------


def floor_spending(Y, N, wU, HU, p: Params):
    """Residential plus commercial floor-space expenditure."""
    return (1.0 - p.alpha) * Y * N + p.k_com * wU * HU


def floor_rent(E, L_bar, p: Params):
    return (E / L_bar) ** (1.0 / (1.0 + p.mu))


# --- within-period job choice (L) --------------------------------------------------------


@dataclass(frozen=True)
class Choice:
    """Frechet choice over (workplace j, sector s) for every residence i, stored without the
    Z x Z x 2 tensor: pi_{js|i} = D_ij e_sj / Phi_s_i, with lnPhi = ln Phi_s + shift."""

    D: np.ndarray  # exp(-kappa*lam*t)
    eU: np.ndarray
    eA: np.ndarray
    Phi_s: np.ndarray
    lnPhi: np.ndarray
    M: np.ndarray  # sum_i D_ij N_i / Phi_s_i
    HU: np.ndarray
    HA: np.ndarray

    def resident_mean(self, vU, vA):
        """sum_{j,s} pi_{js|i} v_{js}: the mean over a resident's job draws."""
        return self.D @ (self.eU * vU + self.eA * vA) / self.Phi_s

    def own_shares(self, D2: np.ndarray, N: np.ndarray):
        """sum_i pi_{js|i}^2 N_i / H_js, the curvature term in d ln H_js / d ln w_js."""
        q = D2.T @ (N / self.Phi_s**2) / self.M
        return self.eU * q, self.eA * q


def farm_mask(xi_A) -> np.ndarray:
    """Locations with a farm sector (§3.11): the farm job option exists where xi_A > 0."""
    return np.asarray(xi_A) > 0.0


def choice(D, ln_wtU, ln_wtA, N, lam, farm=None) -> Choice:
    """farm: locations with a farm sector (default all). Elsewhere the farm option is absent
    (e_A = 0, so H_A = 0), and ln_wtA there is ignored."""
    zU, zA = lam * ln_wtU, lam * np.asarray(ln_wtA, float)
    if farm is None:
        farm = np.ones(zA.shape, bool)
    shift = float(max(zU.max(), zA[farm].max())) if farm.any() else float(zU.max())
    eU = np.exp(zU - shift)
    eA = np.where(farm, np.exp(np.where(farm, zA, 0.0) - shift), 0.0)
    Phi_s = D @ (eU + eA)
    M = D.T @ (N / Phi_s)
    return Choice(D, eU, eA, Phi_s, np.log(Phi_s) + shift, M, eU * M, eA * M)


def expected_log_utility(A, r, lnPhi, p: Params):
    """ln u_i = ln Gamma(1-1/lam) + ln A_i - (1-alpha) ln r_i + ln Phi_i / lam."""
    return math.lgamma(1.0 - 1.0 / p.lam) + np.log(A) - (1.0 - p.alpha) * np.log(r) + lnPhi / p.lam


# --- residence (S), nested (S') ------------------------------------------------------------


def outer_units(nest, Z: int):
    """Residence units of the first-stage choice (spec §3.12): every zone outside a nest is its own
    unit; all zones of a nest form one unit. nest: (Z,) ints, -1 = not in a nest, or None.
    Returns (unit of each zone, number of units, nest label of each unit or -1)."""
    if nest is None or np.all(np.asarray(nest) < 0):
        return np.arange(Z), Z, np.full(Z, -1)
    nest = np.asarray(nest)
    key = np.where(nest < 0, np.arange(Z), Z + nest)  # a nest's key sits after every zone index
    first = {}
    unit = np.empty(Z, int)
    for z, k in enumerate(key):  # units in order of first appearance
        unit[z] = first.setdefault(int(k), len(first))
    label = np.full(len(first), -1)
    label[unit[nest >= 0]] = nest[nest >= 0]
    return unit, len(first), label


def unit_log_values(lnu, nest, lam_M):
    """ln u of each first-stage unit: the zone's own ln u, or a nest's CES value
    ln u_M = logsumexp(lam_M ln u_k) / lam_M over its zones."""
    unit, U, _ = outer_units(nest, lnu.size)
    out = np.full(U, -np.inf)
    for u in range(U):
        z = lnu[unit == u]
        out[u] = z[0] if z.size == 1 else logsumexp(lam_M * z) / lam_M
    return out


def residence_log_shares(lnu, lam_R, nest=None, lam_M=None):
    """ln(N_i / N_bar). Flat (S) without a nest; nested (S') with one: counties and nests by lam_R,
    zones inside a nest by lam_M (>= lam_R)."""
    if nest is None or np.all(np.asarray(nest) < 0):
        z = lam_R * lnu
        return z - logsumexp(z)
    unit, _, _ = outer_units(nest, lnu.size)
    lnu_U = unit_log_values(lnu, nest, lam_M)
    outer = lam_R * lnu_U - logsumexp(lam_R * lnu_U)
    inner = np.where(np.asarray(nest) >= 0, lam_M * (lnu - lnu_U[unit]), 0.0)
    return outer[unit] + inner


def log_welfare(lnu, lam_R, nest=None, lam_M=None) -> float:
    lnu_U = lnu if nest is None or np.all(np.asarray(nest) < 0) else unit_log_values(lnu, nest, lam_M)
    return logsumexp(lam_R * lnu_U) / lam_R


def congestion_elasticities(p: Params):
    """psi_C, psi_R: elasticities of utility to own population in the two-location model (§4)."""
    k = p.k_com
    psi_C = (k + 1.0 - p.alpha) / (1.0 + p.mu + k)
    psi_R = p.theta_T + (1.0 - p.alpha) * p.theta_H / (1.0 + p.mu)
    return psi_C, psi_R
