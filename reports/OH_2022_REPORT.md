# Ohio 2022 county data: validation report

Built 2026-11-25 by `python -m urqse.data.build_state OH 2022`. 88 counties plus one external zone. Outputs: `county.parquet` (one row per zone, schema in `src/urqse/data/schema.py`) and `travel.npz` (`fips`, `t` minutes, `dist` km, rows in table order).

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
| cdl | USDA NASS Cropland Data Layer 2022, 30 m, clipped to state FIPS 39 | `OH/CDL_2022_39.tif` | 2026-11-24 | https://nassgeodata.gmu.edu/axis2/services/CDLService/GetCDLFile?year=2022&fips=39 |
| acs_b08007 | ACS 2018-2022 5-year, table-based summary file B08007 | `US/acs/acsdt5y2022-b08007.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08007.dat |
| acs_b08604 | ACS 2018-2022 5-year, table-based summary file B08604 | `US/acs/acsdt5y2022-b08604.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08604.dat |
| acs_b05005 | ACS 2018-2022 5-year, table-based summary file B05005 | `US/acs/acsdt5y2022-b05005.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b05005.dat |
| ghsl_R4_C12 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C12.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C12.zip |
| ghsl_R5_C11 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C11.zip` | 2026-11-23 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C11.zip |
| ghsl_R5_C12 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C12.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R5_C12.zip |
| nass | Quick Stats bulk economics file `qs.economics_20261121.txt.gz` (Census of Agriculture 2022; Cash Rents Survey 2022) | `qs.economics_20261121.txt.gz` (filtered copy `*_OH.tsv.gz`) | see file | https://www.nass.usda.gov/sites/default/files/datasets/qs.economics_20261121.txt.gz |
| osrm | OSRM public demo server, car profile (OSM data as served on the build date) | `osrm/*.json` (9 cached block requests; the server caps a table at 100 coordinates) | 2026-11-25 | https://router.project-osrm.org/table/v1/driving |

## County sums against published state totals

| Column | Sum of counties | Published state value | Difference |
|---|---|---|---|
| PEP population | 11,756,058 | 11,756,058 | 0.000% |
| ACS workers by residence | 5,579,288 | 5,579,288 | 0.000% |
| ACS workers by workplace | 5,594,384 | 5,594,384 | 0.000% |
| ACS workers working out of state | 144,144 | 144,144 | 0.000% |
| BEA non-farm employment (L80) | 7,222,825 | 7,222,825 | 0.000% |
| BEA farm employment (L70) | 82,352 | 82,352 | 0.000% |
| BEA farm proprietors (L50) | 68,865 | 68,865 | 0.000% |
| BEA farm earnings $ (CAINC45 L370) | 2,846,362,000 | 2,846,362,000 | 0.000% |
| BEA farm wages + supplements $ (CAINC45 L350 + L360) | 611,238,000 | 611,238,000 | 0.000% |
| CoA hired farm labour expense $ | 844,892,000 | 844,895,000 | -0.000% |
| BEA non-farm earnings $ (CAINC5N L82) | 466,311,129,000 | 466,311,129,000 | 0.000% |
| ACS foreign born entered 2010+ | 216,721 | 216,721 | 0.000% |
| CoA owned acres | 7,955,304 | 7,955,304 | 0.000% |
| CoA rented-from-others acres | 5,697,042 | 5,697,042 | 0.000% |
| CoA land in farms, ha | 5,524,908 | 5,524,908 | 0.000% |
| CoA total cropland, ha | 4,258,004 | 4,258,004 | 0.000% |

## Model columns

- **N, HU, HA (jobs = resident workers).** Each county's BEA farm and non-farm job counts are scaled to its ACS count of workers by place of work (scale factor min 0.613, median 0.778, max 0.884; BEA counts jobs, ACS counts people by main job). Sum N = 5,738,528 = sum HU + HA = 5,738,528. Farm jobs after scaling: 63,604 (BEA 82,352). `# VERIFY` the scaling: part-time farm proprietors with an off-farm main job are counted once, in proportion to the county mix.
- **External zone.** Residents = out-of-state workers commuting in (ACS workplace total minus in-state residents working in state) = 159,240. Jobs = in-state residents working out of state = 144,144, split by the state farm share (HA = 1,639). Location: the 39 out-of-state counties within 1 km of the state (18001, 18003, 18029, 18033, 18047, 18075, 18135, 18151, 18161, 18177, 21015, 21019, 21023, 21037, 21089, 21117, 21135, 21161, 21191, 26059, 26091, 26115, 42007, 42039, 42049, 42073, 42085, 54009, 54011, 54029, 54035, 54051, 54053, 54069, 54073, 54095, 54099, 54103, 54107); travel time from a county to the zone is the OSRM time to the nearest of them. Floor space, farmland, farm labour earnings and owner share are state averages scaled to its workers / farm jobs; gateway weight 0 (immigrants settle in-state). `# VERIFY` all of these are conventions, not data, and `log(0)` in `immigration.arrival_shares` needs handling in M3.
- **TF (farmland, ha).** CDL 2022 crop, hay, fallow and tree-crop classes (codes 1-61, 66-77, 204-254), pixel-centre zonal sums on the 30 m Albers grid. State: 3,901,746 ha vs Census of Agriculture cropland 4,258,004 ha and land in farms 5,524,908 ha; county ratio TF / CoA cropland 0.05 to 1.30. Grassland/pasture (codes 62, 176) is kept separately (`pasture_ha`, 1,401,967 ha). County area covered by CDL pixels: 10,685,803 ha vs land area 10,582,362 ha (the difference is water). `# VERIFY` whether pasture belongs in T^F for livestock counties.
- **L (floor space, m^2).** GHSL GHS-BUILT-V 2020 epoch building volume / 3 m storey height (`# VERIFY` storey height; 2020 is the nearest epoch to 2022). State volume 12.17 km^3.
- **wA_obs_usd (farm labour earnings per farm worker).** Farm compensation (CAINC45 L350 wages and salaries + L360 supplements) per farm wage-and-salary job (CAEMP25N L70 - L50), mean of 2018 to 2022, each year relative to the state's non-farm earnings per non-farm job (CAINC5N L82 / CAEMP25N L80) and put at the 2022 value (64,561 $). That per-job wage prices every BEA farm job, proprietors included, giving the county farm labour bill `farm_labour_bill_usd`; wA_obs_usd = bill / HA, so it is per farm worker (ACS head) and the model's wage bill w_A H_A equals the bill in dollars. State: 37,252 $ per BEA farm job, 48,233 $ per farm worker; county range 12,079 to 117,876 $ per worker. State compensation per farm wage job by year: 2018 34,342 $, 2019 36,427 $, 2020 37,145 $, 2021 37,488 $, 2022 45,321 $. Proprietors are priced at the hired wage per job (the market price of farm labour in the county) rather than at a non-farm opportunity wage, which would assume away the farm/non-farm gap xi_A is meant to measure. `# VERIFY` the proprietor imputation: a BEA proprietor job is any sole proprietor or partner, many part-time. Contract labour (CoA 107,201,000 $) is left out: its workers are not BEA farm jobs (they are in agricultural support services, non-farm). Census of Agriculture hired labour expense (844,895,000 $ in 2022, column `hired_labor_coa_usd`) is 1.38x BEA farm compensation (611,238,000 $) and pays a different universe (every hired head, including workers on the farm under 150 days), so it is a comparison column, not the bill. `# VERIFY` that gap. The previous measure, BEA farm earnings (L370, wages + proprietors' income) per BEA farm job, is kept as `wA_bea_earn_usd`: state 34,563 $, county -12,780 to 203,577 $; it includes owner-operators' returns to owned land and capital, which spec §12.1 pays separately. The loader divides wA_obs_usd by state non-farm earnings per non-farm worker (sum over counties of non-farm earnings / HU = 84,312 $), so both sectors are per head. `# VERIFY` vintage mismatch: CAINC45/CAEMP25N are the 2023-11-16 release, CAINC5N the 2026 file (CAINC5N's revised 2022 farm earnings are 2,935,555,000 $ vs CAINC45 2,846,362,000 $).
- **omega.** Census of Agriculture 2022 owned / (owned + rented from others) acres in farms. State 0.583, county range 0.362 to 0.902.
- **cash_rent_usd_acre.** NASS Cash Rents Survey 2022, non-irrigated cropland. State 170 $/acre.
- **land_value_usd_acre.** Census of Agriculture 2022 estimated market value of land and buildings per acre (NASS does not publish annual county land values). State 8,043 $/acre.
- **gateway.** ACS foreign born who entered 2010 or later per resident worker, relative to the state ratio (mean 1 over workers). `# VERIFY` against spec §12.2 once the arrival block is calibrated. 1 counties have no recent foreign born in the ACS sample (Vinton), so their gateway weight is 0 (log(0) in arrival_shares).
- **kind.** core = the metropolitan county with the most non-farm jobs (Franklin); suburb = other counties in a Metropolitan Statistical Area (OMB 2023) (40); rural = the rest (47). `# VERIFY` one core for a multi-metro state.
- **No farm sector** (spec §3.11): 0 counties have no BEA farm jobs.
- **Travel time t (min).** OSRM car durations between 2020 population-weighted county centres, as routed (not symmetrised). Off-diagonal median 166.5 min. Own-county time = 0.5214 x sqrt(land area) at the median effective speed of 61.0 straight-line km/h between counties (median 12.5 to 21.9 min). `# VERIFY` the own-county proxy. `dist` is great-circle km (road/straight median ratio 1.22).

## Suppressed cells and fills

| Variable | County | Rule |
|---|---|---|
| cash_rent_usd_acre | 39013 Belmont | not published; NASS 'other (combined) counties' value = 202 $/acre |
| cash_rent_usd_acre | 39037 Darke | not published; NASS 'other (combined) counties' value = 202 $/acre |
| cash_rent_usd_acre | 39087 Lawrence | not published; NASS 'other (combined) counties' value = 202 $/acre |
| cash_rent_usd_acre | 39107 Mercer | not published; NASS 'other (combined) counties' value = 202 $/acre |
| cash_rent_usd_acre | 39147 Seneca | not published; NASS 'other (combined) counties' value = 202 $/acre |

No BEA (D) cells for this state and year: CAEMP25N L50/70/80, CAINC45 L350/360/370 and CAINC5N L82 are published for every county (2018 to 2022 for the farm-wage lines).

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
| 39001 | Adams | rural | 10,284 | 6,537 | 885 | 24,811 | 9.44M | 30,807 | 7,032 | 0.818 | 130 |
| 39003 | Allen | suburb | 45,300 | 48,651 | 727 | 68,230 | 50.81M | 35,459 | 40,791 | 0.473 | 213 |
| 39005 | Ashland | rural | 24,322 | 20,211 | 835 | 42,019 | 18.28M | 32,888 | 28,309 | 0.602 | 109 |
| 39007 | Ashtabula | suburb | 40,922 | 31,032 | 869 | 30,727 | 30.04M | 36,518 | 3,574 | 0.733 | 52 |
| 39009 | Athens | rural | 27,395 | 25,466 | 570 | 3,238 | 10.94M | 52,133 | -4,777 | 0.819 | 46 |
| 39011 | Auglaize | rural | 23,580 | 21,832 | 875 | 77,797 | 20.87M | 36,641 | 72,048 | 0.552 | 213 |
| 39013 | Belmont | suburb | 28,090 | 22,534 | 604 | 1,653 | 16.11M | 12,079 | -3,351 | 0.794 | 202* |
| 39015 | Brown | suburb | 18,800 | 8,936 | 937 | 50,349 | 12.89M | 25,908 | 11,025 | 0.706 | 146 |
| 39017 | Butler | suburb | 182,553 | 165,821 | 717 | 27,450 | 146.35M | 39,885 | 5,560 | 0.707 | 155 |
| 39019 | Carroll | suburb | 11,572 | 6,911 | 558 | 10,240 | 8.32M | 58,894 | 2,979 | 0.689 | 58 |
| 39021 | Champaign | rural | 18,144 | 11,578 | 703 | 75,890 | 11.84M | 89,243 | 53,707 | 0.484 | 203 |
| 39023 | Clark | suburb | 59,345 | 49,395 | 732 | 57,620 | 37.35M | 59,602 | 41,346 | 0.501 | 178 |
| 39025 | Clermont | suburb | 103,116 | 67,883 | 623 | 21,146 | 50.35M | 55,909 | -3,316 | 0.549 | 149 |
| 39027 | Clinton | rural | 19,725 | 21,281 | 687 | 72,390 | 14.75M | 43,018 | 52,032 | 0.525 | 183 |
| 39029 | Columbiana | rural | 45,689 | 32,886 | 919 | 25,507 | 27.92M | 33,614 | 25,449 | 0.648 | 89 |
| 39031 | Coshocton | rural | 15,264 | 10,916 | 874 | 23,038 | 14.02M | 50,594 | 25,112 | 0.800 | 96 |
| 39033 | Crawford | rural | 18,790 | 13,126 | 571 | 77,148 | 15.94M | 47,494 | 52,300 | 0.454 | 191 |
| 39035 | Cuyahoga | suburb | 592,913 | 705,195 | 126 | 237 | 464.70M | 56,016 | 16,925 | 0.814 | 66 |
| 39037 | Darke | rural | 24,358 | 18,717 | 1,400 | 122,373 | 24.55M | 78,603 | 95,901 | 0.557 | 202* |
| 39039 | Defiance | rural | 18,548 | 15,728 | 805 | 73,676 | 15.95M | 41,740 | 28,760 | 0.490 | 165 |
| 39041 | Delaware | suburb | 112,256 | 103,010 | 597 | 48,490 | 56.64M | 73,180 | 25,010 | 0.433 | 181 |
| 39043 | Erie | suburb | 35,164 | 34,789 | 423 | 31,763 | 28.58M | 62,872 | 35,206 | 0.535 | 169 |
| 39045 | Fairfield | suburb | 77,254 | 47,758 | 822 | 56,514 | 35.04M | 44,958 | 18,263 | 0.529 | 162 |
| 39047 | Fayette | rural | 12,678 | 11,546 | 484 | 83,674 | 10.90M | 51,804 | 100,220 | 0.419 | 227 |
| 39049 | Franklin | core | 682,147 | 777,974 | 381 | 21,012 | 415.84M | 58,231 | 22,852 | 0.489 | 187 |
| 39051 | Fulton | suburb | 20,337 | 18,396 | 679 | 80,145 | 19.42M | 60,549 | 32,494 | 0.467 | 179 |
| 39053 | Gallia | rural | 11,616 | 10,854 | 686 | 3,357 | 8.73M | 43,051 | -7,731 | 0.812 | 80 |
| 39055 | Geauga | suburb | 47,198 | 42,414 | 777 | 7,793 | 19.71M | 40,994 | 4,084 | 0.753 | 40 |
| 39057 | Greene | suburb | 80,299 | 87,761 | 726 | 53,346 | 53.59M | 41,372 | 31,718 | 0.486 | 198 |
| 39059 | Guernsey | rural | 16,560 | 16,279 | 1,014 | 5,871 | 12.36M | 29,893 | -686 | 0.810 | 36 |
| 39061 | Hamilton | suburb | 408,079 | 511,366 | 297 | 3,110 | 341.26M | 61,454 | 24,515 | 0.737 | 142 |
| 39063 | Hancock | rural | 36,806 | 44,975 | 679 | 105,238 | 39.34M | 43,268 | 57,601 | 0.468 | 186 |
| 39065 | Hardin | rural | 13,593 | 9,006 | 765 | 95,122 | 12.06M | 66,876 | 74,871 | 0.417 | 204 |
| 39067 | Harrison | rural | 5,605 | 4,299 | 364 | 4,207 | 4.52M | 43,128 | -515 | 0.742 | 46 |
| 39069 | Henry | rural | 13,385 | 11,117 | 685 | 89,603 | 11.74M | 61,136 | 54,022 | 0.433 | 184 |
| 39071 | Highland | rural | 18,581 | 12,109 | 1,048 | 65,240 | 13.63M | 45,824 | 28,815 | 0.629 | 163 |
| 39073 | Hocking | suburb | 12,424 | 8,628 | 296 | 3,531 | 6.26M | 34,812 | -9,040 | 0.902 | 98 |
| 39075 | Holmes | rural | 20,276 | 22,392 | 1,523 | 23,517 | 14.05M | 38,391 | 41,736 | 0.768 | 100 |
| 39077 | Huron | rural | 26,975 | 23,284 | 980 | 81,660 | 20.62M | 60,259 | 55,083 | 0.481 | 163 |
| 39079 | Jackson | rural | 13,433 | 11,370 | 431 | 6,629 | 9.39M | 47,168 | 311 | 0.806 | 58 |
| 39081 | Jefferson | suburb | 27,544 | 23,126 | 405 | 2,658 | 21.33M | 32,259 | -12,780 | 0.828 | 31 |
| 39083 | Knox | rural | 28,192 | 22,505 | 1,043 | 51,619 | 18.41M | 36,054 | 32,895 | 0.647 | 129 |
| 39085 | Lake | suburb | 118,513 | 103,993 | 582 | 1,084 | 74.06M | 63,553 | 46,267 | 0.674 | 114 |
| 39087 | Lawrence | suburb | 23,216 | 13,851 | 430 | 1,178 | 16.70M | 13,499 | -9,814 | 0.878 | 202* |
| 39089 | Licking | suburb | 85,420 | 77,394 | 1,362 | 54,921 | 47.50M | 45,368 | 21,993 | 0.625 | 132 |
| 39091 | Logan | rural | 20,974 | 20,792 | 766 | 72,744 | 20.03M | 46,571 | 43,553 | 0.515 | 188 |
| 39093 | Lorain | suburb | 144,410 | 111,837 | 1,049 | 37,804 | 106.64M | 70,651 | 26,175 | 0.568 | 127 |
| 39095 | Lucas | suburb | 195,444 | 208,188 | 368 | 24,557 | 160.65M | 57,875 | 22,524 | 0.395 | 172 |
| 39097 | Madison | suburb | 19,749 | 21,283 | 596 | 95,912 | 12.84M | 52,773 | 97,937 | 0.475 | 209 |
| 39099 | Mahoning | suburb | 100,983 | 102,524 | 517 | 16,562 | 93.78M | 54,172 | 25,353 | 0.652 | 86 |
| 39101 | Marion | rural | 26,661 | 26,296 | 517 | 74,223 | 24.15M | 55,205 | 79,266 | 0.453 | 171 |
| 39103 | Medina | suburb | 94,868 | 72,245 | 844 | 23,144 | 50.20M | 34,545 | 1,650 | 0.647 | 80 |
| 39105 | Meigs | rural | 8,159 | 4,014 | 426 | 3,083 | 5.47M | 56,234 | 4,821 | 0.891 | 45 |
| 39107 | Mercer | rural | 21,473 | 19,922 | 1,064 | 95,376 | 22.50M | 43,105 | 203,577 | 0.632 | 202* |
| 39109 | Miami | suburb | 53,983 | 44,925 | 991 | 66,900 | 37.42M | 17,741 | 25,437 | 0.508 | 190 |
| 39111 | Monroe | rural | 5,318 | 3,520 | 547 | 666 | 6.35M | 37,993 | -5,944 | 0.855 | 26 |
| 39113 | Montgomery | suburb | 248,049 | 265,984 | 698 | 33,973 | 216.20M | 70,655 | 21,918 | 0.450 | 175 |
| 39115 | Morgan | rural | 5,347 | 3,310 | 367 | 4,561 | 4.16M | 45,790 | 2,495 | 0.762 | 57 |
| 39117 | Morrow | suburb | 17,173 | 8,165 | 733 | 54,492 | 10.21M | 50,045 | 19,979 | 0.504 | 153 |
| 39119 | Muskingum | rural | 38,989 | 37,391 | 998 | 18,586 | 25.53M | 38,378 | 12,742 | 0.749 | 58 |
| 39121 | Noble | rural | 4,135 | 2,705 | 346 | 1,264 | 3.90M | 25,138 | -8,051 | 0.718 | 46 |
| 39123 | Ottawa | suburb | 18,665 | 14,290 | 466 | 38,514 | 17.42M | 50,787 | 19,015 | 0.536 | 160 |
| 39125 | Paulding | rural | 8,367 | 4,601 | 638 | 87,215 | 8.19M | 112,337 | 71,545 | 0.401 | 172 |
| 39127 | Perry | suburb | 14,819 | 7,044 | 482 | 16,502 | 7.72M | 31,547 | 9,977 | 0.776 | 96 |
| 39129 | Pickaway | suburb | 25,292 | 18,326 | 754 | 88,007 | 16.67M | 57,667 | 68,121 | 0.362 | 195 |
| 39131 | Pike | rural | 10,067 | 10,018 | 363 | 13,116 | 9.74M | 54,426 | 27,685 | 0.768 | 163 |
| 39133 | Portage | suburb | 80,900 | 66,065 | 805 | 17,061 | 37.42M | 36,240 | -8,243 | 0.648 | 66 |
| 39135 | Preble | rural | 19,524 | 12,462 | 871 | 70,783 | 13.18M | 74,315 | 48,301 | 0.521 | 199 |
| 39137 | Putnam | rural | 17,056 | 12,152 | 948 | 104,653 | 15.85M | 74,530 | 50,905 | 0.533 | 172 |
| 39139 | Richland | suburb | 53,293 | 53,425 | 836 | 46,926 | 38.96M | 37,109 | 40,557 | 0.693 | 141 |
| 39141 | Ross | rural | 30,977 | 29,939 | 832 | 50,612 | 22.28M | 29,539 | 25,332 | 0.671 | 164 |
| 39143 | Sandusky | rural | 27,071 | 26,333 | 683 | 74,975 | 23.16M | 48,027 | 29,247 | 0.570 | 170 |
| 39145 | Scioto | rural | 26,345 | 24,147 | 530 | 11,597 | 21.66M | 26,009 | -2,266 | 0.724 | 100 |
| 39147 | Seneca | rural | 26,313 | 20,301 | 856 | 108,007 | 21.73M | 45,817 | 32,094 | 0.583 | 202* |
| 39149 | Shelby | rural | 23,620 | 27,356 | 839 | 76,762 | 22.72M | 50,904 | 57,188 | 0.552 | 236 |
| 39151 | Stark | suburb | 177,007 | 165,876 | 1,056 | 30,291 | 135.89M | 62,964 | 16,624 | 0.628 | 101 |
| 39153 | Summit | suburb | 264,826 | 281,607 | 255 | 2,132 | 179.47M | 41,641 | 7,837 | 0.802 | 54 |
| 39155 | Trumbull | suburb | 84,556 | 70,973 | 746 | 23,596 | 76.30M | 45,603 | 8,279 | 0.732 | 57 |
| 39157 | Tuscarawas | rural | 42,276 | 38,181 | 828 | 19,975 | 31.12M | 45,911 | 44,905 | 0.649 | 76 |
| 39159 | Union | suburb | 31,865 | 36,434 | 870 | 74,365 | 18.69M | 49,822 | 69,795 | 0.561 | 175 |
| 39161 | Van Wert | rural | 13,971 | 11,987 | 559 | 91,053 | 13.58M | 48,962 | 113,450 | 0.481 | 198 |
| 39163 | Vinton | rural | 5,010 | 2,784 | 176 | 2,147 | 2.72M | 62,504 | -991 | 0.897 | 27 |
| 39165 | Warren | suburb | 120,107 | 109,894 | 828 | 26,293 | 71.07M | 40,289 | 12,792 | 0.494 | 131 |
| 39167 | Washington | rural | 26,577 | 25,873 | 859 | 7,435 | 21.71M | 38,973 | 5,898 | 0.833 | 64 |
| 39169 | Wayne | rural | 53,961 | 53,020 | 1,864 | 60,979 | 36.68M | 44,191 | 49,992 | 0.639 | 149 |
| 39171 | Williams | rural | 17,356 | 17,462 | 824 | 71,496 | 16.13M | 50,118 | 36,887 | 0.466 | 171 |
| 39173 | Wood | suburb | 66,642 | 72,511 | 1,032 | 118,670 | 54.69M | 43,727 | 38,965 | 0.483 | 176 |
| 39175 | Wyandot | rural | 10,849 | 9,785 | 482 | 77,920 | 10.03M | 117,876 | 96,895 | 0.471 | 192 |
| EXT | External (out-of-state commuting) | external | 159,240 | 142,505 | 1,639 | 100,532 | 115.82M | 48,233 | n/a | 0.583 | n/a |

`*` filled, see above.
