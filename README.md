# Lab for Exploration

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
Two regions: a synthetic 25-county state and Iowa 2022 (99 counties, Polk as the core).
After changing the model or the Iowa data, rebuild the two web inputs:

```bash
python -m urqse.calibrate.run_state IA 2022   # Iowa estimates (needs data/IA/2022 from urqse.data.build_state)
python -m urqse.data.export_web IA 2022       # docs/migration/data/IA_2022.json (county data, params, map)
python scripts/build_py_bundle.py             # docs/py/urqse.zip
```

The region file's shape is documented in `src/urqse/api.py`. The exporter needs the `data` extras
(pandas, geopandas); the browser bundle needs only NumPy.

## Publish to GitHub Pages (one command)

```bash
./deploy.sh <github-account> [repo-name]      # default repo name: demography-pyramids
```

The script switches `gh` to that account for this run, commits as `minsuk0504@snu.ac.kr`, creates the repo if needed,
pushes, and turns on Pages for `main:/docs`. Run it again to publish updates.
The site appears at `https://<account>.github.io/<repo-name>/`.

*A simplified accounting model for exploring scenarios, not a forecast.*
