"""The county table written by build_state and read by loaders (one row per zone).

Model columns (N, HU, HA, L, TF, wA_obs_usd, omega, gateway, ...) are what calibration consumes.
Source columns keep the raw published values so the report can be checked against them.
The external zone (fips "EXT") closes cross-state commuting so that jobs = resident workers
(spec §5); its source columns are null."""

import numpy as np
import pandera.pandas as pa

EXTERNAL_FIPS = "EXT"
KINDS = ("core", "suburb", "rural", "external")

_pos = pa.Check.gt(0)
_nonneg = pa.Check.ge(0)
_share = pa.Check.in_range(0.0, 1.0)


def _model(checks=_pos):
    return pa.Column(float, checks, nullable=False)


def _source(checks=_nonneg):
    return pa.Column(float, checks, nullable=True)


def _jobs_equal_workers(df):
    return bool(np.isclose(df["N"].sum(), df["HU"].sum() + df["HA"].sum(), rtol=1e-12))


def _one_external(df):
    return int((df["fips"] == EXTERNAL_FIPS).sum()) == 1 and df["fips"].iloc[-1] == EXTERNAL_FIPS


COUNTY_SCHEMA = pa.DataFrameSchema(
    {
        "fips": pa.Column(str, pa.Check.str_matches(r"^(\d{5}|EXT)$"), unique=True),
        "name": pa.Column(str),
        "kind": pa.Column(str, pa.Check.isin(KINDS)),
        "lat": _model(pa.Check.in_range(-90, 90)),
        "lon": _model(pa.Check.in_range(-180, 180)),
        "x_km": _model(None),
        "y_km": _model(None),
        # model inputs (spec §5 'Data per county')
        "N": _model(),  # resident workers
        "HU": _model(),  # non-farm jobs (worker-equivalents)
        "HA": _model(),  # farm jobs (worker-equivalents)
        "L": _model(),  # floor space, m^2
        "TF": _model(),  # farmland in use, hectares
        "wA_obs_usd": _model(),  # farm earnings per farm job, $
        "omega": _model(_share),  # owner-operated share of farmland
        "gateway": _model(_nonneg),  # immigrant gateway weight, state mean 1
        "own_time_min": _model(),
        "own_dist_km": _model(),
        # source values
        "pop": _source(),  # PEP July 1 resident population
        "workers_res": _source(),  # ACS workers 16+ by residence
        "workers_out_state": _source(),  # ACS workers who work outside the state
        "workers_work": _source(),  # ACS workers 16+ by workplace
        "HU_bea": _source(),  # BEA non-farm employment (jobs)
        "HA_bea": _source(),  # BEA farm employment (jobs, incl. proprietors)
        "HA_prop_bea": _source(),  # BEA farm proprietors employment
        "farm_earn_usd": _source(None),  # BEA farm earnings, $ (can be negative)
        "nonfarm_earn_usd": _source(None),  # BEA non-farm earnings, $
        "wU_obs_usd": _source(None),  # non-farm earnings per non-farm job, $
        "pasture_ha": _source(),  # CDL grassland/pasture
        "farmland_census_ha": _source(),  # Census of Agriculture land in farms
        "cropland_census_ha": _source(),  # Census of Agriculture total cropland
        "built_volume_m3": _source(),  # GHSL GHS-BUILT-V
        "owned_acres": _source(),
        "rented_acres": _source(),
        "cash_rent_usd_acre": _source(),  # NASS non-irrigated cropland cash rent
        "cash_rent_filled": pa.Column(bool),
        "land_value_usd_acre": _source(),  # Census of Ag land & buildings value per acre
        "fb_recent": _source(),  # ACS foreign born who entered 2010 or later
        "area_km2": _source(),
    },
    checks=[
        pa.Check(_jobs_equal_workers, error="jobs must equal resident workers (spec §5)"),
        pa.Check(_one_external, error="exactly one external zone, in the last row"),
    ],
    strict=True,
    ordered=True,
)

COLUMNS = list(COUNTY_SCHEMA.columns)


def validate_travel(fips, t, dist):
    """The travel file: square, finite, positive, rows in county-table order."""
    Z = len(fips)
    for name, m in (("t", t), ("dist", dist)):
        if m.shape != (Z, Z):
            raise ValueError(f"{name} has shape {m.shape}, expected {(Z, Z)}")
        if not np.all(np.isfinite(m)) or not np.all(m > 0):
            raise ValueError(f"{name} must be finite and positive (own-zone entries included)")
