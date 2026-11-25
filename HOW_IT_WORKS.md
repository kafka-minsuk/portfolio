# How the migration simulator works

The simulator asks one question about a U.S. state. If something changes in its main city or on its farms, where do people end up living and working, and how long does the countryside take to consolidate? It is a quantitative spatial equilibrium model of one state, calibrated to county data and solved in the browser. The full specification is [URQSE_model_spec.md](URQSE_model_spec.md). This page is the short version.

## Three pieces

The work splits into an offline data build, an offline calibration, and a web page that only solves and draws.

1. `urqse.data.build_state` turns public data into one table per county: workers, non-farm and farm jobs, floor space, farmland, farm wages, land tenure, cash rents, and car travel times between counties. `urqse.data.build_metro` does the same for the census tracts of the core city's metro area.
2. `urqse.calibrate.run_state` estimates two state parameters from data, then inverts the model so that it reproduces every county's data exactly. It writes `src/urqse/calibrate/estimates/{state}_{year}.json` and a calibration report in `reports/`.
3. `urqse.data.export_web` writes one JSON file per state for `docs/migration.html`. The page runs the same Python package under Pyodide, so the browser and the tests use one model.

`scripts/build_all_states.py` runs all three steps for every state and writes `reports/STATES_STATUS.md`.

## What the model assumes

Each person lives in one place and works in one place, in a farm job or a non-farm job. People pick the combination that is best for them. Each person also has an idiosyncratic taste for each option, drawn from a Fréchet distribution, so choices spread out instead of all going to the single best place. Commuting cost rises with travel time.

Non-farm firms use labour and commercial floor space. Farms use labour and farmland. Floor space gets more expensive as more people want it, at a rate set by the supply elasticity μ. Farmland is fixed, so fewer farm workers means more land per worker.

Moving home is slower than changing jobs. The long run uses a second, less elastic choice of residence (λ_R). Along the path, people move period by period with migration costs that rise with distance. The state is closed to the rest of the country by default (η = 0). International immigration is an optional inflow.

The path stops when farmland per rural farm worker has risen by the consolidation target ε, or when nothing moves any more. Land income is wealth. A farmer who moves keeps it, so it does not hold anyone in place unless you turn that switch on.

Two extensions handle real geography. A county or tract with no farm jobs has no farm option at all (spec §3.11). In Iowa the Des Moines metro area is split into 162 census tracts (spec §3.12). People first choose between the metro and other counties, then choose a tract within the metro. Double-click the metro on the map to see it.

## How the numbers are pinned down

The calibration follows the exact-inversion approach of quantitative spatial economics. Given the data and a few elasticities, it solves for the unobserved fundamentals: amenities, productivities, floor-space supply, and the farm-job wedge ξ_A. With those fundamentals the model reproduces jobs, farm wages, and residents in every county to better than one part in ten million. Every counterfactual starts from that baseline.

Two parameters are estimated for each state.

- The commuting slope κλ comes from a gravity regression on LODES commuting flows between counties. It is estimated by Poisson pseudo-maximum likelihood with origin and destination fixed effects.
- The land share in farming θ_T comes from rent shares: NASS cash rent times farmland, against the farm labour bill from BEA.

A third check is not used to fit anything. Model farmland rents are compared with NASS county cash rents as an over-identification test. In Iowa the level matches, but the pattern across counties does not. The calibration report says why.

The other parameters come from the literature and are listed with sources in `src/urqse/model/params.py`. Values that are uncertain carry a `# VERIFY` tag.

## Modelling standards it follows

The model sits in the quantitative spatial economics literature reviewed by Redding and Rossi-Hansberg (Annual Review of Economics, 2017). Each block uses the standard tool for its job.

| Block | Standard | Source |
|---|---|---|
| Home and workplace choice with commuting | Fréchet choice over home and workplace pairs, and exact model inversion | Ahlfeldt, Redding, Sturm and Wolf (Econometrica 2015) |
| Commuting and migration across U.S. counties | County commuting matrix with separate commuting and migration margins | Monte, Redding and Rossi-Hansberg (AER 2018) |
| Gravity estimation | Poisson pseudo-maximum likelihood with fixed effects, zeros kept | Santos Silva and Tenreyro (REStat 2006) |
| Migration along the path | Dynamic logit flows with migration costs | Artuç, Chaudhuri and McLaren (AER 2010), and Caliendo, Dvorkin and Parro (Econometrica 2019) |
| Counterfactuals | Exact hat algebra (planned for fast solves) | Dekle, Eaton and Kortum (2007) |
| Farm-job wedge | Read as a reduced-form gap that includes selection, not a pure distortion | Gollin, Lagakos and Waugh (QJE 2014), and Hamory, Kleemans, Li and Miguel (JEEA 2021) |
| Floor-space supply | Elasticity near 0.5 for U.S. urban tracts | Baum-Snow and Han (JPE 2024) |
| Metro nest | Nested Fréchet, which needs λ_M ≥ λ_R for the nesting to be consistent | McFadden (1978), on nested residential choice |
| Uniqueness | Without spillovers the equilibrium is unique. Spillovers need a check before they are added | Allen, Arkolakis and Li (AER: Insights 2024) |

The numerical rules follow the same literature's practice. Every solve is in logs, with damped fixed-point iteration and Anderson acceleration. A solve stops on the size of the residual, never on step size alone. Every result carries its convergence flag, and the page hides any result that did not converge. The test suite checks the invariants the spec lists: the inversion reproduces the data, a zero shock changes nothing, population is conserved, accounting identities hold, and the two-location closed form of spec §4 matches the solver.

## Where it departs from the literature

These are deliberate simplifications. Each is a known limit, not an oversight.

- There is no agglomeration and no amenity spillover. Ahlfeldt et al. estimate both. Adding them is milestone M7b, at tract scale, with the uniqueness check.
- Agents are myopic along the path. Caliendo, Dvorkin and Parro use forward-looking agents.
- Each state has one core county. A state with several large metros treats the others as suburbs or rural counties.
- The state is closed to domestic migration (η = 0). Only international immigrants arrive, and they currently choose places without regard to size, which over-weights small places. That rule is flagged `# VERIFY`.
- Tract data inside the metro is the county data split by LODES shares. Wages and land tenure are the county's.

## Data rules for particular states

The same pipeline builds every state. Where a state's data breaks a general rule, the build uses one of these fallbacks, records it in that state's reports, and marks it `# VERIFY` in the code.

| State | Gap in the data | Rule used |
|---|---|---|
| Arizona, Nevada | No non-irrigated cropland cash rent | NASS irrigated cropland rent, which is higher than dryland rent where both exist |
| Rhode Island | No cropland cash rent in any series | The mean state rent of Connecticut and Massachusetts |
| Michigan, and its neighbours Indiana, Ohio and Wisconsin | No 2022 LODES commuting file for Michigan | The latest earlier year |
| Washington | No road route to San Juan County (islands) | Straight-line distance at the state's median road speed, which ignores ferry waits |
| Delaware | Three counties give 6 county pairs for 6 parameters, so the commuting regression cannot identify κλ | The regression sample that adds own-county flows |
| Massachusetts, New York, Rhode Island | Connecticut's 2022 planning regions are missing from the 2020 population-centre file | The region's polygon centre, weighted by its 2022 population |
| New Jersey, Rhode Island | Every county is in a metro area | The model runs, and the rural measures are blank |
| 17 states, from California to Wisconsin | Some counties have no farm jobs | Those counties have no farm sector (spec §3.11) |

`tests/test_all_regions.py` runs every state in the menu with its default scenario. It checks that the calibration reproduces the data and that the solves converge under the page's threshold.

## What is in the browser

The **Presets** buttons set common scenarios in one click. City presets change the core: a downtown boom or decline, upzoning, a metro transit line, or better city amenities. State presets act everywhere: a farm technology leap or downturn, a highway programme, an immigration wave, or rural revival. A preset sets every shock and keeps the parameters, so you can compare presets under the same assumptions.

`docs/migration/data/regions.json` lists the states that are built. Alaska, Hawaii, Connecticut, and DC are not built, and `reports/STATES_STATUS.md` gives the reason for each. Each state has two reports. `reports/{state}_2022_REPORT.md` covers the data build. `reports/{state}_2022_CALIBRATION.md` covers the estimates and checks. Only Iowa's reports have been read through by hand.
