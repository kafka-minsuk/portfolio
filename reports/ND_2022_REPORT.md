# North Dakota 2022 county data: validation report

Built 2026-11-24 by `python -m urqse.data.build_state ND 2022`. 53 counties plus one external zone. Outputs: `county.parquet` (one row per zone, schema in `src/urqse/data/schema.py`) and `travel.npz` (`fips`, `t` minutes, `dist` km, rows in table order).

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
| cdl | USDA NASS Cropland Data Layer 2022, 30 m, clipped to state FIPS 38 | `ND/CDL_2022_38.tif` | 2026-11-24 | https://nassgeodata.gmu.edu/axis2/services/CDLService/GetCDLFile?year=2022&fips=38 |
| acs_b08007 | ACS 2018-2022 5-year, table-based summary file B08007 | `US/acs/acsdt5y2022-b08007.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08007.dat |
| acs_b08604 | ACS 2018-2022 5-year, table-based summary file B08604 | `US/acs/acsdt5y2022-b08604.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08604.dat |
| acs_b05005 | ACS 2018-2022 5-year, table-based summary file B05005 | `US/acs/acsdt5y2022-b05005.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b05005.dat |
| ghsl_R4_C10 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C10.zip` | 2026-11-23 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C10.zip |
| ghsl_R4_C11 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C11.zip` | 2026-11-23 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C11.zip |
| nass | Quick Stats bulk economics file `qs.economics_20261121.txt.gz` (Census of Agriculture 2022; Cash Rents Survey 2022) | `qs.economics_20261121.txt.gz` (filtered copy `*_ND.tsv.gz`) | see file | https://www.nass.usda.gov/sites/default/files/datasets/qs.economics_20261121.txt.gz |
| osrm | OSRM public demo server, car profile (OSM data as served on the build date) | `osrm/*.json` (4 cached block requests; the server caps a table at 100 coordinates) | 2026-11-24 | https://router.project-osrm.org/table/v1/driving |

## County sums against published state totals

| Column | Sum of counties | Published state value | Difference |
|---|---|---|---|
| PEP population | 779,261 | 779,261 | 0.000% |
| ACS workers by residence | 404,060 | 404,060 | 0.000% |
| ACS workers by workplace | 431,859 | 431,859 | 0.000% |
| ACS workers working out of state | 12,838 | 12,838 | 0.000% |
| BEA non-farm employment (L80) | 557,849 | 557,849 | 0.000% |
| BEA farm employment (L70) | 29,970 | 29,970 | 0.000% |
| BEA farm proprietors (L50) | 22,613 | 22,613 | 0.000% |
| BEA farm earnings $ (CAINC45 L370) | 4,908,570,000 | 4,908,570,000 | 0.000% |
| BEA farm wages + supplements $ (CAINC45 L350 + L360) | 312,055,000 | 312,055,000 | 0.000% |
| CoA hired farm labour expense $ | 495,580,000 | 495,581,000 | -0.000% |
| BEA non-farm earnings $ (CAINC5N L82) | 36,190,715,000 | 36,190,715,000 | 0.000% |
| ACS foreign born entered 2010+ | 18,589 | 18,589 | 0.000% |
| CoA owned acres | 17,760,268 | 17,760,268 | 0.000% |
| CoA rented-from-others acres | 20,776,754 | 20,776,754 | 0.000% |
| CoA land in farms, ha | 15,595,379 | 15,595,379 | 0.000% |
| CoA total cropland, ha | 10,627,050 | 10,627,050 | 0.000% |

## Model columns

- **N, HU, HA (jobs = resident workers).** Each county's BEA farm and non-farm job counts are scaled to its ACS count of workers by place of work (scale factor min 0.377, median 0.693, max 0.840; BEA counts jobs, ACS counts people by main job). Sum N = 444,697 = sum HU + HA = 444,697. Farm jobs after scaling: 20,863 (BEA 29,970). `# VERIFY` the scaling: part-time farm proprietors with an off-farm main job are counted once, in proportion to the county mix.
- **External zone.** Residents = out-of-state workers commuting in (ACS workplace total minus in-state residents working in state) = 40,637. Jobs = in-state residents working out of state = 12,838, split by the state farm share (HA = 620). Location: the 20 out-of-state counties within 1 km of the state (27027, 27069, 27089, 27107, 27119, 27155, 27167, 30025, 30083, 30085, 30091, 30109, 46013, 46021, 46031, 46063, 46089, 46091, 46105, 46109); travel time from a county to the zone is the OSRM time to the nearest of them. Floor space, farmland, farm labour earnings and owner share are state averages scaled to its workers / farm jobs; gateway weight 0 (immigrants settle in-state). `# VERIFY` all of these are conventions, not data, and `log(0)` in `immigration.arrival_shares` needs handling in M3.
- **TF (farmland, ha).** CDL 2022 crop, hay, fallow and tree-crop classes (codes 1-61, 66-77, 204-254), pixel-centre zonal sums on the 30 m Albers grid. State: 9,853,886 ha vs Census of Agriculture cropland 10,627,050 ha and land in farms 15,595,379 ha; county ratio TF / CoA cropland 0.69 to 1.28. Grassland/pasture (codes 62, 176) is kept separately (`pasture_ha`, 4,373,867 ha). County area covered by CDL pixels: 18,310,882 ha vs land area 17,869,431 ha (the difference is water). `# VERIFY` whether pasture belongs in T^F for livestock counties.
- **L (floor space, m^2).** GHSL GHS-BUILT-V 2020 epoch building volume / 3 m storey height (`# VERIFY` storey height; 2020 is the nearest epoch to 2022). State volume 1.04 km^3.
- **wA_obs_usd (farm labour earnings per farm worker).** Farm compensation (CAINC45 L350 wages and salaries + L360 supplements) per farm wage-and-salary job (CAEMP25N L70 - L50), mean of 2018 to 2022, each year relative to the state's non-farm earnings per non-farm job (CAINC5N L82 / CAEMP25N L80) and put at the 2022 value (64,875 $). That per-job wage prices every BEA farm job, proprietors included, giving the county farm labour bill `farm_labour_bill_usd`; wA_obs_usd = bill / HA, so it is per farm worker (ACS head) and the model's wage bill w_A H_A equals the bill in dollars. State: 42,944 $ per BEA farm job, 61,690 $ per farm worker; county range 36,326 to 135,970 $ per worker. State compensation per farm wage job by year: 2018 41,607 $, 2019 46,039 $, 2020 39,575 $, 2021 40,562 $, 2022 42,416 $. Proprietors are priced at the hired wage per job (the market price of farm labour in the county) rather than at a non-farm opportunity wage, which would assume away the farm/non-farm gap xi_A is meant to measure. `# VERIFY` the proprietor imputation: a BEA proprietor job is any sole proprietor or partner, many part-time. Contract labour (CoA 43,227,000 $) is left out: its workers are not BEA farm jobs (they are in agricultural support services, non-farm). Census of Agriculture hired labour expense (495,581,000 $ in 2022, column `hired_labor_coa_usd`) is 1.59x BEA farm compensation (312,055,000 $) and pays a different universe (every hired head, including workers on the farm under 150 days), so it is a comparison column, not the bill. `# VERIFY` that gap. The previous measure, BEA farm earnings (L370, wages + proprietors' income) per BEA farm job, is kept as `wA_bea_earn_usd`: state 163,783 $, county 1,797 to 405,400 $; it includes owner-operators' returns to owned land and capital, which spec §12.1 pays separately. The loader divides wA_obs_usd by state non-farm earnings per non-farm worker (sum over counties of non-farm earnings / HU = 88,056 $), so both sectors are per head. `# VERIFY` vintage mismatch: CAINC45/CAEMP25N are the 2023-11-16 release, CAINC5N the 2026 file (CAINC5N's revised 2022 farm earnings are 5,083,244,000 $ vs CAINC45 4,908,570,000 $).
- **omega.** Census of Agriculture 2022 owned / (owned + rented from others) acres in farms. State 0.461, county range 0.294 to 0.749.
- **cash_rent_usd_acre.** NASS Cash Rents Survey 2022, non-irrigated cropland. State 73 $/acre.
- **land_value_usd_acre.** Census of Agriculture 2022 estimated market value of land and buildings per acre (NASS does not publish annual county land values). State 2,139 $/acre.
- **gateway.** ACS foreign born who entered 2010 or later per resident worker, relative to the state ratio (mean 1 over workers). `# VERIFY` against spec §12.2 once the arrival block is calibrated. 9 counties have no recent foreign born in the ACS sample (Billings, Eddy, Foster, Hettinger, Kidder, Oliver, Sheridan, Slope, Steele), so their gateway weight is 0 (log(0) in arrival_shares).
- **kind.** core = the metropolitan county with the most non-farm jobs (Cass); suburb = other counties in a Metropolitan Statistical Area (OMB 2023) (7); rural = the rest (45). `# VERIFY` one core for a multi-metro state.
- **No farm sector** (spec §3.11): 0 counties have no BEA farm jobs.
- **Travel time t (min).** OSRM car durations between 2020 population-weighted county centres, as routed (not symmetrised). Off-diagonal median 227.6 min. Own-county time = 0.5214 x sqrt(land area) at the median effective speed of 58.7 straight-line km/h between counties (median 21.5 to 45.1 min). `# VERIFY` the own-county proxy. `dist` is great-circle km (road/straight median ratio 1.33).

## Suppressed cells and fills

| Variable | County | Rule |
|---|---|---|
| cash_rent_usd_acre | 38019 Cavalier | not published; NASS 'other (combined) counties' value = 72 $/acre |
| cash_rent_usd_acre | 38085 Sioux | not published; NASS 'other (combined) counties' value = 72 $/acre |

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
| 38001 | Adams | rural | 1,030 | 793 | 229 | 134,962 | 1.79M | 61,899 | 1,797 | 0.476 | 39 |
| 38003 | Barnes | rural | 5,416 | 4,272 | 579 | 272,476 | 6.16M | 78,101 | 230,205 | 0.420 | 96 |
| 38005 | Benson | rural | 2,014 | 1,611 | 369 | 209,036 | 2.66M | 61,174 | 222,423 | 0.473 | 57 |
| 38007 | Billings | rural | 418 | 322 | 67 | 42,063 | 0.93M | 135,970 | 29,341 | 0.749 | 33 |
| 38009 | Bottineau | rural | 2,976 | 2,333 | 449 | 297,109 | 3.94M | 77,209 | 213,054 | 0.403 | 52 |
| 38011 | Bowman | rural | 1,413 | 1,225 | 230 | 115,713 | 2.18M | 71,185 | 63,206 | 0.561 | 36 |
| 38013 | Burke | rural | 1,039 | 697 | 261 | 161,763 | 1.57M | 60,693 | 168,330 | 0.498 | 40 |
| 38015 | Burleigh | suburb | 50,478 | 54,313 | 629 | 167,164 | 35.44M | 49,704 | 82,766 | 0.456 | 59 |
| 38017 | Cass | core | 107,914 | 123,789 | 824 | 387,356 | 64.42M | 66,823 | 207,074 | 0.294 | 130 |
| 38019 | Cavalier | rural | 1,691 | 1,288 | 410 | 314,971 | 3.37M | 69,322 | 390,275 | 0.403 | 72* |
| 38021 | Dickey | rural | 2,511 | 1,787 | 389 | 176,477 | 3.43M | 62,111 | 248,388 | 0.428 | 116 |
| 38023 | Divide | rural | 971 | 781 | 238 | 211,237 | 1.73M | 49,841 | 92,822 | 0.432 | 34 |
| 38025 | Dunn | rural | 1,881 | 2,173 | 397 | 153,830 | 3.68M | 53,728 | 6,701 | 0.527 | 36 |
| 38027 | Eddy | rural | 1,098 | 720 | 202 | 85,137 | 1.29M | 60,593 | 266,887 | 0.570 | 61 |
| 38029 | Emmons | rural | 1,536 | 1,113 | 386 | 194,086 | 2.64M | 59,086 | 216,312 | 0.403 | 82 |
| 38031 | Foster | rural | 1,794 | 1,707 | 289 | 116,841 | 2.21M | 52,117 | 213,341 | 0.370 | 78 |
| 38033 | Golden Valley | rural | 808 | 619 | 134 | 62,216 | 1.21M | 90,038 | 44,724 | 0.609 | 29 |
| 38035 | Grand Forks | suburb | 39,811 | 42,608 | 870 | 276,540 | 27.29M | 66,808 | 175,611 | 0.383 | 101 |
| 38037 | Grant | rural | 1,034 | 704 | 307 | 156,122 | 2.08M | 61,574 | 83,929 | 0.441 | 38 |
| 38039 | Griggs | rural | 1,106 | 808 | 288 | 110,989 | 1.73M | 70,435 | 198,463 | 0.472 | 78 |
| 38041 | Hettinger | rural | 1,121 | 804 | 341 | 205,216 | 2.01M | 44,648 | 43,819 | 0.468 | 48 |
| 38043 | Kidder | rural | 1,009 | 574 | 252 | 135,480 | 2.05M | 99,742 | 121,139 | 0.517 | 51 |
| 38045 | LaMoure | rural | 2,036 | 1,590 | 479 | 209,067 | 2.99M | 42,110 | 242,816 | 0.412 | 104 |
| 38047 | Logan | rural | 846 | 616 | 232 | 111,504 | 1.67M | 43,437 | 161,590 | 0.455 | 64 |
| 38049 | McHenry | suburb | 2,501 | 1,515 | 562 | 227,165 | 3.33M | 43,291 | 103,763 | 0.486 | 46 |
| 38051 | McIntosh | rural | 1,293 | 998 | 292 | 130,483 | 2.25M | 49,754 | 147,024 | 0.470 | 65 |
| 38053 | McKenzie | rural | 6,700 | 7,896 | 361 | 163,720 | 7.51M | 44,067 | 30,120 | 0.576 | 30 |
| 38055 | McLean | rural | 4,413 | 3,748 | 593 | 328,224 | 5.83M | 44,121 | 174,304 | 0.401 | 60 |
| 38057 | Mercer | rural | 3,756 | 4,190 | 272 | 97,603 | 4.47M | 51,141 | 48,532 | 0.429 | 44 |
| 38059 | Morton | suburb | 18,192 | 12,234 | 571 | 184,661 | 14.82M | 57,974 | 41,185 | 0.524 | 42 |
| 38061 | Mountrail | rural | 4,339 | 5,185 | 438 | 242,391 | 6.47M | 60,508 | 92,567 | 0.405 | 40 |
| 38063 | Nelson | rural | 1,350 | 893 | 331 | 140,317 | 2.03M | 54,296 | 160,056 | 0.489 | 62 |
| 38065 | Oliver | suburb | 775 | 668 | 170 | 71,928 | 1.33M | 59,927 | 77,373 | 0.335 | 42 |
| 38067 | Pembina | rural | 3,169 | 2,936 | 553 | 234,446 | 4.86M | 89,139 | 216,719 | 0.376 | 113 |
| 38069 | Pierce | rural | 1,831 | 1,538 | 302 | 157,592 | 2.66M | 53,848 | 173,580 | 0.545 | 56 |
| 38071 | Ramsey | rural | 5,889 | 5,621 | 423 | 200,672 | 5.58M | 63,412 | 204,856 | 0.511 | 64 |
| 38073 | Ransom | rural | 2,688 | 2,057 | 385 | 130,189 | 3.39M | 79,497 | 166,056 | 0.534 | 100 |
| 38075 | Renville | suburb | 1,156 | 615 | 154 | 177,477 | 1.61M | 67,188 | 405,400 | 0.353 | 53 |
| 38077 | Richland | rural | 8,341 | 8,194 | 738 | 284,396 | 8.83M | 74,879 | 158,856 | 0.348 | 139 |
| 38079 | Rolette | rural | 4,429 | 4,120 | 368 | 123,704 | 3.12M | 56,979 | 140,870 | 0.523 | 46 |
| 38081 | Sargent | rural | 2,051 | 2,559 | 405 | 141,459 | 2.91M | 57,329 | 192,100 | 0.492 | 113 |
| 38083 | Sheridan | rural | 624 | 337 | 232 | 124,272 | 1.29M | 43,488 | 209,961 | 0.447 | 49 |
| 38085 | Sioux | rural | 1,037 | 1,399 | 165 | 50,091 | 0.98M | 36,326 | 98,811 | 0.394 | 72* |
| 38087 | Slope | rural | 412 | 149 | 149 | 108,627 | 0.75M | 78,772 | 20,644 | 0.691 | 40 |
| 38089 | Stark | rural | 16,528 | 16,670 | 478 | 192,300 | 15.64M | 49,897 | 18,549 | 0.486 | 42 |
| 38091 | Steele | rural | 832 | 555 | 234 | 150,529 | 1.47M | 71,427 | 258,792 | 0.409 | 86 |
| 38093 | Stutsman | rural | 10,640 | 10,125 | 809 | 338,532 | 11.36M | 53,357 | 216,200 | 0.448 | 88 |
| 38095 | Towner | rural | 1,037 | 756 | 323 | 199,340 | 1.73M | 68,194 | 267,512 | 0.482 | 52 |
| 38097 | Traill | rural | 4,077 | 3,371 | 439 | 198,578 | 4.44M | 56,172 | 180,254 | 0.383 | 128 |
| 38099 | Walsh | rural | 5,127 | 4,292 | 793 | 248,321 | 6.00M | 91,331 | 175,101 | 0.432 | 97 |
| 38101 | Ward | suburb | 37,132 | 36,121 | 624 | 346,198 | 25.60M | 57,709 | 161,387 | 0.405 | 56 |
| 38103 | Wells | rural | 1,840 | 1,577 | 363 | 238,315 | 3.06M | 63,323 | 370,935 | 0.431 | 71 |
| 38105 | Williams | rural | 19,950 | 23,430 | 485 | 315,002 | 15.03M | 45,093 | 114,181 | 0.410 | 34 |
| EXT | External (out-of-state commuting) | external | 40,637 | 12,218 | 620 | 292,929 | 34.88M | 61,690 | n/a | 0.461 | n/a |

`*` filled, see above.
