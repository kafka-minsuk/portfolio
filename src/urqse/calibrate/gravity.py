"""Commuting gravity by PPML (spec §7): ln E[flow_ij] = FE_i + FE_j - kappa*lam * t_ij.

PPML is fitted by Newton/IRLS on the Poisson log-likelihood with a dense design (origin and
destination dummies). Fine for a state's counties (a few hundred fixed effects)."""

from dataclasses import dataclass

import numpy as np

from ..model.equilibrium import SolveInfo


@dataclass(frozen=True)
class PPMLFit:
    beta: np.ndarray
    mu: np.ndarray  # fitted means
    cov_plain: np.ndarray  # Poisson information inverse (assumes Var = mean)
    cov_robust: np.ndarray  # Eicker-White sandwich (HC0)
    cov_cluster: np.ndarray | None  # sandwich clustered on the given groups
    info: SolveInfo


def ppml(y, X, *, cluster=None, tol=1e-10, max_iter=200) -> PPMLFit:
    """Poisson pseudo-maximum likelihood, E[y] = exp(X beta). Stops on the score residual
    max_k |X_k'(y - mu)| / |X_k|'y."""
    y = np.asarray(y, float)
    X = np.asarray(X, float)

    def loglik(e):
        return float(np.sum(y * e - np.exp(e)))

    # start: one weighted least-squares step on ln((y + mean y) / 2), then Newton with step halving
    mu0 = (y + y.mean()) / 2.0
    XtW = X.T * mu0
    beta = np.linalg.solve(XtW @ X, XtW @ (np.log(mu0) + (y - mu0) / mu0))
    eta = X @ beta
    scale = np.abs(X).T @ y + 1e-300  # each score entry relative to its own data moment
    method = "PPML Newton (step halving)"
    for k in range(max_iter + 1):
        mu = np.exp(eta)
        score = X.T @ (y - mu)
        res = float(np.max(np.abs(score) / scale))
        if res <= tol or k == max_iter:
            break
        d = np.linalg.solve((X.T * mu) @ X, score)
        ll0 = loglik(eta)
        for _ in range(40):
            if loglik(X @ (beta + d)) >= ll0:
                break
            d = d / 2.0
        beta = beta + d
        eta = X @ beta
    info = SolveInfo(bool(res <= tol), k, res, method)
    bread = np.linalg.inv((X.T * mu) @ X)
    u = X * (y - mu)[:, None]
    cov_robust = bread @ (u.T @ u) @ bread
    cov_cluster = None
    if cluster is not None:
        _, g = np.unique(cluster, return_inverse=True)
        S = np.zeros((g.max() + 1, X.shape[1]))
        np.add.at(S, g, u)
        G = S.shape[0]
        cov_cluster = G / (G - 1) * bread @ (S.T @ S) @ bread
    return PPMLFit(beta, mu, bread, cov_robust, cov_cluster, info)


@dataclass(frozen=True)
class GravityFit:
    kappa_lam: float
    se_plain: float
    se_robust: float
    se_cluster_origin: float
    n_obs: int
    n_zero: int
    pseudo_r2: float  # squared correlation of flows and fitted flows
    info: SolveInfo


def _active(flows, mask):
    """Drop origins / destinations with no flow in the sample (their fixed effect is -inf)."""
    mask = mask.copy()
    while True:
        rows = np.where(mask, flows, 0.0).sum(1) > 0
        cols = np.where(mask, flows, 0.0).sum(0) > 0
        new = mask & rows[:, None] & cols[None, :]
        if (new == mask).all():
            return mask
        mask = new


def _identified(oi, dj) -> np.ndarray:
    """Destination dummies to keep: all but the first destination of each connected component of the
    origin-destination graph of the sample pairs. A short-trip sample can split a state into groups
    of counties with no pair between them; each group's fixed effects then need their own
    normalisation (one group, as with all pairs, drops destination 0 only)."""
    no, nd = oi.max() + 1, dj.max() + 1
    label = np.arange(no + nd)  # min-label propagation over the pairs until stable
    while True:
        m = np.minimum(label[oi], label[no + dj])
        new = label.copy()
        np.minimum.at(new, oi, m)
        np.minimum.at(new, no + dj, m)
        new = new[new]
        if (new == label).all():
            break
        label = new
    dest = label[no:]
    keep = np.ones(nd, bool)
    keep[[int(np.flatnonzero(dest == c)[0]) for c in np.unique(dest)]] = False
    return keep


def commuting_gravity(flows, t, mask=None, **kw) -> GravityFit:
    """flows[i, j] = workers living in i and working in j; t in minutes; mask selects the pairs
    used (default: all). Returns kappa*lam, the semi-elasticity per minute."""
    flows = np.asarray(flows, float)
    mask = np.ones(flows.shape, bool) if mask is None else np.asarray(mask, bool)
    mask = _active(flows, mask)
    i, j = np.nonzero(mask)
    oi = np.unique(i, return_inverse=True)[1]
    dj = np.unique(j, return_inverse=True)[1]
    D = np.eye(dj.max() + 1)[dj]
    X = np.column_stack([-t[i, j], np.eye(oi.max() + 1)[oi], D[:, _identified(oi, dj)]])
    y = flows[i, j]
    fit = ppml(y, X, cluster=i, **kw)
    r2 = float(np.corrcoef(y, fit.mu)[0, 1] ** 2)
    return GravityFit(
        kappa_lam=float(fit.beta[0]), se_plain=float(np.sqrt(fit.cov_plain[0, 0])),
        se_robust=float(np.sqrt(fit.cov_robust[0, 0])), se_cluster_origin=float(np.sqrt(fit.cov_cluster[0, 0])),
        n_obs=int(y.size), n_zero=int((y == 0).sum()), pseudo_r2=r2, info=fit.info,
    )  # fmt: skip
