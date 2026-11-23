"""Read a built state (data/{state}/{year}/) into the CountyData object calibration consumes."""

from pathlib import Path

import numpy as np
import pandas as pd

from ..synthetic import CountyData
from .schema import COUNTY_SCHEMA, validate_travel

DATA_ROOT = Path(__file__).resolve().parents[3] / "data"
COUNTY_FILE = "county.parquet"
TRAVEL_FILE = "travel.npz"


def state_dir(state: str, year: int, root: Path = DATA_ROOT) -> Path:
    return Path(root) / state.upper() / str(year)


def read_county(path) -> pd.DataFrame:
    return COUNTY_SCHEMA.validate(pd.read_parquet(path))


def read_travel(path):
    with np.load(path, allow_pickle=False) as z:
        fips, t, dist = z["fips"].astype(str), z["t"], z["dist"]
    validate_travel(fips, t, dist)
    return fips, t, dist


def to_county_data(df: pd.DataFrame, fips, t, dist) -> CountyData:
    """Wages in units of the state's mean non-farm earnings per job (as in synthetic.py)."""
    if list(fips) != list(df["fips"]):
        raise ValueError("travel matrix rows do not match the county table")
    counties = df["kind"] != "external"
    mean_nonfarm = df.loc[counties, "nonfarm_earn_usd"].sum() / df.loc[counties, "HU_bea"].sum()

    def col(name):
        return df[name].to_numpy(float)

    return CountyData(
        names=df["name"].tolist(), kind=df["kind"].to_numpy(str), x=col("x_km"), y=col("y_km"),
        N=col("N"), HU=col("HU"), HA=col("HA"), L=col("L"), TF=col("TF"),
        wA_obs=col("wA_obs_usd") / mean_nonfarm, mean_nonfarm_wage=1.0,
        omega=col("omega"), gateway=col("gateway"), dist=dist, t=t,
    )  # fmt: skip


def load_state(state: str = "IA", year: int = 2022, root: Path = DATA_ROOT) -> CountyData:
    d = state_dir(state, year, root)
    return to_county_data(read_county(d / COUNTY_FILE), *read_travel(d / TRAVEL_FILE))
