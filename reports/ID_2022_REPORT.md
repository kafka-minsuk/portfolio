# Idaho 2022 county data: validation report

Built 2026-11-24 by `python -m urqse.data.build_state ID 2022`. 44 counties plus one external zone. Outputs: `county.parquet` (one row per zone, schema in `src/urqse/data/schema.py`) and `travel.npz` (`fips`, `t` minutes, `dist` km, rows in table order).

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
| cdl | USDA NASS Cropland Data Layer 2022, 30 m, clipped to state FIPS 16 | `ID/CDL_2022_16.tif` | 2026-11-24 | https://nassgeodata.gmu.edu/axis2/services/CDLService/GetCDLFile?year=2022&fips=16 |
| acs_b08007 | ACS 2018-2022 5-year, table-based summary file B08007 | `US/acs/acsdt5y2022-b08007.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08007.dat |
| acs_b08604 | ACS 2018-2022 5-year, table-based summary file B08604 | `US/acs/acsdt5y2022-b08604.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08604.dat |
| acs_b05005 | ACS 2018-2022 5-year, table-based summary file B05005 | `US/acs/acsdt5y2022-b05005.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b05005.dat |
| ghsl_R4_C9 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C9.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C9.zip |
| ghsl_R4_C10 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C10.zip` | 2026-11-23 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C10.zip |
| nass | Quick Stats bulk economics file `qs.economics_20261121.txt.gz` (Census of Agriculture 2022; Cash Rents Survey 2022) | `qs.economics_20261121.txt.gz` (filtered copy `*_ID.tsv.gz`) | see file | https://www.nass.usda.gov/sites/default/files/datasets/qs.economics_20261121.txt.gz |
| osrm | OSRM public demo server, car profile (OSM data as served on the build date) | `osrm/*.json` (4 cached block requests; the server caps a table at 100 coordinates) | 2026-11-24 | https://router.project-osrm.org/table/v1/driving |

## County sums against published state totals

| Column | Sum of counties | Published state value | Difference |
|---|---|---|---|
| PEP population | 1,939,033 | 1,939,033 | 0.000% |
| ACS workers by residence | 862,707 | 862,707 | 0.000% |
| ACS workers by workplace | 842,254 | 842,254 | 0.000% |
| ACS workers working out of state | 41,603 | 41,603 | 0.000% |
| BEA non-farm employment (L80) | 1,150,246 | 1,150,246 | 0.000% |
| BEA farm employment (L70) | 40,378 | 40,378 | 0.000% |
| BEA farm proprietors (L50) | 22,127 | 22,127 | 0.000% |
| BEA farm earnings $ (CAINC45 L370) | 2,739,820,000 | 2,739,820,000 | 0.000% |
| BEA farm wages + supplements $ (CAINC45 L350 + L360) | 808,859,000 | 808,859,000 | 0.000% |
| CoA hired farm labour expense $ | 1,043,118,000 | 1,043,118,000 | 0.000% |
| BEA non-farm earnings $ (CAINC5N L82) | 67,459,460,000 | 67,459,460,000 | 0.000% |
| ACS foreign born entered 2010+ | 27,117 | 27,117 | 0.000% |
| CoA owned acres | 7,707,579 | 7,737,908 | -0.392% |
| CoA rented-from-others acres | 3,793,458 | 3,810,055 | -0.436% |
| CoA land in farms, ha | 4,673,295 | 4,673,295 | 0.000% |
| CoA total cropland, ha | 2,275,756 | 2,275,756 | 0.000% |

## Model columns

- **N, HU, HA (jobs = resident workers).** Each county's BEA farm and non-farm job counts are scaled to its ACS count of workers by place of work (scale factor min 0.311, median 0.697, max 0.903; BEA counts jobs, ACS counts people by main job). Sum N = 883,857 = sum HU + HA = 883,857. Farm jobs after scaling: 28,123 (BEA 40,378). `# VERIFY` the scaling: part-time farm proprietors with an off-farm main job are counted once, in proportion to the county mix.
- **External zone.** Residents = out-of-state workers commuting in (ACS workplace total minus in-state residents working in state) = 21,150. Jobs = in-state residents working out of state = 41,603, split by the state farm share (HA = 1,389). Location: the 22 out-of-state counties within 1 km of the state (30001, 30031, 30053, 30057, 30061, 30063, 30081, 30089, 32007, 32013, 41001, 41045, 41063, 49003, 49005, 49033, 53003, 53051, 53063, 53075, 56023, 56039); travel time from a county to the zone is the OSRM time to the nearest of them. Floor space, farmland, farm labour earnings and owner share are state averages scaled to its workers / farm jobs; gateway weight 0 (immigrants settle in-state). `# VERIFY` all of these are conventions, not data, and `log(0)` in `immigration.arrival_shares` needs handling in M3.
- **TF (farmland, ha).** CDL 2022 crop, hay, fallow and tree-crop classes (codes 1-61, 66-77, 204-254), pixel-centre zonal sums on the 30 m Albers grid. State: 2,264,682 ha vs Census of Agriculture cropland 2,275,756 ha and land in farms 4,673,295 ha; county ratio TF / CoA cropland 0.32 to 2.22. Grassland/pasture (codes 62, 176) is kept separately (`pasture_ha`, 2,871,324 ha). County area covered by CDL pixels: 21,644,166 ha vs land area 21,404,991 ha (the difference is water). `# VERIFY` whether pasture belongs in T^F for livestock counties.
- **L (floor space, m^2).** GHSL GHS-BUILT-V 2020 epoch building volume / 3 m storey height (`# VERIFY` storey height; 2020 is the nearest epoch to 2022). State volume 2.01 km^3.
- **wA_obs_usd (farm labour earnings per farm worker).** Farm compensation (CAINC45 L350 wages and salaries + L360 supplements) per farm wage-and-salary job (CAEMP25N L70 - L50), mean of 2018 to 2022, each year relative to the state's non-farm earnings per non-farm job (CAINC5N L82 / CAEMP25N L80) and put at the 2022 value (58,648 $). That per-job wage prices every BEA farm job, proprietors included, giving the county farm labour bill `farm_labour_bill_usd`; wA_obs_usd = bill / HA, so it is per farm worker (ACS head) and the model's wage bill w_A H_A equals the bill in dollars. State: 45,563 $ per BEA farm job, 65,417 $ per farm worker; county range 33,022 to 147,643 $ per worker. State compensation per farm wage job by year: 2018 42,607 $, 2019 29,885 $, 2020 46,051 $, 2021 55,839 $, 2022 44,319 $. Proprietors are priced at the hired wage per job (the market price of farm labour in the county) rather than at a non-farm opportunity wage, which would assume away the farm/non-farm gap xi_A is meant to measure. `# VERIFY` the proprietor imputation: a BEA proprietor job is any sole proprietor or partner, many part-time. Contract labour (CoA 101,956,000 $) is left out: its workers are not BEA farm jobs (they are in agricultural support services, non-farm). Census of Agriculture hired labour expense (1,043,118,000 $ in 2022, column `hired_labor_coa_usd`) is 1.29x BEA farm compensation (808,859,000 $) and pays a different universe (every hired head, including workers on the farm under 150 days), so it is a comparison column, not the bill. `# VERIFY` that gap. The previous measure, BEA farm earnings (L370, wages + proprietors' income) per BEA farm job, is kept as `wA_bea_earn_usd`: state 67,854 $, county -16,111 to 219,724 $; it includes owner-operators' returns to owned land and capital, which spec §12.1 pays separately. The loader divides wA_obs_usd by state non-farm earnings per non-farm worker (sum over counties of non-farm earnings / HU = 82,861 $), so both sectors are per head. `# VERIFY` vintage mismatch: CAINC45/CAEMP25N are the 2023-11-16 release, CAINC5N the 2026 file (CAINC5N's revised 2022 farm earnings are 2,924,644,000 $ vs CAINC45 2,739,820,000 $).
- **omega.** Census of Agriculture 2022 owned / (owned + rented from others) acres in farms. State 0.670, county range 0.394 to 0.883.
- **cash_rent_usd_acre.** NASS Cash Rents Survey 2022, non-irrigated cropland. State 66 $/acre.
- **land_value_usd_acre.** Census of Agriculture 2022 estimated market value of land and buildings per acre (NASS does not publish annual county land values). State 4,209 $/acre.
- **gateway.** ACS foreign born who entered 2010 or later per resident worker, relative to the state ratio (mean 1 over workers). `# VERIFY` against spec §12.2 once the arrival block is calibrated. 1 counties have no recent foreign born in the ACS sample (Oneida), so their gateway weight is 0 (log(0) in arrival_shares).
- **kind.** core = the metropolitan county with the most non-farm jobs (Ada); suburb = other counties in a Metropolitan Statistical Area (OMB 2023) (13); rural = the rest (30). `# VERIFY` one core for a multi-metro state.
- **Travel time t (min).** OSRM car durations between 2020 population-weighted county centres, as routed (not symmetrised). Off-diagonal median 292.4 min. Own-county time = 0.5214 x sqrt(land area) at the median effective speed of 57.1 straight-line km/h between counties (median 17.8 to 81.1 min). `# VERIFY` the own-county proxy. `dist` is great-circle km (road/straight median ratio 1.40).

## Suppressed cells and fills

| Variable | County | Rule |
|---|---|---|
| omega | 16079 Shoshone | state owner share |
| omega | 16085 Valley | state owner share |
| cash_rent_usd_acre | 16001 Ada | not published; NASS 'other (combined) counties' value = 29.5 $/acre |
| cash_rent_usd_acre | 16013 Blaine | not published; NASS 'other (combined) counties' value = 29.5 $/acre |
| cash_rent_usd_acre | 16015 Boise | not published; NASS 'other (combined) counties' value = 29.5 $/acre |
| cash_rent_usd_acre | 16019 Bonneville | not published; NASS 'other (combined) counties' value = 29.5 $/acre |
| cash_rent_usd_acre | 16023 Butte | not published; NASS 'other (combined) counties' value = 29.5 $/acre |
| cash_rent_usd_acre | 16025 Camas | not published; NASS 'other (combined) counties' value = 29.5 $/acre |
| cash_rent_usd_acre | 16027 Canyon | not published; NASS 'other (combined) counties' value = 29.5 $/acre |
| cash_rent_usd_acre | 16031 Cassia | not published; NASS 'other (combined) counties' value = 29.5 $/acre |
| cash_rent_usd_acre | 16033 Clark | not published; NASS 'other (combined) counties' value = 29.5 $/acre |
| cash_rent_usd_acre | 16037 Custer | not published; NASS 'other (combined) counties' value = 29.5 $/acre |
| cash_rent_usd_acre | 16041 Franklin | not published; NASS 'other (combined) counties' value = 29.5 $/acre |
| cash_rent_usd_acre | 16045 Gem | not published; NASS 'other (combined) counties' value = 29.5 $/acre |
| cash_rent_usd_acre | 16047 Gooding | not published; NASS 'other (combined) counties' value = 29.5 $/acre |
| cash_rent_usd_acre | 16053 Jerome | not published; NASS 'other (combined) counties' value = 29.5 $/acre |
| cash_rent_usd_acre | 16059 Lemhi | not published; NASS 'other (combined) counties' value = 29.5 $/acre |
| cash_rent_usd_acre | 16063 Lincoln | not published; NASS 'other (combined) counties' value = 29.5 $/acre |
| cash_rent_usd_acre | 16067 Minidoka | not published; NASS 'other (combined) counties' value = 29.5 $/acre |
| cash_rent_usd_acre | 16073 Owyhee | not published; NASS 'other (combined) counties' value = 29.5 $/acre |
| cash_rent_usd_acre | 16075 Payette | not published; NASS 'other (combined) counties' value = 29.5 $/acre |
| cash_rent_usd_acre | 16079 Shoshone | not published; NASS 'other (combined) counties' value = 29.5 $/acre |
| cash_rent_usd_acre | 16083 Twin Falls | not published; NASS 'other (combined) counties' value = 29.5 $/acre |
| cash_rent_usd_acre | 16085 Valley | not published; NASS 'other (combined) counties' value = 29.5 $/acre |
| owned_acres | 16079 Shoshone | (D) in Census of Ag; see fills above |
| owned_acres | 16085 Valley | (D) in Census of Ag; see fills above |
| rented_acres | 16079 Shoshone | (D) in Census of Ag; see fills above |
| rented_acres | 16085 Valley | (D) in Census of Ag; see fills above |

No BEA (D) cells for this state and year: CAEMP25N L50/70/80, CAINC45 L350/360/370 and CAINC5N L82 are published for every county (2018 to 2022 for the farm-wage lines).

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
| 16001 | Ada | core | 252,218 | 273,266 | 1,277 | 22,506 | 188.36M | 53,322 | 39,038 | 0.596 | 30* |
| 16003 | Adams | rural | 1,708 | 974 | 112 | 4,491 | 1.50M | 67,616 | 22,324 | 0.584 | 30 |
| 16005 | Bannock | suburb | 38,777 | 36,395 | 634 | 54,889 | 30.01M | 63,663 | 9,913 | 0.883 | 32 |
| 16007 | Bear Lake | rural | 2,644 | 1,724 | 301 | 29,427 | 2.83M | 65,698 | 31,667 | 0.776 | 32 |
| 16009 | Benewah | rural | 3,734 | 3,734 | 232 | 26,675 | 3.52M | 33,022 | 20,370 | 0.608 | 73 |
| 16011 | Bingham | rural | 21,253 | 14,957 | 1,531 | 159,942 | 17.25M | 77,694 | 55,939 | 0.650 | 29 |
| 16013 | Blaine | rural | 13,268 | 14,152 | 211 | 27,356 | 7.40M | 61,901 | 25,694 | 0.715 | 30* |
| 16015 | Boise | suburb | 3,322 | 2,529 | 84 | 718 | 1.85M | 45,069 | 16,575 | 0.638 | 30* |
| 16017 | Bonner | rural | 19,490 | 17,952 | 505 | 5,360 | 12.45M | 41,494 | -3,199 | 0.834 | 42 |
| 16019 | Bonneville | suburb | 55,030 | 62,941 | 926 | 103,533 | 42.28M | 68,024 | 48,551 | 0.611 | 30* |
| 16021 | Boundary | rural | 4,743 | 3,905 | 291 | 19,541 | 3.24M | 99,329 | 21,088 | 0.621 | 70 |
| 16023 | Butte | suburb | 1,047 | 3,085 | 85 | 32,681 | 3.45M | 115,174 | 67,825 | 0.812 | 30* |
| 16025 | Camas | rural | 465 | 266 | 73 | 36,835 | 0.51M | 147,643 | 92,280 | 0.823 | 30* |
| 16027 | Canyon | suburb | 106,912 | 85,134 | 2,700 | 84,323 | 81.87M | 75,920 | 50,643 | 0.512 | 30* |
| 16029 | Caribou | rural | 3,337 | 3,482 | 413 | 76,397 | 3.22M | 60,996 | 49,683 | 0.782 | 44 |
| 16031 | Cassia | rural | 11,236 | 11,034 | 1,477 | 145,154 | 9.03M | 70,005 | 138,797 | 0.658 | 30* |
| 16033 | Clark | rural | 401 | 306 | 98 | 22,350 | 0.45M | 48,334 | 65,363 | 0.815 | 30* |
| 16035 | Clearwater | rural | 3,299 | 3,160 | 219 | 13,026 | 3.40M | 73,689 | 32,033 | 0.800 | 56 |
| 16037 | Custer | rural | 1,762 | 1,538 | 212 | 18,394 | 1.93M | 60,932 | 43,058 | 0.836 | 30* |
| 16039 | Elmore | rural | 13,077 | 11,699 | 750 | 52,834 | 9.74M | 62,509 | 82,768 | 0.651 | 22 |
| 16041 | Franklin | suburb | 6,423 | 3,708 | 664 | 46,450 | 4.74M | 53,361 | 35,747 | 0.803 | 30* |
| 16043 | Fremont | rural | 5,718 | 3,314 | 458 | 68,080 | 5.52M | 102,612 | 52,182 | 0.701 | 56 |
| 16045 | Gem | suburb | 8,321 | 4,906 | 600 | 11,235 | 6.94M | 58,781 | -6,190 | 0.571 | 30* |
| 16047 | Gooding | rural | 7,018 | 4,717 | 1,410 | 47,326 | 7.27M | 77,911 | 219,724 | 0.699 | 30* |
| 16049 | Idaho | rural | 6,403 | 5,180 | 519 | 81,095 | 7.72M | 60,397 | 29,598 | 0.531 | 76 |
| 16051 | Jefferson | suburb | 14,151 | 8,673 | 763 | 104,832 | 7.56M | 72,861 | 58,856 | 0.705 | 52 |
| 16053 | Jerome | suburb | 11,337 | 9,892 | 1,545 | 72,376 | 8.21M | 53,175 | 126,398 | 0.594 | 30* |
| 16055 | Kootenai | suburb | 80,056 | 73,155 | 607 | 23,273 | 61.35M | 41,539 | 1,787 | 0.688 | 68 |
| 16057 | Latah | rural | 18,879 | 15,483 | 772 | 90,019 | 15.05M | 60,087 | 19,590 | 0.394 | 73 |
| 16059 | Lemhi | rural | 3,273 | 2,983 | 301 | 14,501 | 4.37M | 54,081 | 39,821 | 0.825 | 30* |
| 16061 | Lewis | rural | 1,307 | 1,389 | 154 | 63,529 | 1.67M | 61,267 | 80,609 | 0.497 | 87 |
| 16063 | Lincoln | rural | 2,514 | 1,326 | 421 | 39,155 | 1.67M | 67,271 | 139,381 | 0.767 | 30* |
| 16065 | Madison | rural | 26,209 | 24,958 | 664 | 67,484 | 9.56M | 62,536 | 53,527 | 0.610 | 45 |
| 16067 | Minidoka | rural | 9,867 | 7,890 | 1,184 | 82,728 | 7.77M | 70,584 | 82,464 | 0.456 | 30* |
| 16069 | Nez Perce | suburb | 19,581 | 21,586 | 417 | 79,837 | 25.24M | 54,910 | 46,436 | 0.424 | 83 |
| 16071 | Oneida | rural | 2,145 | 1,336 | 312 | 65,162 | 2.14M | 58,255 | 24,822 | 0.783 | 30 |
| 16073 | Owyhee | suburb | 5,214 | 2,851 | 888 | 59,431 | 4.47M | 61,306 | 85,331 | 0.866 | 30* |
| 16075 | Payette | rural | 10,627 | 7,246 | 755 | 25,318 | 10.02M | 63,515 | 60,978 | 0.511 | 30* |
| 16077 | Power | rural | 3,530 | 3,393 | 757 | 102,523 | 4.37M | 65,297 | 81,120 | 0.634 | 31 |
| 16079 | Shoshone | rural | 5,471 | 4,787 | 25 | 501 | 4.80M | 63,377 | -16,111 | 0.670 | 30* |
| 16081 | Teton | rural | 6,681 | 4,519 | 292 | 36,591 | 2.75M | 49,362 | 29,445 | 0.600 | 26 |
| 16083 | Twin Falls | suburb | 41,514 | 39,743 | 1,886 | 114,804 | 33.87M | 66,796 | 94,522 | 0.712 | 30* |
| 16085 | Valley | rural | 4,848 | 5,722 | 85 | 1,695 | 4.52M | 69,720 | 47,220 | 0.670 | 30* |
| 16087 | Washington | rural | 3,897 | 3,142 | 512 | 30,305 | 5.04M | 47,989 | 18,745 | 0.697 | 55 |
| EXT | External (out-of-state commuting) | external | 21,150 | 40,214 | 1,389 | 111,864 | 16.45M | 65,417 | n/a | 0.670 | n/a |

`*` filled, see above.
