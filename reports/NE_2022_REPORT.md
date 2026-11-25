# Nebraska 2022 county data: validation report

Built 2026-11-24 by `python -m urqse.data.build_state NE 2022`. 93 counties plus one external zone. Outputs: `county.parquet` (one row per zone, schema in `src/urqse/data/schema.py`) and `travel.npz` (`fips`, `t` minutes, `dist` km, rows in table order).

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
| cdl | USDA NASS Cropland Data Layer 2022, 30 m, clipped to state FIPS 31 | `NE/CDL_2022_31.tif` | 2026-11-24 | https://nassgeodata.gmu.edu/axis2/services/CDLService/GetCDLFile?year=2022&fips=31 |
| acs_b08007 | ACS 2018-2022 5-year, table-based summary file B08007 | `US/acs/acsdt5y2022-b08007.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08007.dat |
| acs_b08604 | ACS 2018-2022 5-year, table-based summary file B08604 | `US/acs/acsdt5y2022-b08604.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08604.dat |
| acs_b05005 | ACS 2018-2022 5-year, table-based summary file B05005 | `US/acs/acsdt5y2022-b05005.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b05005.dat |
| ghsl_R4_C10 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C10.zip` | 2026-11-23 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C10.zip |
| ghsl_R4_C11 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C11.zip` | 2026-11-23 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C11.zip |
| ghsl_R5_C10 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C10.zip` | 2026-11-23 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C10.zip |
| ghsl_R5_C11 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C11.zip` | 2026-11-23 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C11.zip |
| nass | Quick Stats bulk economics file `qs.economics_20261121.txt.gz` (Census of Agriculture 2022; Cash Rents Survey 2022) | `qs.economics_20261121.txt.gz` (filtered copy `*_NE.tsv.gz`) | see file | https://www.nass.usda.gov/sites/default/files/datasets/qs.economics_20261121.txt.gz |
| osrm | OSRM public demo server, car profile (OSM data as served on the build date) | `osrm/*.json` (9 cached block requests; the server caps a table at 100 coordinates) | 2026-11-24 | https://router.project-osrm.org/table/v1/driving |

## County sums against published state totals

| Column | Sum of counties | Published state value | Difference |
|---|---|---|---|
| PEP population | 1,967,923 | 1,967,923 | 0.000% |
| ACS workers by residence | 1,004,637 | 1,004,637 | 0.000% |
| ACS workers by workplace | 1,022,493 | 1,022,493 | 0.000% |
| ACS workers working out of state | 26,393 | 26,393 | 0.000% |
| BEA non-farm employment (L80) | 1,319,792 | 1,319,792 | 0.000% |
| BEA farm employment (L70) | 52,319 | 52,319 | 0.000% |
| BEA farm proprietors (L50) | 36,572 | 36,572 | 0.000% |
| BEA farm earnings $ (CAINC45 L370) | 3,699,649,000 | 3,699,649,000 | 0.000% |
| BEA farm wages + supplements $ (CAINC45 L350 + L360) | 643,072,000 | 643,072,000 | 0.000% |
| CoA hired farm labour expense $ | 934,813,000 | 934,813,000 | 0.000% |
| BEA non-farm earnings $ (CAINC5N L82) | 89,009,454,000 | 89,009,454,000 | 0.000% |
| ACS foreign born entered 2010+ | 56,774 | 56,774 | 0.000% |
| CoA owned acres | 24,362,210 | 24,362,210 | 0.000% |
| CoA rented-from-others acres | 19,613,483 | 19,613,483 | 0.000% |
| CoA land in farms, ha | 17,796,332 | 17,796,332 | 0.000% |
| CoA total cropland, ha | 8,586,425 | 8,586,425 | 0.000% |

## Model columns

- **N, HU, HA (jobs = resident workers).** Each county's BEA farm and non-farm job counts are scaled to its ACS count of workers by place of work (scale factor min 0.482, median 0.673, max 0.872; BEA counts jobs, ACS counts people by main job). Sum N = 1,048,886 = sum HU + HA = 1,048,886. Farm jobs after scaling: 35,737 (BEA 52,319). `# VERIFY` the scaling: part-time farm proprietors with an off-farm main job are counted once, in proportion to the county mix.
- **External zone.** Residents = out-of-state workers commuting in (ACS workplace total minus in-state residents working in state) = 44,249. Jobs = in-state residents working out of state = 26,393, split by the state farm share (HA = 922). Location: the 40 out-of-state counties within 1 km of the state (08075, 08095, 08115, 08123, 08125, 19071, 19085, 19129, 19133, 19155, 19193, 20013, 20023, 20039, 20043, 20089, 20117, 20131, 20137, 20147, 20153, 20157, 20183, 20201, 29005, 29087, 46007, 46009, 46023, 46027, 46047, 46053, 46102, 46121, 46123, 46127, 46135, 56015, 56021, 56027); travel time from a county to the zone is the OSRM time to the nearest of them. Floor space, farmland, farm labour earnings and owner share are state averages scaled to its workers / farm jobs; gateway weight 0 (immigrants settle in-state). `# VERIFY` all of these are conventions, not data, and `log(0)` in `immigration.arrival_shares` needs handling in M3.
- **TF (farmland, ha).** CDL 2022 crop, hay, fallow and tree-crop classes (codes 1-61, 66-77, 204-254), pixel-centre zonal sums on the 30 m Albers grid. State: 7,906,978 ha vs Census of Agriculture cropland 8,586,425 ha and land in farms 17,796,332 ha; county ratio TF / CoA cropland 0.03 to 1.73. Grassland/pasture (codes 62, 176) is kept separately (`pasture_ha`, 10,134,693 ha). County area covered by CDL pixels: 20,033,459 ha vs land area 19,895,510 ha (the difference is water). `# VERIFY` whether pasture belongs in T^F for livestock counties.
- **L (floor space, m^2).** GHSL GHS-BUILT-V 2020 epoch building volume / 3 m storey height (`# VERIFY` storey height; 2020 is the nearest epoch to 2022). State volume 2.62 km^3.
- **wA_obs_usd (farm labour earnings per farm worker).** Farm compensation (CAINC45 L350 wages and salaries + L360 supplements) per farm wage-and-salary job (CAEMP25N L70 - L50), mean of 2018 to 2022, each year relative to the state's non-farm earnings per non-farm job (CAINC5N L82 / CAEMP25N L80) and put at the 2022 value (67,442 $). That per-job wage prices every BEA farm job, proprietors included, giving the county farm labour bill `farm_labour_bill_usd`; wA_obs_usd = bill / HA, so it is per farm worker (ACS head) and the model's wage bill w_A H_A equals the bill in dollars. State: 45,398 $ per BEA farm job, 66,463 $ per farm worker; county range 31,698 to 126,782 $ per worker. State compensation per farm wage job by year: 2018 41,646 $, 2019 45,387 $, 2020 39,889 $, 2021 39,178 $, 2022 40,838 $. Proprietors are priced at the hired wage per job (the market price of farm labour in the county) rather than at a non-farm opportunity wage, which would assume away the farm/non-farm gap xi_A is meant to measure. `# VERIFY` the proprietor imputation: a BEA proprietor job is any sole proprietor or partner, many part-time. Contract labour (CoA 100,551,000 $) is left out: its workers are not BEA farm jobs (they are in agricultural support services, non-farm). Census of Agriculture hired labour expense (934,813,000 $ in 2022, column `hired_labor_coa_usd`) is 1.45x BEA farm compensation (643,072,000 $) and pays a different universe (every hired head, including workers on the farm under 150 days), so it is a comparison column, not the bill. `# VERIFY` that gap. The previous measure, BEA farm earnings (L370, wages + proprietors' income) per BEA farm job, is kept as `wA_bea_earn_usd`: state 70,713 $, county -14,802 to 217,657 $; it includes owner-operators' returns to owned land and capital, which spec §12.1 pays separately. The loader divides wA_obs_usd by state non-farm earnings per non-farm worker (sum over counties of non-farm earnings / HU = 90,204 $), so both sectors are per head. `# VERIFY` vintage mismatch: CAINC45/CAEMP25N are the 2023-11-16 release, CAINC5N the 2026 file (CAINC5N's revised 2022 farm earnings are 4,717,400,000 $ vs CAINC45 3,699,649,000 $).
- **omega.** Census of Agriculture 2022 owned / (owned + rented from others) acres in farms. State 0.554, county range 0.274 to 0.781.
- **cash_rent_usd_acre.** NASS Cash Rents Survey 2022, non-irrigated cropland. State 162 $/acre.
- **land_value_usd_acre.** Census of Agriculture 2022 estimated market value of land and buildings per acre (NASS does not publish annual county land values). State 3,437 $/acre.
- **gateway.** ACS foreign born who entered 2010 or later per resident worker, relative to the state ratio (mean 1 over workers). `# VERIFY` against spec §12.2 once the arrival block is calibrated. 19 counties have no recent foreign born in the ACS sample (Arthur, Blaine, Cedar, Cherry, Deuel, Dundy, Garden, Garfield, Gosper, Hamilton, Hitchcock, Hooker, Loup, Nance, Nuckolls, Rock, Sherman, Thomas, Valley), so their gateway weight is 0 (log(0) in arrival_shares).
- **kind.** core = the metropolitan county with the most non-farm jobs (Douglas); suburb = other counties in a Metropolitan Statistical Area (OMB 2023) (10); rural = the rest (82). `# VERIFY` one core for a multi-metro state.
- **No farm sector** (spec §3.11): 0 counties have no BEA farm jobs.
- **Travel time t (min).** OSRM car durations between 2020 population-weighted county centres, as routed (not symmetrised). Off-diagonal median 207.3 min. Own-county time = 0.5214 x sqrt(land area) at the median effective speed of 66.5 straight-line km/h between counties (median 11.7 to 58.5 min). `# VERIFY` the own-county proxy. `dist` is great-circle km (road/straight median ratio 1.22).

## Suppressed cells and fills

| Variable | County | Rule |
|---|---|---|
| cash_rent_usd_acre | 31005 Arthur | not published; NASS 'other (combined) counties' value = 53 $/acre |
| cash_rent_usd_acre | 31009 Blaine | not published; NASS 'other (combined) counties' value = 53 $/acre |
| cash_rent_usd_acre | 31035 Clay | not published; NASS 'other (combined) counties' value = 53 $/acre |
| cash_rent_usd_acre | 31045 Dawes | not published; NASS 'other (combined) counties' value = 53 $/acre |
| cash_rent_usd_acre | 31049 Deuel | not published; NASS 'other (combined) counties' value = 53 $/acre |
| cash_rent_usd_acre | 31069 Garden | not published; NASS 'other (combined) counties' value = 53 $/acre |
| cash_rent_usd_acre | 31075 Grant | not published; NASS 'other (combined) counties' value = 53 $/acre |
| cash_rent_usd_acre | 31091 Hooker | not published; NASS 'other (combined) counties' value = 53 $/acre |
| cash_rent_usd_acre | 31105 Kimball | not published; NASS 'other (combined) counties' value = 53 $/acre |
| cash_rent_usd_acre | 31111 Lincoln | not published; NASS 'other (combined) counties' value = 53 $/acre |
| cash_rent_usd_acre | 31113 Logan | not published; NASS 'other (combined) counties' value = 53 $/acre |
| cash_rent_usd_acre | 31115 Loup | not published; NASS 'other (combined) counties' value = 53 $/acre |
| cash_rent_usd_acre | 31117 McPherson | not published; NASS 'other (combined) counties' value = 53 $/acre |
| cash_rent_usd_acre | 31123 Morrill | not published; NASS 'other (combined) counties' value = 53 $/acre |
| cash_rent_usd_acre | 31157 Scotts Bluff | not published; NASS 'other (combined) counties' value = 53 $/acre |
| cash_rent_usd_acre | 31165 Sioux | not published; NASS 'other (combined) counties' value = 53 $/acre |
| cash_rent_usd_acre | 31171 Thomas | not published; NASS 'other (combined) counties' value = 53 $/acre |

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
| 31001 | Adams | rural | 15,172 | 14,878 | 407 | 116,958 | 15.06M | 75,173 | 134,545 | 0.328 | 134 |
| 31003 | Antelope | rural | 3,227 | 2,276 | 584 | 153,283 | 4.59M | 66,470 | 75,498 | 0.504 | 136 |
| 31005 | Arthur | rural | 219 | 113 | 63 | 3,986 | 0.22M | 111,547 | 43,386 | 0.682 | 53* |
| 31007 | Banner | rural | 348 | 134 | 118 | 53,791 | 0.54M | 110,731 | 81,624 | 0.677 | 34 |
| 31009 | Blaine | rural | 200 | 101 | 70 | 4,639 | 0.34M | 83,833 | 50,664 | 0.579 | 53* |
| 31011 | Boone | rural | 2,748 | 2,401 | 506 | 124,179 | 3.81M | 86,796 | 77,760 | 0.565 | 177 |
| 31013 | Box Butte | rural | 5,148 | 5,116 | 449 | 134,725 | 6.41M | 82,559 | 100,573 | 0.611 | 37 |
| 31015 | Boyd | rural | 848 | 567 | 174 | 37,327 | 1.19M | 39,421 | 147,120 | 0.546 | 110 |
| 31017 | Brown | rural | 1,253 | 1,106 | 213 | 26,948 | 1.85M | 76,716 | 89,834 | 0.479 | 56 |
| 31019 | Buffalo | rural | 27,193 | 27,942 | 816 | 132,476 | 17.94M | 56,215 | 44,751 | 0.450 | 124 |
| 31021 | Burt | rural | 2,979 | 1,764 | 366 | 106,286 | 3.56M | 71,443 | 77,145 | 0.405 | 238 |
| 31023 | Butler | rural | 4,408 | 2,385 | 523 | 118,431 | 5.11M | 73,902 | 68,097 | 0.406 | 205 |
| 31025 | Cass | suburb | 13,699 | 6,344 | 407 | 107,242 | 10.56M | 68,228 | 52,900 | 0.413 | 222 |
| 31027 | Cedar | rural | 4,226 | 2,574 | 576 | 142,627 | 5.65M | 71,452 | 71,886 | 0.484 | 222 |
| 31029 | Chase | rural | 1,688 | 1,453 | 271 | 114,564 | 2.14M | 89,519 | 127,930 | 0.397 | 50 |
| 31031 | Cherry | rural | 2,804 | 2,330 | 514 | 24,087 | 3.01M | 63,980 | 42,898 | 0.748 | 36 |
| 31033 | Cheyenne | rural | 4,536 | 4,294 | 418 | 183,911 | 4.81M | 42,574 | 49,034 | 0.578 | 34 |
| 31035 | Clay | rural | 3,030 | 2,155 | 401 | 115,454 | 3.91M | 89,658 | 80,594 | 0.414 | 53* |
| 31037 | Colfax | rural | 5,301 | 4,056 | 460 | 86,610 | 5.59M | 80,433 | 79,747 | 0.422 | 234 |
| 31039 | Cuming | rural | 4,618 | 3,531 | 676 | 125,256 | 6.37M | 79,649 | 159,754 | 0.506 | 259 |
| 31041 | Custer | rural | 5,072 | 4,022 | 854 | 165,862 | 6.48M | 80,802 | 38,619 | 0.532 | 89 |
| 31043 | Dakota | suburb | 10,396 | 12,082 | 200 | 51,239 | 7.43M | 47,905 | 99,936 | 0.274 | 254 |
| 31045 | Dawes | rural | 4,292 | 3,648 | 357 | 54,431 | 3.54M | 31,698 | 11,180 | 0.615 | 53* |
| 31047 | Dawson | rural | 12,263 | 10,720 | 728 | 129,324 | 10.28M | 67,697 | 74,139 | 0.398 | 103 |
| 31049 | Deuel | rural | 876 | 553 | 145 | 78,010 | 1.16M | 61,236 | 39,325 | 0.412 | 53* |
| 31051 | Dixon | rural | 2,734 | 1,396 | 281 | 91,076 | 3.26M | 120,588 | 43,302 | 0.538 | 235 |
| 31053 | Dodge | rural | 17,862 | 17,337 | 556 | 113,194 | 16.74M | 59,286 | 108,022 | 0.339 | 220 |
| 31055 | Douglas | core | 301,107 | 345,471 | 301 | 24,876 | 251.06M | 114,615 | 48,872 | 0.545 | 230 |
| 31057 | Dundy | rural | 945 | 768 | 267 | 84,041 | 1.16M | 59,678 | 143,034 | 0.510 | 44 |
| 31059 | Fillmore | rural | 2,929 | 2,323 | 358 | 129,669 | 3.80M | 70,681 | 83,917 | 0.317 | 161 |
| 31061 | Franklin | rural | 1,347 | 692 | 202 | 71,179 | 1.79M | 77,868 | 41,682 | 0.449 | 100 |
| 31063 | Frontier | rural | 1,171 | 751 | 218 | 91,843 | 1.49M | 56,091 | 75,251 | 0.534 | 62 |
| 31065 | Furnas | rural | 2,189 | 2,051 | 347 | 103,897 | 2.54M | 83,187 | 54,074 | 0.480 | 80 |
| 31067 | Gage | rural | 10,513 | 8,514 | 822 | 160,016 | 12.07M | 48,912 | 37,966 | 0.485 | 163 |
| 31069 | Garden | rural | 696 | 493 | 158 | 56,215 | 1.25M | 77,085 | 58,288 | 0.598 | 53* |
| 31071 | Garfield | rural | 944 | 800 | 168 | 10,252 | 1.14M | 44,060 | 15,335 | 0.469 | 87 |
| 31073 | Gosper | rural | 915 | 481 | 131 | 59,339 | 1.20M | 126,782 | 35,141 | 0.454 | 86 |
| 31075 | Grant | rural | 344 | 246 | 74 | 459 | 0.30M | 60,212 | 45,648 | 0.781 | 53* |
| 31077 | Greeley | rural | 986 | 634 | 226 | 56,322 | 1.56M | 84,658 | 60,814 | 0.615 | 119 |
| 31079 | Hall | suburb | 30,635 | 34,085 | 528 | 96,750 | 26.87M | 64,456 | 55,152 | 0.458 | 123 |
| 31081 | Hamilton | rural | 4,694 | 3,699 | 387 | 120,129 | 5.12M | 69,723 | 116,787 | 0.358 | 167 |
| 31083 | Harlan | rural | 1,479 | 918 | 231 | 83,058 | 1.95M | 75,757 | 94,951 | 0.540 | 93 |
| 31085 | Hayes | rural | 427 | 221 | 144 | 66,713 | 0.56M | 92,923 | 111,701 | 0.645 | 56 |
| 31087 | Hitchcock | rural | 1,126 | 685 | 172 | 86,080 | 1.61M | 61,842 | 77,137 | 0.633 | 54 |
| 31089 | Holt | rural | 5,183 | 4,329 | 929 | 140,774 | 6.20M | 73,507 | 50,356 | 0.576 | 73 |
| 31091 | Hooker | rural | 306 | 279 | 43 | 973 | 0.34M | 81,710 | -14,802 | 0.633 | 53* |
| 31093 | Howard | suburb | 3,189 | 1,543 | 376 | 71,224 | 3.30M | 69,107 | 47,802 | 0.611 | 122 |
| 31095 | Jefferson | rural | 3,428 | 3,171 | 520 | 93,139 | 5.94M | 62,176 | 40,310 | 0.481 | 148 |
| 31097 | Johnson | rural | 2,129 | 1,313 | 331 | 54,771 | 2.52M | 55,362 | 36,294 | 0.635 | 161 |
| 31099 | Kearney | rural | 3,464 | 2,155 | 304 | 110,317 | 3.73M | 82,878 | 166,423 | 0.353 | 123 |
| 31101 | Keith | rural | 3,995 | 3,741 | 337 | 90,180 | 4.07M | 67,072 | 80,991 | 0.510 | 48 |
| 31103 | Keya Paha | rural | 441 | 223 | 179 | 18,353 | 0.56M | 53,197 | 49,680 | 0.677 | 52 |
| 31105 | Kimball | rural | 1,616 | 1,407 | 266 | 100,876 | 2.46M | 48,002 | 27,649 | 0.591 | 53* |
| 31107 | Knox | rural | 3,930 | 2,953 | 697 | 122,629 | 5.52M | 55,903 | 65,223 | 0.659 | 203 |
| 31109 | Lancaster | suburb | 173,171 | 182,205 | 1,318 | 126,328 | 118.41M | 39,370 | 23,565 | 0.535 | 182 |
| 31111 | Lincoln | rural | 16,387 | 16,039 | 910 | 141,241 | 15.15M | 57,981 | 140,773 | 0.586 | 53* |
| 31113 | Logan | rural | 434 | 229 | 92 | 16,973 | 0.35M | 100,163 | 38,579 | 0.725 | 53* |
| 31115 | Loup | rural | 320 | 149 | 87 | 7,914 | 0.41M | 64,163 | 76,873 | 0.777 | 53* |
| 31117 | McPherson | rural | 252 | 125 | 85 | 5,691 | 0.24M | 49,006 | 42,126 | 0.598 | 53* |
| 31119 | Madison | rural | 17,964 | 21,019 | 546 | 113,071 | 16.55M | 54,936 | 84,061 | 0.448 | 198 |
| 31121 | Merrick | suburb | 3,800 | 2,533 | 361 | 83,784 | 3.82M | 72,626 | 69,942 | 0.438 | 121 |
| 31123 | Morrill | rural | 2,063 | 1,368 | 378 | 69,976 | 3.05M | 85,001 | 109,208 | 0.671 | 53* |
| 31125 | Nance | rural | 1,607 | 1,017 | 252 | 63,100 | 2.14M | 104,746 | 17,703 | 0.523 | 165 |
| 31127 | Nemaha | rural | 3,187 | 3,153 | 312 | 76,576 | 3.52M | 61,397 | 71,475 | 0.486 | 193 |
| 31129 | Nuckolls | rural | 2,134 | 1,643 | 327 | 93,563 | 2.96M | 54,766 | 69,538 | 0.416 | 144 |
| 31131 | Otoe | rural | 7,967 | 6,374 | 619 | 117,432 | 7.80M | 50,267 | 36,979 | 0.453 | 182 |
| 31133 | Pawnee | rural | 1,051 | 712 | 252 | 59,948 | 2.00M | 79,691 | 35,975 | 0.588 | 142 |
| 31135 | Perkins | rural | 1,414 | 1,184 | 233 | 178,067 | 2.07M | 103,794 | 217,657 | 0.465 | 52 |
| 31137 | Phelps | rural | 4,446 | 4,900 | 449 | 113,672 | 5.39M | 70,336 | 104,537 | 0.418 | 115 |
| 31139 | Pierce | rural | 3,685 | 2,098 | 434 | 111,954 | 4.34M | 62,807 | 84,541 | 0.422 | 185 |
| 31141 | Platte | rural | 17,594 | 19,915 | 822 | 139,820 | 17.24M | 63,112 | 41,802 | 0.558 | 206 |
| 31143 | Polk | rural | 2,683 | 1,486 | 315 | 91,021 | 2.97M | 73,309 | 129,038 | 0.436 | 180 |
| 31145 | Red Willow | rural | 5,284 | 5,152 | 310 | 96,365 | 5.94M | 75,748 | 81,597 | 0.428 | 68 |
| 31147 | Richardson | rural | 3,650 | 2,652 | 475 | 95,927 | 5.03M | 50,052 | 52,320 | 0.570 | 200 |
| 31149 | Rock | rural | 650 | 510 | 163 | 21,465 | 0.86M | 81,131 | 76,270 | 0.550 | 46 |
| 31151 | Saline | rural | 6,999 | 6,634 | 587 | 113,432 | 6.93M | 52,060 | 55,703 | 0.543 | 144 |
| 31153 | Sarpy | suburb | 103,080 | 84,759 | 287 | 29,140 | 64.47M | 54,444 | 39,061 | 0.348 | 216 |
| 31155 | Saunders | suburb | 11,676 | 6,098 | 681 | 154,030 | 9.35M | 94,943 | 57,545 | 0.454 | 200 |
| 31157 | Scotts Bluff | rural | 16,964 | 16,573 | 729 | 80,872 | 19.06M | 55,278 | 39,329 | 0.557 | 53* |
| 31159 | Seward | suburb | 9,229 | 6,666 | 715 | 111,624 | 7.35M | 51,946 | 73,032 | 0.424 | 186 |
| 31161 | Sheridan | rural | 2,375 | 1,744 | 421 | 81,820 | 3.01M | 68,450 | 58,972 | 0.677 | 33 |
| 31163 | Sherman | rural | 1,419 | 797 | 260 | 54,220 | 1.83M | 56,780 | 69,722 | 0.516 | 127 |
| 31165 | Sioux | rural | 506 | 210 | 199 | 25,643 | 0.83M | 82,067 | 93,346 | 0.559 | 53* |
| 31167 | Stanton | rural | 3,079 | 1,175 | 311 | 79,947 | 4.25M | 70,569 | 55,800 | 0.472 | 237 |
| 31169 | Thayer | rural | 2,405 | 2,103 | 322 | 110,795 | 3.06M | 66,301 | 64,253 | 0.471 | 133 |
| 31171 | Thomas | rural | 352 | 287 | 53 | 1,177 | 0.34M | 92,454 | 44,341 | 0.734 | 53* |
| 31173 | Thurston | rural | 2,632 | 2,703 | 265 | 79,067 | 2.16M | 56,125 | 155,282 | 0.379 | 246 |
| 31175 | Valley | rural | 2,009 | 1,809 | 275 | 53,675 | 2.88M | 75,704 | 90,913 | 0.528 | 118 |
| 31177 | Washington | suburb | 10,853 | 8,516 | 583 | 72,689 | 10.47M | 42,018 | 43,880 | 0.519 | 228 |
| 31179 | Wayne | rural | 5,080 | 4,744 | 500 | 99,231 | 4.54M | 53,520 | 113,800 | 0.455 | 240 |
| 31181 | Webster | rural | 1,745 | 1,025 | 304 | 77,887 | 2.05M | 54,124 | 41,935 | 0.407 | 110 |
| 31183 | Wheeler | rural | 357 | 191 | 149 | 28,122 | 0.76M | 83,937 | 65,030 | 0.707 | 85 |
| 31185 | York | rural | 6,866 | 7,032 | 510 | 129,727 | 7.69M | 58,172 | 83,292 | 0.360 | 173 |
| EXT | External (out-of-state commuting) | external | 44,249 | 25,471 | 922 | 204,098 | 38.45M | 66,463 | n/a | 0.554 | n/a |

`*` filled, see above.
