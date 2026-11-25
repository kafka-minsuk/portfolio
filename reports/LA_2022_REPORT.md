# Louisiana 2022 county data: validation report

Built 2026-11-24 by `python -m urqse.data.build_state LA 2022`. 64 counties plus one external zone. Outputs: `county.parquet` (one row per zone, schema in `src/urqse/data/schema.py`) and `travel.npz` (`fips`, `t` minutes, `dist` km, rows in table order).

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
| cdl | USDA NASS Cropland Data Layer 2022, 30 m, clipped to state FIPS 22 | `LA/CDL_2022_22.tif` | 2026-11-24 | https://nassgeodata.gmu.edu/axis2/services/CDLService/GetCDLFile?year=2022&fips=22 |
| acs_b08007 | ACS 2018-2022 5-year, table-based summary file B08007 | `US/acs/acsdt5y2022-b08007.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08007.dat |
| acs_b08604 | ACS 2018-2022 5-year, table-based summary file B08604 | `US/acs/acsdt5y2022-b08604.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08604.dat |
| acs_b05005 | ACS 2018-2022 5-year, table-based summary file B05005 | `US/acs/acsdt5y2022-b05005.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b05005.dat |
| ghsl_R6_C10 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R6_C10.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R6_C10.zip |
| nass | Quick Stats bulk economics file `qs.economics_20261121.txt.gz` (Census of Agriculture 2022; Cash Rents Survey 2022) | `qs.economics_20261121.txt.gz` (filtered copy `*_LA.tsv.gz`) | see file | https://www.nass.usda.gov/sites/default/files/datasets/qs.economics_20261121.txt.gz |
| osrm | OSRM public demo server, car profile (OSM data as served on the build date) | `osrm/*.json` (4 cached block requests; the server caps a table at 100 coordinates) | 2026-11-24 | https://router.project-osrm.org/table/v1/driving |

## County sums against published state totals

| Column | Sum of counties | Published state value | Difference |
|---|---|---|---|
| PEP population | 4,590,241 | 4,590,241 | 0.000% |
| ACS workers by residence | 1,995,269 | 1,995,269 | 0.000% |
| ACS workers by workplace | 2,006,139 | 2,006,139 | 0.000% |
| ACS workers working out of state | 43,039 | 43,039 | 0.000% |
| BEA non-farm employment (L80) | 2,752,743 | 2,752,743 | 0.000% |
| BEA farm employment (L70) | 31,968 | 31,968 | 0.000% |
| BEA farm proprietors (L50) | 23,297 | 23,297 | 0.000% |
| BEA farm earnings $ (CAINC45 L370) | 851,961,000 | 851,961,000 | 0.000% |
| BEA farm wages + supplements $ (CAINC45 L350 + L360) | 185,924,000 | 185,924,000 | 0.000% |
| CoA hired farm labour expense $ | 343,093,000 | 343,090,000 | 0.001% |
| BEA non-farm earnings $ (CAINC5N L82) | 162,046,329,000 | 162,046,329,000 | 0.000% |
| ACS foreign born entered 2010+ | 76,487 | 76,487 | 0.000% |
| CoA owned acres | 3,567,637 | 3,567,637 | 0.000% |
| CoA rented-from-others acres | 4,418,744 | 4,418,744 | 0.000% |
| CoA land in farms, ha | 3,231,974 | 3,231,974 | 0.000% |
| CoA total cropland, ha | 1,741,640 | 1,741,640 | -0.000% |

## Model columns

- **N, HU, HA (jobs = resident workers).** Each county's BEA farm and non-farm job counts are scaled to its ACS count of workers by place of work (scale factor min 0.398, median 0.695, max 1.021; BEA counts jobs, ACS counts people by main job). Sum N = 2,049,178 = sum HU + HA = 2,049,178. Farm jobs after scaling: 21,791 (BEA 31,968). `# VERIFY` the scaling: part-time farm proprietors with an off-farm main job are counted once, in proportion to the county mix.
- **External zone.** Residents = out-of-state workers commuting in (ACS workplace total minus in-state residents working in state) = 53,909. Jobs = in-state residents working out of state = 43,039, split by the state farm share (HA = 467). Location: the 28 out-of-state counties within 1 km of the state (05003, 05017, 05027, 05073, 05091, 05139, 28001, 28005, 28021, 28045, 28055, 28063, 28091, 28109, 28113, 28147, 28149, 28151, 28157, 48067, 48203, 48245, 48315, 48351, 48361, 48365, 48403, 48419); travel time from a county to the zone is the OSRM time to the nearest of them. Floor space, farmland, farm labour earnings and owner share are state averages scaled to its workers / farm jobs; gateway weight 0 (immigrants settle in-state). `# VERIFY` all of these are conventions, not data, and `log(0)` in `immigration.arrival_shares` needs handling in M3.
- **TF (farmland, ha).** CDL 2022 crop, hay, fallow and tree-crop classes (codes 1-61, 66-77, 204-254), pixel-centre zonal sums on the 30 m Albers grid. State: 1,563,681 ha vs Census of Agriculture cropland 1,741,640 ha and land in farms 3,231,974 ha; county ratio TF / CoA cropland 0.02 to 2.21. Grassland/pasture (codes 62, 176) is kept separately (`pasture_ha`, 982,360 ha). County area covered by CDL pixels: 12,200,746 ha vs land area 11,192,090 ha (the difference is water). `# VERIFY` whether pasture belongs in T^F for livestock counties.
- **L (floor space, m^2).** GHSL GHS-BUILT-V 2020 epoch building volume / 3 m storey height (`# VERIFY` storey height; 2020 is the nearest epoch to 2022). State volume 5.24 km^3.
- **wA_obs_usd (farm labour earnings per farm worker).** Farm compensation (CAINC45 L350 wages and salaries + L360 supplements) per farm wage-and-salary job (CAEMP25N L70 - L50), mean of 2018 to 2022, each year relative to the state's non-farm earnings per non-farm job (CAINC5N L82 / CAEMP25N L80) and put at the 2022 value (58,867 $). That per-job wage prices every BEA farm job, proprietors included, giving the county farm labour bill `farm_labour_bill_usd`; wA_obs_usd = bill / HA, so it is per farm worker (ACS head) and the model's wage bill w_A H_A equals the bill in dollars. State: 20,269 $ per BEA farm job, 29,735 $ per farm worker; county range 7,641 to 92,152 $ per worker. State compensation per farm wage job by year: 2018 21,912 $, 2019 20,909 $, 2020 18,687 $, 2021 19,526 $, 2022 21,442 $. Proprietors are priced at the hired wage per job (the market price of farm labour in the county) rather than at a non-farm opportunity wage, which would assume away the farm/non-farm gap xi_A is meant to measure. `# VERIFY` the proprietor imputation: a BEA proprietor job is any sole proprietor or partner, many part-time. Contract labour (CoA 54,522,000 $) is left out: its workers are not BEA farm jobs (they are in agricultural support services, non-farm). Census of Agriculture hired labour expense (343,090,000 $ in 2022, column `hired_labor_coa_usd`) is 1.85x BEA farm compensation (185,924,000 $) and pays a different universe (every hired head, including workers on the farm under 150 days), so it is a comparison column, not the bill. `# VERIFY` that gap. The previous measure, BEA farm earnings (L370, wages + proprietors' income) per BEA farm job, is kept as `wA_bea_earn_usd`: state 26,650 $, county -57,927 to 232,064 $; it includes owner-operators' returns to owned land and capital, which spec §12.1 pays separately. The loader divides wA_obs_usd by state non-farm earnings per non-farm worker (sum over counties of non-farm earnings / HU = 81,662 $), so both sectors are per head. `# VERIFY` vintage mismatch: CAINC45/CAEMP25N are the 2023-11-16 release, CAINC5N the 2026 file (CAINC5N's revised 2022 farm earnings are 776,876,000 $ vs CAINC45 851,961,000 $).
- **omega.** Census of Agriculture 2022 owned / (owned + rented from others) acres in farms. State 0.447, county range 0.019 to 0.933.
- **cash_rent_usd_acre.** NASS Cash Rents Survey 2022, non-irrigated cropland. State 76 $/acre.
- **land_value_usd_acre.** Census of Agriculture 2022 estimated market value of land and buildings per acre (NASS does not publish annual county land values). State 3,600 $/acre.
- **gateway.** ACS foreign born who entered 2010 or later per resident worker, relative to the state ratio (mean 1 over workers). `# VERIFY` against spec §12.2 once the arrival block is calibrated. 3 counties have no recent foreign born in the ACS sample (East Carroll, Red River, Tensas), so their gateway weight is 0 (log(0) in arrival_shares).
- **kind.** core = the metropolitan county with the most non-farm jobs (East Baton Rouge); suburb = other counties in a Metropolitan Statistical Area (OMB 2023) (36); rural = the rest (27). `# VERIFY` one core for a multi-metro state.
- **No farm sector** (spec §3.11): 1 counties have no BEA farm jobs (Orleans); their farm wage is 0 and the model gives them no farm job option.
- **Travel time t (min).** OSRM car durations between 2020 population-weighted county centres, as routed (not symmetrised). Off-diagonal median 191.7 min. Own-county time = 0.5214 x sqrt(land area) at the median effective speed of 59.0 straight-line km/h between counties (median 11.1 to 31.1 min). `# VERIFY` the own-county proxy. `dist` is great-circle km (road/straight median ratio 1.26).

## Suppressed cells and fills

| Variable | County | Rule |
|---|---|---|
| HA_bea | 22071 Orleans | 0 farm jobs: no farm sector in the model (spec §3.11) |
| cash_rent_usd_acre | 22003 Allen | not published; NASS 'other (combined) counties' value = 39 $/acre |
| cash_rent_usd_acre | 22005 Ascension | not published; NASS 'other (combined) counties' value = 39 $/acre |
| cash_rent_usd_acre | 22013 Bienville | not published; NASS 'other (combined) counties' value = 39 $/acre |
| cash_rent_usd_acre | 22021 Caldwell | not published; NASS 'other (combined) counties' value = 39 $/acre |
| cash_rent_usd_acre | 22023 Cameron | not published; NASS 'other (combined) counties' value = 39 $/acre |
| cash_rent_usd_acre | 22049 Jackson | not published; NASS 'other (combined) counties' value = 39 $/acre |
| cash_rent_usd_acre | 22051 Jefferson | not published; NASS 'other (combined) counties' value = 39 $/acre |
| cash_rent_usd_acre | 22059 LaSalle | not published; NASS 'other (combined) counties' value = 39 $/acre |
| cash_rent_usd_acre | 22063 Livingston | not published; NASS 'other (combined) counties' value = 39 $/acre |
| cash_rent_usd_acre | 22071 Orleans | not published; NASS 'other (combined) counties' value = 39 $/acre |
| cash_rent_usd_acre | 22075 Plaquemines | not published; NASS 'other (combined) counties' value = 39 $/acre |
| cash_rent_usd_acre | 22087 St. Bernard | not published; NASS 'other (combined) counties' value = 39 $/acre |
| cash_rent_usd_acre | 22089 St. Charles | not published; NASS 'other (combined) counties' value = 39 $/acre |
| cash_rent_usd_acre | 22093 St. James | not published; NASS 'other (combined) counties' value = 39 $/acre |
| cash_rent_usd_acre | 22095 St. John the Baptist | not published; NASS 'other (combined) counties' value = 39 $/acre |
| cash_rent_usd_acre | 22103 St. Tammany | not published; NASS 'other (combined) counties' value = 39 $/acre |
| cash_rent_usd_acre | 22109 Terrebonne | not published; NASS 'other (combined) counties' value = 39 $/acre |
| cash_rent_usd_acre | 22115 Vernon | not published; NASS 'other (combined) counties' value = 39 $/acre |
| cash_rent_usd_acre | 22119 Webster | not published; NASS 'other (combined) counties' value = 39 $/acre |
| cash_rent_usd_acre | 22127 Winn | not published; NASS 'other (combined) counties' value = 39 $/acre |

## Coverage gaps and caveats

- ACS is the 5-year period estimate ending in the base year (no 1-year data for small counties); BEA and PEP are single-year. The external zone inherits ACS sampling error in the commuter totals.
- The Census API now requires a key, so ACS comes from the table-based summary files instead (same estimates).
- LODES (for the M3 PPML of kappa*lambda) and IRS SOI migration flows are not part of this build.
- Census of Agriculture is quinquennial (2022 matches the base year); the cash-rent survey is annual.
- x_km / y_km are NAD83 / UTM (EPSG:26915) at the state's middle longitude, for drawing only.
- No satellite population layer (GHS-POP) is used; census counts drive calibration (spec §8).

## County table

| FIPS | Name | Kind | N | HU | HA | TF ha | L m^2 | wA $/worker | BEA farm earnings $/job | omega | rent $/ac |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 22001 | Acadia | suburb | 22,432 | 14,503 | 609 | 70,431 | 23.68M | 35,342 | 19,526 | 0.277 | 62 |
| 22003 | Allen | rural | 7,720 | 7,217 | 311 | 13,281 | 6.93M | 22,734 | 12,069 | 0.457 | 39* |
| 22005 | Ascension | suburb | 61,876 | 51,092 | 198 | 9,406 | 46.71M | 32,172 | 1,438 | 0.297 | 39* |
| 22007 | Assumption | suburb | 8,361 | 4,515 | 163 | 25,028 | 6.34M | 45,017 | 28,763 | 0.317 | 44 |
| 22009 | Avoyelles | rural | 14,535 | 10,142 | 753 | 72,424 | 12.39M | 25,193 | 30,205 | 0.384 | 98 |
| 22011 | Beauregard | rural | 14,499 | 9,671 | 561 | 2,843 | 11.30M | 17,997 | -8,152 | 0.632 | 21 |
| 22013 | Bienville | rural | 4,426 | 3,014 | 144 | 288 | 3.77M | 30,318 | 36,848 | 0.769 | 39* |
| 22015 | Bossier | suburb | 57,584 | 49,687 | 383 | 6,411 | 40.20M | 14,820 | -5,230 | 0.707 | 34 |
| 22017 | Caddo | suburb | 95,321 | 108,634 | 438 | 20,721 | 102.60M | 24,273 | -21,659 | 0.424 | 58 |
| 22019 | Calcasieu | suburb | 90,879 | 101,153 | 735 | 12,310 | 110.45M | 17,966 | -13,171 | 0.420 | 16 |
| 22021 | Caldwell | rural | 3,085 | 2,224 | 181 | 13,340 | 2.26M | 26,699 | 3,022 | 0.836 | 39* |
| 22023 | Cameron | suburb | 2,531 | 6,179 | 344 | 9,913 | 5.08M | 12,231 | 10,496 | 0.374 | 39* |
| 22025 | Catahoula | rural | 2,877 | 1,335 | 249 | 71,351 | 3.01M | 52,127 | 3,679 | 0.386 | 88 |
| 22027 | Claiborne | rural | 4,112 | 2,905 | 207 | 367 | 4.46M | 26,988 | 116,749 | 0.872 | 14 |
| 22029 | Concordia | rural | 5,287 | 4,616 | 380 | 78,101 | 5.63M | 25,417 | 54,647 | 0.444 | 120 |
| 22031 | De Soto | suburb | 10,193 | 7,166 | 444 | 1,348 | 9.40M | 21,178 | -12,275 | 0.757 | 44 |
| 22033 | East Baton Rouge | core | 213,013 | 262,298 | 289 | 1,187 | 199.22M | 23,876 | -7,186 | 0.752 | 16 |
| 22035 | East Carroll | rural | 1,623 | 1,364 | 239 | 76,859 | 2.57M | 45,082 | 52,260 | 0.273 | 134 |
| 22037 | East Feliciana | suburb | 6,530 | 5,356 | 255 | 1,581 | 5.24M | 32,734 | -22,078 | 0.709 | 18 |
| 22039 | Evangeline | rural | 11,046 | 7,568 | 456 | 36,188 | 10.98M | 27,540 | 33,481 | 0.520 | 60 |
| 22041 | Franklin | rural | 6,500 | 4,443 | 658 | 96,788 | 6.34M | 29,304 | 22,558 | 0.472 | 64 |
| 22043 | Grant | suburb | 7,706 | 3,533 | 134 | 5,352 | 4.19M | 49,075 | -15,197 | 0.560 | 94 |
| 22045 | Iberia | rural | 28,561 | 26,681 | 357 | 33,154 | 34.00M | 46,362 | 23,710 | 0.177 | 88 |
| 22047 | Iberville | suburb | 12,009 | 18,573 | 309 | 27,205 | 20.29M | 28,075 | 21,018 | 0.546 | 31 |
| 22049 | Jackson | rural | 4,867 | 3,892 | 126 | 80 | 4.73M | 13,591 | 136,303 | 0.764 | 39* |
| 22051 | Jefferson | suburb | 204,156 | 193,246 | 51 | 50 | 155.82M | 27,831 | 6,480 | 0.040 | 39* |
| 22053 | Jefferson Davis | suburb | 12,900 | 8,561 | 457 | 61,019 | 12.82M | 28,023 | 43,895 | 0.326 | 28 |
| 22055 | Lafayette | suburb | 116,494 | 139,353 | 462 | 12,432 | 99.47M | 33,904 | 8,243 | 0.505 | 66 |
| 22057 | Lafourche | suburb | 41,074 | 35,685 | 365 | 19,105 | 33.62M | 36,600 | 35,299 | 0.493 | 40 |
| 22059 | LaSalle | rural | 6,278 | 5,636 | 153 | 1,297 | 3.35M | 7,641 | -17,046 | 0.777 | 39* |
| 22061 | Lincoln | rural | 20,920 | 22,118 | 303 | 255 | 14.42M | 23,706 | 161,018 | 0.723 | 14 |
| 22063 | Livingston | suburb | 64,898 | 31,253 | 221 | 309 | 30.46M | 31,180 | 13,867 | 0.856 | 39* |
| 22065 | Madison | rural | 2,902 | 2,769 | 284 | 85,037 | 3.86M | 31,948 | 27,275 | 0.422 | 96 |
| 22067 | Morehouse | suburb | 9,196 | 6,121 | 397 | 97,909 | 6.82M | 32,357 | 50,108 | 0.319 | 102 |
| 22069 | Natchitoches | rural | 14,014 | 14,015 | 458 | 21,803 | 11.87M | 27,669 | 43,388 | 0.545 | 53 |
| 22071 | Orleans | suburb | 171,424 | 223,191 | 0 | 31 | 132.17M | 0 | n/a | 0.778 | 39* |
| 22073 | Ouachita | suburb | 67,312 | 71,551 | 381 | 17,766 | 65.12M | 38,441 | 26,692 | 0.570 | 90 |
| 22075 | Plaquemines | suburb | 10,962 | 15,595 | 277 | 66 | 13.92M | 16,573 | 22,160 | 0.019 | 39* |
| 22077 | Pointe Coupee | suburb | 7,836 | 4,428 | 260 | 56,345 | 7.05M | 53,718 | 33,125 | 0.355 | 100 |
| 22079 | Rapides | suburb | 54,593 | 58,223 | 898 | 37,074 | 46.42M | 30,562 | 55,545 | 0.384 | 96 |
| 22081 | Red River | rural | 2,849 | 2,867 | 240 | 7,250 | 2.53M | 28,781 | 14,416 | 0.597 | 60 |
| 22083 | Richland | suburb | 7,436 | 6,064 | 548 | 84,569 | 6.33M | 32,204 | 15,850 | 0.395 | 68 |
| 22085 | Sabine | rural | 7,234 | 5,857 | 280 | 235 | 7.83M | 23,976 | 232,064 | 0.640 | 18 |
| 22087 | St. Bernard | suburb | 18,507 | 13,420 | 41 | 19 | 16.44M | 45,856 | 21,263 | 0.434 | 39* |
| 22089 | St. Charles | suburb | 23,995 | 28,037 | 55 | 1,558 | 29.50M | 45,569 | 5,492 | 0.220 | 39* |
| 22091 | St. Helena | suburb | 3,668 | 1,678 | 185 | 165 | 2.64M | 92,152 | 1,711 | 0.811 | 15 |
| 22093 | St. James | suburb | 8,729 | 8,971 | 122 | 14,958 | 14.70M | 35,832 | 33,669 | 0.213 | 39* |
| 22095 | St. John the Baptist | suburb | 17,519 | 16,273 | 34 | 5,106 | 16.73M | 40,032 | -57,927 | 0.559 | 39* |
| 22097 | St. Landry | rural | 29,973 | 24,243 | 937 | 69,264 | 31.27M | 26,027 | 12,604 | 0.383 | 78 |
| 22099 | St. Martin | suburb | 21,696 | 13,930 | 296 | 25,611 | 18.64M | 28,368 | 13,550 | 0.232 | 84 |
| 22101 | St. Mary | rural | 19,136 | 20,904 | 190 | 27,062 | 24.30M | 46,597 | 44,751 | 0.072 | 78 |
| 22103 | St. Tammany | suburb | 121,358 | 101,903 | 473 | 91 | 80.64M | 32,353 | -3,773 | 0.708 | 39* |
| 22105 | Tangipahoa | suburb | 56,297 | 47,435 | 783 | 965 | 32.20M | 31,645 | 2,416 | 0.713 | 25 |
| 22107 | Tensas | rural | 1,154 | 700 | 194 | 75,932 | 2.08M | 52,586 | 38,555 | 0.279 | 88 |
| 22109 | Terrebonne | suburb | 46,254 | 52,467 | 238 | 6,285 | 44.94M | 26,014 | 35,031 | 0.165 | 39* |
| 22111 | Union | suburb | 7,984 | 4,774 | 236 | 673 | 6.89M | 37,090 | 208,629 | 0.816 | 32 |
| 22113 | Vermilion | suburb | 22,422 | 13,391 | 823 | 71,130 | 22.40M | 32,314 | 44,511 | 0.272 | 66 |
| 22115 | Vernon | rural | 20,966 | 21,399 | 365 | 334 | 13.41M | 15,757 | 17,570 | 0.714 | 39* |
| 22117 | Washington | rural | 16,324 | 12,651 | 645 | 1,909 | 13.86M | 25,695 | 2,044 | 0.807 | 28 |
| 22119 | Webster | rural | 12,853 | 12,751 | 321 | 298 | 12.95M | 16,587 | 357 | 0.858 | 39* |
| 22121 | West Baton Rouge | suburb | 12,469 | 13,327 | 133 | 12,662 | 16.42M | 39,478 | 33,200 | 0.267 | 71 |
| 22123 | West Carroll | rural | 3,554 | 2,266 | 490 | 55,680 | 3.80M | 38,091 | 11,897 | 0.632 | 61 |
| 22125 | West Feliciana | suburb | 5,572 | 5,485 | 151 | 5,223 | 3.21M | 19,505 | -9,878 | 0.734 | 23 |
| 22127 | Winn | rural | 4,788 | 4,047 | 123 | 245 | 3.89M | 37,221 | 45,855 | 0.933 | 39* |
| EXT | External (out-of-state commuting) | external | 53,909 | 42,572 | 467 | 33,547 | 47.19M | 29,735 | n/a | 0.447 | n/a |

`*` filled, see above.
