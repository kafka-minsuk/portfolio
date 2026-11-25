# Maryland 2022 county data: validation report

Built 2026-11-24 by `python -m urqse.data.build_state MD 2022`. 24 counties plus one external zone. Outputs: `county.parquet` (one row per zone, schema in `src/urqse/data/schema.py`) and `travel.npz` (`fips`, `t` minutes, `dist` km, rows in table order).

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
| cdl | USDA NASS Cropland Data Layer 2022, 30 m, clipped to state FIPS 24 | `MD/CDL_2022_24.tif` | 2026-11-24 | https://nassgeodata.gmu.edu/axis2/services/CDLService/GetCDLFile?year=2022&fips=24 |
| acs_b08007 | ACS 2018-2022 5-year, table-based summary file B08007 | `US/acs/acsdt5y2022-b08007.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08007.dat |
| acs_b08604 | ACS 2018-2022 5-year, table-based summary file B08604 | `US/acs/acsdt5y2022-b08604.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08604.dat |
| acs_b05005 | ACS 2018-2022 5-year, table-based summary file B05005 | `US/acs/acsdt5y2022-b05005.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b05005.dat |
| ghsl_R5_C12 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C12.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C12.zip |
| nass | Quick Stats bulk economics file `qs.economics_20261121.txt.gz` (Census of Agriculture 2022; Cash Rents Survey 2022) | `qs.economics_20261121.txt.gz` (filtered copy `*_MD.tsv.gz`) | see file | https://www.nass.usda.gov/sites/default/files/datasets/qs.economics_20261121.txt.gz |
| osrm | OSRM public demo server, car profile (OSM data as served on the build date) | `osrm/*.json` (1 cached block requests; the server caps a table at 100 coordinates) | 2026-11-24 | https://router.project-osrm.org/table/v1/driving |

## County sums against published state totals

| Column | Sum of counties | Published state value | Difference |
|---|---|---|---|
| PEP population | 6,164,660 | 6,164,660 | 0.000% |
| ACS workers by residence | 3,101,081 | 3,101,081 | 0.000% |
| ACS workers by workplace | 2,867,002 | 2,867,002 | 0.000% |
| ACS workers working out of state | 440,545 | 440,545 | 0.000% |
| BEA non-farm employment (L80) | 3,869,819 | 3,869,819 | 0.000% |
| BEA farm employment (L70) | 17,072 | 17,072 | 0.000% |
| BEA farm proprietors (L50) | 10,919 | 10,919 | 0.000% |
| BEA farm earnings $ (CAINC45 L370) | 865,194,000 | 865,194,000 | 0.000% |
| BEA farm wages + supplements $ (CAINC45 L350 + L360) | 242,633,000 | 242,633,000 | 0.000% |
| CoA hired farm labour expense $ | 290,934,000 | 290,934,000 | 0.000% |
| BEA non-farm earnings $ (CAINC5N L82) | 289,159,453,000 | 289,159,453,000 | 0.000% |
| ACS foreign born entered 2010+ | 287,598 | 287,598 | 0.000% |
| CoA owned acres | 1,167,129 | 1,167,129 | 0.000% |
| CoA rented-from-others acres | 810,907 | 810,907 | 0.000% |
| CoA land in farms, ha | 800,483 | 800,483 | 0.000% |
| CoA total cropland, ha | 565,545 | 565,545 | 0.000% |

## Model columns

- **N, HU, HA (jobs = resident workers).** Each county's BEA farm and non-farm job counts are scaled to its ACS count of workers by place of work (scale factor min 0.627, median 0.755, max 0.836; BEA counts jobs, ACS counts people by main job). Sum N = 3,307,547 = sum HU + HA = 3,307,547. Farm jobs after scaling: 12,767 (BEA 17,072). `# VERIFY` the scaling: part-time farm proprietors with an off-farm main job are counted once, in proportion to the county mix.
- **External zone.** Residents = out-of-state workers commuting in (ACS workplace total minus in-state residents working in state) = 206,466. Jobs = in-state residents working out of state = 440,545, split by the state farm share (HA = 1,962). Location: the 26 out-of-state counties within 1 km of the state (10001, 10003, 10005, 11001, 42001, 42009, 42029, 42051, 42055, 42057, 42071, 42111, 42133, 51001, 51013, 51059, 51107, 51510, 54003, 54023, 54027, 54037, 54057, 54065, 54077, 54093); travel time from a county to the zone is the OSRM time to the nearest of them. Floor space, farmland, farm labour earnings and owner share are state averages scaled to its workers / farm jobs; gateway weight 0 (immigrants settle in-state). `# VERIFY` all of these are conventions, not data, and `log(0)` in `immigration.arrival_shares` needs handling in M3.
- **TF (farmland, ha).** CDL 2022 crop, hay, fallow and tree-crop classes (codes 1-61, 66-77, 204-254), pixel-centre zonal sums on the 30 m Albers grid. State: 534,042 ha vs Census of Agriculture cropland 565,545 ha and land in farms 800,483 ha; county ratio TF / CoA cropland 0.26 to 1.38. Grassland/pasture (codes 62, 176) is kept separately (`pasture_ha`, 220,977 ha). County area covered by CDL pixels: 2,664,552 ha vs land area 2,515,177 ha (the difference is water). `# VERIFY` whether pasture belongs in T^F for livestock counties.
- **L (floor space, m^2).** GHSL GHS-BUILT-V 2020 epoch building volume / 3 m storey height (`# VERIFY` storey height; 2020 is the nearest epoch to 2022). State volume 4.84 km^3.
- **wA_obs_usd (farm labour earnings per farm worker).** Farm compensation (CAINC45 L350 wages and salaries + L360 supplements) per farm wage-and-salary job (CAEMP25N L70 - L50), mean of 2018 to 2022, each year relative to the state's non-farm earnings per non-farm job (CAINC5N L82 / CAEMP25N L80) and put at the 2022 value (74,722 $). That per-job wage prices every BEA farm job, proprietors included, giving the county farm labour bill `farm_labour_bill_usd`; wA_obs_usd = bill / HA, so it is per farm worker (ACS head) and the model's wage bill w_A H_A equals the bill in dollars. State: 29,980 $ per BEA farm job, 40,089 $ per farm worker; county range 17,043 to 57,549 $ per worker. State compensation per farm wage job by year: 2018 27,594 $, 2019 24,873 $, 2020 31,089 $, 2021 24,371 $, 2022 39,433 $. Proprietors are priced at the hired wage per job (the market price of farm labour in the county) rather than at a non-farm opportunity wage, which would assume away the farm/non-farm gap xi_A is meant to measure. `# VERIFY` the proprietor imputation: a BEA proprietor job is any sole proprietor or partner, many part-time. Contract labour (CoA 25,604,000 $) is left out: its workers are not BEA farm jobs (they are in agricultural support services, non-farm). Census of Agriculture hired labour expense (290,934,000 $ in 2022, column `hired_labor_coa_usd`) is 1.20x BEA farm compensation (242,633,000 $) and pays a different universe (every hired head, including workers on the farm under 150 days), so it is a comparison column, not the bill. `# VERIFY` that gap. The previous measure, BEA farm earnings (L370, wages + proprietors' income) per BEA farm job, is kept as `wA_bea_earn_usd`: state 50,679 $, county -15,371 to 281,148 $; it includes owner-operators' returns to owned land and capital, which spec §12.1 pays separately. The loader divides wA_obs_usd by state non-farm earnings per non-farm worker (sum over counties of non-farm earnings / HU = 101,309 $), so both sectors are per head. `# VERIFY` vintage mismatch: CAINC45/CAEMP25N are the 2023-11-16 release, CAINC5N the 2026 file (CAINC5N's revised 2022 farm earnings are 1,082,590,000 $ vs CAINC45 865,194,000 $).
- **omega.** Census of Agriculture 2022 owned / (owned + rented from others) acres in farms. State 0.590, county range 0.436 to 0.863.
- **cash_rent_usd_acre.** NASS Cash Rents Survey 2022, non-irrigated cropland. State 111 $/acre.
- **land_value_usd_acre.** Census of Agriculture 2022 estimated market value of land and buildings per acre (NASS does not publish annual county land values). State 9,262 $/acre.
- **gateway.** ACS foreign born who entered 2010 or later per resident worker, relative to the state ratio (mean 1 over workers). `# VERIFY` against spec §12.2 once the arrival block is calibrated. 0 counties have no recent foreign born in the ACS sample (), so their gateway weight is 0 (log(0) in arrival_shares).
- **kind.** core = the metropolitan county with the most non-farm jobs (Montgomery); suburb = other counties in a Metropolitan Statistical Area (OMB 2023) (16); rural = the rest (7). `# VERIFY` one core for a multi-metro state.
- **No farm sector** (spec §3.11): 1 counties have no BEA farm jobs (Baltimore); their farm wage is 0 and the model gives them no farm job option.
- **Travel time t (min).** OSRM car durations between 2020 population-weighted county centres, as routed (not symmetrised). Off-diagonal median 124.0 min. Own-county time = 0.5214 x sqrt(land area) at the median effective speed of 50.8 straight-line km/h between counties (median 8.9 to 25.5 min). `# VERIFY` the own-county proxy. `dist` is great-circle km (road/straight median ratio 1.30).

## Suppressed cells and fills

| Variable | County | Rule |
|---|---|---|
| HA_bea | 24510 Baltimore | 0 farm jobs: no farm sector in the model (spec §3.11) |
| omega | 24510 Baltimore | state owner share |
| cash_rent_usd_acre | 24001 Allegany | not published; NASS 'other (combined) counties' value = 91.5 $/acre |
| cash_rent_usd_acre | 24013 Carroll | not published; NASS 'other (combined) counties' value = 91.5 $/acre |
| cash_rent_usd_acre | 24027 Howard | not published; NASS 'other (combined) counties' value = 91.5 $/acre |
| cash_rent_usd_acre | 24033 Prince George's | not published; NASS 'other (combined) counties' value = 91.5 $/acre |
| cash_rent_usd_acre | 24510 Baltimore | not published; NASS 'other (combined) counties' value = 91.5 $/acre |

## Coverage gaps and caveats

- ACS is the 5-year period estimate ending in the base year (no 1-year data for small counties); BEA and PEP are single-year. The external zone inherits ACS sampling error in the commuter totals.
- The Census API now requires a key, so ACS comes from the table-based summary files instead (same estimates).
- LODES (for the M3 PPML of kappa*lambda) and IRS SOI migration flows are not part of this build.
- Census of Agriculture is quinquennial (2022 matches the base year); the cash-rent survey is annual.
- x_km / y_km are NAD83 / UTM (EPSG:26918) at the state's middle longitude, for drawing only.
- No satellite population layer (GHS-POP) is used; census counts drive calibration (spec §8).

## County table

| FIPS | Name | Kind | N | HU | HA | TF ha | L m^2 | wA $/worker | BEA farm earnings $/job | omega | rent $/ac |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 24001 | Allegany | rural | 26,115 | 29,654 | 240 | 1,310 | 19.49M | 19,449 | 1,157 | 0.863 | 92* |
| 24003 | Anne Arundel | suburb | 306,689 | 307,750 | 345 | 6,044 | 155.41M | 51,157 | 21,515 | 0.657 | 70 |
| 24005 | Baltimore | suburb | 422,546 | 368,142 | 727 | 18,820 | 248.15M | 42,940 | 19,848 | 0.563 | 98 |
| 24009 | Calvert | suburb | 48,004 | 28,710 | 212 | 4,678 | 15.55M | 22,588 | -15,371 | 0.587 | 41 |
| 24011 | Caroline | rural | 15,769 | 9,414 | 560 | 44,851 | 10.33M | 41,529 | 143,226 | 0.531 | 126 |
| 24013 | Carroll | suburb | 90,034 | 62,411 | 1,089 | 35,476 | 44.75M | 45,593 | 16,327 | 0.604 | 92* |
| 24015 | Cecil | suburb | 49,384 | 37,738 | 952 | 23,910 | 23.07M | 35,125 | 25,858 | 0.564 | 157 |
| 24017 | Charles | suburb | 84,812 | 49,079 | 285 | 9,966 | 37.83M | 47,131 | -10,182 | 0.623 | 50 |
| 24019 | Dorchester | rural | 14,681 | 12,117 | 389 | 40,275 | 11.19M | 50,556 | 102,166 | 0.640 | 79 |
| 24021 | Frederick | suburb | 143,078 | 121,698 | 1,344 | 49,421 | 65.79M | 37,265 | 24,543 | 0.543 | 84 |
| 24023 | Garrett | rural | 13,283 | 13,351 | 583 | 8,028 | 8.44M | 17,043 | 27,273 | 0.764 | 37 |
| 24025 | Harford | suburb | 134,818 | 106,836 | 642 | 19,329 | 65.86M | 41,904 | 15,372 | 0.551 | 166 |
| 24027 | Howard | suburb | 173,546 | 176,256 | 359 | 6,203 | 89.45M | 51,693 | 14,920 | 0.695 | 92* |
| 24029 | Kent | rural | 9,119 | 9,325 | 478 | 42,944 | 5.31M | 43,221 | 41,267 | 0.594 | 185 |
| 24031 | Montgomery | core | 551,214 | 532,868 | 600 | 14,095 | 239.83M | 45,667 | 28,095 | 0.436 | 84 |
| 24033 | Prince George's | suburb | 492,653 | 372,092 | 299 | 5,090 | 250.69M | 34,083 | 4,196 | 0.443 | 92* |
| 24035 | Queen Anne's | suburb | 25,693 | 18,141 | 518 | 51,953 | 11.29M | 57,549 | 81,763 | 0.545 | 168 |
| 24037 | St. Mary's | suburb | 58,080 | 54,529 | 540 | 15,495 | 21.82M | 38,526 | -1,540 | 0.674 | 60 |
| 24039 | Somerset | suburb | 9,396 | 7,748 | 300 | 15,826 | 6.98M | 47,014 | 281,148 | 0.645 | 102 |
| 24041 | Talbot | rural | 16,883 | 20,307 | 314 | 34,168 | 12.48M | 42,092 | 54,696 | 0.510 | 113 |
| 24043 | Washington | suburb | 70,057 | 69,749 | 977 | 24,907 | 44.86M | 27,793 | 41,944 | 0.592 | 86 |
| 24045 | Wicomico | suburb | 50,503 | 47,799 | 647 | 28,109 | 30.78M | 48,075 | 163,621 | 0.567 | 90 |
| 24047 | Worcester | rural | 24,119 | 26,608 | 368 | 33,131 | 25.65M | 38,520 | 185,868 | 0.614 | 112 |
| 24510 | Baltimore | suburb | 270,605 | 371,912 | 0 | 15 | 168.39M | 0 | n/a | 0.590 | 92* |
| EXT | External (out-of-state commuting) | external | 206,466 | 438,583 | 1,962 | 82,061 | 107.42M | 40,089 | n/a | 0.590 | n/a |

`*` filled, see above.
