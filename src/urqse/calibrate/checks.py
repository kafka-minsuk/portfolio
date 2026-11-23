"""Farmland-rent checks (spec §5 step 5): the over-identification test of model rents against
county cash rents, and theta_T estimated county by county from rent shares."""

import numpy as np

HA_PER_ACRE = 0.40468564224  # exact (international acre)


def rent_usd_per_acre(rho, usd_per_wage_unit):
    """Model farmland rent (wage units per hectare) in dollars per acre."""
    return np.asarray(rho) * usd_per_wage_unit * HA_PER_ACRE


def theta_T_from_rents(rent_bill, labour_bill):
    """theta_T = rho T^F / (rho T^F + labour bill), from rho T^F = (theta_T/theta_H) w_A H_A (F).
    Works county by county (arrays) or for a state (sums)."""
    return np.asarray(rent_bill) / (np.asarray(rent_bill) + np.asarray(labour_bill))


def overid(model, obs, weight, *, n_outliers=8) -> dict:
    """Model vs observed rent ($/acre). weight = farmland, for the aggregate level ratio.
    Slopes are OLS of the observed on the model rent; outliers are the counties whose log
    ratio is furthest from the median log ratio."""
    model, obs, weight = (np.asarray(v, float) for v in (model, obs, weight))
    lr = np.log(model / obs)
    b, a = np.polyfit(model, obs, 1)
    b_log, a_log = np.polyfit(np.log(model), np.log(obs), 1)
    dev = lr - np.median(lr)
    return {
        "n": int(model.size),
        "corr": float(np.corrcoef(model, obs)[0, 1]),
        "corr_log": float(np.corrcoef(np.log(model), np.log(obs))[0, 1]),
        "slope": float(b),
        "intercept": float(a),
        "slope_log": float(b_log),
        "level_ratio": float(np.sum(model * weight) / np.sum(obs * weight)),  # model / observed
        "median_ratio": float(np.exp(np.median(lr))),
        "sd_log_ratio": float(np.std(lr)),
        "outliers": np.argsort(-np.abs(dev))[:n_outliers],
        "log_ratio": lr,
    }
