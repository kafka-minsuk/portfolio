# CLAUDE.md — URQSE (semi-closed urban–rural spatial equilibrium)

## What this project is
A county-level quantitative spatial equilibrium for one U.S. state. The model, its equations and its calibration are specified in `docs/URQSE_model_spec.md`, and **that spec is the source of truth**. If code and spec disagree, stop and ask; don't silently pick one. A Streamlit app lets a user shock the economy and watch rural consolidation over time.

The reference implementation in `reference/urqse.py` (+ `reference/test_urqse.py`, 9 passing tests) is verified against the spec. Port it, don't rewrite the math. Every refactor must keep those tests passing (move them into `tests/`).

## Fixed modelling decisions (spec §12)
- Stop rule = **consolidation**: stop when rural farmland per farm worker ≥ (1+ε)·baseline, or at steady state.
- **No domestic inflow** (η = 0). Only exogenous **international immigration** I_t, allocated by the residence logit × gateway weights.
- Land = **owner-operators + landlords**, with county owner share ω_n. Land income is portable wealth income: it is in housing demand and welfare, **not** in the location-choice margin (flag `land_income_in_choice=False`).
- Locations = counties; two job types (non-farm U, farm A); one Fréchet choice over (workplace, sector).

## Architecture
```
src/urqse/
  model/      params.py fundamentals.py blocks.py equilibrium.py dynamics.py
              land.py (tenure, consolidation, asset prices) immigration.py hat_algebra.py
  calibrate/  invert.py gravity.py (PPML) checks.py
  data/       schema.py (pandera) loaders.py build_state.py (offline only)
app/streamlit_app.py      # imports urqse; no math in the app
tests/                    # pytest + hypothesis
data/{state}/{year}/county.parquet   # built offline, git-ignored
```
- `urqse` must not import streamlit. The app must not contain model equations.
- Pure functions on numpy arrays. Dataclasses for Params / Fundamentals / Equilibrium.
- Satellite rasters are never processed in the app. `build_state.py` does zonal stats offline.

## Numerical rules
- Solve in **logs** with positive seeds. Never seed at 0.0.
- Fixed points: damped iteration + safeguarded Anderson (m≈6). Stop on the **residual** ‖G(x)−x‖∞, never on step size alone. Default tol 1e-11 inner, 1e-10 outer.
- Every solve returns `{converged, iterations, residual_inf, method}`. Never return or plot an unconverged result without the flag.
- Vectorise. No Python loops over county pairs.
- Use a JAX + Newton (line search) fallback only when Anderson stalls. Keep it optional (`pip install urqse[jax]`).

## Testing rules
- `pytest -q` must pass before any commit. Add a test with every new block.
- Required invariants: inversion reproduces data (1e-7); baseline is an equilibrium; zero shock ⇒ no change (levels and hat algebra); η=0 ⇒ population + cumulative immigration conserved; farm-rent identity; the two-location closed form (spec §4); homogeneity of degree 0 in (w, r); accounting identity: income = wages + land rents distributed per the ownership rule.
- Property tests (hypothesis) on random economies with Z ≤ 15.
- One real-data regression snapshot (Iowa) once data is built.

## Working style
- Small PRs, one milestone at a time (spec §11). Update the spec's changelog when the model changes.
- If a data source or parameter value is uncertain, put it in `params.py` with a `source=` note and a `# VERIFY` tag. Don't invent numbers.
- Ask before adding dependencies beyond numpy, scipy, pandas, pyarrow, geopandas, pandera, streamlit, pydeck, pytest, hypothesis (and optional jax).
