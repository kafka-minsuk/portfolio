# Kansas 2022 county data: validation report

Built 2026-11-24 by `python -m urqse.data.build_state KS 2022`. 105 counties plus one external zone. Outputs: `county.parquet` (one row per zone, schema in `src/urqse/data/schema.py`) and `travel.npz` (`fips`, `t` minutes, `dist` km, rows in table order).

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
| cdl | USDA NASS Cropland Data Layer 2022, 30 m, clipped to state FIPS 20 | `KS/CDL_2022_20.tif` | 2026-11-24 | https://nassgeodata.gmu.edu/axis2/services/CDLService/GetCDLFile?year=2022&fips=20 |
| acs_b08007 | ACS 2018-2022 5-year, table-based summary file B08007 | `US/acs/acsdt5y2022-b08007.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08007.dat |
| acs_b08604 | ACS 2018-2022 5-year, table-based summary file B08604 | `US/acs/acsdt5y2022-b08604.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08604.dat |
| acs_b05005 | ACS 2018-2022 5-year, table-based summary file B05005 | `US/acs/acsdt5y2022-b05005.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b05005.dat |
| ghsl_R5_C10 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C10.zip` | 2026-11-23 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C10.zip |
| nass | Quick Stats bulk economics file `qs.economics_20261121.txt.gz` (Census of Agriculture 2022; Cash Rents Survey 2022) | `qs.economics_20261121.txt.gz` (filtered copy `*_KS.tsv.gz`) | see file | https://www.nass.usda.gov/sites/default/files/datasets/qs.economics_20261121.txt.gz |
| osrm | OSRM public demo server, car profile (OSM data as served on the build date) | `osrm/*.json` (9 cached block requests; the server caps a table at 100 coordinates) | 2026-11-24 | https://router.project-osrm.org/table/v1/driving |

## County sums against published state totals

| Column | Sum of counties | Published state value | Difference |
|---|---|---|---|
| PEP population | 2,937,150 | 2,937,150 | 0.000% |
| ACS workers by residence | 1,445,477 | 1,445,477 | 0.000% |
| ACS workers by workplace | 1,462,536 | 1,462,536 | 0.000% |
| ACS workers working out of state | 101,314 | 101,314 | 0.000% |
| BEA non-farm employment (L80) | 1,921,129 | 1,921,129 | 0.000% |
| BEA farm employment (L70) | 61,129 | 61,129 | 0.000% |
| BEA farm proprietors (L50) | 49,095 | 49,095 | 0.000% |
| BEA farm earnings $ (CAINC45 L370) | 897,889,000 | 897,889,000 | 0.000% |
| BEA farm wages + supplements $ (CAINC45 L350 + L360) | 540,267,000 | 540,267,000 | 0.000% |
| CoA hired farm labour expense $ | 765,937,000 | 765,940,000 | -0.000% |
| BEA non-farm earnings $ (CAINC5N L82) | 125,220,458,000 | 125,220,458,000 | 0.000% |
| ACS foreign born entered 2010+ | 64,841 | 64,841 | 0.000% |
| CoA owned acres | 20,464,734 | 20,464,734 | 0.000% |
| CoA rented-from-others acres | 24,329,968 | 24,329,968 | 0.000% |
| CoA land in farms, ha | 18,127,773 | 18,127,773 | -0.000% |
| CoA total cropland, ha | 11,469,126 | 11,469,126 | -0.000% |

## Model columns

- **N, HU, HA (jobs = resident workers).** Each county's BEA farm and non-farm job counts are scaled to its ACS count of workers by place of work (scale factor min 0.477, median 0.673, max 0.873; BEA counts jobs, ACS counts people by main job). Sum N = 1,563,850 = sum HU + HA = 1,563,850. Farm jobs after scaling: 41,833 (BEA 61,129). `# VERIFY` the scaling: part-time farm proprietors with an off-farm main job are counted once, in proportion to the county mix.
- **External zone.** Residents = out-of-state workers commuting in (ACS workplace total minus in-state residents working in state) = 118,373. Jobs = in-state residents working out of state = 101,314, split by the state farm share (HA = 2,898). Location: the 44 out-of-state counties within 1 km of the state (08009, 08017, 08061, 08063, 08099, 08125, 29003, 29011, 29013, 29021, 29037, 29047, 29087, 29095, 29097, 29145, 29165, 29217, 31057, 31061, 31065, 31067, 31083, 31087, 31095, 31129, 31133, 31145, 31147, 31169, 31181, 40003, 40007, 40025, 40035, 40053, 40059, 40071, 40105, 40113, 40115, 40139, 40147, 40151); travel time from a county to the zone is the OSRM time to the nearest of them. Floor space, farmland, farm labour earnings and owner share are state averages scaled to its workers / farm jobs; gateway weight 0 (immigrants settle in-state). `# VERIFY` all of these are conventions, not data, and `log(0)` in `immigration.arrival_shares` needs handling in M3.
- **TF (farmland, ha).** CDL 2022 crop, hay, fallow and tree-crop classes (codes 1-61, 66-77, 204-254), pixel-centre zonal sums on the 30 m Albers grid. State: 10,091,000 ha vs Census of Agriculture cropland 11,469,126 ha and land in farms 18,127,773 ha; county ratio TF / CoA cropland 0.32 to 1.60. Grassland/pasture (codes 62, 176) is kept separately (`pasture_ha`, 8,503,330 ha). County area covered by CDL pixels: 21,309,554 ha vs land area 21,175,364 ha (the difference is water). `# VERIFY` whether pasture belongs in T^F for livestock counties.
- **L (floor space, m^2).** GHSL GHS-BUILT-V 2020 epoch building volume / 3 m storey height (`# VERIFY` storey height; 2020 is the nearest epoch to 2022). State volume 3.81 km^3.
- **wA_obs_usd (farm labour earnings per farm worker).** Farm compensation (CAINC45 L350 wages and salaries + L360 supplements) per farm wage-and-salary job (CAEMP25N L70 - L50), mean of 2018 to 2022, each year relative to the state's non-farm earnings per non-farm job (CAINC5N L82 / CAEMP25N L80) and put at the 2022 value (65,181 $). That per-job wage prices every BEA farm job, proprietors included, giving the county farm labour bill `farm_labour_bill_usd`; wA_obs_usd = bill / HA, so it is per farm worker (ACS head) and the model's wage bill w_A H_A equals the bill in dollars. State: 42,162 $ per BEA farm job, 61,609 $ per farm worker; county range 30,062 to 112,596 $ per worker. State compensation per farm wage job by year: 2018 40,895 $, 2019 45,964 $, 2020 39,645 $, 2021 40,392 $, 2022 44,895 $. Proprietors are priced at the hired wage per job (the market price of farm labour in the county) rather than at a non-farm opportunity wage, which would assume away the farm/non-farm gap xi_A is meant to measure. `# VERIFY` the proprietor imputation: a BEA proprietor job is any sole proprietor or partner, many part-time. Contract labour (CoA 91,786,000 $) is left out: its workers are not BEA farm jobs (they are in agricultural support services, non-farm). Census of Agriculture hired labour expense (765,940,000 $ in 2022, column `hired_labor_coa_usd`) is 1.42x BEA farm compensation (540,267,000 $) and pays a different universe (every hired head, including workers on the farm under 150 days), so it is a comparison column, not the bill. `# VERIFY` that gap. The previous measure, BEA farm earnings (L370, wages + proprietors' income) per BEA farm job, is kept as `wA_bea_earn_usd`: state 14,688 $, county -45,828 to 170,804 $; it includes owner-operators' returns to owned land and capital, which spec §12.1 pays separately. The loader divides wA_obs_usd by state non-farm earnings per non-farm worker (sum over counties of non-farm earnings / HU = 88,140 $), so both sectors are per head. `# VERIFY` vintage mismatch: CAINC45/CAEMP25N are the 2023-11-16 release, CAINC5N the 2026 file (CAINC5N's revised 2022 farm earnings are 2,469,668,000 $ vs CAINC45 897,889,000 $).
- **omega.** Census of Agriculture 2022 owned / (owned + rented from others) acres in farms. State 0.457, county range 0.245 to 0.656.
- **cash_rent_usd_acre.** NASS Cash Rents Survey 2022, non-irrigated cropland. State 62 $/acre.
- **land_value_usd_acre.** Census of Agriculture 2022 estimated market value of land and buildings per acre (NASS does not publish annual county land values). State 2,324 $/acre.
- **gateway.** ACS foreign born who entered 2010 or later per resident worker, relative to the state ratio (mean 1 over workers). `# VERIFY` against spec §12.2 once the arrival block is calibrated. 8 counties have no recent foreign born in the ACS sample (Anderson, Clark, Clay, Comanche, Lincoln, Mitchell, Wilson, Woodson), so their gateway weight is 0 (log(0) in arrival_shares).
- **kind.** core = the metropolitan county with the most non-farm jobs (Johnson); suburb = other counties in a Metropolitan Statistical Area (OMB 2023) (19); rural = the rest (85). `# VERIFY` one core for a multi-metro state.
- **No farm sector** (spec §3.11): 0 counties have no BEA farm jobs.
- **Travel time t (min).** OSRM car durations between 2020 population-weighted county centres, as routed (not symmetrised). Off-diagonal median 231.4 min. Own-county time = 0.5214 x sqrt(land area) at the median effective speed of 65.3 straight-line km/h between counties (median 9.5 to 29.1 min). `# VERIFY` the own-county proxy. `dist` is great-circle km (road/straight median ratio 1.22).

## Suppressed cells and fills

| Variable | County | Rule |
|---|---|---|
| cash_rent_usd_acre | 20071 Greeley | not published; NASS 'other (combined) counties' value = 44 $/acre |
| cash_rent_usd_acre | 20199 Wallace | not published; NASS 'other (combined) counties' value = 44 $/acre |
| cash_rent_usd_acre | 20209 Wyandotte | not published; NASS 'other (combined) counties' value = 44 $/acre |

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
| 20001 | Allen | rural | 5,637 | 5,435 | 390 | 50,289 | 6.75M | 32,433 | 10,302 | 0.492 | 56 |
| 20003 | Anderson | rural | 3,378 | 2,297 | 405 | 59,537 | 4.31M | 65,934 | 25,053 | 0.565 | 58 |
| 20005 | Atchison | rural | 7,614 | 6,046 | 452 | 59,280 | 8.23M | 49,565 | 10,089 | 0.609 | 118 |
| 20007 | Barber | rural | 1,906 | 1,510 | 197 | 70,558 | 3.16M | 74,284 | -20,023 | 0.425 | 45 |
| 20009 | Barton | rural | 12,256 | 11,796 | 476 | 155,243 | 15.15M | 73,684 | 21,325 | 0.387 | 50 |
| 20011 | Bourbon | rural | 6,404 | 5,664 | 557 | 32,391 | 6.93M | 44,738 | 6,262 | 0.597 | 52 |
| 20013 | Brown | rural | 4,464 | 4,525 | 355 | 105,166 | 5.13M | 69,556 | -5,461 | 0.511 | 181 |
| 20015 | Butler | suburb | 31,549 | 20,364 | 822 | 82,178 | 25.46M | 67,309 | 12,435 | 0.566 | 45 |
| 20017 | Chase | rural | 1,146 | 820 | 151 | 18,580 | 1.43M | 68,874 | 20,892 | 0.438 | 54 |
| 20019 | Chautauqua | rural | 1,318 | 919 | 184 | 6,993 | 1.88M | 82,594 | 2,386 | 0.656 | 36 |
| 20021 | Cherokee | suburb | 8,682 | 5,535 | 500 | 64,675 | 9.67M | 38,214 | 51,259 | 0.476 | 64 |
| 20023 | Cheyenne | rural | 1,261 | 986 | 306 | 133,658 | 1.84M | 60,693 | 48,112 | 0.447 | 50 |
| 20025 | Clark | rural | 912 | 832 | 216 | 56,858 | 1.20M | 62,883 | 23,551 | 0.387 | 33 |
| 20027 | Clay | rural | 3,851 | 2,904 | 354 | 94,294 | 4.95M | 59,865 | 10,868 | 0.458 | 86 |
| 20029 | Cloud | rural | 4,076 | 3,478 | 313 | 105,082 | 5.73M | 60,663 | 9,927 | 0.508 | 92 |
| 20031 | Coffey | rural | 3,832 | 3,640 | 435 | 51,029 | 4.17M | 41,093 | 12,263 | 0.441 | 62 |
| 20033 | Comanche | rural | 855 | 650 | 178 | 43,647 | 1.17M | 35,493 | -33,887 | 0.452 | 30 |
| 20035 | Cowley | rural | 15,037 | 13,521 | 682 | 71,319 | 15.01M | 38,989 | 4,096 | 0.471 | 63 |
| 20037 | Crawford | rural | 19,152 | 19,424 | 657 | 51,917 | 17.11M | 51,413 | 7,160 | 0.507 | 66 |
| 20039 | Decatur | rural | 1,303 | 800 | 176 | 132,146 | 1.99M | 79,595 | 114,951 | 0.441 | 56 |
| 20041 | Dickinson | rural | 8,752 | 6,196 | 664 | 123,188 | 10.59M | 45,526 | 1,622 | 0.503 | 61 |
| 20043 | Doniphan | suburb | 3,677 | 2,326 | 264 | 64,757 | 3.64M | 72,781 | 6,216 | 0.532 | 189 |
| 20045 | Douglas | suburb | 65,718 | 57,500 | 661 | 32,949 | 40.77M | 43,385 | 4,160 | 0.390 | 76 |
| 20047 | Edwards | rural | 1,342 | 842 | 200 | 112,264 | 2.00M | 70,401 | 81,664 | 0.494 | 38 |
| 20049 | Elk | rural | 943 | 606 | 160 | 11,267 | 1.58M | 85,104 | -17,716 | 0.510 | 53 |
| 20051 | Ellis | rural | 16,473 | 16,637 | 409 | 98,417 | 14.67M | 56,850 | -7,870 | 0.476 | 38 |
| 20053 | Ellsworth | rural | 2,589 | 2,251 | 262 | 64,779 | 3.57M | 53,659 | 12,086 | 0.573 | 54 |
| 20055 | Finney | rural | 18,361 | 17,893 | 514 | 226,622 | 17.07M | 81,510 | 58,964 | 0.376 | 44 |
| 20057 | Ford | rural | 16,893 | 16,817 | 544 | 195,680 | 12.47M | 86,038 | 13,589 | 0.421 | 42 |
| 20059 | Franklin | rural | 12,700 | 10,123 | 695 | 55,810 | 11.57M | 112,596 | 10,680 | 0.580 | 74 |
| 20061 | Geary | suburb | 17,723 | 23,497 | 157 | 18,684 | 12.96M | 51,023 | 11,784 | 0.318 | 76 |
| 20063 | Gove | rural | 1,279 | 1,181 | 283 | 142,391 | 2.10M | 62,901 | 23,686 | 0.433 | 52 |
| 20065 | Graham | rural | 1,132 | 891 | 210 | 104,909 | 2.00M | 71,131 | -6,005 | 0.531 | 42 |
| 20067 | Grant | rural | 3,587 | 2,708 | 348 | 104,957 | 4.19M | 78,514 | -11,645 | 0.473 | 28 |
| 20069 | Gray | rural | 2,907 | 2,508 | 422 | 173,244 | 2.68M | 102,208 | 91,229 | 0.442 | 47 |
| 20071 | Greeley | rural | 709 | 517 | 189 | 173,559 | 1.12M | 83,141 | 170,804 | 0.433 | 44* |
| 20073 | Greenwood | rural | 2,818 | 1,660 | 328 | 20,968 | 3.90M | 100,543 | -12,352 | 0.491 | 52 |
| 20075 | Hamilton | rural | 1,161 | 868 | 357 | 139,432 | 1.46M | 87,440 | 154,289 | 0.458 | 34 |
| 20077 | Harper | rural | 2,140 | 1,919 | 250 | 115,662 | 3.73M | 69,995 | 1,793 | 0.412 | 44 |
| 20079 | Harvey | suburb | 16,396 | 15,208 | 525 | 98,685 | 15.30M | 56,933 | 6,595 | 0.362 | 62 |
| 20081 | Haskell | rural | 1,779 | 1,449 | 448 | 126,557 | 2.03M | 73,462 | 56,521 | 0.245 | 42 |
| 20083 | Hodgeman | rural | 842 | 443 | 208 | 108,394 | 1.29M | 82,379 | 31,920 | 0.545 | 36 |
| 20085 | Jackson | suburb | 6,378 | 3,783 | 606 | 51,353 | 5.18M | 44,476 | -16,764 | 0.633 | 87 |
| 20087 | Jefferson | suburb | 9,022 | 4,033 | 558 | 46,143 | 5.64M | 61,300 | 2,518 | 0.510 | 72 |
| 20089 | Jewell | rural | 1,272 | 675 | 258 | 130,249 | 2.47M | 73,752 | -3,686 | 0.415 | 76 |
| 20091 | Johnson | core | 329,681 | 356,456 | 413 | 19,598 | 234.84M | 38,568 | 15,841 | 0.605 | 56 |
| 20093 | Kearny | rural | 1,680 | 1,178 | 351 | 140,466 | 1.78M | 72,081 | 64,457 | 0.369 | 31 |
| 20095 | Kingman | rural | 3,486 | 2,230 | 418 | 102,497 | 4.35M | 58,044 | -638 | 0.471 | 43 |
| 20097 | Kiowa | rural | 1,232 | 980 | 218 | 73,272 | 1.35M | 70,744 | 2,503 | 0.545 | 35 |
| 20099 | Labette | rural | 9,028 | 8,893 | 639 | 53,875 | 10.33M | 69,910 | 31,842 | 0.559 | 48 |
| 20101 | Lane | rural | 782 | 551 | 207 | 114,235 | 1.21M | 98,074 | 65,592 | 0.476 | 39 |
| 20103 | Leavenworth | suburb | 36,661 | 29,019 | 891 | 30,911 | 23.67M | 30,062 | -8,720 | 0.566 | 68 |
| 20105 | Lincoln | rural | 1,406 | 950 | 258 | 81,888 | 2.12M | 78,056 | -5,085 | 0.583 | 62 |
| 20107 | Linn | suburb | 4,188 | 2,308 | 528 | 41,879 | 4.71M | 53,548 | 3,155 | 0.520 | 70 |
| 20109 | Logan | rural | 1,433 | 1,398 | 216 | 143,413 | 1.71M | 73,975 | 34,475 | 0.574 | 50 |
| 20111 | Lyon | rural | 16,237 | 16,141 | 698 | 55,036 | 14.95M | 39,268 | -1,686 | 0.441 | 68 |
| 20113 | McPherson | rural | 15,427 | 16,367 | 794 | 148,974 | 16.58M | 54,404 | -13,559 | 0.388 | 66 |
| 20115 | Marion | rural | 5,588 | 3,580 | 573 | 122,146 | 6.74M | 61,323 | 139 | 0.494 | 57 |
| 20117 | Marshall | rural | 4,827 | 4,346 | 488 | 136,066 | 6.68M | 56,803 | -45,828 | 0.454 | 127 |
| 20119 | Meade | rural | 2,000 | 1,395 | 356 | 110,337 | 2.21M | 73,352 | 67,456 | 0.461 | 39 |
| 20121 | Miami | suburb | 16,970 | 8,800 | 754 | 39,268 | 10.50M | 53,307 | -10,780 | 0.556 | 90 |
| 20123 | Mitchell | rural | 2,661 | 2,922 | 278 | 117,542 | 4.89M | 70,691 | -7,924 | 0.444 | 72 |
| 20125 | Montgomery | rural | 13,540 | 13,803 | 702 | 41,776 | 16.75M | 59,337 | 5,778 | 0.631 | 56 |
| 20127 | Morris | rural | 2,541 | 1,643 | 296 | 46,738 | 2.78M | 58,602 | 20,932 | 0.470 | 56 |
| 20129 | Morton | rural | 1,143 | 880 | 303 | 95,635 | 1.79M | 86,790 | 33,128 | 0.507 | 31 |
| 20131 | Nemaha | rural | 5,073 | 4,941 | 633 | 110,961 | 7.15M | 52,563 | -29,667 | 0.582 | 139 |
| 20133 | Neosho | rural | 6,901 | 6,914 | 495 | 49,385 | 8.99M | 47,416 | -120 | 0.563 | 46 |
| 20135 | Ness | rural | 1,395 | 1,105 | 278 | 139,796 | 2.17M | 63,401 | -94 | 0.489 | 46 |
| 20137 | Norton | rural | 2,071 | 1,998 | 234 | 110,018 | 3.12M | 70,784 | 70,836 | 0.442 | 48 |
| 20139 | Osage | suburb | 7,325 | 2,825 | 486 | 54,476 | 6.03M | 66,670 | 550 | 0.561 | 65 |
| 20141 | Osborne | rural | 1,815 | 1,649 | 239 | 107,647 | 3.01M | 56,503 | -10,208 | 0.393 | 53 |
| 20143 | Ottawa | rural | 2,894 | 1,561 | 362 | 84,525 | 2.83M | 65,533 | -450 | 0.436 | 64 |
| 20145 | Pawnee | rural | 2,774 | 2,913 | 385 | 146,293 | 3.74M | 80,996 | 24,615 | 0.343 | 41 |
| 20147 | Phillips | rural | 2,260 | 2,001 | 289 | 102,225 | 3.80M | 59,755 | -1,426 | 0.490 | 57 |
| 20149 | Pottawatomie | suburb | 12,366 | 10,613 | 600 | 42,732 | 9.70M | 53,676 | -1,709 | 0.544 | 76 |
| 20151 | Pratt | rural | 4,180 | 4,116 | 361 | 127,284 | 6.11M | 87,706 | 39,592 | 0.340 | 46 |
| 20153 | Rawlins | rural | 1,294 | 1,044 | 214 | 151,671 | 1.77M | 58,356 | 91,840 | 0.373 | 60 |
| 20155 | Reno | rural | 28,709 | 26,697 | 1,130 | 175,492 | 29.43M | 46,135 | -3,696 | 0.455 | 55 |
| 20157 | Republic | rural | 2,166 | 1,587 | 352 | 124,335 | 3.57M | 76,235 | 6,082 | 0.402 | 96 |
| 20159 | Rice | rural | 4,323 | 3,536 | 425 | 123,721 | 4.97M | 58,029 | 43,711 | 0.377 | 54 |
| 20161 | Riley | suburb | 41,152 | 38,030 | 441 | 36,272 | 23.83M | 49,276 | 162 | 0.430 | 82 |
| 20163 | Rooks | rural | 2,412 | 1,920 | 266 | 103,807 | 3.79M | 49,082 | -34,379 | 0.390 | 44 |
| 20165 | Rush | rural | 1,424 | 845 | 230 | 117,286 | 2.48M | 74,244 | -6,004 | 0.438 | 44 |
| 20167 | Russell | rural | 3,123 | 2,564 | 256 | 76,108 | 4.81M | 48,353 | -5,774 | 0.504 | 39 |
| 20169 | Saline | rural | 26,767 | 29,074 | 462 | 86,847 | 29.16M | 47,217 | -5,777 | 0.407 | 63 |
| 20171 | Scott | rural | 2,642 | 2,302 | 389 | 150,883 | 2.63M | 85,464 | 69,513 | 0.341 | 60 |
| 20173 | Sedgwick | suburb | 250,143 | 263,638 | 969 | 133,608 | 209.78M | 45,404 | -567 | 0.436 | 53 |
| 20175 | Seward | rural | 10,455 | 10,883 | 349 | 86,208 | 10.39M | 79,908 | 32,845 | 0.356 | 30 |
| 20177 | Shawnee | suburb | 83,882 | 95,010 | 547 | 35,136 | 67.07M | 48,240 | -4,536 | 0.558 | 66 |
| 20179 | Sheridan | rural | 1,349 | 976 | 237 | 142,530 | 1.75M | 100,443 | 16,825 | 0.358 | 55 |
| 20181 | Sherman | rural | 3,030 | 2,779 | 322 | 197,911 | 3.72M | 62,184 | 67,764 | 0.417 | 58 |
| 20183 | Smith | rural | 1,693 | 1,319 | 308 | 131,834 | 3.43M | 66,116 | 16,359 | 0.463 | 77 |
| 20185 | Stafford | rural | 1,943 | 1,165 | 290 | 127,505 | 2.74M | 87,050 | 20,579 | 0.494 | 42 |
| 20187 | Stanton | rural | 978 | 762 | 213 | 129,472 | 1.12M | 98,513 | 106,399 | 0.345 | 38 |
| 20189 | Stevens | rural | 2,386 | 2,032 | 309 | 124,099 | 3.60M | 82,503 | 46,520 | 0.469 | 28 |
| 20191 | Sumner | suburb | 9,872 | 6,682 | 721 | 219,704 | 11.17M | 45,419 | 20,581 | 0.347 | 52 |
| 20193 | Thomas | rural | 4,089 | 3,960 | 376 | 224,633 | 4.44M | 61,134 | 38,467 | 0.439 | 60 |
| 20195 | Trego | rural | 1,404 | 1,051 | 206 | 108,162 | 2.46M | 41,454 | 23,040 | 0.461 | 40 |
| 20197 | Wabaunsee | suburb | 3,246 | 1,318 | 333 | 32,044 | 2.93M | 56,176 | -8,077 | 0.486 | 62 |
| 20199 | Wallace | rural | 701 | 510 | 145 | 116,805 | 0.98M | 83,897 | 46,628 | 0.352 | 44* |
| 20201 | Washington | rural | 2,588 | 1,734 | 445 | 124,602 | 3.99M | 75,753 | -5,544 | 0.582 | 83 |
| 20203 | Wichita | rural | 923 | 810 | 270 | 146,170 | 1.39M | 78,733 | 82,787 | 0.294 | 56 |
| 20205 | Wilson | rural | 3,860 | 3,568 | 280 | 53,863 | 4.77M | 49,426 | 20,537 | 0.406 | 78 |
| 20207 | Woodson | rural | 1,271 | 760 | 158 | 30,773 | 1.82M | 74,608 | -19,811 | 0.484 | 54 |
| 20209 | Wyandotte | suburb | 76,861 | 95,995 | 120 | 2,872 | 74.68M | 52,445 | -3,338 | 0.528 | 44* |
| EXT | External (out-of-state commuting) | external | 118,373 | 98,416 | 2,898 | 699,032 | 104.04M | 61,609 | n/a | 0.457 | n/a |

`*` filled, see above.
