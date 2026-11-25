# Montana 2022 county data: validation report

Built 2026-11-24 by `python -m urqse.data.build_state MT 2022`. 56 counties plus one external zone. Outputs: `county.parquet` (one row per zone, schema in `src/urqse/data/schema.py`) and `travel.npz` (`fips`, `t` minutes, `dist` km, rows in table order).

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
| cdl | USDA NASS Cropland Data Layer 2022, 30 m, clipped to state FIPS 30 | `MT/CDL_2022_30.tif` | 2026-11-24 | https://nassgeodata.gmu.edu/axis2/services/CDLService/GetCDLFile?year=2022&fips=30 |
| acs_b08007 | ACS 2018-2022 5-year, table-based summary file B08007 | `US/acs/acsdt5y2022-b08007.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08007.dat |
| acs_b08604 | ACS 2018-2022 5-year, table-based summary file B08604 | `US/acs/acsdt5y2022-b08604.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b08604.dat |
| acs_b05005 | ACS 2018-2022 5-year, table-based summary file B05005 | `US/acs/acsdt5y2022-b05005.dat` | 2026-11-23 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/5YRData/acsdt5y2022-b05005.dat |
| ghsl_R4_C9 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C9.zip` | 2026-11-24 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C9.zip |
| ghsl_R4_C10 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C10.zip` | 2026-11-23 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C10.zip |
| ghsl_R4_C11 | GHSL GHS-BUILT-V R2023A, epoch 2020, 100 m, Mollweide | `US/ghsl/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C11.zip` | 2026-11-23 | https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_V_GLOBE_R2023A/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_V_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C11.zip |
| nass | Quick Stats bulk economics file `qs.economics_20261121.txt.gz` (Census of Agriculture 2022; Cash Rents Survey 2022) | `qs.economics_20261121.txt.gz` (filtered copy `*_MT.tsv.gz`) | see file | https://www.nass.usda.gov/sites/default/files/datasets/qs.economics_20261121.txt.gz |
| osrm | OSRM public demo server, car profile (OSM data as served on the build date) | `osrm/*.json` (4 cached block requests; the server caps a table at 100 coordinates) | 2026-11-24 | https://router.project-osrm.org/table/v1/driving |

## County sums against published state totals

| Column | Sum of counties | Published state value | Difference |
|---|---|---|---|
| PEP population | 1,122,867 | 1,122,867 | 0.000% |
| ACS workers by residence | 526,969 | 526,969 | 0.000% |
| ACS workers by workplace | 524,574 | 524,574 | 0.000% |
| ACS workers working out of state | 7,645 | 7,645 | 0.000% |
| BEA non-farm employment (L80) | 716,832 | 716,832 | 0.000% |
| BEA farm employment (L70) | 29,362 | 29,362 | 0.000% |
| BEA farm proprietors (L50) | 22,756 | 22,756 | 0.000% |
| BEA farm earnings $ (CAINC45 L370) | 1,016,604,000 | 1,016,604,000 | 0.000% |
| BEA farm wages + supplements $ (CAINC45 L350 + L360) | 294,944,000 | 294,944,000 | 0.000% |
| CoA hired farm labour expense $ | 358,882,000 | 358,883,000 | -0.000% |
| BEA non-farm earnings $ (CAINC5N L82) | 41,564,425,000 | 41,564,425,000 | 0.000% |
| ACS foreign born entered 2010+ | 7,324 | 7,324 | 0.000% |
| CoA owned acres | 39,040,632 | 39,040,632 | 0.000% |
| CoA rented-from-others acres | 18,560,688 | 18,560,688 | 0.000% |
| CoA land in farms, ha | 23,310,427 | 23,310,427 | 0.000% |
| CoA total cropland, ha | 6,503,196 | 6,503,196 | 0.000% |

## Model columns

- **N, HU, HA (jobs = resident workers).** Each county's BEA farm and non-farm job counts are scaled to its ACS count of workers by place of work (scale factor min 0.532, median 0.673, max 0.928; BEA counts jobs, ACS counts people by main job). Sum N = 532,219 = sum HU + HA = 532,219. Farm jobs after scaling: 20,376 (BEA 29,362). `# VERIFY` the scaling: part-time farm proprietors with an off-farm main job are counted once, in proportion to the county mix.
- **External zone.** Residents = out-of-state workers commuting in (ACS workplace total minus in-state residents working in state) = 5,250. Jobs = in-state residents working out of state = 7,645, split by the state farm share (HA = 297). Location: the 22 out-of-state counties within 1 km of the state (16017, 16021, 16033, 16035, 16043, 16049, 16059, 16079, 38011, 38023, 38033, 38053, 38087, 38105, 46019, 46063, 56003, 56005, 56011, 56029, 56033, 56039); travel time from a county to the zone is the OSRM time to the nearest of them. Floor space, farmland, farm labour earnings and owner share are state averages scaled to its workers / farm jobs; gateway weight 0 (immigrants settle in-state). `# VERIFY` all of these are conventions, not data, and `log(0)` in `immigration.arrival_shares` needs handling in M3.
- **TF (farmland, ha).** CDL 2022 crop, hay, fallow and tree-crop classes (codes 1-61, 66-77, 204-254), pixel-centre zonal sums on the 30 m Albers grid. State: 6,718,440 ha vs Census of Agriculture cropland 6,503,196 ha and land in farms 23,310,427 ha; county ratio TF / CoA cropland 0.07 to 1.99. Grassland/pasture (codes 62, 176) is kept separately (`pasture_ha`, 11,504,230 ha). County area covered by CDL pixels: 38,084,196 ha vs land area 37,697,318 ha (the difference is water). `# VERIFY` whether pasture belongs in T^F for livestock counties.
- **L (floor space, m^2).** GHSL GHS-BUILT-V 2020 epoch building volume / 3 m storey height (`# VERIFY` storey height; 2020 is the nearest epoch to 2022). State volume 1.24 km^3.
- **wA_obs_usd (farm labour earnings per farm worker).** Farm compensation (CAINC45 L350 wages and salaries + L360 supplements) per farm wage-and-salary job (CAEMP25N L70 - L50), mean of 2018 to 2022, each year relative to the state's non-farm earnings per non-farm job (CAINC5N L82 / CAEMP25N L80) and put at the 2022 value (57,983 $). That per-job wage prices every BEA farm job, proprietors included, giving the county farm labour bill `farm_labour_bill_usd`; wA_obs_usd = bill / HA, so it is per farm worker (ACS head) and the model's wage bill w_A H_A equals the bill in dollars. State: 48,753 $ per BEA farm job, 70,252 $ per farm worker; county range 18,863 to 113,656 $ per worker. State compensation per farm wage job by year: 2018 42,946 $, 2019 30,197 $, 2020 46,178 $, 2021 56,026 $, 2022 44,648 $. Proprietors are priced at the hired wage per job (the market price of farm labour in the county) rather than at a non-farm opportunity wage, which would assume away the farm/non-farm gap xi_A is meant to measure. `# VERIFY` the proprietor imputation: a BEA proprietor job is any sole proprietor or partner, many part-time. Contract labour (CoA 48,385,000 $) is left out: its workers are not BEA farm jobs (they are in agricultural support services, non-farm). Census of Agriculture hired labour expense (358,883,000 $ in 2022, column `hired_labor_coa_usd`) is 1.22x BEA farm compensation (294,944,000 $) and pays a different universe (every hired head, including workers on the farm under 150 days), so it is a comparison column, not the bill. `# VERIFY` that gap. The previous measure, BEA farm earnings (L370, wages + proprietors' income) per BEA farm job, is kept as `wA_bea_earn_usd`: state 34,623 $, county -17,422 to 164,828 $; it includes owner-operators' returns to owned land and capital, which spec §12.1 pays separately. The loader divides wA_obs_usd by state non-farm earnings per non-farm worker (sum over counties of non-farm earnings / HU = 82,437 $), so both sectors are per head. `# VERIFY` vintage mismatch: CAINC45/CAEMP25N are the 2023-11-16 release, CAINC5N the 2026 file (CAINC5N's revised 2022 farm earnings are 1,271,694,000 $ vs CAINC45 1,016,604,000 $).
- **omega.** Census of Agriculture 2022 owned / (owned + rented from others) acres in farms. State 0.678, county range 0.497 to 0.926.
- **cash_rent_usd_acre.** NASS Cash Rents Survey 2022, non-irrigated cropland. State 31 $/acre.
- **land_value_usd_acre.** Census of Agriculture 2022 estimated market value of land and buildings per acre (NASS does not publish annual county land values). State 1,297 $/acre.
- **gateway.** ACS foreign born who entered 2010 or later per resident worker, relative to the state ratio (mean 1 over workers). `# VERIFY` against spec §12.2 once the arrival block is calibrated. 8 counties have no recent foreign born in the ACS sample (Carter, Fallon, Garfield, Golden Valley, Liberty, McCone, Meagher, Petroleum), so their gateway weight is 0 (log(0) in arrival_shares).
- **kind.** core = the metropolitan county with the most non-farm jobs (Yellowstone); suburb = other counties in a Metropolitan Statistical Area (OMB 2023) (9); rural = the rest (46). `# VERIFY` one core for a multi-metro state.
- **No farm sector** (spec §3.11): 0 counties have no BEA farm jobs.
- **Travel time t (min).** OSRM car durations between 2020 population-weighted county centres, as routed (not symmetrised). Off-diagonal median 331.9 min. Own-county time = 0.5214 x sqrt(land area) at the median effective speed of 59.4 straight-line km/h between counties (median 22.7 to 63.1 min). `# VERIFY` the own-county proxy. `dist` is great-circle km (road/straight median ratio 1.33).

## Suppressed cells and fills

| Variable | County | Rule |
|---|---|---|
| cash_rent_usd_acre | 30001 Beaverhead | not published; NASS 'other (combined) counties' value = 23 $/acre |
| cash_rent_usd_acre | 30023 Deer Lodge | not published; NASS 'other (combined) counties' value = 23 $/acre |
| cash_rent_usd_acre | 30039 Granite | not published; NASS 'other (combined) counties' value = 23 $/acre |
| cash_rent_usd_acre | 30043 Jefferson | not published; NASS 'other (combined) counties' value = 23 $/acre |
| cash_rent_usd_acre | 30047 Lake | not published; NASS 'other (combined) counties' value = 23 $/acre |
| cash_rent_usd_acre | 30049 Lewis and Clark | not published; NASS 'other (combined) counties' value = 23 $/acre |
| cash_rent_usd_acre | 30053 Lincoln | not published; NASS 'other (combined) counties' value = 23 $/acre |
| cash_rent_usd_acre | 30057 Madison | not published; NASS 'other (combined) counties' value = 23 $/acre |
| cash_rent_usd_acre | 30059 Meagher | not published; NASS 'other (combined) counties' value = 23 $/acre |
| cash_rent_usd_acre | 30061 Mineral | not published; NASS 'other (combined) counties' value = 23 $/acre |
| cash_rent_usd_acre | 30063 Missoula | not published; NASS 'other (combined) counties' value = 23 $/acre |
| cash_rent_usd_acre | 30065 Musselshell | not published; NASS 'other (combined) counties' value = 23 $/acre |
| cash_rent_usd_acre | 30069 Petroleum | not published; NASS 'other (combined) counties' value = 23 $/acre |
| cash_rent_usd_acre | 30075 Powder River | not published; NASS 'other (combined) counties' value = 23 $/acre |
| cash_rent_usd_acre | 30077 Powell | not published; NASS 'other (combined) counties' value = 23 $/acre |
| cash_rent_usd_acre | 30087 Rosebud | not published; NASS 'other (combined) counties' value = 23 $/acre |
| cash_rent_usd_acre | 30093 Silver Bow | not published; NASS 'other (combined) counties' value = 23 $/acre |
| cash_rent_usd_acre | 30097 Sweet Grass | not published; NASS 'other (combined) counties' value = 23 $/acre |
| cash_rent_usd_acre | 30103 Treasure | not published; NASS 'other (combined) counties' value = 23 $/acre |
| cash_rent_usd_acre | 30107 Wheatland | not published; NASS 'other (combined) counties' value = 23 $/acre |

No BEA (D) cells for this state and year: CAEMP25N L50/70/80, CAINC45 L350/360/370 and CAINC5N L82 are published for every county (2018 to 2022 for the farm-wage lines).

## Coverage gaps and caveats

- ACS is the 5-year period estimate ending in the base year (no 1-year data for small counties); BEA and PEP are single-year. The external zone inherits ACS sampling error in the commuter totals.
- The Census API now requires a key, so ACS comes from the table-based summary files instead (same estimates).
- LODES (for the M3 PPML of kappa*lambda) and IRS SOI migration flows are not part of this build.
- Census of Agriculture is quinquennial (2022 matches the base year); the cash-rent survey is annual.
- x_km / y_km are NAD83 / UTM (EPSG:26912) at the state's middle longitude, for drawing only.
- No satellite population layer (GHS-POP) is used; census counts drive calibration (spec §8).

## County table

| FIPS | Name | Kind | N | HU | HA | TF ha | L m^2 | wA $/worker | BEA farm earnings $/job | omega | rent $/ac |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 30001 | Beaverhead | rural | 4,559 | 4,026 | 379 | 28,246 | 4.07M | 86,031 | 64,116 | 0.839 | 23* |
| 30003 | Big Horn | rural | 4,664 | 4,338 | 527 | 145,737 | 3.65M | 59,180 | 42,834 | 0.728 | 22 |
| 30005 | Blaine | rural | 2,563 | 1,882 | 519 | 260,982 | 2.19M | 52,702 | 73,082 | 0.692 | 28 |
| 30007 | Broadwater | suburb | 3,138 | 1,787 | 216 | 41,524 | 3.01M | 75,921 | 56,111 | 0.715 | 25 |
| 30009 | Carbon | suburb | 5,137 | 3,243 | 443 | 50,868 | 4.46M | 83,633 | 31,774 | 0.714 | 24 |
| 30011 | Carter | rural | 648 | 387 | 238 | 107,153 | 1.15M | 62,060 | 18,714 | 0.726 | 16 |
| 30013 | Cascade | suburb | 40,313 | 39,853 | 854 | 181,613 | 34.98M | 60,674 | 36,330 | 0.665 | 40 |
| 30015 | Chouteau | rural | 2,495 | 1,362 | 512 | 499,222 | 3.60M | 67,385 | 119,851 | 0.521 | 34 |
| 30017 | Custer | rural | 6,150 | 5,776 | 361 | 77,010 | 6.41M | 62,872 | 4,281 | 0.673 | 18 |
| 30019 | Daniels | rural | 762 | 584 | 224 | 237,045 | 1.29M | 81,461 | 57,161 | 0.523 | 29 |
| 30021 | Dawson | rural | 4,405 | 3,978 | 379 | 180,474 | 3.79M | 48,019 | 26,702 | 0.633 | 27 |
| 30023 | Deer Lodge | rural | 4,088 | 3,847 | 80 | 3,843 | 2.74M | 51,952 | 7,147 | 0.861 | 23* |
| 30025 | Fallon | rural | 1,423 | 1,341 | 219 | 103,911 | 1.71M | 59,650 | 7,553 | 0.694 | 23 |
| 30027 | Fergus | rural | 5,584 | 4,854 | 628 | 270,990 | 6.43M | 62,701 | 5,043 | 0.654 | 32 |
| 30029 | Flathead | rural | 51,262 | 50,991 | 684 | 25,704 | 30.14M | 78,507 | 5,696 | 0.714 | 34 |
| 30031 | Gallatin | suburb | 67,336 | 68,933 | 858 | 82,583 | 33.43M | 73,985 | 34,504 | 0.610 | 40 |
| 30033 | Garfield | rural | 517 | 389 | 201 | 156,436 | 1.12M | 70,596 | 32,851 | 0.694 | 26 |
| 30035 | Glacier | rural | 4,830 | 4,331 | 527 | 183,759 | 3.97M | 48,051 | 81,992 | 0.507 | 28 |
| 30037 | Golden Valley | rural | 377 | 271 | 110 | 53,511 | 0.52M | 83,644 | 26,752 | 0.782 | 19 |
| 30039 | Granite | rural | 1,282 | 1,128 | 114 | 9,169 | 1.36M | 67,424 | 2,629 | 0.730 | 23* |
| 30041 | Hill | rural | 7,348 | 7,210 | 597 | 447,226 | 5.68M | 66,393 | 97,623 | 0.545 | 28 |
| 30043 | Jefferson | suburb | 5,433 | 2,722 | 201 | 11,451 | 3.12M | 98,424 | 5,202 | 0.853 | 23* |
| 30045 | Judith Basin | rural | 971 | 537 | 229 | 130,969 | 1.65M | 86,700 | 70,228 | 0.617 | 29 |
| 30047 | Lake | rural | 12,938 | 10,570 | 805 | 44,727 | 9.54M | 71,883 | 1,007 | 0.778 | 23* |
| 30049 | Lewis and Clark | suburb | 35,944 | 38,349 | 560 | 30,221 | 26.12M | 54,184 | 9,342 | 0.852 | 23* |
| 30051 | Liberty | rural | 743 | 514 | 217 | 223,105 | 1.02M | 66,111 | 164,828 | 0.536 | 28 |
| 30053 | Lincoln | rural | 7,350 | 6,646 | 217 | 254 | 5.72M | 65,693 | -15,700 | 0.779 | 23* |
| 30055 | McCone | rural | 904 | 541 | 284 | 222,716 | 1.44M | 68,202 | 20,151 | 0.636 | 26 |
| 30057 | Madison | rural | 3,962 | 3,713 | 368 | 34,320 | 3.50M | 113,656 | 28,659 | 0.870 | 23* |
| 30059 | Meagher | rural | 1,007 | 695 | 125 | 31,892 | 1.12M | 57,945 | 14,978 | 0.756 | 23* |
| 30061 | Mineral | suburb | 1,890 | 1,151 | 46 | 795 | 1.45M | 18,863 | -17,422 | 0.926 | 23* |
| 30063 | Missoula | suburb | 64,821 | 67,766 | 468 | 6,963 | 43.28M | 88,774 | -315 | 0.922 | 23* |
| 30065 | Musselshell | rural | 1,919 | 1,262 | 216 | 48,761 | 2.23M | 61,046 | 15,090 | 0.726 | 23* |
| 30067 | Park | rural | 8,950 | 6,961 | 407 | 30,020 | 6.12M | 92,764 | 5,394 | 0.813 | 36 |
| 30069 | Petroleum | rural | 235 | 135 | 83 | 49,316 | 0.44M | 60,111 | 36,267 | 0.752 | 23* |
| 30071 | Phillips | rural | 1,866 | 1,355 | 362 | 221,735 | 2.18M | 59,627 | 37,384 | 0.681 | 26 |
| 30073 | Pondera | rural | 2,570 | 1,763 | 396 | 230,118 | 2.96M | 58,698 | 85,709 | 0.624 | 42 |
| 30075 | Powder River | rural | 894 | 654 | 242 | 85,799 | 1.34M | 54,299 | 15,084 | 0.759 | 23* |
| 30077 | Powell | rural | 2,415 | 2,250 | 247 | 14,497 | 3.11M | 53,750 | 21,079 | 0.808 | 23* |
| 30079 | Prairie | rural | 555 | 315 | 124 | 55,686 | 0.78M | 54,923 | 34,847 | 0.840 | 30 |
| 30081 | Ravalli | rural | 19,483 | 14,819 | 890 | 9,080 | 15.31M | 90,571 | 397 | 0.777 | 32 |
| 30083 | Richland | rural | 5,451 | 5,128 | 408 | 185,170 | 5.17M | 84,595 | 59,341 | 0.624 | 32 |
| 30085 | Roosevelt | rural | 3,650 | 3,361 | 445 | 319,886 | 3.56M | 65,581 | 39,943 | 0.542 | 32 |
| 30087 | Rosebud | rural | 3,207 | 3,289 | 391 | 77,875 | 3.03M | 70,462 | 28,763 | 0.710 | 23* |
| 30089 | Sanders | rural | 4,045 | 3,612 | 309 | 10,756 | 4.93M | 87,578 | 1,555 | 0.769 | 22 |
| 30091 | Sheridan | rural | 1,728 | 1,237 | 314 | 269,533 | 2.38M | 70,663 | 10,400 | 0.497 | 40 |
| 30093 | Silver Bow | rural | 16,296 | 16,410 | 100 | 1,243 | 12.69M | 53,763 | -176 | 0.883 | 23* |
| 30095 | Stillwater | suburb | 4,243 | 3,520 | 382 | 81,935 | 3.72M | 77,653 | 16,852 | 0.652 | 19 |
| 30097 | Sweet Grass | rural | 1,793 | 1,710 | 236 | 28,602 | 1.66M | 79,622 | -7,560 | 0.623 | 23* |
| 30099 | Teton | rural | 2,842 | 2,050 | 517 | 215,561 | 3.40M | 70,371 | 58,608 | 0.590 | 42 |
| 30101 | Toole | rural | 2,086 | 2,180 | 323 | 259,430 | 2.62M | 52,969 | 132,825 | 0.540 | 30 |
| 30103 | Treasure | rural | 361 | 206 | 102 | 19,702 | 0.57M | 72,388 | 87,759 | 0.730 | 23* |
| 30105 | Valley | rural | 3,358 | 2,872 | 469 | 349,520 | 3.64M | 61,164 | 71,250 | 0.641 | 30 |
| 30107 | Wheatland | rural | 820 | 636 | 167 | 72,944 | 1.04M | 75,663 | 73,032 | 0.723 | 23* |
| 30109 | Wibaux | rural | 489 | 278 | 102 | 58,061 | 0.61M | 64,046 | 5,708 | 0.616 | 28 |
| 30111 | Yellowstone | core | 82,869 | 84,481 | 953 | 138,797 | 75.40M | 75,329 | 12,379 | 0.744 | 23 |
| EXT | External (out-of-state commuting) | external | 5,250 | 7,348 | 297 | 97,913 | 4.11M | 70,252 | n/a | 0.678 | n/a |

`*` filled, see above.
