# California 2022 county data: validation report

Built 2026-11-25 by `python -m urqse.data.build_state CA 2022`. 58 counties plus one external zone. Outputs: `county.parquet` (one row per zone, schema in `src/urqse/data/schema.py`) and `travel.npz` (`fips`, `t` minutes, `dist` km, rows in table order).

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
| cdl | USDA NASS Cropland Data Layer 2022, 30 m, clipped to state FIPS 06 | `CA/CDL_2022_06.tif` | 2026-11-25 | https://nassgeodata.gmu.edu/axis2/services/CDLService/GetCDLFile?year=2022&fips=06 |
| acs_b08007 | ACS 2018-2022 5-year, table-based summary file B08007 | `US/acs/acsdt5y2022-b08007.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08007.dat |
| acs_b08604 | ACS 2018-2022 5-year, table-based summary file B08604 | `US/acs/acsdt5y2022-b08604.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08604.dat |
| acs_b05005 | ACS 2018-2022 5-year, table-based summary file B05005 | `US/acs/acsdt5y2022-b05005.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b05005.dat |
| ghsl_R4_C8 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C8.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C8.zip |
| ghsl_R4_C9 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C9.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C9.zip |
| ghsl_R5_C8 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C8.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C8.zip |
| ghsl_R5_C9 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C9.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C9.zip |
| ghsl_R6_C8 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R6_C8.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R6_C8.zip |
| nass | Quick Stats bulk economics file `qs.economics_20261121.txt.gz` (Census of Agriculture 2022; Cash Rents Survey 2022) | `qs.economics_20261121.txt.gz` (filtered copy `*_CA.tsv.gz`) | see file | https://www.nass.usda.gov/sites/default/files/datasets/qs.economics_20261121.txt.gz |
| osrm | OSRM public demo server, car profile (OSM data as served on the build date) | `osrm/*.json` (4 cached block requests; the server caps a table at 100 coordinates) | 2026-11-25 | https://router.project-osrm.org/table/v1/driving |

## County sums against published state totals

| Column | Sum of counties | Published state value | Difference |
|---|---|---|---|
| PEP population | 39,029,342 | 39,029,342 | 0.000% |
| ACS workers by residence | 18,353,469 | 18,353,469 | 0.000% |
| ACS workers by workplace | 18,363,886 | 18,363,886 | 0.000% |
| ACS workers working out of state | 76,348 | 76,348 | 0.000% |
| BEA non-farm employment (L80) | 25,072,788 | 25,072,788 | 0.000% |
| BEA farm employment (L70) | 228,186 | 228,186 | 0.000% |
| BEA farm proprietors (L50) | 55,474 | 55,474 | 0.000% |
| BEA farm earnings $ (CAINC45 L370) | 16,004,335,000 | 16,004,335,000 | 0.000% |
| BEA farm wages + supplements $ (CAINC45 L350 + L360) | 8,304,674,000 | 8,304,674,000 | 0.000% |
| CoA hired farm labour expense $ | 9,575,439,000 | 9,575,439,000 | 0.000% |
| BEA non-farm earnings $ (CAINC5N L82) | 2,143,644,404,000 | 2,143,644,404,000 | 0.000% |
| ACS foreign born entered 2010+ | 2,044,637 | 2,044,637 | 0.000% |
| CoA owned acres | 14,226,983 | 14,239,499 | -0.088% |
| CoA rented-from-others acres | 9,946,600 | 9,951,105 | -0.045% |
| CoA land in farms, ha | 9,782,753 | 9,789,590 | -0.070% |
| CoA total cropland, ha | 4,066,878 | 4,066,936 | -0.001% |

## Model columns

- **N, HU, HA (jobs = resident workers).** Each county's BEA farm and non-farm job counts are scaled to its ACS count of workers by place of work (scale factor min 0.574, median 0.747, max 1.116; BEA counts jobs, ACS counts people by main job). Sum N = 18,440,234 = sum HU + HA = 18,440,234. Farm jobs after scaling: 169,692 (BEA 228,186). `# VERIFY` the scaling: part-time farm proprietors with an off-farm main job are counted once, in proportion to the county mix.
- **External zone.** Residents = out-of-state workers commuting in (ACS workplace total minus in-state residents working in state) = 86,765. Jobs = in-state residents working out of state = 76,348, split by the state farm share (HA = 705). Location: the 16 out-of-state counties within 1 km of the state (04012, 04015, 04027, 32003, 32005, 32009, 32019, 32021, 32023, 32031, 32510, 41015, 41029, 41033, 41035, 41037); travel time from a county to the zone is the OSRM time to the nearest of them. Floor space, farmland, farm labour earnings and owner share are state averages scaled to its workers / farm jobs; gateway weight 0 (immigrants settle in-state). `# VERIFY` all of these are conventions, not data, and `log(0)` in `immigration.arrival_shares` needs handling in M3.
- **TF (farmland, ha).** CDL 2022 crop, hay, fallow and tree-crop classes (codes 1-61, 66-77, 204-254), pixel-centre zonal sums on the 30 m Albers grid. State: 4,003,189 ha vs Census of Agriculture cropland 4,066,936 ha and land in farms 9,789,590 ha; county ratio TF / CoA cropland 0.05 to 2.19. Grassland/pasture (codes 62, 176) is kept separately (`pasture_ha`, 4,486,854 ha). County area covered by CDL pixels: 40,981,986 ha vs land area 40,367,362 ha (the difference is water). `# VERIFY` whether pasture belongs in T^F for livestock counties.
- **L (floor space, m^2).** GHSL GHS-BUILT-V 2020 epoch building volume / 3 m storey height (`# VERIFY` storey height; 2020 is the nearest epoch to 2022). State volume 38.70 km^3.
- **wA_obs_usd (farm labour earnings per farm worker).** Farm compensation (CAINC45 L350 wages and salaries + L360 supplements) per farm wage-and-salary job (CAEMP25N L70 - L50), mean of 2018 to 2022, each year relative to the state's non-farm earnings per non-farm job (CAINC5N L82 / CAEMP25N L80) and put at the 2022 value (85,497 $). That per-job wage prices every BEA farm job, proprietors included, giving the county farm labour bill `farm_labour_bill_usd`; wA_obs_usd = bill / HA, so it is per farm worker (ACS head) and the model's wage bill w_A H_A equals the bill in dollars. State: 46,937 $ per BEA farm job, 63,117 $ per farm worker; county range 32,037 to 95,176 $ per worker. State compensation per farm wage job by year: 2018 36,804 $, 2019 45,792 $, 2020 48,995 $, 2021 42,049 $, 2022 48,084 $. Proprietors are priced at the hired wage per job (the market price of farm labour in the county) rather than at a non-farm opportunity wage, which would assume away the farm/non-farm gap xi_A is meant to measure. `# VERIFY` the proprietor imputation: a BEA proprietor job is any sole proprietor or partner, many part-time. Contract labour (CoA 5,034,840,000 $) is left out: its workers are not BEA farm jobs (they are in agricultural support services, non-farm). Census of Agriculture hired labour expense (9,575,439,000 $ in 2022, column `hired_labor_coa_usd`) is 1.15x BEA farm compensation (8,304,674,000 $) and pays a different universe (every hired head, including workers on the farm under 150 days), so it is a comparison column, not the bill. `# VERIFY` that gap. The previous measure, BEA farm earnings (L370, wages + proprietors' income) per BEA farm job, is kept as `wA_bea_earn_usd`: state 70,137 $, county -57,041 to 146,796 $; it includes owner-operators' returns to owned land and capital, which spec §12.1 pays separately. The loader divides wA_obs_usd by state non-farm earnings per non-farm worker (sum over counties of non-farm earnings / HU = 117,820 $), so both sectors are per head. `# VERIFY` vintage mismatch: CAINC45/CAEMP25N are the 2023-11-16 release, CAINC5N the 2026 file (CAINC5N's revised 2022 farm earnings are 18,234,034,000 $ vs CAINC45 16,004,335,000 $).
- **omega.** Census of Agriculture 2022 owned / (owned + rented from others) acres in farms. State 0.589, county range 0.126 to 0.862.
- **cash_rent_usd_acre.** NASS Cash Rents Survey 2022, non-irrigated cropland. State 37 $/acre.
- **land_value_usd_acre.** Census of Agriculture 2022 estimated market value of land and buildings per acre (NASS does not publish annual county land values). State 13,131 $/acre.
- **gateway.** ACS foreign born who entered 2010 or later per resident worker, relative to the state ratio (mean 1 over workers). `# VERIFY` against spec §12.2 once the arrival block is calibrated. 0 counties have no recent foreign born in the ACS sample (), so their gateway weight is 0 (log(0) in arrival_shares).
- **kind.** core = the metropolitan county with the most non-farm jobs (Los Angeles); suburb = other counties in a Metropolitan Statistical Area (OMB 2023) (36); rural = the rest (21). `# VERIFY` one core for a multi-metro state.
- **No farm sector** (spec §3.11): 2 counties have no BEA farm jobs (Alpine, San Francisco); their farm wage is 0 and the model gives them no farm job option.
- **Travel time t (min).** OSRM car durations between 2020 population-weighted county centres, as routed (not symmetrised). Off-diagonal median 304.9 min. Own-county time = 0.5214 x sqrt(land area) at the median effective speed of 60.2 straight-line km/h between counties (median 5.7 to 118.5 min). `# VERIFY` the own-county proxy. `dist` is great-circle km (road/straight median ratio 1.25).

## Suppressed cells and fills

| Variable | County | Rule |
|---|---|---|
| HA_bea | 06003 Alpine | 0 farm jobs: no farm sector in the model (spec §3.11) |
| HA_bea | 06075 San Francisco | 0 farm jobs: no farm sector in the model (spec §3.11) |
| omega | 06003 Alpine | state owner share |
| omega | 06015 Del Norte | state owner share |
| omega | 06075 San Francisco | state owner share |
| cash_rent_usd_acre | 06003 Alpine | not published; NASS 'other (combined) counties' value = 37.5 $/acre |
| cash_rent_usd_acre | 06005 Amador | not published; NASS 'other (combined) counties' value = 37.5 $/acre |
| cash_rent_usd_acre | 06007 Butte | not published; NASS 'other (combined) counties' value = 37.5 $/acre |
| cash_rent_usd_acre | 06011 Colusa | not published; NASS 'other (combined) counties' value = 37.5 $/acre |
| cash_rent_usd_acre | 06013 Contra Costa | not published; NASS 'other (combined) counties' value = 37.5 $/acre |
| cash_rent_usd_acre | 06015 Del Norte | not published; NASS 'other (combined) counties' value = 37.5 $/acre |
| cash_rent_usd_acre | 06017 El Dorado | not published; NASS 'other (combined) counties' value = 37.5 $/acre |
| cash_rent_usd_acre | 06019 Fresno | not published; NASS 'other (combined) counties' value = 37.5 $/acre |
| cash_rent_usd_acre | 06021 Glenn | not published; NASS 'other (combined) counties' value = 37.5 $/acre |
| cash_rent_usd_acre | 06023 Humboldt | not published; NASS 'other (combined) counties' value = 37.5 $/acre |
| cash_rent_usd_acre | 06025 Imperial | not published; NASS 'other (combined) counties' value = 37.5 $/acre |
| cash_rent_usd_acre | 06027 Inyo | not published; NASS 'other (combined) counties' value = 37.5 $/acre |
| cash_rent_usd_acre | 06029 Kern | not published; NASS 'other (combined) counties' value = 37.5 $/acre |
| cash_rent_usd_acre | 06031 Kings | not published; NASS 'other (combined) counties' value = 37.5 $/acre |
| cash_rent_usd_acre | 06033 Lake | not published; NASS 'other (combined) counties' value = 37.5 $/acre |
| cash_rent_usd_acre | 06035 Lassen | not published; NASS 'other (combined) counties' value = 37.5 $/acre |
| cash_rent_usd_acre | 06037 Los Angeles | not published; NASS 'other (combined) counties' value = 37.5 $/acre |
| cash_rent_usd_acre | 06039 Madera | not published; NASS 'other (combined) counties' value = 37.5 $/acre |
| cash_rent_usd_acre | 06047 Merced | not published; NASS 'other (combined) counties' value = 37.5 $/acre |
| cash_rent_usd_acre | 06051 Mono | not published; NASS 'other (combined) counties' value = 37.5 $/acre |
| cash_rent_usd_acre | 06053 Monterey | not published; NASS 'other (combined) counties' value = 37.5 $/acre |
| cash_rent_usd_acre | 06055 Napa | not published; NASS 'other (combined) counties' value = 37.5 $/acre |
| cash_rent_usd_acre | 06057 Nevada | not published; NASS 'other (combined) counties' value = 37.5 $/acre |
| cash_rent_usd_acre | 06059 Orange | not published; NASS 'other (combined) counties' value = 37.5 $/acre |
| cash_rent_usd_acre | 06063 Plumas | not published; NASS 'other (combined) counties' value = 37.5 $/acre |
| cash_rent_usd_acre | 06065 Riverside | not published; NASS 'other (combined) counties' value = 37.5 $/acre |
| cash_rent_usd_acre | 06067 Sacramento | not published; NASS 'other (combined) counties' value = 37.5 $/acre |
| cash_rent_usd_acre | 06071 San Bernardino | not published; NASS 'other (combined) counties' value = 37.5 $/acre |
| cash_rent_usd_acre | 06073 San Diego | not published; NASS 'other (combined) counties' value = 37.5 $/acre |
| cash_rent_usd_acre | 06075 San Francisco | not published; NASS 'other (combined) counties' value = 37.5 $/acre |
| cash_rent_usd_acre | 06077 San Joaquin | not published; NASS 'other (combined) counties' value = 37.5 $/acre |
| cash_rent_usd_acre | 06079 San Luis Obispo | not published; NASS 'other (combined) counties' value = 37.5 $/acre |
| cash_rent_usd_acre | 06081 San Mateo | not published; NASS 'other (combined) counties' value = 37.5 $/acre |
| cash_rent_usd_acre | 06083 Santa Barbara | not published; NASS 'other (combined) counties' value = 37.5 $/acre |
| cash_rent_usd_acre | 06087 Santa Cruz | not published; NASS 'other (combined) counties' value = 37.5 $/acre |
| cash_rent_usd_acre | 06091 Sierra | not published; NASS 'other (combined) counties' value = 37.5 $/acre |
| cash_rent_usd_acre | 06093 Siskiyou | not published; NASS 'other (combined) counties' value = 37.5 $/acre |
| cash_rent_usd_acre | 06099 Stanislaus | not published; NASS 'other (combined) counties' value = 37.5 $/acre |
| cash_rent_usd_acre | 06101 Sutter | not published; NASS 'other (combined) counties' value = 37.5 $/acre |
| cash_rent_usd_acre | 06103 Tehama | not published; NASS 'other (combined) counties' value = 37.5 $/acre |
| cash_rent_usd_acre | 06105 Trinity | not published; NASS 'other (combined) counties' value = 37.5 $/acre |
| cash_rent_usd_acre | 06107 Tulare | not published; NASS 'other (combined) counties' value = 37.5 $/acre |
| cash_rent_usd_acre | 06109 Tuolumne | not published; NASS 'other (combined) counties' value = 37.5 $/acre |
| cash_rent_usd_acre | 06111 Ventura | not published; NASS 'other (combined) counties' value = 37.5 $/acre |
| cash_rent_usd_acre | 06113 Yolo | not published; NASS 'other (combined) counties' value = 37.5 $/acre |
| cash_rent_usd_acre | 06115 Yuba | not published; NASS 'other (combined) counties' value = 37.5 $/acre |
| owned_acres | 06003 Alpine | (D) in Census of Ag; see fills above |
| owned_acres | 06015 Del Norte | (D) in Census of Ag; see fills above |
| owned_acres | 06075 San Francisco | (D) in Census of Ag; see fills above |
| rented_acres | 06015 Del Norte | (D) in Census of Ag; see fills above |
| rented_acres | 06075 San Francisco | (D) in Census of Ag; see fills above |

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
| 06001 | Alameda | suburb | 827,327 | 818,838 | 672 | 3,886 | 471.51M | 95,176 | 87,482 | 0.398 | 20 |
| 06003 | Alpine | rural | 638 | 666 | 0 | 352 | 0.36M | 0 | n/a | 0.589 | 38* |
| 06005 | Amador | rural | 15,508 | 13,503 | 333 | 2,879 | 11.71M | 56,939 | 7,090 | 0.560 | 38* |
| 06007 | Butte | suburb | 91,975 | 89,739 | 2,637 | 115,102 | 85.15M | 63,615 | 44,491 | 0.602 | 38* |
| 06009 | Calaveras | rural | 17,014 | 11,015 | 335 | 993 | 15.21M | 69,942 | -3,266 | 0.444 | 11 |
| 06011 | Colusa | rural | 9,477 | 7,755 | 1,633 | 139,389 | 9.99M | 70,287 | 70,020 | 0.456 | 38* |
| 06013 | Contra Costa | suburb | 556,391 | 435,291 | 688 | 20,728 | 373.40M | 76,791 | 55,564 | 0.408 | 38* |
| 06015 | Del Norte | rural | 9,607 | 9,998 | 251 | 127 | 7.54M | 45,666 | 63,582 | 0.589 | 38* |
| 06017 | El Dorado | suburb | 86,127 | 66,321 | 830 | 1,292 | 53.97M | 61,505 | -5,942 | 0.546 | 38* |
| 06019 | Fresno | suburb | 411,511 | 400,281 | 13,040 | 525,445 | 366.56M | 58,513 | 77,145 | 0.687 | 38* |
| 06021 | Glenn | rural | 12,118 | 9,172 | 1,899 | 116,984 | 14.29M | 62,960 | 53,754 | 0.534 | 38* |
| 06023 | Humboldt | rural | 58,327 | 57,445 | 1,174 | 2,657 | 41.87M | 63,492 | 61,053 | 0.520 | 38* |
| 06025 | Imperial | suburb | 59,335 | 54,021 | 2,648 | 187,936 | 40.29M | 67,917 | 146,796 | 0.272 | 38* |
| 06027 | Inyo | rural | 8,094 | 8,463 | 77 | 1,293 | 5.59M | 47,533 | 115,889 | 0.126 | 38* |
| 06029 | Kern | suburb | 351,806 | 337,716 | 12,650 | 415,683 | 341.78M | 63,090 | 85,848 | 0.563 | 38* |
| 06031 | Kings | suburb | 56,893 | 53,232 | 3,773 | 257,788 | 53.44M | 63,202 | 104,109 | 0.774 | 38* |
| 06033 | Lake | rural | 24,313 | 19,165 | 637 | 6,800 | 22.54M | 47,253 | 17,113 | 0.600 | 38* |
| 06035 | Lassen | rural | 8,909 | 9,040 | 447 | 33,639 | 9.40M | 66,258 | 52,967 | 0.573 | 38* |
| 06037 | Los Angeles | core | 4,737,721 | 4,856,071 | 2,997 | 1,622 | 3,194.61M | 71,892 | 50,712 | 0.239 | 38* |
| 06039 | Madera | suburb | 57,706 | 49,251 | 2,687 | 153,047 | 44.10M | 69,816 | 140,751 | 0.753 | 38* |
| 06041 | Marin | suburb | 126,445 | 130,898 | 277 | 3,296 | 78.60M | 71,250 | 107,971 | 0.537 | 83 |
| 06043 | Mariposa | rural | 7,072 | 7,298 | 255 | 251 | 5.37M | 32,037 | 45,003 | 0.379 | 45 |
| 06045 | Mendocino | rural | 36,841 | 36,464 | 1,288 | 9,336 | 29.26M | 55,729 | 23,841 | 0.623 | 32 |
| 06047 | Merced | suburb | 106,381 | 79,467 | 7,150 | 233,483 | 86.16M | 61,799 | 109,598 | 0.644 | 38* |
| 06049 | Modoc | rural | 3,184 | 2,419 | 342 | 56,869 | 4.56M | 70,260 | 106,134 | 0.725 | 62 |
| 06051 | Mono | rural | 7,400 | 7,759 | 67 | 2,483 | 5.65M | 33,739 | 140,351 | 0.554 | 38* |
| 06053 | Monterey | suburb | 189,526 | 168,860 | 12,842 | 72,370 | 119.87M | 67,070 | 80,374 | 0.634 | 38* |
| 06055 | Napa | suburb | 66,906 | 76,462 | 2,365 | 18,698 | 49.76M | 82,991 | 44,097 | 0.819 | 38* |
| 06057 | Nevada | rural | 44,318 | 40,051 | 448 | 376 | 26.23M | 62,837 | 4,599 | 0.498 | 38* |
| 06059 | Orange | suburb | 1,563,277 | 1,648,454 | 878 | 693 | 1,042.85M | 69,212 | 59,554 | 0.673 | 38* |
| 06061 | Placer | suburb | 187,335 | 193,373 | 919 | 19,697 | 140.04M | 58,351 | 13,640 | 0.441 | 48 |
| 06063 | Plumas | rural | 7,380 | 7,018 | 87 | 7,765 | 7.11M | 67,615 | -13,350 | 0.862 | 38* |
| 06065 | Riverside | suburb | 1,048,421 | 876,952 | 5,261 | 88,024 | 859.89M | 59,384 | 58,235 | 0.592 | 38* |
| 06067 | Sacramento | suburb | 727,094 | 712,703 | 2,092 | 80,383 | 493.25M | 61,254 | 60,640 | 0.465 | 38* |
| 06069 | San Benito | suburb | 30,710 | 18,205 | 810 | 14,887 | 18.61M | 70,797 | 57,981 | 0.537 | 17 |
| 06071 | San Bernardino | suburb | 946,303 | 890,739 | 1,844 | 5,486 | 834.58M | 59,100 | 73,715 | 0.607 | 38* |
| 06073 | San Diego | suburb | 1,622,954 | 1,650,491 | 8,585 | 10,193 | 1,132.74M | 65,476 | 41,744 | 0.790 | 38* |
| 06075 | San Francisco | suburb | 487,526 | 681,323 | 0 | 68 | 144.28M | 0 | n/a | 0.589 | 38* |
| 06077 | San Joaquin | suburb | 325,292 | 286,684 | 6,874 | 233,709 | 273.82M | 63,008 | 75,540 | 0.570 | 38* |
| 06079 | San Luis Obispo | suburb | 129,192 | 128,166 | 2,570 | 54,823 | 118.88M | 64,011 | 43,624 | 0.608 | 38* |
| 06081 | San Mateo | suburb | 393,729 | 417,704 | 1,079 | 907 | 221.18M | 85,721 | 74,726 | 0.658 | 38* |
| 06083 | Santa Barbara | suburb | 204,766 | 203,476 | 10,173 | 27,918 | 139.11M | 61,827 | 53,911 | 0.577 | 38* |
| 06085 | Santa Clara | suburb | 975,427 | 1,096,875 | 1,772 | 7,274 | 587.80M | 74,784 | 59,362 | 0.489 | 20 |
| 06087 | Santa Cruz | suburb | 129,470 | 115,165 | 4,895 | 3,278 | 68.34M | 59,736 | 49,357 | 0.395 | 38* |
| 06089 | Shasta | suburb | 74,304 | 72,875 | 1,328 | 11,674 | 85.36M | 72,928 | 28,198 | 0.579 | 20 |
| 06091 | Sierra | rural | 1,216 | 857 | 33 | 2,150 | 0.80M | 45,425 | 38,545 | 0.735 | 38* |
| 06093 | Siskiyou | rural | 15,974 | 15,140 | 966 | 75,668 | 16.04M | 62,564 | 69,140 | 0.712 | 38* |
| 06095 | Solano | suburb | 209,755 | 160,611 | 1,344 | 79,333 | 151.10M | 63,000 | 53,246 | 0.341 | 34 |
| 06097 | Sonoma | suburb | 242,102 | 225,062 | 4,370 | 33,445 | 161.91M | 68,286 | 32,302 | 0.614 | 57 |
| 06099 | Stanislaus | suburb | 229,451 | 196,393 | 7,168 | 165,523 | 219.87M | 68,363 | 94,144 | 0.635 | 38* |
| 06101 | Sutter | suburb | 41,767 | 32,964 | 2,458 | 121,254 | 32.83M | 56,166 | 47,267 | 0.534 | 38* |
| 06103 | Tehama | rural | 24,769 | 20,443 | 1,756 | 42,943 | 25.89M | 62,468 | 40,124 | 0.463 | 38* |
| 06105 | Trinity | rural | 5,176 | 4,985 | 230 | 387 | 4.70M | 57,129 | 71,209 | 0.591 | 38* |
| 06107 | Tulare | suburb | 184,620 | 164,006 | 11,272 | 307,297 | 159.18M | 58,890 | 109,774 | 0.741 | 38* |
| 06109 | Tuolumne | rural | 19,951 | 20,042 | 252 | 348 | 16.86M | 84,707 | -57,041 | 0.482 | 38* |
| 06111 | Ventura | suburb | 402,639 | 354,167 | 13,396 | 21,665 | 277.46M | 53,494 | 51,057 | 0.637 | 38* |
| 06113 | Yolo | suburb | 100,577 | 117,423 | 1,909 | 154,730 | 78.11M | 68,210 | 62,673 | 0.502 | 38* |
| 06115 | Yuba | suburb | 33,422 | 25,240 | 926 | 46,863 | 19.63M | 58,737 | 36,830 | 0.668 | 38* |
| EXT | External (out-of-state commuting) | external | 86,765 | 75,643 | 705 | 16,643 | 60.99M | 63,117 | n/a | 0.589 | n/a |

`*` filled, see above.
