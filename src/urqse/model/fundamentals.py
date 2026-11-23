"""Location fundamentals recovered by inversion (spec §3.7, §5) and scenario shocks."""

from dataclasses import dataclass, replace

import numpy as np


@dataclass(frozen=True)
class Fundamentals:
    A: np.ndarray  # residential amenity
    B: np.ndarray  # non-farm productivity
    A_farm: np.ndarray  # farm productivity net of K, X (A-tilde, §3.4)
    L_bar: np.ndarray  # floor-supply shifter, L = L_bar r^mu
    TF: np.ndarray  # farmland in use
    xi_A: np.ndarray  # farm-job wedge
    omega: np.ndarray  # owner-operated share of farmland (§12.1)
    t: np.ndarray  # travel time in minutes, (Z, Z)
    tau: np.ndarray  # migration cost, (Z, Z), zero diagonal
    delta: np.ndarray  # flow offsets making the baseline a steady state (§5 step 8)
    gateway: np.ndarray  # immigrant gateway weights g_n (§12.2)
    U_bar: float  # reference utility in (S)
    N_bar0: float  # baseline regional population

    @property
    def Z(self) -> int:
        return self.A.size


TRAVEL_SCOPES = ("into_core", "all")


def with_shocks(
    f: Fundamentals,
    *,
    core: int,
    a_TH: float,
    core_productivity_pct: float = 0.0,
    farm_tfp_pct: float = 0.0,
    travel_cut_pct: float = 0.0,
    travel_cut_scope: str = "into_core",
) -> Fundamentals:
    """Apply a scenario: non-farm productivity B at the core, gross farm TFP everywhere
    (A-tilde moves by (1+g)^(1/(a_T+a_H)), §3.4), and a proportional travel-time cut."""
    B = f.B.copy()
    B[core] *= 1.0 + core_productivity_pct / 100.0
    A_farm = f.A_farm * (1.0 + farm_tfp_pct / 100.0) ** (1.0 / a_TH)
    cut = 1.0 - travel_cut_pct / 100.0
    t = f.t.copy()
    if travel_cut_scope == "all":
        t *= cut
    elif travel_cut_scope == "into_core":
        # VERIFY: "links into the core" read as both directions of every link touching the core,
        # excluding the core's own internal commute.
        own = t[core, core]
        t[:, core] *= cut
        t[core, :] *= cut
        t[core, core] = own
    else:
        raise ValueError(f"travel_cut_scope must be one of {TRAVEL_SCOPES}")
    return replace(f, B=B, A_farm=A_farm, t=t)
