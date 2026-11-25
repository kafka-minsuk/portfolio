# South Dakota 2022 county data: validation report

Built 2026-11-24 by `python -m urqse.data.build_state SD 2022`. 66 counties plus one external zone. Outputs: `county.parquet` (one row per zone, schema in `src/urqse/data/schema.py`) and `travel.npz` (`fips`, `t` minutes, `dist` km, rows in table order).

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
| cdl | USDA NASS Cropland Data Layer 2022, 30 m, clipped to state FIPS 46 | `SD/CDL_2022_46.tif` | 2026-11-24 | https://nassgeodata.gmu.edu/axis2/services/CDLService/GetCDLFile?year=2022&fips=46 |
| acs_b08007 | ACS 2018-2022 5-year, table-based summary file B08007 | `US/acs/acsdt5y2022-b08007.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08007.dat |
| acs_b08604 | ACS 2018-2022 5-year, table-based summary file B08604 | `US/acs/acsdt5y2022-b08604.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08604.dat |
| acs_b05005 | ACS 2018-2022 5-year, table-based summary file B05005 | `US/acs/acsdt5y2022-b05005.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b05005.dat |
| ghsl_R4_C10 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C10.zip` | 2026-11-23 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C10.zip |
| ghsl_R4_C11 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C11.zip` | 2026-11-23 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C11.zip |
| nass | Quick Stats bulk economics file `qs.economics_20261121.txt.gz` (Census of Agriculture 2022; Cash Rents Survey 2022) | `qs.economics_20261121.txt.gz` (filtered copy `*_SD.tsv.gz`) | see file | https://www.nass.usda.gov/sites/default/files/datasets/qs.economics_20261121.txt.gz |
| osrm | OSRM public demo server, car profile (OSM data as served on the build date) | `osrm/*.json` (4 cached block requests; the server caps a table at 100 coordinates) | 2026-11-24 | https://router.project-osrm.org/table/v1/driving |

## County sums against published state totals

| Column | Sum of counties | Published state value | Difference |
|---|---|---|---|
| PEP population | 909,824 | 909,824 | 0.000% |
| ACS workers by residence | 449,118 | 449,118 | 0.000% |
| ACS workers by workplace | 454,123 | 454,123 | 0.000% |
| ACS workers working out of state | 10,904 | 10,904 | 0.000% |
| BEA non-farm employment (L80) | 615,112 | 615,112 | 0.000% |
| BEA farm employment (L70) | 32,848 | 32,848 | 0.000% |
| BEA farm proprietors (L50) | 25,196 | 25,196 | 0.000% |
| BEA farm earnings $ (CAINC45 L370) | 4,347,876,000 | 4,347,876,000 | 0.000% |
| BEA farm wages + supplements $ (CAINC45 L350 + L360) | 320,476,000 | 320,476,000 | 0.000% |
| CoA hired farm labour expense $ | 588,977,000 | 588,977,000 | 0.000% |
| BEA non-farm earnings $ (CAINC5N L82) | 37,517,827,000 | 37,517,827,000 | 0.000% |
| ACS foreign born entered 2010+ | 15,311 | 15,311 | 0.000% |
| CoA owned acres | 24,649,158 | 24,649,158 | 0.000% |
| CoA rented-from-others acres | 17,655,443 | 17,655,443 | 0.000% |
| CoA land in farms, ha | 17,120,065 | 17,120,065 | 0.000% |
| CoA total cropland, ha | 7,482,079 | 7,482,079 | -0.000% |

## Model columns

- **N, HU, HA (jobs = resident workers).** Each county's BEA farm and non-farm job counts are scaled to its ACS count of workers by place of work (scale factor min 0.443, median 0.682, max 1.035; BEA counts jobs, ACS counts people by main job). Sum N = 465,027 = sum HU + HA = 465,027. Farm jobs after scaling: 22,261 (BEA 32,848). `# VERIFY` the scaling: part-time farm proprietors with an off-farm main job are counted once, in proportion to the county mix.
- **External zone.** Residents = out-of-state workers commuting in (ACS workplace total minus in-state residents working in state) = 15,909. Jobs = in-state residents working out of state = 10,904, split by the state farm share (HA = 535). Location: the 34 out-of-state counties within 1 km of the state (19119, 19149, 19167, 19193, 27011, 27073, 27081, 27117, 27133, 27155, 27173, 30011, 30025, 31015, 31027, 31031, 31043, 31045, 31051, 31103, 31107, 31161, 31165, 38001, 38011, 38021, 38029, 38051, 38077, 38081, 38085, 56011, 56027, 56045); travel time from a county to the zone is the OSRM time to the nearest of them. Floor space, farmland, farm labour earnings and owner share are state averages scaled to its workers / farm jobs; gateway weight 0 (immigrants settle in-state). `# VERIFY` all of these are conventions, not data, and `log(0)` in `immigration.arrival_shares` needs handling in M3.
- **TF (farmland, ha).** CDL 2022 crop, hay, fallow and tree-crop classes (codes 1-61, 66-77, 204-254), pixel-centre zonal sums on the 30 m Albers grid. State: 7,419,003 ha vs Census of Agriculture cropland 7,482,079 ha and land in farms 17,120,065 ha; county ratio TF / CoA cropland 0.60 to 1.56. Grassland/pasture (codes 62, 176) is kept separately (`pasture_ha`, 9,740,926 ha). County area covered by CDL pixels: 19,972,826 ha vs land area 19,634,155 ha (the difference is water). `# VERIFY` whether pasture belongs in T^F for livestock counties.
- **L (floor space, m^2).** GHSL GHS-BUILT-V 2020 epoch building volume / 3 m storey height (`# VERIFY` storey height; 2020 is the nearest epoch to 2022). State volume 1.09 km^3.
- **wA_obs_usd (farm labour earnings per farm worker).** Farm compensation (CAINC45 L350 wages and salaries + L360 supplements) per farm wage-and-salary job (CAEMP25N L70 - L50), mean of 2018 to 2022, each year relative to the state's non-farm earnings per non-farm job (CAINC5N L82 / CAEMP25N L80) and put at the 2022 value (60,993 $). That per-job wage prices every BEA farm job, proprietors included, giving the county farm labour bill `farm_labour_bill_usd`; wA_obs_usd = bill / HA, so it is per farm worker (ACS head) and the model's wage bill w_A H_A equals the bill in dollars. State: 44,292 $ per BEA farm job, 65,357 $ per farm worker; county range 38,950 to 104,365 $ per worker. State compensation per farm wage job by year: 2018 40,847 $, 2019 45,436 $, 2020 39,320 $, 2021 40,098 $, 2022 41,881 $. Proprietors are priced at the hired wage per job (the market price of farm labour in the county) rather than at a non-farm opportunity wage, which would assume away the farm/non-farm gap xi_A is meant to measure. `# VERIFY` the proprietor imputation: a BEA proprietor job is any sole proprietor or partner, many part-time. Contract labour (CoA 57,696,000 $) is left out: its workers are not BEA farm jobs (they are in agricultural support services, non-farm). Census of Agriculture hired labour expense (588,977,000 $ in 2022, column `hired_labor_coa_usd`) is 1.84x BEA farm compensation (320,476,000 $) and pays a different universe (every hired head, including workers on the farm under 150 days), so it is a comparison column, not the bill. `# VERIFY` that gap. The previous measure, BEA farm earnings (L370, wages + proprietors' income) per BEA farm job, is kept as `wA_bea_earn_usd`: state 132,363 $, county 2,763 to 250,523 $; it includes owner-operators' returns to owned land and capital, which spec §12.1 pays separately. The loader divides wA_obs_usd by state non-farm earnings per non-farm worker (sum over counties of non-farm earnings / HU = 86,875 $), so both sectors are per head. `# VERIFY` vintage mismatch: CAINC45/CAEMP25N are the 2023-11-16 release, CAINC5N the 2026 file (CAINC5N's revised 2022 farm earnings are 4,828,567,000 $ vs CAINC45 4,347,876,000 $).
- **omega.** Census of Agriculture 2022 owned / (owned + rented from others) acres in farms. State 0.583, county range 0.394 to 0.806.
- **cash_rent_usd_acre.** NASS Cash Rents Survey 2022, non-irrigated cropland. State 125 $/acre.
- **land_value_usd_acre.** Census of Agriculture 2022 estimated market value of land and buildings per acre (NASS does not publish annual county land values). State 2,592 $/acre.
- **gateway.** ACS foreign born who entered 2010 or later per resident worker, relative to the state ratio (mean 1 over workers). `# VERIFY` against spec §12.2 once the arrival block is calibrated. 12 counties have no recent foreign born in the ACS sample (Buffalo, Butte, Corson, Fall River, Haakon, Hyde, Jones, McPherson, Mellette, Miner, Oglala Lakota, Stanley), so their gateway weight is 0 (log(0) in arrival_shares).
- **kind.** core = the metropolitan county with the most non-farm jobs (Minnehaha); suburb = other counties in a Metropolitan Statistical Area (OMB 2023) (7); rural = the rest (58). `# VERIFY` one core for a multi-metro state.
- **No farm sector** (spec §3.11): 0 counties have no BEA farm jobs.
- **Travel time t (min).** OSRM car durations between 2020 population-weighted county centres, as routed (not symmetrised). Off-diagonal median 232.4 min. Own-county time = 0.5214 x sqrt(land area) at the median effective speed of 58.3 straight-line km/h between counties (median 17.5 to 50.9 min). `# VERIFY` the own-county proxy. `dist` is great-circle km (road/straight median ratio 1.35).

## Suppressed cells and fills

| Variable | County | Rule |
|---|---|---|
| cash_rent_usd_acre | 46013 Brown | not published; NASS 'other (combined) counties' value = 99 $/acre |
| cash_rent_usd_acre | 46019 Butte | not published; NASS 'other (combined) counties' value = 99 $/acre |
| cash_rent_usd_acre | 46047 Fall River | not published; NASS 'other (combined) counties' value = 99 $/acre |
| cash_rent_usd_acre | 46063 Harding | not published; NASS 'other (combined) counties' value = 99 $/acre |
| cash_rent_usd_acre | 46071 Jackson | not published; NASS 'other (combined) counties' value = 99 $/acre |
| cash_rent_usd_acre | 46117 Stanley | not published; NASS 'other (combined) counties' value = 99 $/acre |
| cash_rent_usd_acre | 46121 Todd | not published; NASS 'other (combined) counties' value = 99 $/acre |

No BEA (D) cells for this state and year: CAEMP25N L50/70/80, CAINC45 L350/360/370 and CAINC5N L82 are published for every county (2018 to 2022 for the farm-wage lines).

## Coverage gaps and caveats

- ACS is the 5-year period estimate ending in the base year (no 1-year data for small counties); BEA and PEP are single-year. The external zone inherits ACS sampling error in the commuter totals.
- The Census API now requires a key, so ACS comes from the table-based summary files instead (same estimates).
- LODES (for the M3 PPML of kappa*lambda) and IRS SOI migration flows are not part of this build.
- Census of Agriculture is quinquennial (2022 matches the base year); the cash-rent survey is annual.
- x_km / y_km are NAD83 / UTM (EPSG:26914) at the state's middle longitude, for drawing only.
- No satellite population layer (GHS-POP) is used; census counts drive calibration (spec §8).

## County table

| FIPS | Name | Kind | N | HU | HA | TF ha | L m^2 | wA $/worker | BEA farm earnings $/job | omega | rent $/ac |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 46003 | Aurora | rural | 1,384 | 897 | 321 | 101,672 | 2.00M | 52,059 | 92,921 | 0.474 | 115 |
| 46005 | Beadle | rural | 9,186 | 8,329 | 613 | 200,850 | 9.77M | 69,043 | 160,006 | 0.481 | 130 |
| 46007 | Bennett | rural | 1,072 | 807 | 153 | 78,838 | 1.10M | 53,587 | 183,413 | 0.639 | 34 |
| 46009 | Bon Homme | rural | 2,611 | 1,640 | 382 | 98,115 | 4.17M | 52,950 | 154,841 | 0.554 | 146 |
| 46011 | Brookings | rural | 18,827 | 18,793 | 869 | 136,273 | 14.37M | 68,014 | 119,257 | 0.552 | 185 |
| 46013 | Brown | rural | 20,522 | 20,432 | 881 | 299,516 | 17.75M | 58,000 | 202,105 | 0.549 | 99* |
| 46015 | Brule | rural | 2,608 | 2,418 | 319 | 111,912 | 2.54M | 67,975 | 146,446 | 0.613 | 100 |
| 46017 | Buffalo | rural | 583 | 429 | 61 | 36,188 | 0.46M | 59,179 | 102,207 | 0.480 | 78 |
| 46019 | Butte | rural | 4,977 | 3,335 | 397 | 50,010 | 3.55M | 44,438 | 23,477 | 0.694 | 99* |
| 46021 | Campbell | rural | 761 | 589 | 224 | 94,004 | 1.33M | 77,104 | 166,712 | 0.492 | 76 |
| 46023 | Charles Mix | rural | 3,780 | 3,364 | 544 | 169,311 | 4.81M | 54,144 | 128,667 | 0.605 | 128 |
| 46025 | Clark | rural | 1,525 | 907 | 352 | 149,422 | 2.38M | 83,424 | 172,316 | 0.602 | 140 |
| 46027 | Clay | rural | 7,330 | 6,635 | 303 | 88,142 | 5.30M | 71,137 | 216,426 | 0.475 | 204 |
| 46029 | Codington | rural | 15,203 | 15,713 | 546 | 109,396 | 14.51M | 55,144 | 103,418 | 0.604 | 167 |
| 46031 | Corson | rural | 1,156 | 833 | 281 | 141,227 | 1.42M | 47,779 | 100,979 | 0.535 | 42 |
| 46033 | Custer | suburb | 3,786 | 2,317 | 197 | 14,227 | 2.99M | 67,773 | 6,051 | 0.642 | 16 |
| 46035 | Davison | rural | 10,274 | 11,502 | 303 | 76,510 | 10.24M | 49,432 | 200,210 | 0.525 | 153 |
| 46037 | Day | rural | 2,449 | 1,798 | 425 | 144,739 | 3.32M | 92,557 | 160,124 | 0.608 | 145 |
| 46039 | Deuel | rural | 2,085 | 1,105 | 347 | 95,100 | 2.88M | 68,689 | 97,991 | 0.538 | 173 |
| 46041 | Dewey | rural | 1,927 | 1,927 | 213 | 86,793 | 1.56M | 54,096 | 93,719 | 0.538 | 38 |
| 46043 | Douglas | rural | 1,433 | 1,076 | 295 | 81,927 | 2.59M | 62,847 | 142,589 | 0.421 | 139 |
| 46045 | Edmunds | rural | 1,855 | 1,354 | 321 | 176,087 | 2.59M | 72,902 | 250,523 | 0.444 | 99 |
| 46047 | Fall River | rural | 2,858 | 2,943 | 244 | 32,735 | 3.62M | 62,063 | 61,326 | 0.806 | 99* |
| 46049 | Faulk | rural | 947 | 620 | 202 | 153,468 | 1.50M | 71,317 | 234,072 | 0.479 | 97 |
| 46051 | Grant | rural | 3,685 | 3,556 | 484 | 111,613 | 4.62M | 58,794 | 170,330 | 0.480 | 150 |
| 46053 | Gregory | rural | 1,895 | 1,452 | 315 | 81,363 | 2.52M | 48,429 | 75,264 | 0.691 | 74 |
| 46055 | Haakon | rural | 798 | 597 | 146 | 131,103 | 1.14M | 89,620 | 111,927 | 0.662 | 43 |
| 46057 | Hamlin | rural | 2,927 | 2,080 | 336 | 92,960 | 2.90M | 68,056 | 139,432 | 0.532 | 179 |
| 46059 | Hand | rural | 1,609 | 1,264 | 323 | 205,213 | 2.34M | 79,586 | 151,898 | 0.492 | 104 |
| 46061 | Hanson | rural | 1,839 | 741 | 176 | 80,913 | 2.04M | 96,919 | 167,479 | 0.530 | 162 |
| 46063 | Harding | rural | 691 | 546 | 191 | 68,497 | 1.24M | 58,132 | 39,226 | 0.665 | 99* |
| 46065 | Hughes | rural | 9,176 | 9,658 | 253 | 104,776 | 7.51M | 79,185 | 77,535 | 0.541 | 80 |
| 46067 | Hutchinson | rural | 3,649 | 2,921 | 592 | 157,002 | 5.64M | 58,636 | 221,093 | 0.526 | 156 |
| 46069 | Hyde | rural | 727 | 608 | 208 | 96,292 | 1.06M | 52,326 | 119,000 | 0.431 | 72 |
| 46071 | Jackson | rural | 817 | 666 | 174 | 74,844 | 1.09M | 66,814 | 73,890 | 0.701 | 99* |
| 46073 | Jerauld | rural | 961 | 1,213 | 137 | 63,473 | 1.52M | 77,799 | 89,500 | 0.449 | 96 |
| 46075 | Jones | rural | 477 | 355 | 123 | 77,341 | 0.73M | 65,175 | 109,842 | 0.501 | 35 |
| 46077 | Kingsbury | rural | 2,505 | 1,765 | 359 | 145,883 | 3.12M | 66,499 | 172,319 | 0.509 | 152 |
| 46079 | Lake | rural | 6,017 | 5,139 | 353 | 108,885 | 6.81M | 53,101 | 151,628 | 0.508 | 194 |
| 46081 | Lawrence | rural | 14,124 | 13,916 | 197 | 8,392 | 6.69M | 39,085 | 2,763 | 0.695 | 26 |
| 46083 | Lincoln | suburb | 36,779 | 26,587 | 510 | 120,056 | 16.75M | 72,899 | 129,501 | 0.394 | 209 |
| 46085 | Lyman | rural | 1,456 | 1,157 | 275 | 151,667 | 1.83M | 68,961 | 111,513 | 0.596 | 70 |
| 46087 | McCook | suburb | 2,927 | 1,417 | 331 | 111,390 | 3.25M | 80,652 | 204,070 | 0.532 | 175 |
| 46089 | McPherson | rural | 1,072 | 679 | 269 | 119,167 | 1.95M | 83,555 | 185,526 | 0.582 | 92 |
| 46091 | Marshall | rural | 2,184 | 1,603 | 412 | 108,807 | 2.76M | 93,557 | 200,935 | 0.514 | 150 |
| 46093 | Meade | suburb | 15,919 | 9,396 | 580 | 158,340 | 8.53M | 48,623 | 22,350 | 0.691 | 32 |
| 46095 | Mellette | rural | 587 | 321 | 160 | 51,608 | 0.75M | 45,223 | 49,814 | 0.556 | 34 |
| 46097 | Miner | rural | 1,111 | 682 | 262 | 88,700 | 1.74M | 65,838 | 136,370 | 0.575 | 143 |
| 46099 | Minnehaha | core | 108,862 | 123,888 | 820 | 147,284 | 70.07M | 65,759 | 78,002 | 0.478 | 201 |
| 46101 | Moody | rural | 3,013 | 2,133 | 394 | 103,768 | 3.76M | 63,265 | 147,256 | 0.440 | 230 |
| 46102 | Oglala Lakota | rural | 3,123 | 3,652 | 125 | 33,500 | 1.75M | 78,489 | 94,695 | 0.619 | 30 |
| 46103 | Pennington | suburb | 54,623 | 61,184 | 405 | 95,169 | 34.02M | 52,414 | 36,195 | 0.691 | 37 |
| 46105 | Perkins | rural | 1,569 | 1,318 | 351 | 153,830 | 2.43M | 50,656 | 44,898 | 0.684 | 31 |
| 46107 | Potter | rural | 1,212 | 1,094 | 220 | 139,658 | 2.00M | 54,008 | 88,855 | 0.499 | 101 |
| 46109 | Roberts | rural | 4,243 | 3,408 | 605 | 163,355 | 4.47M | 62,752 | 109,642 | 0.535 | 156 |
| 46111 | Sanborn | rural | 1,225 | 599 | 213 | 79,062 | 1.34M | 104,365 | 135,641 | 0.627 | 122 |
| 46115 | Spink | rural | 2,939 | 2,259 | 441 | 288,889 | 4.09M | 92,863 | 212,187 | 0.470 | 121 |
| 46117 | Stanley | rural | 1,714 | 1,051 | 112 | 96,466 | 1.74M | 97,009 | 146,321 | 0.762 | 99* |
| 46119 | Sully | rural | 777 | 729 | 174 | 188,330 | 1.53M | 101,849 | 198,233 | 0.538 | 89 |
| 46121 | Todd | rural | 2,290 | 2,390 | 168 | 45,969 | 1.48M | 49,836 | 16,289 | 0.514 | 99* |
| 46123 | Tripp | rural | 2,599 | 2,179 | 485 | 154,258 | 3.33M | 55,223 | 95,927 | 0.536 | 64 |
| 46125 | Turner | suburb | 4,411 | 2,190 | 489 | 130,611 | 5.49M | 83,002 | 208,698 | 0.401 | 194 |
| 46127 | Union | suburb | 8,435 | 10,138 | 382 | 96,319 | 6.93M | 75,062 | 180,252 | 0.467 | 219 |
| 46129 | Walworth | rural | 2,516 | 2,139 | 179 | 93,822 | 3.15M | 65,863 | 122,209 | 0.535 | 94 |
| 46135 | Yankton | rural | 11,674 | 13,004 | 478 | 88,711 | 9.86M | 55,551 | 167,961 | 0.551 | 191 |
| 46137 | Ziebach | rural | 822 | 427 | 259 | 75,254 | 0.76M | 38,950 | 64,640 | 0.469 | 34 |
| EXT | External (out-of-state commuting) | external | 15,909 | 10,369 | 535 | 178,139 | 12.88M | 65,357 | n/a | 0.583 | n/a |

`*` filled, see above.
