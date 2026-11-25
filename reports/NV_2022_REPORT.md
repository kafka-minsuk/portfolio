# Nevada 2022 county data: validation report

Built 2026-11-25 by `python -m urqse.data.build_state NV 2022`. 17 counties plus one external zone. Outputs: `county.parquet` (one row per zone, schema in `src/urqse/data/schema.py`) and `travel.npz` (`fips`, `t` minutes, `dist` km, rows in table order).

## Sources

| Item | Vintage | File (data_raw) | Retrieved | URL |
|---|---|---|---|---|
| pep | Census PEP Vintage 2022, July 1 2022 estimates | `US/co-est2022-alldata.csv` | 2026-11-23 | https://www2.census.gov/programs-surveys/popest/datasets/2020-2022/counties/totals/co-est2022-alldata.csv |
| cbsa | Census PEP Vintage 2023 CBSA file (OMB July 2023 delineations) | `US/cbsa-est2023-alldata.csv` | 2026-11-23 | https://www2.census.gov/programs-surveys/popest/datasets/2020-2023/metro/totals/cbsa-est2023-alldata.csv |
| cenpop | 2020 Census centers of population, county | `US/CenPop2020_Mean_CO.txt` | 2026-11-23 | https://www2.census.gov/geo/docs/reference/cenpop2020/county/CenPop2020_Mean_CO.txt |
| counties | Census cartographic boundary file 2022, 1:500k | `US/cb_2022_us_county_500k.zip` | 2026-11-23 | https://www2.census.gov/geo/tiger/GENZ2022/shp/cb_2022_us_county_500k.zip |
| bea_emp | BEA CAEMP25N (formerly CAINC25N), released 2023-11-16 | `US/bea_CAEMP25N.zip` | 2026-11-23 | https://apps.bea.gov/regional/zip/CAEMP25N.zip |
| bea_farm | BEA CAINC45, released 2023-11-16 | `US/bea_CAINC45.zip` | 2026-11-23 | https://apps.bea.gov/regional/zip/CAINC45.zip |
| bea_earn | BEA CAINC5N, file dated 2026-01-14 | `US/bea_CAINC5N.zip` | 2026-11-23 | https://apps.bea.gov/regional/zip/CAINC5N.zip |
| cdl | USDA NASS Cropland Data Layer 2022, 30 m, clipped to state FIPS 32 | `NV/CDL_2022_32.tif` | 2026-11-24 | https://nassgeodata.gmu.edu/axis2/services/CDLService/GetCDLFile?year=2022&fips=32 |
| acs_b08007 | ACS 2018-2022 5-year, table-based summary file B08007 | `US/acs/acsdt5y2022-b08007.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08007.dat |
| acs_b08604 | ACS 2018-2022 5-year, table-based summary file B08604 | `US/acs/acsdt5y2022-b08604.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08604.dat |
| acs_b05005 | ACS 2018-2022 5-year, table-based summary file B05005 | `US/acs/acsdt5y2022-b05005.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b05005.dat |
| ghsl_R4_C9 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C9.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C9.zip |
| ghsl_R5_C8 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C8.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C8.zip |
| ghsl_R5_C9 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C9.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C9.zip |
| nass | Quick Stats bulk economics file `qs.economics_20261121.txt.gz` (Census of Agriculture 2022; Cash Rents Survey 2022) | `qs.economics_20261121.txt.gz` (filtered copy `*_NV.tsv.gz`) | see file | https://www.nass.usda.gov/sites/default/files/datasets/qs.economics_20261121.txt.gz |
| osrm | OSRM public demo server, car profile (OSM data as served on the build date) | `osrm/*.json` (1 cached block requests; the server caps a table at 100 coordinates) | 2026-11-25 | https://router.project-osrm.org/table/v1/driving |

## County sums against published state totals

| Column | Sum of counties | Published state value | Difference |
|---|---|---|---|
| PEP population | 3,177,772 | 3,177,772 | 0.000% |
| ACS workers by residence | 1,434,135 | 1,434,135 | 0.000% |
| ACS workers by workplace | 1,434,840 | 1,434,840 | 0.000% |
| ACS workers working out of state | 27,125 | 27,125 | 0.000% |
| BEA non-farm employment (L80) | 2,056,663 | 2,056,663 | 0.000% |
| BEA farm employment (L70) | 5,208 | 5,208 | 0.000% |
| BEA farm proprietors (L50) | 2,864 | 2,864 | 0.000% |
| BEA farm earnings $ (CAINC45 L370) | 177,935,000 | 177,935,000 | 0.000% |
| BEA farm wages + supplements $ (CAINC45 L350 + L360) | 98,043,000 | 98,043,000 | 0.000% |
| CoA hired farm labour expense $ | 134,627,000 | 136,059,000 | -1.052% |
| BEA non-farm earnings $ (CAINC5N L82) | 131,339,636,000 | 131,339,636,000 | 0.000% |
| ACS foreign born entered 2010+ | 121,269 | 121,269 | 0.000% |
| CoA owned acres | 4,296,025 | 4,919,319 | -12.670% |
| CoA rented-from-others acres | 908,986 | 977,335 | -6.993% |
| CoA land in farms, ha | 2,257,782 | 2,386,291 | -5.385% |
| CoA total cropland, ha | 263,006 | 264,620 | -0.610% |

## Model columns

- **N, HU, HA (jobs = resident workers).** Each county's BEA farm and non-farm job counts are scaled to its ACS count of workers by place of work (scale factor min 0.293, median 0.734, max 1.186; BEA counts jobs, ACS counts people by main job). Sum N = 1,461,965 = sum HU + HA = 1,461,965. Farm jobs after scaling: 3,843 (BEA 5,208). `# VERIFY` the scaling: part-time farm proprietors with an off-farm main job are counted once, in proportion to the county mix.
- **External zone.** Residents = out-of-state workers commuting in (ACS workplace total minus in-state residents working in state) = 27,830. Jobs = in-state residents working out of state = 27,125, split by the state farm share (HA = 73). Location: the 24 out-of-state counties within 1 km of the state (04015, 06003, 06017, 06027, 06035, 06049, 06051, 06057, 06061, 06071, 06091, 16031, 16073, 16083, 41025, 41037, 41045, 49001, 49003, 49021, 49023, 49027, 49045, 49053); travel time from a county to the zone is the OSRM time to the nearest of them. Floor space, farmland, farm labour earnings and owner share are state averages scaled to its workers / farm jobs; gateway weight 0 (immigrants settle in-state). `# VERIFY` all of these are conventions, not data, and `log(0)` in `immigration.arrival_shares` needs handling in M3.
- **TF (farmland, ha).** CDL 2022 crop, hay, fallow and tree-crop classes (codes 1-61, 66-77, 204-254), pixel-centre zonal sums on the 30 m Albers grid. State: 250,296 ha vs Census of Agriculture cropland 264,620 ha and land in farms 2,386,291 ha; county ratio TF / CoA cropland 0.38 to 1.55. Grassland/pasture (codes 62, 176) is kept separately (`pasture_ha`, 2,542,080 ha). County area covered by CDL pixels: 28,637,328 ha vs land area 28,453,742 ha (the difference is water). `# VERIFY` whether pasture belongs in T^F for livestock counties.
- **L (floor space, m^2).** GHSL GHS-BUILT-V 2020 epoch building volume / 3 m storey height (`# VERIFY` storey height; 2020 is the nearest epoch to 2022). State volume 3.42 km^3.
- **wA_obs_usd (farm labour earnings per farm worker).** Farm compensation (CAINC45 L350 wages and salaries + L360 supplements) per farm wage-and-salary job (CAEMP25N L70 - L50), mean of 2018 to 2022, each year relative to the state's non-farm earnings per non-farm job (CAINC5N L82 / CAEMP25N L80) and put at the 2022 value (63,861 $). That per-job wage prices every BEA farm job, proprietors included, giving the county farm labour bill `farm_labour_bill_usd`; wA_obs_usd = bill / HA, so it is per farm worker (ACS head) and the model's wage bill w_A H_A equals the bill in dollars. State: 50,757 $ per BEA farm job, 68,790 $ per farm worker; county range 23,347 to 160,922 $ per worker. State compensation per farm wage job by year: 2018 45,840 $, 2019 34,197 $, 2020 45,797 $, 2021 54,593 $, 2022 41,827 $. Proprietors are priced at the hired wage per job (the market price of farm labour in the county) rather than at a non-farm opportunity wage, which would assume away the farm/non-farm gap xi_A is meant to measure. `# VERIFY` the proprietor imputation: a BEA proprietor job is any sole proprietor or partner, many part-time. Contract labour (CoA 14,328,000 $) is left out: its workers are not BEA farm jobs (they are in agricultural support services, non-farm). Census of Agriculture hired labour expense (136,059,000 $ in 2022, column `hired_labor_coa_usd`) is 1.39x BEA farm compensation (98,043,000 $) and pays a different universe (every hired head, including workers on the farm under 150 days), so it is a comparison column, not the bill. `# VERIFY` that gap. The previous measure, BEA farm earnings (L370, wages + proprietors' income) per BEA farm job, is kept as `wA_bea_earn_usd`: state 34,166 $, county -4,302 to 218,419 $; it includes owner-operators' returns to owned land and capital, which spec §12.1 pays separately. The loader divides wA_obs_usd by state non-farm earnings per non-farm worker (sum over counties of non-farm earnings / HU = 91,782 $), so both sectors are per head. `# VERIFY` vintage mismatch: CAINC45/CAEMP25N are the 2023-11-16 release, CAINC5N the 2026 file (CAINC5N's revised 2022 farm earnings are 307,740,000 $ vs CAINC45 177,935,000 $).
- **omega.** Census of Agriculture 2022 owned / (owned + rented from others) acres in farms. State 0.825, county range 0.644 to 0.977.
- **cash_rent_usd_acre.** NASS Cash Rents Survey 2022, irrigated cropland. State 173 $/acre.
- **land_value_usd_acre.** Census of Agriculture 2022 estimated market value of land and buildings per acre (NASS does not publish annual county land values). State 1,123 $/acre.
- **gateway.** ACS foreign born who entered 2010 or later per resident worker, relative to the state ratio (mean 1 over workers). `# VERIFY` against spec §12.2 once the arrival block is calibrated. 4 counties have no recent foreign born in the ACS sample (Lincoln, Mineral, Storey, White Pine), so their gateway weight is 0 (log(0) in arrival_shares).
- **kind.** core = the metropolitan county with the most non-farm jobs (Clark); suburb = other counties in a Metropolitan Statistical Area (OMB 2023) (4); rural = the rest (12). `# VERIFY` one core for a multi-metro state.
- **No farm sector** (spec §3.11): 1 counties have no BEA farm jobs (Storey); their farm wage is 0 and the model gives them no farm job option.
- **Travel time t (min).** OSRM car durations between 2020 population-weighted county centres, as routed (not symmetrised). Off-diagonal median 297.9 min. Own-county time = 0.5214 x sqrt(land area) at the median effective speed of 54.6 straight-line km/h between counties (median 11.1 to 124.3 min). `# VERIFY` the own-county proxy. `dist` is great-circle km (road/straight median ratio 1.33).

## Suppressed cells and fills

| Variable | County | Rule |
|---|---|---|
| HA_bea | 32029 Storey | 0 farm jobs: no farm sector in the model (spec §3.11) |
| cash_rent_usd_acre | 32000  | the state publishes no non-irrigated cropland rent; NASS irrigated cropland rent used |
| omega | 32003 Clark | state owner share |
| omega | 32015 Lander | state owner share |
| omega | 32021 Mineral | state owner share |
| omega | 32029 Storey | state owner share |
| omega | 32510 Carson City | state owner share |
| cash_rent_usd_acre | 32003 Clark | not published; NASS 'other (combined) counties' value = 175 $/acre |
| cash_rent_usd_acre | 32005 Douglas | not published; NASS 'other (combined) counties' value = 175 $/acre |
| cash_rent_usd_acre | 32009 Esmeralda | not published; NASS 'other (combined) counties' value = 175 $/acre |
| cash_rent_usd_acre | 32011 Eureka | not published; NASS 'other (combined) counties' value = 175 $/acre |
| cash_rent_usd_acre | 32015 Lander | not published; NASS 'other (combined) counties' value = 175 $/acre |
| cash_rent_usd_acre | 32017 Lincoln | not published; NASS 'other (combined) counties' value = 175 $/acre |
| cash_rent_usd_acre | 32019 Lyon | not published; NASS 'other (combined) counties' value = 175 $/acre |
| cash_rent_usd_acre | 32021 Mineral | not published; NASS 'other (combined) counties' value = 175 $/acre |
| cash_rent_usd_acre | 32023 Nye | not published; NASS 'other (combined) counties' value = 175 $/acre |
| cash_rent_usd_acre | 32027 Pershing | not published; NASS 'other (combined) counties' value = 175 $/acre |
| cash_rent_usd_acre | 32029 Storey | not published; NASS 'other (combined) counties' value = 175 $/acre |
| cash_rent_usd_acre | 32031 Washoe | not published; NASS 'other (combined) counties' value = 175 $/acre |
| cash_rent_usd_acre | 32033 White Pine | not published; NASS 'other (combined) counties' value = 175 $/acre |
| cash_rent_usd_acre | 32510 Carson City | not published; NASS 'other (combined) counties' value = 175 $/acre |
| owned_acres | 32003 Clark | (D) in Census of Ag; see fills above |
| owned_acres | 32015 Lander | (D) in Census of Ag; see fills above |
| owned_acres | 32021 Mineral | (D) in Census of Ag; see fills above |
| owned_acres | 32029 Storey | (D) in Census of Ag; see fills above |
| owned_acres | 32510 Carson City | (D) in Census of Ag; see fills above |
| rented_acres | 32003 Clark | (D) in Census of Ag; see fills above |
| rented_acres | 32015 Lander | (D) in Census of Ag; see fills above |
| rented_acres | 32510 Carson City | (D) in Census of Ag; see fills above |
| hired_labor_coa_usd | 32021 Mineral | (D) in Census of Ag; left null (comparison column only) |
| hired_labor_coa_usd | 32029 Storey | (D) in Census of Ag; left null (comparison column only) |
| hired_labor_coa_usd | 32510 Carson City | (D) in Census of Ag; left null (comparison column only) |

## Coverage gaps and caveats

- ACS is the 5-year period estimate ending in the base year (no 1-year data for small counties); BEA and PEP are single-year. The external zone inherits ACS sampling error in the commuter totals.
- The Census API now requires a key, so ACS comes from the table-based summary files instead (same estimates).
- LODES (for the M3 PPML of kappa*lambda) and IRS SOI migration flows are not part of this build.
- Census of Agriculture is quinquennial (2022 matches the base year); the cash-rent survey is annual.
- x_km / y_km are NAD83 / UTM (EPSG:26911) at the state's middle longitude, for drawing only.
- No satellite population layer (GHS-POP) is used; census counts drive calibration (spec §8).

## County table

| FIPS | Name | Kind | N | HU | HA | TF ha | L m^2 | wA $/worker | BEA farm earnings $/job | omega | rent $/ac |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 32001 | Churchill | rural | 11,611 | 9,771 | 532 | 24,408 | 12.04M | 88,702 | 41,016 | 0.909 | 178 |
| 32003 | Clark | core | 1,040,510 | 1,043,694 | 300 | 2,030 | 832.28M | 23,347 | 1,124 | 0.834 | 175* |
| 32005 | Douglas | rural | 21,142 | 19,984 | 197 | 6,879 | 19.01M | 85,956 | -4,302 | 0.915 | 175* |
| 32007 | Elko | rural | 25,906 | 24,656 | 524 | 34,050 | 14.16M | 58,260 | 27,617 | 0.811 | 160 |
| 32009 | Esmeralda | rural | 397 | 448 | 56 | 3,670 | 0.54M | 56,960 | 17,766 | 0.843 | 175* |
| 32011 | Eureka | rural | 579 | 1,716 | 54 | 15,432 | 1.14M | 128,539 | 35,649 | 0.882 | 175* |
| 32013 | Humboldt | rural | 8,176 | 8,064 | 457 | 68,244 | 5.35M | 63,162 | -1,980 | 0.774 | 132 |
| 32015 | Lander | rural | 2,335 | 2,141 | 92 | 15,926 | 1.67M | 75,711 | 102,771 | 0.834 | 175* |
| 32017 | Lincoln | rural | 1,651 | 1,578 | 172 | 2,607 | 8.16M | 76,589 | 53,076 | 0.787 | 175* |
| 32019 | Lyon | suburb | 25,834 | 14,034 | 539 | 29,853 | 19.32M | 69,539 | 22,129 | 0.909 | 175* |
| 32021 | Mineral | rural | 1,648 | 1,602 | 47 | 2,014 | 2.81M | 160,922 | 59,750 | 0.834 | 175* |
| 32023 | Nye | rural | 16,552 | 15,175 | 144 | 5,702 | 16.79M | 73,804 | 218,419 | 0.855 | 175* |
| 32027 | Pershing | rural | 1,993 | 1,937 | 174 | 24,873 | 1.66M | 99,590 | 53,729 | 0.644 | 175* |
| 32029 | Storey | suburb | 1,352 | 5,945 | 0 | 102 | 5.05M | 0 | n/a | 0.834 | 175* |
| 32031 | Washoe | suburb | 244,367 | 245,177 | 357 | 4,979 | 174.65M | 51,315 | 30,000 | 0.977 | 175* |
| 32033 | White Pine | rural | 3,387 | 3,889 | 143 | 9,271 | 4.71M | 73,275 | 52,553 | 0.756 | 175* |
| 32510 | Carson City | suburb | 26,695 | 31,183 | 58 | 254 | 19.89M | 34,236 | 16,013 | 0.834 | 175* |
| EXT | External (out-of-state commuting) | external | 27,830 | 27,052 | 73 | 4,732 | 22.11M | 68,790 | n/a | 0.825 | n/a |

`*` filled, see above.
