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


def choice(D, ln_wtU, ln_wtA, N, lam) -> Choice:
    zU, zA = lam * ln_wtU, lam * ln_wtA
    shift = float(max(zU.max(), zA.max()))
    eU, eA = np.exp(zU - shift), np.exp(zA - shift)
    Phi_s = D @ (eU + eA)
    M = D.T @ (N / Phi_s)
    return Choice(D, eU, eA, Phi_s, np.log(Phi_s) + shift, M, eU * M, eA * M)


def expected_log_utility(A, r, lnPhi, p: Params):
    """ln u_i = ln Gamma(1-1/lam) + ln A_i - (1-alpha) ln r_i + ln Phi_i / lam."""
    return math.lgamma(1.0 - 1.0 / p.lam) + np.log(A) - (1.0 - p.alpha) * np.log(r) + lnPhi / p.lam


# --- residence (S) -----------------------------------------------------------------------


def residence_log_shares(lnu, lam_R):
    z = lam_R * lnu
    return z - logsumexp(z)


def log_welfare(lnu, lam_R) -> float:
    return logsumexp(lam_R * lnu) / lam_R


def congestion_elasticities(p: Params):
    """psi_C, psi_R: elasticities of utility to own population in the two-location model (§4)."""
    k = p.k_com
    psi_C = (k + 1.0 - p.alpha) / (1.0 + p.mu + k)
    psi_R = p.theta_T + (1.0 - p.alpha) * p.theta_H / (1.0 + p.mu)
    return psi_C, psi_R
