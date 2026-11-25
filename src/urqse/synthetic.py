"""A synthetic 25-county state (spec §4.1 style): one core, eight suburbs, sixteen rural counties
on a 5 x 5 grid of 40 km counties. Every number here is a synthetic design choice, not data."""

from dataclasses import dataclass

import numpy as np

SPACING_KM = 40.0  # county side, roughly an Iowa county
MIN_PER_KM = 1.0  # synthetic road speed, 60 km/h
OWN_COMMUTE_KM = 0.5 * SPACING_KM  # mean trip inside a county

# Per-kind synthetic profile: residents, farm share of local jobs, non-farm job pull,
# floor space per resident, farmland (ha), farm earnings relative to mean non-farm earnings.
PROFILE = {
    "core": dict(N=300_000, farm_share=0.002, job_pull=1.35, floor=1.0, TF=8_000, wA=0.70),
    "suburb": dict(N=45_000, farm_share=0.03, job_pull=0.85, floor=1.3, TF=70_000, wA=0.62),
    "rural": dict(N=12_000, farm_share=0.18, job_pull=0.92, floor=1.6, TF=120_000, wA=0.58),
}


@dataclass(frozen=True)
class CountyData:
    """Observed county inputs to the inversion (spec §5 'Data per county')."""

    names: list
    kind: np.ndarray  # "core" | "suburb" | "rural" (| "external" for a real state's outside zone)
    x: np.ndarray  # km
    y: np.ndarray  # km
    N: np.ndarray  # resident workers
    HU: np.ndarray  # non-farm jobs
    HA: np.ndarray  # farm jobs
    L: np.ndarray  # floor space (index units)
    TF: np.ndarray  # farmland in use, hectares
    wA_obs: np.ndarray  # farm earnings per worker (units of mean non-farm earnings)
    mean_nonfarm_wage: float
    omega: np.ndarray  # owner-operated share of farmland
    gateway: np.ndarray  # immigrant gateway weights
    dist: np.ndarray  # centroid distance, km (own = mean in-county trip)
    t: np.ndarray  # travel time, minutes
    nest: np.ndarray | None = None  # metro nest label per zone, -1 = not in a nest (spec §3.12)

    @property
    def rural(self) -> np.ndarray:
        return self.kind == "rural"

    @property
    def core(self) -> int:
        """The core zone's index (the first one when the core county is split into tracts)."""
        return int(np.nonzero(self.kind == "core")[0][0])

    @property
    def core_mask(self) -> np.ndarray:
        """Every zone of the core county (one county, or its tracts in a metro nest)."""
        return self.kind == "core"


def distances(x, y, own_km):
    d = np.hypot(x[:, None] - x[None, :], y[:, None] - y[None, :])
    np.fill_diagonal(d, own_km)
    return d


def county_data(kind, x, y, rng, *, jitter=0.15, own_km=OWN_COMMUTE_KM) -> CountyData:
    """Build a consistent data set (jobs = resident workers) from per-kind profiles plus noise."""
    kind = np.asarray(kind)
    Z = kind.size

    def prof(key):
        return np.array([PROFILE[k][key] for k in kind], dtype=float)

    def noisy(v):
        return v * np.exp(rng.uniform(-jitter, jitter, Z))

    N = noisy(prof("N"))
    HA = noisy(prof("farm_share")) * N
    pull = noisy(prof("job_pull")) * N
    HU = pull / pull.sum() * (N.sum() - HA.sum())
    dist = distances(x, y, own_km)
    order = {"core": "Core", "suburb": "Suburb", "rural": "Rural"}
    counts = {k: 0 for k in order}
    names = []
    for k in kind:
        counts[k] += 1
        names.append(order[k] if k == "core" else f"{order[k]} {counts[k]}")
    return CountyData(
        names=names, kind=kind, x=np.asarray(x, float), y=np.asarray(y, float),
        N=N, HU=HU, HA=HA, L=noisy(prof("floor")) * N, TF=noisy(prof("TF")),
        wA_obs=noisy(prof("wA")), mean_nonfarm_wage=1.0,
        omega=np.clip(0.5 + rng.uniform(-0.12, 0.12, Z), 0.0, 1.0),
        gateway=np.ones(Z),  # VERIFY: uniform until ACS foreign-born recent-arrival weights exist
        dist=dist, t=MIN_PER_KM * dist,
    )  # fmt: skip


def synthetic_state(seed: int = 7) -> CountyData:
    """The default 25-county state. Deterministic for a given seed."""
    g = np.arange(5) - 2
    gx, gy = np.meshgrid(g, g, indexing="xy")
    ring = np.maximum(np.abs(gx), np.abs(gy)).ravel()
    kind = np.array(["core", "suburb", "rural"])[ring]
    return county_data(kind, SPACING_KM * gx.ravel(), SPACING_KM * gy.ravel(), np.random.default_rng(seed))


def random_state(Z: int, seed: int) -> CountyData:
    """A random economy for property tests: one core, at least one rural county, random layout."""
    rng = np.random.default_rng(seed)
    kind = np.array(["core", "rural"] + list(rng.choice(["suburb", "rural"], Z - 2)))
    cells = rng.permutation(16)[:Z]  # distinct cells of a 4 x 4 grid of 30 km cells
    x = 30.0 * (cells % 4) + rng.uniform(-10, 10, Z)
    y = 30.0 * (cells // 4) + rng.uniform(-10, 10, Z)
    return county_data(kind, x, y, rng, jitter=0.4, own_km=10.0)
