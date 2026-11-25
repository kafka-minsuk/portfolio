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
    tau: np.ndarray  # migration cost between residence units (§3.12; zones when there is no nest), zero diagonal
    delta: np.ndarray  # flow offsets per residence unit making the baseline a steady state (§5 step 8)
    gateway: np.ndarray  # immigrant gateway weights g_n (§12.2)
    U_bar: float  # reference utility in (S)
    N_bar0: float  # baseline regional population
    nest: np.ndarray | None = None  # (Z,) metro nest label, -1 = not in a nest (§3.12); None = no nest

    @property
    def Z(self) -> int:
        return self.A.size


TRAVEL_SCOPES = ("into_core", "all")


def with_shocks(
    f: Fundamentals,
    *,
    core,
    a_TH: float,
    core_productivity_pct: float = 0.0,
    farm_tfp_pct: float = 0.0,
    travel_cut_pct: float = 0.0,
    travel_cut_scope: str = "into_core",
) -> Fundamentals:
    """Apply a scenario: non-farm productivity B at the core, gross farm TFP everywhere
    (A-tilde moves by (1+g)^(1/(a_T+a_H)), §3.4), and a proportional travel-time cut.
    core: the core county's index, or a boolean mask (its tracts, when it is in a metro nest)."""
    is_core = np.zeros(f.Z, bool)
    is_core[core] = True
    B = f.B.copy()
    B[is_core] *= 1.0 + core_productivity_pct / 100.0
    A_farm = f.A_farm * (1.0 + farm_tfp_pct / 100.0) ** (1.0 / a_TH)
    cut = 1.0 - travel_cut_pct / 100.0
    t = f.t.copy()
    if travel_cut_scope == "all":
        t *= cut
    elif travel_cut_scope == "into_core":
        # VERIFY: "links into the core" read as both directions of every link between the core and
        # anywhere else, excluding commutes inside the core.
        t[is_core[:, None] ^ is_core[None, :]] *= cut
    else:
        raise ValueError(f"travel_cut_scope must be one of {TRAVEL_SCOPES}")
    return replace(f, B=B, A_farm=A_farm, t=t)
