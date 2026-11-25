# Florida 2022 county data: validation report

Built 2026-11-25 by `python -m urqse.data.build_state FL 2022`. 67 counties plus one external zone. Outputs: `county.parquet` (one row per zone, schema in `src/urqse/data/schema.py`) and `travel.npz` (`fips`, `t` minutes, `dist` km, rows in table order).

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
| cdl | USDA NASS Cropland Data Layer 2022, 30 m, clipped to state FIPS 12 | `FL/CDL_2022_12.tif` | 2026-11-25 | https://nassgeodata.gmu.edu/axis2/services/CDLService/GetCDLFile?year=2022&fips=12 |
| acs_b08007 | ACS 2018-2022 5-year, table-based summary file B08007 | `US/acs/acsdt5y2022-b08007.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08007.dat |
| acs_b08604 | ACS 2018-2022 5-year, table-based summary file B08604 | `US/acs/acsdt5y2022-b08604.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08604.dat |
| acs_b05005 | ACS 2018-2022 5-year, table-based summary file B05005 | `US/acs/acsdt5y2022-b05005.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b05005.dat |
| ghsl_R6_C11 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R6_C11.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R6_C11.zip |
| ghsl_R7_C11 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R7_C11.zip` | 2026-11-25 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R7_C11.zip |
| nass | Quick Stats bulk economics file `qs.economics_20261121.txt.gz` (Census of Agriculture 2022; Cash Rents Survey 2022) | `qs.economics_20261121.txt.gz` (filtered copy `*_FL.tsv.gz`) | see file | https://www.nass.usda.gov/sites/default/files/datasets/qs.economics_20261121.txt.gz |
| osrm | OSRM public demo server, car profile (OSM data as served on the build date) | `osrm/*.json` (4 cached block requests; the server caps a table at 100 coordinates) | 2026-11-25 | https://router.project-osrm.org/table/v1/driving |

## County sums against published state totals

| Column | Sum of counties | Published state value | Difference |
|---|---|---|---|
| PEP population | 22,244,823 | 22,244,823 | 0.000% |
| ACS workers by residence | 9,897,435 | 9,897,435 | 0.000% |
| ACS workers by workplace | 9,842,957 | 9,842,957 | 0.000% |
| ACS workers working out of state | 119,468 | 119,468 | 0.000% |
| BEA non-farm employment (L80) | 14,157,445 | 14,157,445 | 0.000% |
| BEA farm employment (L70) | 69,807 | 69,807 | 0.000% |
| BEA farm proprietors (L50) | 38,372 | 38,372 | 0.000% |
| BEA farm earnings $ (CAINC45 L370) | 2,509,338,000 | 2,509,338,000 | 0.000% |
| BEA farm wages + supplements $ (CAINC45 L350 + L360) | 1,649,855,000 | 1,649,855,000 | 0.000% |
| CoA hired farm labour expense $ | 1,969,084,000 | 1,969,084,000 | 0.000% |
| BEA non-farm earnings $ (CAINC5N L82) | 842,469,208,000 | 842,469,208,000 | 0.000% |
| ACS foreign born entered 2010+ | 1,376,694 | 1,376,694 | 0.000% |
| CoA owned acres | 6,114,480 | 6,341,200 | -3.575% |
| CoA rented-from-others acres | 3,360,200 | 3,360,200 | 0.000% |
| CoA land in farms, ha | 3,832,565 | 3,926,017 | -2.380% |
| CoA total cropland, ha | 1,163,419 | 1,163,419 | -0.000% |

## Model columns

- **N, HU, HA (jobs = resident workers).** Each county's BEA farm and non-farm job counts are scaled to its ACS count of workers by place of work (scale factor min 0.529, median 0.716, max 0.907; BEA counts jobs, ACS counts people by main job). Sum N = 9,962,425 = sum HU + HA = 9,962,425. Farm jobs after scaling: 48,944 (BEA 69,807). `# VERIFY` the scaling: part-time farm proprietors with an off-farm main job are counted once, in proportion to the county mix.
- **External zone.** Residents = out-of-state workers commuting in (ACS workplace total minus in-state residents working in state) = 64,990. Jobs = in-state residents working out of state = 119,468, split by the state farm share (HA = 594). Location: the 16 out-of-state counties within 1 km of the state (01003, 01039, 01053, 01061, 01069, 13027, 13039, 13049, 13065, 13087, 13101, 13131, 13185, 13253, 13275, 13299); travel time from a county to the zone is the OSRM time to the nearest of them. Floor space, farmland, farm labour earnings and owner share are state averages scaled to its workers / farm jobs; gateway weight 0 (immigrants settle in-state). `# VERIFY` all of these are conventions, not data, and `log(0)` in `immigration.arrival_shares` needs handling in M3.
- **TF (farmland, ha).** CDL 2022 crop, hay, fallow and tree-crop classes (codes 1-61, 66-77, 204-254), pixel-centre zonal sums on the 30 m Albers grid. State: 1,065,667 ha vs Census of Agriculture cropland 1,163,419 ha and land in farms 3,926,017 ha; county ratio TF / CoA cropland 0.13 to 6.56. Grassland/pasture (codes 62, 176) is kept separately (`pasture_ha`, 1,796,135 ha). County area covered by CDL pixels: 15,085,566 ha vs land area 13,896,282 ha (the difference is water). `# VERIFY` whether pasture belongs in T^F for livestock counties.
- **L (floor space, m^2).** GHSL GHS-BUILT-V 2020 epoch building volume / 3 m storey height (`# VERIFY` storey height; 2020 is the nearest epoch to 2022). State volume 24.64 km^3.
- **wA_obs_usd (farm labour earnings per farm worker).** Farm compensation (CAINC45 L350 wages and salaries + L360 supplements) per farm wage-and-salary job (CAEMP25N L70 - L50), mean of 2018 to 2022, each year relative to the state's non-farm earnings per non-farm job (CAINC5N L82 / CAEMP25N L80) and put at the 2022 value (59,507 $). That per-job wage prices every BEA farm job, proprietors included, giving the county farm labour bill `farm_labour_bill_usd`; wA_obs_usd = bill / HA, so it is per farm worker (ACS head) and the model's wage bill w_A H_A equals the bill in dollars. State: 48,015 $ per BEA farm job, 68,483 $ per farm worker; county range 40,655 to 110,907 $ per worker. State compensation per farm wage job by year: 2018 33,322 $, 2019 36,758 $, 2020 41,341 $, 2021 62,623 $, 2022 52,485 $. Proprietors are priced at the hired wage per job (the market price of farm labour in the county) rather than at a non-farm opportunity wage, which would assume away the farm/non-farm gap xi_A is meant to measure. `# VERIFY` the proprietor imputation: a BEA proprietor job is any sole proprietor or partner, many part-time. Contract labour (CoA 602,946,000 $) is left out: its workers are not BEA farm jobs (they are in agricultural support services, non-farm). Census of Agriculture hired labour expense (1,969,084,000 $ in 2022, column `hired_labor_coa_usd`) is 1.19x BEA farm compensation (1,649,855,000 $) and pays a different universe (every hired head, including workers on the farm under 150 days), so it is a comparison column, not the bill. `# VERIFY` that gap. The previous measure, BEA farm earnings (L370, wages + proprietors' income) per BEA farm job, is kept as `wA_bea_earn_usd`: state 35,947 $, county -8,129 to 98,833 $; it includes owner-operators' returns to owned land and capital, which spec §12.1 pays separately. The loader divides wA_obs_usd by state non-farm earnings per non-farm worker (sum over counties of non-farm earnings / HU = 86,019 $), so both sectors are per head. `# VERIFY` vintage mismatch: CAINC45/CAEMP25N are the 2023-11-16 release, CAINC5N the 2026 file (CAINC5N's revised 2022 farm earnings are 2,710,468,000 $ vs CAINC45 2,509,338,000 $).
- **omega.** Census of Agriculture 2022 owned / (owned + rented from others) acres in farms. State 0.645, county range 0.280 to 0.994.
- **cash_rent_usd_acre.** NASS Cash Rents Survey 2022, non-irrigated cropland. State 57 $/acre.
- **land_value_usd_acre.** Census of Agriculture 2022 estimated market value of land and buildings per acre (NASS does not publish annual county land values). State 7,319 $/acre.
- **gateway.** ACS foreign born who entered 2010 or later per resident worker, relative to the state ratio (mean 1 over workers). `# VERIFY` against spec §12.2 once the arrival block is calibrated. 0 counties have no recent foreign born in the ACS sample (), so their gateway weight is 0 (log(0) in arrival_shares).
- **kind.** core = the metropolitan county with the most non-farm jobs (Miami-Dade); suburb = other counties in a Metropolitan Statistical Area (OMB 2023) (44); rural = the rest (22). `# VERIFY` one core for a multi-metro state.
- **No farm sector** (spec §3.11): 3 counties have no BEA farm jobs (Franklin, Gulf, Monroe); their farm wage is 0 and the model gives them no farm job option.
- **Travel time t (min).** OSRM car durations between 2020 population-weighted county centres, as routed (not symmetrised). Off-diagonal median 245.3 min. Own-county time = 0.5214 x sqrt(land area) at the median effective speed of 63.8 straight-line km/h between counties (median 12.3 to 35.3 min). `# VERIFY` the own-county proxy. `dist` is great-circle km (road/straight median ratio 1.21).

## Suppressed cells and fills

| Variable | County | Rule |
|---|---|---|
| HA_bea | 12037 Franklin | 0 farm jobs: no farm sector in the model (spec §3.11) |
| HA_bea | 12045 Gulf | 0 farm jobs: no farm sector in the model (spec §3.11) |
| HA_bea | 12087 Monroe | 0 farm jobs: no farm sector in the model (spec §3.11) |
| omega | 12037 Franklin | state owner share |
| omega | 12045 Gulf | state owner share |
| omega | 12087 Monroe | state owner share |
| omega | 12129 Wakulla | state owner share |
| cash_rent_usd_acre | 12003 Baker | not published; NASS 'other (combined) counties' value = 36 $/acre |
| cash_rent_usd_acre | 12005 Bay | not published; NASS 'other (combined) counties' value = 36 $/acre |
| cash_rent_usd_acre | 12009 Brevard | not published; NASS 'other (combined) counties' value = 36 $/acre |
| cash_rent_usd_acre | 12011 Broward | not published; NASS 'other (combined) counties' value = 36 $/acre |
| cash_rent_usd_acre | 12015 Charlotte | not published; NASS 'other (combined) counties' value = 36 $/acre |
| cash_rent_usd_acre | 12019 Clay | not published; NASS 'other (combined) counties' value = 36 $/acre |
| cash_rent_usd_acre | 12021 Collier | not published; NASS 'other (combined) counties' value = 36 $/acre |
| cash_rent_usd_acre | 12029 Dixie | not published; NASS 'other (combined) counties' value = 36 $/acre |
| cash_rent_usd_acre | 12031 Duval | not published; NASS 'other (combined) counties' value = 36 $/acre |
| cash_rent_usd_acre | 12035 Flagler | not published; NASS 'other (combined) counties' value = 36 $/acre |
| cash_rent_usd_acre | 12037 Franklin | not published; NASS 'other (combined) counties' value = 36 $/acre |
| cash_rent_usd_acre | 12039 Gadsden | not published; NASS 'other (combined) counties' value = 36 $/acre |
| cash_rent_usd_acre | 12043 Glades | not published; NASS 'other (combined) counties' value = 36 $/acre |
| cash_rent_usd_acre | 12045 Gulf | not published; NASS 'other (combined) counties' value = 36 $/acre |
| cash_rent_usd_acre | 12051 Hendry | not published; NASS 'other (combined) counties' value = 36 $/acre |
| cash_rent_usd_acre | 12053 Hernando | not published; NASS 'other (combined) counties' value = 36 $/acre |
| cash_rent_usd_acre | 12055 Highlands | not published; NASS 'other (combined) counties' value = 36 $/acre |
| cash_rent_usd_acre | 12061 Indian River | not published; NASS 'other (combined) counties' value = 36 $/acre |
| cash_rent_usd_acre | 12069 Lake | not published; NASS 'other (combined) counties' value = 36 $/acre |
| cash_rent_usd_acre | 12073 Leon | not published; NASS 'other (combined) counties' value = 36 $/acre |
| cash_rent_usd_acre | 12077 Liberty | not published; NASS 'other (combined) counties' value = 36 $/acre |
| cash_rent_usd_acre | 12081 Manatee | not published; NASS 'other (combined) counties' value = 36 $/acre |
| cash_rent_usd_acre | 12085 Martin | not published; NASS 'other (combined) counties' value = 36 $/acre |
| cash_rent_usd_acre | 12086 Miami-Dade | not published; NASS 'other (combined) counties' value = 36 $/acre |
| cash_rent_usd_acre | 12087 Monroe | not published; NASS 'other (combined) counties' value = 36 $/acre |
| cash_rent_usd_acre | 12089 Nassau | not published; NASS 'other (combined) counties' value = 36 $/acre |
| cash_rent_usd_acre | 12093 Okeechobee | not published; NASS 'other (combined) counties' value = 36 $/acre |
| cash_rent_usd_acre | 12095 Orange | not published; NASS 'other (combined) counties' value = 36 $/acre |
| cash_rent_usd_acre | 12097 Osceola | not published; NASS 'other (combined) counties' value = 36 $/acre |
| cash_rent_usd_acre | 12103 Pinellas | not published; NASS 'other (combined) counties' value = 36 $/acre |
| cash_rent_usd_acre | 12105 Polk | not published; NASS 'other (combined) counties' value = 36 $/acre |
| cash_rent_usd_acre | 12107 Putnam | not published; NASS 'other (combined) counties' value = 36 $/acre |
| cash_rent_usd_acre | 12109 St. Johns | not published; NASS 'other (combined) counties' value = 36 $/acre |
| cash_rent_usd_acre | 12111 St. Lucie | not published; NASS 'other (combined) counties' value = 36 $/acre |
| cash_rent_usd_acre | 12115 Sarasota | not published; NASS 'other (combined) counties' value = 36 $/acre |
| cash_rent_usd_acre | 12117 Seminole | not published; NASS 'other (combined) counties' value = 36 $/acre |
| cash_rent_usd_acre | 12123 Taylor | not published; NASS 'other (combined) counties' value = 36 $/acre |
| cash_rent_usd_acre | 12125 Union | not published; NASS 'other (combined) counties' value = 36 $/acre |
| cash_rent_usd_acre | 12127 Volusia | not published; NASS 'other (combined) counties' value = 36 $/acre |
| cash_rent_usd_acre | 12129 Wakulla | not published; NASS 'other (combined) counties' value = 36 $/acre |
| cash_rent_usd_acre | 12131 Walton | not published; NASS 'other (combined) counties' value = 36 $/acre |
| land_value_usd_acre | 12045 Gulf | (D) in Census of Ag; see fills above |
| land_value_usd_acre | 12087 Monroe | (D) in Census of Ag; see fills above |
| owned_acres | 12037 Franklin | (D) in Census of Ag; see fills above |
| owned_acres | 12045 Gulf | (D) in Census of Ag; see fills above |
| owned_acres | 12087 Monroe | (D) in Census of Ag; see fills above |
| owned_acres | 12129 Wakulla | (D) in Census of Ag; see fills above |

## Coverage gaps and caveats

- ACS is the 5-year period estimate ending in the base year (no 1-year data for small counties); BEA and PEP are single-year. The external zone inherits ACS sampling error in the commuter totals.
- The Census API now requires a key, so ACS comes from the table-based summary files instead (same estimates).
- LODES (for the M3 PPML of kappa*lambda) and IRS SOI migration flows are not part of this build.
- Census of Agriculture is quinquennial (2022 matches the base year); the cash-rent survey is annual.
- x_km / y_km are NAD83 / UTM (EPSG:26917) at the state's middle longitude, for drawing only.
- No satellite population layer (GHS-POP) is used; census counts drive calibration (spec §8).

## County table

| FIPS | Name | Kind | N | HU | HA | TF ha | L m^2 | wA $/worker | BEA farm earnings $/job | omega | rent $/ac |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 12001 | Alachua | suburb | 130,463 | 146,563 | 1,656 | 22,440 | 83.82M | 59,822 | 19,634 | 0.673 | 44 |
| 12003 | Baker | suburb | 11,312 | 8,239 | 280 | 878 | 9.40M | 40,655 | 17,162 | 0.914 | 36* |
| 12005 | Bay | suburb | 85,923 | 88,854 | 94 | 1,876 | 106.97M | 72,232 | 14,806 | 0.994 | 36* |
| 12007 | Bradford | rural | 10,616 | 8,117 | 395 | 1,777 | 7.90M | 65,677 | 4,472 | 0.435 | 24 |
| 12009 | Brevard | suburb | 269,483 | 258,869 | 395 | 2,119 | 255.11M | 65,089 | 25,300 | 0.435 | 36* |
| 12011 | Broward | suburb | 965,176 | 887,600 | 405 | 339 | 681.39M | 74,093 | 28,803 | 0.280 | 36* |
| 12013 | Calhoun | rural | 4,482 | 2,989 | 182 | 15,101 | 5.04M | 71,690 | 36,113 | 0.895 | 87 |
| 12015 | Charlotte | suburb | 66,322 | 60,465 | 276 | 9,609 | 91.15M | 66,294 | 41,969 | 0.447 | 36* |
| 12017 | Citrus | suburb | 48,459 | 42,108 | 382 | 4,374 | 61.60M | 56,431 | -2,913 | 0.647 | 17 |
| 12019 | Clay | suburb | 103,613 | 64,290 | 253 | 332 | 75.86M | 76,172 | -8,129 | 0.800 | 36* |
| 12021 | Collier | suburb | 158,573 | 167,883 | 958 | 18,599 | 187.90M | 71,909 | 58,005 | 0.609 | 36* |
| 12023 | Columbia | rural | 26,940 | 25,260 | 712 | 13,571 | 24.86M | 76,248 | 7,502 | 0.902 | 52 |
| 12027 | DeSoto | rural | 12,092 | 10,160 | 819 | 37,929 | 10.72M | 72,863 | 46,068 | 0.532 | 34 |
| 12029 | Dixie | rural | 5,345 | 3,680 | 168 | 5,425 | 4.37M | 74,055 | 13,344 | 0.634 | 36* |
| 12031 | Duval | suburb | 489,335 | 569,278 | 469 | 602 | 464.64M | 63,841 | 24,626 | 0.923 | 36* |
| 12033 | Escambia | suburb | 146,059 | 163,410 | 538 | 13,984 | 124.49M | 61,631 | 7,216 | 0.607 | 86 |
| 12035 | Flagler | suburb | 47,069 | 33,869 | 150 | 1,745 | 53.73M | 70,208 | 36,145 | 0.569 | 36* |
| 12037 | Franklin | rural | 4,116 | 3,826 | 0 | 40 | 6.42M | 0 | n/a | 0.654 | 36* |
| 12039 | Gadsden | suburb | 16,195 | 10,036 | 2,218 | 7,216 | 11.30M | 91,785 | 47,533 | 0.945 | 36* |
| 12041 | Gilchrist | suburb | 7,396 | 4,143 | 546 | 22,509 | 4.60M | 68,335 | 28,368 | 0.509 | 67 |
| 12043 | Glades | rural | 3,425 | 1,892 | 230 | 20,887 | 4.78M | 110,907 | 44,903 | 0.864 | 36* |
| 12045 | Gulf | rural | 5,106 | 4,541 | 0 | 529 | 8.66M | 0 | n/a | 0.654 | 36* |
| 12047 | Hamilton | rural | 3,588 | 2,926 | 235 | 13,137 | 4.25M | 57,252 | 22,580 | 0.736 | 60 |
| 12049 | Hardee | rural | 8,845 | 6,756 | 812 | 31,391 | 7.01M | 64,822 | 28,463 | 0.758 | 30 |
| 12051 | Hendry | rural | 17,935 | 15,113 | 1,323 | 84,060 | 11.91M | 102,476 | 98,833 | 0.516 | 36* |
| 12053 | Hernando | suburb | 77,385 | 58,723 | 568 | 4,947 | 90.17M | 53,193 | 3,887 | 0.633 | 36* |
| 12055 | Highlands | suburb | 34,686 | 32,090 | 1,142 | 41,545 | 41.47M | 57,752 | 35,859 | 0.811 | 36* |
| 12057 | Hillsborough | suburb | 723,695 | 768,088 | 3,327 | 8,632 | 510.41M | 56,674 | 35,716 | 0.470 | 60 |
| 12059 | Holmes | rural | 7,533 | 3,790 | 501 | 21,516 | 5.51M | 50,869 | 11,084 | 0.852 | 58 |
| 12061 | Indian River | suburb | 62,037 | 63,208 | 453 | 21,668 | 79.12M | 83,984 | 41,298 | 0.750 | 36* |
| 12063 | Jackson | rural | 16,059 | 14,205 | 801 | 75,970 | 16.28M | 63,512 | 28,838 | 0.700 | 74 |
| 12065 | Jefferson | suburb | 5,936 | 3,014 | 406 | 8,043 | 2.84M | 76,744 | 8,602 | 0.801 | 64 |
| 12067 | Lafayette | rural | 2,894 | 1,807 | 233 | 10,697 | 2.24M | 45,007 | 77,525 | 0.412 | 59 |
| 12069 | Lake | suburb | 160,502 | 121,979 | 1,805 | 12,690 | 133.86M | 71,888 | 31,730 | 0.624 | 36* |
| 12071 | Lee | suburb | 326,302 | 310,853 | 878 | 6,460 | 349.26M | 72,137 | 40,070 | 0.379 | 70 |
| 12073 | Leon | suburb | 147,179 | 165,446 | 216 | 1,911 | 92.95M | 72,092 | 8,875 | 0.886 | 36* |
| 12075 | Levy | suburb | 16,885 | 9,827 | 711 | 30,725 | 10.60M | 76,258 | 55,501 | 0.625 | 61 |
| 12077 | Liberty | rural | 2,492 | 2,008 | 54 | 1,658 | 1.91M | 75,536 | 65,333 | 0.991 | 36* |
| 12079 | Madison | rural | 6,020 | 5,781 | 569 | 21,144 | 4.95M | 64,126 | 27,976 | 0.775 | 26 |
| 12081 | Manatee | suburb | 172,752 | 143,883 | 1,234 | 10,592 | 160.71M | 53,876 | 63,541 | 0.700 | 36* |
| 12083 | Marion | suburb | 139,755 | 126,819 | 2,615 | 6,472 | 169.18M | 69,594 | 676 | 0.731 | 27 |
| 12085 | Martin | suburb | 65,741 | 72,937 | 411 | 13,064 | 85.75M | 69,000 | 45,828 | 0.422 | 36* |
| 12086 | Miami-Dade | core | 1,319,578 | 1,385,676 | 4,882 | 18,904 | 782.01M | 71,415 | 40,266 | 0.559 | 36* |
| 12087 | Monroe | rural | 42,929 | 47,777 | 0 | 19 | 34.65M | 0 | n/a | 0.654 | 36* |
| 12089 | Nassau | suburb | 41,279 | 28,850 | 294 | 796 | 25.74M | 79,116 | 4,745 | 0.962 | 36* |
| 12091 | Okaloosa | suburb | 104,566 | 113,285 | 332 | 8,526 | 88.18M | 72,497 | 7,615 | 0.957 | 66 |
| 12093 | Okeechobee | rural | 15,091 | 12,479 | 795 | 10,048 | 14.72M | 65,831 | 40,149 | 0.676 | 36* |
| 12095 | Orange | suburb | 717,790 | 890,459 | 1,303 | 2,815 | 518.51M | 68,288 | 46,869 | 0.315 | 36* |
| 12097 | Osceola | suburb | 187,046 | 136,132 | 310 | 6,522 | 112.98M | 77,606 | 53,129 | 0.405 | 36* |
| 12099 | Palm Beach | suburb | 682,181 | 704,610 | 1,918 | 178,894 | 609.68M | 87,719 | 78,248 | 0.613 | 50 |
| 12101 | Pasco | suburb | 242,883 | 176,883 | 936 | 12,659 | 185.32M | 61,521 | 16,679 | 0.555 | 38 |
| 12103 | Pinellas | suburb | 454,923 | 478,590 | 122 | 71 | 439.73M | 95,616 | 38,659 | 0.978 | 36* |
| 12105 | Polk | suburb | 315,558 | 277,036 | 1,924 | 60,648 | 243.33M | 65,559 | 27,032 | 0.646 | 36* |
| 12107 | Putnam | rural | 25,550 | 19,456 | 381 | 2,601 | 26.74M | 53,375 | 25,443 | 0.600 | 36* |
| 12109 | St. Johns | suburb | 128,385 | 109,455 | 266 | 5,977 | 75.24M | 66,395 | 55,895 | 0.688 | 36* |
| 12111 | St. Lucie | suburb | 142,823 | 107,996 | 354 | 24,331 | 167.73M | 75,461 | 55,141 | 0.616 | 36* |
| 12113 | Santa Rosa | suburb | 83,822 | 51,502 | 495 | 23,723 | 60.34M | 52,909 | 18,770 | 0.629 | 101 |
| 12115 | Sarasota | suburb | 178,719 | 205,374 | 202 | 1,115 | 207.35M | 80,135 | 22,811 | 0.727 | 36* |
| 12117 | Seminole | suburb | 243,840 | 222,379 | 234 | 494 | 186.93M | 62,275 | 16,713 | 0.825 | 36* |
| 12119 | Sumter | suburb | 27,879 | 39,674 | 1,078 | 8,683 | 60.92M | 65,293 | 11,718 | 0.564 | 36 |
| 12121 | Suwannee | rural | 16,938 | 13,568 | 1,054 | 35,816 | 13.89M | 55,863 | 72,661 | 0.705 | 47 |
| 12123 | Taylor | rural | 6,593 | 6,868 | 128 | 737 | 7.42M | 76,255 | 43,406 | 0.807 | 36* |
| 12125 | Union | rural | 4,225 | 3,646 | 202 | 3,214 | 2.90M | 68,978 | 5,038 | 0.777 | 36* |
| 12127 | Volusia | suburb | 241,735 | 215,291 | 1,466 | 1,253 | 241.31M | 46,062 | 40,100 | 0.625 | 36* |
| 12129 | Wakulla | suburb | 15,067 | 8,583 | 121 | 199 | 7.10M | 51,926 | -1,658 | 0.654 | 36* |
| 12131 | Walton | suburb | 33,781 | 35,947 | 397 | 16,827 | 29.77M | 59,261 | 24,926 | 0.918 | 36* |
| 12133 | Washington | suburb | 8,533 | 7,170 | 332 | 12,596 | 7.40M | 78,046 | 13,320 | 0.844 | 46 |
| EXT | External (out-of-state commuting) | external | 64,990 | 118,874 | 594 | 12,934 | 53.94M | 68,483 | n/a | 0.645 | n/a |

`*` filled, see above.
