# Exploration Lab

Interactive population pyramids by single year of age / birth year for every country and UN region,
1950–2100, with:

- **World map** — double-click a country to open it; Ctrl/⌘-click (or Shift-click) to merge countries.
  Merged groups are modelled country by country and summed, so per-capita values are population-weighted
  for each year. Built-in groups (G7, G20, EU-27, OECD, BRICS, ASEAN…) and saved custom groups.
- **Shocks** — e.g. a war, pandemic, birth slump or immigration wave hitting given ages in given years;
  the change carries forward with those birth cohorts.
- **Cohort productivity** — productivity multipliers by birth year, an age–earnings profile and a
  productivity growth rate, giving a **value added (GDP) pyramid** next to the population pyramid.
- **Retirement cost estimate** — pick a retirement age (country statutory ± shift, or uniform) and see
  pension spending, contributions paid by employees and employers (“self-paid”), state subsidy, and health spending on
  retirees (government / out-of-pocket / other), for any year and as a 1990–2100 path, plus sensitivity to the
  retirement age. All country assumptions are editable in the table.

## Data

| What | Source |
|---|---|
| Population by single age & sex, 1950–2100 | UN World Population Prospects 2024 (estimates + medium variant) |
| GDP, health spending per capita (total / government / out-of-pocket), social contributions | World Bank WDI (WHO GHED) |
| Employment by age band, labour income share, pension coverage (SDG 1.3.1) | ILOSTAT |
| Public pension spending, retirement ages, average wage | OECD Pensions at a Glance, OECD SOCX |
| Mandatory pension contribution rates (employee / employer) | `scripts/curated_pensions.csv`: approximate values from OECD PaG and SSA/ISSA *Social Security Programs Throughout the World* |

Rebuild everything (downloads ~200 MB into `data_raw/`, writes `docs/data/`):

```bash
python3 scripts/build_data.py
```

## Run locally

```bash
python3 -m http.server -d docs 8000   # then open http://localhost:8000
```

## Urban–rural migration simulator (`docs/migration.html`)

The URQSE model (`src/urqse`, spec in `URQSE_model_spec.md`) runs in the browser under Pyodide.
[HOW_IT_WORKS.md](HOW_IT_WORKS.md) explains the model and the modelling standards it follows in two pages.
Regions: a synthetic 25-county state and every U.S. state the 2022 sources can build, one state at a
time (`reports/STATES_STATUS.md` lists which, and why the others are left out: Alaska, Hawaii,
Connecticut, DC, and the states with a county that has no farm jobs). Iowa 2022 (99 counties, Polk as
the core) is the one checked by hand. Rebuild one state, or all of them:

```bash
python -m urqse.data.build_state NE 2022      # data/NE/2022 (downloads cached in data_raw/US and data_raw/NE)
python -m urqse.calibrate.run_state NE 2022   # estimates, calibration report
python -m urqse.data.build_metro IA 2022      # optional: the core's metro area as census tracts (the city view)
python -m urqse.data.export_web NE 2022       # docs/migration/data/NE_2022.json + regions.json (the page's menu)
python scripts/build_all_states.py 2022       # all of the above for every supported state; hours on a first run
python scripts/build_py_bundle.py             # docs/py/urqse.zip
```

National downloads (Census, BEA, NASS, GHSL tiles, LODES) are shared in `data_raw/US/`; each state
adds its Cropland Data Layer raster (0.2 to 2 GB) and its OSRM travel-time requests.
The region file's shape is documented in `src/urqse/api.py`. The exporter needs the `data` extras
(pandas, geopandas); the browser bundle needs only NumPy.

## Publish to GitHub Pages (one command)

```bash
./deploy.sh <github-account> [repo-name]      # default repo name: portfolio
```

The script switches `gh` to that account for this run, commits as `minsuk0504@snu.ac.kr`, creates the repo if needed,
pushes, and turns on Pages for `main:/docs`. Run it again to publish updates.
The site appears at `https://<account>.github.io/<repo-name>/`.

*A simplified accounting model for exploring scenarios, not a forecast.*
