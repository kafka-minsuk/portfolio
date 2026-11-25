# Arizona 2022 county data: validation report

Built 2026-11-25 by `python -m urqse.data.build_state AZ 2022`. 15 counties plus one external zone. Outputs: `county.parquet` (one row per zone, schema in `src/urqse/data/schema.py`) and `travel.npz` (`fips`, `t` minutes, `dist` km, rows in table order).

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
| cdl | USDA NASS Cropland Data Layer 2022, 30 m, clipped to state FIPS 04 | `AZ/CDL_2022_04.tif` | 2026-11-24 | https://nassgeodata.gmu.edu/axis2/services/CDLService/GetCDLFile?year=2022&fips=04 |
| acs_b08007 | ACS 2018-2022 5-year, table-based summary file B08007 | `US/acs/acsdt5y2022-b08007.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08007.dat |
| acs_b08604 | ACS 2018-2022 5-year, table-based summary file B08604 | `US/acs/acsdt5y2022-b08604.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08604.dat |
| acs_b05005 | ACS 2018-2022 5-year, table-based summary file B05005 | `US/acs/acsdt5y2022-b05005.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b05005.dat |
| ghsl_R5_C8 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C8.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C8.zip |
| ghsl_R5_C9 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C9.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C9.zip |
| ghsl_R6_C8 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R6_C8.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R6_C8.zip |
| ghsl_R6_C9 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R6_C9.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R6_C9.zip |
| nass | Quick Stats bulk economics file `qs.economics_20261121.txt.gz` (Census of Agriculture 2022; Cash Rents Survey 2022) | `qs.economics_20261121.txt.gz` (filtered copy `*_AZ.tsv.gz`) | see file | https://www.nass.usda.gov/sites/default/files/datasets/qs.economics_20261121.txt.gz |
| osrm | OSRM public demo server, car profile (OSM data as served on the build date) | `osrm/*.json` (1 cached block requests; the server caps a table at 100 coordinates) | 2026-11-25 | https://router.project-osrm.org/table/v1/driving |

## County sums against published state totals

| Column | Sum of counties | Published state value | Difference |
|---|---|---|---|
| PEP population | 7,359,197 | 7,359,197 | 0.000% |
| ACS workers by residence | 3,244,419 | 3,244,419 | 0.000% |
| ACS workers by workplace | 3,218,534 | 3,218,534 | 0.000% |
| ACS workers working out of state | 49,212 | 49,212 | 0.000% |
| BEA non-farm employment (L80) | 4,259,860 | 4,259,860 | 0.000% |
| BEA farm employment (L70) | 27,735 | 27,735 | 0.000% |
| BEA farm proprietors (L50) | 17,524 | 17,524 | 0.000% |
| BEA farm earnings $ (CAINC45 L370) | 965,062,000 | 965,062,000 | 0.000% |
| BEA farm wages + supplements $ (CAINC45 L350 + L360) | 554,873,000 | 554,873,000 | 0.000% |
| CoA hired farm labour expense $ | 611,170,000 | 611,169,000 | 0.000% |
| BEA non-farm earnings $ (CAINC5N L82) | 284,111,944,000 | 284,111,944,000 | 0.000% |
| ACS foreign born entered 2010+ | 214,665 | 214,665 | 0.000% |
| CoA owned acres | 21,298,619 | 23,574,017 | -9.652% |
| CoA rented-from-others acres | 1,715,046 | 1,951,070 | -12.097% |
| CoA land in farms, ha | 10,329,636 | 10,329,636 | 0.000% |
| CoA total cropland, ha | 494,445 | 494,445 | -0.000% |

## Model columns

- **N, HU, HA (jobs = resident workers).** Each county's BEA farm and non-farm job counts are scaled to its ACS count of workers by place of work (scale factor min 0.652, median 0.799, max 0.947; BEA counts jobs, ACS counts people by main job). Sum N = 3,267,746 = sum HU + HA = 3,267,746. Farm jobs after scaling: 21,177 (BEA 27,735). `# VERIFY` the scaling: part-time farm proprietors with an off-farm main job are counted once, in proportion to the county mix.
- **External zone.** Residents = out-of-state workers commuting in (ACS workplace total minus in-state residents working in state) = 23,327. Jobs = in-state residents working out of state = 49,212, split by the state farm share (HA = 324). Location: the 15 out-of-state counties within 1 km of the state (06025, 06065, 06071, 08083, 32003, 32017, 35003, 35006, 35017, 35023, 35031, 35045, 49025, 49037, 49053); travel time from a county to the zone is the OSRM time to the nearest of them. Floor space, farmland, farm labour earnings and owner share are state averages scaled to its workers / farm jobs; gateway weight 0 (immigrants settle in-state). `# VERIFY` all of these are conventions, not data, and `log(0)` in `immigration.arrival_shares` needs handling in M3.
- **TF (farmland, ha).** CDL 2022 crop, hay, fallow and tree-crop classes (codes 1-61, 66-77, 204-254), pixel-centre zonal sums on the 30 m Albers grid. State: 552,297 ha vs Census of Agriculture cropland 494,445 ha and land in farms 10,329,636 ha; county ratio TF / CoA cropland 0.00 to 1.76. Grassland/pasture (codes 62, 176) is kept separately (`pasture_ha`, 1,559,463 ha). County area covered by CDL pixels: 29,523,292 ha vs land area 29,436,585 ha (the difference is water). `# VERIFY` whether pasture belongs in T^F for livestock counties.
- **L (floor space, m^2).** GHSL GHS-BUILT-V 2020 epoch building volume / 3 m storey height (`# VERIFY` storey height; 2020 is the nearest epoch to 2022). State volume 9.12 km^3.
- **wA_obs_usd (farm labour earnings per farm worker).** Farm compensation (CAINC45 L350 wages and salaries + L360 supplements) per farm wage-and-salary job (CAEMP25N L70 - L50), mean of 2018 to 2022, each year relative to the state's non-farm earnings per non-farm job (CAINC5N L82 / CAEMP25N L80) and put at the 2022 value (66,695 $). That per-job wage prices every BEA farm job, proprietors included, giving the county farm labour bill `farm_labour_bill_usd`; wA_obs_usd = bill / HA, so it is per farm worker (ACS head) and the model's wage bill w_A H_A equals the bill in dollars. State: 48,185 $ per BEA farm job, 63,106 $ per farm worker; county range 30,588 to 71,131 $ per worker. State compensation per farm wage job by year: 2018 42,972 $, 2019 33,895 $, 2020 46,507 $, 2021 55,140 $, 2022 54,341 $. Proprietors are priced at the hired wage per job (the market price of farm labour in the county) rather than at a non-farm opportunity wage, which would assume away the farm/non-farm gap xi_A is meant to measure. `# VERIFY` the proprietor imputation: a BEA proprietor job is any sole proprietor or partner, many part-time. Contract labour (CoA 129,966,000 $) is left out: its workers are not BEA farm jobs (they are in agricultural support services, non-farm). Census of Agriculture hired labour expense (611,169,000 $ in 2022, column `hired_labor_coa_usd`) is 1.10x BEA farm compensation (554,873,000 $) and pays a different universe (every hired head, including workers on the farm under 150 days), so it is a comparison column, not the bill. `# VERIFY` that gap. The previous measure, BEA farm earnings (L370, wages + proprietors' income) per BEA farm job, is kept as `wA_bea_earn_usd`: state 34,796 $, county -3,425 to 111,673 $; it includes owner-operators' returns to owned land and capital, which spec §12.1 pays separately. The loader divides wA_obs_usd by state non-farm earnings per non-farm worker (sum over counties of non-farm earnings / HU = 88,858 $), so both sectors are per head. `# VERIFY` vintage mismatch: CAINC45/CAEMP25N are the 2023-11-16 release, CAINC5N the 2026 file (CAINC5N's revised 2022 farm earnings are 1,446,895,000 $ vs CAINC45 965,062,000 $).
- **omega.** Census of Agriculture 2022 owned / (owned + rented from others) acres in farms. State 0.925, county range 0.246 to 0.992.
- **cash_rent_usd_acre.** NASS Cash Rents Survey 2022, irrigated cropland. State 336 $/acre.
- **land_value_usd_acre.** Census of Agriculture 2022 estimated market value of land and buildings per acre (NASS does not publish annual county land values). State 883 $/acre.
- **gateway.** ACS foreign born who entered 2010 or later per resident worker, relative to the state ratio (mean 1 over workers). `# VERIFY` against spec §12.2 once the arrival block is calibrated. 0 counties have no recent foreign born in the ACS sample (), so their gateway weight is 0 (log(0) in arrival_shares).
- **kind.** core = the metropolitan county with the most non-farm jobs (Maricopa); suburb = other counties in a Metropolitan Statistical Area (OMB 2023) (7); rural = the rest (7). `# VERIFY` one core for a multi-metro state.
- **No farm sector** (spec §3.11): 0 counties have no BEA farm jobs.
- **Travel time t (min).** OSRM car durations between 2020 population-weighted county centres, as routed (not symmetrised). Off-diagonal median 290.0 min. Own-county time = 0.5214 x sqrt(land area) at the median effective speed of 56.7 straight-line km/h between counties (median 31.2 to 121.1 min). `# VERIFY` the own-county proxy. `dist` is great-circle km (road/straight median ratio 1.30).

## Suppressed cells and fills

| Variable | County | Rule |
|---|---|---|
| cash_rent_usd_acre | 04000  | the state publishes no non-irrigated cropland rent; NASS irrigated cropland rent used |
| omega | 04012 La Paz | state owner share |
| omega | 04019 Pima | state owner share |
| cash_rent_usd_acre | 04001 Apache | not published; NASS 'other (combined) counties' value = 112 $/acre |
| cash_rent_usd_acre | 04005 Coconino | not published; NASS 'other (combined) counties' value = 112 $/acre |
| cash_rent_usd_acre | 04007 Gila | not published; NASS 'other (combined) counties' value = 112 $/acre |
| cash_rent_usd_acre | 04011 Greenlee | not published; NASS 'other (combined) counties' value = 112 $/acre |
| cash_rent_usd_acre | 04015 Mohave | not published; NASS 'other (combined) counties' value = 112 $/acre |
| cash_rent_usd_acre | 04017 Navajo | not published; NASS 'other (combined) counties' value = 112 $/acre |
| cash_rent_usd_acre | 04019 Pima | not published; NASS 'other (combined) counties' value = 112 $/acre |
| cash_rent_usd_acre | 04023 Santa Cruz | not published; NASS 'other (combined) counties' value = 112 $/acre |
| cash_rent_usd_acre | 04025 Yavapai | not published; NASS 'other (combined) counties' value = 112 $/acre |
| owned_acres | 04012 La Paz | (D) in Census of Ag; see fills above |
| owned_acres | 04019 Pima | (D) in Census of Ag; see fills above |
| rented_acres | 04012 La Paz | (D) in Census of Ag; see fills above |
| rented_acres | 04019 Pima | (D) in Census of Ag; see fills above |

No BEA (D) cells for this state and year: CAEMP25N L50/70/80, CAINC45 L350/360/370 and CAINC5N L82 are published for every county (2018 to 2022 for the farm-wage lines).

## Coverage gaps and caveats

- ACS is the 5-year period estimate ending in the base year (no 1-year data for small counties); BEA and PEP are single-year. The external zone inherits ACS sampling error in the commuter totals.
- The Census API now requires a key, so ACS comes from the table-based summary files instead (same estimates).
- LODES (for the M3 PPML of kappa*lambda) and IRS SOI migration flows are not part of this build.
- Census of Agriculture is quinquennial (2022 matches the base year); the cash-rent survey is annual.
- x_km / y_km are NAD83 / UTM (EPSG:26912) at the state's middle longitude, for drawing only.
- No satellite population layer (GHS-POP) is used; census counts drive calibration (spec §8).

## County table

| FIPS | Name | Kind | N | HU | HA | TF ha | L m^2 | wA $/worker | BEA farm earnings $/job | omega | rent $/ac |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 04001 | Apache | rural | 18,073 | 14,183 | 3,364 | 115 | 12.22M | 65,090 | -3,425 | 0.985 | 112* |
| 04003 | Cochise | suburb | 46,755 | 44,575 | 1,270 | 85,290 | 57.89M | 66,114 | 33,042 | 0.636 | 145 |
| 04005 | Coconino | suburb | 66,342 | 66,456 | 1,598 | 125 | 36.01M | 59,190 | 8,727 | 0.992 | 112* |
| 04007 | Gila | rural | 18,434 | 17,242 | 144 | 305 | 23.94M | 43,098 | 24,804 | 0.949 | 112* |
| 04009 | Graham | rural | 13,864 | 13,099 | 384 | 28,172 | 13.76M | 57,756 | 10,356 | 0.973 | 175 |
| 04011 | Greenlee | rural | 4,129 | 5,689 | 126 | 1,521 | 2.12M | 30,588 | 55,066 | 0.610 | 112* |
| 04012 | La Paz | rural | 5,410 | 6,173 | 347 | 45,971 | 9.30M | 61,481 | 5,251 | 0.924 | 280 |
| 04013 | Maricopa | core | 2,146,216 | 2,188,991 | 4,168 | 127,230 | 1,916.74M | 71,131 | 53,606 | 0.512 | 209 |
| 04015 | Mohave | suburb | 74,493 | 64,612 | 381 | 7,751 | 127.48M | 62,339 | 61,173 | 0.888 | 112* |
| 04017 | Navajo | rural | 33,309 | 30,404 | 2,912 | 51 | 27.23M | 65,081 | 1,176 | 0.975 | 112* |
| 04019 | Pima | suburb | 461,211 | 460,115 | 861 | 16,814 | 492.04M | 61,682 | 37,250 | 0.924 | 112* |
| 04021 | Pinal | suburb | 167,486 | 108,484 | 1,938 | 162,078 | 122.92M | 51,433 | 69,875 | 0.795 | 192 |
| 04023 | Santa Cruz | rural | 18,616 | 17,072 | 325 | 525 | 21.89M | 47,632 | 20,603 | 0.428 | 112* |
| 04025 | Yavapai | suburb | 92,865 | 88,216 | 943 | 332 | 104.43M | 49,567 | 14,061 | 0.805 | 112* |
| 04027 | Yuma | suburb | 77,216 | 72,045 | 2,417 | 76,017 | 71.62M | 66,445 | 111,673 | 0.246 | 745 |
| EXT | External (out-of-state commuting) | external | 23,327 | 48,888 | 324 | 8,445 | 21.85M | 63,106 | n/a | 0.925 | n/a |

`*` filled, see above.
