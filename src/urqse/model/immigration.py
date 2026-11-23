"""Exogenous international immigration (spec §12.2)."""

import numpy as np

from .blocks import logsumexp


def arrival_shares(lnu, delta, gateway, nu):
    """Pr(n) proportional to g_n exp((ln u_n + delta_n) / nu)."""
    with np.errstate(divide="ignore"):  # g_n = 0 is a county with no arrivals
        z = np.log(gateway) + (lnu + delta) / nu
    return np.exp(z - logsumexp(z))


def immigration_path(per_period: float, periods: int) -> np.ndarray:
    """I_t for t = 0..periods-1 (arrivals between t and t+1)."""
    if per_period < 0:
        raise ValueError("immigration must be non-negative (spec §12.2: I_t >= 0)")
    return np.full(periods, float(per_period))
